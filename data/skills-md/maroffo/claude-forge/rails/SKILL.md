---
name: rails
description: "Ruby on Rails 8 with service-oriented architecture, Dry-validation, Sidekiq/Solid Queue, Hotwire. Use for Rails API, Rails services, Rails forms, RSpec, ActiveRecord, Rails migrations. Not for standalone Ruby gems (use ruby skill)."
allowed-tools: [mcp__acp__Read, mcp__acp__Edit, mcp__acp__Write, mcp__acp__Bash]
---

# ABOUTME: Rails 8 service-oriented architecture, validation contracts, background jobs, Hotwire
# ABOUTME: API development with thin controllers, services, forms, filters, and modern Rails stack

# Ruby on Rails - Modern Development

## Quick Reference

```bash
bundle exec lefthook run all    # Quality checks
bundle exec rspec               # Tests
rails s / bin/dev               # Server (bin/dev for Hotwire)
bin/jobs                        # Solid Queue workers
```

**See also:** `_AST_GREP.md` (sg patterns), `_PATTERNS.md`, `source-control`

**Architecture calls:**
```ruby
MyService.new(user:, params:).call    # Service
MyForm.new(params, user).save         # Form
MyFilter.result(params, scope)        # Filter
MyJob.perform_async(id)               # Sidekiq
MyJob.perform_later(id)               # Solid Queue
```

---

## Sacred Rules (NON-NEGOTIABLE)

1. **NO LOGIC IN CONTROLLERS** - HTTP layer only
2. **ALL LOGIC IN SERVICES/FORMS/FILTERS**
3. **NO ACTIVERECORD VALIDATIONS** - Dry-validation contracts only
4. **MINIMUM MODEL LOGIC** - Data structures + associations
5. **NO MODEL CALLBACKS** - Exception: attachment destruction

---

## Ruby 3.4 & Rails 8

**YJIT enabled by default** (15-30% faster). New `it` block parameter:
```ruby
users.map { it.name }  # replaces _1
```

**Solid Trifecta** (DB-backed alternatives to Redis):
| Component | Purpose | Use When |
|-----------|---------|----------|
| Solid Queue | Jobs | <100 jobs/sec, no Redis needed |
| Solid Cache | Caching | 10TB+ possible |
| Solid Cable | WebSockets | No Redis infra |

**Use Sidekiq when:** latency <100ms required, 10k+ jobs/min

---

## Pattern Summary

**Service:** Complex business logic, multi-step operations, transactions
```ruby
MyService.new(user:, params:).call  # Returns OpenStruct(success, record)
```

**Form:** User input validation + persistence
```ruby
MyForm.new(params, user).save  # Returns true/false
```

**Contract:** Validation rules (Dry-validation)
```ruby
CreateContract.new.call(params)  # Returns Result(success?, errors)
```

**Controller:** HTTP layer only, no business logic
```ruby
def create
  form = CreateForm.new(params, current_user)
  form.save ? render(json: form.model, status: :created) : render(json: { errors: form.errors }, status: :unprocessable_entity)
end
```

**Model:** Associations, enums, simple scopes. NO validations, NO callbacks, NO business logic.
```ruby
belongs_to :user
has_many :tags, dependent: :destroy
enum :status, { draft: 0, published: 1 }
scope :recent, -> { order(created_at: :desc) }
```

---

## Quality Checklist

Before commit: `bundle exec lefthook run all`

- [ ] NO controller logic
- [ ] Validation in contracts only
- [ ] Business logic in services
- [ ] Jobs idempotent
- [ ] Tests pass

---

## Resources

- https://guides.rubyonrails.org/
- https://dry-rb.org/gems/dry-validation/
- https://github.com/rails/solid_queue
- https://turbo.hotwired.dev/

**Key gems:** Dry-validation, Sidekiq/Solid Queue, Scenic, Pundit, Devise/Rodauth, ViewComponent/Phlex

---

**For detailed patterns and examples, see `references/rails-patterns.md`**
