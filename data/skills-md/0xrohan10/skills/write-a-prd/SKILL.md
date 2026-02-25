---
name: write-a-prd
description: Use this skill when writing a PRD for a feature.
---

This skill will be invoked when the user wants to create a PRD. You should go through the steps below. You may skip steps if you don't consider them necessary.

1. Ask the user for a long, detailed description of the problem they want to solve and any potential ideas for solutions. Focus on understanding the **situation** that triggers the need — what is happening when the user feels the pain? What are they trying to accomplish? What does success look like?

2. Explore the repo to verify their assertions and understand the current state of the codebase.

3. Ask whether they have considered other options, and present other options to them.

4. Interview the user about the implementation. Be extremely detailed and thorough. For each capability, clarify the triggering situation, the user's underlying motivation, and the desired outcome.

5. Hammer out the exact scope of the implementation. Work out what you plan to build and what you DON'T plan to build as part of this PRD.

6. Sketch out the major modules you will need to build or modify to complete the implementation. Actively look for opportunities to extract deep modules that can be tested in isolation.

A deep module (as opposed to a shallow module) is one which encapsulates a lot of functionality in a simple, testable interface which rarely changes.

Check with the user that these modules match their expectations. Check with the user which modules they want tests written for.

7. Once you have a complete understanding of the problem and solution, use the template below to write the PRD. The PRD should be submitted as a GitHub issue.

<prd-template>

## Problem Statement

The problem that the user is facing, from the user's perspective. Describe the situation(s) in which this problem arises and why existing solutions are inadequate.

## Solution

The solution to the problem, from the user's perspective.

## Job Stories

A LONG, numbered list of job stories. Each job story should be in the format of:

1. When [situation/trigger], I want to [motivation/action], so I can [expected outcome]

<job-story-example>
1. When I'm about to make a purchase and I'm unsure if I can afford it, I want to see my current account balance, so I can decide whether to proceed without risking an overdraft.
2. When I notice an unexpected drop in my balance, I want to quickly see recent transactions, so I can identify whether it's a legitimate charge or something I need to dispute.
</job-story-example>

Note the difference from user stories: job stories are **situation-driven**, not role-driven. They describe the context that creates the need, the motivation behind the action, and the concrete outcome the user expects. This grounds each requirement in a real scenario rather than an abstract persona.

This list of job stories should be extremely extensive and cover all situations a user may encounter when interacting with the feature, including edge cases, error states, and first-time vs. repeated use.

## 'Polishing' Requirements

Once the job stories are complete, we will end up with a working, but not refined, feature or application. After the work is complete, we should enter a polishing phase.

This should be a list of checks that we want to make at the end of the work to polish and refine the work done for maximum user enjoyment and experience.

They should not meaningfully extend the work but instead ensure harmony of all created elements and ensure any errors are properly handled and make things delightful and beautiful.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this PRD.

## Further Notes

Any further notes about the feature.

</prd-template>
