---
license: MIT
name: agents-md
description: >
  Create, audit, or trim AGENTS.md and its harness mirrors (CLAUDE.md,
  GEMINI.md, .github/copilot-instructions.md, .cursor/rules) so build/test
  commands stay accurate and the file stays under each harness's size cap.
  Use when the user says "create AGENTS.md", "audit AGENTS.md", "trim
  AGENTS.md", "AGENTS.md is stale", "CLAUDE.md drift", "agent instructions
  hygiene", or invokes /agents-md. Covers nested AGENTS.md for monorepo
  packages, nearest-file precedence, and the bundled
  scripts/agents_md_check.py measurement script. Do NOT use for
  `.github/copilot-instructions.md` authoring or Copilot code-review
  configuration — that is /github-copilot-repo-instructions. Do NOT use for
  personal, per-user, or machine-global instruction files (`~/.claude/CLAUDE.md`,
  personal Copilot instructions) — those are out of scope for this
  repository-scoped skill.
---

# agents-md

Repository-scoped hygiene for `AGENTS.md`: create it, measure it, audit its
content, and check it against its harness mirrors. One canonical file,
harness-neutral, no frontmatter.

> `.github/copilot-instructions.md` authoring and Copilot code-review setup
> live in `/github-copilot-repo-instructions` (if installed). This skill only
> checks that file's mirror status against `AGENTS.md`; it does not write
> Copilot-specific content or `applyTo` path rules.
>
> Personal or machine-global instruction files (a user's own `~/.claude/CLAUDE.md`,
> personal Copilot instructions) are out of scope. This skill only touches
> files committed to the repository.

---

## Why AGENTS.md hygiene matters

