---
name: decision-importance-prioritization
description: A framework for classifying product decisions based on impact and reversibility. Use this when you feel like a bottleneck for your team, when you have a massive backlog of choices to make, or when you need to justify spending weeks of research on a single high-stakes problem.
---

The most important part of making a decision is determining how important that decision actually is. By categorizing decisions, you can maintain high team velocity for the trivial and apply rigorous deliberation to the critical few.

## The Classification Framework

Evaluate every decision against two primary filters to determine its "Importance Score."

### 1. Reversibility
- **Low Importance (Reversible):** If the decision is wrong, can you undo it quickly without lasting damage to the brand or technical debt? (e.g., UI copy, small feature toggles).
- **High Importance (Irreversible):** Is this a "one-way door"? Once shipped, does it change the data schema, API contract, or user mental model in a way that is painful to revert? (e.g., pricing changes, platform architecture).

### 2. Material Impact
- **Breadth:** How many users/stakeholders does this affect? (1% vs. 100%).
- **Depth:** How much does it affect them? Does it impact their livelihood or core workflow, or is it a minor convenience?

## The 1/99 Resource Allocation Rule

Once classified, apply your cognitive energy and time disproportionately:

### For the 1% (High Importance)
- **Spend 90% of your time here.**
- Conduct deep research, seek peer feedback, and build high-conviction models.
- "Shoot your shot" only when the strategy is sound, as your reputation and the product's trajectory depend on these few calls.

### For the 99% (Low Importance)
- **Optimize for Speed.**
- **Use your gut:** If a decision is reversible, your intuition is often "good enough."
- **Delegate:** Give these decisions to the team to build their autonomy and "trust battery."
- **Rule of Thumb:** Never be the bottleneck for a reversible decision. Make a call in minutes, not days.

## Implementation Steps

1.  **Identify the Decision:** Clearly state the choice at hand.
2.  **Run the Filters:** Ask, "If this is a disaster, how hard is it to fix?" and "How many people will actually notice?"
3.  **Set the Deadline:** 
    - If Low Importance: Decide within the meeting or by the end of the day.
    - If High Importance: Schedule a dedicated "Deep Dive" or "Investment Plan" review.
4.  **Communicate the "Why":** When delegating or making a fast "gut" call, explain that the low stakes allow for higher velocity.

## Examples

**Example 1: UI Polish**
- **Context:** A designer asks for a decision on whether a secondary action button should be gray or light blue.
- **Application:** This is highly reversible and has low depth of impact.
- **Output:** "Go with your preference. This is a reversible decision; let's ship it and see the heatmaps. Don't let me block you."

**Example 2: Platform API Change**
- **Context:** Changing the way third-party developers access merchant order data.
- **Application:** This is irreversible (breaks existing apps) and has high depth (affects developer livelihoods).
- **Output:** Classify as High Importance. Stop other work. Spend two weeks on a "war time" document analyzing edge cases, data policy, and developer sentiment before deciding.

## Common Pitfalls

- **The Analysis Paralysis Trap:** Treating a reversible decision with the same rigor as an irreversible one. This kills team momentum and wastes your most valuable resource: focus.
- **The Bottleneck Manager:** Requiring all small decisions to cross your desk. This drains the team's "trust battery" and makes you a single point of failure.
- **Sunk-Cost Fallacy:** Sticking with a High Importance decision after the world has changed (e.g., a global pandemic). Have the humility to "throw it all away" if the original conviction is no longer valid.
- **Ignoring "Depth" for "Breadth":** Making a decision because it affects few people, even if it completely ruins the experience for those specific few (e.g., power users or top-tier developers). Always weigh the severity of the impact.