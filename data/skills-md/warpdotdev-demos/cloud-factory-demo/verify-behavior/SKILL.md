---
name: verify-behavior
description: Verify or reproduce visible product behavior by delegating to Oz's dedicated computer-use capability, requiring a native Oz video artifact for meaningful UI flows and durable Oz run/artifact links. Use when triage needs visual reproduction, implementation needs behavioral proof, review needs interactive confirmation, or any factory stage asks to verify UI/app behavior.
---

# Verify behavior

Prove or disprove **visible** product behavior for bugs and greenfield features. Parents (triage, implementation, review) invoke this instead of driving the UI themselves.

## Modes

- **`reproduce`** — does the reported bug still happen on baseline? (usually default branch; triage)
- **`verify`** — does the implemented change match expected behavior? (features and fixes; implementation/review)

Infer if unnamed: issue-only → `reproduce`; implementation/PR branch → `verify`.

## Platform contract (do not invent alternatives)

Oz computer use is a **dedicated capability**, not a generic remote child and not a set of parent-callable capture APIs.

| Layer | What happens |
|---|---|
| **Outer Oz cloud run** | Must already have computer use enabled (`computer_use: true` / `--computer-use` / `computer_use_enabled: true`). Factory implement workflows set this on the parent run. |
| **Parent / orchestrator** | Delegates GUI work through the platform **`computer_use`** capability with a concrete task and expected evidence. |
| **Permission** | `request_computer_use` is **emitted automatically** when the computer-use subagent starts. Parents must **not** call it, simulate it, or document fake tool calls for it. |
| **Computer-use subagent** | Native prompt already covers GUI actions, proactive `start_recording` / `stop_recording`, `report_screenshot`, and forbids ffmpeg / screen-capture CLIs. Do not re-teach capture plumbing or shell out to recorders. |

**Never:**

- Call or invent direct `request_computer_use`, `start_recording`, or `stop_recording` from the parent LLM
- Launch generic `run_agents` remote children as a substitute for `computer_use`
- Build custom recorder pipelines (ffmpeg, x11grab, avfoundation, Playwright video, etc.)
- Claim `gh ... --attach` can upload Oz videos to GitHub (it cannot reliably attach native Oz recordings)

## When to use / skip

**Use** for UI, browser, desktop, mobile, or other interactive behavior where visual proof helps.

**Skip** pure backend/CI/text-only work, or when credentials/state are unavailable (report the blocker). If this skill file is missing, parents continue without visual verification.

## PRODUCT.md coverage

When `PRODUCT.md` exists it is the primary source of stories and acceptance criteria:

1. Read it (parent path, `specs/<issue-slug>/PRODUCT.md`, or issue/PR links).
2. Build a checklist of exercisable user-facing stories. Newer issue comments win on conflict.
3. `reproduce`: stories tied to the failure + path to reach it. `verify`: all in-scope stories (or one assigned story if fanning out).
4. No PRODUCT.md → derive stories from the issue.

## Parent workflow

1. Collect mode, issue/PR, branch/ref, setup commands/URLs, surface hints, PRODUCT.md path/excerpts, and expected behavior.
2. Skip if not visually observable; report why.
3. Confirm the **current** Oz run has computer use enabled. If it does not and you cannot enable it, stop with an explicit blocker — do not fake verification.
4. For each verification unit (full checklist, or one story when fanning out), **delegate once** to the dedicated **`computer_use`** capability with a task that includes:
   - Mode (`reproduce` | `verify`)
   - Branch/ref and app setup
   - Exact story/repro path and acceptance checks
   - Instruction to exercise the critical path end-to-end
   - Expected evidence: **native session video** of the meaningful UI flow (subagent records proactively) plus **reported screenshots** of key states
   - Instruction to return observations and steps, not a vague pass/fail monologue
5. Multi-story `verify`: fan out **bounded** parallel `computer_use` delegations (about 4–6), one key independent story each; stay single-delegation for `reproduce`, one story, sequential stories, or scarce credentials.
6. Aggregate statuses: confirmed / partially confirmed / not reproduced / verified / partially verified / not verified / blocked.
7. Fold evidence into triage comments, PR bodies, or `review.json`. Do not claim behavioral verification without evidence or an explicit blocker.

