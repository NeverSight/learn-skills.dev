---
name: hook-and-pacing
description: Control serial pacing - opening lines, chapter-end hooks, arc rhythm, release cadence. Use when drafting any chapter's opening and closing, and when planning arc temperature.
metadata:
  type: skill
  tier: craft
  force: structural
  when: always
  role: [design, draft, gate]
  owns: [chapter-opening, chapter-hook, temperature-ledger, release-cadence]
---

# hook-and-pacing

Serialized fiction is read one chapter at a time, days apart, on a phone, by someone who is
following six other stories. Every chapter has to re-earn the reader. This skill is about the two
positions that do that work: the first 100 words and the last 100.

**What sits between them is not here.** Whether a beat is played or reported — the decision that
sets how fast a story actually moves — belongs to `story-craft`. This skill can make an opening land
and a hook pull; it cannot stop a chapter from summarising its own turning point.

---

## What lives in `roles/`

| file | open it when |
|---|---|
| `roles/design/hook-and-pacing.the-long-middle.md` | any arc boundary past arc 2, or a stretch that is competently written and building toward nothing anyone can name |
| `roles/shared/hook-and-pacing.arc-rhythm.md` | planning an arc's temperature, or the story is reading as relentless or as flat over a stretch of chapters |

## Chapter length is not a quality metric

**A chapter is judged by what it delivers, not by how long it is.** The gate is
`revision-pass` Pass 9 — want, friction, **change**, cost, next — and this skill has nothing to
add to it. `novel.md` → `chapters.length_band` is a printer's note: the range outside which a
chapter is worth a second look, and nothing more.

This is a correction, and the history is worth knowing because the failure repeats. This skill
used to carry a target with tolerances. Chapters then clustered against the floor. The tolerance
was tightened to ±15% of target; chapters clustered against the new implied floor, and one landed
on the declared minimum **to the word**. A number that gates publication gets optimised, and prose
optimised toward a length is padded or truncated prose. There is no version of this rule that
does not get gamed, so there is no rule.

What the band is still good for:

- Under ~1,200 words a chapter reads as a fragment — usually a real signal that the material was
  split in the wrong place, not that it needs padding.
- Over ~3,000 it gets abandoned mid-chapter on a commute, and a chapter abandoned halfway is worse
  than one never started.
- **Consistency is a reader expectation, not a target.** Readers form a sense of your chapter size
  from the first ten and feel short-changed by sudden deviation. A chapter at half your usual size
  needs a reason; it does not need filler.
- Higher release cadence supports shorter chapters. Weekly releases need more substance per
  chapter and a stronger recap clause.

**Never pad, and never trim to a number.** If the chapter's material ends, it ends. If it runs
long and every scene is delivering, ship it long. The only length question worth asking is the
skim test (`roles/shared/hook-and-pacing.arc-rhythm.md`): *would a reader lose anything by skipping this?*

**What to do when a chapter comes out short.** Not padding — diagnosis. A short chapter almost
always means one of: the turn happened offstage, the cost was skipped, or a scene ended at its
first obstacle instead of its consequence. Fix the delivery and the length follows. Pulling
material forward from the next chapter is legitimate; adding sentences is not.

## Openings

The reader is deciding whether to keep going. You have two sentences.

**Never open with:** weather · waking up · a recap paragraph · an in-world encyclopaedia entry ·
a rank or status recital · a date/time stamp alone · a character reflecting on the last chapter.

**Openings that work:**

| type | shape |
|---|---|
| Mid-argument | a line of dialogue already in conflict |
| Action in progress | the verb is already happening |
| Wrong detail | something present that should not be, stated flatly |
| Declarative with a story inside it | *The coat did not fit and she wore it anyway.* |
| Consequence first | open on the aftermath, fill in backwards inside the scene |
| Contradiction of the last hook | the hook promised a fight; open on the two of them eating |

**Re-anchoring.** Readers arrive days later. Carry the recap in **one clause inside a sentence
doing other work** — never a paragraph, never "as you'll recall". If a chapter genuinely needs
more context than one clause, the previous chapter's hook was unclear.

## Hooks

`chapters.hook_required: true` means every chapter ends on one. A hook is not a cliffhanger — a
sword swinging mid-air every chapter exhausts readers and cheapens the real ones.

A hook is **an unresolved pressure the reader wants relieved.**

| hook type | slug | what it does | frequency |
|---|---|---|---|
| **Revelation** | `reveal` | new information reframes what came before | often |
| **Arrival** | `arrival` | someone or something appears | often |
| **Decision** | `decision` | the MC chooses, and the reader wants the consequence | often |
| **Question** | `question` | a fact that does not fit | often |
| **Threat** | `threat` | a clock starts, or an intention is stated | moderate |
| **Reversal** | `reversal` | what the reader thought was true is not | occasional |
| **Cliffhanger** | `cliff` | physical peril, unresolved | **max once per 8–10 chapters** |
| **Quiet** | `quiet` | a line that lands emotionally; no question at all | once per arc, after a heavy chapter |

The slug goes in the `hooktype` column of `plan/chapters.md`, **set when the row is planned, not
after the chapter is written**. Written afterwards it is a label describing what came out;
written beforehand it is a decision the prose has to meet. `sw arc` checks the distribution — no
shape more than twice in any five chapters, four distinct shapes across an arc — and never scores
a single chapter, because a per-chapter rule here is satisfied by appending a sentence.

