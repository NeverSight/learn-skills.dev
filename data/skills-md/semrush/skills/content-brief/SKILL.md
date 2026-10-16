---
name: content-brief
description: Turn one target keyword into a content brief a writer can ship — intent, audience and angle, SERP context, title and meta description, outline, FAQs, scope guidance, and an internal linking plan. Use when the user asks for a content brief, a blog outline, what to write about a keyword, or how long an article should be.
---

# Content brief

This skill turns one target keyword into a content brief that a writer can use to ship a publish-ready article. It is opinionated about what belongs in a brief and what does not. A good brief sets the scope, frames the angle, and gets out of the way.

A brief should not write the article for you. Over-specified briefs read like compliance checklists and produce content that ranks like compliance checklists. The job is to give the writer enough context to make real decisions, not enough specification to remove the decisions.

## Before you start

Ask for these inputs once.

- **Target keyword.** One primary keyword per brief. If the user gives a list, choose with the user or prioritize by relevance, business value, intent fit, attainability, and SERP evidence. Do not default to the highest-volume term.
- **Domain.** Optional but improves results by exposing relevant existing pages, rankings, and internal-link destinations. Do not claim that the tested public MCP returns personalized keyword difficulty for a supplied domain.
- **Whether the Semrush MCP is connected.** This unlocks Semrush keyword and organic reports for live SERP data. If it is not connected, you can still write the brief, but the SERP analysis should be labeled manual or directional. The Semrush MCP connects through Semrush's own auth flow, so there is no API key to paste.
- **Target audience.** A brief without an audience definition produces content that talks to no one. Ask once if the user has a written ICP, content guidelines, or audience notes. If not, ask for two sentences on who the reader is.
- **Goal.** Rank for traffic, support an existing campaign, build a topical hub, refresh an underperforming page. The goal changes the brief.

## How to use the Semrush MCP

Use Semrush MCP only.

The callable MCP tool names are the research entry points plus schema execution. Report/product names such as Keyword Overview and Keyword Magic Tool are selected through the schema flow, not called directly as tools.

- Use `keyword_research` → `phrase_this` for available generic keyword metrics such as volume, generic KD, intent, and CPC. The tested schema has no domain input, PKD field, or SERP-feature field.
- Use `keyword_research` → `phrase_related` and `phrase_questions` for related and question-format keywords. These reports provide keyword rows, not Keyword Magic Tool groups, automatic clusters, or an outline.
- Use `keyword_research` → `phrase_organic` with `positions_type: organic` for ranking URLs. Use `positions_type: all` only when feature-position rows are intentionally required, and keep those rows separate from organic rankings. Preserve every raw row, but deduplicate identical URLs for page-review and format-count purposes while recording every returned position. Do not attribute word count, page traffic, page-level referring domains, or Authority Score to this report.

Interpret report output conservatively:

- Preserve numeric intent and SERP-feature codes exactly as returned. Map a code to a human-readable label only when the current discovered schema or official documentation supplies that mapping. Otherwise, show the raw code as unresolved and keep any manual intent or feature classification separate as a model inference or observation.
- Screen related and question rows for duplicates, explicit search operators, broken encoding, obvious misspellings, and off-topic terms before using them in the brief. Preserve the original rows, state the screening rule and excluded count, and never assign a removed row's metrics to a corrected spelling.
- When two Semrush reports disagree, retain both values with their report name, database, target, and available date or snapshot context. Do not silently merge them or choose the more favorable value. Explain which value, if any, is used for the decision and why; otherwise mark the metric inconsistent.

The canonical workflow stays the same: discovery via Semrush MCP `keyword_research` or `organic_research` → `get_report_schema` for the specific report → `execute_report` with the parameters.

If a structured SERP Analysis artifact is supplied, consume its keyword context, intent, feature map, ranked URLs, evidence availability, format distribution, gaps, and confidence instead of rerunning the same research. Otherwise, build that evidence with the reports above and fetch additional domain or URL evidence only when needed. Label manual inspection, format classification, gap detection, clustering, and outline decisions as analyst/model judgments rather than returned Semrush fields.

## MCP access and cost guardrails