### Delegation task shape

```text
Mode: verify | reproduce
Branch/ref: <implementation head or baseline>
Setup: <install/start commands or URL>
Story or repro: <one checklist item or full path>
Checks: <what must be visibly true>
Evidence required:
- Native Oz computer-use recording of the critical interactive path
- Reported screenshots for baseline, key action, and outcome states
Return: steps taken, observations per check, blockers, artifact/run references
```

Prefer browser-oriented interaction when the product is a pure web app and the environment provides browser automation inside computer use; prefer full desktop computer use for native surfaces, OS dialogs, or multi-window flows. Record `Channel: browser | desktop | hybrid` and a one-line why in the parent summary.

## Evidence requirements

For every meaningful UI flow:

1. **Native Oz video artifact** — produced inside the computer-use session via platform recording. Required unless the subagent reports that recording failed; quote that failure.
2. **Durable Oz links** — include `https://oz.warp.dev/runs/<run-id>` (or `https://oz.staging.warp.dev/runs/<run-id>` on staging). Never `app.warp.dev` or `/run/` (singular).
3. **Reported screenshots** — supplementary keyframes via the subagent's `report_screenshot` path; useful, not a substitute for video on multi-step flows.
4. **PR / issue write-up** — status, story checklist outcomes, Oz run link(s), and pointers to the native video/screenshot artifacts on the Oz run. Prefer platform PR artifact helpers (e.g. `get_artifacts_for_pull_request_description`) when available so managed screenshot/video markdown is embedded. Do not invent `gh --attach` video uploads.

Screenshots-only is allowed only when recording was attempted and failed, with the error quoted, or when the check is a single static state with no meaningful motion.

A verification that never delegated to `computer_use` on a computer-use-enabled run is **incomplete**.

### Screenshot captions (required on GitHub)

Whenever a screenshot is posted back to a **GitHub issue or PR** — including platform-managed evidence blocks, PR body sections, issue comments, and any other evidence summary — put a **concise caption immediately below** each screenshot that states:

1. The **UI state or test case** being verified (e.g. idle preview, in-flight submit, settled error)
2. **What the screenshot demonstrates** relative to the acceptance check (e.g. overlay present with spinner; overlay cleared)

Apply captions for managed markdown (e.g. `![…](…)` from artifact helpers) and for any hand-written evidence summary. Prefer short one-liners under each image; do not dump long prose. If the platform helper only supplies alt text, still add an explicit caption line under the image in the issue/PR write-up when you control that text.

Do **not** invent unsupported upload commands to satisfy captions. Captions travel with whatever evidence path the platform already supports.

## Report shape

```text
Behavior verification:
- Mode / change type / channel(s) / fan-out
- Status / issue-PR / branch-ref
- PRODUCT.md stories: n passed / failed / blocked / not run
- Oz run: https://oz.warp.dev/runs/<id>
- Evidence: native video (required for flows) + captioned screenshots (supplementary)
- Findings / next step
```

**reproduce** statuses: confirmed | partially confirmed | not reproduced | blocked  
**verify** statuses: verified | partially verified | not verified | blocked

## Guardrails

- Delegate GUI work through **`computer_use`**; parents do not click through unless the user explicitly asks
- Outer run must have computer use enabled; do not substitute generic remote children
- Do not call `request_computer_use` or parent-level recording APIs
- No ffmpeg or external recorders
- Native Oz video required for meaningful UI flows; screenshots supplement
- Every GitHub-posted screenshot needs a concise caption (state/case + what it shows)
- Durable Oz run/artifact links on issue and PR write-ups; no fake GitHub binary-attach of Oz recordings
- Features are first-class; PRODUCT.md drives coverage when present
- Bounded fan-out; no secrets in prompts, screenshots, or reports
- No claim of verification without evidence or an explicit blocker

Optional `verify-behavior-local` may specialize setup/surface/fan-out only — not weaken evidence, privacy, captions, or this contract.
