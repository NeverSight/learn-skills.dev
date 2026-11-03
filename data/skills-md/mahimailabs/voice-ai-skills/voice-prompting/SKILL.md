---
name: voice-prompting
description: Write system prompts for agents that speak instead of type. Covers spoken-output rules, splitting persona from task, writing numbers, dates, and phone numbers so the TTS says them correctly, confirmation phrasing, sentence length for interruptible speech, and what never belongs in a voice prompt. Use when writing or reviewing a voice agent system prompt, when the agent reads markdown or bullet points aloud, when replies run too long or the agent talks too much, or when the TTS mangles or mispronounces numbers, dates, times, or names.
license: MIT
metadata:
  author: mahimairaja
  version: "0.1.0"
  category: voice-ai
---

# Voice Prompting

A voice prompt decides what the caller hears, word by word. This file sets the four
blocks a voice prompt needs, the spoken form of every number, and the sentence budget.

## Use this when

- The agent reads asterisks, headers, or bullet characters aloud.
- The agent says a date as "twenty twenty six dash oh three dash fourteen".
- The agent talks for forty words and the caller gives up waiting.
- You are porting a chat prompt onto a phone line.
- A read-back before a write is missing, wrong, or phrased differently every call.

## Do not

- Reuse a chat prompt on a phone line. Every failure listed below starts there.
- Allow markdown, lists, or headers in output. The characters get read aloud.
- Write numbers as digits in prompt examples. The model copies the digit form.
- Put persona and tool policy in one paragraph. An edit to one breaks the other.
- Write example sentences longer than 20 words. The model matches your length.
- Ask for concision without a word count. "Be concise" measures nothing.
- Put the knowledge base in the system prompt. Retrieve what the turn needs.

## Why a chatbot prompt fails out loud

- Markdown is spoken: the caller hears "asterisk asterisk" and "pound sign".
- Lists are spoken as lists: three options arrive as one wall of audio.
- Digits are read wrong: 1952 becomes "one thousand nine hundred fifty two".
- Sentences run past 25 words: the caller interrupts before the point lands.

## The four blocks

Split the prompt into four labeled blocks, in this order. Copy-paste text for all
four is in [references/prompt-blocks.md](references/prompt-blocks.md).

**Spoken output.** How text becomes speech: no markdown, no symbols, one idea per
sentence, under 20 words, numbers written as words. It carries no persona and no
procedure. This block is close to identical across every agent you ship.

**Persona.** Who is speaking: name, role, tone, pace, and what it refuses to do.
Two to five sentences. It carries no step order and no tool name. Change the voice
here without touching the booking flow.

**Task.** The call flow in order, the fields to collect, and which tool to call at
each step. It names tools and arguments. It carries no tone words. When a scenario
fails on flow, this is the only block you edit.

**Confirmation.** The read-back script, the fields to repeat, and the rule that a
write follows a spoken yes. It carries no alternative phrasings, because a read-back
that varies per call is a read-back you cannot assert on.

## Numbers, dates, and codes

This table is the centerpiece. The left column is what a tool or a database returns.
The middle column is what the prompt tells the agent to say.

| written | say | never say |
| --- | --- | --- |
| phone number 555 0142 | "five five five, oh one four two" | "five hundred fifty five, one forty two" |
| date 2026-04-14 | "Tuesday, April fourteenth" | "twenty twenty six dash oh four dash fourteen" |
| time 15:15 | "three fifteen in the afternoon" | "fifteen colon fifteen" |
| money $40.00 | "forty dollars" | "four zero point zero zero dollars" |
| confirmation code R4K9 | "R as in Romeo, four, K as in Kilo, nine" | "arfourkaynine" |
| record number 00814226 | "zero zero, eight one, four two, two six" | "eight hundred fourteen thousand two hundred twenty six" |
| ordinal 3rd | "third" | "three R D" |
| year 1952 | "nineteen fifty two" | "one thousand nine hundred fifty two" |
| percentage 12% | "twelve percent" | "twelve percent sign" |
| address 120 Front St N | "one twenty Front Street North" | "one hundred twenty Front S T N" |

