---
name: privacy-safe-skill-extraction
description: >-
  Turn an internal standard, runbook, prompt, or repeated workflow into a
  reusable skill for a public or broader audience. Use whenever asked to
  generalize or publish guidance derived from private material. Preserve useful
  behavior while removing organization, product, customer, repository,
  infrastructure, and operational identifiers; inspect the final artifacts for
  leakage before sharing them.
---

# Privacy-safe skill extraction

Extract reusable knowledge without exporting the source document. The goal is
to preserve general decision rules and workflows while removing details that
identify private products, people, systems, or operations.

## Establish scope and audience

1. Identify the source material, intended audience, destination, and whether the
   result will be public, team-only, or project-local.
2. Inspect existing skills and public/private boundaries to avoid duplicating a
   skill or moving private policy into a broader scope.
3. If the audience or publication scope is unclear, ask before preparing a
   shareable artifact. Do not publish, commit, push, or install globally unless
   separately authorized.

## Extract reusable behavior

Separate source content into:

- portable principles and decision procedures that can be kept;
- organization-specific policy that belongs only in the organization's own
  materials;
- repository-specific facts and commands that must be replaced with generic
  guidance or omitted; and
- secrets, personal/customer data, or confidential information that must never
  be included in the new artifact.

Write the reusable skill in imperative, task-oriented language. Define its
trigger, inputs, workflow, boundaries, safety rules, and expected result. Keep
repository commands as "inspect and use the target repo's documented command"
unless a particular public tool is genuinely part of the reusable workflow.

## Sanitize examples and references

For a public or broader-scope artifact:

- Replace company, product, customer, employee, partner, and project names with
  neutral or synthetic names.
- Remove private repository paths, issue keys, board/project IDs, internal
  URLs, hostnames, API endpoints, service names, deployment topology, and
  environment-specific commands.
- Remove credentials, tokens, passwords, private keys, resolved environment
  values, customer data, and confidential business details. Do not reproduce
  them in the report or scan output.
- Replace examples with synthetic values that preserve the teaching point, or
  omit examples that cannot be safely generalized.
- Review links, filenames, frontmatter, bundled references, eval prompts, and
  metadata as well as the main `SKILL.md`.
- Preserve a source link only when it is intentionally public and appropriate
  for the target audience; otherwise remove it.

Do not treat a simple secret scan as sufficient. Product names, internal URLs,
issue identifiers, and architecture details can be confidential even when they
are not credentials.

## Verify before sharing

1. Compare the new skill's behavior with the source at an abstract level; do not
   copy private wording just to preserve fidelity.
2. Search all new files and generated artifacts for source-specific names,
   identifiers, URLs, paths, and infrastructure references. Keep scan output
   private; report only whether findings exist and their sanitized file/line
   locations.
3. Resolve each finding by generalizing or removing it. If a detail may still
   identify a private system, omit it or ask the owner rather than guessing.
4. Validate skill metadata, references, eval files, and installation/catalog
   entries. Use synthetic prompts in evals; do not include private incident or
   product context.
5. Show the sanitized result and validation scope. State clearly that a scan
   cannot guarantee the absence of all sensitive information.

## Boundaries

- Do not access or publish material beyond the source the user authorized.
- Do not copy large source sections into public artifacts; extract principles.
- Do not weaken safety, privacy, or legal obligations while generalizing.
- Do not infer permission to commit, push, release, or publish from permission
  to draft the skill.

## Completion report

Report the new skill's path, what kind of reusable workflow it captures, which
sanitization and structural checks ran, and any unresolved privacy questions.
Never quote sensitive findings or claim a privacy scan proves the artifact is
perfectly safe.
