---
name: counselors
description: "Fan out a prompt to multiple AI coding agents in parallel and synthesize their responses."
---

# Counselors — Multi-Agent Review Skill

Fan out a prompt to multiple AI coding agents in parallel and synthesize their responses.

Arguments: $ARGUMENTS

**If no arguments provided**, ask the user what they want reviewed.

---

## Phase 1: Context Gathering

Parse `$ARGUMENTS` to understand what the user wants reviewed. Then auto-gather relevant context:

1. **Files mentioned in the prompt**: Use Glob/Grep to find files referenced by name, class, function, or keyword
2. **Recent changes**: Run `git diff HEAD` and `git diff --staged` to capture recent work
3. **Related code**: Search for key terms from the prompt and read the most relevant files (up to 5 files, ~50KB total cap)

Be selective — don't dump the entire codebase. Pick the most relevant code sections.

---

## Phase 2: Agent Selection

**Default agents:** `or-claude-opus`, `or-gemini-3.1-pro`, `or-codex-5.4`

1. **Use defaults unless the user overrides.** If `$ARGUMENTS` does not contain agent-selection instructions (e.g. "use all agents", "add codex", "only gemini"), skip directly to the confirmation step with the defaults.

2. **If the user requests different agents** (in `$ARGUMENTS` or via follow-up), discover available agents by running via Bash:
   ```bash
   counselors ls
   ```
   Print the full output, then ask the user to pick using AskUserQuestion.

   **If 4 or fewer agents**: Use AskUserQuestion with `multiSelect: true`, one option per agent.

   **If more than 4 agents**: AskUserQuestion only supports 4 options. Use these fixed options:
   - Option 1: "All [N] agents" — sends to every configured agent
   - Option 2-4: The first 3 individual agents by ID
   - The user can always select "Other" to type a comma-separated list of agent IDs from the printed list above

   Do NOT combine agents into preset groups (e.g. "claude + codex + gemini"). Each option must be a single agent or "All".

3. **MANDATORY: Confirm the selection before continuing.** Echo back the exact list you will dispatch to:

   > Dispatching to: **or-claude-opus**, **or-gemini-3.1-pro**, **or-codex-5.4**

   Then ask the user to confirm (e.g. "Look good?") before proceeding to Phase 3. This prevents silent tool omissions. If the user corrects the list, update your selection accordingly.

---

## Phase 3: Prompt Assembly

1. **Generate a slug** from the topic (lowercase, hyphens, max 40 chars)
   - "review the auth flow" → `auth-flow-review`
   - "is this migration safe" → `migration-safety-review`

2. **Create the output directory** via Bash. The directory name MUST always be prefixed with a **second-precision** UNIX timestamp so runs are lexically sortable and never collide:
   ```
   ./agents/counselors/TIMESTAMP-[slug]
   ```
   For example: `./agents/counselors/1770676882-auth-flow-review`

   > **Mac tip:** Generate with `date +%s` (seconds since epoch). Millisecond precision is NOT available via `date` on macOS without GNU coreutils — use `date +%s` for portable second-precision timestamps.

3. **Write the prompt file** using the Write tool to `./agents/counselors/TIMESTAMP-[slug]/prompt.md`:

```markdown
# Review Request

## Question
[User's original prompt/question from $ARGUMENTS]

## Context

### Files Referenced
[Contents of the most relevant files found in Phase 1]

### Recent Changes
[git diff output, if any]

### Related Code
[Related files discovered via search]

## Instructions
You are providing an independent review. Be critical and thorough.
- Analyze the question in the context provided
- Identify risks, tradeoffs, and blind spots
- Suggest alternatives if you see better approaches
- Be direct and opinionated — don't hedge
- Structure your response with clear headings
```

---

## Phase 4: Dispatch

Tell the user before dispatching:
> "Dispatching to [N] agents: [list]. This typically takes 2-5 minutes..."

Note the **prompt directory path** you created (e.g. `./agents/counselors/1772865337-auth-flow-review/`). The counselors CLI creates a sibling output directory with a second timestamp suffix.

