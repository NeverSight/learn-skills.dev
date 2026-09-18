---
name: w-yolo
description: Fix failing or requested local checks without publishing.
disable-model-invocation: true
---

Not a second full gate. Fix failing or requested local checks without publishing. Do not edit `.env`. Point at `/w-ship` if they want the full gate and a PR. Follow [git publish](references/git-publish.md) for the no-publish rule.

1. Use the smallest command that failed (or lint/w-test for the change). If the user named a command, run that. Never the full pre-push suite.
2. Fix owning causes. Re-run the failed command. Do not delete features to make a check pass. No secrets or unrelated dotfiles.
3. Optionally review the task diff with `/w-review` (read-only). Apply fixes only for defects you can evidence.
4. If CodeRabbit or CI comments exist and the user asked to consume them, follow `/w-coderabbit` or `/w-comments` without committing.
5. Docs: `/w-docs` if behavior or commands changed.
