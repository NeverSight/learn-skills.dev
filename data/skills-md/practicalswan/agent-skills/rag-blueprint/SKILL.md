---
name: rag-blueprint
version: "2.0"
last_updated: 2026-09-08
tags: [nvidia, rag, deployment, retrieval, blueprint, ops]
description: "NVIDIA RAG Blueprint deployment, configuration, troubleshooting, and shutdown guidance for Docker, Helm, and library-based RAG stacks."
license: "Apache-2.0"
compatibility: "Guidance imported from the NVIDIA RAG Blueprint skill for Docker Compose, Helm, and Python 3.11+ RAG deployments."
---
# NVIDIA RAG Blueprint

## Purpose

Use this skill for NVIDIA RAG Blueprint operations: deployment, configuration,
troubleshooting, shutdown, and feature management across Docker, Helm, and
library deployments.

## Instructions

1. Match the user request to the intent routing table below.
2. Read the referenced playbook before making changes.
3. Use repository docs and deployment config files as the source of truth.
4. Verify the affected service or workflow after changes.

## Prerequisites

- NVIDIA RAG Blueprint repository checkout.
- Docker/Compose or Kubernetes/Helm for deployments.
- Python 3.11+ for library workflows.
- NVIDIA GPU tooling for self-hosted NIM services.

## Autonomy Principles

- Auto-detect everything: GPU, VRAM, drivers, Docker, CUDA, disk, OS, ports, existing services, NGC key, repo state.
- If it can be checked with a command, check it — don't ask the user.
- Ask only when user action is required: providing an API key, confirming data deletion, or choosing between equally valid options.
- Once analysis is done, route to the correct workflow and execute.

## Intent Detection

Determine what the user wants and route immediately:

| User Intent | Action |
|-------------|--------|
| Deploy, install, set up, start RAG | Read and follow `references/deploy.md` |
| Configure, enable, change, toggle a feature | Use the Configure section below |
| Troubleshoot, debug, fix, error, unhealthy | Read and follow `references/troubleshoot.md` |
| Stop, shutdown, tear down, clean up | Read and follow `references/shutdown.md` |

If the intent is ambiguous, infer from context (e.g., "RAG isn't working" → troubleshoot; "get RAG running" → deploy). Only ask if genuinely unclear.

---

## Configure

Requires a running RAG deployment. If services are not running, deploy first via `references/deploy.md`.

Match the user's request to a reference file, then read and follow it:

| Feature Keywords | Reference |
|-----------------|-----------|
| VLM, VLM embeddings, image captioning | `references/configure/vlm.md` |
| NeMo Guardrails | `references/configure/guardrails.md` |
| Agentic RAG, planning/execution agent, agentic streaming, stage events | `references/configure/agentic-rag.md` |
| Query rewriting, decomposition, multi-turn | `references/configure/query-and-conversation.md` |
| Ingestion (text-only, audio, Nemotron Parse, OCR, batch CLI, NV-Ingest, volume mount, performance) | `references/configure/ingestion.md` |
| Search, retrieval, hybrid search, multi-collection, metadata, filters, Elasticsearch filters, reranker, topK, accuracy/performance | `references/configure/search-and-retrieval.md` |
| LLM/embedding/ranking model changes, vector DB, Milvus/Elasticsearch auth, service keys, model profiles, ports/GPU | `references/configure/models-and-infrastructure.md` |
| Reasoning, thinking mode, `reasoning_content`, self-reflection, prompts, generation params (tokens, temperature, citations), per-request LLM params | `references/configure/reasoning-and-generation.md` |
| Summarization | `references/configure/summarization.md` |
| Observability (tracing, Zipkin, Grafana, Prometheus) | `references/configure/observability.md` |
| Multimodal query (image + text) | `references/configure/multimodal-query.md` |
| Data catalog (collection/document metadata) | `references/configure/data-catalog.md` |
| User interface (UI settings, reasoning panel, metadata filters) | `references/configure/user-interface.md` |
| API reference (endpoints, schemas) | `references/configure/api-reference.md` |
| Evaluation (RAGAS metrics) | `references/configure/evaluation.md` (and skill `rag-eval`) |
| MCP server & client, agent toolkit | `references/configure/mcp.md` |
| Migration (version upgrades) | `references/configure/migration.md` |
| Notebooks (setup and catalog) | `references/configure/notebooks.md` |

