---
name: ookami-code-review
description: >
  ookami team code review guidelines. Use this skill whenever reviewing pull
  requests, giving or receiving PR feedback, writing review comments, approving
  or requesting changes on a PR, preparing code for review, or discussing code
  review etiquette. Also use when the user asks about how to phrase review
  comments, how to respond to feedback, or best practices for code reviews.
---

# Code Review Guide

Follow these guidelines when reviewing code or having your code reviewed.
Full reference: https://github.com/ookamiinc/guides/blob/master/code_review.md

## General Etiquette (Everyone)

- Accept that many programming decisions are opinions. Discuss tradeoffs, state your preference, and reach a resolution quickly.
- Ask questions instead of making demands. ("What do you think about naming this `:user_id`?")
- Ask for clarification when something is unclear. ("I didn't understand. Can you clarify?")
- Avoid selective ownership of code ("mine", "not mine", "yours").
- Avoid terms that refer to personal traits ("dumb", "stupid"). Assume everyone is attractive, intelligent, and well-meaning.
- Be explicit. People don't always understand intentions online.
- Be humble. ("I'm not sure - let's look it up.")
- Don't use hyperbole ("always", "never", "endlessly", "nothing").
- Don't use sarcasm.
- If too many "I didn't understand" or "Alternative solution:" comments arise, move to a synchronous conversation. Post a follow-up comment summarizing the offline discussion.

## When Having Your Code Reviewed

- Be grateful for suggestions. ("Good call. I'll make that change.")
- Don't take feedback personally — the review is of the code, not you.
- Explain why the code exists. ("It's like that because of these reasons. Would it be more clear if I rename this class/file/method/variable?")
- Extract unrelated changes and refactorings into future tickets/stories.
- Link to the code review from the ticket/story.
- Push feedback-based changes as isolated commits (do not squash until ready to merge) so reviewers can read individual updates.
- Try to respond to every comment.
- Wait for CI to pass before merging.
- Merge once you feel confident in the code and its impact on the project.

## When Reviewing Code

- Understand why the code is necessary (bug fix, UX improvement, refactoring) before reviewing.
- Communicate which ideas you feel strongly about and which you don't.
- Identify ways to simplify the code while still solving the problem.
- If discussion becomes too philosophical, move it offline. Let the author make the final decision on alternative implementations.
- Offer alternative implementations, but assume the author already considered them. ("What do you think about using a custom validator here?")
- Seek to understand the author's perspective.
- Sign off on the pull request with a thumbs-up or "Ready to merge" comment.

## Style Comments

- When a style guideline is missed, comment with a reference to the guideline.
- If you disagree with a guideline, open an issue rather than debating it in the code review. Apply the guideline in the meantime.
