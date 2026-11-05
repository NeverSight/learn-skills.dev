---
name: port-context-lake
description: "Design and build a Port context lake: a connected, semantically-rich data model of blueprints, relations, and mirror/aggregation properties that AI agents, scorecards, and workflows can query and act on, not just a plain software catalog. Use when asked to 'build a context lake', 'design a Port data model for AI agents', 'set up the engineering intelligence data model', 'connect services to teams and orgs in Port', 'model our org hierarchy in Port', or 'why can't Port AI answer questions about our org structure'."
license: MIT
compatibility: "Claude Code, Cursor, Codex CLI, GitHub Copilot"
metadata:
  version: "1.0.0"
  author: port-labs
  repository: https://github.com/port-labs/port-skills
  tags: port,context-lake,data-model,ontology,reference
  summary: Design a Port context lake with connected blueprints and semantic relations
---

# Build a context lake

A context lake is Port's data model once it stops being a flat catalog and
becomes a connected graph: blueprints related to each other, with mirror and
aggregation properties, descriptions, and relation titles precise enough
that an AI agent can traverse it and act, not just browse it. This skill
designs that model. For the JSON mechanics of any single blueprint,
property, or relation, use `port-blueprints`; this skill is the layer above
that: what to build, in what order, and why.

## Prerequisites

- Go over the `port-getting-started` skill first if this is your first time
  working with Port, it covers signing up and connecting Port's MCP server.
- If Port's MCP server is connected, this skill can use it to check what
  already exists (`list_blueprints`) and apply the resulting blueprint,
  relation, and property changes directly (`upsert_blueprint`), rather than
  just handing you JSON to apply yourself. Search
  `search_port_knowledge_sources` for anything this skill doesn't cover.

## How to build it

1. **Start from what Port already gives you.** Every account ships built-in
   blueprints (`_user`, `_team`, `_scorecard`, and others) that you extend,
   not replace. See [references/default-blueprints.md](references/default-blueprints.md).
2. **Design the core layer before the provider layer.** Model your
   organization's own shape first (organization, team, service), then relate
   it to provider-specific blueprints your integrations create (GitHub,
   GitLab, Jira, ...), rather than duplicating provider data into your core
   blueprints. See [references/reference-architecture.md](references/reference-architecture.md)
   for a full worked example.
3. **Model hierarchy with a self-relation, not one blueprint per tier.** A
   `parent_team` relation on `_team` handles arbitrary org depth. See
   [references/relations-and-hierarchy.md](references/relations-and-hierarchy.md).
4. **Use ownership instead of a custom team relation.** Port's built-in
   `$team` field already rolls up into `_team` aggregations for free. See
   [references/ownership.md](references/ownership.md).
5. **Add mirror and aggregation properties, not duplicated data.** Mirror a
   single related value onto its source; aggregate across many related
   entities on the blueprint that sits above them. For the JSON shape, see
   `port-blueprints`' [references/calculation-properties.md](../port-blueprints/references/calculation-properties.md);
   for which one to use and where to put it, see
   [references/mirror-vs-aggregation.md](references/mirror-vs-aggregation.md).
6. **Write it as an ontology, not a schema.** Descriptions, relation titles,
   and typed properties are what let an agent understand the graph instead
   of just enumerating it. See [references/ontology.md](references/ontology.md).
7. **Decide integration vs. MCP connector per data source.** Only data that
   needs relations, ownership, or scorecards belongs in the lake as ingested
   entities; everything else can stay a live MCP fetch. See
   [references/ingestion-strategy.md](references/ingestion-strategy.md).

## Examples

- [assets/team-hierarchy-patch.json](assets/team-hierarchy-patch.json): adds
  a `parent_team` self-relation and mirror property to `_team`.
- [assets/service-github-mirrors-patch.json](assets/service-github-mirrors-patch.json):
  relates `service` to `githubRepository` and mirrors its key fields.
- [assets/team-aggregation-patch.json](assets/team-aggregation-patch.json):
  adds an aggregation property rolling up owned services onto `_team`.

## Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Tried to delete or fully redefine `_user`/`_team` | System blueprints can't be deleted, only extended | `PATCH` in new relations only; leave the protected schema alone |
| `service` has no `team` relation and it seems wrong | Port uses built-in ownership (`$team`), not a custom relation, for this | Set `ownership` on `service`, don't add a redundant relation |
| One blueprint per org-hierarchy tier (team, group, division, org) | Hierarchy modeled as a chain of distinct blueprints instead of a self-relation | Use a single `parent_team` self-relation on `_team`, extensible to any depth |
| Same repo/PR data duplicated on two different blueprints | Two integrations model the same real-world thing separately | Map by property into the existing blueprint instead of creating a second one |
| Agent can't tell which of several relations to a blueprint is which | Relations exist but have generic titles like `team` or `service` | Give each relation a semantic title (`Owned by`, `Runs in`, `Depends on`) |

## Quick reference

- Core layer first (organization, team, service), provider layer relates to
  it, never duplicates it.
- Hierarchy: one self-relation (`parent_team`), not one blueprint per tier.
- Ownership over relations: use `$team`, don't hand-roll a team relation.
- Mirror = one related value, surfaced as-is. Aggregation = computed across
  many, placed on the higher-abstraction blueprint.
- An ontology has descriptions, semantic relation titles, and typed
  properties; a schema is just field names.
- Integration = persistent, related, governed data. MCP connector = live,
  on-demand, unmodeled data. Use both, for different data.
