---
name: prototype
description: Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like.
metadata:
  credits:
    - skill: prototype
      author: Matt Pocock
      url: "https://github.com/mattpocock/skills/blob/main/skills/engineering/prototype/SKILL.md"
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Pick a branch

Identify which question is being answered, using the user's prompt, the surrounding code, or by asking if the user is around:

- **"Does this logic / state model feel right?"** → [LOGIC.md](LOGIC.md). Build a single shareable HTML file (free-play buttons plus tabbed guided walkthroughs) that pushes the state machine through cases that are hard to reason about on paper, and that a non-developer can drive.
- **"What should this look like?"** → [UI.md](UI.md). Generate several radically different UI variations, built from the components and layouts the app already uses, on a single route, switchable via a URL search param and a floating bottom bar.
- **"How should this sound or move?"** (video, audio, motion) → render each variant and put them all on one shareable HTML comparison page. Change one thing per variant where you can, and state exactly what differs between them.

The two branches produce very different artifacts, so getting this wrong wastes the whole prototype. If the question is genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (a backend module → logic; a page or component → UI) and state the assumption at the top of the prototype.

## Rules that apply to both

1. **Throwaway from day one, and clearly marked as such.** Locate the prototype code close to where it will actually be used (next to the module or page it's prototyping for) so context is obvious, but name it so a casual reader can see it's a prototype, not production. For throwaway UI routes, obey whatever routing convention the project already uses; don't invent a new top-level structure.
2. **Trivial to run.** A UI prototype starts from one command in the project's task runner: `pnpm <name>`, `python <path>`, `bun <path>`, etc. A logic demo is a single HTML file the user double-clicks. Either way, no thinking required to start it.
3. **No persistence by default.** State lives in memory. Persistence is the thing the prototype is _checking_, not something it should depend on. Seeding the local dev database so a UI prototype has data to render is fine (see [UI.md](UI.md)). If the question explicitly involves a database, hit a scratch DB or a local file with a clear "PROTOTYPE, wipe me" name.
4. **Skip the polish.** No tests, no error handling beyond what makes the prototype _runnable_, no abstractions. The point is to learn something fast.
5. **Surface the state.** After every action (logic) or on every variant switch (UI), print or render the full relevant state so the user can see what changed.
6. **Hand it over so it actually opens.** Any form works (an HTML file, a running route, screenshots), as long as the user can see it from where they are. Before handing it over, check that it works from the user's side, not just yours: a `localhost` URL or a path on your machine points at nothing on theirs. Prefer something they can click through over still images. If the host can render HTML in the chat (T3 Code's `html_render`), show the prototype there and also give the file or open it for them. Screenshots in the chat are the fallback when nothing interactive reaches them; embed them so they render (in T3 Code, as data URIs in an `html_render` page, not as file paths). Put the prototype and the question about it in the **last message of your turn**: anything you post after it (a follow-up, a reply to a stop hook) pushes it into the collapsed work log. Ask in the message text, never in a question dialog that covers it.
7. **Capture it when done.** Fold any validated decision into the real code, unless the prototype serves a planning map (wayfinder), where the decision only gets recorded. Then capture the prototype itself as a **primary source**: commit it to a throwaway `prototype/<slug>` branch, out of main, and push it (`[skip ci]` in the commit message: it never merges, so CI does not apply), and leave a context pointer to that branch on the implementation issue. Capture the answer too (the verdict and the question it settled) in the issue or a commit. The main branch keeps only the validated decision.
