---
name: audio-intelligence
description: >
  Analyze what was said in audio, not just transcribe it. Use when a task mentions
  "audio intelligence", "sentiment", "sentiment analysis", "summarize a recording",
  "summarization", "topics", "topic detection", "intents", "intent recognition",
  "entity detection", "detect entities", "extract names and amounts from a call",
  or "analyze a call recording". These are five query parameters layered on the
  speech-to-text endpoint /v1/listen (summarize, sentiment, topics, intents,
  detect_entities), not a separate API. Covers the prerecorded-only and English-only
  limits, where each result lives in the JSON, and the errors you get when you cross
  a limit. Routes to the api, docs, recipes, starters, and per-language SDK skills.
---

# Deepgram Audio Intelligence

Audio intelligence is not a separate endpoint. It is five query parameters on `/v1/listen`, the
same endpoint that returns the transcript. You get the transcript and the analysis in one response,
from one API call. This skill gets a verified request working and states the limits precisely.

## Decide first

- **Your input is audio** (a file, a URL, a call recording) and you want analysis: stay here, use
  `POST https://api.deepgram.com/v1/listen`.
- **Your input is already text** (a transcript, an email, a chat log, a support ticket): the
  parameters below do not apply. Use the Read API, `POST /v1/read`. Open the `text-intelligence` skill.
- **You only want the transcript**: drop these parameters and open the `speech-to-text` skill.
- **You are streaming live audio**: see the matrix (`detect_entities` only).

## Feature matrix

| Parameter | Prerecorded | Streaming (`wss`) | Language |
|---|---|---|---|
| `summarize=v2` (or `summarize=true`) | yes | **no** | English only; an explicit non-English `language` is a 400 (mistake 3 covers `detect_language`) |
| `sentiment=true` | yes | **no** | English only |
| `topics=true` | yes | **no** | English only |
| `intents=true` | yes | **no** | English only |
| `detect_entities=true` | yes | **yes** | English only |

`detect_entities` is the odd one out twice over: it is the only feature that works on the live
socket, and it is the only one that does **not** exist on the Read API. Streaming entity detection
runs on Nova, Nova-2, Nova-3, and Enhanced; it is not available on Base models or on Flux STT. [2]

## Verified request

```bash
curl -s -X POST 'https://api.deepgram.com/v1/listen?model=nova-3&smart_format=true&summarize=v2&sentiment=true&topics=true&intents=true&detect_entities=true' \
  -H "Authorization: Token $DEEPGRAM_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://dpgr.am/spacewalk.wav"}'
```

Returns 200. The analysis is scattered across the response, not collected in one place:

| Result | Path |
|---|---|
| Summary | `results.summary.short` (with `results.summary.result` = `"success"`) |
| Sentiment per segment | `results.sentiments.segments[]` — `text`, `start_word`, `end_word`, `sentiment`, `sentiment_score` |
| Sentiment overall | `results.sentiments.average` — `sentiment`, `sentiment_score` |
| Sentiment per word | `results.channels[0].alternatives[0].words[]` gains `sentiment` and `sentiment_score` |
| Topics | `results.topics.segments[].topics[]` — `topic`, `confidence_score` |
| Intents | `results.intents.segments[].intents[]` — `intent`, `confidence_score` |
| Entities | `results.channels[0].alternatives[0].entities[]`: `label`, `value`, `raw_value`, `confidence`, `start_word`, `end_word` |

Note the plural: the parameter is `sentiment`, the result key is `sentiments`. `metadata` gains a
`summary_info`, `sentiment_info`, `topics_info`, and `intents_info` block per enabled feature, each
with `model_uuid`, `input_tokens`, and `output_tokens`. `sentiment_score` runs from `-1` to `1`,
and the break point between `neutral` and `positive` or `negative` is `0.333...` either side of
zero; `confidence_score` on topics and intents runs from `0` to `1`. [3] Entity labels come back
uppercased (`NAME`, `ORGANIZATION`, `LOCATION_CITY`, `MONEY`, `DATE_INTERVAL`, `CARDINAL`).
`value` is the formatted text and `raw_value` is the text as spoken; `raw_value` is present when
a formatting feature such as `smart_format` is on. [4] Deepgram documents 59 entity types, and
`redact` accepts 56 of them: `cardinal`, `ordinal`, and `percent` are detected but are not valid
`redact` values, and passing one to `redact` returns a 400. [6]

`summarize` needs more than 50 words of speech. For a shorter input, `summary.short` is the
original input returned as-is, and no tokens in or out are billed as summarization usage, so a
`summary_info` with zero tokens on a short clip is not a failure. [3]

On the live socket, `detect_entities=true` adds a **top-level** `entities` array to `Results`
messages, next to `channel` and not inside `channel.alternatives[0]`. Read entities only from
messages whose `is_final` is `true`. Interim results can carry the key too, usually `[]` and
sometimes populated, and those values are not final. A final result with nothing detected
carries `"entities": []`. Same field shape as above, `raw_value` included when formatting is on. [4]

To return complete entities, the server holds a final result until the speaker moves on to
non-entity speech, 3 seconds of silence pass, or a `Finalize` message arrives. `no_delay=true`
forces immediate finalization without that wait, and leaves entities missed or incomplete in
many cases. Send `no_delay=true` only when latency matters more than entity
accuracy. [4]

## Narrowing topics and intents

