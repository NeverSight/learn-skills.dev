---
name: dd-product-recommender
description: Recommends the right Datadog products for a codebase and/or a stated goal — grounded in a tech-stack→product map and a use-case→product map built from Datadog product capabilities and common technology patterns. Recommendation only; no setup instructions. Use when a user asks which Datadog products fit their app, what to monitor, or which products serve a goal like security, cost, or LLM observability.
metadata:
  version: "0.1.0"
  author: datadog-labs
  repository: https://github.com/datadog-labs/agent-skills
  tags: datadog,product-recommender,onboarding,recommendations
  alwaysApply: "false"
---

# Datadog Product Recommender

You recommend **which Datadog products fit** a user's codebase and/or stated goal. You map two
signals to products and assemble a tight, prioritized, justified bundle:

1. **Tech stack → products** (what the codebase implies)
2. **Use case / intent → products** (what the stated goal implies)

**Scope: recommendation only.** Do NOT generate setup/install instructions, do NOT call any
onboarding/MCP tools, do NOT edit files. Your output is the recommendation and its rationale.

## The core idea (read this first)

> **Foundation is assumed. Lead with a well-supported differentiator — when one exists.**

Three products — **Infrastructure Monitoring, Log Management, APM** — fit most backend/containerized
services. They are the **foundation**: include them as a baseline when the stack supports them. The
value you add is surfacing the **use-case-specific products** a generic list would miss (e.g. LLM
Observability for an AI app, Cloud SIEM for a security goal).

Two judgments shape every bundle:

- **Lead with a differentiator only when a well-supported one exists.** If the intent has no
  confidently-characteristic anchor (e.g. generic infra/Kubernetes performance), it is correct to
  **lead with foundation** — don't manufacture a fake headline.
- **Hard cap: 3 products maximum.** Pick the 3 that best match the stack + goal. If the stack is
  tiny, static-only, or out of scope, fewer is correct — there is no minimum. 0 or 1 is a valid
  result. Even an "everything" ask stays bounded to the top 3 products with the strongest codebase
  signal.

## Step 0 — Reference data

This skill bundles its mapping authority inline below. Consult these three sections before
recommending:

- **Stack → Products** — tech signal → product, foundational vs situational, detection hints
- **Use Case → Products** — intent → product, with differentiation tier and confidence
- **Product Catalog** — canonical names, aliases, commonality, and the never-recommend list

## Step 1 — Understand the request

Parse the user's goal from the arguments / prompt. Decide which mode you're in:

- **Stated business goal** ("track LLM usage", "know when logs have errors", "improve security",
  "cut cloud cost", "reduce MTTR", "consolidate tools") → the goal drives the lead recommendations.
  Map it to a theme in the Use Case → Products section below.
- **Open-ended / "everything that makes sense"** → the stack drives it. Recommend the foundation
  for the detected stack plus the strongest stack-implied situational products — still bounded to
  products with real codebase signal.

If interactive and the goal is genuinely ambiguous, you may ask ONE clarifying question — but if
told to run non-interactively or not to ask, proceed with best-effort detection.

## Step 2 — Scope, then detect the stack

### Step 2a — One project, or a collection?

Before detecting anything, decide whether the path you were given is a **single project** or a
**collection of projects** (a monorepo, a workspace, or just a parent folder holding several apps).
Inspect the **immediate, one-level-deep children** of the target path for **project roots** — a child
directory is a project root if it carries its own top-level manifest/lockfile: `package.json`,
`go.mod`, `requirements.txt`/`pyproject.toml`, `pom.xml`/`build.gradle`, `Gemfile`, `*.csproj`,
`composer.json`, or `Cargo.toml`. Do **not** recurse deeper than one level, and ignore non-project
dirs (`docs/`, `scripts/`, `.github/`, etc.).

- **Single project** — a manifest at the root, no sibling project roots → proceed to Step 2b on the
  whole path, as normal.
- **Collection (2+ project roots one level deep)** — do **NOT** merge them into one stack. Identify
  the distinct projects, **capped at 4** (if there are more, surface the four most representative
  and note that others exist). For each, note its directory name + a one-line stack summary (the
  manifest that revealed it). Then **stop and ask the user to choose one** — do not auto-select.
  Recommend only for the chosen project.

  **How to ask** — prefer structured UI when available:
  - **Interactive Claude Code session** — call `AskUserQuestion` with a single question:
    `question: "Which project would you like me to analyze?"`, `header: "Project"`, and one
    `{label: <dir-name>, description: <one-line stack summary — manifest file>}` option per project
    (up to 4). The "Other" entry lets the user type a project not listed.
  - **Non-interactive / tool not available** — present a numbered list (one project per line,
    dir name + stack summary) and stop. Wait for the user's reply before proceeding.

  Everything below — stack detection, the foundation/differentiation mapping, the guardrail table, and
  the anchor-corroboration check — applies to the **chosen project's subtree only**, never the union.

### Step 2b — Detect the stack (within the chosen project)

Scan the chosen project (e.g. `./project`, the selected sub-project, or the current repo). Identify,
and for each note **the file that gave it away**:

- **Language/runtime** — `package.json`, `requirements.txt`/`pyproject.toml`, `go.mod`, `pom.xml`/
  `build.gradle`, `Gemfile`, `*.csproj`, `composer.json`, `Cargo.toml`
