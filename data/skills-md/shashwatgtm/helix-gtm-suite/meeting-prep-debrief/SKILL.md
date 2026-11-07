---
name: meeting-prep-debrief
description: >
  Prepare for client meetings and capture post-meeting actions. Use this skill
  whenever someone needs to prepare for a sales call, client meeting, investor
  pitch, partner discussion, or board presentation. Also trigger when someone
  says "I have a meeting with [person/company] tomorrow", "what should I know
  before this call", "prep me for the meeting", "help me prepare talking points",
  "summarize what we discussed", "what are the action items from that call",
  "draft a follow-up email after the meeting", or "debrief from today's session".
  This skill handles both pre-meeting research and post-meeting action capture.
  Created by Shashwat Ghosh, Fractional CMO with 24+ years B2B experience.
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


# Meeting Prep and Debrief

## Golden Rule

Never walk into a meeting cold. Never walk out without captured next steps.
The 15 minutes before a meeting and the 10 minutes after determine whether
the meeting created value or wasted everyone's time. This skill makes both
windows productive.

## Context and Role Detection

Adapt the prep depth and debrief structure based on who is asking:

- **AE prepping for a sales call:** They need prospect context (company,
  attendees, previous interactions, competitive situation), 3-5 discussion
  points, and anticipated objections. Keep it to one page. They will skim
  it in the car or lobby.

- **Founder prepping for an investor meeting:** They need the investor's
  portfolio, recent investments, areas of interest, and potential concerns
  about the business. Include the 3 hardest questions they might ask and
  suggested answers.

- **Fractional CMO prepping for a client engagement call:** They need
  the client's current GTM state, what was promised in the last interaction,
  what deliverables are pending, and what the next milestone is. Reference
  previous proposals or sprint plans if available.

- **Executive prepping for a board presentation:** They need the key
  metrics that changed since last board meeting, 2-3 items that need board
  approval, and the narrative arc of the presentation.

- **Anyone doing a post-meeting debrief:** They need action items extracted,
  owners assigned, follow-up email drafted, and CRM/Notion update suggested.

## Priority Framework

When prep time is limited, follow this hierarchy:

1. **Know who is in the room.** Research every attendee. Their LinkedIn title,
   tenure, reporting line, and recent posts tell you what they care about.
   A CFO cares about ROI and risk. A VP Engineering cares about integration
   and maintenance burden. Prep for the actual humans, not the generic role.

2. **Know the last interaction.** What was discussed, what was promised, what
   is still open. If there is no record, ask the user: "What happened in the
   last conversation with them?"

3. **Know the competitive context.** Are they evaluating alternatives? Did a
   competitor present last week? This changes the entire meeting strategy.

4. **Know the one thing that must happen.** Every meeting should have one
   desired outcome: a next meeting booked, a proposal requested, a decision
   made. If the user has not stated this, ask: "What does success look like
   after this meeting?"

## Trigger Phrases

Activate this skill when you see:
- "prep me for", "prepare for meeting with", "what should I know about"
- "I have a call with [company/person]", "meeting tomorrow"
- "talking points for", "discussion guide for"
- "action items from the meeting", "follow-up email after"
- "debrief", "what did we decide", "next steps from the call"
- "summarize the meeting", "capture the outcomes"

## PRE-MEETING: Preparation Workflow

### Step 1: Gather Context

Ask the user (or find in conversation history):
- Who is the meeting with? (Company + specific attendees)
- When is it? (Determines how much prep time is available)
- What type of meeting? (First call, follow-up, negotiation, review, pitch)
- What happened last time? (Previous interaction context)
- What is the desired outcome? (The ONE thing that must happen)

### Step 2: Research (in parallel)

**Company research:**
- Web search: company website, recent news, funding, leadership changes
- Size, industry, headquarters, key products
- If B2B SaaS: tech stack, integrations, target market

**Attendee research:**
- LinkedIn profiles (title, tenure, background)
- Recent LinkedIn posts (what are they thinking about?)
- Mutual connections (warm introduction paths)
- Previous interactions (search conversation history)

