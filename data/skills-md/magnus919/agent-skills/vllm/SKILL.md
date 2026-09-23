---
name: vllm
description: >-
  Operate, configure, benchmark, and troubleshoot vLLM inference servers: Docker
  and Kubernetes deployment, quantization-aware model configuration (tensor
  parallelism, KV cache), OpenAI-compatible API serving, throughput and latency
  benchmarking, continuous batching tuning, GPU operation, and upgrade/rollback.
  Use when deploying or running a vLLM server (vllm serve, vllm/vllm-openai),
  sizing a model and its KV cache for GPUs, selecting quantization and
  parallelism, serving via /v1 endpoints, measuring serving throughput or
  latency, tuning batching, or diagnosing GPU, OOM, or startup failures in a
  vLLM deployment. Do not use for model training, fine-tuning, evaluation-set
  design, or engine-selection methodology (that is ml-engineering), or for
  operating the llama.cpp stack with GGUF models (that is llama-cpp); other
  inference engines (TGI, Ollama, Triton) are out of scope.
license: MIT
compatibility: >-
  Requires a vLLM release (v0.26.0 or a pinned older release), an NVIDIA CUDA,
  AMD ROCm, or Intel XPU GPU with the matching driver, or a supported CPU build.
  The bundled vllm-health script runs on Python 3.9+ and needs no vLLM server
  for --help; live probes require HTTP(S) access to a running vLLM server.
metadata:
  source: https://docs.vllm.ai/en/latest/
  source_index: references/00-source-index.md
  research_checked: "2026-08-03"
---

# vLLM Inference Serving

Use this skill to operate **vLLM** as a production inference server: deploy it with Docker or Kubernetes, configure the model and engine (quantization, tensor parallelism, KV cache, context length), serve the OpenAI-compatible API surface, benchmark throughput and latency with comparable evidence, tune continuous batching, operate the GPUs underneath, and upgrade or roll back safely. This is a **tool skill** for one named engine. Serving *methodology* — engine selection, quantization trade-offs, deployment plans, regression triage — belongs to [ml-engineering](../ml-engineering/SKILL.md); local single-node GGUF serving with the llama.cpp stack belongs to [llama-cpp](../llama-cpp/SKILL.md). This skill owns the day-to-day operation of vLLM itself.

## Operating contract

1. **Record the deployment before tuning it.** Capture the vLLM version or image digest, model and revision, quantization, parallelism, `max-model-len`, KV cache settings, batching limits, GPU inventory, and workload. The [serving config template](templates/serving-config.md) exists for exactly this.
2. **Confirm the target, scope, and rollback path before acting.** Read-only discovery (health probes, `/metrics`, `nvidia-smi`) may proceed without confirmation. Mutations — restarting a server, changing serving args, scaling replicas, upgrading the image — require an explicit human directive naming the deployment.
3. **A server that responds is not a server that serves.** `/health` returning 200 proves liveness, not that the model loaded or that inference works. Verify at the delivery boundary: `/v1/models` reports the served model and a representative request returns generated tokens.
4. **Benchmark before and after every change.** vLLM flags, defaults, and behavior change between releases; an unmeasured tuning change is a guess. Compare only matched conditions (version, model, GPU, context, batch, workload) and record the evidence in the [benchmark run record](templates/benchmark-run-record.md).
5. **Keep evidence bounded.** Summarize logs, configs, and metrics; never dump full server logs, `.env` files, or HF tokens into chat. `--enable-log-requests` with debug logging can leak prompt content; keep request logging off or redacted in shared sessions.

## The vllm-health script

`scripts/vllm-health` is an agent-first, read-only probe for a running vLLM server. It issues GET requests only, never mutates, and emits bounded JSON.

```bash
scripts/vllm-health --help                    # no server needed
scripts/vllm-health --url http://127.0.0.1:8000 --json
scripts/vllm-health --check health --check models --json
scripts/vllm-health --check metrics --timeout 10 --json
```

Exit codes: 0 all checks passed, 1 issues found or a fatal error, 2 usage error, 124 timeout. Checks: `health` (`/health`), `version` (`/version`), `models` (`/v1/models`), `load` (`/load`), and `metrics` (a bounded prefix of `/metrics`). The script never sends data anywhere and never writes files.

## Operating loop

1. **Identify the deployment**: vLLM version or image digest, model and revision, served model name, parallelism, and how it is deployed (bare `vllm serve`, Docker, Kubernetes).
2. **Collect evidence**: run `vllm-health --json` for health, version, models, and load; check `/metrics` counters (`vllm:num_requests_running`, `vllm:num_requests_waiting`, `vllm:gpu_cache_usage_perc`); inspect GPU state with `nvidia-smi`.
3. **Triage against the symptom**: map the problem to the evidence (OOM → KV cache or `gpu_memory_utilization`; high latency → batching, TTFT vs TPOT; model not found → served name or chat template; slow start → model download or compile cache).
4. **Act with confirmation**: bounded, scoped changes after a human directive, with a rollback path named first.
5. **Verify**: re-run the probe and the representative request at the delivery boundary, and re-benchmark if the change affects performance.

## Deployment: Docker and Kubernetes

