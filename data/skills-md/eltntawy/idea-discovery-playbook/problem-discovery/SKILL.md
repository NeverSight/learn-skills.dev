---
name: problem-discovery
description: Runs Mom Test-style problem discovery for software ideas, including ICP definition, interview scripts, pain scoring, commitment signals, and kill criteria. Use when the user asks about problem interviews, pain validation, ICP, customer discovery, or whether a problem is real.
disable-model-invocation: true
---

# Problem Discovery

Validate the **problem** before the solution. Use past behavior, workarounds, and spend — not hypotheticals or compliments.

If `discovery/INDEX.md` is missing, create it with the active topic slug before saving artifacts.

## Checklist

- [ ] State the problem hypothesis and target user
- [ ] Define ICP and disqualifiers
- [ ] Prep **big 3 learning goals** (scariest unknowns) for this batch
- [ ] Run desk research first when it can answer a question without interviews
- [ ] Draft past-focused questions (question ladder below)
- [ ] Target **15–20** ICP interviews (minimum **8** before a strong go on problem)
- [ ] Collect evidence from multiple **independent** sources (not friends-only)
- [ ] Score pain frequency and intensity
- [ ] Record workaround behavior and commitment signals
- [ ] Run a **batch review** and update big 3 + next segment
- [ ] Set kill criteria before recommending more work

## Before each batch

1. Choose a focused, findable segment (who + where to reach them).
2. As a team (or solo), write the **big 3 learning goals** — what must be true after this batch?
3. Commit to **no pitching** until the last 2 minutes (if at all).
4. Prepare 8–10 past-focused questions from the ladder below.

## No-pitch opener

> I'm researching how [ICP] handles [job/problem]. I'm not selling anything — I want to learn from your experience. Can I ask about the last time you dealt with this?

## Question ladder

Ask specifics in the past. Do not ask "Would you use this?"

| Level                   | Purpose                   | Example                                                                     |
| ----------------------- | ------------------------- | --------------------------------------------------------------------------- |
| A — Last time           | Anchor in real events     | "Tell me about the last time you [faced X]. Walk me through what happened." |
| B — Pain and impact     | Frequency and cost        | "What was hardest? What did it cost in time, money, or risk?"               |
| C — Workarounds         | Proof the problem is real | "What do you use today? What hacks or spreadsheets do people use?"          |
| D — Money and decisions | Budget and buying process | "What did you pay last time? Who approves spend? What almost stopped you?"  |

## Interview rules (Mom Test)

- Talk about **their life**, not your idea.
- Ask about **specifics in the past**, not generics about the future.
- **Listen** — aim for them talking ~80% of the time.
- Deflect compliments; dig under "that's interesting."
- End with a **commitment** when pain seems real (see below).

## Commitment ladder (strongest last)

| Type       | Example signal                                           |
| ---------- | -------------------------------------------------------- |
| Time       | Follow-up call, beta review session, design-partner hour |
| Reputation | Intro to boss, peer, or budget holder                    |
| Financial  | Pre-order, deposit, LOI, paid pilot                      |

## Notes template (per interview)

| Column                     | Capture                              |
| -------------------------- | ------------------------------------ |
| Problems and pains         | Verbatim quotes, triggers, frequency |
| Workarounds and solutions  | Tools, hacks, spend, switching pain  |
| Commitments and next steps | What they agreed to do, if anything  |

## Evidence table

| Source | Quote or signal | Frequency | Workaround | Willingness signal |
| ------ | --------------- | --------- | ---------- | ------------------ |
|        |                 |           |            |                    |

## Pain score

Rate 1–10 for frequency, intensity, and work impact. Note whether the pain is professional, recurring, and tied to revenue or efficiency.

**Strong go on problem (directional):** at least half of relevant interviews confirm urgent, recurring pain with workarounds or spend. Align with `idea-scorecard` kill cues.

## Kill criteria

Kill or pause if:

- No independent sources describe the problem
- The problem is rare or tolerated
- Users show no workaround or spend behavior
- Fewer than half of relevant interviews confirm the problem after a full batch

## After each batch (weekly or per batch)

- Review notes together; hunt **patterns** (recurring pains, segments, workarounds).
- Update the big 3: answered, still open, newly emerged.
- Decide: more interviews (same or new segment), pivot segment, or escalate to market validation.

## Escalation

- **Switching / why they buy** → `jtbd-interviews` skill
- **Riskiest assumptions and test queue** → `assumption-map` skill
- **Live market and competitors** → `market-research` skill

## Output

Save to `discovery/<topic-slug>/briefs/YYYY-MM-DD-<topic-slug>-brief.md` using Facts, Assumptions, Evidence, Analysis, Decision, Next experiment.

Read `discovery/INDEX.md` and the topic's existing artifacts first.

When opening a new active research folder, create `discovery/<topic-slug>/TOPIC.md` from [TOPIC-TEMPLATE.md](TOPIC-TEMPLATE.md) and add the slug to `discovery/INDEX.md`.
