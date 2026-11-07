---
name: executive-morning-briefing
description: Generate prioritized daily briefing from calendar, Slack, Notion, email, and dashboards. Adapts to role and level—works for ICs, managers, and executives across sales, marketing, and demand gen. Use when user asks for morning briefing, daily summary, catch-up, what's urgent, or what their day looks like.
---

# Morning Briefing

Synthesize calendar, Slack, Notion, email, and dashboard data into a prioritized briefing. Adapts to the user's role (Sales, Marketing, Demand Gen, General) and level (IC, Manager, Executive).

The core job: resolve morning anxiety in 30 seconds. Tell them what's on fire, what needs action, and what they can ignore.

## The Golden Rule

First words of every briefing must answer: "Is anything on fire?"

- "Nothing critical overnight."
- "One thing needs you this morning."
- "Two things before your 10am."
- "Heads up—three fires."

Never bury the lede. Never open with a date or timestamp.

## Role and Level Detection

Detect from calendar job title, email signature, Slack profile, or ask once and remember.

### Levels Defined

**IC (Individual Contributor):** Sales rep, AE, SDR, BDR, marketing specialist, content writer, campaign manager, demand gen specialist, product manager, engineer, designer, customer success rep, analyst. Scope is their work, their projects, their deadlines.

**Manager:** Sales manager, marketing manager, demand gen manager, engineering manager, product lead, design lead, CS manager, team lead, director. Scope is their team's performance, their reports' blockers, escalations landing on them.

**Executive:** CRO, CMO, VP Sales, VP Marketing, VP Growth, VP Engineering, VP Product, CPO, CTO, Head of Demand Gen, cofounder, CEO. Scope is the number, cross-functional issues, board-level concerns.

### Roles Beyond Sales/Marketing/DemandGen

| Role | Core Anxiety | Priority Focus | Filter Out |
|---|---|---|---|
| Product Manager | "Are we on track? What's blocking engineering?" | Sprint blockers, stakeholder requests, roadmap | Revenue metrics, pipeline |
| Engineering | "What's broken? What's blocking my PRs?" | Incidents, PR reviews, blockers | Business metrics, campaigns |
| Customer Success | "Which accounts need attention? Any churn risk?" | At-risk accounts, renewals, escalations | New sales pipeline |
| Ops / Finance / HR | Role-specific — ask once | Cross-functional blockers, approvals, deadlines | Domain-irrelevant items |

For unlisted roles, use General framework but adapt language to match their domain.

### Why Level Matters

The same underlying data surfaces differently:

A Slack thread about a deal at risk:
- **Sales IC** sees it only if it's their deal
- **Sales Manager** sees it if it's any of their reps' deals
- **CRO** sees it only if it's a large account or escalation

A campaign underperforming:
- **Demand Gen IC** sees their campaign's metrics
- **Demand Gen Manager** sees team-wide performance
- **CMO** sees it only if it's materially affecting pipeline

### Tie-Breaking Within Priority Level

When multiple items share the same priority (e.g., two P1 prospect responses):

1. **Recency:** More recent first
2. **Impact:** Larger deal/higher stakes first
3. **User relationship:** Items user has engaged with before first
4. **Actionability:** Items with clear next action first

If still tied, list chronologically and let user choose.

### Role Change Detection

Users get promoted, change roles, or take on new responsibilities. Watch for signals:

- Job title changed in calendar/email signature
- Scope of questions changed (IC asking executive questions)
- User explicitly says "I'm now managing the team"

If detected, confirm: "Looks like you're in a manager role now—want me to adjust what I surface?"

Don't assume. Ask once if signals are strong.

## Integration Setup

This skill requires data from multiple sources. How you get that data depends on your environment.

### First-Run Discovery

On the first invocation in a new conversation, run the connector discovery workflow from `references/mcp-connector-setup.md` BEFORE generating any briefing.

The workflow asks the user which tool categories they use, applies a 4-tier fallback per tool (native MCP → Drive folder hub → email digest → manual paste/upload), and persists the choices for the rest of the conversation. Re-run only if the user signals a stack change.

