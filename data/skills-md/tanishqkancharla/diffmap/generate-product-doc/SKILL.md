---
name: generate-product-doc
description: Create general-purpose visual documents with productdoc, including live previews of components and user flows from Storybook stories. Use to explain existing systems, plan future work, review changes through user behavior, workflows, or involved services, or preview components and review a user journey across several UI states.
---

# Productdoc

Before writing or updating a document, run this from the repository root and follow what it prints:

```sh
npx product-doc guide
```

The CLI guide owns the authoring instructions and document format, keeping them version-matched to the viewer. If `guide` is unavailable in an installed release, run `npx product-doc update`, then retry.

**Migration:** productdoc succeeds Diffmap; the two skills coexist temporarily. Keep existing documents rather than creating migration copies.
