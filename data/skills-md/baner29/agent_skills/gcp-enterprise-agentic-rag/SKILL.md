---
name: gcp-enterprise-agentic-rag
description: >-
  Scaffolds, provisions, and deploys an enterprise serverless multi-agent RAG system
  on Google Cloud Platform using Google ADK, Vertex AI Agent Runtime (Agent Engine),
  Vertex AI Session & Memory Bank Services, Cloud DLP, Pub/Sub, BigQuery ML remote models,
  and Vertex AI Search. Use when building or deploying enterprise multi-agent systems
  on GCP, adding privacy-preserving RAG, or setting up managed agent memory.
license: Apache-2.0
compatibility: >-
  Requires Google Cloud SDK (gcloud CLI), Python 3.10+, BigQuery, Vertex AI, and GCP API access.
  Compatible with Claude Code, Codex, Cursor, Antigravity, and other coding agents.
metadata:
  author: "Abhishek Banerjee"
  version: "1.0.0"
  category: "cloud-infrastructure"
  tags: "gcp,vertex-ai,adk,rag,cloud-dlp,bigquery"
  source: "https://github.com/baner29/agent_skills"
allowed-tools: Bash(gcloud:*) Bash(bq:*) Bash(python:*) Read Write
---
# Enterprise Serverless Managed RAG Agentic Framework on GCP

This skill guides coding agents (Claude Code, Codex, Cursor, Antigravity, and others) to scaffold, validate, provision, and deploy a production-grade multi-agent system on Google Cloud Platform (GCP).

## When to use

- Building or deploying an enterprise multi-agent architecture on GCP.
- Implementing an autonomous root orchestrator (`root_agent`) with specialized sub-agents.
- Integrating managed session state (`VertexAiSessionService`) and persistent memory bank (`VertexAiMemoryBankService`).
- Establishing a closed-loop RAG pipeline with automatic Cloud DLP PII redaction and BigQuery ML summarization.
- Deploying natively to Vertex AI Agent Runtime (Agent Engine).

## When not to use

- Single-turn text completions or simple one-off Gemini API scripts.
- Non-GCP deployments (AWS, Azure, or self-hosted Kubernetes clusters).
- Traditional containerized microservices on Cloud Run without Agent Engine.

---

## Workflow Checklist

Maintain and check off each step before proceeding to the next:

Progress:

- [ ] **Step 1: Requirements Discovery** — Conduct user interview ([references/discovery.md](references/discovery.md))
- [ ] **Step 2: Pre-Requisite Verification** — Run infrastructure checks (`scripts/check_prereqs.sh`)
- [ ] **Step 3: Codebase Scaffolding** — Generate multi-agent structure ([references/architecture.md](references/architecture.md))
- [ ] **Step 4: Pre-Deployment Validation** — Self-validate codebase integrity (`scripts/validate_agent.py`)
- [ ] **Step 5: Managed RAG Pipeline** — Provision BigQuery ML & DLP ([references/rag_pipeline.md](references/rag_pipeline.md))
- [ ] **Step 6: Agent Runtime Deployment** — Deploy via AdkApp ([references/agent_runtime.md](references/agent_runtime.md))
- [ ] **Step 7: Post-Deployment Verification** — Verify live system (`scripts/verify_deployment.py`)
- [ ] **Step 8: Generate Application Documentation** — Create root README.md ([references/documentation.md](references/documentation.md))

---

## Step 1: Requirements Discovery

Ask the user questions to collect application specifications. See [references/discovery.md](references/discovery.md) for the complete questionnaire.

Key defaults:

- Root Orchestrator: **`root_agent`** (fixed default).
- Default LLM: **`gemini-3.8-flash`**.

---

## Step 2: Infrastructure & Pre-Requisite Verification

Run the bundled pre-requisite check script to ensure all GCP APIs and IAM roles are active:

```bash
bash scripts/check_prereqs.sh "<gcp_project_id>" "<service_account_email>"
```

For the complete list of required APIs, IAM roles, and recommended MCP servers, load [references/prerequisites.md](references/prerequisites.md).

---

## Step 3: Codebase Scaffolding

Generate the multi-agent application layout using the templates in `assets/`:

- Multi-Agent Orchestrator & Sub-agents: [assets/template_agent.py](assets/template_agent.py)
- Agent Runtime Deployment Script: [assets/template_deploy.py](assets/template_deploy.py)
- Cloud DLP Sanitization Cloud Function: [assets/template_cf_main.py](assets/template_cf_main.py)

For memory bank callback patterns and architecture details, load [references/architecture.md](references/architecture.md).

---

## Step 4: Pre-Deployment Self-Validation

> [!IMPORTANT]
> The coding agent must validate the scaffolded codebase before attempting any GCP deployment.

Execute the validator:

```bash
python scripts/validate_agent.py .
```

If validation fails, review the output, fix errors in the code, and re-run. Proceed only when all checks report `✅ PASSED`.

---

## Step 5: Managed RAG & Privacy Pipeline Setup

1. **Pub/Sub & BigQuery Table Creation**: Create topic `agent-session-transcripts` and dataset tables.
2. **Deploy Cloud DLP Cloud Function**: Deploy Gen 2 function `process-transcript-stream` with Cloud DLP redaction.
3. **Automated BigQuery ML Provisioning**:
   ```bash
   bash scripts/setup_bq_ml.sh "<gcp_project_id>" "<gcp_region>" "<bq_dataset_id>"
   ```
4. **Vertex AI Search**: Link BigQuery insights table to Discovery Engine.

For step-by-step SQL queries and Cloud DLP configurations, load [references/rag_pipeline.md](references/rag_pipeline.md).

---

## Step 6: Vertex AI Agent Runtime Deployment

1. **Create Engine**: Run `create_engine.py` to obtain `AGENT_ENGINE_ID`.
2. **Deploy Application**:
   ```bash
   python deploy_agent_engine.py --mode=create
   ```

For OpenTelemetry flags and AdkApp deployment options, load [references/agent_runtime.md](references/agent_runtime.md).

---

## Step 7: Post-Deployment Self-Validation

Verify the live deployment:

```bash
python scripts/verify_deployment.py --project="<gcp_project_id>" --engine_id="<agent_engine_id>"
```

Execute a test query through the deployed Agent Engine to ensure OpenTelemetry spans export to Cloud Trace and session events stream to Pub/Sub and BigQuery.

---

## Step 8: Generate Application Documentation

Generate a comprehensive `README.md` file in the root of the generated project directory. The documentation must detail:

1. **Agent Architecture & Working**: Explaining `root_agent`, specialized sub-agents, memory bank persistence, and the closed-loop RAG pipeline.
2. **Runtime Invocation & Environment**: Configuration (`.env`), deployment commands, and programmatic SDK/API usage.
3. **Interactive Testing via GCP Console Playground**: Step-by-step instructions for testing queries, inspecting sub-agent tool calls, validating memory retention, and viewing OpenTelemetry waterfall traces directly in the Vertex AI Agent Engine Playground on the Google Cloud Console.

Follow the complete documentation guide and template in [references/documentation.md](references/documentation.md).

---

## Gotchas & Troubleshooting

Before troubleshooting unexpected GCP errors, consult [references/gotchas.md](references/gotchas.md) for solutions to:

- BigQuery Connection Service Account `roles/aiplatform.user` permission errors.
- Memory Bank asynchronous client garbage collection bug workarounds (`wait_for_completion=False`).
- Sub-agent session context window isolation.
- OpenTelemetry GenAI experimental flags for Cloud Trace.
