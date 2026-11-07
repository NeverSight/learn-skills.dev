---
name: agent-guardrails
description: Installs agentic guardrails into a Python repo — Claude Code hooks, a Stop gate that signs off only what pre-commit accepts, vetted public skills — and troubleshoots hooks that don't fire or block. Use for 'add Claude Code hooks', 'write an AGENTS.md', 'make this repo agent-ready', 'agent keeps bypassing checks', 'agent says done but pre-commit fails'. Not for authoring the pre-commit config.
license: MIT
---

# agent-guardrails

Install the agent-facing enforcement layer of a Python repo: Claude Code hooks
that give a coding agent instant, deterministic feedback (and hard-block the
few things it must never do), the settings wiring that ships them, a concise
rules file, and vetted public skills. The failure this skill fixes is
advisory-only guardrails — rules the model forgets under context pressure,
hooks that silently never fire, and `exit 1` "blocks" that block nothing.

## When NOT to use

- Git hooks — `.pre-commit-config.yaml`, commit-msg/pre-push stages. The
  python-precommit skill, if installed, owns the commit-time layer.
- CI workflows, required checks, branch rulesets — the python-ci skill. CI is
  the authoritative gate this skill's layers feed into, not what it installs.
- Validating LLM *output data* — Pydantic/Instructor schema validation,
  retry-with-error-context, SQL safety validators. That is runtime data
  validation in your application, not repo guardrails; this skill does not
  cover it.
- Tuning what the checks themselves do — ruff rules (python-lint), type
  checker config (python-typing), test infra (python-testing). This skill
  wires *when* checks run against agent actions, not their contents.
- Generic prompt engineering or system-prompt writing.

## The layer model (read this first)

Guardrails only work layered; each layer catches what the previous cannot
(convention, not an official spec — but it is strong cross-source consensus):

| Layer | Runs | Catches | Bypassable? |
| --- | --- | --- | --- |
| Rules file (AGENTS.md/CLAUDE.md) | read at session start | conventions, commands | yes — advice the model can forget |
| Claude Code hooks | at the moment of each agent action | bad writes/commands *before or as they happen* | yes — local, user-controlled |
| pre-commit | at commit | whole-diff issues | yes — `--no-verify` |
| CI + rulesets | at merge | everything, on infra the agent doesn't control | no — the only real gate |

Two consequences to state to the user every time: **anything that must always
happen belongs in a hook, not prose** (rules files are wishes; hooks are
contracts the harness executes), and **hooks are never the security
boundary** — they are local and user-editable, and alternate tool paths
(`bash` heredocs instead of Edit) route around file matchers, so CI and
server-side rules stay authoritative. (Hooks from settings files *do* run
inside subagents, with `agent_id` in the input — that gap is closed.)
Hooks' one unique power: PreToolUse denial happens *before the file ever
exists on disk* — the only layer that can do prevention rather than cleanup.

## Workflow

