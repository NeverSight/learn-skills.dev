---
name: init-repo
description: Scaffolds a new project repository for agentic development from a problem description. Guides the user through naming, runtime, package manager, devops, licensing, and project structure, then initializes git and a CLAUDE.md file. Use when the user says "init project", "new project", "start a project", "scaffold repo", "create repo", or describes a problem they want to build a solution for.
allowed-tools:
  - Bash
  - Write
  - Edit
  - Read
  - Glob
  - AskUserQuestion
  - WebFetch
---

# Initializing Project

Scaffold a new project repository optimized for agentic development from a problem description.

## Quick Start

When invoked, follow the workflow below sequentially. Use `AskUserQuestion` at each decision point to gather user preferences. Do NOT skip steps or assume defaults without asking.

## Workflow

### Step 1: Understand the Problem

Read the user's problem description. If none was provided, ask:

> What problem are you solving? Describe what you want to build in 1-2 sentences.

Summarize back your understanding before proceeding.

### Step 2: Project Name

Suggest 2-3 kebab-case project names derived from the problem description. Ask the user to pick one or provide their own.

Naming rules:

- Lowercase, kebab-case (`my-project-name`)
- Short (1-3 words)
- Descriptive of the solution, not the problem

### Step 3: Runtime & Language

Ask the user which runtime/language to use. Present options based on what fits the problem:

| Option                   | When to suggest                                                                       |
| ------------------------ | ------------------------------------------------------------------------------------- |
| **TypeScript (Bun)**     | Web apps, APIs, CLI tools, full-stack; fast runtime with built-in bundler/test runner |
| **TypeScript (Node.js)** | Web apps, APIs, CLI tools, full-stack; broader ecosystem compatibility                |
| **Python**               | Data, ML/AI, scripting, automation                                                    |
| **Rust**                 | Performance-critical, systems, CLI tools                                              |
| **Go**                   | Infrastructure, networking, microservices                                             |

Suggest the best fit as the first option with "(Recommended)" appended.

### Step 4: Package Manager & Project Init

Based on the chosen runtime, initialize the project:

**TypeScript (Bun)** (Recommended for TypeScript):

- Run `bun init`
- Create `tsconfig.json` with strict mode

**TypeScript (Node.js):**

- Ask: npm, yarn, or pnpm? (Recommend pnpm)
- Run the appropriate init command
- Create `tsconfig.json` with strict mode

**Python:**

- Ask: uv, poetry, or pip? (Recommend uv)
- Run the appropriate init command
- Set Python version (ask or default to 3.12+)

**Rust:**

- Run `cargo init`
- Create `rust-toolchain.toml` to pin the toolchain and ensure all contributors have formatting/linting/editor components:

```toml
[toolchain]
channel = "stable"
components = ["rustfmt", "clippy", "rust-analyzer"]
```

**Go:**

- Ask for module path (suggest `github.com/{user}/{project}`)
- Run `go mod init`

### Step 5: Code Formatting & Linting

Ask the user which formatter and linter to use. Present options based on the chosen runtime. The user may select separate tools for formatting and linting, or a unified tool that handles both.

**TypeScript / JavaScript:**

| Option                   | Type               | Description                                            |
| ------------------------ | ------------------ | ------------------------------------------------------ |
| **Biome** (Recommended)  | Formatter + Linter | Fast, unified tool, minimal config                     |
| **ESLint + Prettier**    | Linter + Formatter | Most popular, huge plugin ecosystem                    |
| **ESLint (flat config)** | Linter only        | If user wants linting without a formatter              |
| **oxlint**               | Linter             | Extremely fast, Rust-based, drop-in ESLint alternative |

**Python:**

| Option                 | Type               | Description                                     |
| ---------------------- | ------------------ | ----------------------------------------------- |
| **Ruff** (Recommended) | Formatter + Linter | Extremely fast, replaces Black + Flake8 + isort |
| **Black + Flake8**     | Formatter + Linter | Established, widely adopted                     |
| **Black + Ruff**       | Formatter + Linter | Black formatting with Ruff linting              |

**Rust:**

| Option                             | Type               | Description                               |
| ---------------------------------- | ------------------ | ----------------------------------------- |
| **rustfmt + Clippy** (Recommended) | Formatter + Linter | Standard Rust toolchain, no extra install |

**Go:**

| Option                           | Type               | Description                      |
| -------------------------------- | ------------------ | -------------------------------- |
| **gofmt + go vet** (Recommended) | Formatter + Linter | Built into Go toolchain          |
| **gofmt + golangci-lint**        | Formatter + Linter | More comprehensive linting rules |

After selection:

