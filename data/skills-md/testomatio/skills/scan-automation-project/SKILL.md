---
name: scan-automation-project
description: Scan project source code to inventory languages, frameworks, and existing tests (manual `*.test.md` and automated test files). Use this skill whenever analyzing a codebase for test planning, detecting test frameworks, or preparing for test automation. Specifically, when the user mentions "scan project", "what tests exist", "analyze codebase", "detect frameworks", "test matrix", or needs a codebase inventory before a QA workflow.
license: MIT
metadata:
  author: Testomat.io
  version: 1.0.0
---

# Scan Automation Project

Scan project source code and return a QA-focused inventory: languages, frameworks, and existing tests.

**Shallow scan only.** No full import resolution, no line-by-line parsing, no reading full test implementations. High-level structure only.

## Step 1: Locate Source Code

- If the project root has non-empty source folders or files, go to Step 2.
- If **no source** files are found, stop and ask the user:

```
❓ No application source code detected (folder may be empty or missing).
Where is the source code?
1. Use local project from another folder (I will create a symlink)
2. Clone from Git repo
3. I don't know yet (stop here)
```

- Wait for the user's reply.
- If the user gives a Git repo or another folder, clone or symlink it into `.testeiya/code/`. No-op if it is already there.

### Rule for pulled data

**When you need to pull external data** (manual test cases, app code, e2e tests from another repo) into this project:

| This project has | Store pulled data in | Gitignored? |
| ------------------ | ---------------------- | ----------- |
| **Source code** (`src/` folder) or **big project** | `.testeiya/…` | **Yes** |
| **Only test infrastructure** (e2e dirs like `tests/`, `playwright/`, `cypress/` but no `src/`) | `manual-tests/` or `e2e-tests/` | No |
| **Empty / manual-only** | `manual-tests/` | No |

Detection logic:
1. Has `src/` folder or is a monorepo? → Use `.testeiya/`
2. Has e2e test dirs (`tests/`, `playwright/`, `cypress/`, `e2e/`)? → Use tracked folder (`manual-tests/`, `e2e-tests/`)
3. Otherwise → Default to `manual-tests/`

- Any skill that creates `.testeiya/...` must also add `.testeiya/` to the project's `.gitignore` — but only if it is not there yet. Never add it twice.
- The rule covers *pulled* data only. Output a skill *produces* and the user wants — a `coverage.*.yml`, new `*.test.md` files — goes in the repo as normal.
- On a source repo with no manual tests, this skill changes no tracked file: it only creates the gitignored `.testeiya/` directory and, if needed, adds one line to `.gitignore`.
- **Only touch `.testeiya/` and tracked folders — never pollute the repo with cache in a wrong location.**

## Step 2: Project Analysis

Collect source file paths only. **Do NOT read file contents.**

Include:
- Application source files.
- View/template files: `.html`/`.htm`, `.vue`, `.svelte`, `.hbs`/`.handlebars`, `.ejs`, `.pug`/`.jade`, `.mustache`, `.liquid`, `.erb`, `.haml`, `.slim`, `.blade.php`, `.twig`, `.j2`/`.jinja`/`.jinja2`, `.cshtml`/`.razor`, `.jsp`. They are application source — coverage skills map UI changes through them.

Exclude:
- Dependencies, build output, coverage, reports, caches, config, lock, and environment files.
- Paths ignored by `.gitignore` — but **not** `.testeiya/code/`. In a manual-tests repo the app code lives there; scan it as source.
- Testeiya internal files (e.g. `session-factory.ts`, `system-prompt.ts`).
- **If in doubt**, exclude.

From the file list:
- Detect languages and frameworks. Collect one `frameworks` list with ALL application and testing frameworks.
- Extract the project name from a project config file (`package.json`, `Cargo.toml`, `pom.xml`, ...); fall back to the root directory name.
- Rate complexity by source file count:

| File Count | Complexity   |
|------------|--------------|
| 1-30       | `small`      |
| 31-150     | `moderate`   |
| 151-500    | `large`      |
| 500+       | `very-large` |

## Step 3: Test Inventory (optional)

Detect existing tests, automated and manual. Stay shallow.

Automated tests:
- Detect frameworks via config files (`jest.config.*`, `playwright.config.*`, `vitest.config.*`, `pytest.ini`, `pom.xml`, ...), project dependencies, and test file patterns (`*.test.*`, `*.spec.*`, `*_test.*`).
- For each framework: identify its test file pattern and count matching files.

Manual tests:
- Find all `.test.md` files and parse test titles. `find .` also looks inside `.testeiya/manual-tests/`, so a re-run after a pull finds the cached cases instead of reporting "no manual tests":

```bash
find . -name "*.test.md" -exec awk '
  /^<!-- test/   { in_block=1; kind="TEST";  next }
  /^<!-- suite/  { in_block=1; kind="SUITE"; next }
  in_block && /^-->/ { in_block=0; expect=1; next }
  expect && /^#+[[:space:]]+/ {
    title=$0; sub(/^#+[[:space:]]+/, "", title)
    if (kind == "SUITE") printf "SUITE: %s\n", title
    else             printf "|- %s\n",     title
    expect=0
  }
' {} +
```

- If the only `.test.md` files are under `.testeiya/manual-tests/`, say so in the inventory: they came from Testomat.io, not from this repo.

## Step 4: Output

Return one structured markdown result directly. **Do NOT save to a file.**

```markdown
# Project Overview

- **Project Name:** acme-web-app
- **Description:** A React-based customer dashboard with an Express API.
- **Languages:** TypeScript, SQL
- **Frameworks:** React, Express, Jest, Playwright
- **Complexity:** small (12 files)

## Test Inventory

- **Automated Tests:** 10 files
- **Manual Tests:** 37 cases

### Manual Tests (20 of 37 shown)

- SUITE: Authentication
  |- User can login
  |- User can reset password
- SUITE: Billing
  |- User can view invoice
  ...and 17 more

### Automated Tests (10 of 10 shown)

- home.page.spec.ts
...
```

Field rules:
- **Description:** 1-2 sentences based only on detected source code and folder structure (include the domain area if that makes sense).
- **Complexity:** one of `small` | `moderate` | `large` | `very-large`, plus the file count.
- **Manual Tests:** preserve hierarchy as plain strings — SUITE items as parent bullets, test titles (`|-`) as nested children.
- **Automated Tests:** list of detected test files.
- All values must come from observable files. Do NOT guess missing data or add fields not shown above.

Sections:
- If Step 3 was skipped or found no tests, omit `## Test Inventory` and note that the project contains no tests; the `# Project Overview` section is still useful for next steps.
- If one test type is absent, note it with a blockquote, e.g. ``> No manual tests (`.test.md`) found in the project.``

Test listing truncation:
- Show at most the first 20 entries per list, in original file order.
- Mark truncation in the heading (`(20 of 37 shown)`) and with `...and N more`.
- Do not print full test listings beyond that.