Run counselors via Bash with the prompt file, passing the user's selected agents:

```bash
set -a; for f in ~/.env .env ~/.vibe-tools/.env; do [ -f "$f" ] && source "$f"; done; set +a; counselors run -f ./agents/counselors/[slug]/prompt.md --tools [comma-separated-selections] --json
```

> **Why the env sourcing?** Claude Code's Bash tool may not inherit API keys (e.g. `OPENAI_API_KEY`) from the user's interactive shell. The `set -a` + source pattern loads keys from standard dotenv files portably (works in bash, zsh, sh). Files that don't exist are silently skipped.

Example: `--tools claude,codex,gemini`

Use Bash `timeout: 480000` (8 minutes). Tools run in parallel (not sequentially). Per-tool timeouts in the counselors config control how long each individual tool gets.

**Important**: Use `-f` (file mode) so the prompt is sent as-is without wrapping. Use `--json` to get structured output for parsing.

---

## Phase 5: Read Results (filesystem-based — does NOT depend on stdout)

**IMPORTANT:** Do NOT rely solely on JSON stdout. The CLI only writes `run.json` and prints JSON after ALL tools finish. If any tool hangs or the process is killed, stdout will be empty. Always fall back to scanning the filesystem.

**Step 1: Find the output directory.**
```bash
ls -dt ./agents/counselors/[slug]-*/ 2>/dev/null | head -1
```
If no directory found, the CLI failed before dispatching. Tell the user and suggest `counselors doctor`. **Stop.**

**Step 2: Check for `run.json` (happy path).**
If `run.json` exists, parse it:
- `status: "success"` with `wordCount > 0` — genuine success
- `status: "timeout"` — tool hit its timeout
- `status: "error"` — tool crashed
- `status: "success"` with `wordCount: 0` — **silent failure** (read `.stderr`)

**Step 3: If NO `run.json`, scan for individual files.**
For each expected tool, check if `{tool-id}.md` exists and has size > 0. Check `{tool-id}.stderr` for error details.

**Step 4: Report to user.**
- **All tools produced output:** Proceed to Phase 6.
- **Some tools produced output:** Tell the user which failed and why, then ask: "Continue with [N] of [M] responses, or retry?"
- **Zero tools produced output:** Report errors. Suggest `counselors doctor`. **Stop.**

---

## Phase 6: Synthesize and Present

Combine all agent responses into a synthesis:

```markdown
## Counselors Review

**Agents consulted:** [list of agents that responded]

**Consensus:** [What most agents agree on — key takeaways]

**Disagreements:** [Where they differ, and reasoning behind each position]

**Key Risks:** [Risks or concerns flagged by any agent]

**Blind Spots:** [Things none of the agents addressed that seem important]

**Recommendation:** [Your synthesized recommendation based on all inputs]

---
Reports saved to: [output directory from manifest]
```

Present this synthesis to the user. Be concise — the individual reports are saved for deep reading.

---

## Phase 7: Action (Optional)

After presenting the synthesis, ask the user what they'd like to address. Offer the top 2-3 actionable items from the synthesis as options. If the user wants to act on findings, plan the implementation before making changes.

---

## Error Handling

- **counselors not installed**: Tell the user to install it (`npm install -g counselors`)
- **No tools configured**: Tell the user to run `counselors init` or `counselors add`
- **No output directory created**: CLI failed before dispatching (bad config, missing binary). Check stderr from the Bash call.
- **Output directory exists but no `run.json`**: CLI was killed before all tools finished. Scan for individual `.md` files — completed tools will have written their output. This is the most common partial-failure mode.
- **Silent failure** (`status: "success"` but `wordCount: 0`, or `.md` file is 0 bytes): Read the `.stderr` file. Common causes: expired API key, 402 payment required, rate limit.
- **Single agent fails**: Note it, ask user whether to continue with remaining responses or retry.
- **All agents fail**: Report each error from `.stderr` files. Suggest `counselors doctor`. Do NOT proceed to synthesis.
- **Never wait indefinitely**: The 8-minute Bash timeout is the hard ceiling. Do not add sleep/retry loops.
