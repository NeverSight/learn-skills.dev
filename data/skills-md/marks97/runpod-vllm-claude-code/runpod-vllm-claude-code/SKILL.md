---
name: runpod-vllm-claude-code
description: Deploy any HuggingFace model to RunPod as a vLLM server, bridge it to Claude Code (which speaks Anthropic's Messages API, not OpenAI's), smoke-test that tool-calling actually works end to end, and tear everything down with zero trace (pod, network volumes, local processes, scratch files). Use this whenever you want to run a model on RunPod, try a model with Claude Code, test whether a HF/GGUF/abliterated checkpoint supports tool use, benchmark a model for coding-agent use, or spin up/kill a disposable GPU inference box. Also trigger it for anything about hooking Claude Code up to a non-Anthropic backend (vLLM, Ollama, LM Studio) via ANTHROPIC_BASE_URL, or questions like 'what GPU do I need to run X' and 'how much will it cost to run this model'.
---

# RunPod vLLM + Claude Code bridge

Two things are being solved together here, and it's worth being clear about which is which:

1. **Getting a model running on RunPod.** Straightforward — pick a GPU, start a
   vLLM container, wait for health.
2. **Getting Claude Code to actually talk to it.** Not straightforward — Claude Code
   speaks Anthropic's Messages API (`/v1/messages`, content blocks, SSE events).
   vLLM speaks OpenAI's `/v1/chat/completions`. Nothing bridges these two by default.
   `ANTHROPIC_BASE_URL` lets Claude Code point at *any* server that implements the
   Messages API shape — so a small translation proxy in the middle is what makes
   "point Claude Code at my RunPod box" actually work. `scripts/anthropic-openai-proxy.js`
   is that proxy, already fixed for the two protocol mismatches that will otherwise burn
   an hour of retries (see Gotchas below). Use it as-is; don't re-derive it from scratch.

This is exploratory/disposable infra by nature — a GPU pod costs real money per hour
the moment it exists. Before creating one, tell the user which GPU and roughly $/hr,
unless they already named the machine and accepted the cost.

## Step 0: get real numbers on the model before guessing hardware

Don't trust generic "VRAM requirements" blog posts for a model name — the GPU-rental
SEO space is full of content-farm sites (things like "willitrunai.com", "canitrun.dev",
"orcarouter.ai") that auto-generate plausible-looking spec pages for *any* model name,
including ones that barely exist yet. They will confidently disagree with each other.

Get ground truth from the HuggingFace API instead:

```bash
# Real param count / architecture (don't trust the repo name's number):
curl -s "https://huggingface.co/<org>/<model>/raw/main/config.json"

# Real total weight size, which is what actually has to fit in VRAM:
curl -s "https://huggingface.co/<org>/<model>/raw/main/model.safetensors.index.json" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['metadata']['total_size'] / 1e9, 'GB')"
```

bf16 weight size in GB ≈ params(B) × 2. Budget the GPU so weights leave at least
~20-30GB of headroom for KV cache + activations — more if the model is a dense
transformer (full KV cache scales with context), less if it's a hybrid/linear-attention
architecture (Mamba/GDN layers keep fixed-size state, so long context is much cheaper
than a same-size dense model).

If the model is a known problem architecture (very new hybrid attention, a fresh
release), search for `"<architecture class name>" vllm github issues` — e.g.
`Qwen3_5ForConditionalGeneration vllm issues` — before committing to a GPU choice,
since brand-new architectures sometimes have open correctness bugs in vLLM
(garbled output, tensor-format mismatches). Flag this risk to the user rather than
silently hoping it works.

## Step 1: pick and check GPU availability/price (don't guess the type string)

RunPod's REST API 404s on `/v1/gputypes` and `/v1/datacenters` — those aren't real
endpoints despite being an obvious guess. Use the GraphQL API instead:

```bash
curl -s -X POST https://api.runpod.io/graphql \
  -H "Authorization: Bearer $RUNPOD_API_KEY" -H "Content-Type: application/json" \
  -d '{"query":"query { gpuTypes(input: {id: \"NVIDIA H100 80GB HBM3\"}) { id lowestPrice(input: {gpuCount: 1}) { uninterruptablePrice stockStatus } } }"}'
```