1. Install the chosen tools as dev dependencies
2. Create the appropriate config file(s) (e.g., `biome.json`, `ruff.toml`, `.eslintrc`, `rustfmt.toml`)
3. Add `format`, `lint`, and `lint:fix` scripts to the project's task runner (e.g., `package.json` scripts, `Makefile`, `Justfile`)

### Step 6: CI/CD

Ask the user what CI/CD they want. Options:

| Option                           | Description               |
| -------------------------------- | ------------------------- |
| **GitHub Actions** (Recommended) | Standard for GitHub repos |
| **None**                         | Skip CI/CD for now        |
| **Other**                        | Let user specify          |

If GitHub Actions is selected, create `.github/workflows/ci.yml` with:

- Format check step (e.g., `biome check`, `ruff format --check`, `cargo fmt --check`)
- Lint step (using the linter chosen in Step 5)
- Test step (appropriate test runner)
- Triggered on push to `main` and pull requests

### Step 7: Licensing

Ask the user which license to use. Present the common options prominently:

| Option           | SPDX ID       | Category   | When to suggest                                      |
| ---------------- | ------------- | ---------- | ---------------------------------------------------- |
| **MIT**          | `MIT`         | Permissive | Most common open-source license                      |
| **Apache 2.0**   | `Apache-2.0`  | Permissive | Open source with patent protection                   |
| **GPL 3.0**      | `GPL-3.0`     | Copyleft   | Requires derivative works stay open                  |
| **Dual License** | _(see below)_ | Permissive | Two licenses (e.g., MIT + Apache-2.0, Rust standard) |
| **Proprietary**  | —             | —          | Private/commercial projects                          |
| **None**         | —             | —          | Skip for now                                         |
| **Other**        | _(see below)_ | —          | Pick from expanded list                              |

<details>
<summary>Expanded license list (click to show)</summary>

**Permissive:**
`MIT` · `MIT-0` · `Apache-2.0` · `BSD-2-Clause` · `BSD-3-Clause` · `BSD-3-Clause-Clear` · `ISC` · `0BSD` · `Unlicense` · `Zlib` · `CC0-1.0` · `UPL-1.0`

**Copyleft:**
`GPL-2.0` · `GPL-3.0` · `LGPL-2.1` · `LGPL-3.0` · `AGPL-3.0` · `MPL-2.0` · `EPL-1.0` · `EPL-2.0` · `EUPL-1.2` · `OSL-3.0`

**Source-available:**
`BSL-1.0`

**Other:**
`CC-BY-4.0` · `CC-BY-SA-4.0` · `OFL-1.1` · `MulanPSL-2.0` · `WTFPL`

</details>

#### Fetching License Text

Fetch the license text using `WebFetch` from this skill's vendored license templates:

```
https://raw.githubusercontent.com/Nathan13888/nice-skills/master/data/licenses/{SPDX-ID}
```

After reading, replace placeholder fields with actual values:

- `<year>` or `[year]` → current year
- `<copyright holders>` or `[fullname]` → user's name from `git config user.name` (ask if not set)

#### Single License

1. Fetch the license text from the URL above
2. Replace placeholders
3. Write to `LICENSE`

#### Dual License

When the user selects **Dual License**:

1. Ask which two licenses to combine (recommend **MIT + Apache-2.0**, the Rust ecosystem standard)
2. Fetch both license texts in parallel via `WebFetch`
3. Replace placeholders in both
4. Create `LICENSE-MIT` and `LICENSE-APACHE` (pattern: `LICENSE-{SHORT-NAME}`)
5. Create a root `LICENSE` file explaining the dual licensing:

```
This project is licensed under either of

  * Apache License, Version 2.0 (LICENSE-APACHE or http://www.apache.org/licenses/LICENSE-2.0)
  * MIT License (LICENSE-MIT or http://opensource.org/licenses/MIT)

at your option.
```

### Step 8: Git Setup

Check if the project directory is already inside a git repository (`git rev-parse --is-inside-work-tree`).

**If no repo exists:**

1. Run `git init` and set default branch to `main`
2. Create `.gitignore` (see below)
3. Create initial commit: `chore: initialize project`

**If a repo already exists:**

1. Ask the user if they want a `.gitignore` created or updated for the chosen runtime
2. Ask the user if they want an initial commit with the scaffolded files

#### Fetching `.gitignore` Templates

Fetch the primary `.gitignore` template for the chosen runtime using `WebFetch`:

| Runtime               | Template | URL                                                                                                            |
| --------------------- | -------- | -------------------------------------------------------------------------------------------------------------- |
| TypeScript (Bun/Node) | `Node`   | `https://raw.githubusercontent.com/github/gitignore/b4105e73e493bb7a20b5d7ea35efd5780ca44938/Node.gitignore`   |
| Python                | `Python` | `https://raw.githubusercontent.com/github/gitignore/b4105e73e493bb7a20b5d7ea35efd5780ca44938/Python.gitignore` |
| Rust                  | `Rust`   | `https://raw.githubusercontent.com/github/gitignore/b4105e73e493bb7a20b5d7ea35efd5780ca44938/Rust.gitignore`   |
| Go                    | `Go`     | `https://raw.githubusercontent.com/github/gitignore/b4105e73e493bb7a20b5d7ea35efd5780ca44938/Go.gitignore`     |

