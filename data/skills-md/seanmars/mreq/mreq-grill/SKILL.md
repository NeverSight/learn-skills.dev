---
name: mreq-grill
description: Pressure-test an mreq task document under .mreq/ with a four-quadrant Known/Unknown interview, then write what it settles back into the document's Decisions, Tasks, Assumptions, and Open sections. Use when the user says "grill", "grill me", or wants to find unspoken assumptions and blind spots in a plan, or after mreq-define hands a document over.
argument-hint: "[<path>]"
---

# mreq-grill

Stress-test one `.mreq/` document until every assumption is named and every open question is answered or parked. Then write the outcome into the document.

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

Write every path with `/`, never with `\`, on Windows too: the script prints its paths that way, and a shell can drop a `\`. Run `uv run "${CLAUDE_SKILL_DIR}/../mreq-shared/scripts/mreq.py" <command>` first, with the script's path always in double quotes. When `uv` fails before the script starts (`uv` is not found, or `uv` prints its own error, for example a cache directory it cannot create), run `python` in place of `uv run`; when `python` is not found, run `python3`. An error the script prints is not a reason to switch, and neither is a denied command: follow "When a tool call is denied". The allow rule for a denied script command is `Bash(uv run *mreq.py*)` or `PowerShell(uv run *mreq.py*)` (`python` or `python3` in place of `uv run` when you ran it).

- `list --open`: open documents, most recently updated first. An item with `warning` or `error` is a file the script cannot trust: name it to the user.
- `update <path> [--status active]`: sets `updated` to now. Never write the dates yourself. `update` rewrites the file: read the document again before your next Edit of it.

## When a tool call is denied

Run every command on its own: no `cd`, `&&`, `||`, `;`, `|` or `$()`. When any command, Write, or Edit is denied, do not retry it another way: no other shell, no other path, no other form of the command. Show the user each denied command or path exactly as you ran it, with one allow rule for each. Use the rule this file gives for it; otherwise, for a command, write the tool you ran it in and the exact command, with no `*`, for example `Bash(python -m unittest discover -s tests)`. Never merge two denied commands into one rule, and never suggest a broader rule. Then stop.

## Steps

1. **Pick the document.**
   Use the path the user gave, or the one document this conversation is about. Otherwise run `list --open` and let the user pick, even when only one exists. Never pick one yourself.
   Ask one question (see "Asking the user") with one option per document, in the order `list` gives: its title as the label, and its status, task progress and absolute path in the description. With one document, add **Stop** as the second option. With more than 4, offer the first 4 and say in the question that the user can type another document's path in the free-text answer.
   When there is no open document, say so and suggest `/mreq-define`. Do not invent a subject.

2. **Read it and the code it cites.**
   When its `status` is `done`, say so before you read the code, and ask once: **Reopen** (grill it; step 5 sets it back to `active`), **Discuss only** (grill it, but write nothing in step 5), or **New document** (suggest `/mreq-define` and stop).
   When `## Handoff` has an `Unconfirmed:` line, tell the user first: nobody confirmed this document's assumptions and decisions. Grill each of them as a known unknown.

3. **Sweep the four quadrants.**
   Read `GRILL.md` in the `mreq-shared` directory (`../mreq-shared` from this skill's directory) and follow it. The subject is the document. Report the four quadrants separately, in the order it gives.

4. **Restate and get confirmation.**
   In your own words: the claims that held and the ones that fell, the assumptions now explicit, the decisions made (each with its reason and the alternative ruled out), and what is still open.

   Then ask one question (see "Asking the user") with these three options, the first one recommended:
   - **Correct, write it into the document**: go to step 5, then step 6.
   - **Correct, write it into the document, then implement**: go to step 5, then run `mreq-apply` on the document (step 6).
   - **Something is wrong**: ask one multi-select question (`multiSelect`) that lists up to 4 restated items most likely to be wrong, assumptions first, each as an option. Then grill each item the user picked, and restate again.

   When the user picked **Discuss only** in step 2, step 5 writes nothing: offer **Correct, stop here** (go to step 6), **Grill more** (go back to step 3) and **Something is wrong** instead.

   Tell the user that, when something is wrong, they can type the correction as a free answer: with `AskUserQuestion`, in the free-text option at the bottom of the question; in plain text, as a reply in place of a number. Word the options and this hint in your own words each time; keep their meaning. A correction means keep grilling, then restate again. Running out of questions is not confirmation; only the user's pick of a "Correct" option is.

5. **Write the outcome into the document.**
   - Change only the body, section by section, with Edit. Never rewrite the whole file and never touch the front matter: `update` owns it.
   - Write each part of the step 4 restatement into its section:
     - **Decisions made**: add or change `### Dn:` entries in `## Decisions`. When a decision replaces an old one, rewrite it and add `Changed by grill: <what it said before>`.
     - **Assumptions now explicit**: `## Assumptions`, one bullet each.
     - **Claims that fell**: correct the section that states them (`## Goal`, `## Scope`, `## Context`, or the schema's own sections). Change those sections nowhere else, except where the user corrected them.
     - **Still open**: `## Open`, one `- Open: <question>` bullet each. A follow-up you found goes there too, as `- Follow-up: <what>`.
   - Change `## Tasks` when a decision changes the work. Never uncheck or reword a done task; put the correction in a new task or in `## Open`.
   - Delete an `Unconfirmed:` line in `## Handoff`: the user has now confirmed a restatement.
   - Run `update <path>`. For a reopened `done` document, run `update <path> --status active`.

6. **Ask for the next step.**
   When the user picked **Correct, write it into the document, then implement** in step 4, do not ask: run the `mreq-apply` skill on this document now (in Claude Code: with the Skill tool).

   Otherwise, ask one question (see "Asking the user"), the first option recommended:
   - **Implement (mreq-apply)**: run the `mreq-apply` skill on this document (in Claude Code: with the Skill tool).
   - **Grill more**: go back to step 3.
   - **Stop here**: give the document's absolute path.

   When the Skill call is denied, give the user `/mreq-apply <path>` and the allow rule `Skill(mreq-apply)`, then stop. Never read another skill's SKILL.md and follow it yourself.

## Guardrails

- Write only to the document being grilled. Never edit source code.
- Do not create files, even temporary ones. When a claim needs a measurement, make it a task or an `Open:` item.
- Write nothing before the user confirms the restatement.
- When the user wants to keep going after the restatement, keep going.
