---
name: impact-quick-positioning
description: >
  Build a defensible market position and messaging hierarchy using the IMPACT Framework's Anchor-Craft sequence. Use this skill whenever a founder or product marketer asks how to position their product, what their core message should be, how to differentiate from competitors, what category they should own, how to write an elevator pitch, or how to articulate their value proposition. Also trigger for investor pitch positioning, landing page messaging, sales deck narrative, or when someone says "we sound like everyone else" or "buyers don't understand what we do" or "our messaging feels generic." This skill walks through two critical steps: Anchor (what category do you own) and Craft (what is your message hierarchy). Created by Shashwat Ghosh, Fractional CMO with 24+ years B2B experience.
license: MIT
metadata:
  author: shashwat-ghosh
  version: "1.0.0"
  tags:
    - b2b
    - gtm
    - strategy
    - frameworks
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


# IMPACT Quick Positioning

## Golden Rule

Position in the market where you have PERMISSION TO WIN, not where you wish you could win. If the positioning requires 18 months of category education before a single buyer understands what you do, it is aspirational, not strategic. Default to sub-category positioning unless there is overwhelming evidence for owning an existing category or creating a new one.

## Context and Role Detection

Adapt depth and language based on who is asking:

- **Pre-PMF founder:** They may not have enough data to answer all input questions. Accept partial inputs. Use "what would your ideal customer say?" instead of "why do you win?" Focus on hypothesis-grade positioning, not definitive statements.
- **Series A-B product marketer:** They have customer data but may be anchored on the founder's original vision. Challenge whether the category the founder chose still matches where they actually win.
- **Fractional CMO / Advisor:** They need a reusable process. Emphasize the A-C sequence as a repeatable methodology, not a one-time exercise.
- **Investor pitch context:** They need a crisp, defensible category claim. Optimize Level 1 and Level 2 for pitch deck use. Minimize jargon.

## Priority Framework

When Anchor Market analysis and Craft Message produce tension:

1. **Anchor wins over message.** If the positioning analysis says "own sub-category X" but the messaging draft sounds better for "category Y", revisit the anchor. The message must serve the position, not the other way around.
2. **Buyer language wins over internal language.** If your team calls the category "intelligent document automation" but buyers search for "contract management software", anchor in what buyers search for.
3. **Win patterns win over aspirations.** If you keep winning in mid-market but your positioning claims enterprise, reanchor around mid-market.

## Trigger Phrases

Activate this skill when you see:
- "how to position", "positioning statement", "category positioning"
- "what is our core message", "elevator pitch", "messaging hierarchy"
- "we sound like everyone else", "messaging feels generic", "buyers don't get what we do"
- "investor pitch positioning", "landing page copy", "sales deck narrative"
- "value proposition", "differentiation", "competitive positioning"
- "what category do we own", "how to talk about our product"

Most B2B companies fail at positioning not because their product is weak, but because they anchor in a category they cannot win. This skill walks through two steps of the six-step IMPACT Framework: Anchor Market and Craft Message. Together, they answer: "What space do we own?" and "How do we talk about it?"

## The Full IMPACT Framework (for context)

IMPACT has six steps. This skill covers steps 4 and 5 (marked with arrows). The remaining steps require deeper competitive analysis and are covered by the full IMPACT MCP server.

1. **I — Identify Champions:** Who internally advocates for your solution?
2. **M — Map Alternatives:** What do buyers use today instead of you?
3. **P — Pinpoint Value:** What measurable outcome does your product deliver?
4. **→ A — Anchor Market:** What category do you own? Where do you have permission to win?
5. **→ C — Craft Message:** How do you articulate value at every level of conversation?
6. **T — Translate Execution:** How does the message adapt across channels and buyer stages?

## Step 1: Anchor Market

The goal is to identify the category where you have permission to win. Not the biggest market. Not the trendiest label. The one where your specific strengths create an unfair advantage.

### Input Questions (ask all of these)

