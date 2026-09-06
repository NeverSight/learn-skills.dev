---
name: next-chunking-optimizer
description: >
  Optimize production JavaScript chunking, initial route load, and repeated
  client navigation in Next.js 16.3.0 or later in App Router
  repositories building with Turbopack. Use when asked to tune experimental
  Turbopack chunking, reduce critical JavaScript, or compare chunking behavior.
  Present measured variants for approval before retaining a change.
---

# Next.js Chunking Optimizer

Compare Turbopack chunking variants through reproducible browser experiments. Present the results before asking the user to approve a configuration change.

## Instruction Precedence & Transparency

- The user's instructions take precedence over guidelines provided in this skill. If explicit user instructions conflict with this skill's instructions, prioritize the user's instructions.
- A request to run this skill or optimize chunking authorizes temporary configuration edits, production builds, and browser measurements. Complete these experiments without pre-approval, then restore the control configuration.
- **Keep a variant as the final configuration only after the user has reviewed the results and exact delta and explicitly approved that variant.** This approval is for retaining the change; it does not block temporary test edits. Ask at the end of the comparison, then wait with the control restored. Selecting the target app, a preselected recommendation, or silence is not approval. Honor approval already given for the same measured variant and delta; do not ask again.
- If this skill causes you to ask for permission or confirmation, pause, leave requested work unfinished, or diverge from the user's intent, name and link to the exact SKILL.md file you read, quote the relevant instruction, and briefly explain how it applies. Distinguish explicit skill requirements from your interpretation of guidelines.

## Execution Mode & Completion

After the minimum-version check passes, the default is to **run the experiments**: inspect the app, build the current control, measure it, test supported configuration variants, restore control, and present the comparison for approval. The read-only setup steps are preparation for this workflow.

- Use analysis-only mode when the user explicitly limits the task to inspection or planning, or forbids the temporary changes or execution needed for experiments. Quote that limiting instruction when explaining why experiments were not run. Requiring permission before retaining a variant does not impose analysis-only mode.
- A normal completed run includes a fresh production baseline, at least one meaningfully different supported configuration variant, browser measurements for the declared journeys, and a final comparison table. Static bundle statistics, an import audit, and proposed future tests are preparatory findings.
- If execution is blocked, report the concrete failed command or missing prerequisite, what was attempted, and the smallest input needed to continue. Label the experiment incomplete. An absent or stale build means a new baseline build is needed; it is not itself a blocker.

## Core Invariants

- **Minimum version**: Requires Next.js 16.3.0 or later. Below 16.3.0, stop after identifying the target and its version. Do not analyze routes, imports, or bundles, run builds or experiments, or offer an analysis-only fallback. This applies even to analysis-only requests. Exactly 16.3.0 passes this version check.
- **Eligibility**: The target must use App Router and Turbopack in production builds. Confirm each tested option against the installed schema and production build. Handle a concrete incompatibility or failed setup as described in Step 0.
- **In-Place & Non-Destructive (Default)**: Execute baselines and candidates sequentially in the current checkout. Restore control after each candidate, including failed builds or measurements. Preserve pre-existing edits. If the user explicitly requests isolation (e.g. worktree/checkout), the user's instruction wins.
- **Single-Variable Testing (Default)**: Default to one config option at a time. Only combine route priority, component chunking, and size thresholds into a single candidate if the user explicitly requests it; note the confounding when combined.
- **Statistical Rigor (Default)**: Default to a run count ($N \ge 3$) committed upfront. Report medians and observed minimum-to-maximum ranges—never single point estimates. Test cold loads and warm navigations separately. If the user asks for a quick/scout check, allow $N = 1$–$2$, label it as low-confidence scout, and do not present it as a verdict.
- **Browser-Centric Evaluation**: Base decisions on user-visible browser metrics (FCP, LCP, click-to-render timing, transferred bytes), not bundle visualization or chunk counts alone.

---

## Workflow

### 0. Inspect the Target & Setup

Perform these initial checks read-only, then continue to the production baseline:

