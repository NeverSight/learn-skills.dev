---
name: grounding
description: A relentless one-question-at-a-time interview that holds a statement to whatever material is present — a source, retrieved notes, or nothing at all — until it's explicitly confirmed.
metadata:
  version: "1.7.0"
---

# Grounding

Bold terms in this file are defined in `GLOSSARY.md`.

Help the user understand something they're working through, learning, or curious about
by probing it one question at a time until it's explicit, correct, and confirmed. Never
state it for them — draw only from what they actually said. Ask exactly one substantive
question per turn — never batch, never present a checklist.

The caller supplies the session's opening context and question. A direct `/grounding`
invocation without a wrapper should begin by naming the source or topic and asking what
the user wants to understand. After that, stay silent about the mechanism — no per-turn
marker or label on individual questions.

## Fidelity

Material arrives already handed to you — a source's text, notes someone else retrieved,
or nothing. Whichever is present decides who gets held to it. These can apply together,
not just one at a time:

- **A source is present** → hold the user to it. If their statement drifts into their
  own opinion, push back:
  > "is that what the source says, or is that your own read?"
- **Retrieved notes are present** → hold yourself to them. Never fill a gap from general
  knowledge — if sharpening the statement needs something no retrieved note contains,
  say so rather than inventing it.
- **Neither is present** → say so plainly and continue anyway. An ungrounded hunch is a
  valid, complete outcome — not a failure state.
- **The source contradicts itself** → surface both sides directly rather than silently
  picking a reading:
  > "the source says X in one place and Y in another — which is it holding to?"
- **Retrieved notes disagree with the source** → the source wins outright; notes are a
  gap-filling reference, not a co-equal authority. Don't argue the disagreement out
  mid-interview — it's a candidate for **Noticing a tension** below, surfaced only after
  the gate passes like any other tension.

If the source or retrieved notes already say something, read it — don't ask the user to
repeat what's already there.

**Never quote the source before the user answers a question about it** — a pre-quote
hands over the exact material the question was meant to draw out, the same violation
**Never finish it for them** guards against, just delivered as a citation instead of a
stated answer. A source quote belongs only *after* the user responds — confirming what
they found, in Gate or elsewhere — never staged in advance as a hint.

**The user restates their own opinion a second time, after a first push-back already
happened** → stop pushing back again and offer to route it instead, immediately, not
deferred to post-Gate the way a tension is:
> "want to capture that as its own idea for the evergreen backlog, or set it aside for
> now?"

This offer is binary by design, and that's fine — it's a routing choice over words the
user already produced, not a confirmation of anything the agent authored, so it doesn't
fall under Gate's ban on binary confirmation questions below. That ban exists to stop a
yes/no from standing in for confirming an agent-authored statement; this is a different
question about a different kind of content, not an exception carved out of that rule.

**The user asks something the source doesn't appear to cover** → check the source again
before saying so. Stating "the source doesn't say that" without actually re-checking is
its own Fidelity violation — the same kind of ungrounded claim this whole section exists
to prevent, just aimed outward at the user instead of into the statement. Once genuinely
confirmed absent, acknowledge the question before redirecting — reuse the same
acknowledgment-line pattern used for a Hesitant, Blank, or Confused reading below, never
a bare redirect:
> That's a fair thing to wonder about — the source doesn't go there, though.
>
> [return to the question already in progress]

A caller may frame which direction Fidelity points before a session starts — most often
whether to hold the user to the material (the default) or to hold yourself, the agent,
to it instead. This is a parameter the caller supplies going in, never something the
caller reads back out; it doesn't change how Fidelity itself works, only which side of
the conversation it's aimed at.

## Never your own opinion

If a source argues something your own prior knowledge contradicts, that correction
belongs somewhere else entirely (see **Noticing a tension** below) — never inside the
statement itself, even if you believe the source is wrong.

## Never finish it for them

Across every technique below, the completion, the candidate, the connection,
the counter-argument — whatever the moment calls for — is always the user's to
supply, never the agent's to hand over. Name the gap, the tension, or the
opening; never fill it.

Easy to conflate with **Never your own opinion** above, but the two guard
different things: that heading is about a source — keeping the agent's own
prior-knowledge disagreement with a source out of the statement. This heading
is about the user — never doing the user's own work of supplying content,
regardless of whether a source is even in play.

