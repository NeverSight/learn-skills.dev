---
name: ea-connected-vault-setup
description: Organize a sparse, mostly unconnected Markdown/Obsidian vault into a light topic hierarchy. Use when a user wants 5–10 topic root notes, a capitalized `Parents` list assigning notes to topic roots, an embedded Obsidian Base that lists each root's children, and meaningful body-level/`Related` wikilinks that make concept notes navigable without substantive rewriting.
---

# EA Connected Vault Setup

Create a **light navigation layer**, not a new taxonomy or a content rewrite. Preserve every note's text, existing properties, filenames, folders, templates, query blocks, and links unless the requested linking requires a small additive edit.

## Scope and safety

- Work only on the user-designated corpus. Exclude configuration, templates, attachments, generated/cache folders, daily logs, and existing database/query files unless the user includes them.
- Search filenames, aliases, frontmatter keys, links, and existing root/MOC notes before creating anything. Reuse a clearly matching root rather than duplicating it.
- Use the exact, capitalized property names `Parents` and `Related`. Both are YAML/Markdown lists of wikilinks, even when they initially contain one item. Do not replace populated values; merge without changing their existing representation or casing.
- In this initial setup, give each child exactly one `Parents` entry: its cluster root. Do not introduce multiple root assignments.
- Do not infer a topical relationship from name similarity alone. Leave uncertain notes in a deliberately named holding root (for example, `Unsorted concepts`) and flag them.
- This operation changes many files. First produce an inventory and proposed clustering; obtain confirmation before writing. After approval, apply only additive, minimal diffs and report every created/changed file.

## 1. Inventory and cluster proposal

1. Read each in-scope Markdown note's title, aliases, frontmatter, headings, outbound links, and enough body text to establish its subject. Read linked context when it resolves ambiguity.
2. Exclude the future root notes from the child count. Identify existing hubs, broad concepts, and duplicate/near-duplicate titles.
3. Propose topic clusters that are semantically coherent and navigable:
   - Target **5–10** roots for a substantial collection.
   - Target roughly **8–15 child notes per root**. Use fewer roots for a small corpus; split an oversized coherent cluster only when it has a meaningful internal division.
   - Give each root a specific, durable, plural-friendly name (for example, `Plant functional traits`, not `Miscellaneous`).
   - Assign every in-scope note exactly one proposed root, with a one-line reason for ambiguous assignments.
4. Present the proposal as a compact table: root name, intended scope, child count, and any uncertain notes. Do not write yet.

## 2. Create roots and the child Base

After approval:

1. Create the shared Base at `__Support/Bases/Children by Parents.base` unless the user specifies another support location. Copy the bundled [`assets/Children by Parents.base`](assets/Children by Parents.base) verbatim.
2. Create a `Roots/` folder at the vault root if it does not already exist. Create every new root note in `Roots/`, using that vault's root/topic template when one exists. If there is no template, use this minimal structure:

   ```md
   ---
   ---

   # Root name

   > [!note] AI-generated
   > Created by EA Connected Vault Setup as a navigation root. Review the cluster boundary before treating it as a settled taxonomy.

   ![[__Support/Bases/Children by Parents.base]]
   ```

   Keep the embed directly below the title/provenance. The Base resolves `this` to the root that embeds it, so the same file lists the correct children in every root. Its table displays the child **Note** first, followed by its **Related** list.
3. If a reused root already exists outside `Roots/`, leave it in place; do not rename or move it. Add the Base embed only if it has no equivalent child listing, and do not overwrite or rearrange its content.

The Base contents are:

```yaml
filters: 'Parents.contains(this.file)'
properties:
  file.name:
    displayName: Note
  Parents:
    displayName: Parents
  Related:
    displayName: Related
views:
  - type: table
    name: Children
    order:
      - file.name
      - Related
```

## 3. Assign each child

For every approved in-scope, non-root note:

