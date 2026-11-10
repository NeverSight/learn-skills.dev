---
name: wiki-merge
description: "Merge an overlap cluster of Vault concepts into one canonical concept, rewrite wikilinks, and preserve a dry-run/apply boundary. Use when $wiki-curate has identified a winner and fold-in slugs. Not for general wiki auditing or automatic article promotion."
allowed-tools: Bash, Read
argument-hint: "[--apply] <winner-slug> <loser-slug-1> [<loser-slug-2> ...]"
---

# Wiki Merge — Collapse an Overlap Cluster

> Folds one or more concept slugs into a single canonical entry.
> Preserves provenance, rewrites incoming wikilinks across atlas /
> books / concepts / project knowledge folders, deletes the losers,
> and denylists them so the Saturday `wiki-grow` cron doesn't
> re-promote.

## When to Use

- Right after `wiki-curate` flags an overlap cluster in Section A
  and you've decided which slug should be canonical.
- Manual cleanup when you notice two concepts that should be one.

## When NOT to Use

- For trivial renames — keep both files and add an alias.
- For tag normalisation — that's edit-in-place, not a merge.
- When the "overlap" turns out to be a genuine sub-concept relation
  — keep both, add a `[[wikilink]]` reference between them instead.

---

## What it does

```
uv run python scripts/wiki-merge.py <winner> <loser1> [<loser2> ...]
uv run python scripts/wiki-merge.py --apply <winner> <loser1> [<loser2> ...]
```

Steps performed (in order, only on `--apply`):

1. **Read** winner + every loser concept file under `~/vault/concepts/`.
2. **Build merged body** — winner's body verbatim, then each loser's
   body under a `## From <loser-slug>` section. Each section includes
   a small admonition naming the source project + promotion date for
   traceability. Sub-headings in loser bodies are demoted by one
   level (`##` → `###`) so they don't compete with the new section
   delimiter.
3. **Build merged frontmatter** — winner's fields preserved; tags
   becomes the union of winner ∪ loser tags; a new `fold_in_sources:`
   block records each loser's slug + source_project + promoted_on
   date; `last_merged:` is set to today.
4. **Write merged content** back to the winner's file.
5. **Rewrite wikilinks** — every `[[<loser-slug>]]` (with or without
   alias suffix) across atlas topics, book chapters, other concepts,
   and project knowledge folders gets rewritten to
   `[[<winner-slug>|<original-display-text>]]`. The alias keeps the
   original display label visible so the change isn't jarring on
   pages that referenced the loser by name.
6. **Delete loser files** from `~/vault/concepts/`.
7. **Append to denylist** — each loser slug is added to
   `~/vault/concepts/.denylist` with a comment noting the
   merge date. This stops the Saturday `wiki-grow` cron from
   re-promoting the loser slug if a project knowledge article with
   that slug still exists.

## Dry-run output

Default invocation (no `--apply`) prints a plan:

```
Merge plan (dry-run):
  Winner:  goodharts-law  (concepts/goodharts-law.md)
  Fold in: goodhart-taxonomy, goodhart-resistance
  Merged file size: 11666 chars (winner was 3516)
  Wikilink rewrites: 12 file(s)
    concepts/strategic-classification.md: 1 occurrence(s)
    .../knowledge/goodhart-resistance.md: 1 occurrence(s)
    ...
  Denylist additions: goodhart-taxonomy, goodhart-resistance
  Files to delete: concepts/goodhart-taxonomy.md, concepts/goodhart-resistance.md

(dry-run — pass --apply to perform the merge)
```

Inspect the file count and the rewrite targets. If anything looks
wrong (e.g. a loser slug is wildly overrepresented across the corpus
suggesting it's actually a distinct concept), abort and reconsider.

## Apply

```
uv run python scripts/wiki-merge.py --apply goodharts-law goodhart-taxonomy goodhart-resistance
```

Performs all six steps. After the run:

- `~/vault/concepts/goodharts-law.md` contains the merged
  content with fold-in provenance in frontmatter.
- `goodhart-taxonomy.md` and `goodhart-resistance.md` are deleted.
- All atlas/books/concepts/project-knowledge files that wikilinked to
  the loser slugs now wikilink to the winner with the original
  display label preserved as the alias.
- `~/vault/concepts/.denylist` has two new lines.

**Verify with `wiki-curate`** — the goodhart cluster should be gone
on the next run.

---

## Safety properties

- **Dry-run is default.** Forgetting `--apply` previews only.
- **Loser frontmatter preserved in `fold_in_sources:`** — even though
  the loser file is deleted, the merged file records source_project +
  promoted_on for each fold-in, so the provenance is recoverable.
- **Wikilinks preserve display labels** — rewrite produces
  `[[winner|Original Display]]` form, so a topic page that wrote
  `[[Goodhart Taxonomy]]` will still render "Goodhart Taxonomy" after
  the merge, just pointing at `goodharts-law` now.
- **Denylist prevents re-promotion** — if a project still has
  `<loser-slug>.md` in its knowledge folder, the next Saturday cron
  won't re-promote it.

## Anti-patterns

- **Don't merge a curated concept INTO an auto-generated one.** If
  you must, swap winner/loser. Curated content should be the
  canonical surface.
- **Don't merge concepts from different domains** just because slugs
  share a token (e.g. `model` token in `language-model` and
  `linear-model`). Use judgement.
- **Don't merge without dry-running first.** The dry-run output is
  the only confirmation step.

---

## Cross-References

| Skill | Relationship |
|-------|-------------|
| `wiki-curate` | Identifies the clusters this skill collapses. |
| `wiki-grow` | Writer of auto-promoted concepts; denylist entries from `wiki-merge` prevent it from re-promoting losers. |
| `compile-knowledge` | Source of project knowledge articles that get promoted to concepts. |
