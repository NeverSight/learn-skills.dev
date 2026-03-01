---
name: dial-your-context
description: Interactive session to create Instructions field content for a Sanity Agent Context MCP
---

# Dial Your Context

Help a user create the Instructions field content for their Sanity Agent Context MCP. The goal is a concise set of **pure deltas** — only information the agent can't figure out from the auto-generated schema.

## What you're building

The Agent Context MCP already provides the agent with:

- A compressed schema of all document types and fields
- A GROQ query tutorial (~194 lines)
- Response style guidance
- Tool descriptions for GROQ queries, semantic search, etc.

The Instructions field you're crafting gets injected as a `## Custom instructions` section between `## Response style` and `## Tools` in the MCP's instructions blob. It should contain **only what the schema doesn't make obvious**:

- Counter-intuitive field names (e.g., `body` is actually a slug, `hero` is a reference to `mediaAsset`)
- Second-order reference chains the schema doesn't connect (e.g., "to find products with Dolby Atmos, chain `product → productFeature` and match on the feature's `id` field — the schema shows each hop but not the full path")
- Data quality issues the schema can't reveal (e.g., "the `product` type has a `features` array but it's always empty — use `support-product` instead")
- Required filters the agent must always apply (locale, draft status, etc.)
- Known data gaps confirmed by the user (e.g., "the `subtitle` field is unused — ignore it")
- Query patterns for common use cases that aren't obvious from the schema
- Fallback strategies when primary approaches fail

**Never duplicate** what the schema already communicates clearly.

## Prerequisites

You need one of these to run this session:

**Path A — Write access (recommended):** A Sanity write token or the general Sanity MCP (OAuth). This lets you create a draft context doc, write instructions + filter to it during the session, and promote it to production when done. Production is never touched until you're ready.

**Path B — URL params only:** If no write access is available, you can use `?instructions=` and `?groqFilter=` URL query params on the MCP endpoint to test everything. At the end, provide the final content for the user to enter manually in Sanity Studio.

Both paths are safe — neither modifies the production agent during the session.

## Critical rules

1. **Pure deltas only.** If the schema makes it obvious, don't put it in Instructions.
2. **Never generalize from small samples.** Querying 3 docs and concluding "field X is always null" is the #1 failure mode. Every claim must be verified with the user before inclusion.
3. **The user knows their data.** Schema dialogue beats data exploration. Present the schema, ask questions, listen.
4. **Verify every claim with evidence.** For each line in the draft Instructions, show the query + result that supports it. The user confirms or corrects.
5. **Keep it concise and factual.** The compaction step (summarizing findings into Instructions) is where information gets lost or distorted. No creative interpretation. Short declarative sentences.

## Workflow

### Step 1: Connect & Clean Slate

**Goal:** Establish MCP access, set up a safe working environment.

Connect to the user's Sanity Agent Context MCP. Get the project ID, dataset, and slug from the user if not already known.

**Set up your working environment:**

**Path A (write access):** Create a new draft context doc by copying the existing one (if any) to a new slug like `tuning-draft`. All exploration and iteration happens against this draft — the production agent is untouched.

**Path B (no write access):** Use URL query params throughout the session:

- `?instructions=""` — forces a blank slate (ignores existing instructions)
- `?groqFilter=<expression>` — applies a filter without writing to the context doc

Check if the context document already has instructions content:

- If yes, present the existing instructions to the user verbatim
- Ask: "Do you want to keep any of this, or start fresh?"
- Let the user decide — don't assume existing instructions are wrong
- If they have existing instructions from a previous session, you'll verify and refine each finding rather than starting from scratch

Verify you can query the dataset by running a simple GROQ query like `*[0..2]._type` to confirm access.

**Output:** Confirmed MCP access, safe working environment established (draft doc or URL params), any existing instructions surfaced to user.

### Step 2: Schema Dialogue

**Goal:** Understand the dataset through conversation, not just exploration.

Retrieve the schema (the MCP provides this). Present the document types to the user in a clear list:

> Here are the document types in your dataset:
>
> - `article` (14 fields)
> - `author` (8 fields)
> - `category` (5 fields)
> - ...
>
> Which of these are the ones your agent will need to work with?

This is a **conversation**, not a monologue. Ask the user:

1. **Which types matter?** "Which of these will your agent need to query? Any types here that are internal/system types the agent should ignore?"
2. **What's misleading?** "Any field names that don't mean what they sound like? Fields that are unused or deprecated?"
3. **What are the relationships?** "How do these types connect? For example, do articles reference authors? How — direct reference, array of references, something else?"
4. **Any required filters?** "Does the agent need to always filter by locale, published status, or any other field?"
5. **What's the primary content language?** If i18n is involved, clarify the pattern.

**Suggest a filter.** The MCP supports a `groqFilter` — a full GROQ expression that scopes which documents the agent can access. This is high-leverage — it reduces noise significantly and prevents the agent from querying irrelevant types.

