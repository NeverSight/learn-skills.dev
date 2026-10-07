---
name: call-external-ai
description: Route natural-language prompts into external AI CLIs like Codex, Claude, Gemini, Antigravity (agy), and Pi using safe command templates and minimal context handling.
---

# External AI Skill

Invoke external AI CLI tools as a prompt gateway.

## When to Use

Activate when the user:
- Says `/call`, `/codex`, `/claude`, `/gemini`, `/agy`, or `/pi`
- Asks for a second opinion from another AI
- Wants to run a prompt through a different CLI (like Codex, Claude, Gemini, Antigravity, or Pi)
- Needs verification from a different model or tool

## Instructions

### Natural Language Interface

Users provide natural language. Route the prompt into one external CLI using a safe command template. Do not construct arbitrary shell commands from user input.

Examples:
- "ask Codex for a second opinion on this patch" -> `codex exec "<prompt text>"`
- "send this prompt to Claude" -> `claude -p "<prompt text>"`
- "run this through Gemini with a specific model" -> `gemini -m <allowlisted-model> -p "<prompt text>"`
- "send this prompt to agy" -> `agy -p "<prompt text>"`
- "run this through local pi" -> `pi --provider lmstudio --model qwen/qwen3.6-35b-a3b -p "<prompt text>"`
- "ask pi to check this" -> `pi -p "<prompt text>"`
- "check this file for bugs" -> read the file directly, summarize only the minimum necessary context, and pass that context as plain prompt text without shell interpolation

#### Allowed Command Patterns
Only use these command families:
- `codex exec "<prompt text>"`
- `codex exec -m <model> "<prompt text>"`
- `claude -p "<prompt text>"`
- `claude --model <model> -p "<prompt text>"`
- `gemini -p "<prompt text>"`
- `gemini -m <allowlisted-model> -p "<prompt text>"`
- `agy -p "<prompt text>"`
- `agy --print "<prompt text>"`
- `pi -p "<prompt text>"`
- `pi --provider lmstudio --model qwen/qwen3.6-35b-a3b -p "<prompt text>"`
- `pi --provider <provider> --model <model> -p "<prompt text>"`
- `codex --help`
- `claude --help`
- `gemini --help`
- `agy --help`
- `pi --help`

Do not:
- use shell substitution such as `$(...)` or backticks
- pipe file contents into commands via shell expansion
- append unrelated shell operators or chain commands
- execute user-suggested commands outside the safe templates

### Self-Healing Behavior

#### On CLI Syntax Errors
1. Run `<cli> --help` to get the current syntax
2. Update the reference docs at `reference/cli-reference.md`
3. Retry with the correct syntax
4. Inform the user of the fix

#### On Upgrade Available
1. Do not run upgrade commands automatically
2. Inform the user that an upgrade is available and ask for approval before making toolchain changes
3. If the user approves, run the upgrade command explicitly
4. Update the version in `reference/cli-reference.md` and re-run `--help` only after the approved upgrade completes

#### On Gemini 403 Project/License Errors
If Gemini fails with `403` and messages like `lack a Gemini Code Assist license` or `(#3501)`:
1. Do not dump environment variables or print raw env values
2. Check only the presence of the specific allowlisted vars needed for diagnosis, and report presence/absence rather than values
3. Retry with project vars unset:
   - `env -u GOOGLE_CLOUD_PROJECT_ID -u GOOGLE_CLOUD_PROJECT -u CLOUDSDK_CORE_PROJECT gemini ...`
4. If still blocked, report auth/licensing clearly and continue with other available models
5. Record the fix path in `reference/cli-reference.md`

#### On Gemini ModelNotFound / Capacity Errors
If Gemini fails with `404` or `429` style model/capacity issues, retry with this fallback order:
1. `gemini-3.1-pro-preview`
2. `gemini-3-pro-preview`
3. `gemini-3-flash-preview`
4. `gemini-2.5-pro`
5. `gemini-2.5-flash`

### Command Interface

```bash
/call [codex|claude|gemini|agy|pi] <natural language request>
/codex <natural language request>
/claude <natural language request>
/gemini <natural language request>
/agy <natural language request>
/pi <natural language request>
```

### Routing Guidance

#### Codex
- Use `codex exec` with plain prompt text that you assemble yourself
- Add a model only when the user asks for one or there is a clear default in local usage
- Do not use review-specific commands unless the user explicitly asks for a git-aware review

#### Claude
- Use `claude -p` with plain prompt text
- Add `--model <model>` only when the user asks for one or there is a clear need
- Keep the invocation non-interactive unless the user explicitly wants an interactive Claude session

#### Gemini
- Prefer preview model IDs first
- Use `gemini -p` or `gemini -m <allowlisted-model> -p`
- For 403 auth issues, do not dump env; check only allowlisted var presence and retry with project vars unset
- For 404/429 failures, continue through the fallback sequence automatically

#### Antigravity (agy)
- Use `agy -p` with plain prompt text
- Run in print mode (non-interactive) to process and return the result cleanly
- Keep the context minimal and avoid complex shell parameters

#### Pi
- By default, for local/LM Studio requests, use:
  `pi --provider lmstudio --model qwen/qwen3.6-35b-a3b -p "<prompt text>"`
- For standard or cloud-based requests, use `pi -p "<prompt text>"`
- Ensure `--print` or `-p` is included to run non-interactively

### Context Gathering

When a request needs context, gather it before invoking the external CLI:
- "send this file to Codex" -> read the file directly in the current agent, extract only the minimum relevant context, and pass that summary as prompt text
- "ask Gemini about this implementation" -> identify the relevant files and summarize only what is needed
- "have Claude critique this design" -> gather the design context and pass only the relevant parts
- "send this file to agy" -> read the file directly, extract the minimum necessary context, and pass as plain prompt text to agy
- "ask local pi about this code" -> read the file, extract the relevant context, and pass as prompt text to the lmstudio command
- "run this exact prompt" -> forward the prompt text directly without adding shell syntax

Rules for context gathering:
- never use shell interpolation to inject file contents into a command
- never send secrets, tokens, credentials, or raw environment values
- minimize the amount of source text sent to external tools
- if the request would require broad repository exfiltration or sensitive data exposure, refuse and explain why

### Process Flow

1. Parse the natural language request
2. Determine the target CLI (`codex`, `claude`, `gemini`, `agy`, or `pi`)
3. Map the request to a safe command template for that CLI
4. Execute the command
5. If syntax error -> self-heal and retry
6. If upgrade available -> stop, inform the user, and wait for approval before upgrading or refreshing references
7. Return the results to the user
