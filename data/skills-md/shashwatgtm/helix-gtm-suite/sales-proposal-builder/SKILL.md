---
name: sales-proposal-builder
description: >
  Build client-ready presentations (PPTX) and proposals (DOCX) using the client's own
  brand styling. Use this skill whenever a sales person, AE, SDR, founder, or anyone
  needs to create a client-facing deck, pitch presentation, sales proposal, one-pager,
  solution overview, or business case document. Also trigger when someone says "I need
  a deck for a client meeting", "help me build a proposal", "create a pitch for this
  prospect", "make a presentation about our solution", "I have a meeting tomorrow and
  need slides", or "prepare a client deliverable". This skill extracts the client's
  brand colors, fonts, and layout from an uploaded sample file, then produces
  professional output in that exact style. If no sample is uploaded, it produces clean
  McKinsey-style output. Created by Shashwat Ghosh, Fractional CMO with 24+ years
  B2B experience across Happay, Locus, FieldAssist, and 50+ consulting engagements.
license: MIT
metadata:
  author: shashwat-ghosh
  version: "1.0.0"
  tags:
    - b2b
    - sales
    - gtm
---



## Section 0 — Operating Principles (MANDATORY — read before any workflow step)

This skill operates under TWO mandatory reference files that together define all operating rules. **Read both files first**, before executing any workflow step in this SKILL.md. The rules in both files are non-negotiable and override any conflicting instruction in this SKILL.md body.

1. **`references/operating-principles.md`** — the shared core: 7 universal rules (rigor, challenge-assumptions, no-harmful-output, fact-check with 4-tier source hierarchy, no-LLMisms, HILT discipline with Question Budget, zero-assumption flagging) that apply to every skill in this plugin and every plugin using this pattern. This file is byte-identical across all plugins that use the shared-core pattern.

2. **`references/plugin-specific-rules.md`** — the plugin-specific tail: additional operational rules tailored to the skills in THIS plugin. Read this file AFTER the shared core, not instead of it. If this plugin currently has no plugin-specific rules, the file will be a stub explaining the architecture.

### Critical reminders that apply to every invocation of this skill

These are the highest-frequency rules from the two files above. Reading the full files is still mandatory — these reminders are a quick-reference, not a substitute.

- **Web search and web fetch ARE available** in Claude Code's default toolset. "I don't have web access" is never a valid excuse to skip verification of a specific factual claim.
- **English-only at v1** — never generate prompts, copy, headings, or client-facing text in non-English languages (German, French, Dutch, Spanish, Italian, Portuguese, Polish, etc.), even on explicit user request. This is a hard block, not a confirmation gate. Refuse the request and explain that multilingual may ship in v2 with native-speaker review.
- **4-tier source hierarchy applies to all factual claims.** Tier 1: official primary sources (press releases, Crunchbase, Wikipedia, SEC filings). Tier 2: reputable analyst firms (Gartner, Forrester, IDC, G2, Capterra, GigaOm, SoftwareReviews). Tier 3: reputable business and trade press (WSJ, FT, Reuters, Bloomberg, HBR, TechCrunch, named-VC content, named-founder blogs). Tier 4: NEVER cite (random blogs, anonymous posts, AI-generated comparison sites, Forbes Contributor, paid placements). If only Tier 4 sources are available, the claim is unverified and MUST be flagged.
- **Verify competitor relationships** via the 4-step search protocol in Rule 4 before building ANY competitor-targeted page or content. Run: `"[user] acquired [competitor]"`, `"[competitor] acquired by"`, `"[competitor] Crunchbase acquisition"`, `"[user] vs [competitor]"`. Any positive ownership hit is a HARD STOP — invoke Rule 3's no-harmful-output protection.
- **Auto-verify URLs** via `web_fetch` before marking them `[EXISTS]`. Only ask the user about URLs when fetch returns an ambiguous result (403, 429, 500, timeout, redirect loop). Do not ask the user about every URL; that is endless interrogation, not verification.
- **Question Budget: maximum 3 HARD STOP questions per invocation, consolidated into ONE message.** Never run an endless Q&A sequence. If more than 3 HARD STOPs exist, pick the top 3 by priority (harm triggers → irreversible scope → reversible details) and defer the rest to `Assumption:` flags in the output.
- **Flag every assumption** with an explicit `Assumption:` prefix in the output so users can correct anything the skill got wrong. Use the `[User to add: <description>]` placeholder convention for any field where the user must supply specific information.

