---
name: vendor-rip
description: "Scan, assess, plan, and replace SaaS tools with AI-built code. Analyzes your codebase for SaaS integrations, generates migration plans, executes replacements, and validates results."
---

# vendor.rip Agent Skill

> Scan, assess, plan, and replace SaaS tools in any codebase.
> Works with any AI agent: Claude Code, Cursor, Windsurf, or any tool with codebase access.

## Version & Prerequisites

- Skill version: 0.1.1
- Spec: `design/agent-skill-spec.md` v0.1.1
- Requires: file system access, code search, web search, package installation (npm install, pip install, etc.), code generation, command execution
- Optional: tool profiles in `profiles/{tool}/` for enriched analysis

## Quick Start

Three entry points:

- **Scan**: `vendor-rip scan <tool>` — deep assessment of one tool
- **Discover**: `vendor-rip discover` — find all rippable SaaS in this codebase
- **Plan**: `vendor-rip plan <tool>` — generate migration plan (runs scan first if needed)

## How This Skill Works

This skill follows a five-step journey:

```
┌─────────────────────────────────────────────────────────────┐
│  ○ Scan   ○ Plan   ○ Execute   ○ Validate   ○ Done        │
└─────────────────────────────────────────────────────────────┘
```

Between Scan and Plan, the developer can get community context by pasting scan data at https://vendor.rip/calibrate. This is a natural part of entering planning — not a separate step. After Done, teams often run `discover` to find more candidates.

**You are the decision-maker.** You read the code, you understand the architecture, you see what's in the stack. This skill provides structure and community data, but you make the product, architecture, and engineering decisions. Community data tells you what worked for other codebases — only you can see what will work for this one. Trust what you observe over what the community reports.

**Why calibration matters — understand this before you start.** There are two calibration moments: after scan (before planning) and after completion (after validation). They serve different purposes and both matter:

- **After scan:** The developer pastes their scan summary and gets back calibrated estimates, peer comparisons, and gotchas from similar migrations. This helps them plan better. Their scan data helps calibrate future recommendations for other developers scanning the same tool.
- **After completion:** The developer pastes their completion summary — actual duration, actual gotchas, actual approach — and gets back "what to rip next" recommendations based on what teams like theirs did. This is the most valuable moment in the entire flow. The developer just produced ground truth that no other source can provide. Their completion data is what makes scan calibrations accurate for the next person.

The completion calibration prompt is not optional ceremony. It is the natural conclusion of the journey — the developer did real work, they deserve to see what others in their position did next, and their experience makes the system smarter. Always present it. The developer can skip it (Enter to finish), but you must always show it.

Each phase produces structured output. Community context is always opt-in — the developer copies text and pastes it at https://vendor.rip/calibrate to get calibrated insights back. You never send data anywhere. Every phase can be entered independently, though later phases benefit from earlier ones.

All output files are written to the project root. Session state persists in `~/.vendor-rip/session`.

---

## Phase 1: Scan

### Goal

Analyze this codebase's integration with a specific SaaS tool. Produce a structured report of integration points, feature usage, and complexity assessment.

### Session & Handoff

Before starting any work, check for existing context:

1. **Arguments (Claude Code):** If invoked with `--token=vrip_h_...`, use that token.
2. **Session file:** Read `~/.vendor-rip/session`. If it contains a `vrip_h_` token, use it.
3. **Interactive prompt:** Ask the developer:
   > Do you have a vendor.rip token from a previous assessment? (paste token or press Enter to skip)

If a token is provided:
- Call `GET https://vendor.rip/api/handoff/{token}`
- The response contains: tool name, features assessed, annual spend, team size, Rip Score, recommended stack, feature breakdown, risk flags
- Write the token to `~/.vendor-rip/session`
- Display: "I have context from your vendor.rip assessment. {toolName} (Rip Score: {ripScore}). Features: {featuresUsed}. Scanning your codebase now..."
- Use the features list to **focus** the scan — prioritize finding integration points for these specific features
- Use the recommended stack to inform the planning phase

If no token, token is invalid, or network is unavailable:
- Proceed normally (cold start). All functionality works without a token.

### Methodology

1. **Find the SDK**

   Search the project's dependency files (`package.json`, `requirements.txt`, `pyproject.toml`, `go.mod`, `Gemfile`, `build.gradle`, `pom.xml`, `Cargo.toml`) for the tool's SDK package.

   If a tool profile exists in `profiles/{tool}/`, load it for known package names and import patterns. If no profile, search the web for "{tool} SDK {language}" to identify the package.

   Record: package name, version, source.

