---
name: text-intelligence
description: >
  Analyze text you already have with Deepgram's Read API. Use when a task says
  "text intelligence", "read API", "/v1/read", "analyze text", "sentiment of this
  text", "summarize this transcript", "summarize a document", "topic detection on
  text", "intent recognition on text", "analyze a support ticket", or "analyze a chat
  log". One REST call, POST /v1/read, with four features: summarize, sentiment,
  topics, intents. Covers the two required query parameters people miss, the
  text-versus-url body, the English-only limit, and why entity detection is not
  here. Routes to audio-intelligence for audio input and to the api, docs, recipes,
  starters, and per-language SDK skills.
---

# Deepgram Text Intelligence (Read API)

`POST https://api.deepgram.com/v1/read` takes text and returns analysis. No audio, no transcript,
no streaming — one request, one response. Four features: `summarize`, `sentiment`, `topics`,
`intents`.

## Decide first

- **Your input is text** — a transcript you already have, a document, an email, a chat log, a
  support ticket: stay here.
- **Your input is audio**: do not transcribe and then call this. `/v1/listen` runs the same analysis
  during transcription, in a single API call. Open the `audio-intelligence` skill.
- **You need entity detection** (names, amounts, dates): only `/v1/listen` detects entities
  (`/v1/read` does not offer `detect_entities`), so your input has to be audio.
- **You need streaming**: there is none. `/v1/read` is POST-only — a GET returns 405, and so does a
  WebSocket upgrade against the same path.

## Verified request

Both `language` and at least one feature are **required**. Omitting either is a 400.

```bash
curl -s -X POST 'https://api.deepgram.com/v1/read?language=en&summarize=v2&sentiment=true&topics=true&intents=true' \
  -H "Authorization: Token $DEEPGRAM_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"text":"Hi, this is Maria Gonzalez from Acme Corp in Denver. The invoice we received on March 3rd double-charged us on the annual plan, and the second line item does not match the quote your sales team sent us in February. I would like a refund for the duplicate charge and I want to cancel the second subscription. Please confirm by email once the refund is issued, and let me know whether we need to sign a new agreement to keep the remaining seats active through the end of the year."}'
```

Returns 200. The sample runs to 90 words because `summarize` needs more than 50 words of input.
For a shorter input, `results.summary.text` is the original text returned unchanged, and no
tokens in or out are billed as summarization usage, so `metadata.summary_info` reports zero. A
summary that reads exactly like the input is the input. [3]

Where each result lives:

| Result | Path |
|---|---|
| Summary | `results.summary.text` |
| Sentiment per segment | `results.sentiments.segments[]` — `text`, `start_word`, `end_word`, `sentiment`, `sentiment_score` |
| Sentiment overall | `results.sentiments.average` — `sentiment`, `sentiment_score` |
| Topics | `results.topics.segments[].topics[]` — `topic`, `confidence_score` |
| Intents | `results.intents.segments[].intents[]` — `intent`, `confidence_score` |

The parameter is `sentiment`; the result key is `sentiments`. `metadata` carries `request_id`,
`created`, `language`, and one `summary_info` / `sentiment_info` / `topics_info` / `intents_info`
block per enabled feature, each with `model_uuid`, `input_tokens`, and `output_tokens`. That token
count is what you reconcile usage against. `sentiment_score` runs from `-1` (most negative) to `1`
(most positive), and the break point between `neutral` and `positive` or `negative` is `0.333...`
either side of zero. `confidence_score` on topics and intents runs from `0` to `1`. [3]

## The body: exactly one of `text` or `url`

Three accepted shapes:

- `Content-Type: application/json` with `{"text": "..."}`.
- `Content-Type: application/json` with `{"url": "..."}`, where the URL serves either
  `text/plain` or `application/json` with a `text` field. Deepgram fetches it. [7]
- `Content-Type: text/plain` with the raw text as the whole body, no JSON wrapper.

