---
name: terra-models
description: Run Terra API health models (Sleep Window, Menstrual Cycle Tracker, Smart Fill) over a connected user's data for a date range to return ready-to-use wellness insights. Use when building with Terra API Models, the /v2/models or /v2/models/run endpoints, model_run pricing, or turning a user's Terra API data into a sleep-schedule, menstrual-cycle or gap-filled-metrics insight.
license: MIT
metadata:
  author: terra
  version: "1.1.0"
compatibility: Requires network access to docs.tryterra.co for full request and response schemas.
---

# Terra API Models

Run one of Terra API's health models over a connected user's data for a date range and get a ready-to-use insight back: one request in, one insight out. No model to host. Every model is a **wellness indicator, not a medical or diagnostic tool**; never present its output as clinical.

## From the terminal

Account configuration lives in the [Terra dashboard](https://dashboard.tryterra.co), which an agent cannot click. The `terra` CLI does the same from a terminal, and Models has generated commands of its own, including the run log that says why a run did not return what you expected:

```sh
terra models catalog list                                           # the models available, account-wide
terra models runs list --env <dev-id> --status error                # failed runs
terra models runs list --env <dev-id> --user-id <uuid> --model <model>
terra models runs list --env <dev-id> --run-id <run_id>             # one run, by id
```

Two things about that log. It holds **30 days** by default, so an older run is not there and an empty page is not evidence a run never happened. But `--run-id` widens the lookup to the full retained history, so a run you have an id for is never cut off by the window.

Because a run costs a credit whether or not it returns an insight, `runs list --status error` is also the fastest read on credits being spent on runs that never produced anything.

Install it with `brew install tryterra/tap/terra` on macOS or `npm install -g @tryterra/cli` elsewhere. The `terra-cli` skill carries the guardrails (`--reveal` on anything returning a credential, `--yes` on anything destructive), the exit codes, and a playbook per task. It administers the integration; it does not replace the API calls this skill describes.

## When to use this

Building anything that calls `GET /v2/models` or `GET /v2/models/run`, prices `model_run` usage, or turns a user's Terra API data into a sleep-schedule, menstrual-cycle, or gap-filled-metrics insight.

## Connect the user first

Models run for a user you have connected through the Unified API (see the `terra-unified-api` skill), over a date range you choose. A model cannot always return an insight for a given user and range; when it cannot you get either an unsupported result or an error, and the run still costs a credit either way (see Reading the result and Pricing).

## The three models (generally available)

| `model` id            | Returns                                                                                                                                       | Needs                                                           |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| `sleep_window`        | A recommended bedtime, wake time and in-bed duration, a 0–100 consistency score with a band, and the single change that would most improve it | Overnight sleep sessions from across the user's history         |
| `cycle_phase_tracker` | A per-day menstrual cycle phase, plus the period onsets and fertile windows detected in overnight physiology, each with a confidence band     | At least 30 days of overnight sleep carrying heart rate and HRV |
| `graph_impute`        | Smart Fill: one day's metrics for a chosen table, marking which the device recorded and which the model reconstructed                         | Recorded history for that user in the table you ask for         |

**`sleep_window`, `cycle_phase_tracker` and `graph_impute` are GA** and documented. Treat any other model id as pre-GA and unstable: it may be runnable, but its response shape can change without notice.

`cycle_phase_tracker` is a wellness indicator, **not a medical or contraceptive tool**, and it detects onsets from physiology alone – it neither needs nor reads a user's logged period dates.

## Making a run

`GET https://api.tryterra.co/v2/models/run`

Query params: `model`, `user_id`, `start_time`, `end_time` (all ISO 8601). Headers: `x-api-key` and `dev-id` (your own keys; this is not a privileged endpoint).

**`graph_impute` needs one more param: `table`, one of `sleeps`, `dailies` or `activities`.** The endpoint refuses the run without it rather than choosing a table for you, so a request built from the generic param list alone returns `400`. The three tables carry different metrics.

```bash
curl --request GET \
  'https://api.tryterra.co/v2/models/run?model=sleep_window&user_id=USER_ID&start_time=2026-04-01T00:00:00Z&end_time=2026-07-01T00:00:00Z' \
  --header 'x-api-key: YOUR_API_KEY' \
  --header 'dev-id: YOUR_DEV_ID'
```

Fetch https://docs.tryterra.co/models/models.md for the exact params and the full per-model response schema before you build request or response types; the response shape differs per model and evolves.

## Reading the result (the part agents get wrong)

- **Unsupported device is a 200, not an error.** When the user's device or provider cannot produce the model, the run returns HTTP 200 with `unsupported: true` (plus `unsupported_reason` and `supported`/`supported_devices`) in place of an insight. Handle that as a normal outcome and surface it to the user, not as a failure.
- **A genuine error is a real error.** Bad or missing inputs return `4xx`, and a run that cannot be computed (for example too little data in the range) can return `5xx`. These come back as RFC 7807 problem+json (`title`, `detail`, and `errors[]` for validation), for example `400 unknown model`, `404 invalid user id`. This is not the graceful `unsupported` case above; do not swallow it.
- **Every run bills, including failures.** A run is metered before it computes, so an unsupported or errored run still costs a credit. Validate the model id, the user, and that the device is supported up front rather than probing blindly.
- **Empty is not always `unsupported`.** `sleep_window` uses `unsupported`/`unsupported_reason` for a device it cannot serve and `no_data`/`no_data_reason` for a user it has too little history for. `cycle_phase_tracker` only ever uses `no_data`/`no_data_reason`. Handle both keys; do not branch on `unsupported` alone.
- **The shape is per-model.** `sleep_window` returns a `window` object (`recommended_bed`/`recommended_wake` are local clock times; `approximate: true` means the schedule was estimated from limited history), a `sleep_regularity` object (`score` 0–100 and a `band` of Low/Fair/Good/Excellent), and, unless the user is already consistent, a `recommendation` object (`change`, `reason`, `moves_to`, `gain`) naming the single biggest change that would raise the score. `cycle_phase_tracker` returns `results` plus `periods` and `fertile_windows`. `graph_impute` returns `table`, `features` and `results`.
- **`sleep_window` ignores the range you pass.** It reads the user's whole sleep history, so `start_time` and `end_time` do not change its answer. Do not build a UI that implies picking a window changes the schedule.
- **`cycle_phase_tracker`'s `results` is not a list of answers.** It carries one row per calendar day of the range you asked for, **including days the model had no data for** – so `results.length` is never a coverage signal. Branch on each row's `available`. Read the `*_confidence` bands (low/medium/high), never a raw probability, and note a period day is never also a fertile day.
- **For `graph_impute`, `computed` and `reported` are the whole point.** Each entry in a day's `fields` carries `reported: true` if the device actually recorded the value and `computed: true` if the model reconstructed it, with a `confidence` on the reconstructed ones. Never present a computed value as recorded.
- **The response's `data_type` is not the catalog's `data_type`.** The catalog reports the data a model reads (`sleep_window` → `sleep`); a run response reports its own value (`sleep_window` → `sleep_window`). Do not assert one from the other.
- **`truncated: true`** means the run hit the per-request data cap; the insight is still valid but computed over a bounded slice of the range.
- Model outputs are modest-confidence indicators. Do not present a single result as authoritative.

## Pricing

Usage-based: **$0.01 per model run**, drawn from your plan's monthly credit allowance. One run is one model over one user for one date range, regardless of how much data the range covers; running two models, or the same model on two users, is two runs. A run started from the Terra Dashboard and one made through this API bill through the identical path. Details: https://docs.tryterra.co/unified-api/pricing

## Boundaries

- **Not the Unified API.** Connecting users, webhooks, and historical data are the Unified API (`terra-unified-api`); a model run analyzes a connected user's data and returns an insight.
- **Not Health Scores.** Health Scores are continuous physiological scores; Models return a discrete, on-demand insight from a single call.
