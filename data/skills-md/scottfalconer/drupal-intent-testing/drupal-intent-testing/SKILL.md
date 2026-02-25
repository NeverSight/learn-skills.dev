---
name: drupal-intent-testing
description: >-
  Exploratory, intent-focused UI testing for Drupal sites using the agent-browser
  CLI (accessibility-tree based; no vision model required). Use to “poke around
  like a human”: create/edit content, change module configuration, build Canvas
  pages, and verify the intended UX/output. Supports guided testing, seeded
  fuzz/monkey testing, and paired before/after comparisons with artifacts
  (snapshots, screenshots, console/errors).
license: MIT
compatibility: >-
  Requires Node.js + Chromium via agent-browser. Designed for AI coding agents
  that can run shell commands (Claude Code, OpenAI Codex, etc.).
metadata:
  author: drupal-ai
  version: "0.2"
allowed-tools: Bash(agent-browser:*) Bash(python3:*) Read Write
---

# Drupal Intent Testing (agent-browser)

This skill is for **“does this do what we meant?”** testing — the semi-random, UI-first verification you’d do manually, but with an agent driving a real browser.

It is intentionally **not** a replacement for Drupal’s PHPUnit/Kernel/FunctionalJavascript tests. It complements them by validating UX, integration glue, and end-to-end intent.

## Why `agent-browser`?

- **Works in CLI agents** (Claude Code, Codex, Copilot, Cursor…) because it’s a shell tool.
- Uses the **accessibility tree + deterministic element refs**, so it **doesn’t require a vision model**.
- Still captures **real rendering** via screenshots for evidence.

## Safety note

Exploratory testing can create content, change config, and click destructive buttons.

- Prefer running against **local/dev instances**.
- Use **`--safety read-only`** (fuzz mode) unless you explicitly want mutation.

Credentials note: examples use placeholder `admin` / `admin`. Do not store real credentials in public artifacts; prefer local overrides or env vars.

---

## Setup

Install agent-browser and download Chromium:

```bash
npm install -g agent-browser
agent-browser install
```

On Linux you may need dependencies:

```bash
agent-browser install --with-deps
```

---

## Core workflow (agent-driven)

1. Navigate: `agent-browser open <url>`
2. Get a snapshot: `agent-browser snapshot -i -c --json`
3. Interact using **refs** (`@e1`, `@e2`) or semantic locators (`find label`, `find role`)
4. Re-snapshot after page changes
5. Capture evidence: `agent-browser screenshot <path>`

## Evidence Pack + checkpoints

This skill treats **checkpoints** as the unit of evidence. A checkpoint captures:

- Interactive snapshot (for driving)
- Screenshot (visual evidence)
- Console + JS errors
- Current URL
- Drupal messages (`role=status` / `role=alert`)
- AI Agents Explorer output (non-interactive text blocks)
- Optional backend probes (`--probe-cmd`)

AI Explorer extracts store `pre_texts`, `final_answer`, and `tool_payload`, plus summary metrics:
- `raw_in_final_answer` vs `raw_in_tool_payload`
- optional label checks via `--label-term`
- raw-value regexes via `--raw-value-regex`

## Intent manifest (autonomous loop)

Use an **intent manifest** to encode what to test and what counts as PASS/FAIL:

```yaml
issue:
  url: "https://www.drupal.org/node/3551315"
  title: "Enum options should expose UI labels"

environment:
  base_url: "https://canvas-dev.ddev.site:8443"
  login_url: "/user/login"
  admin_user: "admin"
  admin_pass: "admin"
  probe_cwd: "/path/to/project"

adr:
  - "Consumers can reliably map labels to stored values without guessing."
  - "Translation correctness depends on cache context bubbling and serialization boundaries; labels are kept stringable until serialization."
  - "Additional schema warnings are logged in a dedicated channel for troubleshooting malformed enum metadata."

strategy:
  mode: "single"               # single | compare
  between_cmd: "ddev snapshot restore intent-baseline"
  retries: 1
  timeouts:
    page_load_ms: 120000
    ai_response_ms: 600000

steps:
  - open: "/admin/config/ai/agents/explore?agent_id=canvas_page_builder_agent"
  - action:
      type: run_ai_agent_explorer
      prompt_file: "resources/vienna-hero-labels-mini.txt"
      model: "gpt-4.1"
      completion_texts: ["Final Answer", "Ran"]
      run_buttons: ["Run Agent", "Run"]
      post_completion_timeout_ms: 60000
      post_completion_stable_ms: 1500
      pre_min_count: 1
  - checkpoint: "after_run"

assertions:
  - id: "no_raw_values_in_final_answer"
    type: "text_absent"
    scope: "final_answer"
    patterns: ["hg:", "flex-row"]
    severity: "fail"

guards:
  - id: "no_js_errors"
    type: "no_console_errors"
    severity: "fail"
```

