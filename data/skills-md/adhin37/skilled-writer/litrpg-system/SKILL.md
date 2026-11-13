---
name: litrpg-system
description: Optional (default off). Run a game-like system layer - status screens, levels, skills, quests - with discipline about frequency and what the numbers decide. Use only while enabled.
metadata:
  type: skill
  tier: optional
  force: structural
  when: optional.litrpg-system == on
  role: [design, draft, gate]
  owns: [system-layer, status-screen]
---

# litrpg-system

**Gate.** Applies only if `novel.md` → `optional.litrpg-system` is `on`. If `off`, no status
screens, no numbers, no system voice anywhere. Ever.

A system layer is a legitimate, popular structure. It is also the fastest way to replace a story
with a spreadsheet. These rules keep it a story.

---

## Design

**Answer the diegetic question first, and record it in `bible/power-system.md`:**

| question | why it matters |
|---|---|
| Who or what made the system? | Determines whether it can lie, err, or want something |
| Does everyone see it, or only the MC? | Changes every social scene in the novel |
| Can it be wrong, gamed, or hidden from? | A system that cannot be gamed is a scoreboard |
| Who benefits from people believing it? | This is where the plot is |
| What does it *not* measure? | The most important question. It is where character lives |

A system that is simply true, universal and impartial gives you nothing to write about. Give it an
origin, an interest, or a flaw.

**Numbers must mean something concrete.** If the reader cannot say what 14 Strength lets someone
do that 12 did not, the numbers are decoration. Anchor the scale to a physical referent early
(*10 is a fit adult; 20 lifts a door off its hinges*) and hold it.

**Levels render `state/power.md` §2's ladder; they are not a second ladder.** `power-scaling` owns
the mapping, where it is recorded, and when a level-up counts as a gain — follow it rather than
keeping a second set of rules here.

**Levels are not the progression.** Character growth, skill, and understanding are. A level-up
that changes nothing about how the MC solves problems is a receipt, not a beat.

## Formatting discipline

- **One status block per chapter, maximum.** Most chapters have none.
- **Never open a chapter with a status block.** It is the equivalent of a rank recital.
- Blocks are **short**: 3–8 lines. A full character sheet appears at most a few times in a novel —
  after major transitions — and never as a substitute for a scene.
- **Never repeat unchanged values.** Show the delta only.
- **System text is the meta channel, `[…]`** — `narrator-voice` §The four channels owns the
  convention; `bible/lexicon.md` §Meta block format holds this novel's exact shape. Set it once
  and never vary it. Skill and spell names appear in brackets in the narrative the same way, which
  is what lets a reader's eye skip a block they have already absorbed.
- **Never two meta blocks in a row**, and never one in place of a scene.
- **The system does not narrate the story.** No "Congratulations! You have defeated…" flattery,
  no system commentary standing in for the MC's reaction. If the system has a voice, it is a
  character with an agenda, and it is used sparingly.

Recommended minimal form:

```
[ Echo-step — Rank 2 (was 1)
  Cost: 6 hours' recovery, down from 12 ]
```

Inline, mid-sentence, for a single value or a named skill: `[Echo-step]`, `[Rank 2]`. The block
form is for a delta the reader has to stop and read; the inline form is for a name.

## Narrative rules

**The numbers never resolve the conflict.** They describe capability; the MC's choices, plans and
costs resolve things. A fight won because a number was higher is a fight the reader could have
skipped.

**Notifications interrupt at the worst times, and that costs.** A screen appearing mid-fight is a
half-second of attention the MC does not have. Use it as pressure, not as a reward chime.

**Quests are obligations with consequences**, not to-do lists. A quest the MC can decline without
cost is not a quest. Rewards are priced (see `power-system`'s escalation budget: every gain
creates a new problem).

**The system's categories are not the truth.** A person the system labels an enemy may not be one.
This gap — between the measurement and the reality — is where the best stories in this subgenre
live, and it is free.

**Grinding is not a chapter.** Repetitive advancement is compressed to a sentence unless
something goes wrong.

## Self-check

- [ ] At most one status block, and it is not at the chapter opening
- [ ] Only changed values shown
- [ ] Every number in the block has a concrete meaning the reader can state
- [ ] No system flattery, no system narrating the reader's reaction
- [ ] The chapter's conflict was resolved by a choice, not by a stat
- [ ] Any gain created a new problem
- [ ] The block format matches `lexicon.md`, and uses the `[…]` meta channel
