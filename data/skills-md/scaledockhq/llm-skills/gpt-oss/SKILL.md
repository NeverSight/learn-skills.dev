---
name: gpt-oss
description: Serve and configure OpenAI gpt-oss-120b and gpt-oss-20b (and gpt-oss-safeguard, NVIDIA gpt-oss-puzzle-88B) with the harmony format, reasoning_effort, MXFP4 weights, vLLM/SGLang/llama.cpp/Ollama/TensorRT-LLM parsers and quants per platform. Use when running gpt-oss on DGX Spark, RTX, Apple Silicon or H100/B200, choosing a quant, or fixing harmony errors, empty content, lost reasoning in tool loops, HarmonyError vocab downloads or analysis/final text leaking into replies. Not for choosing an engine (self-hosted-llms, local-llms).
license: MIT
compatibility: Any shell with curl and jq; engines run on Linux NVIDIA, Apple Silicon or AMD hosts. Installs, downloads and service restarts need the user's approval.
metadata:
  author: ScaleDockHQ
  version: "0.1.0"
---

# gpt-oss

Get OpenAI's open-weight gpt-oss models serving correctly: right weights, right parser flags, right reasoning
setting, right sampling, and a request that returns separate reasoning and answer text.

**Scope:** this model family: chat templates, tool and reasoning parsers per engine, recommended quants per platform, context limits, licenses and known bugs.
Out of scope: engine installs and stack wiring (`self-hosted-llms`, `local-llms`, `cloud-llms`), producing quants
(`model-quantization`), training (`fine-tuning-llms`).

Work through the steps in order. Load a reference only when a step names it.

## Discover first

Inspect the live system before changing anything. Every command is read-only and never prints secrets.

```bash
# Hardware and memory
uname -sm; nvidia-smi --query-gpu=name,compute_cap,memory.total --format=csv,noheader 2>/dev/null
sysctl -n hw.memsize 2>/dev/null; free -h 2>/dev/null

# Engines and versions already present
for t in vllm sglang llama-server ollama trtllm-serve mlx_lm.server; do command -v "$t" >/dev/null && echo "$t: $("$t" --version 2>&1 | head -1)"; done
docker ps --format '{{.Names}}\t{{.Image}}\t{{.Ports}}' 2>/dev/null | grep -Ei 'vllm|sglang|llama|ollama|tensorrt'

# A gpt-oss endpoint that is already up (default ports; adjust)
for p in 8000 8080 11434; do curl -s -m 3 "http://127.0.0.1:$p/v1/models" | jq -r '.data[]?.id' 2>/dev/null | grep -i oss; done
curl -s -m 3 http://127.0.0.1:11434/api/show -d '{"model":"gpt-oss"}' | jq '.thinking' 2>/dev/null

# Weights already downloaded
ls ~/.cache/huggingface/hub 2>/dev/null | grep -Ei 'gpt-oss|gpt_oss'
```

## Decision flow

1. Pick the size: 20b (3.6B active, 16 GB class) for latency or small machines; 120b (5.1B active, one 80 GB GPU,
   or DGX Spark / 96 GB+ Mac) for quality. `references/models.md`.
2. Use the official MXFP4 weights or an MXFP4 GGUF or MLX conversion. Do not quantize further without a quality gate
   (`llm-evals`). `references/platforms-and-quants.md`.
3. Pick the engine from the platform: Spark -> NVIDIA's vLLM image, Ollama or llama.cpp; RTX/Mac -> llama.cpp, Ollama
   or MLX; H100/B200 -> vLLM, SGLang or TensorRT-LLM. TensorFold has no gpt-oss qualification; do not plan on it.
4. Set the parsers and reasoning flags from `references/parsers-and-templates.md`.
5. If anything misbehaves, match the symptom in `references/known-issues.md` before tuning.

## Rules

- **Ask before changing the system.** Installs, services, firewall rules and exposure need approval and an undo path.
- **Secrets never touch output.** Keys live in `0600` files or environment variables; `HF_TOKEN` and `EXA_API_KEY`
  come from the environment.
- **Verify upstream.** Versions, flags and defaults come from upstream docs read on the writing date.
- **harmony only.** The model does not work without its response format. Use the engine's chat endpoint with the
  repo or GGUF template, never a generic ChatML wrapper.
- **Never show raw chain of thought to end users.** Return it to developers in `reasoning`, not to customers.
- **Do not use the demo Python tool on a shared host.** `PYTHON_EXECUTION_BACKEND=dangerously_use_uv` (vLLM) and
  `PYTHON_EXECUTION_BACKEND=UV` (SGLang) run model-generated code on the host.
- **Measure.** Benchmark before and after each flag change (`bench.sh` in `self-hosted-llms`).

## Serving the family

- [ ] Confirm the platform and memory against the table in `references/platforms-and-quants.md`.
- [ ] Launch with the official weights and the parser flags: vLLM `--reasoning-parser openai_gptoss`,
      `--tool-call-parser openai --enable-auto-tool-choice`; SGLang `--reasoning-parser gpt-oss --tool-call-parser gpt-oss`;
      llama.cpp `--jinja`; Ollama and TensorRT-LLM handle harmony internally. `references/parsers-and-templates.md`.
- [ ] Set sampling to `temperature=1.0`, `top_p=1.0`, no repetition penalty. On llama.cpp set them explicitly,
      because its defaults (`top-k 40`, `min-p 0.1`) differ.
- [ ] Choose the reasoning level (`low`, `medium` default, `high`) per request or per alias; budget `max_tokens` for `high`.
- [ ] Context: 131,072 is the native maximum; size the server to the real need (`--max-model-len`, `--ctx-size`).
- [ ] Verify: one request returns non-empty `content` and, with a parser, a separate `reasoning`; a tool-call request
      returns `tool_calls`; a second turn works after sending `reasoning` back with the tool call.

## Reference index

- `references/models.md`: the two sizes, safeguard, NVIDIA and AMD derivatives, architecture, context, license. Load first.
- `references/parsers-and-templates.md`: harmony roles and channels, multi-turn rules, reasoning toggles and parser flags per engine, sampling.
- `references/platforms-and-quants.md`: formats, memory table, DGX Spark, RTX, Apple Silicon, H100/B200/AMD settings.
- `references/known-issues.md`: error strings and symptoms with causes and fixes.

## Companion skills

- `self-hosted-llms`: run it behind llama-swap and LiteLLM on a DGX Spark or GPU server. Install: `npx skills add ScaleDockHQ/llm-skills --skill self-hosted-llms`.
- `local-llms`: laptop and desktop runtimes (Ollama, llama.cpp, LM Studio, MLX). Install: `npx skills add ScaleDockHQ/llm-skills --skill local-llms`.
- `cloud-llms`: hosted or rented gpt-oss endpoints. Install: `npx skills add ScaleDockHQ/llm-skills --skill cloud-llms`.
- `model-quantization`: produce or check GGUF, MLX, FP8 or NVFP4 variants. Install: `npx skills add ScaleDockHQ/llm-skills --skill model-quantization`.
- `fine-tuning-llms`: LoRA or QLoRA on gpt-oss and merging adapters. Install: `npx skills add ScaleDockHQ/llm-skills --skill fine-tuning-llms`.
- Engine skills such as vLLM, SGLang, llama.cpp, Ollama, TensorRT-LLM and `tool-calling-parsers` cover the engines themselves.