Group long digit strings in twos or threes, with a comma between groups. The comma
buys the caller a pause to write. Read alphanumeric codes with a letter word for
every letter, because letters collapse on a narrowband line.

## Sentence length

Cap agent output at 20 words per sentence, one idea per sentence. A caller who
interrupts at word 25 has already lost the point, and the agent has to restart the
whole thought. Put the cap in the prompt as a number. "Be concise" gives the model
nothing to measure against, so it writes paragraphs and calls them brief.

## Persona versus task

Persona and task change for different reasons and at different rates. Persona changes
when the brand or the voice changes. Task changes when the flow, the fields, or a tool
changes. Merged into one paragraph, the model blends them and drops the middle. Tone
bleeds into step order, and a tone edit silently reorders the call. Separate blocks
also tell you which block to edit when a scenario fails.

## What never goes in a voice prompt

- The knowledge base. Retrieve the two or three facts the turn needs.
- Tool schemas. The tool layer already sends them to the model.
- Markdown headers, asterisks, bullet characters, and emoji.
- Digits in example lines. Write the spoken form instead.
- Example sentences over 20 words. The model copies the length.
- Internal identifiers, record keys, and secrets the agent could read aloud.

## The clinic example

Riverside Family Medicine, four physicians, booking on the main line. Four lines of a
chatbot prompt, and the voice rewrite of each.

| chatbot line | voice rewrite |
| --- | --- |
| "Format answers in Markdown with bullet points." | "You are speaking on a phone call. No lists, no headers, no symbols." |
| "Offer available slots, for example 2026-04-14 15:15 with Dr. Osei." | "Offer at most three slots, one sentence each. Say 'Tuesday, April fourteenth at three fifteen with Doctor Osei.'" |
| "Be concise and professional." | "Keep every sentence under twenty words. One idea per sentence. No filler words." |
| "Confirm the booking with the patient." | "Read back name, day, date, time, and physician in one sentence. Call book_appointment only after the caller says yes." |

The full clinic prompt, with all four blocks and the three canonical tools, is in
[references/prompt-blocks.md](references/prompt-blocks.md).

## Using this skill

Read related skills by name from your installed skills when available. The repository
links are optional deeper guidance; this skill and its bundled references can be used
on their own. If a linked skill is unavailable, continue with the rules here and name
any analysis you could not complete.

Before writing SDK calls, verify the relevant adapter against current official docs
or a docs MCP. If neither is accessible, use supplied version-matched docs or mark the
API detail unverified. Continue vendor-neutral analysis; do not invent a method or
claim an integration was tested. Python is needed only when running a bundled helper.

## Adapters

Vendor names appear only in this section and in
[references/adapters.md](references/adapters.md), which carries a doc URL per claim.

### LiveKit Agents
Pinned 1.8.x, verified 11 September 2026. The system prompt is the required
keyword-only `instructions` on the `Agent` subclass. Override it for one reply with
`session.generate_reply(instructions=...)`, also keyword-only.

```python
super().__init__(instructions=SPOKEN + PERSONA + TASK + CONFIRM)
```
Docs: https://docs.livekit.io/agents/start/voice-ai/

### Pipecat
Pipecat 1.0 docs, checked 11 September 2026. The system prompt goes in
`system_instruction` on the LLM service `Settings`, not in a context message.

```python
prompt = SPOKEN + PERSONA + TASK + CONFIRM
settings = OpenAILLMService.Settings(system_instruction=prompt)
llm = OpenAILLMService(api_key=key, settings=settings)
```
Docs: https://docs.pipecat.ai/pipecat/learn/function-calling

### Vapi
Unversioned docs, checked 11 September 2026. The system prompt is a `system` role
entry in `model.messages`. The greeting is the separate `firstMessage` field.

```python
model = {"provider": "openai", "model": MODEL,
         "messages": [{"role": "system", "content": PROMPT}]}
assistant = {"model": model, "firstMessage": GREETING}
```
Docs: https://docs.vapi.ai/openai-realtime
