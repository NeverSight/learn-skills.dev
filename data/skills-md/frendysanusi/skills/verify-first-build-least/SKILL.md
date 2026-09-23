---
name: verify-first-build-least
description: >
  Ground a change in the real code before writing it, build the smallest thing
  that works, then fold what you wrote into what already exists. Use when
  implementing a feature, fix, or ticket in a codebase you do not fully know,
  and whenever the user says "verify first", "don't assume", "check the code
  first", "make it minimal", "what can we reuse", "is there an existing
  method", "yagni", "do less", or complains about bloat and unnecessary
  dependencies. Covers the ladder from standard library and native platform
  features before new dependencies, the evidence a claim needs before you make
  it, and what must never be simplified away.
---

# Verify first, build least

Most avoidable coding mistakes come from writing against an imagined codebase,
or from rewriting something that already exists in the real one. This loop
grounds the plan first, then keeps what gets built as small as the problem
allows.

Scale it to the task. The loop trades speed for caution, which a one-line fix
does not need.

## 1. Ground the plan in the real code

Replace every assumption the plan rests on with something you observed. You are
looking for the specific shapes and signatures your code will touch.

Read the ticket or request as the source of truth and pull out both the
acceptance criteria and the constraints. Separate what is buildable now from
what is blocked on something that does not exist yet, and say so early, because
that reshapes scope before you invest in the wrong half.

Search for the subsystem before designing: the models, the existing handlers,
the layer where similar logic already lives. That tells you where the change
belongs and what it can lean on.

Then open the real files and confirm what your code will touch:

- The exact data shape. Do not assume field names or nesting.
- The exact signature and direction of each function you will call. A check that
  computes `expected = f(x)` is not the same as one that corrects `x`.
- The existing behaviour you might duplicate or contradict.
- Where the code actually runs: write time or read time, per item or batch,
  inside a transaction or not. This often decides the whole approach.

For a bug, reproduce the reported behaviour before changing anything, then run
the same steps again afterwards. If you cannot reproduce it, report the missing
access, input, or environment rather than fixing blind.

When you catch yourself about to write code based on what a function is
probably called, stop and read it. State the facts you verified back to the user
in a line or two, so they can catch a wrong premise before it becomes a wrong
diff.

When verification turns up a genuine fork the user owns, present it with your
recommendation first. A fork with a conventional default needs no question, so
state the default you are taking and keep going.

Say what you assumed and what stayed unclear. When two readings of the request
are both plausible, put both to the user rather than quietly picking one. When a
simpler approach than the one requested would work, say so and give the reason,
even if the user named the harder one.

Before starting anything multi-step, write the plan as steps with a check
against each:

```
1. <step> -> verify: <check>
2. <step> -> verify: <check>
```

A criterion like "make it work" cannot tell you when to stop. "The invalid-input
tests pass" can.

## 2. Build the least that works

Climb this ladder and stop at the first rung that holds:

1. Does this need to exist at all? Speculative need, skip it and say so in one line.
2. Does it already exist here? A helper, type, or pattern a few files over is the most common thing to reinvent.
3. Does the standard library do it?
4. Does a native platform feature cover it? `<input type="date">` over a picker library, a database constraint over application code.
5. Does an already-installed dependency solve it? Never add a new one for what a few lines do.
6. Can it be one line?
7. Only then, the minimum code that works.

The ladder runs after you understand the problem, never instead of it. A small
change in the wrong place creates a second bug.

Build nothing speculative. One implementation needs no interface, one call site
needs no abstraction, and a value nobody changes needs no configuration option.
Error handling for a state the data cannot reach is speculation too. Add
flexibility when something asks for it. Before calling the work done, ask
whether an experienced engineer reading it would say it is overcomplicated.

Build one slice at a time, one acceptance criterion or one fix, rather than the
whole feature at once. Every changed line should trace to the task. Match the
surrounding style even where you would personally differ, leave untouched lines
unformatted, and mention pre-existing issues such as dead code rather than removing them. Clean up
only what your own change orphaned.

A bug report names a symptom. Grep every caller of the function you are about to
touch, because one guard in the shared function is both the smaller diff and the
real fix, while patching the path the ticket names leaves every sibling caller
broken.

When you cut a real corner on purpose, leave a marker naming the ceiling and the
way out, such as `# simplification: global lock, per-account locks if throughput
matters`.

## 3. Prove it

Use the repository's own setup, test, and lint commands. Find them. Never invent
a verification command.

Write the tests, then make them pass. Tests double as a clarity check, since a
task you cannot write a coherent test for usually has incoherent numbers in its
example. Keep the test data telling a real story.

Match the evidence to the claim. A screenshot shows appearance. An interaction
claim needs the sequence actually exercised. A performance claim needs
comparable measurements rather than an argument.

Run the tests, linter, formatter, and type checker, then read the output
honestly. Separate what your change introduced from what was already failing,
fix the first and note the second. If a tool flags a line you did not touch,
check it against the base branch before deciding it is not yours. When something
fails or you skip it, say so.

## 4. The reuse pass

This is the phase everyone skips, and first-draft code that works is rarely the
code worth keeping. Re-read your own diff with one question: does any of this
already exist?

For each helper, fetch, or coercion you wrote, search for a repository method
that already does the job. A query method that does your hand-rolled lookup. A
shared utility that already parses or formats it. A near-twin private method
that should be promoted and shared. Dead but correct code that only needs a
caller.

Prefer reusing it, even when that means a small refactor such as making a
private helper public, or pulling one shared function out of two near-duplicates.
The line count should usually fall here.

Check that reuse preserves behaviour. When you unify two near-duplicates,
confirm their semantics actually match, since one may treat `""` as `0` where
the other treats it as `None`, and keep the established one so existing callers
do not shift under you. Reuse that quietly changes behaviour is worse than
honest duplication.

Then ask whether the code can simply be less. Collapse defensive ladders the
data shape does not warrant, and fold a re-read into the value you already
computed. If the real problem is an untyped boundary, name that as the root
cause rather than papering over it at every call site.

Run the gates again. A reuse pass that breaks a test is not done.

## Never simplify away

Input validation at trust boundaries. Error handling that prevents data loss.
Security measures. Accessibility basics. Anything the user explicitly asked for.
When the user wants the full version, build it without re-arguing.

Never be lazy about understanding the problem, because the ladder only shortens
the solution and never the reading it rests on.

## After the work

Record the decisions the code and git history do not already carry: why the
scope landed where it did, which fork you took, which trade-off you accepted.
A memory, the pull request description, or a ticket comment all work.

When the same mistake keeps recurring, fix the environment that allows it, and
choose the smallest mechanism that does the job:

| The failure | The fix |
| --- | --- |
| An invalid state can be designed out | Change the architecture, API, or data model. |
| A bad pattern is mechanically detectable | Add or reuse a type, lint rule, or CI check. |
| It needs context and judgement | Write a short project rule or review criterion. |
| There is no repeatable procedure | Capture the workflow in a skill. |

Prefer the enforceable rows. A written rule is the weakest of the four, and a
check you have not watched reject the bad case is not yet verified.
