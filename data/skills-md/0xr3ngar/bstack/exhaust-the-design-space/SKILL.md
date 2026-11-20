---
name: exhaust-the-design-space
description: "Apply before you commit to a design that has no precedent in the codebase, or when the first idea came too fast: an interface, a data model, a UI interaction, an architecture."
disable-model-invocation: true
license: MIT
compatibility: "No tools needed."
---

# Exhaust-the-design-space

The first design that works is seldom the best one. Put two or three real alternatives side by side before you commit.

- Always include the options that add nothing: use what the platform or a library already gives, reuse a part that exists, or remove the need.
- Make each option concrete enough to compare: the caller's code, the stored shape, a rendered mock. Two options that differ only in wording are one option.
- Compare them in one table: what the user writes or sees, what it costs to build, what it deletes, what it makes hard later.
- Choose one and give the real reason. Do not invent a weakness for the others.
- Settle it with a run when a run can settle it. A prototype or a probe is better than an argument.

Where the feel decides, as in a UI, build the candidates as throwaway pages and look at them.
