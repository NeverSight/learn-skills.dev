---
name: reflect
description: >-
  After an implementation effort, re-read the new code, reflect, and improve it.
  Apply non-product simplifications and improvements immediately; 
  Report silent product decisions and unclear forks. Use when the user requests reflection,
  re-read, a second pass.
disable-model-invocation: false
---

# Reflect

The first implementation is a draft. Now that the code exists, review and re-think whether it was done in the best way. Ask questions of the code and context. Act on improvements that do not depend on a product decision. Raise the rest.

Goal: a higher-quality first pass before the user looks in detail. This is not a code review. Formal review comes later.

"Best" means:
- Simplest solution that solves the problem
- The domain model is clearly expressed
- Coherent and consistent with the existing codebase
- Re-uses existing objects, helpers, conventions when appropriate
- Isn't contorted around existing code that wasn't built with the new requirements in mind
- Comments explain the intent and rationale for the code
- Raises the average quality of the codebase, sets examples that others can follow
- The right long-term architecture, not the smallest change

## When to use

- The user says reflect, look again, second pass, shape this
- Implicitly, after finishing a first implementation, including incremental changes to a WIP
- Do not use during planning, while waiting on a design question, or as a substitute for a formal review

## Workflow

### 1. See the code

Re-read the change as if seeing it for the first time. Read the new/changed files and the surrounding modules they plug into. The goal is a high quality final shape, not the smallest diff.

### 2. Hunt and apply

Work through the questions below. For each realization that does **not** depend on a product decision: do it. Do not ask permission to improve the code just written.

Leave it for the report when:

- A requirement would be relaxed, changed, or dropped
- Two product-valid paths exist and it is not obvious which is better
- A product decision was taken silently during the build
- A significant refactor to existing code is called for

### 3. Repeat

Fresh problems and opportunities will appear with each iteration. 
Repeat the reflection and improvement process until it stabilizes, or you reach only product or design decisions that require the user's input.

### 4. Report

Brief. What changed. Then leftover observations and decisions, numbered.

Wait for the user to respond.

## Questions

Mostly, use your own judgement. 

Now that you can see the code: was this the simplest and best way to address the need? Can it be simpler or more obvious?

Ask these of what you've just written:

- Which requirements drove the complexity? Were any requirements interpreted too strictly? Which requirements were implicit? Challenge the user about them.
- Now that you see the code, can it be rearranged to be more coherent?
- What opportunities for simplification or improvement have emerged?
- Are core concepts expressed just once, in a re-usable way?
- Is anything awkward or surprising? Why?
- Is the new code working around deficiencies in the codebase? Is there a straightforward fix?
- What coupling emerged or was discovered? Is it justified?
- Does this belong here, or should it pass through and live closer to where it's used?
- Am I backing out or introspecting something that should have been constructed and passed through?
- Can similar paths or structures be fruitfully unified?
- Are there two different ways to do the same thing? Just pick one.
- Is each piece of code in the right place?
- Do we need this? Is it doing anything?
- Are optional things truly optional?
- What code smells are present?
- Are names still appropriate, describing the now-current concepts?
- What's the right architecture for this overall problem?
- Would I actually build it this way if starting over?
- Is this a hack?

## Silent product decisions

Report these even when the code is fine. The user did not confirm them.

- One of two user-visible behaviors was chosen
- An application rule was encoded
- A gate, cap, empty state, or copy path was invented
- A default was picked that the user might want to see

## Do not

- Silently drop or loosen a requirement
- Invent a base class or a prospective second caller
- Rename a landed API field
- Keep a workaround
- Treat this as review-diff or a commit gate
