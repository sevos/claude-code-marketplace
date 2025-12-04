# Controller Patterns

## Directory Structure

```
app/controllers/
├── application_controller.rb
├── concerns/
│   ├── authentication.rb
│   ├── authorization.rb
│   ├── board_scoped.rb
│   ├── card_scoped.rb
│   └── filter_scoped.rb
├── boards_controller.rb
├── cards_controller.rb
├── boards/
│   └── columns_controller.rb
└── cards/
    ├── comments_controller.rb
    └── closures_controller.rb
```

## ApplicationController

Keep it minimal, delegate to concerns:

```ruby
class ApplicationController < ActionController::Base
  include Authentication
  include Authorization
  include CurrentRequest, CurrentTimezone
  include TurboFlash

  etag { "v1" }
  allow_browser versions: :modern
end
```

## Controller Concerns

### Resource Scoping Concerns

```ruby
module BoardScoped
  extend ActiveSupport::Concern

  included do
    before_action :set_board
  end

  private
    def set_board
      @board = Current.user.boards.find(params[:board_id])
    end

    def ensure_permission_to_admin_board
      head :forbidden unless Current.user.can_administer_board?(@board)
    end
end
```

```ruby
module CardScoped
  extend ActiveSupport::Concern

  included do
    before_action :set_card, :set_board
  end

  private
    def set_card
      @card = Current.user.accessible_cards.find_by!(number: params[:card_id])
    end

    def set_board
      @board = @card.board
    end

    def render_card_replacement
      render turbo_stream: turbo_stream.replace(
        [@card, :card_container],
        partial: "cards/container",
        method: :morph,
        locals: { card: @card.reload }
      )
    end
end
```

### Request Context Concern

```ruby
module CurrentRequest
  extend ActiveSupport::Concern

  included do
    before_action do
      Current.http_method = request.method
      Current.request_id  = request.uuid
      Current.user_agent  = request.user_agent
      Current.ip_address  = request.ip
    end
  end
end
```

### Turbo Flash Concern

```ruby
module TurboFlash
  extend ActiveSupport::Concern

  included do
    helper_method :turbo_stream_flash
  end

  private
    def turbo_stream_flash(**flash_options)
      turbo_stream.replace(:flash, partial: "layouts/shared/flash", locals: { flash: flash_options })
    end
end
```

## Resource Controllers

### Minimal CRUD Pattern

```ruby
class BoardsController < ApplicationController
  before_action :set_board, except: %i[new create]
  before_action :ensure_permission_to_admin_board, only: %i[update]

  def show
    # Render view
  end

  def new
    @board = Board.new
  end

  def create
    @board = Board.create!(board_params.with_defaults(all_access: true))
    redirect_to board_path(@board)
  end

  def edit
    # Prepare data for form
  end

  def update
    @board.update!(board_params)
    redirect_to edit_board_path(@board), notice: "Saved"
  end

  def destroy
    @board.destroy
    redirect_to root_path
  end

  private
    def set_board
      @board = Current.user.boards.find(params[:id])
    end

    def board_params
      params.expect(board: [:name, :all_access, :auto_postpone_period])
    end
end
```

### Bang Methods for Fail-Fast

Always use bang methods (`create!`, `update!`) - let Rails handle exceptions:

```ruby
def create
  @card = Card.create!(card_params)  # Raises on validation failure
  redirect_to @card
end

def update
  @card.update!(card_params)  # Raises on validation failure
  render_card_replacement
end
```

## Strong Parameters

Use `params.expect()` for strict parameter validation:

```ruby
# Simple case
def email_address
  params.expect(:email_address)
end

# Nested hash
def board_params
  params.expect(board: [:name, :all_access, :public_description])
end

# With arrays
def card_params
  params.expect(card: [:title, :description, tag_ids: []])
end

# Complex nested params
def webhook_params
  params.expect(webhook: [:name, :url, subscribed_actions: []])
        .merge(board_id: @board.id)
end
```

## Nested Resource Controllers

