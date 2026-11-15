---
name: ui-sdk-write-docs
description: Write or review ui-sdk website documentation in apps/docs/content/docs, including Core, framework, component, and agent guides. Use for new pages, prose edits, example explanations, and documentation reviews, following the current site's writing style.
metadata:
  internal: true
---

# Write ui-sdk Docs

Write in the website's current style. This skill is for contributors working on the website.

Size the work to the request. For a small edit, such as a sentence, caption, or typo, read the writing guide and the section you're changing, verify any API claim you change, and reread that section. For a new section, new page, or rewrite, follow the steps below. In either case, use only the checks the change reaches.

Honor the requested scope: a review produces findings, a draft stays in chat, and an edit changes files. Treat existing wording and structure as intentional. Preserve the maintainer's edits unless the request calls for revising them; suggest unrelated improvements separately.

## 1. Read the Page and Its Reference

Read [Writing Website Docs](../../../contributing/docs-writing.md) and its main voice reference, Build a Component. Then read the page being changed and choose a reference for that page type from the guide. For a new page, read the neighboring pages so it continues what the reader already knows.

Identify what this page adds and which concepts can be linked instead of repeated.

## 2. Check What the API Does

For behavior you introduce or change in the explanation, inspect the relevant exported types, implementation, and tests. This matters especially for defaults, persistence, cancellation, SSR, and hydration. Resolve mismatches against the actual behavior rather than assuming either prose or JSDoc is correct. Keep planned capabilities separate from shipped behavior.

When writing code examples, follow [ui-sdk-write-code](../ui-sdk-write-code/SKILL.md) and the relevant framework conventions.

## 3. Write the Explanation

Apply the writing guide to the requested scope. For changes shared across framework pages, update the corresponding copies with each framework's actual API. Framework-specific changes stay in the affected framework.

## 4. Read and Verify

Reread the changed section or page using the writing guide's final question. Check links, file titles, snippets, and generated references affected by the edit. Consult [the docs-site guide](../../../contributing/docs-site.md) for the implementation and [the test guide](../../../tests/README.md) for commands when these checks apply:

- **Walkthrough code:** the React and Web Components `docs-walkthrough` tests extract code from Compose Behaviors and their Rendering pages. Check the extraction and run the affected tests when changing those snippets; update the tests if the documented behavior requires it.
- **Headings:** keep `TypeTable` examples maps and incoming fragment links in sync with renamed headings. The maps derive anchors from heading text.
- **Component examples:** `tests/docs/props.spec.ts` checks public API coverage in React examples. Preserve that coverage when replacing or removing examples, and check the corresponding framework copies.
- **Live demos:** run the relevant specs under `tests/docs/` and try changed interactions in the rendered page. Check captions and layout stability. A prose-only edit doesn't need a new demo or a full browser sweep.
- **MDX rendering:** for changes to MDX components, tables, or framework-specific blocks, check both the rendered page and its Markdown export.

Report what changed and what was verified, including checks you couldn't run.
