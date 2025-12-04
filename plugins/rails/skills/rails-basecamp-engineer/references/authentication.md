# Authentication Patterns

## Architecture Overview

The authentication system separates global identity from account-specific users:

- **Identity**: Global user record (email-based), can belong to multiple accounts
- **User**: Account-specific membership with roles
- **Session**: Active login session tied to Identity

```
Identity (email: david@example.com)
  ├── User (Account: Basecamp, role: owner)
  ├── User (Account: Hey, role: admin)
  └── Session (device: Chrome on Mac)
```

## Models

### Identity Model

```ruby
class Identity < ApplicationRecord
  has_many :magic_links, dependent: :destroy
  has_many :sessions, dependent: :destroy
  has_many :users, dependent: :nullify
  has_many :accounts, through: :users

  normalizes :email_address, with: ->(value) { value.strip.downcase.presence }

  def send_magic_link(purpose: :sign_in)
    magic_links.create!(purpose: purpose).tap do |link|
      MagicLinkMailer.send("#{purpose}_instructions", link).deliver_later
    end
  end
end
```

### Session Model

```ruby
class Session < ApplicationRecord
  belongs_to :identity

  # Stores user_agent and ip_address for device tracking
end
```

### User Model

```ruby
class User < ApplicationRecord
  belongs_to :account
  belongs_to :identity, optional: true

  enum :role, %i[owner admin member system].index_by(&:itself)

  def admin?
    super || owner?  # Owner implicitly has admin permissions
  end
end
```

## Passwordless Magic Link Authentication

### Magic Link Model

```ruby
class MagicLink < ApplicationRecord
  CODE_LENGTH = 6
  EXPIRATION_TIME = 15.minutes

  belongs_to :identity
  enum :purpose, %w[sign_in sign_up], prefix: :for, default: :sign_in

  scope :active, -> { where(expires_at: Time.current...) }
  scope :stale, -> { where(expires_at: ..Time.current) }

  before_create do
    self.code = Code.generate(CODE_LENGTH)
    self.expires_at = EXPIRATION_TIME.from_now
  end

  def self.consume(code)
    active.find_by(code: Code.sanitize(code))&.consume
  end

  def consume
    destroy  # One-time use
    self
  end
end
```

### Code Generation

```ruby
module MagicLink::Code
  CODE_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ".chars.freeze
  CODE_SUBSTITUTIONS = { "O" => "0", "I" => "1", "L" => "1" }.freeze

  def self.generate(length = 6)
    length.times.map { CODE_ALPHABET.sample }.join
  end

  def self.sanitize(code)
    code.to_s
        .upcase
        .gsub(/[#{CODE_SUBSTITUTIONS.keys.join}]/, CODE_SUBSTITUTIONS)
        .gsub(/[^#{CODE_ALPHABET.join}]/, "")
  end
end
```

### Authentication Controller Concern

```ruby
module Authentication
  extend ActiveSupport::Concern

  included do
    before_action :require_account
    before_action :require_authentication
    helper_method :authenticated?
  end

  class_methods do
    def require_unauthenticated_access(**options)
      allow_unauthenticated_access(**options)
      before_action :redirect_authenticated_user, **options
    end

    def allow_unauthenticated_access(**options)
      skip_before_action :require_authentication, **options
      before_action :resume_session, **options
    end

    def disallow_account_scope(**options)
      skip_before_action :require_account, **options
    end
  end

  private
    def authenticated?
      Current.session.present?
    end

    def require_account
      redirect_to session_menu_url(script_name: nil) unless Current.account.present?
    end

    def require_authentication
      resume_session || request_authentication
    end

    def resume_session
      if session = find_session_by_cookie
        set_current_session(session)
      end
    end

    def find_session_by_cookie
      Session.find_signed(cookies.signed[:session_token])
    end

    def start_new_session_for(identity)
      identity.sessions.create!(
        user_agent: request.user_agent,
        ip_address: request.remote_ip
      ).tap { |session| set_current_session(session) }
    end

    def set_current_session(session)
      Current.session = session
      cookies.signed.permanent[:session_token] = {
        value: session.signed_id,
        httponly: true,
        same_site: :lax
      }
    end

    def terminate_session
      Current.session.destroy
      cookies.delete(:session_token)
    end

    def request_authentication
      session[:return_to_after_authenticating] = request.url if Current.account.present?
      redirect_to new_session_path(script_name: nil)
    end

    def after_authentication_url
      session.delete(:return_to_after_authenticating) || landing_url
    end
end
```

