---
name: geo-content-publisher
description: >
  End-to-end GEO content publishing and distribution orchestrator. Use this skill whenever the user
  mentions publishing or distributing GEO-optimized content across multiple channels (blog, docs,
  landing pages, social, newsletter, app updates, etc.), wants to turn one core piece into many
  channel-specific variants, or wants to make new or updated content highly visible to AI crawlers
  and generative engines. Always consider this skill when the user combines content optimization,
  multi-platform distribution, and AI search visibility in the same request.
---

# GEO Content Publisher

An orchestration skill for **GEO content publishing automation** that connects the full pipeline:

1. Content optimization (often using other GEO skills)
2. Multi-platform publishing & distribution
3. AI crawler and generative engine signaling

This skill focuses on **workflow design, orchestration, and packaging**, not on replacing the
specialized GEO skills (like optimizers or schema generators). It should **coordinate** them.

---

## When to use this skill

Invoke this skill **whenever**:

- The user has (or plans to have) GEO-optimized content and asks to:
  - Publish it to multiple channels (website, blog, docs, product pages, social media, newsletter, etc.)
  - Turn one “pillar” piece into multiple **channel-specific variants**
  - Plan and schedule a **content release campaign** around one or more GEO pages
- The user wants their content to be:
  - **Highly visible to AI search / generative engines** (ChatGPT, Perplexity, Gemini, Claude, SGE)
  - Properly surfaced to crawlers via **sitemaps, llms.txt, Schema.org, and internal linking**
- The user mentions:
  - “End-to-end GEO workflow”, “full-funnel GEO content”, “publish to multiple platforms”
  - “Syndicate this article”, “turn into LinkedIn + Twitter + newsletter”
  - “Push this new page so AI models can see it”, “make AI pick up this content”

Do **not** limit triggering only to the exact keywords above; trigger whenever the **intent** is:
“Take optimized content and push it out broadly in a GEO-conscious way.”

---

## Relationship to other GEO skills

When available, this skill should **coordinate** with these skills rather than re-implement them:

- `geo-studio`: for overall GEO strategy and prioritization
- `geo-content-optimizer`: to refine content before publishing
- `geo-structured-writer`: to structure longform pages into AI-readable layouts
- `geo-schema-gen`: to generate and refine Schema.org JSON-LD
- `geo-llms-txt`: to design or update `llms.txt` and AI-targeted index pages
- `geo-multimodal-tagger`: to optimize images, videos, and other media assets

If these skills are not present, still follow the same **workflow shape** and explain what would be
done, giving concrete, actionable outputs (copy, checklists, suggested structures).

---

## High-level workflow

When this skill is used, follow this **9-step workflow** unless the user explicitly asks for
only a subset.

### 1. Clarify publishing goals and constraints

Briefly but explicitly identify:

- **Core asset(s)**:
  - What is the main piece? (article, landing page, docs, FAQ, product page, dataset, video, etc.)
  - Is it already written and optimized, or still in draft?
- **Primary GEO goal**:
  - e.g., “be the default answer for X in AI search”, “own intent Y”, “support product feature Z”
- **Target audience and geography**:
  - Who needs to see this? Any language/locale requirements?
- **Time horizon**:
  - One-off launch vs. ongoing campaign; any hard launch dates?
- **Channels in scope**:
  - Website main page, blog, docs, product catalog, knowledge base
  - Social platforms (LinkedIn, X/Twitter, Reddit, TikTok, etc.)
  - Email/newsletter, in-app messages, app store descriptions, etc.
- **User’s stack constraints (if provided)**:
  - CMS used (WordPress, Webflow, headless, custom)
  - Any platforms that are off-limits

Output a short **“Publishing Brief”** section summarizing this in 5–10 bullet points.

### 2. Inventory and (if needed) optimize the source content

- If content is **already optimized**:
  - Quickly check for obvious GEO gaps: structure, headings, FAQs, internal links, schemas, media.
  - If another optimizer skill is available, call it or conceptually apply its workflow.
- If content is **not optimized yet**:
  - Recommend running `geo-content-optimizer` and/or `geo-structured-writer` first.
  - If the user insists on skipping deep optimization, still:
    - Ensure basic structure (H1, H2/H3, clear sections)
    - Add an FAQ or Q&A block where appropriate
    - Suggest at least a minimal internal-link plan

