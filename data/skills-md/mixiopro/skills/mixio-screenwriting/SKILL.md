---
name: mixio-screenwriting
description: "Use when developing story material before Mixio Studio production: idea discovery, logline, character/world, structure, scene writing, dialogue/subtext, story rewrites, or screenplay quality gates."
version: 0.1.0
invoke: /mixio:screenwriting
---

# Mixio Screenwriting Bridge

This is the writer-development boundary between story work and Mixio production. Use the complete Mixio-owned `how-to-make-script` screenplay system for the eight requested routes, then hand off the screenplay package and its quality findings to `mixio-pipeline`.

## Companion requirement

The vendored repository is the source for the writing protocols, rubrics, knowledge atoms, schemas, examples, and router. The files under `skills/how-to-make-script/` are Mixio-owned and may be customized, but preserve the dependency graph and update [UPSTREAM.md](../how-to-make-script/UPSTREAM.md) when importing upstream changes. Do not copy only one route `SKILL.md`, paraphrase its dependencies, or silently replace a missing route with a generic screenplay answer.

The standard Mixio package installs the root skill recursively. For a local checkout, verify the owned package before using the bridge:

```bash
test -f skills/how-to-make-script/SKILL.md
test -f skills/how-to-make-script/UPSTREAM.md
test -f skills/how-to-make-script/skills/idea-discovery/SKILL.md
test -f skills/how-to-make-script/skills/quality-gating/SKILL.md
```

Load only the route that matches the current request:

- `idea-discovery` — vague idea, image, theme, or situation
- `logline-premise` — story engine needs compression and clarity
- `character-world` — character pressure, relationships, or world rules
- `structure-beat` — beat sheet, sequence, outline, or treatment
- `scene-writing` — scene card, scene draft, or screenplay draft
- `dialogue-subtext` — dialogue objectives, voice separation, and subtext
- `rewrite-doctor` — story-level diagnosis and rewrite prioritization
- `quality-gating` — screenplay contract, rubric, preflight, or recheck

## Ownership boundary

The screenplay system owns premise, character pressure, structure, scene/dialogue craft, story-level diagnosis, and screenplay quality. Mixio owns native screenplay persistence, exact Cast & World references, sheets, anchors, shot breakdown, visual continuity, generation, and rendered-media evaluation.

Do not confuse the layers:

- `rewrite-doctor` diagnoses story and text layers; `mixio-continuity` creates the director-led Continuity Checklist for the local or persisted shot plan.
- `quality-gating` checks screenplay contracts and craft lenses; `mixio-reference-audit` checks Cast & World readiness.
- Upstream-only writing work needs no Studio project/episode lookup and must not submit billable jobs.

## Handoff

When the user asks for screenplay development before Mixio production, produce the handoff described in [screenplay-handoff.md](references/screenplay-handoff.md). The screenplay may be a draft, but its intent, constraints, and quality findings must be explicit. Treat `pass`, `pass_with_weaknesses`, and `needs_revision` as advisory quality outcomes: summarize any weaknesses and offer focused fixes, but do not block the user's requested next step when they confirm “proceed.” For a full production run based on a high-level script, outline, or underdeveloped screenplay, `/mixio:pipeline` develops the director’s screenplay before shot breakdown. Use relevant scene-writing, structure, and quality-gating routes; preserve the source story and dialogue while adding clearly labeled visual, continuity, and connective direction. A production-ready screenplay can proceed directly to breakdown without a persisted Studio approval status.

At the handoff boundary:

1. Resolve the Mixio project and episode according to `AGENTS.md`.
2. Read the native screenplay grammar and list existing references.
3. Normalize the screenplay into Mixio's native grammar and copy exact reference mentions; never invent Studio IDs or `#` tokens upstream.
4. Present the complete proposed screenplay and a source-to-screenplay change map as a checkpoint. Keep source facts/dialogue distinct from `INFERRED` direction and surface consequential changes as `OPEN DECISION`s. On the user's “proceed” or prior authorization for this scope, persist the native screenplay as a draft and read it back. Continue production from that confirmed draft; no separate Studio approval action/status is required.
5. Continue production through `mixio-pipeline`: confirmed screenplay, local breakdown, director-led Continuity Checklist, confirmed sync, reference readiness, shot planning, and generation. If the user elects to proceed with an open story question, preserve it explicitly and continue unaffected work.

If story intent changes after the breakdown has been synced (pipeline Step 03), return to the upstream route and re-run the relevant quality gate before re-entering production. A screenplay edit invalidates the local plan and its Studio diff; after sync it also invalidates downstream continuity, shot planning, and generated media.

## Not this skill

Do not use this bridge for a request that is already a Studio production operation such as creating an episode, managing references, breaking a screenplay into shots, generating media, or evaluating renders. Use the corresponding Mixio skill or start at `mixio-pipeline` when the production step is unclear.
