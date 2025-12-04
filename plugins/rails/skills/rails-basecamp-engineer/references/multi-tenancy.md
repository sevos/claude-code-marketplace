# Multi-Tenancy Patterns

This document covers two approaches to multi-tenancy:
1. **URL Path-Based** (shared database) - Fizzy/Basecamp pattern
2. **Subdomain-Based** (database per tenant) - Using activerecord-tenanted gem

## Approach 1: URL Path-Based Multi-Tenancy

### Overview

- Single shared database with `account_id` on all tenant tables
- Account ID extracted from URL path: `/{account_id}/boards/...`
- Middleware moves slug to `SCRIPT_NAME`, making Rails think it's "mounted" at that path
- All queries filtered by `account_id`

### Account Slug Middleware

```ruby
# config/initializers/tenanting/account_slug.rb
module AccountSlug
  PATTERN = /(\d{7,})/
  FORMAT = "%07d"
  PATH_INFO_MATCH = /\A(\/#{PATTERN})/

  def self.decode(slug) slug.to_i end
  def self.encode(id) FORMAT % id end

  class Extractor
    def initialize(app)
      @app = app
    end

    def call(env)
      request = ActionDispatch::Request.new(env)

      # Extract account ID from URL path
      if request.path_info =~ PATH_INFO_MATCH
        # Move slug from PATH_INFO to SCRIPT_NAME
        request.engine_script_name = request.script_name = $1
        request.path_info = $'.empty? ? "/" : $'

        env["app.external_account_id"] = AccountSlug.decode($2)
      end

      if env["app.external_account_id"]
        account = Account.find_by(external_account_id: env["app.external_account_id"])
        Current.with_account(account) { @app.call(env) }
      else
        Current.without_account { @app.call(env) }
      end
    end
  end
end

# Insert after Rack middleware
Rails.application.config.middleware.insert_after Rack::TempfileReaper, AccountSlug::Extractor
```

### CurrentAttributes

```ruby
class Current < ActiveSupport::CurrentAttributes
  attribute :session, :user, :account
  attribute :request_id, :user_agent, :ip_address

  delegate :identity, to: :session, allow_nil: true

  def session=(value)
    super(value)
    if value.present? && account.present?
      self.user = identity.users.find_by(account: account)
    end
  end

  def with_account(value, &block)
    with(account: value, &block)
  end

  def without_account(&block)
    with(account: nil, &block)
  end
end
```

### Model Scoping via Defaults

All models derive `account_id` from associations:

```ruby
class Board < ApplicationRecord
  belongs_to :creator, class_name: "User", default: -> { Current.user }
  belongs_to :account, default: -> { creator.account }
end

class Card < ApplicationRecord
  belongs_to :account, default: -> { board.account }
  belongs_to :board
end

class Comment < ApplicationRecord
  belongs_to :account, default: -> { card.account }
  belongs_to :card, touch: true
end

# For top-level models without a parent
class Tag < ApplicationRecord
  belongs_to :account, default: -> { Current.account }
end
```

### Account Model

```ruby
class Account < ApplicationRecord
  has_many :users, dependent: :destroy
  has_many :boards, dependent: :destroy
  has_many :cards, dependent: :destroy

  before_create :assign_external_account_id

  def slug
    "/#{external_account_id}"
  end

  private
    def assign_external_account_id
      self.external_account_id ||= ExternalIdSequence.next
    end
end
```

### Background Job Context Preservation

```ruby
# config/initializers/active_job.rb
module TenantedActiveJobExtensions
  extend ActiveSupport::Concern

  prepended do
    attr_reader :account
    self.enqueue_after_transaction_commit = true
  end

  def initialize(...)
    super
    @account = Current.account
  end

  def serialize
    super.merge({ "account" => @account&.to_gid })
  end

  def deserialize(job_data)
    super
    if _account = job_data.fetch("account", nil)
      @account = GlobalID::Locator.locate(_account)
    end
  end

  def perform_now
    if account.present?
      Current.with_account(account) { super }
    else
      super
    end
  end
end

ActiveSupport.on_load(:active_job) do
  prepend TenantedActiveJobExtensions
end
```

### ActionCable Multi-Tenancy

```ruby
# app/channels/application_cable/connection.rb
module ApplicationCable
  class Connection < ActionCable::Connection::Base
    identified_by :current_user

    def connect
      set_current_user || reject_unauthorized_connection
    end

    private
      def set_current_user
        if session = find_session_by_cookie
          account = Account.find_by(external_account_id: request.env["app.external_account_id"])
          Current.account = account
          self.current_user = session.identity.users.find_by!(account: account) if account
        end
      end
  end
end
```

### Turbo Streams with Multi-Tenancy

