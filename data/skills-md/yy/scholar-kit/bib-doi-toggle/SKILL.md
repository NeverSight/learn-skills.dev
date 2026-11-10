---
name: bib-doi-toggle
user_invocable: true
description: Toggle DOI, URL, eprint, and ISBN display in a biblatex bibliography. Use when the user asks to show or hide identifiers or make bibliography identifiers available as links.
---

# Toggle bibliography identifiers

Apply this skill only to biblatex projects. Natbib and `.bst` styles require style-specific changes; report that limitation instead of guessing.

## Workflow

1. Use an explicit manuscript path when provided. Otherwise, identify the build entrypoint from the project configuration and TeX structure.
2. Locate the biblatex configuration that controls the target build. It may be in `\usepackage[...]{biblatex}` or `\ExecuteBibliographyOptions{...}`. If multiple build variants use different settings, ask which one to change.
3. Infer `on` or `off` from the request. Ask only when the direction is unspecified.
4. Update the existing configuration in place. Preserve unrelated biblatex options and do not add a duplicate package call.

For `on`, set:

```latex
doi=true, url=true, eprint=true, isbn=false
```

For `off`, set:

```latex
doi=false, url=false, eprint=false, isbn=false
```

Do not change bibliography data or hyperlink styling. If the request specifically requires clickable links, verify that the project has hyperlink support and report any separate change needed. Build with the project's normal entrypoint when available, then report the edited configuration and compilation result.
