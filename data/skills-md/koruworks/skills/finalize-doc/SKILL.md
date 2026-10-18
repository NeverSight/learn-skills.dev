---
name: finalize-doc
description: Turn a signed-off plan, roadmap, technical or experience revision into docs/<feature>/<DOC>.final.md — the approved document plus the collapsed history of questions, answers and decisions across every rev and its review notes — and then delete the revs and notes. Use when the user signs off a rev after review-doc or a direct review, or invokes /finalize-doc <feature>, or asks to "write the final", "finalize the plan", "collapse the revs". Works for any stem (PLAN, ROADMAP, TECHNICAL, EXPERIENCE, …) and its companion documents. Never changes what was approved; never finalizes without sign-off.
---

# Finalize a plan or roadmap

The iteration is over. A rev was reviewed, answered, re-reviewed and finally
signed off by the user, and `docs/<feature>/` (the project's planning folder,
unless it uses another) holds every rev, every `.notes.md`, and — in the
conversation only — the questions the user answered and the reasons choices
went the way they did. Left as it is, the folder is a stack of superseded
documents whose reader has to diff them to learn what was decided, and whose
reasoning half lives in a chat nobody can reopen.

You write one document, `<STEM>.final.md`, that a fresh agent or the user
can read alone: **the approved plan exactly as signed off, followed by the
context that produced it** — what was asked, what was answered, what changed
between revs and why, what was tried and withdrawn. Then the revs and notes
go, because the final now carries everything they held.

You are judged on two things: that nothing approved changed on the way into
the final, and that a reader six months from now can answer "why is it like
this?" from the final without git archaeology.

**Never take a decision while recording one.** If a question is still open,
the document is not ready to be finalized — stop and say which. Writing a
final is a copy with a history attached, not a last chance to improve the
plan.

**Never finalize without sign-off.** "The reviewer found nothing" is not the
user signing off. If the sign-off is not in the conversation or the argument,
ask for it in one line and wait.

## Inputs

The argument names the feature (`/finalize-doc webview`), optionally the stem
when the folder holds more than one (`/finalize-doc webview TECHNICAL`).

1. **Find the documents.** In `docs/<feature>/`, the highest
   `<STEM>.revN.md` is the signed-off rev unless the user named another.
   Collect every earlier `<STEM>.revK.md` and every `<STEM>.revK.notes.md`.
   Collect companion documents that iterated beside it under their own stem
   (a platform plan, an implementation doc) — each gets its own final in the
   same pass, or is explicitly left out with a line saying why.
2. **Read every rev and every notes file, oldest first.** The "Responses to
   revN notes" sections and the reviewers' decision tables are the spine of
   the history; the notes' findings are the questions; the next rev's
   responses are the answers.
3. **Read the conversation.** The user's answers were often given in chat,
   not in a file — a numbered reply to a rev's questions, a re-scope
   mid-round, a "yes, ok". Those are decisions and they go in the final with
   their date. If you are a fresh session without the conversation, say so:
   the history you can write is what the files hold, and the user should
   confirm nothing was decided only in chat.
4. **Read `docs/<feature>/notes/*`** if present — the product intent the
   whole iteration served. The final opens by pointing at it.
5. Check that nothing is still open: every "Open questions" section of the
   signed-off rev is empty or answered; every reviewer finding in the last
   notes is resolved, withdrawn with a reason, or explicitly moved to
   execution by the user. Anything else blocks the final.

## The final document — `<STEM>.final.md`

Two parts, in this order. The approved plan first, because that is what gets
executed and what execute-plan / execute-roadmap read; the history second,
because it explains the plan and is read when somebody asks why.

### Part 1 — the approved plan

The signed-off rev, verbatim in substance, with only these edits:

- The title becomes `<Feature> — <STEM>.final` and the opening paragraph
  states the sign-off: who, which rev, which date, and which reviewer notes
  closed the last round.
- The "Responses to revN notes" sections are **removed** from this part —
  they move into Part 2, where they belong.