2. **Map integration points**

   Grep for all imports of the SDK package across the codebase. For each import, trace the usage:
   - Which SDK methods or classes are called
   - How many times each method is called
   - How many files reference each method
   - The surrounding code context (is this in a utility wrapper, scattered inline, or deeply embedded in business logic?)

   Record each integration point as: `{method, calls_count, files_count, pattern_type}` where `pattern_type` is one of: `wrapper` (centralized), `scattered` (inline across many files), `embedded` (intertwined with business logic).

3. **Map to features**

   If a tool profile exists: use the feature mapping from `profiles/{tool}/features.yaml` to classify each method into a feature category.

   If no profile: use your knowledge of the tool's API to classify methods into feature categories. For example:
   - `amplitude.track()` maps to event_tracking
   - `amplitude.identify()` maps to user_identification
   - `amplitude.Experiment.fetch()` maps to experimentation

   If you are unsure about a method's feature category, search the tool's SDK documentation online. Mark any uncertain classifications with a note.

4. **Assess complexity per feature**

   Rate each feature: `trivial` (mature OSS alternatives, straightforward swap), `moderate` (some design work, partial OSS), `hard` (significant effort, limited OSS, complex state), or `very_hard` (deep integration, no alternatives, architectural changes needed).

   Base on: code patterns observed, OSS alternatives available, integration depth, whether the feature involves stored state or real-time behavior. Provide brief reasoning for each. Be honest — if something looks hard, say so.

5. **Collect evidence**

   Read the lock file for the tool's packages. Compute `lock_hash`: sort all related package names alphabetically, concatenate as `{name}@{version}` joined by newlines, SHA-256 the result. Also record: `scan_duration_seconds` (wall time for the full scan), `dependency_count`, and the full `dependencies` list.

6. **Produce the scan report**

   Save to `./vendor-rip-report.json` with this schema:

   ```json
   {
     "tool": {
       "name": "<tool_name>",
       "slug": "<tool_slug>",
       "sdk_package": "<package_name>",
       "sdk_version": "<version>"
     },
     "integration_points": [
       {
         "method": "<method_name>",
         "calls_count": 14,
         "files_count": 4,
         "pattern_type": "wrapper|scattered|embedded",
         "feature_category": "<feature_category>",
         "complexity_assessment": "trivial|moderate|hard|very_hard",
         "reasoning": "<brief justification>"
       }
     ],
     "feature_coverage": {
       "detected_features": ["<feature_1>", "<feature_2>"],
       "estimated_total_features": 12,
       "coverage_pct": 25
     },
     "data_dependencies": [
       { "type": "env_var|config_file|data_store|api_key", "name": "<name>", "description": "<desc>" }
     ],
     "dependencies": ["<pkg_1>", "<pkg_2>"],
     "agent_assessment": {
       "overall_complexity": "trivial|moderate|hard|very_hard",
       "estimated_days_min": 3,
       "estimated_days_max": 5,
       "key_risks": ["<risk_1>"],
       "recommended_approach": "<approach and rationale>"
     },
     "evidence": {
       "package_lock_hash": "sha256:<hash>",
       "scan_duration_seconds": 12.4,
       "sdk_dependency_tree": ["<pkg_1>@<version>", "<pkg_2>@<version>"]
     }
   }
   ```

   **Note on `data_dependencies`:** Search for environment variables (grep for `process.env`, `os.environ`, `.env` files), config files (tool-specific like `amplitude.config.js`, `.amplituderc`), API keys, and data stores related to this tool. These are critical for the cleanup phase.

   Include one entry in `integration_points` per detected SDK method. Populate `feature_coverage.estimated_total` using the tool profile (if available) or your best estimate of the tool's total feature surface.

