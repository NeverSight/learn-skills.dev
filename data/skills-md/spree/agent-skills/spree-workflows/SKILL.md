---
name: spree-workflows
description: Use when the user wants to run custom code inside a Spree 6 business flow — veto an add-to-cart, block checkout completion, enforce a purchase limit or B2B rule, add data to tax or promotion calculation, react inside the order-placement transaction, customize returns eligibility, or write a new multi-step operation with compensation and gateway calls. Common phrasings include "Spree.hooks.register", "workflow hook", "carts.add_item.validate", "carts.complete.before_finalize", "set_tax_line_context", "reject!", "Spree::Workflow", "step / external_step / on_flow_failure", "run_hooks", "halt!", "has_status", "add_status", "state machine replacement", "where do I put business logic", "step.spree_workflow", "trace a workflow". Covers services vs workflows, the three hook kinds, the hook catalog, writing your own workflow, statuses, instrumentation and testing. Reach for this BEFORE swapping a class via Spree.dependencies or decorating a model.
---

# Spree Workflows & Hooks

> Commands use the Spree CLI (`spree …`). On a classic Rails app without the CLI, use `bin/rails …` / `bundle exec rake …` from the app root. Paths below assume the Rails app lives in `server/`.

Spree's business logic lives in two kinds of plain Ruby classes, called the same way and returning the same `Spree::ServiceModule::Result`:

| Tier | Lives in | Use for |
|---|---|---|
| **Service** | `app/services/` | Plain create/update/delete, one sequential `call` body. Most of Spree. |
| **Workflow** (`Spree::Workflow`) | `app/workflows/` | Flows that need **extension points**, **external calls** (gateways, carriers), or **compensation** (undo when a later step fails): cart add/complete, order cancel, payment capture, fulfillment, returns, product status changes, imports… |

```ruby
result = Spree.cart_add_item_workflow.call(cart: cart, variant: variant, quantity: 2)
result.success?   # never raise on expected failures — check this
result.value      # the line item
result.error.to_s # message on failure; result.error.value is ActiveModel::Errors for rejections
```

There are **no state machines** in Spree. Records carry a plain `status` string (`Spree::HasStatus`), and every transition is a workflow with its own hooks.

## Where custom logic goes — decide first

| You want to… | Use |
|---|---|
| Stop an operation (purchase limit, B2B eligibility, fraud hold, return policy) | **`validate` hook** |
| Contribute data to a calculation (tax exemption, promotion eligibility, carrier data) | **Context hook** (`set_*_context`, `get_provider_data`, `extend_payload`) |
| Write related rows atomically with the change | **Lifecycle hook** (`after_*`, some run inside the transaction) |
| Send email, call a webhook, update a search index, sync an ERP | **Event subscriber** — `spree-events-webhooks` |
| Add a checkout requirement (the customer must provide X) | `Spree::Checkout::Registry.add_requirement` — `spree-checkout` |
| Replace a whole operation | `Spree.dependencies` — `spree-dependencies` (last resort; you own the copy) |
| Add a brand-new multi-step operation | Your own `Spree::Workflow` (below) |

Reach for the smallest one. A hook survives upgrades; a replaced class has to be re-synced every release.

**Don't** put business behavior on models (new public model methods that write, `after_save` side effects, transition callbacks) and **don't** decorate or patch `finalize!`, `Order#cancel`, `Payment#capture!` and friends — those are deprecated shells delegating to workflows (`Order#finalize!` → `Spree.order_complete_workflow`), and the real flow (`Spree::Carts::Complete`, `Spree::Orders::Cancel`, `Spree::Payments::Capture`) never calls your override. Use a hook on the workflow instead.

## Registering a hook

In `config/initializers/spree.rb`:

```ruby
Spree.hooks.register('carts.add_item.validate', 'MyStore::CheckPurchaseLimit')
Spree.hooks.register('carts.upsert_items.validate', 'MyStore::CheckPurchaseLimit')

# A block works for one-liners (but can't be deduplicated or unregistered by name)
Spree.hooks.register('orders.cancel.after_cancel') do |workflow|
  MyStore::Analytics.track(:order_canceled, workflow.order.number)
end
```

