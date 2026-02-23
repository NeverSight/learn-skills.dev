---
name: action-policy-coder
description: Use proactively for authorization with ActionPolicy. Creates policies, scopes, and integrates with GraphQL/ActionCable. Preferred over Pundit for composable, cacheable authorization.
allowed-tools: Read Write Edit Grep Glob Bash WebFetch
---

# ActionPolicy Coder

## When Invoked

1. **Create policy classes** with proper rules and inheritance
2. **Implement authorization** in controllers with `authorize!` and `allowed_to?`
3. **Set up scoping** with `authorized_scope` for filtered collections
4. **Configure caching** for performance optimization
5. **Add I18n** for localized failure messages
6. **Write tests** using ActionPolicy RSpec matchers
7. **Integrate** with GraphQL and ActionCable

## Installation

```ruby
# Gemfile
gem "action_policy"
gem "action_policy-graphql"  # For GraphQL integration

# Generate base policy
bin/rails generate action_policy:install
bin/rails generate action_policy:policy Post
```

## Policy Classes

### ApplicationPolicy Base

```ruby
# app/policies/application_policy.rb
class ApplicationPolicy < ActionPolicy::Base
  alias_rule :edit?, :destroy?, to: :update?
  pre_check :allow_admins

  private

  def allow_admins
    allow! if user.admin?
  end
end
```

### Resource Policy

```ruby
# app/policies/post_policy.rb
class PostPolicy < ApplicationPolicy
  def index? = true
  def show? = true
  def update? = owner?
  def destroy? = owner? && !record.published?
  def publish? = owner? && record.draft?

  private

  def owner? = user.id == record.user_id
end
```

## Controller Integration

```ruby
class PostsController < ApplicationController
  def show
    @post = Post.find(params[:id])
    authorize! @post
  end

  def update
    @post = Post.find(params[:id])
    authorize! @post
    @post.update(post_params) ? redirect_to(@post) : render(:edit)
  end

  def publish
    @post = Post.find(params[:id])
    authorize! @post, to: :publish?
    @post.publish!
    redirect_to @post
  end
end
```

### Conditional Rendering

```erb
<% if allowed_to?(:edit?, @post) %>
  <%= link_to "Edit", edit_post_path(@post) %>
<% end %>
```

## Policy Scoping

```ruby
class PostPolicy < ApplicationPolicy
  relation_scope do |relation|
    user.admin? ? relation.all : relation.where(user_id: user.id).or(relation.published)
  end

  relation_scope(:own) { |relation| relation.where(user_id: user.id) }
  relation_scope(:drafts) { |relation| relation.where(user_id: user.id, status: :draft) }
end

# Controller usage
@posts = authorized_scope(Post.all)
@drafts = authorized_scope(Post.all, type: :relation, as: :drafts)
```

## Caching

```ruby
class PostPolicy < ApplicationPolicy
  def update?
    cache { owner_or_collaborator? }  # Cache expensive checks
  end
end

# config/initializers/action_policy.rb
ActionPolicy.configure do |config|
  config.cache_store = Rails.cache
end
```

## I18n Failure Messages

```yaml
# config/locales/action_policy.en.yml
en:
  action_policy:
    policy:
      post_policy:
        update?: "You can only edit your own posts"
        destroy?: "You cannot delete a published post"
```

```ruby
class ApplicationController < ActionController::Base
  rescue_from ActionPolicy::Unauthorized do |exception|
    flash[:alert] = exception.result.message
    redirect_back fallback_location: root_path
  end
end
```

## Deliverables

When implementing authorization, provide:

1. **Policy Classes**: With rules, scopes, and caching
2. **Controller Integration**: authorize! and allowed_to? usage
3. **Scoping**: For index actions and filtered collections
4. **I18n**: Localized error messages
5. **Tests**: RSpec policy and request specs
6. **GraphQL**: preauthorize for mutations if applicable
