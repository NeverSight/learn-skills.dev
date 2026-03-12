---
name: swain-help
description: "Contextual help and onboarding for the swain skill ecosystem. Use when users ask about swain — what skills exist, how to use them, what artifacts are available, how workflows connect, or when they need a quick reference. Also invoked after swain-init to orient new users. Triggers on: 'how do I...', 'what is...', 'help', 'what can swain do', 'show me the commands', 'I'm confused', 'where do I start', any question about swain skills, artifacts, or workflows, and after project onboarding completes."
user-invocable: true
license: MIT
allowed-tools: Read, Glob, Grep, Skill
metadata:
  short-description: Contextual help and onboarding for swain
  version: 1.0.0
  author: cristos
  source: swain
---

# swain-help

Contextual help for the swain skill ecosystem.

## Mode detection

Determine the mode from context:

| Signal | Mode |
|--------|------|
| Invoked from swain-init Phase 4, or user says "just set up swain" / "what now after init" | **Onboarding** |
| User asks a specific question ("how do I...", "what is...", "when should I...") | **Question** |
| User asks for a reference, cheat sheet, commands, or overview | **Reference** |

## Onboarding mode

Present a concise orientation — help the user understand what they just installed without overwhelming them. Adapt tone to context (first-time dev vs experienced engineer).

Present this:

> **Welcome to swain.** Here's how it works:
>
> **The big picture:** Swain manages your project's documentation artifacts (specs, stories, ADRs, etc.) and tracks implementation work — so nothing falls through the cracks between sessions.
>
> **Three things to know:**
>
> 1. **`/swain` is your entry point.** It routes to the right sub-skill automatically. You can also call skills directly (`/swain-design`, `/swain-do`, etc.).
>
> 2. **Design before you build.** When you want to implement something, start with `/swain` to create a spec or story. Swain enforces a "plan before code" workflow — it creates tracked tasks before implementation begins.
>
> 3. **Health checks are automatic.** `/swain-doctor` runs at session start to ensure routing rules are in place and `.beads/` is healthy. You don't need to think about it.
>
> **Common starting points:**
> - "I want to plan a new feature" → creates an Epic or Story
> - "Write a spec for X" → creates an Agent Spec
> - "What should I work on next?" → checks your task backlog
> - "File a bug" → creates a Bug artifact
> - "Let's release" → version bump + changelog
>
> **Need more?** Ask me anything about swain, or say `/swain help reference` for a full cheat sheet.

Then stop. Let the user ask follow-up questions — don't dump everything at once.

## Question mode

Answer the user's specific question using your knowledge of swain. If you need details beyond what's in this skill, read the relevant reference:

| Topic | Where to look |
|-------|---------------|
| Artifact types, phases, relationships | `references/quick-ref.md` — Artifacts section |
| Commands and invocations | `references/quick-ref.md` — Commands section |
| Step-by-step walkthroughs | `references/workflows.md` |
| Artifact definitions and templates | `../swain-design/references/<type>-definition.md` |
| bd (beads) CLI reference | `../swain-do/references/bd-cheatsheet.md` |
| Troubleshooting | `../swain-design/references/troubleshooting.md` |

Guidelines for answering:

- **Be concise.** Answer the question, don't dump the entire reference.
- **Use examples** when they clarify — "You'd say `/swain create a spec for auth token rotation`".
- **Hand off when appropriate.** If the user's question is really a request to *do* something (e.g., "how do I create a spec?" followed by "ok do it"), invoke the relevant skill directly via the Skill tool. Explain what you're doing: "I'll hand this off to swain-design."
- **Admit gaps.** If something isn't covered, say so rather than inventing swain features.

## Reference mode

When the user wants an overview or cheat sheet, read `references/quick-ref.md` and present the relevant section. If they want "everything", present the full quick reference but note it's dense.

For workflow walkthroughs, read `references/workflows.md`.
