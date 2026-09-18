---
name: w-coderabbit
description: Fetch CodeRabbit review comments, apply authorized fixes, and stop at local verification.
disable-model-invocation: true
---

Fetch CodeRabbit comments for the current PR or uncommitted diff. Apply high-confidence fixes. Follow [git publish](references/git-publish.md). Do not commit unless asked.

1. Identify the branch and PR with `gh`. If there is no PR, review the current task diff.
2. Fetch CodeRabbit comments via the available CodeRabbit MCP. Group by file and severity.
3. Fix root causes starting with critical/high. Follow repository rules. Run the repo lint/type/w-test commands that match the change.
4. Leave style-only or unclear items as a list. Do not invent security or quality bars.
5. Docs: `/w-docs` if behavior or commands changed.
