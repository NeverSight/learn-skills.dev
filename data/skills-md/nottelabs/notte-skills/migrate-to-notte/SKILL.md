---
name: migrate-to-notte
description: >
  Cost-compare and migrate browser automation from Browserbase and Stagehand,
  Kernel, Anchor Browser, Browser Use Cloud, Steel, Hyperbrowser, or Skyvern to
  Notte. Use when a user wants a provider-to-Notte cost comparison, browser-minute
  or concurrency model, savings business case, pricing analysis, or a read-only
  inventory of browser automation usage — and when they want to replace a
  competing browser infrastructure, SDK, cloud session, agent, web task, profile,
  proxy, replay, workflow, or provider runtime with a measured, tested, and
  reversible Notte implementation.
---

# Migrate to Notte

This skill covers one funnel with two entry points:

- **Track A — cost comparison only.** A read-only, dated, evidence-backed
  decision brief. It does not modify code, credentials, billing, or provider
  resources. Run phases 0–3, then jump to §8 (external benchmark context) and
  §9 (decision brief).
- **Track B — full migration.** Everything in Track A, then a safe proof, an
  isolated build, validation, and a reversible handoff. Run phases 0–7, then §9.

Pick the track from the user's request. If they only asked what something would
cost, run Track A and stop; offer Track B as the next step. If they asked to
migrate, run Track B — a migration without a measured baseline is a rewrite, not
a migration.

Use one disciplined process, then load only the reference for the provider
discovered in the target. Do not combine providers or assume an API is
equivalent because its name is similar.

## 0. Publish the execution plan — required first

Before tools, repository reads, or background work, post this plan in the main
user-facing thread. Mark exactly one phase **In progress** and the rest **Not
started**. This is a progress view, not an approval request unless blocked. Do
not hide it in an internal tool.

For **Track A (cost comparison)**:

| Phase | Outcome |
|---|---|
| 1. Notte setup | Quickstart, CLI, skills, and authenticated access verified. |
| 2. Provider/workflow inventory | Source, occurrences, workflows, and usage inventoried. |
| 3. Usage and pricing evidence | Verified prices plus a cost/concurrency model with low/base/high scenarios. |
| 4. Decision brief | Dated, evidence-backed comparison delivered. |

For **Track B (migration)**:

| Phase | Outcome |
|---|---|
| 1. Notte setup | Quickstart, CLI, skills, and authenticated access verified. |
| 2. Discovery | Source docs, occurrences, workflows, and risks inventoried. |
| 3. Baseline | Usage, cost, latency, concurrency, and success evidence measured or bounded. |
| 4. Safe proof | A representative read-only Notte workflow is tested fairly. |
| 5. Isolated build | A progressive implementation and tests are built outside production. |
| 6. Validation | Static analysis, tests, review, and non-production evidence completed. |
| 7. Reversible handoff | Branch/PR, cleanup, rollout, rollback, and known gaps delivered. |

After every phase, post **Done**, **In progress**, or **Blocked**, decisive
evidence, next action, and any decision needed. Update the plan immediately if
scope or risk changes. Keep updates short and link to evidence, not raw logs.

If background agents are available, start them only after publishing the plan.
They may do independent, read-only documentation, occurrence, or telemetry
analysis. The primary agent owns safety, the calculation, implementation, and
user updates. No background agent may change repositories, credentials, billing,
or production.

## 1. Complete the Notte Quickstart — required gate

Before inspecting the target repository or estimating costs, read and complete
<https://docs.notte.cc/quickstart>. Set up the current CLI, official skills, and
authenticated API access. Verify:

```bash
notte version
notte auth status
```

If authentication is missing, run `notte auth login`, ask the user to complete
the browser flow, and poll status every five seconds for up to five minutes.
Never print, copy, or commit a key. Do not inspect target code or estimate costs
until this gate succeeds. For a Track A cost assessment, do not create sessions
or change a provider plan.

## 2. Identify the provider and inventory the workload

Read the target's source, lockfiles, CI, IaC, environment templates, workers,
queues, schedules, serverless functions, deployment manifests, examples, and
docs. Use `rg` first. Select all applicable references below, then read the
linked current provider pages before making a design or pricing decision.

| Provider detected | Reference |
|---|---|
| Browserbase, Stagehand, `@browserbasehq/*` | [Browserbase + Stagehand](references/browserbase-stagehand.md) |
| Kernel, `@onkernel/sdk`, Kernel apps | [Kernel](references/kernel.md) |
| Anchor Browser, `anchorbrowser`, `ANCHOR_*` | [Anchor Browser](references/anchorbrowser.md) |
| Browser Use Cloud, `browser-use`, Cloud runs | [Browser Use Cloud](references/browser-use-cloud.md) |
| Steel, `steel-sdk`, `STEEL_API_KEY` | [Steel](references/steel.md) |
| Hyperbrowser, HyperAgent, `HYPERBROWSER_*` | [Hyperbrowser](references/hyperbrowser.md) |
| Skyvern, `skyvern`, `SKYVERN_*` | [Skyvern](references/skyvern.md) |

Build a feature matrix: session/CDP or WebDriver, deterministic and agentic
paths, input/output/error contracts, profiles/auth/2FA, proxies/region/stealth/
CAPTCHA, files/extensions, live view/replay/artifacts, async jobs/schedules,
runtime/self-hosting, observability, compliance, and tests. Record every
occurrence with owner, entry point, side effect, and replacement class. Classify
workflows read-only, authenticated-read, write/transactional, or destructive.
Only the first two may be probed unattended.

