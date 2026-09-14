---
name: qwen-image-edit
description: Prepare and run the pinned Qwen Image Edit consistency workflow through local ComfyUI with one or two reference images, an exact edit prompt, deterministic workflow copies, dependency preflight, monitoring, and result retrieval. Use only when the user explicitly invokes `$qwen-image-edit` or `$qwen-image-edit help`; never invoke this skill implicitly for ordinary image-editing requests.
---

# Qwen Image Edit

Run the bundled Qwen consistency-edit workflow without silently changing its graph, models, or prompt.

## Route the invocation

- For `$qwen-image-edit help`, read and show [the installation guide](references/comfyui-workflow-install.md). Do not connect to or modify ComfyUI.
- Otherwise, read [the runtime procedure](references/runtime.md) and follow it in order.
- On any preparation or run failure, include the installation-guide link. For a missing node, model, connection, or validation dependency, also show the relevant guide section and smallest corrective action.

## Interpret controls

Remove the single `$qwen-image-edit` invocation that routed the request; it is not prompt content. Then recognize these case-insensitive control tokens and strip only these tokens before using the edit prompt:

For every `<boolean>` below, accept `true`, `on`, `yes`, or `1` as true and `false`, `off`, `no`, or `0` as false.

- `[return=<boolean>]`; default true.
- `[load_workflow=<boolean>]`; default false.
- `[preview=<boolean>]`; default true and effective only when workflow loading resolves to true.
- `[prompt_enhance=<boolean>]` or `[pe=<boolean>]`; default false.

Match every boolean flag name and value case-insensitively. If the same flag appears more than once, use its last occurrence. Treat any other value as invalid control syntax and stop before workflow preparation.

Treat the remaining user text as the prompt payload. Unless enhancement resolves to true, copy that payload directly to the workflow prompt input with the same characters, order, whitespace, line breaks, punctuation, spelling, capitalization, and language. Do not reason about, summarize, rewrite, expand, translate, correct, sanitize, classify, filter, moderate, or add preservation language to it. Do not ask for prompt-wording clarification. The workflow performs its own prompt enhancement and filtering.

When enhancement is enabled, improve the payload once for clarity and Qwen editability without adding a new subject, edit, or intent, then use that result as the workflow prompt. Never modify the template's system instruction. Do not run a separate skill-level safety filter in either path; higher-level system and tool policies still apply.

## Enforce media limits

Use one or two images in attachment order. With one image, remove the second-image connection through the preparer. With more than two, ask the user to select two; never discard attachments silently.

## Preserve execution integrity

- Upload local images through ComfyUI and patch only the returned remote filenames.
- Resolve the exact checkpoint and LoRA conservatively; never download, install, or restart without explicit permission.
- Run `scripts/prepare_workflow.py`; do not edit the JSON by ad-hoc string replacement.
- Validate before enqueueing. Enqueue exactly once and bind monitoring, diagnosis, and result retrieval to its exact `prompt_id`.
- Retain both prepared API and UI workflows with the result.
- Treat a workflow-side rejection as a content-filter result, not an environment failure; do not bypass or disable the workflow filter.