1. Add this list to the existing YAML frontmatter. Preserve ordering and formatting otherwise:

   ```yaml
   Parents:
     - "[[Root name]]"
   ```

2. If the note lacks YAML frontmatter, add a minimal block containing this `Parents` list.
3. Do not change an existing non-empty `Parents` list without flagging it in the review report. If it clearly points to an obsolete equivalent, ask before replacing it.
4. Verify every `Parents` target resolves to a root note and every root Base has at least one expected child.

## 4. Make each note alive with discourse-advancing body links

Make a separate pass after parent assignment. A frontmatter list is only a navigation aid: it must not be the sole connection between notes. Review **every substantive paragraph** rather than aiming for a quota.

For each candidate target, read the target note and score the prospective link. Add it only when its overall case is strong; the purpose is to deepen the note's line of thought, not to make its graph denser.

| Criterion | 0 points | 1 point | 2 points |
| --- | --- | --- | --- |
| **1. Available target** | No suitable existing note. | A broadly adjacent note exists. | A specific existing note directly covers the concept, mechanism, method, evidence, or implication. |
| **2. Contribution to discourse** | Merely interesting, decorative, or navigational. | Helpful context. | Advances the paragraph's reasoning: it defines a premise, supplies a mechanism, qualifies a claim, provides evidence, or opens a necessary next question. |
| **3. Existing treatment** | The target is already linked nearby and another link adds no value. | Mentioned/linked elsewhere in the note, but this paragraph needs a local entry point. | Not already linked in the relevant context, or a deliberate repeated link materially improves navigation. |
| **4. Minimal integration** | Requires new claims or rewriting. | Requires a short contextual line below the paragraph. | Can be integrated by linking an existing phrase or making only a word-level edit. |
| **5. Semantic precision** | The relationship is ambiguous or misleading. | Plausible but indirect. | The link label and target accurately express the exact relationship implied by the paragraph. |
| **6. Reader utility** | The reader gains little by opening it. | Useful background. | Opening the target is likely to resolve a real conceptual, methodological, or evidential need created by this paragraph. |

- Add inline links for candidates scoring **9–12**, and normally reject candidates scoring **0–6**. Treat **7–8** as editorial judgment: retain only when the link clearly improves the reader's path through the argument.
- Prefer direct inline links. Convert a natural, unlinked mention to `[[Canonical note title|visible phrase]]`. Make only the smallest word-level edit necessary for a grammatical, precise anchor; never alter a source claim or manufacture a sentence.
- When a candidate clears the threshold but lacks a natural anchor, add a compact contextual line immediately below the relevant existing paragraph, for example:

  ```md
  *Related: [[Concept A]] and [[Concept B]].*
  ```

  This line must qualify or extend that paragraph without adding an unverified claim. Do not append detached link dumps or use these lines to satisfy a quota.
- Add or merge the strongest body-level connections into a capitalized `Related` list in frontmatter. There is **no fixed length**: include only the compact set of links that remains useful as navigation. `Related` supplements body links rather than replacing them:

  ```yaml
  Related:
    - "[[Concept A]]"
    - "[[Concept B]]"
  ```

- Preserve existing links and `Related` values. A second contextual link to the same note is valid only when it gives a later paragraph its own needed entry point. If no candidate clears the threshold, add none and list the note for human review.

## 5. Validate and report

- Confirm that each child has exactly one resolving `Parents` entry.
- Confirm that every Base file is valid YAML and its filter is exactly `Parents.contains(this.file)`.
- Check that every substantive paragraph was considered against the link score, that each added link meets the discourse/precision threshold, and that `Related` only supports rather than substitutes for those links.
- Check for broken wikilinks introduced by this setup and for accidental links to the Base/template itself.
- Report: `Roots/` folder created/reused, roots created/reused, Base location, number of children assigned, number of inline/contextual links and `Related` lists added, uncertain notes, and anything intentionally untouched.
- Clearly label the root notes as AI-created; do not add AI-generated prose to existing notes beyond the requested structural properties and links.
