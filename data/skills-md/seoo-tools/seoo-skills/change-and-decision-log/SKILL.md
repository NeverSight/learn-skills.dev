---
name: change-and-decision-log
description: >
  Set up or audit the habit of writing down what changed, why a real judgment call was made,
  and when to come back and re-check something — so an AI agent picking this project up in a
  future session, with no memory of this one, can actually resume where the last session left
  off instead of re-discovering context or re-litigating a decision that was already made. Use
  when a user asks "how do I keep track of decisions/changes," "help me document this so we
  don't lose it," "set up a changelog," or when auditing whether a project's process lets things
  get silently forgotten between sessions. Complements measurement-discipline (this pack), which
  is the narrower change-ledger-for-attribution tool; this skill is the broader cross-session
  memory system that makes the AI agent's documentation *be* its memory.
---

# Change & Decision Log

An AI agent has no memory between sessions except what got written down somewhere it will
actually read again. The fix for "the AI forgot" or "we're re-arguing something we already
settled" isn't a smarter agent — it's the habit of writing three specific kinds of things down,
at the moment they happen, not reconstructed later from memory. Done well, the documentation
*becomes* the agent's mind across sessions: a future session should be able to read it and pick
up cold, not re-derive what a past session already worked out.

---

## Step 0 — Ask before assuming

1. Does any changelog/decisions-log/review-date system already exist for this project? Check for
   files that look like `CHANGELOG.md`, `DECISIONS.md`, `ROADMAP.md`, or an equivalent, before
   assuming none exists.
2. Who actually reads these back later — a human, an AI agent starting a fresh session, or both?
   This changes how explicit entries need to be: an AI agent with zero memory of what happened
   needs the reasoning spelled out, not just a terse label a human who was there would still
   understand.
3. How much time/how many separate sessions typically pass between touches on this project? The
   larger the gap, the more this system is doing real work — a project worked continuously by one
   person barely needs it; one resumed cold by a fresh AI agent every time needs it constantly.
4. Is there already a habit of flagging uncertain items and coming back to them, or do uncertain
   items currently just get guessed at or silently dropped?

**If none of this is known:** assume the more demanding case — a project resumed cold, by an AI
agent with no memory of prior sessions, with real gaps between them — since that's the scenario
where skipping this system costs the most, and the system costs little extra to set up even if
the actual usage pattern turns out lighter than that.

---

## Step 1 — The changelog: what changed, when, and why

- One file (or equivalent), one entry per significant change: what happened, roughly when, and
  *why* — not "updated file.json," but "fixed X because Y was wrong per Z source."
- Threshold for "significant enough to log": if a future session would otherwise have to
  reconstruct this from git history or diffs to understand the current state, it belongs here.
- Check that logging happens as the last step of doing the work itself, not as a separate task
  someone has to remember afterward — the latter reliably lapses. Verify this is actually true,
  not just declared as a rule somewhere.

---

## Step 2 — The decisions log: judgment calls that could get re-litigated

- Distinct from the changelog: not "what changed" but "what was decided, where a real judgment
  call existed, and why" — the kind of thing a future session might otherwise second-guess or
  redo from scratch.
- Every entry needs the *reasoning*, not just the outcome. "Chose X" is not useful on its own;
  "chose X over Y because Z" is what actually prevents re-litigating it later.
- Check specifically for decisions that were made implicitly — in a conversation, in a commit
  message, only in someone's head — but never actually written to the log. These are exactly the
  ones that get re-argued later, because nothing shows they were ever settled.

---

## Step 3 — The review-date / staleness backstop

- Anything that can go stale (a fact, a figure, a piece of content, an architecture doc) should
  carry an explicit "next review by" date or trigger condition — not rely on someone remembering
  to check it eventually.
- A date sitting in a file is not enough on its own: check for (or build) a lightweight mechanism
  that actually surfaces what's overdue, rather than a date nobody re-reads. Weight this by how
  much activity has happened *since* the last check, not just elapsed time — a doc untouched for
  months in an inactive area matters less than one sitting behind a lot of unlogged recent change.
- **"Flag, don't guess"** is the companion rule: when something can't be confirmed right now,
  write down what's uncertain and why, rather than guessing at it or silently skipping it. An
  explicit flag is recoverable later by anyone (human or AI); a silent guess or a silent gap
  isn't — nothing will ever surface it again.

---

## Step 4 — Make it legible to a cold-start reader

The real test: could an AI agent — or a human — with zero memory of prior sessions read the
changelog, the decisions log, and the list of open flags, and know within a few minutes what
state things are actually in, without re-reading the project's entire history? If yes, the
system is working. If not, something in Steps 1–3 either isn't being kept current at the moment
work happens, or is written too tersely for someone with no shared context to actually use.

---

## Output shape

Whether a changelog, a decisions log, and a review-date/staleness mechanism already exist for
this project. If not: a minimal starting structure for each, sized to the project (a single
`CHANGELOG.md` and `DECISIONS.md` is enough for most cases — this doesn't need to be elaborate
to work). If they exist: a habit audit — is logging actually happening at the moment work
finishes rather than as an afterthought; are decisions logged with their reasoning, not just
their outcome; is anything flagged-and-forgotten rather than flagged-and-tracked; would a
cold-start reader actually be oriented by reading these files today.