1. **Select the target app using the request, context, and package/workspace metadata.** Check manifests and workspace declarations for Next.js apps. If one clear target is identified, proceed and state the selection briefly. If multiple plausible targets remain, show their paths, package names, and Next.js versions and ask which app to use. Keep this discovery limited to target and version identification; defer route, import, and bundle inspection until the version check passes.
2. **Check the minimum version before further analysis.** Resolve the version from the target's installed Next.js package, or its lockfile if dependencies are absent; a manifest range alone is not an exact version. Compare semantic versions against 16.3.0, including prerelease ordering. If below 16.3.0, stop immediately with the short blocker message below. Do not inspect the schema, fill out an experiment report, or run any later step. If the exact version cannot be established, request that missing information before proceeding.
3. Once the version passes, snapshot the target app's configuration and working diff, including its existing `experimental.turbopackChunking` block (or its absence). Treat that state as the control, not as the framework default. Record the target, selection basis, and considered alternatives in [experiment-rig.md](./references/experiment-rig.md).
4. Confirm the target app uses the App Router (its own `app/` directory, not the repo root).
5. Inspect the target app's production build and serve scripts (`cwd` is the target app directory, or `pnpm --filter <pkg>` from the root). Do not assume `next start`; use the script the target app declares (e.g. `opennextjs-cloudflare preview`). Confirm the task runner actually selects that app; some runners resolve to root tasks even from an app directory. Note when `turbopack.root` points above the app at the monorepo root.
6. Read the installed schema using [chunking-controls.md](./references/chunking-controls.md) before forming candidates. A missing or retyped option affects that candidate, not all other supported options.

For a version below the minimum, use this message in the user's language, with the detected version and the exact skill path. Do not add an audit, offer to bypass the blocker, or upgrade dependencies automatically:

> Blocked: this app uses Next.js {version}. [This skill](<exact SKILL.md path>) requires “Next.js 16.3.0 or later” for its chunking workflow. No analysis or experiments were run. Upgrade Next.js to a supported version, then run the skill again.

After the version check passes, if the router or configured production bundler is incompatible, report the evidence and the scope change needed. Otherwise attempt the declared production build and normal local setup. Verify Turbopack in its output. Resolve routine setup issues within the authorized scope. If build, serving, browser access, or authentication still fails, report that concrete blocker and continue independent work. Do not require a pre-existing verified production build before attempting one.

### 1. Map Routes & Classify Site

Scope this entire step to the target app selected in §0. Re-classify after selection; never carry a site type over from another app.

1. In the target app, identify critical entry routes, shared layout client components, dynamic imports, and heavy client libraries. Keep this inspection focused on choosing journeys and chunking hypotheses. Defer unrelated import or component refactors; complete the available configuration experiments first.
2. Classify the application using [site-types.md](./references/site-types.md) to determine:
   - **Primary Journey**: The route and load type (cold root load, deep link, or warm transition) to optimize.
   - **Guardrail Journeys**: Secondary routes or navigations that must not regress.
3. Prepare the experiment setup following [experiment-rig.md](./references/experiment-rig.md).

### 2. Establish Production Baseline

Measurement driver (optional): if `agent-browser` is installed, prefer it for serving checks, snapshots, hover-prefetch, clicks, and performance sampling. Run `agent-browser --help` and load its workflow via `agent-browser skills get core`. Otherwise use any available browser harness. Never block asking for install; the user's harness preference wins.

