---
name: counselors
description: Fan out a prompt to multiple AI coding agents in parallel and synthesize their responses.
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

**Default agents:** `claude-opus`, `gemini-3-pro-preview`, `amp-smart`

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

   > Dispatching to: **claude-opus**, **gemini-3-pro-preview**, **amp-smart**

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

Run counselors via Bash with the prompt file, passing the user's selected agents:

```bash
counselors run -f ./agents/counselors/[slug]/prompt.md --tools [comma-separated-selections] --json
```

Example: `--tools claude,codex,gemini`

Use `timeout: 600000` (10 minutes). Counselors dispatches to the selected agents in parallel and writes results to the output directory shown in the JSON output.

**Important**: Use `-f` (file mode) so the prompt is sent as-is without wrapping. Use `--json` to get structured output for parsing.

---

## Phase 5: Read Results

1. **Parse the JSON output** from stdout — it contains the run manifest with status, duration, word count, and output file paths for each agent
2. **Read each agent's response** from the `outputFile` path in the manifest
3. **Check `stderrFile` paths** for any agent that failed or returned empty output
4. **Skip empty or error-only reports** — note which agents failed

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
- **Agent fails**: Note it in the synthesis and continue with other agents' results
- **All agents fail**: Report errors from stderr files and suggest checking `counselors doctor`
