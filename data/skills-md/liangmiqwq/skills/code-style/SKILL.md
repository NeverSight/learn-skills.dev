---
name: code-style
description: You are required to load this before writing code. Do not use this skill for reading code or analyzing tasks unless users require to care about codestyle.
---

Load $precise-minor-adjustment skill as needed, it is used to tell agents how to make code simple and consistent with other parts in codebase.

After you finish your task, also run a round of simplify according to $precise-minor-adjustment before commit or summarizing.

# Code Style

Read the corresponding file below as needed:

| Language                | Reference            |
| ----------------------- | -------------------- |
| JavaScript / TypeScript | `languages/js-ts.md` |
| Rust                    | `languages/rust.md`  |

The most important rule of my code style is always to find the regular patterns emerging from irregular logic. You can change the way you organize the code, and use comment to achieve this goal.

## Organize

One goal to achieve when coding is to make the code more structured and predictable. That will make humans easy to control and review your code.

For example, you can use a big `match`(Rust), and handle different branches for different cases with simple lines.

A thousand lines of structured, predictable, regular code is better than five hundred lines of messy code.

## Comments

**Comments are necessary for complex logic.** Do not wrap a sentence's comment into multiple lines unless the linter / checker requires.

We should keep comments simple and short. If the next reader can infer it from the code in three seconds, the comment is unnecessary.

Keep comments that capture what the code cannot express on its own:

- A non-obvious constraint or external requirement
- Why a seemingly better approach was rejected
- Context that only exists outside the codebase (a spec, a quirk of an upstream service, a compliance rule)

And the comments there should explain why, not what.

Never write a doc comment that only restates the function name — it adds nothing and will drift out of sync.

---

Another acceptable form of annotation is a flow comment for complex functions. For a part of complex, multiple phases logic, we can add comments like `// 1. Check environment` `// 2. Read config` to help human divide code into different parts.

If a piece of logic can be clearly divided into multiple stages and exceeds 50 lines, then it needs flow comments.

---

After finishing your whole implementation, check the code diff, if the diff is more than 50 lines while there are no comments added, there are problems.

## Visibility

**Start with nothing visible. Add visibility only when another module needs it.**

Every export or public item is a contract: a name that must stay stable, a surface that must stay compatible. Keep that surface as small as possible.

## Diagnostics Handling

In my project, I have a set of strict linting rules. It's normal to meet the diagnostics.

When meeting diagnostics, the first thing you do is to think, not to change the code. You should check whether the diagnostic's purpose fit the current code's purpose and behavior target. You should check whether following diagnostic will make the code more complex, more confusing or more simple.

You should reject some unreasonable diagnostics, and keep the reasonable ones. Follow the code style.

When you are rejecting an unreasonable diagnostics, prefer use comment (`// oxlint-disable-...`, `#[allow(...)]`) to disable it, instead of disabling it globally and modifying config files. You can also check the codebase to know whether there is other cases disable the same rules, if a rule is disabled too many time, you can suggest me to adjust config file in the response. But do not modify them urself unless I required.

## After writing

After finishing the goal, you need to review your own code. Especially focus on the code organization.