1. Build the current working tree with the control configuration and serve that production artifact from the target app (`cwd` is the target app directory, or `pnpm --filter <pkg>` from the root; use the target app's declared serve command). Preserve existing user edits. Old build reports can guide hypotheses, but cannot supply the baseline when their source differs from the current tree.
2. Run one setup pass through every selected journey before collecting samples. Verify authentication, current link selectors, visible readiness markers, and paint measurements using the preflight in [experiment-rig.md](./references/experiment-rig.md). Freeze the working measurement setup for the comparison.
3. Execute the primary and guardrail journeys for the pre-set run count (default $N \ge 3$; $N = 1$–$2$ only for user-requested scout checks). Keep setup failures separate from valid samples. If the measurement method changes, repeat the affected control and candidate samples under the same method.
4. Record medians and min–max ranges for:
   - FCP, LCP, and time-to-usable marker.
   - Total transferred and encoded JavaScript bytes.
   - Request count and waterfall structure. Label requests observed before readiness as such; timing alone does not prove they block rendering.

### 3. Propose & Test Candidates

Select single-variable hypotheses using the installed-schema snapshot from Step 0 and [chunking-controls.md](./references/chunking-controls.md). Derive each delta from the actual supported types. Apply deltas to the target app's `next.config.*` only.
- **Dashboards / SaaS**: Consider `generateComponentChunks: true` when it differs from control. An existing setting is not a new candidate or a proven improvement.
- **Content / Ecommerce**: Start with targeted `priorityRoutes` for critical entry points.
- **Size adjustments**: Test `minChunkSize` or `maxMergeChunkSize` only when initial graphs show fragmentation or oversized blocking chunks.

#### Candidate Plan (No Pre-Approval Needed for Reversible Tests)
State the planned candidates briefly, then execute them in the same run. For each candidate: apply its temporary delta, build and serve that candidate, measure the same journeys as control, then restore control immediately. Complete all planned candidates or record why an individual candidate failed or was skipped. These tests do not authorize retaining a candidate; request final approval in Step 4.

| Candidate | Exact Config Delta | Hypothesis | Target Journey | Planned Runs | Guardrails |
| :--- | :--- | :--- | :--- | :---: | :--- |
| Candidate 1 | `experimental.turbopackChunking: { ... }` | Explain hypothesis | Primary flow | $N$ | Guardrail routes |

#### Dashboard Navigation Measurement Protocol
When testing authenticated warm navigations:
1. **Pre-flight**: Serve candidate build; navigate to source screen in authenticated state.
2. **Prefetch window**: Record prefetch traffic separately. Trigger product link prefetch (e.g. hover/focus); wait for network idle plus settling window (150ms).
3. **Click & sample**: Clear resource-timing buffer; click real `<Link>`. Start timing in the browser's click event. Record document/script requests, transferred bytes, and time until the visible target marker renders. Verify client navigation rather than assuming zero document requests.

### 4. Restore, Report & Request Approval

1. **Restore and clean up**: Verify that only the experiment's changes were reversed and the recorded control is restored, including pre-existing chunking values. Stop experiment-owned servers and browser sessions. Complete this before requesting approval. Restoring source does not change a running candidate build.
2. **Present the comparison**: Show a short table of control and every attempted variant, the primary result, download cost, and guardrail outcome. Include failed or skipped planned variants with a status and reason; unavailable measurements are `—`, not zero. Keep medians, ranges, and sample counts visible. Link the full measurement report from [experiment-rig.md](./references/experiment-rig.md), with raw samples, failed attempts, setup, and exact deltas. The user must be able to assess the choice from the response itself.
3. **Recommend**: Name the best supported option and explain its tradeoffs. Distinguish repeatable byte savings from noisy timing differences. State that chunking options are experimental. If valid comparisons show no clear benefit, recommend keeping control and finish with no application change; approval is not needed to retain the existing configuration. If no candidate produced a valid comparison, report the experiment incomplete rather than concluding that no improvement exists.
4. **Request final approval**: If recommending a change, show its exact configuration delta and ask whether to apply that named variant. Briefly explain the approval requirement with a link to this skill and its quoted rule. Stop and wait for an explicit answer before Step 5. Do not turn a recommendation into a retained change automatically.

### 5. Apply & Verify

After the user approves a measured variant in Step 4 (or has already approved the same reported results and delta):
1. Confirm the current configuration still matches the measured control. If it changed while awaiting approval, preserve those edits and reassess the comparison. Apply only the approved delta to the target app's `next.config.*`.
2. Run the production build and verify type checking and linting scoped to the target app.
3. Perform a final smoke test on primary and guardrail routes.

Run tests appropriate to the approved change. Production builds and journey measurements are required for experiments; reserve additional linting, type checks, and final smoke tests for a retained change unless repository instructions require them earlier. When keeping control or waiting for approval, verify restoration without an extra production rebuild solely to close the report. Once required checks pass, repeat testing only for new changes, failures, or unresolved concerns.

### 6. Parallelization via Subagents

After the target passes the minimum-version check, when collaboration tools are available, delegate independent read-only work such as route mapping, installed-schema inspection, or results analysis if it could save time or improve quality.

Assign one agent to own configuration changes, production builds, serving, browser measurements, and control restoration. Run this experiment sequence one candidate at a time, including baseline and guardrail measurements. Do not run other builds or measurements on the same machine during a measured journey, even with separate checkouts or ports.

Messages that you send to other agents and your final answer may be read by a human, so ensure they are legible. Always put proper spaces between words and/or numbers.

### 7. Reporting Style

Use the user's language and short, direct sentences. Lead with the recommendation and the numbers that support it. Explain technical terms only when they help the decision. Put detailed logs and secondary metrics in the linked report. End with the approval request when a change is proposed, or state that control was kept when no candidate earned a recommendation.