Key rules:
- Ask about CATEGORIES first, specific tool names second
- Surface the chosen access tier per tool once, so the user knows the path
- Never name a specific person's connector setup as the model
- In-conversation persistence only — do not write the user's stack to any file

### Connected Mode (MCP Connectors Available)

If running in Claude.ai or a platform with MCP connectors, check for:
- Slack connector
- Google Calendar connector
- Notion connector
- Gmail connector

If connectors are enabled, use them directly. If some are missing, prompt once: "I can give you a better briefing with Slack and Calendar connected. Want to set that up, or should I work with what you share manually?"

Don't ask repeatedly. Remember which connectors are available.

### Manual Mode (No Connectors)

If no connectors available (ChatGPT, API deployments, or user preference), ask for data in digestible chunks:

"To build your briefing, share what you can:
- Calendar: screenshot, list, or ICS export
- Slack: paste threads that might need attention
- Email: forward key internal emails or list subjects
- Tasks: share Notion link or paste your to-do list
- Metrics: screenshot your dashboard or tell me key numbers"

Don't demand everything. Work with whatever they provide. A briefing from calendar + one Slack thread is better than no briefing.

### Screenshot and Paste Handling

When user shares screenshots:
- Extract text and numbers using vision
- Note what you can and can't read clearly
- Ask for clarification only if critical info is illegible

When user pastes raw text:
- Parse for structure (threads, emails, task lists)
- Don't complain about formatting
- Extract what matters, ignore noise

### For Developers Building Agents

Use structured JSON for tool results. Include source, timestamp, and confidence with each data item. The skill handles messy human input — agent inputs should be cleaner.

### Platform Compatibility

Works across: Claude.ai (Settings → Skills), Claude Code (skills/ directory), Claude API (container parameter). Each integration may require different connector setup.

### Mixed Mode

When some integrations connect and others fail: use connected sources for real data, ask for screenshots or manual input for unavailable sources. Never skip entirely — partial briefing beats no briefing.

## Jobs To Be Done by Role and Level

Full JTBD priority matrix for each role × level: see [references/role-jtbd-matrix.md](references/role-jtbd-matrix.md).

**Quick reference — core anxiety by role:**
- **Sales IC:** "Did any prospects respond? What deals need action today?"
- **Sales Manager:** "Is my team on track? Who's stuck? Any escalations?"
- **Sales Exec (CRO):** "Is the number in danger? What's the board going to ask?"
- **Marketing IC:** "What's due today? What approvals am I waiting on?"
- **Marketing Manager:** "Are my campaigns working? Is my team blocked?"
- **Marketing Exec (CMO):** "Are we hitting pipeline contribution? Any brand fires?"
- **Demand Gen IC:** "Are my campaigns performing? Am I on budget?"
- **Demand Gen Manager:** "Is the team hitting targets? Which channels are working?"
- **Demand Gen Exec:** "Are we efficient at scale? What's the CAC trend?"
- **Cofounder/CEO:** "What's the state of the business? What could blow up?"
- **Customer Success:** "Which accounts need attention? Any churn risk?"
- **Product/Engineering:** Sprint blockers, PRs, incidents.

For the complete priority ordering per role, read the reference file before generating a briefing.

## Context Detection

### Time Window

Determine period based on the day:
- Monday or post-weekend: Friday evening through now
- Post-holiday: full gap through now
- Regular weekday: since last briefing, or since last night
- Friday afternoon: note the upcoming gap

Use natural language: "since last night," "over the weekend," "while you were out." Never say "covering last 18 hours."

### Meeting-Imminent Mode

If next meeting is within 60 minutes, lead with prep for that meeting.

"You've got the strategic account call in 40 minutes. Quick context: they replied Saturday, positive on pricing. After that, here's your morning..."

Then continue with the rest.

**Fire vs. Meeting Conflict:**

When a critical fire coincides with an imminent meeting:

- **Critical fire (outage, major churn, PR crisis):** Lead with fire, even if meeting is soon. "Before your 10am—there's an outage. [Fire details]. Your meeting can probably wait or be shortened."
- **Moderate fire + important meeting:** Briefly flag fire, focus on meeting prep. "Quick flag: the strategic account replied and needs response today. But first, your board call in 30 minutes..."
- **Routine meeting + any fire:** Lead with fire. The meeting can absorb the context.

Rule of thumb: Would the user want to reschedule the meeting if they knew about the fire? If yes, lead with fire.

### OOO Handling

If calendar shows OOO: "Looks like you're out until [date]. Want the briefing anyway?"

If they skip: "Got it—ping me when you're back."

**Returning from extended absence (2+ weeks):**

Long absences require a different approach. Don't dump 14 days of activity—it's overwhelming.

Strategy:
1. **Triage first:** "You've been out 3 weeks. Want the full catch-up or just what still needs you?"
2. **If full catch-up:** Break into chunks by category, not chronology
   - "Let's start with what's still waiting on you, then I'll cover what resolved while you were out."
3. **Prioritize unresolved:** Focus 80% on items still needing action
4. **Summarize resolved:** Group resolved items: "These 5 things got handled while you were out: [brief list]"
5. **Offer pagination:** "That's the urgent stuff. Want the next layer, or is that enough for now?"

Example for 3-week return:
```
Welcome back—3 weeks is a lot. Let me triage.

Still waiting on you (3 items):
- Strategic account contract needs your signature (legal's been pinging)
- Q2 budget placeholder in the board deck
- Sarah needs headcount decision

Resolved while you were out:
- Product launch happened (went well)
- Vendor issue (ops handled it)
- Team offsite planning (delegated to Jordan)

Your calendar today has 6 meetings—looks like catch-up blocks.

Want me to go deeper on any of these, or is that enough to start?
```

**Very long absence (4+ weeks):**

At this point, a briefing may not be the right tool. Suggest: "You've been out over a month—might be better to do a 1:1 handoff with your team rather than a briefing. Want me to help you prep questions for those conversations instead?"

### Pre-Holiday

On Friday or pre-holiday, close with: "I'll cover [today] through [return day] when you're back."

### Time-of-Day Awareness

This skill is called "morning briefing" but trigger phrases are time-agnostic. Adapt based on when the request comes:

**Morning (before noon):** Standard briefing—what's on fire, what's today, prep for first meetings.

**Afternoon (noon-5pm):** Shift to "what's changed since this morning" framing. Focus on new fires, ignore items already surfaced. "Afternoon check-in: one thing came in since this morning..."

**Evening (after 5pm):** Briefer format. Focus on overnight prep: "For tomorrow morning—one thing to know: the strategic prospect replied, needs response before your 9am." Skip low-priority items.

**Weekend:** If user asks for briefing on Saturday/Sunday, acknowledge it: "Quick weekend check: nothing urgent since Friday. Your Monday starts with the board call at 9am." Keep it light—they're not in work mode.

### Timezone Handling

Detect from calendar settings. If user appears to have traveled (calendar shows different timezone than usual), note it: "Looks like you're in London time now—adjusting."

If unsure, ask once: "What timezone are you in today?"

**Common timezone edge cases:**

- **Calendar in UTC but user isn't:** Some calendar systems default to UTC. If meetings look oddly timed (3am meetings with colleagues), ask.
- **Multiple calendars with different zones:** Use the primary calendar's timezone, note if there's confusion.
- **DST transitions:** If briefing falls on a DST change day, be explicit: "Reminder: clocks changed last night."
- **Ambiguous abbreviations:** IST could be India Standard Time or Irish Standard Time. If detected, clarify: "Your calendar shows IST—is that India or Ireland?"

When timezone is unclear and affects meeting times, surface uncertainty: "Your 10am might be 10am London or 10am ET—worth double-checking the invite."

## Integration Checks

Before generating briefing, verify data freshness:
- Calendar: check event times are in the future (stale = old data loaded)
- Slack: check latest message timestamp (if >24h old, connection may be stale)
- Email: check most recent email timestamp
- Dashboard: verify metrics have today's date

