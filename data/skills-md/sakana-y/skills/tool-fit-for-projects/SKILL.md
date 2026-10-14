---
name: tool-fit-for-projects
description: Evaluate which tools fit a repository need, or audit the repository for material tool opportunities, without implementing a change. Use only when the user explicitly invokes $tool-fit-for-projects.
---

# Tool Fit for Projects

Find fit, not a winner.

Work read-only from the current repository and current evidence. Compare external tools with the Current Baseline: the existing tool, local implementation, manual work, or deliberate absence of a tool. A No-change Result is a successful outcome.

## Choose One Mode

### Tool Decision

Use this mode when the user names a need, decision, current tool, or Candidate Seed. Complete the decision workflow and stop at the Tool Choice Checkpoint.

### Repository Tool Audit

Use this mode only when the user asks to inspect the repository for tool opportunities. Scan broadly, report at most five Material Tool Opportunities, and stop. The user chooses an opportunity before a full Tool Decision begins.

**Done when:** the invocation is in exactly one mode. An audit has not silently expanded into candidate research.

## Tool Decision Workflow

### 1. Frame the Decision

Establish the Tool Decision Context:

- the concrete repository work to improve;
- the affected users;
- the desired outcome and observable success conditions;
- known technical, organizational, budget, security, data, and time constraints.

Resolve facts from the repository and current sources. Ask one focused question only when a missing user-owned constraint would materially change candidate eligibility or the result. If no repository evidence is accessible, state that boundary and obtain the minimum project context instead of producing a generic product comparison.

Classify Decision Depth:

- **Quick** — local, reversible, narrow in code and responsibility, with no persistent-data or external-service effect;
- **Standard** — affects a workflow, several modules, or a meaningful compatibility surface;
- **High-stakes** — changes architecture, persistent data, identity, security, infrastructure, deployment, or a critical external service.

**Done when:** the decision is about a repository job rather than abstract products, and its depth matches the observable change radius and reversibility.

### 2. Establish the Baseline

Describe how the repository handles the job today, what works, the observable pain or risk, and the cost of keeping it. Include self-implementation and no-tool approaches when they are viable.

End with a No-change Result before external discovery when there is no material problem or when plausible research and adoption cost already exceeds the available benefit. State the evidence instead of manufacturing alternatives.

**Done when:** every external candidate can be compared against a concrete Current Baseline and no-change remains eligible.

### 3. Select Category Profiles

Read the smallest set of profiles that covers the material risks of the decision:

- [Code and developer tools](references/code-and-developer-tools.md) — frameworks, libraries, runtimes, build, test, lint, formatting, code generation, and developer workflow tools.
- [Data and infrastructure](references/data-and-infrastructure.md) — databases, caches, queues, search, storage, and stateful infrastructure.
- [Cloud and deployment](references/cloud-and-deployment.md) — compute, hosting, deployment platforms, networking, and managed cloud services.
- [Hosted and commercial services](references/hosted-and-commercial-services.md) — external SaaS, APIs, identity providers, observability products, and other vendor-operated services.

A candidate may require more than one profile. Do not load a profile merely because its category is adjacent.

**Done when:** every material Candidate Gate and comparison concern belongs to a loaded profile.

### 4. Build the Evidence Base

When several candidate questions can be researched independently, use [candidate evidence assignments](references/candidate-evidence.md). Fix the Current Baseline, gates and comparison questions first. The main owner retains comparison and recommendation; simple or tightly coupled decisions stay inline.

Follow the Tool Evidence Hierarchy:

1. repository code, manifests, configuration, history, issues, and existing Read-only Validation;
2. current official documentation, source, support matrices, release and deprecation notes, security advisories, licenses, pricing, and service terms;
3. reproducible independent benchmarks, downstream issues, and credible adoption evidence for claims the first two levels cannot establish.

Trace every material claim. Separate verified facts, repository-specific inference, user constraints, and unknowns. Treat popularity, stars, downloads, and feature counts as discovery signals rather than proof of fit.

Read-only Validation may run existing tests, benchmarks, and diagnostic commands that require no dependency, source, configuration, or service mutation. Plan new trials; do not execute them.

**Done when:** the evidence needed for every Candidate Gate is verified, user-owned, or named as unresolved.

### 5. Discover to Saturation

Treat every user-named tool as a Candidate Seed, never as the search boundary or a guaranteed finalist. Search independent solution shapes, including keeping the baseline, simplifying it, using a built-in capability, self-implementing the bounded need, and adopting an external tool.

