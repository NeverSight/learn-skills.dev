---
name: workflow-score-to-target
description: Score work out of 10 against a clear rubric, then improve it round by round until every item reaches the target score the user named (for example "get it to 8 out of 10", "bring everything under 6 up to 6+"). Covers anchored rubrics, measurable criteria, independent or blind judging, before/after scorecards, and honest reporting of anything still short. Use whenever the user asks to score, rate, grade or judge something out of 10, names a target score, or asks "what would make this a 9?".
---

# Workflow: score to a target

The user sets quality bars as numbers:
- "score them out of 10. let's get them to 8 out of 10"
- "anything less than 6 out of 10, get them to 6+"
- "give it a score out of 10. get at least 8"
- "make it 8 or 9 out of 10"

The job isn't just the score; it's reaching the bar, proving it, and saying plainly where it falls short.

## 1. Pin down the target and the items

- Restate the bar: the target (6, 8 or 9), and whether it applies to **every** item or the average. "Get them to 8" means every item reaches 8.
- List every item being scored: each skill, each weapon, each screen element, each object. Score them one by one, never as one blob.
- Name the benchmark the user judges against, such as the games or sites they compare to. A 7 means nothing without one.
- **A bar the user sets once is a standing rule for that kind of work.** Record it where future work will see it, such as project instructions, memory, or a test.

## 2. Anchor the rubric before scoring

Write the scale down so scores mean the same every round. Default anchors:

| Score | Means |
|---|---|
| 10 | Best-in-class, something you'd study |
| 9 | Excellent: a trained eye finds almost nothing |
| 8 | Polished and intentional, only minor nits |
| 7 | Good, but a noticeable flaw |
| 6 | Acceptable: works and reads clearly, with visible rough edges |
| 5 | Mediocre: the idea is there, the execution distracts |
| 3–4 | Clearly broken or wrong in places |
| 1–2 | Barely works, or reads as something else |

Then break each item into 3–5 criteria, **0–2 points each**, so the total is out of 10 and every point has a reason. For example:

- **Animation:** weight and timing, body mechanics, final pose, props, context and variety.
- **A skill or spell:** its rules (a clear job of its own), the hover (shows where it lands and the numbers), the cast (its own pose, effect and sound), and what it leaves behind that you can see.
- **An object:** silhouette at play distance, material and detail, fitting its setting, readability.

Wherever a criterion can be measured, measure it. Examples:
- foot slide under 10% of travel speed;
- weapon clipping in millimetres;
- a 48% win rate over 40 seeds;
- a download of 28 MB.

Numbers stop the score drifting with mood.

## 3. Score honestly from real evidence

- Score from renders, recordings or measurements of the actual thing, never from the code or from memory. Capture the state first; see the `workflow-progress-screenshots` skill.
- Score the baseline before changing anything. The before→after is the proof.
- **Judge independently when it matters.** Hand the captures to a fresh subagent that didn't do the work. Give it the rubric and benchmark, but not your hopes or the previous scores. Use two blind judges per item if you can, and take the lower score or reconcile the difference.
- Never round up to reach the bar. A 7.5 on an 8 bar is below the bar.

## 4. Improve in rounds

1. Fix the lowest items first, and the criterion costing the most points in each.
2. Re-capture, and re-score only with the same rubric and judge setup.
3. Send a picture per round (the start and the result), with the score moving: for example, "Hollow Keeper 3 → 6 → 8".
4. Stop when every item meets the bar, or when an item plateaus because of something outside the task (a model limit, an art asset, a performance budget). Report that item as short, with the reason and what it would take.
5. Keep guardrails while climbing: don't trade away performance budgets, tests or other items' scores to raise one number. Note any trade-off you made.

## 5. Lock it in

- Where the bar can be checked by a machine, add a test so it can't quietly regress. Examples: weapons out of bodies in seven poses, a skill has its own pose and card, win rate at least 90%.
- Save the scorecard in the project (for example `qa/<area>/README.md`), with the rubric, every item's before and after, the evidence, and the date. Future rounds start from it.

## Report

Lead with the result: "All 49 now score 8 or better; 38 started below 8; the average rose from 6.7 to 8.1."

Then:

- **A table:** item, before → after, and the main fault fixed (or the reason it's still short). See `templates/scorecard.md`.
- **How it was scored:** the rubric, the benchmark, who judged (you, an independent subagent, or blind judges), and from what evidence.
- **Where it isn't perfect:** items at or just over the bar with known nits, and anything still below.
- **The pictures:** before and after per item, or per round.
- Say that scores are judgements. Say which criteria were measured, and label captures honestly.
