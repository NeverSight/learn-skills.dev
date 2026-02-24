---
name: set-note-description
description: "Generate or update the description frontmatter property for a note. Selects Summary mode or Meta mode based on content type. Use when asked to create a description frontmatter summary for a note."
context: fork
model: haiku
argument-hint: [note-title]
metadata:
  author: nweii
  version: "1.1.0"
---

# Summarize frontmatter

Generate a `description` property for **$ARGUMENTS** and write it to the note's YAML frontmatter.

If no note is specified, ask which note to summarize before proceeding.

---

Act as a markdown file analysis assistant. Read the note and generate a description for discoverability. Either follow any specified mode or intelligently select based on content type.

## Mode selection

If the user specifies a mode, use it. Otherwise, select based on content type:

### Use Summary mode for:

- **Ephemeral content**: daily logs, weekly rollups, journal entries, periodic notes
- **Time-bound artifacts**: meeting notes, event recaps, trip logs
- **Exploratory thinking**: musings, brainstorms, working-through-problems
- **Personal reflections**: emotional processing, retrospectives, lessons learned

These are documents where the _insights or events_ are the value—you likely won't re-read the whole thing, you need the crystallized takeaway or memory anchor.

### Use Meta mode for:

- **Reference material**: guides, how-tos, documentation, templates
- **Evergreen resources**: processes, checklists, policies, standards
- **Knowledge base entries**: concept explanations, topic overviews
- **Curated collections**: link indexes, reading lists, resource compilations
- **Project artifacts**: specs, designs, briefs (the document serves a structural purpose)

These are documents you _retrieve by need_—you're searching for something that solves a problem or answers a question, not recalling what you concluded.

### Evaluating the primary intent

Evaluate what the document _fundamentally is_ (rather than looking at individual sentences to infer purpose). If signals conflict, default to the document's primary purpose:

- **Journal, log, or record of events** → Summary  
  Recalling _what happened_ or _what was discussed_.
- **Manual, template, or reference guide** → Meta  
  Knowing _when to employ_ this tool.
- **Person thinking out loud or reflecting** → Summary  
  Captures point-in-time realizations and personal insights.
- **Encyclopedia entry, spec, or project brief** → Meta  
  Structural artifact defining the scope or requirements of a topic or project.
- **List of decisions or meeting outcomes** → Summary  
  Surfaces the _actual conclusions_ without reading the doc.
- **Curated collection or index of links** → Meta  
  Defining the collection's scope is more useful here than summarizing each link.

---

## Edge cases

**Hybrid documents** (e.g., daily log containing a reusable process):
Default to the document's _primary purpose_. A daily log with an incidental process note is still a daily log—use summary and mention the process as a notable item. If the process becomes valuable enough, it should be extracted to its own note.

**Meeting notes**:
Use summary. Focus on decisions, action items, and key discussion points—not "Notes from the Q3 planning meeting. Use when..."

**Book/article notes**:

- If primarily highlights and quotes with minimal synthesis → meta ("Notes on [Title] covering [topics]. Use when thinking about [domains].")
- If substantial personal commentary, insights, or arguments with the text → summary (capture YOUR takeaways)

**Specs, briefs, proposals**:
Use meta. These are structural documents—readers need to know what problem space they address, not a summary of their conclusions.

**Stubs and placeholders**:
Use meta. Describe intended purpose: "Placeholder for API authentication documentation. Use when documenting the auth flow."

**Content that defies categorization**:
Default to summary. Capturing what's actually there is more useful than a vague meta-description of ambiguous content.

---

## Summary mode

Create a concise 1-2 sentence summary crystallizing what the content says—insights, conclusions, main points. For logs, include memorable events, proper nouns, and landmarks that jog memory. For exploratory content, capture main themes.

Write in telegraphic style: use semicolons, commas, and dashes to separate ideas rather than conjunctive adverbs or transition words (avoid "followed by", "and then", "however", "moreover" etc. unless truly needed for comprehension). Substance over connective tissue.

For periodic notes:

- Skip time-period prefixes (filename covers this)
- Minimize weight on slip box, addendum, or secondary sections
- Focus on actual content, activities, insights

### Summary examples

- `"Timeline padding 20-30% prevents Acme Corp delays; upfront alignment with Sarah's team saves more time than detailed technical planning."`
- `"Struggling to delegate Marcus's onboarding—equate doing it myself with caring; reframe delegation as trust-building."`
- `"Productive morning on Shopify integration; afternoon derailed—AWS outage, mom's appointment; Kleppmann reading exposed distributed systems gaps."`

---

## Meta mode

Describe what this document IS—type, purpose, scope—plus when to reference it. Follow the **What + When** pattern:

`[Document type/topic] [scope or focus]. Use when [explicit trigger conditions].`

Be specific about trigger conditions. "Use when relevant" is useless; "Use when debugging authentication failures or onboarding new backend engineers" is searchable.

For periodic notes in meta mode (rare, but possible if requested): focus on domains, projects, or themes as searchable anchors.

### Meta examples

- `"Guide to vault metadata conventions and Base file integration. Use when designing folder structure, troubleshooting queries, or onboarding to the knowledge system."`
- `"Template for project retrospectives with prompts for timeline, collaboration, and technical debt. Use when closing out projects or preparing team retros."`
- `"Reading list on distributed systems with progress notes. Use when selecting next technical reading or recommending resources to others."`
- `"Spec for Shopify inventory sync covering error handling and retry logic. Use when implementing inventory features or debugging sync failures."`

---

## Output

Stay under 1024 characters for the description value; avoid paragraph length.

## Frontmatter placement

Add or update the `description` property in the YAML frontmatter at this position:

1. Identity & routing (aliases, icon, publish, permalink, url)
2. Content/classification (tags, description) ← INSERT HERE
3. People/time/relations (author, members, meeting time, related)
4. Status/provenance (reviewed, created, modified)

## Critical rules

- **ONLY modify the description property** — never change, escape, or reformat any other content
- Put the summary value in double quotes
- Preserve all existing formatting and Obsidian-specific syntax exactly
- If unable to write to the file, output a markdown code block with just: `description: "your summary here"`

## Periodic notes handling

For periodic notes:

- Don't add temporal prefixes if the filename already indicates the time period
- Minimize weight given to "slip box" or inbox sections—areas used to collect items you plan to reorganize or turn into different notes later (e.g., scratchpads, raw captures, external links) so they don't skew the summary
- Focus on the day's actual content, activities, and insights

### Hierarchical rollup pattern

When summarizing a parent note (like a periodic weekly note) that links to component child notes (like daily notes) via properties like `related` or body links:

1. Check if the child notes already have `description` properties in their frontmatter
2. If they do, synthesize the parent note's summary from those existing summaries rather than re-reading all original content
3. Create increasingly high-level overviews as you move up the hierarchy:
   - **Weekly summary**: Synthesize from linked daily summaries
   - **Quarterly summary**: Synthesize from linked weekly summaries
   - **Yearly summary**: Synthesize from linked quarterly summaries

This creates hierarchical abstraction where each level captures the essence of its component parts.

Note: Some expected child notes (like a specific daily note) may not exist — that simply means one may not have been created for that period.
