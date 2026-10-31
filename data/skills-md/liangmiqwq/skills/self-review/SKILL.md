---
name: self-review
description: Load this skill when you are required to handling Codex's review suggestion on GitHub (`@codex review`). Do not load it when you are just handling someone else's review suggestions or just adjusting code according to the prompt.
---

## Before the review

You shouldn't fetch GitHub review suggestions or start to do code change at first. The first task for you is to understand the PR's motivation and design direction.

You can read the PR description, original commit and diff, make sure you completely understand the goal the PR makes. Breaking changes boundary and features that are explicitly postponed.

If you are in a loop, or in a `goal` mode, you should storage all these things, make sure you can still remember them during your sessions. Keep them in mind.

Sometimes, users won't let you to use `@codex review` directly. Follow users' guidance such as `using subagents to review`.

## Handle the review

When you are required to resolve Codex's review, you are basically in a loop. I'm not sure where is the start of the loop, maybe you will find users already called `@codex review` for you. And you should continue this loop unless users tell you only fix one turn.

You are required to handle this process, and for detailed things, like analyzing the review suggestion should be done by subagents, refer to `How to handle the resaonable review suggestions` part to learn more about how to divide the jobs.

- Submit a comment under the corresponding pull request, the content of the comment is `@codex review`
- Wait for its responding and review suggestions. It usually takes 5-15 minutes, you'd better to check it every minute. If you didn't get the response in one hour, stop and tell the user `timeout`.
- After you get the Codex's response, there can be three different cases. If you get the message that `limitation hit`, stop and tell the user that no enough credit, or if you get the message `Didn't find any major issues.`, stop and do the rest of operations below, if you get review suggestions, just switch to the next step.
- Do not start modify the code immediately, you need to determine whether it is a valid suggestion first. Divide them into these cases.
  - True regression: the real regression issue that the PR imports
  - Old problem: the problem that already has before this PR.
  - Defensive edge cases: boundary conditions like broken status and breaking installation
  - Design conflict: the solution to the problem conflicts with the core design direction of the PR. Like things that are explicitly postponed.
- Make patches and commits to resolve valid ones, then mark them as resolved. Explain design conflict, old problems, etc... Mark unreasonable ones are resolved. For defensive edge cases, you shouldn't fix them by default. And then check whether its real trigger, only fix one that will actually happen. To avoid wasting too much effort on hypothetical damage scenarios, you can explain that such situations are practically impossible.
- If you found all of them are completely bullshit, you can treat your work as done, and get into the next part.

There are some cases where you are strictly forbidden to modify the code

- Requires adding mechanisms for ownership, rollback, transactions, repair, or cross-version compatibility
- The fix results in a net increase in code significantly or significantly offsets the code reduction achieved by the original refactoring (If it is a refactor)
- The new finding is a side effect of a fix from the previous review
- The behavior falls under follow-up functionality explicitly deferred in the PR description
- If a review suggestion conflicts with a breaking change, the suggestion should be rejected with an explanation; do not restore compatibility behaviors that were intentionally removed.

You should avoid too many review turns. The bigger the number of turns is, the less trustable the review suggestions are. You can maintain a score system in your own side to control this. Every cost should be made to grow at a quadratic rate.

Most of the time, the third turn is wished to be the last one. (This marks a threshold; beyond this stage, any suggestions should be treated with caution)

You should prevent turns more than 8.

If the PR is exceptionally large, the figures here may be multiplied, but this applies only to large PRs.

## How to divide the work and delegate to subagents

You should handle the whole process, and delegate work to subagents for detailed tasks. If your working environment doesn't support subagents feature, ignore this paragraph.

What should be done on your side:

- Analyze the PR's direction, and don't forget the PR's goal
- Analyze user's specific prompt and do the decisions
- Handle the timer
- Summon and manage subagents

What should be done to subagents (one item means one subagent):

- Triage whether this is a valid review suggestion (include leaving comments for rejected ones)
- Fix a set of valid review suggestions (including commit, comment)
- Finish `Work after the loop` and users' specific work unless user required not to use subagents

For the `triage` and `determine` step, you should create multiple in parallel. You are not allowed to pre-triage. You should prompt subagents and let them only return `yes` or `not`, instead of returning detailed reason. Get into the next step after all subagents return.

For the `fix` step, you are expected to create only one agent for one review run. You are not allowed to tell subagents the thought or other things to fix this bug, you should only tell the agents about the changes' purpose and the content or link of valid review suggestions. And let subagents explain the exact implementation detail in the GitHub comments rather than response or subagent response. You should only know if all of them got ready. In this part, subagents themselves are allowed to create nested subagents, if the works are independent and won't cause conflict.

## Work after the loop

After you think you've done the work (like got the thumb up, or find they are all invalid), do a round of simplify. Then, review the accumulated diffs, remove unnecessary patches, and avoid introducing new behaviors.

## What you should learn before

Be clear: your goal is not to resolve all review suggestions.

What is your true goal: protect the PR's boundary, protect the PR's goal.

Do not accept Codex review comments by default. A review comment is a hypothesis to be verified, not an acceptance criterion.