- Before the first `execute_report` call, tell the user that Semrush MCP queries consume API units. Request only the fields needed, use the smallest result limit that answers the question, and expand only after reviewing the first batch. Never request all rows by default.
- If authentication is incomplete, a required tool, report, schema, or field is unavailable, or execution fails because of access or units, stop that MCP branch. State what is unavailable and which parts of the brief are affected, then use the strongest fallback below. Never invent or silently substitute missing Semrush metrics.

## Fallback ladder

Use the strongest available data source and state which one you used.

1. Semrush MCP keyword, SERP, and URL/domain reports.
2. Semrush UI exports supplied by the user.
3. Manual SERP inspection in the target country.
4. User-provided competitor URLs and first-party audience notes. Label missing metrics as unknown rather than guessing.

## Evidence contract

Keep source provenance and confidence separate. Use these labels for material inputs and recommendations:

- **Semrush data:** A value returned by a named MCP report. Include the report name.
- **Semrush-supported guidance:** An editorial recommendation supported by a linked Semrush source. Do not present it as a search-engine requirement.
- **User-provided:** First-party goals, audience knowledge, conversion evidence, constraints, or approved sources.
- **Manual observation:** A directly inspected SERP or page characteristic that was not returned by the MCP.
- **Model inference:** A recommendation derived from the available evidence, such as format, angle, grouping, or outline structure.
- **Configurable default:** A starting scope chosen for usability rather than a universal SEO rule.

In the user-facing brief, show provenance where it changes how a claim should be trusted. Keep the labels compact in an evidence or rationale note instead of tagging every sentence. Rate confidence separately as high, medium, or low and state the missing evidence when it lowers confidence.

## The brief structure

A working brief has these eight sections. Anything else is optional.

1. Target keyword and intent
2. Audience and angle
3. SERP context (top 10 analysis)
4. Title and meta description
5. Outline (H1, H2s, H3s)
6. Scope guidance
7. Linking plan (internal and external)
8. Style and voice notes

Run them in order. Each section feeds the next.

---

## 1. Target keyword and intent

Capture the primary keyword and the available `phrase_this` metrics, such as volume, generic KD, CPC, and the raw intent value. Mark unavailable fields as unknown and keep each value tied to its Semrush report. Do not attribute SERP features to `phrase_this`. The brief opens with the keyword so the writer understands the proposed search target before reading anything else.

Classify intent as informational, navigational, commercial, or transactional only when the returned code has a verified mapping or when live SERP evidence supports a separate model judgment. Label which path was used. The format the writer should produce changes by intent.

- Informational intent often supports a guide or article, but confirm the format against the live SERP.
- Commercial intent often supports comparisons, alternatives, reviews, or pricing context.
- Transactional intent often points to a product, category, service, or pricing page. Recommend the appropriate page type rather than automatically stopping the workflow.
- Navigational intent often points to a product or brand page. Mixed or fractured intent is possible, so use the observed SERP distribution before deciding.

Add only secondary keywords that the same page can satisfy without mixing incompatible intents. Choose them from Semrush rows plus transparent intent and SERP-overlap analysis; do not promise that the page will rank for every included term.

## 2. Audience and angle

Two short paragraphs. No more.

The audience paragraph names who the reader is, what they already know about the topic, and what they need from the article. "Senior SEO at a B2B SaaS, has read three guides on this already, wants the part nobody else covers" is useful. "Marketers" is not.

The angle paragraph names the page's hook. What does this article say that the top 10 do not? If you cannot answer that in one sentence, the brief is not ready. Generic coverage of the topic loses to the existing top 10, which already cover the topic.

Possible angles:

- A first-party data point (a survey, an experiment, a tool result the writer can cite).
- A contrarian read (the conventional advice is wrong here, and we can prove it).
- A more specific scope (the top 10 are generic, ours is for a specific industry or use case).
- A more useful format (the top 10 are walls of text, ours is a tool, calculator, template, or checklist).

## 3. SERP context

Pull the top 10 organic results for the primary keyword via the Semrush MCP or by inspecting the SERP directly.

For a representative set of ranking results, capture:

- URL
- Page type (guide, listicle, comparison, calculator, product page)
- Word count only when it can be measured directly; label it as descriptive competitor evidence, not a target or ranking factor
- Notable angle or differentiator
- Whether the page is part of a topical hub on its site

Also capture which SERP features appear when they can be verified through mapped `phrase_organic` codes or direct SERP inspection: featured snippet, PAA boxes, video carousel, shopping results, and AI Overview. Never guess a feature name from an unmapped numeric code. Use verified features to identify eligible formats and likely searcher needs. Do not assume a fixed answer length or claim that an AI Overview always reduces clicks; describe only what the observed evidence supports.

Common patterns to flag for the writer.

- If one format dominates, note the strength of that pattern and whether an alternative format could satisfy the same intent better.
- If ranking pages show a consistent depth or scope, use that as descriptive context while defining the coverage the reader needs. Do not convert competitor word counts into a ranking requirement.
- If one site holds several results, record the concentration as an observation. Do not treat it alone as proof that the site owns the topic.

## 4. Title and meta description

Two title candidates, one meta description.

Titles:

- **Semrush-supported guidance:** Aim for 550 pixels or fewer, typically 50 to 60 characters, to reduce truncation or rewriting risk. Search engines and AI systems do not enforce a maximum, so use a preview rather than treating the range as a hard failure.
- Make each title descriptive, concise, and aligned with the page's actual topic and intent.
- Include the primary keyword once and naturally when it accurately communicates the topic. Do not stuff related variants.
- Add a value signal such as the audience, scope, evidence, or format only when the page delivers it.
- Propose different defensible angles so the user can choose. Keep the title and H1 similar enough to communicate the same page topic without requiring an exact match.

Meta description:

- **Semrush-supported guidance:** Aim for no more than 135 characters to reduce truncation risk across devices. Treat this as an editorial target, not a ranking factor or hard validation failure.
- Summarize the page accurately and give the searcher a useful reason to visit.
- Include the primary keyword or a close variant naturally when it improves relevance and clarity.
- Address the observed search intent and consider answering the core question when a concise answer is useful.
- Preview the result because device width, character width, query bolding, and search-engine rewriting affect the displayed snippet.

Do not withhold a useful answer merely to manufacture a click. The title and description must represent what the page actually delivers without misleading or clickbait framing.

## 5. Outline

The outline is the spine of the brief. Get this right and the writer can do the rest.

Build the outline from three sources.

- SERP analysis. Identify recurring subjects and meaningful gaps, then decide which belong in this page based on audience and intent. Do not copy competitor headings automatically.
- People Also Ask. Use relevant questions as research inputs; include them only when they help satisfy the page's purpose, not as automatic H2 or FAQ entries.
- Semrush keyword rows. Group related terms through transparent intent and SERP-overlap analysis, then use the resulting topics as outline evidence. Do not imply that the MCP returns semantic clusters or that a fixed number of terms maps to one heading.

Recommend one clear H1 that describes the page, addresses its primary intent, and is consistent with the title's topic. **Semrush-supported guidance:** Start with one H1 for the main title, then use H2s for main sections and H3s for subsections. Treat one H1 as an editorial and structural recommendation, not a ranking guarantee or automatic failure condition.

Make headings clear, direct, and descriptive. Aim for fewer than 60 characters when practical, but do not sacrifice clarity to meet the target. Concise labels such as "Pricing" are valid when they unambiguously describe the section. Focus each heading on one topic or idea.

Include the primary keyword in the H1 and relevant secondary keywords or questions in H2s and H3s when they fit naturally. Put the reader first; do not force exact-match wording. Use the H1 and first H2 to address the primary intent, then use later headings for relevant supporting intents.

Use H3s as genuine subsections directly under an H2, not merely to create visual rhythm. Keep the hierarchy logical and consistent.

**Configurable default:** Give each outline entry 1 to 3 lines of notes covering what the section should address, any specific source to cite, and any data point to include. Avoid drafting the section itself. The writer needs structure, not prose.

## 6. Scope guidance

