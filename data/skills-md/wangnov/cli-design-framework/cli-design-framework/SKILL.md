---
name: cli-design-framework
description: Use when designing a new CLI, reviewing an existing CLI, or resolving uncertainty about a CLI's role, user type, interaction form, statefulness, risk profile, or human-vs-machine surfaces.
---

# CLI Design Framework

## Overview

Design and review CLIs with a classification-first framework.

Treat this as a decision system, not a generic style guide. Do not assume every CLI should become agent-first, machine-protocol-first, or raw-payload-first.

## When to Use

Use this skill when:
- designing a new CLI and the right command shape is not obvious
- reviewing an existing CLI whose help, output, or command tree feels mismatched
- deciding whether a CLI is primarily Capability, Runtime, Environment / Workspace, Workflow, Package / Build, or Meta
- deciding whether human-readable and machine-readable surfaces are primary or secondary
- deciding whether session semantics are justified or over-engineered

Do not use this skill when:
- the CLI classification is already settled and you only need implementation mechanics
- the question is only about parser libraries, repository layout, or exact flag spelling
- the task is purely cosmetic copy editing with no design consequence

## Quick Path

- For quick asks, produce a compressed pass: purpose, classification, short reasoning, top design consequences, and only the unresolved questions that could change the answer.
- Use the full blueprint or full review template only when the user asks for it explicitly, or when ambiguity or risk justifies the longer form.

## Core rule

Classify first. Design second. Review third.

Always work in this order:
1. State the CLI purpose in one sentence.
2. Classify the primary role/control surface.
3. Classify the primary user type.
4. Classify the primary interaction form.
5. Classify statefulness.
6. Classify risk profile.
7. Identify secondary surfaces explicitly.
8. Derive design consequences.

Start with these files when using the framework:
- `references/taxonomy.md` for the taxonomy.
- `references/output-templates.md` for the required output shape.

Pull these only when needed:
- `references/classification-examples.md` for classification anchors when the category is ambiguous.
- `examples/design-blueprint-example.md` and `examples/review-example.md` when you need a concrete example of final form.
- `examples/anti-patterns.md` when the design smells wrong but the category mistake is not yet crisp.

## Operating modes

Operate in one of two modes:
1. **Design mode** — create or refine a CLI design direction.
2. **Review mode** — evaluate an existing CLI against the framework.

---

## Design mode

### Goal

Clarify the CLI's design target, then produce a blueprint that constrains implementation.

### Workflow

1. Infer what is already known.
   - Extract every strong signal from the user's request.
   - Infer likely role, user type, interaction form, statefulness, risk profile, and secondary surfaces whenever possible.
   - Do not ask for facts that are already strongly implied.

2. Ask only the highest-leverage unresolved questions.
   - Ask the smallest set of questions that could materially change the classification or the blueprint.
   - Prefer classification questions over implementation trivia.
   - Prioritize: purpose → control surface → primary user → interaction form → statefulness → side effects → secondary surfaces.
   - If the current information is already sufficient, do **not** ask questions. Produce the blueprint directly.

3. Classify the CLI explicitly.
   - State the inferred or confirmed:
     - primary role/control-surface type
     - primary user type
     - primary interaction form
     - statefulness
     - risk profile
     - secondary surfaces
   - State confidence when inference is uncertain.
   - Use explicit primary-vs-secondary wording. Do not blur them together.

4. State the design stance before proposing commands.
   - Write one short paragraph that says what the CLI is optimizing for.
   - State what the CLI is **not** trying to be.
   - Do not jump straight from classification to command trees.

5. Produce a design blueprint.
   - Use the structure in `references/output-templates.md`.
   - Use the full template when the user wants a blueprint or when the ambiguity/risk warrants it.
   - For quick requests, compress to: purpose, classification, classification reasoning, design stance, top design consequences, and only the unresolved questions that matter.
   - Connect classification directly to design consequences.
   - Keep the blueprint concrete, not generic.

6. Constrain downstream implementation.
   - End with a short direction section that states:
     - what to optimize for
     - what not to optimize for
     - acceptable patterns
     - category mistakes
     - v1 boundaries and non-goals

### Required design discipline

For every blueprint, enforce these rules:

- **Primary vs secondary surfaces**
  - Name the primary surface explicitly.
  - Name secondary surfaces explicitly.
  - State what each surface is for.
  - Do not describe JSON, event streams, templates, raw payloads, or TUI as “important” without saying whether they are primary or secondary.

- **Human-primary / balanced discoverability**
  - If the CLI is human-primary or balanced, explicitly cover:
    - help quality
    - examples
    - discoverability
    - explain/describe surfaces when appropriate
  - Do not discuss only command structure and ignore learnability.

- **Structured machine contract**
  - If the CLI has a machine-readable surface, explicitly state:
    - which commands expose it
    - output format (`--json`, `--jsonl`, etc.)
    - whether field names are stable
    - whether exit codes matter
    - whether schema / fields / describe support is needed
  - Do not call a surface “script-friendly” unless the contract is described.

- **Risk ladder**
  - If the CLI mutates state, define at least:
    - low-risk operations
    - medium-risk operations
    - high-risk operations
  - State the expected guardrails for each level.
  - Do not stop at “be careful” or “add confirmations.”

- **State model**
  - If the CLI is sessionful, long-running, or attach/detach capable, describe session identity and lifecycle explicitly.
  - If it is mostly stateless, say so explicitly and avoid inventing session semantics.

- **v1 boundaries**
  - State what v1 should include.
  - State what v1 should defer.
  - State what would be premature abstraction.

