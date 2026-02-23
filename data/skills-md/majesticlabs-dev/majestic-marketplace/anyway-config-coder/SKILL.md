---
name: anyway-config-coder
description: Implement type-safe configuration with anyway_config gem. Use when creating configuration classes, replacing ENV access, or managing application settings. Triggers on configuration, environment variables, settings, secrets, or ENV patterns.
---

# Anyway Config Coder

**Never use ENV directly or Rails credentials.** Wrap all configuration in typed `anyway_config` classes.

```ruby
# WRONG
api_key = ENV["GEMINI_API_KEY"]

# RIGHT
class GeminiConfig < Anyway::Config
  attr_config :api_key, timeout: 30
  required :api_key
end
GeminiConfig.new.api_key
```

## Configuration Class Pattern

```ruby
# config/configs/gemini_config.rb
class GeminiConfig < Anyway::Config
  attr_config :api_key, model: "gemini-pro", timeout: 30, max_retries: 3
  required :api_key

  def configured? = api_key.present?
end
```

ENV auto-mapping: `GeminiConfig` -> `GEMINI_API_KEY`, `GEMINI_MODEL`, etc. Override prefix with `config_name :payment`.

Nested config uses hash defaults, accessed via dot notation: `AppConfig.new.database.host`.

## Singleton Pattern (Recommended)

```ruby
class GeminiConfig < Anyway::Config
  attr_config :api_key, :model

  class << self
    def instance = @instance ||= new
  end
end

GeminiConfig.instance.api_key
```

## Directory Structure

```
config/
├── configs/          # Ruby config classes
│   ├── gemini_config.rb
│   └── stripe_config.rb
└── settings/         # YAML overrides (optional)
    └── gemini.yml
```

YAML files use `default: &default` with environment-specific overrides (`development:`, `test:`, `production:`).

## Validation

```ruby
class StorageConfig < Anyway::Config
  attr_config :bucket, :region, :access_key_id, :secret_access_key
  required :bucket, :region
  required :access_key_id, :secret_access_key, env: :production  # Conditional

  def validate!
    super
    raise_validation_error("Invalid region") unless %w[us-east-1 us-west-2 eu-west-1].include?(region)
  end
end
```

## Type Coercion

```ruby
class ApiConfig < Anyway::Config
  # Automatic coercion
  attr_config timeout: 30       # Integer
  attr_config enabled: true     # Boolean
  attr_config rate: 1.5         # Float

  # Coerce arrays from comma-separated strings
  coerce_types allowed_origins: {
    type: :string,
    array: true
  }
  # ALLOWED_ORIGINS="example.com,other.com" => ["example.com", "other.com"]
end
```

## Testing Configurations

Test defaults, required validations, and computed methods. Override in tests with `with_env`:

```ruby
RSpec.describe GeminiConfig do
  it "requires api_key" do
    expect { described_class.new(api_key: nil) }.to raise_error(Anyway::Config::ValidationError)
  end
end

# spec/support/anyway_config.rb - global override
RSpec.configure do |config|
  config.around(:each) do |example|
    with_env("GEMINI_API_KEY" => "test-key") { example.run }
  end
end
```

## Common Patterns

### API Client Config

Add `client_options` helper to build connection hashes:

```ruby
class OpenAIConfig < Anyway::Config
  attr_config :api_key, :organization_id, model: "gpt-4", max_tokens: 1000
  required :api_key

  def client_options = { access_token: api_key, organization_id: }.compact
end
```

### Multi-Provider Config

Use predicate methods and `case` for provider-specific options:

```ruby
class StorageConfig < Anyway::Config
  attr_config provider: "local", bucket: nil, endpoint: nil

  def s3? = provider == "s3"
  def local? = provider == "local"
  def service_options = case provider when "s3" then s3_options else local_options end
end
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Direct `ENV["KEY"]` | No type safety, scattered | Config class |
| `ENV.fetch` everywhere | Duplication, no validation | Centralized config |
| Rails credentials | Complex, hard to test | anyway_config classes |
| Hardcoded secrets | Security risk | Environment variables |
| Magic strings | Typos, no IDE support | Config constants |

## Detailed References

- `references/advanced-patterns.md` - Dynamic configs, callbacks, inheritance