Define the questions, evidence, examples, and decisions the page must cover to satisfy the audience and intent. Competitor length may be reported as descriptive SERP context when it was measured directly, but never turn it into a minimum, maximum, ranking guarantee, or padding formula.

If the writer requests a planning range, make it a clearly labeled editorial estimate based on the approved outline and expected depth. Explain that useful completeness matters more than matching a competitor's word count.

## 7. Linking plan

Internal links.

- Identify relevant destinations before the writer starts. Pull from the user's existing site via Semrush organic reports, a supplied export, or a manual sitemap.
- Plan both directions: links from the new page to contextually related existing pages, and links from relevant existing or authoritative pages to the new page.
- **Semrush-supported guidance:** Aim for at least two or three incoming internal links to each new piece of content. Treat this as an editorial aim, not an automatic failure condition. Recommend outgoing internal links based on contextual relevance rather than a fixed count.
- Use pillar-to-cluster and cluster-to-pillar links when they reflect the site's actual architecture. Do not automatically require a homepage or pillar link.
- Use concise, descriptive anchor text—ideally five words or fewer. Exact-match internal anchors are acceptable when relevant, but avoid keyword stuffing and generic anchors such as "click here" or "this page."

External links.

- Identify relevant, credible, and professional external sources needed to substantiate claims or provide useful context.
- **Configurable source-quality default:** Prefer government sources, original research, primary product documentation, and credible industry publications when available. Do not treat every aggregator as automatically unacceptable; evaluate the actual source and evidence.
- Do not impose a fixed external-link count. Use concise, descriptive anchor text and recommend a link only when it adds value for the reader.
- Avoid clickbait, low-quality information, low-quality directories or bookmark sites, and any link scheme intended to manipulate rankings.
- Normal editorial links to trusted sources do not need a special relationship attribute. Use `rel="nofollow"` when the site should not be endorsed or associated with. Mark sponsored or affiliate links with `rel="sponsored"` or `rel="nofollow"`; do not ban them categorically.

## 8. Style and voice notes

Three to five bullet points. Cover:

- Reading level (technical, mainstream, beginner).
- First-person, second-person, or none. Pick one and tell the writer.
- Examples policy. Real numbers and real names, or hypothetical placeholders.
- Banned phrases or AI tells the user has flagged before.
- House style links (a tone-of-voice doc, a style guide URL).

---

## How to report the brief

Output the brief as a single markdown document. Use H2 section headings matching the eight sections above. Include a "Notes for the writer" section at the bottom for anything that did not fit the structured sections.

Two rules for the brief itself.

- State actual values with their source. "Semrush `phrase_this`: volume 2,400, KD 38%, intent code 1 (mapping unresolved)" is useful when no verified mapping exists. "Decent target" is not.
- Suggest concrete sources for every data point you cite. A brief that says "according to a recent study" without naming the study is asking the writer to hallucinate.
- Label manual observations and model-generated recommendations, and add a short confidence note when incomplete evidence materially affects the proposed format, angle, or outline.

Keep the brief proportional to the topic's complexity and the writer's needs. Remove instructions that do not change the writer's decisions.

## Sources

This skill is grounded in the following Semrush editorial sources:

- [How to create content briefs](https://www.semrush.com/blog/content-brief/)
- [How to create a content outline](https://www.semrush.com/blog/content-outline/)
- [How to write a blog post](https://www.semrush.com/blog/how-to-write-a-blog-post/)
- [Keyword research for SEO](https://www.semrush.com/blog/keyword-research/)
- [What is search intent](https://www.semrush.com/blog/search-intent/)
- [What is a title tag?](https://www.semrush.com/blog/title-tag/)
- [What is a meta description?](https://www.semrush.com/blog/meta-description/)
- [What are heading tags?](https://www.semrush.com/blog/heading-tags/)
- [Internal links: ultimate guide and strategies](https://www.semrush.com/blog/internal-links/)
- [What is an external link?](https://www.semrush.com/blog/external-links/)
- [What is anchor text?](https://www.semrush.com/blog/anchor-text/)

Keep these articles as methodology references. Include article links in the user-facing brief only when the user asks for methodology citations or when a specific claim needs verification.