- Key is `'<workflow key>.<hook>'`. The workflow key derives from the class name: `Spree::Carts::AddItem` → `carts.add_item`.
- Handlers are stored as **class-name strings**, constantized when the hook fires — boot-safe and reload-safe. Registering the same class twice is a no-op.
- **Timing:** `Spree.hooks` is a process-wide registry core never resets, so top-level registration in an initializer is correct (unlike registries such as `payment_methods`, which core reassigns and must be appended in `after_initialize`). Don't register in `config.to_prepare` — it re-runs on every dev reload and duplicates block handlers. The one case needing `Rails.application.config.after_initialize` is *unregistering* a handler core registers (below).
- The handler is any class with `#call(workflow)`. It receives the **workflow instance**: every `#perform` keyword is a public reader (`workflow.cart`, `workflow.variant`, `workflow.quantity`), plus whatever the workflow exposes via `attr_reader` (`workflow.line_item`, `workflow.order`, `workflow.fulfillment`…). Check the workflow source / `references/hooks.md` for which readers are populated at each hook — e.g. `line_item` is nil during `carts.add_item.validate`.
- Keys are validated at boot when `eager_load` is on (production, usually CI): a typo raises `Spree::Hooks::UnknownHookError` listing the valid hooks. In development (lazy loading) a bad key silently never fires — run `Spree.hooks.validate!` in a console after `Rails.application.eager_load!` to check.
- `Spree.hooks.unregister(key, 'Handler')` removes one handler; `unregister(key)` removes all for the key.

```ruby
module MyStore
  class CheckPurchaseLimit
    def call(workflow)
      return if (workflow.quantity || 1).to_i <= 10   # carts.add_item quantity defaults to nil (=1)

      workflow.errors.add(:quantity, :purchase_limit_exceeded,
                          message: 'You can order at most 10 of this item.')
      workflow.reject!
    end
  end
end
```

`workflow.errors` is an `ActiveModel::Errors`. `reject!` (or `reject!('message')`, shorthand for an error on `:base`) aborts the flow, unwinds compensation, rolls back an open transaction and returns a failure result. The API renders it exactly like a model validation failure — 422 `validation_error` with `details` keyed by field — so SDK clients need no special handling. Prefer a symbolic type (`:purchase_limit_exceeded`) plus `message:` so clients can branch on the code.

`carts.add_item` **adds** to a quantity; `carts.upsert_items` **sets** it (quantity edits, removals, bulk payloads). A cart rule belongs on both keys — the readers (`cart`, `variant`, `quantity`) match, so one handler class registers on each. On the storefront an `upsert_items` rejection skips that item and reports it in the cart's `warnings` instead of failing the batch; admin order edits fail the whole edit.

## The three hook kinds

| Kind | Names | Runs | Return value | Many handlers |
|---|---|---|---|---|
| **Validate** | `validate` (also `orders.cancel.before_cancel`) | Before anything is written — rejecting costs nothing | Ignored; veto with `reject!` | Run in registration order; **first `reject!` stops the flow**, later validators never run |
| **Context** | `set_promotion_context`, `set_tax_line_context`, `get_provider_data`, `extend_payload` | Before a calculation | **Return a Hash** — merged (deep) across handlers and handed to the calculation | All run; key collision → last registered wins and is reported via `Rails.error` |
| **Lifecycle** | `before_*` / `after_*` (`after_item_added`, `before_finalize`, `after_cancel`, `before_capture`…) | Around/after the work; several run **inside** the flow's transaction | Ignored | All run in order |

```ruby
# Context hook: contribute tax-exemption evidence to totals recalculation
module MyStore
  class TaxExemption
    def call(workflow)
      cert = MyStore::ExemptionLookup.for(workflow.cart.customer)
      cert ? { exemption_certificate: cert.number } : {}
    end
  end
end
Spree.hooks.register('carts.recalculate_totals.set_tax_line_context', 'MyStore::TaxExemption')
```

The merged hash reaches the tax provider as `context:`; for promotions it's exposed as `workflow.promotion_context` (`carts.recalculate.set_promotion_context`).

