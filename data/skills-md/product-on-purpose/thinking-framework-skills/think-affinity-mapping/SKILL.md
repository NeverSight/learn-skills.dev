---
name: think-affinity-mapping
description: Produces a clustered theme map that groups many raw notes, observations, quotes, or data points bottom-up into a small set of named, traceable themes (the KJ method). Use when a scattered pile of dozens to hundreds of existing items needs to become a few emergent themes, such as synthesizing user-research notes, support tickets, survey free-text, or retro stickies, and the right structure should emerge from the data rather than be imposed.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.affinity-mapping
  family: synthesis
  evidence-tier: "P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Affinity Mapping

Affinity mapping takes a pile of many individual items - raw notes, observations, quotes, data points - and groups them *bottom-up by felt similarity* until a small set of emergent themes appears, then names each theme so the names become the structure. The load-bearing move is **deferred, bottom-up categorization**: you do not sort items into predefined buckets, you let the categories surface from the items themselves. This externalizes comparison so patterns hidden in a linear list become visible, resists the frame you walked in with, and compresses many items into a few themes while keeping every item traceable to its theme. The output is a **clustered theme map**, not a discussion.

## When to Use

- When dozens to hundreds of existing items - user-research notes, interview quotes, support tickets, survey free-text, retro stickies, workshop output - need to become a few themes.
- When the right structure is not known in advance and should emerge from the data rather than be imposed.
- When the items already exist and the job is synthesis, not generation.
- When traceability matters: you want each theme to point back to the specific items that support it.

## When NOT to Use

- **When there are only a handful of items.** With a dozen or fewer you can reason about them directly; the clustering ceremony adds overhead without insight.
- **When you need a top-down logical structure** - a question decomposed into MECE sub-questions or a hypothesis tree. That is top-down decomposition from a question; use an issue-tree skill. Affinity mapping is bottom-up, from items.
- **When you need to generate ideas or options.** Affinity mapping only organizes items that already exist and produces no new ideas. Use an ideation skill (for example brainwriting) to create the items first, then affinity-map them.
- **When the categories are already fixed and authoritative** (a required taxonomy, a compliance schema). Then you are coding into known buckets, not discovering emergent themes.
- **As a ritual** - grouping into a few buckets and slapping confident names on them with no traceability is cargo-cult synthesis, not insight.

## Instructions

When asked to run an affinity map, follow these steps:

1. **Frame the question and gather the items.** State in one sentence what synthesis is for (for example, "what is blocking free-tier activation?"), and assemble every item as a discrete, comparable unit. If there are only a handful of items, or the categories are already fixed, say so and stop.
2. **Cluster before naming.** Place items that feel related together, bottom-up, by similarity. Do not start from predefined buckets and do not name groups yet. Let clusters form, split, and merge as items accumulate. This deferral is the mechanism; naming first defeats it.
3. **Name each emergent theme from its contents.** Once clusters are stable, give each a short descriptive name that answers to the items inside it, not to your prior frame. A theme whose items do not cohere is a signal to split or dissolve it, not to force a label.
4. **Keep every item traceable.** Each theme records the source items it contains (by list, or by count plus representative examples). Items that did not cluster go to an explicit outliers / parking lot, never silently dropped.
5. **Weight and read the themes.** Note each theme's relative size or strength, and state what the map tells you - which themes dominate, which are thin, what surprised you. Size is a signal of salience, not of truth; flag thin or borderline clusters as tentative.
6. **Emit the theme map and a short summary.** Produce the artifact in `references/TEMPLATE.md`: a one-paragraph "themes and what they tell us" summary above the named-theme table, with outliers kept visible.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the filled clustered theme map plus its summary, not a prose essay.

## Quality Checklist

Before finalizing, verify:

- [ ] Clustering happened before naming (themes emerged from items, not from predefined buckets).
- [ ] Each theme has a short name that answers to the items inside it, not to a prior frame.
- [ ] Every item is traceable to a theme, and items that did not cluster are kept in an explicit outliers / parking lot, not dropped.
- [ ] Themes are weighted by relative size or strength, and thin or borderline clusters are flagged as tentative, not laundered by a confident label.
- [ ] The output is the clustered theme map artifact, not prose.
- [ ] No overclaiming: the skill organizes a scattered pile into named, traceable themes; it does not promise objectively better or bias-free themes (see `evidence/dossier.md`).

## Evidence

Tier **P** (practitioner). Affinity mapping is a long-standing, widely-taught practitioner standard for synthesizing large qualitative piles (the KJ method; Kawakita 1967), with a plausible cognitive basis in external representation and chunking. It does **not** have strong controlled evidence that it produces better, more accurate, or less biased themes than another synthesis method, and "group by similarity" remains a subjective judgment. The evidence is transferred from human practice and has not been validated for AI-augmented use. Full grading, sources, and caveats: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed run.
