---
name: tool-skill-development
description: "create a skill", "build a new skill", "skill template", "skill best practices" — guidance for creating well-structured, agent-executable skills
version: 1.0.0
author: hungv47
tags: [tooling, skill-creation, best-practices, meta]
---

# Skill Development Guide

**Meta-skill** — Create skills that agents can execute reliably, every time.

## Inputs Required

- Purpose: What should this skill accomplish?
- Domain: What area does this skill operate in?
- Chain position: Does it connect to other skills? What does it read/produce?

## Output

`skills/[skill-name]/SKILL.md` — A complete, self-contained skill file following the canonical structure.

Optionally: `skills/[skill-name]/references/*.md` for domain knowledge supplements.

## Chain Position

**Standalone** — this skill can be invoked independently. It does not read or produce artifacts in any chain.

## Before Starting

### Required Artifacts

None — this skill works from user requirements.

### Step 0: Interview

Before creating a skill, ask these questions if the user hasn't provided the information:

1. **What does this skill produce?** (Single artifact — one skill, one output)
2. **What does it need to start?** (Prerequisites — files, user input, context)
3. **Where does it sit in a workflow?** (Before/after other skills, or standalone)
4. **What makes the output good vs. bad?** (Quality criteria — must be falsifiable)
5. **Who triggers this skill and how?** (Trigger phrases — verbs, not nouns)

## Step 1: Define the Skeleton

Every well-structured skill follows this anatomy:

```
SKILL.md
├── YAML Frontmatter (name, description/triggers, version, author, tags)
├── Title + Subtitle (one-sentence purpose, track position if applicable)
├── Inputs Required (explicit file paths or user input needed)
├── Output (exact artifact path)
├── Chain Position (Previous → This → Next, or Standalone)
├── Before Starting
│   ├── Required Artifacts (STOP/INTERVIEW/SKIP table)
│   ├── Optional Artifacts (enrichment, not blocking)
│   └── Step 0: Product Context check (if marketing skill)
├── Numbered Steps (each producing tangible intermediate output)
├── Artifact Template (full markdown structure as code block)
├── Quality Gate (3-5 falsifiable checks)
├── Worked Example (complete, not excerpted)
├── Next Step (what to run after this skill)
└── references/ (domain knowledge, frameworks, rubrics — optional)
```

## Step 2: Write the Frontmatter

```yaml
---
name: [skill-name]
description: "[trigger phrase 1]", "[trigger phrase 2]" — [one-line description]
version: 1.0.0
author: [author]
tags: [relevant, tags]
---
```

**Trigger phrase rules:**
- Use verbs, not nouns: "diagnose the problem" > "marketing diagnosis"
- Include 2-4 unique anchor phrases that no sibling skill shares
- Put the most distinctive phrases first in the description
- Test: could another skill reasonably match these phrases? If yes, differentiate.

## Step 3: Define Prerequisites with STOP/INTERVIEW/SKIP

Use this table format in the "Before Starting" section:

```markdown
### Required Artifacts
| Artifact | Source | If Missing |
|----------|--------|------------|
| `[file].md` | [source-skill] | **STOP.** "[Run source-skill first.]" |
| `[file].md` | [source-skill] | **INTERVIEW.** [Ask N questions inline to bootstrap.] |

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `[file].md` | [source-skill] | [What it adds if present] |
```

Three standard responses:
- **STOP** — hard dependency, cannot proceed without this artifact. Tell user exactly which skill to run.
- **INTERVIEW** — can bootstrap inline by asking the user questions. Use for product-context.md or similar foundational context.
- **SKIP** — nice-to-have enrichment. Proceed without it, note what's missing.

## Step 4: Write the Steps

Each step must:
1. **Start with a clear action verb** (Scan, Analyze, Generate, Validate)
2. **Produce a tangible intermediate output** (a list, a table, a decision)
3. **Include WebSearch directives inline** where external data is needed:
   ```
   Search: "[specific query template]" — [what you're looking for]
   ```
4. **Be self-contained** — an agent should be able to execute the step without referring back to other steps

**Step-writing anti-patterns to avoid:**
- Steps that say "analyze" without specifying what to look for
- Steps that produce no visible output
- Steps that require judgment calls without criteria (provide rubrics)
- Steps that bundle multiple unrelated actions

## Step 5: Create the Quality Gate

Quality gate checks must be **falsifiable** — answerable yes/no by looking at the artifact with zero judgment required.

**Good checks:**
- "Contains two numbers (current state AND target state)"
- "Every hypothesis follows If/Then/Because format"
- "Every score has a one-sentence evidence citation"
- "A/B variant changes exactly ONE element"

**Bad checks (never use these):**
- "Is well-written"
- "Is compelling"
- "Provides actionable insights"
- "Is comprehensive enough"

Write 3-5 checks. Each should catch a specific failure mode you've seen or can anticipate.

