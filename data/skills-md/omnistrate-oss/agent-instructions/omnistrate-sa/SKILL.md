---
name: omnistrate-sa
description: Guide users through designing application architectures from scratch for SaaS deployment on Omnistrate, including deployment-model selection (hosted/BYOC/BYOC-K8s/air-gapped) and monetization model (Stripe end-to-end billing vs custom metering export for marketplaces, Chargebee, or non-built-in pricing dimensions). Focuses on technology selection, domain-specific architecture patterns, compliance and SLA requirements, and iterative compose spec development. Output may be a production-ready Docker Compose spec handed off to the FDE skill, or a ServicePlanSpec skeleton recommendation (when the stack uses Helm, Terraform, or a Kubernetes operator). Do NOT use when the user already has a deployable artifact (→ omnistrate-fde; operator services → omnistrate-operator) or needs to debug a failed instance (→ omnistrate-sre).
---

# Omnistrate Solutions Architect

Any Omnistrate commands referenced here or in the reference use the `omnistrate-ctl` CLI (alias `omctl`) — install and authenticate with `omnistrate-ctl login` first. An Omnistrate MCP server exposes equivalent tools (`mcp__ctl__*`); use those only if the user explicitly asks to work through MCP.

**Check platform capabilities before you design around them.** Design-time claims about what Omnistrate supports (autoscaling, backups, multi-zone, tenancy modes, GPU instance types) must be confirmed, not assumed — a design built on a capability that doesn't exist costs a whole onboarding cycle to unwind. `omctl docs` answers these without a login (network access is still required):

| Need | Command |
|---|---|
| Every compose tag / `x-omnistrate-*` extension | `omctl docs compose-spec` |
| One extension's capabilities and examples | `omctl docs compose-spec "x-omnistrate-capabilities"` |
| One extension's authoritative schema (enum values, required fields) | `omctl docs json-schema x-omnistrate-capabilities` |
| ServicePlanSpec sections, when the output is Helm/Terraform/operator | `omctl docs plan-spec` |
| `$sys.*` system parameters | `omctl docs system-parameters` |
| Whether the platform supports something at all | `omctl docs search "<capability>" --limit 15` |

Add `-o json` for machine-readable output. The JSON schema is the arbiter for what values a field accepts — read it before promising an ISV a specific tenancy mode, instance type, or autoscaling metric.

## When to Use This Skill

**Use this skill when**:
- Designing new SaaS applications from scratch and choosing technology stacks
- Architecting microservices and selecting databases, caches, message queues
- Understanding domain-specific requirements (AI/ML, analytics, APIs, data platforms)
- Evaluating compliance needs (SOC2, HIPAA, GDPR, data residency)
- Determining customer SLA requirements and availability zones
- Making architectural decisions informed by Omnistrate's tenancy and deployment models
- Iteratively developing and refining a Docker Compose specification
- **User has a compose file with `build:` contexts** that only runs locally
- **Converting local development compose** (build contexts) to cloud-ready compose (image registries)
- **Setting up container image registries** and authentication for private images

**Do NOT use this skill when**:
- User already has a compose spec with ALL services using `image:` references (no `build:` contexts) AND images are accessible in registries → Use **FDE skill** instead
- User needs to debug failed deployments → Use **SRE skill** instead

## Relationship to Other Skills

```
SA Skill                    FDE Skill                   SRE Skill
┌─────────────────┐        ┌──────────────────┐       ┌──────────────┐
│ Design app from │   →    │ Transform compose│   →   │ Debug failed │
│ scratch         │        │ to Omnistrate    │       │ deployments  │
│                 │        │ native           │       │              │
│ • Tech choices  │        │ • x-omnistrate-* │       │ • Workflows  │
│ • Architecture  │        │   extensions     │       │ • Logs       │
│ • Compose spec  │        │ • API params     │       │ • kubectl    │
│ • Domain needs  │        │ • Service plans  │       │              │
└─────────────────┘        └──────────────────┘       └──────────────┘
     This skill            Handoff to FDE              If issues arise
```

**Output**: A vanilla Docker Compose spec optimized for Omnistrate's capabilities (tenancy, deployment models, scaling) but WITHOUT `x-omnistrate-*` extensions yet.

## Core Responsibilities

As a Solutions Architect, you will:

1. **Understand domain and requirements** - Ask questions about business model, target customers, compliance, SLAs
2. **Select appropriate technologies** - Choose databases, frameworks, languages, infrastructure components
3. **Design service architecture** - Define microservices, data flow, dependencies, state management
4. **Consider Omnistrate deployment models** - Design for Hosted, BYOC-Account, BYO-VPC, BYOC PrivateLink, BYOC-K8s, or Air-gapped from the start (see Phase 1 discovery table)
5. **Plan for tenancy** - Architecture decisions that support shared, siloed, or hybrid tenancy
6. **Build compose spec iteratively** - Start simple, validate, add complexity, refine
7. **Prepare for FDE handoff** - Ensure compose spec is ready for Omnistrate-native transformation

## Architectural Workflow

### Phase 1: Discovery & Requirements

**Ask clarifying questions** to understand the user's needs:

#### Business Context
- What problem does your SaaS solve? (domain: AI/ML, analytics, APIs, databases, etc.)
- Who are your target customers? (startups, mid-market, enterprise, developers)
- What is your pricing model? (freemium, usage-based, tiered plans)
- What customer segments need different deployment models? (SaaS, BYOC, On-Premise)

#### Deployment Model Discovery (ask BEFORE technology selection)

Ask these questions before discussing tech stack — the answers determine not just where instances run, but what artifact format (compose vs. helm vs. operator) makes sense and which reference to use at handoff time.