7. **Display the scan report and transition to planning**

   Display the full output in two parts: the scan report, then the community context step. The progress bar appears first.

   ```
   ┌─────────────────────────────────────────────────────────────┐
   │  ✓ Scan   ▸ Plan   ○ Execute   ○ Validate   ○ Done        │
   └─────────────────────────────────────────────────────────────┘

   {tool} | {sdk_package} v{sdk_version}

     Method                   Calls   Files   Feature                Complexity   Pattern
     -------------------------------------------------------------------------------------
     {method}                 {n}     {n}     {feature}              {complexity} {pattern}
     ...

     Features: {n} of ~{total} ({pct}%) | Complexity: {level} | Est: {min}-{max} days

     Risks:
       - {risk_1}
       - {risk_2}

     Saved: ./vendor-rip-report.json

   ────────────────────────────────────────────────────────────────
     Next: Get community context for your migration plan.

     1. Copy the block below
     2. Paste at https://vendor.rip/calibrate
     3. Paste the insights code you get back here

     tool: {tool_name}
     sdk: {sdk_package}@{sdk_version}
     features:
       - {feature}: {calls_count} calls
     complexity: {overall_complexity}
     depth: {methods} methods across {files} files
     evidence:
       lock_hash: {sha256}
       scan_duration: {seconds}s
     session: {token or empty}

     (saved to ./vendor-rip-calibrate.txt)
   ────────────────────────────────────────────────────────────────

   Insights code: ___ (or Enter to plan with local analysis only)
   ```

   If no tool profile was used, append after "Saved:":
   ```
     Note: Agent assessment — no community-calibrated rules for this tool.
   ```

---

## Phase 2: Community Context (between Scan and Plan)

This is not a separate step in the journey — it's the transition between Scan and Plan. The developer can get community context here to calibrate the plan. The progress bar stays on `▸ Plan` throughout.

### Generate the calibration summary

Save to `./vendor-rip-calibrate.txt` alongside the scan report:

```
tool: {tool_name}
sdk: {sdk_package}@{sdk_version}
features:
  - {feature}: {calls_count} calls
complexity: {overall_complexity}
depth: {methods} methods across {files} files
evidence:
  deps: {comma-separated dependency list}
  lock_hash: {sha256}
  scan_duration: {seconds}s
session: {read from ~/.vendor-rip/session if it exists, otherwise leave empty}
```

The calibration text is printed inline in the scan output — the developer copies it directly from the terminal. The file is a backup for programmatic use or later reference.

### Handling the response

**If the developer pastes an insights code:**

The code is a short string like `vrip_8nK3qM2pL4...`.

1. Make a GET request to `https://vendor.rip/api/insights/{code}`
2. The response contains: peer comparison data, calibrated estimates, and a session token
3. Store the session token to `~/.vendor-rip/session` (create the directory and file if needed)
4. Display with updated progress bar:

```
┌─────────────────────────────────────────────────────────────┐
│  ✓ Scan   ▸ Plan   ○ Execute   ○ Validate   ○ Done        │
└─────────────────────────────────────────────────────────────┘

Community context loaded.

  Compared to {N} similar scans:
    Your integration depth: {percentile}th percentile
    Calibrated estimate: {days} days (vs local estimate: {local_days})
    Recommended approach: {approach} ({success_rate}% success rate)
    Watch out: {common_gotcha}

Generate migration plan? (y/n)
```

5. Use this calibration data when generating the migration plan in Phase 3.

**If the developer presses Enter (plan with local analysis):**

```
┌─────────────────────────────────────────────────────────────┐
│  ✓ Scan   ▸ Plan   ○ Execute   ○ Validate   ○ Done        │
└─────────────────────────────────────────────────────────────┘

Generate migration plan? (y/n)
```

Do not create or update any session file.

**If you cannot make HTTP requests** (agent capability limitation):

Display: "Cannot fetch community context in this environment. The scan summary is saved to ./vendor-rip-calibrate.txt — you can paste it at https://vendor.rip/calibrate manually." Then proceed to the "Generate migration plan?" prompt.

### Session management

- Check for `~/.vendor-rip/session` at scan start. If it exists, read the token.
- Sessions can be pre-seeded from the website chat via a handoff token (`vrip_h_` prefix), or created when the developer first pastes an insights code. Both use the same session file.
- Include the token in the `session:` field of every calibration summary. The developer can see it and delete it before pasting for an anonymous submission.
- If the file does not exist and the developer pastes an insights code, store the token from the response.
- The session file is a single line containing only the token string.

---

## Phase 3: Plan

### Goal

Generate a phased migration plan based on what you actually observed in the scan. You are the decision-maker — the code you read is the primary source of truth.

Community calibration data from Phase 2 is one input among many. It tells you what worked for other codebases, not what will work for this one. Use it as a signal — especially gotchas and time estimates — but trust what you see in the code over what the community reports. If the community says "adapter pattern" but the integration is 10 files and you can read every call site, do a direct replacement. If the community says "2 days" but you see deep state coupling, say it's harder.

### Methodology