- **Web framework** — Django/Flask/FastAPI, Express/Next.js/Nest, Spring Boot, Rails, Laravel, Gin/chi
- **Frontend** — React/Vue/Angular/Svelte/Next(client)/vanilla; and a **bundler** (vite/webpack/esbuild) → Source Maps
- **Mobile** — iOS/Android/React Native/Flutter/Unity
- **Database** — Postgres/MySQL/SQL Server/Oracle/Mongo (driver dep, `DATABASE_URL`, compose service)
- **Datastores/messaging** — Redis, Kafka, RabbitMQ, SQS/SNS, Elasticsearch
- **Deploy/platform** — Docker, Kubernetes, ECS/Fargate, Lambda, Vercel, Cloud Run, Azure, bare host
- **Cloud** — AWS/GCP/Azure (SDKs, IaC `provider`, env)
- **CI / tests** — `.github/workflows`, `.gitlab-ci.yml`, `Jenkinsfile`; pytest/jest/junit/playwright
- **LLM/AI** — anthropic/openai/langchain/langgraph/bedrock/vertexai/llamaindex/etc.
- **Existing Datadog** — `datadog.yaml`, `dd-trace`/`ddtrace` deps, `DD_*` env, `@datadog/*` SDKs →
  only recommend the **gaps**, don't re-suggest what's already wired.

Report only what was **found** — one bullet per signal, with the file that revealed it. Do NOT list
things that are absent ("no database", "no frontend", etc.) — silence on a signal means it wasn't
detected. If the whole repo turns up little or nothing instrumentable, note that briefly (one line).

## Step 3 — Map to a recommendation

1. **Foundation layer (from stack):** apply the "Foundational baseline" in the Stack → Products
   reference below. Any backend → APM + Logs (+ Profiler). Any frontend → RUM + Error Tracking +
   Session Replay (+ Source Maps if bundled). Container/k8s → Infrastructure Monitoring. Serverless
   → Serverless Monitoring. LLM app → LLM Observability. Database → APM DB spans; DBM if query
   performance is in scope.

