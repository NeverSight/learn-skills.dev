---
name: ai-diff-reviewer
description: Local & CI companion to the AI Diff Reviewer GitHub Action (DailybotHQ/ai-diff-reviewer on GitHub, "AI Diff Reviewer" on the Marketplace). Router for five capabilities — (1) run a local review of the current branch's diff using the SAME methodology as the CI action, (2) generate a repo-tailored `.review/extension.md` via the `generate-extension` sub-skill, (3) install and configure the GitHub Action itself in a repo that doesn't have it yet via the `setup` sub-skill (also doubles as the reference manual for every `action.yml` input), (4) author a well-documented pull request from the current branch's diff (Conventional-Commits title inference, structured body, PR-template merge, `gh pr create`/`edit`) via the `open-pr` sub-skill, (5) read the AI review the CI Action posted back on the current branch's open PR, present findings in the same format as the local review, and optionally walk the developer through each finding to apply/defer/skip (multi-leg-aware, per-finding consent, no commits/pushes) via the `apply-review` sub-skill. Auto-detects `.review/extension.md` (or `.github/ai-diff-reviewer/extension.md` as fallback) and layers it on top of the shipped default prompt for full local↔CI parity. Use when the developer wants a local pre-flight review before pushing, asks "run a code review on my current changes", wants to customize the reviewer to this repo, asks "how do I set up ai diff reviewer?", asks a reference-style question about any of the action's inputs, asks to "open a PR", "create the pull request", or "write the PR body" for the current branch, or asks "what did the CI review say?", "apply the AI review's fixes", or "walk me through the review findings".
version: "2.0.1"
documentation_url: https://github.com/DailybotHQ/ai-diff-reviewer/blob/main/skills/ai-diff-reviewer/SKILL.md
user-invocable: true
metadata: {"openclaw":{"emoji":"🔍","homepage":"https://github.com/DailybotHQ/ai-diff-reviewer","requires":{"anyBins":["git"]}}}
allowed-tools: Bash, Read, Grep, Glob
---

# AI Diff Reviewer — Local & CI Companion Skill

The [**AI Diff Reviewer**](https://github.com/marketplace/actions/ai-diff-reviewer)
is a GitHub Action that runs an LLM review on every pull request in
CI. **This skill is its local counterpart** — the same reviewer,
driven by your coding agent (Cursor, Claude Code, Codex, Gemini,
Copilot, Cline, Windsurf), on the branch you're editing right now. It
also installs and configures the CI Action itself when your repo
doesn't have it yet.

**Two audiences, same skill.**

- If your repo **already runs the Action in CI** → use the skill
  locally to catch what CI would catch, seconds before pushing. When
  CI is wired to the same extension file
  (`prompt-extension-file: .review/extension.md`), local and CI
  reviews match — same base prompt, same overrides. See the "Parity
  guarantee (Flow B)" section below for the wiring details.
- If your repo **doesn't have the Action yet** (or you don't want it)
  → the skill still gives you the full review locally, AND — when
  you're ready — helps you install the Action in CI with sensible
  defaults for strictness, triggers, and external-contributor policy.

**Five coordinated capabilities**, routed by intent:

| # | Capability | Sub-skill | Surface |
|---|---|---|---|
| 1 | Run the review on the current branch | *(default flow — this file)* | 🖥️ Local |
| 2 | Author repo-specific overrides (`.review/extension.md`) | [`generate-extension`](generate-extension/SKILL.md) | 🖥️ Local **+** ☁️ CI (shared file) |
| 3 | Install the GitHub Action + write `pr-review.yml` | [`setup`](setup/SKILL.md) | ☁️ CI |
| 4 | Draft the PR title + body from the diff | [`open-pr`](open-pr/SKILL.md) | 🖥️ Local → GitHub |
| 5 | Read the CI review on the PR + walk through findings to apply/defer/skip | [`apply-review`](apply-review/SKILL.md) | ☁️ CI → 🖥️ Local |

Sub-skill 3 (`setup`) also doubles as the **reference manual** for
every `action.yml` input via [`setup/reference.md`](setup/reference.md)
— any agent can answer *"what does `strictness` do?"* without opening
the action source.