The filter is a GROQ expression string, not just a type list. This means you can carve out exactly the document set you want:

- Simple type filter: `_type in ["product", "support-article", "productFeature"]`
- Exclude drafts: `!(_id in path("drafts.**")) && _type in ["product", "article"]`
- Locale filter: `_type in ["product", "article"] && lang == "en-us"`
- Complex: `_type in ["product", "article"] && !(_id in path("drafts.**")) && defined(title)`

Based on the conversation, propose a filter:

> Based on what you've told me, I'd suggest this filter:
>
> ```
> _type in ["article", "author", "category", "tag"]
> ```
>
> This means the agent won't see `siteSettings`, `redirect`, `migration`, etc. Does that sound right?

**Apply the filter immediately.** Once the user agrees:

- **Path A (write access):** Write the `groqFilter` field to the draft context doc
- **Path B (URL params):** Add `?groqFilter=<expression>` to all subsequent MCP calls

All exploration from this point forward should use the agreed filter.

**Output:** A shared understanding of which types matter, known quirks, relationships, and an active filter. There's no point exploring types the production agent won't see.

### Step 3: Expected Questions

**Goal:** Get concrete examples of what the production agent will be asked.

Ask the user:

> What questions will people ask the agent that uses this context? Give me 5-20 examples — the more realistic, the better.

Examples might be:

- "Which speakers support Dolby Atmos?"
- "How do I fix WiFi connection issues?"
- "What's the return policy for refurbished products?"
- "Compare the features of product X and product Y"

These questions drive the exploration in Step 4. They tell you what query patterns actually matter.

For simple datasets, 5 questions is fine. For complex ones, push for 15-20.

**Output:** A numbered list of expected questions.

### Step 4: Explore & Verify

**Goal:** Answer each expected question using the MCP, track what works and what doesn't.

> **Steps 4–6 are iterative, not sequential.** Verify findings with the user as you go. Don't explore 15 questions, draft everything, then discover half your claims don't hold up.

Work through the expected questions one by one (or in logical groups). For each question:

1. **Write a GROQ query** to answer it
2. **Run the query** via the MCP
3. **Note the result** — did it work? Was the data what you expected?
4. **Track findings** in a running list:
   - ✅ Worked as expected (no instruction needed)
   - ⚠️ Worked but required non-obvious pattern (instruction needed)
   - ❌ Failed or returned unexpected results (investigate, then verify with user)

**Critical: Do not assume.** If a query returns empty results or unexpected data:

- Do NOT conclude "this field is always empty" from a small sample
- Instead, ask the user **immediately** — don't batch null-field findings: "When I query for X, I get Y. Is that expected? Is the data actually there?"
- The user confirms or explains the discrepancy

Track your findings in a simple table:

| #   | Question             | Query                                                    | Result               | Finding                                                    |
| --- | -------------------- | -------------------------------------------------------- | -------------------- | ---------------------------------------------------------- |
| 1   | "Recent articles"    | `*[_type == "article"] \| order(publishedAt desc)[0..4]` | ✅ 5 results         | Works with schema alone                                    |
| 2   | "Articles by author" | `*[_type == "article" && references(authorId)]`          | ⚠️ Empty             | Authors linked via `contributors[].person`, not direct ref |
| 3   | "Published only"     | `*[_type == "article" && status == "published"]`         | ❌ No `status` field | User confirms: use `!(_id in path("drafts.**"))` instead   |

**Adapt to scale:**

- Simple dataset (3-5 types, 5 questions): This step might take 10 minutes
- Complex dataset (50 types, 20 questions): Group related questions, explore systematically, but still verify each finding

**Output:** A findings table with verified results for each expected question.

### Step 5: Draft Instructions

**Goal:** Distill findings into concise, factual Instructions content.

Review the findings table from Step 4. Include **only** items marked ⚠️ or ❌ — things that required non-obvious patterns or failed with the obvious approach.

Write the Instructions as short, declarative statements organized by category:

```markdown
### Rules

- Always filter drafts: use `!(_id in path("drafts.**"))` — there is no `status` field
- Always include `[_lang == "en"]` for localized content unless user specifies otherwise

### Schema notes

- `contributors` on `article` is an array of objects with a `person` reference to `author` — not a direct author reference
- `hero` on `article` is a reference to `mediaAsset`, not an image field
- `body` on `page` is a Portable Text array, not a string — use `pt::text(body)` for plain text search

### Query patterns

- Articles by author: `*[_type == "article" && contributors[].person._ref == $authorId]`
- Published articles by date: `*[_type == "article" && !(_id in path("drafts.**"))] | order(publishedAt desc)`

### Known limitations

- `subtitle` field on `article` is unused — ignore it
- `relatedArticles` is manually curated and often empty for older content
```