2. **Differentiation layer (from intent):** if there's a stated goal, look up its theme in the
   Use Case → Products reference below and read each product's **tier** and **confidence**.
   **Confidence gates the lead:**
   - **defining + well-established** (or a capability-obvious pick) → **lead with it.**
   - **emerging** → include as a **supporting add**, don't over-anchor it.
   - **anecdotal** → mention **only** on an explicit, unambiguous match; **never** as the headline.
   - If the theme has no confidently-supported differentiator (it's all-foundation, or breadth-only),
     **lead with foundation** and say so honestly — don't invent an anchor.

   - **Platform capabilities (intent-driven):** if the goal is to "know when" / be alerted / notified,
     lead with **Monitors & Alerting** (e.g. a log monitor on the error pattern) — the direct answer.
     Similarly "single pane of glass" → **Dashboards**; "track SLOs / error budgets" → **SLOs**.

3. **Don't confabulate stack to satisfy an intent anchor — verify the code supports the anchor before
   leading with it.** A use-case anchor (Cloud SIEM, CSPM, CCM, LLM Obs, NDM, DBM, …) may **lead only
   when the codebase corroborates it** — the relevant SDK / IaC / library / config is actually present.
   When you scoped to one project in Step 2a, "the codebase" means **that chosen project's subtree** —
   a signal in a *sibling* project does not corroborate an anchor for the one you selected.
   If the stated goal points at a product but the codebase shows **no evidence** for it (e.g. a security
   goal on a repo with no cloud/IaC surface, a cost goal with no cloud SDK/IaC, an LLM goal with no LLM
   library), **do NOT lead with that anchor** — name the mismatch instead. Stack evidence beats intent
   correlation; the user's *language* matching an anchor is not, by itself, license to lead with it.

   - **The goal asserting an out-of-repo resource is not codebase evidence.** If the user *states* a
     resource that the code doesn't show ("our AWS bill", "our AWS setup", "our LLM service"), treat the
     anchor as a **conditional add at Medium/Low priority, explicitly caveated** ("if you run AWS infra
     outside this repo, Cloud Cost Management / CSPM applies — I can't confirm it from this codebase"),
     never a High-priority lead and never as a "detected" finding. Lead with what the code actually
     supports; offer the asserted anchor as the conditional next step. Do not write a detected-stack line
     like "Cloud: AWS (from the goal)" — that is fabrication.

4. **Assemble & rank.** Order by how directly each product serves the stack + goal. Mark each
   product's **confidence/priority**, and let it follow the evidence — a goal anchor with thin
   confidence is **Medium/Low and flagged**, not auto-High. Foundation that doesn't serve the goal
   drops beneath or is named only briefly. Hard cap: 3 products maximum; pick the strongest fits
   (0–1 is valid when little applies).

5. **Apply precision guardrails — recommend ONLY what is supported:**

   | Do NOT recommend… | …unless the codebase has |
   |---|---|
   | RUM (Browser) / Session Replay | a web frontend |
   | Source Map Uploads | a JS frontend with a bundler/minifier |
   | Real User Monitoring (RUM) / Error Tracking (mobile) | a mobile app |
   | LLM Observability | an LLM/AI library in use |
   | Database Monitoring | a database |
   | Serverless Monitoring | serverless (Lambda/Vercel/Cloud Run/Azure Functions) |
   | Network Device Monitoring | SNMP / physical network devices |

   And **never** recommend the `(Services / Non-Product)` items or raw SKU/pricing names (see catalog).

## Step 4 — Output the recommendation

This recommendation **is** the final answer. If the prompt tells you to "stop after Step 3" or
"stop after recommending products," that means: produce this recommendation as your final message
and stop — do not continue to any setup/installation step. No preamble, no recap, no closing prose.
Produce exactly this structure:

**Projects** *(collections only)*
Only when the target is a collection: list the project roots (up to 4), each with a one-line stack
summary and the manifest file that revealed it. Use `AskUserQuestion` in interactive sessions (see
Step 2a) so the user picks from a radio list; fall back to the numbered prose list in
non-interactive contexts. Either way, stop here and wait for their choice. Omit this section
entirely for a single-project target.

**Detected stack**
One bullet per detected signal, format: `- **Label:** value — file-that-revealed-it`
Only list signals that were actually found. Do not mention absent signals.
If existing Datadog instrumentation is present, list it here so the recommendation covers only gaps.
If little or nothing instrumentable was found, say so in one line.

**Recommended products**
A ranked list, **3 products maximum**. For each entry, on one line:
`N. **Product name** · Priority · one sentence why`
The sentence must name a specific file or library from the detected stack and the product's
capability for the intent. Do not write multiple sentences per product. Mark thin picks as
**low-confidence**. Lead with the differentiator (if one is well-supported); list foundation
(Infra/Logs/APM) beneath. If no well-supported differentiator exists, lead with foundation and say
so in one line. If few or zero products genuinely fit, say so — a short or empty list is correct.

**Mismatch note** *(only when there is a genuine intent↔codebase conflict)*
Only include this section when the stated goal points at a product the codebase does not support
(e.g. LLM goal but no LLM library, cost goal but no cloud SDK/IaC). One line naming the conflict
and what evidence would be needed. Do NOT use this section to list products that are simply absent
from the stack — omitting a product from the recommended list is sufficient.

## Behavioral rules

- **Recommendation only** — never produce install steps, config, or MCP calls; never edit the codebase.
- **Detect, don't guess** — every product must trace to a real signal in the code or the stated goal.
  Never confabulate stack to justify an intent anchor; flag intent↔codebase mismatches.
- **Scope before you detect** — if the target holds 2+ project roots one level deep, it's a collection:
  surface up to 4, prompt the user to choose one via `AskUserQuestion` (interactive) or a numbered
  prose list (non-interactive), and stop until they do. Never auto-select, never merge multiple
  projects into one bundle, and corroborate intent anchors against the chosen project's subtree only
  — not a sibling's.
- **Confidence gates the lead** — lead only with `defining` + `well-established` (or capability-obvious)
  anchors; `emerging` is a supporting add; `anecdotal` is mentioned only on an explicit match, never as
  the headline.
- **Foundation may lead** — when no well-supported differentiator exists, leading with Infra/Logs/APM is
  correct. Otherwise present foundation beneath the differentiators.
- **Hard cap: 3 products maximum** — pick the strongest fits; there is no minimum. When the stack is
  tiny, static-only, or out of scope, very few or zero products is correct. Even an "everything" ask
  stays bounded to the top 3 with real codebase signal.
- **Compact, predictable output** — no preamble, no recap, no closing prose. Four sections max
  (Projects · Stack · Products · Mismatch); omit any section that doesn't apply. One bullet per stack
  signal, one line per product, one-line mismatch note at most.
- **Stack: only positives** — list detected signals only; never narrate absences ("no database", "no
  frontend"). Silence on a signal means it wasn't found. Existing Datadog instrumentation is listed so
  the recommendation covers gaps, not re-recommendations.
- **Justify with capability + evidence, not magnitude** — one sentence per product naming a specific
  file/library and the product's capability for the intent. Never cite figures, percentages, or
  ranking magnitude.
- **Precision over breadth** — a tight, correct bundle beats a long dump. Omitting an unsupported
  product is sufficient; never explain the omission. Honor the guardrail table; never recommend
  services/enablement/SKU strings.
- **Confidence & restraint are first-class output** — a product may be marked low-confidence/optional;
  a thin-confidence goal anchor is Medium/Low and flagged, not auto-High; "few/no products apply" is a
  valid final answer.

---

## Reference: Stack → Products

The axis orthogonal to use-case: **given a concrete technical signal, which products apply,
independent of stated goal.** Two tiers:

- **Foundational** — recommend whenever the signal is present, *regardless* of the user's goal.
  This is the baseline floor.
- **Situational** — recommend only when the use case / intent calls for it (see Use Case → Products
  below). Present here so you know what a signal *enables*, not what to always push.

Detection hints are the files/dependencies/patterns that reveal each signal.

### Backend languages → APM + Profiler + Logs (Foundational)

The seven GA languages (Python through PHP) have a GA APM tracer **and** a Continuous Profiler
(profiler ships inside the tracer) — these are foundational. Rust and C/C++ are the exceptions:
their tracing/profiling is Preview/manual, so treat them as **situational**, not foundational.

| Signal | Detection hint | Products | Notes |
|---|---|---|---|
| Python | `requirements.txt`, `pyproject.toml`, `Pipfile`, `*.py` | APM + Profiler + Logs | GA `ddtrace`, broad auto-instrumentation |
| Node.js | `package.json`, `*.js/*.ts` | APM + Profiler + Logs | GA `dd-trace` |
| Java / JVM (Kotlin, Scala) | `pom.xml`, `build.gradle`, `*.java/*.kt` | APM + Profiler + Logs | GA `-javaagent` |
| Go | `go.mod`, `*.go` | APM + Profiler + Logs | GA `dd-trace-go`; instrumentation via contrib/Orchestrion (compiled lang, not zero-touch) |
| Ruby | `Gemfile`, `*.rb` | APM + Profiler + Logs | GA `datadog` gem |
| .NET (C#/F#) | `*.csproj`, `*.sln`, `*.cs` | APM + Profiler + Logs | Profiler **not auto-enabled with APM**, no ARM64, no Lambda |
| PHP | `composer.json`, `*.php` | APM + Profiler + Logs | GA tracer |
| Rust | `Cargo.toml`, `*.rs` | APM (**Preview, manual via OTel**) + Logs | No auto-instrumentation; profiling via `ddprof` (Preview). **Situational**, not foundational |
| C / C++ | `CMakeLists.txt`, `*.cpp/*.c` | Profiler via `ddprof` (Preview) | No auto-APM. **Situational** |

### Web frameworks → strengthen APM; enable AAP (Situational)
Presence of any web framework → **APM** gets HTTP route/request spans out of the box, and the
service is web-facing so **App and API Protection** becomes a situational option.

- Python: Django / Flask / FastAPI · Node: Express / Koa / Nest / Next.js(server) · Java: Spring Boot ·
  Ruby: Rails · PHP: Laravel · Go: Gin / Echo / chi / Fiber · .NET: ASP.NET (Core).

### Frontend frameworks → RUM + Error Tracking + Session Replay (Foundational)
A browser frontend is foundational for the RUM bundle. **Source Map Uploads becomes foundational
the moment a bundler/minifier is present** (otherwise stack traces are unreadable). Product Analytics
is a **situational (explicit-match-only)** add here, not part of the foundational floor — see the
catalog and the digital-experience theme.

| Signal | Detection hint | Notes |
|---|---|---|
| React | `react`/`react-dom`, `*.tsx` | dedicated `@datadog/browser-rum-react` plugin |
| Vue | `vue`, `*.vue` | dedicated `browser-rum-vue` plugin (3.5+) |
| Next.js (client) | `next`, `app/` or `pages/` | dedicated `browser-rum-nextjs` plugin |
| Angular | `@angular/core`, `angular.json` | core SDK + manual `startView` |
| Svelte/SvelteKit | `svelte`, `svelte.config.js` | core SDK, init in `hooks.client.ts` |
| Vanilla JS | `index.html` + `<script>` | core SDK via npm or CDN |
| **Bundler/minifier** | `vite.config.*`, `webpack.config.js`, `esbuild`, `rollup`, `rspack` | → **Source Map Uploads** (foundational alongside any frontend) |

### Mobile → Real User Monitoring (RUM) + Error Tracking (Foundational)
iOS (`*.xcodeproj`, `Podfile`, `*.swift`) · Android (`build.gradle` + `AndroidManifest.xml`, `*.kt`) ·
React Native (`react-native` + `android/`+`ios/`) · Flutter (`pubspec.yaml`, `*.dart`) ·
Unity (`Assets/`, `*.unity`) · Kotlin Multiplatform · Roku.

### Databases → Database Monitoring (Situational); APM DB spans (Foundational, free with APM)
**DBM officially supports: PostgreSQL, MySQL/MariaDB, SQL Server, Oracle, MongoDB** (+ DocumentDB,
ClickHouse). **Key distinction:** a DB client library alone gives you **APM client-side DB spans**
for free (the query as the app sees it). **DBM** is the deep, opt-in product (explain plans, query
samples, locks, engine metrics) — recommend it **when DB/query performance is a concern**, not as
part of every-service baseline.

Detection hints: `pg`/`psycopg2`/`lib/pq`/`pgx` (Postgres) · `mysql`/`mysql2`/`go-sql-driver` ·
`pyodbc`/`Microsoft.Data.SqlClient` (SQL Server) · `cx_Oracle`/`ojdbc` · `mongoose`/`pymongo`/`mongo-go-driver` ·
`DATABASE_URL`, `postgres`/`mysql`/`mongo` service in compose.

### Datastores / messaging → integration + APM spans; DSM for queues (Situational)
Redis · Memcached · Elasticsearch/OpenSearch → APM cache/query spans (foundational) + Agent integration (situational).
**Kafka · RabbitMQ · SQS · SNS · Kinesis · Pub/Sub · IBM MQ · Azure Service Bus · BullMQ** →
**Data Streams Monitoring** (Situational) for end-to-end pipeline latency, consumer lag, and throughput
across services. DSM SDKs: Java, Python, Node.js, .NET, Ruby (Kafka), Go (Kafka).
Also a fit without an explicit broker dependency when the architecture is event-driven: microservices
that hand work to each other asynchronously, sync requests that fan out to background jobs, or Lambda
functions triggered by SQS / SNS / Kinesis. Not for Redis-backed job queues (Sidekiq, Celery on Redis, RQ),
which DSM does not monitor.

### Deployment / platform → Infrastructure / Serverless (Foundational)
| Signal | Detection hint | Products |
|---|---|---|
| Docker | `Dockerfile`, `docker-compose.yml` | Infrastructure Monitoring + Container Monitoring (+ Logs/APM via agent) |
| Kubernetes (EKS/GKE/AKS) | `kind: Deployment`, `Chart.yaml`, `k8s/` | Infra + Container + Logs + APM; **USM** situational |
| AWS ECS / Fargate | `task-definition.json`, `launchType` | Infra + Container + APM + Logs (agent sidecar) |
| AWS Lambda | `serverless.yml`, `template.yaml` (SAM), `cdk.json`, `AWS::Lambda::Function` | **Serverless Monitoring** (+ APM, enhanced metrics, logs) |
| Vercel | `vercel.json`, `.vercel/` | Serverless Monitoring (Vercel integration) |
| GCP Cloud Run | Cloud Run `service.yaml`, `gcloud run` | Serverless Monitoring (serverless/sidecar agent) |
| Azure App Service / Functions | `host.json`, `function.json`, `*.azurewebsites` | Serverless Monitoring (extension / compatibility layer) |
| Bare VM / host | no Dockerfile/k8s; systemd, cloud-init, Ansible | Infrastructure Monitoring + Logs + APM (host agent) |

### Cloud providers → integration (Foundational); CCM + CSM (Situational)
AWS (`boto3`, `~/.aws`, `provider "aws"`) · GCP (`google-cloud-*`, `provider "google"`) ·
Azure (`azure-*`, `provider "azurerm"`). The cloud **integration** (metrics/logs/inventory) is
foundational; **Cloud Cost Management** and **Cloud Security Management (CSPM/CIEM)** are situational
(recommend on cost / security intent).

### IaC → IaC Security / Code Security (Situational, security-gated)
Officially scans **Terraform** (`*.tf`), **CloudFormation** (`template.yaml` w/ `AWS::`), **Kubernetes
manifests**, **Helm** (renders to K8s). CDK/Pulumi synthesize to CFN/TF → scan the synthesized output.

### CI providers → CI Visibility (Situational)
GitHub Actions (`.github/workflows/`) · GitLab CI (`.gitlab-ci.yml`) · Jenkins (`Jenkinsfile`) ·
CircleCI (`.circleci/`) · Buildkite · Azure Pipelines. Cloud CIs use Agentless mode.

### Test frameworks → Test Optimization (Situational)
pytest · jest (jest-circus) · mocha · vitest · junit/testng/spock · playwright (links to RUM) ·
**cypress (manual instrumentation only)** · rspec/minitest · **go test (via Orchestrion)** ·
.NET xUnit/NUnit/MSTest · Swift XCTest.

### LLM / AI libraries → LLM Observability (Foundational for an LLM app — the headline product)
Auto-instrumentation matrix (Python unless noted):

| Library | Auto-support | Detection hint |
|---|---|---|
| anthropic | Python ✅, Node ✅ | `anthropic`, `@anthropic-ai/sdk` |
| openai | Python ✅, Node ✅, Java ✅ | `openai` |
| langchain | Python ✅, Node ✅ | `langchain`, `@langchain/*` |
| langgraph | Python ✅ | `langgraph` |
| vercel-ai | Node ✅ | `ai` + `@ai-sdk/*` |
| amazon-bedrock | Python ✅, Node ✅ | `bedrock-runtime`, `@aws-sdk/client-bedrock-runtime` |
| vertexai / google-genai | Python ✅, Node ✅ | `vertexai`, `google-genai`, `@google/genai` |
| crewai / openai-agents / litellm / pydantic-ai / google-adk / mcp | Python ✅ | resp. package name |
| llamaindex | ✗ not auto (manual SDK / OTel) | `llama-index`, `llamaindex` |

Also auto-supported (Python): Claude Agent SDK, Strands Agents, vLLM.

### Networking → NDM vs CNM (Situational)
- **SNMP / physical or virtual network devices** (routers, switches, firewalls) → **Network Device
  Monitoring**. Hints: `snmp.d/conf.yaml`, device IPs/OIDs, `community_string`, NetFlow config.
- **Service mesh / Istio / Envoy** → **Cloud Network Monitoring** (+ USM). Hints: `istio-proxy`
  sidecars, `VirtualService`/`DestinationRule` CRDs, `envoy.yaml`. (This is CNM, **not** NDM.)

### Existing Datadog → suppress, recommend only gaps

| Signal | Already set up | Recommend instead |
|---|---|---|
| `datadog.yaml` / `datadog-values.yaml` | Agent installed | Disabled sub-features (`logs_enabled: false` → Logs) |
| `dd-trace`/`ddtrace`/`datadog` tracer dep | APM present | Adjacent gaps: Profiler, DBM, AAP |
| `DD_*` env vars | Unified tagging / partial config | The missing vars (`DD_SERVICE` set, no `DD_PROFILING_ENABLED` → Profiler) |
| `@datadog/browser-rum*` | Browser RUM live | Source Map Uploads, Session Replay rate, Error Tracking |
| `@datadog/mobile-*`, `dd-sdk-android*` | Real User Monitoring (RUM) live | Error Tracking + symbol upload |
| `ddtrace[llmobs]`, `DD_LLMOBS_ENABLED` | LLM Obs live | verify framework integration captured |

### Foundational baseline (the floor, before use-case tailoring)

| If the codebase has… | Always recommend |
|---|---|
| Any backend service | **APM + Log Management + Continuous Profiler** (Rust/C/C++ excepted — tracing Preview/manual) |
| Any web frontend | **RUM + Error Tracking + Session Replay**; **Source Maps** if bundled (Product Analytics only on explicit match) |
| Any mobile app | **Real User Monitoring (RUM) + Error Tracking** |
| Any container / Docker | **Infrastructure Monitoring** (+ Container Monitoring) |
| Any Kubernetes | **Infrastructure + Container + Logs + APM** |
| Any serverless function | **Serverless Monitoring** |
| Any LLM/AI app | **LLM Observability** as the headline (+ APM + Logs) |
| Any cloud account | the matching **cloud integration** |

> Foundation ≠ headline. These are the assumed floor. When the user states a goal, lead with a
> **differentiator** from the Use Case section — a product with **defining** (or **strong**)
> differentiation for that intent — **when a well-supported one exists**, and present the foundation
> beneath it. When no well-supported differentiator applies, leading with the foundation is the
> correct answer; don't manufacture a fake headline to crowd it out.

---

## Reference: Use Case → Products

This section turns a **stated goal or business intent** into the Datadog products that fit it.
Its companion (Stack → Products above) maps the codebase; read both and reconcile — intent sets the
headline, the stack confirms what's actually buildable.

*Built from Datadog product capabilities and common technology patterns — pairing a stated goal
with the products whose capabilities fit it.*

### The one principle that makes this better than a generic list

> **Foundation is assumed. Lead with differentiation.**

- A handful of products fit **almost every backend service** — Infrastructure Monitoring, Log
  Management, APM. They are the **foundation**: the assumed baseline beneath nearly any answer.
  Presenting them *as the headline* is technically correct but unhelpful.
- **Differentiators** are selective. They show up when an intent specifically calls for them —
  and surfacing the differentiator a generic answer would miss is the whole value of this map.
- So: name the foundation briefly beneath, and **lead with the product that is characteristic of
  the user's intent** — when a well-supported one exists.

### Guardrails (read before recommending)

1. Encode rank/tier, not magnitude. Output **defining / strong / weak-or-none**, never a multiplier.
2. Every intent→product mapping must be explainable from product **capability**. If you can't say
   *why* it serves the intent, don't lead with it.
3. **Capability is the basis; defer to stack evidence.** A capability-obvious pick is never vetoed;
   the tiers below inform ordering, not inclusion.
4. **Absence is not evidence.** This map lists characteristic fits, not an exhaustive ranking — a
   product's absence from a theme is not a reason against it.
5. Coarse confidence only — **well-established / emerging / anecdotal** — a stability judgment,
   never a count.
6. No numbers, names, or quotes — ever.
7. Foundation is assumed; lead with a differentiator **when a well-supported one exists**, else
   leading with foundation is correct. Keep the bundle tight (3 products maximum), but it may be 0–1 when
   little or nothing applies.

### The lead rule (this gates everything below — do not skim past it)

**Confidence and tier together decide what may be the headline.** Apply this before naming any lead:

- **defining + well-established** (or capability-obvious) → **may LEAD.** This is the headline.
- **emerging** → **supporting add only.** Include it, but do not anchor the recommendation on it.
- **anecdotal** → **explicit-match-only.** Mention it solely when the user's language is an
  unambiguous match for it; **never make it the headline.**
- **weak-or-none** → foundation or noise. Name it beneath; never lead.

When no anchor clears the bar, leading with foundation is the correct, honest answer — do not
manufacture a differentiated headline to fill the slot.

### Sharp-signal anchors — LEAD when intent matches and the code corroborates

These are the most characteristic intent→product signals. An anchor becomes the headline only when
**both** hold: (1) the user's language matches and the tier/confidence clears the lead rule above,
**and** (2) the codebase actually corroborates it — the relevant SDK / IaC / library / config is
present. Language alone is **not** enough: a security or cost goal on a repo with no cloud/IaC
surface, or an LLM goal with no LLM library, must **not** lead with the cloud/LLM anchor.

| Intent signal in user language | Anchor product | Tier | Confidence |
|---|---|---|---|
| AI / LLM / GenAI / prompts / agents / tokens | **LLM Observability** | defining | well-established |
| security / SIEM / threat detection / compliance | **Cloud SIEM** | defining | well-established |
| cloud posture / misconfig / CSPM / DevSecOps | **Cloud Security Management** | defining | well-established |
| network devices / SNMP / switches / routers / NetFlow | **Network Device Monitoring** | defining | well-established |
| code / supply-chain / SAST / SCA / vulnerabilities | **Code Security** | strong | well-established |
| runtime threat / workload / container security | **Workload Protection** | strong | emerging |
| cloud cost / spend / bill / FinOps | **Cloud Cost Management** | defining | emerging |
| customer-facing / frontend / UX / web vitals | **Real User Monitoring** | defining | well-established |
| slow queries / database / query performance | **Database Monitoring** | defining | well-established |
| AWS-native / CloudWatch / serverless / Lambda / ECS | **Serverless Monitoring** | defining | well-established |

When the user's language is **security-coded** *and the codebase has a cloud/log surface to act on*,
shift decisively to the security suite: lead with Cloud SIEM + Cloud Security Management and bring in
Code Security / App & API Protection / Workload Protection per the specific signal. If there is **no
cloud SDK / IaC / centralized-log surface** in the code, do not lead with SIEM/CSPM; lead with the
*code-level* security products that are supported (**Code Security** for SAST/SCA, **App & API
Protection** for a public API), and name SIEM/CSPM only as conditional adds.

### Intent without a supporting stack (the mismatch rule)

The intent map sets a *candidate* headline; the **stack confirms what is actually buildable**. When
the goal points at an anchor the codebase does not corroborate, the anchor must **not** lead:

- **Pure absence → name the gap, lead with what's supported.**
- **User asserts an out-of-repo resource → conditional, never a lead, never "detected."** A goal that
  *states* "our AWS bill" or "our LLM service" is **not** codebase evidence. Offer the anchor as a
  **Medium/Low conditional**; never mark it High and never write a detected-stack line for it.
- **Partial → scope per product.** Recommend supported sub-products and explicitly decline unsupported
  siblings.

### Intent → products, by theme

Match the user's stated goal/pain to a theme, then recommend the anchor(s) + supporting products.
Foundation (Infra / Logs / APM) is assumed beneath all of these — name it briefly, don't lead with it.

**Security · SIEM · compliance** — confidence: well-established
- Triggers: security, SIEM, threat detection, compliance, SOC 2, FedRAMP, HIPAA, PCI, audit,
  vulnerability, posture, misconfiguration, DevSecOps, PII.
- Lead (only if the code has a cloud/log surface): **Cloud SIEM** + **Cloud Security Management**.
  On a repo with no cloud SDK / IaC / centralized logging, lead with **Code Security** + **App & API
  Protection** instead, and name SIEM/CSPM as conditional adds.
- Strong adds: **Workload Protection** · **Sensitive Data Scanner**.
- Foundation beneath: Log Management; Infra + APM round out.

**AI / LLM observability** — confidence: well-established
- Triggers: LLM, GenAI, AI app, chatbot, agent, RAG, prompt, token usage, model latency/cost; an LLM
  client library in the stack.
- Lead (defining): **LLM Observability**.
- Strong adds: **APM** + **Log Management**.
- Do NOT add RUM / DBM / Source Maps unless independently signaled.

**Network** — confidence: well-established
- Triggers (devices): SNMP, routers, switches, firewalls, NetFlow → Lead: **Network Device Monitoring**.
- Triggers (traffic): service-to-service connectivity, mesh, Istio/Envoy → Strong: **Cloud Network Monitoring**.
- Foundation beneath: Infra + Logs.

**Cloud cost / FinOps** — confidence: emerging
- Triggers: reduce cloud spend, cost visibility, cost allocation, FinOps, "bill is too high."
- Lead with **Cloud Cost Management** only when cloud infra/IaC is detected. On a repo with no cloud
  SDK and no IaC, name CCM as a conditional add and lead with foundation.
- Strong add: **Infrastructure Monitoring** (right-sizing from utilization).

**Digital experience · frontend · customer-facing** — confidence: well-established
- Triggers: end-user experience, frontend performance, UX, web vitals, conversion, session,
  "customers are complaining."
- Lead (defining): **Real User Monitoring** + **Session Replay**.
- Strong adds: **Error Tracking** · **Product Analytics** (emerging) · **Synthetics** · **Source Maps**
  when JS is bundled.
- Foundation beneath: APM + Logs.

**Cloud migration (Azure / hybrid / on-prem→cloud)** — confidence: well-established
- No single defining anchor. Strong adds: **Network Device Monitoring** · **Cloud Cost Management** ·
  **Cloud Network Monitoring** · **Synthetics** · **On-Call**.
- Foundation beneath: matching cloud integration + Infra + Logs + APM.

**AWS-native / serverless / ECS · CloudWatch displacement** — confidence: well-established
- Triggers: cloudwatch / lambda / ecs / fargate language; replacing CloudWatch.
- Lead (defining): **Serverless Monitoring**.
- Strong adds: **Custom Metrics** · **Cloud Cost Management**.
- Foundation beneath: AWS integration + APM + Logs.

**Incident response / MTTR** — confidence: emerging
- Triggers: MTTR, MTTD, reduce downtime, on-call, paging, alert fatigue, faster resolution.
- No defining anchor. Strong adds: **Incident Management** · **On-Call** · **Error Tracking**.
- **APM** does real work here (root-cause traces) — name it as doing work, not just baseline.

**Tool consolidation / platform unification** — confidence: well-established
- Triggers: consolidate, "single pane of glass," fragmented tooling, too many tools, unify monitoring.
- No anchor — it's the breadth play. Foundation + long-tail: **CI Visibility**, **Continuous Profiler**,
  **LLM Observability**, **Universal Service Monitoring**, **Data Observability**.

**Database / query performance** — confidence: well-established
- Triggers: slow queries, database performance, query latency, explain plans, engine performance.
- Lead (defining): **Database Monitoring**.
- Strong add: **APM** — DB spans tie each query back to the calling service.

**Greenfield / new launch** — confidence: emerging
- Triggers: new product, launching, greenfield, MVP, "before users hit it."
- No defining anchor. Strong adds: **Synthetics** · **RUM**.
- Anecdotal (explicit-match-only): **Product Analytics**.
- Foundation beneath: APM + Logs + Infra.

**Infra / Kubernetes performance** — confidence: well-established (flat / all-foundation)
- Triggers: infrastructure performance, resource utilization, capacity, k8s health.
- No exotic differentiator. **Infrastructure Monitoring** leads, with **Cloud Network Monitoring** and
  **Database Monitoring** as modest adds where those signals appear.

**Alerting / "know when" / notification** — intent-driven
- Triggers: "know when," "alert me when," "notify me," "get paged when," "detect when X happens."
- Lead with capability: **Monitors & Alerting** — the direct answer to "know when."
- Add: **Error Tracking** + **Log Management**. "Single pane" → **Dashboards**; "SLOs" → **SLOs**.

**Full-stack / frontend↔backend correlation** — confidence: well-established (mostly foundation)
- Triggers: correlate frontend and backend, end-to-end visibility, distributed tracing.
- Lead with the assembly: **APM** + **RUM** + **Log Management**, plus **Error Tracking** and
  **Incident Management**. This is the foundation, well-assembled — say so rather than inventing a
  differentiator.

### Intent phrasings → products (identity-free cues)

- "nothing in place for security logging / SIEM; needs to meet a compliance standard"
  → Cloud SIEM (+ Workload Protection for stricter regimes).
- "manages many external APIs and faces an audit requiring stronger API security"
  → Code Security + App & API Protection.
- "lacks visibility at the container level and wants stronger security posture"
  → Cloud Security Management.
- "recently migrated to a cloud provider and lacks visibility into the new environment"
  → Network Device Monitoring + Cloud Cost Management + Cloud Network Monitoring.
- "running on CloudWatch which isn't ideal; disconnected tooling over a serverless stack"
  → Serverless Monitoring (+ Custom Metrics, Cloud Cost Management).
- "no insight into end-user behavior; wants to see user sessions and identify friction"
  → RUM + Session Replay + Product Analytics.
- "siloed monitoring causing slow detection/resolution; no visibility front-end to back-end"
  → RUM + APM + Incident Management.
- "consolidating a patchwork of monitoring tools to reduce cost and overhead"
  → consolidation play (foundation + long-tail).
- "wants observability into an LLM/AI application"
  → LLM Observability (+ APM + Logs).
- "wants to proactively monitor uptime and key user flows / core web vitals"
  → Synthetics + RUM.

---

## Reference: Product Catalog

This is the **controlled vocabulary** for recommendations. Always name products using the
**Canonical name** column. Use the **Aliases** to recognize a product when the user or the codebase
refers to it by another name.

> **Commonality** is a coarse mainstream-vs-niche marker, **not** a ranking weight and **not** a
> fitness score. A **niche** product can be exactly the right call; a **mainstream** product is
> never auto-recommended just because it's common. Use Commonality only to gauge how confidently a
> match can be inferred, never to order or weight a recommendation.

- **mainstream** — broadly adopted; safe to recommend on a clear match.
- **niche** — appears rarely; recommend **only** on an explicit, unambiguous match, never as a guess.

### Recommendable products by category

**Core observability (foundation)**
| Canonical name | Commonality | Aliases / how it shows up |
|---|---|---|
| **Infrastructure Monitoring** | mainstream | Infra, host monitoring, container monitoring, server monitoring, Orchestrator Explorer |
| **Log Management** | mainstream | Logs, logging, log analytics, log ingestion/indexing, Flex Logs, Observability Pipelines |
| **APM** | mainstream | Application Performance Monitoring, distributed tracing, tracing, traces, spans, ddtrace/dd-trace |
| **Continuous Profiler** | niche | Profiler, profiling, code profiling, flame graphs, `DD_PROFILING_ENABLED` |

**Digital experience (frontend / mobile / end-user)**
| Canonical name | Commonality | Aliases / how it shows up |
|---|---|---|
| **Real User Monitoring (RUM)** | mainstream | RUM, browser monitoring, frontend/client-side monitoring, mobile RUM, `@datadog/browser-rum` |
| **Session Replay** | RUM add-on | session replay, replay; capability of the RUM SDK |
| **Error Tracking** | niche | error grouping, exception tracking, crash reporting (mobile) |
| **Product Analytics** | niche | PA, funnels, retention analysis, user-behavior analytics, experimentation |
| **Synthetic Monitoring** | mainstream | Synthetics, synthetic tests, API tests, browser tests, uptime checks, multistep API tests |
| **Source Map Uploads** | RUM/ET enabler | source maps, sourcemaps, symbolication (needed when JS is minified/bundled) |

**Data layer**
| Canonical name | Commonality | Aliases / how it shows up |
|---|---|---|
| **Database Monitoring (DBM)** | mainstream | query monitoring, slow queries, explain plans, query performance, Postgres/MySQL/SQL Server/Oracle/Mongo monitoring |
| **Data Streams Monitoring (DSM)** | niche | Kafka/RabbitMQ/SQS/SNS/Kinesis/Pub/Sub monitoring, queue lag, consumer lag, pipeline latency, streaming monitoring, event-driven architecture |
| **Data Observability** | niche | Data Jobs Monitoring (DJM), Spark/Databricks monitoring, data quality monitoring |

**Network**
| Canonical name | Commonality | Aliases / how it shows up |
|---|---|---|
| **Network Device Monitoring (NDM)** | mainstream | SNMP monitoring, NetFlow, switch/router/firewall monitoring, network devices, Network Path |
| **Cloud Network Monitoring (CNM)** | mainstream | NPM, Network Performance Monitoring, network flows, service-to-service traffic, service mesh traffic |
| **Universal Service Monitoring (USM)** | niche | service monitoring without code, eBPF service map, instant service catalog telemetry |

**Cloud & cost**
| Canonical name | Commonality | Aliases / how it shows up |
|---|---|---|
| **Serverless Monitoring** | mainstream | Lambda monitoring, Fargate tasks, serverless functions/apps, FaaS, Cloud Run / Azure Functions monitoring |
| **Cloud Cost Management (CCM)** | mainstream | cost monitoring, cloud spend, cost optimization, FinOps, Cloudcraft, cost allocation |

**Security**
| Canonical name | Commonality | Aliases / how it shows up |
|---|---|---|
| **Cloud SIEM** | mainstream | SIEM, security monitoring, threat detection, security logs, security analytics |
| **Cloud Security Management (CSM)** | mainstream | CSPM, Cloud Security Posture Management, CIEM, misconfigurations, DevSecOps, posture management |
| **Workload Protection** | niche | CWS, Cloud Workload Security, runtime threat detection, container runtime security |
| **App and API Protection (AAP)** | niche | ASM, Application Security Management, WAF, RASP, API security, app-layer threat protection |
| **Code Security** | mainstream | SAST, IAST, SCA, secret scanning, IaC Security, supply-chain security, app sec testing |
| **Sensitive Data Scanner (SDS)** | niche | SDS, PII scanning, data redaction, sensitive-data detection |

**Software delivery**
| Canonical name | Commonality | Aliases / how it shows up |
|---|---|---|
| **CI Visibility** | niche | CI/CD Visibility, Pipeline Visibility, CI pipeline monitoring |
| **Test Optimization** | niche | Test Visibility, flaky-test detection, test analytics, Test Impact Analysis |

**LLM / AI**
| Canonical name | Commonality | Aliases / how it shows up |
|---|---|---|
| **LLM Observability** | niche | LLM Obs, LLMObs, AI/GenAI observability, prompt/model monitoring, token & cost tracking |

**Service management**
| Canonical name | Commonality | Aliases / how it shows up |
|---|---|---|
| **Incident Management** | niche | IM, incident response, postmortems, Enterprise Incident Response |
| **On-Call** | niche | paging, on-call scheduling, alert escalation |
| **Workflow Automation** | niche | workflows, runbook automation, automated remediation |
| **Event Management** | niche | event correlation, alert correlation, event pipeline |

**Other (niche — match explicitly only)**
| Canonical name | Commonality | Aliases / how it shows up |
|---|---|---|
| **Custom Metrics** | niche | custom metrics/events, DogStatsD metrics, MetricsWithoutLimits |
| **GPU Monitoring** | niche | NVIDIA/GPU metrics |
| **IoT Monitoring** | niche | device/edge monitoring |
| **Feature Flags** | niche | feature flagging, feature toggles |
| **App Builder** | niche | low-code internal apps |
| **Bits AI** | niche | AI SRE, AI incident investigations |
| **CoScreen** | niche | collaborative screen sharing, pair debugging |

**Platform capabilities (Monitors & Alerting / Dashboards / SLOs — recommend by intent)**
These are core Datadog capabilities available across the platform; recommend them **by intent**:

| Capability | Recommend when the goal is… |
|---|---|
| **Monitors & Alerting** | "know when", "alert me", "notify me", "get paged when", "detect when X happens" |
| **Dashboards** | "see it all in one view", "single pane of glass", "visualize", "build a dashboard" |
| **SLOs** | "track SLAs / SLOs", "error budget", "reliability targets", "uptime guarantee" |

### Never recommend (services / enablement / SKU / pricing strings)

These are professional services / enablement / training / events — **not** Datadog products:

- **(Services / Non-Product)** bucket: DASH Tickets, Implementation Services (any package),
  Premium Enablement, TEM Bootcamp.
- **Rule:** treat any item whose name contains *Bootcamp*, *Enablement*, *Implementation Services*,
  *Tickets*, *Training*, *Onboarding Services*, or *Support Package* as non-recommendable.
- Also do not surface internal SKU / pricing-tier names or anything prefixed *Deprecated –* /
  *Legacy –*. Always recommend the **Canonical product name** instead.