**Construction.**

1. End on the **last strong beat**, not on the wind-down after it. The most common hook failure
   is three paragraphs past the right stopping point.
2. Put the hook in the **final sentence or short paragraph**, alone on the line.
3. Make it **concrete**. "Something was wrong" is not a hook. "His father's name was the first
   line in the ledger" is.
4. **Do not answer it in the first line of the next chapter.** Let it breathe for a page.
5. **Rotate types.** Three revelation hooks in a row and the reader stops feeling them.
   Benchmark run #2 closed *four of five* chapters on the same shape — a short, withheld,
   ironic line of narration with nobody speaking: *"The gate hung open." · "The small hand found
   hers, tighter, in her sleep." · "Neither did Odell." · "The door stayed shut, this time, and
   nobody was watching it."* Each one is a good last line. Together they are a tic, and a reader
   registers the sameness long before they could say what is repeating. `sw lint` reports this
   as `closer-sameness`.
6. The **arc-ending hook** is the strongest in the arc — usually a reversal or a threat that
   reframes the next 25 chapters.

**Hook honesty.** A hook that implies a fight and delivers a conversation is a bait. It works once
and costs trust. Deliver the thing you implied, or deliver something better and more surprising —
never something smaller.

## The temperature ledger

Nothing in this toolkit tracked register before, which is why benchmark run #2 did not have one.
Five chapters, one temperature: quiet, interior, controlled, ironic. A massacre, a forged
record, a governor's interrogation and a child refusing a bowl of rice all read at exactly the
same pitch — and a reader who cannot point at a bad sentence still closes the tab, because a
book with one gear is a book that does not seem to care which scene it is in.

Every planned row in `plan/chapters.md` declares a **temp** before it is drafted:

| temp | what the chapter feels like |
|---|---|
| `fast` | events outrun reflection; the POV character is behind the situation |
| `tense` | slow, but something could go wrong at any line |
| `loud` | confrontation, a crowd, a fight, a public scene |
| `warm` | connection that is not undercut — allowed to simply land |
| `funny` | the chapter is enjoying itself; the stakes still exist |
| `bleak` | the cost is paid and nothing softens it |
| `procedural` | competence on display; the pleasure is watching work get done |
| `quiet` | recovery, intimacy, the small scene after the loud one |

**Rules, all distributional.**

- Never the same temp three chapters running.
- At least four distinct temps across an arc.
- **Every temperature is earned, in both directions.** `quiet` and `warm` land because the
  chapter before them was `loud` or `bleak`; `bleak` and `tense` land because something before
  them was worth keeping. Two quiet chapters running is a stall, and so is a fourth grim one —
  the reader stops paying emotional attention to a book that never repays it. Until 2026-09-22
  only the first half of this rule was written down, which is most of why five runs came out at
  one temperature.
- The temp is written **before** drafting. Set afterwards it is a label; set beforehand it is a
  constraint the prose has to satisfy.

**What `warm` and `funny` actually require**, since a label is not a method and these two are the
rows a drafter is most likely to write as a cold chapter with a nice thing in it:

| | it is working when | it is not when |
|---|---|---|
| `warm` | the connection is *not undercut* — no ironic tag on the last line, no pulling back to safety | the scene closes on the narrator declining to feel it |
| `funny` | the joke comes from character and the stakes survive it | the narration signals that a line was funny |

The move that ruins both is the same one: reaching the good beat and then flinching off it. A
`warm` chapter is allowed to simply land, and one that isn't allowed to land was a `quiet` chapter
mislabelled. `conflict-engine` §What the chapter gives back is where the material comes from;
`comedy-levity` owns humour placement when it is switched on, and `voice-separation` owns who in
the cast can carry a joke at all.

`sw arc` prints the ledger and flags runs, thin variety, and hook repeats. It does not score any
chapter, and it must not — a number attached to one chapter is a number the next chapter gets
written toward (`docs/design-notes.md`, "Why the gate is delivery, not length").

**Temperature is not the same as pacing.** `temp` is what the *chapter* feels like from outside;
the table below is how sentences move *within* it. A `quiet` chapter still varies its sentence
speed internally.

## Pacing within a chapter

| register | sentence & paragraph shape |
|---|---|
| fast | short sentences, short paragraphs, dialogue with few beats, cuts between actions |
| medium | mixed lengths, action beats between exchanges, one grounding detail per paragraph |
| slow | longer subordinated sentences, interiority, sensory detail, silence given room |

Vary it *within* the chapter, not just between chapters. A 2,000-word chapter at one speed is
monotonous whatever that speed is. The standard shape: medium open → fast through the turn →
slow for the follow-through → fast for the hook.

## Self-check

- [ ] Opening does not use a banned pattern; it earns the second sentence
- [ ] Re-anchoring is one clause, not a paragraph
- [ ] The chapter ends on its last strong beat, not after it
- [ ] The hook is concrete and in the final sentence or paragraph
- [ ] Hook type differs from the previous two chapters
- [ ] No cliffhanger if one fired within the last 8 chapters
- [ ] Pace varies within the chapter
- [ ] The chapter passes the skim test
- [ ] The chapter delivers a **change** — `revision-pass` Pass 9, not a word count
- [ ] Nothing was padded, and nothing was trimmed, to reach a number
- [ ] If the chapter is far outside `length_band`, that was a decision and not an accident
