---
name: campaign-strategy
description: Create email campaign strategy for a single segment. Generates email sequence blueprints and AI personalization variables for one segment within a campaign plan. Receives a segment folder path and reads the segment's angle from the parent plan.md. Triggers on requests like 'create strategy for segment', or when dispatched by campaign-planning.
model: opus
thinking: true
---

# Campaign Strategy Skill

Transform client research into an actionable email strategy for a single segment. Output email sequence blueprints and AI personalization variables for the Email Copywriting skill to execute.

## Output Contract

`strategy.md` is not machine-parsed - it's read by downstream skills (email-copywriting, prompt-writer) for context. Hard rules this skill must honor anyway, since its output flows into files that other tools read:

- AI variable names must be Title Case with spaces: `Subject Line`, `First Line`, `PS Line`. They become `[Title Case]` brackets in emails.md and H3 headings in prompts.md - the three have to agree exactly.
- AI variable names ≤30 chars (enforced in prompts.md by the prompt-writer contract).
- Never reference data sources personalization tools typically lack (news, funding, events, social media, blogs) - these propagate into prompts.md and break at runtime when the data is not available.

## Required Context

Before creating a strategy, always load the client context:

1. **Read `{workspace}/research.md`** - Client research: overview, ICP, value prop, case studies, lead magnets
2. **Read `{workspace}/notes.md`** (if it exists) - Client-specific preferences
3. **Read plan.md from parent directory** - Get segment definition, angle, ICP, and testing hypothesis

**Directory Structure Reference** (`{workspace}` = the client campaign workspace, default `./cold-email/{slug}/`):
```
{workspace}/
├── research.md       # Client research - ICP, value prop, case studies
├── notes.md          # Optional client preferences and feedback
└── {plan_folder}/    # One per campaign, e.g. "03-15 - plan 1"
    ├── plan.md           # Plan with ICP, segments, angles, testing hypothesis
    ├── 1 - {segment}/
    │   └── strategy.md   # THIS file - segment strategy
    ├── 2 - {segment}/
    │   └── strategy.md
    └── ...
```

## Required Inputs

After loading context, gather:

1. **Segment folder path** - e.g., `{workspace}/03-15 - plan 1/1 - early-stage/`
2. **Plan.md** - Read from parent directory of segment folder to get:
   - Broad ICP definition
   - Segment-specific criteria
   - Messaging angle for this segment
   - Testing hypothesis (if any)
3. **Client Research Document** - Check `{workspace}/research.md` or uploads
4. **Campaign Goal** - What action to drive:
   - Book demos/meetings
   - Drive traffic to landing page
   - Get replies for qualification
   - Promote lead magnet

## Output Format

Generate a single Markdown document saved to `{segment_folder}/strategy.md`:

```markdown
# {Client} - {Segment Name} Strategy

## Segment Overview
- **ICP**: {Broad ICP from plan.md}
- **Segment**: {Specific segment criteria from plan.md}
- **Angle**: {Messaging angle from plan.md}
- **Goal**: reply-based / click-based
- **Funnel Type**: {type}

## Email Sequence

[Markdown format - see references/email-sequence-guide.md]

## AI Personalization Variables

[JSON array - see references/ai-variables-guide.md]

## AI Rewriting (Optional)

Enable: [yes/no]
Tone: [description]

## Sequence Tests (Optional)

[Only when supporting macro test from plan.md Testing Hypothesis]
```

## AI Rewriting Guidelines

Include the AI Rewriting section when:
- Campaign uses AI personalization (first lines, PS lines, body variables)
- Higher quality/variation is desired for personalization outputs
- Budget allows ($5 per 1,000 contacts for rewriting flow)

Skip AI Rewriting when:
- No AI personalization variables exist
- Subject lines only (rewriting too risky for subjects)
- Budget constraints require minimizing AI costs

When enabled, prompt-writer will add a rewriting prompt at the end of prompts.md.

## Core Principles

1. **Building block approach** - Treat copy and campaigns as modular building blocks (like Legos) that can be tested in many combinations. Volume of combinations is how we discover what works. See `references/building-blocks.md` for the full philosophy.