```ruby
class Cards::CommentsController < ApplicationController
  include CardScoped

  before_action :set_comment, only: %i[show edit update destroy]
  before_action :ensure_creatorship, only: %i[edit update destroy]

  def create
    @comment = @card.comments.create!(comment_params)
    # Turbo Stream response
  end

  def update
    @comment.update!(comment_params)
  end

  def destroy
    @comment.destroy
  end

  private
    def set_comment
      @comment = @card.comments.find(params[:id])
    end

    def ensure_creatorship
      head :forbidden if Current.user != @comment.creator
    end

    def comment_params
      params.expect(comment: :body)
    end
end
```

## State Machine Controllers

Instead of traditional actions, create controllers for state transitions:

```ruby
class Cards::ClosuresController < ApplicationController
  include CardScoped

  def create
    @card.close(user: Current.user)
    render_card_replacement
  end

  def destroy
    @card.reopen(user: Current.user)
    render_card_replacement
  end
end

class Cards::NotNowsController < ApplicationController
  include CardScoped

  def create
    @card.postpone
    render_card_replacement
  end
end
```

## Authorization in Controllers

### Permission Checks

```ruby
def ensure_admin
  head :forbidden unless Current.user.admin?
end

def ensure_permission_to_admin_board
  head :forbidden unless Current.user.can_administer_board?(@board)
end

def ensure_creatorship
  head :forbidden if Current.user != @comment.creator
end
```

### Conditional Redirects

```ruby
def update
  @board.update!(board_params)

  if @board.accessible_to?(Current.user)
    redirect_to edit_board_path(@board), notice: "Saved"
  else
    redirect_to root_path, notice: "Saved (you were removed from the board)"
  end
end
```

## Response Formats

### Turbo Stream Responses

```ruby
def create
  @comment = @card.comments.create!(comment_params)

  render turbo_stream: [
    turbo_stream.before([@card, :new_comment], partial: "cards/comments/comment", locals: { comment: @comment }),
    turbo_stream.update([@card, :new_comment], partial: "cards/comments/new", locals: { card: @card })
  ]
end
```

### Multiple Response Formats

```ruby
def index
  @notifications = Current.user.notifications.ordered.preloaded

  respond_to do |format|
    format.turbo_stream if current_page_param
    format.html
  end
end
```

### Rendering with Morph

```ruby
def render_card_replacement
  render turbo_stream: turbo_stream.replace(
    [@card, :card_container],
    partial: "cards/container",
    method: :morph,
    locals: { card: @card.reload }
  )
end
```

## ETags and Caching

```ruby
class ApplicationController < ActionController::Base
  etag { "v1" }
  etag { Current.session.id if authenticated? }
end

# In actions
def show
  fresh_when etag: @card
end

def index
  fresh_when etag: @page.records
end
```

## Public/Unauthenticated Controllers

```ruby
class Public::BaseController < ApplicationController
  allow_unauthenticated_access

  before_action :set_board, :set_public_cache_expiration

  layout "public"

  private
    def set_board
      @board = Board.find_by_published_key(params[:board_id])
    end

    def set_public_cache_expiration
      expires_in 30.seconds, public: true
    end
end
```

## Admin Controllers

```ruby
class AdminController < ApplicationController
  disallow_account_scope
  before_action :ensure_staff
end

class Account::SettingsController < ApplicationController
  before_action :ensure_admin, only: :update
end
```

## Rate Limiting

```ruby
class SessionsController < ApplicationController
  rate_limit to: 10, within: 3.minutes, only: :create,
             with: -> { redirect_to new_session_path, alert: "Try again later." }
end
```

## Class-Level Authentication Control

```ruby
class SessionsController < ApplicationController
  disallow_account_scope                    # Works outside account context
  require_unauthenticated_access except: :destroy  # Redirect if already signed in

  def new
    # Login form
  end

  def destroy
    terminate_session
    redirect_to root_path
  end
end
```

## URL Helpers with Multi-Tenancy

URLs automatically include account slug via middleware. No special handling needed in controllers:

```ruby
redirect_to board_path(@board)  # Generates /12345/boards/abc
redirect_to root_path           # Generates /12345/
```

For routes outside account scope:

```ruby
redirect_to session_menu_url(script_name: nil)  # Generates /session/menu
```
