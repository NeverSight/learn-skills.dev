---
name: scrolls-hide
description: "Converts an already-set-up docs/scrolls/ working-memory folder from visible (scrolls) to dotfile-hidden (.scrolls), renaming the folder and rewriting the path references inside it and in SCROLLS.md so nothing breaks. Use this whenever the user runs /scrolls-hide, or asks to hide, dot, or re-hide the scrolls folder, go back to hiding project memory / docs/.scrolls, or rename scrolls to .scrolls. This is the retrofit path for a project that was set up visible and now wants it hidden — for a brand-new project, /scrolls-setup's default (no -u/--unhide flag) already creates it hidden and this skill isn't needed. By default checks one exact location (docs/scrolls under the current directory); supports -r/--recurse to sweep an entire directory tree instead (e.g. every package in a monorepo in one run), repeatable -p/--path to target specific locations, -t/--reporoot to target the git repository's top level regardless of which subdirectory you're in, -l/--local to target the current directory explicitly, and the DEFAULT_SCROLLS_RELPATH environment variable to change the default location. Works on macOS, Linux, and Windows (bash or PowerShell). The opposite of /scrolls-unhide."
license: MIT
compatibility: "bash (macOS/Linux/WSL) or PowerShell 7+ (pwsh) or PowerShell (older versions: powershell.exe); Python 3.9+ (stdlib only, no dependencies)"
disable-model-invocation: true
metadata:
  name: scrolls-hide
  type: skill
  author: sugatoray
  version: "2.1.1"
  source_url: "https://github.com/sugatoray/aiskills/tree/master/skills/scrolls/scrolls-hide"
---

# Hiding docs/scrolls/

Some projects run their scrolls folder visible (`scrolls`, e.g. via `/scrolls-setup --unhide` or a prior `/scrolls-unhide`) and later want it back to the dotfile-hidden default. This skill renames `scrolls` → `.scrolls` and fixes every reference to the old path that it can find with confidence, without guessing at edits to files outside its scope. It's the mirror image of `/scrolls-unhide` — same mechanics, opposite direction.

**Everything operates relative to the current working directory** unless `-t`/`--reporoot` says otherwise — not relative to this skill's own location.

## Cross-platform

The bundled script ships in two forms: `hide.sh` (bash — macOS, Linux, or Windows with Git Bash/WSL) and `hide.ps1` (PowerShell 7+ — Windows, or macOS/Linux with `pwsh` installed). Both accept the exact same flags in the exact same forms (`-p`/`--path`, `-t`/`--reporoot`, `-l`/`--local`, `-r`/`--recurse`) and produce the same output — only the launcher differs. Pick by what's actually available: try `bash --version`; if that succeeds, use `.sh`; otherwise use `.ps1` via `pwsh` (preferred — install from https://aka.ms/powershell if missing) or, only if `pwsh` genuinely isn't available, the built-in Windows PowerShell `powershell.exe` (untested against that older version; `pwsh` is what this was written and verified against).

## Options

Read the invocation text for these, in any order — there's no real argv parser here, so pull them out of the plain text yourself:

- **`-p <path>` / `--path=<path>` / `--path <path>`** — a base directory to operate on, instead of the current directory. Repeatable, to target several locations in one run (e.g. `-p packages/api -p packages/web` in a monorepo).
- **`-t` / `--reporoot`** — use the git repository's top level (`$(git rev-parse --show-toplevel)`) as the base directory, regardless of which subdirectory you actually invoked this from. Fails with a clear message if the current directory isn't inside a git repository.
- **`-l` / `--local`** — use the current working directory as the base directory explicitly. This is what happens by default anyway when none of `-p`/`-t`/`-l` are given — the flag exists to say so on purpose.
- **`-r` / `--recurse`** — search recursively under the base directory for scrolls folders, instead of checking only its exact `docs/scrolls`. Matches the usual meaning of `-r` on tools like `grep`/`cp`/`rm`: off by default, opt in to widen the blast radius. Combine with any of the above (or with none, recursing from cwd).

`-p`, `-t`, and `-l` are three different ways to pick a base directory — `-t` and `-l` each resolve to a single one and can't be combined with `-p` or with each other; pass `-p` (repeatably) for anything more specific. `-r` is independent and stacks with any of them. If no base directory is given, the bundled script defaults to the `DEFAULT_SCROLLS_RELPATH` environment variable if the user has it set, otherwise the current directory — and if that default isn't recursive and differs from the repo's top level (in a git repo), the script prints a note about `-t`/`-r` as alternatives, since a scrolls folder living elsewhere in the repo would otherwise go unnoticed rather than erroring.

