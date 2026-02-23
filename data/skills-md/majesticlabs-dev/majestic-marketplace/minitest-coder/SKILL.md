---
name: minitest-coder
description: Write Minitest tests for Ruby and Rails applications. Use when creating test files, writing test cases, or testing new features. Not for RSpec — use rspec-coder instead. Covers both traditional and spec styles, fixtures, mocking, and Rails integration testing patterns.
allowed-tools: Read Write Edit MultiEdit Grep Glob Bash WebSearch
---

# Minitest Coder

## Core Philosophy

- **AAA Pattern**: Arrange-Act-Assert structure for clarity
- **Behavior over Implementation**: Test what code does, not how
- **Isolation**: Tests should be independent
- **Descriptive Names**: Clear test descriptions
- **Coverage**: Test happy paths AND edge cases
- **Fast Tests**: Minimize database operations
- **Fixtures**: Use fixtures for test data

## Minitest Styles

| Style | Best For | Syntax |
|-------|----------|--------|
| Traditional | Simple unit tests | `test "description"` |
| Spec | Complex scenarios with contexts | `describe`/`it` with `let`/`subject` |

### Traditional Style

```ruby
class UserTest < ActiveSupport::TestCase
  test "validates presence of name" do
    user = User.new
    assert_not user.valid?
    assert_includes user.errors[:name], "can't be blank"
  end
end
```

### Spec Style

```ruby
class UserTest < ActiveSupport::TestCase
  describe "#full_name" do
    subject { user.full_name }
    let(:user) { User.new(first_name: "Buffy", last_name:) }

    describe "with last name" do
      let(:last_name) { "Summers" }

      it "returns full name" do
        assert_equal "Buffy Summers", subject
      end
    end
  end
end
```

## Test Organization

### File Structure

- `test/models/` - Model unit tests
- `test/services/` - Service object tests
- `test/integration/` - Full-stack tests
- `test/mailers/` - Mailer tests
- `test/jobs/` - Background job tests
- `test/fixtures/` - Test data
- `test/test_helper.rb` - Configuration

### Naming Conventions

- Mirror app structure: `app/models/user.rb` → `test/models/user_test.rb`
- Use fully qualified namespace: `class Users::ProfileServiceTest`
- **Don't add** `require 'test_helper'` (auto-imported)

## Spec Style Patterns

See [references/spec-patterns.md](references/spec-patterns.md) for detailed examples.

| Pattern | Use Case |
|---------|----------|
| `subject { ... }` | Method under test |
| `let(:name) { ... }` | Lazy-evaluated data |
| `describe "context"` | Group related tests (max 3 levels) |
| `before { ... }` | Complex setup |

```ruby
describe "#process" do
  subject { processor.process }
  let(:processor) { OrderProcessor.new(order) }
  let(:order) { orders(:paid_order) }

  it "succeeds" do
    assert subject.success?
  end
end
```

## Fixtures

```yaml
# test/fixtures/users.yml
alice:
  name: Alice Smith
  email: alice@example.com
  created_at: <%= 2.days.ago %>
```

```ruby
class UserTest < ActiveSupport::TestCase
  fixtures :users

  test "validates uniqueness" do
    duplicate = User.new(email: users(:alice).email)
    assert_not duplicate.valid?
  end
end
```

## Mocking and Stubbing

See [references/spec-patterns.md](references/spec-patterns.md) for detailed examples.

| Method | Purpose |
|--------|---------|
| `Object.stub :method, value` | Stub return value |
| `Minitest::Mock.new` | Verify method calls |

```ruby
test "processes payment" do
  PaymentGateway.stub :charge, true do
    processor = OrderProcessor.new(order)
    assert processor.process
  end
end
```

## Assertions Quick Reference

### Basic Assertions

```ruby
# Boolean
assert user.valid?
assert_not user.admin?

# Equality
assert_equal "Alice", user.name
assert_nil user.deleted_at

# Collections
assert_includes users, admin_user
assert_empty order.items

# Exceptions
assert_raises ActiveRecord::RecordInvalid do
  user.save!
end
```

