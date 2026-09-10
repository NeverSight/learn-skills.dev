---
name: hiapi-gpt-image-2-5
description: Use only for HiAPI GPT Image 2.5 image generation and editing with the exact model IDs gpt-image-2.5-flare or gpt-image-2.5-sunburst. Covers text-to-image, image-to-image, schema validation, dry-run estimates, idempotent async creation, polling, resume, and output download. Do not invoke for GPT Image 2, other GPT Image versions, or unrelated image models.
---

# HiAPI GPT Image 2.5

This released 0.1.0 skill wraps HiAPI's unified async image API for exactly two model IDs:

- `gpt-image-2.5-flare` — the default when no model is selected.
- `gpt-image-2.5-sunburst` — use only when the caller explicitly selects it.

Both IDs expose the same public input contract: one required prompt, optional public reference URLs, an aspect ratio or supported pixel size, quality, background, and output format. Each accepted task produces one image. Do not infer a quality, speed, or visual advantage between Flare and Sunburst from their names.

## Required sequence

1. Decide whether the request is text-to-image (omit `image_urls`) or image-to-image/editing (send 1–16 accessible HTTP(S) URLs). A local file path is not accepted by this CLI; serve it from an accessible URL or use the direct API with an accessible URL.
2. Validate the prompt and options locally. Run `--dry-run --estimate` before a paid create. The estimate reads the current `/api/pricing` snapshot and creates no task.
3. Submit once with a stable `--idempotency-key`. The CLI prints the key and task ID to stderr immediately after acceptance. If acceptance is ambiguous, reuse the same key; never blind-retry with a new key.
4. Use the default wait, or `--no-wait` to return after submission. Use `--resume-task-id` to poll/download an existing task without creating another task. Use `--no-save` when you only need the output URL.
5. Keep the downloaded image through technical and creative checks. Treat temporary output URLs as expiring.

Read [references/api.md](references/api.md) for the field contract, [references/workflow.md](references/workflow.md) for delivery and QC, and [references/output.md](references/output.md) for response handling and recovery.

## Safety boundary

`--dry-run`, `--estimate`, and local validation are non-billing. Creating a task may spend account balance. This package does not claim a paid generation or client runtime acceptance. Callbacks and HiAPI persistent storage are not implemented as CLI flags in this package; use the direct API snippets in the references when those features are enabled for the account.
