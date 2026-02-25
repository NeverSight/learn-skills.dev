---
name: realtime-voice-prompt
description: Expert guide for writing voice prompts for OpenAI's Realtime API (speech-to-speech). Use when creating, editing, or reviewing system prompts, conversation flows, tool definitions, or session configuration for voice assistants built on the Realtime API. Covers prompt structure, personality/tone, voice behavior (speed, language, variety), reference pronunciations, tool calling patterns (preambles, behavior types, rephrase supervisor), conversation flow design (static state machines, dynamic session.update), sample phrases, and safety/escalation. Use this skill whenever the task involves writing or improving a voice AI prompt.
---

# Voice Prompt Builder

Build effective voice prompts for OpenAI's Realtime API. Based on OpenAI's official Realtime Prompting Guide.

## General Tips

- **Iterate relentlessly** — small wording changes make or break behavior.
- **Bullets over paragraphs** — clear, short bullets outperform long prose.
- **Guide with examples** — the model closely follows sample phrases.
- **Be precise** — ambiguity or conflicting instructions = degraded performance.
- **Pin language** — explicitly constrain output language to prevent unwanted switching.
- **Reduce repetition** — add a Variety rule to avoid robotic phrasing.
- **CAPITALIZE key rules** — makes them stand out for the model.
- **Convert non-text rules to text** — write "IF MORE THAN THREE FAILURES THEN ESCALATE" not "IF x > 3 THEN ESCALATE".

## Prompt Structure

Organize the system prompt into labeled sections. Each section focused on one thing.

```
# Role & Objective             — who you are and what "success" means
# Personality & Tone           — voice, style, brevity, pacing
# Conversational Liveness      — backchannels, micro-acknowledgements, repair warmth
# Context                      — retrieved context, relevant info
# Reference Pronunciations     — phonetic guides for tricky words
# Tools                        — names, usage rules, preambles
# Instructions / Rules         — do's, don'ts, approach
# Conversation Flow            — states, goals, transitions
# Safety & Escalation          — fallback and handoff logic
```

Add domain-specific sections as needed (e.g., Compliance, Brand Policy). Remove sections not needed.

For detailed guidance on each section, see: [references/prompt-sections.md](references/prompt-sections.md)

## Tool Design

Tools in the Realtime API follow OpenAI function calling format. Key patterns:

### Behavior Types

Assign each tool a behavior type:

| Type | When to use | Model behavior |
|------|------------|----------------|
| **PROACTIVE** | Read-only lookups, low-risk | Call immediately, no confirmation, no preamble |
| **PREAMBLES** | Latency-sensitive lookups | Say a short filler phrase, then call immediately |
| **CONFIRMATION FIRST** | Write operations, bookings | Ask user before calling |

### Per-Tool Instructions

For each tool in the prompt, specify:
- **Use when**: specific trigger condition
- **Do NOT use when**: specific exclusion
- Preamble sample phrases (in tool description for PREAMBLES type)

### Preamble Sample Phrases in Tool Description

Add sample preamble phrases directly in the tool's `description` field:

```json
{
  "name": "lookup_account",
  "description": "Retrieve account by email or phone.\n\nPreamble sample phrases:\n- Let me look that up for you.\n- One moment, checking your account."
}
```

For advanced tool patterns (rephrase supervisor, common tools, error handling), see: [references/tools-patterns.md](references/tools-patterns.md)

## Conversation Flow

Break the interaction into phases with clear goals, instructions, and exit criteria.

### Per-State Format

Each state needs:
1. **Goal** — one sentence, what "done" means
2. **How to respond** — bullet list of actions
3. **Sample phrases** — 2-3 examples + "vary your responses"
4. **Exit criteria** — concrete condition to leave
5. **Transition** — which state to go to next

### Two Patterns

1. **Static State Machine** — all states in the system prompt as JSON or markdown. Good for simpler flows (4-6 states).
2. **Dynamic via session.update** — only current state's instructions + tools loaded. Swap on transition. Better for complex flows (6+ states, many tools per state).

For detailed flow design, state machine patterns, and sample phrases guidance, see: [references/conversation-flow.md](references/conversation-flow.md)

## Conversational Liveness

Micro-behaviors that make the voice agent feel present and actively listening, rather than robotic.

Key rules:
- **Backchannels** — brief signals ("mhm", "okay", "right") at most once every 2-3 caller utterances; never repeat the same one twice in a row
- **Micro-acknowledgements** — confirm what was heard in one short phrase before moving on: "Got it, [key detail]."
- **Turn-yield cues** — use softeners ("go ahead", "whenever you're ready") when handing the floor back; allow silence after questions
- **Micro-repair warmth** — when misunderstandings occur, use warm phrasing ("Let me make sure I have that right…"); never blame the caller
- **Never-list** — no fillers/backchannels while reading numbers, dates, or codes; no delay cues during emergencies; no casual fillers during legal/official procedures

For detailed guidance, see: [references/prompt-sections.md](references/prompt-sections.md)

## Safety & Escalation

Always include escalation rules. Define WHEN to escalate:

- Safety risk (self-harm, threats, harassment)
- User explicitly asks for a human
- Severe frustration (repeated complaints, profanity)
- 2 failed tool attempts on the same task OR 3 consecutive no-match events
- Out-of-scope or restricted topics (financial/legal/medical advice)

Define WHAT to say:
```
"Thanks for your patience — I'm connecting you with a specialist now."
```

Then call `escalate_to_human` tool.

## Voice Behavior Checklist

Apply these rules to every voice prompt:

- [ ] Max 1-2 sentences per response turn (never more than 3)
- [ ] Ask ONE question at a time, never multiple
- [ ] Use natural filler words for the target language
- [ ] Greeting under 15 words
- [ ] If interrupted, stop and listen
- [ ] When user pauses mid-sentence, wait
- [ ] Say numbers/dates naturally, not formally
- [ ] Read back numbers/codes digit-by-digit with hyphens (e.g., 4-1-5)
- [ ] Do not produce sound effects or background music
- [ ] Add unclear audio handling instructions
- [ ] Add variety rule to prevent repetition
- [ ] Pin to target language if needed
- [ ] Include backchannel rules (frequency + variation)
- [ ] Add micro-acknowledgement before each state transition
- [ ] Add turn-yield cues and silence-after-question rule
- [ ] Include micro-repair warmth phrasing
- [ ] Apply never-list (no fillers during numbers/emergencies/legal)

## Quality Check

After writing a prompt, verify:

1. **No conflicting instructions** — rules should not contradict each other
2. **Tools in prompt match tools list** — do not mention tools not in the tools array
3. **Tool descriptions do not contradict each other**
4. **Every state has exit criteria and a transition target**
5. **Sample phrases exist for every state** (with "vary your responses" note)
6. **Language is pinned** if multilingual switching is undesired
7. **Voice behavior rules** are included (see checklist above)

Use the Instructions Quality Prompt from [references/prompt-sections.md](references/prompt-sections.md) to have a text model critique your prompt before deploying.