- **Docker**: the official image is `vllm/vllm-openai` (Docker Hub). Run with GPU access, the Hugging Face cache mounted, the HF token for gated models, port 8000 published, and `--ipc=host` (or a `--shm-size`) for the shared memory tensor parallelism relies on. See [references/01-deployment.md](references/01-deployment.md).
- **Kubernetes**: a Deployment with `nvidia.com/gpu` (or `amd.com/gpu`) resources, a PVC for the model cache, an `emptyDir` backed by Memory at `/dev/shm`, liveness/readiness probes on `/health` port 8000, and a Service. Raise probe `failureThreshold` for large models that take minutes to load — a premature kill shows up as `KeyboardInterrupt: terminated` in the container log.
- Pin image tags to a release (for example `vllm/vllm-openai:v0.26.0`) instead of `latest`, and persist the compile cache (default `~/.cache/vllm`) across restarts so `torch.compile` artifacts are reused.

## Model configuration

- **Model identity**: `--model` is the HF repo or local path; `--revision` pins the exact weights. `--served-model-name` sets the name clients must use in `/v1` requests and in the `model` field of responses. `--trust-remote-code` is required for some model repos and should be reviewed before use.
- **Context length**: `--max-model-len` bounds prompt plus output per request. Unset, it derives from the model config; `-1`/`auto` picks the largest length that fits GPU memory. It is the single biggest driver of KV cache size.
- **Quantization-aware serving**: pass `--quantization` (or `-q`) only when the model weights require it (GPTQ/AWQ/GGUF checkpoints load their scheme from config). Weight types and activation dtypes must match what the kernels support; a quantized model served at the wrong dtype fails to load or silently degrades. Hardware support varies by method (see [references/02-model-configuration.md](references/02-model-configuration.md)).
- **Tensor parallelism**: `--tensor-parallel-size N` shards one model across N GPUs in the same node; `--pipeline-parallel-size` splits layers across nodes. TP requires NVLink/fast interconnect and equal per-GPU memory; startup logs the memory profiling result, which is the evidence that the model fits.
- **KV cache**: `--gpu-memory-utilization` (default 0.92) caps the fraction of GPU memory the model plus KV cache may use. `--kv-cache-dtype fp8` shrinks the cache for long contexts on supported GPUs. The engine logs `GPU KV cache size: N tokens` and the implied max concurrency — record both; they tell you how many concurrent requests of a given length the box can hold.

## OpenAI-compatible API surface

- Basic endpoints: `/health` (liveness), `/version`, `/v1/models` (served models), `/load` (load metrics), `/metrics` (Prometheus). Inference: `/v1/completions` and `/v1/chat/completions` (chat requires the model to ship a chat template, or pass `--chat-template`); `/v1/embeddings` for pooling models; `/v1/responses` for the Responses API.
- Streaming, tool calling (`--enable-auto-tool-choice --tool-call-parser openai`), structured outputs, and parallel sampling are server-side options that change request/response behavior — verify each against the installed release rather than assuming parity.
- Exposing the server beyond loopback requires an explicit decision about bind address, API keys, TLS or a trusted reverse proxy, and firewall rules. Development-only endpoints (`/reset_prefix_cache`, weight transfer, profiling) must not be exposed in production.

## Benchmarking: throughput and latency

- **Online serving benchmark**: run `vllm bench serve` against a live server with a representative dataset (ShareGPT, a local `custom` JSONL, or your own prompts) and fixed `--num-prompts`, `--request-rate`, and `--max-concurrency`. It reports request throughput (req/s), output token throughput (tok/s), total token throughput, and TTFT/TPOT/ITL percentiles.
- **Offline throughput**: `vllm bench throughput` measures raw engine throughput without the HTTP path; use it for engine-only comparisons, not end-to-end user latency.
- **Comparable evidence**: the benchmark run record template freezes version, model, quantization, parallelism, context, batching, GPU, dataset, and load pattern. Never compare numbers across different conditions as if one variable changed. TTFT is a latency metric; token throughput is a throughput metric — an optimization that helps one can hurt the other.
- For production capacity testing, vLLM's docs recommend the separate GuideLLM framework; this skill's scope is the bundled `vllm bench` tools.

## Continuous batching tuning

- vLLM batches continuously by default: the scheduler admits sequences as capacity frees up, mixing prefill and decode. `--max-num-seqs` caps sequences per iteration, `--max-num-batched-tokens` caps tokens per iteration, and `--enable-chunked-prefill` lets prefill share an iteration with decode.
- Start from defaults and change one knob at a time against the frozen benchmark: raising `--max-num-seqs` raises throughput at the cost of per-request latency and KV cache pressure; lowering it improves latency stability at the cost of utilization.
- `--enable-prefix-caching` reuses KV blocks across requests with shared prefixes (chat system prompts, RAG contexts); the hit rate is visible in `/metrics` and in the benchmark's input token accounting. `--performance-mode` trades between `interactivity` (latency) and `throughput` at the kernel level.

## GPU operation