**Version parity.** The [`prompt.md`](prompt.md) in this skill is
byte-identical to the one the Action ships in the same tagged release
(enforced by CI's `Skills — prompt-sync invariant` job). Pinning
`@v2.0.0` on both surfaces guarantees the same methodology and severity
model (CI may additionally dedupe on round 2+ via Iteration-Aware
Review; local reviews stay a full pass).

Source: <https://github.com/DailybotHQ/ai-diff-reviewer> · License: MIT

---

## Two supported flows: local-only or dual-surface

The five sub-skills are **independent**. There is no ordering
requirement, and installing the CI GitHub Action is **NOT** a
prerequisite for using this skill locally. Every consumer repo falls
into one of two flows — pick the one that matches the repo's use case:

| Flow | Use when | Sub-skills to run | Sub-skills to skip |
|---|---|---|---|
| **A. Local-only** | You want your coding agent to run the same review methodology on the branch you're working on right now, but you do NOT want the review to fire in CI on every PR. Common for personal repos, experimental repos, repos where the team hasn't opted into automated PR review yet. | **Optional but recommended:** `generate-extension` (once, to tailor `.review/extension.md`). Then the parent `run a local review` flow on every branch — works with or without an extension file (falls back to the shipped base prompt if Step 2.5 is declined). Optionally `open-pr` at the end. | `setup` — do NOT run it. It writes `.github/workflows/pr-review.yml`, which activates the CI Action. `apply-review` — nothing to apply (no CI review posts back to the PR without the Action installed). |
| **B. Dual-surface** | You want both: pre-flight local review before pushing AND a full CI review on every PR, sharing the same methodology and severity model on both surfaces (CI may additionally dedup on round 2+ via IAR — see below). Recommended for team repos and anything production-facing. | `setup` (once, installs the CI Action + accepts the Step 5 handoff to `generate-extension`), then the parent `run a local review` flow on every branch. `open-pr` when the PR is ready. After push, once CI has posted its review, `apply-review` closes the loop (read the CI findings, walk through them, apply fixes). | Nothing — all five capabilities are used across the lifecycle. |

**Parity guarantee (Flow B).** When `setup` writes the workflow with
`prompt-extension-file: .review/extension.md` wired in (default when
you accept the Step 5 handoff to `generate-extension`), the CI Action
reads the same file your local agent uses. Same base prompt + same
extension file = same review methodology and severity model, locally
and in CI. CI may still post a *shorter* finding set on round 2+ of a
generation because Iteration-Aware Review dedups there (local reviews
never do — see below). If the Step 5 handoff is declined, `setup`
omits `prompt-extension-file` and you get base-prompt parity only —
you can add the input manually later, or re-run `setup` and accept
the handoff.

**CI-only surfaces (not mirrored locally).** Two Action capabilities
run only in GitHub Actions, not in this skill's local review flow:

1. **Iteration-Aware Review (IAR)** — content-anchored dedup across
   rounds, four convergence policies (default
   `first-pass-exhaustive`), escape label (`full-review-please`),
   and user-forced reset (remove `applied-label` then re-trigger).
   A local review is always a **full pass** against the current
   diff — it may surface findings CI has already deduped on
   round 2+ of the same generation. Spec:
   [`docs/ITERATION_AWARENESS.md`](https://github.com/DailybotHQ/ai-diff-reviewer/blob/main/docs/ITERATION_AWARENESS.md).
   Tuning example:
   [`examples/iteration-aware.yml`](https://github.com/DailybotHQ/ai-diff-reviewer/blob/main/examples/iteration-aware.yml).
2. **`skip-review-label` emergency bypass** — when the configured
   label is on the PR, CI short-circuits to success with no LLM
   call. Hotfixes / rollbacks only; protect the label with a
   ruleset. Spec:
   [`docs/TRIGGER_MODES.md` § Emergency-bypass](https://github.com/DailybotHQ/ai-diff-reviewer/blob/main/docs/TRIGGER_MODES.md).
   Example:
   [`examples/skip-review-label.yml`](https://github.com/DailybotHQ/ai-diff-reviewer/blob/main/examples/skip-review-label.yml).

The full input reference (including every IAR knob and
`skip-review-label`) lives in
[`setup/reference.md`](setup/reference.md).

**Signalling the flow to your agent.** If the ambiguous request "set
up the reviewer" could mean either flow, the agent will ask. To skip
that question, be explicit the first time in each repo:

- Flow A: *"Set up ai-diff-reviewer for local-only use — do NOT install the GitHub Action."*
- Flow B: *"Full ai-diff-reviewer setup — install the Action workflow AND generate the extension file."*

Every subsequent request in the repo (`"review my branch"`,
`"open the PR"`, etc.) works identically across both flows — the flow
distinction only matters at first-time setup.

---

## Install

```bash
# Latest v2.x
npx skills add DailybotHQ/ai-diff-reviewer --skill ai-diff-reviewer

# Or pin to a specific tag for reproducibility
npx skills add DailybotHQ/ai-diff-reviewer@v2.0.0 --skill ai-diff-reviewer
```

This vendors the skill into `.agents/skills/ai-diff-reviewer/` in the
consumer repo and records source + content hash in `skills-lock.json` so
any teammate can restore identical bytes with `npx skills experimental_install`.
Bump to the latest with `npx skills update ai-diff-reviewer`.

> **Note on the git repo slug.** The repo path stays at
> `DailybotHQ/ai-diff-reviewer` (historical — published tags from v1.0.0
> onward, current major `@v2`). The `--skill ai-diff-reviewer` flag
> matches the Marketplace listing name; both refer to the same product.

---

## Activation

**Default flow (run a review) — triggers:**

- "Review my current branch"
- "Run a code review on my changes"
- "Do a pre-flight review before I push"
- "Code review the diff against `main`"
- "What would CI say about my current commits?"

**Generate-extension flow — triggers:**

- "Generate a `.review/extension.md` for this repo"
- "Customize the code review for our project"
- "Help me write repo-specific review rules"
- "Tailor the reviewer to our stack"

**Setup flow (install the GitHub Action) — triggers:**

- "Set up AI Diff Reviewer for this repo"
- "Configure the reviewer action"
- "Install the AI Diff Reviewer GitHub Action"
- "Help me create the pr-review workflow"
- "How do I add AI Diff Reviewer to this project?"
- Also fires as the answer to reference-style questions about the
  action — *"what does `strictness` do?"*, *"how do I use
  `label-gate`?"* — via [`setup/reference.md`](setup/reference.md).

**Open-PR flow (author the pull request) — triggers:**

- "Open the PR", "create a pull request for this branch"
- "Draft the PR title and description"
- "Write the PR body"
- "Update the PR description", "rewrite the PR body in the proper format"
- "Make a draft PR" (adds `--draft`)

**Apply-review flow (read + apply the CI review on the PR) — triggers:**

- "What did the CI review say?"
- "Read the review on this PR", "show me the review findings"
- "Apply the AI review's fixes", "walk me through the findings"
- "Help me address the critical findings", "critical only"
- "Which findings blocked the merge?"
- "The bot posted a review — help me address it"

If the trigger is ambiguous (e.g. developer says "help me with the
review" on a repo that has no `.review/extension.md` yet, or says
"handle the PR" on a repo where a PR both needs a review AND has a
one-line body), ask ONE clarifying question before routing. Heuristics
that help disambiguate:

- Repo already has `.github/workflows/pr-review.yml` (or similar) →
  probably NOT the setup flow.
- Repo has no `.github/workflows/pr-review.yml` (or similarly-named
  AI Diff Reviewer workflow — grep the `.github/workflows/` tree for
  `DailybotHQ/ai-diff-reviewer` or `ai-diff-reviewer` action refs)
  AND no `.review/extension.md`, and the developer just installed the
  skill → **ask** which of the two flows they want ("Flow A
  local-only" vs "Flow B dual-surface"; see the "Two supported flows"
  section above). Do NOT default to `setup` — Flow A (local-only) is
  a first-class use case, and running `setup` unrequested would
  write `.github/workflows/pr-review.yml` and force the CI Action
  into a repo where the developer may not want it. The presence of
  unrelated workflows (CI tests, deploy pipelines, dependency bots)
  is NOT evidence of Flow B; only an ai-diff-reviewer workflow is.
- Developer just finished a session of code changes and hasn't asked for
  a review yet → default review flow (local).
- The word *"review"* is ambiguous when a PR already exists for the
  current branch AND has live `<!-- ai-pr-reviewer-marker -->` comments
  from a recent CI run. In that case, *"read the review"* usually means
  the CI review on the PR (apply-review flow), not a fresh local one.
  Ask once: *"Read the CI review that just landed on PR #N, or run a
  new local review on your working tree?"*
- Developer just accepted a local review's findings and applied fixes
  → probably the open-pr flow (natural next step, first PR of the
  session).
- Developer just applied fixes from the CI review → probably `open-pr`
  in edit mode (to refresh the PR body if the scope changed), then
  `git commit + git push` (they'll do it themselves).

Some harnesses (Claude Code, Cursor) also expose these as slash
commands (`/ai-diff-reviewer`, `/ai-diff-reviewer-generate-extension`,
`/ai-diff-reviewer-setup`, `/ai-diff-reviewer-open-pr`,
`/ai-diff-reviewer-apply-review`); check the harness's
skill-invocation docs.

---

## Default flow: how the local review works

Everything below (Steps 0 through 5) describes **only capability #1**
from the table above — running the review on the current branch. The
four sibling sub-skills have their own procedures in their respective
`SKILL.md` files:

- [`generate-extension/SKILL.md`](generate-extension/SKILL.md) — author `.review/extension.md`
- [`setup/SKILL.md`](setup/SKILL.md) — install the GitHub Action
- [`open-pr/SKILL.md`](open-pr/SKILL.md) — author the PR title + body
- [`apply-review/SKILL.md`](apply-review/SKILL.md) — read + apply the CI review posted on the PR

---

## Step 0 — Trust boundary

This skill is **near read-only** on the working tree and does **not**
call any remote API. It:

- Reads files from the current git checkout (`Read`, `Grep`, `Glob`).
- Runs `git diff` and `git log` locally (no push, no fetch).
- Composes the review prompt in the agent's context and produces the
  review as terminal output.

The **only** writes it may perform, and only with explicit developer
consent in Step 2.5:

- Create `.review/` and write `.review/extension.md` — if the developer
  answers **yes** to the bootstrap offer (invokes the
  `generate-extension` sub-skill).
- Create `.review/` and touch `.review/.skip-bootstrap` (0 bytes) — if
  the developer answers **never** to the bootstrap offer.

It does **not**:

- Post inline comments to GitHub (that's the CI action's job).
- Modify any source file, workflow, or config file in the working tree.
- Call the LLM provider directly — it uses the coding agent that's
  already running you.
- Send any data off your machine.

If the coding agent has broader powers (e.g. can write files or run
arbitrary bash), those come from the harness, not this skill.

---

## Step 1 — Detect context

Run these to establish the review's inputs. Emit the JSON to your working
context; do not print it to the user unless they ask.

```bash
# Base branch: prefer the tracked upstream's short name, fall back to `main`.
BASE=$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null | sed 's|.*/||')
BASE="${BASE:-main}"

# Current branch + head SHA
HEAD_BRANCH=$(git branch --show-current)
HEAD_SHA=$(git rev-parse --short HEAD)

# The three artifacts the review needs
git diff --stat "origin/${BASE}...HEAD"    # summary of what changed
git diff "origin/${BASE}...HEAD"           # the actual diff
git log "origin/${BASE}..HEAD" --oneline   # the commit trail
```

If the diff is empty, tell the developer "no changes vs `<BASE>` — nothing
to review" and stop. If `origin/${BASE}` doesn't exist (fresh clone,
missing remote), fall back to `git merge-base main HEAD` and diff against
that; note the fallback in the summary.

---

## Step 2 — Compose the prompt (base + extension)

The review methodology lives in [`prompt.md`](prompt.md) — the exact same
prompt the CI action ships. Read it into your context as the base.

Then check for a **repo-specific extension** in this order of precedence
(first match wins; the rest are ignored):

1. `.review/extension.md` (recommended convention — runtime-agnostic)
2. `.github/ai-diff-reviewer/extension.md` (fallback for teams that
   prefer `.github/` sibling to workflow files;
   `.github/ai-pr-reviewer/extension.md` also accepted for back-compat
   with the pre-v1.5 skill name)

**If a match is found** — read it, append its content to the base prompt
verbatim, and skip to Step 3.

**If no match is found**:

- If `.review/.skip-bootstrap` exists → the developer opted out of the
  bootstrap offer previously. Use the base prompt alone (no announcement),
  skip to Step 3.
- Otherwise → go to **Step 2.5** (first-time bootstrap offer).

Announce the composed configuration in one line, e.g.
`Reviewing feat/foo (a1b2c3d) against main. Base prompt + .review/extension.md.`

The final composed prompt is what governs the review — the severity
definitions, the "what NOT to comment on" rules, the output shape.

---

## Step 2.5 — Offer to bootstrap the extension (first-time only)

This step fires only when Step 2 found no extension file **and** no
`.review/.skip-bootstrap` marker exists. It's the one moment the skill
educates the developer about the extension convention. After the answer
is recorded (either as generated content or an opt-out marker), the
skill never asks again in this repo unless the developer removes the
marker.

Ask the developer ONE question:

> **No `.review/extension.md` found for this repo.**
>
> I can run the review right now with the shipped default prompt — that
> catches ~90% of general-purpose issues (SQL injection, unhandled
> promises, missing input validation, obvious perf regressions, etc.).
>
> But it will miss the **repo-specific** stuff: your money-handling
> conventions, the modules where `console.log` is banned, the RFC-014
> pattern, the always-critical SQL patterns tied to YOUR schema. That's
> what a `.review/extension.md` gives you — file-anchored severity
> overrides written against THIS codebase.
>
> Want to bootstrap one now? (~30 seconds of Discovery + a ~100-line
> file of concrete overrides.)
>
> - **yes** — I'll route to the `generate-extension` sub-skill, then
>   come back and run the review with the fresh extension layered on.
> - **no** — run the review this once with the base prompt only. I'll
>   ask again the next time the skill activates.
> - **never** — never ask again in this repo. I'll create
>   `.review/.skip-bootstrap` (a tracked 0-byte marker). Commit it so
>   your whole team inherits the same preference. To re-enable the
>   offer later, delete the marker.

Handle the response:

- **yes** → invoke the `generate-extension` sub-skill in extension mode
  (see [`generate-extension/SKILL.md`](generate-extension/SKILL.md)).
  When the sub-skill finishes writing `.review/extension.md`, re-enter
  Step 2 from the top — the freshly-written file will be picked up and
  layered onto the base prompt. Do NOT skip the sub-skill's Discovery
  phase (12+ tool calls); that's where the value is.
- **no** → skip to Step 3 with the base prompt alone. Do NOT persist
  anything. The offer fires again next time.
- **never** → run:
  ```bash
  mkdir -p .review
  touch .review/.skip-bootstrap
  ```
  Then skip to Step 3 with the base prompt alone. Suggest the developer
  commit the marker: `git add .review/.skip-bootstrap && git commit -m
  "chore(review): opt out of AI Diff Reviewer bootstrap offer"`.

If the developer's response is ambiguous, default to **no** (the
minimally-disruptive choice) — do not silently opt them out.

---

## Step 3 — Execute the review

Apply the composed prompt to the diff **using the coding agent's own
tools** (Read, Grep, Glob):

- The prompt tells you to `read_file` / `grep` / `glob` — translate those
  to whatever primitives the harness gives you. Read the changed files in
  full; the diff alone is rarely enough context.
- The prompt tells you to `post_inline_comment(path, line, body, severity)`
  — since you are running locally without GitHub write access, instead
  **collect** each finding into an internal list of
  `{path, line, severity, body}` records and print them as a table in
  Step 4.
- The prompt tells you to `submit_review(summary)` **exactly once** — this
  is your cue that the review is complete. When you reach this point,
  print the final summary and stop.

**Cost discipline:** cap yourself at the same number of turns the CI
action does (~25) and the same inline-comment cap (default 20). Don't
grep the whole world; grep the files you're commenting on plus their
imports.

---

## Step 4 — Print the review

Emit the review to the terminal in the **same format** the CI bot would
post on a PR — this is the parity contract:

```markdown
## Verdict
<one sentence — "Looks good", "Blocking security fix needed", etc.>

## Findings

| # | Severity | File | Summary |
|---|----------|------|---------|
| 1 | 🚨 critical | `src/auth.ts:55` | SQL injection in raw-string login query |
| 2 | ⚠️ warning  | `src/cache.ts:120` | Unbounded cache key cardinality |
| 3 | ℹ️ info     | `tests/utils.ts:12` | Helper could be reused from existing fixture |

### 1. `src/auth.ts:55` — 🚨 critical
<the full finding body — 2-4 sentences + optional ```suggestion block```>

### 2. `src/cache.ts:120` — ⚠️ warning
<...>

### 3. `tests/utils.ts:12` — ℹ️ info
<...>

## Notes (no inline anchor)
- <cross-cutting concerns, architecture, test-strategy comments>

**Recommendation:** approve / request-changes / comment-only
```

Reproducing this exact shape (verdict → findings table → per-finding
body → notes → recommendation) is what lets a developer trust the
same methodology and severity model on both surfaces. On CI round 2+
of a generation, Iteration-Aware Review may additionally dedupe
findings that a local full pass would still list — that difference is
expected, not a parity bug (see **CI-only surfaces** above).

**Optional next-step hint.** When the review is clean (no 🚨 critical or
⚠️ warning findings) OR when the developer explicitly signals they're
ready to push, close the output with a one-line pointer to the sibling
sub-skill:

```text
Next step: want me to open the PR? — I can draft the title + body from
this same diff (see the `open-pr` sub-skill). Or run `gh pr create`
yourself.
```

Do not print this hint when the review found blocking issues — fix
first, ship second.

---

## Step 5 — Extension file convention (for consumers)

Three ways to end up with an extension file, all valid:

1. **Automated bootstrap** — say "review my branch" on a fresh repo,
   answer **yes** at the Step 2.5 prompt. The `generate-extension`
   sub-skill runs its 12+ tool-call Discovery and writes
   `.review/extension.md` for you. Simplest path — recommended for the
   first setup.
2. **Explicit sub-skill invocation** — say "generate a
   `.review/extension.md` for this repo" (or one of the other triggers
   listed in Activation). Same result as (1) but skips the bootstrap
   prompt. Use this to regenerate or refine an existing file.
3. **Hand-written** — create the file yourself, using the schema and
   examples below. Best when you know exactly what overrides you want
   and don't need the Discovery walkthrough.

Whichever path you take, the layout options are the same:

**Option A — `.review/extension.md`** (recommended):

```
my-repo/
├── .review/
│   └── extension.md         ← auto-detected by this skill
└── .github/
    └── workflows/
        └── pr-review.yml    ← CI workflow uses the same file
```

**Option B — `.github/ai-diff-reviewer/extension.md`** (fallback if you
prefer keeping the file next to your workflows). The pre-v1.5 path
`.github/ai-pr-reviewer/extension.md` is still recognised for
back-compat.

The **same file** should be referenced from your CI workflow's
`prompt-extension-file:` input so local and CI stay in perfect sync:

```yaml
# .github/workflows/pr-review.yml
- uses: DailybotHQ/ai-diff-reviewer@v2
  with:
    api-key: ${{ secrets.ANTHROPIC_API_KEY }}
    github-token: ${{ secrets.GITHUB_TOKEN }}
    prompt-extension-file: .review/extension.md   # same file the skill auto-detects
```

Example `.review/extension.md`:

```markdown
## Severity overrides for our codebase

- Any `SELECT * FROM users` in a request path is **critical** (PII exposure).
- Missing `AbortController` on a `fetch()` in `apps/frontend/` is **warning**
  (React 18 pattern we standardized on in RFC-014).

## Don't comment on

- Formatting in `apps/legacy/*` — that module is scheduled for a rewrite.
- Missing tests in `experiments/` — that folder is intentionally exploratory.
```

Full authoring guide (structure, tips, worked examples):
[`docs/PROMPTS.md`](https://github.com/DailybotHQ/ai-diff-reviewer/blob/main/docs/PROMPTS.md).

---

## Notes

- **The skill runs your local agent — it doesn't invoke a separate
  LLM.** If your harness is Cursor and you're on `auto`, the review costs
  are billed to your Cursor Pro subscription. If your harness is Claude
  Code with an API key, it's Anthropic tokens. Either way the local
  review is a "free bonus" if you were going to use the agent anyway.
- **When paired with the CI Action (Flow B), this skill does not
  replace it.** The CI Action still runs on every PR and posts the
  authoritative review (inline comments, severity gating,
  merge-blocking); the skill is for the "before pushing" moment. In
  Flow A (local-only), the local skill IS the entire reviewer — no CI
  leg, no post-push authority; findings live only in your terminal
  and you decide what to act on before opening the PR.
- **Extension parity is guaranteed on your side, not enforced by
  tooling.** If your `.review/extension.md` says something different
  from what your CI workflow's `prompt-extension-file:` points at, you
  get drift. Keep them at the same path.
- **Opt-out marker (`.review/.skip-bootstrap`).** A 0-byte tracked
  marker file that tells the skill "don't offer to bootstrap the
  extension anymore in this repo — the team knows the option exists
  and chose to stick with the base prompt." Created by answering
  **never** at the Step 2.5 prompt. Delete the file to re-enable the
  offer. Committing it is the intended behaviour so the whole team
  inherits the same UX.
- **Bugs, feature requests, and extension patterns to add to the
  starter templates:**
  [`github.com/DailybotHQ/ai-diff-reviewer/issues`](https://github.com/DailybotHQ/ai-diff-reviewer/issues).