Sending both `text` and `url`, or neither, returns 400 `{"err_code":"PAYLOAD_ERROR","err_msg":"Failed
to deserialize JSON payload. Please specify exactly one of \`text\` or \`url\` in the JSON body."}`.
Any other `Content-Type` returns 415 `{"err_code":"UNSUPPORTED_MEDIA_TYPE","err_msg":"\`Content-Type\`
header is not supported. \`Content-Type\` must be either \`text/plain\` or \`application/json\`."}`. [7]

Input is capped at 150K tokens per request. Above that the response is 400
`{"err_code":"TOKEN_LIMIT_EXCEEDED","err_msg":"Text input for <api_name> currently supports up to
150K tokens. Please revise your text input to fit within the defined token limit. For more
information, please visit our API documentation."}`. [3]

Chunk a document that approaches 150K tokens rather than sending it whole.

## Hosts and concurrency

`/v1/read` is served on `api.eu.deepgram.com`, `api.au.deepgram.com`, and `api.in.deepgram.com`
as well as `api.deepgram.com`. A request to a regional host is never routed outside that region;
if the region is unavailable the request fails rather than falling back. [10]

Concurrency limits are scoped to the project, not the key, so every key in a project draws from
one pool and adding projects to an account does not raise it. On Pay as You Go and Growth, each
Read feature allows up to 10 concurrent requests on `api.deepgram.com`; on the EU, AU, and India
hosts `summarize` and `topics` keep 10 while `sentiment` and `intents` drop to 5. Enterprise starts
at 10 per feature, 20 for `summarize`. [11]

## Options

