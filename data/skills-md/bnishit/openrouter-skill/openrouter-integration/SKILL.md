---
name: "openrouter-integration"
description: "Connect apps to 300+ AI models through OpenRouter's OpenAI-compatible API — model discovery, image generation, multimodal chat (text, images, PDFs), exact per-generation cost tracking, provider routing with fallbacks, tool calling with safety limits, structured output validation, free-model filtering, starter templates (Next.js, Express), asset workflows (icons, OG images), production playbooks, and verification scripts. Use when an agent needs to add or debug OpenRouter usage, build a model picker, proxy `/api/v1/models`, `/api/v1/models/user`, `/api/v1/providers`, or `/api/v1/generation`, send image or PDF content to `/api/v1/chat/completions`, generate images through OpenRouter, build icon or OG image flows, parse OpenRouter responses, inspect generation cost after the fact, add Next.js or Express server routes, validate structured outputs, run smoke tests, verify current docs against OpenRouter before coding, or wire model or provider fallbacks into a server or UI."
---

# OpenRouter Integration

Use official OpenRouter docs as the source of truth for current endpoints, parameters, and capability metadata. Prefer `openrouter.ai/docs`, `openrouter.ai/openapi.json`, and the API reference pages under `openrouter.ai/docs/api-reference`.

## Quick Snippets

Use these for fast copy-paste before reaching for the fuller references or templates.

### Curl: list models

```bash
curl -s https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Accept: application/json"
```

### Curl: list providers

```bash
curl -s https://openrouter.ai/api/v1/providers \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Accept: application/json"
```

### Curl: fetch one generation and its cost

```bash
curl -s "https://openrouter.ai/api/v1/generation?id=$GENERATION_ID" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Accept: application/json"
```

### Fetch: free models from the catalog

```ts
const res = await fetch("https://openrouter.ai/api/v1/models", {
  headers: {
    Authorization: `Bearer ${process.env.OPENROUTER_API_KEY}`,
    Accept: "application/json",
  },
});

const json = await res.json();
const freeModels = (json?.data ?? []).filter((model: any) => {
  const pricing = model?.pricing ?? {};
  return ["prompt", "completion", "request", "image"].every((key) => {
    const value = pricing[key];
    return value == null || value === "0";
  });
});
```

### Curl: text-only chat call

```bash
curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -H "HTTP-Referer: ${OPENROUTER_SITE_URL:-http://localhost:3000}" \
  -H "X-OpenRouter-Title: ${OPENROUTER_APP_NAME:-My App}" \
  -d '{
    "model": "openai/gpt-4o-mini",
    "messages": [
      {"role": "user", "content": "Write a one-line summary of invoice OCR."}
    ],
    "temperature": 0
  }'
```

### Fetch: image input

```ts
const res = await fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.OPENROUTER_API_KEY}`,
    "Content-Type": "application/json",
    "HTTP-Referer": process.env.OPENROUTER_SITE_URL || "http://localhost:3000",
    "X-OpenRouter-Title": process.env.OPENROUTER_APP_NAME || "My App",
  },
  body: JSON.stringify({
    model: "google/gemini-2.5-flash",
    messages: [
      {
        role: "user",
        content: [
          { type: "text", text: "Extract all visible text from this image." },
          {
            type: "image_url",
            image_url: { url: imageDataUrl },
          },
        ],
      },
    ],
    temperature: 0,
  }),
});

const json = await res.json();
const content = json?.choices?.[0]?.message?.content;
```

### Fetch: image generation

```ts
const res = await fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.OPENROUTER_API_KEY}`,
    "Content-Type": "application/json",
    "HTTP-Referer": process.env.OPENROUTER_SITE_URL || "http://localhost:3000",
    "X-OpenRouter-Title": process.env.OPENROUTER_APP_NAME || "My App",
  },
  body: JSON.stringify({
    model: "google/gemini-3.1-flash-image-preview",
    messages: [
      {
        role: "user",
        content: "Generate a clean product-style illustration of a glass teacup on a plain background.",
      },
    ],
    modalities: ["image", "text"],
    image_config: { size: "1024x1024" },
  }),
});

const json = await res.json();
const imageUrl = json?.choices?.[0]?.message?.images?.[0]?.image_url?.url;
```

### Fetch: PDF input with file-parser