1. **Who are your customers?** (segment/industry: startups, enterprise, regulated sectors such as healthcare/finance/defense?)
2. **Data sovereignty or compliance demands?** Do any customers require their data to stay in their own cloud account, or in a specific geography?
3. **Cloud account / cluster ownership?**
   - Do any customers require instances to run in *their* own cloud account (AWS/GCP/Azure)? → BYOC-Account
   - Do any customers require deployment into an *existing* VPC or private network they control? → BYO-VPC
   - Do any customers require a no-public-egress guarantee (PrivateLink)? → BYOC PrivateLink
   - Do any customers want to bring their own Kubernetes cluster (EKS on-prem, OpenShift, Rancher)? → BYOC-K8s
   - Do any customers operate fully disconnected environments (government, defense, no internet)? → Air-gapped
4. **Connectivity constraints?** Any customers with air-gap, firewall, egress, or PrivateLink requirements?

**Map answers to deployment model(s):**

| Customer says… | Deployment model | Spec block |
|----------------|-----------------|------------|
| "Just host it for me" | **Hosted** | `hostedDeployment` |
| "Run it in our AWS/GCP/Azure account" | **BYOC-Account** | `byoaDeployment` |
| "Deploy into our existing VPC/VNet" | **BYO-VPC** | `byoaDeployment`; the customer supplies their VPC ID as the `cloud_provider_native_network_id` input parameter at instance create (portal, or `--param`/`--param-file`) |
| "We need PrivateLink — no public endpoints" | **BYOC PrivateLink** | `byoaDeployment`; PrivateLink is enabled at account onboarding (`account customer create --private-link`), not a spec key |
| "We run OpenShift/EKS on-prem, cluster has outbound egress" | **BYOC-K8s** | `byoaDeployment` (`--cloud-provider byoc-onprem`) |
| "Defense/air-gapped, no internet whatsoever" | **Air-gapped** | `onPremDeployment` |

> A service can offer several models (e.g. hosted starter/pro tiers plus a BYOC enterprise tier), but **each deployment model requires its own separate Plan** — never a single plan declaring both `hostedDeployment` and `byoaDeployment`, and never offer to build one plan serving multiple models. Confirm which model(s) to support before proceeding.
>
> For every `byoaDeployment` variant (BYOC-Account, BYO-VPC, PrivateLink, BYOC-K8s), the spec's account configuration is always an **AWS** account config designated as the **"Control Plane" account** — irrespective of which cloud the customers deploy into. The onboarding skill (FDE/operator) asks the user for that account explicitly at intake; note it in the handoff so it isn't defaulted.
>
> Architecture-level implications per model (networking, licensing, backup, upgrade agility) are tabulated in `SOLUTIONS_ARCHITECT_REFERENCE.md` §"Deployment Model Implications for Architecture". Spec blocks and account-onboarding flows are authored later, during onboarding — do not hand-write them at design time.

**Record the chosen model(s) — you will name them explicitly in the handoff summary.**

#### Monetization (ask during discovery — it shapes the architecture)
- **How do you charge, and who takes the payment?** (Stripe / a cloud
  marketplace / an existing billing system like Chargebee / not billing yet)
- **What do you charge for?** Omnistrate's built-in billable dimensions are
  cpu, memory, storage, replica, and deploymentCell. Anything else — per-seat,
  per-request, per-document, per-GB-processed — cannot be priced natively.
- Map the answers:
  - *Stripe + built-in dimensions suffice* → **end-to-end billing** (`pricing` +
    `billingProviders`; Omnistrate meters, invoices, collects).
  - *Extra dimensions, custom aggregation/rating, or any non-Stripe provider
    (AWS/GCP/Azure Marketplace, Chargebee, Clazar, in-house)* → **custom
    metering**: usage exports to the ISV's own bucket and **an exporter service
    becomes part of the architecture** — call that out now, not at go-live.
- Note the choice in the handoff summary; the onboarding skill implements it.
  Architecture-level implications: `SOLUTIONS_ARCHITECT_REFERENCE.md`
  §"Metering & Billing".

#### Technical Requirements
- What is your expected scale? (users, requests/sec, data volume)
- What are your performance requirements? (latency, throughput)
- Do you have existing infrastructure or starting from scratch?
- What programming languages/frameworks does your team know?
- Any existing codebases to integrate?

#### Compliance & Security
- What compliance certifications do you need? (SOC2, HIPAA, GDPR, ISO 27001)
- Any data residency requirements? (EU data in EU, etc.)
- What industries are you targeting? (healthcare, finance, etc.)
- Do customers need data isolation? (dedicated infrastructure, encryption)

#### SLA & Availability
- What uptime SLA do you promise? (99.9%, 99.99%)
- What is acceptable downtime? (planned maintenance windows)
- Need multi-region for disaster recovery?
- What is your RTO (Recovery Time Objective) and RPO (Recovery Point Objective)?

### Phase 2: Technology Selection

Based on requirements, recommend appropriate technology stack.

#### Application Framework Selection

**API/Web Services**:
- **Node.js/Express**: Fast I/O, JavaScript ecosystem, good for APIs
- **Python/FastAPI**: ML/AI workloads, data science, rapid development
- **Go**: High performance, concurrent workloads, system services
- **Java/Spring Boot**: Enterprise, complex business logic, banking/finance
- **.NET/ASP.NET**: Microsoft ecosystem, Windows integration, enterprise

**Considerations**:
- Team expertise (choose familiar stack for faster iteration)
- Performance requirements (Go/Rust for low latency, Python for ML)
- Ecosystem maturity (npm, PyPI, Maven availability)
- Containerization ease (Alpine base images, build times)

#### Database Selection

**Relational (ACID, structured data)**:
- **PostgreSQL**: General purpose, JSON support, extensions, most versatile
- **MySQL/MariaDB**: High read throughput, WordPress/PHP ecosystems
- **SQL Server**: Microsoft stack, enterprise features
- **CockroachDB**: Distributed SQL, global scale, Postgres-compatible

**Document/NoSQL**:
- **MongoDB**: Flexible schema, rapid iteration, JSON documents
- **DynamoDB**: Serverless, AWS-native, predictable performance
- **Cassandra**: Write-heavy, time-series, high availability

