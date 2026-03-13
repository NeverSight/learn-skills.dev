---
name: Meeting Digest Truth Extractor
description: |
  Extract decisions, commitments, risks, stakeholders, and MEDDICC updates from meeting transcripts.
  Use when a user asks "summarize my meeting", "what was decided in the call", "extract action items
  from the meeting", or needs a structured digest of what happened. Enforces truth hierarchy
  (CRM > transcript > notes) and returns structured, actionable output.
metadata:
  author: sixty-ai
  version: "2"
  category: sales-ai
  skill_type: atomic
  is_active: true
  command_centre:
    enabled: true
    label: "/summarize"
    description: "Summarize meeting or activity history"
    icon: "file-edit"
  context_profile: full
  agent_affinity:
    - meetings
  triggers:
    - pattern: "summarize my meeting"
      intent: "meeting_summary"
      confidence: 0.85
      examples:
        - "summarize the meeting"
        - "what happened in the meeting"
        - "meeting summary"
    - pattern: "what was decided in the call"
      intent: "meeting_decisions"
      confidence: 0.85
      examples:
        - "what decisions were made"
        - "meeting decisions and commitments"
        - "key takeaways from the call"
    - pattern: "extract action items from the meeting"
      intent: "meeting_actions"
      confidence: 0.80
      examples:
        - "action items from the meeting"
        - "meeting next steps"
        - "what did we commit to"
    - pattern: "meeting digest"
      intent: "meeting_digest"
      confidence: 0.85
      examples:
        - "create a meeting digest"
        - "digest from my last call"
        - "post-meeting digest"
  keywords:
    - "meeting"
    - "digest"
    - "summary"
    - "decisions"
    - "commitments"
    - "action items"
    - "transcript"
    - "call"
    - "MEDDICC"
    - "next steps"
  required_context:
    - meeting_id
    - transcript_id
    - company_name
  inputs:
    - name: meeting_id
      type: string
      description: "The meeting identifier to extract a digest from"
      required: true
    - name: contact_id
      type: string
      description: "Primary contact associated with the meeting for CRM enrichment"
      required: false
    - name: include_transcript
      type: boolean
      description: "Whether to fetch and analyze the full transcript"
      required: false
      default: true
  outputs:
    - name: decisions
      type: array
      description: "Decisions made during the meeting with decision maker, confidence, and source"
    - name: commitments
      type: array
      description: "Commitments made with owner, deadline, status, and missing info"
    - name: meddicc_deltas
      type: object
      description: "Changes to MEDDICC fields (metrics, economic buyer, criteria, process, pain, champion, competition)"
    - name: risks
      type: array
      description: "Identified risks with severity and suggested mitigations"
    - name: stakeholders
      type: array
      description: "Stakeholders mentioned with role, influence level, and sentiment"
    - name: unknowns
      type: array
      description: "Questions and unknowns that need follow-up"
    - name: next_steps
      type: array
      description: "Recommended next steps with owners and deadlines"
  requires_capabilities:
    - meetings
    - crm
  priority: critical
  tags:
    - sales-ai
    - meetings
    - transcript
    - meddicc
    - post-meeting
---

## Available Context & Tools
@_platform-references/org-variables.md
@_platform-references/capabilities.md

# Meeting Digest Truth Extractor

## Why Truth Extraction Matters

Meetings generate enormous amounts of information. Almost none of it gets captured accurately.

- **63% of verbal commitments made in meetings are never documented** (Harvard Business Review, 2022). They exist only in someone's memory -- and memory degrades within hours.
- **Within 24 hours, people forget 50-80% of meeting content** (Ebbinghaus forgetting curve applied to meeting recall, SalesHacker study). By the end of the week, key details are gone.
- **The average B2B deal involves 6.8 stakeholders** (Gartner). After a multi-person meeting, each participant walks away with a different understanding of what was agreed.
- **Reps update CRM accurately after only 29% of meetings** (Salesforce State of Sales). The other 71% of the time, deal records are incomplete or stale.
- **Forecast accuracy drops 34% when meeting outcomes are not captured within 24 hours** (Clari analysis). Stale meeting data propagates into pipeline reviews, QBRs, and board reports.

