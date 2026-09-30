---
name: speckit-auto
description: |
  Runs an end-to-end spec-driven delivery pipeline from a requirement or Jira issue using a
  pluggable provider: github-speckit (repo-installed GitHub Spec Kit agents) or superpowers
  (obra/superpowers skills library). Handles provider setup and auto-install, Jira intake via
  jira-to-speckit, spec/design, implementation, a speckit-code-review remediation loop until
  pass, then human review (default) or YOLO commit and push. Use when a feature must go from
  requirement to committed implementation in one run.
compatibility: "Runs on GitHub Copilot, Claude Code, OpenCode, and Hermes Agent. Discovered from ~/.agents/skills/, ~/.claude/skills/, ~/.config/opencode/skills/, or ~/.hermes/skills/ (/opt/data/skills/ in Docker). Requires git and bash; network access for Jira intake via --issue."
license: MIT
allowed-tools: bash glob grep view create edit skill
metadata:
  author: Alex Nguyen
  version: "0.4.0"
---

# Speckit Auto

Entry point only: parse the invocation, resolve the provider, then run the stages.

**Progressive loading is a hard rule.** Load a reference file at the moment its step runs, never
ahead of time. Never load a stage you are not in, a provider you did not resolve, an install-
recovery file on a healthy run, or a file already in context. See the loading map below.

## Entry Dispatch (every invocation)

1. **Parse the invocation text** (slash-command body on Copilot/Claude Code; the natural-language
   trigger message on OpenCode and Hermes Agent — flags may be embedded anywhere):
   - `--integration <value>` → setup intent (setup ONLY, no pipeline)
   - `--issue <url>` → Jira pipeline intent
   - `--yolo` → mode = yolo (else default)
   - free text → requirement pipeline intent

2. **Note the host** from the directory this file was loaded from: `~/.copilot/skills/`,
   `.github/skills/`, `~/.agents/skills/` → Copilot; `~/.claude/skills/` → Claude Code;
   `~/.config/opencode/skills/`, `.opencode/skills/` → OpenCode; `~/.hermes/skills/`,
   `/opt/data/skills/` → Hermes Agent. Directories that overlap
   (`.claude/skills/`, `.agents/skills/`) or any other ambiguity → resolve via the tie-break in
   [references/shared/host-adaptation.md](references/shared/host-adaptation.md). The host is fixed
   for the run; look up host-specific values (ask tool, skill dirs, install host key) from that
   same file when a step needs one.

3. **Setup intent** (`--integration` present): load
   [references/shared/integration-setup.md](references/shared/integration-setup.md) and follow it.
   END TURN after — do not enter the pipeline, and do not load any pipeline file.

4. **Pipeline intent**: resolve the provider from **exactly one source** —
   `<repo-root>/.speckit/integration.json` → `integration` field. No global fallback, no first-run
   prompt. Missing file, unparseable content, or an unsupported value → stop immediately and tell
   the user to run `/speckit-auto --integration github-speckit` (or `superpowers`) first. On
   success, record it as `integration` in run state; never re-read or change it mid-run, and never
   infer the provider from repo contents.

5. Load **exactly three files**, then enter Stage 01 in this same turn:
   [references/shared/operating-rules.md](references/shared/operating-rules.md), the adapter for
   the resolved provider, and
   [references/pipeline/stage-01-intake.md](references/pipeline/stage-01-intake.md).

Never return an acknowledgement-only response. If the skill is already loaded mid-run (resume
marker: `<skill-context name="speckit-auto">` on Claude Code, `<available_skills>` on OpenCode,
the skill tool list on Copilot; Hermes Agent sessions never rotate, so the running session itself
is the resume marker), resume from the current stage using available run context and
load only that stage's file — never block asking the user to re-run the skill.

## Loading Map

| File | Load when |
|------|-----------|
| `references/shared/operating-rules.md` | every pipeline run, at entry (the only eager load) |
| `references/providers/<provider>.md` | every pipeline run, at entry — resolved provider only |
| `references/pipeline/stage-01-intake.md` | entering Stage 01 |
| `references/pipeline/stage-02-spec-design.md` | entering Stage 02 |
| `references/pipeline/stage-03-implement-review.md` | entering Stage 03 |
| `references/pipeline/stage-04-finish.md` | `speckit-code-review` returns `pass` |
| `references/shared/commit.md` | first commit gate reached (Stage 02 → 03) |
| `references/shared/host-adaptation.md` | a step needs an ask-tool name, skill dir, or install host key |
| `references/shared/integration-setup.md` | `--integration` present (setup runs; no stage file loads) |
| `references/providers/<provider>-install.md` | provider validation fails — never on a healthy run |
| `references/pipeline/jira-fallback.md` | `--issue` run and `jira-to-speckit` is unavailable |
| `assets/execution-report-template.md` | `--issue` run, at execution-report init |

Once loaded, a reference file from the table above stays in context for the run — never re-read
it. That rule covers `references/**` pipeline files only. Stage-local context (interviews, failed
review bodies) is dropped when leaving a stage; project **guideline** files are cached in
`loaded_guidelines` and may be dropped from context and re-read on demand later — when you drop
one, also drop its `loaded_guidelines` cache entry so a later stage knows to re-read it.

## Modes

- **Default**: human-in-the-loop. Mandatory checkpoints: the Stage 02 approval interactions, the
  Stage 02 → Stage 03 start-implementation confirmation, and Stage 04.
- **YOLO** (`--yolo`): no human checkpoints; Stage 02 interactions and Stage 04 human review are
  skipped, with an auto-generated commit message.

Stage 03 is a NO-STOP ZONE in both modes.

## Sub-Skill Dependencies

| Sub-skill | Purpose | Invocation |
|-----------|---------|------------|
| `jira-to-speckit` | Jira fetch + compaction (steps 1–5 only) + ticket snapshot write | `skill` tool, name `jira-to-speckit` |
| `speckit-code-review` | Authoritative JSON pass/fail review gate | `skill` tool, name `speckit-code-review` |

Both are provider-independent and used by every provider.

## Required Inputs

- Requirement text, or a Jira issue link via `--issue <jira link>`
- Jira credentials in the project root `.env` (gitignored) when using `--issue`:
  `JIRA_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN` — consumed by `jira-to-speckit`; never printed.

## Output Behavior

At each checkpoint, report: current stage, result (`done` / `needs changes` / `failed`), next
stage. At completion, report: resolved provider, `speckit-code-review` final status (`pass`),
implementation commit status/hash, and the spec completion commit hash. For a setup invocation
(`--integration`), report: resolved provider, file written, scope, and the next command.

## Portability Note

`allowed-tools` uses Copilot-style tool names; Claude Code and OpenCode expose the same
capabilities under their own names (`Bash`, `Read`, `Edit`, `Write`, `Glob`, `Grep`, `Skill`).
Hermes Agent exposes the same capabilities as `terminal`, `read_file`, `write_file`, `patch`,
`search_files`, `skill_view` (see references/shared/host-adaptation.md).
Never refuse to act because a tool is named differently.