## Step 6: Write the Artifact Template

Provide the FULL artifact structure as a markdown code block. This is the few-shot example agents will follow.

```markdown
---
skill: [skill-name]
version: 1
date: [today's date]
status: draft
---

# [Artifact Title]

## Section 1
[What goes here — be specific about structure]

## Section 2
[Table format? Bullet list? Prose? Specify exactly]

## Next Step
Run `[next-skill]` to [what happens next].
```

**Critical rule:** The template must be COMPLETE, not excerpted. Never use "..." or "[more items]". Agents use templates as few-shot examples — partial templates produce partial output.

Include artifact frontmatter with:
- `skill:` — which skill produced this
- `version:` — starts at 1, increments on re-runs
- `date:` — creation date
- `status:` — draft or final

## Step 7: Write the Worked Example

Create a FULL worked example showing the complete artifact with realistic data. This is the most important part of the skill for agent execution quality.

Rules:
- Use realistic domain data (not placeholder "Lorem ipsum")
- Show EVERY section from the template filled in
- Include edge cases where relevant (e.g., an item that fails a quality check)
- Never truncate with "..." — show the full artifact

## Step 8: Add Cross-Skill Integration (if applicable)

If this skill can be called from multiple places or feeds into multiple downstream skills, add a "Cross-Skill Integration" section:

```markdown
## Cross-Skill Integration

### Called FROM
- `[skill-name]`: [context — what input it provides, what output is expected]

### Feeds INTO
- `[skill-name]`: [what artifact it reads, what it does with it]
```

This prevents horizontal skills from floating disconnected in the framework.

## Step 9: Validate Against Principles

Before finalizing, check the skill against these 10 principles:

- [ ] **One skill = one artifact.** Single responsibility. Does this skill try to do two jobs? Split if so.
- [ ] **Quality gates are falsifiable.** Every checkbox is yes/no with zero judgment. No subjective criteria.
- [ ] **"Before Starting" handles every prerequisite.** STOP, INTERVIEW, or SKIP — no ambiguity about what happens when a file is missing.
- [ ] **Worked example is FULL.** Not excerpted, not "...". Complete artifact from start to finish.
- [ ] **Trigger phrases are verbs.** Command language first, noun keywords second. No overlap with sibling skills.
- [ ] **Artifact ends with `## Next Step`.** Enables chaining even without a navigator.
- [ ] **WebSearch directives are inline.** At the point of need, not in a separate section.
- [ ] **References are for domain knowledge, not instructions.** Core workflow stays in SKILL.md. References are lookup tables, rubrics, examples.
- [ ] **Horizontal skills have integration points.** If called from multiple places, document WHERE it plugs in.
- [ ] **Version is set.** Semantic versioning in frontmatter.

## Step 10: Create Reference Files (if needed)

References supplement the skill with domain knowledge. They should contain:
- Lookup tables (e.g., scoring rubrics, benchmark data)
- Framework explanations (e.g., MECE principles, copywriting formulas)
- Extended examples beyond the worked example

References should NOT contain:
- Core workflow steps (those belong in SKILL.md)
- Instructions that override SKILL.md
- Duplicate content from SKILL.md

Place in `skills/[skill-name]/references/[name].md`.

## Quality Gate

- [ ] Skill follows the canonical skeleton structure (all sections present)
- [ ] Every prerequisite has explicit STOP/INTERVIEW/SKIP handling
- [ ] Quality gate contains only falsifiable checks (no subjective criteria)
- [ ] Worked example is complete (no "..." truncation, no "[more items]" placeholders)
- [ ] Trigger phrases in description are unique — no overlap with existing skills in the repository
- [ ] Artifact template includes frontmatter (skill, version, date, status)

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| **God skills** that try to do everything | Agent loses focus, output quality drops | Split into focused single-artifact skills |
| **Subjective quality gates** ("is it compelling?") | Agent can't self-evaluate, always passes | Rewrite as falsifiable yes/no checks |
| **Missing prerequisite handling** | Skill proceeds with generic output | Add STOP/INTERVIEW/SKIP table |
| **Excerpt-only examples** | Agents produce excerpt-quality output | Write complete worked examples |
| **Overlapping triggers** | Wrong skill activates | Audit triggers, add unique anchor phrases |
| **Instructions buried in references** | Agent may not read reference files | Keep workflow in SKILL.md, references for lookup only |
| **No Next Step** | Chain breaks, user doesn't know what's next | Always end artifact with `## Next Step` |
| **Abstract WebSearch directives** | Agent searches poorly | Provide specific query templates with placeholders |

## Worked Example

**Scenario:** User wants to create a skill called "competitor-analysis" that researches competitors.

### Output: `skills/competitor-analysis/SKILL.md`

~~~markdown
---
name: competitor-analysis
description: "analyze competitors", "competitive landscape", "competitor research" — systematic competitor analysis with positioning gaps
version: 1.0.0
author: hungv47
tags: [marketing, research, competitive-intelligence]
---

