---
name: mreq-close
description: Finish an mreq task document under .mreq/. Check that the code does what the document agreed, then delete the document. Use for /mreq-close.
argument-hint: "[<path>]"
disable-model-invocation: true
---

# mreq-close

Run only when the user typed `/mreq-close`. If you are reading this file on your own, stop and ask the user to run `/mreq-close <path>`.

Check the code against one `.mreq/` document, then delete the document. The code is the record of what was done.

**Input**: Optional. A document path.

## Language

Write and reply in the language the agent instruction files (`AGENTS.md`, `CLAUDE.md`, ...) set. When they set none, use the language the user writes in. A reply that only picks an option (`1`, `Accept the code`) or gives a path does not change it. When the user has written no natural language yet (only a command or a path), use the language of the document: the language of its title and `## Goal`, not of the template's headings or text. A title such as `add 輸入 1,000 時當掉` means Traditional Chinese, though every heading is English. Use that language in every message, from the first line to the report, including the short notes between tool calls. Only fixed labels such as `Open:` stay as written.

## Asking the user

When the `AskUserQuestion` tool is available, ask with it: up to 4 independent questions at once, the recommended option first and labelled "(Recommended)". Otherwise, ask in plain text as a numbered list, the recommended option first, and wait for the answer.

Ask with options, so the user picks instead of types:
- Give every question 2 to 4 options. Keep each label short (1 to 5 words) and put the detail in its description. Keep each `header` to 12 characters or fewer.
- Never add an "Other" option: `AskUserQuestion` adds a free-text answer to every question. When an answer may need a value no option holds (a path, a correction), say in the question that the user can type it there.
- Ask for a typed answer only when no option can hold it, such as an error message only the user has seen. When you can guess the answer, offer the guess as an option.
- Never ask the user to type a command that this skill's steps say to run for them.

## The script

The script is `${CLAUDE_SKILL_DIR}/../mreq-shared/scripts/mreq.py`. `${CLAUDE_SKILL_DIR}` is this skill's directory; when it still reads as a variable, put the directory's absolute path in its place. Every document path you show the user is the absolute path the script printed.

- `list`: every document, most recently updated first. An item with `warning` or `error` is a file the script cannot trust: name it to the user.
- `delete <path>`: deletes the document. It refuses any file outside `.mreq/`.

Write every path with `/`, never with `\`, on Windows too: the script prints its paths that way, and a shell can drop a `\`. Run `uv run "${CLAUDE_SKILL_DIR}/../mreq-shared/scripts/mreq.py" <command>` first, with the script's path always in double quotes. When `uv` fails before the script starts (`uv` is not found, or `uv` prints its own error, for example a cache directory it cannot create), run `python` in place of `uv run`; when `python` is not found, run `python3`. An error the script prints is not a reason to switch, and neither is a denied command: follow "When a tool call is denied". The allow rule for a denied script command is `Bash(uv run *mreq.py*)` or `PowerShell(uv run *mreq.py*)` (`python` or `python3` in place of `uv run` when you ran it).

## When a tool call is denied

Run every command on its own: no `cd`, `&&`, `||`, `;`, `|` or `$()`. When any command, Write, or Edit is denied, do not retry it another way: no other shell, no other path, no other form of the command. Show the user each denied command or path exactly as you ran it, with one allow rule for each. Use the rule this file gives for it; otherwise, for a command, write the tool you ran it in and the exact command, with no `*`, for example `Bash(python -m unittest discover -s tests)`. Never merge two denied commands into one rule, and never suggest a broader rule. Then stop.

## Steps

1. **Pick the document.**
   Use the path the user gave. Otherwise run `list` and let the user pick, documents with `status` `done` first. Never pick one yourself. Ask one question (see "Asking the user") with one option per document, in that order: its title as the label, and its status, task progress and absolute path in the description. With one document, add **Stop** as the second option. With more than 4, offer the first 4 and say in the question that the user can type another document's path in the free-text answer. Your first message starts with the line `Closing: <absolute path>`, also when the user gave the path: when they gave it, say it before any tool call; otherwise, right after they pick.
   When this conversation made the changes (for example, it ran `mreq-apply` on this document), the audit is not independent: say so, recommend running `/mreq-close <path>` in a new session, and ask once: **Continue here** or **Stop**. Stop: give `/mreq-close <path>` and stop.

2. **Check the tasks.**
   When a task is unchecked, ask once:
   - **Continue (mreq-apply)**: hand the document to `mreq-apply` (see "Handing over to mreq-apply"), with no findings.
   - **Close anyway**: go on, and name the unfinished tasks in the report.
   - **Keep it**: stop.

3. **Check the code against the document.**
   1. **Audit.** Audit it yourself, under these rules.
      - Judge only from the document and the code as you read them now, not from what you remember of this conversation.
      - Read the document and every file it cites in full: this is an audit, not a search.
      - For `## Goal`, each `### Dn:` in `## Decisions`, and each checked task: does the code do it? Answer done, partly done, done differently, or missing, with `path:line`.
      - A finding is code that contradicts the document or misses something it asked for. Code that adds a detail the document did not mention, without contradicting it, goes in the not-asked-for list.
      - Note anything the code does that the document never asked for.
      - Run no command that executes the project's code or writes a file.
   2. **Run.** After the audit, run the checks the document names, and only those.
      - **What to run**: its test command (when it names none, the one in the project's README or agent instruction files); for `issue`, the `## Symptom` repro; for `refactor`, the `## Behavior Pin`; and the check a task names.
      - **When to skip the test command**: skip it when a checked task's work is to run the related tests (for example the `issue` template's "Run the related tests"): `mreq-apply` ran them to check that task off. Do not look for another test command then. A task that only says how it is checked, or an unchecked one, does not count. This skips only the test command: still run the repro, the Behavior Pin, and each task's own check.
      - **As written**: run each command exactly as written: add no `uv run`, and use no `python -c` in its place. When a check needs a script, run it inline.
      - **Off the real data**: when a check writes or changes files beyond caches (a data file, a database), keep it off the project's real data: point it at a new path the command accepts (for example a `--file` option), or give it to the user to run. That new path is the only change you make to a command.
      - **No checks of your own**: add none, not even to confirm a finding: the audit's `path:line` is the evidence.
      - **A denied command**: when any command you ran in this step is denied, do not retry it another way, and do not stop: it goes to **Tests not run** in step 4.