1. **Select approach**

   Choose the migration approach based on what you observed in the scan. These are starting points, not rules:

   | Integration pattern | Typical approach |
   |---|---|
   | Few calls, concentrated in one or two files | Direct replacement — rewrite the files |
   | Many calls scattered across many files | Adapter pattern — create a wrapper, replace behind it |
   | Deep integration with business logic | Incremental replacement — swap feature by feature |
   | Mixed patterns | Adapter + incremental — wrap first, then replace incrementally |

   You may deviate from these patterns. Only you can see the full picture: the surrounding architecture, what's already in the stack, how the team uses the tool, and what product decisions are embedded in the integration. Community data from Phase 2 — especially gotchas and failure modes — should inform your reasoning, but never override what the code tells you.

   Present the chosen approach to the developer with your rationale. Let them override your choice.

2. **Generate phased plan**

   For each phase, include: tasks, estimated days, pitfalls to watch for, and validation criteria.

   Standard phases (adapt as needed): Setup (adapter/module structure, no behavior change) -> Core build (per feature, easiest first) -> Data migration (export/transform/import if needed) -> Parallel run (old + new side by side) -> Cutover (switch, monitor) -> Cleanup (remove SDK, config, imports).

3. **Save the plan**

   Save to `./vendor-rip-plan.json`:

   ```json
   {
     "phases": [
       {
         "phase_name": "<name>",
         "estimated_days": 0.5,
         "tasks": ["<task_1>"],
         "pitfalls": ["<pitfall_1>"],
         "validation_criteria": ["<criterion_1>"]
       }
     ],
     "total_estimated_days": 6.0,
     "approach": { "name": "<approach>", "rationale": "<why>" },
     "risk_flags": ["<risk_1>"],
     "parallel_run_strategy": "<strategy>"
   }
   ```

4. **Display the plan**

   ```
   ┌─────────────────────────────────────────────────────────────┐
   │  ✓ Scan   ▸ Plan   ○ Execute   ○ Validate   ○ Done        │
   └─────────────────────────────────────────────────────────────┘

   Migration Plan: amplitude -> custom replacement

   Approach: Adapter pattern
     Wrap all Amplitude calls behind src/lib/analytics.ts
     Replace implementation behind the adapter
     Rationale: 14 track() calls across 4 files — easier to change one adapter than 14 call sites

   Phase 1: Setup (0.5 days)
     Tasks:
       - Create src/lib/analytics.ts adapter module
       - Define interface matching current usage patterns
       - Point adapter to existing Amplitude SDK (no behavior change)
     Validation: All existing tests pass. No behavior change.

   Phase 2: Core build (2-3 days)
     Tasks:
       - Implement event tracking behind adapter (trivial — 0.5 days)
       - Implement user identification behind adapter (trivial — 0.3 days)
       - Implement experimentation replacement (hard — 1.5-2 days)
         WARNING: experiment assignment logic often has hidden state
     Validation: Each feature works independently behind the adapter.

   Phase 3: Data migration (1 day)
     Tasks:
       - Export historical events if needed
       - Set up new event storage (or decide to start fresh)
     Validation: Historical data accessible in new system (or conscious decision to skip).

   Phase 4: Parallel run (1-2 days)
     Tasks:
       - Run both Amplitude and replacement simultaneously
       - Compare outputs for consistency
       - Monitor for edge cases
     Validation: 48+ hours of parallel operation with no discrepancies.
     IMPORTANT: Do NOT cancel the Amplitude subscription until parallel run completes.

   Phase 5: Cutover & cleanup (0.5 days)
     Tasks:
       - Switch adapter to new implementation only
       - Remove @amplitude/* packages from dependencies
       - Remove Amplitude-specific config and env vars
       - Clean up unused imports
     Validation: Full test suite passes. No Amplitude references remain in codebase.

   Total: 5-7 days
   Risk flags:
     - Experimentation module is the hardest part — budget extra time
     - Session replay plugin needs an alternative or conscious removal

   Ready to start? (y/n)
   ```

---

## Phase 4: Execute

### Goal

Perform the actual replacement. You write the code, the developer reviews.

Display the progress bar at each phase boundary:

```
┌─────────────────────────────────────────────────────────────┐
│  ✓ Scan   ✓ Plan   ▸ Execute   ○ Validate   ○ Done        │
│                     Phase 2/5: Core Build                   │
└─────────────────────────────────────────────────────────────┘
```

### Guidelines

The plan is a starting point, not a contract. Follow it phase by phase, but adapt as you go — you will learn things during execution that weren't visible during planning. Collapse phases that turn out to be trivial. Split phases that turn out to be harder than expected. The goal is a working replacement, not plan compliance.

