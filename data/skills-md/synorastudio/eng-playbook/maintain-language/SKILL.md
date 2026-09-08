---
name: maintain-language
description: Maintain bounded project vocabulary in scoped LANGUAGE.md files. Use when defining, renaming, or resolving conflict around a recurring project-specific term. Do not use for general programming concepts or one-off implementation names.
---

# Maintain language

Create and maintain `LANGUAGE.md` files. Follow `LANGUAGE-FORMAT.md`.

`LANGUAGE.md` is vocabulary only.

## Add a term

Add a term only when it is:

- Project-specific.
- Likely to recur across agent or human conversations.
- Useful for preventing ambiguity, synonym drift, or wrong implementation choices.

Do not add general programming concepts, implementation details, plans, decisions, acceptance criteria, or open questions.

## Choose the scope first

Start local unless the term crosses boundaries.

- Root `LANGUAGE.md`: terms shared across multiple project areas.
- Local `LANGUAGE.md`: feature, module, or bounded-area terms.
- `LANGUAGE-MAP.md`: navigation for multiple language files.

Promote a local term to root only when multiple areas need the same meaning.

## Definition style

Use:

```md
**Term**:
One or two sentences defining what the term is.
_Avoid_: Ambiguous synonym, deprecated name
```

Be opinionated. Pick one canonical term and list aliases to avoid.

## Workflow

When changing language:

1. Check existing `LANGUAGE.md` and `LANGUAGE-MAP.md`.
2. Update the smallest relevant language file.
3. Prune obsolete or overly generic terms.
4. Surface conflicts immediately when user language contradicts existing vocabulary.
5. Do not preserve old terms unless they matter for migration, user-facing copy, or external integrations.
6. Check that each changed term has one canonical definition in the smallest relevant language file.