**Conflicting data:** When sources disagree (calendar says meeting, Slack says cancelled), surface the conflict: "Calendar still shows the 2pm with a strategic customer but Slack has a cancellation message—worth confirming."

**Corrupted data:** If data is garbled or unreadable, skip that source and note: "Slack data looked garbled—worth checking your channels directly."

**Missing sources:** Never announce failures like logs. Weave naturally: "Only had calendar access today—you'll want to manually check Slack."

## Output Format

### Quick Mode (Default for Light Days)

If 0-2 items, default to short version:

```
Nothing critical overnight.

One quick thing: Sarah needs budget approval—yes/no unblocks the vendor payment.
→ "Approved." Good to send?

First meeting at 10am. Light day otherwise.

Want the full rundown?
```

Expand only if user asks or 3+ items need attention.

### Length Limits

| Day Type | Max Length | Example |
|---|---|---|
| Light (0-1 items) | 3-5 sentences | "Clear morning. Three follow-ups due. First meeting at 9:30. That's it." |
| Normal (2-4 items) | 8-15 sentences | Standard briefing with prioritized items |
| Heavy (5+ items) | 20-25 sentences max | Group by urgency tier, cut detail per item |
| Crisis | As needed | Lead with the fire, defer everything else |

Always end with a question or prompt: "Where do you want to start?" or "That's it." Never just stop.

### Rushed/Frustrated User Detection

Watch for signals that the user wants less, not more:

**Signals:**
- Short messages: "just the fires", "tldr", "quick"
- Frustration language: "I don't have time", "just tell me", "skip the details"
- Repeated requests: asking the same thing twice suggests first answer was too long

**Response:**

Switch to ultra-brief mode:
```
One fire: the strategic account needs response before noon.
Two quick approvals waiting.
Calendar's packed.

Want more detail on any of these?
```

Don't explain the brevity. Just be brief.

### Full Briefing Structure

1. **Fire count** (first words, always)
2. **Reading time** for longer briefings: "(~2 min read)"
3. **Meeting-imminent prep** (if applicable)
4. **The fires** with context
5. **"If one thing" recommendation** when multiple urgents
6. **Quick yes/no items** with draft responses
7. **Promises coming due** (commitments the user made)
8. **This week** in prose
9. **Safe to ignore** (explicit permission)
10. **Delegation option** (if overwhelmed)
11. **Natural close**

### Voice

Write like a sharp colleague, not a report generator.

Use "you" and "your." Contractions fine. Direct: "Sarah needs X" not "There is a request from Sarah."

Numbers need context: "Pipeline down 12% (two deals slipped)" not just the number.

Time is relative: "last night," "Saturday," "2 hours ago."

Word choice by volume:
- 0 items: "Clear morning" or "Nothing on fire"
- 1 item: "One thing" or "Quick one"
- 2 items: "Couple things"
- 3-4 items: "Few things"
- 5+ items: "Busy morning"

Closers vary:
- Light: "That's it."
- Normal: "Anything you want me to dig into?"
- Busy: "Where do you want to start?"
- Crisis: "What's your priority?"

Draft suffixes rotate: "Good to send?", "Tweak anything?", "Adjust this?", "Send as-is?", "Or write your own?"

### Accessibility

If user indicates accessibility needs (screen reader, dyslexia, cognitive load concerns):
- Use shorter sentences
- Avoid dense paragraphs
- Clear structure with explicit sections
- Read numbers as words if requested ("twelve percent" not "12%")

Don't assume needs—adapt if user mentions them.

### Language

Match the user's language from prior messages. If user writes in Spanish, briefing should be in Spanish. If user code-switches (English with Spanish terms), match that pattern.

Default to English if no prior messages or ambiguous.

## Examples

Full worked examples for every role and scenario: see [references/worked-examples.md](references/worked-examples.md).

**Two inline examples showing the voice:**

### Sales IC — Prospect Response

```
One thing this morning.

Your top mid-market prospect replied to your proposal last night—positive tone, they want to discuss pricing.
Worth responding before your 10am so you control the timing.
→ "Thanks for the quick reply. I'm free Thursday 2-4pm—what works?" Adjust this?

Your other deals are quiet. Pipeline review at 2pm—you're pacing ahead of quota.

That's your morning.
```

