---
name: prototype
description: Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like.
license: MIT
metadata:
  author: "Sascha Grau"
  version: "1.0.0"
  category: "engineering"
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Pick a branch

Identify which question is being answered — from the user's prompt, the surrounding code, or by asking if the user is around:

- **"Does this logic / state model feel right?"** → [LOGIC.md](references/LOGIC.md). Build a single shareable HTML file — free-play buttons plus tabbed guided walkthroughs — that pushes the state machine through cases that are hard to reason about on paper, and that a non-developer can drive.
- **"What should this look like?"** → [UI.md](references/UI.md). Generate several radically different UI variations on a single route, switchable via a URL search param and a floating bottom bar.

The two branches produce very different artifacts — getting this wrong wastes the whole prototype. If the question is genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (a backend module → logic; a page or component → UI) and state the assumption at the top of the prototype.

## Rules that apply to both

1. **Mark the shell as throwaway from day one.** Locate prototype code close to where it will be used so context is obvious, and name it so a casual reader can identify it as a prototype. For UI routes, follow the project's routing convention.
2. **Make it trivial to run.** A UI prototype starts from one command in the project's task runner — `pnpm <name>`, `python <path>`, `bun <path>`, etc. A logic demo is a single HTML file the user opens directly. Starting it requires no project-specific discovery.
3. **Keep state local by default.** Use in-memory state. When persistence is the question, use a clearly named scratch database or local file that is safe to wipe.
4. **Keep the scope tight.** Write only the code needed to answer the question and make it runnable. A decision-rich reducer, state machine, schema, or type shape may inform production code later; integrate it under the target module's normal production standards rather than promoting the prototype implementation unchanged.
5. **Surface the state.** After every logic action or UI variant switch, render the full relevant state so the user can see what changed.
6. **Capture it when done.** Fold the validated decision into the real code, then preserve the executable prototype as a **primary source** on a throwaway branch outside main. Record the question, verdict, and branch reference on the implementation issue. If no issue exists, use the repository's normal planning artifact or the decision commit. Keep decision-rich excerpts in the relevant specification or ticket, marked as prototype-derived; keep the executable demo and incidental implementation detail in its primary source. Main retains only the validated decision.