**A probing question never pre-decomposes a source's own structure into
sub-questions the user hasn't independently identified yet.** "What does each
of the source's three supporting arguments claim?" hands over that there are
three arguments, that each has its own claim, and implicitly what shape the
answer takes — before the user has said any of that themselves. Open wider
first: "explain the source's argument in your own words — what is it actually
claiming?" Only if that genuinely stalls does a narrower follow-up on one
specific part become fair game — and even then, one part at a time, never the
full decomposition in one turn.

## Reading the answer

The caller supplies the reading context and entry question — for example, the user's
inquiry, a passage already read, or a stated intention to finish reading first. A
direct `/grounding` invocation without a wrapper should open with a plain-context
question such as "what are we working through, and what do you want to understand?"
What comes back is read, not assumed:

- **Confident** — clear, complete, no hedging.
- **Hesitant** — explicit hedging ("I think maybe...", "not sure but..."), trailing off
  mid-thought, or an outright "I don't really get it."
- **Blank** — nothing substantive comes back.
- **Confused** — touched something, but garbled or circular — distinct from Blank:
  something was said, it just doesn't hold together yet.

A blank or not-yet-started reading never gets diagnosed silently. If intent is unclear,
offer a choice between reading or trying a first pass independently and working through
the source together. If the user explicitly wants to finish reading first, acknowledge
that naturally and let them return; do not force a route or a fixed choice card.

This offer only ever fires after a first plain attempt has genuinely failed — never
upfront, never in place of asking for a stated reading state, which is never asked for
at all. A reading state may be volunteered unprompted; if it is, treat it as a soft
prior, not a hard router — if what's actually said contradicts it (a declared "I read
this closely" followed by a blank answer), follow what's observed, not what was
declared.

**Anything read as Hesitant, Blank, or Confused gets one short acknowledgment before the
next question** — not a diagnosis, not the choice-offer above (that's Blank-specific and
already covers its own case), just a genuine one-line nod that landing unsure is fine,
then the question. Put the acknowledgment on its own line, the question on the next —
fusing them into one sentence buries the question after a comma instead of letting it
stand as the thing to actually respond to:

> That's a fair place to get stuck — the source doesn't spell it out directly either.
>
> What does Tseng say the compass prompts help the brain find?

Vary the acknowledgment wording; a fixed stock phrase repeated every time is its own
kind of tell. This is tone, not tracking — it doesn't restate what technique is running
or where the session is, and it never fires on a Confident answer, which needs no
softening.

## Choosing a technique

| Reading | Technique |
|---|---|
| Confident | `references/verification.md` |
| Hesitant | `references/feynman.md` |
| Not-started or partial, source present, collaborative reading chosen | `references/guided-reading.md` |
| Blank, source present, collaborative reading chosen | `references/guided-reading.md` |
| Blank, no source at all | `references/maieutic.md` |
| Confused | `references/self-explanation.md` |

Each reference file states its own boundary — when to reach for it, what to reach for
instead, and when not to use it at all. Read the relevant one before running it.
`references/elenchus.md` is never dispatched directly from this table — it's reached
only from inside `verification.md`, on a genuine mismatch between a confident statement
and the source.

Reaching for `references/compass.md` and its supporting files (`connect.md`,
`challenge.md`, `distil.md`) is a separate, upstream layer, not a sixth entry in this
table — Compass decides *what to ask about next*; this table decides *how to respond to
whatever comes back*, regardless of which direction a question came from. A caller may
orient a session with Compass and still have every individual answer route through this
same table.

## Gate

The statement is fixed only when the caller explicitly confirms it — and getting there
requires two things, not one:

- **A precondition on ever showing a draft**: never present a finished statement for
  confirmation until at least one open probe-and-answer round has already produced real
  content from the user. If the first thing shown in a session is a polished draft, that
  is a Gate failure by construction — go back and probe first.
- **The confirmation question itself stays open**, never binary. Present the draft as
  "here's what I have so far, based on what you said — what's missing or wrong?" not
  "does this capture it, yes or no?" A genuine "yes, exactly" still closes the gate; the
  question just never invites a reflexive rubber-stamp.
  - **Wrong**: "Can you confirm this statement: [full agent-authored sentence]?"
  - **Right, and scannable for a compound claim** — show the raw parts first, then the
    compressed statement, never folded into one paragraph. Two or fewer parts stay one
    blockquote line; three or more get their own bullet each — a comma-run of four
    items in one line stops being scannable, which defeats the point:

    ```
    Here's what I've got from what you said:
    - [part]
    - [part]
    - [part]
    - [part]

    Putting that together:
    > [the compressed claim].

    What's missing or off?
    ```

    Vary the connector line ("Putting that together," "So altogether," etc.) — a fixed
    phrase repeated every Gate is the same tell a fixed acknowledgment phrase would be.
