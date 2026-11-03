---
name: stride-threat-modeling
description: Run a STRIDE-based threat modeling workshop — diagram the system, enumerate threats per element, rank them, and drive mitigations into the backlog. Use during design reviews and new feature planning.
---

# STRIDE Threat Modeling

Threat model a system in a structured workshop format.

## 1. Model the System

Draw the diagram: processes, data stores, data flows, external actors, and trust boundaries (dashed lines where privilege/context changes).

- Every element numbered; technologies noted on processes/stores
- Include the boring parts: auth flows, async jobs, admin tooling, backups

## 2. Enumerate with STRIDE

For each element, apply the applicable categories:

| Category | Applies To | Question |
|---|---|---|
| **S**poofing | Processes, actors | Can someone pretend to be this? (auth) |
| **T**ampering | Flows, stores | Can data be modified in transit/at rest? (integrity) |
| **R**epudiation | Processes | Can actions be denied? (logging/audit) |
| **I**nformation disclosure | Flows, stores | Can data leak to unauthorized parties? (confidentiality) |
| **D**enial of service | Processes, flows | Can this be exhausted or crashed? (availability) |
| **E**levation of privilege | Processes | Can rights be gained? (authz) |

Work systematically: element × category grid so nothing is skipped.

## 3. Rank

Score each threat by impact (worst realistic outcome) × likelihood (attack complexity, exposure). Prioritize: unauthenticated remote > authenticated remote > local > physical.

## 4. Mitigate

For each accepted threat, pick a strategy: reduce (control), transfer, accept (documented, with owner), or avoid (design change). Map mitigations to concrete backlog tickets with acceptance criteria.

## 5. Validate

- Review the model when the architecture changes (trigger: new external dependency, new trust boundary, new data class)
- Retro: incidents found in prod vs threats previously modeled — feed misses back into the method

## Output

System diagram with trust boundaries, element × STRIDE threat grid, ranked risk register, and mitigations as tracked tickets.
