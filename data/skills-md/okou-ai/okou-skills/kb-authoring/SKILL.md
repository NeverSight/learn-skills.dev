---
name: kb-authoring
description: Write or update knowledge base articles, FAQs, troubleshooting guides, and known-issue docs.
---

## Article Anatomy

### Mandatory Components

Every knowledge base article includes:

1. **Title**: Outcome-oriented or symptom-oriented. Written in the language a customer would type into a search bar -- never internal jargon.
2. **Summary**: 1-2 plain-language sentences stating what the article covers and who benefits from it.
3. **Content body**: Organized by article type (see below).
4. **Cross-references**: Links to companion articles for adjacent topics.
5. **Metadata**: Category, tags, intended audience, last-modified date.

### Formatting Standards

- **Headings (H2, H3)**: Create a scannable outline so readers can jump to the relevant section.
- **Numbered lists**: For ordered procedures where sequence matters.
- **Bullet lists**: For unordered sets of items or options.
- **Bold text**: For UI labels, critical terms, and points of emphasis.
- **Code blocks**: For commands, API payloads, error strings, and configuration snippets.
- **Tables**: For side-by-side comparisons, option matrices, and reference data.
- **Callouts / admonitions**: For warnings, tips, and must-read caveats.
- **Paragraph length**: Cap at 2-4 sentences. Dense paragraphs drive readers away.
- **Section discipline**: One concept per section. If a section serves two purposes, split it.

## Making Articles Findable

An article that cannot be discovered through search is an article that does not exist.

### Title Construction

| Effective Title | Ineffective Title | Rationale |
|-----------------|-------------------|-----------|
| "Set up SSO with Okta" | "SSO Configuration" | Names the specific tool customers search for |
| "Fix: Dashboard displays blank page" | "Dashboard Problem" | Mirrors the exact symptom customers experience |
| "API rate limits and quota reference" | "API Details" | Contains the precise terms people query |
| "Error: 'Connection refused' during data import" | "Import Errors" | Includes the literal error string customers paste into search |

### Keyword Strategy

- **Embed exact error messages**: Customers frequently paste error text directly into search fields.
- **Write in the customer's dialect**: "can't log in" outperforms "authentication failure" for discoverability.
- **Cover synonyms**: "delete / remove", "home page / dashboard", "download / export".
- **Offer alternate framings**: Address the same problem from multiple angles in the summary.
- **Tag by product surface**: Categories and tags should reflect the customer's mental model, not the engineering org chart.

### Opening Line Patterns

Anchor every article with a first sentence that restates the task or problem in everyday language:

- **Procedural**: "Follow these steps to [accomplish X]."
- **Diagnostic**: "Seeing [symptom]? This article walks through the fix."
- **Factual**: "[Question phrased as a customer would ask]? Here is the answer."
- **Advisory**: "Some users encounter [symptom]. Here is what is happening and how to work around it."

## Article Blueprints

### Procedural (How-To) Articles

**Goal**: Walk a customer through a task from start to finish.

```
# How to [accomplish task]

[Summary: what this covers and when you would need it]

## Before You Begin

- [Prerequisite 1]
- [Prerequisite 2]

## Instructions

### Step 1: [Action verb phrase]
[Precise instruction with path: Settings > Integrations > API Keys]

### Step 2: [Action verb phrase]
[Instruction, including what the user should see after completing this step]

## Confirm Success

[How to verify the task completed correctly]

## Troubleshooting

- [Potential hiccup]: [Resolution]

## See Also

- [Related article links]
```

**Guidance:**
- Open every step with a verb.
- Specify navigation paths explicitly: "Go to Settings > Team > Roles."
- Describe expected outcomes at key checkpoints: "A green banner confirms the save."
- Validate instructions against a recent ticket resolution or by walking through them yourself.

### Diagnostic (Troubleshooting) Articles

**Goal**: Help a customer identify and resolve a specific malfunction.

```
# [Problem statement matching what the user observes]

## What You See

- [Observable symptom 1]
- [Observable symptom 2]

## Why This Happens

[Concise, jargon-free explanation of the root cause]

## How to Fix It

### Fix 1: [Most likely resolution]
[Step-by-step instructions]

### Fix 2: [Alternate resolution if Fix 1 does not apply]
[Step-by-step instructions]

## Preventing Recurrence

[Configuration change or practice that avoids this in the future]

## Need More Help?

[How to contact support]
```

**Guidance:**
- Organize by symptoms first -- that is what customers search for.
- Present the most probable fix before alternatives.
- Always include a "Need more help?" escape hatch pointing to support.
- If the technical cause is complex, keep the customer explanation simple.