2. **Start strong, diversify, close strong** - Lead email uses strongest angle. Middle emails try new angles. Final email is a breakup with second-strongest angle.

3. **Relevance over personalization** - Don't just use {firstName}. Show deep understanding of their world using AI variables sourced from LinkedIn/website.

4. **One idea per email** - Each email has one goal, one CTA, one main point.

5. **Value-first** - Every touch provides insight, education, or genuine help.

6. **Data constraints** - AI variables can ONLY use: company website main page, LinkedIn company page, LinkedIn individual profile. No news, events, funding announcements, or timely triggers.

## Sequence Structure

- **3-5 emails maximum**
- **Delays**: 0 days for first, 2-4 days between follow-ups
- **CTAs**: Reply-based for meetings, click-based for lead magnets. **Every email's CTA asks for the actual offer, including Email 1** (which leads with the strongest version of that ask). No soft diagnostic questions as CTAs. Never send naked booking links - ask a direct question first.
- **Length**: keep static bodies punchy - at or under ~80 words (follow-ups well under). email-review enforces a hard ceiling.
- **Format**: AI variables use `{{Title Case}}`; every email signs with `{sender_signature}`.

## Workflow

1. Receive segment folder path
2. Read plan.md from parent directory to get ICP, segment definition, and angle
3. Load client research from `{workspace}/research.md`
4. Read references:
   - [references/building-blocks.md](references/building-blocks.md) - Campaign testing philosophy
   - [references/email-sequence-guide.md](references/email-sequence-guide.md) - Sequence planning details
   - [references/ai-variables-guide.md](references/ai-variables-guide.md) - Personalization patterns
   - [references/sequence-tests-guide.md](references/sequence-tests-guide.md) - Email sequence A/B testing
5. **Check for test opportunities** (optional):
   - Read plan.md Testing Hypothesis section
   - Evaluate if sequence tests would SUPPORT (not conflict with) macro test
   - Only propose tests that refine HOW, not change WHAT (ICP/angle/offer)
   - Skip tests if first campaign for client, low TAM, or no clear hypothesis
6. Generate strategy document with email sequence (Markdown) and AI variables (JSON)
7. Save to `{segment_folder}/strategy.md`

## Alignment Checklist

Before finalizing, verify:
- [ ] Value props from client research are woven through sequence
- [ ] Segment-specific pain points inform email hooks
- [ ] Angle from plan.md is reflected in the messaging
- [ ] Funnel type matches campaign goal
- [ ] Lead magnets integrated at appropriate point
- [ ] AI variables feasible with available data sources
- [ ] Each email has distinct purpose in sequence progression

## Edit Mode (Improvement Context)

When invoked with improvement context (`mode: "edit"`), this skill edits/rewrites portions of strategy.md while preserving what works.

### Detecting Edit Mode

Check for improvement context in the conversation:
- `mode: "edit"` indicates edit mode
- `trigger: "analytics"` or `trigger: "feedback"` indicates source
- `improvement_instruction` contains specific changes to make

### Edit Mode Workflow

1. **Read improvement context**: Extract `improvement_instruction` object
2. **Load existing strategy.md**: Parse current strategy from segment folder
3. **Identify preservation zones**: What should NOT change (see below)
4. **Identify change zones**: What specifically to modify
5. **Apply scoped changes**: Only modify specified sections
6. **Generate diff**: Show before/after for changed sections
7. **Get approval**: Wait for user to confirm changes
8. **Save**: Update strategy.md with approved changes
9. **Cascade check**: Notify if changes affect downstream files (emails.md, prompts.md)
10. **Log**: Update improvement-log.md in plan folder

### Handling Edit Scopes

| Scope | Action | What Changes | Cascades To |
|-------|--------|--------------|-------------|
| "email sequence" | Rewrite email descriptions | Email blueprint section | emails.md, prompts.md |
| "AI variables" | Update AI variable definitions | AI variables JSON | prompts.md |
| "segment overview" | Update ICP, goal, funnel type | Overview section | May affect all |
| "pivot angle" | Change messaging angle | Multiple sections | emails.md, prompts.md |
| "full rewrite" | Generate new strategy | Everything | All downstream |