### Configure Flow

1. Match the user's request to a reference file from the table above.

2. Detect what's running:
   ```bash
   echo "=== NIM ===" && docker ps --format '{{.Names}}' 2>/dev/null | grep -iE '(nim-llm|nemotron-(vlm-)?embedding|nemotron-ranking|nemotron-vlm|nemotron-3-nano-omni|page-elements|graphic-elements|table-structure|nemotron-ocr)' || echo "NO_LOCAL_NIMS"; echo "=== RAG ===" && docker ps --format '{{.Names}}' 2>/dev/null | grep -iE '(rag-server|ingestor-server|elasticsearch|milvus|seaweedfs|lancedb)' || echo "NO_DOCKER_RAG"; echo "=== K8S ===" && kubectl get pods -n rag 2>/dev/null | head -5 || echo "NO_K8S"; echo "=== LIBRARY ===" && ps aux 2>/dev/null | grep -E '(nvidia_rag|uvicorn.*rag)' | grep -v grep || echo "NO_LIBRARY"
   ```

3. Use this table to determine platform, deployment type, and where config lives:

   | Local NIMs running? | RAG services running? | Deployment Type | Config Location |
   |---------------------|-----------------------|-----------------|-----------------|
   | Yes (Docker) | Any | Self-hosted | `deploy/compose/.env` |
   | No | Yes (Docker) | NVIDIA-hosted | `deploy/compose/nvdev.env` |
   | Yes (K8s pods) | Any | Self-hosted | `values.yaml` (NIM sections) |
   | No | Yes (K8s pods) | NVIDIA-hosted | `values.yaml` (envVars) |
   | — | Library processes | Library mode | `notebooks/config.yaml` |
   | No | No | Not running | Deploy first via `references/deploy.md` |

   Tell the user what you detected and ask to confirm. Example: "I see local NIM containers running (nim-llm-ms, nemotron-vlm-embedding-ms) — this is a self-hosted deployment. Config file is `deploy/compose/.env`. Correct?"

4. Check current feature state before changing anything — read the config location from step 3, then cross-check the live service:
   - Docker: `docker exec rag-server env 2>/dev/null | grep -E "<VAR_NAME>"`
   - Helm: `kubectl get pod -n rag -l app=rag-server -o jsonpath='{.items[0].spec.containers[0].env}' 2>/dev/null`

   If the config file and live service disagree, tell the user the service has stale config and will need a restart.

5. If the feature needs extra GPUs, check availability against hardware restrictions (see below):
   ```bash
   nvidia-smi --query-gpu=index,name,memory.total,memory.used --format=csv,noheader 2>/dev/null || echo "NO_GPU"
   ```

6. Read the reference file and apply changes:
   - Docker: edit the env file (uncomment to enable, re-comment to disable — the env file is the source of truth). Then restart the affected service:
     ```
     source <env-file> && docker compose -f deploy/compose/<compose-file> up -d
     ```
     | Service | Compose File |
     |---------|-------------|
     | rag-server | `docker-compose-rag-server.yaml` |
     | ingestor-server | `docker-compose-ingestor-server.yaml` |
     | Elasticsearch, Milvus, etcd, SeaweedFS | `vectordb.yaml` |
     | NIM containers (LLM, embedding, ranking, VLM, OCR, parse, audio, extraction) | `nims.yaml` |
     | guardrails | `docker-compose-nemo-guardrails.yaml` |
     | observability (Grafana, Prometheus, Zipkin) | `observability.yaml` |
   - Helm: edit `values.yaml`, then upgrade: `helm upgrade rag <chart> -n rag -f values.yaml`
   - Library: edit `notebooks/config.yaml`, then restart the Python process

