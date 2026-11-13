---
name: pm-user-story
description: Write or critique a user story — a small unit of user value framed from a real persona's need, not a restated task. Frames stories around who/what/why, keeps them INVEST and testable, maps them across the journey, and resists writing stories that add no clarity. Applies the always-true core and gates context-dependent decisions (strict formula vs. free-form, whether to write a story at all, acceptance-criteria depth, splitting into a map, communication framing). Trigger when asked to write user stories, turn a persona or need into stories, frame requirements as stories, build a story map, apply INVEST, or review/strengthen existing stories.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# User Story Skill

## How this skill behaves (read first)

This is a **generative** skill, and user stories are where requirements quietly turn back into a task list. The default move is to restate a feature as a story — "Add login feature," or the hollow "As a user, I want a button so I can submit" — describing *what to build* instead of *who needs what and why*. A real user story is **a small, testable unit of user value, grounded in a real persona's need**, that gives the team a shared who/what/why — and the discipline to *not* write one when it adds nothing the spec already says. So this skill gates:

1. **Establish whose need this is, whether it's real, and what the story feeds** — a story with no grounded user is an assumption in costume.
2. **Apply the always-true core** — frame from user value, keep the story small with detail pushed to acceptance criteria, make it INVEST/testable, map stories across the journey, and cut stories that add no clarity.
3. **Surface the context-dependent decisions** (strict formula vs. free-form, write-a-story-at-all, acceptance-criteria depth, splitting into a map, communication framing) with trade-offs.

Then it **hands off to `pm-spec-quality-audit`** (which flags task-stories, untestable stories, and broken traceability) and **`pm-assumption-rigor-audit`** (is the user need evidenced or assumed?).

Scope: this skill owns the **user-story artifact**. It defers **building the persona** to `pm-personas-jtbd`, **framing the underlying problem** to `pm-problem-statement`, and the **full spec/PRD and acceptance-criteria depth** to `pm-product-spec` (audited by `pm-spec-quality-audit`). **Agile ceremonies, backlog grooming, and sprint mechanics** are out of scope.

---

## Step 0 — Establish context before writing stories

Ask if not known; state the assumption if proceeding without an answer:

- **Whose need is this, and is it real?** A story starts from a research-grounded persona and a validated need — "As Maria, who has no time to configure settings…" beats "users prefer automation." If the persona or need is assumed, say so; an ungrounded story propagates the assumption into the backlog. (Build the persona in `pm-personas-jtbd`.)
- **How complex is the need?** A single discrete need fits the "As a [persona], I want [action], so that [benefit]" formula; a feature spanning multiple user types or layered benefits may need to be split or written free-form.
- **Does a story add clarity the PRD/spec doesn't already have?** If the team gets full context elsewhere, a story is documentation for its own sake. Write it only when it earns its place.
- **What does it feed?** A backlog, a spec, or an imminent sprint — this sets how much acceptance-criteria detail to attach now.

---

## The always-apply core (true for any user story)

