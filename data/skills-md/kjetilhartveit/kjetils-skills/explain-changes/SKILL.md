---
name: explain-changes
description: Use when the user asks to explain changes (code changes or any other changes).
---

# Explain changes

One review page, the same in every AI tool, that shows exactly what changed. `assets/review.py` builds it from git,
from file snapshots taken before and after, and from the commands it ran itself. You never retell the changes from
memory: the only text you write is a short description at the top and the notes on files and changes, and the page
says which parts are yours.

## Use this skill when

- Use when the user asks to explain changes (code changes or any other changes).
- Check changes you made: a repo, files outside a repo, a scheduled task, an integration.

This isn't `explain-visually`. That one explains a decision or a design in a story; this one shows the changes themselves, quickly, with the diff as the main thing.

## Pick the route

| What changed                                                                                | Review it with                                                                                         |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| A GitHub repo, pushed branch                                                                | The page **and** the GitHub compare link on it. A draft PR only when the task or the user asks for one |
| A local repo or unpushed work                                                               | The page, `--git <repo>`. Uncommitted and untracked files are included and flagged                     |
| Files outside a repo                                                                        | A session: `begin --files <path>` before you change them                                               |
| State you can only read with a command (cron, Task Scheduler, a service, an API's settings) | A session: `begin --capture NAME=COMMAND` before, the page diffs the output after                      |
| A one-off command with side effects                                                         | Run it through `review.py run`, so the command, exit code and output are recorded                      |
| An MCP tool call (Notion, TickTick, email)                                                  | `review.py note`, with the raw result saved to a file as `--evidence`. It shows as "reported by agent" |

GitHub's own PR view and the AI tools' diff views are good too, and better for line comments. The page is for what
they don't cover: changes outside a repo, several repos at once, state and actions, and one look across tools.

## How

`review.py` needs Python 3.10+ and git, nothing else. `<skill>` is this skill's folder (`~/.agents/skills/explain-changes`).

**Repo only**, at the end:

```bash
python <skill>/assets/review.py render --git . --out <scratchpad>/review/review.html
python <skill>/assets/review.py render --git C:/git/a --git C:/git/b=origin/develop --description why.md --out review.html
```

The diff is from the merge base with the base branch (default `origin/HEAD`) to the working tree, so it shows
committed, uncommitted and untracked changes together. Commits, push status and the compare link come with it.

**Anything else**, a session in the scratchpad. Start it _before_ the first change:

```bash
R="python <skill>/assets/review.py"
$R begin <scratchpad>/review --title "Move backups to D:" \
  --files "C:/Users/me/scripts" --capture "tasks=schtasks /query /fo csv" --git C:/git/my-app
# ... your work ...
$R run <scratchpad>/review "schtasks /change /tn Backup /st 03:00"
$R note <scratchpad>/review --title "Set Status to Pågår on the task" --evidence <scratchpad>/notion-result.json
$R render --session <scratchpad>/review --description <scratchpad>/review/why.md --out <scratchpad>/review/review.html
```

- `--files` takes a file or folder (repeatable). Text files up to 1 MB are kept for the diff; moves are found by
  content. `.git`, `node_modules` and build folders are skipped.
- `--capture` commands should only read, and print the same output for the same state (sort it if needed).
- Don't put secrets in watched files or captured output: the page shows them. Leave out `.env*` files.
- `--description` is Markdown shown under the title, in three short paragraphs: why the change was made; a little
  background (`**Background:** ...`) if the reader needs it; and what was fixed or changed (`**Fixed:** ...` or
  `**Changed:** ...`), in plain words, the outcome rather than the code. A label at the start of a paragraph gets its
  own line.

**Notes per file and per change.** Before `render`, run `outline` with the same `--git`/`--session` options. It lists
every changed file and change, and writes a JSON template. So the end of a review is always:

```bash
$R outline --git . --template <scratchpad>/review/notes.json
# write why.md, and fill in "summary" per file and "text" per change in notes.json, then:
$R render --git . --description <scratchpad>/review/why.md --annotations <scratchpad>/review/notes.json   --out <scratchpad>/review/review.html --artifact
```

- One sentence each, on what and why: "Pairs removed and added lines so the inline view can show one modified
  line", not "Adds a function `hunk_rows`". Leave a value empty to skip it; skip the obvious ones.
- Each change is keyed by its first changed line (`+N` new file, `-N` old). Run `outline` again after more edits:
  filled-in notes are kept and new changes are added. A note that no longer matches a change shows as a warning on
  the page, so read the page after the last edit.
- A file's note shows as FILE at the top of the file and under its name in the file list. A change's note shows as
  CHANGE right above its first changed line, so a hunk with two separate changes gets two notes.

## Show it

1. Check the page before you link it: the files and +/− that `render` prints match
   `git diff --shortstat $(git merge-base <base> HEAD)` (the base the page names, e.g. `origin/main`; it counts
   uncommitted changes like the page does, but not untracked files) plus anything outside git; the page has no "!"
   warnings about notes; and in a browser, the notes sit above the right changes.
2. Publish it with the `Artifact` tool (private) and link it, rendered with `--artifact`, which leaves out the
   document skeleton the tool adds itself. Without that tool, show it with T3's `html_render`, or
   give the file path. A page over 16 MB won't publish; review the biggest files on GitHub instead.
3. Don't read the page into your context: it's hundreds of kB. Publish it by its path and check it in a browser.
   That keeps a review cheap: `outline` and `render` take about a second each, and the notes and description a few
   thousand tokens.
4. Put the link where the review starts, e.g. your reply or the task's notes.

## The page

The description, then boxes with the totals (files, lines, repos and folders when there are several, checked
states, commands run, actions reported by agent) and when the page was made. The contents list in the corner names
each changed file under its repo or folder.

Then one section per source: repo (branch vs base, commits, push status, GitHub link) or folder; a file list
with status, +/− and the agent's file summary; and the diffs, with line numbers. Big, generated (lock files) and
deleted files start collapsed. Then the state diffs and the recorded actions. Expand/collapse all and a "Viewed" box
per file (kept in the browser) make a long review easier to get through; a viewed file folds and fades, in the file
list too. Below each diff, a bar repeats "Viewed" with a "Collapse" button, so a long file can be marked and folded
from its end; folding from there scrolls back to the file's header.

Two diff views, switched in the toolbar and remembered in the browser: **Inline** (the default) shows a modified line
once, removed words red and struck through, added words green, with one line-number column (the old number on
removed lines); **Old + new** shows removed lines, then added lines, with the changed words highlighted and both
line numbers. Lines that differ too much to pair show as plain removed and added lines in
both. **Wrap lines**, on by default and remembered, wraps long lines under the line they belong to instead of
scrolling sideways. On a phone there's one line-number column.

## Changing review.py

1. Change this file in the same commit, so it says what the script does now: the options, the page and its parts.
   Also check the other skills that mention `explain-changes`, e.g. with `grep -rn explain-changes skills`.
2. Run `python examples/build_examples.py <scratchpad>/examples --check`. It builds three example pages (a code fix
   on a branch; an ops change with a script, its config, a scheduled task, a command and a Notion note; and a folder
   reorganisation) and checks them against the examples' own git history and snapshots: the files, their status and
   moves, every diff line, the notes, the description and its order, the boxes, and the code example's own tests. All
   three must say `ok`.
3. When you add or change something on the page, add it to `EXPECTED` and `check_page` in that script, and make
   sure the check fails without your change.
4. Open the pages in a browser, on desktop and at phone width (375 px, no sideways scrolling) and in both themes.
   The check can't see layout.
