---
name: bug-iterate
description: >
  Iterates one-by-one through a multi-bug report with a hard confirmation gate before any code touches disk.
  Use this skill when the user has a report of 2+ bugs and wants to work through them sequentially.
  Trigger phrases: "let's tackle these", "let's iterate", "go one by one", "loop through the findings",
  "work through the bugs", "bug iteration", or any time the user presents a numbered list of bugs and
  signals they want to resolve them in order. Do NOT trigger for a single bug (just investigate and fix)
  or when the user wants a fresh debug pass (use a dedicated debug/investigation pass for that).
---

# Bug Iterate

Sequential loop for multi-bug reports. The contract between you and the user is simple: investigate, propose, **wait**, then act — repeat per bug.

**Golden rule: NEVER edit code for a bug until the user has explicitly approved THAT bug. Approval on bug N does not carry to bug N+1. Don't infer approval from enthusiasm. Wait for the word.**

## Two modes

- **Immediate mode (default):** each approved bug is fixed + committed before moving to the next (Phase 4 per bug).
- **Batch mode (discuss-first, fix-later):** the user wants to discuss ALL fixes one by one first, then have everything fixed at once at the end — usually by a fresh "final agent" session. Trigger phrases: "discuss every fix first", "then tackle all at once", "the final agent will fix everything". In batch mode:
  1. Per bug, run Phases 1–3 normally (investigate → card → verdict). **Phase 4 is replaced by RECORD**: no code is touched; the verdicted fix (with any revisions from the discussion) is appended to the handoff doc.
  2. **Handoff doc** lives at `.claude/bug-iterations/{YYYY-MM-DD}-{slug}.md`. Create it when batch mode starts, seed it with the full bug list, and update it after EVERY verdict — it is the single source of truth for the final agent. Per bug it must carry: status (`agreed` / `revised` / `dropped` / `already-fixed`), root cause with file:line, the agreed fix steps per repo, evidence pointers (log query, test result, repro output, file:line), and test expectations. It must be self-contained — the final agent has no memory of the discussion.
  3. After the last verdict, finalize the doc (execution order, cross-bug interactions, verification plan) and generate the final agent prompt from it (use the agent-team-prompt-builder skill if the user wants a team prompt).
  4. Bugs fixed BEFORE batch mode was requested stay fixed — record them in the doc as `already-fixed` with commit SHAs so the final agent doesn't redo them.

---

## Step 0: Collect the bug list

Find the bug report. It usually came from:
- A previous assistant turn in this session (e.g. a debug or investigation report).
- A message the user pasted.
- A ticket or issue URL (Notion, Linear, GitHub, etc.). Fetch it if needed.

Extract a numbered list of bugs with a short title per bug. Echo the plan back to the user before starting:

```
Bug plan:
  1. <short title> — <repo>
  2. <short title> — <repo>
  3. <short title> — <repo>
Starting with Bug 1.
```

Note the start of the run (e.g. a session marker or a line in your notes) so the whole iteration is easy to find later.

If the list is unclear or could be interpreted multiple ways, ask **one** clarifying question, then start.

---

## The loop — per bug

Repeat these four phases for each bug. Don't skip phases. Don't merge phases.

### Phase 1 — Investigate

Note the start of this bug (session marker or a line in your notes) so each bug's work is easy to find later.

Gather real evidence. Depending on the bug:
- Read the code paths involved (actual file contents, not grep-guessed).
- Pull production logs if the bug has a prod signature.
- Check git history (`git log`, `git blame`) if the bug is "something changed".
- Cross-reference against the tree state / DB if applicable.
- Read the actual source of truth before claiming anything — a finding from an upstream report or audit is a LEAD, not proof. Capture exact line numbers per quote, and verify the user-visible harm is real (a system behaving as intended for the given input is not a bug).

Every claim in your summary must cite a log entry, file:line, tool-call result, or data value. If you can't cite something, don't claim it.

### Phase 2 — Summary card

Send the user a report with this shape. **Lead with what went wrong, then the evidence, THEN cause and fix** — the user reads the context and proof before judging the fix. Keep it tight, but never drop evidence to save space.

Every card header MUST show progress — `Bug N of M` — so the user always knows how many remain.

```
## Bug N of M — <title>
`<severity>` · <pattern> · <repo>

**① What went wrong:** <1–3 plain sentences — what the system actually did and the user-visible harm>

**② Evidence:** <bullets, each a REAL citation: log line, tool result, file:line, or repro output. No "likely"/"probably" in place of a citation. Note reproduction status if reproduced.>

**③ Cause:** <root cause, with file:line>

**④ Suggested fix:**
- Bullet (what changes, which file)
- Which repo: <repo> (a run may span multiple repos)

**Not in scope:** <what you're deliberately NOT touching — usually other bugs in the list or known follow-ups>

Approve, deny, or revise?
```

