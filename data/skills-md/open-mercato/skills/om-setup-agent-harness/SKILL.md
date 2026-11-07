---
name: om-setup-agent-harness
description: Configure or diagnose the staged-only multi-model harness, including selectable implementation workers, review advisors, high-assurance packet policy, provider probes, and optional Claude model-matrix output style. Use when the user says "set up the agent harness", "configure multi-model reviewers", "choose worker models", "check harness setup", "skonfiguruj harness", or "sprawdź modele".
---

# Setup Agent Harness

Configure the optional `agentHarness` section without changing the existing PR
pipeline skills. Preserve the rest of `.ai/agentic.config.json`, store no
secrets, probe every selected adapter, and leave repository-owned setup changes
staged but uncommitted.

## Arguments

- `--check` (optional) — validate and probe the current configuration without writing.
- `--preset <cross-model-jury|custom>` (optional) — start from the bundled jury or an empty custom registry; default `cross-model-jury`.
- `--defaults` (optional) — enable the detected members of the bundled cross-model jury without asking questions.
- `--no-output-style` (optional) — do not install the optional Claude output style.
- `--no-hooks` (optional) — do not install the prevention hooks into `.claude/hooks/` and `.claude/settings.json`.

## Workflow

**ALWAYS check first:** Apply `.ai/skills/om-setup-agent-harness/SKILL.md` when present; safety rules still win.

0. **Agentic setup** — follow `references/agentic-setup.md` before any action: load approved configuration, apply local extensions and shared rules, and preserve the untrusted-content boundary.

### 1. Detect available adapters

Read `references/provider-catalog.md` and start from the bundled jury in
`references/configuration-template.json`: Codex, DeepSeek, Kimi, GLM, and MiMo.
Detect Claude as the host. Use the harness `probe` operation to check executable
versions and credential availability without printing or copying credentials.
The built-in DeepSeek and OpenCode Zen adapters may check their official local
auth-store entries internally; the setup agent never reads or displays the key.

When no bundled provider is detected, say so plainly and lead with the
bring-your-own-reviewer path from the provider catalog: any OpenAI-compatible
endpoint or any locally installed CLI can be bound as a reviewer through the
generic adapters — the bundled jury is a default, not a requirement. The only
fixed element is Claude as the host. A user with no external provider at all
still has a working `standard` profile (fresh Claude review only); offer that
explicitly instead of failing, but only after explaining what the multi-model
profiles would have added, so choosing it is an informed decision rather than
a silent default.

### 2. Select roles and policy

Unless `--defaults` is set, ask which detected models should act as workers,
reviewers, or both; which are required; the desired concurrency, timeout, and
retry policy (attempts, backoff, timeout escalation); and whether to enable
the `high-assurance` profile. Offer every bundled model independently, then offer “add custom
model” using the generic contracts in the provider catalog. Require command
adapters for workers. Keep HTTP and built-in subscription/API presets review-only.
Accept a worker only when its provider or OS sandbox demonstrably disables
network, remote/tracker writes, and Git ref writes; record that mechanism in
`workerSecurity`. Use only runtime-recognized audited adapters; version 1
supports `codex-workspace-write-sandbox`. A prompt-only promise or arbitrary
adapter declaration is insufficient.

### 3. Write the additive configuration

Build an `agentHarness` object from `references/configuration-template.json` and
the user's choices. Remove unselected bundled models from the active profiles;
do not delete custom models. Keep the `multi*` profiles on `all-required` with
`requiredReviewers` recalculated to exactly the selected reviewer set; use
advisory mode only when no reviewer is selected at all. If `high-assurance` is enabled, require a worker plus enough reviewers
outside its model family for the configured risk and verification rules; do not
silently weaken those rules. Detect the current Codex model from non-secret CLI
configuration, but keep the shipped compatible default when that model fails a
smoke review. Preserve every existing top-level config value. Resolve the
installed `om-harness` skill (its directory sits beside this skill's own install
directory; when it is absent, stop and ask the user to install the collection
with `om-harness` included), then run `node <om-harness>/scripts/harness.mjs
configure` against the working-tree config. Show the exact diff before staging it.
Keep portable team bindings in the repository object; put personal executable
paths or endpoints in the user-local overlay named by
`OM_AGENT_HARNESS_CONFIG`, and do not stage that overlay.

