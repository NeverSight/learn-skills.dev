---
name: code-reviewer
description: Use when explicitly asked to run the code-reviewer subagent or when another skill requires the code-reviewer agent card.
---

# Code Reviewer Subagent

Use the `code-reviewer` agent card to handle this specialized task.

## Run

```bash
codex-subagent code-reviewer <<'EOF'
[Provide the task context, scope, and any issue/PR numbers.]
EOF
```

## Notes

- Include concrete scope and constraints in the context block.
- Fold the subagent output back into the main workflow.