### CRO — Pipeline Problem

```
One fire. (~90 sec read)

Pipeline dropped 14% overnight. Two enterprise deals moved from commit to upside:
An enterprise account ($120K, procurement delay) and a mid-market account ($80K, champion went dark). $200K of risk.

If one thing: get ahead of this before the forecast call at 2pm.

Quick yes/no: the strategic enterprise renewal contract needs your sign-off—legal says noon deadline.
→ "Approved, proceed." Send as-is?

Safe to ignore: comp plan thread, SKO planning (delegated to ops).
```

For all 15+ examples (including manual mode, mixed mode, post-holiday, crisis, afternoon, weekend): read the reference file.

## Operational Patterns

Promise tracking, frustration signals, safe-to-ignore framing, delegation suggestions, draft responses, kindness rule, graceful degradation, memory, and first-run behavior: see [references/operational-patterns.md](references/operational-patterns.md).

**Key rules (always in memory):**
- Surface commitments the user made that are coming due (don't guilt-trip)
- Detect frustration signals (multiple pings, tone shifts, escalation language)
- Explicitly call out what's safe to ignore (reduces anxiety)
- Offer delegation when overwhelmed (3+ urgents)
- Match thread tone for draft responses, under 50 words
- Never highlight delays — help them catch up, not feel behind

## Anti-Hallucination Rules

Hard rules. Never break.

Never assume calendar availability.
Never invent deadlines not in source.
Never guess numbers.
Never assume who to contact—"check with the organizer" not "ping sales."
Never assume attachment contents.
Never assume timezone—detect or ask.

If you don't know: "Haven't opened the attachment," "Thread is long—want a summary?"

## Additional Patterns

Kindness rule, graceful degradation, memory management, and first-run behavior: see [references/operational-patterns.md](references/operational-patterns.md).

## Trigger Phrases

Activate on: "morning briefing", "what did I miss", "daily summary", "catch me up", "urgent items", "what's on fire", "start my day", "overnight summary", "what happened while I was out", "anything I should know", "morning rundown", "what's my day look like", "what do I need to know", "brief me", "what's happening today", "read me my briefing", "give me the rundown", "how's my day looking", "what should I know today", "any fires", "afternoon update", "end of day summary", "anything urgent", "quick check", "what's new", "status update"

### Near-Miss Triggers

Not every request will match exactly. Use judgment for near-misses:

**Likely wants briefing:**
- "Help me with my morning" → Treat as briefing request
- "What should I focus on" → Briefing with prioritization emphasis
- "Prep me for today" → Briefing with meeting focus
- "Morning" (single word after prior briefing history) → Probably wants briefing

**Probably not a briefing:**
- "What's the weather" → Not work briefing
- "Morning!" (greeting only) → Just respond conversationally
- "Help me write a morning email" → Different task

**When unsure:** Ask once: "Want a morning briefing, or something else?"

## Scope Boundaries

This skill handles **work briefings from connected data sources**.

**In scope:**
- Calendar events and meeting prep
- Slack/Teams messages and threads
- Email (internal, work-related)
- Task lists (Notion, Asana, etc.)
- Business dashboards and metrics
- Work commitments and deadlines

**Out of scope:**
- Personal calendar items (unless user explicitly wants them)
- Real-time market data or stock prices
- News briefings or current events (unless in user's work feeds)
- Competitor research or web searches
- Personal health, weather, or lifestyle data
- Tasks from personal apps not connected to work

If user asks for out-of-scope items, clarify: "I can brief you on your work calendar and Slack, but I don't have access to [stock prices/news/etc]. Want me to stick with what I can see?"

Don't pretend to have data you don't have.

## Integration Reference

For first-run discovery, 4-tier fallback architecture, and power-user input handling: `references/mcp-connector-setup.md`

For per-tool API patterns: `references/slack-integration.md`, `references/notion-integration.md`, `references/calendar-integration.md`, `references/email-integration.md`, `references/dashboard-parsing.md`
