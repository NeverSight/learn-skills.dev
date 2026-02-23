---
name: gem-builder
description: Build production-quality Ruby gems. Use when creating new gems, structuring gem architecture, implementing configuration patterns, setting up testing, or preparing for publishing. Covers all gem types - libraries, CLI tools, Rails engines, and API clients.
allowed-tools: Read Write Edit MultiEdit Grep Glob Bash WebSearch
---

# Gem Builder

## Core Philosophy

- **Minimal dependencies**: Only add gems you truly need
- **Single responsibility**: Each class/module does one thing well
- **Semantic versioning**: Follow SemVer strictly (MAJOR.MINOR.PATCH)
- **Test coverage**: Every public method has tests
- **Documentation**: YARD docs, README, and CHANGELOG
- **Fail fast**: Validate inputs early, raise descriptive errors

## Gem Structure

```
my_gem/
├── lib/
│   ├── my_gem.rb              # Main entry point
│   ├── my_gem/
│   │   ├── version.rb         # VERSION constant
│   │   ├── config.rb          # Configuration class
│   │   ├── errors.rb          # Error hierarchy
│   │   └── [feature].rb       # Feature modules
├── test/                      # Test suite
├── my_gem.gemspec             # Gem specification
├── Gemfile                    # Development dependencies
├── Rakefile                   # Build tasks
├── README.md                  # User documentation
├── CHANGELOG.md               # Version history
└── LICENSE.txt                # License file
```

### Main Entry Point

```ruby
# lib/my_gem.rb
require_relative "my_gem/version"
require_relative "my_gem/config"
require_relative "my_gem/errors"

module MyGem
  class << self
    def config
      @config ||= Config.new
    end

    def configure
      yield(config)
    end

    def reset_configuration!
      @config = nil
    end
  end
end
```

## Gemspec Best Practices

```ruby
# my_gem.gemspec
require_relative "lib/my_gem/version"

Gem::Specification.new do |spec|
  spec.name          = "my_gem"
  spec.version       = MyGem::VERSION
  spec.authors       = ["Your Name"]
  spec.email         = ["you@example.com"]
  spec.summary       = "One-line description"
  spec.homepage      = "https://github.com/username/my_gem"
  spec.license       = "MIT"
  spec.required_ruby_version = ">= 3.2.0"

  spec.metadata["rubygems_mfa_required"] = "true"
  spec.metadata["changelog_uri"] = "#{spec.homepage}/blob/main/CHANGELOG.md"

  # Exclude test/CI files
  spec.files = IO.popen(%w[git ls-files -z], chdir: __dir__, err: IO::NULL) do |ls|
    ls.readlines("\x0", chomp: true).reject { |f| f.start_with?(*%w[bin/ test/ .github/]) }
  end
  spec.require_paths = ["lib"]
end
```

## Gem Types

| Type | Key Features |
|------|--------------|
| Library | Pure Ruby, no external services |
| API Client | HTTP wrapper with resource pattern |
| CLI Tool | `spec.executables`, bindir setup |
| Rails Integration | Railtie with `ActiveSupport.on_load` |

### API Client Pattern

```ruby
class Client
  def initialize(api_key: nil)
    @api_key = api_key || MyGem.config.api_key
    raise ArgumentError, "API key required" if @api_key.to_s.empty?
  end

  def users = @users ||= Resources::Users.new(self)
  def posts = @posts ||= Resources::Posts.new(self)
end
```

### Rails Integration

**Never require Rails directly.** Use lazy loading:

```ruby
# lib/my_gem/railtie.rb
class Railtie < Rails::Railtie
  initializer "my_gem.configure" do
    ActiveSupport.on_load(:active_record) do
      extend MyGem::Model
    end
  end
end

# lib/my_gem.rb
require_relative "my_gem/railtie" if defined?(Rails)
```

### Class Macro DSL

The pattern used by `searchkick`, `lockbox`:

```ruby
# Usage: mygemname word_start: [:name]
module Model
  def mygemname(**options)
    unknown = options.keys - KNOWN_OPTIONS
    raise ArgumentError, "Unknown: #{unknown.join(", ")}" if unknown.any?

    mod = Module.new
    mod.module_eval { define_method(:some_method) { options[:key] } }
    include mod
    class_variable_set(:@@mygemname_options, options.dup)
  end
end
```

