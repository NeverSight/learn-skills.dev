---
name: add-molab-badge
description: Add "Open in molab" badge(s) linking to marimo notebooks. Works with READMEs, docs, websites, or any markdown/HTML target.
---

# Add molab badge

Add "Open in molab" badge(s) linking to marimo notebooks. The badge can be added to any target: a GitHub README, documentation site, blog post, webpage, or any other markdown/HTML file.

## Instructions

### 1. Determine the notebook links

The user may provide notebook links in one of two ways:

- **User provides links directly.** The user pastes URLs to notebooks. Use these as-is — no discovery needed.
- **Notebook discovery (README target only).** If the user asks you to add badges to a repository's README and doesn't specify which notebooks, discover them:
  1. Find all marimo notebook files (`.py` files) in the repository. Use `Glob` with patterns like `**/*.py` and then check for the marimo header (`import marimo` or `app = marimo.App`) to confirm they are marimo notebooks.
  2. If the README already has links to notebooks (e.g., via `marimo.app` links or existing badges), replace those.
  3. Otherwise, ask the user which notebooks should be linked.

### 2. Construct the molab URL

For each notebook, construct the molab URL using this format:

```
https://molab.marimo.io/github/{owner}/{repo}/blob/{branch}/{path_to_notebook}
```

- `{owner}/{repo}`: the GitHub owner and repository name. Determine from the git remote (`git remote get-url origin`), the user-provided URL, or by asking the user.
- `{branch}`: typically `main`. Confirm from the repository's default branch.
- `{path_to_notebook}`: the path to the `.py` notebook file relative to the repository root.

### 3. Apply the `/wasm` suffix rules

- If **replacing** an existing `marimo.app` link, append `/wasm` to the molab URL. This is because `marimo.app` runs notebooks client-side (WASM), so the molab equivalent needs the `/wasm` suffix to preserve that behavior.
- If adding a **new** badge (not replacing a `marimo.app` link), do **not** append `/wasm` unless the user explicitly requests it.

### 4. Format the badge

Use the following markdown badge format:

```markdown
[![Open in molab](https://marimo.io/molab-shield.svg)](URL)
```

Where `URL` is the constructed molab URL (with or without `/wasm` per the rules above).

For HTML targets, use:

```html
<a href="URL"><img src="https://marimo.io/molab-shield.svg" alt="Open in molab" /></a>
```

### 5. Insert or replace badges in the target

- When replacing existing badges or links:
  - Replace `marimo.app` URLs with the equivalent `molab.marimo.io` URLs.
  - Replace old shield image URLs (e.g., `https://marimo.io/shield.svg` or camo-proxied versions) with `https://marimo.io/molab-shield.svg`.
  - Set the alt text to `Open in molab`.
  - Preserve surrounding text and structure.
- Edit the target file in place. Do not rewrite unrelated sections.
- If the user just wants the badge markdown/HTML (not editing a file), output it directly.

## Examples

**Replacing a marimo.app badge in a README:**

Before:
```markdown
[![](https://marimo.io/shield.svg)](https://marimo.app/github.com/owner/repo/blob/main/notebook.py)
```

After:
```markdown
[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/owner/repo/blob/main/notebook.py/wasm)
```

Note: `/wasm` is appended because this replaces a `marimo.app` link.

**Adding a new badge from user-provided links:**

User says: "Add molab badges for these notebooks: `https://github.com/owner/repo/blob/main/demo.py`, `https://github.com/owner/repo/blob/main/tutorial.py`"

Output:
```markdown
[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/owner/repo/blob/main/demo.py)
[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/owner/repo/blob/main/tutorial.py)
```

Note: no `/wasm` suffix by default for new badges.