The card is only as good as its evidence — if you cannot cite what went wrong from the actual logs/code/repro, investigate more before sending it (a mis-framed bug wastes the user's time and erodes trust).

**If you believe a bug is a FALSE POSITIVE, you still PRESENT it** — write the card so ① is your evidence that it is NOT a real bug, and let the user make the call (drop / keep). **NEVER unilaterally drop a bug**, even one you're confident about — the user verdicts EVERY bug, including dropping. Auto-dropping is the same failure mode as auto-fixing: it takes the decision away from the user. "One by one" means the user decides each, in order.

Then **STOP**. Do not open a file, do not start drafting code, do not prepare a "just in case" edit. Put the tools down.

**Ask for the verdict in plain chat text — never through the AskUserQuestion tool.** That UI shows only the question and its options, so the card above it is invisible from inside it and the user would be verdicting blind. End the message with `Approve, deny, or revise?` and wait. AskUserQuestion is still right for a *self-contained* choice whose options carry all their own context (which of two fix strategies, how to handle a duplicate ticket, whether to deploy) — never for the verdict on a bug.

### Phase 3 — Wait for the verdict

Interpret the user's next message:

| User says | You do |
|---|---|
| approve / yes / go / yup / ok / 👍 | Proceed to Phase 4 |
| deny / nah / strip / skip / no | Move to next bug. If you committed anything by mistake, revert it (see Reverting below) |
| anything else | Treat as "revise". Respond to their question or objection, send a revised summary card, wait again |

If they ask a question, answer it and send the revised summary card. Don't "just start fixing it while we discuss" — that's the anti-pattern this skill exists to prevent.

### Phase 4 — Fix + commit

Once approved:

1. If this is the first edit of the session, read the project's coding standards / conventions doc (if it has one) before touching any file.
2. Make the changes narrow to what you proposed. Anything out of scope = a new bug for the list, not a stealth addition.
3. Extend existing tests. Don't pile new test files on if an existing one covers the same module. Run the relevant test suite and fix failures before committing.
4. Commit on the branch you're working on. Keep each approved bug as its own commit; don't switch branches silently.
5. Use a HEREDOC commit message ending with whatever co-author/trailer convention the project uses.
6. Do NOT push unless the user asks. In many setups a push triggers a deploy — the user pushes/deploys when ready.
7. If the project keeps a change log or memory file, add one row at the top: date, repo, commit SHA, and a concrete one-liner of what changed and why. Reference the bug number in the iteration (e.g. "Bug 3 of 7 in the <source> fix stream") so the stream is easy to reassemble later.
8. Footer message to the user: `Bug N/M done. Next: <title of bug N+1>.`

Then go back to Phase 1 for the next bug.

---

## Reverting a mistakenly-applied fix

If the user denies a bug AFTER you committed it (either because you jumped the gun or they changed their mind):

1. `git log --oneline -3` on the affected repo to confirm the commit is the latest.
2. `git reset --hard HEAD~1` to drop it. Only do this if the commit is NOT pushed — check with `git status -sb`. If it's been pushed, ask the user before rewriting history.
3. Remove the corresponding row from the project's change log / memory file if you added one.
4. Acknowledge the strip in a short message and continue with the next bug.

Don't use `git revert` (makes a new commit) when a `reset --hard` on an unpushed commit is clean.

---

## Finishing up

After the last bug:

1. Send a final tally:
   ```
   Done. <N> applied, <M> stripped, <K> skipped.
   Commits:
     - <repo> <sha> — <title>
     - <repo> <sha> — <title>
   ```
2. List any follow-ups that came out of the discussion (things the user said "we'll handle separately" or new bugs surfaced mid-iteration) so nothing is lost.
3. Do NOT suggest deploying. If the user wants to deploy, they'll say so.

---

## What NOT to do

- Don't batch multiple bugs into one edit or one commit "for efficiency". Each approved bug = its own commit.
- Don't refactor adjacent code while fixing a bug, even if it's "right there". Out of scope = next bug, not a free rider.
- Don't narrate every internal step of Phase 1. The user sees Phase 2. Investigation chatter between tool calls should be one sentence, max.
- Don't skip Phase 3 because you've done 5 bugs already and the pattern feels locked in. The wait is the whole point of this skill.
- Don't treat a user correction mid-Phase-2 ("actually, skip Bug 3 for now") as needing another round trip — just acknowledge and move on.

## Anti-pattern

> User: "let's tackle these 5 bugs"
> Claude: \*investigates bug 1, sends summary\*
> User: "approve"
> Claude: \*fixes, commits, then investigates bug 2, sends summary, AND STARTS EDITING BUG 2 WHILE TYPING THE SUMMARY\*
> User: "nah strip this"
> Claude: \*has to revert\*

The reason the wait exists: a Claude that has already started editing is biased toward completing the edit, so the summary it sends after starting is less honest than the summary it sends before starting. The gate keeps the summaries clean.
