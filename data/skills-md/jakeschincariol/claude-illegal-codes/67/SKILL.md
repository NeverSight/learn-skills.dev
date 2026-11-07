---
name: "67"
description: Runs the task through six agents in parallel, each locked to a different strategy, then a seventh judge ranks the six attempts and synthesizes a final answer that steals the strongest part of each; invoke via /67 for high-stakes or open-ended work where a single attempt would leave quality on the table.
---

# 67

One attempt is a sample size of one. This runs six, each forced down a different road, then a seventh agent judges the field, ranks it, and builds the final from the best parts. You ship the strongest version that exists, not the first one that came out.

## When to use
- High-stakes deliverables: the pitch, the architecture, the pricing page, the cold email.
- Open-ended problems with many valid approaches and no obvious winner.
- Not for trivial tasks. Six agents on a one-liner is theater.

## Behavior

### 1. Frame once
Write a single task brief every agent receives verbatim: the task, the deliverable format, and the constraints. Tight enough that all six outputs are directly comparable.

### 2. Fan out six agents in parallel
Spawn all six in one message (Agent/Task tool). Each gets the same brief plus ONE strategy lock it must follow:

| # | Lens | Instruction |
|---|------|-------------|
| 1 | Minimalist | Smallest thing that fully works. Cut everything optional. |
| 2 | Maximalist | Most complete version. Cover every edge and every objection. |
| 3 | First principles | Ignore convention. Derive the answer from scratch. |
| 4 | Prior art | Find how the best existing versions do it and adapt the strongest pattern. |
| 5 | Adversarial | Design against failure. Ask what breaks each choice, keep what survives. |
| 6 | Wildcard | One unreasonable creative bet, executed seriously. |

Each agent must return a complete, standalone answer. No hedging, no "it depends" without a decision.

If no sub-agent tool is available, run six sequential passes with a hard reset between each: "discard the previous approach entirely; you are now agent N with this lens."

### 3. Agent seven judges
The judge never writes its own answer first. It scores each attempt 1 to 10 on correctness, completeness, and taste; ranks all six with a one-line verdict each; and names each attempt's single strongest element, including the losers'.

### 4. Synthesize
Build the final on the winner's skeleton, then graft in every strongest element worth stealing. Note what was taken from whom.

## Output
The leaderboard (rank, score, one-line verdict per agent), then the synthesized final, then a short "stolen parts" ledger.