**Keep it tight.** Each line should pass this test: "Would an agent with the schema alone get this wrong?" If you're unsure, test it — try answering 2-3 questions with `?instructions=""` and see what the model gets wrong on its own. That's your empirical baseline for what actually needs to be here. If no, cut it.

**Do not include:**

- General GROQ syntax (the tutorial covers this)
- Field lists or type descriptions (the schema covers this)
- Response formatting guidance (the response style section covers this)
- Anything the agent would figure out on its own

**Output:** A draft Instructions block, typically 10-40 lines depending on dataset complexity.

### Step 6: Verify Claims

**Goal:** Ensure every line in the draft is backed by evidence.

Go through the draft Instructions line by line. For each claim, show the user:

1. **The claim:** e.g., "contributors on article is an array of objects with a person reference"
2. **The evidence:** The GROQ query and result that demonstrates it
3. **Ask for confirmation:** "Is this accurate? Anything to add or correct?"

Example:

> **Claim:** "Always filter drafts using `!(_id in path("drafts.**"))` — there is no status field"
>
> **Evidence:** `*[_type == "article" && defined(status)][0..2]` → 0 results. `*[_type == "article" && _id in path("drafts.**")][0..2]` → 3 draft documents found.
>
> **Is this correct?**

If the user corrects a claim, update the draft immediately.

If the user adds new information ("oh, and you should also know that..."), add it to the draft and verify it the same way.

**Output:** A verified Instructions block where every claim has been confirmed by the user.

### Step 7: Deploy

**Goal:** Get the Instructions and filter into production safely.

Present the final Instructions content and filter to the user for one last review:

> Here's the final configuration:
>
> **Filter (GROQ expression):**
>
> ```
> _type in ["article", "author", "category", "tag"]
> ```
>
> **Instructions:**
> [final instructions block]
>
> Ready to deploy?

**Path A (write access):**

1. Write the `instructions` and `groqFilter` fields to the draft context doc
2. Verify by querying the draft MCP endpoint — confirm the instructions appear in `## Custom instructions`
3. **Promote to production:** Either update the production context doc's `instructions` and `groqFilter` fields to match, or update the production agent's MCP URL to point to the new slug
4. Verify the production endpoint serves the correct instructions

**Path B (no write access):**

1. Provide the final MCP URL with all params baked in:
   ```
   https://api.sanity.io/vX/agent-context/{project}/{dataset}/{slug}?instructions=<URL-encoded>&groqFilter=<URL-encoded>
   ```
2. Also provide the raw content separately for the user to paste into their Agent Context Document in Sanity Studio:
   - **Instructions field:** [final instructions block]
   - **Filter field:** [GROQ expression]
   - Location: Sanity Studio → Agent Context document → Instructions / Filter fields

**After deployment, verify:** Query the production MCP endpoint and confirm the instructions and filter are active.

**Output:** Instructions and filter live in production, verified working.

## Adaptation guidelines

This workflow scales to any dataset size:

**Small dataset (3-5 types, 5 questions):**

- Step 2 might be a 2-minute conversation
- Step 4 might find zero non-obvious patterns
- Final Instructions might be 5 lines or even empty (which is fine — it means the schema is self-explanatory)

**Large dataset (50+ types, 20 questions):**

- Step 2 needs more structure — group types by domain area
- Step 3 is critical — without good questions, you'll explore aimlessly
- Step 4 should group related questions to avoid redundant exploration
- Final Instructions might be 30-40 lines with multiple sections

**The filter matters more for large datasets.** A 50-type dataset where the agent only needs 8 types benefits enormously from a filter.

## Anti-patterns to avoid

- **Don't explore without the user.** Running 50 queries silently and presenting a wall of findings is overwhelming and error-prone. Explore interactively.
- **Don't assume from samples.** "I checked 3 articles and none had a subtitle" ≠ "subtitle is unused." Ask the user.
- **Don't duplicate the schema.** "The article type has fields: title, body, author, publishedAt..." — the agent already knows this.
- **Don't write prose.** Instructions should be scannable bullet points, not paragraphs.
- **Don't over-engineer.** If the dataset is simple and the schema is clear, the Instructions might be 3 lines. That's a success, not a failure.
- **Don't skip verification.** Every claim needs evidence + user confirmation. This is the quality gate.

## Session state tracking

Throughout the session, maintain a mental model of:

```
- [ ] MCP access verified
- [ ] Working environment set up (draft context doc or URL params)
- [ ] Existing instructions reviewed (if any)
- [ ] Schema discussed with user
- [ ] Filter agreed and applied
- [ ] Expected questions collected
- [ ] Questions explored and findings tracked
- [ ] Draft instructions written
- [ ] Each claim verified with evidence
- [ ] Instructions deployed to production
- [ ] Production deployment verified
```

This checklist is your progress tracker. Share it with the user periodically so they know where you are in the process.