### Quick-Answer (FAQ) Articles

**Goal**: Deliver a concise response to a common question.

```
# [Question in the customer's natural phrasing]

[Direct answer: 1-3 sentences]

## Additional Context

[Deeper explanation, edge cases, or nuance if needed]

## Related Questions

- [Link to related FAQ 1]
- [Link to related FAQ 2]
```

**Guidance:**
- Answer the question in the very first sentence.
- If the answer requires a multi-step walkthrough, it belongs in a how-to article, not an FAQ.
- Interlink related FAQs so customers can self-serve adjacent questions.

### Known-Issue Advisories

**Goal**: Document an active bug or limitation along with its current status and any available workaround.

```
# [Known Issue]: [Brief description]

**Status:** [Investigating / Workaround Available / Fix Underway / Resolved]
**Who is affected:** [Scope]
**Last updated:** [Date]

## What Users Experience

[Description of the observable behavior]

## Workaround

[Step-by-step workaround, or "No workaround is currently available."]

## Resolution Timeline

[Estimated fix date or current engineering status]

## Change Log

- [Date]: [Update summary]
```

**Guidance:**
- Keep the status field current -- stale status information erodes trust faster than almost anything else.
- Update the article the moment a fix ships and mark it Resolved.
- Leave resolved advisories published for at least 30 days so customers still searching old symptoms can find closure.

## Content Lifecycle and Maintenance

Knowledge bases decay without active stewardship. Follow this cadence:

| Activity | Cadence | Owner |
|----------|---------|-------|
| **Peer review of new articles** | Before every publication | Author + subject-matter expert |
| **High-traffic article accuracy audit** | Quarterly | Support team |
| **Stale content detection** | Monthly | Flag anything untouched for 6+ months |
| **Known-issue status refresh** | Weekly | Update every open advisory |
| **Effectiveness review** | Monthly | Examine helpfulness ratings, bounce rates, and search-to-click ratios |
| **Coverage gap analysis** | Quarterly | Identify top ticket drivers that lack corresponding KB articles |

### Article States

1. **Draft**: Written, pending review
2. **Live**: Published and accessible to customers
3. **Flagged**: Marked for revision due to product changes, user feedback, or age
4. **Archived**: Retired from customer view but retained internally for reference
5. **Deleted**: Permanently removed from the knowledge base

### Update vs. Create Decision Framework

**Revise an existing article when:**
- A product update has changed the steps but the topic is the same
- The article is fundamentally sound but missing a detail
- Customer feedback points to a confusing section
- A superior workaround or solution has been discovered

**Write a new article when:**
- A new feature or product area has no documentation
- A closed ticket reveals a topic with zero KB coverage
- An existing article has grown unwieldy and should be split
- A distinct audience needs the same information presented differently

## Taxonomy and Cross-Linking

### Recommended Category Hierarchy

Structure the knowledge base around how customers navigate, not how the organization is structured:

```
Getting Started
  Account creation and setup
  Initial configuration
  Quickstart walkthroughs

Product Capabilities
  [Capability area A]
  [Capability area B]
  [Capability area C]

Integrations
  [Integration A]
  [Integration B]
  API reference

Problem Solving
  Frequent errors
  Performance and reliability
  Active known issues

Billing and Account Management
  Plans and pricing
  Payment and invoicing
  Account settings
```

### Cross-Linking Principles

- **Diagnostic to procedural**: "For setup instructions, see [How to configure X]."
- **Procedural to diagnostic**: "Running into errors? See [Troubleshooting X]."
- **FAQ to in-depth article**: "For a complete walkthrough, see [Guide to X]."
- **Advisory to workaround**: Minimize the number of clicks between problem identification and resolution.
- **Prefer relative links**: They survive reorganizations better than absolute URLs.
- **Avoid gratuitous circular links**: A linking to B and B linking back to A is only justified when both are genuine entry points.

## Guiding Principles

1. Write for the frustrated customer who is mid-search for an answer -- be direct, specific, and immediately helpful.
2. Every article must be discoverable using the words a real customer would type.
3. Validate your work: follow the steps yourself or have someone unfamiliar with the topic attempt them.
4. Maintain focus: one problem, one resolution per article. Split when scope creeps.
5. Tend the garden aggressively: an outdated article is more harmful than a missing one.
6. Track the gaps: every ticket that could have been deflected by an article represents a content opportunity.
7. Measure outcomes: articles with low traffic, poor ratings, or no ticket-deflection impact need rework or retirement.
