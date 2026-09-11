---
name: segmentation
description: Write AI segmentation prompts that divide prospects into campaign segments. Creates audience description and segment-specific criteria for an AI segmentation step. Use when setting up AI segmentation for a campaign. Triggers on "write segmentation", "segment contacts", or when dispatched by campaign-planning.
model: sonnet
thinking: true
---

# Segmentation Skill

Write the audience description and segment-specific prompts for AI segmentation. These prompts feed any segmentation step that routes prospects into mutually exclusive audience segments.

## Output Contract

`segmentation.md` must follow a fixed structure so downstream campaign tooling can parse it reliably. Hard rules this skill must honor:

- `## Default Segment` H2 (or legacy `## General Audience`) - its body is the general audience description for the Default / catch-all segment.
- `## Segments` H2 wraps all audience-segment H3s.
- Each audience segment is `### Segment N: {Name}` (or `### {Name}`). Authors may write `Segment N:` prefix for organization; tooling strips it before slugifying.
- The canonical name slug (`re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")`) MUST match the segment folder's slug. Mismatches warn and leave the segment with an empty description.
- Always create the `0 - default/` folder alongside the numbered segments. Audience segments are `1 - {slug}/`, `2 - {slug}/`, etc.
- Optional `## Segmentation Mode` H2 selects `ai` (default) or `percentage`. In `percentage` mode each `### Segment N` carries a `- **Weight**: N` line (int 1-100) instead of criteria, and so does `## Default Segment` (the Default is one of the test arms - use it as the baseline/control); weights of ALL arms including the Default must sum to exactly 100, and tooling records a percentage weight per arm. See the Segmentation Modes section below.

## Required Context

1. **Read `plan.md`** from the plan folder - Segment definitions and angles
2. **Read `qualification.md`** from the plan folder (if exists) - Audience description to reuse, criteria to NOT repeat
3. **Read `search-strategy.md`** from the plan folder - Search filters already applied. Never restate any of these dimensions in segment criteria.
4. **Read `{workspace}/research.md`** - Client overview, ICP details (`{workspace}` = the client campaign workspace, default `./cold-email/{slug}/` under the current directory)

## Segmentation Modes

A campaign is in exactly one mode (set by `## Segmentation Mode`, default `ai`):

- **`ai` (sub-ICP segmentation)** - the normal mode. Contacts are assigned by AI to the segment whose criteria they match. Each `### Segment N` H3 holds detectable criteria. This is what the rest of this skill describes.
- **`percentage` (sequence A/B test)** - contacts are distributed **randomly** across the arms by weight, and each arm runs a totally different email sequence (authored in its own folder). Used to test entire sequences against each other. There are **no criteria** - each `### Segment N` carries only a `- **Weight**: N` line, and so does `## Default Segment` - the Default is one of the test arms, used as the baseline/control variant whenever the test has one. The weights of ALL arms - numbered plus the Default - must sum to exactly 100.

The two modes are mutually exclusive - never mix percentage arms with AI-criteria segments in one campaign. When dispatched by `campaign-planning`, follow the mode declared in `plan.md`.

## Core Rules

- **Write short, trust the AI** - The segmentation AI is intelligent. Describe each segment in a sentence or two of plain language and let it route. Don't hand it exhaustive title lists or keyword tables - a clear picture of the persona is enough.
- **Never repeat the search filters** - the search strategy / filters already bound the list (headcount, geography, titles, seniority, industries). Don't restate any of it in the audience description or segment criteria. Segments split the audience by something the filters didn't already pin down - usually persona, role focus, or company type - never by re-stating a filter dimension.
- **Do NOT repeat qualification criteria** - If qualification.md exists, reuse only its audience description. Don't duplicate any of its dis/qualification criteria.
- **Segments must be mutually exclusive** - (AI mode) Each contact fits exactly one segment. Keep the line that distinguishes them crisp.
- **Cover the full audience** - (AI mode) Every qualified contact should land somewhere; the Default segment catches whatever doesn't match a numbered one.
- **Default segment = the general audience description** - The `## Default Segment` body is NOT catch-all criteria. Write it as the short, general audience description (persona + org type only, no filters). The segmentation AI surfaces it as the campaign's overall audience description, so keep it broad and brief - no headcount, geography, value-prop, or "doesn't fit the above" language.
- **Skill scope is description + criteria only** - Write the audience description and segment-specific criteria. A surrounding system prompt (if any) is tool-side; do not invent a full prompt template here.
- **Percentage mode carries no criteria** - In `percentage` mode, skip all criteria. Write only the audience description (still used by qualification) and a `- **Weight**: N` per arm. Assignment is random, so mutual-exclusivity/coverage rules don't apply.
- **Reasoning should be citable** - (AI mode) Write criteria around concrete, observable signals the model can actually cite (role focus, company type, stage) rather than vague vibes - that makes routing reasons legible and auditable when a tool stores them.