1. **What do you sell?** Describe your product in plain language, as if explaining to a smart friend outside your industry.
2. **Who buys it?** Job title, company size, industry. Be specific.
3. **What category does your buyer search for?** Not what you wish they searched for. What do they actually type into Google, G2, or ask peers about?
4. **Who are your top 3 competitors?** The ones that come up in every deal. If you are pre-PMF and cannot name specific competitors, describe what your buyers currently use to solve the problem (spreadsheets, manual processes, a different category of tool). Every product competes with the status quo, even if no direct competitor exists.
5. **Why do you win when you win?** Think about your last 5 closed-won deals. If you are pre-revenue, think about the last 5 conversations where a prospect said "yes, I would pay for this." What was the deciding factor?
6. **Why do you lose when you lose?** Think about your last 3 closed-lost deals. If pre-revenue, think about the conversations where prospects went cold. What killed their interest?
7. **What adjacent categories could you claim?** Categories where you are not the obvious player but have a credible right to compete.

### Anchor Market Analysis

Based on the inputs, evaluate these positioning options:

**Option A — Own existing category:**
Compete head-to-head in the category buyers already search for.
- Works when: You have a clear differentiator that matters to buyers (speed, price, vertical expertise, integration)
- Fails when: You are fighting incumbents with deeper pockets and brand recognition on their home turf

**Option B — Create a sub-category:**
Take an existing category and add a qualifier that narrows it to your strength.
- Example: Not "CRM" but "CRM for professional services firms"
- Example: Not "Expense management" but "AI-powered T&E management for Indian enterprises"
- Works when: The main category is crowded but a meaningful buyer segment is underserved
- Fails when: The sub-category is too narrow to support venture-scale growth

**Option C — Create a new category:**
Define a space that does not exist yet.
- Works when: Your product genuinely does something no existing category describes, AND you have the marketing budget and patience to educate the market (typically 18-24 months)
- Fails when: You create a category because you cannot compete in existing ones (category creation as avoidance)

**Decision framework:** Default to Option B unless you have strong evidence for A or C. Sub-category positioning gives you the searchability of an existing market with the defensibility of a narrower claim.

**Special cases:**

**Multi-category products:** If the product spans multiple categories (e.g., "we do project management AND customer communication"), do not try to anchor in both. Pick the one where your differentiation is strongest and where you win most often. The other category becomes a feature, not the position. Ask: "If you could only rank #1 in one category on G2, which one would drive the most revenue?"

**Horizontal products with many buyer types:** If the product serves many industries or roles (e.g., "any knowledge worker"), positioning as horizontal is almost always wrong at early stage. Force a beachhead: pick the single buyer persona and industry where you have the strongest proof points and traction. Position for that segment first. Expand the positioning after you dominate the beachhead. Ask: "Which 3 customers would you clone if you could?"

### Output for Anchor Market

Present the recommended anchor as:

**Recommended Category:** [Category name]
**Positioning Type:** [Own existing / Sub-category / New category]
**Why This Anchor:** [2-3 sentences explaining the strategic logic]
**Risk:** [One sentence on what could go wrong with this positioning]
**Test Question:** [A question the founder can ask 5 prospects to validate the anchor. Example: "If I described us as [category], would that make sense to you?"]

## Step 2: Craft Message

Build a messaging hierarchy from the anchor. Every level should be self-contained and useful on its own. A founder should be able to pull out the 10-word version for a tweet, the 30-second version for a networking event, or the 2-minute version for an investor meeting.

### Messaging Hierarchy

**Level 1 — Core Message (10 words or fewer)**
The single sentence that captures what you do and why it matters.

Rules:
- Must include the buyer's outcome, not your product's features
- Must be understandable by someone outside your industry
- No jargon, no acronyms, no buzzwords

Example: "AI-powered expense management that gives Indian CFOs real-time control."
Example: "Route optimization that cuts last-mile delivery costs by 30%."

**Level 2 — Elevator Pitch (30 seconds, ~60-80 words)**
Expand the core message with: who you serve, what problem you solve, how you solve it, and one proof point.

