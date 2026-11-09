---
name: threat-model
description: Use when the user asks for a threat model (new or updated), STRIDE analysis, attack surface or trust boundary review, a data flow diagram with trust boundaries, "what could go wrong" security-wise, or the scope for a pentest, DAST scan or security hackathon; before implementing anything security-sensitive (auth, authorization, roles, tenants, payments, uploads, admin features, webhooks, integrations); and, even without the words "threat model", when a feature adds an AI component (chatbot, agent, RAG, tool calling, MCP server) or a security test plan needs a scope.
---

# Threat model

A threat model is a design review with an adversarial lens. It answers four questions
(Adam Shostack's four-question frame): what are we working on, what can go wrong,
what are we going to do about it, did we do a good job. The output is a short document
plus a data flow diagram that a team can read in ten minutes and that tells the next
step (a code review, a DAST scan, a pentest agent) exactly what to try.

Why this matters for AI-assisted development: coding agents are good at avoiding
textbook bugs (SQL injection, XSS) and bad at adding controls nobody asked for
(authorization checks, rate limits, CSRF, security headers). The threat model is the
"ask list". A threat that is written down gets a mitigation and a test; a threat that
only lives in someone's head gets neither.

This skill produces a plan. It does not run attacks, scans, or exploit code. Testing
happens later, in an isolated environment, with synthetic data only.

## Workflow

### 0. Check for an existing model

Look for `docs/security/threat-model.md` (or any `*threat-model*.md`). If one exists,
update it instead of starting over: keep its structure and threat IDs, mark threats
that are now mitigated, add new ones, update the diagram, and add a dated line to the
changelog. A rewritten model loses the history of what was accepted and why.

### 1. Discover the system

Do not assume a stack or an application type; find out. The threats that matter for a
browser-facing web app (CSRF, XSS, IDOR) are not the ones for a queue worker, a CLI, an
MCP server or a batch pipeline, and the places to look for entry points differ by
framework. `references/discovery.md` lists what to look for and where, per stack.

1. **Inventory the applications.** Check for monorepo markers (workspaces, `apps/`,
   `packages/`, `services/`, `docker-compose.yml`, Kubernetes or Terraform manifests)
   and manifest files (`package.json`, `composer.json`, `pyproject.toml`, `go.mod`,
   `Cargo.toml`, `pom.xml`, `*.csproj`, `Gemfile`). List every deployable unit.
2. **Classify each one.** Type: browser web app, HTTP API, background worker or queue
   consumer, scheduled job, CLI, mobile backend, serverless function, AI agent or
   service, MCP server, shared library (libraries get no model of their own; their
   consumers do). Framework and language. How it is deployed.
3. **Understand the architecture.** Monolith, modular monolith, frontend plus API,
   microservices, event-driven; which data stores and message brokers; how
   authentication works (sessions, JWT, OAuth/OIDC provider, API keys, mTLS) and where
   authorization is enforced; whether the system is multi-tenant and how tenancy is
   scoped in queries; which external systems and AI components exist and with whose
   credentials they are called.
4. **Write the System profile** section of the template before anything else. It
   is short, but it drives the rest: it decides which STRIDE prompts apply, which
   OWASP lists are relevant, and whether one model covers the repository or each
   application needs its own section.

Read README, specs, ADRs and AGENTS.md / CLAUDE.md first, then confirm against the
code; documentation describes intent, code describes reality, and the gap between them
is often where the threats are. Do not invent architecture. If the code does not show
how something works, write it as an assumption under "Assumptions and open questions"
and move on. A wrong guess presented as fact is worse than a visible gap.

### 2. Decompose: what are we working on?

With the profile in hand, fill in the four lists from the template: assets (what we
protect), actors (who could attack, including a logged-in user of another tenant and
untrusted content the system reads), entry points, and trust boundaries.

Then draw the data flow diagram. This is a deliverable, not an illustration: it is the
one artifact a reviewer can check in a minute. Follow `references/dfd-conventions.md`
(Mermaid, external entities as rectangles, processes as rounded boxes, stores as
cylinders, trust boundaries as dashed subgraphs, flows labelled with what they carry).
Keep it to the elements that handle sensitive data or cross a boundary, roughly 15
nodes at most. A large system gets one context diagram plus one diagram per
application in scope, not one diagram of everything. After step 3, annotate flows
with the IDs of the threats that sit on them, so the picture and the table point at
each other.

### 3. What can go wrong?

Walk each entry point and each flow across a trust boundary through STRIDE
(Spoofing, Tampering, Repudiation, Information disclosure, Denial of service,
Elevation of privilege). `references/stride-prompts.md` has the questions per letter
and per application type, plus the AI-specific ones. Skipping a letter is the most
common gap, so ask all six even when the answer is "not applicable here".

For every AI component (anything where model output influences what the system does),
run the lethal trifecta check: does it process untrusted input, does it have access to
sensitive data or systems, can it change state or communicate externally? All three in
one session means prompt injection can cause real damage. Record the verdict against
Meta's Agents Rule of Two (at most two of the three without a human approval step) and
treat the missing property or the approval gate as the primary mitigation.

Prioritize instead of enumerating. A useful model has roughly 8 to 15 threats, each one
specific to this system ("user of tenant A reads tenant B's invoices via `GET
/api/invoices/{id}`"), not generic ("injection attacks"). Score each with Likelihood and
Impact as High / Medium / Low; that is enough to order the work. Map each threat to an
OWASP ID (Web Top 10:2025, API Security Top 10, LLM Top 10 2026, Agentic Top 10 2026,
MCP or Skills Top 10) and a CWE where one fits; `references/owasp-map.md` has the
lists. The mapping lets reviewers and auditors speak the same language and points to
published mitigations.

### 4. What are we going to do about it?

For each threat choose a response: mitigate, eliminate (remove the feature or the
property), transfer (a provider or an insurance covers it), or accept (with a reason and
a name). Note whether a control already exists in the code (name the file or middleware)
or is missing.

The most important column is "How we verify". Every threat gets a concrete check:
a unit or integration test, a SAST rule, a DAST probe, a manual test with two accounts,
a prompt injection attempt, a review of logs. This column is the security test plan;
copy it into the "Test scope" section so a tester or a pentest agent can start from it
without reading the rest.

Write what is out of scope and the rules of engagement (which environment, synthetic
data only, what must not be touched). A test scope without boundaries is how people
break production.

### 5. Did we do a good job?

Run the checklist at the end of the template before saving. In particular: every
application in scope has a profile, every boundary crossing on the diagram was walked
through all six letters, every High threat has a mitigation and a verification, every
assumption is marked, and nothing in the document is an attack instruction.

### 6. Write the outputs

- `docs/security/threat-model.md` from `assets/THREAT_MODEL_TEMPLATE.md`, with the
  Mermaid diagram inline (GitHub, GitLab and most editors render it).
- `docs/security/threat-model.mmd` with the diagram source alone, so it can be
  rendered or edited separately. If a Mermaid renderer is already available (`mmdc`,
  or `npx @mermaid-js/mermaid-cli` with node present), also render
  `docs/security/threat-model.svg`; do not install browsers or heavy dependencies just
  for this, say instead how to render it.

Write in the language of the project's existing documentation; if the repository has
none, use the language the user writes in. Keep the document to roughly two pages: the
point is that people read it.

If the project keeps a task list or issue tracker the user works with, offer to create
one task per missing High mitigation. Do not create them without asking.

## Judgment calls

- Scope the model to the change when asked for a feature ("threat model the new
  upload endpoint"); scope it to the system when asked for the project. Both use the
  same template; a feature-level model lists only the elements the feature touches and
  reuses the existing profile and diagram.
- Monorepos: one document with a context diagram and one section per application in
  scope when they share a trust domain; separate documents when they are deployed and
  owned separately. Ask if it is not obvious.
- Multi-tenant or multi-role systems: always include a cross-tenant and a cross-role
  threat, even if the current project has one tenant. They are the most common real
  finding in AI-generated code and the cheapest to test with two seeded accounts.
- Non-web applications still have boundaries: a CLI trusts its arguments, config file
  and environment; a worker trusts its queue; a batch job trusts its input files. Model
  those flows the same way.
- When the system has several cooperating agents, or the user asks for MAESTRO, this
  skill is too small; point to OWASP's `multi-agentic-threat-model` play from the
  Secure Agent Playbook instead.
- Re-run triggers worth adding to AGENTS.md or a PR template: a new application or
  entry point, a change to auth or authorization, a new external integration, a new AI
  component or tool given to an existing one.

## Example of a good threat row

| ID | Threat | STRIDE | Where | L | I | Response | Control today | How we verify | OWASP / CWE |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-03 | Logged-in user of company A reads company B's request via `GET /api/requests/{id}` (IDOR) | I, E | `api/requests/[id]/route.ts` | H | H | Mitigate: scope the query by `organizationId` from the session, deny by default | None: handler loads by `id` only | Integration test with two seeded organizations; DAST probe swapping IDs with user A's token | A01:2025, API1:2023, CWE-639 |

A bad row for comparison: "Broken access control, High, add authorization" says
nothing about where, how to fix it, or how to prove it is fixed.
