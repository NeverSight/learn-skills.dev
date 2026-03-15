---
name: wikilinks
description: When generating or editing markdown content, actively look for existing pages to link to and incorporate relevant wikilinks so content is interconnected. Use when writing notes, docs, or any .md content.
---

# Wikilinks in Content

## When to apply

- Generating or editing markdown (`.md`) content
- Writing notes, docs, or knowledge-base material
- User asks for wikilinks, cross-links, or interconnected content

## Core rules

1. **Actively look for link targets**: Before or while generating text, search the codebase (e.g. file tree, grep, or project search) for existing notes or pages that match concepts, people, or terms you mention. Prefer linking to those real pages where possible.

2. **Use double square brackets** for wikilinks: `[[concept]]`, `[[Product Name]]`, `[[Person Name]]`.

3. **Link what matters**: concepts, products, people, domain-specific terms. Prefer linking where a reader might want to jump to a dedicated note.

4. **Targets need not exist**: The linked page does not have to exist yet; if you find a relevant existing note, link to it. Otherwise a new target is fine.

5. **Use aliases for readable prose**: Prefer natural wording over raw filenames.
   - Format: `[[target page|display text]]`
   - Example: `[[1.2.B Local Unit Manager|Unit Manager]]` so the sentence reads “the Unit Manager” not the filename.

6. **Inline, not collected**: Do not add a separate “References” or “See also” section. Place each link in the body where the concept is first or most relevant.

## Examples

**Avoid:**
```markdown
The Unit Manager is responsible for approvals. See 1.2.B Local Unit Manager for details.

## References
- [1.2.B Local Unit Manager](1.2.B%20Local%20Unit%20Manager.md)
```

**Prefer:**
```markdown
The [[1.2.B Local Unit Manager|Unit Manager]] is responsible for approvals.
```

**Multiple links in flow:**
```markdown
[[Project Alpha]] uses the new [[approval workflow]]; the [[1.2.B Local Unit Manager|Unit Manager]] signs off before [[deployment]].
```

## Summary

- Actively search for existing pages that match what you mention; link to them when found
- `[[page]]` or `[[page|label]]` in the main text
- No standalone references section
- Link once where the concept is most relevant