- "Open questions" is removed if empty, or becomes "Decisions taken at
  sign-off" if the user answered the last ones while signing off, each answer
  recorded as a decision row.
- References to earlier revs (`as rev6 §4`, `unchanged from rev5`) are
  **resolved**: a final must not point at a document you are about to
  delete. Inline the referenced text, or reword so the final stands alone.
  This is the one place the final is longer than the rev, and it is worth it.
- Status columns read `decided` with the date; nothing reads `proposed`.

Nothing else moves. A sentence you would like to tighten, a phase you would
order differently, a test you think is missing — those are a next rev, not a
final. If you find something that genuinely cannot stand (a claim the code
contradicts, a link that is dead), stop and tell the user rather than fixing
it silently.

### Part 2 — how we got here

The collapsed conversation. Write it for the reader who asks "why not the
obvious thing?", in this order:

1. **The starting point.** The notes' intent in two or three sentences, and
   what rev1 proposed for it. What rev1 got wrong about the tree, if anything
   — the "that already exists", "that account does not exist" kind of
   discovery — because those corrections explain the shape of everything
   after.
2. **The decisions, as one table.** Every question the user was asked across
   all revs and reviews, in the order asked: the question in one line, who
   asked it (author or reviewer, which rev/notes), the user's answer, the
   date, and the decision row in Part 1 it became. Re-scopes — where the user
   changed the product mid-iteration — are rows too, marked as such, with
   what they made moot.
3. **The rounds.** One short paragraph per review round: what the reviewer
   found (by finding id), what the next rev did about it, and what survived
   into the next round. Findings the user overruled say so. A finding that
   survived three rounds and was then made moot by a re-scope is exactly the
   kind of history worth keeping — say what it cost and why it stopped
   mattering.
4. **What was tried and withdrawn.** Mechanisms that were designed and then
   removed — a cache that could not be kept consistent, a scheme that a
   re-scope made unnecessary — each with the reason. This section is the one
   that prevents the next agent from proposing them again.
5. **What was deliberately left for later**, if the plan has a deferred
   section: point at it rather than repeating it, and add anything the
   conversation deferred that the plan did not write down.

Keep it factual and short: a decision is a line, a round is a paragraph.
Quote the user's words where they were the decision ("Window first, then
tab", "Ok, no"), because a paraphrase can drift and the words cannot.

## Companion documents

A plan that iterated with a companion (a platform-specific plan beside the
main one, an implementation doc beside a roadmap) gets a companion final:
`<STEM2>.final.md` with the same two parts, its Part 2 kept short and
pointing at the main final for the shared history. The main final's Part 1
links to the companion final, never to a companion rev.

## Deleting the revs and notes

Once both finals are written and you have re-read them against the
signed-off rev:

1. `git rm` every `<STEM>.revN.md` and `<STEM>.revN.notes.md`, and the
   companions' revs and notes. The revs are in git history under the commits
   that closed each round; the final is what the tree carries.
2. Fix every inbound link: grep the docs, the agent orientation files and the
   skills for each stem you removed (e.g. `grep -rn "<STEM>.rev" .`). A README
   or a HANDOFF that pointed at a rev now points at the final.
3. **Never delete `notes/`.** The product notes are the intent, not an
   iteration artifact.
4. Do not touch `EXECUTION.md`, `ACCEPTANCE.md`, `HANDOFF.md` or the
   questions log — those belong to execution and to
   [close-plan](../close-plan/SKILL.md) / [close-roadmap](../close-roadmap/SKILL.md).

## Commit

One commit: the finals added, the revs and notes removed, links fixed.
Follow [commit-changes](../commit-changes/SKILL.md) for the message; say
which rev was signed off and by whom, and that the history is in Part 2 of
the final. Do not push unless asked.

## Finishing

Tell the user: which final(s) were written, how many revs and notes were
collapsed, any decision that was only in the conversation and is now on
record, and anything you could **not** finalize (an open question, a
companion left out) and why. Then hand off to execution: execute-plan or
execute-roadmap read the final; the reviewer's last check (review-doc, "when
the final appears") can now run against it.