**Time-Series**:
- **TimescaleDB**: PostgreSQL extension, SQL interface
- **InfluxDB**: Purpose-built, high ingestion rates
- **Prometheus**: Metrics, monitoring data

**Graph**:
- **Neo4j**: Relationships, social networks, recommendations
- **ArangoDB**: Multi-model, graph + document

**Selection criteria**:
- Data model fit (relational vs document vs graph)
- Query patterns (complex joins vs key-value lookups)
- Consistency requirements (ACID vs eventual consistency)
- Scale expectations (GB vs TB vs PB)
- Operational complexity (managed vs self-hosted)

#### Cache/Session Store Selection

**In-Memory Cache**:
- **Redis**: Versatile, pub/sub, data structures, most common
- **Memcached**: Simple key-value, high performance, less features
- **Valkey**: Redis fork, open-source alternative

**Use cases**:
- Session storage (user login sessions)
- Database query caching (reduce DB load)
- Rate limiting (API throttling)
- Real-time leaderboards, counters

#### Message Queue/Streaming Selection

**Message Queues**:
- **RabbitMQ**: AMQP protocol, reliable, work queues
- **Apache Kafka**: High throughput, event streaming, log aggregation
- **NATS**: Lightweight, low latency, microservices
- **Amazon SQS**: Serverless, AWS-native

**Use cases**:
- Asynchronous processing (email sending, report generation)
- Event-driven architectures (microservices communication)
- Log aggregation (centralized logging)
- Real-time analytics (stream processing)

#### Storage Selection

**Object Storage**:
- **S3/GCS/Azure Blob**: Media files, backups, data lakes
- **MinIO**: Self-hosted S3-compatible

**File Storage**:
- **NFS**: Shared filesystems
- **EFS/Cloud Filestore**: Managed network filesystems

**Use cases**:
- User uploads (images, documents)
- Backups and archives
- ML model storage
- Static assets (CDN origin)

### Phase 3: Architecture Design

Design the service architecture based on domain patterns.

#### Pattern 1: Simple API Service
**Domain**: REST APIs, microservices, webhooks
```
Internet → API Server → Database
              ↓
            Cache (optional)
```

**Components**:
- API server (Node.js/Python/Go/Java)
- PostgreSQL/MySQL (relational data)
- Redis (optional: caching, rate limiting)

**Tenancy considerations**:
- Shared tenancy: One API service, logical tenant isolation in DB (tenant_id column)
- Siloed tenancy: Separate database per tenant, shared application tier

#### Pattern 2: Three-Tier Web Application
**Domain**: SaaS apps, dashboards, admin panels
```
Internet → Load Balancer → Web Tier (static) → App Tier (API) → Database
                                                     ↓
                                                  Cache
```

**Components**:
- Web tier: NGINX/Apache (static assets, reverse proxy)
- App tier: Backend API (Node.js/Python/Java)
- Database: PostgreSQL/MySQL
- Cache: Redis

**Tenancy considerations**:
- Shared: Shared app tier + database, tenant routing by subdomain
- Siloed: Separate app + DB per tenant (enterprise customers)

#### Pattern 3: Data Processing Pipeline
**Domain**: ETL, analytics, data warehousing
```
Data Sources → Ingestion API → Message Queue → Workers → Database/Data Warehouse
                                     ↓
                                 Object Storage
```

**Components**:
- Ingestion: FastAPI/Go service (data collection)
- Queue: Kafka/RabbitMQ (buffering, reliability)
- Workers: Python/Java (data transformation)
- Storage: PostgreSQL + S3 (structured + raw data)

**Tenancy considerations**:
- Shared queue with tenant partitioning
- Isolated workers per tenant for security

#### Pattern 4: AI/ML Service
**Domain**: Model serving, inference APIs, ML platforms
```
Internet → API Gateway → Inference Service (GPU) → Model Storage (S3)
                              ↓
                         Result Database
```

**Components**:
- API: FastAPI/Flask (REST endpoints)
- Inference: GPU-enabled containers (CUDA, TensorFlow, PyTorch)
- Storage: S3/GCS (model weights)
- Database: PostgreSQL (metadata, results)
- Cache: Redis (model caching, request dedup)

**Tenancy considerations**:
- GPU isolation per tenant (cost optimization)
- Shared inference tier with request queuing

#### Pattern 5: Real-Time Analytics
**Domain**: Dashboards, metrics, monitoring
```
Events → Stream Processor → Time-Series DB → Query API → Visualization
            ↓
         Object Storage (archives)
```

**Components**:
- Stream: Kafka/NATS
- Processor: Flink/custom workers
- Database: TimescaleDB/InfluxDB
- API: GraphQL/REST (query layer)

**Tenancy considerations**:
- Tenant data partitioning in time-series DB
- Shared stream with tenant tagging

### Phase 4: Deployment Model Planning

**Design for Omnistrate's deployment models from the start**, using the branch
taxonomy from the Phase 1 discovery table: **Hosted / BYOC-Account / BYO-VPC /
BYOC PrivateLink / BYOC-K8s / Air-gapped**. Confirm the chosen model(s) against
that table (§Deployment Model Discovery) before making architecture decisions.

Spec blocks, `deployment:` fields, and account-onboarding flows are authored
during onboarding, not at design time. The architecture-level
constraints each model imposes (networking, licensing, backup storage, upgrade
agility) are tabulated in `SOLUTIONS_ARCHITECT_REFERENCE.md` §"Deployment Model
Implications for Architecture" — read it alongside this phase. The notes below
are only the design decisions to make while shaping the compose/architecture.

#### Hosted (Most Common)
**Architecture**: All infrastructure in *your* (provider) cloud account; shared
or dedicated resources per tenant; you manage everything.

**Design decisions**:
- Use shared databases with tenant_id isolation (cost-effective)
- Load balancers for multi-tenant access
- Consider Custom Networks for enhanced isolation (hosted-only; VPC per customer)

**Best for**: Startups, mid-market, most B2B SaaS

