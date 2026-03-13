---
name: claude-code-clawdbot
description: "Run Claude Code (Anthropic) from this host via the `claude` CLI (Agent SDK) in headless mode (`-p`) for codebase analysis, refactors, test fixing, and structured output. Use when the user asks to use Claude Code, run `claude -p`, use Plan Mode, auto-approve tools with --allowedTools, generate JSON output, or integrate Claude Code into Clawdbot workflows/cron." 
---

# Claude Code (Clawdbot)

Use the locally installed **Claude Code** CLI reliably.

This skill supports two execution styles:
- **Headless mode** (non-interactive): best for normal prompts and structured output.
- **Interactive mode (tmux)**: required for **slash commands** like `/speckit.*` (Spec Kit), which can hang or be killed when run via headless `-p`.

This skill is for **driving the Claude Code CLI**, not the Claude API directly.

## Quick checks

Verify installation:
```bash
claude --version
```

Run a minimal headless prompt (prints a single response):
```bash
./scripts/claude_code_run.py -p "Return only the single word OK."
```

## Core workflow

### 1) Run a headless prompt in a repo

```bash
cd /path/to/repo
/home/ubuntu/clawd/skills/claude-code-clawdbot/scripts/claude_code_run.py \
  -p "Summarize this project and point me to the key modules." \
  --permission-mode plan
```

### 2) Allow tools (auto-approve)

Claude Code supports tool allowlists via `--allowedTools`.
Example: allow read/edit + bash:
```bash
./scripts/claude_code_run.py \
  -p "Run the test suite and fix any failures." \
  --allowedTools "Bash,Read,Edit"
```

### 3) Get structured output

```bash
./scripts/claude_code_run.py \
  -p "Summarize this repo in 5 bullets." \
  --output-format json
```

### 4) Add extra system instructions

```bash
./scripts/claude_code_run.py \
  -p "Review the staged diff for security issues." \
  --append-system-prompt "You are a security engineer. Be strict." \
  --allowedTools "Bash(git diff *),Bash(git status *),Read"
```

## Notes (important)

- **After correcting Claude Code's mistakes**: Always instruct Claude Code to run:
  > "Update your CLAUDE.md so you don't make that mistake again."
  
  This ensures Claude Code records lessons learned and avoids repeating the same errors.

- Claude Code sometimes expects a TTY.
- **Headless**: this wrapper uses `script(1)` to force a pseudo-terminal.
- **Slash commands** (e.g. `/speckit.*`) are best run in **interactive** mode; this wrapper can start an interactive Claude Code session in **tmux**.
- Use `--permission-mode plan` when you want read-only planning.
- Keep `--allowedTools` narrow (principle of least privilege), especially in automation.

## High‑leverage Claude Code tips (from the official docs)

### 1) Always give Claude a way to verify (tests/build/screenshots)

Claude performs dramatically better when it can verify its work.
Make verification explicit in the prompt, e.g.:
- “Fix the bug **and run tests**. Done when `npm test` passes.”
- “Implement UI change, **take a screenshot** and compare to this reference.”

### 2) Explore → Plan → Implement (use Plan Mode)

For multi-step work, start in plan mode to do safe, read-only analysis:
```bash
./scripts/claude_code_run.py -p "Analyze and propose a plan" --permission-mode plan
```
Then switch to execution (`acceptEdits`) once the plan is approved.

### 3) Manage context aggressively: /clear and /compact

Long, mixed-topic sessions degrade quality.
- Use `/clear` between unrelated tasks.
- Use `/compact Focus on <X>` when nearing limits to preserve the right details.

### 4) Rewind aggressively: /rewind (checkpoints)

Claude checkpoints before changes.
If an approach is wrong, use `/rewind` (or Esc Esc) to restore:
- conversation only
- code only
- both

This enables “try something risky → rewind if wrong” loops.

### 5) Prefer CLAUDE.md for durable rules; keep it short

Best practice is a concise CLAUDE.md (global or per-project) for:
- build/test commands Claude should use
- repo etiquette / style rules that differ from defaults
- non-obvious environment quirks

Overlong CLAUDE.md files get ignored.

### 6) Permissions: deny > ask > allow (and scope matters)

In `.claude/settings.json` / `~/.claude/settings.json`, rules match in order:
**deny first**, then ask, then allow.
Use deny rules to block secrets (e.g. `.env`, `secrets/**`).

### 7) Bash env vars don’t persist; use CLAUDE_ENV_FILE for persistence

Each Bash tool call runs in a fresh shell; `export FOO=bar` won’t persist.
If you need persistent env setup, set (before starting Claude Code):
```bash
export CLAUDE_ENV_FILE=/path/to/env-setup.sh
```
Claude will source it before each Bash command.

### 8) Hooks beat “please remember” instructions

Use hooks to enforce deterministic actions (format-on-edit, block writes to sensitive dirs, etc.)
when you need guarantees.

### 9) Use subagents for heavy investigation / independent review

Subagents can read many files without polluting the main context.
Use them for broad codebase research or post-implementation review.

### 10) Treat Claude as a Unix utility (headless, pipes, structured output)