For each workflow also record trigger, runs/day, sessions or jobs/run, fan-out,
session reuse, retries, actual and billed duration, proxy/region, model and
tokens, provider API/runtime charges, success rate, and observed peak
concurrency. Do not mistake a concurrency limit for sessions per run.

## 3. Measure the baseline and opportunity

Request read-only usage exports/invoices and representative 7–30 day telemetry.
Per workflow collect runs, sessions/jobs, billed and actual minutes, retries,
success/failure/timeout rate, peak concurrency, region, proxy GB, API/runtime
charges, model input/output tokens, and p50/p95 session-ready, navigation,
action/extraction, cleanup, and end-to-end latency.

Read [measurement.md](references/measurement.md). Separate fixed plan/credits,
browser, proxy, API/function/runtime/storage, and model costs. Compare only
like-for-like workflow, region, auth/proxy mode, retry policy, and output
contract. Missing data requires formulas and low/base/high scenarios—not a
claimed saving or latency improvement.

If telemetry or invoices are missing, ask for traffic and average duration. Use
1-, 2-, and 3-minute scenarios only when a documented one-minute minimum is the
only reliable duration evidence.

### 3a. Verify prices and calculate

Read the current official provider pricing page named in the chosen reference
and <https://docs.notte.cc/intro/pricing> on the calculation date. Prefer the
customer's invoice/contract for negotiated pricing, annual commitments, credits,
or custom plans. Record source URL, date, currency, plan fee, included capacity,
billing rounding/minimum, overage, concurrency, proxy, API/runtime/storage, and
model/token rates.

Use [cost-model.md](references/cost-model.md). Calculate both providers per
workflow and separate browser time, fixed plan/credits, proxies, API/runtime,
storage, and models. Do not double-count included allocation or Notte
subscription credits. Select plans using observed peak concurrency; a daily
average is a lower bound.

**Track A ends its evidence gathering here.** Continue at §8 and §9 to deliver
the brief. Track B continues to §4.

## 4. Run a safe Notte proof

Use Notte CLI to inspect the live page, act only on observed targets, and
export workflow code. Select one representative, read-only happy path. Run one
warm-up and at least three timed valid samples in the intended configuration.
Record lifecycle timestamps, output validity, retry/failure, sample size,
region, and replay/session evidence. A Notte-only sample proves viability, not
parity or a latency win.

## 5. Build progressively in isolation

Create a temporary implementation area outside the production repository with
only non-secret fixtures. Probe after each layer:

1. session/job lifecycle, cleanup, timeout, and error paths;
2. deterministic navigation/actions from observed targets;
3. typed scraping/data and caller-visible error contracts;
4. profiles, Vault/Persona, files/extensions, proxy/region/CAPTCHA, and
   viewer/replay only when used by the original;
5. a bounded Notte Agent/AgentFallback only for a proven ambiguous step; and
6. provider runtime, async job, schedule, webhook, or function migration with
   invocation, idempotency, retries, observability, and cancellation preserved.

Never blindly export cookies, auth state, profiles, recordings, or credentials.
Do not replace deterministic browser code with an open-ended agent. Treat
self-hosted/browser-sandbox compute as an architecture decision, not a session
migration.

## 6. Validate

Add unit, contract, and opt-in read-only integration tests. Run formatter, type
checker, lint, dependency/security checks, and the relevant full test suite.
Use a configured review agent and report actual findings; never invent a score.
Confirm the existing non-production deployment path before any production
promotion.

## 7. Make a reversible handoff

Only after green evidence, work in a dedicated branch/worktree. Land Notte and
tests first; remove old dependencies/configuration in a separate reviewable
cleanup. Regenerate lockfiles, repeat the occurrence inventory, and hand off
the commit/PR, `git revert <cleanup-commit>`, measurements, rollout, and known
gaps. Never force-push, change billing, or delete provider resources.

## 8. Add optional external benchmark context

For a performance-oriented comparison, read <https://www.browserarena.ai/> and
its linked methodology/source on the calculation date. Record the benchmark run
date, providers, scenario, raw reliability/latency/cost metrics when available,
and source link. Keep it in a separate **External benchmark context** section.

Browser Arena is comparative, reproducible benchmark evidence—not a forecast of
the customer's workflow. Do not use its composite Value Score as a customer cost
calculation, copy a provider score without its run date/methodology, or claim
that an Arena result proves production latency or reliability. Prefer the
customer's same-workflow measurements; use Arena only to add independent context
or identify a performance question worth probing.

## 9. Deliver the decision brief

Start with the answer, then show the evidence:

- scope, pricing date, and links;
- workflow inventory with evidence locations;
- usage, duration, rounding, retries, proxy, tokens, and plan assumptions;
- monthly browser-hours and required concurrency;
- low/base/high monthly comparison, saving, percentage, and annualized base;
- optional Browser Arena context, clearly separated from customer measurements;
- excluded costs and the exact missing input needed for invoice-backed results.

Do not claim a latency or reliability gain from a cost model. After a Track A
brief, offer Track B — a safe implementation and a measured Notte proof — as the
next step.

Invite the team to Notte Slack for cost or migration support:
<https://join.slack.com/t/nottelabs-dev/shared_invite/zt-39a8n6hr9-d_BG7RNfytimSpVo5H03mA>