- **Frame from user value, not the task.** "As a [persona], I want [action], so that [benefit]" expresses *intent and value*, not a technical to-do. ❌ "Add login feature" / "Improve dashboard performance." ✅ "As a returning user, I want to log in quickly so I can access my saved data." Each story is a *problem to solve*, not a feature to ship.
- **Ground each story in a real persona and need.** Go from persona → story; for complex or early problems, dig into the user's frustrations first so the story reflects a real obstacle, not an assumed one. Build from insight, not convenience.
- **Treat the formula as a starting point, not a rule.** When a feature involves multiple user types, several actions, or layered benefits, one sentence won't hold it — splitting or writing free-form is valid, as long as *who, what, and why* stay clear.
- **Keep the story a small unit of value; push detail to acceptance criteria.** The story names the need; specifics like filter types, edge cases, and interaction rules live in the acceptance criteria and the spec that follow. Don't inflate a story into a mini-spec.
- **Make it INVEST and testable.** Independent, Negotiable, Valuable, Estimable, Small, Testable. Acceptance criteria define "done" so design, engineering, and QA share one definition of success ("users can add, view, and remove saved destinations").
- **Map stories across the journey.** Story mapping connects four blocks — *problem → functionalities → user stories → tasks* — so every requirement traces back to a real user need. Organizing the spec by story keeps the work grounded; the map itself is a shared-understanding tool before anything is formally documented.
- **Spot and fix weak stories.** Missing context, overly technical phrasing, or no measurable goal signal a task in disguise. Repair by returning to who–what–why and reviewing against the persona.
- **Don't write a story that adds no clarity.** Not every feature needs one. If the PRD/spec already gives the team the context, a story adds noise, not value — the test is always "does this add clarity that isn't captured elsewhere?"
- **Communicate the story clearly.** Lead with the user value and the decision in plain product language, not design/feature language ("prioritizes the most commonly used filters to reduce choice overload," not "we added a filter component"). Synthesize to one direction and cut noise so stakeholders grasp the intent fast.

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0; let the user choose. **Mechanically stamping every ticket into the "As a user…" template is the failure mode.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Strict formula vs. free-form** | The formula for a discrete, single-persona need | Forcing one sentence onto a multi-user / layered feature | Formula by default; split or go free-form when who/what/why won't fit one line |
| **Write a story at all** | When it adds shared who/what/why the spec lacks | Generating a story per ticket as ritual documentation | Write only when it adds clarity not already captured elsewhere |
| **Acceptance-criteria depth now** | Enough AC to define "done" for the current stage; fuller AC when feeding a sprint/spec | Front-loading exhaustive AC during early framing, or shipping a story with none | Attach AC that define done; defer testability depth and structure to `pm-product-spec` / `spec-quality` |
| **Single story vs. split into a map** | Split when a story spans multiple actions/personas or is too big to finish in a sprint (INVEST: Small) | One giant epic-as-story, or over-splitting into technical task-stories | Split by *user value*; map problem → functionality → story → task |
| **Communication framing** | Leading with the decision and user value when presenting to stakeholders | Design-language or feature-list framing that buries the decision | State the user value first, structure for scanning, remove noise |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After producing or revising, hand it to the audit lenses rather than declaring it done. These are **candidate** lenses — posture per `docs/orchestration-policy.md`, or route the whole artifact through `pm-product-review`. Here **`assumption-rigor` is the always-relevant lens (auto-runs)**; the others are **offered**, tied to what the artifact actually contains. If the user invoked this skill for one specific thing, respect that scope.

- **`pm-assumption-rigor-audit`** *(auto-runs)* — is the persona and need each story rests on grounded in evidence, or assumed? Flag stories built on an untested belief about who the user is or what they need.
- **`pm-spec-quality-audit`** *(offer — if it writes stories that feed a spec)* — the core spec check here: it flags **task-stories** (a feature restated as a story with no user value), untestable stories with no acceptance criteria, and broken traceability between requirements and the user need. It also owns acceptance-criteria depth and full-flow coverage that the story itself defers downstream.

**Composition (per `docs/orchestration-policy.md` §9):** the story is fed by upstream work rather than auditing it — the **persona** (`pm-personas-jtbd`) and the **problem** (`pm-problem-statement`) are upstream inputs. If the audits show a story is really a task or rests on an assumed user, resolve toward the purpose: **a user story exists to keep the team building for a real person's real need — if it doesn't name who benefits and why, it's a task wearing a story's clothes.** For a full idea-to-plan build, `pm-idea-to-plan` is the compositional front door that sequences this step with the rest of the ladder and enforces evidence before the spec.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| "Add login feature" / "Improve dashboard performance" | "As a returning user, I want to log in quickly so I can access my saved data" |
| "As a user, I want a button so I can submit" | Name a real persona, a genuine action, and the value behind it |
| Invent the user the story serves | Ground it in a research-based persona and a validated need |
| Force every feature into one "As a…" sentence | Use the formula as a default; split or go free-form for complex needs |
| Pack filter types and edge cases into the story | Keep the story small; push specifics to acceptance criteria |
| Leave the story untestable | Make it INVEST; AC define "done" for design, eng, and QA |
| A flat backlog of unrelated stories | Map problem → functionality → story → task so each traces to a need |
| Write a story for every ticket out of habit | Skip the story when the spec already gives full context |
| Describe the solution in design/feature language | Lead with user value and the decision in plain product language |
| Ship stories unchecked | Hand off to spec-quality + assumption-rigor |

---

## Source lessons (Uxcel)

- [Understanding Users and Framing User Stories](https://uxcel.com/lessons/understanding-users-and-framing-user-stories-802)
- [Communicating Your Solution Clearly](https://uxcel.com/lessons/communicating-your-solution-clearly-589)