Run it:

```bash
python3 -m scripts.intent.validate_manifest path/to/intent.yaml
python3 -m scripts.intent_test path/to/intent.yaml --output-dir test_outputs
```

---

## Agent runbook: intent verification loop for Drupal.org issues

This is the default operating procedure for contrib fixes/features. If there is no Drupal.org issue, use the provided intent statement instead.

### 0) Mission statement

Your job is not “make tests pass.” Your job is:

- Understand user intent (from Drupal.org issue if available)
- Implement the change
- Verify like a human in a tight loop:
  - Doesn’t error
  - Actually does the thing the user wanted
- If you can’t verify confidently, escalate with excellent evidence and a specific question

Default behavior: if the user says “test with drupal-intent-testing” and does not provide a scenario/manifest, you must **author the verification artifact yourself** from the intent and run it. Do not ask for a script unless you are blocked on missing environment details (base URL, credentials, or success criteria).

### 1) Inputs you start from

You will be given at least:

- Drupal.org issue URL (or node id) **if available**
- Local dev base URL (DDEV or other), and credentials if needed
- Repo working tree/branch

### 2) Pick the right verification mode (decision tree)

Prefer the strongest behavioral proof available (rendered UI, saved config, persisted output) to minimize upstream maintainer burden; avoid tests that only check token presence if a behavioral proof is possible.

A) **UI/behavioral issue** (click here, see X, config form, node form, rendering):

- Use **Compare mode** with a generated scenario script + assertions.

B) **AI Agents Explorer output or tool payload shape**:

- Use **intent manifest + `python -m scripts.intent_test` + judge**.
- Checkpoints auto-extract AI Explorer `<pre>` blocks into `final_answer` and `tool_payload`.

C) **Unclear, hard to reproduce, or multiple workflows**:

- Do a short **guided exploration** to learn the UI path, then convert to Compare/Manifest.

D) **Light fuzz smoke** (optional but recommended):

- After a likely fix, run seeded fuzz in `read-only` unless you have snapshot restore.

### 3) Core loop (bugfix + feature)

**Step 1 — Pull “intent” from the issue (if available)**

