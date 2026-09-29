---
name: fish-audio-api
description: Generate narration with the public Fish Audio REST API using environment credentials and a user-selected voice. Provides shared public API helpers for Fish narration, OpenAI word timestamps, and optional GPT Image generation; no browser cookies or private proxy.
---

# Fish Audio public API

Use this skill when a video needs Fish narration. The release uses the official `POST https://api.fish.audio/v1/tts` endpoint. It does not ship a web-session proxy, cookies, an account, or a voice. Node.js 22.20 or later is required. Install FFmpeg/ffprobe for the video audio pipeline.

## Configure locally

Copy [env.example](env.example) to the **video project's** `.env`, ensure `.env` is ignored by Git, then fill it locally. Never request that users paste credentials into chat. Existing process environment values take precedence over `.env`. Scripts never print secret values or upstream error bodies.

| Variable | Meaning |
|---|---|
| `FISH_API_KEY` | API key created in the user's Fish account; required for generation. |
| `FISH_REFERENCE_ID` | A voice ID the user has permission to use; required unless a project explicitly supplies one. |
| `FISH_MODEL` | Defaults to `s2.1-pro-free`; supported choices also include `s1`, `s2-pro`, `s2.1-pro`. Account access and quotas are provider-controlled. |

No silent model fallback is allowed. An unknown model fails locally, because the provider may otherwise choose a paid default. Availability and pricing can change; check the account before generation. Setting a key does not itself authorize a charge: run synthesis only for the user's requested scope.

## Generate and revise

For a scaffolded HyperFrames project, edit `scripts/narration.json`. Its `voice.referenceId` and `voice.model` may be `null` to use the environment. All other voice settings are explicit in the template. Preview one short paragraph before producing a whole narration.

```sh
node scripts/tts-fish.mjs --section s0
node scripts/tts-fish.mjs
node scripts/tts-fish.mjs --section s2 --para 1 --force
```

`--para` requires every unselected paragraph in that section to exist. To start a new project, first generate one short section with `--section s0`; use `--para` for a later repair. Matching paragraph text and voice profiles reuse frozen audio. `--force` makes another API request for the selected speech.

The common helper [public-media-api.cjs](scripts/public-media-api.cjs) supports the shared audio engine as well. Its Fish configuration accepts `fish.transport: "official-api"`, `fish.reference_id`, `fish.model`, and `fish.request`. Sampling fields are top-level request fields, such as `temperature` and `top_p`; a website-style `backend`/`sampler` profile is not this API contract. Never put credentials in JSON project profiles.

Every generation POST is sent once. A timeout can occur after the provider started work; inspect provider usage before deliberately retrying. Redirects are refused. Official endpoints are pinned. `FISH_API_URL` with `HYPERFRAMES_TEST_ALLOW_FISH_LOOPBACK=1` is only for local mock tests.

## Optional public media APIs

The same helper supports OpenAI `whisper-1` transcription with word timestamps, and GPT Image PNG generation. These are separate account/billing capabilities, not features bundled by an agent subscription. See [requirements](../hyperframes-media/references/requirements.md) and [transcription](../hyperframes-media/references/transcribe.md). Images require an explicit `OPENAI_IMAGE_MODEL` or `--model`; choose a GPT Image model available to the user's account. External image/video tools, including Codex image tools and video-generation plugins, are optional and are not installed or authenticated by this skill package.

## Maintainer verification

```sh
node --test skills/fish-audio-api/tests/public-media-api.test.cjs
node --test skills/hyperframes/scripts/tests/fish-tts.test.mjs
```

These tests use fake keys and loopback HTTP, not paid services. The release verification does not establish that a user's account has model access.

Official references checked on 2026-09-26: [Fish TTS API](https://docs.fish.audio/api-reference/endpoint/openapi-v1/text-to-speech), [Fish developer guide](https://docs.fish.audio/developer-guide/core-features/text-to-speech).
