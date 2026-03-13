---
name: convo-agent-skills
version: 1.3.0
description: >
  Build real-time conversational AI applications using Agora SDKs and Next.js.
  Covers voice agents, video agents, AI agent lifecycle, live transcript/subtitles,
  RTM messaging/chat, avatar integration (HeyGen/Anam/Akool), settings persistence,
  and MCP tool calling. User and agent only; no host controls. Use alongside next-best-practices skill.
  Activates when the user wants to build a conversational AI app, voice/video agent,
  real-time communication with Agora, or add AI agent features to a Next.js app.
---

# Convo Agent Skills

Build Agora Conversational AI apps in Next.js. Pair with `next-best-practices` for Next.js conventions.

## Discovery — Ask Before Building

**IMPORTANT**: Before loading any references or writing any code, you MUST use the AskUserQuestion tool to gather requirements. Do NOT skip these questions.

Use AskUserQuestion with these questions:

**Question 1:**
- question: "What type of agent are you building?"
- header: "Agent type"
- multiSelect: false
- options:
  - Voice-only (Real-time voice conversation with AI agent)
  - Video + voice (Voice agent with camera/video support)
  - Text chat (RTM-based text messaging with AI)
  - Full-featured (Voice, video, text, and all features)

**Question 2:**
- question: "Which additional features do you need?"
- header: "Features"
- multiSelect: true
- options:
  - Live transcript / subtitles (Real-time speech-to-text display)
  - Settings UI (LLM, TTS, ASR configuration panel)
  - Avatar (HeyGen, Anam, or Akool avatar integration)

**Question 3:**
- question: "Are you building from scratch or adding to an existing project?"
- header: "Starting point"
- multiSelect: false
- options:
  - From scratch (New Next.js project, scaffold everything)
  - Existing project (Add Agora features to an existing Next.js app)

Wait for all answers before proceeding. Use the answers to determine which references to load from the Loading Paths table below.

## Loading Paths

Based on answers, load ONLY the needed references (one at a time, as user progresses):

| Goal | References to load (in order) |
|------|-------------------------------|
| Voice-only agent | 00 → 01 → 02 → 05 |
| Video + voice agent | 00 → 01 → 02 → 03 → 05 |
| Text chat with AI | 00 → 01 → 04 → 05 |
| Full-featured | 00 → 01 → 02 → 03 → 04 → 05 → 06 |
| + Transcript/subtitles | add 06 (and 04 if RTM mode) |
| + Settings UI | add 07 |
| + Avatar | add 08 (requires 03 + 05) |
| + MCP / advanced | add 09 |

## Dependency Graph

```
00-core-setup ← everything starts here
01-token-auth ← required by all features
02-rtc-voice ← requires 01
03-rtc-video ← requires 02 (extends voice with camera)
04-rtm-messaging ← requires 01 (independent of RTC)
05-agent-lifecycle ← requires 01 + (02 or 04)
06-transcript ← requires 05 + (02 or 04)
07-settings ← requires 05
08-avatar ← requires 03 + 05
09-advanced ← requires 05
```

## How to Load

Read references one at a time as the user progresses:
```
Read: <skill-path>/references/<filename>.md
```
For copy-paste code files:
```
Read: <skill-path>/snippets/<filename>
```

**IMPORTANT**: Do NOT load all references upfront. Load the next one only when the user is ready.

## Critical Architecture Patterns

Embed these in every implementation:

1. **Module-scoped singletons** — RTC/RTM clients and track refs MUST be module-scoped (outside hook function), NOT `useRef` inside hooks. Multiple components call `useAgora()` — each gets its own hook instance, so `useRef` state is NOT shared.

2. **Track lifecycle** — To guarantee hardware release (mic/camera indicator off):
   ```ts
   track.getMediaStreamTrack()?.stop(); // browser-native, guaranteed
   track.stop();
   track.close();
   ```

3. **Server key injection** — Client sends sentinel `"__USE_SERVER__"` for API keys. Server reads from env and replaces. Keys never appear in client code or browser.

## Common Post-Generation Issues

Fix these immediately if present in generated code:

1. **Agent UID "0"** — Invite route MUST return `responseData.agent_uid` from Agora, NOT the input `"0"`
2. **Agent in participant list** — Filter `agentRtcUid` + `agentAvatarRtcUid` in `handleUserPublished` (see 02)
3. **Empty transcript** — Do NOT skip `data.object` messages in RTM handler; route to `processTranscriptMessage` (see 04)
4. **Video toggle error** — Cleanup existing track before creating new one (see 03)
5. **No chat** — `sendChatMessage` must publish to agent UID with `channelType: "USER"` (see 04)
6. **Duplicate transcripts** — Use `addedTurnIds` Set + separate user/agent turn tracking (see 06)
7. **Chat echo** — Track sent messages in `recentlySentMessages` Set (see 04)
8. **Agent name 409** — Generate unique names: `${baseName}-${timestamp}-${random}` (see 05)
9. **Wrong field names** — User uses `final`, agent uses `turn_status` (NOT `is_final`) (see 06)
10. **Controls layout** — Center: mic/camera/end-call, Right: agent/settings

## Skill Boundaries

- **This skill**: Agora SDK patterns, token generation, agent API, transcript, RTM, avatar
- **next-best-practices**: API route structure, RSC boundaries, error handling, performance