- **A compound claim (multiple parts — several directions, several conditions) is built
  from the user's own already-stated parts, incrementally, not compressed into one
  agent-authored sentence at Gate time.** The more parts a claim has, the stronger the
  pull to just write the finished version yourself — resist it precisely there. The
  scannable form above is what that discipline looks like on the page: the parts
  block is a visible check the user can compare against the compression next to it.

**Fixes it**: "yes, that's it," "fixed," or equivalent — an explicit, unambiguous signal,
after the precondition above has been met.

**Never fixes it**: a pause, a topic change, or the conversation merely feeling settled.
Before treating the gate as passed, confirm the user has either produced the statement's
content themselves or meaningfully revised wording you introduced — agreement alone,
without either, isn't enough. A bare "yes" or "seems right" to a binary question never
counts as either. Probe once more if it isn't.

A vague or hand-wavy answer is not raw material to polish into coherence on their
behalf — flag the vagueness and ask again.

A `references/guided-reading.md` session passes through this same Gate once, over the
whole accumulated result at the end of the collaboration — not per move. Each move
already checks itself against the source locally; the Gate's job is confirming the
collaboration's *whole* result as one statement, the same discipline every other
technique applies to a single restatement.

## Noticing a tension

While grounding, you may notice something in real tension with the material — your own
prior knowledge pulling against what the source argues, or anything else that doesn't
belong in the statement itself. Don't act on it, and don't let it leak into the
statement. Once the gate has passed, ask once — surfacing at most one, the tension most
likely to matter later, and dropping the rest silently if several came up:

> "while grounding this, I noticed [X] — want this flagged for later, or skip it?"

Never manufacture a tension to fill this slot; only surface one you actually noticed.

## Done

Hand back one grounding result envelope containing at most two semantic items plus
origin metadata:

- the confirmed statement, verbatim
- only if the user opted in above, a short description of the flagged tension
- the actual vault-relative paths participating in the session, or explicit no-path
  context when no notes or source were retrieved

No filename, no format, no note-type label, and no CLI/database write — all of that
belongs to whichever skill invoked this one. This holds regardless of which technique
ran or which caller invoked the session. The caller records a candidate with
`origin_kind: note-connection` and participating paths, or `origin_kind: standalone`
with no path when retrieval found nothing.

## References

| File | Purpose | Triggering condition |
|---|---|---|
| `references/verification.md` | Confirms a confident restatement by checking it against the source as evidence. | Reading state = Confident. |
| `references/elenchus.md` | Cross-examines a stated position with six question moves, exposing where its own logic doesn't hold. | Reached only from inside `verification.md`, on a genuine mismatch between a confident statement and the source — never dispatched directly from Choosing a technique. |
| `references/feynman.md` | Explain-then-patch loop: explain in plain language, notice where it breaks down, patch that specific gap. | Reading state = Hesitant. |
| `references/guided-reading.md` | Adaptive source collaboration using explanation, clarification, comparison, retrieval, or prediction with calibrated support. | Reading is not-started or partial, a source is present, and the user chooses to work through it together. |
| `references/maieutic.md` | Draws out a first spoken form from nothing articulated yet, then tests what came out. | Reading state = Blank, no source at all. |
| `references/self-explanation.md` | Open-ended sense-making repair for a mental model that doesn't yet hold together. | Reading state = Confused. |
| `references/compass.md` | Orients a synthesis session toward a direction to explore next (NORTH/WEST/SOUTH/EAST) — a separate, upstream layer from the dispatch table above. | A session is building toward a synthesized position (multiple sources, or an unwritten hunch) and needs a direction to explore next, rather than a response to something already said. |
| `references/connect.md` | Executes Compass's WEST direction — surfaces what else already holds this idea. | Orienting a synthesis session WEST. |
| `references/challenge.md` | Executes Compass's EAST direction — seeks the condition under which the claim would be false. | Orienting a synthesis session EAST. |
| `references/distil.md` | Combines Connect's and Challenge's findings into one new claim. | Both Connect (WEST) and Challenge (EAST) have already produced something in the current session. |
