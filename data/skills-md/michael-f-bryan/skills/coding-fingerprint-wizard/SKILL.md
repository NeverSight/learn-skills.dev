---
name: coding-fingerprint-wizard
description: Analyse several example projects to synthesise a reusable coding fingerprint. Use when the user wants to capture a person's coding style, engineering principles, project-shaping preferences, architectural tendencies, or implementation habits so agents can reproduce them consistently.
---

# Coding Fingerprint Wizard

Create a reusable coding fingerprint from example projects.

The goal is not to infer formatter trivia or generic "clean code" advice. The goal is to identify the decisions that make a person's work recognisable: how they shape modules and repositories, where they validate, what they test, what they document, how they use frameworks, what they refuse to abstract, and which trade-offs they make repeatedly.

The output is a `coding-fingerprint-[name]/SKILL.md` file that another agent can apply when planning, writing, reviewing, or refactoring code.

## When To Apply

Use this skill when the user wants to capture a person's:

- coding style
- engineering principles
- repo-shaping preferences
- architectural tendencies
- testing and validation habits
- abstraction thresholds

Do not use it for superficial style analysis, formatter imitation, or one-project hero worship.

## Operating Model

Treat this as a strict diverge-converge workflow:

1. **Prepare**: define the sample set and its caveats
2. **Discover**: gather project-level evidence in parallel
3. **Define**: converge on durable cross-project patterns
4. **Develop**: challenge the draft fingerprint for overfitting and weak inference
5. **Deliver**: generate the reusable fingerprint skill
6. **Validate**: check whether another agent can actually use it

Do not collapse early. Breadth comes before synthesis, and challenge comes before canonisation.

## Coordinator Default

The top-level agent is a coordinator.

- Spawn sub-agents for detailed analysis.
- Run parallel sub-agents where the work is independent.
- Use `references/analysis-worksheet.md` as the source of truth for artefact contracts.
- Decide when the evidence is broad enough to converge.
- Resolve conflicts between worker outputs.

Do not let the coordinator do the full analysis itself unless it is reconciling disagreements, repairing a failed handoff, or validating the final result.

## Sample Quality

Prefer 2-5 samples with real authorship signal.

Strong samples usually have:

- meaningful code rather than generated scaffolding
- tests, docs, commit history, or review context
- similar era and responsibility level
- code the subject would still endorse

Weak samples usually include:

- heavily templated repositories
- one-off experiments with little behavioural signal
- team code with unclear authorship
- repos dominated by framework defaults

If the sample set mixes very different contexts, record that explicitly and treat context-specific patterns as weaker evidence.

## Read Order

1. Start with `SKILL.md`.
2. Read [references/REFERENCE.md](references/REFERENCE.md) to choose the next file deliberately.
3. Read [references/analysis-worksheet.md](references/analysis-worksheet.md) before creating or checking any `_working/coding-fingerprint/` artefact.
4. Read [references/fingerprint-template.md](references/fingerprint-template.md) only when Phase 4 begins.
5. Read [references/example-coding-fingerprint.md](references/example-coding-fingerprint.md) only if the output shape is unclear or you are calibrating the result.

## Phase Gates

### Phase 0: Prepare

Create the sample inventory before any synthesis work. Record scope, samples, evidence quality, and caveats in `_working/coding-fingerprint/` using the worksheet contract.

### Phase 1: Discover

Run sub-agents in parallel.

Default shape:

- one worker per project for `project-profile-<slug>.md`
- optional lens workers for testing, architecture, review style, or error handling when the projects are large

The goal here is breadth. Collect evidence first; do not collapse to principles early.

### Phase 2: Define

Run a synthesis worker after the project profiles exist.

Only promote a pattern if it appears across projects or is supported by strong surrounding evidence. Separate:

- durable fingerprint traits
- context-specific choices
- contradictions
- open questions

Treat repo-shaping as first-class output. A good fingerprint should help another agent choose module boundaries, repo layout, contract surfaces, CI defaults, and dependency posture.

### Phase 3: Develop

Stress-test the draft fingerprint before it becomes canonical.

At minimum, challenge:

- overfitting to one project
- avoidances and things the author consistently does not do
- reproducibility across independent analysers
- predictive power on plausible implementation choices

### Phase 4: Deliver

Generate the final fingerprint skill using [references/fingerprint-template.md](references/fingerprint-template.md).

Save it as:

```text
coding-fingerprint-[name]/
└── SKILL.md
```

### Phase 5: Validate

Use a fresh sub-agent with access only to the generated fingerprint and a small representative task. Compare its choices back to the source projects.

Refine the fingerprint if it sounds generic, contradicts evidence, overfits one codebase, captures style without principles, or cannot be applied reliably by another agent.

## Signal Quality

Prefer high-signal patterns over surface polish.

Strong signals:

- where validation lives
- how boundaries are drawn
- how repositories are split once boundaries appear
- what gets abstracted versus duplicated
- what gets generated versus handwritten
- how tests express intent
- preferred error semantics
- docs, CI, and drift-check habits around important contracts
- naming choices that reveal domain modelling

Weak signals:

- formatter output
- language defaults with no visible choice
- isolated clever code
- framework boilerplate

## Failure Modes

Avoid:

- reducing the fingerprint to style-guide cliches
- treating one impressive project as the whole person
- confusing ecosystem constraints with personal preference
- inferring principles without citing evidence
- producing a fingerprint that another agent cannot operationalise
- skipping the challenge phase because the synthesis looks right

## Quality Bar

The final fingerprint is good only if it helps another agent answer questions like:

- How would this person split the module?
- How would this person shape the repository or workspace?
- Where would they validate input?
- What would they test first?
- What docs, schemas, or CI checks would they expect to exist?
- Which abstraction would they reject as premature?
- What code smell would they flag immediately?

If the skill cannot answer those questions, the fingerprint is still too vague.

## Additional Resources

- Reference router: [references/REFERENCE.md](references/REFERENCE.md)
- Artefact contracts and worker deliverables: [references/analysis-worksheet.md](references/analysis-worksheet.md)
- Final output template: [references/fingerprint-template.md](references/fingerprint-template.md)
- Worked example: [references/example-coding-fingerprint.md](references/example-coding-fingerprint.md)

## Related Skills

- Use `working-docs` when you need scratch notes outside this workflow
- Use `test-driven-development` when validating the generated fingerprint against an implementation task