```ts
const res = await fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.OPENROUTER_API_KEY}`,
    "Content-Type": "application/json",
    "HTTP-Referer": process.env.OPENROUTER_SITE_URL || "http://localhost:3000",
    "X-OpenRouter-Title": process.env.OPENROUTER_APP_NAME || "My App",
  },
  body: JSON.stringify({
    model: "google/gemini-2.5-flash",
    messages: [
      {
        role: "user",
        content: [
          { type: "text", text: "Extract the invoice totals as JSON." },
          {
            type: "file",
            file: {
              filename: "invoice.pdf",
              file_data: pdfDataUrl,
            },
          },
        ],
      },
    ],
    plugins: [
      {
        id: "file-parser",
        pdf: { engine: "pdf-text" },
      },
    ],
    response_format: { type: "json_object" },
    temperature: 0,
  }),
});
```

## Workflow

1. Check the docs before making non-trivial changes.
   - Run `scripts/check_openrouter_docs.py --quick` when accuracy matters or the integration seems stale.
   - If the script flags warnings, read `references/docs-check-workflow.md` and browse only the flagged official pages.
   - Reconcile templates, headers, and parameter usage with the current docs before coding.

2. Keep secrets server-side.
   - Do not expose `OPENROUTER_API_KEY` in browser code.
   - Put a server route in front of OpenRouter for model discovery and chat calls.
   - Set `HTTP-Referer` and `X-OpenRouter-Title` headers when the app has a stable URL and title.
   - Do not forward arbitrary user-supplied `http(s)` asset URLs straight to OpenRouter. Fetch trusted assets server-side and convert them to `data:` URLs, or enforce an explicit host allowlist such as `OPENROUTER_ALLOWED_REMOTE_ASSET_HOSTS`.

3. Install a starter instead of retyping boilerplate.
   - Use `scripts/install_template.sh` with `--template nextjs` or `--template express`.
   - Override base path and env var names at install time when the target project already has conventions.
   - Copy shared helpers, streaming UI example, and test fixtures with the template.

4. Decide what you are integrating.
   - Catalog, providers, free-model filters, or generation cost lookup: read `references/catalogs-and-costs.md`.
   - Model catalog or picker: read `references/models-and-ui.md`.
   - Model selection, provider filters, or fallback policy that should be production-friendly: read `references/catalog-routing-best-practices.md`.
   - Text, image analysis, image generation, or PDF inference: read `references/requests-and-responses.md`.
   - End-to-end image asset workflows such as icons, OG images, preview, and storage: read `references/image-generation-best-practices.md`.
   - Tool calling or an agentic loop: read `references/tools-and-function-calling.md`.
   - Tool reliability or structured-output extraction that should survive production use: read `references/tool-calling-and-structured-output-best-practices.md`.
   - Routing and failover policy: read `references/routing-and-fallbacks.md`.
   - Logging, generation audit, and cost observability: read `references/operations-and-observability-best-practices.md`.
   - Common failures: read `references/troubleshooting.md`.

5. Discover models before choosing one.
   - Use `GET /api/v1/models` for the full catalog.
   - Use `GET /api/v1/models/user` when user or provider preferences matter.
   - Use `GET /api/v1/providers` when provider routing, privacy, or availability matter in the UI.
   - Use `GET /api/v1/models/:author/:slug/endpoints` when you need endpoint-level provider data.
   - Derive free-model lists by filtering zero-priced entries from the model catalog.
   - Store model `id`, not model `name`.
   - Filter by `architecture.input_modalities` and `architecture.output_modalities` first; use name heuristics only as fallback.

6. Build requests in OpenAI-compatible format.
   - Send text-only prompts as normal chat `messages`.
   - Send images with `content` arrays containing a `text` part and one or more `image_url` parts.
   - Generate images by sending normal chat `messages` plus `modalities` that include `image`; pass `image_config` when output settings matter.
   - Choose image-output models from the live catalog by checking `architecture.output_modalities` for `image`.
   - Send PDFs with a `file` content part and, when needed, the `file-parser` plugin.
   - Default to `data:` URLs for private uploads and for any untrusted remote asset. Use remote `http(s)` URLs only from explicit allowlisted hosts that you control or trust.
   - Keep `tools` in every tool-calling request, including follow-up calls that only send tool results.

7. Choose response handling deliberately.
   - For plain prose, read `choices[0].message.content`.
   - For image generation, read `choices[0].message.images`.
   - For structured data, prefer `response_format: { type: "json_schema", ... }` when the model supports `structured_outputs`.
   - Fall back to `response_format: { type: "json_object" }` when you need JSON but not full schema enforcement.
   - Use `assets/shared/parse-openrouter-response.ts` for robust text, generated-image, and tool-call extraction.
   - Use `assets/shared/stream-openrouter-sse.ts` for streaming.
   - Use `assets/shared/validate-structured-output.ts` with `zod` for type-safe parsing.
   - Use `assets/nextjs-template/components/openrouter-streaming-chat.tsx` as the end-to-end streaming UI example.

8. Reuse parsed PDFs when iterating.
   - If a PDF request returns assistant `annotations`, pass them back on follow-up requests to avoid reparsing cost and latency.
   - Preserve the original file message and append the annotated assistant message before the next user turn.

9. Verify the integration.
   - Run `assets/tests/smoke-curl.sh` for text, structured JSON, tools, image analysis, image generation, and PDF cases.
   - Run `assets/tests/smoke-catalogs.sh` for models, user models, providers, free-model filtering, image-output model discovery, and generation cost lookup.
   - Check both successful responses and non-2xx OpenRouter errors.
   - Log returned `usage`, `cost`, finish reason, resolved model id, and generation id for debugging.
   - Fetch `GET /api/v1/generation?id=...` when exact post-hoc cost or token accounting matters.

## Resources

- Docs-check script: `scripts/check_openrouter_docs.py`
- Installer script: `scripts/install_template.sh`
- Next.js starter: `assets/nextjs-template/`
- Express starter: `assets/express-template/`
- Shared TypeScript helpers: `assets/shared/`
- Smoke tests and fixtures: `assets/tests/`
- Catalog and cost helper: `assets/shared/openrouter-catalog-and-cost.ts`
- Image asset helper: `assets/shared/openrouter-generated-image-assets.ts`
- Node image persistence helper: `assets/shared/openrouter-generated-image-assets-node.ts`
- Catalogs, providers, free-model filters, and generation cost lookup: `references/catalogs-and-costs.md`
- Catalog and routing production rules: `references/catalog-routing-best-practices.md`
- Image generation usage, preview, storage, icons, and OG workflows: `references/image-generation-best-practices.md`
- Tool calling and structured-output production rules: `references/tool-calling-and-structured-output-best-practices.md`
- Operations, logging, and generation audit rules: `references/operations-and-observability-best-practices.md`

## Quality Rules

- Prefer a server proxy with caching for model lists.
- Keep model picker UIs searchable; plain `<select>` breaks down on large catalogs.
- Use `architecture.input_modalities` and `architecture.output_modalities` as the primary capability signals.
- Treat pricing fields as strings from the API; convert explicitly if you need numeric math.
- Persist generation ids anywhere later cost inspection matters.
- Prefer exact generation lookup over estimated UI-only price math when a completed request id exists.
- Include the organization prefix in model ids such as `openai/gpt-4o-mini`.
- Expect `choices` to always be an array.
- For streaming, expect SSE comment lines and ignore them.
- For PDFs, choose `pdf-text` for clean text PDFs, `mistral-ocr` for scanned or image-heavy PDFs, and `native` only when the selected model supports file input natively.
- Do not assume every model supports `response_format`, `structured_outputs`, `tools`, or every OpenAI parameter; check `supported_parameters` first.
- When a request depends on specific parameters such as tools or `response_format`, prefer `provider.require_parameters: true`.

## References

- Model discovery, caching, and picker UX: `references/models-and-ui.md`
- Catalogs, providers, free-model filters, and generation cost lookup: `references/catalogs-and-costs.md`
- Catalog and routing production rules: `references/catalog-routing-best-practices.md`
- Image generation usage, preview, storage, icons, and OG workflows: `references/image-generation-best-practices.md`
- Text, image analysis, image generation, and PDF request patterns plus response handling: `references/requests-and-responses.md`
- Tool calling and agentic loops: `references/tools-and-function-calling.md`
- Tool calling and structured-output production rules: `references/tool-calling-and-structured-output-best-practices.md`
- Model routing, provider routing, and fallbacks: `references/routing-and-fallbacks.md`
- Operations, logging, and generation audit rules: `references/operations-and-observability-best-practices.md`
- Troubleshooting and failure diagnosis: `references/troubleshooting.md`
- Docs-check workflow: `references/docs-check-workflow.md`