# Competitor Analysis

**Research** — Map the competitive landscape to find positioning gaps and stolen strategies.

## Inputs Required

- Product or company to analyze
- `.agents/mkt/product-context.md` (if available)

## Output

`.agents/mkt/competitor-analysis.md`

## Chain Position

**Standalone** — enriches mkt-icp-research and mkt-imc but not required by either.

## Before Starting

### Required Artifacts
| Artifact | Source | If Missing |
|----------|--------|------------|
| Product context | User or `product-context.md` | **INTERVIEW.** Ask: What do you sell? Who buys it? What problem does it solve? |

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `icp-research.md` | mkt-icp-research | Better understanding of what customers compare |

## Step 1: Identify Competitors

Ask the user: "Who are your top 3-5 competitors? Include direct competitors (same solution) and indirect competitors (different solution, same problem)."

If user doesn't know all competitors:

Search: "[product category] alternatives [year]" — find comparison/listicle pages
Search: "best [solution type] for [target audience]" — find what ICP actually considers
Search: site:g2.com "[product category]" — find rated alternatives

List competitors in a table:

| Competitor | Type | Why They Compete |
|---|---|---|
| [Name] | Direct / Indirect | [Same audience, different approach / Same solution, different segment] |

## Step 2: Analyze Each Competitor

For each competitor, research and document:

Search: "[competitor] pricing" — current pricing model
Search: "[competitor] reviews site:g2.com OR site:capterra.com" — customer sentiment
Search: "[competitor] vs" — see who THEY position against

Document:
- **Positioning:** How do they describe themselves? (Tagline, hero copy)
- **Pricing:** Model and approximate price points
- **Strengths:** What do reviewers praise? (Use real quotes)
- **Weaknesses:** What do reviewers complain about? (Use real quotes)
- **Audience:** Who are they targeting? (Job titles, company size)

## Step 3: Build Comparison Matrix

Create a feature/positioning matrix:

| Dimension | You | Competitor A | Competitor B | Competitor C |
|---|---|---|---|---|
| Primary audience | | | | |
| Price point | | | | |
| Key differentiator | | | | |
| Biggest weakness | | | | |
| Positioning angle | | | | |

## Step 4: Identify Gaps and Opportunities

Analyze the matrix for:
1. **Underserved segments:** Audiences no competitor targets well
2. **Feature gaps:** Capabilities no competitor offers
3. **Positioning gaps:** Messages no competitor owns
4. **Pricing gaps:** Price points with no options

## Step 5: Write Recommendations

For each gap, write a specific recommendation:
- What to do (action)
- Why it matters (evidence from research)
- How it connects to your positioning

## Artifact Template

```markdown
---
skill: competitor-analysis
version: 1
date: [today's date]
status: draft
---

# Competitive Analysis: [Product/Company]

## Competitors Identified

| Competitor | Type | Why They Compete |
|---|---|---|
| [Name] | [Direct/Indirect] | [Reason] |

## Competitor Deep Dives

### [Competitor A]
- **Positioning:** [Their tagline/hero message]
- **Pricing:** [Model and price points]
- **Strengths:** "[Real review quote]" — [Source]
- **Weaknesses:** "[Real review quote]" — [Source]
- **Audience:** [Who they target]

### [Competitor B]
[Same structure]

## Comparison Matrix

| Dimension | Us | Comp A | Comp B | Comp C |
|---|---|---|---|---|
| Primary audience | | | | |
| Price point | | | | |
| Key differentiator | | | | |
| Biggest weakness | | | | |

## Gaps & Opportunities

1. **[Gap type]:** [Description] — Evidence: [what research showed]
2. **[Gap type]:** [Description] — Evidence: [what research showed]

## Recommendations

1. [Specific action] — because [evidence]
2. [Specific action] — because [evidence]

## Next Step

Run `mkt-icp-research` to validate these gaps against real customer language, or `mkt-imc` to build messaging around identified positioning gaps.
```

## Quality Gate

- [ ] Every competitor has real pricing data or "not publicly available" noted (not guessed)
- [ ] Every strength/weakness cites a real review quote with source platform
- [ ] Comparison matrix has no empty cells (use "N/A" or "Unknown" with search attempted)
- [ ] Each recommendation traces to a specific gap found in research
- [ ] At least 3 competitors analyzed (minimum viable competitive view)

## Next Step

Use the output to inform `mkt-icp-research` (validate gaps against customer language) or `mkt-imc` (build positioning around gaps).
~~~

## Next Step

After creating a skill, test it by invoking it with a real scenario. Check that:
1. Prerequisites are handled correctly (try invoking without required artifacts)
2. Quality gate catches bad output (try producing output that violates a check)
3. Worked example matches the template structure exactly
4. Trigger phrases activate the right skill (test with ambiguous queries)
