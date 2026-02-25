---
name: oracle
description: Get a second opinion by bundling a prompt + a curated file set, then asking another powerful LLM for debugging, refactor advice, design checks, or code reviews.
---

# Oracle (cross-model)

Use this skill when you want a “second brain” pass from an *opposite model family* than the one you’re currently using.

- Under a model powered by **OpenAI** (e.g. GPT): bundle context, then ask **Claude CLI** (Opus 4.6) for review.
- Under a model powered by others (e.g. Claude, Gemini): bundle context, then ask **Codex CLI** (GPT-5.3-Codex, `xhigh` reasoning) for review.

## Workflow

1. Pick the smallest file set that contains the truth (avoid secrets by default).
2. Verify the selected files / bundle look right.
3. Run the oracle target you want: **Opus** (`oracle-to-opus`) if your current session is using an OpenAI model, **GPT-5.3-Codex** (`oracle-to-gpt`) otherwise.

## Commands

From the skill directory:

```bash
# Preview selection
$HOME/.agents/skills/oracle/scripts/oracle-bundle --dry-run -p "<task>" --file "src/**" --file "!**/*.test.*"

# Preview bundle
$HOME/.agents/skills/oracle/scripts/oracle-bundle -p "<task>" --file "src/**" --file "!**/*.test.*"

# Ask Claude Opus (Anthropic) if runnign under a model powered by OpenAI
$HOME/.agents/skills/oracle/scripts/oracle-to-claude -p "<task>" --file "src/**" --file "!**/*.test.*"

# Ask GPT-5.3-Codex (OpenAI) if runnign under any other model
$HOME/.agents/skills/oracle/scripts/oracle-to-codex -p "<task>" --file "src/**" --file "!**/*.test.*"
```

## Tips

- Prefer a minimal file set over “whole repo”.
- If you need diffs reviewed, paste the diff into the prompt or attach the diff file via `--file`.
- Make the prompt completely standalone: include intent, goals, constraints, error text (if any), and the desired output format (plan vs patch vs pros/cons.
- Never include secrets (`.env`, tokens, key files).
- Instruct the Oracle to be thorough. For example, if asking for a general code review, ask for feedback on the correctness of the solution, consistency with existing code, simplicity (no unecessary complexity, abstractions, etc), maintainability, performance, security, and edge cases.
- Don't blindly follow Oracle's ideas or recommendations. Reason from first principles, and be clear on what has merit, and what doesn't.
- Oracle can be slow while it reasons. Allow it several minutes to process.
