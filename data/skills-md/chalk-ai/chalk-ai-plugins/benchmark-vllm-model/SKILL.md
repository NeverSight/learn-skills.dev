---
name: benchmark-vllm-model
description: Benchmark throughput and cost-per-token of a model served on vLLM in Chalk's container infrastructure. Use when someone asks for $/token, $/request, tokens/sec, "how much would it cost to self-host this model", GPU sizing for an LLM, or wants to compare a self-hosted model's economics against a hosted API.
---

# Benchmark $/token for a model on vLLM in Chalk

Produces a defensible cost-per-token number: serve the model on a GPU, drive it
to saturation, confirm the GPU is actually the limiter, then divide authoritative
cloud pricing by measured throughput.

The order matters. A throughput number without a saturation check is unfalsifiable,
and a $/hr figure pulled from a blog post is usually wrong (see step 5).

## 1. Serve the model

```sh
chalk container run --dir <chalk-project> --json --no-spinners \
  -i vllm/vllm-openai:latest -n bench-server \
  --gpu nvidia-l4:1 --cpu 4 --memory 16Gi --port 8000 --lifetime 2h \
  --env "HF_TOKEN=$HF_TOKEN" --env HF_HOME=/root/.cache/huggingface \
  --await-running --await-timeout 20m \
  -e vllm -- serve <MODEL> --port 8000 \
  --dtype bfloat16 --max-model-len 16384 --gpu-memory-utilization 0.90
```

`chalk container get --name bench-server` returns `webUrl` (publicly reachable)
and `podName`. Poll `GET $webUrl/health` — it returns 503 until weights are
loaded, then 200. Expect several minutes for a 7B download.

**GPU selection.** Only GPU pools labelled `chalk.ai/workload-type=compute` can
run container/sandbox workloads. On the staging cluster that is `l4-gpus` (L4,
24GB, native bf16), capped at 2 nodes x 1 GPU. A pool that lacks the label
(e.g. `t4-gpus`) will leave the pod Unschedulable and the controller gives up
after **300s** — shorter than a cold GPU node autoscale, so a valid request can
fail purely on capacity. Free a GPU and retry.

Turing (T4) has no native bf16; use `--dtype float16` there.

## 2. Serving flags that change the answer

Benchmark the config you intend to run, and say which flags you set. These
materially move the result:

| Flag | Why it matters |
|---|---|
| `--max-num-seqs` | Caps concurrent sequences. Too high wastes scheduler time on short requests — throughput can *fall* as you raise it. Sweep it. |
| `--max-num-batched-tokens` | Prefill chunk budget. The binding constraint for prompt-heavy / short-output workloads. |
| `--enable-prefix-caching` | On by default in vLLM V1. Inflates apparent prompt throughput (see pitfalls). |
| `--limit-mm-per-prompt '{"image":1}'` | Multimodal models profile peak activation memory against worst-case images per prompt, stealing KV cache. Pin it. |
| `--dtype` | bf16 on Ada/Hopper; fp16 on Turing. |
| `--enforce-eager` | Skips CUDA graph capture: faster startup, slower decode. Fine for 1-token outputs, wrong for general serving. Don't leave it on in a benchmark you intend to generalize. |
| `--api-key` | The container `webUrl` is publicly resolvable. An unauthenticated LLM endpoint is exposed. Pair with `chalk container run --authenticated`. |

## 3. Drive load

Use `scripts/bench.py` (bundled with this skill). It sweeps prompt length and
concurrency, and reads throughput from vLLM's **own Prometheus counters**
(`vllm:prompt_tokens_total`, `vllm:generation_tokens_total`,
`vllm:request_success_total`) across a steady-state window.

```sh
./scripts/bench.py --base-url "$URL" --model "$MODEL" \
  --input-lens 128,512 --concurrency 8,32,64 --duration 30
```

Methodology rules, each of which fixes a real failure mode:

- **Sustained windows, not fixed request counts.** Sub-10s windows are dominated
  by jitter. Use >=20s and a warm ramp before the measured window.
- **Server-side counters, not client timing.** Removes client overhead and WAN
  latency from the measurement.
- **Sweep concurrency until throughput stops rising.** One concurrency level
  tells you nothing about where saturation is.
- **Unique prompt prefixes.** Identical prompts hit the prefix cache and inflate
  results (bundled script seeds each request).
- **Watch for client-side bottlenecks.** If throughput *drops* at high
  concurrency, suspect the load generator's CPU before the server. Re-run from a
  bigger box, or from inside the cluster.

**Where to run the driver.** From a laptop is fine to start. To rule out the
network path, run it as a container inside the cluster (`--cpu 6`, the vLLM image
already has Python + httpx) and point it at the server's **pod IP**
(`kubectl get pod <podName> -o jsonpath='{.status.podIP}'`), then repeat against
the public `webUrl`. If the two agree, the ingress is not your bottleneck —
measure this rather than assuming it.

