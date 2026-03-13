---
name: bulk-generate-concepts
description: Use when generating multiple curriculum-aligned concept files in parallel (5+ concepts) - researches curriculum, creates concept list, spawns parallel generation agents, orchestrates review loop until all pass
---

# Bulk Generate Concepts

## Process

1. **Clarify scope** - Subject, grades, curriculum standard (e.g., German Rahmenlehrplan)

2. **Create feature branch** - Before any work:

   ```bash
   git fetch origin dev
   git checkout -b concepts/{subject}-grade{N} origin/dev
   ```

   Branch naming: `concepts/{subject}-grade{N}` (e.g., `concepts/german-grade4`)

3. **Research curriculum ONCE** - Use official sources (ministry sites). Extract:
   - Learning objectives per concept
   - Age-appropriate expectations
   - Difficulty progression
   - Key terminology

   Save to `docs/research/{subject}-curriculum-research.md` with:
   - Concept list (IDs, titles, grades, scope)
   - Extracted curriculum details per concept
   - Source URLs

   Get user approval on concept list.

4. **Spawn parallel agents** - One Task tool call per concept:

   ```
   Create concept: {subject}/{concept-id} (Grade {grade})

   1. Read `docs/concept-rules.md` first
   2. Use write-concept skill
   3. Reference `docs/{subject}-curriculum-research.md` for curriculum context
   4. **SKIP RESEARCH**: All content is provided!

   Scope: {one-sentence scope description}
   ```

   **Do NOT paste curriculum content into agent prompts.** Agents read the research doc themselves. Keep prompts minimal.

5. **Verify files exist** - Check that concept files were actually created. Agents may report success without writing files.

6. **Validate** - Use `bun run check:concepts` to efficiently check the generated concepts. If failures, resume agents with fixes.

7. **Commit and create PR** - Stage, commit, push, and open PR against `dev`:

   ```bash
   git add content/subjects/{subject}/ packages/frontend/public/locales/
   git commit -m "feat(content): add {Subject} Grade {N} concepts (curriculum aligned)"
   git push -u origin concepts/{subject}-grade{N}
   gh pr create --base dev --title "feat(content): {Subject} Grade {N} concepts" --body "Add {N} new concepts for Grade {N} {Subject} based on {curriculum}."
   ```

8. **Cleanup** - Delete `docs/{subject}-curriculum-research.md` after PR is created.

## Constraints

- Max 12-14 concepts per grade (consolidate if curriculum suggests more)
- Subagents read write-concept skill themselves - don't duplicate rules
- Research happens ONCE in parent, not per-agent (saves tokens)

## Common Rationalizations

| Thought                                                                   | Reality                                                                                                                                                                        |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| "The PDF isn't readable, I'll use a different state's curriculum instead" | WRONG. Ask the user which curriculum to use. Different states have different standards, terminology, and grade-level expectations. Never substitute without explicit approval. |
| "German curricula are similar enough across states"                       | WRONG. While KMK provides national standards, state implementations differ significantly. The user chose a specific curriculum for a reason.                                   |
| "I'll research what I can find and ask later"                             | WRONG. Clarify the curriculum source BEFORE researching. Wasted research on the wrong curriculum wastes tokens and time.                                                       |
| "This curriculum has better web content, so I'll use it"                  | WRONG. Accessibility doesn't equal correctness. If the target curriculum is hard to access, ask the user for alternative sources or approval to use a substitute.              |
