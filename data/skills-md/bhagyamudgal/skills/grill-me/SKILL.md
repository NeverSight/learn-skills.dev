---
name: grill-me
description: Grill the user on a plan one question at a time until every decision is settled, then check the plan's facts against the codebase. Use when the user says "grill me", "harden", "check" or "verify" a plan, or passes a plan file to be interrogated.
---

Interview me relentlessly about every aspect of this plan. Walk down each branch of the decision tree and settle dependencies between decisions one by one. I would rather get grilled now than rebuild later. Once the decisions are settled, check every factual claim in the plan against the real codebase before I code.

If I invoke you with a file path argument, read that file first and grill its contents as the plan. If the decisions are already settled and I ask only for verification, skip to the verification pass below.

## Rules

Always use the AskUserQuestion tool for every question you present to me. Every decision reaches me as a cursor-selectable option.

- Before the first question, enumerate the open decisions in the plan as a numbered list and print it.
- Ask decision zero first: is this approach even right. Offer one credible alternative drawn from the codebase or the issue, and grill it before the rest.
- Ask one question at a time. Make one AskUserQuestion call per turn, then wait for my answer.
- Give 2-4 options per question. Put your recommended answer first with "(Recommended)" in the label.
- Each option needs a clear `description` that explains the trade-off or implication, not just a label.
- State each question in plain words with one line of context, then give one concrete example before the options. Never ask a bare technical question.
- After each answer, acknowledge the choice in 1 sentence max, ending with `<n> of <total> resolved`, then ask the next question.
- If my answer is non-committal, something like "not sure" or "whatever you think" or "both", do not record it. Restate the trade-off in one sentence and re-ask the same decision once. Record the second answer either way.
- When an answer contradicts an earlier one or leaves a dependency unresolved, say which one and re-ask before moving on.
- If you can answer a question by exploring the codebase, explore it instead of asking me. Use Grep, Glob, Read, or Agent to verify assumptions before grilling me on them.
- If I say "enough" or "done" or "stop" or "skip the rest", append per the file rule and post per the issue rule below with the decisions captured so far, then announce "Grill complete." and exit.
- When every numbered decision has a recorded answer and no answer has opened a new one, move to the verification pass below instead of closing out. If an answer opens a new decision, append it to the list and say so.

## Verification pass

The decisions are settled. Now prove the plan is true before I code.

- List every factual claim in the plan: file paths, symbol names, numbers, commands, flags, CI job names.
- Check each claim yourself with Grep, Glob, Read, or Agent. Fix what you can verify without asking, and say what you changed in one line each.
- Ask about only what you cannot resolve on your own. Ask it exactly like a decision question: plain words, one line of context, one concrete example, 2-4 options with your recommended answer first.
- Never ask me to confirm a fact you could have checked. Never batch questions.
- If I invoked you with a file path, append the numbered decisions and the verified corrections under a `## Decisions` heading in that file before announcing "Grill complete."
- If a GitHub issue was provided in context as a URL, number, or issue body, post an issue comment for tracking before announcing "Grill complete." The body holds the numbered decisions and the verified corrections followed by the full plan, or whatever is captured so far on early exit. Comment on the exact issue from context with `gh issue comment <url> --body`. When context holds only a number, resolve its repository first instead of assuming the checkout.
- When every claim is verified or answered, announce "Grill complete." with the numbered decisions and the corrections.