#### BYOC-Account (Bring Your Own Cloud — customer account)
**Architecture**: Deploy into the customer's own cloud account (AWS/GCP/Azure/
OCI/Nebius); customer owns the account, you operate the service; data stays in
the customer's environment.

**Design decisions**:
- Minimize cross-account dependencies; use the customer's IAM roles via the bootstrap role
- Enable licensing (`x-customer-integrations.licensing`) — software runs outside your perimeter
- Assume customer-account object storage for backups; confirm bootstrap-role write access

**Best for**: Enterprise customers, data sovereignty, regulated industries

#### BYO-VPC (BYOC into an existing customer network)
**Architecture**: BYOC-Account, but deployed into an *existing* customer VPC/VNet
instead of a fresh one; the customer controls routes, endpoints, and egress.

**Design decisions**:
- Design endpoints for customer-controlled routing and egress governance
- Same licensing/backup considerations as BYOC-Account
- The VPC ID is supplied as the `cloud_provider_native_network_id` input parameter at instance create

**Best for**: Customers with centralized firewall/egress governance

#### BYOC PrivateLink (zero public exposure)
**Architecture**: BYOC with all control traffic over AWS PrivateLink; no public
endpoint on the customer's cluster. Selected per-account at onboarding.

**Design decisions**:
- Use INTERNAL `networkingType`; expose only what the customer VPC can reach
- Same licensing/backup considerations as BYOC-Account

**Best for**: Regulated finance/government with no-public-egress policies

#### BYOC-K8s (customer-managed Kubernetes)
**Architecture**: Deployed into a customer-*managed* Kubernetes cluster; the
customer owns nodes, storage, DNS, and routing; the cluster stays **connected**
to your control plane over outbound mTLS/gRPC. Omnistrate provisions no infra.

**Design decisions**:
- Expose services via `$sys.network.internalClusterEndpoint` (INTERNAL); use `externalClusterEndpoint`/PUBLIC only if the cluster has a working load balancer
- For an HTTP/HTTPS app there is **no platform cloud LB** — design for ClusterIP + the customer's own ingress, and take the external hostname as an apiParameter
- Validate customer StorageClasses, ingress controllers, and DNS during onboarding; never design around a cloud-specific StorageClass name
- Cluster-level components (ingress, cert-manager, monitoring) belong in deployment-cell amenities, not the plan
- Confirm the cluster is allowed **outbound** egress to your control plane, image registries, and chart registries — if not, this is an air-gapped design, not BYOC-K8s
- Enable licensing — same as BYOC-Account

**Best for**: Customers standardizing on EKS/AKS/GKE/OpenShift/Rancher/k3s

**Hand off with**: the FDE skill's `BYOC_K8S_REFERENCE.md` — it carries the
onboarding flow, egress allowlist, endpoint patterns, and the BYOC-K8s vs
air-gapped disambiguation the build phase needs.

#### Air-gapped (self-contained installer)
**Architecture**: A self-contained installer artifact the customer runs locally,
including fully disconnected networks — **no live control-plane connection**.
The installer packages a Helm chart (non-Helm stacks must first be bundled into
one). Uses the `onPremDeployment` spec block.

**Design decisions**:
- No dependence on live internet, remote telemetry, or automatic image pulls
- Use `INSTALLER_EMBED` pull mode so images are bundled into the artifact
- Backup action hooks write to customer-local storage; do not assume an S3-style object store
- The offline license does **not** auto-rotate — plan a license-refresh workflow into the upgrade cycle

**Best for**: Government, defense, air-gapped/disconnected environments

#### Pricing-tier pairing

Pair models with pricing tiers by planning **one Plan per deployment model**
(e.g. a hosted plan with `hostedDeployment` for starter/pro tiers and a
separate BYOC plan with `byoaDeployment` for an enterprise tier) — a single
plan never serves multiple deployment models. Name the chosen model(s)
explicitly in the Phase 11 handoff summary so FDE builds one plan (with its
matching `deployment:` block) per model.

#### Multi-Model Strategy
Support multiple deployment models with the same architecture — one separate
Plan per model:
```yaml
# Same application architecture, one plan per deployment model
services:
  app:
    image: myapp:latest
    # Works for Hosted, BYOC (Account/BYO-VPC/PrivateLink), BYOC-K8s, Air-gapped
```

**Design principles**:
- Externalize configuration (12-factor app)
- No hard-coded cloud-specific logic
- Support air-gapped deployments (container registries)
- Identical functionality across models

### Phase 5: Tenancy Architecture

**Omnistrate supports multiple tenancy models** - design for flexibility.

#### Shared Tenancy
**Architecture**: Single infrastructure, logical isolation
```
Customer A ─┐
Customer B ─┤→ Shared App → Shared DB (tenant_id partitioning)
Customer C ─┘
```

**Pros**:
- Cost-effective (resource sharing)
- Simple operations (one deployment)
- Easy scaling (horizontal app scaling)

**Cons**:
- "Noisy neighbor" risks
- Limited customization per tenant
- Shared security boundary

**Best for**: Freemium, small/medium customers, standardized offerings

**Compose design**:
- Single database service
- App environment variables include tenant routing logic
- Shared cache (tenant key prefixes)

#### Siloed Tenancy
**Architecture**: Dedicated infrastructure per tenant
```
Customer A → App A → DB A
Customer B → App B → DB B
Customer C → App C → DB C
```

**Pros**:
- Complete isolation (security, performance)
- Per-tenant customization
- Easier compliance (HIPAA, PCI)

**Cons**:
- Higher cost (no sharing)
- More complex operations (many deployments)
- Scaling overhead

**Best for**: Enterprise, regulated industries, high-value customers

**Compose design**:
- Full stack per tenant instance
- Omnistrate manages multiple instances
- Each instance is isolated deployment

#### Hybrid Tenancy
**Architecture**: Shared app tier, isolated data tier
```
Customer A ─┐
Customer B ─┤→ Shared App → DB A, DB B, DB C (dedicated)
Customer C ─┘
```