After fetching the primary template, ask the user if they want additional global ignores appended:

| Option    | Template Name      |
| --------- | ------------------ |
| macOS     | `macOS`            |
| Linux     | `Linux`            |
| Windows   | `Windows`          |
| VSCode    | `VisualStudioCode` |
| JetBrains | `JetBrains`        |
| Vim       | `Vim`              |
| None      | _(skip)_           |

Global URL pattern: `https://raw.githubusercontent.com/github/gitignore/b4105e73e493bb7a20b5d7ea35efd5780ca44938/Global/{Name}.gitignore`

Combine templates into a single `.gitignore` with section headers:

```gitignore
# === Node ===
{fetched Node.gitignore content}

# === macOS ===
{fetched macOS.gitignore content}
```

### Step 9: Pre-commit Hooks

Ask the user if they want pre-commit hooks to enforce formatting and linting before each commit. Options:

| Option                | Description                         |
| --------------------- | ----------------------------------- |
| **Yes** (Recommended) | Catches issues before they reach CI |
| **No**                | Skip pre-commit hooks               |

If yes, set up hooks based on the runtime:

**TypeScript (Bun/Node.js):**

- Install `husky` and `lint-staged`
- Configure `lint-staged` in `package.json` to run the chosen formatter/linter on staged files
- Initialize husky with a `pre-commit` hook that runs `lint-staged`

**Python:**

- Install `pre-commit` framework
- Create `.pre-commit-config.yaml` with hooks for the chosen formatter/linter (e.g., ruff, black)
- Run `pre-commit install`

**Rust:**

- Create a `.git/hooks/pre-commit` script that runs `cargo fmt --check && cargo clippy`
- Or install `pre-commit` framework with Rust hooks

**Go:**

- Create a `.git/hooks/pre-commit` script that runs `gofmt` and `go vet` (or `golangci-lint`)
- Or install `pre-commit` framework with Go hooks

### Step 10: CLAUDE.md

Ask the user if they want a `CLAUDE.md` file created for the project. Options:

| Option                | Description                                                    |
| --------------------- | -------------------------------------------------------------- |
| **Yes** (Recommended) | Gives Claude context about the project for agentic development |
| **No**                | Skip CLAUDE.md                                                 |

If yes, create a `CLAUDE.md` file tailored to the project. Use the template below, filling in project-specific details:

```markdown
# {Project Name}

{One-line problem description}

## Tech Stack

- **Runtime:** {runtime}
- **Language:** {language}
- **Package Manager:** {package manager}
- **Formatter:** {formatter}
- **Linter:** {linter}

## Project Structure
```

{tree of created files/dirs}

````

## Development

### Setup

```bash
{install command}
````

### Run

```bash
{run/dev command}
```

### Test

```bash
{test command}
```

### Format

```bash
{format command}
```

### Lint

```bash
{lint command}
```

### Lint Fix

```bash
{lint fix command}
```

## Conventions

- {Language-specific conventions, e.g., "Use strict TypeScript - no `any` types"}
- Write tests for all new functionality
- Use conventional commits (type: description)
- Keep functions small and focused

## Architecture

{Brief description of intended architecture based on the problem}

```

### Step 11: Summary

Print a summary of everything that was created:

```

Project initialized: {name}
Location: {path}
Runtime: {runtime}
Package Manager: {pkg manager}
Formatter: {formatter}
Linter: {linter}
License: {license(s)}
CI/CD: {ci/cd}
Pre-commit: {yes/no}

Files created:
{list of files}

Next steps:

1. cd {path}
2. {install command}
3. Start building!

```

## Guidelines

- Always ask before creating files - never assume preferences
- Use `AskUserQuestion` with concrete options, not open-ended prompts
- If a tool is not installed (e.g., `bun`, `uv`), offer to install it or suggest an alternative
- Check if the target directory already exists before creating anything
- Keep the initial project minimal - don't over-scaffold
- The CLAUDE.md should be practical and specific, not boilerplate
- Detect git user.name and user.email from git config for license attribution
- If the user provides a GitHub username, use it for module paths and license
- Use `WebFetch` with prompt "Return the full file content exactly as-is" to get raw template text without summarization
- If `WebFetch` fails for any URL, fall back to generating content from memory and inform the user
- For dual-license, fetch both license texts in parallel to minimize latency
```