## Workflow

### Step 1: Load Context
- [ ] Read plan.md for segment definitions
- [ ] Read qualification.md (if exists) for audience description and criteria to avoid repeating
- [ ] Read client context and research

### Step 2: Write Segmentation Prompts

**Audience Description:**
- Reuse from qualification.md if it exists; otherwise one short sentence.
- No filter dimensions (headcount, geography, titles, industries).

**Segment Criteria:**
- One short section per segment from plan.md - a sentence or two on who belongs, the persona not a keyword list.
- Detectable from a LinkedIn profile + company data. Make the distinction crisp, then trust the AI to handle the edges.

### Step 3: Write segmentation.md

**AI mode (default):**

```markdown
# Segmentation Prompt

## Audience Description
[Reuse from qualification.md or write new - short description of target audience]

## Segments

### Segment 1: [Name from plan.md]
[Criteria for assigning contacts to this segment - what makes them belong here]

### Segment 2: [Name from plan.md]
[Criteria for this segment]

### Segment 3: [Name from plan.md]
[Criteria for this segment]

## Default Segment
[The general audience description: a short, plain statement of who the whole audience is - persona + org type only, e.g. "Financial advisors and wealth managers at independent RIAs and advisory practices". Very short and general: NO criteria, filters, headcount, geography, or "doesn't fit the above" language. The segmentation AI surfaces this as the campaign's general audience description. Maps to the local `0 - default/` folder.]
```

**Percentage mode (sequence A/B test):**

```markdown
# Segmentation Prompt

## Segmentation Mode
percentage

## Audience Description
[Reuse from qualification.md - applies via qualification; same as AI mode]

## Segments

### Segment 1: [Arm name from plan.md]
- **Weight**: 33

### Segment 2: [Arm name from plan.md]
- **Weight**: 33

## Default Segment
- **Weight**: 34

[The baseline / control arm. Put the control sequence here - the one the other arms are measured against. The Default is a real A/B arm and gets its weighted share of traffic.]
```

The Default is **one of your A/B arms** in percentage mode - use it as the baseline / control variant (the one you measure the other arms against). It is always active, so it can't be a weightless catch-all; rather than waste it, give it the control sequence. Like any arm it carries its own `- **Weight**:`, and the weights of ALL arms - numbered **plus** the Default - must be integers summing to exactly 100. (Omit the Default's weight line and tooling can back-fill the remainder `100 - sum(arms)` instead, so you can also list arms summing to ≤99 and let the Default absorb the rest.) Each arm name still has to slugify to its `N - {slug}/` folder. No criteria - the arm's full email sequence lives in its own segment folder.

### Step 4: Create Segment Folders

Always scaffold a `0 - default/` folder in addition to the numbered audience segments. The default folder holds the catch-all / general-audience copy for the Default segment. Its numeric prefix `0` sorts it first and marks it as the default segment folder.

```
{plan_folder}/0 - default/
{plan_folder}/1 - {segment-slug}/
{plan_folder}/2 - {segment-slug}/
{plan_folder}/3 - {segment-slug}/
```

Slug format for audience segments: lowercase, hyphens, no special characters. Derived from segment name. The default folder is always named `0 - default` (literal, no variation).

## Output Handling

### Workflow mode (plan folder provided):
1. Write `segmentation.md` to the plan folder root
2. Create segment subfolders
3. Confirm: "Segmentation saved. Created segment folders: [list]"

### Standalone mode:
1. Return the output inline to the user

## Segment Mapping

How `segmentation.md` maps to local folders and routing behavior (tool-neutral):

**AI mode:**
- Audience description / `## Default Segment` body -> general audience description used for campaign-wide routing context; local folder `0 - default/`.
- Each numbered `### Segment N` -> matching `N - {slug}/` folder and an AI-criteria segment. Assignment uses the written criteria.
- Default remains the catch-all when a contact does not match a numbered segment; still write its body as the short general audience description, not "everyone else" criteria.

**Percentage mode (sequence A/B test):**
- Each numbered arm and the Default are percentage-weight arms. No AI criteria prompts - contacts distribute by weight only.
- Default is a real arm (baseline/control when you have one), not a weightless catch-all. All arm weights including Default must sum to exactly 100.
- Audience description still applies via qualification.
- Mode is fixed for the campaign plan - do not mix AI-criteria segments with percentage arms in one plan.