### Preservation Rules

When editing strategy.md:

**Always preserve (unless explicitly changing):**
- ICP and segment definition (unless pivoting)
- Available data sources and constraints
- Funnel type (reply-based vs click-based)
- Core value proposition from client research

**Consider preserving:**
- Email sequence structure if only changing copy angle
- AI variable names if prompts are working

**Safe to change:**
- Email descriptions and goals
- AI variable definitions
- Messaging angle and hooks
- Offer/CTA specifics

### Edit Mode Output Format

```markdown
## Proposed Changes to strategy.md

### Email Sequence Section

**Before:**
Email 3:
- primary_goal: Re-engage with social proof
- description: Share a case study relevant to their industry
- delay_in_days: 3

**After:**
Email 3:
- primary_goal: Re-engage with curiosity hook
- description: Ask a thought-provoking question about their growth strategy, no case study yet
- delay_in_days: 3

**Rationale:** Email 3 has 15% lower opens - case study subject lines may feel too salesy

### Cascade Impact
- emails.md: Email 3 will need rewriting (invoke email-copywriting after approval)
- prompts.md: No changes needed (same AI variables)

---

Approve these changes? [Yes/No/Modify]
```

### Analytics-Informed Editing

When `analytics_context` is provided:
- Use `sequence_stats` to identify which emails need strategic changes
- Reference `weak_spots` for specific improvement areas
- Consider `sibling_comparison` to learn from winning campaigns

**Common patterns:**
- Low Email 1 opens = Strengthen opening hook strategy
- Drop-off after Email 2 = Email 3 strategy needs pivot
- Low replies across all = CTA or offer strategy issue

### Feedback-Informed Editing

When `feedback_context` is provided:
- "Wrong angle" = Pivot messaging strategy
- "Offer not resonating" = Update lead magnet/CTA strategy
- "ICP mismatch" = Update segment overview section
- "Emails too long" = Adjust email descriptions

### Cascade Notifications

After editing strategy.md, check if changes affect downstream files:

| Change Type | Affects | Action Needed |
|-------------|---------|---------------|
| Email descriptions | emails.md | Re-run email-copywriting |
| AI variables | prompts.md | Re-run prompt-writer |
| ICP or offer | All files | Consider full regeneration |

Notify user: "Strategy updated. These downstream files may need regeneration: [list]"

### Edit Mode Checklist

Before saving edits, verify:
- [ ] Only specified sections were modified
- [ ] Preservation zones respected
- [ ] Changes align with client research
- [ ] Cascade impacts identified
- [ ] Diff shown and approved by user

## Sequence Test Guidelines

Define micro-level email sequence tests that complement (not duplicate) macro-level tests from campaign-planning.

> **Two A/B levels - don't confuse them.** This skill defines **email-step A/B** (`### Variant A/B` *inside one step* - subject, hook, CTA). Testing **whole sequences against each other** is a different thing: a **segment-level sequence A/B test**, set up in campaign-planning as `percentage` mode (random %-distribution arms, each arm a totally different sequence). If the plan is in `percentage` mode, each arm is its own segment folder and you write its full sequence normally - the "test" is the arm itself, so you usually skip within-step variants in that arm.

