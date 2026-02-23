---
name: ruby-coder
description: This skill guides writing of new Ruby code following modern Ruby 3.x syntax, Sandi Metz's 4 Rules for Developers, and idiomatic Ruby best practices. Use when creating new Ruby files, writing Ruby methods, or refactoring Ruby code to ensure adherence to clarity, simplicity, and maintainability standards.
allowed-tools: Read Write Edit MultiEdit Grep Glob Bash WebSearch
---

# Ruby Coder

## Ruby 3.x Modern Syntax

Use hash shorthand when keys match variable names:

```ruby
age = 49
name = "David"
user = { name:, age: }
```

For general naming conventions, semantic methods, and enumerable patterns, see `references/ruby-style-conventions.md`.

## Sandi Metz's 4 Rules for Developers

These rules enforce strict limits to maintain code quality. Breaking them requires explicit justification.

### Rule 1: Classes Can Be No Longer Than 100 Lines

**Limit**: Maximum 100 lines of code per class

**Check**: When a class exceeds this limit, extract secondary concerns to new classes

```ruby
# When exceeding 100 lines, extract secondary concerns:
class UserProfilePresenter  # Presentation logic
class UserProfileValidator  # Validation logic
class UserProfileNotifier   # Notification logic
```

**Exceptions**: Valid Single Responsibility Principle (SRP) justification required

### Rule 2: Methods Can Be No Longer Than 5 Lines

**Limit**: Maximum 5 lines per method. Each if/else branch counts as lines.

```ruby
# Good - 5 lines or fewer
def process_order
  validate_order
  calculate_totals
  apply_discounts
  finalize_payment
end

# Avoid - extract when too long
def process_order
  return unless items.any?
  return unless valid_address?
  self.subtotal = items.sum(&:price)
  self.tax = subtotal * tax_rate
  self.total = subtotal + tax
  charge_customer
  send_confirmation
end
```

**Exceptions**: Pair approval required (Rule 0: break rules with agreement)

### Rule 3: Pass No More Than 4 Parameters

**Limit**: Maximum 4 parameters per method. Use parameter objects or hashes when more data is needed.

```ruby
# Parameter object when data is related
def create_post(post_params)
  Post.create(user: post_params.user, title: post_params.title, content: post_params.content)
end
```

**Exceptions**: Rails view helpers like `link_to` or `form_for` are exempt

### Rule 4: Controllers May Instantiate Only One Object

**Limit**: Controllers should instantiate only one object; other objects come through that via facade pattern.

```ruby
# Good - single object via facade
class DashboardController < ApplicationController
  def show
    @dashboard = DashboardFacade.new(current_user)
  end
end

# Avoid - multiple instance variables
class DashboardController < ApplicationController
  def show
    @user = current_user
    @posts = @user.posts.recent
    @notifications = @user.notifications.unread
  end
end
```

- Prefix unused instance variables with underscore: `@_calculation`
- Avoid direct collaborator access in views: `@user.profile.avatar` -> use facade method

## Code Quality Standards

### Thread Safety

Use `Mutex` for shared mutable state:

```ruby
class Configuration
  @instance_mutex = Mutex.new

  def self.instance
    return @instance if @instance
    @instance_mutex.synchronize { @instance ||= new }
  end
end
```

### Idempotent Operations

Design operations to be safely repeatable:

```ruby
def activate_user
  return if user.active?
  user.update(active: true)
  send_activation_email unless email_sent?
end
```

## Refactoring Triggers

Extract classes when:
- Class exceeds 100 lines (Sandi Metz Rule 1)
- Class has multiple responsibilities
- Class name contains "And" or "Or"

Extract methods when:
- Method exceeds 5 lines (Sandi Metz Rule 2)
- Conditional logic is complex
- Code has nested loops or conditionals
- Comments explain what code does (code should be self-explanatory)

Use parameter objects when:
- Methods require more than 4 parameters (Sandi Metz Rule 3)
- Related parameters are always passed together
- Parameter list is growing over time

Create facades when:
- Controllers need multiple objects (Sandi Metz Rule 4)
- Views access nested collaborators
- Complex data aggregation is needed

## When to Break Rules

Sandi Metz's "Rule 0": Break any of the 4 rules only with pair approval or clear justification.

| Rule | Valid Exception |
|------|---------------|
| 100 lines | Clear SRP justification required |
| 5 lines | Complex but irreducible algorithms |
| 4 params | Rails view helpers exempt |
| 1 object | Simple views without facades |

Document all exceptions with clear reasoning in code comments.

## References

- `references/sandi-metz.md` - Code smells, refactoring, testing principles
- `references/ruby-tips.md` - Type conversion, hash patterns, proc composition, refinements
- `references/ruby-style-conventions.md` - Naming, semantic methods, enumerables, composition
