---
name: bootloops-setup
description: Set up the BootLoops protocol skills for this user. Use when the user asks to set up BootLoops, activate or install its skills, or asks what discipline the toolkit ships with. Presents the roster, asks which skills to activate, and installs only what the user chooses.
---

# bootloops-setup

BootLoops ships twelve working protocols in `skills/` at the repository root.
They are a library, not an installation: nothing in `skills/` is active until
the user chooses to activate it. This skill is the installer. Never activate
anything without an explicit choice.

## Procedure

1. **Show the roster.** Present the two groups below (one line each). The
   protocol layer is discipline for any quantitative work; the research skills
   are heavier machinery for specific tasks.

   *The protocol layer:*
   - **acceptance-gate** — what "done" means: never-fit digits against an independent route
   - **constant-recognition** — integer-relation discipline: declared rings, height bounds, refusal over invention
   - **planted-truth** — synthetic-truth controls before real data
   - **independence-bookkeeping** — provenance of reference values; no oracle that fed a fit certifies the result
   - **timing-discipline** — measure a small run first; a multi-hour projection means restructure
   - **reading-contract** — sources-only assertion for document-reading instruments
   - **tool-stewardship** — consult the toolkit first, write code last, document for the next agent

   *The research skills:*
   - **prove-protocol** — proving with agents: adversary-first pipelines, skeptic loops
   - **referee-sim** — pre-circulation audit: the strongest standard objection from every audience
   - **lit-review** — the literature audit behind a novelty claim: papers actually read, citation chains both directions
   - **ref-check** — bibliography verification against authoritative sources
   - **prose-lint** — scientific-prose linter: hype vocabulary, empty structures, agentless prose, honesty and number checks

2. **Ask what to activate.** Offer: all twelve, the protocol layer only, the
   research skills only, an individual selection, or none. Use the host's
   question/multi-select interface if it has one (in Claude Code, grouped
   multi-select questions fit within the four-option limit); otherwise ask in
   plain text. "None" is a fine answer — the library stays available to read
   or load ad hoc either way.

3. **Ask the scope.** Project-level (`.claude/skills/` in the user's project —
   active only there) or user-level (`~/.claude/skills/` — active in every
   project). Default to project-level if the user has no preference.

4. **Install.** Copy each chosen skill's directory from `skills/<name>/` in
   this repository into the chosen location, keeping the directory name.
   Nothing else: no edits to the files, no extra registration step.

5. **Confirm.** List what is now active and where. Note that an activated
   skill still only engages when its work actually comes up; activation makes
   it discoverable, not mandatory. To deactivate one later, delete its
   directory from the install location. Re-run this setup any time to add or
   change the selection.
