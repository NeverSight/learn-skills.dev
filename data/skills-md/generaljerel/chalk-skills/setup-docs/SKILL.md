---
name: setup-docs
description: Analyze the codebase and populate all .chalk/docs profile stubs with real project content. Run once after chalk init.
owner: chalk
version: "1.0.0"
metadata-version: "1"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[optional: specific vertical to populate, e.g. 'engineering only']"
---

One-shot bootstrap that analyzes the codebase and populates all three `.chalk/docs/` profile stubs with real, project-specific content. Meant to run once, right after `npx get-chalk` or Chalk Browser setup.

## When to Use

- After running `npx get-chalk` to populate the stub docs
- After setting up Chalk via the browser's "Set Up Chalk" prompt
- When profile docs contain `<!-- STUB -->` markers or placeholder content

## Workflow

1. **Analyze the codebase** — Read `package.json`, `README.md`, `src/` directory structure, config files (`tsconfig.json`, `vite.config.*`, `tailwind.config.*`, etc.), and any existing docs.

2. **Check which docs need population** — Read each profile doc. Skip any that are already populated (no `<!-- STUB -->` comment and more than 20 lines of real content).

3. **Populate Product Profile** (`.chalk/docs/product/0_PRODUCT_PROFILE.md`):
   - Summary: product name, one-liner, primary users, core JTBD, value prop
   - Problem: what pain this solves
   - Target Users: table (Persona, Job, How This Helps)
   - Core Jobs To Be Done: numbered list
   - Current Status: what's built, what's planned
   - What It Is / What It Is Not
   - How It Works: user flow

4. **Populate Engineering Profile** (`.chalk/docs/engineering/0_ENGINEERING_PROFILE.md`):
   - Architecture Overview: execution contexts, process model, diagram
   - Tech Stack: table (Layer, Technology, Version, Purpose)
   - Data Flow: key pipelines
   - Database / Storage: schema, persistence model
   - Conventions: code style, patterns, state management, error handling
   - Build & Development: commands and prerequisites
   - Implementation Status: module table

5. **Populate AI Profile** (`.chalk/docs/ai/0_AI_PROFILE.md`):
   - Project Identity: one paragraph
   - Codebase Orientation: "Where Things Live" table (What, Where, Notes)
   - Conventions: code style, state management, error handling
   - Key Gotchas: numbered list of agent-surprising things
   - Prompt Patterns: "For X changes, work in Y"

6. **Update AGENTS.md** — Enrich with project-specific pointers to the populated docs and critical conventions.

7. **Confirm** — List what was populated and what was skipped.

## Rules

- **Write substantive content, not stubs** — Every section should have real information from the codebase analysis.
- **Remove `<!-- STUB -->` markers** — When populating a doc, remove the stub comment.
- **Preserve existing content** — If a doc already has real content in some sections, update/enhance rather than overwrite.
- **Use the vertical's tone** — Product docs are business-facing. Engineering docs are technical. AI docs are agent-facing reference-style.
- **Include the "Last updated" line** — Format: `Last updated: YYYY-MM-DD (populated from codebase analysis)`.

## Differences from /create-doc

- `/create-doc` creates a **single new doc** for a specific topic on demand
- `/setup-docs` is a **one-shot bootstrap** that populates **all three profile stubs** at once
- After setup, use `/create-doc` and `/update-doc` for ongoing doc management
