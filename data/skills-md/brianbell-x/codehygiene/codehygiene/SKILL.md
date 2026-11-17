---
name: codehygiene
description: >-
  Offline readability gate (~7-50 ms on small diffs) for touched code in Python, TypeScript, JavaScript, Rust, Go, C, C++, Zig, Java, C#, and Lua. Catches structural smells formatters miss: narrator comments, swallowed errors, deep nesting, `*Factory`/`*Manager` ceremony, cryptic 1-2 char names, magic indices, and duplicated blocks. Use on newly written or modified functions and small diffs rather than full-repository sweeps.
---

# Code Hygiene

Passing tests, typecheckers, and formatters (`ruff`, `eslint`, `prettier`, `rustfmt`, `gofmt`, `clang-format`) verifies execution and surface syntax rather than structural readability. Run `codehygiene` on newly written or modified code to catch AI slop and structural smells while applying engineering judgment to every diagnostic.

## Preview Status & Scope Disclaimer

- **Early preview & benchmark collection:** `codehygiene` is not a finished release; circuit thresholds still need work, and false positives or missed edge cases occur. Real-world user review and issue reports directly guide circuit fixes and build stronger readability benchmarks.
- **Clean code that may diverge from traditional linters:** `codehygiene` produces clean, flat, low-ceremony code in ways traditional rule-based linters (`ruff`, `eslint`, `pylint`, `clippy`) do not check and may occasionally disagree with—such as favoring early guard returns over single-exit rules, removing restated boilerplate docstrings, or rejecting lint-suppression comments. When an active project linter rule directly conflicts in CI, keep project CI green rather than ping-ponging between tools.
- **Step 1 toward harness hooks (not a long-term skill):** `codehygiene` is best run deterministically as a zero-token hook inside an agent harness (`PostToolUse`, `Stop`, or lint hooks) rather than inside prompt context as an agent skill. Shipping this skill is Step 1 to collect real-world feedback and benchmark cases for improvements.
- **Poor fit and high token cost on large codebases:** Applying skill-driven refactor loops across large repositories, multi-file sweeps, or long legacy modules does not work well yet and can burn heavy tokens. Keep checks scoped to small touched diffs, and warn the user before attempting any broad or repo-wide pass (offer a read-only `--json` check on 1–2 target files instead).

## Run It

The pure-NumPy runtime (`__init__.py`, `__main__.py`) and `weights.npz` (`14.5 KiB` `1.58-bit` ternary model) are bundled inside `<SKILL_DIR>` (the directory containing this `SKILL.md`) and run offline across macOS, Linux, and Windows:

```bash
python3 "<SKILL_DIR>" <touched-files> --check --no-color
```

- Active virtualenv, conda, or Windows `python`: `python "<SKILL_DIR>" <touched-files> --check --no-color`
- Environments without `numpy` preinstalled: `uv run --with numpy "<SKILL_DIR>/__init__.py" <touched-files> --check --no-color`
- Installed on `PATH`: `codehygiene <touched-files> --check --no-color`
- Line-level inspection on existing files or piped `stdin`: pass `--json`

Supported extensions (`11` languages): `.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.mjs`, `.cjs`, `.rs`, `.go`, `.c`, `.h`, `.cc`, `.cpp`, `.cxx`, `.hpp`, `.zig`, `.java`, `.cs`, `.lua`.

## Workflow