Examples:
```bash
cat build-error.txt | claude -p "Explain root cause" 
claude -p "List endpoints" --output-format json
```
This is ideal for CI and automation.

## Interactive mode (tmux)

If your prompt contains lines starting with `/` (slash commands), the wrapper defaults to **auto → interactive**.

Example:

```bash
./scripts/claude_code_run.py \
  --mode auto \
  --permission-mode acceptEdits \
  --allowedTools "Bash,Read,Edit,Write" \
  -p $'/speckit.constitution ...\n/speckit.specify ...\n/speckit.plan ...\n/speckit.tasks\n/speckit.implement'
```

It will print tmux attach/capture commands so you can monitor progress.

## Spec Kit end-to-end workflow (tips that prevent hangs)

When you want Claude Code to drive **Spec Kit** end-to-end via `/speckit.*`, do **not** use headless `-p` for the whole flow.
Use **interactive tmux mode** because:
- Spec Kit runs multiple steps (Bash + file writes + git) and may pause for confirmations.
- Headless runs can appear idle and be killed (SIGKILL) by supervisors.

### Prerequisites (important)

1) **Initialize Spec Kit** (once per repo)
```bash
specify init . --ai claude
```

2) Ensure the folder is a real git repo (Spec Kit uses git branches/scripts):
```bash
git init
git add -A
git commit -m "chore: init"
```

3) Recommended: set an `origin` remote (can be a local bare repo) so `git fetch --all --prune` won’t behave oddly:
```bash
git init --bare ../origin.git
git remote add origin ../origin.git
git push -u origin main || git push -u origin master
```

4) Give Claude Code enough tool permissions for the workflow:
- Spec creation/tasks/implement need file writes, so include **Write**.
- Implementation often needs Bash.

Recommended:
```bash
--permission-mode acceptEdits --allowedTools "Bash,Read,Edit,Write"
```

### Run the full Spec Kit pipeline

```bash
./scripts/claude_code_run.py \
  --mode interactive \
  --tmux-session cc-speckit \
  --permission-mode acceptEdits \
  --allowedTools "Bash,Read,Edit,Write" \
  -p $'/speckit.constitution Create project principles for quality, accessibility, and security.\n/speckit.specify <your feature description>\n/speckit.plan I am building with <your stack/constraints>\n/speckit.tasks\n/speckit.implement'
```

### Monitoring / interacting

The wrapper prints commands like:
- `tmux ... attach -t <session>` to watch in real time
- `tmux ... capture-pane ...` to snapshot output

If Claude Code asks a question mid-run (e.g., “Proceed?”), attach and answer.

## Operational gotchas (learned in practice)

### 1) Vite + ngrok: "Blocked request. This host (...) is not allowed"

If you expose a Vite dev server through ngrok, Vite will block unknown Host headers unless configured.

- **Vite 7** expects `server.allowedHosts` to be `true` or `string[]`.
  - ✅ Allow all hosts (quick):
    ```ts
    server: { host: true, allowedHosts: true }
    ```
  - ✅ Allow just your ngrok host (safer):
    ```ts
    server: { host: true, allowedHosts: ['xxxx.ngrok-free.app'] }
    ```
  - ❌ Do **not** set `allowedHosts: 'all'` (won't work in Vite 7).

After changing `vite.config.*`, restart the dev server.

### 2) Don’t accidentally let your *shell* eat your prompt

When you drive tmux via a shell command (e.g. `tmux send-keys ...`), avoid unescaped **backticks** and shell substitutions in the text you pass.
They can be interpreted by your shell before the text even reaches Claude Code.

Practical rule:
- Prefer sending prompts from a file, or ensure the wrapper/script quotes prompt text safely.

### 3) Long-running dev servers should run in a persistent session

In automation environments, backgrounded `vite` / `ngrok` processes can get SIGKILL.
Prefer running them in a managed background session (Clawdbot exec background) or tmux, and explicitly stop them when done.

## OpenSpec workflow (opsx)

OpenSpec is another spec-driven workflow (like Spec Kit) powered by slash commands (e.g. `/opsx:*`).
In practice it has the same reliability constraints:
- Prefer **interactive tmux mode** for `/opsx:*` commands (avoid headless `-p` for the whole flow).

### Setup (per machine)

Install CLI:
```bash
npm install -g @fission-ai/openspec@latest
```

### Setup (per project)

Initialize OpenSpec **with tool selection** (required):
```bash
openspec init --tools claude
```

Tip: disable telemetry if desired:
```bash
export OPENSPEC_TELEMETRY=0
```

### Recommended end-to-end command sequence

Inside Claude Code (interactive):
1) `/opsx:onboard`
2) `/opsx:new <change-name>`
3) `/opsx:ff` (fast-forward: generates proposal/design/specs/tasks)
4) `/opsx:apply` (implements tasks)
5) `/opsx:archive` (optional: archive finished change)

If the UI prompts you for project type/stack, answer explicitly (e.g. “Web app (HTML/JS) with localStorage”).

## Bundled script

- `scripts/claude_code_run.py`: wrapper that runs the local `claude` binary with a pseudo-terminal and forwards flags.
