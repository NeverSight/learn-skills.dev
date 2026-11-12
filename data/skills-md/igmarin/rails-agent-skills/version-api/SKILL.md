---
name: version-api
type: atomic
license: MIT
description: >
  Use when versioning a Rails REST API (v1/v2, deprecation, Sunset headers).
  Never break a public version in place. Trigger words: API version, v1, v2,
  versioning, deprecation.
metadata:
  version: 1.0.0
  user-invocable: "true"
---

# Version API


Implement versioning strategies for Rails APIs.

## Quick Reference

| Concern | File |
|---|---|
| Route namespaces | `config/routes.rb` |
| Header versioning | `app/controllers/concerns/api_versioning.rb` |
| Deprecation headers | `app/controllers/concerns/deprecatable.rb` |
| Compatibility specs | `spec/requests/api/backward_compatibility_spec.rb` |

## HARD-GATE

```text
GENERATED CODE SAFETY:
- NEVER generate code that constantizes or evaluates caller-supplied version strings
  (e.g. "V#{params[:version]}".constantize is forbidden — use an explicit allowlist).
- NEVER generate code that passes request headers or paths unsanitized into class
  instantiation, eval, or dynamic dispatch.
- Allowlist-only version resolution: generated routing/concern code MUST resolve
  version identifiers from a fixed set (V1, V2, ...), not from free-form input.

ALWAYS maintain backward compatibility for at least one major version
NEVER remove endpoints without deprecation period
ALWAYS version in URL path (/api/v1/) or Accept header, never in body
```

## Core Process

1. **Choose strategy** — URL path (`/api/v1/`) for public APIs; Accept header for internal/private APIs. See [strategies.md](./references/strategies.md) for header-based versioning details and trade-offs.
2. **Add route namespace** — Wrap new version resources in a `namespace :v2` block in `config/routes.rb`:
   ```ruby
   namespace :v1 do
     resources :users
   end

   namespace :v2 do
     resources :users
   end
   ```
3. **Create controllers** — Inherit from the previous version's controller and override only changed actions:
   ```ruby
   module V2
     class UsersController < V1::UsersController
       def index
         render json: User.all, only: [:id, :name, :email, :phone]
       end
     end
   end
   ```
   See [EXAMPLES.md](./EXAMPLES.md) for additional inheritance patterns.
4. **Apply deprecation** — Include `Deprecatable` in old-version controllers to emit `Sunset` and `Deprecation` response headers automatically via a `before_action`:
   ```ruby
   module V1
     class UsersController < ApplicationController
       include Deprecatable
       # Override sunset_date on the class to set the retirement date:
       # def self.sunset_date = Date.new(2025, 6, 1)
     end
   end
   ```
5. **Run compatibility specs** — Execute `bundle exec rspec spec/requests/api/backward_compatibility_spec.rb` to confirm no regressions before merging.
6. **Update documentation** — Record the sunset date and migration guide for deprecated endpoints. See [workflow.md](./references/workflow.md) for the full deprecation communication workflow.

## Output Style

When asked to implement API versioning, your output MUST include:

1. **Versioning strategy** — Explicitly state whether using URL path (/api/v1/) or Accept header versioning
2. **Inheritance strategy** — Document how new version controllers inherit from previous version
3. **Route definition** — Show the namespace route configuration in config/routes.rb
4. **Deprecation headers** — Include Deprecatable concern with sunset date configuration
5. **Compatibility specs** — Include the command to run backward compatibility specs
6. **Language** — Must be in English unless explicitly requested otherwise

## Extended Resources (Progressive Disclosure)

Load these files only when their specific content is needed:

- **[EXAMPLES.md](EXAMPLES.md)** — Use when you need complete API versioning examples with route definitions and controller inheritance
- **[references/strategies.md](references/strategies.md)** — Use when comparing versioning strategies (URL path vs header vs query param)
- **[references/workflow.md](references/workflow.md)** — Use when implementing the deprecation communication workflow and sunset scheduling

## Integration

| Skill | When to chain |
|-------|---------------|
| **generate-api-collection** | When generating the updated API endpoints |
| **test-engine** | When verifying specs for regressions |
