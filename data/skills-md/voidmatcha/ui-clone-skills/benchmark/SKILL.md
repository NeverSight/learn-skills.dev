---
name: benchmark
description: |
  Local-only regression / benchmark skill for ui-clone-skills maintainers.
  Drives the standard ui-reverse-engineering pipeline against the canonical
  reference site (https://realfood.gov) and records AE/SSIM, iteration count,
  gate fail counts, and outcome to benchmark/history.csv so prompt /
  sub-doc / model-version drift surfaces as a trend.

  Trigger phrases: "run benchmark" / "regression benchmark" / "benchmark
  clone". The Makefile no longer has a `benchmark` target — setup is inline
  bash in this skill (Step 1 below).

  Internal: NOT registered in `.claude-plugin/plugin.json` `skills`. Not part
  of the public 3-skill marketplace surface. Maintainer tooling only.
metadata:
  filePattern:
    - "**/benchmark/history.csv"
    - "**/benchmark/history/**"
  bashPattern:
    - "benchmark-harvest\\.sh"
  priority: 70
---

# benchmark — local regression / benchmark skill

## ⚡ Activation sentinel (READ FIRST)

The FIRST RESPONSE you generate after reading this file in reaction to a
"run benchmark" / "regression benchmark" / "benchmark clone" trigger MUST
begin with the exact line below — no decoration, no preamble, no header
above it:

```
[BENCHMARK-SKILL-ACTIVE v1 / skills/benchmark/SKILL.md]
```

Concretely: the response that comes right after the tool-result of your
`Read(skills/benchmark/SKILL.md)`. Reading this file IS the start of
execution; do not defer the sentinel to a later "more real" response, do
not announce the rule in prose instead of emitting the token, do not
prepend a step heading. The first line of that response is the token
itself, and only the token. Anything else (Step 1 announcement,
`bash skills/benchmark/scripts/setup.sh` call, status notes) goes
below it on subsequent lines.

Only that one response needs the sentinel — later responses in the same
session do not need to repeat it. Empirically, LLMs drop a per-message
prepend after a few turns even when the rule says "every response," so a
single emission anchored to the post-read response is the reliable signal
the maintainer checks.

Edge case — tool-only first turn. If the response immediately after the
SKILL.md Read would otherwise contain only a tool call with no text (e.g.
you decide to dispatch `bash skills/benchmark/scripts/setup.sh` without
saying anything), prefix that turn with the sentinel as a one-line text
message before the tool call. The text-only line is the sentinel; the
tool dispatch follows on the next line. Do not skip the sentinel just
because the turn would have been silent.

Maintainer-shell note. In some maintainer environments `ls` is aliased
to `eza`, where `ls -t` fails with `-t needs a value (modified|...)`.
Inside benchmark commands prefer the portable forms `\ls -1t`,
`/bin/ls -t`, or `find ... -printf '%T@ %p\n' | sort -rn` instead of
bare `ls -t` so the pipeline doesn't break on the maintainer's shell.

Why this is the activation signal. This skill is intentionally NOT registered
in `.claude-plugin/plugin.json` `skills` (see "Internal-only skills" in
AGENTS.md), so Claude Code's `--plugin-dir` discovery will never auto-load
it. The supported activation path is the AGENTS.md fallback: AGENTS.md is
imported into the system prompt via `CLAUDE.md → @AGENTS.md`, lists the
trigger phrases, and on trigger the agent must read this SKILL.md and act on
it. The sentinel therefore CANNOT appear in the *very first* response (the
one that decides to read SKILL.md), and the maintainer must not interpret
its absence there as a failure. It MUST appear in the next response — the
one right after the SKILL.md Read tool-result.

## Trigger

Maintainer asks the agent to "run benchmark". This is not a public skill — it
is invisible to contributors using the plugin and is not registered in either
host's marketplace manifest.

## Why this exists

`tests/` covers Python regression (gates, hooks, DAG — 360+ tests). It does
not cover: SKILL.md / sub-doc prompt drift, agent-browser version drift, real
reference-site DOM drift, or Anthropic / OpenAI model version drift. This
skill closes that gap by running the actual pipeline end-to-end against a
canonical site and recording metrics across runs.

## Architecture

**You (the LLM) drive the entire loop.** Python provides verification (`goal.py`,
`gate.py`, `measure.py`) and post-run metrics (`benchmark-harvest.sh`) only.
There is no external loop driver, no static prompt re-injection, no harness
choosing your next move. You iterate inside this Claude Code session using
your normal tool-use pattern until every STRICT v2 stop condition is met,
then you stop.

This intentionally mirrors how real users invoke the `ui-reverse-engineering`
skill — single session, agent-driven, verification gates surface failures so
you know what's left.

### Measurement coverage (multi-path)

Benchmark MUST exercise both invocation paths so single-path coverage doesn't
silently hide fragility (the v0.5.0 → v0.6 lesson: the wrapped-command path
passed every loop, while fresh-prompt path quietly regressed because nested
agents invented ad-hoc artifact names that no script consumed).

When the runner records a row in `benchmark/history.csv`, set the `path`
column to one of:

- `wrapped` — the benchmark wrapper invoked the canonical script chain
  (`dom-scaffold.sh`, `extract-dom.sh`, `section-compare.sh`) by name.
  Always required.
- `natural` — a separate run started from a fresh top-level folder with a
  free-form prompt (e.g. `"clone <URL> as a React + Tailwind app"`) and no
  script-name hints. Required for any SKILL.md prompt-surface change, any
  artifact-name rename, any new pre_*/post_* hook, and any change to
  `ui_clone/hooks/_common.py:CANONICAL_REF_ARTIFACTS`. The two rows
  should land within one factor of two of each other; a wider gap means
  the fresh path is degraded — find which step diverged before merging.

### Prompt neutrality (validation runs)

Benchmark / loop-validation prompts must be user-like, not harness-like. The
prompt given to the agent may contain only the request a real user would type:
the target URL and, if isolation is needed, the output directory. Keep model,
reasoning effort, permissions, cache flags, and working directory in CLI launch
flags or the outer runner — not in the prompt text.

Allowed natural prompt examples:

```text
Clone https://realfood.gov into scratch/loop-N/impl.
```

```text
Use ui-clone-skills to clone https://realfood.gov into scratch/loop-N/impl.
```

Forbidden in a natural validation prompt:

- Pipeline / goal-card / stop-marker instructions.
- Script names such as `section-compare.sh`, `dom-scaffold.sh`, or
  `spec-implementation-coverage.sh`.
- Agent-browser operational rules (`--session`, IIFE evals, close sessions).
- Previous-loop findings, required adjustments, known bug explanations,
  gate-game examples, or gate-specific remediation hints.

If a natural validation prompt produces a static mirror, HTTP-only verification,
missing `pipeline-state.json`, or no section-compare artifacts, treat that as a
skill or hook failure to fix in this repository. Do not add pipeline
instructions to the prompt to make the next run pass.
The same applies when a run creates an early `pipeline-state.json` but then
copies the live site into `impl/public` before `post-implement`.

Those details must be learned from the loaded skill docs, hooks, AGENTS.md, and
repo code. Adding them to the prompt turns the run into a guided diagnostic
attempt rather than a skill validation.

If an operator feels tempted to add scope paragraphs, script reminders,
gate-specific remediation hints, or marker schema requirements to the prompt,
stop and move that requirement into the relevant skill doc, referenced sub-doc,
hook, gate, test, or benchmark/coordinator validator. The natural prompt should
stay close to one sentence; the repo-owned skill surface must do the
remembering.

When a loop exposes a failure pattern, encode the lesson in the repo first:
update the relevant skill doc, gate script, tests, or hook, verify it, commit
and push it, then rerun the same natural prompt shape. A bespoke
feedback-filled or harness-instructed prompt is allowed only for diagnosis, and
its result must not be compared as a benchmark/history row.

### External harness concepts

External design-to-code arenas are useful operating patterns for this benchmark.
Keep these transferable ideas:

- **state capsule:** every prep/finalize split should leave one compact file with
  URLs, viewport, artifact roots, port/PID, report paths, and the metrics needed
  by later qualitative review;
- **free-port preview discipline:** outer runners may allocate an OS free port,
  assert no holder is already listening, poll readiness, capture, then clean up
  the owning process; never let the prompt text carry those operational details;
- **ranked summaries first:** compare loops should read `sections/result.txt`,
  transition reports, and proof rollups before opening raw screenshots or JSON;
- **archive for drift:** append comparable metrics to `benchmark/history.*` so a
  prompt, hook, model, browser, or site drift is visible across runs.

Avoid importing fixed design dimensions, fixed y-band section maps, dashboard
posting, PR-admin worktree policy, or challenge-specific scoring formulas into
the public clone workflow. Translate those harness details into the existing
semantic section-compare / runtime-proof / transition-proof metrics instead.

## Procedure

### Step 1 — Setup (MANDATORY, single command)

```bash
bash skills/benchmark/scripts/setup.sh
```

This is the **only entry point**. The script wipes any stale work dir at the
current SHA, creates `benchmark/work/<sha>/{ref,impl}`, force-relinks
`tmp/ref/realfood → benchmark/work/<sha>/ref`, and fails fast on symlink
mismatch. It is idempotent — safe to re-run if you suspect setup is stale.

The `ui_clone.hooks.pre_bash` hook will **block** any benchmark-related Bash
command (`section-compare.sh`, `extract-assets.sh`, `benchmark-harvest.sh`,
`visual-judge.sh`, `section-spec.sh`, any path under `benchmark/work/`, or
any use of `tmp/ref/realfood`) when `tmp/ref/realfood` points at a different
SHA's work dir than the current HEAD. Rounds A / B / V3 silently inherited
the prior run's symlink and produced misleading benchmarks; the hook + this
script close that loophole.

Bypass for emergencies only: `UI_RE_SKIP_BASH_GATE=1 <command>`.

### Step 2 — Drive the ui-reverse-engineering pipeline

Source URL: `https://realfood.gov`. Component name: `realfood`. STRICT path policy
— use EXACTLY component name `realfood` and ref dir EXACTLY
`benchmark/work/<sha>/ref` (already symlinked from `tmp/ref/realfood`). If you
catch yourself typing `realfood-main` or any variant, STOP — `benchmark-harvest.sh`
reads the canonical ref dir only, any other location is invisible to metrics.

Follow the normal ui-reverse-engineering pipeline:

- **Phase 1 (capture)** — if `<ref>/static/ref/` has fewer than 5 PNGs:
  ```
  ui-capture https://realfood.gov '' realfood
  ```
  Populates sections + scroll video + regions.json into `<ref>` via the symlink.

  **Fix 12 — scroll-reveal trigger before enumeration**. realfood.gov uses
  GSAP ScrollTrigger + Intersection Observer reveal animations: sections
  outside the initial viewport stay `height: 0` until the user scrolls to
  them. If `section-map.json` ends up with most entries at `height: 0`
  (observed V8 / d4b369d: 15/15 sections at h=0), the capture happened
  before reveal — re-run after scrolling the page to the bottom and back:
  ```bash
  agent-browser --session realfood-bench eval "
  (() => {
    return new Promise(resolve => {
      let y = 0; const step = window.innerHeight * 0.8;
      const tick = () => {
        window.scrollTo(0, y);
        y += step;
        if (y < document.documentElement.scrollHeight) {
          setTimeout(tick, 250);
        } else {
          window.scrollTo(0, 0);
          setTimeout(() => resolve('done'), 500);
        }
      };
      tick();
    });
  })()
  "
  ```
  After this completes, re-run the section enumeration to capture
  post-reveal heights. Without this, ref-sections has zero-height wrappers
  that section-compare's synthesis (Fix 12 filter) drops, leaving fewer
  comparable rows and inflating per-section AE for the wrappers that DID
  reveal.

- **Phase 2 — extraction** (DOM, CSS, bundles, fonts, paid features).

  **DOM extraction MUST go through `extract-dom.sh`** (Fix 14). Across V5–V10,
  agents wrote their own variants of the DOM extraction eval, losing the
  Fix 6 v1 `text` field and the Fix 13 `styles` field. Prose-level guidance
  in dom-extraction.md was ignored. The script is now the only canonical
  entry:
  ```bash
  bash skills/visual-debug/scripts/extract-dom.sh "$REF_DIR" realfood-bench '.target-selector'
  ```
  Writes `<ref-dir>/structure.json` with the Fix 13 schema (per-node text +
  styles). Validation is built into the script — it fails fast if the
  resulting JSON lacks `tag` / `children` keys (schema drift detection).

- **Phase 2.5 — asset transfer (MANDATORY, not just cataloging)**:
  ```bash
  bash scripts/extract/extract-assets.sh realfood-bench "$REF_DIR" "$IMPL_DIR/public"
  ```
  Downloads ref images / fonts / videos to `impl/public/`. Without this step
  the impl renders placeholder boxes for every image and section-compare AE
  explodes to 1M+ on every section. Also parse `<ref>/visible-images.json`
  and reference any non-CDN URLs in your generated code.

  **Completeness check (mandatory before Phase 4)**. extract-assets.sh
  silently partial-fails on origin redirects, signed URLs, or CDN
  cookies — observed in benchmark runs where AE stayed saturated because
  3 of 86 visible images were missing. After the script runs:
  ```bash
  EXPECTED=$(jq '[.[] | select(.type=="image") | .url] | unique | length' "$REF_DIR/visible-images.json")
  ACTUAL=$(find "$IMPL_DIR/public/images" -type f 2>/dev/null | wc -l | tr -d ' ')
  echo "images: expected=${EXPECTED} actual=${ACTUAL}"
  test "$ACTUAL" -ge "$((EXPECTED * 9 / 10))" || { echo "FAIL: more than 10% of images missing — re-run extract-assets.sh or fall back to inlining the missing URLs in <img src> rather than placeholders"; exit 1; }
  ```
  If under 90% transfer, the gate fails immediately rather than letting
  Phase 4 generate against broken assets — the AE regression that
  causes is invisible to visual-judge (it just sees a uniform mismatch
  with no actionable selector).

- **Phase 2.7 — DOM scaffold (MANDATORY, deterministic, Fix 8)**:
  Merge `structure.json` + `styles.json` + `section-map.json` into a single
  scaffold that the Phase-4 generator MUST follow verbatim:
  ```bash
  bash skills/visual-debug/scripts/dom-scaffold.sh "$REF_DIR"
  ```
  Produces `<ref-dir>/dom-scaffold.json` with: full DOM tree + Fix 6 v1 text
  per node + measured CSS (`bg`, `color`, `ff`, `fs`, `fw`, `lh`, ...) +
  per-section bbox metadata. This is the *source of truth* for Phase 4 — no
  LLM cost (pure Python merge of existing Phase 2 artifacts). It eliminates
  the "agent fabricates because lossy JSON input" failure mode at the
  cheapest layer.

- **Phase 2.6 — LLM-driven section spec (MANDATORY, anti-fabrication grounding)**:
  Before Phase 3 / Phase 4, run section-spec.sh on each section's ref clip to
  generate a verbatim, evidence-anchored spec (text content, hex colors,
  typographic scale, layout pattern, key elements, asset paths). Without this
  step Phase 4 fabricates plausible-but-wrong text (e.g., guessing "Eat Real
  Food" from URL when ref actually shows "Real Food Wins") and arbitrary
  styling from class names. The spec is the **primary input** to Phase 4 —
  the agent paste-translates the spec into TSX instead of inferring from
  lossy JSON dumps.

  For each section in section-map.json:
  ```bash
  bash skills/visual-debug/scripts/section-spec.sh \
    "$REF_DIR/sections/ref/section-N.png" \
    --label section-N \
    --metadata "$(jq -c '.sections[N]' $REF_DIR/section-map.json)" \
    --out "$REF_DIR/sections/spec/section-N.json"
  ```

  Each spec captures: verbatim text (h1/subhead/body/cta_label/captions), hex
  colors (bg/fg/accent), typographic scale (size+weight+family observed),
  layout vocabulary term, enumerated key elements, asset paths. Phase 4 then
  reads `sections/spec/*.json` and follows it deterministically.

- **Phase 2.8 — Deterministic transpile (MANDATORY, Fix 13)**:
  Run the JSON-to-JSX transpiler to produce skeleton component files from
  the per-node styles captured in Phase 2 (Fix 13 extension):
  ```bash
  bash skills/visual-debug/scripts/scaffold-to-jsx.sh "$REF_DIR" "$IMPL_DIR"
  ```
  Output: one `.tsx` per ref section under `impl/src/components/`, with
  verbatim text, verbatim inline styles, original tag hierarchy. This
  replaces the LLM-interpretation step of Phase 4 with a deterministic AST
  transform — no fabrication, no Tailwind class guessing, no stub
  regression. The LLM still has Phase 4 for things the transpiler can't
  deduce (event handlers, state, scroll-trigger animation).

- **Phase 3 — spec** (transition-spec, verification-plan).

- **Phase 4 — pre-generate + scaffold + LLM refinement**: if `<impl>` is
  empty, scaffold a Next.js project:
  ```
  npx create-next-app@latest "$IMPL_DIR" --typescript --tailwind --app \
      --src-dir --no-eslint --use-npm --no-import-alias --yes
  ```
  Then generate the cloned component there, REFERENCING the downloaded assets
  in `public/` (not placeholder rectangles). Split into per-section components
  under `src/components/` — `componentization` gate fails when `page.tsx` >
  200 LOC AND components/ < 3.

  **MANDATORY LLM refinement step (do NOT skip).** After `scaffold-to-jsx.sh`
  emits the deterministic TSX skeleton, you (the LLM) MUST iterate over each
  `impl/src/components/<Name>.tsx` and refine it. The deterministic transpile
  only captures verbatim text + inline styles + tag hierarchy — it does
  *not* produce production fidelity. Refine each component for:

  1. **Tailwind class replacement of inline styles** where the inline value
     maps cleanly (`style={{display:"flex",gap:"24px"}}` → `className="flex
     gap-6"`). Keep inline only for measured values that don't fit Tailwind's
     scale (e.g. `gap: 22.5px`). **Always strip `transform: matrix(...)` and
     `transform: matrix3d(...)` from inline style** — Phase 2's getComputedStyle
     snapshots these as the *final animation state*, so leaving them in
     locks every element at "post-animation" coordinates (commonly seen as
     "the impl renders shifted ~785px to the left" in Loop 7). Either map
     the transform to a Framer Motion `initial`/`animate` pair, a GSAP
     timeline, or just delete it and let the layout sit at its natural
     position.
  2. **Image references**: every `<img>`/`<source>` MUST point at
     `public/images/...` paths produced by Phase 2.5, not external CDNs and
     not `placeholder` rectangles. Check `visible-images.json` + `<impl>/public/`.
  3. **Font stacks**: components MUST use the project's font CSS variable
     (Geist / Die Grotesk / whatever Phase 2 detected) — not browser default.
  4. **Event handlers + state**: when `interactions-detected.json` flags an
     element (accordion, tab, modal, video play, scroll-driven reveal),
     wire React `useState` / event handlers / IntersectionObserver. The
     transpiler emits a static snapshot; behavior is your job.
  5. **Scroll-trigger animation**: when `transition-spec.json` declares
     scroll-driven entries (`progress`, `pinning`, etc.), wire them via
     Framer Motion / GSAP / Lenis-aware refs to match the ref's motion. If
     you do nothing here, AE on scroll sections inflates to ~1M permanently
     and visual-judge has no leverage to reduce it (it can only suggest
     Tailwind tweaks, not author behavior).
     Transition proof must be runtime behavior, not static markers:
     hidden spans, `data-transition-hooks`, `data-scroll-hook`,
     `data-hover-hook`, and generic motion words placed in inert attributes
     are benchmark contamination. `spec-implementation-coverage.json` must
     pass for real trigger wiring before the motion row can be treated as
     comparable.
  6. **Responsive variants**: the benchmark target is also rendered on
     mobile (375 / 414), tablet (768 / 834) and desktop (1280 / 1440)
     viewports. The deterministic transpiler captures the 1440 snapshot
     only; you must inspect `responsive/<viewport>/section-*.png` if it
     exists, otherwise re-capture at each viewport via
     `agent-browser --session realfood-bench set viewport <w> <h>` +
     screenshot, and add Tailwind responsive variants (`sm:`, `md:`,
     `lg:`, `xl:`) so the layout collapses correctly. Common patterns:
     `flex-col md:flex-row`, `text-2xl md:text-5xl lg:text-7xl`,
     `gap-4 md:gap-12`, `px-4 md:px-12 lg:px-20`. Without this step the
     impl renders broken on the very viewports `verification-plan.json`
     expects to verify, and any "responsive" sub-check in the gate fails
     deterministically.
  7. **Section-matcher: real sections, not sentinel hacks**.
     `section-compare.sh` descends `<main>` wrapper divs when they contain
     multiple nested `<section>` / `<main>` descendants, but the robust
     implementation pattern is still a flat list of real `<section>` elements
     under `<main>`. Apply each color-zone as a `style={{ background: ... }}`
     on the `<section>` itself when possible, preserve the ref CSS-module
     class names verbatim (`dga_hero__AjMaf`, `dga_stats__Wj1Kx`, etc.), and
     never add hidden sentinel / dummy children solely to manipulate verifier
     enumeration. Hidden enumeration sentinels are a gate-game signal; fix the
     section structure instead.
  8. **No other-SHA impl bootstrap**. Do NOT copy
     `benchmark/work/<other-sha>/impl/` as a warm-start base for the
     current SHA — that contaminates the measurement (you're benchmarking
     the prior maintainer's work plus your refinement, not the current
     SHA's pipeline). Each run must start from `npx create-next-app`
     scaffold + the SHA's own Phase 1-3 artifacts. Bootstrapping is
     allowed for the *ref* side (the live site is identical across SHAs,
     so `cp benchmark/work/<other-sha>/ref/*` saves capture time without
     contaminating measurement) but never for `impl`.

  Skipping the refinement step is the #1 cause of the "Phase 5 visual-judge
  loop runs forever but AE never drops" failure mode observed in
  benchmark/history.csv. The deterministic skeleton + macro wrapper fixes
  cannot move AE below ~400k on any non-trivial section; only refined
  components reach the < 100k range where the gate's critical threshold
  (and the gradient signal visual-judge needs) actually live.

- **Phase 5 — verification**: run `npm run dev` (background, capture port),
  then run section-compare, tree-diff, transition-compare against the local
  impl URL. Use `python -m ui_clone.measure` to invoke the comparison scripts
  with locked default env (`EXCLUDE_DYNAMIC=1`, `SECTION_THRESHOLD=2000`) so
  the classifier can't be tuned to mask gaming.

- **Phase 5b — visual-judge iteration (when section-compare fails)**:
  When `sections/result.txt` has FAIL rows with high AE/Mpx, the AE signal
  itself is a dead gradient (every section ~950k, no direction). DO NOT
  quit. `python -m ui_clone.goal <ref-dir>` will route you through
  `skills/visual-debug/scripts/visual-judge.sh`, which calls a multimodal
  LLM on each ref-clip vs impl-clip pair and emits actionable findings
  (`category`, `severity`, `selector_hint`, tailwind suggestions).
  Apply the `priority_fix` from each `visual-judge-<section>.json` to
  `impl/src/components/<Name>.tsx`, re-run section-compare, re-route via
  `python -m ui_clone.goal`. Repeat until result.txt has 0 FAIL rows or
  the per-section AE/Mpx drops below the section-compare critical threshold.

  **Mandatory: dev-server restart between iterations.** Next.js 16 + Turbopack
  HMR has been observed (benchmark/history Loop 3 12:05) to serve stale HTML
  for several sections mid-iteration even after the source file is updated
  via Edit — `dga_section__k3uwv` and `real_food_wins` rows stayed unchanged
  across 3 visual-judge iters until the dev server was restarted, despite
  source diffs being correctly applied. Before each `section-compare` re-run
  inside the Phase 5b loop:
  ```bash
  pkill -f "next.*dev"; sleep 2
  PORT=<port> npm run dev > /tmp/dev.log 2>&1 &
  until grep -q "Ready" /tmp/dev.log; do sleep 1; done
  ```
  This trades ~3s per iter for measurement validity. Without it, refinements
  silently don't land and AE plateaus look like "fix didn't work" when the
  actual fix is fine — the dev server just hadn't re-rendered.

  **Graded stop allowed.** STRICT v2 demands all 10 post-implement
  sub-checks PASS, but in practice `video-motion-compare` and
  `scroll-end-completion` need frame-perfect GSAP/Lenis parity that
  Phase 4 LLM refinement can approximate only loosely; insisting on
  perfect PASS there sends the loop forever. The pipeline is allowed
  to emit `INCOMPLETE-CONVERGED` instead of `DONE` when ALL of the
  conditions below hold simultaneously — that is a successful run for
  the benchmark even though it does not pass STRICT v2's `done` gate:

  - `result.txt` has zero `saturated` rows (no AE/Mpx ≥ 800k).
  - `ae_avg` improved by ≥ 30% versus the prior recorded run in
    `benchmark/history.csv` for the same SHA.
  - All static-content sub-checks PASS:
    `hydration-check`, `tailwind-transform-conflict`, `asset-transfer`,
    `transition-spec-coverage`, `spec-implementation-coverage`.
  - At most two of the dynamic-content sub-checks remain incomplete:
    `video-motion-compare`, `scroll-end-completion`, `text-fidelity-check`,
    `dom-mirror-check`, `image-fidelity`.

  **Hard disqualifiers.** Before emitting `INCOMPLETE-CONVERGED`, inspect the
  current `sections/result.txt` and `sections/visual-judge-*.json` artifacts.
  The graded stop is forbidden when any of these are true:

  - The section summary has `0 PASS` rows.
  - FAIL rows outnumber PASS rows.
  - Any row is marked `saturated` / `🌑`.
  - No `visual-judge-*.json` refinement artifact exists for the current
    failed section-compare run.
  - `tree-diff-status.json.status != "pass"`.

  These are not "close enough" states. Route through
  `python -m ui_clone.goal "$REF_DIR"` again, apply the visual-judge
  `priority_fix` findings to concrete component/CSS files, restart the dev
  server, and re-run section-compare before deciding whether convergence is
  defensible.

  Record outcome `INCOMPLETE-CONVERGED` via `benchmark-harvest.sh` when
  these hold. Treat it as a clean stop, not a forced quit — the data
  point is valid and the agent should not keep iterating against
  dynamic-content gates that can't converge inside one session.

  **Multi-section fairness when comparing history.csv rows.** An `ae_avg`
  computed over 1 section is not the same metric as `ae_avg` over 15
  sections — a single-section measurement reflects only that section's
  match quality. When the maintainer asks "did we beat baseline X," the
  honest comparison is between rows with similar `sections_captured`
  counts. A 1-section 156k run is not a better result than a 15-section
  187k run; it's a different measurement. Phase 5 must capture *all*
  sections present in section-map.json (skipping zero-height entries
  per Fix 12), and harvest's `sections_captured` field is what the
  fairness comparison reads.

  **`.benchmark-start` timestamp must be reset every setup.** When
  `setup.sh` runs in an existing work dir, the prior `.benchmark-start`
  marker file can survive and inflate `wallclock_s` in the next harvest
  (observed Loop 10 → wallclock_s=69688 ≈ 19h, real elapsed ~30min). The
  setup script always writes a fresh `date +%s` into `.benchmark-start`
  after the wipe, but verify the file's mtime before trusting
  harvest's elapsed time — if it predates the run, the row is bogus.

After every chunk of work, route the next action via:

```bash
python -m ui_clone.goal "$REF_DIR"
```

The goal card emits one bounded "Next action" string based on
`pipeline-state.json.current_gate` and any blocking gate failures. Run that
next action, then re-route.

### Step 3 — STRICT v2 stop conditions

**Do NOT self-impose a stop.** The visual-judge convergence loop in Phase 5b
IS the procedure, not the measurement subject. A first-pass result with FAIL
rows is not a valid stopping point on the grounds that "iterating would
invalidate the data point." The data point this skill records — wallclock,
iteration count, AE/Mpx, gate-fail counts — is exactly what `benchmark-harvest.sh`
computes *after* you converge or genuinely hit a blocker. Treat this run the
same as a real user invoking `ui-reverse-engineering`: iterate until 100%
visual match, exactly as that skill's own SKILL.md directs. The whole point
of this benchmark is to *mirror* real usage; deviating "to keep the data
clean" defeats the entire measurement.

You may emit "DONE" and stop ONLY when EVERY condition below is true:

- **Structure**: `impl/src/app/page.tsx` < 200 LOC AND `impl/src/components/`
  has > 3 .tsx files.
- **Section-compare**: `pipeline-state.json.gate_fail_counts == {}` AND
  `current_gate == "done"`. result.txt has 0 ❌ FAIL rows, 0 MISSING impl
  rows, NO `STRUCTURAL_ONLY` rows whose `structure-diff.json` severity is
  critical or major-with-height-ratio<0.5, and **no more than 50% of rows
  marked STRUCTURAL_ONLY** (gate fires "structural-only excess" when
  substitution covers more than half the page).
- **SECTION_THRESHOLD integrity**: every `minor` / `ok` row in result.txt
  has AE/Mpx ≤ 2000 (the gate detects classifier inflation and fails it).
- **tree-diff convergence**: `tree-diff-status.json.status == "pass"` AND
  `elements_walked >= max(30, section_count * 5)` AND `counts.unpaired` is
  not greater than `counts.ok` (the gate enforces the floor and pairing
  integrity — a near-empty impl that walks 11 elements or a layout where most
  walked elements cannot pair does not count).
- **Motion**: `transitions/result.txt` exists AND has 0 ❌ FAIL rows.
  If `transition-spec.json` declares any transitions, `result.txt` must
  contain at least one ✅/❌ measurement row (the gate fails an empty
  artifact as "transition-compare never ran") and
  `spec-implementation-coverage.json.status == "pass"` with no marker-only
  implementation proof.
- **Composition**: `bundle-impl-coverage.json.status == "pass"` (every lib
  detected in `bundle-map.json` is installed in `impl/package.json`) AND
  `asset-utilization.json.status == "pass"` with `downloaded >= 5`.

The verifier is:

```bash
python -m ui_clone.goal "$REF_DIR" --check-done
```

Exits 0 when all gates pass, 2 if pipeline-state has unclonable_reasons,
1 otherwise. Do not declare DONE before this exits 0.

### Step 4 — Harvest metrics

After you successfully stop (or after you decide the run cannot make further
progress), run:

```bash
bash skills/benchmark/scripts/benchmark-harvest.sh "$REF_DIR"
```

Reads `pipeline-state.json` + `sections/result.txt` + the `.benchmark-start`
marker, writes `benchmark/history/<timestamp>-<sha>.json` plus a one-row
append to `benchmark/history.csv`, prints a delta-vs-previous summary.

### Step 5 — Inspect the delta

A worsening trend on `ae_avg`, `iterations_to_done`, or new
`unclonable_reasons` means a regression in the prompt / sub-doc / external
dependency stack. Investigate before the next release.

## Outcome values

| Outcome | Meaning |
|---|---|
| `DONE` | All STRICT v2 stop conditions satisfied; `--check-done` exit 0. |
| `ABORT` | `pipeline-state.json.unclonable_reasons[]` non-empty (paid font, DRM canvas, auth-gated). Records the reason but no AE/SSIM. |
| `INCOMPLETE-CONVERGED` | Graded clean stop: STRICT v2 is not done, but all Phase 5b graded-stop conditions and hard disqualifiers above pass. |
| `INCOMPLETE` | Catch-all for "not done, not aborted" — agent decided the run cannot make further progress (cost cap, persistent failure, etc.). Inspect `pipeline-state.json.completed_gates` + `gate_fail_counts` for which gate halted. |

## Headless / CI path (optional)

`ui_clone/benchmark_harness.py` invokes `claude --print` per-iter with focused
prompts and Python-side stop checks. Useful for unattended cron / CI where
no interactive Claude Code session exists. **Not the canonical entry point**
— this skill is the canonical entry. The harness is a separate Python module
you invoke directly if you need it:

```bash
python -m ui_clone.benchmark_harness "$REF_DIR" --impl-dir "$IMPL_DIR" \
    --orig-url https://realfood.gov --impl-url http://localhost:3000 \
    --max-iter 100 --token-budget 500000 --wall-budget-s 14400
```

## Metrics in `benchmark/history.csv`

```
timestamp,sha,outcome,iterations,wallclock_s,ae_avg,ssim_avg,gate_fail_total,unclonable_count
2026-05-16T00:00:00Z,abc123,DONE,12,1840,0.023,0.94,4,0
```

The full JSON record at `benchmark/history/<timestamp>-<sha>.json` additionally
carries an `advisory_deductions` block aggregated from the Phase E reviewer's
`phase-e-review.json` (deduction count, penalty sum, and per-label counts for
`completeness` / `visual-effect` / `icon-variant`). Advisory trend signal only —
it feeds no gate and is absent (`null`) when Phase E did not run or the review
predates schemaVersion 2. CSV schema is unchanged.

## What this skill is NOT

- Not a CI tool. Lives entirely in the maintainer's local session.
- Not a model benchmark. Measures the *pipeline's* behavior against a fixed
  site, mixing prompt + model + ref-site contributions. Cross-version model
  A/B requires separate methodology.
- Not contributor-facing. Contributors can ignore this skill entirely; their
  workflow uses only `ui-reverse-engineering`, `ui-capture`, `visual-debug`.

## When NOT to run

- Mid-clone of a real user component (would interleave with the active
  pipeline state).
- Without an LLM session (the skill needs the agent to actually drive the
  clone — pure shell cannot).

## Storage policy

`benchmark/history.csv` and `benchmark/history/` are **gitignored**. Trend
data lives only on the maintainer's machine. If you want to share trend,
export and attach manually.
