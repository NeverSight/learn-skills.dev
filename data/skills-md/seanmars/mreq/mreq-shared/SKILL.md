---
name: mreq-shared
description: Shared files for the other mreq skills, not a task. Holds the task-document script, its templates, the page script, the Pele bundle, the diagram checker, the grill method and the Mermaid rules. Never run it on its own.
disable-model-invocation: true
user-invocable: false
---

# mreq-shared

This skill does nothing on its own. If you are reading this file because a user asked for something, stop: nothing here is a task. Tell the user which mreq skill fits their request (`/mreq-define`, `/mreq-how`, `/mreq-graph`, ...) and do not use any file here.

The other mreq skills find this directory at `../mreq-shared` from their own directory, and use these files by path. Each skill's `SKILL.md` says when to read or run them.

| File | What it is | Used by |
| --- | --- | --- |
| `scripts/mreq.py` | Creates, lists, updates, shows the progress of, and deletes task documents under `.mreq/` | mreq-define, mreq-grill, mreq-apply, mreq-close |
| `templates/` | One task-document template per schema; `mreq.py new` reads them | `mreq.py` |
| `scripts/page.py` | Builds and checks the offline page. Its first argument, `how` or `graph`, picks the output folder under `.mreq/` and that skill's `skeleton.html` | mreq-how, mreq-graph |
| `GRILL.md` | How to grill a document or a restatement: the four quadrants, the interview rules and the limits | mreq-grill, mreq-define |
| `MERMAID.md` | How to write a diagram figure: the markup, size, colors, Mermaid rules and the legend | mreq-how, mreq-graph |
| `vendor/pele.global.js` | Pele (https://pele.run/), which draws the Mermaid diagrams; `page.py build` inlines it in each page | `page.py` |
| `scripts/check.mjs` | Renders each diagram with Pele in Node, so the build sees the errors the browser would show | `page.py` |

Never edit these files while running another skill.