## 4. Confirm the GPU is the limiter

A throughput number is only a *hardware* number if the hardware was saturated.
Check DCGM on the node running the model:

```sh
NODE=$(kubectl -n ns-<env> get pod <podName> -o jsonpath='{.spec.nodeName}')
DCGM=$(kubectl -n chalk-telemetry get pods -o wide | grep "dcgm.*$NODE" | awk '{print $1}')
kubectl -n chalk-telemetry port-forward "$DCGM" 19400:9400 &
curl -s localhost:19400/metrics | grep -E '^DCGM_FI_DEV_(GPU_UTIL|POWER_USAGE|FB_USED)'
```

Sample it *during* the run. `GPU_UTIL` at 100 and `POWER_USAGE` at the card's TDP
(72W for L4, 300W for A100 40GB) means you are GPU-bound and the number is real.
Utilization well under 100% means you measured your client, the network, or a
scheduler cap — not the GPU. Note the exporter scrapes on an interval, so
identical consecutive samples are expected.

## 5. Get the real $/hr

**Do not trust third-party pricing pages or a web search summary.** For GPU
machine families the accelerator is often a **separate SKU** from vCPU and RAM,
and aggregator sites frequently omit it — which understates the node by 3x.

Query GCP's Cloud Billing Catalog directly (Compute Engine service
`6F81-5844-456A`), summing the SKUs that make up the node:

```py
# paginate skus?pageSize=5000&currencyCode=USD with an Authorization: Bearer token
# from `gcloud auth print-access-token`, filter serviceRegions for your region,
# then match description against your machine family and accelerator.
```

Worked example, `g2-standard-8` (8 vCPU, 32 GiB, 1x L4) in `us-central1`:

| SKU | Rate | Qty | Subtotal |
|---|---|---|---|
| G2 Instance Core running in Americas | $0.024988 /hr | 8 | $0.199904 |
| G2 Instance Ram running in Americas | $0.002927 /GiB-hr | 32 | $0.093664 |
| **Nvidia L4 GPU running in Americas** | **$0.560040 /hr** | 1 | **$0.560040** |
| | | | **$0.853608 /hr** |

Omitting the GPU SKU yields $0.2936/hr — a number that appears on public pricing
aggregators and is wrong. Sanity-check by computing spot the same way and
confirming it lands at the expected discount.

Also pull Spot and 1yr/3yr CUD rates; they are separate SKUs and are what a
production deployment would actually pay.

## 6. Compute the cost

```
$/sec        = node_hourly / 3600
$/1M in-tok  = $/sec / prompt_tok_per_s * 1e6
$/1M req     = $/sec / rps * 1e6
```

Report **$/1M input tokens** and **$/1M requests**, plus the on-demand / spot /
CUD variants.

**Pick the right unit.** For a classifier or guardrail that emits a single token,
output tokens are identical to requests and "$/output token" is a degenerate
metric — lead with **$/classification**. For a chat or coding model, decode
dominates and $/output token is the meaningful figure; set `--output-tokens` to a
realistic completion length rather than 1.

## Pitfalls

- **Prefix caching inflates $/input-token.** A shared system prompt gets cached,
  so `prompt_tokens_total` counts tokens that were never recomputed. The bundled
  script reports the hit rate. It is a *fair* comparison against a vendor who
  bills you for every input token, but it is **not** your real compute headroom —
  say which one you are quoting.
- **Saturation numbers are a floor, not a forecast.** These are 100%-duty-cycle
  figures. At 20% real utilization, multiply by 5. Idle GPU time is the dominant
  cost in most production deployments.
- **Tool-calling models need the right parser and the right checkpoint.**
  `--enable-auto-tool-choice --tool-call-parser hermes` plus an *instruct* model.
  Some Coder-tuned checkpoints emit tool calls as fenced JSON text that the parser
  ignores, so `tool_calls` returns null under `tool_choice: auto` while
  `tool_choice: required` works (guided decoding forces the shape).
- **Completed container pods are garbage-collected**, taking their logs. End a
  one-shot driver script with `sleep` so you can still `kubectl logs` it.
- **`chalk container exec` is unimplemented for k8s containers**
  (`only implemented for host containers`). Drive work via the entrypoint, or use
  `--compute-class host` / the sandbox API.
- **Piping a script into `bash` breaks silently** if it invokes anything that
  reads stdin — the child eats the rest of the script. Write it to a file and add
  `exec </dev/null`.
- **Sandboxes have no network egress** and no flag to grant it; even public IPs
  are blocked. Use `chalk container run --route <CIDR>` when the workload must
  reach anything.

## Reporting

State the model, GPU, every non-default serving flag, the measured throughput,
the DCGM saturation evidence, and the SKU breakdown behind the $/hr. A
cost-per-token figure without those is not reproducible and should not be quoted.