**Pros**:
- Balance cost and isolation
- Shared compute, isolated data
- Flexible per-tier decisions

**Cons**:
- More complex architecture
- Connection pooling challenges

**Best for**: Mixed customer base (SMB + Enterprise)

**Compose design**:
- Shared app service (scales horizontally)
- Database connection routing to tenant-specific DB instances

### Phase 6: Compliance & Security Architecture

Design for compliance requirements from the start.

#### SOC2 (Security, Availability, Confidentiality)
**Requirements**:
- Encryption at rest and in transit
- Access logging and audit trails
- Multi-factor authentication
- Regular backups
- Incident response procedures

**Compose decisions**:
- Use TLS/SSL for all services
- Enable database encryption
- Log all API requests
- Backup volumes daily

#### HIPAA (Healthcare)
**Requirements**:
- PHI (Protected Health Information) encryption
- Access controls and audit logs
- Business Associate Agreements (BAA)
- Dedicated infrastructure (no shared tenancy for PHI)

**Compose decisions**:
- Siloed tenancy for healthcare customers
- Encrypted databases (PostgreSQL with encryption)
- No caching of PHI data
- Detailed access logging

#### GDPR (European Data Privacy)
**Requirements**:
- Data residency (EU data in EU regions)
- Right to deletion (data purging)
- Data portability
- Consent management

**Compose decisions**:
- Multi-region deployments (EU, US)
- Clear data retention policies
- Data export APIs
- Customer data deletion workflows

#### PCI DSS (Payment Card Data)
**Requirements**:
- No storage of CVV, full PAN
- Encrypted card data
- Network segmentation
- Regular security scans

**Compose decisions**:
- Use payment gateways (Stripe, no card storage)
- Isolate payment processing services
- TLS everywhere

### Phase 7: SLA & Availability Architecture

Design for target SLA from the start.

#### 99.9% Uptime (8.76 hours downtime/year)
**Architecture**:
- Single region, single zone
- Basic health checks
- Manual failover acceptable

**Compose design**:
- Single replica per service
- Database with persistent volumes
- Basic health endpoints

#### 99.95% Uptime (4.38 hours downtime/year)
**Architecture**:
- Single region, multi-zone
- Automated health checks
- Load balancing across zones

**Compose design**:
- Multiple replicas per service (2-3)
- Load balancer configuration ready
- Multi-zone volume replication (plan for it)

#### 99.99% Uptime (52.6 minutes downtime/year)
**Architecture**:
- Multi-region active-passive
- Automated failover
- Redundant databases

**Compose design**:
- Replicated services (3+ replicas)
- Database replication ready
- Health checks with quick failover

#### 99.999% Uptime (5.26 minutes downtime/year)
**Architecture**:
- Multi-region active-active
- Global load balancing
- Distributed databases

**Compose design**:
- Highly replicated services
- Distributed databases (CockroachDB, Cassandra)
- Multiple cloud providers

### Phase 8: Compose Spec Development (Iterative)

**Build the Docker Compose spec iteratively** - start simple, validate, add complexity.

#### Iteration 1: Core Services (MVP)
**Goal**: Get basic architecture working

```yaml
version: '3.8'
services:
  app:
    image: mycompany/api:latest
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://postgres:password@database:5432/app
    depends_on:
      - database

  database:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=app
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

**Validate**:
- Run `docker-compose up` locally
- Test API endpoints
- Verify database connectivity
- Check logs for errors

#### Iteration 2: Add Caching & Dependencies
**Goal**: Add performance and reliability layers

```yaml
services:
  app:
    image: mycompany/api:latest
    environment:
      - DATABASE_URL=postgresql://postgres:password@database:5432/app
      - REDIS_URL=redis://cache:6379
    depends_on:
      - database
      - cache

  cache:
    image: redis:7-alpine
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru

  database:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=app
    volumes:
      - db_data:/var/lib/postgresql/data
```

**Validate**:
- Test cache hit/miss
- Verify performance improvement
- Check memory usage

#### Iteration 3: Add Health Checks & Readiness
**Goal**: Production-grade reliability

```yaml
services:
  app:
    image: mycompany/api:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    environment:
      - DATABASE_URL=postgresql://postgres:password@database:5432/app
      - REDIS_URL=redis://cache:6379
    depends_on:
      database:
        condition: service_healthy
      cache:
        condition: service_started

  database:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

**Validate**:
- Test startup order
- Verify health check responses
- Test graceful degradation

#### Iteration 4: Multi-Service (If Needed)
**Goal**: Microservices architecture

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api

  api:
    image: mycompany/api:latest
    environment:
      - DATABASE_URL=postgresql://postgres:password@database:5432/app
      - REDIS_URL=redis://cache:6379
      - WORKER_URL=http://worker:8081
    depends_on:
      - database
      - cache

  worker:
    image: mycompany/worker:latest
    environment:
      - DATABASE_URL=postgresql://postgres:password@database:5432/app
      - REDIS_URL=redis://cache:6379
    depends_on:
      - database
      - cache

  database:
    image: postgres:15
    volumes:
      - db_data:/var/lib/postgresql/data

  cache:
    image: redis:7-alpine
```

**Validate**:
- Test service-to-service communication
- Verify load balancing
- Check worker job processing

#### Iteration 5: Parameterization & Configuration
**Goal**: Prepare for Omnistrate's multi-tenancy

```yaml
services:
  app:
    image: mycompany/api:${APP_VERSION:-latest}
    environment:
      - DATABASE_URL=postgresql://${DB_USER:-postgres}:${DB_PASSWORD}@database:5432/${DB_NAME:-app}
      - REDIS_URL=redis://cache:6379
      - LOG_LEVEL=${LOG_LEVEL:-info}
      - MAX_CONNECTIONS=${MAX_CONNECTIONS:-100}
    depends_on:
      - database
      - cache

  database:
    image: postgres:${POSTGRES_VERSION:-15}
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME:-app}
      - POSTGRES_USER=${DB_USER:-postgres}
    volumes:
      - db_data:/var/lib/postgresql/data

  cache:
    image: redis:7-alpine
    command: redis-server --maxmemory ${CACHE_SIZE:-256mb} --maxmemory-policy allkeys-lru