### Conflict resolution

If a domain rule in Section 7 of this SKILL.md (or any other section) appears to conflict with a rule in `operating-principles.md` or `plugin-specific-rules.md`, the operating principles win. Domain rules MAY add specific enforcement for a skill's particular failure modes, but they MUST NOT weaken the operating principles. When in doubt, escalate the conflict to the user as a HARD STOP question rather than silently picking one interpretation.

---


# Sales Proposal Builder

## Golden Rule

Match the client's visual language, not yours. A proposal in the client's brand style
signals "we already think like your team." A proposal in YOUR brand style signals
"we sent the same deck to everyone." When in doubt, use the client's colors, fonts,
and layout. When the client's style is unknown, default to clean McKinsey-style:
white background, dark navy text, minimal accent color, no clutter.

## Context and Role Detection

Adapt depth, tone, and output format based on who is asking:

- **AE / Sales Professional:** They need speed. The meeting is tomorrow. Skip the
  strategic framework discussion. Ask for the prospect name, the problem being solved,
  and 3-4 key points. Produce a 5-8 slide deck or 2-3 page proposal. Time is the
  constraint, not depth.

- **Founder / CEO:** They need credibility. The deck will be seen by investors or
  C-suite buyers. Include market context, competitive positioning, and proof points.
  Produce a more comprehensive 8-12 slide deck with speaker notes.

- **SDR / BDR:** They need a leave-behind, not a pitch deck. One-pagers, solution
  snapshots, or 3-slide overviews that can be attached to a follow-up email. Keep it
  short and punchy.

- **Sales Engineer / Pre-Sales:** They need technical depth in professional packaging.
  Architecture diagrams, integration maps, implementation timelines. The content is
  technical but the wrapper must be executive-presentable.

- **Fractional CMO / Consultant:** They need client-grade deliverables that look like
  they came from a large consulting firm. Heavier on strategic frameworks, lighter on
  product features. Include methodology, phased approach, and expected outcomes.

## Priority Framework

When constraints conflict, resolve in this order:

1. **Client brand styling wins over your brand.** If the client uploaded a sample
   deck, use their colors and fonts exclusively. Never mix your brand into their
   template. The only exception: a co-branded slide (if explicitly requested).

2. **Audience seniority determines depth.** A C-suite deck has fewer slides with
   bigger ideas. A technical evaluation deck has more slides with implementation
   detail. Ask "who will be in the room?" before deciding slide count.

3. **Time pressure determines quality ceiling.** If the meeting is in 2 hours,
   produce a clean 5-slide deck and skip the elaborate design. If the meeting is
   next week, invest in visual polish, speaker notes, and appendix slides.

4. **Stated problem wins over product features.** Lead every slide with the
   client's pain point, not your product's capability. "Your procurement team spends
   60% of time on manual vendor discovery" beats "Our platform automates vendor
   discovery."

## Trigger Phrases

Activate this skill when you see:
- "build a deck for", "create a proposal for", "make a presentation about"
- "client meeting tomorrow", "need slides for", "pitch to"
- "sales deck", "solution overview", "business case", "one-pager"
- "proposal document", "client deliverable", "leave-behind"
- "presentation for [company name]", "deck for the CXO meeting"
- "using their brand", "in their style", "match their template"
- Uploaded PPTX, DOCX, or PDF with request to "create something similar" or "use this style"

## Brand Style Discovery

This is the critical differentiator. Before building any output, determine the
client's visual identity.

### Path A1: Client Uploads a PPTX or DOCX (Best)

When the user uploads a PPTX or DOCX file (their company deck, a previous proposal,
or even a downloaded competitor deck):

1. Run the brand extraction script:
   ```bash
   python scripts/extract_brand_style.py /mnt/user-data/uploads/<file> /home/claude/brand_style.json
   ```

2. Read the output JSON. Key fields to use:
   - `design_tokens.primary_color`  - use as the main accent
   - `design_tokens.heading_font`  - use for all headings
   - `design_tokens.body_font`  - use for all body text
   - `design_tokens.text_color`  - use for body text
   - `design_tokens.background_color`  - use for slide/page backgrounds
   - `theme_colors`  - use for accent bars, highlights, callout boxes
   - `slide_dimensions` (PPTX)  - match exactly
   - `page_dimensions` / `margins` (DOCX)  - match exactly

