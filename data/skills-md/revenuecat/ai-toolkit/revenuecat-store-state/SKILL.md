---
name: revenuecat-store-state
description: Use when the user wants to inspect or change the state of products in App Store Connect, Google Play Console, RC Billing, or Test Store (prices, availability, localizations, review screenshots) via RevenueCat product-store-state plans
---

# Managing product store state

The store is the source of truth for prices, availability, localizations, and offers. Reads are immediate. Writes go through a **product store state plan**: create a draft, compute a reviewable diff, then apply. Nothing reaches the store until the plan is applied.

MCP and the `rc` CLI (see the `revenuecat-cli` skill) use the same plan/apply model. Prefer whichever surface is available. Refer to the MCP tool schemas (or `rc commands --schemas --json`) for exact parameters.

There is at most one active (non-terminal) plan per project. List plans before creating a new one; if create fails because a plan is already in progress, fetch it, describe what is pending, and decide with the user whether to continue it or discard it.

## Reads

Always use `get-product-store-state` (CLI: `rc products show <product-id> --store-state`). Never infer store prices, availability, or trials from `get-product`, `list-products`, or offering data — those are RevenueCat catalog, not store state. Surface the response's `warnings`.

## Prerequisites

Store-state writes require store credentials connected to the RevenueCat project (an App Store Connect API key, or a Google Play service account with the **Manage store presence** permission) and a RevenueCat login with write access to the project. If a write fails with a credentials or permission error, report what is missing and how to fix it (dashboard app settings for store credentials) instead of retrying.

## Confirm before applying

Apply writes to production stores and can change what live customers see and pay. **Never call apply until you have shown the planned diffs and the user has explicitly confirmed.**

After planning succeeds:

1. Summarize `summary` and each `plan_items[*].diff` in plain language (before → after per field).
2. Report every warning (`severity`, `field`, `message`). Never apply if any `plan_items[*].warnings` has `severity: blocker`. Fix the desired state, update the plan, and re-plan until there are no item-level blockers.
3. Optionally share the dashboard review URL:
   `https://app.revenuecat.com/projects/{project_id}/product-catalog/product-editor/review-changes?plan_id={plan_id}`
4. Wait for an explicit go-ahead. Confirm each product's change individually or as one clearly itemized batch — never fold unrelated changes into a single confirmation.
5. Only then call apply, and only if `actions` includes `apply`.

Reads do not need confirmation. Submitting products to Apple for review is a separate confirmed write (`submit-products-to-store`).

## Recommended write flow (MCP)

1. **Inspect first.** `get-product-store-state` on existing products before deciding the desired changes.
2. **Create a draft plan.** `create-product-store-state-plan` with one `desired_states` entry per product.
   - Target an existing RevenueCat product with `product_id`, or pass `create_revenuecat_product` (`app_id`, `store_identifier`, `type`, `display_name`, and `title` — when the user gave only one name, use it for both).
   - Set `store` to `app_store`, `play_store`, `rc_billing`, or `test_store` and populate the matching `store_state`.
   - Put prices, availability, localizations, and (if the user provided one) the review screenshot in the desired state. Do not call `create-product-prices`, `upload-product-store-state-screenshot`, or `equalize-subscription-prices`.
   - App Store subscriptions: send the prices to keep in `territory_prices` and include `common.pricing.equalize_missing_subscription_prices` with that `base_territory` so missing Apple territories are filled at apply. Do not send that field for App Store one-time products.
   - App Store review screenshots: omit screenshot so apply can upload a blank placeholder unless the user supplied an image.
   - RC Billing / Test Store: pricing is `common.pricing.currency_prices` (create-only; updating an existing currency is rejected).
3. **Plan.** `plan-product-store-state-plan`, then poll `get-product-store-state-plan` until status is `planned`, `planned_and_finished`, or `plan_errored`.
4. **Review with the user.** Follow [Confirm before applying](#confirm-before-applying). If planning failed, report `error_message` / per-item errors and the review URL; do not apply.
5. **Apply.** `apply-product-store-state-plan`. Then poll `get-product-store-state-plan` until `applied` or `apply_errored`. Report per-product `apply_status` and any `apply_error_message`. If apply fails because the store changed after planning, tell the user and start a new plan from the fresh state.
6. **Submit for review when ready.** App Store only: after apply succeeded, the change is in App Store Connect but not yet submitted to Apple. Offer `submit-products-to-store` for the products just applied (confirmed write). Skip for Play Store, RC Billing, and Test Store.

To abandon a draft or planned plan, `discard-product-store-state-plan`. To change a draft, `update-product-store-state-plan` then plan again.

## CLI equivalents

See the `revenuecat-cli` skill for install, auth, and schema discovery. Mapping:

- Read: `rc products show <product-id> --store-state`
- Create + compute diff: `rc products store plan <app-id> --file <csv|json>`
- Re-display a saved plan: `rc products store show <plan-id>`
- Apply / discard: `rc products store apply <plan-id>` / `rc products store discard <plan-id>`

CLI apply waits for completion (no separate poll). Still show the plan diff and wait for confirmation before `apply`. Confirm exact flags with `rc commands --schemas --json`.

## Do not use these MCP tools for writes

These may still appear in the MCP catalog. They write one product with no previewable plan. Prefer the plan tools above.

- `set-product-store-state`
- `get-product-store-state-operation`
- `create-product-prices`
- `upload-product-store-state-screenshot`
- `equalize-subscription-prices`