**What campaign-planning handles (DON'T duplicate):**
- ICP testing (different personas/industries)
- Messaging Angle testing (different hooks/pain points)
- Lead Magnet testing (different offers)
- Whole-sequence testing (`percentage` mode - each arm a different full sequence)

**What sequence tests handle:**
- Email execution tests within a SINGLE segment/arm
- Tests defined here, implemented in emails.md by email-copywriting skill
- Variants appear in same emails.md file (Variant A / Variant B)

### Testable Variables

Only email sequence tests (no prompt tests):

| Category | Variables |
|----------|-----------|
| **Subject Line** | Personalized vs static, short vs medium, question vs statement |
| **Opening Hook** | With/without AI first line, question vs observation |
| **Body Structure** | Short (3-4 lines) vs medium (5-7 lines), paragraph vs bullets |
| **Social Proof** | Include vs exclude case study reference, metric vs name drop |
| **CTA Phrasing** | Low commitment ("Curious if...") vs direct ("Worth 15 min?") |
| **Tone** | Casual vs professional, humble vs assertive |
| **PS Line** | With vs without, personal vs professional content |
| **Timing** | Short delays (2-2-3 days) vs long (3-4-5 days) |
| **Email Length** | Concise vs detailed |
| **Proof Placement** | Early (email 1-2) vs late (email 3) |

### When to Propose Tests

- Plan has clear macro hypothesis to support (sequence test refines delivery)
- Campaign targets 5,000+ prospects (enough volume to split 50/50)
- Two reasonable approaches exist for an element
- Client expressed preference worth validating
- Historical data suggests optimization opportunity

### When to Skip Tests

- Macro test is already complex (don't add noise)
- Limited TAM (<2,000 contacts - not enough volume)
- First campaign for client (establish baseline first)
- No clear hypothesis (testing for testing's sake)
- Tests would conflict with plan's macro test variable

### Test Design Rules

1. **Maximum 1 test per strategy** (keep it simple)
2. **Must reference plan.md's test variable** (show how it supports the macro test)
3. **Hold constant**: ICP, messaging angle, offer, AI variables
4. **Vary only**: Delivery elements (subject format, PS line, body length, CTA phrasing, timing)
5. **Clear hypothesis**: State expected outcome and why
6. **Measurable**: Define primary metric (open rate / reply rate / click rate)

### Sequence Tests Output Format

When including a sequence test, add this section to strategy.md:

```markdown
## Sequence Tests

### Test Context
**Plan Test Variable**: [From plan.md - what macro test is running]
**Supporting Hypothesis**: [How this micro-test supports the macro test]

### Active Test

**Test Name**: [e.g., PS Line Inclusion Test]
**Variable**: [What's being tested]
- **Variant A (Control)**: [Default approach - describe]
- **Variant B (Test)**: [Alternative approach - describe]
- **Hypothesis**: [Why we think B might outperform A]
- **Primary Metric**: [Open rate / Reply rate / Click rate]
- **Affected Emails**: [Which emails have variants - e.g., "Email 1 only", "All emails", "Emails 2-3"]

**Implementation for email-copywriting:**
[Clear instructions on how to create variants in emails.md]
```

### Example: PS Line Inclusion Test

```markdown
## Sequence Tests

### Test Context
**Plan Test Variable**: Messaging Angle (guarantee vs ROI)
**Supporting Hypothesis**: The guarantee angle may perform differently with/without personal PS lines - testing whether personalization adds or detracts from the focused offer message.

### Active Test

**Test Name**: PS Line Inclusion Test
**Variable**: PS Line
- **Variant A (Control)**: Include AI-personalized PS line after signature
- **Variant B (Test)**: No PS line - end email at CTA
- **Hypothesis**: The guarantee message is already strong; PS line may dilute focus or add unnecessary length
- **Primary Metric**: Reply rate
- **Affected Emails**: Email 1 and Email 4 (the emails that currently use {{PS Line}})

**Implementation for email-copywriting:**
- Email 1: Write two versions - one with {{PS Line}} placeholder, one without
- Email 4: Write two versions - one with {{PS Line Final}} placeholder, one without
- Emails 2-3: No variants needed (they don't have PS lines)
```

### Alignment with Campaign Planning

Before defining a sequence test, verify it SUPPORTS (not conflicts with) the macro test:

| Plan Tests | Compatible Sequence Tests | Why Compatible |
|------------|---------------------------|----------------|
| Messaging Angle | Subject format, PS line, body length | Same audience, same offer, different delivery |
| ICP | None recommended | Keep execution identical to isolate ICP |
| Lead Magnet | CTA phrasing, proof placement | Same audience, refines offer delivery |

**Rule**: If plan.md is testing ICP, skip sequence tests entirely to get clean ICP comparison.