- Verify GPUs with `nvidia-smi` (or `rocm-smi` on AMD): device list, memory, utilization, temperature, and ECC errors before and after changes. `CUDA_VISIBLE_DEVICES` selects which GPUs a `vllm serve` process sees; tensor parallel ranks map to the visible devices in order.
- Watch `/metrics` for `vllm:gpu_cache_usage_perc` (KV cache pressure), `vllm:num_requests_running`/`waiting`, and `vllm:generation_tokens_total`. A cache-usage signal near 1.0 with requests waiting means the deployment is at capacity — scale out or reduce `max-model-len`/concurrency rather than overcommitting.
- OOM during startup usually means the model + KV cache did not fit: lower `--gpu-memory-utilization` does not help if weights alone exceed memory — reduce `--max-model-len`, switch quantization, or add GPUs. OOM mid-run means KV cache pressure: shrink context, concurrency, or batch limits.

## Upgrade and rollback

- **Pin everything**: image tag or `pip install vllm==<version>`, model revision, and the full serving command. `latest` images and unpinned revisions make rollback impossible and upgrades unreproducible.
- **Upgrade path**: read the release notes for the full version span, review changed/removed flags (`--engine-args` change frequently), validate the new version on a scratch instance with the real model and workload, re-run the frozen benchmark, then swap with a rollback plan: previous image tag and previous serving config ready to reapply.
- **Rollback**: because the config is versioned, rollback is a redeploy of the previous pinned image + config. KV cache layout, defaults, and flag names change between releases — do not assume a config that ran on v0.25.x behaves identically on v0.26.x without re-validating and re-benchmarking.

## Reference routing

| Load when | Reference |
|---|---|
| Sources, version observations, refresh procedure | `references/00-source-index.md` |
| Docker and Kubernetes deployment, image pinning, probes, storage | `references/01-deployment.md` |
| Model config: quantization, tensor parallelism, KV cache, memory budgeting | `references/02-model-configuration.md` |
| OpenAI-compatible API surface, chat templates, tools, auth | `references/03-openai-api.md` |
| Benchmarking methodology and `vllm bench` commands | `references/04-benchmarking.md` |
| Continuous batching, chunked prefill, prefix caching, performance mode | `references/05-batching-and-tuning.md` |
| GPU operation, observability, upgrade/rollback, troubleshooting | `references/06-gpu-ops-and-lifecycle.md` |

## Included artifacts

- `scripts/vllm-health`: read-only health/version/models/load/metrics probe (stdlib-only, `--json`, `--check` subsets, `--help` without a server).
- `tests/test_vllm_health.py`: deterministic tests against a local stub HTTP server, including the read-only contract.
- `templates/serving-config.md` and `templates/benchmark-run-record.md`: fillable records that make deployments reproducible and benchmark evidence comparable.
- `references/`: seven dated, source-indexed references covering the operational topics above.
- `evals/evals.json`: six output-quality evaluation cases for agent runs.

## Verification boundary

| Claim | Minimum evidence |
|---|---|
| The server is alive | `vllm-health --check health` reports `/health` 200 |
| The right model is served | `/v1/models` lists the expected served model name |
| Inference works | A representative `/v1/chat/completions` or `/v1/completions` request returns generated tokens with a `finish_reason` |
| The model fits | Startup log shows memory profiling completed and `GPU KV cache size: N tokens` for the configured parallelism |
| A tuning change helped | The frozen benchmark shows the declared metric improving with matched conditions, variance reported |
| The deployment is upgradable | Previous pinned image + serving config are recorded and the upgrade was rehearsed on a scratch instance |
| A diagnosis is sound | Evidence was collected before the claim, and the fix was verified by re-running the probe and the benchmark |

## Hard boundaries

- Never restart, redeploy, scale, or upgrade a vLLM deployment without an explicit human directive naming the target and a stated rollback path. Read-only discovery may proceed freely.
- Never expose an unauthenticated server beyond loopback by accident; development-only endpoints and profiling routes must stay off production ingress.
- Never print or commit HF tokens, `.env` contents, or full server logs; summarize evidence instead.
- Never compare benchmark numbers from different versions, models, quants, parallelism, contexts, batches, or workloads as if one variable changed.
- Never run `vllm-health` as anything but what it is — read-only. It has no mutation surface.

## When not to use

- **Model training, fine-tuning, evaluation-set design, quantization decisions, and serving methodology** — that is [ml-engineering](../ml-engineering/SKILL.md).
- **The llama.cpp stack** (llama-cli, llama-server, GGUF conversion and quantization, local Metal/CUDA builds) — that is [llama-cpp](../llama-cpp/SKILL.md).
- **Other inference engines** (TGI, Ollama, Triton, vLLM's embedding/rerank-only workloads are in scope, but engine selection among them is not) — engine-selection trade-offs belong to `ml-engineering`.
- **Kubernetes and Docker fundamentals** (manifests, RBAC, image registries, GPU device plugins) — that is [kubernetes](../kubernetes/SKILL.md) and [docker-compose](../docker-compose/SKILL.md).
- **GPU infrastructure provisioning** (drivers, cluster scheduling, capacity planning) — that is [platform-engineering](../platform-engineering/SKILL.md); this skill operates the GPUs a vLLM server already targets.
