---
name: signals-synthesis
description: Detect patterns across ingested signals and propose hypothesis candidates. Use for /synthesize workflows.
---

# Signals Synthesis Skill

Procedural guidance for synthesizing signals across Slack, Linear, HubSpot, transcripts, and other sources.

## When to Use

- Running `/synthesize [topic]`
- Running `/synthesize --all`
- Investigating persona-specific or source-specific patterns

## Inputs

- Topic or filter (`--persona`, `--source`, date range)
- Signal corpus in `pm-workspace-docs/signals/`
- Optional hypothesis index in `pm-workspace-docs/hypotheses/_index.json`

## Workflow

1. Load signals and apply requested filters.
2. Group by recurring problems, requested outcomes, and affected persona.
3. Separate open problems from tracked, in-progress, or resolved items.
4. Score signal strength:
   - `Strong`: 5+ occurrences, 3+ sources, multiple personas
   - `Moderate`: 3-4 occurrences, 2+ sources
   - `Weak`: 1-2 occurrences, single source
5. Match themes to existing hypotheses where possible.
6. Propose net-new hypotheses only when evidence is strong enough.

## Required Output

- Executive summary
- Theme clusters with evidence
- Signal strength table
- Existing hypothesis matches
- New hypothesis candidates
- Recommended actions and owners

## Save Location

- `pm-workspace-docs/research/synthesis/YYYY-MM-DD-[topic].md`

## Next Actions

- New strong pattern: `/hypothesis new [name]`
- Existing pattern strengthened: `/hypothesis validate [name]`
- Pattern ready for commitment: `/hypothesis commit [name]`