```

**Validate**:
- Test with different parameter values
- Verify `.env` file support
- Check parameter validation

#### Iteration 6: Container Image Registry Setup
**Goal**: Ensure all services have image references (not build contexts)

**Check for build contexts**:
```yaml
services:
  app:
    build: ./app  # ❌ Won't work on Omnistrate
    # OR
    build:
      context: ./backend
      dockerfile: Dockerfile  # ❌ Won't work on Omnistrate
```

**If build contexts exist**, you MUST work with customer to convert them:

1. **Build and push images to a registry**:
   ```bash
   # Option 1: Docker Hub
   docker build -t mycompany/api:v1.0.0 ./app
   docker push mycompany/api:v1.0.0

   # Option 2: GitHub Container Registry
   docker build -t ghcr.io/mycompany/api:v1.0.0 ./app
   docker push ghcr.io/mycompany/api:v1.0.0

   # Option 3: Private registry
   docker build -t registry.company.com/api:v1.0.0 ./app
   docker push registry.company.com/api:v1.0.0
   ```

2. **Replace build context with image reference**:
   ```yaml
   services:
     app:
       image: mycompany/api:v1.0.0  # ✅ Now cloud-deployable
       # build: ./app  # Remove this
   ```

3. **Identify registry authentication needs** (if using private registries):

   As SA you **collect** the requirements — you do **not** add
   `x-omnistrate-image-registry-attributes` to the compose spec. That extension
   (and the paired Omnistrate secrets) is configured by the **FDE skill** during
   onboarding, per the compose reference's "Image Registry Authentication"
   section. For each private image, record:
   - The registry hostname (`docker.io`, `ghcr.io`, `registry.company.com`, …)
   - Whether the image is public or private (if known)
   - Which credential the customer will use (PAT / token / username+password)

   Hand this list to FDE; it tests accessibility, guides the customer through
   token creation, creates the Omnistrate secrets (environment-specific: Dev,
   Staging, Prod), and adds the `x-omnistrate-image-registry-attributes` block.

**Validate**: All services have `image:` field with registry reference

#### Iteration 7: Resource Sizing Hints
**Goal**: Guide Omnistrate resource allocation

```yaml
services:
  app:
    image: mycompany/api:v1.0.0  # Must have image reference
    deploy:
      replicas: ${APP_REPLICAS:-2}
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
    environment:
      - DATABASE_URL=postgresql://postgres:password@database:5432/app

  database:
    image: postgres:15
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
    driver: local
    driver_opts:
      type: none
      device: /data/postgres
      o: bind
```

**Note**: These are hints for FDE transformation, not strict Omnistrate syntax yet.

### Phase 9: Container Image Registry Validation

**Critical**: Omnistrate cannot build images from source. All services must have `image:` references to pre-built container images.

**Check for build contexts**:
```bash
grep -r "build:" docker-compose.yaml
```

**If any service uses `build:` instead of `image:`**:

1. **Identify all services with build contexts**:
   ```yaml
   services:
     api:
       build: ./backend  # ❌ Not supported by Omnistrate
     worker:
       build:
         context: ./worker
         dockerfile: Dockerfile  # ❌ Not supported
   ```

2. **Ask customer where to host images**:

   **Question**: "I see these services need container images: [list services with build contexts]. Where would you like to host these images?"

   **Options to present**:
   - Docker Hub (docker.io) - public or private
   - GitHub Container Registry (ghcr.io) - public or private
   - AWS ECR (123456.dkr.ecr.region.amazonaws.com)
   - GCP Artifact Registry (region-docker.pkg.dev/project/repo)
   - Azure Container Registry (company.azurecr.io)
   - Custom private registry

3. **Guide customer to build and push images**:
   ```bash
   # Example: Docker Hub
   docker build -t mycompany/api:v1.0.0 ./backend
   docker push mycompany/api:v1.0.0

   # Example: GitHub Container Registry
   docker build -t ghcr.io/mycompany/worker:v1.0.0 ./worker
   docker push ghcr.io/mycompany/worker:v1.0.0
   ```

4. **Replace build contexts with image references in compose**:
   ```yaml
   services:
     api:
       image: mycompany/api:v1.0.0  # ✅ Now has registry reference
       # build: ./backend  # ❌ Remove build context entirely

     worker:
       image: ghcr.io/mycompany/worker:v1.0.0  # ✅ Registry reference
       # build:  # ❌ Remove build section
       #   context: ./worker
       #   dockerfile: Dockerfile
   ```

5. **Document registry information for FDE handoff**:

   Create a list for FDE skill:
   - Custom images: `mycompany/api:v1.0.0` (docker.io), `ghcr.io/mycompany/worker:v1.0.0` (ghcr.io)
   - Public images: `nginx:alpine`, `postgres:15`, `redis:7-alpine`
   - Registries used: docker.io, ghcr.io

   **Do NOT add `x-omnistrate-image-registry-attributes`** - FDE skill will:
   - Test if images are publicly accessible using docker pull
   - Guide customer through PAT/token creation for private registries
   - Collect credentials and create Omnistrate secrets
   - Add the `x-omnistrate-image-registry-attributes` section to the compose file

**Validate before moving to next phase**:
- ✅ Every service has `image:` field with valid registry reference
- ✅ NO `build:` contexts remain in compose file
- ✅ Customer has pushed all custom images to registries
- ✅ Registry information documented (image names, registry hostnames, public/private if known)

### Phase 10: Omnistrate-Aware Design Decisions

**While building the compose spec, consider Omnistrate features** (even though you won't add `x-omnistrate-*` extensions yet).

#### Design for Autoscaling
**Compose consideration**: Make app tier stateless
```yaml
services:
  app:
    # Stateless - no local file storage
    # Session in Redis, not in-memory
    image: mycompany/api:latest
    depends_on:
      - cache  # For session storage