Keep every selected advisor in the profile reviewer list. Under the shipped
`all-required` policy every selected reviewer must complete (the runtime
retries failures automatically); selecting a reviewer is a commitment to hear
from it, never a best-effort hint.

Write only satisfiable profiles. Keep `standard` always; include `optimized`,
`multi-optimized`, and `high-assurance` only when an audited worker is bound,
and `multi`/`multi-optimized` only when at least one reviewer is selected. A
wrapper that later requests a profile this configuration does not define
reroutes back here instead of running with an empty jury.

### 4. Validate and smoke-test

Run `validate-config`, then `probe` for every selected profile. Run one harmless
structured review per selected advisor using the complete installed
`om-code-review` rubric so a valid binary but expired subscription is reported
correctly. This is an adapter smoke test, not an operational bound council; the
wrappers supply the required fresh Claude artifact and exact-subject packet.
A
required unavailable model or failed review policy is blocking; an optional
unavailable model is reported as skipped with its concrete smoke-test reason.
For `high-assurance`, require `validate-config` to accept its packet policy and
probe its full worker/reviewer readiness. Do not run a real worker against
repository files during setup.

### 5. Install the optional Claude output style

Unless disabled, copy `assets/claude-review-output-style.md` to
`.claude/output-styles/om-harness-review.md`. Never overwrite a locally edited
copy silently; show a diff and ask whether to replace, merge, or keep it.

### 6. Install the prevention hooks

Offer to install the structural stop-before-PR and test-freeze guards (default
yes). Copy `guard.mjs`, `block-push-and-pr.sh`, and `freeze-tests.sh` from the installed
`om-harness` skill's `hooks/` directory to `.claude/hooks/om-harness/`, keep
them executable, and merge the `PreToolUse` entries from the sibling
`hooks-settings-snippet.json` into `.claude/settings.json` without disturbing
existing hooks. These are the preventive layer of the stage-only contract: the
Bash guard is inactive until `capture` starts a run in the current worktree and
denies `git push` and PR creation until successful `stage` or explicit
`end-run` ends it. Other linked worktrees and ordinary publication workflows
remain usable. Keep both hook executable paths quoted so installation works
in directories containing spaces. The Edit/Write/MultiEdit/NotebookEdit
guard denies test-file edits while a `.om-freeze-tests` sentinel is present.
Never overwrite locally edited hook files or settings silently; show a diff and
ask.

### 7. Stage and report

Stage only `.ai/agentic.config.json`, the output-style file when created, and
the hook files plus `.claude/settings.json` when the hooks were installed.
Never commit, push, or publish. Print the readiness table defined in
`references/provider-catalog.md`, the configured profiles, skipped adapters,
and the staged paths. With `--check`, write and stage nothing.

## Rules

- Shared communication, marker, label, and safety rules: `references/rules.md`. They always apply.

- Keep Claude as host, conductor, and final reconciler.
- Require the operational wrappers to prove a new Claude review context; never configure the conductor's current context as its replacement.
- Keep `delivery.mode` fixed to `stage-only`.
- Keep secrets out of repository and user-local JSON; store only environment-variable names.
- Never replace existing pipeline config values that the user did not ask to change.
- Never install a worker binding whose command has not been confirmed to edit only the current worktree.
- Never commit, push, open a pull request, or mutate tracker state.

Hook support requires Bash and Node on macOS, Linux, or WSL. Native PowerShell
hook wiring is unsupported. Document that limitation during setup and block a
staged run when the host cannot enforce publication permissions.
