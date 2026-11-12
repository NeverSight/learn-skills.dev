---
name: review-architecture
type: atomic
license: MIT
description: >
  Use when reviewing Rails structure, fat models or controllers, or service
  boundaries. Trigger words: architecture, fat model, fat controller,
  boundaries, tech debt.
metadata:
  version: 1.0.0
  user-invocable: "true"
---

# Review Architecture


## Quick Reference

| Area | What to check |
|------|---------------|
| Controllers | Coordinate only — no domain logic |
| Models | Own persistence + cohesive domain rules, not orchestration |
| Services | Create real boundaries, not just moved code |
| Callbacks | Small and unsurprising — no hidden business logic |
| Concerns | One coherent capability per concern |
| External integrations | Behind dedicated collaborators |

## HARD-GATE (Authoritative Verification Rule)

```text
DO NOT list findings that do not survive code-level confirmation.
Verify each High-severity finding by reading the actual code to confirm it is a real structural problem.
If verification reveals it is not genuine, downgrade it or remove it entirely.
If no source files were provided or read, do not invent High findings. Return an
architecture review checklist or assumptions block instead, and say code-level
confirmation is required before reporting findings.
SECRET SAFETY: code-level evidence must never reproduce secrets, tokens, API
keys, passwords, private keys, session cookies, or credential values. If a file
contains a hard-coded secret, report only the file/path, symbol name, credential
type, and a redacted fingerprint such as `[REDACTED_API_KEY]`; do not quote the
literal value.
```

## Core Process

Use this skill when the task is to review or improve the structure of a Rails application or library.

**Core principle:** Prioritize boundary problems over style. Prefer simple objects and explicit flow over hidden behavior.

### Review Order

1. Identify the main entry points: controllers, jobs, models, services.
2. Check where domain logic lives.
3. Inspect model responsibilities, callbacks, and associations.
4. Inspect controller size and orchestration.
5. Read every concern, helper, and presenter: does it do one coherent thing, or does it mix auditing + notifications + emails + external API calls? Mixed concerns are High or Medium severity depending on blast radius. **Treat any concern used by only one class as a candidate for deletion — inline it instead.**
6. Check whether abstractions clarify the design or only move code around.
7. **Verify each High-severity finding** per the HARD-GATE above — confirm real structural problem, redact any credential-like values found.

### Severity Levels

#### High-Severity Findings

- Business logic hidden in callbacks or broad concerns
- Controllers orchestrating multi-step domain workflows inline
- Models coupled directly to HTTP, jobs, mailers, or external APIs
- Abstractions that add indirection without a clear responsibility
- Cross-layer constant reach that makes code hard to change

#### Medium-Severity Findings

- Duplicated workflow logic across controllers or jobs
- Scopes or class methods carrying too much query or policy logic
- Helpers or presenters leaking domain behavior
- Service objects wrapping trivial one-liners
- Concerns combining unrelated responsibilities — check EVERY concern in the app

## Output Style

1. **Scope**: State that the task is an architecture/structure review, not style review, and identify the Rails entry points inspected.
2. **Order**: Begin with entry points. Then write findings ordered by review area.
3. **Boundary-first lens**: Prioritize where domain logic lives, whether flow is explicit, and whether abstractions clarify the design or only move code around.
4. **Finding Structure**: Every finding uses a four-field structure:
   ```text
   **Severity:** High
   **Affected file:** app/controllers/orders_controller.rb — OrdersController#create
   **Risk:** Controller runs a 5-step domain workflow. Partial state on failure; untestable without HTTP.
   **Improvement:** Extract to Orders::CreateOrder.call(params). Controller handles response/redirect only.
   ```
5. **High-severity verification**: For every High finding, state the concrete code-level evidence read (per HARD-GATE). Redact any secret-like literal. Never use representative file paths or fabricated line numbers as evidence.
6. **Completeness**: For each finding include severity, affected files or area, why the structure is risky, and the smallest credible improvement. Then list open assumptions and recommended next refactor steps.
7. **Language**: Must be in English unless explicitly requested otherwise.

## Integration

| Skill | When to chain |
|-------|---------------|
| **code-review** | For smaller scopes and PR reviews |

## Extended Resources (Progressive Disclosure)

Load these files only when their specific content is needed:

- **[assets/examples.md](assets/examples.md)** — Use when you need complete architecture review examples with findings and recommendations
- **[assets/findings_schema.json](assets/findings_schema.json)** — Use when you need the structured JSON schema for architecture review findings output