`custom_topic` and `custom_intent` (repeatable, up to 100 of each) add your own labels;
`custom_topic_mode` and `custom_intent_mode` take `extended` (default, your labels plus the
model's) or `strict` (your labels only). `strict` returns `"segments": []` whenever nothing
matches your list, which looks like a broken request but is not. Start with `extended`. [3]

## Common mistakes

1. **Expecting these to work on streaming.** `summarize` fails the WebSocket handshake with 400 `"Summarization is not available
   for streaming."`. `topics` and `intents` fail it with 403
   `{"err_code":"UNAUTHORIZED_FEATURES_REQUESTED","err_msg":"Project does not have access to the
   requested feature/s [\"topics\"]."}`, which reads as a permissions problem but is not one: the
   same key's prerecorded `topics` requests succeed, and the docs matrix lists streaming as
   unsupported for both. [2] `sentiment` is worse still: the
   handshake **succeeds** and no sentiment is ever returned. Only `detect_entities` works.
2. **Expecting a non-English request to fail loudly.** It does not. With `language=es` on real
   Spanish audio, `sentiment`, `topics`, `intents`, and `detect_entities` return **HTTP 200** with
   the transcript, the analysis keys silently absent, and the reason only in `metadata.warnings`:
   `[{"parameter":"sentiment","type":"unsupported_language","message":"Sentiment is only supported
   for English."}]`, plus `"Topics are only supported for English."`, `"Intents are only supported
   for English."`, and `"Entity detection is only supported for English."`. Read
   `metadata.warnings` before you conclude the model found nothing.
3. **Assuming `summarize` behaves the same way.** It is the exception when `language` is explicit:
   `language=es` is a hard 400,
   `{"err_code":"Bad Request","err_msg":"Summarization v2 not supported for non-English languages"}`,
   and `language=multi` gets the same 400. With `detect_language=true` and non-English speech it
   behaves like the others: HTTP 200, a `metadata.warnings` entry with `"parameter":"summarize"`
   and `"type":"unsupported_language"`, and `results.summary` present with `"result":"failure"`
   and a `short` string that says the feature is English only. Check `summary.result` before you
   use `summary.short`. [3]
4. **`language=multi` as a workaround.** It is not one. For `sentiment`, `intents`, and `topics`,
   `multi` returns the analysis when the detected speech is English and drops it with the same
   `metadata.warnings` when it is not, so the same request succeeds or silently degrades
   depending on what the caller said. `summarize` with `language=multi` is a 400.
5. **`summarize=v1`.** Returns 400 `"To use the summarize feature, please use 'summarize=true' or
   'summarize=v2'. The 'summarize=v1' parameter is deprecated."` Use `v2`; `true` is accepted and
   returns the same `summary.short` shape.
6. **Looking for `results.summary.text`.** That is the Read API's shape. On `/v1/listen` the
   summary is at `results.summary.short`.
7. **Putting any of these on Flux STT.** `/v2/listen` rejects all five at the handshake with 400
   `{"err_code":"INVALID_QUERY_PARAMETER","err_msg":"Unknown query parameters: detect_entities"}`,
   and the same message naming `summarize`, `sentiment`, `topics`, or `intents`. Transcribe with
   Flux STT, then send the transcript to `/v1/read`.
8. **Reaching for these to mask PII.** Detection returns entities, it does not remove them. Use
   `redact` for that, which is a speech-to-text parameter and rejects `cardinal`, `ordinal`, and
   `percent` (see the entity-type counts above). [6]

## Pricing

Enabling these features changes what a request costs. Rates and the billing model change, so read
<https://deepgram.com/pricing> rather than any figure quoted in a skill.

## Use a different skill when

- Your input is text rather than audio, or you need the Read API's input limits: `text-intelligence`
  skill (`/v1/read`).
- You want every parameter and the full response schema: `api` skill, `references/listen.md`.
- You only need transcription, diarization, redaction, or captions: `speech-to-text` skill.
- You want a runnable demo app: `starters` skill. Note there is no `audio-intelligence` starter; the
  `text-intelligence` feature (13 frameworks) is the Read API app.
- You want a snippet under 50 lines: `recipes` skill, "Audio Intelligence `v1`" — `summarize`,
  `sentiment`, `topics`, `intents`, `entities`, in Python, JavaScript, Go, .NET, Java, Rust, and the
  CLI. [7]
- You want language-idiomatic SDK code: install `deepgram-{js,python,java,go,rust,dotnet}-audio-intelligence`
  from the matching SDK repository (`npx skills add deepgram/deepgram-python-sdk`, and so on).
- You want to find a docs page: `docs` skill. You want the docs in your editor: `setup-mcp` skill.

## Sources

1. https://developers.deepgram.com/docs/audio-intelligence (getting started)
2. https://developers.deepgram.com/docs/stt-intelligence-feature-overview (the prerecorded/streaming/language matrix, and the streaming entity-detection model footnote)
3. https://developers.deepgram.com/docs/summarization, https://developers.deepgram.com/docs/sentiment-analysis, https://developers.deepgram.com/docs/topic-detection, https://developers.deepgram.com/docs/intent-recognition
4. https://developers.deepgram.com/docs/detect-entities
5. https://developers.deepgram.com/docs/language and https://developers.deepgram.com/docs/models-languages-overview
6. https://developers.deepgram.com/docs/supported-entity-types (59 entity types, 56 of them valid `redact` values) and https://developers.deepgram.com/docs/redaction
7. https://github.com/deepgram/recipes/blob/main/COVERAGE.md ("Audio Intelligence `v1`" section)
8. https://developers.deepgram.com/reference/speech-to-text/listen-pre-recorded and https://developers.deepgram.com/reference/speech-to-text/listen-streaming
9. https://developers.deepgram.com/docs/errors and https://deepgram.com/pricing