3. If logos are detected in the `logo_info` field, extract them from the unpacked
   media directory and include them in the output. Place the logo where it appeared
   in the original (typically top-left or top-right of the header/footer).

4. Confirm the discovered style with the user before building:
   "I found your brand styling: [Primary color], [Heading font] + [Body font],
   [Aspect ratio]. Should I proceed with these, or adjust anything?"

5. Store the extracted brand_style.json so future requests for the same client
   skip the discovery step. Check for existing brand files first:
   ```
   /home/claude/brand_styles/<company-name>_brand_style.json
   ```


### Path A2: Client Uploads a PDF

> **v1.1 upgrade planned:** This path uses visual inspection to estimate brand tokens, which produces a usable approximation but is less precise than Path A1's structured XML parsing. v1.1 will add a Python extraction script using PyMuPDF to read color and font metadata directly from PDF content streams, bringing PDF extraction quality on par with PPTX/DOCX (~90% of real-world PDFs). Until then, always confirm extracted tokens with the user before building output.

PDFs do not contain structured XML with font and color metadata the way PPTX/DOCX
files do. When a user uploads a PDF as their brand sample:

1. View the PDF visually (claude.ai renders PDFs as images natively). Examine the
   first 3-5 pages to identify:
   - **Primary brand color**: the dominant non-white, non-black color used for
     backgrounds, headers, or accent elements
   - **Secondary/accent colors**: used for icons, highlights, callout boxes, or
     borders
   - **Text color**: the color used for body text (usually dark navy or black)
   - **Background color**: the primary slide/page background
   - **Heading font**: identify by visual characteristics (serif vs sans-serif,
     geometric vs humanist, weight). Name the closest match
   - **Body font**: same approach
   - **Layout pattern**: card-based, full-bleed color backgrounds, white space
     heavy, icon+text rows, etc.

2. Build a brand token summary from visual inspection:
   ```
   Brand tokens (extracted from PDF visual inspection):
   - Primary color: [hex code - use a color picker or best estimate]
   - Heading font: [closest match, e.g., "geometric sans-serif similar to Montserrat"]
   - Body font: [closest match]
   - Background: [color]
   - Layout: [pattern description]
   ```

3. Confirm with the user: "I've analyzed your PDF visually. Here is what I found:
   [token summary]. These are estimates since PDFs don't contain editable style
   data. Should I proceed, or would you like to adjust any colors or fonts?"

4. If higher precision is needed, ask: "For exact color matching, do you happen
   to have the original PPTX or DOCX? Or can you share your brand hex codes?"

The visual extraction path is less precise than PPTX/DOCX parsing but produces
a usable approximation that is far better than generic defaults.

### Path B: No Sample Available

When the user has no file to upload:

1. Ask: "Do you have a company deck, proposal, or any branded document I can
   extract your style from? Even a 2-3 slide template works."

