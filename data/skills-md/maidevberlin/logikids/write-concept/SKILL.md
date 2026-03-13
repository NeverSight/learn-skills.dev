---
name: write-concept
description: Use when creating or improving educational concept files - includes curriculum research for new concepts, always updates translations before validation
---

# Write Concept

## Process

### 1. Understand

- Clarify: country, subject, grade, concept scope
- Ask user if anything is unclear

### 2. Research (new concepts only)

- **Skip if curriculum info provided** (e.g., from bulk-generate-concepts)
- Otherwise: WebSearch `"[country] [subject] curriculum [grade]"`
- Find official curriculum documents
- Extract: concept scope, learning objectives, difficulty progression

### 3. Read rules

- `docs/concept-rules.md`
- `content/schema.ts`

### 4. Write/edit concept file

- Location: `content/subjects/{subject}/official/{id}.md`
- Follow concept-rules.md for all field requirements
- **Always update:** `version` (increment) and `version_notes` (describe changes)
- **Prerequisites:** Check `content/subjects/{subject}/official/` for existing concept IDs

### 5. Update translations

- Update ALL files: `packages/frontend/public/locales/*/subjects/{subject}.json`
- Key: `concepts.{concept-id}` with `name` and `description`

### 6. Validate

```bash
bun run check:concepts {subject}/{concept-id}
```

## Red Flags

- "I'll skip curriculum research" → You won't know what to put in fields
- "I'll add examples to help the AI" → CARDINAL RULE violation
- "Problem types look similar but different" → Not distinct enough