Valid `gpuTypeIds` include `"NVIDIA H100 80GB HBM3"` (SXM), `"NVIDIA H100 PCIe"`,
`"NVIDIA H100 NVL"`, `"NVIDIA A100 80GB PCIe"`, `"NVIDIA A100-SXM4-80GB"` — get the
full list with `query { gpuTypes { id displayName memoryInGb } }` if unsure. Pass a
short list of acceptable types to pod creation (see below) so RunPod falls back
automatically if your first choice is out of stock, rather than failing the whole
provision.

Where the key lives: check `$RUNPOD_API_KEY` in the environment first; if it is not
set, export it (create one in the RunPod console under Settings -> API Keys).

## Step 2: create the pod

```bash
curl -s -X POST https://rest.runpod.io/v1/pods \
  -H "Authorization: Bearer $RUNPOD_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name": "vllm-<model-slug>-test",
    "gpuTypeIds": ["NVIDIA H100 PCIe", "NVIDIA H100 80GB HBM3", "NVIDIA H100 NVL"],
    "imageName": "vllm/vllm-openai:latest",
    "containerDiskInGb": <weights_GB * 1.5, minimum 80>,
    "ports": ["8000/http"],
    "dockerStartCmd": [
      "--model", "<org>/<model>",
      "--host", "0.0.0.0", "--port", "8000",
      "--trust-remote-code",
      "--enforce-eager",
      "--gpu-memory-utilization", "0.90",
      "--max-model-len", "65536",
      "--served-model-name", "<served-name>",
      "--enable-auto-tool-choice",
      "--tool-call-parser", "hermes"
    ],
    "env": { "HF_HOME": "/root/.cache/huggingface" }
  }'
```

Notes on the flags:
- **`--max-model-len`: go big, bigger than feels necessary.** 65536 sounded generous
  but a real multi-hour coding session (git surgery, lots of tool output) reached
  ~127K tokens and hit the wall — and worse, `/compact` itself needs input + a real
  output budget for the summary, so if the conversation is already near the ceiling,
  compact fails with the *same* overflow error at the exact moment you need it most.
  Prefer the model's own native context length — check `max_position_embeddings` in
  the HF `config.json` from Step 0 — and use that if GPU memory allows (a 262144-token
  window on an 80GB H100 was comfortable for a ~28B model). Going from 65536 straight
  to the model's real max avoided a second round of the same problem.
- **`--tool-call-parser`**: pick the one matching the model family (`hermes` is a
  reasonable default for most fine-tunes; `qwen3_coder` + `--reasoning-parser qwen3`
  for Qwen3.x-coder-style models). Wrong parser choice won't error loudly — the model
  will just never emit tool_calls, only text. If Claude Code isn't calling tools,
  check the parser first.
- **`--enforce-eager`**: keep it for the first smoke test — it avoids CUDA-graph
  compile time and any related instability while you're just checking the model
  responds sanely. Drop it once correctness is confirmed and you care about speed.
- Poll `GET /v1/pods` first and reuse a `RUNNING` pod with a matching `name` if one
  already exists, instead of creating a duplicate.

The vLLM URL is always `https://<podId>-8000.proxy.runpod.net`. Poll `/health` (expect
404 then a string of 502s while the image pulls and weights download, then 200) —
budget several minutes for a 50GB+ model. Run the poll loop in the background
(`run_in_background: true`) rather than blocking the conversation on it.

Once healthy, sanity-check with a raw curl before involving Claude Code at all:

```bash
curl -s "$VLLM_URL/v1/chat/completions" -H "Content-Type: application/json" -d '{
  "model": "<served-name>", "messages": [{"role":"user","content":"What is 2+2? One word."}],
  "max_tokens": 20, "temperature": 0
}'
```

Coherent output here proves the model+vLLM combo works before adding the Claude Code
layer's own complexity on top. If this step gives garbled/repeating tokens, it's a
model or vLLM version issue, not a bridging issue — don't proceed to step 3 yet.

## Step 3: bridge Claude Code to it

Copy `scripts/anthropic-openai-proxy.js` next to where you're working and run it:

```bash
VLLM_URL="https://<podId>-8000.proxy.runpod.net" PORT=<free-port> SERVED_MODEL="<served-name>" \
  node anthropic-openai-proxy.js
```

Pick a genuinely free local port first — `ss -ltn | grep :<port>` — this box runs
many Claude sessions in parallel and a common port like 8787 is often already taken
by someone else's process. Don't just assume your port is free.

Then run an **isolated** Claude Code invocation against it — isolated meaning it must
not fall back to the user's real, billed Anthropic account if the override doesn't
take:

```bash
env -u ANTHROPIC_AUTH_TOKEN -u CLAUDE_CODE_OAUTH_TOKEN \
  ANTHROPIC_BASE_URL="http://localhost:<port>" \
  ANTHROPIC_API_KEY="sk-local-dummy-key" \
  CLAUDE_CODE_MAX_CONTEXT_TOKENS=<max-model-len used above> \
  claude --bare -p "<test task>" \
  --dangerously-skip-permissions \
  --model <served-name> \
  --output-format text
```

- **`--bare`** is what makes this safe: it forces auth to be strictly
  `ANTHROPIC_API_KEY`/`apiKeyHelper`, never OAuth or keychain. Without it, a
  misconfigured override can silently fall through to the user's real logged-in
  account and bill it — `--bare` closes that off structurally rather than relying on
  the env override being perfect.
- **`CLAUDE_CODE_MAX_CONTEXT_TOKENS`**: without this, an unrecognized `--model` name
  makes Claude Code assume a 200k window for its own budgeting, which causes it to
  request far more `max_tokens` than the vLLM server's `--max-model-len` allows.
  Set it to the same number you passed vLLM.
- **`CLAUDE_CODE_MAX_OUTPUT_TOKENS`**: a separate, easy-to-miss ceiling. When
  `/compact` has to summarize a very large conversation, Claude Code computes how big
  an output budget it needs and can hit an internal hard limit ("Claude's response
  exceeded the 128000 output token maximum"), refusing *client-side* before ever
  contacting the backend — no proxy log entry, nothing to debug remotely. Set this to
  something reasonable (e.g. `8192`) alongside `CLAUDE_CODE_MAX_CONTEXT_TOKENS`.
- Watch the proxy's own stdout log while this runs — it prints incoming message/tool
  counts per turn, which is the fastest way to see whether requests are actually
  reaching the remote model versus dying in the bridge.
- Give it 2-3+ minutes for a real coding task; a `--dangerously-skip-permissions -p`
  run that hasn't returned in 180s is normal, not stuck — let it background rather
  than assuming failure.

## Mid-session: swapping the pod under a live conversation

If a real session outgrows the context window it was started with, you don't need
to lose the conversation to fix it — the chat's history lives locally in Claude
Code's own transcript, not on the pod. The pod is disposable and swappable:

1. Terminate the old pod, create a new one with a bigger `--max-model-len` (same
   image, same served-model-name).
2. Poll the new pod's `/health` same as Step 2.
3. Kill the running proxy process and restart it with the *same PORT*, pointing
   `VLLM_URL` at the new pod. Nothing on the Claude Code side needs to change —
   same `ANTHROPIC_BASE_URL`, same port.
4. Have the user resume: `claude --bare --resume <session-id> ...` with
   `CLAUDE_CODE_MAX_CONTEXT_TOKENS` bumped to match the new window.

Restarting the proxy while a request is in flight will error that one request out
(Claude Code shows an API error and usually auto-retries) — tell the user before
doing this if they're actively mid-turn, don't just do it silently.

## Known gotchas (already fixed in the bundled proxy — know them if you have to debug further)

1. **`max_tokens` overflow.** Claude Code's default requested `max_tokens` can be
   ~32000 regardless of the actual `--max-model-len`. If prompt + max_tokens exceeds
   the server's context window, vLLM 400s on every single turn and Claude Code just
   retries forever, burning GPU time for nothing. Fix: clamp the forwarded
   `max_tokens` to something sane (the bundled proxy defaults to 4096, override with
   `MAX_TOKENS_CAP`).
2. **Interleaved `role:"system"` messages.** Claude Code sends `<system-reminder>`
   content as separate `role:"system"` turns mid-conversation (not just the one
   top-level `system` field). Anthropic's own API is fine with this, but vLLM's chat
   templates enforce "system must be the first message" and 400 on anything else.
   Fix: fold any non-leading system-role message into `user` before forwarding.
3. **A `pkill -f <pattern>` that matches your own shell kills your current command
   (exit 144).** When killing a stuck nested `claude` process, find its exact PID
   with `ps aux | grep` and `kill <pid>` — don't `pkill -f "claude"` from inside a
   shell whose own invocation string also contains "claude". This isn't just a
   `claude`-specific gotcha: `pkill -f "node proxy.js"` self-matched too, because the
   shell wrapper's own command line contained that same string. Always kill by exact
   PID, never by a pattern that could describe the command you're running it from.
4. **A single long blocking backend response can exceed RunPod's edge-proxy
   timeout.** Regular RunPod Pods have no configurable timeout setting exposed via
   the API (`executionTimeoutMs`/`idleTimeout` exist in RunPod's API but are
   Serverless-only, not Pods) — so a `/compact` that has to reason over 100K+ tokens
   before answering can silently exceed it, and the proxy gets back an HTML gateway
   error page instead of JSON (`Unexpected token '<', "<!DOCTYPE"`). Fix: always
   request `stream: true` (+ `stream_options: {include_usage: true}`) from vLLM and
   relay chunks as they arrive — continuous bytes flowing means the idle timeout
   never triggers, no matter how long generation takes. The bundled proxy already
   does this.
5. **vLLM can report `prompt_tokens: 0` in the final streaming usage chunk** even
   when `completion_tokens` comes back correct and real generation happened (seen
   after heavy tool-call turns). Since Claude Code uses the reported input token
   count for its own auto-compact timing, a false 0 can make it think there's far
   more headroom than there really is — silently setting up the exact same overflow
   this whole skill exists to avoid. The bundled proxy falls back to a rough
   character-count estimate (`fallbackInputTokens`) whenever the backend's number is
   falsy; don't strip that out.

## Watching a live session's context usage from outside

You can monitor how full a running `--resume` session's context is without touching
it, by reading its own transcript for the latest assistant turn's usage — useful when
the user wants periodic "what % full am I" updates while they work.

```bash
# --bare sessions land under ~/.claude/projects/<cwd-slug>/<session-id>.jsonl —
# NOT the account-specific ~/.claude-<acct>/ dirs. find it with:
find ~/.claude -iname "*<session-id>*"

python3 -c "
import json
with open('<transcript.jsonl>') as f:
    lines = f.readlines()
for line in reversed(lines):
    line = line.strip()
    if not line: continue
    try: o = json.loads(line)
    except: continue
    if o.get('type') == 'assistant':
        usage = o.get('message', {}).get('usage')
        if usage and usage.get('input_tokens'):
            print(o['timestamp'], usage['input_tokens'], usage['input_tokens']/<max_model_len>*100)
            break
"
```

Scan the file in *reverse from the end*, not a fixed `tail -N` window — a single turn
with many tool round-trips can push the latest usage-bearing line much further back
than a small tail captures, making it look like nothing happened when it did.

## Recovering from a bad `/compact`

If `/compact` produces a summary so lossy the model loses track of the task (or
worse, takes destructive action out of confusion), the raw pre-compact messages are
still sitting in the transcript file — compact just tells *future* turns to use the
summary instead of replaying everything before it. That means you can surgically
remove the compact and resume from before it happened. **This is genuinely easy to
get wrong twice in a row** (it was, here) — read `references/transcript-surgery.md`
before attempting it, don't wing it from first principles.

## Step 4: teardown — "sin dejar rastro" means verify, not assume

When the user says kill/delete everything, that means confirm the negative, not just
issue the delete calls:

```bash
# kill exact PIDs (not pkill -f, see gotcha 3)
ps aux | grep -E "anthropic-openai-proxy|claude --bare" | grep -v grep
kill <pid> <pid>

# terminate the pod
curl -s -X DELETE "https://rest.runpod.io/v1/pods/<podId>" -H "Authorization: Bearer $RUNPOD_API_KEY" -w "\n%{http_code}\n"

# confirm nothing is left running or costing money
curl -s https://rest.runpod.io/v1/pods -H "Authorization: Bearer $RUNPOD_API_KEY"          # expect []
curl -s https://rest.runpod.io/v1/networkvolumes -H "Authorization: Bearer $RUNPOD_API_KEY" # expect [] unless one was deliberately kept
curl -s -X POST https://api.runpod.io/graphql -H "Authorization: Bearer $RUNPOD_API_KEY" \
  -H "Content-Type: application/json" -d '{"query":"query { myself { clientBalance currentSpendPerHr } }"}'
# currentSpendPerHr should read 0

# delete scratch files (proxy copy, test project, logs) from wherever they were put —
# the session scratchpad directory, never the repo
rm -rf <scratch-dir>
```

A network volume (persistent disk) is a *separate* billable resource from a pod —
terminating the pod does not delete an attached network volume. If one was created for
this session (rather than pre-existing), delete it explicitly:
`DELETE /v1/networkvolumes/<id>`.

Report the final state back with the actual numbers (balance, `currentSpendPerHr`,
empty pod/volume lists) rather than just saying "done" — that's what "sin dejar
rastro" is actually asking to see proof of.