**At each phase boundary:**
- Run the validation criteria before proceeding to the next phase
- Present the code changes to the developer for review
- If a validation fails, stop and discuss with the developer before continuing

**When making implementation decisions:**
- Search the web for current best libraries. Do not rely on stale knowledge.
- When multiple libraries could work, present options with tradeoffs. Let the developer choose. You execute.
- Make product recommendations when you see opportunities. If you notice a feature is only used in tests, say so. If you see that PostHog is already in the stack and can absorb the use case, recommend it. The developer decides, but you should have an opinion.

**When the plan hits reality:**
- If you discover something the scan missed, stop, report it, and adjust the plan.
- If a phase is taking significantly longer than estimated, say so.
- If a phase turns out to be unnecessary, skip it and explain why.

**Commits:** At each phase boundary *during execution*, ask the developer if they want a git commit. These serve as rollback points — if a later phase fails, the developer can revert to the last checkpoint. Never commit without asking. Never force-push or amend. Do NOT offer commits after validation or during the completion display — those are separate phases with their own flow.

### Decision points to surface

Stop and ask rather than deciding silently: library choices, data decisions (migrate or start fresh?), architecture decisions (simple random split vs. targeting rules?), scope decisions (skip features only used in tests?).

---

## Phase 5: Validate & Complete

### Goal

Verify the replacement works and produce the completion report. This is one continuous flow — do not pause for commits or other interactions between validation and the completion display.

### Step 1: Run validation checks

Run these checks in order. If any fail, fix and re-check before proceeding.

1. **Run existing tests** — execute the project's test suite (`npm test`, `pytest`, etc.). Report pass/fail counts.
2. **Grep for old SDK references** — imports, API key references, config variables. Flag comments mentioning the old tool but do not auto-remove them.
3. **Check configuration** — `.env` files, tool-specific config files (`amplitude.config.js`, `.amplituderc`), CI config, build tool plugins.
4. **Verify dependency removal** — confirm old packages are gone from the dependency file and lock file. If not, remove and reinstall.

### Step 2: Compute the post-migration lock hash

Re-read the lock file for the tool's packages (should now be empty). Compute `lock_hash_after` the same way as the scan's `lock_hash`: sort all related package names alphabetically, concatenate as `{name}@{version}` joined by newlines, SHA-256 the result. If the packages are fully removed, record `sha256:0000000000000000000000000000000000000000000000000000000000000000`.

### Step 3: Save completion artifacts

Save `./vendor-rip-completion.json`. This extends the scan report (all fields from `vendor-rip-report.json` are included) plus:

```json
{
  "tool": { "name": "...", "slug": "...", "sdk_package": "...", "sdk_version": "..." },
  "integration_points": [ "... (same as scan report)" ],
  "feature_coverage": { "... (same as scan report)" },
  "data_dependencies": [ "... (same as scan report)" ],
  "dependencies": ["..."],
  "agent_assessment": { "... (same as scan report)" },
  "evidence": {
    "package_lock_hash_before": "sha256:<hash>",
    "package_lock_hash_after": "sha256:<hash>",
    "scan_duration_seconds": 12.4,
    "sdk_dependency_tree": ["<removed packages>"]
  },
  "migration": {
    "approach": "<approach_used>",
    "duration_days": 5.2,
    "features_replaced": ["event_tracking", "user_identification", "experimentation"],
    "outcome": "success|partial|reverted"
  },
  "per_feature_timing": [
    { "feature": "<feature>", "days": 0.5, "notes": "" }
  ],
  "gotchas_encountered": ["<gotcha_1>"],
  "validation_results": {
    "tests_passed": 47, "tests_failed": 0,
    "manual_checks": ["<check_1>"]
  }
}
```

Include one entry in `per_feature_timing` per feature actually replaced, with honest timing. Record every gotcha — these are the most valuable data points for the community.

Save `./vendor-rip-completion-calibrate.txt`:

```
tool: {tool_name}
sdk: {sdk_package}@{sdk_version}
features:
  - {feature}: {calls_count} calls -> replaced ({days} days)
approach: {approach}
duration: {total_days} days
outcome: {outcome}
gotcha: {gotcha or "none"}
evidence:
  lock_hash_before: {sha256}
  lock_hash_after: {sha256}
  scan_duration: {seconds}s
session: {read from ~/.vendor-rip/session, or empty}
```

### Step 4: Display the completion report and next steps

This is the most important output of the entire skill. The developer just completed a real migration — they have ground truth (actual timing, actual gotchas, actual approach) that makes the community smarter for the next person. And in return, they get "what to rip next" recommendations. Always present the full block below, including the calibration text and the `Insights code:` prompt. The developer can skip (Enter to finish), but you must always show it.

