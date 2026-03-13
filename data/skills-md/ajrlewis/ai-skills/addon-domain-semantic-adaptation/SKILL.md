---
name: addon-domain-semantic-adaptation
description: Use when generated output must match domain terms and tone while preserving architecture; pair with architect-stack-selector and addon-human-pr-review-gate.
---

# Add-on: Domain Semantic Adaptation

Use this skill when generic scaffold outputs should reflect the user's domain language (terminology, labels, workflows, and intent phrasing) without changing core architecture patterns.

## Compatibility

- Works with all `architect-*`, `addon-*`, and `ui-*` skills.
- Recommended default in `production-default` mode.

## Inputs

Collect:
- `DOMAIN_BRIEF`: one-paragraph business/domain context.
- `CANONICAL_TO_DOMAIN_MAP`: key term map (for example `document->clause packet`, `user->counsel`).
- `PREFERRED_TONE`: `neutral` | `formal` | `technical` | `friendly`.
- `FORBIDDEN_TERMS`: terms to avoid in UI/docs.
- `PUBLIC_COPY_SCOPE`: `ui-only` | `ui+docs` | `ui+docs+api-names`.

## Integration Workflow

1. Add semantic contract artifacts:
```text
docs/DOMAIN_LANGUAGE.md
docs/DOMAIN_DECISIONS.md
```
- `DOMAIN_LANGUAGE.md` should contain:
- domain brief
- canonical-to-domain table
- forbidden terms
- naming rules

2. Apply semantic mapping in generated outputs:
- UI labels, helper text, empty/loading/error states
- README and operational docs
- endpoint and command aliases (when `PUBLIC_COPY_SCOPE` allows it)

3. Preserve technical stability:
- Keep internal architecture and safety controls unchanged.
- Prefer additive aliases over breaking renames for API/CLI contracts.

4. Add validation notes:
- Record mapped terms and intentional non-mapped technical terms in `DOMAIN_DECISIONS.md`.

## Required Template

### `docs/DOMAIN_LANGUAGE.md`
```markdown
# Domain Language Contract

## Domain Brief
<short context>

## Canonical To Domain Terms
| Canonical | Domain |
|---|---|
| user | counsel |
| document | clause packet |

## Forbidden Terms
- foo
- bar

## Naming Rules
- UI and docs must use domain terms.
- Internal safety/security identifiers may remain canonical.
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Do not change security-critical semantics for stylistic reasons.
- Do not rewrite internal identifiers when that would break compatibility.
- Keep naming consistent across UI, docs, and prompts.
- Surface ambiguous term mappings as explicit review items.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
test -f docs/DOMAIN_LANGUAGE.md
test -f docs/DOMAIN_DECISIONS.md
rg -n "Canonical To Domain Terms|Forbidden Terms|Naming Rules" docs/DOMAIN_LANGUAGE.md
```
Manual checks:
- Generated UI/docs reflect domain terms from user prompt.
- No forbidden terms appear in user-facing copy.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