This skill exists to solve the "meeting black hole" -- the gap between what was said and what gets captured. It extracts structured, verified truth from meeting transcripts and cross-references it against CRM data to produce an actionable, trustworthy digest.

## The Truth Hierarchy (Deep Explanation)

Not all information sources are equal. When sources conflict -- and they frequently do -- the Truth Hierarchy determines which source wins.

### Tier 1: CRM Data (Highest Priority)

**What it is:** Structured data in deal records, contact records, activity logs, and custom fields. This is the system of record.

**Why it's the highest tier:** CRM data represents the agreed-upon state of the deal. If CRM says the deal is in "Negotiation" stage, that is the official status even if someone mentioned "we're still evaluating" in the transcript. The CRM may have been updated by the rep after the meeting, or it may reflect information from other touchpoints that the transcript doesn't capture.

**When to override CRM:** Only when the transcript contains an explicit, unambiguous statement that directly contradicts CRM data AND the statement is more recent. Example: CRM says close date is March 31, but the VP said "We're pushing this to Q3." In this case, flag the contradiction and recommend a CRM update -- but do not silently override the CRM data. Surface it as a delta.

**CRM data to pull:**
- Deal stage, amount, close date
- MEDDICC field values (current state)
- Contact roles and relationships
- Activity history (last 30 days)
- Open tasks and commitments
- Relationship health score

### Tier 2: Transcript Data (Medium Priority)

**What it is:** Verbatim or near-verbatim records of what was said in the meeting. This includes Fathom transcripts, 60 Notetaker recordings, and any other automated transcript.

**Why it's the second tier:** Transcripts capture what people said, but not necessarily what they meant. People hedge, brainstorm aloud, play devil's advocate, and say things they later retract. A transcript is a record of the conversation, not a record of decisions.

**How to parse transcripts for truth:**
1. **Explicit statements** (high confidence): "We've decided to go with your proposal." "Our budget is $150K." "We need this live by April 1."
2. **Conditional statements** (medium confidence): "If pricing works out, we'd be interested." "Assuming legal approves, we could move forward next month."
3. **Exploratory statements** (low confidence): "We might consider..." "I wonder if..." "What would it look like if..."
4. **Retracted statements** (ignore): "Actually, scratch that." "Let me rethink that." "That's not what I meant."

**Key parsing rules:**
- Look for performative verbs: "decide," "agree," "commit," "approve," "confirm," "promise," "guarantee"
- Look for hedge words that reduce confidence: "might," "could," "possibly," "I think," "maybe," "probably," "in theory"
- Look for authority markers: "I can approve," "that's my call," "I'll sign off" (these indicate decision-maker authority)
- Look for deflection markers: "I'd need to check with," "let me run it by," "that's above my pay grade" (these indicate non-decision-makers)

### Tier 3: User Notes (Lowest Priority)

**What it is:** Manual notes taken by the rep during or after the meeting. Free-form text, often paraphrased and subjective.

**Why it's the lowest tier:** Notes are filtered through the rep's perspective, biases, and selective memory. They often contain interpretation rather than fact. "They seemed really interested" is a rep's opinion, not a data point.

**When notes are valuable:** When neither CRM data nor transcript is available (e.g., an in-person meeting with no recording). In that case, notes are the best available source -- but confidence should be marked lower.

### Conflict Resolution Matrix

| Conflict | Resolution | Action |
|----------|-----------|--------|
| CRM says Stage X, transcript mentions Stage Y | Trust CRM unless transcript is explicitly more recent | Flag delta, recommend CRM review |
| Transcript says "we agreed to X," notes say "they were unsure" | Trust transcript (verbatim record beats paraphrase) | Use transcript version, note discrepancy |
| Two speakers in transcript disagree | Record both positions | Flag as unresolved, note which speaker has authority |
| CRM data is older than 30 days | Flag as potentially stale | Recommend CRM update based on transcript findings |
| No CRM data exists for a field | Use transcript as primary source | Mark confidence based on transcript parsing rules |

## Decision Extraction Methodology

See `references/extraction-patterns.md` for the full pattern library including commitment language patterns (strong vs. weak), risk indicator phrases, decision language taxonomy, stall/delay indicators, buying signal phrases, and authority indicators.