### Multi-handler rules you must design for

- **Assume you are never alone on a hook.** Your app, extensions and Spree itself register handlers (core registers `Spree::Returns::EligibilityValidator` on `returns.create.validate` and `exchanges.create.validate`).
- **Don't depend on ordering** between handlers. Order = registration order (gem initializer load order). If two pieces must be sequenced, put them in one handler.
- **Handlers are not isolated.** An exception propagates out of the workflow, skips later handlers, and rolls back the open transaction — a `raise` in `after_item_added` means the item was never added. Rescue inside optional work, or move it to an event subscriber.
- **Reject only from `validate`.** `carts.complete.before_finalize` runs *after* the card was charged — rejecting there rolls back the order while the charge stands.
- **No slow work in in-transaction lifecycle hooks** (`after_item_added`, `after_cancel`, `after_*` on status workflows). Network calls hold a DB connection across a round trip; use a subscriber.

### Replacing a hook Spree registers itself

Core's return-window validator is registered by an engine initializer that runs *before* your `config/initializers/*`, so a plain `unregister` in an initializer removes it:

```ruby
# config/initializers/spree.rb
Spree.hooks.unregister('returns.create.validate', 'Spree::Returns::EligibilityValidator')
Spree.hooks.unregister('exchanges.create.validate', 'Spree::Returns::EligibilityValidator')
Spree.hooks.register('returns.create.validate', 'MyStore::ReturnPolicy')
Spree.hooks.register('exchanges.create.validate', 'MyStore::ReturnPolicy')
```

## Most useful hook points

