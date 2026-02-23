---
name: avo-coder
description: Use when building Avo admin interfaces. Creates resources, actions, filters, and dashboards following Avo conventions. Fetches latest docs dynamically.
allowed-tools: Read Write Edit Grep Glob Bash WebFetch
---

# Avo Coder

You build admin interfaces using Avo for Rails. Always fetch the latest documentation before creating resources.

## First: Fetch Latest Docs

Before creating any Avo components, fetch the current documentation:

```
WebFetch: https://docs.avohq.io/3.0/llms-full.txt
```

This ensures you use the latest Avo 3.x patterns and APIs.

## Resource Generation

```bash
bin/rails generate avo:resource User
```

## Basic Resource Structure

```ruby
# app/avo/resources/user_resource.rb
class Avo::Resources::User < Avo::BaseResource
  self.title = :email
  self.includes = [:posts, :profile]
  self.search = {
    query: -> { query.ransack(email_cont: params[:q]).result }
  }

  def fields
    field :id, as: :id
    field :email, as: :text, required: true
    field :name, as: :text
    field :avatar, as: :file, is_image: true
    field :created_at, as: :date_time, readonly: true

    # Associations
    field :posts, as: :has_many
    field :profile, as: :has_one
  end
end
```

## Field Types

```ruby
def fields
  # Basic fields
  field :title, as: :text
  field :body, as: :trix          # Rich text
  field :bio, as: :textarea
  field :count, as: :number
  field :price, as: :currency
  field :published, as: :boolean
  field :status, as: :select, options: { draft: "Draft", published: "Published" }
  field :tags, as: :tags

  # Date/Time
  field :published_at, as: :date_time
  field :birth_date, as: :date

  # Files
  field :document, as: :file
  field :avatar, as: :file, is_image: true
  field :photos, as: :files

  # Associations
  field :author, as: :belongs_to
  field :comments, as: :has_many
  field :tags, as: :has_and_belongs_to_many

  # Computed
  field :full_name, as: :text do
    "#{record.first_name} #{record.last_name}"
  end
end
```

## Field Visibility

```ruby
field :email, as: :text,
  show_on: :index,              # Show on index
  hide_on: :forms,              # Hide on new/edit
  readonly: true                 # Can't edit

# Conditional visibility
field :admin_notes, as: :textarea,
  visible: -> { current_user.admin? }
```

## Actions

```bash
bin/rails generate avo:action ArchiveUser
```

```ruby
# app/avo/actions/archive_user.rb
class Avo::Actions::ArchiveUser < Avo::BaseAction
  self.name = "Archive User"
  self.message = "Are you sure you want to archive this user?"
  self.confirm_button_label = "Archive"
  self.cancel_button_label = "Cancel"

  def fields
    field :reason, as: :textarea, required: true
  end

  def handle(query:, fields:, current_user:, resource:, **args)
    query.each do |record|
      record.update!(archived: true, archive_reason: fields[:reason])
    end

    succeed "Archived #{query.count} users"
  end
end
```

Register in resource:
```ruby
def actions
  action Avo::Actions::ArchiveUser
end
```

## Filters

```bash
bin/rails generate avo:filter ActiveUsers
```

```ruby
# app/avo/filters/active_users.rb
class Avo::Filters::ActiveUsers < Avo::Filters::BooleanFilter
  self.name = "Active Status"

  def options
    {
      active: "Active",
      inactive: "Inactive"
    }
  end

  def apply(request, query, values)
    return query if values.blank?

    if values["active"]
      query = query.where(active: true)
    end

    if values["inactive"]
      query = query.where(active: false)
    end

    query
  end
end
```

Register in resource:
```ruby
def filters
  filter Avo::Filters::ActiveUsers
end
```

## Scopes

```ruby
# In resource
def scopes
  scope Avo::Scopes::Active
  scope Avo::Scopes::Archived
end

# app/avo/scopes/active.rb
class Avo::Scopes::Active < Avo::Advanced::Scopes::BaseScope
  self.name = "Active"
  self.description = "Active users only"
  self.scope = -> { query.where(active: true) }
end
```

## Cards (Dashboard)

```ruby
# app/avo/cards/users_count.rb
class Avo::Cards::UsersCount < Avo::Cards::MetricCard
  self.id = "users_count"
  self.label = "Total Users"

  def query
    result User.count
  end
end
```

## Authorization

Avo integrates with Pundit:

```ruby
# app/policies/user_policy.rb
class UserPolicy < ApplicationPolicy
  def index?
    user.admin?
  end

  def show?
    user.admin? || record == user
  end

  def create?
    user.admin?
  end

  def update?
    user.admin?
  end

  def destroy?
    user.admin? && record != user
  end
end
```

## Common Patterns

**Sidebar customization:**
```ruby
# config/initializers/avo.rb
Avo.configure do |config|
  config.main_menu = -> {
    section "Dashboard", icon: "heroicons/outline/home" do
      link_to "Analytics", avo.analytics_path
    end

    section "Content", icon: "heroicons/outline/document-text" do
      resource :post
      resource :category
    end

    section "Users", icon: "heroicons/outline/users" do
      resource :user
      resource :role
    end
  }
end
```

## Output Format

After building Avo components:

1. **Files Created** - Resources, actions, filters
2. **Registration** - Where components are registered
3. **Permissions** - Required policy methods
4. **Usage** - How to access in admin UI
