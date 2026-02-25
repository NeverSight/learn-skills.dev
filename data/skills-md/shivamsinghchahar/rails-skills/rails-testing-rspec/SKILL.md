---
name: rails-testing-rspec
description: Write Rails tests with RSpec, FactoryBot, and mocking patterns. Use when creating tests, writing specs for models/controllers/requests, setting up test fixtures, or mocking external services.
---

# Rails Testing with RSpec

Build comprehensive test suites using RSpec and FactoryBot. This skill covers spec structure, factories, mocking, and testing best practices.

## Quick Start

Add to Gemfile:
```ruby
group :test do
  gem 'rspec-rails'
  gem 'factory_bot_rails'
  gem 'faker'
end
```

Generate RSpec install:
```bash
rails generate rspec:install
```

Write a test:
```ruby
require 'rails_helper'

RSpec.describe User, type: :model do
  describe 'validations' do
    it { is_expected.to validate_presence_of(:email) }
    it { is_expected.to validate_uniqueness_of(:email) }
  end
  
  describe '#full_name' do
    it 'returns concatenated first and last name' do
      user = build(:user, first_name: 'John', last_name: 'Doe')
      expect(user.full_name).to eq('John Doe')
    end
  end
end
```

Run tests:
```bash
rspec                    # All specs
rspec spec/models       # Only model specs
rspec spec/models/user_spec.rb:10  # Specific line
```

## Core Topics

**RSpec Setup**: See [rspec-setup.md](rspec-setup.md) for configuration, describe blocks, contexts, and common matchers.

**Factories**: See [factories-fixtures.md](factories-fixtures.md) for FactoryBot setup, defining factories, and sequences.

**Mocking**: See [mocking-stubbing.md](mocking-stubbing.md) for stubbing, mocking, spies, and testing external dependencies.

**Patterns**: See [patterns.md](patterns.md) for test organization, DRY specs, and common patterns.

## Examples

See [examples.md](examples.md) for:
- Model specs with validations and scopes
- Controller/request specs
- Integration tests
- Testing background jobs