| Key | Kind | When |
|---|---|---|
| `carts.add_item.validate` | validate | Before the line item is built (outside the transaction) |
| `carts.add_item.after_item_added` | lifecycle | After save + recalc, in transaction (`workflow.line_item`, `line_item_created`) |
| `carts.upsert_items.validate` / `.after_items_upserted` | validate / lifecycle | Per item before it's applied / after the batch |
| `carts.merge.validate` / `.after_merge` | validate / lifecycle | Guest→customer cart merge |
| `carts.recalculate.set_promotion_context` | context | Before promotions are evaluated |
| `carts.recalculate.after_recalculate` | lifecycle | After repricing |
| `carts.recalculate_totals.set_tax_line_context` | context | Before tax is estimated |
| `carts.complete.validate` | validate | After checkout requirements pass, before the order exists — **the place to block checkout** (credit limit, approval required) |
| `carts.complete.before_finalize` / `.after_finalize` | lifecycle | After payment, before/after the order is placed (`workflow.order`, `order_group`) |
| `orders.cancel.before_cancel` / `.after_cancel` | validate / lifecycle | Veto a cancel / write alongside it (in transaction) |
| `payments.capture.validate` | validate | Fraud holds — before the gateway is called |
| `payments.process.validate` | validate | Before authorize/purchase hits the gateway |
| `refunds.create.validate` | validate | Before a refund record exists (approval thresholds) |
| `fulfillments.create.get_provider_data` | context | Carrier account / service level / customs data |
| `fulfillments.fulfill.validate` / `.after_fulfill` | validate / lifecycle | Before/after marking shipped |
| `returns.create.validate` | validate | Return eligibility (replace core's window rule) |
| `customers.create.validate` | validate | Registration policy (bot screening, B2B approval) |
| `customers.anonymize.validate` | validate | Refuse a GDPR erasure (open disputes, legal hold) |
| `products.activate.validate` | validate | Require image/price/category before a product goes live |
| `products.create/update.validate` | validate | Fires for Admin API, CSV imports and seeds alike |

Admin draft-order editing uses **twin workflows** with their own keys and the same hooks: `orders.add_item`, `orders.upsert_items`, `orders.recalculate`, `orders.recalculate_totals`. Register on the cart key for storefront carts, the order key for admin edits, or both. Twins forward `order:` as `cart:`, so handlers read `workflow.cart` on either key.

**Full catalog (every workflow, hook, dependency key and reader):** [references/hooks.md](references/hooks.md).

Inspect at runtime (no rake task — use the console):

```ruby
Spree.hooks.workflows                     # { 'carts.add_item' => 'Spree::Carts::AddItem', ... }
Spree.hooks.carts                         # { 'carts.add_item' => [:validate, :after_item_added], ... }
Spree::Carts::Complete.declared_hooks     # [:validate, :before_finalize, :after_finalize]
Spree.hooks.keys                          # keys with registered handlers
Spree.hooks.handler_count('carts.complete.validate')
Spree.hooks.validate!                     # true, or raises UnknownHookError
```

## Writing your own workflow

Write one only for a *new* multi-step operation with external calls, compensation, or extension points. Plain CRUD stays a service (or a model save).

```ruby
# server/app/workflows/my_store/subscriptions/renew.rb
module MyStore
  module Subscriptions
    class Renew < Spree::Workflow
      hooks :validate, :after_renew      # declare every run_hooks name
      attr_reader :order                 # derived state handlers may read

      # The signature IS the contract. Bare `super` turns each keyword into a reader.
      def perform(subscription:, renewed_at: nil)
        super

        step :ensure_renewable
        run_hooks :validate

        ApplicationRecord.transaction do
          step :build_order, on_flow_failure: :discard_order
          step :extend_period
        end

        external_step :charge_customer   # refuses to run inside a transaction this workflow opened

        run_hooks :after_renew
        subscription.publish_event('subscription.renewed')
        success(order)
      end

      private

      def ensure_renewable
        failure(subscription, :not_active) unless subscription.active?   # raises — aborts the flow
      end

      def build_order
        @order = MyStore::Subscriptions::BuildOrder.call(subscription: subscription).value
      end

      def extend_period
        subscription.update!(renews_at: (renewed_at || Time.current) + 1.month)
      end

      def charge_customer
        Spree.payment_capture_workflow.call(payment: order.payments.last)   # a failure Result fails this step
      end

      def discard_order   # undo — armed when the transaction commits, run in reverse on later failure
        order&.destroy
      end
    end
  end
end
```

| Word | Meaning |
|---|---|
| `step :name` | Run the private method. A returned failure `Result` fails the flow. |
| `step :name, with: -> { Spree.some_workflow }` | Delegate to a swappable collaborator; its keywords are sliced from this workflow's readers |
| `on_flow_failure: :undo` | Compensation for the step, run in reverse if a later step fails |
| `external_step :name` | Network/gateway I/O; raises `Spree::Workflow::ContractError` inside a workflow-opened transaction |
| `run_hooks :name` | Dispatch a declared hook; returns the merged Hash (context hooks) |
| `failure(value, error)` | Abort from anywhere (raises internally, so an open transaction rolls back) |
| `workflow.reject!` | The handler-facing twin of `failure`, carrying `errors` |
| `halt!(value)` | Successful early exit — not allowed inside a transaction the workflow opened |
| `hooks :a, :b` / `workflow_key 'x.y'` | Declare extension points / override the derived key |

Rules: network calls never share a DB transaction (`external_step` enforces it); `failure`/`halt!` raise `Exception` subclasses, so a plain `rescue` in `#perform` won't swallow them — and don't `rescue Exception`. Inside `#perform` a parameter name is a local variable that shadows its reader; name derived state differently (`variant` in, `line_item` out).

## Statuses (instead of state machines)

```ruby
class MyStore::Subscription < Spree.base_class
  include Spree::HasStatus
  has_status :trialing, :active, :paused, :canceled, default: :trialing
end
# => inclusion validation, #paused?, .paused scope, .with_status(:active, :trialing)

Spree::GiftCard.add_status(:on_hold, after: :active)   # extend a core model's statuses
```

No transition graph, no events, no callbacks — moving a record between statuses is a workflow (`MyStore::Subscriptions::Pause.call(...)`, not `subscription.pause!`). A custom status needs your own workflow to move records into it; core workflows guard on core statuses, and `add_status` is additive only. Call Spree's transitions through their workflows too: `Spree.product_archive_workflow.call(product: product)`.

## Observability

Every run, step and hook dispatch emits `ActiveSupport::Notifications`:

| Event | Payload |
|---|---|
| `perform.spree_workflow` | `workflow`, `outcome` (`success`/`failure`/`error`) |
| `step.spree_workflow` | `workflow`, `step`, `external`, `outcome` |
| `hooks.spree_workflow` | `workflow`, `hook`, `handler_count` |

```ruby
ActiveSupport::Notifications.subscribe('step.spree_workflow') do |*, payload|
  Rails.logger.info("#{payload[:workflow]}##{payload[:step]} #{payload[:outcome]}")
end
```

With the `spree_opentelemetry` gem (plus `OTEL_EXPORTER_OTLP_ENDPOINT`), these become spans automatically: one per workflow run, one per step (`external_step`s as `client` spans), one per hook dispatch that has handlers.

## Testing

Handlers are plain classes — unit-test them with a real workflow instance, and integration-test through the workflow:

```ruby
RSpec.describe MyStore::CheckPurchaseLimit do
  let(:cart)    { create(:cart) }
  let(:variant) { create(:variant) }
  let(:handler) { 'MyStore::CheckPurchaseLimit' }

  before { Spree.hooks.register('carts.add_item.validate', handler) }
  after  { Spree.hooks.unregister('carts.add_item.validate', handler) }

  it 'rejects more than 10' do
    result = Spree.cart_add_item_workflow.call(cart: cart, variant: variant, quantity: 11)

    expect(result).to be_failure
    expect(result.error.value.details[:quantity]).to include(a_hash_including(error: :purchase_limit_exceeded))
    expect(cart.line_items.count).to eq(0)
  end
end
```

- If the handler is registered in `config/initializers/spree.rb`, it is already active in specs — skip the `before`/`after`.
- **Never `Spree.hooks.clear!` in app specs** — it permanently wipes core registrations (the return-window validator) for the rest of the process. Unregister exactly what you registered. For blocks, keep the proc: `h = ->(w) { ... }; Spree.hooks.register(key, &h)` … `Spree.hooks.unregister(key, h)`.
- Add a boot-time check to CI: `Rails.application.eager_load!; Spree.hooks.validate!`.

## Gotchas

- **Swapping a workflow class changes its hook key.** `MyApp::Carts::AddItem < Spree::Carts::AddItem` dispatches `my_app.carts.add_item.*` — every handler on `carts.add_item.*` (yours, extensions', core's) silently stops firing. If you must subclass, declare `workflow_key 'carts.add_item'` in it. See `spree-dependencies`.
- Registering on `orders.complete.*` raises `UnknownHookError` at boot (eager load) — `Spree::Orders::Complete` declares no hooks. Checkout goes through `carts.complete`.
- `carts.recalculate_totals` only has `set_tax_line_context`; promotion context is on `carts.recalculate`.
- **Workflows run from jobs, rake tasks or the console need a store context.** Set `Spree::Current.store = cart.store` (or `order.store`) first — `Spree::Store.default` may be nil. A job walking records of several stores wraps each in `Spree::Current.with_store(record.store) { … }` (or `each_store_of(relation)` in a `Spree::BaseJob` subclass). Doing so also arms the dev/test `Spree::StoreScopeGuard` for that job, so an unscoped query inside a handler you wrote gets flagged there just as it would in an API request.
- Validate hooks see arguments, not results: `workflow.line_item`, `workflow.order`, `workflow.fulfillment` are nil until the step that sets them has run.

## Where to read further

- `node_modules/@spree/docs/dist/developer/customization/workflows.md` (https://spreecommerce.org/docs/developer/customization/workflows)
- `node_modules/@spree/docs/dist/developer/customization/validations.md` — hooks vs model validations vs validator registries
- `node_modules/@spree/docs/dist/developer/providers/observability.md` — OpenTelemetry setup
- Source: `spree_core` `lib/spree/workflow.rb`, `lib/spree/hooks.rb`, `app/workflows/spree/**`, `app/models/concerns/spree/has_status.rb`
- Related skills: `spree-dependencies` (replace a class), `spree-events-webhooks` (after-the-fact side effects), `spree-checkout` (requirements registry), `spree-customization` (routing)