### 1. Audit what exists

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/check_guardrails.py" --root .
```

Read-only: reports settings files and scopes, wired hooks and their matchers,
rules files and their length, obvious defects (lowercase matchers, `exit 1`
used as a block, missing script files, unguarded Stop hooks). Also check
`claude --version` — hook behavior has version drift; the current docs are
the source of truth: https://code.claude.com/docs/en/hooks

### 2. Rules file — context, not enforcement

Write (or trim) `AGENTS.md` at the repo root, with `CLAUDE.md` containing only
`@AGENTS.md` so every agent reads one canonical file. Start from
[assets/AGENTS.md.template](assets/AGENTS.md.template). Rules that earn their
place in a Python repo:

- exact commands, not prose — `uv sync`, `uv run pytest`,
  `uv run ruff check --fix`, `uv run mypy src/`
- "Use uv, never pip or poetry" (the single most-reported agent failure:
  defaulting to global pip installs)
- "Run lint + typecheck + tests before calling a task done"
- "Never weaken a gate to pass it — no lowering coverage, skipping tests, or
  `|| true`" (agents under pressure take the cheapest path to green)
- blast-radius lines: "flag changes to auth, dependencies, or lockfiles for
  human review"

Keep it under ~200 lines and hand-curated: auto-generated context files have
measurably *hurt* agent success in evaluations — write what is specific to
this repo, not a generic overview. Recurring PR-review corrections are the
best source of new lines.

### 3. Hooks — the deterministic layer

Copy the three hook scripts from [assets/hooks/](assets/hooks/) into
`.claude/hooks/`, make them executable, then wire
[assets/settings.json.template](assets/settings.json.template) into
`.claude/settings.json`. The architecture is thin JSON, heavy script: the
settings file only routes events; logic lives in versioned scripts.

| Goal | Event + matcher | Script |
| --- | --- | --- |
| Block dangerous bash (`--no-verify`, `SKIP=`, hooksPath tricks, force-push main, bare pip, broad `rm -rf`) | `PreToolUse` on `Bash` | `guard_bash.py` |
| Instant ruff feedback on the Python file just edited (report, never rewrite) | `PostToolUse` on `Edit\|Write\|NotebookEdit` | `lint_edited_file.py` |
| Sign off only what the commit gate would accept | `Stop` | `stop_verify.py` |

All three are stdlib Python (no `jq`): the bash guard lexes the command
(wrappers, `bash -c`, newlines, `git -c`/`-C` options) instead of grepping it,
so `git push origin HEAD:main --force`, `git -c core.hooksPath=/dev/null commit`
and `python3.12 -m pip` are caught, and `git commit -uno` is not.

**The parity rule.** The Stop gate never re-implements checks: when the repo
has `.pre-commit-config.yaml`, `stop_verify.py` runs **pre-commit itself**
over the changed + untracked files — the identical gate `git commit` will run
(`pre-commit run --files` checks the worktree as-is; no stashing). Auto-fixing
hooks (prettier, ruff `--fix`, whitespace fixers) exit non-zero *after*
repairing the tree, so the gate runs twice and a clean second run passes. A
hand-rolled subset (`ruff check .` alone) drifts from the config and produces
the classic failure: agent says done, the owner's commit fails on prettier.
Repos without pre-commit keep the single fast `VERIFY_CMD` fallback.

The exit-code contract — the part everyone gets wrong (verified against
https://code.claude.com/docs/en/hooks, 2026-09-10):

- **`exit 0`** — proceed. stdout may carry a JSON decision; on exit 0 plain
  stderr goes only to the debug log, so a warning the user must see goes in
  `{"systemMessage": "..."}` on stdout.
- **`exit 2`** — the blocking exit code on blockable events, and nothing in
  JSON can override it. The reason shown is the JSON decision's `reason` if
  you printed one, otherwise **stderr** — so the simple recipe is still
  "exit 2 + reason on stderr". What "block" means is event-dependent:
  PreToolUse prevents the call; PostToolUse cannot undo — stderr is feedback
  only (and it fires only on success; failed calls go to `PostToolUseFailure`);
  Stop *prevents stopping* and forces the agent to keep working.
- **`exit 1` (or any other code)** — non-blocking *unless* stdout holds valid
  decision JSON, which is honored on every exit code. A bare `exit 1` with a
  message is logged and ignored; this single fact breaks a large share of hook
  setups.

Rules for hooks that survive contact with a team:

- Scope PostToolUse to the single edited file and keep it sub-second — it
  runs synchronously on every matching call. Anything slower (mypy, tests)
  belongs in the Stop hook, pre-commit, or CI.
- Stop hooks MUST honor `stop_hook_active` in the stdin JSON — the template
  re-verifies once, then releases (exit 0) instead of blocking again — or they
  loop; the harness force-overrides after 8 consecutive blocks.
- Give the Stop gate a generous explicit timeout (the template wires 300 s)
  and pre-build hook environments at setup (`uv run pre-commit install
  --install-hooks`): a hook that hits its timeout is **non-blocking**, so a
  cold first-run env build silently skips verification.
- Matchers are case-sensitive: `bash` never matches `Bash`. Letters, digits,
  `_`, `-`, spaces, commas and `|` are exact-match lists; any other character
  makes it an unanchored regex (`Edit.*` also catches `NotebookEdit`).
- `Edit|Write|NotebookEdit` misses shell-driven edits (`sed -i`, heredocs).
  Cover the gap with the Stop-hook verification pass, which sees the whole
  worktree; `FileChanged` exists for watching paths if you need per-file
  reaction to shell writes.
- `ConfigChange` (matcher `project_settings`) can block edits to
  `.claude/settings.json` — the one hook that stops an agent from rewriting
  its own guardrails mid-session.
- Hard-deny (`exit 2`) only deterministic, unambiguous violations; prefer
  non-blocking feedback for style-level issues — an over-eager PreToolUse
  block can stall the agent entirely instead of guiding it.
- Roll out observe → warn → enforce: log-only first, then narrow denies for
  patterns that caused real damage.

Full mechanics (per-event exit-2 semantics, matcher and `if`-field rules, JSON
decision channels, scopes, known version-drift issues):
[references/hooks-reference.md](references/hooks-reference.md).
Which check belongs at which layer:
[references/layer-assignment.md](references/layer-assignment.md).

### 4. Settings scopes and permissions

- `.claude/settings.json` — committed, applies to every contributor. This is
  the team contract; changes to it deserve PR-level scrutiny (see security
  below).
- `.claude/settings.local.json` — gitignored, personal experiments.
- `~/.claude/settings.json` — user-global. All scopes merge additively; a
  project file cannot switch off a user hook, only add.
- Hooks tighten policy but do not replace the permission system: a hook
  `exit 0` does not approve anything, and the `if` filter is best-effort and
  fails open on ambiguous commands. Hard allow/deny of tools belongs in
  `permissions` rules; hooks add checks the permission grammar cannot express.

### 5. Install and vet public skills

Recommend established public skills instead of rebuilding them — but treat
every third-party skill, plugin, and MCP server as an unreviewed dependency
with full user permissions. Minimum vet before install: read the plugin
manifest (an `mcpServers` entry means network access), every hook it ships and
the commands they run, and each full SKILL.md body; check requested
permissions are proportional to the stated function; pin versions and review
updates like dependency bumps. Curated starting points and the full checklist:
[references/vetting-skills-and-plugins.md](references/vetting-skills-and-plugins.md).

### 6. Verify by tripping every wire

A guardrail that has never fired is unverified. Test each one deliberately:

```bash
# 1. Scripts standalone, with realistic stdin — check exit code + stderr
echo '{"tool_input":{"command":"git commit --no-verify -m x"}}' \
  | python3 .claude/hooks/guard_bash.py; echo "exit=$?"        # expect exit=2
