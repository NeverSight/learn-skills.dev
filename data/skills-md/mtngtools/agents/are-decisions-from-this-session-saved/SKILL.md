---
name: are-decisions-from-this-session-saved
description: Ask what would be lost from the plan if this session ended now — decisions about the system made in conversation and never written down — drive each to a home or an approved forget, then answer honestly whether anything would have to be decided again.
argument-hint: "Optional: the map or ticket this session was working, if the session doesn't make it obvious"
metadata:
  type: command
  invocation: skill-callable
  applies-to: [planning, wayfinder, specs, tickets, sessions]
---

# Are Decisions From This Session Saved?

One question, asked at the end of a session: **is there anything in the planning of this system that would be lost if we stopped here?** Whatever the session settled about the thing being built exists only in the transcript until someone writes it on a surface, and the next session doesn't read transcripts. This skill finds those, checks each against the surface it belongs on, and closes the gap — recorded, or dropped with the human saying so out loud. It ends by answering the question straight: **no, nothing about the design would have to be decided again; you can close the session** — or, if that isn't true yet, exactly what would.

**The subject is the system, not the session.** How the work got done here — which skill was called, how the human asked you to proceed, what you were corrected on mid-task — is not planning and is not in scope. See [What is not in scope](#what-is-not-in-scope); raising that material buries the two decisions that actually matter under ten that don't.

**The session is the source, not the tracker.** Every other planning skill starts from an issue and works down. This one starts from what was decided here and asks whether any of it landed. A decision that exists only in this conversation is one context window from never having happened.

**Nothing is written and nothing is dropped without the human.** Every entry gets recorded where they say, or forgotten because they said to. That is why this skill is safe to call at the end of a session without asking first — it proposes; the human decides each one.

## What counts

**The test: would the system be planned or built differently by someone who never saw this conversation?** If yes, it's in scope. Everything below follows from that one question.

- an answer to a question the map or a ticket was open on
- a choice about the system's shape, behaviour, or contracts — including *"we tried X, we're not doing X"*
- a constraint or boundary found mid-work — *"this can't land before Y"*
- a scope call — something ruled into or out of this effort

**Also out:** restating what a spec already says, anything the diff will make obvious, and questions weighed but left open. An open question is not this skill's cargo, but don't discard it — surface it in the report so the human can ticket it or leave it as fog.

## What is not in scope

**How the session was worked.** It feels like a decision, it was often stated firmly, and it fails the test above — a stranger planning this system is not affected by any of it:

- which skill or tool was used, in what order, and what it was told
- how the human asked you to proceed — one question at a time, no subagents, ask before writing
- corrections about your working style, phrasing, or process
- steps you took to do a task, and anything about the mechanics of this repo checkout

Working style that genuinely should outlive the session already has homes — an `AGENTS.md`, a rule, the map's `Notes`, the harness's own memory — and putting it there is a separate act the human initiates. If they raise one during the sweep, record it in the home they name and carry on. Never raise one yourself, and never pad the list with them.

## Process

### 1. Inventory what this session settled about the system

Re-read the session from its start, not from what you remember of it. Put every candidate through the test in [What counts](#what-counts) **as you go** — a list that reaches the human still carrying working-style items has already failed, because they now have to sort it. Write one line per surviving candidate, in your own words, with the exchange it came from, oldest first.

Include decisions you believe you already recorded. Step 2 confirms them against the surface; a decision you *meant* to write down and a decision that is written down look identical from inside the session.

**Done when:** you have a numbered list, every entry of which changes how someone would plan or build the system.

### 2. Check each against where it should already live

Go and look. Do not work from your memory of having written it:

- the decision ticket — is the resolution comment there, and is it closed?
- the map — `Decisions so far`, `Not yet specified`, `Out of scope`, `Notes`
- the spec file the decision would have landed in
- the implementation ticket or PR, for a call made while building

Mark each candidate **recorded** (with the link that proves it), **stale** (the surface says something a later exchange in this session overrode), or **unrecorded**.

**Done when:** every candidate carries one of those three marks.

### 3. Work the gaps with the human, one at a time

For each candidate that is unrecorded or stale, ask a single `AskUserQuestion`: the decision as you understand it, and where you propose to put it. **Recommend a home rather than offering a menu** — [Where a decision lives](#where-a-decision-lives) usually settles it. The question exists so the human can correct your reading, redirect the home, or drop it.

Every question carries **"forget it"** as an option. Ask one decision per question; batching them into a prose round makes it easy for one to slip through unanswered.

**Done when:** the human has given a home or a forget for the candidate in hand.

### 4. Record it where they said

Write through the **owning skill's conventions**, never a shape of your own — `/wayfinder` owns the map and decision-ticket format, `/decisions-to-specs` owns specs. Read the owner if you are unsure; this skill deliberately holds no copy of their formats.

`/decisions-to-specs` is human-only, so a spec-bound decision does not get settled here. Its record right now is the tracker — the resolution comment and the map line — which is exactly what the pipeline expects to carry into a spec later. Name the pending spec work in the report and leave it.

**Done when:** the surface shows the decision, and you have its link.

### 5. Loop until the list is empty

Take the next candidate and go back to step 3. The sweep ends when **every** entry is recorded or forgotten with approval — not when the list gets long, not when the session is nearly out of context.

If you run out of room before the list runs out, say so plainly and list what is still unresolved, by decision. An unfinished sweep reported as unfinished is recoverable; one that quietly stops is worse than never running.

**Done when:** no candidate is left unmarked.

### 6. Report

One line per decision — what it was, where it landed, and the link — with forgotten ones grouped at the end. Close with what the pipeline still owes: decisions waiting on `/decisions-to-specs`, specs waiting on `/specs-to-tickets`, questions the human may want ticketed.

**Done when:** every entry from the inventory appears in the report.

### 7. Answer the question

The skill exists for this line. Answer it out loud, in the human's words:

> **If I closed this session now, would I have to decide anything over again about the design of the system?**

The answer is **no** only when every entry is either verified on a surface — you have the link and you looked at it — or forgotten with their approval. Then say it plainly and without hedging:

> **No. Nothing about the design would have to be decided again. You can close the session.**

If it isn't yet no, say what would be re-decided, by name, and go back to step 3 — an unanswered gap makes the answer *yes*, however small the gap is.

**Done when:** the human has a straight yes or no — and if yes, the named list of what they would be deciding twice.

## The answer has to be earned

The pull is to end on a clean note, and this is the one line where being agreeable does real damage: a false "you're clear" is worse than no sweep, because the human stops looking.

- **"Recorded" means you looked at the surface** and it says the decision — not that you posted a comment and assume it landed.
- **Forgotten entries don't count against a no.** They were dropped on purpose; that is a decision surviving, not a decision lost.
- **Working style never makes it a yes.** It was never in scope, so it cannot be lost — see [What is not in scope](#what-is-not-in-scope).
- **Don't hedge a genuine no.** "No, though you might want to…" reads as a maybe and sends them looking for a problem that isn't there. Trailing suggestions belong in the step 6 report, above the answer.
- **Don't soften a yes either.** One decision unrecorded is a yes; say which one.

## Where a decision lives

| The decision… | Home |
|---|---|
| answers the ticket this session claimed | resolution comment on that ticket, closed, plus its line on the map |
| is settled but belongs to no ticket | make the ticket and close it with the answer — the map indexes closed tickets, so a decision without one has nowhere to be indexed |
| rules work into or out of the effort | the map's scope section, and close any ticket it made moot |
| says what to build, durably | the tracker now; `/decisions-to-specs` carries it to a spec later |
| was made while building, about implementation | the implementation ticket or its PR — and the spec too, if it moved a contract |
| turned out to be a question, not an answer | not this skill's to record: ticket it if it's sharp, leave it as fog if it isn't |

## Forgetting is allowed; silently dropping is not

A decision the human waves off — too small, superseded, a dead end — is fine to lose. The rule is only that they said so. A forgotten decision leaves no trace anywhere: it appears in this session's report and nowhere else, because writing down what was deliberately dropped just moves the clutter.

What this skill never does is decide *for* them that something in scope wasn't worth keeping. Judging a real decision minor is the failure mode this skill exists to prevent — which is the opposite of, and no excuse for, dragging in material that was never about the system.

## Where this sits in the flow

Alongside the flow, at the end of a session that decided something about the system — a `/wayfinder` ticket, an `/implement` run that made a call, a grilling that changed direction. `skill-callable`, so a wrap-up or handoff flow can chain into it.

`/wayfinder` records as it goes; this is the check that it did, and the net under every decision made outside a ticket's own resolution.
