---
name: documentation
description: Governs code comments, API documentation, JSDoc/TSDoc typing docs, README standards, and prevents verbose filler documentation.
---

# Documentation & Comments Skill

Activate this skill when documenting modules, writing API specifications, authoring READMEs, adding inline code comments, or updating project memory.

> **Documentation Law:** *Document the "Why" and non-obvious constraints, never the self-evident "What".*

---

## 1. Code Comments: Document "Why", Not "What"

* **High-Value Comments (Encouraged):**
  - Documenting subtle edge cases, workaround for upstream library bugs, concurrency locks, or regulatory/compliance reasons.
  - Explaining complex mathematical algorithms, bitwise tricks, or performance-critical micro-optimizations.
* **Low-Value Comments (Forbidden):**
  - Restating obvious code (`// increment counter by 1`, `// return user object`).
  - Stale comments that no longer match the active code behavior.

---

## 2. JSDoc / TSDoc Standards for Public APIs

For public functions, exported hooks, and library interfaces, provide concise TSDoc comments:

```ts
/**
 * Synchronizes multi-agent adapter rules across 10+ AI coding assistant platforms.
 *
 * @param workspaceRoot - Absolute path to the active project root directory.
 * @param options - Synchronization flags including overwrite behavior and verbosity.
 * @returns Array of relative file paths that were generated or updated.
 * @throws {Error} If workspaceRoot does not exist or lacks write permissions.
 */
export async function syncAdapters(
  workspaceRoot: string,
  options: SyncOptions = {}
): Promise<string[]> {
  // ...
}
```

---

## 3. Evidence-Based Project Documentation Invariants

1. **Zero Placeholder Documentation:** Never ship generic `"TODO: Add documentation here"` blocks in production memory files.
2. **Verifiable Command Examples:** Every command listed in READMEs or `.ai/` documentation must be directly runnable in the project workspace with zero guesswork.
3. **Keep a Changelog Standard:** Record public releases in `CHANGELOG.md` following Semantic Versioning (`MAJOR.MINOR.PATCH`) with categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