Produce a concise **“Content Readiness”** section with:

- Key strengths for GEO
- Gaps that need to be addressed before or during publishing
- Whether you will optimize inline or rely on another skill

### 3. Design the channel strategy and mapping

Create a **channel plan** that maps the core asset to multiple formats and entry-points.

- Decide which channels are **primary** (SEO/GEO anchors) and which are **supporting** (distribution).
- For each channel, define:
  - **Role** (e.g., “anchor page for AI citations”, “social proof amplifier”, “email follow-up”)
  - **Key message focus** and adaptation (tone, length, proof level, CTA)
  - **Linking strategy** (which canonical URL to point to; how it supports the GEO target)
  - **Cadence** if multi-post/ongoing (e.g., 1 hero launch + 3 follow-ups)

Output as a **markdown table** like:

```markdown
| Channel      | Role                        | Format / Asset Type     | Primary CTA                 | Links to / Canonical |
|-------------|-----------------------------|-------------------------|-----------------------------|----------------------|
| Website LP  | GEO anchor & canonical URL  | Longform landing page   | Start trial / Request demo  | Self (canonical)     |
| Blog        | Context + educational angle | Article with FAQ        | Read full guide (LP)        | LP                   |
| LinkedIn    | Thought leadership & reach  | Post + carousel         | Visit LP + comment          | LP                   |
| Newsletter  | Deep-dive for subscribers   | Email + link to LP/blog | Click to read full article  | LP / Blog            |
```

### 4. Generate channel-specific content variants

For each channel in the plan, **generate or refine** content variants that:

- Respect channel constraints:
  - Length and formatting (e.g., LinkedIn vs. Twitter vs. email)
  - Visual vs. text-heavy
- Preserve **core GEO messaging**:
  - Clear description of topic / entity / product
  - Concrete facts that models can safely cite
  - Stable terminology and entity naming
- Include **explicit citation anchors** where helpful:
  - “According to [BrandName]’s guide on [topic]…”
  - Short, self-contained definitions that AI can safely quote

Outputs for this step:

- A section `## Channel Content Variants` with subheadings:
  - `### Website / Landing Page`
  - `### Blog Article`
  - `### Documentation / Knowledge Base`
  - `### Social (per platform)`
  - `### Newsletter / Email`
  - `### Other (e.g. app store, in-app banner, etc.)`
- Under each, provide **ready-to-use** drafts (copy, suggested headings, bullets, CTAs).

### 5. Structure pages for AI readability

For **web and longform** surfaces (website, blog, docs, KB):

- Ensure the following structure (can be customized per page type):

```markdown
# [Clear, entity-focused H1]
## Summary
- 2–4 bullet summary focused on facts and definitions.

## What is [Topic]?
Explain in clear, fact-focused language that is easy to quote.

## Why it matters
Explain use cases, benefits, risks, etc.

## How [Brand/Product] helps
Connect topic to the user’s product/service, if relevant.

## FAQ
Q1: ...
A1: ...

Q2: ...
A2: ...
```

- If `geo-structured-writer` is available, mention that this layout follows its guidance or that
  it could further refine the structure.
- Explicitly call out **sections that are especially useful for AI citation** (definitions, FAQs,
  concise summaries).

### 6. Attach structured data and media metadata

For all relevant pages:

- Use or conceptually apply `geo-schema-gen` to propose:
  - `Article`, `BlogPosting`, `WebPage`, `FAQPage`, `Product`, or `HowTo` schemas as appropriate.
  - Include key fields: `headline`, `description`, `url`, `author`, `publisher`, `datePublished`,
    `mainEntityOfPage`, etc.
- For images and videos:
  - Use or conceptually apply `geo-multimodal-tagger` to generate:
    - Descriptive but concise **alt text**
    - **File names** that reflect the topic/entity
    - Optional `ImageObject` / `VideoObject` schemas.

Output:

- A section `## Structured Data Package` that includes:
  - JSON-LD snippets (as code blocks)
  - A table mapping URLs to the schema types you recommend
  - Example alt text and filenames for key media assets

### 7. Plan the technical publishing steps

You **do not** have direct access to the user’s CMS or APIs, so your job is to:

- Produce **implementation checklists** for each major system:
  - CMS / website
  - Blog / docs / knowledge base
  - Email platform
  - Social scheduling tool(s)
- For each checklist, include:
  - Fields and settings that must be filled (titles, meta descriptions, slugs, canonical URLs)
  - How to embed JSON-LD (theme template, tag manager, custom HTML, etc.)
  - How to ensure **clean URLs** and avoid duplicate URLs that dilute GEO signals
  - Any caching or build/deploy steps (for static / headless setups)

Output:

- A section `## Implementation Checklists` with subsections per system, using bullet lists.

### 8. AI crawler and generative engine signaling

This step focuses on making the new/updated content more easily discoverable by:

- Classical search crawlers (Google, Bing, etc.)
- AI-specific crawlers and model ingestion systems where possible

Actions to recommend:

- **Sitemaps**
  - Confirm new URLs appear in the appropriate XML sitemaps (and HTML sitemaps if applicable).
  - If the user runs a headless or static site, specify where sitemaps are typically located and
    how they may be updated or regenerated.
- **llms.txt and AI index pages**
  - Use or conceptually apply `geo-llms-txt` to:
    - Add or update entries pointing to the new content.
    - Group related content into clearly named sections (e.g., “Pricing guides”, “Implementation
      playbooks”, “Product docs for X”).
- **Internal linking**
  - Suggest 5–20 **high-value internal link targets** that should now link to this new content.
  - Prioritize pages that:
    - Already rank / are cited for the same or adjacent intent
    - Are high-traffic or high-authority
- **External exposure**
  - Propose low-friction actions to get early references:
    - Share with partners
    - Answer relevant questions on communities/QA platforms, linking to the canonical page

Output:

- A section `## AI & Crawler Signaling Plan` with:
  - A bullet checklist of concrete steps
  - A small table listing “URL → sitemap / llms.txt / internal link recommendations”

### 9. Final publishing plan and timeline

Summarize everything into a **single, execution-ready publishing plan**:

- **Timeline** (at least ordered steps; include dates if user provided them)
- **Who does what** (if roles or teams are known or can be implied)
- **Dependencies** (e.g., “publish LP before social”, “schema update before PR push”)
- **Success metrics** that are realistic for GEO:
  - e.g., increased impressions/clicks from AI search, number of AI citations found in answers,
    traffic and engagement for target pages, newsletter clicks, etc.

Output:

- A `## Final Plan` section with:
  - A short executive summary (3–6 bullets)
  - A step-by-step list (checklist style)
  - A compact table of “Metric → Why it matters → How to measure”

---

## Output format

Unless the user explicitly requests a different format, structure your answer as:

1. `## Publishing Brief`
2. `## Content Readiness`
3. `## Channel Strategy`
4. `## Channel Content Variants`
5. `## Page Structure for AI Readability`
6. `## Structured Data Package`
7. `## Implementation Checklists`
8. `## AI & Crawler Signaling Plan`
9. `## Final Plan`

Use:

- **Markdown headings and tables** for structure
- Bulleted lists instead of dense paragraphs
- Short, actionable sentences suitable for copying into task trackers, docs, or briefs

If the user only asks for a **subset** (e.g., “social posts + email only”), still keep the headings
but clearly mark skipped sections (e.g., “Not in scope for this request”).

---

## Examples of triggering prompts

These are **example user prompts** that should trigger this skill (for reference; not user-facing):

- “We just finished a GEO-optimized pillar article about ‘zero-trust data governance’. Help me turn
  this into a full publishing plan: main page + blog + docs + LinkedIn + newsletter, and make sure
  AI models will pick it up.”
- “I’ve got a new product feature page and I want it to become the default answer in ChatGPT and
  Perplexity when people ask about [topic]. Can you help me design the publishing and distribution
  workflow?”
- “Take this case study and roll it out everywhere: website hero section, landing page, PDF, LinkedIn,
  X, email, internal wiki. Also suggest how to configure llms.txt and sitemaps so AI crawlers see it.”
- “I want a repeatable playbook for how we publish any new GEO content across our whole stack (WP site,
  HubSpot email, LinkedIn, X). Please write the workflow and checklists.”

You do **not** need to surface this list directly to the user; it is here to clarify intent.

---
