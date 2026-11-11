---
name: recap
description: "Recap finished work for its owner, as a chat reply, a PR body, a file or a page. Use when handing over a finished task, when asked to show the work, or for the PR body of finished work."
---

# Recap

A recap tells the owner what the agent did, so they can accept the work without re-reading it.
Take the facts from your own session and pipeline: the conversation, the diff, the PR, the checks you ran.

## Steps

1. **Write the recap** in the form of [format.md](references/format.md), with the prose of the `plain-writing` skill.
   Start from the example closest in size: [small-fix](examples/small-fix/recap.md), [interview-sensei](examples/interview-sensei/recap.md), [research](examples/research/recap.md).
   Size it to the work: a small fix is a verdict, one or two items and one check.
   Done when each claim names where it holds: a file, a command and its result, or a link.
2. **Deliver it** to every place that applies:

   | Where | When | How |
   |---|---|---|
   | the chat | always | reply with the text |
   | a PR | a PR exists, or the pipeline opens one | write the text to a temporary file outside the project, then `gh pr create --body-file <file>` or `gh pr edit --body-file <file>` |
   | a file | the owner or the pipeline asks for one | `<repo>/.reports/recap/<date>-<topic>.md`; add `.reports/` to `.git/info/exclude` when `.gitignore` lacks it |
   | a page | the owner asks to see the work, or must accept it | build it by [page.md](references/page.md) |

3. **If you built a page, show it.** When the app can show HTML inside the chat, use its way; in Orca that is the `orca-chat-visuals` skill.
   Otherwise save it as `<date>-<topic>.html` next to the file, give its path, and open it when the machine has a screen (`open` on macOS, `xdg-open` on Linux).
