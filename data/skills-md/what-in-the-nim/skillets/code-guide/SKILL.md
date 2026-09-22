---
name: code-guide
description: Explain code, a diff, PR changes, a class, a module, or a package by building the simplest correct model, adding one edge case at a time, and ending at the current design.
---

# Code Guide

Use this method for a code walkthrough or design explanation.

## Method

1. Inspect the current source, tests, configuration, and relevant diff. Done when the relevant code paths are known.
2. State the core idea in one to three short sentences. Done when a new reader can name the main job.
3. Show the smallest useful public interface. Done when the main boundary is visible.
4. Add one real edge case at a time. Update the model after each case. Done when each relevant branch has an explanation.
5. Stop only when the current design, important paths, and relevant edge cases are clear. Done when the final model matches the source.

Each pass must contain:

- **Rule:** one simple statement of the behavior.
- **Interface:** a short code block that shows the boundary.
- **Edge case:** the new case that changes the model.
- **Reader meaning:** what the reader can now expect and why the rule matters.

Use an interface sketch when the code is complex. Use the project language when it helps. Use pseudocode when the language hides the idea.

Build the sketch in small steps. Start with one item:

```python
class Store:
    def save(self, item: Item) -> Receipt: ...
```

Then add the retry rule:

```python
class Store:
    def save(self, item: Item) -> Receipt: ...
    def find_receipt(self, item_id: str) -> Receipt | None: ...
```

In project code, use comments only for **WHY**. Do not use comments to restate **WHAT** the code does.

## Reader view

Write from the reader's point of view. Imagine that they see the code for the first time.

Start each pass with the question the reader may have:

- What does this do?
- What happens next?
- Why is this extra rule needed?
- What can I rely on?

Answer with direct sentences:

- When you call this, it does that.
- If this case occurs, the code does this.
- This extra rule protects this behavior.

Explain user-visible effects before internal names. Connect each new branch to its effect on input, output, state, errors, or timing.

## Choose the view

For a class, module, or package, explain in this order:

1. Public boundary.
2. Main data or control flow.
3. Collaborators and ownership.
4. Invariants and lifecycle rules.
5. Failure paths and edge cases.

For a diff or PR, explain in this order:

1. Behavior before the change.
2. Behavior after the change.
3. The changed path and its boundary.
4. The edge case that caused each extra branch.
5. Tests, risks, and remaining unknowns.

Do not describe intent as fact. Mark it as an assumption when the source does not prove it. Prefer observed behavior from code and tests.

## Final design

End with a compact final model:

- Core idea.
- Public interface or changed boundary.
- Main flow.
- Invariants.
- Edge-case behavior.
- What the reader can rely on and any open question.

Keep iterating until this model matches the current source. Do not invent a cleaner design. Describe a proposed design separately from the current design.

## Language

Use simple English based on ASD-STE100:

- Use short sentences and active voice.
- Use one term for one concept.
- Use concrete verbs.
- Explain an acronym at first use.
- Remove filler, idioms, vague claims, and repeated points.
- Keep examples short and interface-focused.