### Question policy

Ask only questions that affect classification or the blueprint.

Do **not** begin with implementation-detail questions such as:
- language choice
- parsing library
- repository layout
- naming bikesheds
- exact flag spelling

Ask those only if they materially affect the CLI's classification or design consequences.

---

## Review mode

### Goal

Inspect the CLI and its source, reverse-infer its design intent, then review it in two layers:
1. **Classification fit** — Is it designed like the right kind of CLI?
2. **Execution quality** — Given that type, how well is it executed?

### Workflow

1. Inspect before asking.
   - Inspect help output, subcommand help, docs, examples, parser code, output code, error handling, state/session code, config surfaces, and tests.
   - Prefer direct evidence over speculation.

2. Reverse-infer the design intent.
   - Infer:
     - apparent purpose
     - likely primary role/control-surface type
     - likely primary user type
     - likely interaction form
     - likely statefulness
     - likely risk profile
     - existing secondary surfaces

3. Confirm only what cannot be inferred reliably.
   - Ask focused confirmation questions only when the answer could materially change the classification or review.
   - Do not ask the user to restate facts already evident from the CLI or code.

4. Review in two layers.
   - Keep **classification fit** and **execution quality** separate.
   - Do not criticize a human-primary CLI for not being agent-primary unless the user explicitly wants that shift.

5. Produce a structured review.
   - Use the review structure in `references/output-templates.md`.
   - Use the full template when the user wants a formal review or when the category tension is material.
   - For quick requests, compress to: inferred intent, classification, evidence-backed category mistakes, in-category weaknesses, and highest-priority improvements.
   - Separate category mistakes from in-category execution weaknesses.

### Required review checks

When reviewing, explicitly check these areas when relevant:

- **Primary vs secondary surface clarity**
  - Is the CLI clear about what the main surface is?
  - Are secondary surfaces real contracts or just informal add-ons?

- **Discoverability**
  - Does help output support the claimed user type?
  - Are examples, option descriptions, and command structure aligned with the CLI's center of gravity?

- **Structured output contract**
  - Are JSON / JSONL / field-selection / exit-code surfaces explicit and stable?
  - Are unknown fields rejected or silently tolerated?
  - Is the machine surface strong enough for the claims made in docs?

- **Risk model**
  - Are low-, medium-, and high-risk actions meaningfully separated?
  - Are confirm / dry-run / preview / audit guardrails aligned with the risk profile?

- **State model**
  - Is statefulness handled correctly?
  - Are attach/detach/resume/session/history concepts used only when justified?

- **v1 discipline**
  - Does the CLI keep a coherent v1 boundary?
  - Does it introduce premature abstraction or missing contracts?

### Review rules

- Do not grade every CLI on an agent-first curve.
- Do not require raw payloads, full schema introspection, or machine-first output unless the classification justifies them.
- Treat modern CLIs as multi-surface systems: one primary role, one primary interaction form, optional secondary surfaces.
- Prefer strong inference, then targeted confirmation.
- When criticizing machine support, specify whether the problem is:
  - missing primary/secondary surface clarity,
  - weak machine contract,
  - or a true category mismatch.

---

## Handling hybrid CLIs

Some CLIs genuinely straddle multiple roles at the subcommand level.

Rules for hybrid CLIs:
1. Classify at the **product level** first — what is the CLI's center of gravity?
2. If subcommands clearly split into different roles, note the split explicitly.
3. Name the **primary role** (the one that defines the CLI's identity and design constraints).
4. Name **secondary roles** as secondary surfaces with their own local constraints.
5. Do not force a single role on a CLI whose subcommands genuinely serve different roles.

Example: Docker
- Product-level primary role: **Runtime** (its center of gravity is container execution).
- `docker run`, `docker exec`, `docker attach` → Runtime interaction.
- `docker image ls`, `docker volume inspect` → Capability-like resource surfaces (secondary).
- `docker compose up` → Workflow/Orchestration (secondary).

Guidance for evolving CLIs:
- If a CLI is migrating from one type to another, state the current center of gravity and the intended direction.
- Do not classify based on the future target alone; classify based on current evidence and note the trajectory.

---

## Common failure modes

Watch for these mistakes:
- Treating every CLI as a capability CLI.
- Treating every CLI as a runtime CLI.
- Treating TUI or REPL as a role instead of an interaction form.
- Ignoring statefulness.
- Ignoring risk profile.
- Ignoring help/discoverability for human-primary CLIs.
- Treating automation fitness as a top-level identity instead of a design consequence.
- Forcing human-primary tools into agent-only patterns.
- Calling a JSON surface “strong” without defining the contract.
- Ignoring secondary surfaces in mixed-mode CLIs.
- Jumping from classification directly to command trees without stating design stance.
- Failing to mark v1 boundaries and non-goals.
- Forcing a single role on a hybrid CLI whose subcommands genuinely serve different control surfaces.
- Over-engineering statefulness for a CLI that only has durable config/lockfile side-effects but no true sessions.
- Classifying a CLI by its future aspirations instead of its current evidence.

## Output bar

Keep final outputs:
- explicit about classification
- explicit about classification reasoning when there is tension or ambiguity
- explicit about evidence, confidence, and assumptions
- explicit about design consequences
- explicit about primary vs secondary surfaces
- explicit about discoverability and machine contracts when relevant
- explicit about risk ladders when mutations exist
- scaled to the user's requested depth
- concise but dense
- diagnostic rather than generic

Avoid vague advice such as "improve UX" or "make it more agent-friendly" unless tied to a specific classification and a concrete design consequence.
