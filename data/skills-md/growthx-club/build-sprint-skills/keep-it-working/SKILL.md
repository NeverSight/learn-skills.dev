---
name: keep-it-working
description: Decide how much proof a piece of work needs — from just looking at it, to walking the flow, to writing a test, to writing the test first. Use right after a feature works, before changing code that already works, and every time something that used to work breaks. Also use when the builder asks whether they need tests, or when a change touches money, auth, permissions, data they can't get back, or logic with rules and edge cases.
---

# Keep it working

The goal is not tests. The goal is that the thing they got working today still works on demo day, after forty more changes and an agent that doesn't know what it isn't supposed to touch.

So the question after every feature is never "should I write tests." It's **would we notice if this broke, and how bad is it if we don't.** Answer those two and the level picks itself.

## The ladder

Pick the cheapest rung that actually catches the failure. Climbing higher than the risk deserves is how a two-week sprint turns into a testing project.

| Rung | Use when | What you do |
|---|---|---|
| **1. Look at it** | The failure would be obvious on sight — layout, copy, colour, spacing | Open the page. Look. Done. No test earns its keep here |
| **2. Walk the path** | Multi-step flow you can still click through — sign up → create → see it listed | Drive the running app once, end to end, and report what you saw. No setup, no files. See `playwright` |
| **3. Write one test** | Breaking it would be silent, or checking by hand takes more than a minute — background jobs, webhooks, anything with a database round trip | One test for the happy path. Not a suite. For whole flows, `playwright` |
| **4. Test first** | You can state the rule before the code exists, or you're fixing a bug you can reproduce | Write the failing test, watch it fail, then make it pass |

## When test-first actually pays

Not a principle, a calculation. Write the test first when:

- **You can say the rule as a sentence with inputs and outputs.** "Orders over ₹2000 ship free, except international." Pricing, scoring, quotas, limits, permissions, date maths. The sentence *is* the test, so writing it first costs almost nothing and pins the rule down before the code wanders off.
- **The bug is reproducible.** Always. A bug you can trigger is a test you can write in a minute, and it's the only way to know the fix worked and stays working. This is the single highest-value test in any sprint project.
- **Many branches.** Empty, one, many, too many, wrong type, expired, already used. If you'd otherwise check five cases by clicking, checking them in code is faster on the second run.
- **You'll change it repeatedly.** Anything you already rewrote once will be rewritten again.

Don't write the test first when:

- **It's how something looks.** Tests can't see. Use rung 1 or 2.
- **You don't know what correct is yet.** Explore, get it working, *then* pin it down with a test if it earned one. Exploration first is fine — just don't keep the exploration and call it done.
- **It's a one-off** — a migration you'll run once, a script that seeds fake data, a prototype you've already agreed to throw away.

## The rule that isn't negotiable

**Anything that broke once gets a test.** No judgment call, no ladder. It broke, so it can break again, and now you know exactly how to trigger it.

This is what stops the sprint's worst pattern: fix something on Tuesday, agent quietly re-breaks it on Thursday, nobody notices until the demo.

## Don't build a test setup before it's earned

The sprint stack ships without a test runner, and that's correct — most work lands on rungs 1 and 2.

The first time a change genuinely lands on rung 3 or 4, install the smallest possible runner and write that one test. Not a config, not a suite, not coverage. If setting it up is going to take more than a few minutes of their sprint, say so and offer rung 2 instead — then let them choose.

## Once tests exist

- Run them after every change, not just the change that touched them.
- Red suite? Stop. Fix it before adding anything new. Building on a red suite is how an afternoon disappears.
- Report every failure by name, including ones you didn't cause. A red test that scrolled past unmentioned is a lie by omission.
- Keep them honest: the name says the behaviour, the assertion is on real behaviour and not on a mock, one behaviour per test. A test that can't fail is worse than no test, because it buys false confidence.

## How to talk about this

Never "you should have written tests." They're learning to ship, and the ladder exists so they don't have to carry that guilt.

Say what's worth protecting and what it costs: *"the pricing rule is the kind of thing that breaks quietly — two minutes to lock it down, want me to?"* Then respect the answer. If they say no, note it and move on; `checkpoint` is still underneath them either way.

When a test catches a regression, say so out loud. That's the moment the idea sells itself.

---

Ours. The red-green discipline and the test-honesty rules are adapted from [obra/superpowers](https://github.com/obra/superpowers), MIT License — the ladder and the "when does this pay" triage are ours, because sprint builders need to ship first and prove second.