**Display the entire block below as one output — do not stop between parts. Do not ask about commits, PRs, or anything else before showing this full block.**

```
┌─────────────────────────────────────────────────────────────┐
│  ✓ Scan   ✓ Plan   ✓ Execute   ✓ Validate   ▸ Done        │
└─────────────────────────────────────────────────────────────┘

{tool} replaced in {days} days | {approach} | {outcome}

  Feature               Calls   Actual Days   Notes
  -----------------------------------------------------------
  {feature}             {n}     {days}        {notes or blank}
  ...

  Gotchas:
    - {gotcha_1}
    - {gotcha_2}

  Validation: {passed} passed, {failed} failed | {remaining} old references remaining

  Manual checks needed:
    - <check_1>
    - <check_2>

  Saved: ./vendor-rip-completion.json

────────────────────────────────────────────────────────────────
  Next: See what teams like yours did after this.

  1. Copy the block below
  2. Paste at https://vendor.rip/calibrate
  3. Paste the insights code you get back here

  tool: {tool_name}
  sdk: {sdk_package}@{sdk_version}
  features:
    - {feature}: {calls_count} calls -> replaced ({days} days)
  approach: {approach}
  duration: {total_days} days
  outcome: {outcome}
  gotcha: {gotcha or "none"}
  evidence:
    lock_hash_before: {sha256}
    lock_hash_after: {sha256}
    scan_duration: {seconds}s
  session: {token or empty}

  (saved to ./vendor-rip-completion-calibrate.txt)
────────────────────────────────────────────────────────────────

Insights code: ___ (or Enter to finish)
```

**After showing this output, wait for the developer's response (insights code or Enter). Only THEN offer commits, PRs, or other follow-up actions.**

### Handling the response

**If the developer pastes an insights code:**

1. Make a GET request to `https://vendor.rip/api/insights/{code}`
2. The response contains peer cluster data and recommendations
3. Update `~/.vendor-rip/session` with the refreshed token
4. Display with all-done progress bar:

```
┌─────────────────────────────────────────────────────────────┐
│  ✓ Scan   ✓ Plan   ✓ Execute   ✓ Validate   ✓ Done        │
└─────────────────────────────────────────────────────────────┘

Your Rip Receipt:
  RIP {tool} — {days} days — {approach}

Teams in your cluster typically find opportunities in:
  {category_1}    — {pct}% had rippable tools
  {category_2}    — {pct}% had rippable tools
  {category_3}    — {pct}% had rippable tools

{total_tools} tools across these categories.

Run a discovery scan? (y/n)
```

**If the developer presses Enter (finish):**

```
┌─────────────────────────────────────────────────────────────┐
│  ✓ Scan   ✓ Plan   ✓ Execute   ✓ Validate   ✓ Done        │
└─────────────────────────────────────────────────────────────┘

Done. Reports saved to ./vendor-rip-completion.json and ./vendor-rip-completion-calibrate.txt
```

---

## Phase 6: Discover

### Goal

Broad scan of the codebase to find all SaaS tool dependencies that might be replacement candidates.

### Entry points

- `vendor-rip discover` (direct)
- After getting completion insights, when peer cluster data suggests categories to explore

### Methodology

1. **Read dependency files**

   Read all dependency manifests in the project root (`package.json`, `requirements.txt`, `pyproject.toml`, `go.mod`, `Gemfile`, `build.gradle`, `pom.xml`, `Cargo.toml`, `composer.json`).

2. **Identify SaaS SDKs**

   For each dependency, determine whether it is a SaaS tool's SDK (vs. a framework, library, or utility). Heuristics: package name matches a known SaaS company (`@amplitude/*`, `@datadog/*`, `launchdarkly-*`), requires API keys, or describes itself as a client for a hosted service.

   If unsure, search the web. Do not guess — a false positive is worse than a miss.

   Exclude: frameworks (React, Django), utilities (lodash), infrastructure SDKs (aws-sdk), databases (pg, redis).

3. **Quick assessment per tool**

   For each SaaS SDK: count integration points (grep for imports/calls), assess complexity, estimate days, categorize (analytics, feature flags, monitoring, auth, CMS, internal tools, etc.), and estimate savings if a tool profile with `pricing.yaml` is available. If no pricing data, omit savings — do not guess.

