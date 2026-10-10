---
name: synthesia-interactive-avatar
description: |
  Integrate the Synthesia Interactive Avatar into a LiveKit Agent end-to-end — detects the user's existing LiveKit setup and attaches the avatar with the three-line pattern, or scaffolds a complete boilerplate voice agent if none exists. Use when: (1) adding a real-time, interactive, conversational, or lip-sync avatar to a LiveKit agent, app, or site, or switching/swapping avatars mid-session, (2) the user mentions the Synthesia avatar plugin, livekit-plugins-synthesia, synthesia.AvatarSession, or the Interactive Avatar, (3) migrating from another avatar provider (HeyGen LiveAvatar, Tavus, Beyond Presence, Hedra) to Synthesia, (4) debugging Synthesia avatar issues — SynthesiaError (type AUTH, UNKNOWN_AVATAR, TIMEOUT, ...), avatar never joins, avatar joins but no lip-sync, (5) building any voice agent where the user wants a human face on it, even if they don't name Synthesia explicitly.
license: MIT
metadata:
  author: synthesia
  version: "1.5.0"
---

# Synthesia Interactive Avatar Integration

The Synthesia Interactive Avatar is a **plugin component for LiveKit Agents (Python)**. It renders a photoreal, lip-synced avatar and publishes it into the LiveKit room as a regular participant. The agent produces speech exactly as it always does; the component reroutes that audio to Synthesia's hosted avatar worker, which broadcasts synced audio + video back to the room.

This skill assesses what the user already has, picks ONE integration pathway, and implements it.

## Constraints — read before doing anything

These shape every recommendation. State them to the user up front if they're relevant:

- **Access-gated.** The API key must come from a Synthesia workspace with Interactive Avatar access; other keys are rejected (`SynthesiaError`, `type` `AUTH` or `FEATURE_NOT_IN_PLAN`). If the user has no key, stop and point them to the [Synthesia developer console](https://docs.synthesia.io/reference/synthesia-api-quickstart) — nothing you build will run without it.
- **Python only.** The plugin targets the Python LiveKit Agents framework, Python 3.10+. Node.js agents are not supported.
- **Default avatar:** Kenji, `"7572faa9-15da-400d-8227-ef1ab8932523"`. `AvatarConfig` takes `avatar_ids`: a list of one to five gallery ids. The first is the active avatar; the rest are precomputed so `swap_avatar()` can switch to them mid-session. Use Kenji alone unless the user names other avatars available to their workspace — inaccessible ids raise `SynthesiaError` with `type` `UNKNOWN_AVATAR` at `start()`, and a bare string instead of a list raises `ValueError`.
- **No sandbox.** Unlike some competitors, there is no free sandbox avatar — every session counts against the workspace's quota (`SynthesiaError` with `type` `QUOTA_EXCEEDED`, HTTP 402, on cap).
- **Install from PyPI:** `pip install "livekit-plugins-synthesia~=1.8"` (or the `uv add` equivalent).

## Step 1: Discover what the user has

Check the codebase and conversation before asking anything. **Do not ask questions the codebase already answers.**

### Signals to scan for automatically

| Signal | Where to look | What it means |
|--------|--------------|---------------|
| `livekit-agents` / `livekit.agents` imports | `pyproject.toml`, `requirements.txt`, imports | Has a Python LiveKit Agent → **Attach** |
| `AgentSession(llm=...realtime...)` | agent entrypoint | Realtime voice-to-voice mode |
| `AgentSession(stt=..., llm=..., tts=..., vad=...)` | agent entrypoint | Component-pipeline mode |
| `@livekit/agents` in `package.json` | Node project | Node agent → **Port or pause** (unsupported) |
| `livekit.plugins.tavus` / `bey` / `hedra` / `heygen` | imports | Another LiveKit avatar plugin → **Swap** |
| Calls to `api.heygen.com` / `api.liveavatar.com` | code, config | HeyGen LiveAvatar platform integration — see migration notes below |
| `livekit.plugins.synthesia` already imported | imports | Existing integration → **debug**, don't rebuild; go to `references/api-and-troubleshooting.md` |
| `SYNTHESIA_API_KEY` | `.env`, secret config | Synthesia key present |
| `LIVEKIT_URL` / `LIVEKIT_API_KEY` / `LIVEKIT_API_SECRET` | `.env`, config | LiveKit credentials present |
| `OPENAI_API_KEY` | `.env` | Can default to OpenAI Realtime for greenfield |
| LiveKit client SDK / `useVoiceAssistant` | frontend code | Has a LiveKit frontend — avatar appears there automatically |
| Python version | `pyproject.toml`, `python --version` | Must be 3.10+ |
| `livekit-agents` version | `pyproject.toml`, lockfile, `pip show livekit-agents` | Must be ≥ 1.8.2 — the plugin requires it |

### Questions to ask (only what's still unknown)

Ask as one concise checklist, never one at a time:

```
To wire up the Synthesia Interactive Avatar, I need to know:

1. **Do you have a Synthesia API key from a workspace with Interactive Avatar access?** Access
   is gated — without this, every session is rejected, so it's the first thing to confirm.
2. **Do you already have a LiveKit Agent running?** (Python or Node? Realtime model, or your own
   STT + LLM + TTS pipeline?)
3. **If we're building from scratch:** do you have an OpenAI API key (for a Realtime voice
   model), or do you have preferred STT/LLM/TTS providers?
```

Skip any question the codebase or conversation already answered.

## Step 2: Route to ONE pathway

**Always pick the simplest path that works. Make the call — do not offer a menu.**

```
Existing livekit.plugins.synthesia code already present?
  → DEBUG — read references/api-and-troubleshooting.md, fix in place

Working Python LiveKit Agent (realtime OR pipeline)?
  → ATTACH — three-line pattern, implemented inline below

Python agent using another LiveKit avatar plugin (tavus / bey / hedra / heygen)?
  → SWAP — near drop-in replacement, see below

LiveKit Agent exists but it's Node.js?
  → PORT OR PAUSE — plugin is Python-only. If the agent is simple, offer to port the
    entrypoint to Python; otherwise the honest answer is to wait for broader support.

No agent at all?
  → GREENFIELD — scaffold a minimal Python agent + avatar.
    Default: OpenAI Realtime (fewest moving parts, one extra key).
    Use the component pipeline variant only if the user lacks Realtime access or
    explicitly wants specific STT/LLM/TTS providers.
    → read references/greenfield-quickstart.md and follow it end-to-end
```

Then tell the user what you recommend and why, in 2–3 sentences, and proceed directly to implementation. Example:

> You already have a working pipeline agent (Deepgram STT + GPT-4o + ElevenLabs TTS), so this is an **Attach**: install the plugin, add three lines to your entrypoint, and the avatar lip-syncs to your existing TTS. No changes to your pipeline or frontend.

## Step 3: Implement

### Pathway: ATTACH (existing Python agent)

Works identically for realtime and pipeline agents — the component intercepts `session.output.audio` regardless of what produces it.

1. Install: `uv add "livekit-plugins-synthesia~=1.8"` (or pip equivalent). Raise any `livekit-agents` pin below 1.8.2 first; the plugin requires it.
2. Add `SYNTHESIA_API_KEY` to the agent's environment (secret manager or `.env` — never hard-code, never in frontend code).
3. In the entrypoint, after building `AgentSession` and **before** `session.start(...)`:

```python
from livekit.plugins import synthesia

avatar = synthesia.AvatarSession(
    synthesia.AvatarConfig(avatar_ids=["7572faa9-15da-400d-8227-ef1ab8932523"]),  # Kenji
)
await avatar.start(session, room=ctx.room)
```

4. If the user wants to switch avatars mid-session, pass every id up front (max five — only precomputed ids can be swapped in) and call:

```python
await avatar.swap_avatar("<another-id-from-avatar-ids>")  # switch mid-session
await avatar.swap_avatar("default")                       # back to the first id
```

That's the whole integration. No frontend changes: the avatar joins as a regular LiveKit participant, so any LiveKit client renders it automatically.

### Pathway: SWAP (from another LiveKit avatar plugin)

LiveKit standardised the avatar-plugin pattern, so this is usually a three-line diff:

| Their code | Replace with |
|------------|--------------|
| `from livekit.plugins import tavus` (or `bey`, `hedra`, `heygen`) | `from livekit.plugins import synthesia` |
| `tavus.AvatarSession(replica_id=..., persona_id=...)` etc. | `synthesia.AvatarSession(synthesia.AvatarConfig(avatar_ids=["7572faa9-15da-400d-8227-ef1ab8932523"]))` |
| `TAVUS_API_KEY` / provider env vars | `SYNTHESIA_API_KEY` |

Keep their `await avatar.start(session, room=ctx.room)` call and its position. Remove the old plugin extra from dependencies, add the synthesia extra.

**Migrating from HeyGen LiveAvatar specifically:** if they used HeyGen's *LITE mode* (their own STT + LLM + TTS pipeline driving a WebSocket), they already have a complete pipeline — build a LiveKit `AgentSession` around those same providers, then **Attach**. If they used HeyGen's *FULL mode* (HeyGen hosted the whole pipeline), they have no pipeline of their own — treat as **Greenfield**. Either way, delete their `X-API-KEY` / `livekit_client_token` plumbing; the Synthesia component mints room tokens itself inside the agent process.

### Pathway: GREENFIELD

Read `references/greenfield-quickstart.md` and follow it. It contains the full `.env` template, both agent variants (realtime and pipeline), frontend options, and run instructions.

## Principles that apply to ALL paths

- **Attach before start.** `await avatar.start(session, room=ctx.room)` must complete before `await session.start(...)`. Wrong order → avatar never appears, often with no error.
- **Never reassign `session.output.audio` after attaching.** The component owns that routing; overriding it silently kills lip-sync.
- **Match the voice to the avatar.** The avatar lip-syncs whatever voice the model produces — a mismatched persona (e.g. a female-presenting voice on a male-presenting avatar) reads as broken. Propose a voice that fits from the provider's list ([OpenAI Realtime](https://platform.openai.com/docs/guides/realtime), [OpenAI TTS](https://platform.openai.com/docs/guides/text-to-speech), or the user's TTS provider) and confirm with the user rather than shipping a default.
- **The API key stays in the agent process.** It is a workspace-bound secret. If you see `SYNTHESIA_API_KEY` heading toward frontend code, stop and restructure.
- **Two different "consoles" — never conflate them.** The *terminal* run mode (`python agent.py console`) is a local mock room: the avatar will never appear there and no error is raised. The **LiveKit Cloud Agent Console** (dashboard → project → Agents → Console) is the opposite — a real browser room that renders video for avatar agents, and the fastest place to test. So: run with `dev`, test in the Agent Console. When talking to the user, say "terminal `console` run mode" vs "LiveKit Cloud Agent Console" explicitly — a bare "don't use console" will be read as a warning against the very tool they should be using.
- **Fail fast on access.** Verify the API key works before writing lots of code: a quick `dev`-mode run surfaces `SynthesiaError` with `type` `AUTH` or `FEATURE_NOT_IN_PLAN` (no Interactive Avatar access) immediately.
- **Respect retryability.** Branch on `e.retryable` (`if not e.retryable: raise`). Retryable types: `TIMEOUT` (raise `join_timeout` — cold starts happen), `CONNECTION`, `RATE_LIMITED` and `CONCURRENCY_LIMIT` (honour `e.retry_after`). Everything else is a config problem to surface, not loop.

