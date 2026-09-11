---
name: think-causal-loop-diagrams
description: Builds a signed causal loop diagram by closing the feedback loops in a situation, labeling each loop reinforcing (R) or balancing (B) with its link polarities, and reading likely dynamics (spiral, goal-seeking, or oscillation) off which loop dominates. Use when a situation feeds back on itself - growth that funds more growth, a fix that recreates its own problem, capacity that relieves then re-attracts demand - and you need to see why it keeps accelerating, stalling, or overshooting. Not for a single accumulation, a one-directional consequence tree, or a genuinely linear chain.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.causal-loop-diagrams
  family: systems-and-consequences
  evidence-tier: "M/P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Causal Loop Diagrams

People narrate systems as one-directional chains and silently drop the loop-back. "More users, so more revenue" omits "...which funds acquisition, which brings more users" - the cycle that actually drives the behavior. This skill performs one distinct move: **close the feedback loops and sign them**. Trace each cycle back to its start so it closes, give every link a polarity (does a rise in A raise (+) or lower (-) B), and label the whole loop **reinforcing (R)** when the signs multiply to net-positive (it amplifies: a vicious or virtuous spiral) or **balancing (B)** when they multiply to net-negative (it counteracts: goal-seeking, or oscillation when delayed). Then read likely behavior off the structure: which loop dominates, and therefore whether the system spirals, seeks a goal, or oscillates. The output is a **signed causal loop diagram** framed as a structured argument about dynamics - not a prediction. It corrects a specific, well-evidenced failure (people misperceive feedback); it does not claim to predict the system or to teach systems thinking wholesale.

## When to Use

- A variable plausibly feeds back on itself through a cycle (growth funds growth; a fix recreates its problem; relief of a constraint re-attracts the load).
- The puzzle is *why does this keep accelerating / stalling / overshooting and undershooting* - behavior that a linear story cannot explain.
- You want an inspectable, signed structure (R/B loops with polarities) before reasoning about leverage or intervention.

## When NOT to Use

- **A single accumulation, no loop** (one stock, net flow, no cycle): use `think-stocks-and-flows-reasoning`. That skill reasons about one quantity from its net flow; it does not close or sign a loop.
- **You only need to name that feedback exists** as one structural layer among events, patterns, and structure: use `think-iceberg-model`. It names feedback as a structure item but does not close, sign, or diagram loops.
- **Forward, one-directional consequences** that fan out and do not loop back: use `think-futures-wheel`. It is an acyclic consequence tree by construction - no loop, no polarity.
- **The structure is genuinely open-loop / linear.** If the chain does not actually feed back, forcing a loop manufactures false feedback. Say "no closed loop found - this is a linear chain" and stop; do not invent a loop to fill the diagram.
- Teaching general systems thinking, hunting leverage points, or wholesale systems mapping - out of scope (separate catalog rows). This skill does one move: close and sign loops, then read dominance.

## Instructions

When asked to map why a situation keeps accelerating, stalling, or oscillating, follow these steps:

1. **List the candidate variables.** The quantities and conditions in play (users, marketing spend, capacity, defect rate, morale). Use variables that can rise or fall, not events.
2. **Find the loops by closing them.** For each chain, follow it forward and check whether it returns to a variable it started from. If it does, you have a **closed loop**. If it does not, mark that chain **open (linear)** and set it aside - do not force it closed.
3. **Sign each link.** For every arrow A -> B, assign a polarity: **+** if a rise in A pushes B up (and a fall pushes it down, same direction), **-** if a rise in A pushes B down (opposite direction).
4. **Label each loop R or B.** Multiply the link signs around the loop. Even number of negatives (net +) = **reinforcing (R)**: it amplifies (spiral). Odd number of negatives (net -) = **balancing (B)**: it counteracts (goal-seeking; oscillation if there is a delay). Name and number each loop (R1, B1, ...).
5. **Note delays.** Mark any link where the effect arrives late; delays in balancing loops are what turn goal-seeking into oscillation/overshoot.
6. **Read the behavior off the structure.** State which loop currently **dominates** and the resulting dynamic: reinforcing dominance = a vicious or virtuous **spiral**; balancing dominance = **goal-seeking**; a delayed balancing loop = **oscillation**. Frame this as an argument ("if R1 dominates, expect..."), explicitly not a prediction.
7. **Record the open parts honestly.** Note where no loop closed, so the diagram does not overstate how much of the situation is actually feedback-driven.
8. **Emit the signed causal loop diagram** per `references/TEMPLATE.md`.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the signed loop diagram - the R/B loop inventory with link polarities and the behavior read-out framed as an argument - not prose.

## Quality Checklist

Before finalizing, verify:

- [ ] Every loop is genuinely **closed** (the chain returns to a variable it started from); open chains are marked linear, not forced into loops.
- [ ] Every link has a polarity (+/-), and each loop's R/B label follows from the product of its signs.
- [ ] Delays are marked where they exist (they drive oscillation/overshoot).
- [ ] The behavior read-out names the **dominant** loop and the resulting dynamic (spiral / goal-seeking / oscillation).
- [ ] The read-out is framed as a structured **argument**, not a prediction or forecast.
- [ ] No loop was manufactured to fill the diagram; the linear parts are recorded honestly.
- [ ] No overclaim: it externalizes and signs structure; it does not predict the system or teach systems thinking wholesale (see `evidence/dossier.md`).
- [ ] The output is the signed causal loop diagram artifact, not prose.

## Evidence

Tier **M/P**, transferred-evidence. The strongly evidenced fact is the **failure** this skill targets: people systematically misperceive feedback and accumulation (Sterman 1989, *Management Science*; Sweeney & Sterman 2000, *System Dynamics Review*). That base is shared with `think-stocks-and-flows-reasoning` and does **not** by itself prove that drawing a causal loop diagram fixes it. The CLD-specific evidence is **moderate and conditional**: a 2025 quasi-experimental study (ScienceDirect S2451958825000284) finds a conditional effect, and Schaffernicht (2010, *Systems Research and Behavioral Science*) documents CLD reliability problems (subjectivity, non-reproducibility) - cited here against inflation. All evidence is human-subject, not AI-agent-validated. The transferable claim is scoped to **externalizing loop structure and signing polarity**, not to predicting system behavior. No effect size is quoted because none has been verified against the source. Full grading: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed signed causal loop diagram.