- `summarize` accepts `v2` **and** `true`; both return `results.summary.text`.
- `custom_topic` and `custom_intent` (repeatable, up to 100 of each) add your own labels.
  `custom_topic_mode` and `custom_intent_mode` take `extended` (default: your labels plus the
  model's own) or `strict` (your labels only). `strict` returns `"segments": []` when nothing
  matches, which reads as a broken request but is not. Start with `extended`. [3]
- `callback` (with optional `callback_method`, `POST` by default or `PUT`) makes the request
  asynchronous. The response body becomes just `{"request_id":"..."}` and the analysis is sent to
  your URL. The URL is `http` or `https` on port 80, 443, 8080, or 8443 only. Authenticate the
  callback either with Basic Auth credentials embedded in the URL or by checking the `dg-token`
  header Deepgram adds, which carries the API Key Identifier of the key that made the request. If
  your endpoint answers with a status outside 200 to 299, Deepgram retries up to 10 times with a
  30-second delay between attempts. [5]
- `tag` (repeatable) labels the request for usage reporting. Each tag is at most 128 characters,
  at most 500 unique tags are accepted per day, and a tag cannot be changed once set. Tags on the
  API key are applied to the request too. [6]

## Common mistakes

1. **Omitting `language`.** The generated API reference documents `language` as optional with
   default `en`. It is not optional. The live API returns 400
   `{"err_code":"INVALID_QUERY_PARAMETER","err_msg":"Failed to deserialize query parameters:
   missing field \`language\`"}`. Always send `language=en`. This error fires *before* any other
   validation, so it masks every other mistake in the request — fix it first.
2. **Enabling no features.** `language=en` alone returns 400 `"Request did not enable any features.
   Please enable at least one feature. Available features: \`summarize\`, \`topics\`, \`intents\`,
   \`sentiment\`."` That error string is also the authoritative list of what the Read API does.
3. **Any language other than English.** `language=es` returns 400 `"Request specified unsupported
   language: es. Only English is supported."` Same for `fr`, and `language=multi` is rejected the
   same way — there is no code-switching mode here, unlike `/v1/listen`. Regional English tags are
   fine: `en-US` is accepted and reported back as `"language": "en"`.
4. **Sending `detect_entities`.** 400 `{"err_code":"INVALID_QUERY_PARAMETER","err_msg":"unknown
   query parameter: detect_entities"}`. Entity detection exists only on `/v1/listen`.
5. **Pointing `url` at audio.** `{"url":"https://dpgr.am/spacewalk.wav"}` returns 400
   `{"err_code":"REMOTE_CONTENT_ERROR","err_msg":"Failed to deserialize remote text data. Please
   provide \`application/json\` with a \`text\` field or \`text/plain\`."}`. `url` means a text
   document. Audio goes to `/v1/listen`.
6. **Looking for `results.summary.short`.** That is `/v1/listen`'s shape. Read returns
   `results.summary.text`. Code that handles both endpoints has to branch.
7. **Transcribing, then calling Read.** Two round trips instead of one, and no entity detection:
   when you start from audio, put the parameters on `/v1/listen` (`audio-intelligence` skill).
8. **Wrong auth scheme.** API keys use `Authorization: Token <key>`. `Bearer` is only for the
   short-lived JWT from `POST /v1/auth/grant`. [7]

## Pricing

Every feature you enable adds to what the request costs. Rates and the billing model change, so
read <https://deepgram.com/pricing> rather than any figure quoted in a skill.

## Use a different skill when

- Your input is audio: `audio-intelligence` skill. It also covers entity detection.
- You want every parameter and the response schema: `api` skill, `references/read.md`. `language`
  is required with no default (mistake 1), `summarize` accepts `v2` as well as `true`, and the
  response is the flat shape in the table above. [4]
- You want a shell command rather than application code: `cli` skill. `dg read --file document.txt
  --summarize --sentiment --topics --intents` runs the same request. [12]
- You want a runnable demo app: `starters` skill, feature `text-intelligence`, available for node,
  bun, deno, fastapi, flask, django, go, java, csharp, rust, ruby, php, and cpp.
- You want a snippet under 50 lines: `recipes` skill. The repo's "Text Analysis `v1`" section has
  `summarize`, `sentiment`, `topics`, and `intents` in Python, JavaScript, Go, .NET, Java, Rust, and
  the CLI. [8]
- You want language-idiomatic SDK code: install `deepgram-{js,python,java,go,rust,dotnet}-text-intelligence`
  from the matching SDK repository (`npx skills add deepgram/deepgram-python-sdk`, and so on).
- You want speech-to-text, text-to-speech, or a voice agent: the `speech-to-text`, `text-to-speech`,
  or `voice-agent` skill.
- You want to find a docs page: `docs` skill. You want the docs in your editor: `setup-mcp` skill.

## Sources

1. https://developers.deepgram.com/docs/text-intelligence (getting started)
2. https://developers.deepgram.com/docs/text-intelligence-feature-overview (the four features, English only, no streaming)
3. https://developers.deepgram.com/docs/text-summarization, https://developers.deepgram.com/docs/text-sentiment-analysis, https://developers.deepgram.com/docs/text-topic-detection, https://developers.deepgram.com/docs/text-intention-recognition
4. https://developers.deepgram.com/reference/text-intelligence/analyze-text
5. https://developers.deepgram.com/docs/text-intelligence-callback
6. https://developers.deepgram.com/docs/text-intelligence-tagging
7. https://developers.deepgram.com/guides/fundamentals/authenticating and https://developers.deepgram.com/docs/errors
8. https://github.com/deepgram/recipes/blob/main/COVERAGE.md ("Text Analysis `v1`" section)
9. https://developers.deepgram.com/docs/text-intelligence-template-apps and https://deepgram.com/pricing
10. https://developers.deepgram.com/reference/regional-endpoints (`/v1/read` on the EU, AU, and India hosts)
11. https://developers.deepgram.com/reference/api-rate-limits (Text Intelligence concurrency per plan and region) and https://developers.deepgram.com/docs/working-with-concurrency-rate-limits
12. https://developers.deepgram.com/developer-tools/cli/text-intelligence (`dg read`)