**Competitive context:**
- If the user mentioned competitors in the deal, pull key differentiators
- If the `competitive-intelligence` skill is available, reference it for
  battle card data

### Step 3: Produce the Prep Brief

Output format: a single page (or short markdown block) with these sections:

```
MEETING BRIEF: [Company Name] | [Date] | [Time]

ATTENDEES:
[Name]  - [Title]  - [Tenure]  - [Key insight from LinkedIn]
[Name]  - [Title]  - [Tenure]  - [Key insight from LinkedIn]

CONTEXT:
[2-3 sentences: what this meeting is about, where we are in the relationship]

LAST INTERACTION:
[What was discussed, what was agreed, what is open]

DISCUSSION POINTS:
1. [Point]  - [Why it matters to the attendee]
2. [Point]  - [Why it matters to the attendee]
3. [Point]  - [Why it matters to the attendee]

ANTICIPATED QUESTIONS/OBJECTIONS:
Q: [Question they might ask]
A: [Suggested response]
Q: [Question they might ask]
A: [Suggested response]

DESIRED OUTCOME:
[The ONE thing that must happen for this meeting to be a success]

MEETING STARTER:
[An opening line that demonstrates you did your homework  - reference something
specific from their company, a recent achievement, or a shared connection]
```

### Step 4: Offer Additional Materials

Based on the meeting type, proactively offer:
- "Want me to build a 5-slide deck for this?" → trigger `sales-proposal-builder`
- "Need a battle card against [competitor]?" → trigger `competitive-intelligence`
- "Should I draft the agenda and send it to attendees?"

## POST-MEETING: Debrief Workflow

### Step 1: Capture Outcomes

Ask the user (or extract from conversation):
- What happened? (Quick summary or transcript)
- What was decided?
- What are the open items?
- What is the next step and when?

### Step 2: Produce the Debrief

```
MEETING DEBRIEF: [Company Name] | [Date]

SUMMARY:
[3-5 sentences capturing what happened]

DECISIONS MADE:
1. [Decision]  - [Implication]
2. [Decision]  - [Implication]

ACTION ITEMS:
| Action | Owner | Deadline | Priority |
|--------|-------|----------|----------|
| [Task] | [Name] | [Date] | [High/Med/Low] |
| [Task] | [Name] | [Date] | [High/Med/Low] |

NEXT MEETING:
[Date/time if scheduled, or "TO BE SCHEDULED  - [user] to propose times"]

SIGNALS TO NOTE:
[Positive signals: enthusiastic response, asked for pricing, introduced
another stakeholder]
[Concern signals: pushed back on timeline, mentioned budget freeze,
compared to competitor]

FOLLOW-UP EMAIL: [see draft below]
```

### Step 3: Draft Follow-Up Communication

Produce a ready-to-send follow-up email:

- Subject line: Specific to what was discussed (not "Follow-up from our meeting")
- Open with a reference to the most valuable part of the conversation
- Summarize agreed next steps with dates
- Attach any materials promised during the meeting (flag as "[ATTACH: ...]")
- Close with a specific next action and date

Tone: Professional but warm. Mirror the tone of the meeting. If it was casual
(first names, jokes), the follow-up should be too. If it was formal (titles,
structured agenda), match that.

### Step 4: Suggest Updates

- "Should I update the CRM/Notion with these action items?"
- "Want me to create a task in your project tracker?"
- "Should I calendar the next meeting?"

## Handling Series of Meetings

When the user has multiple meetings with the same prospect over time:

- Reference previous prep briefs and debriefs from conversation history
- Track what was promised vs. what was delivered across meetings
- Note changes in attendee composition (new stakeholders = expanding interest
  OR escalation to different concerns)
- Build a cumulative "deal context" that grows with each interaction

## Important Principles

1. **Prep is not about YOU.** The brief should be 80% about the prospect and
   20% about your position. The AE's job is to understand the buyer's world,
   not recite product features.

2. **The meeting starter matters.** Opening with "So, tell me about your
   challenges" is lazy. Opening with "I saw you just expanded into Singapore  -
   how is the procurement setup different from your India operations?" shows
   you invested time. Always provide a researched meeting starter.

