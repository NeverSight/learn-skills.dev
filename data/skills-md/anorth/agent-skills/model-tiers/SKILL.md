---
name: model-tiers
description: >-
  Resolves which model a subagent runs on from three tiers (cheap, standard, strong),
  listed in this skill's defaults or the user's ~/.agents/model-tiers.md, and matched to what the harness offers.
  Use when a skill says to spawn a subagent on a tier, when choosing models for reviewers or verifiers,
  or when the user asks to set up or change model tiers.
disable-model-invocation: false
---

# Model tiers

Skills name a tier, not a model.
This skill turns a tier, or a model the user names, into a model the current harness accepts.

## Tiers

- **cheap**: high-volume, narrow work. One theme of a themed review, scanning, summarising.
- **standard**: routine implementation and review.
- **strong**: judgment. Design, coordination, triage, reviewing or verifying others' work, the hardest changes.

## Config

The tiers are one list for all harnesses.
If `~/.agents/model-tiers.md` exists, it is the config, and replaces the defaults entirely.
Otherwise the config is [`defaults.md`](defaults.md), in this skill's directory.

Each tier line names models in preference order, by family and version as a person would write them.
An optional effort in parentheses applies where the harness supports it.

Not every harness offers every model. Entries the harness can't run are skipped.

## Spawning

Spawn a fresh general-purpose subagent, not a fork of this conversation.
A fork may ignore the model and carries the implementer's context.
If the harness has no subagent tool, tell the user and stop; don't do the subagent's work inline.

## Match a model name

To turn a config entry or a name the user gives ("Opus", "GPT") into a model,
match it against the values the subagent tool accepts: its schema, or the list in a rejection message.

- Cursor-style tools take full slugs, which encode effort: pick the slug for that model and effort.
- Claude Code-style tools take an alias (`opus`, `sonnet`, …) and a separate effort parameter.
- Match family and version.
  If that version isn't offered, take the nearest newer one in the same family.
  Never substitute a different family.
- An entry with no match is unavailable here; skip it.

## Resolve a tier

1. Read the config once per session, as **Config** describes, and take the tier's line.
2. Drop entries that don't match an available model.
3. For a reviewer or verifier, take the first remaining entry that passes **Reviewers differ from the implementer**.
   For anything else, take the first.
4. If the tool rejects a model, try the next.
   If the line runs out, omit the model so the subagent inherits the parent's, and say so.
5. If the tier's line is missing: ask the user once which model to use for that tier this session,
   and offer to add it to `~/.agents/model-tiers.md`. If you can't ask, omit the model and say so.

A model the user names explicitly wins over the config. If it has no match, or the match is ambiguous, ask.
When the user gives a count larger than the models they name, resolve the rest from the tier the calling skill uses.

## Reviewers differ from the implementer

A reviewer or verifier of work runs on a different model from the one that wrote it,
so it doesn't share the author's blind spots.

- The implementer is whichever model wrote the change:
  this session's model if you wrote it, or the model given to the implementing subagent.
  If you don't know, say so.
- Prefer a different model family (Claude, GPT, Gemini, …).
  Where the harness offers one family, a different model in it.
- Several reviewers doing the *same* thing each get a distinct model, all different from the implementer.
  Reviewers with different lenses can share a model.
- If the tier's line has no qualifying model, look in higher tiers, then lower tiers.
  If none qualify at all, use the implementer's model. Say which in the report.
- Flag a user-named model that matches the implementer.

## Set up or change tiers

Changes for one environment go in `~/.agents/model-tiers.md`.
If it doesn't exist yet, copy `defaults.md` there.
Then ask the user how they'd like it changed, and edit it.

Changes meant for every environment go in `defaults.md` instead.
