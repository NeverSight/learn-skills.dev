---
name: deploy-pass
description: Analyzes a software project and designs the full deployment system it actually needs — build, artifact, config & secrets, infrastructure, release strategy, data & migrations, deploy gates, verify & observe, and recovery — instead of assuming a fixed platform or running a canned deploy command. Never assumes infrastructure, secrets, production permissions, or release strategy; never executes an irreversible action without explicit per-step authorization. Produces DEPLOY-PLAN.md before touching anything, then executes and documents only what the user authorizes. Use when the user asks to deploy their project, design a deployment pipeline, set up CI/CD, or take a project to production.
---

# Deploy Pass

## Goal

Deployment is not a command. It's a system: build → artifact → package → configure → release →
run → verify → observe. This skill's job is to understand what a specific project actually needs
from that system, design it, generate the pieces, and only then — with explicit permission at each
step — operate it.

Do not assume the stack, the cloud provider, or the release strategy. Discover them. A project
deployed to Vercel + Render + NeonDB needs a completely different system than one deployed to a
Kubernetes cluster on GCP — this skill decides which, based on evidence from the project, not from
a default.

The flow this skill implements, every time:

```
DISCOVER → DESIGN → GENERATE → EXECUTE → VERIFY → DOCUMENT
```

with a feedback loop: what VERIFY and DOCUMENT learn feeds back into DESIGN for the next deploy of
the same project.

## Non-negotiable rule

This skill may analyze, ask, design, generate files, and propose freely. It may **never** execute
an irreversible or production-affecting action — deploy, release, rollback, infrastructure change,
secret rotation, data migration — without the user's explicit authorization for that specific
action, at that specific moment. Designing the rollback plan is this skill's job; pressing the
button that rolls back is the user's call every time.

**What this skill can do:**

- Analyze the project
- Ask what it can't infer
- Design the deploy workflow
- Generate workflows, scripts, and configs
- Execute commands — only with authorization
- Verify that everything works
- Detect problems
- Execute a rollback — only if authorized
- Document the process

**What this skill must never assume:**

- A default infrastructure or provider
- Secrets or credentials
- Production permissions
- A release strategy
- Any destructive action
- Any decision without the user's approval

The user has control. This skill is a copilot, not an operator.

## Required Input

None is mandatory in isolation — this skill discovers what the project actually has:

- Stack, runtime, framework, package manager
- Build process, test suite
- Database, external services, queues
- Existing infrastructure (cloud, VPS, PaaS, containers)
- Existing CI/CD
- Environment variables, secrets manager
- Domains/DNS, storage, observability tooling
- Deployment docs, if any exist

If a category doesn't exist yet in the project, that's a design decision to make in DESIGN, not a
gap to silently fill with a default.

## Workflow

### 1. DISCOVER — understand the project

