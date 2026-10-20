---
name: principle-guard-the-context-window
description: "Apply before a large read, a long command output, or a subagent brief, not only when context is filling up. Route bulk to subagents, take thin reports back, and keep summaries in the main thread, not raw payloads."
---

# Guard the Context Window

The context window is finite and non-renewable within a session. Every token should be worth its cost.

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Isolate large payloads.** Route verbose outputs, screenshots, and large documents to subagents. The main context gets summaries, not raw data.
- **Keep frequently used content inline.** Templates and references used on every invocation belong in the skill file, not in separate files that cost a read each time.
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.
- **Return thin.** When a subagent's report feeds your next step, its brief names where the full report goes, a file the subagent writes or the PR, and asks for only the verdict or status line, any blockers, and that path or URL. Read the full report only to act on a blocker. A subagent whose output is the deliverable you relay, such as a `how` explanation, a `why` synthesis, the trail reviewer's flags, or an arena cross-judge's scores, returns it in full.
- **Budget the lead's reads.** Send a file or command output longer than about 150 lines to a subagent unless you will edit it. Cut command output with `head`, `tail`, `grep`, or `--jq` before it reaches you. Do not reread a file a `how` pass already mapped unless you are about to edit it. A read that a playbook or skill step assigns to you, such as Code review's changed files, Eval's candidate outputs, or show-me-your-work's transcript audit, is exempt.
- **Read steps, not whole playbooks.** To open a worklist, print the playbook's prose before step 1 and its numbered steps with their indented sub-items (`awk '/^[0-9]+\. /{p=1} !p && !/^#/ && NF {print; next} p && /^[^ ]/ && !/^[0-9]+\. /{exit} p' <playbook>`) instead of the whole file. The prose before step 1 is the worklist's first item. When that prose says to read the playbook in full, read it in full.
