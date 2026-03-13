---
name: modal-batch-processing
description: >-
  Use this skill for Modal job orchestration with `.map`, `.starmap`, `.spawn`,
  `.spawn_map`, or `@modal.batched`. Trigger when the user needs to fan out
  work across Modal containers, collect results in-process, return a pollable
  job ID from a web server, cap concurrency, recover from partial failures, or
  batch many small requests into fewer GPU calls. Do not use it for vLLM or
  SGLang serving, model fine-tuning, or sandbox lifecycle questions.
license: MIT
---

# Modal Batch Processing

## Quick Start

1. Verify the actual local Modal environment before writing code.

```bash
modal --version
python -c "import modal,sys; print(modal.__version__); print(sys.executable)"
modal profile current
```

- Do not assume the default `python` interpreter matches the environment behind the `modal` CLI.
- Switch to the project virtualenv or the interpreter behind the installed `modal` CLI before writing examples or running scripts.
- Use `with modal.enable_output():` around `with app.run():` when local provisioning logs or remote prints are needed for debugging.

2. Classify the request before writing code.

- Caller waits and needs the results back in the same process: use `.map` or `.starmap`.
- Caller should return immediately and poll later: use `.spawn`.
- Detached fan-out writes results somewhere durable: use `.spawn_map`.
- Many small homogeneous requests should share one execution: use `@modal.batched`.

3. Read exactly one primary reference before drafting code.

- `.map` or `.starmap`: [references/map-and-gather.md](references/map-and-gather.md)
- `.spawn` or `.spawn_map`: [references/job-queues-and-detached-runs.md](references/job-queues-and-detached-runs.md)
- `@modal.batched`: [references/dynamic-batching.md](references/dynamic-batching.md)

## Choose the Workflow

- Use `.map` or `.starmap` when the caller can wait for the full fan-out to finish and the results must come back to the same local process. Read [references/map-and-gather.md](references/map-and-gather.md).
- Use `.spawn` when the caller should return immediately and keep a stable `FunctionCall` handle or job ID for later polling and collection. Deploy the function first if another service submits the work. Read [references/job-queues-and-detached-runs.md](references/job-queues-and-detached-runs.md).
- Use `.spawn_map` only when each detached task writes its own durable output to a Volume, CloudBucketMount, database, or another external sink. Do not choose it when the caller expects programmatic result retrieval later. Read [references/job-queues-and-detached-runs.md](references/job-queues-and-detached-runs.md).
- Use `@modal.batched` when many individual requests can be coalesced into fewer container or GPU executions. Keep the function contract list-in and list-out. Read [references/dynamic-batching.md](references/dynamic-batching.md).

## Default Rules

- Start with plain `@app.function` functions for stateless work. Move to `@app.cls` only when the container must reuse loaded state or expensive initialization.
- Keep orchestration local with `@app.local_entrypoint` or a plain Python script plus `with app.run():` when the entire workflow can stay within one session.
- Deploy with `modal deploy` and use `modal.Function.from_name(...)` when another service must submit jobs or look up a stable remote function later.
- Set `timeout=` intentionally on remote work. Add `retries=` only when the work is idempotent and safe to re-run.
- Set `max_containers=` when upstream systems, GPU quotas, or external APIs need a hard concurrency cap.
- Persist outputs externally whenever detached work may outlive the caller or when using `.spawn_map`.
- Use Volumes or CloudBucketMounts for durable caches, model weights, and shared intermediates; do not rely on ephemeral container disk.
- Prefer `.map` or `.starmap` over `.spawn` when the caller genuinely needs results immediately and no durable job handle is required.
- Prefer `.spawn` over `.map` when the caller needs a stable job ID or should return before the remote work finishes.
- Treat `.spawn_map()` as detached fire-and-forget in Modal 1.3.4. The installed SDK docstring says programmatic result retrieval is not supported, so only use it when each task writes its output elsewhere.
- If the task is really about OpenAI-compatible vLLM or SGLang serving, stop and use `modal-llm-serving`.
- If the task is really about training model weights, stop and use `modal-finetuning`.
- If the task is really about isolated interactive execution, tunnels, or sandbox restore flows, stop and use `modal-sandbox`.

## Validate

- Run `npx skills add . --list` after editing the package metadata or skill descriptions.
- Keep `evals/evals.json` and `evals/trigger-evals.json` aligned with the actual workflow boundary of the skill.
- Run [scripts/smoke_test.py](scripts/smoke_test.py) with a Python interpreter that can import `modal` when changing the workflow guidance or runnable artifact.

## References

- Read [references/map-and-gather.md](references/map-and-gather.md) for synchronous fan-out and in-process result collection.
- Read [references/job-queues-and-detached-runs.md](references/job-queues-and-detached-runs.md) for deployed job queues, job IDs, detached runs, and external result sinks.
- Read [references/dynamic-batching.md](references/dynamic-batching.md) for `@modal.batched` contracts and tuning.
