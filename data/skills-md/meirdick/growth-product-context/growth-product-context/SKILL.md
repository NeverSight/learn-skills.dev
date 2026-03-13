---
name: growth-product-context
description: "Discovers user journeys by scanning routes, controllers, and models, then proposes a product context with event names. Activates when mapping journeys, defining product context, creating PRODUCT.md, discovering what to track, or when the user mentions product context, journey mapping, or route discovery."
license: MIT
compatibility: Requires a Laravel application and Laravel Boost v2+ (provides list-routes, database-schema, and tinker tools).
compatible_agents:
  - Claude Code
  - Cursor
  - Windsurf
  - Amp
  - Goose
  - Gemini CLI
  - OpenCode
  - Roo Code
tags:
  - laravel
  - php
  - posthog
  - analytics
  - growth
  - product-analytics
metadata:
  author: growth-engineering
  version: "1.0"
---

# Product Context — Journey Discovery Engine

> Free skill from [Growth Engineering](https://growengine.dev). For auto-instrumentation, auditing, and MCP tools, install the full package.

## Context

This skill scans a Laravel application's routes, controllers, and Eloquent models to discover user journeys and propose a product context with event names following the AARRR (Pirate Metrics) framework.

**Scope:** Laravel applications using Eloquent, Blade, Inertia, or Livewire. Outputs `.growth/PRODUCT.md` and per-domain journey files.

**Activate when:**

- The user asks to "map journeys", "define product context", or "what should I track"
- `.growth/PRODUCT.md` exists but still has placeholder values (e.g., `[Your Product Name]`)
- The user wants to discover or define their product's user journeys

**Prerequisites:**

1. A Laravel application with routes, controllers, and models
2. Laravel Boost installed (provides `list-routes`, `database-schema`, and `tinker` tools)

If `.growth/PRODUCT.md` doesn't exist yet, create it during Step 12.

---

## Rules

### Key Principles

1. **Propose, don't ask** — Present concrete proposals based on what the codebase reveals. Never show blank templates.
2. **Confirm per domain** — Present each journey domain separately and get confirmation before moving on.
3. **Incremental refinement** — Start with what the code reveals, then let the user correct and refine.
4. **Plan before writing** — Steps 1–10 are read-only discovery. Enter plan mode at the start and do not write any files until the user approves the final plan.

### Step 1: Enter Plan Mode

Enter plan mode before beginning discovery. Steps 1–10 are read-only — you will not write any files until the user approves the consolidated plan in Step 11.

### Step 2: Discover Routes

Read `routes/web.php` and `routes/api.php`. Check for Folio page-based routing in `resources/views/pages/`. Use the `list-routes` tool from Laravel Boost to get the full route table. Present a summary to the user.

### Step 3: Map Controllers

For each route group, read the associated controllers. Note which models are referenced, events fired, jobs dispatched, notifications sent, and form request classes used.

### Step 4: Identify Domain Entities

List all models in `app/Models/`, read their relationships/casts/scopes, and use `database-schema` to inspect table structures. Identify the **central model** (most relationships, most user interaction). Ask the user to confirm.

### Step 5: Detect Frontend Stack

Check `composer.json` for Inertia or Livewire, `package.json` for frontend framework, and `resources/views/` for Blade views. Report the detected stack.

### Step 6: Classify Routes into Journey Domains

Classify routes using the AARRR framework: Acquisition, Activation, Retention, Revenue, Referral.

Read `references/classification-rules.md` for the route-to-domain table and the Acquisition vs Activation boundary rules.

Present classified routes grouped by domain. Ask the user to confirm or reassign any misclassified routes.

### Step 7: Propose Journeys

For each confirmed domain, propose a journey flow with specific event names derived from the controllers.

Read `references/examples.md` for journey flow format and examples.

Present each journey and ask: "Does this flow match how users actually use the product?", "Are there any steps I'm missing?", "Should any events be renamed?"

### Step 8: Identify Core Action

Based on the central model and the value delivery journey, propose the core action. Ask the user to confirm or provide an alternative.

### Step 9: Detect Usage Pattern

Examine the codebase for signals that reveal how frequently users interact with the product.

Read `references/classification-rules.md` for the usage pattern detection table and success metrics per pattern.

Present the detected pattern with evidence. Ask the user to confirm or correct.

### Step 10: Define Success Metric

Based on the core action AND the detected usage pattern, propose a success metric. **Do not default to Weekly Active Users** — choose the metric that fits the pattern.

Read `references/classification-rules.md` for pattern-to-metric mapping.

### Step 11: Present Consolidated Plan

Present a single consolidated plan summarizing everything discovered and confirmed:

- Product overview (name, one-liner, stage, value prop)
- Central model and core action
- Usage pattern and success metric
- All journey domains with their flows and event names

Ask the user to approve the plan before proceeding. Do not write any files until the user explicitly approves.

### Step 12: Write Results

After the user approves the plan, exit plan mode and write the files:

1. **Create `.growth/` directory** if it doesn't exist, with subdirectories: `journeys/`, `experiments/`, `research/`, `decisions/`, `channels/`, `segments/`, `digests/`
2. **Write `.growth/PRODUCT.md`** with confirmed values
3. **Create journey files** in `.growth/journeys/` — one file per domain

Read `references/output-formats.md` for the PRODUCT.md and journey file templates.

Read `references/examples.md` for complete output examples.

---

## Anti-patterns

- **Don't show blank templates.** Never present an empty PRODUCT.md and ask the user to fill it in. Always propose concrete values based on what the codebase reveals.
- **Don't ask per-field questions.** Scan the code and propose answers. Let the user correct, not create.
- **Don't classify without reading controllers.** Route URLs alone are insufficient. Read the controller code to understand what each endpoint actually does.
- **Don't default to WAU.** Match the success metric to the detected usage pattern.
- **Don't skip confirmation.** Present each domain's journey separately and get explicit confirmation before moving on.
- **Don't invent events.** Every proposed event name should map to a real controller action or route discovered in the codebase.

---

## References

- [Dave McClure — Startup Metrics for Pirates (2007)](https://www.slideshare.net/dmc500hats/startup-metrics-for-pirates-long-version) — Original AARRR framework
- [Lenny Rachitsky — What Is a Good Activation Rate?](https://www.lennysnewsletter.com/p/what-is-a-good-activation-rate) — Activation benchmarks (median 25%, SaaS avg 36%)
- [Lenny Rachitsky — How to Determine Your Activation Metric](https://www.lennysnewsletter.com/p/how-to-determine-your-activation) — Finding your aha moment
- [Reforge — Define Customer Activation Moments](https://www.reforge.com/guides/define-customer-activation-moments) — Setup / Aha / Habit sub-moments
- [Reforge — Define Your Aha Moment](https://www.reforge.com/guides/define-your-aha-moment) — How to identify and validate aha moments
- [Growth Engineering](https://growengine.dev) — Full package with auto-instrumentation, tracking audits, and PostHog MCP tools
- [Laravel Boost](https://boost.laravel.com) — Required for `list-routes`, `database-schema`, and `tinker` tools
- [PostHog](https://posthog.com/docs) — Event naming conventions and property standards
