---
name: roast-room
description: Use when a founder wants a hard business decision debated by a council of world-class operators, says "roast room", "put this in the Roast Room", "founder council", "convene the council", "take this to the board", "what would Hormozi, Bezos, or Buffett say", "should I do X", or can't make up their mind on pricing, hiring, raising money, a new product, a partnership, a pivot, an event, or spending. Seven sub-agents, each built from one expert's public work (Bezos, Paul Graham, Hormozi, Gary Vaynerchuk, Dan Martell, Gino Wickman, Buffett), argue it over three rounds, then a Chair returns a scored verdict, the reasoning, the dissent, and next steps. Also does a one-seat consult ("ask the Hormozi seat"). Not /roast (generic personas, idea validation).
argument-hint: "[the decision] [--quick] [--seats hormozi,buffett,...] | ask <seat> [question]"
---

## What this does

The Roast Room: runs a board meeting on one decision. Seven seats, one per business pillar, each a sub-agent that reasons and talks the way its expert does, grounded in a brain compiled from that person's videos, essays, letters, talks, and books as they teach them in public. The seats argue across three rounds: open, debate, vote. You act as the **Chair**: you never argue a side, you run the room, keep the score, and write the verdict.

Read once before the first run: `references/seats.md` (roster, weights, tensions), `references/round-prompts.md` (what each seat gets), `references/scoring.md` (math and overrides), `references/report-template.md` (output), `references/live-room.md` (the small JSON files the visual room plays). A finished example council lives in `sessions/2026-10-09-example-take-the-seed/`.

## Modes

- **Full council** (default): all seven seats, three rounds. For decisions that are expensive or hard to undo.
- **Quick** (`--quick`): four seats chosen per `seats.md`, Rounds 1 and 2, Round 3 only if the scores did not converge. For reversible calls.
- **Named seats** (`--seats a,b,c`): only those seats, three rounds.
- **Consult** (`ask <seat> ...`): one seat, one answer, using the single-seat prompt. No scoring, no session folder needed.

## Step 1: The brief

The council is only as good as the brief. Build it from what the user gave you. If any of the first four items is missing, ask for them in one batch (AskUserQuestion, at most four questions), then proceed. If the user says "just run it", fill gaps with stated assumptions.

1. **The decision** in one line, and the options on the table as A, B, C. Always include "don't do it" (or "keep doing what you do now") and any alternative the founder mentioned. If the founder brought one idea, add the obvious smaller version as an option.
2. **The business**: what it sells, to whom, stage, monthly revenue, margin if known, team size.
3. **The resources**: cash or runway, founder hours, deadline.
4. **What success looks like** and the time horizon.
5. **Which way the founder is leaning, and why** (the council tests the lean, it does not echo it).

Context lookup: if this project holds notes about the founder's business (a `CLAUDE.md`, a `business.md`, or similar), read them for real numbers before asking.

Keep the brief under 300 words. Mark every assumption as `(assumed)`.

## Step 2: Set up the room

- Set a relevance weight per seat (1 to 3) with a one-line reason, per `seats.md`.
- Create the session folder: `sessions/YYYY-MM-DD-<decision-slug>/` at the project root. Save `brief.md` (the brief, the options, and the weights table) and `council.json` (`live-room.md`).
- Tell the user once: "Watch it live at http://localhost:4730" (the Roast Room plays the council as these files land; it is optional and the council runs the same without it).

## Step 3: Round 1, opening positions

Spawn every seat in **one message**, in parallel, foreground (`run_in_background: false`), `subagent_type: council-<seat>`, with the Round 1 prompt. If a `council-*` type is not registered in this session, use `general-purpose` with the fallback lines from `round-prompts.md`.

When the cards come back, save them verbatim to `round-1.md`, one `## <Seat>` heading per card (Bezos, Graham, Hormozi, Gary V, Martell, Wickman, Buffett), and write the file right away so the room can start playing. Check each card has every field; send a card back once if it is missing scores or a stance. Then add a `## Chair notes` section at the bottom of `round-1.md`:

