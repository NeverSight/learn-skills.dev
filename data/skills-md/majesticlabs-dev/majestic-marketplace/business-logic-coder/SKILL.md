---
name: business-logic-coder
description: Implement business logic with ActiveInteraction and AASM state machines. Routes to specialized skills for typed operations and state management.
---

# Business Logic Patterns

Orchestrator for structured business logic in Rails.

## Skill Routing

| Need | Skill | Use When |
|------|-------|----------|
| Typed operations | `active-interaction-coder` | Creating business operations, refactoring service objects |
| State machines | `aasm-coder` | Implementing workflows, managing state transitions |

## When to Use Each

### ActiveInteraction

Use for **operations** - things that happen once:

- User registration
- Order placement
- Payment processing
- Data imports
- Report generation

```ruby
# Example: One-time operation with typed inputs
outcome = Users::Create.run(email: email, name: name)
```

### AASM

Use for **state management** - things with lifecycle:

- Order status (pending → paid → shipped)
- Subscription state (trial → active → cancelled)
- Document workflow (draft → review → published)
- Task status (todo → in_progress → done)

```ruby
# Example: Stateful entity with transitions
order.pay!  # pending → paid
order.ship! # paid → shipped
```

## Combined Pattern

Often used together - interactions trigger state changes:

```ruby
module Orders
  class Process < ActiveInteraction::Base
    object :order, class: Order

    def execute
      order.process!  # AASM transition
      fulfill_order(order)
      order
    end
  end
end
```

## Setup

```ruby
# Gemfile
gem "active_interaction", "~> 5.3"
gem "aasm", "~> 5.5"
```

## Quick Reference

**ActiveInteraction:**
- `.run` - Returns outcome (check `.valid?`)
- `.run!` - Raises on failure
- `compose` - Call nested interactions

**AASM:**
- `.event!` - Transition or raise
- `.event` - Transition or return false
- `.may_event?` - Check if transition valid
- `.aasm.events` - List available events

## Related Skills

- **`event-sourcing-coder`** - Record domain events from state transitions
