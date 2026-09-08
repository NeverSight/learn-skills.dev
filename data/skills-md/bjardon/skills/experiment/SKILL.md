---
name: experiment
description: Bootstrap a Personal Experiment and build its first user-visible outcome with disposable code and minimal process.
disable-model-invocation: true
---

# Experiment

Establish a Personal Experiment's durable operating mode, then build the requested first outcome quickly. Treat the implementation as disposable and delegate engineering choices to the agent.

## Confirm the mode

Use this one-time bootstrap workflow only when the user identifies the project as a Personal Experiment or clearly asks for disposable, vibe-coded work. Project size and commercial potential do not determine the mode.

If intent is ambiguous, ask whether the user wants a personal experiment or a professional project. Do not silently downgrade professional work into an experiment.

A Personal Experiment requires both:

- A repository under the creator's personal GitHub account.
- A devlog page in the Notion experiments wiki.

Require the user to provide the devlog page as part of the initial request. Read it through an available Notion integration before building so its framing informs the work. If the page is missing or inaccessible, ask for a usable page; do not create or discover one on the user's behalf.

After bootstrap, future agents continue the experiment through its `AGENTS.md`; they do not need to invoke this skill again.

## Build for the outcome

- Start from the user's desired outcome and implement immediately.
- Make reasonable product, stack, architecture, and implementation choices without design ceremony.
- Prefer the shortest path to a working result over maintainability, extensibility, abstraction, or polish beneath the requested surface.
- Ask only when missing information blocks the outcome or a choice carries meaningful cost, safety, privacy, or external-system consequences.
- Verify the user-visible behavior in proportion to the experiment. Do not introduce a professional test strategy unless requested.

## Establish minimal artifacts

Create a minimal `AGENTS.md`, a short `README.md`, and a concise `TODO.md`. Preserve useful existing content when any of them already exist.

### AGENTS.md

Use `AGENTS.md` to preserve the Personal Experiment operating mode across future agent runs. Keep it short and include:

- That the repository is a Personal Experiment built outcome-first with disposable code and minimal process.
- Pointers to `README.md` for purpose and run instructions, `TODO.md` for build status, and the supplied Notion devlog for durable decisions, learnings, and dead ends.
- Project-specific build, run, or user-visible verification instructions discovered while producing the first outcome.
- Essential guardrails relevant to the experiment.
- The wrap-up rules below.

Encode these wrap-up rules without prescribing a particular integration mechanism:

- Implement and verify freely, but ship only after the user explicitly signals acceptance or asks to wrap up.
- Before shipping, verify the accepted user-visible behavior in proportion to the experiment.
- Refresh `TODO.md` so completed, partial, and unfinished outcomes remain accurate in the accepted work.
- Integrate the accepted work into `main` and push it. If the environment isolated the work, complete whatever integration is necessary; opening a pull request is not a completed wrap-up.
- Do not introduce required review, branch protection, or professional quality gates unless the user asks for them.
- Consider the devlog during every wrap-up, but append only durable decisions, learnings, or dead ends. Do not duplicate routine implementation activity already represented by Git history or `TODO.md`.
- If integration is blocked, report wrap-up as incomplete and name the blocker. Do not record the work as shipped.

### README.md

Explain what the experiment does and how to run it. Keep build status in `TODO.md`, not the README.

### TODO.md

Use `TODO.md` as the only repo-level build-status tracker.

- Create it when absent.
- Track user-visible outcomes, not engineering tasks.
- Mark completed outcomes and keep unfinished or partially working outcomes accurate.
- Keep it short enough to reveal the experiment's current state at a glance.

Do not create plans, issues, ADRs, architecture docs, `LANGUAGE.md`, a Professional Project Agent Operating System, or other standard project documentation unless the user explicitly asks for a specific artifact.

## Keep essential guardrails

Disposable code does not remove responsibility for secrets, personal data, destructive operations, paid services, deployment, or people who rely on the experiment. Ask before consequential external actions and surface support or safety risks plainly.

Do not add professional ceremony merely because the experiment has users or needs a small maintenance fix.

Bootstrap is complete when the first requested outcome works, the user-visible behavior has been checked, the three repo artifacts describe the current experiment, and the supplied devlog remains the durable record for decisions, learnings, and dead ends.