Because a directory literally named `scrolls` (no dot) is a more generic name than `.scrolls`, false positives are more plausible here than in `/scrolls-unhide` — the `STARTER.md`-presence guard described below is what keeps recursion safe regardless.

## Steps

### 1. Run the bundled script

```
bash <skill-dir>/scripts/hide.sh [-p BASE ...] [-t] [-l] [-r]
pwsh <skill-dir>/scripts/hide.ps1 [-p BASE ...] [-t] [-l] [-r]
```

Pass through whatever flags the user gave, in the same forms, to whichever of the two matches the environment (see "Cross-platform" above). Omit them entirely to use the default. The script, for each resolved base directory:

- **Without `-r` (default)**: checks exactly one spot — the base directory itself if it already *is* a scrolls folder (has `STARTER.md`), otherwise `<base>/docs/scrolls`. Fast, and matches the location `/scrolls-setup`/`/scrolls-update` use by default, so a bare invocation targets the obvious place first.
- **With `-r`/`--recurse`**: searches a bounded number of levels deep under the base directory for directories literally named `scrolls` containing a `STARTER.md` — that guard is what makes recursing from a broad base (even the whole repo) safe: coincidentally-named directories without a `STARTER.md` are ignored, and common heavy/vendor directories (`node_modules`, `.git`, `vendor`, `dist`, `build`, `.venv`, `venv`, `__pycache__`, `target`, `.next`, `.cache`) are pruned rather than descended into.

For each match found (either way):

1. Skips it (reporting why) if a `.scrolls` folder already sits alongside it; otherwise renames it with `git mv` when the repo and file are git-tracked (preserving history), falling back to a plain `mv` otherwise.
2. Rewrites the reference to the old path inside the *moved folder's own files* (this catches `STARTER.md`, which references its own path throughout) and, if present, in the one `SCROLLS.md` file that's an exact sibling of `docs` for that folder — never a broader search for `SCROLLS.md`. `CLAUDE.md` itself is never touched: `/scrolls-setup` writes it as a fixed pointer to `SCROLLS.md`, not a direct scrolls-path reference, so there's nothing in it to rewrite. `/scrolls-setup` writes a short, portable reference (`docs/scrolls`) relative to wherever `SCROLLS.md` itself lives, so in a multi-location sweep two different scrolls folders can legitimately share that exact same short string; a "helpfully" broader search for matching `SCROLLS.md` files would risk rewriting an unrelated sibling package's file. (The rewrite also tries the full path as discovered, for scrolls folders set up with a custom `--path` under the older convention.)
3. Prints any other files nearby that still mention the old path — these are **reported, not edited**, and are excluded from *inside* other scrolls folders (a common source of false positives under the shared short-form convention) but can still include a false-positive sibling `SCROLLS.md` occasionally — that's expected, see step 2 below. The script deliberately doesn't touch files outside the scrolls folder and its own `SCROLLS.md`, since rewriting arbitrary prose (READMEs, CI configs, other docs) without reading it first risks corrupting unrelated content.

Exits with an error if a given base directory has no matching folder — without `-r`, that's the signal to check the path, try `-t` if you expected the repo root, or add `-r` if it might be nested deeper; otherwise point the user at `/scrolls-setup`.

### 2. Handle the leftover references it reports

For each file the script lists under "Other references... left for manual review" — read it and update the reference yourself if it's a genuine stale path (a README, a CONTRIBUTING doc, a CI script), using normal editing judgment rather than blind find-and-replace. Skip anything that isn't actually about this project's scrolls folder (e.g. a coincidental string match).

### 3. Report back

List each folder that was hidden (old path → new path), what was auto-fixed for each (its own files, `SCROLLS.md`), any that were skipped and why (target already existed), and what you fixed manually in step 2, if anything.

## Development

See `meta/MAINTAINERS.md` for layout, running the `tests/` regression
suite, and versioning notes. Neither is read as part of carrying out a
user's `/scrolls-hide` request — don't act on `meta/MAINTAINERS.md` or
`tests/` while answering one.