4. **Act on the result.**
   - **All done, tests pass**: go to step 5.
   - **Tests already run by a task** (step 3 skipped the test command because a checked task ran it): this alone asks nothing. When no other case in this list applies, go to step 5. Never call it a pass: name it in the report with the task number.
   - **Failing tests**: name each failure, and ask once: **Fix now (mreq-apply)** (hand the document to `mreq-apply` with each failure as a finding; see "Handing over to mreq-apply") or **Stop** (give `/mreq-apply <path>` with the failures, then `/mreq-close <path>` again).
   - **Tests not run** (a command in step 3 was denied, or you found no tests): give the user each command that did not run, exactly as you ran it, with one allow rule for each denied one (see "When a tool call is denied"), and ask once: **Close anyway** or **Keep it**. Never count it as a pass. Close anyway: go on, and name it in the report. Keep it: stop.
   - **A finding** (partly done, done differently, missing): ask one question per finding. Quote the document's line, say what the code does, and offer **Accept the code** or **Fix the code**.
     - Any **Fix the code**: hand the document to `mreq-apply` with those findings, and any failing test (see "Handing over to mreq-apply").
     - All **Accept the code**: go to step 5, and name each finding in the report as an accepted departure.

   Ask the finding questions up to 4 at a time; when there are more, ask the next ones after the user answers.

5. **Delete the document.**
   Do this only after every step 4 question is answered.
   Before the delete, collect the items in `## Open`, and any follow-up, `Open:` or `Unconfirmed:` line still in `## Handoff`: nothing keeps them once the file is gone. They go in the report.
   Run `delete <path>`; never delete with another command. Do not check git, and do not ask before the delete.

6. **Report.**
   What was deleted, what the check found, each accepted departure, unfinished tasks and tests not run if any, the test command not rerun and the task that ran it, the follow-ups from step 5, every file a check left behind (other than caches), and anything the code does that the document never asked for.

## Handing over to mreq-apply

Do this only where a step above says so, and never delete the document then.
1. Tell the user that after the fixes, `/mreq-close <path>` checks the code again, best in a new session after a commit.
2. Run the `mreq-apply` skill (in Claude Code: with the Skill tool). Pass the document's absolute path as its argument, then each finding or failure on its own line: the document's line, what the code does, and its `path:line` or the failing command.
3. Do nothing more in this skill. When the Skill call is denied, give the user `/mreq-apply <path>` with the findings, and the allow rule `Skill(mreq-apply)`, then stop. Never read another skill's SKILL.md and follow it yourself.

## Guardrails

- Never edit source code or the document. Fixes go through `mreq-apply`.
- Create no files yourself; caches the test run leaves are fine, and so is a new data path a check needs (step 3).
- Delete only in step 5, after every question in steps 1 to 4 is answered. Never delete after handing the document to `mreq-apply`.
- Run the check in step 3 unless the user explicitly asks to skip the check. "Just close it" alone does not skip it.