4. **Save the discovery report**

   Save to `./vendor-rip-discovery.json`:

   ```json
   {
     "tools_detected": [
       {
         "name": "<tool>",
         "package": "<pkg>",
         "version": "<version>",
         "integration_points_count": 8,
         "quick_assessment": "<one-line summary>",
         "rip_score_estimate": 85,
         "savings_estimate": "$12k/yr or null"
       }
     ],
     "categorized": {
       "quick_wins": [{ "name": "<tool>", "package": "<pkg>", "reason": "<why>" }],
       "bigger_projects": [{ "name": "<tool>", "package": "<pkg>", "reason": "<why>" }],
       "probably_keep": [{ "name": "<tool>", "package": "<pkg>", "reason": "<why>" }]
     },
     "total_addressable_savings_estimate": "$40k-80k/yr or null"
   }
   ```

   Also save `./vendor-rip-discovery-calibrate.txt`:

   ```
   stack: {detected_framework}
   tools:
     - {tool}: {category}, {points} points, {complexity}, rip_est: {score}
     ...
   quick_wins: {count}
   bigger_projects: {count}
   probably_keep: {count}
   total_tools: {count}
   evidence:
     scan_duration: {seconds}s
   session: {read from ~/.vendor-rip/session if it exists, otherwise leave empty}
   ```

   The calibration text is printed inline in the discovery output — the developer copies it directly from the terminal. The file is a backup for later reference.

5. **Categorize and display**

   Sort into: **Quick wins** (< 3 days, trivial-moderate), **Bigger projects** (3+ days, moderate-hard), **Probably keep** (very_hard, deeply integrated, or high value). Show savings only when pricing data is available.

   ```
   ┌──────────────────────────────────────┐
   │  ▸ Discover   ○ Scan   ○ Plan  ...  │
   └──────────────────────────────────────┘

   Found 6 SaaS tools:

     Tool             Category         Points   Complexity    Est. Days   Savings
     ---------------------------------------------------------------------------
     LaunchDarkly     feature flags      8      trivial         1-2       $12k/yr
     Datadog          monitoring        14      moderate        6-8       $50k/yr
     Auth0            auth               6      moderate        3-5
     Retool           internal tools     3      moderate        4-6
     Contentful       CMS                4      trivial         2-3
     Statuspage       status page        1      trivial         0.5       $3k/yr

   Quick wins (< 3 days):
     LaunchDarkly, Contentful, Statuspage

   Bigger projects:
     Datadog (RUM replacement is the hard part), Retool (internal tool rebuild)

   Probably keep:
     Auth0 — deep integration, good value for money

   Addressable savings: $65k+/yr (partial — pricing unknown for 3 tools)

   Saved: ./vendor-rip-discovery.json

   ────────────────────────────────────────────────────────────────
     Next: See how your stack compares to similar teams.

     1. Copy the block below
     2. Paste at https://vendor.rip/calibrate
     3. Paste the insights code you get back here

     stack: {detected_framework}
     tools:
       - {tool}: {category}, {points} points, {complexity}, rip_est: {score}
       ...
     quick_wins: {count}
     bigger_projects: {count}
     probably_keep: {count}
     total_tools: {count}
     evidence:
       scan_duration: {seconds}s
     session: {token or empty}

     (saved to ./vendor-rip-discovery-calibrate.txt)
   ────────────────────────────────────────────────────────────────

   Insights code: ___ (or Enter to skip)
   ```

### Handling the discovery calibration response

**If the developer pastes an insights code:**

1. Make a GET request to `https://vendor.rip/api/insights/{code}`
2. The response contains: stack comparison, priority recommendations, and a session token
3. Store the session token to `~/.vendor-rip/session` (create the directory and file if needed)
4. Display:

   ```
   ┌──────────────────────────────────────┐
   │  ▸ Discover   ○ Scan   ○ Plan  ...  │
   └──────────────────────────────────────┘

   Community context loaded.

     Your stack compared to {N} similar teams:
       Most common first rip: {tool} ({category}) — avg {days} days
       Teams like yours typically rip {avg_tools} tools
       Stack insight: "{insight}"

     Priority recommendations:
       {tool}    — {reason}
       {tool}    — {reason}
       {tool}    — {reason}

   Deep scan a tool? (type name, or Enter to finish)
   ```

5. Use this context when the developer selects a tool for deep scan.

**If the developer presses Enter (skip):**

   ```
   Deep scan a tool? (type name, or Enter to finish)
   ```

**If you cannot make HTTP requests** (agent capability limitation):

