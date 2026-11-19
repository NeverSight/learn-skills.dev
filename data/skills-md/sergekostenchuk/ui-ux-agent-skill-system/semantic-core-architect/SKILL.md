---
name: semantic-core-architect
description: Build evidence-labeled semantic cores for SEO, LLM-readable architecture, and site information design. Use this skill when the user asks for semantic core, query clusters, search intents, audience segments, entity/topic maps, language or locale priorities, competitor/source evidence, pillar-topic planning, or a structured handoff before URL architecture and internal linking. It must mark unknown search volume, difficulty, and ranking data as unknown instead of inventing metrics.
---

# Semantic Core Architect

Use this skill before URL architecture, internal linking, schema, content planning, or LLM-friendly page design. It turns a site goal into reusable semantic artifacts.

Read [references/semantic-core-rubric.md](references/semantic-core-rubric.md) before producing a full semantic core.

## Owns

- query clusters;
- user/search intents;
- audience and job-to-be-done mapping;
- entity and topic mapping;
- language and locale priority;
- evidence labels and data gaps;
- handoff to information architecture.

## Does Not Own

- final URL/canonical policy;
- internal link graph;
- schema implementation;
- page copywriting;
- rank guarantees;
- external link placement.

## Workflow

1. Capture the goal, audience, markets, languages, content model, constraints, and forbidden areas.
2. Separate observed facts, user-provided facts, inferred assumptions, and unknowns.
3. Build query clusters by intent, not by keyword volume alone.
4. Map entities and topics to likely canonical page candidates without deciding final URLs.
5. Assign priority from strategic value, page feasibility, audience fit, and evidence strength.
6. Mark volume, difficulty, competitive strength, and rank opportunity as `unknown` unless verified from an approved source.
7. Produce `semantic-core.yaml` and `entity-topic-map.yaml` using the templates in [assets/](assets/).
8. Hand off to `information-architecture-seo` with gaps and assumptions explicit.

## Evidence Rules

- Search volume, difficulty, traffic, ranking, and assistant citation claims require current evidence.
- If keyword tools, Search Console, rank trackers, logs, or assistant-monitoring data are unavailable, use `unknown`.
- Current facts about search engines, AI crawlers, rich results, or platforms must follow the cluster freshness policy.
- Do not use competitor pages as proof of volume unless they come with a measured source.

## Priority Model

Use `P0` only when a cluster is both central to the site's identity and needed by downstream architecture. Use `P1` for important supporting clusters. Use `P2` for useful expansion. Use `P3` for backlog or speculative ideas.

Priority is not ranking probability.

## Required Outputs

Create or update:

- `semantic-core.yaml`, based on [assets/semantic-core.template.yaml](assets/semantic-core.template.yaml);
- `entity-topic-map.yaml`, based on [assets/entity-topic-map.template.yaml](assets/entity-topic-map.template.yaml);
- a gap list for unverified data and needed research.

Each cluster must include intent, audience, languages, entities, queries, evidence, assumptions, unknown metrics, and downstream notes.

## Validation

Before marking work complete:

- check every cluster has intent, audience, language, priority, and at least one query or topic seed;
- check every metric field is either evidence-backed or `unknown`;
- check entity names have stable ids;
- check no URL/canonical decision is made as final;
- run the cluster linter after skill edits.

Validate skill edits with:

```bash
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $HOME/SKILL/skills/semantic-core-architect
python3 $HOME/SKILL/plans/seo-llm-skill-cluster/scripts/lint_skill_cluster.py $HOME/SKILL
```

Forward tests for this skill live in [evals.json](evals.json).

## Output Shape

Return:

1. Semantic core summary.
2. Top clusters by priority.
3. Entity/topic map summary.
4. Unknown metrics and evidence gaps.
5. Handoff notes for information architecture.