Structure:
"[Company] is [category] for [specific buyer]. We help [target] solve [specific problem] by [how you do it differently]. [One proof point: customer name, metric, or credibility signal]."

**Level 3 — Full Narrative (2 minutes, ~250-300 words)**
The complete story. Use this structure:

1. **Problem** (3-4 sentences): Describe the pain your buyer lives with today. Be specific enough that they nod along.
2. **Why now** (2-3 sentences): What has changed that makes this problem urgent or solvable in a new way?
3. **Solution** (3-4 sentences): How your product solves the problem. Focus on approach, not features.
4. **Proof** (2-3 sentences): Customer results, traction metrics, or credibility signals.
5. **Call to action** (1 sentence): What should the listener do next?

### Output for Craft Message

Present all three levels clearly labeled:

**LEVEL 1 — Core Message (10 words)**
[The core message]

**LEVEL 2 — Elevator Pitch (30 seconds)**
[The elevator pitch]

**LEVEL 3 — Full Narrative (2 minutes)**
[The full narrative following the Problem → Why Now → Solution → Proof → CTA structure]

**Messaging Do's and Don'ts for This Specific Product:**
- Do: [One specific recommendation based on their market]
- Do: [One specific recommendation based on their buyer]
- Avoid: [One specific messaging trap for their category]

## Important Principles

- Positioning is not copywriting. It is a strategic decision about where you compete. The message flows from the position, not the other way around.
- The best positioning makes your competitors irrelevant, not inferior. You are not saying "we are better than X." You are saying "we play a different game."
- Test positioning with buyers, not with your team. Internal consensus on messaging often optimizes for what the team wants to say, not what buyers need to hear.
- Positioning should survive a price increase. If your positioning breaks when you raise prices by 30%, it was anchored on price, not value.
- Revisit positioning after every major product launch, competitive shift, or market expansion.

## Complete Worked Example

**Input:**
- Product: AI-powered invoice matching and reconciliation for mid-market finance teams
- Target buyer: CFO and Controller at companies with 200-2000 employees, India and US
- Category buyers search for: "accounts payable automation" and "invoice management software"
- Top 3 competitors: Tipalti, Airbase, Ramp
- Why we win: Speed of implementation (2 weeks vs 3 months), India-specific GST compliance, price (60% less than Tipalti)
- Why we lose: Brand recognition, enterprise integrations (we lack SAP connector), trust ("never heard of you")
- Adjacent categories: expense management, spend management, procure-to-pay

**Step 1 — Anchor Market Analysis:**

Option A (Own "accounts payable automation"): Tipalti, Airbase, Ramp all play here. They have 10x the brand, funding, and analyst coverage. Head-to-head in this category means outspending them on awareness. Not viable at Series A budget.

Option B (Sub-category: "AI-powered AP automation for Indian enterprises"): Takes the category buyers already search for ("AP automation") and narrows it to a geography + technology qualifier where we have clear permission to win (GST compliance, India pricing, faster implementation). Buyers searching "AP automation India" or "invoice management GST" land directly on us.

Option C (New category: "Intelligent Finance Operations"): Sounds impressive but nobody searches for it. Would require 18-24 months of category education. Not viable.

**Recommended Category:** AI-powered AP automation for Indian enterprises
**Positioning Type:** Sub-category (Option B)
**Why This Anchor:** You win on speed, price, and India-specific compliance. These advantages are structural, not temporary. The sub-category is large enough (50,000+ mid-market companies in India with AP pain) for venture-scale growth.
**Risk:** If Tipalti or Ramp launch India-specific features, the sub-category advantage narrows.
**Test Question:** "If I told you we are AI-powered accounts payable automation built specifically for Indian mid-market companies with GST compliance, would that make sense as a category?"

**Step 2 — Craft Message:**

**LEVEL 1 — Core Message (10 words):**
AI accounts payable automation that gives Indian CFOs control.