Full parameter, method, event, and exception tables plus the symptom→fix troubleshooting matrix are in `references/api-and-troubleshooting.md`. Read it whenever an error name appears or behaviour doesn't match expectations.

## Step 4: Verify and wrap up

1. Run `python agent.py dev`, then connect. Fastest path: **LiveKit Cloud Agent Console** — dashboard → the same project → Agents → Console → select the agent by its `agent_name` (`synthesia-avatar-agent` in the boilerplate) → **Start session**. Otherwise use the user's own LiveKit frontend.
2. Confirm the avatar joins and publishes video within `join_timeout` (default 30 s).
3. Speak to the agent; confirm the avatar's lip-sync matches the reply audio.
4. Confirm no secrets ended up client-side.

## What to consult

- `references/greenfield-quickstart.md` — full scaffold: env, install, both agent variants, frontend options, run instructions.
- `references/api-and-troubleshooting.md` — `AvatarSession` / `AvatarConfig` parameters, methods, events, exceptions with retryability, and the troubleshooting matrix.
- [Synthesia developer console](https://docs.synthesia.io/reference/synthesia-api-quickstart) — API keys and usage.
- [interactive-avatar-quickstarts/minimal](https://github.com/synthesia-ai/interactive-avatar-quickstarts/tree/main/minimal) — end-to-end quickstart: agent + frontend. Crib its frontend/token endpoint; its agent is latency-tuned beyond this skill's templates (the avatar lines are identical).
- [LiveKit Agents docs](https://docs.livekit.io/agents/) — framework reference.
