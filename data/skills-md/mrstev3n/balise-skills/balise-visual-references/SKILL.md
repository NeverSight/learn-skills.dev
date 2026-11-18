---
name: balise-visual-references
description: Finds, selects, and analyzes visual references for products, interfaces, brands, websites, decks, campaigns, motion, and specific UI patterns. Use when inspiration, benchmarking, art direction, or pattern research is needed; when the user wants sources and search terms to explore; or when supplied screenshots, recordings, links, and examples must be translated into original design principles rather than copied.
---

# Visual References

Build a focused visual-reference set, then turn the selected examples into transferable design principles. Match the research method to the available capabilities and evidence. Never imply that a page, image, interaction, or recording was inspected when it was not.

## Choose the research mode

- Use **direct research** when a reliable browsing or computer-use capability is available and the user wants the agent to locate and inspect references.
- Use **guided selection** when the user wants to explore personally or when direct visual browsing is unavailable.
- Use a **hybrid workflow** when source discovery can be automated but final visual selection should remain with the user.
- Infer the mode when the request or available capabilities make it clear. Ask one concise question only when the choice materially changes the result.

## Use the bundled catalog

1. Run `scripts/search_catalog.py` to shortlist sources without loading the complete catalog.
2. Read [taxonomy.md](references/taxonomy.md) when the request spans several deliverables, patterns, regions, formats, or levels of detail.
3. Read [source-catalog.json](references/source-catalog.json) only when maintaining the catalog or examining a shortlisted source in depth.
4. Treat categories as cumulative facets. A source may support several deliverables and patterns.
5. Recheck live facts such as access, filters, pricing, content, or integrations before presenting them as current.

Resolve resource and script paths relative to this skill directory.

```bash
python3 scripts/search_catalog.py --deliverable mobile-app --pattern navigation
python3 scripts/search_catalog.py --deliverable website --granularity component --json
```

Use `--require-all-facets` for a strict intersection. Keep the default ranked union when complementary sources are useful.

## Frame the research target

Extract the following from the brief:

1. deliverable: what is being designed;
2. pattern: the visual or interaction problem to study;
3. granularity: system, page, section, screen, component, flow, interaction, or asset;
4. context: audience, market, industry, tone, region, and constraints;
5. evidence format: screenshots, video, live sites, cases, analyses, flows, or templates;
6. intended decision: what the references should help the user decide.

Select two to four complementary sources by default. Prefer sources that match both the deliverable and the requested pattern over popular but generic galleries.

## Conduct direct research

When browsing is available:

1. Use the environment's approved browsing or computer-use capability and follow its active operating instructions.
2. Open the exact source URL and inspect visible state before interacting.
3. Use focused search, filters, archives, categories, and detail pages instead of broad scraping.
4. Capture the smallest view that preserves useful context:
   - a page or screen for composition and hierarchy;
   - a section or component with enough surroundings to explain its role;
   - a sequence for flows, motion, or state changes;
   - a system view for recurring visual grammar.
5. Collect three to eight strong references unless the brief requires another amount. Stop when new examples repeat an established pattern.
6. Record the source, exact URL, title, consultation date, observed pattern, and selection reason.
7. Save captures only in the active project or an explicitly requested destination.

Do not bypass authentication, paywalls, CAPTCHAs, regional restrictions, or safety warnings. Use an accessible alternative when it can satisfy the same need.

## Guide manual selection

When the user will inspect sources personally:

1. Recommend three to six complementary sources matched to the brief.
2. For each source, provide:
   - why it matches;
   - the exact starting URL;
   - useful categories, filters, or search terms;
   - the page, project, screen, component, or interaction to target;
   - what to capture and how much context to retain;
   - relevant access or freshness notes.
3. Provide verified direct resource links when available. Otherwise give a concise navigation route instead of inventing URLs.
4. Ask the user to return the chosen screenshots, recordings, or URLs.
5. Treat the initial output as a research itinerary, not a completed visual audit.

Use this handoff format:

| Source | Why it fits | Starting point | Search terms or filters | What to capture | Access notes |
| --- | --- | --- | --- | --- | --- |

## Analyze supplied references

For each reference, separate:

- **Observation**: what is visibly present in composition, hierarchy, typography, color, imagery, motion, copy, or interaction.
- **Transferable principle**: why the observed choice works in its original context.
- **Project application**: how the principle could answer the current brief.
- **Boundary**: what should not be copied literally and what depends on another audience, medium, brand, or technical context.

Then compare the set:

- identify recurring patterns and meaningful disagreements;
- distinguish structural principles from stylistic decoration;
- note states, responsiveness, accessibility, content, or interaction behavior that static captures cannot prove;
- recommend one direction or a small set of genuinely distinct directions.

Do not reproduce distinctive protected expression, brand assets, copy, or proprietary screens. Use references to support original design decisions.

## Deliver the result

Return a concise reference brief containing:

1. the interpreted research target;
2. sources selected and why;
3. captures or URLs actually inspected;
4. one observation and transferable principle per reference;
5. cross-reference patterns, tensions, and opportunities;
6. recommended application to the project;
7. access, provenance, freshness, and verification limits.

For guided selection, deliver the itinerary first and complete the brief only after the user supplies the selected material.

## Maintain the catalog

Keep `references/source-catalog.json` canonical. Use the vocabulary in [taxonomy.md](references/taxonomy.md), avoid duplicate URLs, replace stale access facts, and validate changes with:

```bash
python3 scripts/validate_catalog.py
```
