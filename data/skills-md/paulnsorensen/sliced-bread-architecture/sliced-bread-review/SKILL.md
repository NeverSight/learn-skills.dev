---
name: sliced-bread-review
description: >-
  Review a diff, PR, branch, or path against the Sliced Bread architecture
  rules: dependency direction, crust integrity, model purity, growth
  justification, and event usage. Use when the user asks for an architecture
  review, says "check this against sliced bread", "review the slice
  boundaries", "is this import allowed", or before merging changes that add
  directories, abstractions, or cross-slice imports. Do NOT use for general
  bug-hunting or a full repo audit — this reviews a bounded change set.
---

# Sliced Bread Review

Review the target change set against the Sliced Bread architecture. The full
rationale lives at
<https://cheeselord.dev/sliced-bread-architecture/reference/sliced-bread/>;
this skill is the operational checklist.

## Scope

Determine the review target from the invocation, in priority order:

1. An explicit path, diff, branch, or PR named by the user.
2. The current branch's diff against the default branch.
3. Uncommitted changes (`git diff HEAD`).

Review only the changed files plus any file a changed import points at.

## The Five Checks

Run every check against every changed file. Cite `file:line` and quote the
offending import or definition for each finding.

### 1. Import direction

Arrows may only point in a permitted direction. Only the composition root
(`app/bootstrap`, `main`) may import concrete adapters, and nothing imports
`entrypoints/`. A slice may import a sibling slice's public seam directly.
The arrows describe permitted direction, not required directories — a repo with
no `entrypoints/` layer is not in violation.

<!-- doctrine:arrows:start -->

```text
entrypoints/   ->  app/  ->  domains/*  ->  domains/common/
app/bootstrap  ->  adapters/          (composition root only)
adapters/      ->  domains/*          (implement domain ports)

Never:
  app/use_cases/*  ->  adapters/*
  domains/*        ->  adapters/ | app/ | entrypoints/
  adapters/*       ->  app/ | entrypoints/
  common/          ->  sibling domains
  anything         ->  entrypoints/
```

<!-- doctrine:arrows:end -->

Any inversion of these arrows is a **blocker**; a use case importing a concrete
adapter is **medium**.

### 2. Crust integrity

External consumers use a slice's public seam in the language's native form —
exported identifiers in Go, the package `__init__` surface in Python, an index
module in TypeScript, a public class surface elsewhere — never its internals.
`from domains.pricing import calculate_discount` is fine;
`from domains.pricing.discount_calculator import ...` is a violation —
**high** with multiple consumers, **low** with one.

### 3. Model purity

Domain files import only stdlib, `common/`, and sibling slice public APIs.
A domain file importing an HTTP client, ORM, or queue is a violation; the fix
is a port (protocol) defined in the domain and implemented by an adapter.
Grade severity from the `doctrine:severity-cases` matrix under
[Severity](#severity) below, in first-match order.

### 4. Growth justification

New directories and abstractions require demonstrated pressure. Two concrete uses are the normal evidence threshold, not a hard requirement. An abstract base with one implementation, an event bus interface when no event exists yet, or a registry with one plugin is medium only when no concrete pressure justifies it. "Numeric thresholds" in the guards below means the advisory growth signals (~200 lines, 3+ concepts, 3+ clustered files), not gradeable limits. Suppress these false positives:

<!-- doctrine:growth-guards:start -->

- A single consumer does not by itself prove premature abstraction; grade whether concrete pressure exists. Two consumers are normal evidence, not a hard requirement.
- New single-file concepts that stayed single files are correct; do not flag them.
- A dispatcher introduced to break a cross-slice cycle is demonstrated pressure, even with one event and one subscriber.
- Numeric thresholds are advisory signals, not gradeable violations; grade implementation share, public-surface size, and lifetime mixing.
- In a language whose only privacy mechanism is file placement, a subdirectory marking its contents internal is demonstrated pressure for that visibility boundary, even with a single file inside.

<!-- doctrine:growth-guards:end -->

<!-- prettier-ignore-start -->
<!-- doctrine:growth-cases:start -->

| ID | Given | Expected | Rationale |
| --- | --- | --- | --- |
| `growth-cycle-event` | An event dispatcher is introduced to break a cross-slice cycle. | `allow` | The dispatcher removes a concrete cycle and is a canonical exception to the pressure-first growth signal. |
| `growth-positional-one-file` | A one-file positional crust marks internal visibility in a language without another privacy mechanism. | `allow` | The directory is a visibility boundary rather than speculative growth structure, even when it contains one file. |
| `growth-single-unpressured` | A new abstraction has one concrete consumer and no demonstrated pressure. | `medium` | The normal two-concrete-consumer signal has not been met, so the abstraction should be challenged as premature rather than treated as a blocker. |

<!-- doctrine:growth-cases:end -->
<!-- prettier-ignore-end -->

Apply the reference-owned `doctrine:growth-cases` matrix in first-match order; do not infer outcomes from prose outside the matrix.

### 5. Event usage

Events exist for reverse dependencies: B reacts to A without A knowing B.
Cycles between slices must resolve via events typed in `common/`, not mutual
imports (**high**).
Events used as general-purpose messaging where a direct import is the natural
dependency are a **medium** finding.

## Severity

The severities cited in the checks above derive from this table.

<!-- doctrine:severity:start -->

| Severity | Meaning                                                                                                                                                              |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| blocker  | Inverted dependency arrow; infrastructure executing at import time in a domain file                                                                                  |
| high     | Cross-slice internal import; circular slice dependency; crust bypass with multiple consumers                                                                         |
| medium   | Model-purity drift (infrastructure imported, not executed at import time); premature abstraction; events-as-messaging; adapter imported outside the composition root |
| low      | Single-consumer crust bypass; naming drift                                                                                                                           |

<!-- doctrine:severity:end -->

<!-- prettier-ignore-start -->
<!-- doctrine:severity-cases:start -->

| ID | Given | Expected | Rationale |
| --- | --- | --- | --- |
| `severity-import-exec` | A domain module executes infrastructure work while it is imported. | `blocker` | Import-time side effects make every consumer pay infrastructure cost and can fail before application startup is controlled. |
| `severity-static-domain-infra` | A domain model has a static dependency on infrastructure. | `medium` | The dependency violates model purity and increases change coupling, but a static edge alone is not an import-time execution failure. |
| `severity-static-concrete-adapter` | A use case or application service imports a concrete adapter instead of a domain port. | `medium` | The application layer is coupled to infrastructure selection; dependency injection through a port restores the intended boundary. |
| `severity-other-forbidden-edge` | A dependency edge points in a forbidden direction and does not match a more specific severity case. | `blocker` | Unmatched structural inversions break the slice dependency contract and require immediate correction. |

<!-- doctrine:severity-cases:end -->
<!-- prettier-ignore-end -->

Apply the reference-owned `doctrine:severity-cases` matrix in first-match order; do not infer outcomes from prose outside the matrix.

## Output

Report findings grouped by severity, most severe first. Each finding:
`severity — check — file:line — quoted evidence — one-line fix`. An empty
report is a valid outcome; never manufacture findings. Do not fix anything —
this skill reviews only.
