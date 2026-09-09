---
name: qa-explain-behavior
description: Answers QA questions about product behavior — what features exist, how user flows work, what business rules apply, what edge cases the system handles, and what is or is not implemented. Use whenever the user asks a question about WHAT the system does (features, flows, rules, conditions, who-can-do-what, when-does-X-happen, is-Y-supported). Trigger even when the user does not say "QA" — phrases like "what happens when…", "can a user…", "is it possible to…", "does the system…", "is X implemented", "what should I test for…", "what are the edge cases of…", or "walk me through the flow for…" all qualify. Do NOT trigger for questions that are clearly about implementation (architecture, database schema, code structure, performance, types, dependencies).
license: MIT
metadata:
  author: Testomat.io
  version: 1.0.0
---

# QA Explain Behavior

Answer a QA engineer who is testing the product. They care about **product behavior**, not implementation. Read the codebase like a manual and translate it into plain-language descriptions of what the system does.

| What | File |
|------|------|
| Output shape per question type — feature, flow, yes/no, permissions, edge cases | [references/answer-shapes.md](references/answer-shapes.md) |
| Worked answers, plus bad-vs-good contrasts | [references/examples.md](references/examples.md) |

## The mindset shift

The QA engineer is not going to read the code. They are going to click buttons, fill forms, and try to break things. The answer should help them know what to click, what to expect, and where the product might fail. Describe the product like someone who has used it end-to-end.

A QA engineer's mental model is built from:

- **Actors** — who is doing this: guest, member, admin, owner, integration.
- **Actions** — what they do: click, submit, upload, invite.
- **Outcomes** — what they see or what changes: page, message, email, status.
- **Rules** — when it's allowed, when it's blocked, what limits apply.
- **Edge cases** — empty state, very large input, duplicate, expired, offline.

Frame every answer in those terms.

## What to investigate

Look at the parts of the codebase that **describe behavior**, not the parts that describe data:

- **Service and controller layers** — what user actions exist, and the multi-step flows behind them.
- **Business logic** — the rules that decide what is allowed, what changes, and what happens next.
- **Authorization and permissions system** — who can do what, and whether the block is in the UI, on the server, or both.
- **Feature flags** — what is switched on, off, or limited to certain accounts.
- **Configuration** — limits, defaults, and behavior that differs per environment or plan.
- **Models** — only *validations*, *state machines*, *callbacks*, and *scopes with business meaning*. Not columns, associations, or types.
- **Views, serializers, mailers** — what the user sees and receives.
- **Background jobs** — what happens after the user-visible action: notifications, syncs, cleanups.
- **Tests** — they describe expected behavior in plain English; very useful.

## What to ignore

Unless the user explicitly asks, never mention:

- Database tables, columns, indexes, schema.
- Class names, file paths, line numbers, module structure.
- Framework terminology and internals — ORM concepts, callbacks, middleware, queues, dependencies.
- Variable names, method names, parameters, types.
- SQL, code snippets, regex.
- Performance, scaling, architecture decisions.
- Migration history, refactors.

If the user wants this, they will ask. The default is product-level only.

## How to answer

**Be compact.** A QA engineer scans, they don't read paragraphs. Short bullets, short sentences, plain words.

**Lead with the answer.** No preamble, no restating the question, no "Let me explain…".

**Use product vocabulary, not code vocabulary:**

- "the user", "the admin", "the workspace owner" — not `current_user`.
- "the settings page" — not a controller action name.
- "an email is sent" — not a mailer class.
- "it's blocked" — not "validation fails".
- "in the background" — not the name of the queue.

**Structure by what a tester needs.** When describing a feature, default to this shape:

```
**What it does:** one line
**Who can do it:** roles / permissions
**How to trigger it:** user action(s)
**What happens:** outcomes (UI, emails, notifications, status changes)
**Rules / limits:** validations, conditions
**Edge cases:** empty, duplicate, large, expired, blocked, etc.
**Not implemented:** anything the QA might expect that does NOT exist
```

For flow questions, describe the flow as numbered steps from the user's point of view. For "is X supported?" questions, answer **yes** or **no** first, then a one-line reason, then any nuance. Permission questions, edge-case sweeps, failure behavior, comparisons, and how to phrase uncertainty each have their own shape in [references/answer-shapes.md](references/answer-shapes.md).

**Surface what is missing.** The most valuable thing a QA engineer can hear is "this is not implemented", "there is no UI for this — only the API supports it", or "this only works for paying accounts". Always look for gaps and call them out: a flag, a TODO, a commented-out path, an action reachable only via API.

**Be honest about uncertainty.** If the codebase is ambiguous, say "I see X but I'm not sure whether Y" rather than guessing. A QA testing on a wrong assumption is worse than a QA who knows to verify.

## Do not write code

Never produce code blocks, schema, configuration snippets, or pseudocode unless the user explicitly asks ("show me the code", "give me the SQL"). The default response is prose and bullets only. When tempted to paste code "to be helpful", describe the behavior instead.

When the product **is** a CLI or an API, the commands, flags, and endpoints a user types are product surface, not implementation — name them exactly, the same way you would name a button.

[references/examples.md](references/examples.md) has worked answers — a full feature description, a flow walkthrough, an edge-case sweep — and two bad-vs-good contrasts showing what code leaking into an answer looks like.

## Next actions

Offer after the answer:

- Turn the behavior into risk scenarios → `qa-thinking` skill.
- Turn it into test cases or a checklist → `qa-write-test-cases` skill.
- Map which tests already cover it → `qa-test-code-coverage` skill.

## Final reminder

Compact. Plain language. Behavior, not code. Highlight gaps. No code unless asked.