### Sessions Controller

```ruby
class SessionsController < ApplicationController
  disallow_account_scope
  require_unauthenticated_access except: :destroy
  rate_limit to: 10, within: 3.minutes, only: :create

  layout "public"

  def new
    # Show email entry form
  end

  def create
    if identity = Identity.find_by_email_address(params[:email_address])
      identity.send_magic_link
    end
    redirect_to session_magic_link_path
  end

  def destroy
    terminate_session
    redirect_to new_session_path
  end
end
```

### Magic Link Redemption Controller

```ruby
class Sessions::MagicLinksController < ApplicationController
  disallow_account_scope
  require_unauthenticated_access
  rate_limit to: 10, within: 15.minutes, only: :create

  def show
    # Display code entry form
  end

  def create
    if magic_link = MagicLink.consume(params[:code])
      start_new_session_for(magic_link.identity)
      redirect_to after_sign_in_url(magic_link)
    else
      redirect_to session_magic_link_path, alert: "Try another code."
    end
  end

  private
    def after_sign_in_url(magic_link)
      magic_link.for_sign_up? ? new_signup_completion_path : after_authentication_url
    end
end
```

## Traditional Password Authentication

To add password authentication alongside magic links:

### Migration

```ruby
class AddPasswordToIdentities < ActiveRecord::Migration[8.0]
  def change
    add_column :identities, :password_digest, :string
  end
end
```

### Identity Model Addition

```ruby
class Identity < ApplicationRecord
  has_secure_password validations: false

  def authenticate_password(password)
    password_digest.present? && authenticate(password)
  end
end
```

### Password Sessions Controller

```ruby
class Sessions::PasswordsController < ApplicationController
  disallow_account_scope
  require_unauthenticated_access
  rate_limit to: 10, within: 3.minutes, only: :create

  def new
    # Show email + password form
  end

  def create
    if identity = Identity.find_by_email_address(params[:email_address])
      if identity.authenticate_password(params[:password])
        start_new_session_for(identity)
        redirect_to after_authentication_url
        return
      end
    end

    redirect_to new_session_password_path, alert: "Invalid email or password"
  end
end
```

## Account Menu (Multi-Account Selection)

```ruby
class Sessions::MenusController < ApplicationController
  disallow_account_scope

  def show
    @accounts = Current.identity.accounts

    # Auto-redirect if only one account
    if @accounts.one?
      redirect_to root_url(script_name: @accounts.first.slug)
    end
  end
end
```

## Session Security Features

1. **Signed Cookies**: Rails cryptographic signing prevents tampering
2. **HTTPOnly**: JavaScript cannot access session tokens
3. **SameSite=Lax**: CSRF protection
4. **One-Time Links**: Magic links consumed on use
5. **Short Expiration**: 15-minute window for magic links
6. **Rate Limiting**: Prevents brute force attacks
7. **Device Tracking**: User agent and IP stored per session

## Request Flow

```
1. User visits /session/new
2. User enters email → POST /session
3. MagicLink created, email sent
4. Redirect to /session/magic_link (code entry form)
5. User enters code → POST /session/magic_link
6. MagicLink.consume(code) finds and destroys link
7. start_new_session_for(identity) creates Session
8. Signed cookie set with session.signed_id
9. Redirect to account menu or dashboard
10. Future requests: resume_session reads cookie
```

## Testing Authentication

```ruby
def sign_in_as(identity)
  identity = identities(identity) unless identity.is_a?(Identity)

  identity.send_magic_link
  magic_link = identity.magic_links.last

  untenanted do
    post session_magic_link_url, params: { code: magic_link.code }
  end

  assert_response :redirect
  assert cookies[:session_token].present?
end

def with_current_user(user)
  old_session = Current.session
  Current.session = Session.new(identity: user.identity)
  yield
ensure
  Current.session = old_session
end
```