```ruby
# config/initializers/tenanting/turbo.rb
module TurboStreamsJobExtensions
  extend ActiveSupport::Concern

  class_methods do
    def render_format(format, **rendering)
      if Current.account.present?
        ApplicationController.renderer.new(
          script_name: Current.account.slug
        ).render(formats: [format], **rendering)
      else
        super
      end
    end
  end
end

Rails.application.config.after_initialize do
  Turbo::StreamsChannel.prepend TurboStreamsJobExtensions
end
```

---

## Approach 2: Subdomain-Based Multi-Tenancy

### Overview

- Uses `activerecord-tenanted` gem
- Each tenant has its own database
- Tenant identified by subdomain
- Automatic query scoping via model inheritance

### Setup

```ruby
# Gemfile
gem "activerecord-tenanted", "~> 0.5.0"
```

### Configuration

```ruby
# config/initializers/tenancy.rb
Rails.application.configure do
  config.active_record_tenanted.tenant_resolver = ->(request) {
    TenantNameValidator.resolve(request.subdomain)
  }
  config.active_record_tenanted.default_tenant = Rails.env.local? ? "dev" : nil
  config.active_record_tenanted.connection_class = "AccountRecord"
end
```

### Database Configuration

```yaml
# config/database.yml
default: &default
  adapter: sqlite3
  pool: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>
  timeout: 5000

development:
  primary:
    <<: *default
    database: storage/development/primary.sqlite3
  account:
    <<: *default
    database: storage/development/account/%{tenant_id}.sqlite3
    migrations_paths: db/account_migrate
```

### Base Models

```ruby
# app/models/application_record.rb
class ApplicationRecord < ActiveRecord::Base
  primary_abstract_class
  # For shared/global data
end

# app/models/account_record.rb
class AccountRecord < ActiveRecord::Base
  self.abstract_class = true
  tenanted "account"  # Specifies tenant database
end
```

### Account Model with Database Lifecycle

```ruby
class Account < ApplicationRecord
  include WithDatabase

  validates :tenant_id, presence: true, uniqueness: true,
            format: { with: /\A[a-z0-9-]+\z/ }
end

module Account::WithDatabase
  extend ActiveSupport::Concern

  included do
    after_create :create_tenant_database
    after_destroy :destroy_tenant_database
  end

  private
    def create_tenant_database
      AccountRecord.create_tenant(tenant_id)
    end

    def destroy_tenant_database
      AccountRecord.destroy_tenant(tenant_id)
    end
end
```

### Tenant Models

```ruby
class User < AccountRecord
  # Automatically scoped to current tenant database
end

class Reflection < AccountRecord
  belongs_to :user
end
```

### Current Context

```ruby
class Current < ActiveSupport::CurrentAttributes
  attribute :session, :account

  delegate :user, to: :session, allow_nil: true

  def account
    super || self.account = Account.find_by(tenant_id: AccountRecord.current_tenant)
  end
end
```

### Controller Concern

```ruby
module Tenancy
  extend ActiveSupport::Concern

  included do
    helper_method :current_tenant
  end

  def current_tenant
    AccountRecord.current_tenant
  end
end
```

### Background Jobs

Jobs must manually pass and restore tenant context:

```ruby
class UpdateStateJob < ApplicationJob
  def perform(tenant_id, user_id)
    AccountRecord.with_tenant(tenant_id) do
      user = User.find(user_id)
      user.update_state
    end
  end
end

# Enqueuing
UpdateStateJob.perform_later(AccountRecord.current_tenant, user.id)
```

### ActionCable

```ruby
module ApplicationCable
  class Connection < ActiveRecord::Tenanted::CableConnection::Base
    identified_by :current_user

    def connect
      AccountRecord.with_tenant(tenant_id) do
        self.current_user = find_verified_user
      end
    end
  end
end
```

---

## Comparison

| Aspect | URL Path-Based | Subdomain-Based |
|--------|----------------|-----------------|
| Database | Shared, account_id filtering | Separate per tenant |
| Isolation | Row-level | Database-level |
| Query Scoping | Manual (default lambdas) | Automatic (inheritance) |
| Job Context | Automatic (extensions) | Manual (parameter) |
| Gem | None (custom) | activerecord-tenanted |
| URL Format | `/123456/boards` | `tenant.app.com/boards` |
| Scaling | Horizontal (row filtering) | Horizontal (database sharding) |
| Dev Setup | Simple (one database) | Complex (manage N databases) |

## Testing Multi-Tenancy

### URL Path-Based

```ruby
class ActionDispatch::IntegrationTest
  setup do
    integration_session.default_url_options[:script_name] =
      "/#{ActiveRecord::FixtureSet.identify("37signals")}"
  end
end

def untenanted(&block)
  original = integration_session.default_url_options[:script_name]
  integration_session.default_url_options[:script_name] = ""
  yield
ensure
  integration_session.default_url_options[:script_name] = original
end
```

### Subdomain-Based

```ruby
class ActionDispatch::IntegrationTest
  setup do
    host! "dev.app.localhost"
  end
end

def with_tenant(tenant_id, &block)
  AccountRecord.with_tenant(tenant_id, &block)
end
```