Decisions are the highest-value output of any meeting. A decision changes the state of the deal. Everything else is conversation.

### What Counts as a Decision

A decision is a statement that:
1. **Changes the state** of an agreement, plan, or commitment
2. **Has an identifiable decision-maker** (someone with authority)
3. **Is stated with commitment language** (not exploration or brainstorming)

### Decision Detection Patterns

**Strong decision signals (high confidence):**
- "We've decided to..." / "Our decision is..."
- "I'm approving..." / "Consider it approved"
- "Let's go with [option]" / "We'll take [option]"
- "Agreed" / "Deal" / "Done"
- "I'll sign off on that" / "You have my approval"
- "We're moving forward with..."

**Moderate decision signals (medium confidence):**
- "I think we should go with..." (single person, may need group validation)
- "Sounds like we're aligned on..." (implied consensus, not explicit)
- "Unless anyone objects, we'll..." (consent-based, watch for objections)
- "Let me confirm -- we're doing [X]?" followed by affirmative

**Not decisions (do not extract):**
- "We should think about..." (no commitment)
- "It would be nice to..." (aspiration, not decision)
- "In an ideal world..." (hypothetical)
- "What if we..." (exploration)
- "I'll need to check with [person]" (deferred decision)

### Decision Object Structure

For each extracted decision:
```
{
  decision: "Agreed to proceed with Phase 1 pilot for 50 users",
  decision_maker: "Sarah Chen, VP of Operations",
  authority_level: "final" | "recommender" | "influencer",
  confidence: "high" | "medium" | "low",
  source: "transcript",
  source_quote: "Let's go ahead with the 50-user pilot. I can approve that.",
  timestamp: "00:34:12",
  conditions: ["Pending security review completion"],
  impact_on_deal: "Advances deal from Evaluation to Pilot stage"
}
```

## Commitment Capture Framework (RACI Model)

Commitments are promises to take action. Unlike decisions (which change state), commitments are forward-looking obligations. Every untracked commitment is a potential broken promise and a damaged relationship.

### The RACI Framework for Commitments

For each commitment captured, identify:

- **R**esponsible: Who is doing the work? (The person who said "I'll do X")
- **A**ccountable: Who is ultimately accountable? (The person whose reputation is on the line)
- **C**onsulted: Who needs to provide input? ("I'll need to check with Legal first")
- **I**nformed: Who needs to know the outcome? ("I'll loop in the team")

### Commitment Detection Patterns

**Explicit commitments (high confidence):**
- "I will send you [X] by [date]"
- "We'll have [deliverable] ready by [deadline]"
- "I commit to [action]"
- "You'll have that by end of week"
- "Consider it done"
- "I'll make sure [X] happens"

**Implied commitments (medium confidence -- flag for confirmation):**
- "I should be able to get that to you..." (intention, not commitment)
- "Let me try to..." (effort, not guarantee)
- "I'll see what I can do" (vague, no deliverable or deadline)
- "We're working on that" (ongoing, no completion criteria)

**Missing information flags:**
Every commitment must have an owner and a deadline. If either is missing, flag it:
- "We'll send the proposal" -- WHO on your team? WHEN?
- "I'll review it" -- By WHEN?
- "Someone from our team will reach out" -- WHO specifically?

### Commitment Object Structure

```
{
  commitment: "Send revised pricing proposal with volume discount options",
  owner: { name: "Alex Rivera", email: "alex@example.com", side: "seller" },
  accountable: { name: "Alex Rivera" },
  consulted: ["Finance team for discount approval"],
  informed: ["Sarah Chen (prospect) will receive the deliverable"],
  deadline: "Friday, Feb 14",
  deadline_source: "explicit" | "inferred" | "missing",
  status: "new",
  confidence: "high",
  source_quote: "I'll have the revised pricing with volume options to you by Friday",
  missing_info: [],
  suggested_task: {
    title: "Send revised pricing to Sarah Chen",
    due_date: "2026-02-14",
    priority: "high",
    description: "Include volume discount options as discussed in the meeting"
  }
}
```

## MEDDICC Delta Extraction Guide

