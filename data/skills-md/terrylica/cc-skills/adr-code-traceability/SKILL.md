---
name: adr-code-traceability
description: Add ADR references to code for traceability. TRIGGERS - ADR traceability, code reference, document decision in code.
allowed-tools: Read, Edit, Grep, Glob
---

# ADR Code Traceability

Add Architecture Decision Record references to code for decision traceability. Provides language-specific patterns and placement guidelines.

## When to Use This Skill

- Creating new files as part of an ADR implementation
- Documenting non-obvious implementation choices
- User mentions "ADR traceability", "code reference", "document decision"
- Adding decision context to code during `/itp:go` Phase 1

## Quick Reference

### Reference Format

```
ADR: {adr-id}
```

**Path Derivation**: `ADR: 2025-12-01-my-feature` → `/docs/adr/2025-12-01-my-feature.md`

### Language Patterns (Summary)

| Language   | New File Header                      | Inline Comment              |
| ---------- | ------------------------------------ | --------------------------- |
| Python     | `"""...\n\nADR: {adr-id}\n"""`       | `# ADR: {adr-id} - reason`  |
| TypeScript | `/** ... \n * @see ADR: {adr-id} */` | `// ADR: {adr-id} - reason` |
| Rust       | `//! ...\n//! ADR: {adr-id}`         | `// ADR: {adr-id} - reason` |
| Go         | `// Package ... \n// ADR: {adr-id}`  | `// ADR: {adr-id} - reason` |

See [Language Patterns](./references/language-patterns.md) for complete examples.

---

## Placement Decision Tree

```
Is this a NEW file created by the ADR?
├── Yes → Add reference in file header
└── No → Is the change non-obvious?
    ├── Yes → Add inline comment with reason
    └── No → Skip ADR reference
```

See [Placement Guidelines](./references/placement-guidelines.md) for detailed guidance.

---

## Examples

### New File (Python)

```python
"""
Redis cache adapter for session management.

ADR: 2025-12-01-redis-session-cache
"""

class RedisSessionCache:
    ...
```

### Inline Comment (TypeScript)

```typescript
// ADR: 2025-12-01-rate-limiting - Using token bucket over sliding window
// for better burst handling in our use case
const rateLimiter = new TokenBucketLimiter({ rate: 100, burst: 20 });
```

---

## Do NOT Add References For

- Every line touched (only where traceability adds value)
- Trivial changes (formatting, typo fixes)
- Standard patterns (well-known idioms)
- Test files (unless test approach is an ADR decision)

---

## Reference Documentation

- [Language Patterns](./references/language-patterns.md) - Python, TS, Rust, Go patterns
- [Placement Guidelines](./references/placement-guidelines.md) - When and where to add

---

## Troubleshooting

| Issue                  | Cause                  | Solution                                  |
| ---------------------- | ---------------------- | ----------------------------------------- |
| ADR not found          | Wrong path format      | Use relative path from repo root          |
| Reference not showing  | Comment syntax wrong   | Check language-specific comment format    |
| Too many references    | Over-documenting       | Only add where traceability adds value    |
| Outdated ADR link      | ADR was renamed        | Update path to match current ADR filename |
| Hook reminder annoying | No ADR for this change | Add inline ADR comment or create new ADR  |