AGENTS.md is a vendor-neutral, plain-Markdown convention with no required
fields ([agents.md](https://agents.md)). Every major harness loads the file
in full on every turn, so its length is a per-run token cost, not a one-time
readability cost. A stale command or a bloated file taxes every future turn.

Effectiveness evidence is mixed: keep the file for the token-cost and
precedence reasons above, not on a promise of a guaranteed task-success
lift. See `references/harness-matrix.md` for the sourced detail.

---

## Protocol

### 1. Inventory instruction files

List what exists, repository-relative, root and nested:

```bash
find . -maxdepth 4 \( -name AGENTS.md -o -name CLAUDE.md -o -name CLAUDE.local.md \
  -o -name GEMINI.md -o -path '*/.github/copilot-instructions.md' -o -path '*/.cursor/rules*' \) \
  -not -path '*/node_modules/*'
```

Each harness reads a different subset with different precedence and caps.
Read `references/harness-matrix.md` before assuming one file's presence
or absence is equivalent to another's — nearest-file precedence is the
norm (agents.md spec, Codex, Copilot, Cursor), but Claude Code's own trigger
is different: it reads `AGENTS.md` only when no `CLAUDE.md`/`CLAUDE.local.md`
exists above the working file, or via an explicit `@AGENTS.md` import inside
a `CLAUDE.md`.

### 2. Measure

```bash
python3 "$AGENTS_MD_CHECK" [path/to/AGENTS.md]
```

Resolve `AGENTS_MD_CHECK` from the loaded `SKILL.md` directory
(`scripts/agents_md_check.py`), resolving symlinks first. Do not assume the
skill sits at `skills/agents-md/` in the target repository.

Reports bytes, lines, the heading map, every referenced `just <recipe>`
checked against a nearby `justfile`, every referenced repo-relative path,
and the mirror status of `CLAUDE.md`, `.github/copilot-instructions.md`, and
`GEMINI.md`. Flag a file over ~200 lines as a soft readability warning. The
script also sums the `AGENTS.md` chain from the repository root to each
directory at or below the checked file. A chain over 32 KiB fails outright.
OpenAI Codex concatenates that chain from the root down. It stops adding
files when the combined size reaches `project_doc_max_bytes` (32 KiB by
default), so the files nearest the working directory drop first
(<https://developers.openai.com/codex/guides/agents-md/>).

Root discovery and skip rules follow Codex:

- The root is the nearest directory at or above the checked file that
  contains `.git`. With no `.git`, each chain is the checked file only,
  and the report says "file directory" instead of "repository root".
- Per directory, `AGENTS.override.md` counts when present, else `AGENTS.md`.
- Sizes are raw on-disk bytes, so CRLF line endings count in full.
- The walk skips dot directories, `node_modules`, broken symlinks, and any
  subdirectory with its own `.git` (a nested project root).

Exit codes: 0 when no chain breaches the cap, no mirror has diverged, and
every referenced recipe and path exists. 1 on a cap breach, on any drift
(diverged mirror, missing recipe, or missing path), or when the file does
not exist.

`--json` prints these fields: `path`, `bytes`, `chain_bytes`, `chain_dir`
(the deepest directory of the largest chain, relative to the root),
`root_marker` (true when a `.git` root was found), `lines`, `byte_cap`,
`cap_breach`, `near_cap`, `line_warn`, `headings`, `justfile`,
`referenced_just_recipes`, `missing_recipes`, `referenced_paths`,
`missing_paths`, `mirrors`, `diverged_mirrors`, and `drift`.

### 3. Content audit

For every command and path AGENTS.md names, verify it against the real
repository, not against memory:

- Every backticked `just <recipe>` exists in the `justfile` — the script
  checks this; treat a `FAIL missing just recipes` line as a stale command,
  not a script bug.
- Every backticked repo-relative path exists — same treatment for
  `FAIL missing referenced paths`.
- Quality gates, conventions, and "do not touch" boundaries match the
  project's actual CI and review practice, not an aspirational one.
- PR and commit rules are stated, not implied.

Anti-patterns to flag and remove, per `references/content-checklist.md`:
narrative history, README duplication, secrets or tokens, per-person
preferences, and any command that no longer runs.

### 4. Mirror strategy

Keep exactly one canonical `AGENTS.md`. For each mirror:

- `CLAUDE.md`: either absent, or contains only `@AGENTS.md` (a Claude Code
  import — <https://code.claude.com/docs/en/memory>). Do not duplicate
  content into it.
- `.github/copilot-instructions.md`: either absent (Copilot reads
  `AGENTS.md` directly) or a short pointer. If the user wants Copilot-specific
  content (path-scoped `applyTo` rules, code-review knobs), route to
  `/github-copilot-repo-instructions` — do not author that file here.
- `GEMINI.md`: either absent or a short pointer, same pattern as CLAUDE.md.

Report any mirror the check script marks `diverged` as drift, and propose
collapsing it to a pointer or removing it.

### 5. Nested AGENTS.md

For a monorepo or multi-package layout, put a nested `AGENTS.md` in each
package that needs its own rules. Codex, Claude Code, Cursor, Gemini CLI,
and Copilot CLI load the nested file together with every ancestor file. No
harness replaces the root file with the nested file. The nearer file wins
only on conflict. See `references/harness-matrix.md` for each harness.

- Put only the subtree's delta in the nested file: its own commands,
  boundaries, and exceptions. A copied root rule loads twice on every turn
  and drifts.
- State each exception to a root rule explicitly, and name the root rule
  that it replaces. VS Code warns that harnesses do not share one
  precedence order.
- Keep every root-to-leaf chain under the Codex 32 KiB cap. Codex drops
  the nearest files first.
- Claude Code reads a nested `AGENTS.md` only when that directory has no
  `CLAUDE.md` of its own.

### 6. Trim or rewrite

Propose changes as a diff against the current file. Ask before overwriting
`AGENTS.md` or any mirror. Use `assets/AGENTS.md.template` as the starting
shape for a new file, not as boilerplate to paste unedited — every section
must reflect this repository's actual commands and boundaries.

### 7. Verify

```bash
python3 "$AGENTS_MD_CHECK" --self-test
python3 "$AGENTS_MD_CHECK"
```

Both must exit 0. Re-run any command the audit changed or added before
reporting done.

---

## Rules

- One canonical `AGENTS.md` per directory scope. Mirrors point at it; they
  do not restate it.
- Never invent a command or path. Every backticked `just <recipe>` and
  every referenced path must exist — the check script verifies this, do
  not skip it.
- Do not add narrative, README duplication, secrets, or per-person
  preferences. See `references/content-checklist.md` for the full list.
- Do not write `.github/copilot-instructions.md` content beyond a short
  pointer — that authoring belongs to `/github-copilot-repo-instructions`.
- Do not touch personal or machine-global instruction files.
- Ask before overwriting an existing `AGENTS.md` or mirror; show the diff
  first.

## References

- `references/harness-matrix.md` — which harness reads which file, with
  precedence and size caps, cited.
- `references/content-checklist.md` — what belongs in AGENTS.md and what
  does not. Harness-behavior claims are cited; the lists are this skill's
  guidance.
- `assets/AGENTS.md.template` — a short, sectioned starting template.