Stop at Evidence Saturation: additional independent search paths no longer produce a materially different qualified candidate. Retain at most five finalists for full Tool Candidate Cards. Give every user-named seed a visible disposition and reason, even when it does not become a finalist.

**Done when:** the report can name the paths checked, stopping condition, finalist boundary, and disposition of every user seed.

### 6. Gate, Then Compare

Apply the loaded profiles' Candidate Gates before comparison. A failed non-negotiable gate cannot be offset by features, popularity, or another benefit.

For every candidate that passes or has a resolvable unknown, compare qualitatively:

- benefit for the repository job and success conditions;
- discovery cost for future users and maintainers to recognize the tool's purpose and find the right path, not the agent's search time;
- learning, price, adoption, integration, extension, migration, and maintenance cost;
- category-specific operational and lifecycle risks;
- progressive fit: bounded introduction, coexistence, optional capability growth, migration middle stages, rollback, and exit.

Do not calculate a total score. Assign exactly one Tool Candidate Disposition:

- **Recommended** — gates pass and evidence supports the lead choice;
- **Viable Alternative** — gates pass and a different trade-off may suit the user;
- **Trial** — a cheap repository experiment must verify a material fit claim;
- **Needs Evidence** — a missing fact or user-owned constraint prevents judgment;
- **Rejected** — a gate fails or cost and risk defeat the benefit.

**Done when:** every finalist and user seed has a reasoned disposition, and the recommendation remains relative to the Current Baseline.

### 7. Design the Stairs

For each Recommended or Trial candidate, design a Progressive Adoption Path:

1. the cheapest remaining evidence check;
2. an isolated, reversible trial;
3. a coexistence or migration checkpoint;
4. the passing observation and the signal that kills or revises the candidate;
5. rollback, data recovery where relevant, and the exit path.

Describe the path; do not install, prototype, migrate, purchase, or change services. Viable Alternatives receive only their material adoption difference unless the user selects one later.

**Done when:** the lead choices can be tested and abandoned before an irreversible commitment.

## Repository Tool Audit

Inspect the whole repository for observable problems, risks, duplicated capability, or maintenance burden that an external or built-in tool might materially improve. The existence of a newer or more popular tool is not an opportunity.

Return at most five opportunity cards, prioritized by problem severity, plausible benefit, change cost, and evidence strength. Each card contains:

- repository evidence and affected scope;
- the Current Baseline;
- the improvement hypothesis;
- likely Tool Category Profile and Decision Depth;
- why a full Tool Decision may be worthwhile.

State the audit coverage and stopping boundary. End at a Tool Choice Checkpoint where the user may select one opportunity, request a narrower audit, or stop. Do not search candidate ecosystems during the audit.

**Done when:** every reported opportunity is grounded in a material repository condition and no full selection has begun without the user's choice.

## Tool Decision Report

Lead with the result. Keep the structure stable and the detail proportional to Decision Depth:

1. **Decision Context** — repository job, users, success conditions, constraints, and depth.
2. **Current Baseline** — current value, pain, keep cost, and no-tool or self-implementation alternatives.
3. **Search Coverage** — Candidate Seeds, paths checked, Evidence Saturation, sources, and evidence boundary.
4. **Disposition Index** — every user seed and finalist with its Tool Candidate Disposition and one-line reason.
5. **Candidate Cards** — at most five, with repository evidence, gates, benefit, total cost, category risks, progressive fit, and uncertainty.
6. **Recommendation and Choices** — lead recommendation, viable alternatives, No-change Result when applicable, and material trade-offs.
7. **Progressive Adoption Paths** — full paths for Recommended and Trial candidates.
8. **Tool Choice Checkpoint** — invite the user to select a candidate, keep the baseline, authorize one targeted evidence question, or stop.

Compress a Quick decision when the same contract fits in a few paragraphs. Fully expand gates, uncertainty, operational risk, and exit conditions for High-stakes decisions. Keep the report in the conversation unless the user explicitly asks to save it. Selection does not authorize implementation.

## Origin of the Lens

This independent, unofficial skill applies Anthony Fu's cost balance and progressive-path lens to repository tool decisions. Antfu compares the cost of learning and using a tool with doing the work oneself, then describes progressive onboarding, integrations, features, and breaking changes as stairs that make complexity approachable. Repository audit, candidate discovery, category gates, dispositions, and the report contract are independent extensions. See Antfu's [official talk index](https://antfu.me/talks) and [source slides with speaker notes](https://github.com/antfu/talks/blob/main/2024-02-29/src/slides.md).
