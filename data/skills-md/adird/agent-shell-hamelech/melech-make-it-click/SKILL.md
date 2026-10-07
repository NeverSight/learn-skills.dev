---
name: melech-make-it-click
description: Recover when the agent's explanation did not land by finding the smallest thing blocking understanding and replacing the failed mental model with a concrete one.
disable-model-invocation: true
---

# Make It Click

The user invoked this because your previous explanation was smart, dense, or
technically correct, but they still do not understand it.

Do not defend, summarize, or merely shorten that explanation. **Find the
smallest thing preventing the user from understanding. Explain that first using
the most concrete route available. Do not simplify the entire previous answer;
replace its failed mental model.**

## Recover the thread

Use the conversation, especially the user's latest wording, to infer the exact
sticking point. Often it is much smaller than the topic:

- "Are we dropping the remaining data?"
- "Where does this value exist while the program runs?"
- "Why does this extra identifier exist at all?"

Answer that question first, even if the previous answer covered ten other
things. If the user's confusion is visible from context, do not ask them to
identify it again. If two or more sticking points are equally plausible, ask
one narrow question that distinguishes them instead of guessing.

## Change the route

The previous route already failed. Choose a different one:

- walk one concrete input through the system;
- show a tiny value or code example;
- state the before/after in plain language;
- use an analogy only when it maps cleanly;
- remove an unnecessary concept if complexity—not wording—is the problem.

Prefer real nouns and actions over category names. Introduce one idea at a time.
Define unavoidable jargon at the moment it appears.

## Response shape

1. Lead with the direct answer to the likely sticking point.
2. Build the smallest concrete model that makes that answer true.
3. Reconnect it to the original topic in one sentence.
4. Stop. Offer deeper detail only after the core idea has landed.

There is no mandatory analogy, numbered walkthrough, or ELI5 voice. Match the
route to the confusion. The outcome is understanding, not a particular format.

## Hard boundaries

- Do not repeat the same explanation with shorter words.
- Do not restart the whole topic from first principles unless that is the gap.
- Do not preserve jargon just because it is precise.
- Do not dump every caveat, branch, implementation detail, or adjacent concept.
- Do not speak to the user like a child or announce that you are "dumbing it down."
- Do not turn the recovery into another essay.
- Do not ask "does that make sense?" before giving the new explanation.

For grounded examples of three different recovery routes, see
[`references/examples.md`](references/examples.md).
