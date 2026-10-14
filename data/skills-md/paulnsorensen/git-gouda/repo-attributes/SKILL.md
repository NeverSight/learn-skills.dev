---
license: MIT
name: repo-attributes
description: >
  Configure .gitattributes, .editorconfig, .gitignore, and Git LFS filters
  for a repository: normalize line endings, mark generated, vendored, and
  documentation paths for GitHub linguist, set per-language editor
  defaults, and merge .gitignore content from GitHub templates. Use when
  the user says "add .gitattributes", "fix line endings", "CRLF",
  "linguist", "mark generated files", "set up .editorconfig", "gitignore
  template", "git lfs", or invokes /repo-attributes. Do NOT use for prek
  or pre-commit hook configuration — use /prek. GitHub custom properties
  (organization-level metadata) are out of scope; this skill only touches
  per-repository attribute, editor, and ignore files. Community health
  files (README, LICENSE, CODE_OF_CONDUCT, CONTRIBUTING, SECURITY) belong
  to /oss-hygiene, not this skill.
---

# repo-attributes

Configures the file-level attribute layer of a repository: `.gitattributes`, `.editorconfig`, `.gitignore`, and Git LFS filter patterns.

This is repository-only configuration. It does not touch pre-commit hooks, CI pipelines, org-level custom properties, or community health files.

## Where this skill fits

| Concern | Skill |
|---|---|
| Line endings, linguist overrides, editor defaults, ignore rules, LFS patterns | **`/repo-attributes`** (this skill) |
| Pre-commit / prek hook selection and `prek.toml` | `/prek` |
| Community health files (README, LICENSE, CODE_OF_CONDUCT, CONTRIBUTING, SECURITY) | `/oss-hygiene` |
| Org-wide settings as code, including custom properties | `/safe-settings` |

## Protocol

### 1. Detect language markers and existing config

Scan the repo root for language markers, reusing the same detection approach as `/prek`:

| Marker file | Language/Framework |
|---|---|
| `Cargo.toml` | Rust |
| `pyproject.toml`, `setup.py`, `requirements.txt` | Python |
| `package.json` | TypeScript/JavaScript |
| `go.mod` | Go |
| `Gemfile` | Ruby |
| `*.sh`, `zsh/`, `bin/` | Shell |
| `Dockerfile` | Docker |

Multiple markers mean a polyglot project. Cover every detected language in the generated files.

Check for existing `.gitattributes`, `.editorconfig`, `.gitignore`, and `.gitmodules`. Read each file present and treat its content as a floor, not a target for replacement.

Check for Git LFS usage:

```bash
git lfs ls-files
```

When `git lfs` is not installed, skip LFS detection and say so; do not guess at LFS-tracked paths.

### 2. Propose `.gitattributes`

Use `assets/gitattributes.example` as the starting shape. Include, based on step 1 detection:

- `* text=auto` — let Git normalize line endings for text files it detects.
- Explicit `eol=lf` for scripts and other files that must never gain CRLF, for example `*.sh text eol=lf`.
- Binary markers for asset types that must skip line-ending and diff conversion, for example `*.png binary`.
- `linguist-generated`, `linguist-vendored`, and `linguist-documentation` for paths that should not count toward the GitHub language bar or code review diffs.
- `merge=union` for append-only files such as `CHANGELOG.md`, so parallel entries merge instead of conflicting.
- `export-ignore` for paths that should not ship in `git archive` output, for example CI-only directories.
- `diff=` drivers for file types with a more useful semantic diff (for example `*.md diff=markdown`, when the driver is already configured).
- LFS patterns (`filter=lfs diff=lfs merge=lfs -text`) for any path already tracked by `git lfs ls-files`, or ones the user names.

Diff the proposal against any existing `.gitattributes` and ask before overwriting a line that already exists with different content.

### 3. Propose `.editorconfig`

Use `assets/editorconfig.example`. Include `root = true`, a `[*]` section with `charset`, `end_of_line`, `insert_final_newline`, `trim_trailing_whitespace`, `indent_style`, and `indent_size`, then one override section per detected language for its idiomatic indent style (for example tabs for Go and Makefiles, four-space indents for Python).

### 4. Propose `.gitignore`

Fetch the templates GitHub ships for the detected languages:

```bash
gh api /gitignore/templates
gh api /gitignore/templates/{name} --jq .source
```

Merge the fetched template content with any existing `.gitignore`. Append missing template lines; never remove an existing user entry, even one that looks redundant.

### 5. Renormalize line endings (only when authorized)

When `.gitattributes` changes alter how tracked files should be stored, `git add --renormalize .` rewrites tracked file content to match the new rules. This is a destructive rewrite of tracked content, so:

- Require a clean working tree first: `git status --porcelain` must print nothing.
- Require explicit user authorization before running the command. Never renormalize as a side effect of proposing `.gitattributes`.
- If the tree is dirty, stop and ask the user to commit or stash before renormalizing.

### 6. Verify

```bash
git check-attr -a <file>
git ls-files --eol
gh api repos/{owner}/{repo}/languages
```

Use `git check-attr -a <file>` to confirm the attributes applied match the proposal. Use `git ls-files --eol` to confirm working-tree and index line endings agree with `.gitattributes`. Use the GitHub `languages` API call to confirm linguist overrides changed the reported language mix, after the change reaches GitHub.

## What this skill is NOT for

- Pre-commit or prek hook selection — that's `/prek`.
- GitHub custom properties or other organization-level metadata — out of scope for this skill.
- Community health files (README, LICENSE, CODE_OF_CONDUCT, CONTRIBUTING, SECURITY) — that's `/oss-hygiene`.
- CI pipeline configuration — not a repo-attributes concern.

## Gotchas

- `* text=auto` alone does not force LF for scripts on a contributor's Windows checkout; pair it with an explicit `eol=lf` rule for files that must not gain CRLF.
- `linguist-generated` and `linguist-vendored` change the GitHub language bar and default PR diff collapsing, not local `git diff` output.
- `git add --renormalize .` only rewrites the index and working tree; it does not rewrite history. Existing clones still show the old line endings until they pull and re-run it themselves.
- LFS filter patterns without `git lfs install` run locally have no effect; confirm LFS is installed before proposing filter patterns as the fix for a large-file problem.
- `.gitignore` only affects untracked files. A path already tracked keeps being tracked until it is explicitly removed with `git rm --cached`.

## References

- `references/attributes.md` — cited sources for `.gitattributes`, linguist overrides, `.editorconfig`, line-ending configuration, `.gitignore`, and Git LFS.