Before proposing anything, build a real model of the project. Read what exists (glob/grep first,
don't assume file layout), and ask directly for whatever can't be inferred:

- Stack / runtime / framework / package manager
- Build process and its outputs
- Tests (what exists, what the project currently trusts)
- Database(s) and how they're currently reached
- External services and integrations
- Existing infrastructure, if any (cloud account, VPS, PaaS, containers, K8s)
- Existing CI/CD, if any
- Environment variables and how secrets are currently handled
- Domains, storage, queues, observability already in place
- Single repo or monorepo — if monorepo, how service/package boundaries are actually defined
- Whether any artifact is a **published package** (npm, Composer/Packagist, PyPI...) consumed by
  third parties, rather than a service this project runs itself

Use `assets/deployment-system-vocabulary.md` as the list of things to notice — not a form to fill
mechanically. Skipping this and jumping to a generic "npm run build && deploy" is the failure mode
this skill exists to prevent.

### 2. DESIGN — propose the deployment system

For each block that actually applies to this project, decide and justify a concrete approach:

- **Build** — how the project turns into something deployable, deterministically
- **Artifact** — exactly what gets deployed (image, package, binary, static bundle...), versioned
  and traceable back to a commit
- **Config & secrets** — what's config vs. what's a secret, and where each lives (never in the
  repo, never in logs)
- **Infrastructure** — where it runs, chosen for this project (AWS/GCP/Azure/VPS/Docker/K8s/PaaS —
  whatever fits, not a default)
- **Environments** — dev/staging/prod, and what changes between them (config/secrets — not code)
- **Release strategy** — direct release, rolling, blue/green, canary, feature flags — chosen for
  this project's risk tolerance, not applied by default
- **Data & migrations** — schema changes, backward compatibility, migration ordering, zero-downtime
  strategy if needed. State explicitly: a code rollback does not automatically mean a data rollback
- **Deploy gates** — what must pass before a release is allowed (tests, security checks, build
  success). A gate that only runs as an informational CI check alongside a platform's own
  auto-deploy-on-push is not a gate — a red check and a live deploy can both exist at once. If the
  target platform (Render, Vercel, Netlify, and similar PaaS) supports disabling its native
  auto-deploy and exposes a deploy hook (a URL that triggers a deploy on demand), design the real
  gate as: disable auto-deploy-on-push on the platform, then let CI trigger the deploy hook only
  after its checks pass. Check for that capability before settling for a weaker check-only design.
  If the platform truly cannot be gated this way, say so explicitly in the plan instead of quietly
  downgrading to an informational check.
- **Verify & observe** — health checks and smoke tests to confirm it worked; logs/metrics/traces to
  watch afterward
- **Recovery** — what happens if it fails: rollback, redeploy, restore infrastructure, restore
  data, incident handling

Write this design to `DEPLOY-PLAN.md` (see `assets/deploy-plan-template.md`) **before generating or
executing anything**, then **stop and wait for the user to explicitly approve the plan**. This is
a hard checkpoint, not a formality — do not continue into GENERATE on your own just because DESIGN
finished. Approval covers the plan as a whole (unlike EXECUTE, which is authorized action by
action); once given, move on to GENERATE.

### 3. GENERATE — produce the pieces

Once the plan in `DEPLOY-PLAN.md` is approved, generate the concrete artifacts it calls for:
CI/CD workflow files, build/deploy scripts, config templates, migration scaffolding. Generating
files is not an irreversible action — it doesn't require step-by-step authorization the way EXECUTE
does, but nothing generated here runs on its own.

### 4. EXECUTE — operate it, with permission

Nothing in this phase runs without the user explicitly authorizing that specific action at that
specific moment. Walk through the plan's steps (build → package → configure → release → run) and
ask before each one that touches real infrastructure, real secrets, or a real environment. Never
batch-authorize "just do the whole deploy" into a single blanket approval for destructive steps.

### 5. VERIFY

Run the health checks, smoke tests, and critical-path checks the plan defined. Confirm the release
actually worked before calling it done — a deploy that "completed" but fails its health check is a
failed deploy, not a successful one with a follow-up.

### 6. DOCUMENT

Append what happened to `DEPLOY-PLAN.md`: what was executed, what verification showed, what (if
anything) went wrong and how it was resolved. This turns the plan into a living record — the next
Deploy Pass on this project starts by reading it instead of rediscovering everything from zero.

## Output

- `DEPLOY-PLAN.md` at the project root — written after DESIGN, before any execution. Updated with
  an execution/verification log after EXECUTE and VERIFY.
- Whatever CI/CD workflow files, scripts, and configs the plan calls for, generated in GENERATE.
- No other file in the project changes, and no infrastructure or environment changes, without
  explicit authorization tied to that specific change.

## Quality Gate

Before returning, silently check:

- DISCOVER actually happened first — the design in step 2 is grounded in real facts about this
  project, not a generic template.
- No infrastructure, provider, secret, production permission, or release strategy was assumed by
  default anywhere in the plan.
- `DEPLOY-PLAN.md` exists and was shown to the user **before** any EXECUTE step ran.
- The skill actually stopped after DESIGN and waited for explicit plan approval — it didn't run
  straight through into GENERATE on its own.
- Every EXECUTE action that touched real infrastructure, secrets, or an environment had explicit,
  specific authorization — not a single upfront blanket "yes."
- VERIFY actually ran and its result is recorded, not assumed from "the command didn't error."
- DOCUMENT captured what happened, including failures — not just the happy path.

## What this skill deliberately does not do yet

It runs on-demand, invoked directly, for one project at a time. It doesn't wire itself into an
existing CI/CD trigger, run unattended, or manage multiple projects at once — that's a real need to
build toward later, not something to speculate into v1.
