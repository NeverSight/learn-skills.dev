---
name: app-design
description: Use when the user wants to understand, audit, or improve an application that already exists. Triggers on "understand this codebase and improve it", "analyze this app and find bugs", "audit and plan next steps", "what should I fix first". Question-driven lifecycle — analyze → verify with the user → test → triage → propose improvements. Uses the dogfood skill for runtime QA. For a project that does not exist yet, use the ideator skill instead.
license: MIT
metadata:
  version: 2.0.0
  argument-hint: "[project-path-or-idea]"
allowed-tools: read, write, edit, bash, grep, find, ls
---

# App Design — Design & Build Lifecycle (pi edition)

This skill walks the user through understanding and improving an app **that
already exists**. It is **question-driven**: you ask, the user answers, you act.
Analyze → verify with the user → test → triage bugs → propose improvements.

**For a project that does not exist yet, this is the wrong skill.** Hand off to
[`ideator`](../ideator/SKILL.md), which starts the new-project chain:
`/ideator` (brief) → `/constructor` (architecture) → `/datasecurer` (security and
redundancy). Say so in one line and stop rather than starting here.

See also: [USE_CASES.md](USE_CASES.md) for trigger phrases and a worked
example, and the [top-level skills index](../USE_CASES.md). The Test
phase calls [`dogfood`](../dogfood/SKILL.md) directly for web apps.

## How to ask questions (important — read this)

pi has **no special question tool and no menu popups**. You ask questions as
plain text in your reply. Do it like this:

- Ask **2–4 questions at a time**, numbered. Wait for answers. Then ask more.
- Keep each question tied to one real decision. No "tell me everything".
- After the user answers, briefly say what you concluded, then continue.
- **STOP and wait** at every point that says "ask the user". Do not guess
  answers and keep going.

Draw question wording from [references/question-bank.md](references/question-bank.md).

## Rules

1. **Verify assumptions** — don't act on a guess; ask.
2. **Show your reasoning** — when you propose a stack/fix/refactor, give the
   trade-offs and why. Never present one option as the only option.
3. **Confirm before changing code** — list the change, get a yes, then edit.
4. **Write artifacts to disk** with the `write` tool, under
   `./app-design-output/` so they survive the session.

## Step 0 — Confirm this is the right skill

1. If the user points at a folder/repo, or you are inside one with source files,
   you are in the right place. Confirm in one line:
   "This looks like an existing <type> app — I'll analyze it first. Correct?"
2. If the user describes something to build that **doesn't exist yet**, stop and
   redirect: "That's a new project — `/ideator` sharpens the idea into a brief,
   then `/constructor` designs the architecture. Want me to hand off?"
3. If unclear, ask: "Are we improving an existing codebase, or starting from
   scratch?" — then STOP and wait.

Then make the output folder:

```sh
mkdir -p app-design-output
```

---

## The lifecycle

Full step-by-step playbook: read [references/existing-project.md](references/existing-project.md).
Question wording: [references/question-bank.md](references/question-bank.md).

The five phases (do them in order, do not jump ahead):

1. **Discover** — Map the code. Detect stack, entry points, structure,
   dependencies, data model, and how to build/run/test. Use `ls`, `find`,
   `grep`, and `read` (see playbook for the exact commands).
2. **Verify** — Write down what you THINK the app does, then ask the user
   numbered questions to confirm or correct it. Save the agreed truth to
   `app-design-output/app-model.md`. **Do not test until the user confirms.**
3. **Test** — Run the test battery in [references/test-battery.md](references/test-battery.md): install,
   build, lint, typecheck, run existing tests, then runtime QA. For web apps,
   run [`/skill:dogfood`](../dogfood/SKILL.md) against the running app. Collect every bug.
4. **Triage** — Show findings grouped by severity. Ask the user which are real
   bugs vs intended behavior. Fix ONLY what they approve.
5. **Enhance** — Propose new features and refactors, each with value, effort,
   and risk. Save to `app-design-output/recommendations.md`. Let the user pick.

## New projects belong elsewhere

This skill used to carry a second mode for projects that did not exist yet. That
work is now owned by a dedicated chain, which does it better because each stage
produces an artifact the next one consumes:

| Stage | Skill | Produces |
|---|---|---|
| Sharpen the idea | [`ideator`](../ideator/SKILL.md) | `ideator-output/project-brief.md` |
| Design the build | [`constructor`](../constructor/SKILL.md) | architecture, folder structure, dependencies |
| Secure it | [`datasecurer`](../datasecurer/SKILL.md) | threat model, security and redundancy plan |

Redirect rather than improvising a parallel version of it.

**One gap to be honest about:** that chain stops at the security plan. It does not
produce a written specification or a milestone plan. If the user wants those after
`/datasecurer`, this skill still owns that step — follow
[references/spec-and-plan.md](references/spec-and-plan.md), which fills
[templates/specifications-template.md](templates/specifications-template.md) and
[templates/development-plan.md](templates/development-plan.md) *from the chain's
artifacts* rather than re-interviewing a user who has already answered these
questions once.

---

## Artifacts (write these with the `write` tool)

| File | Purpose |
|------|---------|
| `app-design-output/app-model.md` | Verified purpose, structure, flows |
| `dogfood-output/report.md` | Bug report from the dogfood QA run |
| `app-design-output/recommendations.md` | Approved fixes, features, refactors |

Only if the user asks for them after the new-project chain has run:

| File | Purpose |
|------|---------|
| `app-design-output/specifications.md` | Full spec, from the template here |
| `app-design-output/development-plan.md` | Milestones + ordered tasks |

## Reminders for staying on track

- Keep a short checklist of the phases in your reply and tick them off as you
  go (pi has no to-do tool, so just write the list in text).
- Never skip Verify — testing the wrong assumed intent manufactures fake bugs.
- If it turns out there is no existing code, stop and hand off to `/ideator`
  rather than quietly becoming a new-project skill.
- If [`/skill:dogfood`](../dogfood/SKILL.md) or its browser script isn't usable, fall back to the
  non-browser runtime checks in [references/test-battery.md](references/test-battery.md).