If available, use the `drupal-issue-queue` skill (https://github.com/scottfalconer/drupal-issue-queue) to extract:

- Beneficiary persona: site builder, content editor, admin, dev
- Expected behavior (“success looks like…”)
- Repro steps (exact UI journey)
- Edge cases + regression risks

If you do not have the skill installed, summarize the issue manually and proceed.

If there is no Drupal.org issue, use the provided intent statement instead.

Output (required): write a short “Intent statement”:

- “The user is trying to ___”
- “Success means ___”
- “Failure modes to guard against: ___”

If an ADR applies, include its statements in the intent summary and translate each into assertions.

**Step 2 — Generate a verification artifact**

Option A: **Scenario script** (Compare mode) — preferred for UI issues  
Create: `scripts/test_scenarios/issue_<nid>.txt`

- Direct route navigation (Drupal admin is URL-addressable)
- Semantic locators (`find label`, `find role`)
- Checkpoints at key moments
- Assertions that encode success + regression guards

Option B: **Intent manifest** — preferred for AI Explorer/tool payload assertions  
Create: `.intent/issue_<nid>.yaml`

Minimum required fields:

- `issue.url`, `issue.title`
- `environment.base_url`
- non-empty `steps`

If there is no Drupal.org issue, use `intent_statement` instead of `issue.*`.

If credentials are provided, add `environment.admin_user/admin_pass` to auto-generate login flow.

If an ADR applies, list it under `adr:` and map each statement to concrete assertions.

**Step 3 — Baseline run**

Run verification **before** code changes to prove the problem exists.

Compare mode:

```bash
python3 scripts/compare_runs.py   --url "https://YOUR.ddev.site"   --script "scripts/test_scenarios/issue_<nid>.txt"   --output-dir "test_outputs/issue_<nid>"   --output "comparison_report.json"   --output-md "comparison_report.md"
```

Manifest compare mode:

- Use `strategy.mode: compare` and `between_cmd` to reset state.

Baseline expectations:

- Bugfix: baseline should FAIL intent assertions or show the problem clearly.
- Feature: baseline should show “not present yet.”
- If you cannot reproduce, **escalate**.

**Step 4 — Implement the change**

Make code changes. Run built-in tests as normal.

**Step 5 — Modified run**

Repeat the exact same verification artifact.

**Step 6 — Produce verdict + summary**

If using manifest/judge:

- `python -m scripts.intent.validate_manifest` validates required keys.
- `python -m scripts.intent_test` runs and writes `intent_run.json` + verdict.
- `judge_intent.py` produces `ready_to_submit`.

Supported judge assertion types:

- `no_console_errors`
- `no_drupal_messages` (alert/status)
- `url_contains`
- `text_absent` / `text_present` (AI Explorer `final_answer` / `tool_payload`)
- `yaml_path_equals`

If using Compare mode:

- `assert-*` results are recorded.
- Checkpoints provide full evidence packs.

**Required summary format:**

- Intent statement (1–3 sentences)
- What you ran (commands + artifact paths)
- Baseline outcome
- Modified outcome
- Regressions checked (JS errors / Drupal alerts / etc.)
- Confidence level (high/medium/low) + why

### 4) How to write good verification artifacts (“like a human”)

- Prefer direct routes (`/admin/config`, `/node/add/article`, etc.)
- Prefer semantic locators (`find label`, `find role`)
- Always include guardrails:
  - No JS errors
  - No Drupal alerts (`role=alert`)
  - Expected status message (`role=status`) when saving
- Place checkpoints at decision points:
  - after login
  - after key action
  - after expected result

### 5) Escalation protocol

Escalate when:

- You cannot reproduce baseline
- Success criteria are ambiguous/subjective
- Verification results are flaky
- Environment prevents verification

Template:

```
ESCALATION: intent verification blocked / uncertain
Issue: <url or “no issue provided”>
Intent (my understanding): …
Verification mode: Compare / Manifest / Explore
Commands run: …
Artifacts: test_outputs/...
Baseline result: PASS/FAIL/ERROR + key evidence
Modified result: PASS/FAIL/ERROR + evidence
Why I’m not confident: …
What I need from you: …
```

### 6) Done criteria

Do not mark complete until:

- You attempted to observe the intended outcome in the UI
- You verified both:
  - no errors (JS + Drupal alerts)
  - intended behavior occurs (assertion or strong evidence)
- Prefer the strongest behavioral proof available; increase timeouts when needed instead of failing fast.
- Bugfixes: baseline failure + modified success (or escalated if unreproducible)
- You produced attachable artifacts (screenshots + reports + brief narrative)

### 7) Optional next improvements

- Rely on `assert-*` heavily so judge output stays crisp.
- Add more assertion types as needed.
- Use default probes (e.g., `drush ws`) for root-cause context.

## If you have a Drupal.org issue (source of intent)

When a specific issue is driving the work, the **issue discussion is the intent**. Use it to derive your test goals, steps, and expectations before you explore.

Recommended flow (uses the `drupal-issue-queue` skill; skip if you do not have it installed):

If installed, this command comes from that skill:

```bash
# Summarize the issue discussion (acceptance criteria, expected/actual, edge cases).
python scripts/dorg.py issue <nid-or-url> --format md --mode summary --comments 20
```

Then:
- Extract **intent statements** (acceptance criteria, expected behavior, and repro steps).
- Translate each into **scenario steps** with `expect` assertions.
- Use the scenario as your baseline for Compare or Guided exploration.

Example mapping:
- Issue: “When adding a context label, it should appear in the Canvas AI sidebar.”
- Scenario: add label → `expect --text "New Label"` → screenshot.

---

## Modes

### Mode 1 — Watch (guided, human-validating)

Use when you want to visually inspect outcomes (new UI element appears, content looks right).

Suggested pattern:

```bash
agent-browser open "https://my.ddev.site/user/login"
agent-browser snapshot -i -c
agent-browser find label "Username" fill "admin"
agent-browser find label "Password" fill "admin"
agent-browser find role button click --name "Log in"
agent-browser wait --load networkidle

agent-browser open "https://my.ddev.site/admin/config/canvas-ai"
agent-browser wait --load networkidle
agent-browser screenshot test_outputs/canvas-ai-config.png
```

### Mode 2 — Compare (paired A/B, semi-deterministic)

Runs the *same script* twice and produces a diff report + artifacts (including console/errors captured at each snapshot).

Useful flags:
- `--trace`: capture `trace.zip` per run
- `--probe-cmd`: run backend probes at each checkpoint (repeatable)
- `--probe-cwd`: working directory for probe commands
- `--raw-value-regex` / `--label-term`: AI output metrics

```bash
python3 scripts/compare_runs.py   --url "https://my.ddev.site"   --script scripts/test_scenarios/canvas_ai_context_label.txt   --output-dir test_outputs   --output comparison_report.json   --output-md comparison_report.md
```

**Strongly recommended:** reset DB/state between A and B so your script starts from the same world.

If you use DDEV, you can snapshot/restore:

- `ddev snapshot --name intent-baseline`
- `ddev snapshot restore intent-baseline`

`compare_runs.py` supports running an arbitrary “between” shell command and optional evidence probes:

```bash
python3 scripts/compare_runs.py   --url "https://my.ddev.site"   --script scripts/test_scenarios/canvas_ai_context_label.txt   --between-cmd "ddev snapshot restore intent-baseline"   --probe-cmd "ddev exec drush ws --count=50 --format=json"   --trace   --output-dir test_outputs
```

### Mode 3 — Explore

#### 3A — Guided mission (LLM-driven)

Best for requests like: **“Build a microsite using Canvas and give feedback.”**

Recommended loop (the agent does this):

1. Decide a small next step toward the goal (e.g., “create a landing page”, “add a hero component”).
2. Run:
   - `agent-browser snapshot -i -c --json`
   - choose element(s) using refs or `find`
   - execute action(s)
   - `agent-browser wait --load networkidle`
   - `agent-browser screenshot ...`
3. Append observations to `test_outputs/mission_log.md`
4. Repeat until timebox ends.
5. Produce a structured summary: what worked, what was confusing, errors seen, suggestions.

#### 3B — Seeded fuzz/monkey testing (scripted, no LLM required)

Good for: “click around like a distracted user and see what breaks” — **for an hour**.

```bash
python3 scripts/explore.py   --url "https://my.ddev.site"   --duration 60m   --mode fuzz   --seed 1337   --safety dangerous   --checkpoint-every 20   --probe-cmd "ddev exec drush ws --count=50 --format=json"   --output-dir test_outputs   --output exploration_report.md
```

`safety` levels:
- `read-only`: no “Save/Submit/Apply” clicks; avoids mutation.
- `dangerous`: anything goes.

Optional fuzz flags:
- `--checkpoint-every N`: capture full evidence every N actions
- `--probe-cmd ...`: include backend probes at checkpoints
 - `--probe-cwd ...`: working directory for probes (useful for DDEV)

---

## Scenario script format (for Compare)

The compare runner understands a tiny DSL:

- `open /path` (prefixes `--url`)
- `snapshot <name>` (saves snapshot JSON to artifacts)
- `checkpoint <name>` (full evidence bundle: snapshot + screenshot + console/errors + message extraction)
- `screenshot <file.png>`
- `wait <seconds>` (numeric)
- `expect …` (assert/await; passed to `agent-browser wait`)
- `assert-present --text "..."` / `assert-absent --text "..."` (basic assertions)
- `assert-no-js-errors` / `assert-no-drupal-alerts`
- `assert-url --contains "/node/123"`
- `assert-count --selector ".some-class" --eq 3`
- `extract eval <name> <js>` / `extract text <name> <locator>`
- `probe shell <name> -- <command>` / `probe drush <name> -- <args>`
- Any other line is passed through as a raw `agent-browser …` command

**Best practice:** prefer semantic locators (stable) over hard-coded refs.
`checkpoint` is the preferred evidence capture; `snapshot` remains for legacy scripts.

Example:

```text
open /user/login
wait --load networkidle
find label "Username" fill "admin"
find label "Password" fill "admin"
find role button click --name "Log in"
wait --load networkidle
expect --text "Log out"
screenshot 01_logged_in.png

open /admin/config/canvas-ai
wait --load networkidle
checkpoint config_page
screenshot 02_config_page.png
```

---

## Drupal patterns

See [references/drupal_patterns.md](references/drupal_patterns.md) for practical Drupal UI patterns (login, messages, admin routes, CKEditor, AJAX).

---

## Reading results

Artifacts are written under `--output-dir` (default `./test_outputs/`):

- `baseline/` and `modified/` subfolders (compare mode)
- `*.png` screenshots
- `*.json` snapshots (normalized in the report)
- `*.errors.json` / `*.console.json` (captured at snapshot checkpoints)
- `*.drupal_messages.json` (status/alert text at checkpoints)
- `*.ai_explorer.json` (AI Agents Explorer output + summary metrics)
- `*.probe.N.json` (optional backend probes)
- `*.trace.zip` (if `--trace` enabled)
- `comparison_report.json` (diff + summary)
- `comparison_report.md` (human summary)
- `exploration_report.md` (fuzz mode report)
- `intent_run.json` / `intent_verdict.json` (manifest runner outputs)
