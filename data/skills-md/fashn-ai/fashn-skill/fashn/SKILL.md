---
name: fashn
description: Integrate FASHN generative image & video models for fashion into a project, or run it inline. Use for virtual try-on, product-to-model, model create/swap, face-to-model, edit, reframe, background removal, and image-to-video, via the FASHN REST API, the TypeScript SDK (fashn npm), or the Python SDK (fashn pip).
allowed-tools: Bash, Read, Write, Edit
---

# FASHN API & SDKs

FASHN is an AI-first company specializing in human-centric generative image models tailored for fashion applications: virtual try-on, AI models, product photography, editing, and image-to-video. Everything runs through **one prediction endpoint** that takes a `model_name` plus an `inputs` object.

This skill helps you do two things:

1. **Integrate FASHN into a project**: write production code against the REST API, the **TypeScript SDK** (`fashn` on npm), or the **Python SDK** (`fashn` on PyPI).
2. **Run a one-off generation inline**: execute a single call and hand the result back to the user (see [Inline quickstart](#inline-quickstart)).

When the user asks to *add FASHN to their app / repo*, integrate (write code into their project). When they ask to *just do a try-on / generate an image now*, run it inline.

> Full per-endpoint parameter tables, the error catalog, webhooks, and credits live in **[reference.md](reference.md)**. Load it when you need exact `inputs` for a given `model_name`.

## Authentication

- Get an API key from the Developer API dashboard: https://app.fashn.ai/api
- All FASHN calls are server-side: **never hard-code the key or expose it client-side**.
- REST: send `Authorization: Bearer $FASHN_API_KEY`. Both SDKs read `FASHN_API_KEY` from the environment by default.

**Resolve the key (check in order; prompt only if all fail):**

1. `FASHN_API_KEY` env var (preferred, used by integration code, CI, and deploys). Check: `echo "${FASHN_API_KEY:+set}"`.
2. Cache file `~/.fashn/.env`. Load, then re-check: `set -a; [ -f ~/.fashn/.env ] && . ~/.fashn/.env; set +a`.
3. Otherwise, ask the user, then cache it (next bullet).

**Caching (inline use only).** When you had to ask the user for the key, **save it to `~/.fashn/.env` by default** (right after you receive it) so later inline runs don't re-prompt, then tell the user it's cached there and that `rm ~/.fashn/.env` removes it. Only skip if they decline. Run:

```bash
umask 077; mkdir -p ~/.fashn; printf 'FASHN_API_KEY=%s\n' '<key>' > ~/.fashn/.env; chmod 600 ~/.fashn/.env
```

Never echo the key back, write it to a shell profile, or commit it.

**Integrations differ:** pull the key from the *project's* own env (gitignored `.env`) or secret manager, never `~/.fashn/.env` or anywhere in the repo.

## Core concepts (apply to every path)

**One endpoint, many models.** Every request is `{ model_name, inputs }`. Available `model_name`s:

| Category | `model_name` | Required inputs |
|---|---|---|
| Virtual try-on (flagship) | `tryon-max` | `model_image`, `product_image` |
| Virtual try-on (legacy/fast) | `tryon-v1.6` | `model_image`, `garment_image` |
| Product → person wearing it | `product-to-model` | `product_image` |
| Generate a model from a prompt | `model-create` | `prompt` |
| Change a model's identity | `model-swap` | `model_image` |
| Headshot → upper-body avatar | `face-to-model` | `face_image` |
| Freeform edit | `edit` | `image`, `prompt` |
| Change aspect ratio (outpaint/crop) | `reframe` | `image`, `aspect_ratio` |
| Remove background → transparent PNG | `background-remove` | `image` |
| Animate an image → video | `image-to-video` | `image` |

**Prediction lifecycle.** Two ways to get a result:

- **`subscribe` (recommended)**: submit and auto-poll until a terminal state, then return the final result. Both SDKs expose this; for raw REST you implement the poll loop yourself.
- **Manual `run` + `status`**: `run` returns a prediction `id` immediately; poll `status(id)` until `completed`/`failed`. Use this for fire-and-forget, your own queue, or when pairing with **webhooks**.

**Response envelope.** A terminal prediction looks like:

```json
{ "id": "...", "status": "completed", "output": ["https://cdn.fashn.ai/.../output_0.png"], "error": null }
```

- `status`: `starting` → `in_queue` → `processing` → `completed` | `failed` (SDK `subscribe` may also return `canceled` / `time_out`).
- `output`: array of CDN image URLs (or base64 if `return_base64: true`); MP4 URLs for `image-to-video`.
- `error`: `null` on success, else `{ name, message }`.

**Credits.** Spend is returned in the `x-fashn-credits-used` response header (REST) and as `creditsUsed` (TS) / `credits_used` (Python) on the result. **Failed predictions are not charged.** Cost scales with `generation_mode` and `resolution`; see reference.md. Check the balance with `GET /v1/credits`.

**Errors (two kinds):**
- *API errors* (HTTP 4xx/5xx, before the job runs): SDKs throw (`APIError` subclasses); REST returns `{ "error": "<Code>", "message": "..." }`.
- *Runtime errors* (job ran but failed): HTTP 200 with `status: "failed"` and `error: { name, message }`, e.g. `ImageLoadError`, `ContentModerationError`, `PoseError`. Always branch on `status` even when no exception is thrown.

**Limits:** handle `429` responses with backoff when batching.

---

## Path A: TypeScript SDK (`fashn`)

Install into the user's project: `npm install fashn`

```ts
import Fashn from 'fashn';

const client = new Fashn(); // reads FASHN_API_KEY from env

// Recommended: submit + auto-poll to completion
const result = await client.predictions.subscribe({
  model_name: 'tryon-max',
  inputs: {
    model_image: 'https://example.com/person.jpg',
    product_image: 'https://example.com/garment.jpg',
  },
  // optional: pollInterval (ms, default 1000), timeout (ms, default 300000),
  onEnqueued: (id) => console.log('queued', id),
  onQueueUpdate: (s) => console.log('status', s.status),
});

if (result.status === 'completed') {
  console.log(result.output, 'credits:', result.creditsUsed);
} else {
  console.error('failed:', result.status, result.error?.name, result.error?.message);
}
```

Manual lifecycle:

```ts
const { id } = await client.predictions.run({ model_name: 'tryon-max', inputs: { /* ... */ } });
const status = await client.predictions.status(id); // poll until terminal
```

Error handling (API vs runtime):

```ts
try {
  const r = await client.predictions.subscribe({ model_name: 'tryon-max', inputs: { /* ... */ } });
  if (r.status !== 'completed') console.error('runtime error:', r.error?.name, r.error?.message);
} catch (err) {
  if (err instanceof Fashn.APIError) console.error('API error:', err.status, err.message);
  else throw err;
}
```

## Path B: Python SDK (`fashn`)

Install into the user's project: `pip install fashn`

```python
import fashn
from fashn import Fashn

client = Fashn()  # reads FASHN_API_KEY from env

result = client.predictions.subscribe(
    model_name="tryon-max",
    inputs={
        "model_image": "https://example.com/person.jpg",
        "product_image": "https://example.com/garment.jpg",
    },
)

if result.status == "completed":
    print(result.output, "credits:", result.credits_used)
else:
    print("failed:", result.status, result.error)
```

Manual lifecycle: `client.predictions.run(...)` → `client.predictions.status(prediction_id)`.
Async: use `from fashn import AsyncFashn` and `await client.predictions.subscribe(...)`.
API errors raise `fashn.APIError` (`e.status_code`, `e.message`); runtime failures arrive as `result.status == "failed"` with `result.error`.

## Path C: REST (any language)

Base URL `https://api.fashn.ai/v1`. Submit, then poll.

```bash
# Submit → returns {"id": "...", "error": null}
curl -s -X POST https://api.fashn.ai/v1/run \
  -H "Authorization: Bearer $FASHN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model_name":"tryon-max","inputs":{
        "model_image":"https://example.com/person.jpg",
        "product_image":"https://example.com/garment.jpg"}}'

# Poll → repeat until status is "completed" or "failed"
curl -s https://api.fashn.ai/v1/status/<id> -H "Authorization: Bearer $FASHN_API_KEY" -i
#   read x-fashn-credits-used from the response headers

# Balance
curl -s https://api.fashn.ai/v1/credits -H "Authorization: Bearer $FASHN_API_KEY"
```

**Webhooks** (skip polling): append `?webhook_url=` to `/run`. FASHN POSTs the terminal payload (`completed`/`failed`) to that URL, retrying up to 5 times over ~5 min. There's no signature header, so make the handler idempotent and respond 2xx fast. Details in reference.md.

---

## Inline quickstart

For a one-off generation (not an integration), run the TS SDK from `~/.fashn` so you don't touch the user's project:

1. Install if needed: `ls ~/.fashn/node_modules/fashn 2>/dev/null || npm install --prefix ~/.fashn fashn`
2. Resolve the key: `[ -z "$FASHN_API_KEY" ] && { set -a; . ~/.fashn/.env 2>/dev/null; set +a; }`. If still unset, see [Authentication](#authentication).
3. Run it. **Pipe the script via a single-quoted heredoc** so the shell leaves backticks/`$`/quotes alone, and **`cd ~/.fashn`** first so ESM resolves the `fashn` import (it ignores `NODE_PATH`):

```bash
[ -z "$FASHN_API_KEY" ] && { set -a; . ~/.fashn/.env 2>/dev/null; set +a; }
cd ~/.fashn && node --input-type=module <<'NODE'
import Fashn from 'fashn';
const r = await new Fashn().predictions.subscribe({
  model_name: 'tryon-max',
  inputs: {
    model_image: 'https://example.com/person.jpg',
    product_image: 'https://example.com/garment.jpg',
  },
  timeout: 120000, // ms
});
if (r.status !== 'completed') { console.error('Failed:', r.status, r.error); process.exit(1); }
console.log(JSON.stringify({ output: r.output, creditsUsed: r.creditsUsed }, null, 2));
NODE
```

- **Local image inputs**: read the file as base64 (`readFile(path, { encoding: 'base64' })` from `node:fs/promises`) and pass it as `product_image: 'data:image/jpeg;base64,' + b64`. Save a result with `fetch(r.output[0])`.
- Don't write script files or put the key on the command line (use step 2's cache); back off on `429` when batching.

## Reference

See **[reference.md](reference.md)** for every endpoint's full `inputs` (types, allowed values, defaults), the complete error catalog, credit/pricing notes, webhook payloads, and rate limits.

## User's request

$ARGUMENTS
