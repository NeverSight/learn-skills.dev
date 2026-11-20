---
name: north-star
description: Distill a pile of wants into one north star sentence, with the Five W's beneath it.
disable-model-invocation: true
argument-hint: "What are you trying to get clear about?"
---

# North Star

The user arrives with **wants**: things they want to build, fix, have, or become. Wants are surface. Under each want sits a **need**, the reason that want matters, and under the needs sits a single **why**. This skill ladders from the pile down to that why, states it as one sentence, and writes it down.

**A compass, not a plan.** The output points; it does not sequence. When *how* and *when* crowd in, note them on the side and carry on — the star has to outlive the plan.

Interview **relentlessly**. The user will offer the first plausible answer and want to be finished; that answer is almost always a want restated. Keep pushing.

## Rounds

Work in **rounds**. Number each question and put your own recommended answer beneath it, so the user corrects rather than composes. One round per message: wait for the answers before the next round.

When a round is a genuine choice between options, ask it with a tappable-options tool if one is available — choosing costs the user less than typing. Keep the laddering rounds typed: there the exact wording *is* the data, and options would put your words in the user's mouth.

```
❓ **Q1** — **<title>**: <question>

➡️ <your recommended answer>
```

## 1. Read before you ask

A question whose answer is already written down is worse than no question. Before the first round, exhaust what you can reach:

- An existing `NORTH-STAR.md`, `MISSION.md`, `CONTEXT.md`, README, or planning notes in the workspace
- The conversation so far, and anything the user attached
- The codebase, which often states what someone is actually building more honestly than a hurried reply will

Bring what you found into round one as a draft pile the user edits, rather than a blank page they fill. An existing star is a **revision**, not a fresh start: open by asking what moved.

Done when you have either a draft pile from the sources, or a specific reason there was nothing to find.

## 2. Empty the pile

Get every want out, unranked and unjudged. Ask what they want, then ask what else, until they are empty. Push for the wants that feel too small, too obvious, or too embarrassing to say — those carry the most signal.

Read the pile back as a list. Done when the user recognises the list and has nothing to add.

## 3. Ladder each want to bedrock

Take a want. Ask why it matters. Take that answer and ask why *it* matters. Repeat until the answer stops moving — the same reason coming back in different words. That is **bedrock**: a need.

Catch two things while laddering:

- **A how in a why's clothing.** "I need a knowledge graph" names a mechanism. Ask what the mechanism buys and it drops away, leaving the need.
- **Someone else's why.** Some reasons are inherited — an employer's, an industry's, a peer group's. Keep them, and mark them: the user should see which needs they hold and which they are carrying for someone else.

Done when every want in the pile traces to bedrock, and one more push on that bedrock returns the same answer twice.

## 4. Find the one why

Cluster the bedrock needs. Most of them turn out to serve a smaller number, and often one. Present the clustering and name the candidate why: the need the others are in service of.

**Two stars is no star.** If the pile genuinely splits into two unrelated whys, say so plainly and split it: one north star each, and the user picks which one this session is for.

Done when the user agrees on a single candidate why.

## 5. Test the candidate

Five tests. A fail sends you back to step 3 or step 4 — it does not get waived.

- **Inversion** — would anyone sane claim the opposite? If nobody would, it is a platitude ("do good work", "deliver value") and it steers nothing. Rewrite until the inverse is a position a real person holds.
- **Forbid** — name at least two wants from step 2 that this star says no to. A star that forbids nothing is decoration.
- **Signature** — could someone else in the user's position sign it unchanged? Then it is the field's why, not theirs. Sharpen until it is theirs.
- **Live decision** — take three decisions the user has open right now and run each through the star. It must change or confirm at least two. If it moves none, it is not operative.
- **Survival** — would it still hold if the current job, tool, project, or plan vanished? If not, it is a how. Ladder further.

Done when all five pass and you can show the user the evidence for each, test by test.

## 6. Write it

Read [`references/NORTH-STAR-FORMAT.md`](references/NORTH-STAR-FORMAT.md) and draft the document.

Show the draft and hand control back before writing anything to disk: the star is the user's to sign, not yours to file. Ask whether it lands or what to change, and where it should go — defaulting to `./NORTH-STAR.md`.

Once they sign it, write the file, then read the star sentence back on its own with none of the scaffolding. It has to stand up alone.
