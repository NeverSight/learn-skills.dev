---
name: typescript-best-practices
description: Apply disciplined TypeScript modeling and boundary parsing. Use when reading or editing TypeScript.
---
# TypeScript Best Practices

- Parse unknown external data at the boundary; keep `unknown` until validated.
- Prefer discriminated unions for mutually exclusive states and exhaustive handling for closed variants.
- Give domain meaning to primitives when accidental mixing would be costly.
- Avoid widening useful literal information and avoid `any` as an escape hatch.
- Let callers consume one coherent return shape instead of correlated optional fields.
- Use generics only when they express a real relationship between inputs and outputs.
- Keep async/error states explicit at the public boundary.
- Test behavior through exported APIs, not private helper choreography.