## Configuration Pattern

```ruby
# lib/my_gem/config.rb
class Config
  attr_accessor :api_key, :base_url, :timeout
  attr_writer :logger

  def initialize
    @api_key = ENV.fetch("MY_GEM_API_KEY", nil)
    @base_url = ENV.fetch("MY_GEM_BASE_URL", "https://api.example.com")
    @timeout = Integer(ENV.fetch("MY_GEM_TIMEOUT", 30)) rescue 30
  end

  def logger
    @logger ||= defined?(Rails) ? Rails.logger : Logger.new($stderr)
  end
end
```

Usage:
```ruby
MyGem.configure do |config|
  config.api_key = "secret"
end
```

## Error Handling

```ruby
# lib/my_gem/errors.rb
module MyGem
  class Error < StandardError
    attr_reader :status, :body

    def initialize(message = nil, status: nil, body: nil)
      super(message)
      @status, @body = status, body
    end
  end

  class ConfigurationError < Error; end
  class AuthenticationError < Error; end  # 401
  class ClientError < Error; end          # 4xx
  class ServerError < Error; end          # 5xx
  class NetworkError < Error; end         # Connection failures
end
```

## Testing Setup

```ruby
# test/test_helper.rb
$LOAD_PATH.unshift File.expand_path("../lib", __dir__)
require "my_gem"
require "minitest/autorun"
require "webmock/minitest"

module TestConfig
  def setup_config
    WebMock.reset!
    MyGem.reset_configuration!
    MyGem.configure { |c| c.api_key = "test-key" }
  end

  def teardown_config
    WebMock.reset!
    MyGem.reset_configuration!
  end
end
```

```ruby
class ClientTest < Minitest::Test
  include TestConfig
  def setup = setup_config
  def teardown = teardown_config

  def test_requires_api_key
    MyGem.config.api_key = nil
    assert_raises(ArgumentError) { MyGem::Client.new }
  end
end
```

## Documentation

### YARD Setup (`.yardopts`)

```
--markup markdown
--no-private
lib/**/*.rb
- README.md
```

### README Sections

Installation, Quick Start, Configuration, Features, Development, License.

### CHANGELOG (Keep a Changelog)

```markdown
## [1.0.0] - 2025-01-15
### Added
- Initial release
```

## Build & Release

### Rakefile

```ruby
require "bundler/gem_tasks"
require "minitest/test_task"
Minitest::TestTask.create

require "rubocop/rake_task"
RuboCop::RakeTask.new

task default: %i[test rubocop]
```

### Release Workflow

```bash
# 1. Update lib/my_gem/version.rb
# 2. Update CHANGELOG.md
# 3. Commit and release
git commit -am "Release v1.0.0"
bundle exec rake release
```

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| `method_missing` | `define_method` |
| `@@class_variables` | `class << self` with ivars |
| Requiring Rails directly | `ActiveSupport.on_load` |
| Many runtime deps | Prefer stdlib |
| Committing Gemfile.lock | Only lock in apps |
| Heavy DSLs | Explicit Ruby |
| `autoload` | `require_relative` |

## Best Practices Checklist

**Structure:**
- [ ] Standard directory layout
- [ ] Version in single location
- [ ] Frozen string literals

**Gemspec:**
- [ ] All metadata populated
- [ ] `rubygems_mfa_required` = true
- [ ] Minimal runtime deps

**Configuration:**
- [ ] Environment variable fallbacks
- [ ] Block-based DSL
- [ ] Test-friendly reset method

**Error Handling:**
- [ ] Custom hierarchy
- [ ] Descriptive messages
- [ ] Status/body preserved

**Testing:**
- [ ] Isolation between tests
- [ ] WebMock for HTTP
- [ ] Success and failure cases

**Documentation:**
- [ ] YARD on public methods
- [ ] README with quick start
- [ ] CHANGELOG

**Rails (if applicable):**
- [ ] Optional with `if defined?(Rails)`
- [ ] Isolated namespace
- [ ] `ActiveSupport.on_load` hooks

## References

- `references/templates.md` - Copy-paste templates (CI, gemspec, README)
- `references/advanced-patterns.md` - Database adapters, multi-version testing
- `references/engine-migrations.md` - Keep migrations in Rails engines