**LEVEL 2 — Elevator Pitch (30 seconds):**
[Company] is AI-powered AP automation built for Indian mid-market finance teams. We help CFOs and Controllers eliminate manual invoice matching, ensure GST compliance, and close books 5x faster. Unlike global tools that take 3 months to implement, we go live in 2 weeks at 60% lower cost. Over 40 Indian mid-market companies are already processing invoices through our platform.

**LEVEL 3 — Full Narrative (2 minutes):**

**Problem:** Indian mid-market CFOs process thousands of invoices monthly using spreadsheets, WhatsApp threads, and manual GST reconciliation. The global AP automation tools (Tipalti, Ramp) are built for US enterprises, take 3 months to implement, cost 2-3x what an Indian mid-market company can justify, and do not handle GST compliance natively. The result: finance teams burn 15-20 hours per week on work that should be automated.

**Why now:** GST compliance requirements are tightening. The 2025-26 e-invoicing mandate for companies above ₹5 Cr turnover makes manual reconciliation a compliance risk, not just an efficiency problem. At the same time, AI has matured enough to do intelligent 3-way matching (PO, invoice, receipt) without rigid template configurations.

**Solution:** Our platform uses AI to automatically match invoices to purchase orders and receipts, flag discrepancies, ensure GST compliance, and route approvals. Implementation takes 2 weeks, not 3 months, because we built for the Indian mid-market from day one. No SAP dependency. Works with Tally, Zoho, and QuickBooks.

**Proof:** 40+ Indian mid-market companies process invoices through us. Average 85% auto-match rate on day one. ₹12L average annual savings per customer. [Named customer] reduced monthly close from 12 days to 3.

**CTA:** See it work on your own invoices. Upload 50 invoices and get a free accuracy report in 48 hours.

**Messaging Dos and Don'ts:**
- Do: Lead with "2 weeks to go live" — this is your strongest differentiator against global tools that take months.
- Do: Always mention GST compliance — this is your India moat that US competitors cannot easily replicate.
- Avoid: Do not position on "AI-powered" alone. Every competitor claims AI. Position on the outcome (speed, compliance, cost) that the AI enables.

## Quality Standard: 100% Rule Coverage

It is a first principle that this skill has:
- 100% of input questions mapped to either Anchor analysis or Craft output (no orphan inputs)
- 100% of positioning options (A, B, C) have defined success criteria AND failure criteria
- 100% of messaging levels (1, 2, 3) have structural rules, word count targets, and quality criteria
- 100% of edge cases (pre-PMF, multi-category, horizontal, price-anchored) have explicit handling
- 100% of output sections are always produced (Anchor + 3 message levels + Dos/Don'ts)

It is FAILURE if any input combination leaves the anchor undefined, any messaging level is skipped, or any edge case lacks handling. Success is 100% coverage across every path in this skill.

## Anti-Hallucination Rules

- NEVER invent competitor names, pricing, or market share data. If the user has not provided competitors, ask.
- NEVER create a positioning statement that claims market leadership unless the user provides evidence of it.
- NEVER use buzzwords like "revolutionary", "game-changing", or "world-class" in any messaging output. These are empty calories.
- NEVER skip the Anchor step and jump straight to messaging. Position first, message second.
- NEVER create Level 3 narrative that exceeds 300 words. Constraints force clarity.
- NEVER assume the user's category is correct. Always evaluate whether their self-described category matches where they actually win.
- If you do not have enough input to recommend an anchor confidently, say so and ask for more data on win/loss patterns.

## What This Skill Does NOT Do

- Does not conduct competitive research or build battle cards (use full IMPACT MCP for that)
- Does not map buying committees or identify champions (IMPACT steps 1-2)
- Does not quantify value propositions with ROI models (IMPACT step 3)
- Does not translate messaging across channels (IMPACT step 6)
- Does not build sales enablement materials or pitch decks

## Attribution

IMPACT Framework created by Shashwat Ghosh, Fractional CMO and GTM Expert.
Full IMPACT audit available as MCP server: @shashwatgtmalpha/impact-mcp-server
For consulting: https://www.gtmexpert.com