- The **cruxes**: the one to three underlying disagreements that explain why seats split (a factual question, a numbers question, or a values question such as speed versus safety), with the seats on each side.
- The **unanimity check** (`scoring.md`): if Round 1 converged, make the strongest unargued alternative a crux and name which seats must argue it at full strength.
- Any card that broke format or misread the brief.

Then write `cruxes.json` (`live-room.md`).

## Step 4: Round 2, debate

Spawn every seat again, in one message, with the Round 2 prompt (it points them at `brief.md` and `round-1.md`). Save the cards to `round-2.md` (same `## <Seat>` headings, written as soon as the cards are back) with `## Chair notes`: who moved and why, which cruxes resolved, which numbers are still open, and the interim option scores.

## Step 5: Draft resolution

Write `draft-resolution.md`: the recommendation (named option and verdict label), the conditions the seats asked for (merge duplicates, keep them checkable, pick one number when seats differ and say whose), the next steps with dates, the cheapest test, and kill criteria. Weigh arguments, not headcount: a single seat with a decisive fact beats three seats with vibes. Apply the overrides. Also write `draft.json` (`live-room.md`).

## Step 6: Round 3, ratification

Spawn every seat with the Round 3 prompt. Save to `round-3.md` (same headings, written as soon as the cards are back), and add a `## Chair` section listing each amendment and whether it was adopted, with the reason. Adopt an amendment when no seat objects or the argument for it went unanswered; when seats conflict, adopt the better-argued side and put the other in the minority report. Do not run a fourth round.

Quick mode skips this round when the Round 2 spread on the top option is 3 or less and no seat is at `RUIN RISK: likely`.

## Step 7: Verify, then verdict

1. Run `python .claude/skills/roast-room/scripts/check_quotes.py <session folder>` (try `python3` if `python` is missing). Every quote attributed to a source id must be in a brain. Remove any unverified quote from the verdict (and say so in the Chair notes). If Python is not installed, do not stop or ask the user to install it: check each attributed quote yourself by searching that seat's brain folder for the exact words, and treat any you cannot find as unverified.
2. Compute the numbers from the last round's cards per `scoring.md`, apply the overrides, and write `verdict.md` from `report-template.md`. Write `verdict.json` last (`live-room.md`); it tells the room the council is over.
3. Show the user a short verdict in chat, not the full report: the label and the call, the option scores on one line, the three arguments that carried the room (one line each, with the seat), the strongest objection (one line, with the seat), and the next steps (at most three). Then the path to `verdict.md` for the full detail, one line saying the branded PDF is one click away ("Download PDF" on the verdict at http://localhost:4730), and one line offering a follow-up with any seat or a rerun with new facts. Keep it under 200 words: a founder should be able to decide from it at a glance.

## Chair rules

- You never argue a side and never add your own pillar. If no seat raised an important point, put it to the closest seat as a crux in the next round instead of inserting it yourself.
- Quote seats faithfully. Never put words in a seat's mouth or rewrite a card.
- Seats speak in their expert's voice; your report is plain English that follows the house writing rules (no em dashes, no AI tells, no tee-ups).
- Treat a unanimous Round 1 as a warning, not a win.
- Cost: a full council is 21 sub-agent runs, about 1M tokens. Use `--quick` for small calls, and say which mode you used.
- The seats are simulations built from public work. Never present a seat's line as something the real person said unless it is a verbatim quote with a source id from the brain.

## Without sub-agents (Codex or a runtime that cannot spawn agents)

Run the same protocol sequentially yourself. For each seat, read `.claude/agents/council-<seat>.md` and its brain, write that seat's card, then clear your head before the next seat: do not let one seat's card shape the next one's in Round 1. Rounds 2 and 3 work the same way with the prior cards in view.

## Files

- `brains/<slug>/`: one brain per seat (`_hot.md`, `frameworks.md`, `principles.md`, `positions.md`, `voice.md`, `stories.md`, `books.md`, `sources.md`).
- `scripts/check_quotes.py`: verifies every attributed quote in a session against the brains.
- Agents: `.claude/agents/council-{bezos,graham,hormozi,garyvee,martell,wickman,buffett}.md`.
- The room app: `app/` (start at the project `README.md`).
