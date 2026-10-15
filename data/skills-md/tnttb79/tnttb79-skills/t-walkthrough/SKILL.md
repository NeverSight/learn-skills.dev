---
name: t-walkthrough
description: Generate a complete set of concise, evidence-based lecture-style walkthrough docs (a lectures/ directory) that teach an unfamiliar codebase by analyzing its current source and structure. Breaks the project into topics (by architecture layer, feature, or a hybrid, whichever fits) and writes the full lecture set in one pass, starting with a concise 00 project-overview lecture. Asks once about the reader's background to calibrate depth, skipping that question if the context was already given. Use when the user wants to learn or onboard onto a codebase, asks for a walkthrough, tour, or architecture explainer, wants onboarding docs generated, or says things like "walk me through this codebase," "explain the architecture," or "help me understand this project."
disable-model-invocation: true
---

# Codebase Walkthrough Generator

## Goal

Help the user build a strong mental model of an unfamiliar codebase by generating a
complete, evidence-based set of lecture-style Markdown files in a `lectures/` directory.
Derive the topic breakdown by analyzing the current state of the code itself.

Every lecture must teach both **how** the implementation works and **why** it was designed
that way. Do not merely summarize files or restate code. Read
[references/authoring-guide.md](references/authoring-guide.md) before writing lectures.

## Step 0 — Calibrate to the reader's background

Check whether the user already stated their background when invoking the skill (e.g. "I
know React well but this is my first Rust project," "senior backend engineer, new to this
repo").

- If they did, use it directly — do not ask again.
- If they didn't, ask **one** question covering: general experience level, which parts of
  the stack they already know, and anything they already know about this project.

Use the answer to decide what to explain in depth versus in passing. Don't over-explain
concepts they already know; do explain unfamiliar framework behavior, architecture
patterns, and project-specific decisions before relying on them. Keep this to one question,
then move on.

## Step 1 — Analyze the codebase and plan the topic breakdown

1. Inspect the repo: directory structure, entry points, config and build files,
   README/docs, package boundaries, and major dependencies.
2. Choose the segmentation that produces the clearest, least-overlapping topics for *this*
   project — by architecture layer, by feature/domain, or a hybrid. Don't force a scheme
   the codebase doesn't fit.
3. Draft a topic outline before writing anything: one lecture per topic, each mapped to the
   files and directories it will draw evidence from. Keep topics distinct — no two lectures
   share the same code as their primary subject.
4. Reserve `00` for the project overview. Number the rest `01`, `02`, … in learning order:
   foundational and architecture topics before feature-specific ones, dependencies before
   dependents.

For a large codebase where per-topic evidence-gathering is expensive, delegate research
per topic to parallel sub-agents, then write all lectures yourself for a consistent voice
and correct cross-references. See the authoring guide.

## Step 2 — Lecture 00: project overview

Write this first. Keep it a quick orientation, not a deep dive:

- What the project does and who or what it's for.
- Tech stack at a glance.
- Overall architecture: a short diagram (Mermaid or a directory tree) plus a paragraph on
  how the major pieces relate.
- A map of the other lectures (topic → filename) so `00` doubles as a table of contents.

## Step 3 — Generate the full lecture set in one pass

Write the complete `lectures/` directory — `00` plus every planned topic — in this run.
Follow [references/authoring-guide.md](references/authoring-guide.md) for the per-lecture
anatomy and evidence rules. In short: base every claim on the actual current source, trace
symbols across file and package boundaries, cite repo-relative paths (and symbol or line
where useful), quote only the relevant snippet, and verify paths and names against the repo
before finishing. Favor short, clear explanations — this is a map, not an exhaustive
reference.

Filename format: `NN-descriptive-topic-name.md`.

## Step 4 — Report back

Give a brief summary: the file list with a one-line description each, and point to
`lectures/00-*.md` as the starting point. Don't dump lecture content into the chat — the
files are the deliverable.

## Ongoing use (after the initial generation)

When the user later asks about a topic:

- If a lecture already covers it, answer directly using that lecture plus the current source
  as context. Don't regenerate or duplicate it.
- If it's genuinely uncovered (new code since generation, or a topic missed originally),
  create one new lecture in the same conventions and add it to the `00` overview's map.

If `lectures/` already exists when the skill is invoked, don't blindly overwrite. Tell the
user what's there and ask whether to refresh existing lectures, extend with new topics, or
start over.

## Scope guardrails

- Only create or update files under `lectures/` (and the map in `00`). Never modify
  application source unless the user explicitly asks for an implementation change.
- Never create a duplicate lecture for a subject that already has one.
