---
name: groove-work-doc
description: "Create a 'how does X work' documentation file for a codebase component or concept. Use $ARGUMENTS as the doc topic if provided."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

<!-- groove:managed — do not edit; changes will be overwritten by groove update -->

# groove-work-doc

Use $ARGUMENTS as the doc topic if provided.

## Outcome

A structured documentation file explaining how a component, concept, or pattern works — for future agents and humans picking up the codebase.

## Acceptance Criteria

Doc file contains:
- **Overview**: What this component/concept is and what problem it solves
- **Key Files**: The most important files, with a one-line role for each
- **How It Works**: Step-by-step explanation of the main flow or logic
- **Gotchas**: Non-obvious constraints, edge cases, known sharp edges

## Constraints

- Sanitize topic for use as filename — strip path separators, special characters, and traversal patterns (`../`)
- Docs directory is always `.groove/memory/docs/`
- Ensure the docs directory exists (create if missing)
- Research the codebase thoroughly before writing (use Explore agent) — docs should reference actual file paths, not generic descriptions
- Interview user if scope is ambiguous: "What's the audience — a new contributor, a future agent, or both?"
- Write doc in isolated context (use general-purpose agent)
- Verify all four required sections exist before completing
- Keep each section concise — this is a reference doc, not a tutorial

## Quality Signals

- Key Files lists actual paths found in the codebase
- How It Works traces a real execution path (e.g. "user runs X → Y reads config → Z writes file")
- Gotchas surface things that are not obvious from reading the code
- Doc does not duplicate what a spec already says — link to the spec if one exists