7. Verify:
   - Docker: `docker ps --format "table {{.Names}}\t{{.Status}}" | head -20; curl -s http://localhost:8081/v1/health?check_dependencies=true 2>/dev/null | head -1`
   - Helm: `kubectl get pods -n rag; kubectl rollout status deployment/rag-server -n rag --timeout=120s`
   - Library: `curl -s http://localhost:8081/v1/health 2>/dev/null | head -1`

8. If restart fails, read `references/troubleshoot.md`. If multiple features requested, repeat from step 1 for each.

## Examples

- "Deploy RAG" -> route to `references/deploy.md`.
- "Enable VLM" -> route to `references/configure/vlm.md`.
- "RAG is unhealthy" -> route to `references/troubleshoot.md`.
- "Stop RAG" -> route to `references/shutdown.md`.

## Limitations

- Operational guidance only applies to this RAG Blueprint repository.
- Live deployment changes require a running Docker, Helm, or library target.
- Secrets such as `NGC_API_KEY` must be supplied by the user environment.

## Troubleshooting

| Error / signal | What to do |
|----------------|------------|
| Services are not running | Follow `references/deploy.md` before configuring features. |
| Restart or health check fails | Follow `references/troubleshoot.md`. |
| User requests teardown | Follow `references/shutdown.md` and confirm destructive cleanup. |

### When User Says "Configure" Without Specifics

Run steps 2–3 above, then read the identified config file to list what's currently enabled:
```bash
grep -E "^(export )?(ENABLE_|APP_)" <config-file> 2>/dev/null | sort
```
Summarize what's running and enabled, then ask which feature to change.

---

## Hardware Restrictions

Read `docs/support-matrix.md` for current GPU requirements per deployment mode.
Read `docs/service-port-gpu-reference.md` for port mappings and GPU assignments.

| GPU | Feature Restrictions |
|-----|---------------------|
| B200 | No VLM, No Guardrails, No Nemotron Parse. May need multi-GPU LLM (`LLM_MS_GPU_ID`). |
| RTX PRO 6000 | No Nemotron Parse. No Audio on Helm. |

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/rag-blueprint` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the NVIDIA RAG Blueprint skill without MCP. Rely on its local instructions, bundled resources, standard shell or editor tools, and direct verification. Show the evidence used before concluding."
- Do not claim an MCP operation was used when the active host does not expose it.
- Treat local files, tests, rendered outputs, logs, or screenshots as the fallback evidence path.

<!-- MCP:END -->

## Anti-Patterns

- Changing deployment knobs before identifying the active deployment mode: Compose, Helm, and library paths are not interchangeable.
- Treating retrieval, model, and infrastructure faults as the same class of problem: It wastes time and can hide the real failing layer.
- Stopping or tearing down services without checking persistence impact: Cleanup can destroy the exact evidence needed for recovery.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The workflow identifies the active deployment path and uses the matching upstream playbook before proposing changes.
2. Pass/fail: Any configuration change is tied to the exact file, chart value, or environment variable that owns the behavior.
3. Pass/fail: Health checks, logs, or a real retrieval request are used before claiming the stack is healthy again.
4. Pressure-test scenario: Apply the workflow to a half-running deployment where ingestion works but retrieval answers are empty.
5. Success metric: The requested RAG feature or service state is reproducible, observable, and verified with a live check path.

## Related Skills

- [cloud-design-patterns](../cloud-design-patterns/SKILL.md): Use it when the RAG deployment decision also needs broader distributed-system tradeoff analysis.
- [devops-tooling](../devops-tooling/SKILL.md): Use it when the work also needs repo, CI, or infrastructure automation steps.
- [notebooklm-management](../notebooklm-management/SKILL.md): Use it when the user also needs retrieval-oriented research workflows outside the deployment stack.