```

#### Design for Multi-Zone HA
**Compose consideration**: Multiple replicas, load balancer ready
```yaml
services:
  app:
    deploy:
      replicas: 3  # Spread across zones later
```

#### Design for Backups
**Compose consideration**: Clear volume paths
```yaml
services:
  database:
    volumes:
      - db_data:/var/lib/postgresql/data  # FDE will add backup config here
```

#### Design for Observability
**Compose consideration**: Metrics endpoints, structured logging
```yaml
services:
  app:
    environment:
      - METRICS_PORT=9090  # Prometheus endpoint
      - LOG_FORMAT=json     # Structured logs
```

#### Design for Multi-Tenant Routing
**Compose consideration**: Tenant ID in requests
```yaml
services:
  app:
    environment:
      - TENANT_HEADER=X-Tenant-ID  # Header-based routing
```

### Phase 10b: Output-Format Decision

Before drafting the handoff, decide which artifact format the FDE skill (or operator skill) should receive. The decision affects the handoff artifact and which reference file the next skill uses.

| Stack description | Output format | Consequence for handoff |
|-------------------|--------------|------------------------|
| Plain containers, no existing Helm chart or Terraform | **Docker Compose** (default) | Produce a vanilla compose spec; FDE uses `COMPOSE_ONBOARDING_REFERENCE.md` |
| Application already ships a Helm chart | **Helm ServicePlanSpec skeleton** | Recommend a `helmChartConfiguration` skeleton; FDE uses `HELM_ONBOARDING_REFERENCE.md` |
| Cloud-managed services (RDS, CloudSQL, Azure DB) in the architecture, provisioned via Terraform/OpenTofu | **Terraform ServicePlanSpec skeleton** | Recommend a `terraformConfigurations` skeleton; FDE uses `TERRAFORM_KUSTOMIZE_REFERENCE.md` |
| Data infrastructure managed by a Kubernetes operator (e.g., CloudNativePG, Strimzi, KubeAI) | **Operator** | Do NOT produce compose or helm; hand off to the **omnistrate-operator** skill (separate install) |
| Mixed stack (e.g., Terraform infra + Helm app) | **Mixed ServicePlanSpec skeleton** | Recommend combined spec with `dependsOn`; FDE uses both `HELM_ONBOARDING_REFERENCE.md` and `TERRAFORM_KUSTOMIZE_REFERENCE.md` |

**Decision rule**: if the user has containers only and no existing Helm/Terraform artifacts, default to Docker Compose — it is the quickest path to a running instance. Escalate to Helm/Terraform only when those artifacts already exist or when the architecture inherently requires cloud-managed services.

### Phase 11: Handoff to FDE Skill

**Once the output artifact (compose spec or ServicePlanSpec skeleton + notes) is validated**, prepare the onboarding handoff.

#### Pre-Handoff Checklist
- [ ] Compose spec runs successfully with `docker-compose up` (compose path)
- [ ] All services start in correct order (depends_on) (compose path)
- [ ] Health checks pass (compose path)
- [ ] Inter-service communication works (compose path)
- [ ] Database migrations run successfully (compose path)
- [ ] **All services have `image:` references (no `build:` contexts remain)**
- [ ] **Container images pushed to registry (customer completed this)**
- [ ] **Registry information documented** (which images, which registries, public/private)
- [ ] Environment variables parameterized
- [ ] Resource limits documented
- [ ] Volumes clearly defined
- [ ] Multi-service architecture decision finalized (single vs multi-service)
- [ ] Tenancy model documented (shared, siloed, hybrid)
- [ ] Deployment model(s) noted (Hosted / BYOC-Account / BYO-VPC / PrivateLink / BYOC-K8s / Air-gapped)
- [ ] SLA requirements documented
- [ ] Compliance requirements noted

#### Handoff Documentation
Provide to FDE skill:
1. **Compose spec file** (vanilla, WITHOUT `x-omnistrate-image-registry-attributes` - FDE will add if needed)
2. **Container image inventory**:
   - List all custom images with full registry URLs (e.g., `mycompany/api:v1.0.0`, `ghcr.io/myorg/worker:v1.0.0`)
   - Mark which are public vs private (if known)
   - List public images (postgres, redis, nginx, etc.) separately
3. **Registry information**: Hostnames of registries used (docker.io, ghcr.io, custom registries)
4. **Architecture diagram** (ASCII or description)
5. **Service plan requirements**:
   - Free tier: What features/limits?
   - Pro tier: What features/limits?
   - Enterprise tier: What features/limits?
6. **Deployment model preferences**:
   - SaaS only?
   - BYOC for enterprise?
7. **Compliance requirements**: SOC2, HIPAA, GDPR, etc.
8. **SLA targets**: 99.9%, 99.95%, 99.99%
9. **Scaling expectations**: Fixed replicas, manual, or autoscaling?
10. **Backup requirements**: Daily, retention period?
11. **Observability preferences**: NewRelic, Datadog, Omnistrate native?

#### Handoff Routing

Route to the correct skill/path based on the output-format decision from Phase 10b. **Always name the chosen deployment model(s) in the handoff summary.**

| Output format | Route to | Reference used by next skill |
|---------------|----------|------------------------------|
| Docker Compose | **omnistrate-fde** (compose path) | `COMPOSE_ONBOARDING_REFERENCE.md` |
| Helm ServicePlanSpec | **omnistrate-fde** (helm path) | `HELM_ONBOARDING_REFERENCE.md` |
| Terraform/Kustomize ServicePlanSpec | **omnistrate-fde** (terraform/kustomize path) | `TERRAFORM_KUSTOMIZE_REFERENCE.md` |
| Mixed ServicePlanSpec | **omnistrate-fde** (mixed path) | `HELM_ONBOARDING_REFERENCE.md` + `TERRAFORM_KUSTOMIZE_REFERENCE.md` |
| Any format, air-gapped target | **omnistrate-fde** (air-gapped installer path) | `DEPLOYMENT_MODELS_REFERENCE.md` §Air-gapped |
| Operator (CRDs + controller) | **omnistrate-operator** skill | (operator skill owns this path) |

In every path, the onboarding workflow builds the `deployment:` block that encodes the chosen model(s) — name them explicitly in the handoff so it can.

The onboarding flow does not end at a running instance: it finishes with **portal distribution** (release the Plan, make the prod environment public, configure the Customer Portal) and by generating a **`DEPLOYMENT_OVERVIEW.md`** artifact. Your chosen deployment model(s) and the customer-facing parameters you recommend here flow directly into that overview's architecture and responsibility-split diagrams — so make both explicit in the handoff summary.

#### Example Handoff Message
```
Ready for Omnistrate onboarding. Here's the summary:

Architecture: Three-tier web app (NGINX → API → PostgreSQL + Redis)
Tenancy: Hybrid (shared API, isolated databases for enterprise)
Output format: Docker Compose
Deployment models: Hosted (starter/pro tiers) + BYOC-Account (enterprise tier)
  → two separate plans: a hosted plan (hostedDeployment) for starter/pro;
    a BYOC plan (byoaDeployment) for enterprise — one plan per model
  → See DEPLOYMENT_MODELS_REFERENCE.md for deployment: block and account-onboarding flow
Compliance: SOC2, GDPR data residency
SLA: 99.95% (multi-zone)
Monetization: Stripe, priced on cpu + storage (built-in dimensions)
  → end-to-end billing; no exporter needed
  → (if it were a marketplace/Chargebee/per-seat model: custom metering export
     + an ISV-side exporter service)

Container Images:
Custom images (customer pushed):
- API: company/api:v1.0.0 (docker.io registry)
- Worker: company/worker:v1.0.0 (docker.io registry)

Public images (no auth needed):
- NGINX: nginx:alpine
- PostgreSQL: postgres:15
- Redis: redis:7-alpine

Registry Info:
- docker.io used for custom images (FDE will test if authentication needed)

Service plans:
- Starter: 1 API replica, 20GB DB, no backups
- Pro: 3 API replicas, 100GB DB, daily backups, autoscaling
- Enterprise: Custom sizing, BYOC-Account option, multi-region

Next step: hand compose spec to omnistrate-fde → compose path (COMPOSE_ONBOARDING_REFERENCE.md).
```

## Domain-Specific Guidance

### AI/ML Platforms
**Key decisions**:
- GPU requirements (inference: T4, training: A100)
- Model storage (S3/GCS for weights)
- Batch vs real-time inference
- Model versioning strategy

**Compose architecture**:
```yaml
services:
  api:
    image: fastapi-app
  inference:
    image: pytorch-gpu:latest
    # FDE will map to GPU instance types
  model-storage:
    # S3 bucket (external, not in compose)
```

### Data Analytics Platforms
**Key decisions**:
- Query engine (Presto, Spark, custom)
- Data lake architecture (S3 + metadata)
- Streaming vs batch processing
- Column storage (Parquet, ORC)

**Compose architecture**:
```yaml
services:
  query-api:
    image: query-engine
  workers:
    image: spark-workers
  metadata-db:
    image: postgres
```

### API Platforms
**Key decisions**:
- Gateway pattern (Kong, Envoy, custom)
- Rate limiting strategy
- API versioning
- Documentation (OpenAPI/Swagger)

**Compose architecture**:
```yaml
services:
  gateway:
    image: kong
  api-v1:
    image: api:v1
  api-v2:
    image: api:v2
```

### Database-as-a-Service
**Key decisions**:
- Which DB to offer (PostgreSQL, MySQL, MongoDB)
- Backup and restore strategy
- Replication topology (primary-replica, multi-primary)
- Connection pooling (PgBouncer)

**Compose architecture**:
```yaml
services:
  primary:
    image: postgres:15
  replica:
    image: postgres:15
  pooler:
    image: pgbouncer
```

## Iterative Refinement Workflow

```
1. Discovery → 2. Tech Selection → 3. Simple Compose → 4. Validate
                                            ↓
                                         Issues? → Refine
                                            ↓
                                           No issues
                                            ↓
5. Add Complexity → 6. Validate → 7. Image Registry Setup → 8. Omnistrate-Aware Adjustments
                        ↓
                     Issues? → Refine
                        ↓
                      No issues
                        ↓
9. Document → 10. Handoff to FDE
```

**Key principle**: Validate at each step before adding complexity.

## Success Criteria

- ✅ User's domain and requirements clearly understood
- ✅ Technology stack selected with clear rationale
- ✅ Service architecture designed (single vs multi-service)
- ✅ Tenancy model selected (shared, siloed, hybrid)
- ✅ Deployment models planned (SaaS, BYOC, etc.)
- ✅ Compliance requirements addressed in architecture
- ✅ SLA targets mapped to architecture decisions
- ✅ Docker Compose spec validated locally (`docker-compose up` works)
- ✅ All services start and communicate correctly
- ✅ Health checks defined and passing
- ✅ **All services have `image:` references (no `build:` contexts)**
- ✅ **Custom images pushed to registry (Docker Hub, GHCR, ECR, etc.)**
- ✅ **Registry information documented** (for FDE to test accessibility and configure auth if needed)
- ✅ Environment variables parameterized
- ✅ Resource sizing hints documented
- ✅ Omnistrate-aware design decisions made (autoscaling, backups, multi-zone)
- ✅ Handoff documentation prepared for FDE skill

## Reference
See SOLUTIONS_ARCHITECT_REFERENCE.md for:
- Technology comparison matrices
- Domain-specific architecture patterns
- Compliance requirement checklists
- SLA architecture guidelines
- Compose spec best practices
- Common architectural anti-patterns
