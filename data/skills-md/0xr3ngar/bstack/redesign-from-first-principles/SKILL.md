---
name: redesign-from-first-principles
description: "Apply when a new requirement meets an existing design, and for every refactor."
disable-model-invocation: true
license: MIT
compatibility: "No tools needed."
---

# Redesign-from-first-principles

Do not bolt the change onto what exists. Design as if the requirement had been there from the first day.

- Read every affected part and say what the current design is for.
- Ask: if we wrote this from scratch today, with this requirement, what would we build? Existing tickets, stacks and code are inputs. They are not limits.
- Prefer deleting to simplifying, simplifying to optimizing, and optimizing to automating. A refactor removes more than it adds. If it grows the code, name what the growth buys, or stop.
- Never rebuild the old design under new names. Spend no work on code that the redesign deletes.
- Move every caller to the new shape and delete the old path in the same change. No shims, and no old and new paths side by side.
- Carry the change through every reference: types, tests, documents, examples, drawings.
- Think the whole redesign through. Then deliver it in steps that each work.

A reviewer uses the same question as a verdict: is this what one would build from scratch for its requirements, and is it carried through every reference?
