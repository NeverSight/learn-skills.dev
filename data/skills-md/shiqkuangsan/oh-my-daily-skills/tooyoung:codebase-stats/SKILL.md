---
name: tooyoung:codebase-stats
description: "Count lines of code by file type and auto-detected module for any codebase. Supports monorepo, full-stack, Java multi-module, Go, Python, and Rust workspaces. Trigger words: codebase stats, loc, count lines, code stats, codebase-stats"
metadata:
  version: "1.0.0"
---

# Codebase Stats

Count lines of code with auto-detected project structure. No external tools required.

**Tools to use:** `Bash` for file discovery and counting, `Glob` and `Read` for config file detection.
Do NOT use `cloc`, `tokei`, `scc`, or any external LOC counter.

## Activation

Trigger on:

- `/codebase-stats` or `/loc`
- "count lines of code", "LOC by module", "code stats", "project size"

## Execution Flow

### Step 1: Detect Project Structure

Use `Glob` and `Read` to inspect config files at the project root. Follow this decision tree **in order** (first match wins):

#### 1a. JS/TS Workspace Monorepo

**Signal files:** `pnpm-workspace.yaml`, `turbo.json`, `nx.json`, `lerna.json`, or root `package.json` containing `"workspaces"`

**Module extraction:**

- `pnpm-workspace.yaml`: read `packages` globs, expand with Glob
- `package.json` workspaces: read array, expand globs
- Each directory with its own `package.json` = one module
- Label: `workspace`

#### 1b. Rust Workspace

**Signal:** root `Cargo.toml` containing `[workspace]`

**Module extraction:** parse `members` array, expand globs. Label: `workspace`

#### 1c. Java / Kotlin Multi-Module

**Signal:** root `pom.xml` with `<modules>`, or `settings.gradle` / `settings.gradle.kts`

**Module extraction:**

- Maven: parse `<module>` tags
- Gradle: parse `include(...)` or `include '...'`, convert `:a:b` to `a/b`
- Label: `maven-module` or `gradle-module`

#### 1d. Go Multi-Module

**Signal:** `go.mod` found in 2+ directories

**Module extraction:** each directory containing `go.mod` = one module. Label: `go-module`

#### 1e. Python Multi-Package

**Signal:** `pyproject.toml` or `setup.py` found in 2+ directories

**Module extraction:** each directory containing either file = one module. Label: `py-package`

#### 1f. Full-Stack Monolith

**Signal:** top-level directory pairs matching known patterns:

- `src` + `src-tauri` (Tauri)
- `frontend` + `backend`
- `client` + `server`
- `web` + `api`
- `app` + `server`

**Module extraction:** each matched directory = one module. Label: `monolith`

#### 1g. Simple Single-Module

**Fallback:** none of the above matched.

**Module:** project root as the only module. Label: `single`

**Always:** add a `<root>` pseudo-module for files in the project root not belonging to any detected module.

### Step 2: Count Lines

Run a single Bash script. The counting logic:

```bash
# Template - adapt ROOT, MODULES, PRUNE_DIRS as needed

find "$ROOT" \
  \( -name .git -o -name node_modules -o -name target -o -name dist \
     -o -name build -o -name out -o -name coverage -o -name .next \
     -o -name .nuxt -o -name .svelte-kit -o -name .turbo -o -name .cache \
     -o -name __pycache__ -o -name .venv -o -name venv -o -name .mypy_cache \
     -o -name .pytest_cache -o -name vendor -o -name third_party \
     -o -name .yarn -o -name .pnpm-store -o -name Pods -o -name DerivedData \
     -o -name .gradle -o -name .idea -o -name .vscode -o -name .settings \
     -o -name gen -o -name generated \
     -o -name bin -o -name obj -o -name tmp -o -name temp \
  \) -prune -o \
  -type f ! -name '*.min.js' ! -name '*.min.css' ! -name '*.bundle.js' \
  ! -name '*.map' ! -name '*.snap' ! -name '*.lock' ! -name '*.d.ts' \
  ! -name 'package-lock.json' ! -name 'pnpm-lock.yaml' ! -name 'go.sum' \
  ! -name '*.pb.go' ! -name '*_pb2.py' \
  ! -name '*.generated.*' ! -name '*.gen.*' ! -name '*.g.dart' \
  ! -name '*.designer.*' \
  -print0 | \
while IFS= read -r -d '' f; do
  # skip symlinks
  [ -L "$f" ] && continue
  # skip binary
  grep -qI . "$f" 2>/dev/null || continue
  # get extension or basename for extensionless files
  base=$(basename "$f")
  case "$base" in
    Makefile|Dockerfile|Vagrantfile|Rakefile|Gemfile|Justfile|CMakeLists.txt) ext="$base" ;;
    *.*) ext="${base##*.}" ;;
    *) ext="$base" ;;
  esac
  # count
  lines=$(wc -l < "$f" 2>/dev/null) || continue
  loc=$(grep -cve '^[[:space:]]*$' "$f" 2>/dev/null || echo 0)
  # output: path<TAB>ext<TAB>lines<TAB>loc
  printf '%s\t%s\t%d\t%d\n' "$f" "$ext" "$lines" "$loc"
done
```

**File type mapping:** Apply this extension-to-type table to classify each file:

| Type   | Extensions                        |
| ------ | --------------------------------- |
| ts     | `.ts`                             |
| tsx    | `.tsx`                            |
| js     | `.js`, `.mjs`, `.cjs`             |
| jsx    | `.jsx`                            |
| py     | `.py`                             |
| rs     | `.rs`                             |
| go     | `.go`                             |
| java   | `.java`                           |
| kt     | `.kt`, `.kts`                     |
| swift  | `.swift`                          |
| c      | `.c`                              |
| cpp    | `.cc`, `.cpp`, `.cxx`             |
| h      | `.h`, `.hh`, `.hpp`, `.hxx`       |
| css    | `.css`, `.scss`, `.sass`, `.less` |
| html   | `.html`, `.htm`                   |
| sql    | `.sql`                            |
| sh     | `.sh`, `.bash`, `.zsh`, `.fish`   |
| toml   | `.toml`                           |
| json   | `.json`, `.jsonc`                 |
| yaml   | `.yml`, `.yaml`                   |
| xml    | `.xml`                            |
| md     | `.md`, `.mdx`                     |
| vue    | `.vue`                            |
| svelte | `.svelte`                         |
| dart   | `.dart`                           |
| rb     | `.rb`                             |
| php    | `.php`                            |
| cs     | `.cs`                             |
| scala  | `.scala`                          |
| elixir | `.ex`, `.exs`                     |
| docker | `Dockerfile`                      |
| make   | `Makefile`, `CMakeLists.txt`      |

Unmatched extensions: group into `other`. Skip known non-source: `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.ico`, `.pdf`, `.woff`, `.woff2`, `.ttf`, `.eot`, `.mp3`, `.mp4`, `.webm`, `.webp`, `.zip`, `.tar`, `.gz`, `.dmg`, `.exe`, `.dll`, `.so`, `.dylib`, `.DS_Store`.

**Module assignment:** for each file path, find the longest-matching module root prefix. Files not matching any module go to `<root>`.

### Step 3: Render Output

**Language:** Match the user's prompt language. If the user writes in Chinese, use Chinese table headers and labels (e.g., "扫描根目录", "文件类型", "模块", "占比"). If in English, use English. Technical terms (module names, file types, paths) stay as-is regardless of language.

Produce **four Markdown tables** in this exact order:

#### Table 1: Project Summary

```markdown
| Metric                   | Value                       |
| ------------------------ | --------------------------- |
| Scan Root                | `/path/to/project`          |
| Structure                | `monorepo (pnpm workspace)` |
| Modules                  | 5                           |
| Source Files             | 842                         |
| LOC (non-empty)          | 59,040                      |
| Total Lines              | 72,318                      |
| Skipped (binary/symlink) | 12                          |
```

#### Table 2: By File Type

Sorted by LOC descending.

```markdown
| Type | Files |    LOC |  Lines | Share |
| ---- | ----: | -----: | -----: | ----: |
| ts   |   120 | 18,420 | 22,510 | 31.2% |
| tsx  |    44 |  9,720 | 11,300 | 16.5% |
| rs   |    28 |  5,180 |  6,420 |  8.8% |
| css  |    15 |  2,340 |  2,890 |  4.0% |
| ...  |       |        |        |       |
```

`Share = LOC / total LOC * 100`, 1 decimal place.

#### Table 3: By Module

Sorted by LOC descending.

```markdown
| Module        | Kind      | Files |    LOC | Share | Top Types              |
| ------------- | --------- | ----: | -----: | ----: | ---------------------- |
| packages/core | workspace |   210 | 25,110 | 42.5% | ts(10.2k), tsx(9.7k)   |
| packages/ui   | workspace |   160 | 18,890 | 32.0% | tsx(15.4k), css(1.9k)  |
| <root>        | root      |    18 |  1,320 |  2.2% | json(0.5k), yaml(0.4k) |
```

`Top Types`: top 3 file types by LOC within the module, formatted as `type(Xk)` using abbreviation (e.g., `1.2k` for 1,200).

#### Table 4: Module x Type Detail (Top 20)

Only show if multiple modules detected. Sorted by LOC descending, capped at 20 rows.

```markdown
| Module        | Type | Files |    LOC |
| ------------- | ---- | ----: | -----: |
| packages/core | ts   |    95 | 12,340 |
| packages/core | tsx  |    75 | 10,210 |
| packages/ui   | tsx  |    88 | 15,420 |
```

If more than 20 combinations exist, append: `Showing top 20 of N combinations.`

### Number Formatting

- Use thousand separators for numbers >= 1,000 (e.g., `59,040`)
- Percentages: 1 decimal place (e.g., `31.2%`)
- Abbreviated form in Top Types: `1.2k` for 1,200

## Edge Cases

| Case                                         | Behavior                                              |
| -------------------------------------------- | ----------------------------------------------------- |
| Empty project                                | Show summary with zeros, note "No source files found" |
| Symlinks                                     | Never follow, count in "Skipped"                      |
| Binary files with source extension           | Detect via `grep -qI`, skip, count in "Skipped"       |
| Very large repo (>10k files)                 | Print warning before counting, continue normally      |
| Permission errors                            | Skip file, increment "Skipped" count                  |
| Nested monorepo (workspace inside workspace) | Use deepest module root (longest prefix match)        |
| Generated directories (`gen/`, `generated/`) | Exclude by default                                    |
| `other` share > 15%                          | Warn user to review unmapped extensions               |

## Performance Tips

- Always use `find -prune` to skip heavy directories early
- Process files in a single `find | while read` loop, not per-file tool calls
- Aggregate with `awk` or `sort | uniq -c`, not per-row processing
- Use `Read` only for config files (manifests), never for source files
- For repos with >5,000 files, run counting in a single Bash invocation
