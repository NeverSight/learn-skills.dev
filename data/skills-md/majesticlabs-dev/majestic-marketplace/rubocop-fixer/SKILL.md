---
name: rubocop-fixer
description: Use when fixing Rubocop violations. Runs Rubocop to identify issues, applies fixes following project conventions, and explains non-obvious corrections.
allowed-tools: Read Write Edit Bash Grep Glob
---

# Rubocop Fixer

You fix Rubocop violations in Rails projects while respecting project-specific configurations.

## Process

### 1. Check Configuration

First, understand the project's Rubocop setup:

```bash
# Check for config file
cat .rubocop.yml

# Check inherited configs
cat .rubocop_todo.yml 2>/dev/null
```

### 2. Run Rubocop

```bash
# All violations
bundle exec rubocop

# Specific file
bundle exec rubocop app/models/user.rb

# Specific cop
bundle exec rubocop --only Style/StringLiterals

# Auto-correct safe violations
bundle exec rubocop -a

# Auto-correct all (including unsafe)
bundle exec rubocop -A
```

### 3. Understand the Violation

Before fixing, understand why the cop exists:

```bash
# Show cop documentation
bundle exec rubocop --show-cops Style/StringLiterals
```

## Common Violations & Fixes

### Style/StringLiterals

```ruby
# Before (violation)
name = "hello"

# After (if configured for single quotes)
name = 'hello'

# Note: Use double quotes when interpolation or escapes needed
name = "hello #{user}"
```

### Style/FrozenStringLiteralComment

```ruby
# Add at top of file
# frozen_string_literal: true

class User
  # ...
end
```

### Layout/LineLength

```ruby
# Before (too long)
def very_long_method_name(first_parameter, second_parameter, third_parameter, fourth_parameter)

# After
def very_long_method_name(
  first_parameter,
  second_parameter,
  third_parameter,
  fourth_parameter
)
```

### Style/Documentation

```ruby
# Before (missing documentation)
class UserService
end

# After
# Handles user-related business logic including registration
# and profile management.
class UserService
end

# Or disable for specific class
class UserService # rubocop:disable Style/Documentation
end
```

### Metrics/MethodLength

```ruby
# Before (too long)
def process_order
  validate_items
  calculate_subtotal
  apply_discounts
  calculate_tax
  calculate_shipping
  finalize_total
  create_invoice
  send_confirmation
  update_inventory
  notify_warehouse
end

# After (extract methods)
def process_order
  prepare_order
  complete_order
  post_order_tasks
end

private

def prepare_order
  validate_items
  calculate_totals
end

def calculate_totals
  calculate_subtotal
  apply_discounts
  calculate_tax
  calculate_shipping
  finalize_total
end

def complete_order
  create_invoice
  send_confirmation
end

def post_order_tasks
  update_inventory
  notify_warehouse
end
```

### Metrics/AbcSize

ABC = Assignments, Branches, Conditions

```ruby
# Before (high ABC)
def process(user)
  if user.active?
    user.name = params[:name]
    user.email = params[:email]
    user.role = params[:role]
    user.save!
    notify(user)
  end
end

# After (lower ABC)
def process(user)
  return unless user.active?

  update_user_attributes(user)
  user.save!
  notify(user)
end

def update_user_attributes(user)
  user.assign_attributes(user_params)
end

def user_params
  params.slice(:name, :email, :role)
end
```

### Rails/HasManyOrHasOneDependent

```ruby
# Before
has_many :posts

# After
has_many :posts, dependent: :destroy
# or
has_many :posts, dependent: :nullify
```

### Rails/InverseOf

```ruby
# Before
has_many :posts
belongs_to :user

# After
has_many :posts, inverse_of: :user
belongs_to :user, inverse_of: :posts
```

## Inline Disabling

When a violation is intentional:

```ruby
# Disable for line
some_code # rubocop:disable Style/SomeCop

# Disable for block
# rubocop:disable Style/SomeCop
some_code
more_code
# rubocop:enable Style/SomeCop

# Disable for file (at top)
# rubocop:disable Style/SomeCop
```

## Generating TODO File

For legacy codebases with many violations:

```bash
# Generate .rubocop_todo.yml with all current violations
bundle exec rubocop --auto-gen-config

# Then incrementally fix cops
bundle exec rubocop --only Style/StringLiterals -a
```

## Output Format

After fixing violations:

1. **Violations Fixed** - List of cops and count
2. **Manual Fixes** - Changes requiring human judgment
3. **Remaining** - Violations that need review
4. **Verification** - `bundle exec rubocop` output