### Rails Assertions

```ruby
# Changes
assert_changes -> { user.reload.status }, to: "active" do
  user.activate!
end

assert_difference "User.count", 1 do
  User.create(name: "Charlie")
end

# Responses
assert_response :success
assert_redirected_to user_path(user)
```

## AAA Pattern

```ruby
test "processes refund" do
  # Arrange
  order = orders(:completed_order)
  original_balance = order.user.account_balance

  # Act
  result = order.process_refund

  # Assert
  assert result.success?
  assert_equal "refunded", order.reload.status
end
```

**Spec style with subject**:
```ruby
describe "#process_refund" do
  subject { order.process_refund }
  let(:order) { orders(:completed_order) }

  it "updates status" do
    subject
    assert_equal "refunded", order.reload.status
  end

  it "credits user" do
    assert_changes -> { order.user.reload.account_balance }, by: order.total do
      subject
    end
  end
end
```

## Test Coverage Standards

| Type | Test For |
|------|----------|
| Models | Validations, associations, scopes, callbacks, methods |
| Services | Happy path, sad path, edge cases, external integrations |
| Controllers | Status codes, redirects, parameter handling |
| Jobs | Execution, retry logic, error handling |

### Coverage Example

```ruby
class UserTest < ActiveSupport::TestCase
  # Validations
  test "validates presence of name" do
    user = User.new(email: "test@example.com")
    assert_not user.valid?
    assert_includes user.errors[:name], "can't be blank"
  end

  # Methods
  describe "#full_name" do
    subject { user.full_name }
    let(:user) { User.new(first_name: "Alice", last_name: "Smith") }

    it "returns full name" do
      assert_equal "Alice Smith", subject
    end

    describe "without last name" do
      let(:user) { User.new(first_name: "Alice") }

      it "returns first name only" do
        assert_equal "Alice", subject
      end
    end
  end
end
```

## Advanced Patterns

See [references/advanced-patterns.md](references/advanced-patterns.md) for production-tested patterns from 37signals.

| Pattern | Problem Solved |
|---------|----------------|
| Current.account fixtures | Multi-tenant URL isolation |
| Assertion-validating helpers | Early failure with clear messages |
| Deterministic UUIDs | Predictable fixture ordering |
| VCR timestamp filtering | Reusable API cassettes |
| Thread-based concurrency | Race condition detection |
| Adapter-aware helpers | SQLite/MySQL compatibility |

## Anti-Patterns

See [references/anti-patterns.md](references/anti-patterns.md) for detailed examples.

| Anti-Pattern | Why Bad |
|--------------|---------|
| `require 'test_helper'` | Auto-imported |
| >3 nesting levels | Unreadable output |
| `@ivars` instead of `let` | State leakage |
| Missing `subject` | Repetitive code |
| `assert x.include?(y)` | Use `assert_includes` |
| Testing private methods | Implementation coupling |
| Not using fixtures | Slow tests |

## Best Practices Checklist

**Organization**:
- [ ] Files mirror app structure
- [ ] NOT adding `require 'test_helper'`
- [ ] Using fully qualified namespace

**Style Choice**:
- [ ] Traditional for simple tests
- [ ] Spec for complex contexts
- [ ] Max 3 nesting levels

**Test Data**:
- [ ] Using fixtures (not factories)
- [ ] Using `let` for shared data
- [ ] Using `subject` for method under test

**Assertions**:
- [ ] Correct assertion methods
- [ ] Rails helpers (`assert_changes`, `assert_difference`)
- [ ] Testing behavior, not implementation

**Coverage**:
- [ ] Happy path tested
- [ ] Sad path tested
- [ ] Edge cases covered

## When to Choose Style

**Traditional**: Simple validations, straightforward tests, no shared setup

**Spec**: Multiple contexts, lazy evaluation needed, nested scenarios, reusable subject

**Can mix both** in the same file if it improves clarity.