echo '{"tool_input":{"command":"git status"}}' \
  | python3 .claude/hooks/guard_bash.py; echo "exit=$?"        # expect exit=0
# 2. Audit passes
python3 "${CLAUDE_SKILL_DIR}/scripts/check_guardrails.py" --root .
```

Then, in a live session: ask the agent to do a blocked action (expect a
blocked call with the reason), edit a file with a deliberate lint error
(expect hook feedback), and end a turn with a failing check (expect the Stop
gate to push back). In a repo with pre-commit, also end a turn with an
unformatted YAML/Markdown file in the tree — the Stop gate must run the
commit gate and auto-fix or block, never sign it off. If a hook doesn't fire:
matcher case, settings nesting, and that `python3` is on PATH — in that order.

## Output spec

Done means:

- `AGENTS.md` (≲200 lines, repo-specific) with `CLAUDE.md` importing it.
- `.claude/settings.json` wiring PreToolUse guard, PostToolUse single-file
  check, and a Stop gate that runs the repo's own commit gate (pre-commit
  over the change set) or a single fast verify command; scripts in
  `.claude/hooks/`, executable, blocking only via exit 2 + stderr, Stop
  guarded by `stop_hook_active`.
- Every hook demonstrated to fire and to block (step 6 transcript).
- `scripts/check_guardrails.py` exits 0.
- The user told, in one sentence each: hooks are convenience, CI is the gate;
  and committed hooks execute on every contributor's machine.

## Failure modes & gotchas

| Symptom | Cause / fix |
| --- | --- |
| Hook "blocks" but the action proceeds | `exit 1` — only exit 2 blocks; everything else is logged and ignored |
| Block reason never shown to the agent | reason printed as plain text on stdout — on exit 2 the reason is the JSON `reason` field if any, else stderr; plain stdout text is neither |
| Warning from an exit-0 hook never appears | stderr on exit 0 goes to the debug log only — print `{"systemMessage": "..."}` on stdout |
| Hook never fires | case-sensitive matcher (`bash`≠`Bash`), wrong settings nesting, unexpanded `$HOME`, or a `python3` that is not on PATH — all fail silently |
| Stop hook loops forever | missing `stop_hook_active` guard; harness caps at 8 blocks but fix the guard |
| Agent "done" but the owner's `git commit` fails (prettier reformats, whitespace fixers fire) | Stop gate re-implements a subset instead of running the repo's pre-commit — wire stop-verify.sh's parity path (`pre-commit run --files` over the change set) |
| First Stop in a fresh clone hangs or times out | cold hook-env build; pre-build at setup (`pre-commit install --install-hooks`) and keep the generous timeout — a timed-out hook is non-blocking, i.e. a silent pass |
| Agent edits files but the format hook is silent | edit made via Bash (`sed -i`, `cat >`) — `Edit\|Write` never fires; rely on the Stop-hook worktree pass |
| Formatter hook fights the agent | an auto-fixing PostToolUse hook rewrites the file under the agent and its next edit fails the stale-file check — the shipped hook only reports; auto-fix belongs to pre-commit and the Stop gate's second pass |
| PreToolUse exit-2 stalls the agent instead of correcting it | known behavior in some versions — keep hard denies rare and actionable; put style feedback in non-blocking channels |
| Hooks treated as security | they are local and user-controlled; alternate tool paths (shell writes) route around file matchers — CI + rulesets are the boundary. Hooks do run inside subagents. |
| Committed hook = code execution on every clone | `.claude/` changes are code: CODEOWNERS them, review in the web UI before checking out PR branches (real CVEs exist here) |
| Plugin/skill turns out malicious | vet before install (step 5), pin versions, prefer official/curated sources |
| Hook advice from tutorials doesn't match behavior | the event surface and blocking semantics drift across versions — trust https://code.claude.com/docs/en/hooks over any static list, including this skill's |

## Files

- `scripts/check_guardrails.py` — read-only audit of settings, hooks, matchers
  and rules files; non-zero exit on defects.
- `assets/settings.json.template` — hook wiring for the three-script setup.
- `assets/hooks/guard_bash.py` — PreToolUse deny (lexer-based, stdlib):
  `--no-verify`/`-n`/abbreviations, `SKIP=` hook skips, `core.hooksPath`
  redirects, force-push to main in any argument order, bare pip / `python -m
  pip` outside uv, recursive force-delete of broad paths.
- `assets/hooks/lint_edited_file.py` — PostToolUse single-file `ruff check` +
  `format --check` via the project's own ruff (`uv run`); reports, never rewrites.
- `assets/hooks/stop_verify.py` — Stop gate with the `stop_hook_active` guard,
  runs in `$CLAUDE_PROJECT_DIR`: the repo's pre-commit over changed + untracked
  files (twice, so auto-fix hooks converge; `uv run` fallback), or one
  `VERIFY_CMD` list in repos without pre-commit; releases via `systemMessage`.
- `assets/AGENTS.md.template` — starting rules file.
- `references/hooks-reference.md` — full hook mechanics + known issues.
- `references/layer-assignment.md` — which check runs at which layer.
- `references/vetting-skills-and-plugins.md` — vetting checklist + curated skills.