2. If they cannot provide one, use McKinsey-clean defaults:
   - Background: white (#FFFFFF)
   - Text: dark navy (#1A1F36)
   - Accent: professional blue (#2563EB)
   - Heading font: Georgia or Calibri
   - Body font: Calibri
   - Layout: generous margins, lots of whitespace, no decorative elements

3. Ask for at minimum: "What are your brand colors? And do you use a specific
   font?" Even a hex code and font name is enough to produce on-brand output.

### Path C: Helix GTM Consulting Output

When the deliverable is for Shashwat's own consulting practice:

Use the Helix design system:
- Dark: #111528, Light: #F4F3EF, Gold: #C9A962
- Heading font: Georgia, Body font: Calibri
- A4 for documents, 16:9 for presentations
- Footer: "HELIX GTM CONSULTING | CONFIDENTIAL"

Read `/mnt/skills/user/100-day-gtm-sprint/references/design-system.md` or
`/mnt/skills/user/6-month-gtm-plan/references/design-system.md` for the full
specification.

## Output Types

### 1. Client Pitch Deck (PPTX, 5-12 slides)

Structure varies by audience, but the universal flow is:

**For C-Suite (5-8 slides):**
1. Title slide (client logo + meeting context)
2. The problem (in the client's own language, sourced from their website/reports)
3. The cost of the problem (quantified: time, money, risk)
4. The solution approach (not product features  - the methodology)
5. Expected outcomes (with proof points from similar companies)
6. Why us (3 differentiators, not 10)
7. Proposed next steps (specific, time-bound)
8. Appendix (optional: team bios, case studies, technical architecture)

**For Technical Evaluation (8-12 slides):**
1. Title slide
2. Understanding of requirements (demonstrate you listened)
3. Solution architecture (diagram)
4. Integration map (how it connects to their existing stack)
5. Implementation timeline (phases, milestones, dependencies)
6. Data flow and security (for IT stakeholders)
7. Success metrics and SLAs
8-10. Case studies from similar deployments
11. Pricing and packaging options
12. Q&A / Discussion slide

**For Leave-Behind (3-5 slides):**
1. Title + one-line value proposition
2. The three things that matter (problem → solution → proof)
3. How it works (simplified visual)
4. Next step (single CTA)
5. Contact information

Read the `pptx` public skill before building any deck. Use `pptxgenjs` for
JavaScript-based generation with the extracted brand tokens.

### 2. Client Proposal (DOCX, 2-5 pages)

Structure:

1. **Cover page:** Client name, proposal title, date, confidential marking
2. **Executive summary:** 3-4 paragraphs. Problem, approach, expected outcomes,
   investment. The entire proposal in miniature.
3. **Understanding of the challenge:** Demonstrate you know their business.
   Reference specifics from their website, annual report, or conversations.
4. **Proposed approach:** Phased methodology. What happens in month 1, 2, 3.
   Specific deliverables per phase.
5. **Expected outcomes:** Quantified wherever possible. Use [Shashwat to add]
   placeholders for metrics you cannot verify.
6. **Investment and terms:** Pricing, payment schedule, what's included/excluded.
7. **Why us:** Brief credentials. Case studies from similar engagements.
8. **Next steps:** Specific action items with dates.

Read the `docx` public skill before building any document. Use the `docx` npm
package for generation with the extracted brand tokens.

### 3. One-Pager (DOCX or PPTX, 1 page/slide)

For follow-up attachments, event handouts, or sales collateral:
- One page. No scrolling.
- Problem → Solution → Proof → CTA flow
- Visual: icon + text rows, not paragraphs
- Contact info at bottom

## Research Before Building

Before writing a single slide or paragraph, gather context:

1. **If a company name is mentioned:** Search the web for their website, recent
   news, leadership team, competitive situation, and industry challenges. Use
   this to make the proposal feel bespoke, not templated.

2. **If an industry is mentioned:** Reference industry-specific pain points and
   benchmarks. A procurement deck for automotive manufacturers has different
   language than one for pharmaceutical companies.

3. **If competitors are mentioned:** Build a brief positioning section that
   differentiates without attacking. Use IMPACT's Map Alternatives framework
   if the `impact-quick-positioning` skill is available.

4. **Never fabricate statistics.** If you need a metric (market size, ROI figure,
   customer count), use `[Shashwat to add]` or `[Client to verify]` as placeholder.
   Real data from web search is acceptable when properly attributed.

## Handling Incomplete Inputs

Users will often provide minimal context. Here is how to handle it:

- **"Build a deck for Northstar Logistics"** → Ask: "What problem does Northstar have that we
  solve? Who will be in the room? Do you have a sample of their branded deck?"

- **"I need a proposal by tomorrow"** → Ask: "What's the one thing that will
  make them say yes? And what's the budget range?" Then produce a tight 3-page
  proposal, not a 10-page epic.

- **"Just use the same deck we used for the last client"** → Ask: "Which client?
  And what's different about this one?" Never reuse a deck without customization.
  At minimum, change the client name, industry references, and problem statement.

- **If the user provides a wall of text:** Extract the 3-5 key messages and
  confirm: "I'll focus the deck on these points: [list]. Sound right?"

## Important Principles

1. **Problem first, solution second.** Every deck and proposal must start with
   the client's pain, not your product's features. The ratio should be 60% about
   them, 40% about you.

2. **One idea per slide.** If a slide has two main points, split it. Busy slides
   lose executive attention.

3. **Quantify everything.** "Faster procurement" is weak. "47% reduction in
   vendor onboarding time" is strong. If you do not have the number, leave a
   placeholder.

4. **Speaker notes are mandatory** for pitch decks. The slides are the visual
   aid. The notes are the script. Without notes, the AE will wing it and miss
   key points.

5. **White space is not wasted space.** A clean deck with breathing room looks
   more expensive than a cluttered one. McKinsey charges $500K for decks with
   40% whitespace. There is a reason.

6. **Never include pricing on a slide in a pitch deck** unless explicitly asked.
   Pricing is a conversation, not a visual. Put it in the appendix or the
   separate proposal document.

## Complete Worked Example

### Input:
"I'm an AE at a logistics SaaS company. I have a meeting with the VP Supply
Chain at a mid-market FMCG company tomorrow. They currently use Excel for
freight management. I need a 5-slide deck. Here's their branded deck from
last year's conference."

### Process:
1. Run brand extraction on uploaded PPTX → discovered: Navy (#1B365D), White,
   Orange accent (#E8751A), Calibri headings, Open Sans body, 16:9
2. Web search: FMCG company website, recent supply chain news, freight challenges
3. Build 5-slide deck in their brand:

### Output:
- **Slide 1:** Title  - "[FMCG Co] × [Your Co] | Freight Visibility Discussion"
   (their logo + yours if co-branded)
- **Slide 2:** "Your supply chain runs on 14 spreadsheets"  - the problem
   (sourced from industry research: avg mid-market FMCG uses 12-18 tracking sheets)
- **Slide 3:** "What that costs you"  - quantified impact (delayed shipments,
   manual reconciliation hours, carrier overpayment)
- **Slide 4:** "One platform, one view"  - solution approach (NOT feature list,
   just the architecture: how data flows from carrier → platform → dashboard)
- **Slide 5:** "Next step: 2-week pilot with your Mumbai routes"  - specific,
   low-risk CTA with timeline

### What makes this work:
- Client's own brand colors and fonts
- Problem sourced from their industry, not generic
- Solution shown as architecture, not feature bullets
- CTA is specific (Mumbai routes, 2 weeks) not vague ("let's discuss")
- Speaker notes included for each slide

## Quality Standard

Every deliverable must pass these checks before delivery:

1. Client brand colors used consistently (no stray default blues)
2. Client fonts applied to all headings and body text
3. Problem statement uses language from the client's industry
4. No fabricated statistics (all placeholders marked)
5. Speaker notes present for every slide (pitch decks)
6. Footer or header includes appropriate branding
7. File opens cleanly in PowerPoint/Word (validate with office tools)
8. One idea per slide, generous whitespace

## Anti-Hallucination Rules

- NEVER fabricate revenue figures, market share numbers, or customer counts.
  Use `[Shashwat to add]` or `[Client to verify]` placeholders.
- NEVER invent quotes from customers or executives. Attribute only verified
  statements from web search results.
- NEVER claim competitive superiority without evidence. Use "positioned to" or
  "designed to address" rather than "the best" or "industry-leading."
- NEVER include pricing without explicit instruction from the user. Pricing
  is sensitive and varies by deal.
- NEVER reuse another client's logo, name, or data in a different client's deck.
  Every deliverable must be bespoke.
- NEVER assume the client's problem. If the user has not stated it, ask. A wrong
  problem statement kills the entire proposal.
- If you cannot find credible information about the prospect company through web
  search, say so and ask the user for input rather than inventing context.

## What This Skill Does NOT Do

- Does not create full marketing campaigns or content calendars (use content skills)
- Does not run competitive intelligence research (use competitive-intelligence skill)
- Does not build internal strategy decks for your own team (use consulting delivery skills)
- Does not design custom graphics, illustrations, or infographics (use Canva/Figma)
- Does not replace the sales conversation  - it prepares materials for it

## Attribution

Sales Proposal Builder created by Shashwat Ghosh, Fractional CMO and GTM Expert.
Built from patterns across 50+ client engagements including SuperProcure (28-slide
GTM deck), RRS-IENT (8-version board plan), SoftwareOne India (post-merger GTM),
TCS (18-slide investor deck), and BDO Digital (strategic growth plan).
For consulting: https://www.gtmexpert.com