Consult `references/meddicc-guide.md` for the complete MEDDICC extraction guide including what to listen for in each field, example phrases indicating strength vs. gaps, questions that uncover each element, and CRM field update mappings.

MEDDICC is the gold standard qualification framework for enterprise sales. This skill does not fill MEDDICC from scratch -- it extracts CHANGES (deltas) from the meeting that update existing MEDDICC fields.

### What to Look for in Each Field

#### M -- Metrics
**Listen for:** Numbers, KPIs, success criteria, ROI expectations, benchmarks.
- "We need to reduce churn by 15%"
- "Our target is $2M in pipeline by Q3"
- "If we can cut onboarding time from 6 weeks to 2, that's a win"

**Delta types:**
- New metric introduced (previously unknown)
- Existing metric updated (number changed, timeline shifted)
- Metric confirmed (same as CRM, but now explicitly stated)
- Metric retracted ("Actually, the churn number isn't the priority anymore")

#### E -- Economic Buyer
**Listen for:** Budget authority, approval power, sign-off references.
- "I can approve up to $100K without board approval"
- "This needs to go through our CFO, Janet Walsh"
- "Procurement handles anything over $50K"

**Delta types:**
- Economic buyer identified (name + role)
- Economic buyer changed (different person than CRM says)
- Budget range revealed or updated
- Approval process clarified

#### D -- Decision Criteria
**Listen for:** Requirements, must-haves, evaluation criteria, vendor selection factors.
- "Security certification is non-negotiable"
- "We need native Salesforce integration"
- "Total cost of ownership over 3 years is the deciding factor"

**Delta types:**
- New criterion added
- Criterion weight changed ("Security is now #1, not integration")
- Criterion met ("Your SOC2 cert checks that box")
- Criterion unmet ("We need HIPAA and you don't have that yet")

#### D -- Decision Process
**Listen for:** Timeline, approval steps, stakeholders involved, evaluation stages.
- "We'll make a decision by end of Q1"
- "Next step is a technical review with our engineering team"
- "Board meets monthly -- we'd need to present in the March meeting"

**Delta types:**
- Timeline updated (accelerated or delayed)
- New step introduced ("We also need a security review")
- Step completed ("The technical eval went well")
- Process changed ("We're fast-tracking this")

#### I -- Identify Pain
**Listen for:** Problems, frustrations, inefficiencies, complaints, workarounds.
- "Our team wastes 10 hours a week on manual data entry"
- "We lost a major customer because our response time was too slow"
- "The current tool crashes every time we run a report over 10K rows"

**Delta types:**
- New pain point identified
- Existing pain quantified (added numbers/impact)
- Pain confirmed as top priority
- Pain resolved or deprioritized

#### C -- Champion
**Listen for:** Internal advocacy, willingness to sell internally, personal stake.
- "I'll bring this to the leadership team"
- "I've already mentioned your solution to our CTO"
- "This would make my team's life so much easier -- I want this to work"

**Delta types:**
- Champion identified or confirmed
- Champion strength changed (stronger or weaker)
- Champion lost access or influence
- New potential champion emerged

#### C -- Competition
**Listen for:** Alternative vendors, internal solutions, DIY approaches, status quo.
- "We're also looking at [Competitor]"
- "Our engineering team thinks they can build this in-house"
- "Honestly, we might just stick with what we have"

**Delta types:**
- New competitor entered evaluation
- Competitor eliminated
- Competitor preference shifted
- Build-vs-buy consideration raised
- Status quo strengthened as alternative

### MEDDICC Delta Object Structure

```
{
  metrics: {
    changed: true,
    previous: "Reduce churn by 10%",
    current: "Reduce churn by 15% within 6 months",
    source: "transcript",
    source_quote: "Actually, our new target is 15% churn reduction...",
    confidence: "high"
  },
  economic_buyer: { changed: false },
  decision_criteria: {
    changed: true,
    added: ["HIPAA compliance requirement"],
    removed: [],
    updated: [],
    source: "transcript",
    confidence: "medium"
  },
  // ... same structure for each field
}
```

## Risk Identification Patterns in Meetings

Risks are not always stated explicitly. Often they must be inferred from conversational patterns, tone, and language. Here are the patterns to detect.

