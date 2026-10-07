---
name: revenuecat-experiment-analysis
description: Use when the user asks to analyze or understand a RevenueCat experiment or its results.
---

To analyze an experiment, follow the following steps. Make sure to execute all steps in this order, do not skip any. More details on the step below. If you already have partial information (eg. the experiment ID), you may skip that step only. Continue following all of the other steps. Within a step, issue independent calls together so they run in parallel.

1. Get the experiment ID
2. Get experiment details
3. Get supporting chart data [DO NOT SKIP]
4. Get experiment results
5. Interpret results
6. Report your overall findings

# Step 1: Get the experiment ID

If you don't have the experiment ID yet, find it using the `list-experiments` RevenueCat tool. It receives a single parameter: `project_id`, which requires the `proj...` Project ID. You can also pass a `status` filter (`draft`, `running`, `paused`, `stopped`).

# Step 2: Get experiment details

## Step 2a: Experiment setup

Get the experiment setup / metadata by using the `get-experiment` RevenueCat tool. Parameters: `project_id` (as above) and `experiment_id` (from step 1). Pass the following values to the `expand` parameter: `offering.package.product.indicative_price` and `offering.paywall`.

Relevant information to extract:

- Offerings (offering_a, offering_b, ...): these define the variants of the experiment. More sophisticated setups might also include a `placements` object which defines different offerings per placement (eg. onboarding, feature gate, ...). Offerings include details on the products offered. Products include an `indicative_price`. Note that only USD prices for the US are returned to provide an understanding of overall pricing levels. Any introductory price is not returned. For price localization tests, tests scoped explicitly outside of the US, or introductory prices, this will not provide the full picture, you might have to resort to the `get-product-store-state` tool instead (see the `revenuecat-store-state` skill). Offerings may also include a `paywall_id`, if the offering uses a RevenueCat Paywall. If `paywall_id` is `null`, that means the app is using a custom paywall.
- Product fields are RevenueCat catalog data, not store state: `indicative_price` and the `subscription` fields (`trial_duration`, `duration`) reflect what RevenueCat last synced from the store and can be stale. Before presenting a trial, intro offer, or price from these fields as fact, or flagging one as an experiment confound, confirm with `get-product-store-state` and cross-check the results' trial metrics.
- notes: Any notes that were provided about the experiment
- display_name: Name of the experiment
- targeting_conditions: the experiment only applies to customers meeting these conditions
- enrollment_mode: defines whether only new customers are enrolled (default) or whether this experiment also applies to existing customers
- experiment_type: what kind of experiment this is (user selected out of a predefined list)
- primary_metric, secondary_metrics: primary and secondary success metrics as set up when creating the experiment.
- Status:
  - `draft` means the experiment has not yet started, and there are no results yet.
  - `running` means the experiment is still actively enrolling new customers.
  - `paused` means the experiment is no longer enrolling customers, but already-enrolled customers are still assigned to their variant, and the experiment is continuing to collect data for up to 400 days. The experiment can be resumed to continue enrolling new customers.
  - `stopped` means the experiment is no longer enrolling customers, and already-enrolled customers have gone back to being served their default offering. Results continue to refresh for up to 400 days. The experiment can no longer be started or resumed.

## Step 2b: Paywalls

For any paywall_id in any offering of the experiment, use the `render-paywall-screenshot` tool (parameters `project_id`, `paywall_id`, `version: "published"`) to look at the paywall and understand the differences. Pass `version: "published"` so you see what customers were served; the tool defaults to the draft, which may contain unpublished edits. Skip this step if every offering uses a custom paywall (`paywall_id` is `null`).

# Step 3: Get supporting chart data

Pull recent chart data scoped to the experiment's runtime, using the `get-chart-data` RevenueCat tool. Do not skip this step, it provides valuable context to how the app was performing overall in the time frame.

Parameters:

- project_id: {project_id}
- chart_name: revenue
- start_date: {experiment_start_date}
- end_date: {experiment_end_date}, or today if still running
- resolution: week (or day if < 2 weeks running)

Also pull data for chart_name :

- conversion_to_paying — overall conversion trend during experiment
- trials_new — trial volume trend
- trial_conversion_rate — trial-to-paid during experiment
- initial_conversion – Initial conversion rate (conversion from install to trial, upfront subscription, or one-time purchase)

# Step 4: Get experiment results

Get the experiment results (so far) using the `get-experiment-results` RevenueCat tool.
Parameters:

- project_id
- experiment_id
- platform (optional), filter results by platform, eg. `ios`
- country (optional), filter results by country, eg. `us`
- exposure_status (optional), filter experiment results by paywall view status. Use `exposed` for customers who viewed a paywall or `not_exposed` for customers who did not view a paywall. Omit this parameter to include all enrolled customers. This filter is available for both enrollment modes.

The results can include a metric named `Exposed customers`. Refer to it as `Paywall viewers` when talking to the user.

# Step 5: Interpret results

Understanding what changes were made in the experiment, now interpret the results. Use your best judgment.

If the user disputes a claim you derived from catalog metadata, verify it yourself with `get-product-store-state` rather than asking the user to check the store.

# Step 6: Report your overall findings

Report your overall findings back to the user, with links to the relevant charts and dashboard entities (see the `revenuecat-dashboard-links` skill).