1. **Verify behavior first:** Pass syntax checks, typecheckers, and unit tests before running `codehygiene`.
2. **Scope to small touched diffs:** Pass only newly created or substantially edited files from the current turn (skip mechanical multi-file renames and sweeps across large legacy files). On existing files, pass `--json` and inspect only line ranges modified in this turn.
3. **Apply high-value fixes (at most 2 passes):** Fix genuine squiggles (`>= 0.55`) in touched code, then re-run `codehygiene` and tests once. Cap cleanup at 2 passes to avoid token-heavy edit loops.
4. **Skip useless or conflicting edits:** Leave code untouched when a squiggle would alter intended runtime behavior (such as intentional local defaults), clash with an enforced project linter rule, fight normal language idioms (class-method indentation, parameter alignment, docstrings), or split clear lines into awkward fragments just to force exit code `0`.
5. **Ask for review & healthy issue feedback:**
   - Summarize `codehygiene`-motivated refactors in one short note (especially opinionated clean-code choices that differ from traditional linters) so the user can review them.
   - Whenever an edit is skipped as useless, clashes with a project linter, or is disliked by the user, keep or restore the preferred code immediately, note constructively that `codehygiene` is an early preview (Step 1 skill collecting feedback and benchmark cases toward harness hooks), and ask whether the user would like an issue opened on `brianbell-x/codehygiene` so the case can be benchmarked and fixed.

## Opening Feedback Issues

Once the user confirms opening an issue:

1. Construct a minimal, synthetic reproducer snippet (never include proprietary logic, credentials, or internal identifiers).
2. Include the language/extension, `codehygiene -V` version, squiggle `kind` + probability, any conflicting linter rule, and a one-sentence explanation of why the diagnostic or suggested refactor was unhelpful.
3. Run `gh issue create --repo brianbell-x/codehygiene` directly and share the issue URL, or provide a pre-filled `https://github.com/brianbell-x/codehygiene/issues/new` link and markdown body when `gh` is unavailable or unauthenticated.

## Squiggle Reference

| Squiggle `kind` | Typical Trigger | Recommended Fix (When Genuine) |
| :--- | :--- | :--- |
| `deep_nesting` | Pyramid control flow (`4+` indent levels) | Invert conditions into early `return` / `continue` guard clauses or extract a flat helper. |
| `noisy_comment` | Comment restates next-line identifiers, `# Step 1` narration, `// ... rest` elisions, `3+` commented-out code lines, `TODO`, or lint noise | Delete narrator comments, placeholder elisions, and dead commented code; retain comments only for non-obvious *why* or invariants. |
| `swallowed_error` | Bare `except Exception: pass`/`return None`, empty `catch {}`, redundant internal runtime type guards, silent `env` fallbacks, `as any` / `cast(Any, ...)`, `\|\| {}` / `or []`, or `# noqa` / `@ts-ignore` | Catch specific errors, fail fast on missing required config, trust internal static types, and fix root causes rather than suppressing lints. |
| `poor_naming` | Enterprise ceremony (`*Factory`, `*Manager`, `*Helper`, `*Impl`), dead suffixes (`*_old`, `*_bak`, `*_deprecated`), 1–2 char variable walls (`xx = ...`), or magic indices (`buf[47]`) | Remove dead copies, use plain domain nouns/verbs (`>= 3` chars), and extract named constants for non-trivial indices or sizes. |
| `dense_line` | Chained `.map().filter().reduce()`, nested ternaries, or lines past `96`–`110` cols | Split into named intermediate steps and wrap long expressions cleanly. |
| `special_casing` | Repeated `if x == "a": return ...` literal ladders or scattered `typeof` / `isinstance` checks | Replace branch ladders with a dispatch table/map or normalize types at the boundary. |
| `duplicate_block` | Copy-pasted imperative blocks `8–31` lines apart | Extract shared logic into a parameterized helper or loop over data. |
| `cramped_layout` | Long statement walls with zero blank-line separation | Separate setup, transformation, and return phases with single blank lines. |

## Guardrails

- Execute the CLI directly rather than guessing scores from visual inspection.
- Do not game scores by shortening clear identifiers to 2 letters, cramming multiple statements onto one line, stripping legitimate error handling, or raising `-t` / `--threshold` above `0.55`; skip false positives openly instead.
- When `stderr` prints a `codehygiene` update notice, mention the available update briefly at the end of the turn (or offer `npx skills update codehygiene -y` / `npx skills update codehygiene -g -y`).