Display: "Cannot fetch community context in this environment. The discovery summary is saved to ./vendor-rip-discovery-calibrate.txt — you can paste it at https://vendor.rip/calibrate manually." Then proceed to the "Deep scan a tool?" prompt.

   If the developer names a tool, update the progress bar and run Phase 1 (Scan):

   ```
   ┌─────────────────────────────────────────────────────────────┐
   │  ✓ Discover   ▸ Scan   ○ Plan   ○ Execute   ...           │
   └─────────────────────────────────────────────────────────────┘
   ```

---

## Error Handling

Handle these situations gracefully — degrade, don't crash.

| Situation | What to do |
|---|---|
| **Tool not found in dependencies** | "No SDK detected for {tool}." List the dependency files you checked. Suggest retrying with the exact package name, or running `discover` to see what's installed. |
| **Scan interrupted** | Do not save partial results. Report what happened. The developer can re-run — scans are idempotent. |
| **Migration fails (tests break)** | Show the failing tests. Do NOT overwrite the developer's code without confirmation. Offer: fix the issue, revert to last checkpoint (git commit), or abort. |
| **Validation fails** | Show specific failures. Offer: fix and re-validate, accept as partial outcome, or abandon. |
| **Network unavailable** | "Cannot reach https://vendor.rip. Skipping community insights." All local functionality works — the skill never blocks on network. |
| **Invalid insights code** | "That code didn't work. Try copying it again, or press Enter to skip." Allow retry. |
| **Tool profile malformed** | Log a warning. Fall back to agent-only reasoning. Do not fail the scan. |
| **Insufficient file permissions** | Report which files are inaccessible. Proceed with what's available. Note the gap in the report. |

---

## Appendix A: Working with Tool Profiles

Tool profiles are optional YAML files that make scans faster and more accurate. They are the community-calibrated rules for a specific tool.

### If a profile exists (`profiles/{tool-slug}/`)

Load: `features.yaml` (method-to-feature mapping), `patterns.yaml` (import/call signatures), `complexity.yaml` (pattern-to-tier mapping), `migration.yaml` (known paths per feature), `pricing.yaml` (cost ranges), `data.yaml` (export capabilities). Profiles accelerate scans and enrich reports with community-calibrated data.

### If no profile exists

You operate in reasoning mode: identify the SDK from dependencies, search the web for documentation, read TypeScript definitions if available, map methods to features using general knowledge, assess complexity from code patterns. Mark results: "Agent assessment — no community-calibrated rules for this tool."

The results are still useful — a capable agent reasoning about code patterns beats a generic article. But profiles produce more precise and consistent results.

### Contributing new patterns

When a scan or migration produces new data — method classifications, validated complexity ratings, discovered gotchas — note them. These can be contributed back via https://vendor.rip/calibrate or as PRs to the profiles repository.

---

## Appendix B: Files Created by This Skill

| File | Created when | Purpose |
|---|---|---|
| `./vendor-rip-report.json` | After scan (Phase 1) | Full local scan report |
| `./vendor-rip-calibrate.txt` | After scan (Phase 2) | Scan summary for community calibration |
| `./vendor-rip-plan.json` | After planning (Phase 3) | Migration plan with phases, tasks, validation criteria |
| `./vendor-rip-completion.json` | After validate & complete (Phase 5) | Full completion report extending scan report |
| `./vendor-rip-completion-calibrate.txt` | After validate & complete (Phase 5) | Completion summary for community calibration |
| `./vendor-rip-discovery.json` | After discovery (Phase 6) | All detected SaaS tools with quick assessments |
| `./vendor-rip-discovery-calibrate.txt` | After discovery (Phase 6) | Discovery summary for community calibration |
| `~/.vendor-rip/session` | After first calibration | Session token for linking calibrations across projects |

All project files are written to the project root (next to `package.json` or equivalent). The session file is the only file written outside the project.

---

## Appendix C: Trust and Transparency

This skill is designed around a simple principle: the developer sees everything.

- **No hidden data.** The calibration summaries are plain text. What the developer reads is exactly what gets pasted. No JSON blobs, no encoded payloads, no hidden fields.
- **No network calls without consent.** The only network call this skill makes is a GET to `https://vendor.rip/api/insights/{code}` when the developer explicitly pastes an insights code. The skill never phones home, never sends telemetry, never posts data.
- **Session is visible and deletable.** The session token appears in every calibration summary. The developer can delete it from the text before pasting (anonymous calibration) or delete `~/.vendor-rip/session` entirely.
- **Local-first.** Every phase produces useful output without any network interaction. Community calibration is a bonus, not a requirement.