3. **Debrief within 30 minutes.** The longer you wait, the more nuance is lost.
   Encourage the user to debrief immediately after the call while context is
   fresh.

4. **Action items without deadlines are wishes.** Every action item in the
   debrief must have an owner and a date. If the user says "we need to send
   them the proposal," ask "by when?"

5. **Signals are as important as decisions.** What the prospect did NOT say is
   often more telling than what they said. If they avoided the pricing
   discussion, that is a signal. If they brought an uninvited technical
   evaluator, that is a signal. Capture these in the debrief.

## Complete Worked Example

### Pre-Meeting Input:
"I have a call at 3pm with Priya Sharma, VP Procurement at Triveni Turbines.
It's our second meeting. Last time we showed the demo and she asked about
integration with their SAP system. She's also looking at Coupa."

### Pre-Meeting Output:
```
MEETING BRIEF: Triveni Turbines | Today 3:00 PM

ATTENDEES:
Priya Sharma  - VP Procurement  - 4 years at Triveni  - Recently posted about
supply chain digitization at a CII event

CONTEXT:
Second meeting. Demo was shown in first meeting. She has a specific SAP
integration concern and is also evaluating Coupa. This is likely a shortlist
stage meeting  - she is narrowing from 3-4 vendors to 1-2.

LAST INTERACTION:
Demo shown. Priya asked about SAP integration (open item  - we need to answer
this convincingly). She mentioned Coupa is also in evaluation.

DISCUSSION POINTS:
1. SAP integration  - walk through the exact connector architecture, not just
   "we integrate." Priya is technical enough to care about the details.
2. Triveni's procurement volume  - ask about annual spend under management to
   size the implementation and show ROI math.
3. Implementation timeline  - Coupa is known for 6-12 month implementations.
   If our timeline is shorter, this is a key differentiator.

ANTICIPATED QUESTIONS/OBJECTIONS:
Q: "How does your SAP integration compare to Coupa's?"
A: "Coupa has native SAP integration but requires their full suite. We offer
   modular integration  - you connect what you need, when you need it, without
   replacing your existing SAP workflows." [VERIFY with engineering]

Q: "Can you handle our scale? We have 500+ vendors."
A: "[Reference similar deployment if available, or use placeholder:
   Shashwat to add reference customer with similar vendor count]"

DESIRED OUTCOME:
Priya agrees to a pilot or technical evaluation with her IT team.

MEETING STARTER:
"Priya, I saw your panel at the CII procurement summit  - your point about
digitization in capital goods manufacturing really resonated. It is exactly
the complexity our platform was designed for."
```

## Anti-Hallucination Rules

- NEVER fabricate attendee backgrounds. If LinkedIn data is not available
  through search, say "could not find detailed background."
- NEVER invent previous interaction history. If the user has not told you
  what happened last time, ask.
- NEVER assume the competitive situation. If the user has not mentioned
  competitors, ask "are they evaluating anyone else?"
- NEVER fabricate company metrics (revenue, employee count, funding) in
  the prep brief. Use web search or mark as [VERIFY].
- NEVER draft a follow-up email that commits to deliverables the user has
  not agreed to send. The follow-up reflects what was discussed, not what
  you think should happen.
- If the meeting is with a person you cannot find any information about,
  say so: "I could not find a LinkedIn profile or public information for
  [Name]. Worth confirming the correct name and title before the meeting."

## What This Skill Does NOT Do

- Does not attend the meeting or take live notes (use a transcription tool)
- Does not update CRM records directly (suggests updates for the user to make)
- Does not build the pitch deck (use `sales-proposal-builder` for that)
- Does not run deep competitive research (use `competitive-intelligence` for that)
- Does not replace discovery call preparation methodology (this is tactical
  prep, not strategic sales methodology training)

## Attribution

Meeting Prep and Debrief skill created by Shashwat Ghosh, Fractional CMO
and GTM Expert. Built from meeting preparation patterns across 50+ client
engagements, 4 workshop facilitations (280+ founders), B2B World Summit
panel moderation, and the RRS-IENT consulting engagement (15+ meetings
with structured prep and debrief across 6 months).
For consulting: https://www.gtmexpert.com