### Verbal Risk Signals

**Hedging language (medium risk):**
- "I think this could work..." (uncertainty)
- "In theory, yes..." (doubt about practice)
- "I hope we can..." (low confidence)
- "We'll try to..." (not committing)

**Deflection language (high risk):**
- "That's a good question, let me get back to you" (avoidance)
- "I'd need to check with [unnamed person]" (hidden stakeholder)
- "That's above my pay grade" (no authority)
- "I'm not the right person to answer that" (misaligned meeting)

**Competing priority language (medium risk):**
- "We have a lot on our plate right now" (bandwidth constraint)
- "There are other priorities we need to address first" (not #1)
- "Let's revisit this next quarter" (delay tactic)
- "Our board is focused on [other thing]" (misaligned executive priorities)

**Negative sentiment language (high risk):**
- "I'm not sure this is the right fit" (evaluation concern)
- "That's more than we expected to spend" (budget objection)
- "Our team had some concerns about..." (internal resistance)
- "We've had bad experiences with similar tools" (historical baggage)

**Champion erosion language (critical risk):**
- "I'm starting to wonder if..." (champion doubt)
- "My team isn't fully on board" (internal resistance)
- "I've been getting pushback from..." (political opposition)
- "I might be moving to a different role" (champion departure)

### Structural Risk Patterns

These are not about what was said, but about the structure and dynamics of the meeting:

- **New unknown attendee appears**: Someone joined who wasn't expected. Why? Possible evaluator, possible blocker, possible champion.
- **Key stakeholder drops off**: The economic buyer was supposed to attend but didn't. Red flag for deal priority.
- **Meeting cut short**: The prospect ended the meeting early. Either they have what they need (positive) or they've lost interest (negative).
- **Prospect not asking questions**: In a demo, silence is rarely golden. It usually means disengagement.
- **Prospect asking only technical questions**: May indicate they're focused on finding reasons NOT to buy (technical disqualification).
- **Multiple people talking over each other**: Internal disagreement on the prospect side.
- **Long pauses after key questions**: Usually indicates the answer is complicated or uncomfortable.

### Risk Object Structure

```
{
  risk: "Champion mentioned internal pushback from engineering team",
  severity: "high",
  category: "champion_erosion" | "competitive" | "timing" | "budget" | "stakeholder" | "scope" | "technical",
  evidence: "Direct quote: 'I've been getting some pushback from the engineering leads'",
  source: "transcript",
  timestamp: "00:22:45",
  mitigation: "Schedule a technical deep-dive with the engineering leads. Prepare integration architecture doc and security whitepaper. Ask champion to facilitate introduction.",
  urgency: "Act within 48 hours -- before the next internal review"
}
```

## Stakeholder Mapping from Meeting Dynamics

Every meeting reveals information about the buying committee, even when it is not explicitly discussed. Extract stakeholder intelligence from both explicit mentions and conversational dynamics.

### Stakeholder Detection

**From direct mentions:**
- "My boss, [Name], will need to approve this" -- Maps to economic buyer or authority
- "I'll need to loop in our security team" -- Maps to technical evaluator
- "[Name] in procurement handles vendor contracts" -- Maps to gatekeeper

**From conversational dynamics:**
- Who speaks the most? (Often the champion or the meeting owner)
- Who asks the toughest questions? (Often the skeptic or technical evaluator)
- Who defers to whom? (Reveals hierarchy and authority)
- Who was quiet but present? (May be observing/evaluating silently)
- Who was referenced but not present? (Hidden stakeholders with influence)

### Stakeholder Object Structure

```
{
  name: "Janet Walsh",
  title: "CFO",
  company: "Prospect Corp",
  role_in_deal: "economic_buyer" | "champion" | "influencer" | "gatekeeper" | "evaluator" | "end_user" | "unknown",
  present_in_meeting: true | false,
  influence_level: "high" | "medium" | "low",
  sentiment: "positive" | "neutral" | "negative" | "unknown",
  evidence: "Mentioned as final budget approver. Quote: 'Janet signs off on anything over $75K'",
  engagement_level: "active" | "passive" | "disengaged",
  concerns: ["Budget timing -- fiscal year ends in June"],
  recommended_action: "Request introduction to Janet. Prepare CFO-level business case."
}
```

## Unknown/Gap Identification Methodology

Unknowns are as valuable as knowns. Every gap identified is a question to answer in the next interaction.

### Categories of Unknowns

1. **Unanswered questions**: Questions asked during the meeting that received vague or deferred answers
2. **Unasked questions**: Questions that SHOULD have been asked but weren't (based on deal stage and MEDDICC gaps)
3. **Contradictions**: Statements that conflict with each other or with CRM data
4. **Assumptions**: Things the rep or prospect assumed but never validated
5. **Missing stakeholders**: Decision-makers or influencers who haven't been engaged
6. **Timeline gaps**: Unclear timelines, undefined milestones, vague deadlines

### Unknown Object Structure

```
{
  unknown: "Budget approval process and timeline not discussed",
  category: "unanswered" | "unasked" | "contradiction" | "assumption" | "missing_stakeholder" | "timeline_gap",
  importance: "critical" | "important" | "minor",
  meddicc_field: "decision_process",
  suggested_question: "What does the budget approval process look like? Who needs to sign off, and what's the typical timeline?",
  when_to_ask: "Next meeting or follow-up email"
}
```

## Data Gathering (via execute_action)

1. **Fetch transcript**: Use meeting/transcript capability to get full transcript text
2. **Fetch CRM deal data**: `execute_action("get_deal", { id: deal_id })` -- stage, amount, MEDDICC, custom fields
3. **Fetch contact details**: `execute_action("get_contact", { id: contact_id })` -- name, title, company, relationship history
4. **Fetch company info**: `execute_action("get_company_status", { company_name })` -- overview, health score
5. **Fetch previous meeting digests** (if available): Compare against previous commitments to detect unfulfilled promises

## Output Contract

Return a SkillResult with:

- `data.executive_summary`: 2-3 sentence summary of the meeting outcome in plain language. Written for a VP who has 10 seconds to scan.
- `data.decisions`: Array of decision objects (see Decision Object Structure above)
- `data.commitments`: Array of commitment objects (see Commitment Object Structure above)
  - Split into `seller_commitments` (our team owes) and `buyer_commitments` (their team owes)
- `data.meddicc_deltas`: Object with MEDDICC field changes (see MEDDICC Delta Object Structure above)
  - Only include fields that changed. If a field didn't change, set `changed: false`.
- `data.risks`: Array of risk objects (see Risk Object Structure above)
- `data.stakeholders`: Array of stakeholder objects (see Stakeholder Object Structure above)
  - Include both present and mentioned-but-absent stakeholders
- `data.unknowns`: Array of unknown objects (see Unknown Object Structure above)
- `data.next_steps`: Array of recommended next steps:
  - `action`: What needs to happen
  - `owner`: Who should do it (name, side: "seller" | "buyer")
  - `deadline`: When (explicit from meeting or suggested)
  - `priority`: "critical" | "high" | "medium"
  - `depends_on`: Any prerequisite actions
- `data.key_quotes`: Array of the 3-5 most important verbatim quotes from the transcript, with speaker, timestamp, and context for why they matter
- `data.sentiment_summary`: Overall meeting sentiment (positive / mixed / negative) with evidence
- `references`: Links to transcript, CRM records, related meetings

## Quality Standards for Each Extracted Item

### Decisions
- Must have a decision-maker identified (by name, not "they")
- Must have a confidence level justified by the detection pattern used
- Must include the source quote (exact words, not paraphrase)
- Must note conditions or caveats ("pending security review")

### Commitments
- Must have an owner (by name, not "the team" or "we")
- Must have a deadline (or be explicitly flagged as "deadline missing")
- Must distinguish between seller and buyer commitments
- Must flag vague commitments that need clarification

### MEDDICC Deltas
- Must compare against CRM baseline (not invented baseline)
- Must include source quote for each change
- Must distinguish between confirmed (validates CRM) and changed (contradicts CRM)
- Must only include fields that actually changed

### Risks
- Must include specific evidence (quote, behavior, or pattern)
- Must include actionable mitigation (not just "monitor the situation")
- Must be categorized by type (competitive, budget, timing, etc.)

### Stakeholders
- Must distinguish between "present in meeting" and "mentioned but absent"
- Must note decision authority based on evidence, not assumption
- Must flag any stakeholder sentiment changes from previous meetings

## Quality Checklist

Before returning the digest, verify:

- [ ] **Truth hierarchy was applied.** CRM data was used as the baseline. Transcript data was cross-referenced. No item relies solely on inference.
- [ ] **Every decision has a decision-maker.** No anonymous decisions like "it was decided that..."
- [ ] **Every commitment has an owner and deadline.** Missing info is explicitly flagged, not silently omitted.
- [ ] **MEDDICC deltas are changes, not full MEDDICC.** Only include fields that were affected by this meeting.
- [ ] **Risks have evidence.** No speculative risks without specific quotes or behavioral evidence.
- [ ] **Unknowns include suggested questions.** Each gap has a clear path to resolution.
- [ ] **No hallucinated quotes.** Every quoted statement actually appears in the transcript.
- [ ] **Executive summary is scannable.** 2-3 sentences max. A VP can read it in 10 seconds and know the outcome.
- [ ] **Commitments are split by side.** Seller commitments and buyer commitments are clearly separated.
- [ ] **Sentiment assessment has evidence.** "Positive meeting" is backed by specific quotes or behaviors, not vibes.

## Error Handling

### Transcript not available
If the transcript is missing or access is denied, fall back to CRM activity data and user notes. Mark all extracted items with confidence "low" and source "inferred_from_notes". Note: "Full transcript not available. Digest is based on CRM data and meeting notes only. Accuracy is reduced."

### Transcript is very short (under 5 minutes)
Short meetings often indicate a cancelled meeting, a quick check-in, or a problem. Generate a minimal digest and flag: "Meeting transcript is very short ([X] minutes). This may have been a brief check-in or the recording may be incomplete."

### Transcript is very long (over 60 minutes)
For long transcripts, focus extraction on:
1. The first 5 minutes (agenda setting and context)
2. The last 10 minutes (conclusions and next steps)
3. Any segments with decision or commitment language
4. Segments with risk indicators

### No CRM deal found
Generate the digest without MEDDICC deltas or deal context. Flag: "No CRM deal associated with this meeting. MEDDICC analysis skipped. Consider creating a deal record if this is a sales opportunity."

### Multiple speakers with same first name
Use full names, titles, and company affiliations to disambiguate. If still ambiguous, mark the speaker as "[First Name] (disambiguation needed)" and flag it.

### Transcript quality is poor (ASR errors)
When the transcript has obvious speech-to-text errors, note: "Transcript quality is below normal. Some quotes may contain ASR errors. Verify critical items before acting." Focus on extracting meaning from context rather than relying on exact words.

### Meeting was primarily internal (no prospect)
Detect if all participants are internal team members. If so, adjust extraction to focus on internal decisions and action items rather than MEDDICC and deal-oriented analysis. Flag: "This appears to be an internal meeting. Digest focuses on internal decisions and action items."

### Contradictory statements in the same meeting
When the same person says contradictory things (e.g., "Budget isn't an issue" early on, then "We need to be cost-conscious" later), flag both statements with timestamps and note: "Contradictory statements detected. The later statement may reflect the true position after deeper discussion."

## Guidelines

- De-duplicate contradictions using the truth hierarchy. Never present both sides of a contradiction as equal.
- Use Organization Context to identify ${company_name} products, competitors, and terminology when interpreting transcript content and mapping MEDDICC fields.
- Flag missing information explicitly. A commitment without an owner is not a commitment -- it is a risk.
- Extract explicit quotes for the "key quotes" section. These are the 3-5 statements a manager would want to see.
- Be conservative: when uncertain about whether something is a decision or exploration, default to exploration. Over-reporting decisions erodes trust.
- Always generate suggested tasks for commitments. Make it easy for the rep to act immediately.
- Prioritize recency: if the same topic was discussed multiple times in the meeting, use the final position as the truth.
- Never include raw transcript chunks in the output. Always extract, structure, and attribute.
- Preserve the prospect's exact language in key quotes -- do not paraphrase. The words they chose reveal sentiment and intent.
