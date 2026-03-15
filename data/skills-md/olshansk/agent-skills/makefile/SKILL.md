---
name: makefile
description: "Create or improve Makefiles with minimal complexity. Templates available: base, python-uv, python-fastapi, nodejs, go, chrome-extension, flutter."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Makefile Helper

Create Makefiles that are simple, discoverable, and maintainable.

## Core Principles

1. **Default to rich help** - Use categorized help with emoji headers unless user requests minimal
2. **Ask about structure upfront** - For new Makefiles, ask: "Flat or modular? Rich help or minimal?"
3. **Follow existing conventions** - Match the project's style if Makefile already exists
4. **Don't over-engineer** - Solve the immediate need, not hypothetical futures
5. **Use `uv run`** - Always run Python commands via `uv run` for venv context
6. **Explain decisions** - If choosing flat/minimal, explain why before generating

## When to Use This Skill

- Creating a new Makefile for a project
- Adding specific targets to an existing Makefile
- Improving/refactoring an existing Makefile
- Setting up CI/CD make targets
- Distributing pre-built binaries via GitHub Releases

## Quick Start

For new projects, use the appropriate template:

| Project Type | Template | Complexity |
|-------------|----------|------------|
| Any project | `templates/base.mk` | Minimal |
| Python with uv | `templates/python-uv.mk` | Standard |
| Python FastAPI | `templates/python-fastapi.mk` | Full-featured |
| Node.js | `templates/nodejs.mk` | Standard |
| Go | `templates/go.mk` | Standard |
| Chrome Extension | `templates/chrome-extension.mk` | Modular |
| Flutter App | `templates/flutter.mk` | Modular |

### Chrome Extension Structure

The chrome extension template uses a modular structure:

```
Makefile                              # Main file with help + includes
makefiles/
  colors.mk                           # ANSI colors & print helpers
  common.mk                           # Shell flags, VERBOSE mode, guards
  build.mk                            # Build zip, version bump, releases
  dev.mk                              # Test, lint, clean, install
```

Copy from `templates/chrome-extension-modules/` to your project's `makefiles/` directory.

**Key features:**
- `build-release` - Version bump menu (major/minor/patch) + zip for Chrome Web Store
- `build-beta` - (Optional) GitHub releases with `gh` CLI
- `dev-test` / `dev-test-e2e` - Vitest + Playwright testing
- `VERBOSE=1 make <target>` - Show commands for debugging

### Flutter App Structure

```
Makefile                    # Main file with help + includes
makefiles/
  colors.mk                # ANSI colors & print helpers
  common.mk                # Shell flags, VERBOSE mode, guards
  dev.mk                   # Setup, run simulator/device, devices, clean
  build.mk                 # iOS/Android builds (IPA, APK, AAB)
  deploy.mk                # TestFlight upload
  lint.mk                  # Dart analyze & format
```

Copy from `templates/flutter-modules/` to your project's `makefiles/` directory.

**Key features:**
- `flutter-run-ios` auto-boots simulator and waits for it
- `flutter-run-android` auto-launches emulator and waits for it
- `flutter-run-device` auto-detects or uses `FLUTTER_IOS_DEVICE` / `FLUTTER_ANDROID_DEVICE`
- `flutter-build-ipa` + `flutter-export-ipa` + `flutter-deploy-testflight` full iOS release workflow
- `flutter-export-ipa` re-exports IPA from existing archive without rebuilding
- `_check-asc-app` pre-flight App Store Connect validation (with ASC_API_KEY/ASC_API_ISSUER)
- `flutter-lint FIX=true` Dart formatting with FIX pattern
- `VERBOSE=1 make <target>` show commands for debugging

## Interaction Pattern

1. **Understand** - What specific problem are we solving?
2. **Check existing** - Is there already a Makefile? Read it first!
3. **Default to modular** - For 5+ targets, use modular structure unless user requests flat
4. **Match preferences** - Use python-fastapi.mk template style as default for rich help
5. **Explain structure** - If you choose flat/minimal, explain the reasoning
6. **Iterate** - Add complexity or simplify based on feedback

## Naming Conventions

Use **kebab-case** with consistent prefix-based grouping:

```makefile
# Good - consistent prefixes (hyphens, not underscores)
build-release, build-zip, build-clean    # Build tasks
dev-run, dev-test, dev-lint              # Development tasks
db-start, db-stop, db-migrate            # Database tasks
env-local, env-prod, env-show            # Environment tasks

# Internal targets - prefix with underscore to hide from help
_build-zip-internal, _prompt-version     # Not shown in make help

# Bad - inconsistent
run-dev, build, localEnv, test_net
build_release, dev_test                  # Underscores - don't use
```

**Name targets after the action, not the tool:**
```makefile
# Good - describes what it does
remove-bg          # Removes background from image
format-code        # Formats code
lint-check         # Runs linting

# Bad - names the tool
rembg              # What does this do?
prettier           # Is this running prettier or configuring it?
eslint             # Unclear
```

## Key Patterns

### Binary Distribution

For projects distributed as pre-built binaries via GitHub Releases:

```makefile
GITHUB_REPO ?= owner/repo
OS := $(shell uname -s | tr '[:upper:]' '[:lower:]')
ARCH := $(shell uname -m | sed 's/x86_64/amd64/' | sed 's/aarch64/arm64/')

.PHONY: install-cli
install-cli: ## Download and install CLI from latest GitHub release
	@RELEASE=$$(curl -fsSL https://api.github.com/repos/$(GITHUB_REPO)/releases/latest | grep tag_name | cut -d'"' -f4); \
	echo "Installing $$RELEASE for $(OS)/$(ARCH)..."; \
	curl -fsSL -o ~/.local/bin/cli \
		"https://github.com/$(GITHUB_REPO)/releases/download/$$RELEASE/cli-$(OS)-$(ARCH)"; \
	chmod +x ~/.local/bin/cli
```

**Key considerations:**
- Detect OS and architecture automatically
- Download from GitHub Releases (no Python/uv required)
- Install to `~/.local/bin` (user-writable, in PATH)
- Preserve existing config files during updates

### Always Use `uv run` for Python

```makefile
# Good - uses uv run with ruff (modern tooling)
dev-check:
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/
	uv run mypy src/

dev-format:
	uv run ruff check --fix src/ tests/
	uv run ruff format src/ tests/

# Bad - relies on manual venv activation
dev-format:
	ruff format .
```

### Use `uv sync` (not pip install)

```makefile
env-install:
	uv sync  # Uses pyproject.toml + lock file
```

### Categorized Help (for 5+ targets)

```makefile
help:
	@printf "$(BOLD)=== 🚀 API ===$(RESET)\n"
	@printf "$(CYAN)%-25s$(RESET) %s\n" "api-run" "Start server"
	@printf "%-25s $(GREEN)make api-run [--reload]$(RESET)\n" ""
```

**Makefile ordering rule - help targets go LAST, just before catch-all:**

1. Configuration (`?=` variables)
2. `HELP_PATTERNS` definition
3. Imports (`include ./makefiles/*.mk`)
4. Main targets (grouped by function)
5. `help:` and `help-unclassified:` targets
6. Catch-all `%:` rule (absolute last)

### Preflight Checks

```makefile
_check-docker:
	@docker info >/dev/null 2>&1 || { echo "Docker not running"; exit 1; }

db-start: _check-docker  # Runs check first
	docker compose up -d
```

### External Tool Dependencies

When a target requires an external tool (not a system service):

- **Don't create public install targets** (no `make install-foo`)
- **Use internal check as dependency** (prefix with `_`, no `##` comment)
- **Show install command on failure** - tell user what to run, don't do it for them

```makefile
# Internal check - hidden from help (no ##)
_check-rembg:
	@command -v rembg >/dev/null 2>&1 || { \
		printf "$(RED)$(CROSS) rembg not installed$(RESET)\n"; \
		printf "$(YELLOW)Run: uv tool install \"rembg[cli]\"$(RESET)\n"; \
		exit 1; \
	}

# Public target - uses check as dependency
.PHONY: remove-bg
remove-bg: _check-rembg ## Remove background from image
	rembg i "$(IN)" "$(OUT)"
```

**Key points:**
- Name target after the action (`remove-bg`), not the tool (`rembg`)
- Check runs automatically - user just runs `make remove-bg`
- If tool missing, user sees exactly what command to run

### Env File Loading

Load `.env` and export to child processes:

```makefile
# At top of Makefile, after .DEFAULT_GOAL
-include .env
.EXPORT_ALL_VARIABLES:
```

For per-target env override:

```makefile
# Allow: E2E_ENV=.test.env make test-e2e
test-e2e:
	@set -a && . "$${E2E_ENV:-.env}" && set +a && uv run pytest tests/e2e/
```

### FIX Variable for Check/Format Targets

Use a `FIX` variable to toggle between check-only and auto-fix modes:

```makefile
FIX ?= false

dev-check: ## Run linting and type checks (FIX=false: check only)
	$(call print_section,Running checks)
ifeq ($(FIX),true)
	uv run ruff check --fix src/ tests/
	uv run ruff format src/ tests/
else
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/
endif
	uv run mypy src/
	$(call print_success,All checks passed)
```

In help output, show usage:

```makefile
@printf "$(CYAN)%-25s$(RESET) %s\n" "dev-check" "Run linting (FIX=false: check only)"
@printf "%-25s $(GREEN)make dev-check FIX=true$(RESET)  <- auto-fix issues\n" ""
```

## When to Modularize

**Default to modular** for any new Makefile with 5+ targets.

**Use flat file only when:**
- Simple scripts or single-purpose tools
- User explicitly requests it
- < 5 targets with no expected growth

Standard modular structure:
```
Makefile              # Config, imports, help, catch-all
makefiles/
  colors.mk          # ANSI colors & print helpers
  common.mk          # Shell flags, VERBOSE, guards
  <domain>.mk        # Actual targets (build.mk, dev.mk, etc.)
```

## Legacy Compatibility

**Default: NO legacy aliases.** Only add when:
- User explicitly requests backwards compatibility
- Existing CI/scripts depend on old names (verify with `rg "make old-name"`)

When legacy IS needed, put them in a clearly marked section AFTER main targets but BEFORE help:

```makefile
############################
### Legacy Target Aliases ##
############################

.PHONY: old-name
old-name: new_name ## (Legacy) Description
```

## Key Rules

- **Always read existing Makefile before changes**
- **Search codebase before renaming targets** (`rg "make old-target"`)
- **Test with `make help` and `make -n target`**
- **Update docs after Makefile changes** - When adding new targets:
  1. Add to `make help` output (in the appropriate section)
  2. Update `CLAUDE.md` if the project has one (document new targets)
  3. Update any other relevant docs (README.md, Agents.md, etc.)
- **Never add targets without clear purpose**
- **No line-specific references** - Avoid patterns like "Makefile:44" in docs/comments; use target names instead
- **Single source of truth** - Config vars defined once in root Makefile, not duplicated in modules
- **Help coverage audit** - All targets with `##` must appear in either `make help` or `make help-unclassified`

## Help System

**ASCII box title for visibility:**
```makefile
help:
	@printf "\n"
	@printf "$(BOLD)$(CYAN)╔═══════════════════════════╗$(RESET)\n"
	@printf "$(BOLD)$(CYAN)║     Project Name          ║$(RESET)\n"
	@printf "$(BOLD)$(CYAN)╚═══════════════════════════╝$(RESET)\n\n"
```

**Categorized help with sections:**
```makefile
	@printf "$(BOLD)=== 🏗️  Build ===$(RESET)\n"
	@grep -h -E '^build-[a-zA-Z_-]+:.*?## .*$$' ... | awk ...
	@printf "$(BOLD)=== 🔧 Development ===$(RESET)\n"
	@grep -h -E '^dev-[a-zA-Z_-]+:.*?## .*$$' ... | awk ...
```

**Key help patterns:**
- `help` - Main categorized help
- `help-unclassified` - Show targets not in any category (useful for auditing)
- `help-all` - Show everything including internal targets
- Hidden targets: prefix with `_` (e.g., `_build-internal`)
- Legacy targets: label with `## (Legacy)` and filter from main help

**Always include a Help section in `make help` output:**

```makefile
	@printf "$(BOLD)=== ❓ Help ===$(RESET)\n"
	@printf "$(CYAN)%-25s$(RESET) %s\n" "help" "Show this help"
	@printf "$(CYAN)%-25s$(RESET) %s\n" "help-unclassified" "Show targets not in categorized help"
	@printf "\n"
```

**help-unclassified pattern** (note the `sed` to strip filename prefix):

```makefile
help-unclassified: ## Show targets not in categorized help
	@printf "$(BOLD)Targets not in main help:$(RESET)\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		sed 's/^[^:]*://' | \
		grep -v -E '^(env-|dev-|clean|help)' | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "$(CYAN)%-25s$(RESET) %s\n", $$1, $$2}' || \
		printf "  (none)\n"
```

**Description format - one line with example:**
```makefile
# Good - concise description + example on next line
@printf "$(CYAN)%-14s$(RESET) %s\n" "scrape" "Fetch posts into SQLite, detect problems"
@printf "               $(GREEN)make scrape SUBREDDITS=python,django LIMIT=10$(RESET)\n"
@printf "$(CYAN)%-14s$(RESET) %s\n" "dev-check" "Run ruff linter and formatter"
@printf "               $(GREEN)make dev-check FIX=true$(RESET)\n"

# Bad - too verbose, multi-line explanation
@printf "  $(CYAN)$(BOLD)setup$(RESET)\n"
@printf "      Install Python dependencies using uv. Run this once after cloning.\n"
@printf "      Creates .venv/ and installs packages from pyproject.toml.\n"
@printf "      $(GREEN)make setup$(RESET)\n"
```

**Help description rules:**
- **One line max** - Description must fit on single line unless user explicitly asks for more
- **Include what it affects** - e.g., "creates .venv", "exports to CSV", "deletes database"
- **Example on next line** - Show realistic usage with parameters in `$(GREEN)`
- **Skip examples for simple targets** - If no parameters, no example needed

**Catch-all redirects to help:**
```makefile
%:
	@printf "$(RED)Unknown target '$@'$(RESET)\n"
	@$(MAKE) help
```

## Common Pitfalls

| Issue | Fix |
|-------|-----|
| `$var` in shell loops | Use `$$var` to escape for make |
| Catch-all `%:` shows error | Redirect to `@$(MAKE) help` instead |
| Config vars scattered | Put all `?=` overridable defaults at TOP of root Makefile |
| `HELP_PATTERNS` mismatch | Must match grep patterns in help target exactly |
| Duplicate defs in modules | Define once in root, reference in modules |
| Trailing whitespace in vars | Causes path splitting bugs - trim all variable definitions |
| `.PHONY` on file targets | Only use `.PHONY` for non-file targets |
| Too many public targets | Don't expose `install-X` or `check-X` - use internal `_check-X` dependencies |
| `$(DIM)` for usage text | Appears grey/unreadable - use `$(GREEN)` instead |
| Target named after tool | Name after the action: `remove-bg` not `rembg` |
| `help-unclassified` shows filename | Use `sed 's/^[^:]*://'` to strip `Makefile:` prefix |
| No `.env` export | Add `-include .env` and `.EXPORT_ALL_VARIABLES:` at top |

## Cleanup Makefile Workflow

When user says "cleanup my makefiles":

**IMPORTANT: Build a plan first and explain it to the user before implementing anything.**

### Phase 1: Audit (no changes yet)

```bash
make help                    # See categorized targets
make help-unclassified       # Find orphaned targets
cat Makefile                 # Read structure
ls makefiles/*.mk 2>/dev/null # Check if modular
rg "make " --type md         # Find external dependencies
grep -E '\s+$' Makefile makefiles/*.mk  # Trailing whitespace
```

### Phase 2: Build & Present Plan

Create a checklist of proposed changes:

- [ ] **Structure** - Convert flat → modular (if 5+ targets) or vice versa
- [ ] **Legacy removal** - List specific targets to delete (with dependency check)
- [ ] **Duplicates** - List targets to consolidate
- [ ] **Renames** - List `old_name` → `new-name` changes
- [ ] **Description rewrites** - List vague descriptions to improve
- [ ] **Missing targets** - Suggest targets that should exist (e.g., `help-unclassified`)
- [ ] **Ordering fixes** - Config → imports → targets → help → catch-all

**Ask user to approve the plan before proceeding.**

### Phase 3: Implement (after approval)

1. **Restructure** (if needed) - Create `makefiles/` directory, split into modules
2. **Remove legacy** - Delete approved targets
3. **Consolidate duplicates** - Merge into single targets
4. **Rename targets** - Apply hyphen convention, add `_` prefix for internal
5. **Rewrite descriptions** - Make each `##` explain the purpose
6. **Fix formatting**
   - Usage examples in yellow: `$(YELLOW)make foo$(RESET)`
   - Remove trailing whitespace
   - `.PHONY` only on non-file targets
7. **Add missing pieces** - `help-unclassified`, catch-all `%:`, etc.

### Phase 4: Verify

```bash
make help          # Clean output?
make help-unclassified  # Should be empty or minimal
make -n <target>   # Dry-run key targets
```

### What NOT to do without asking:

- Rename targets that CI/scripts depend on
- Remove targets that look unused
- Change structure (flat ↔ modular) without approval

## Files in This Skill

- `reference.md` - Detailed patterns, categorized help, error handling
- `templates/` - Full copy-paste Makefiles for each stack
- `modules/` - Reusable pieces for complex projects

## Example: Adding a Target

User: "Add a target to run my tests"

```makefile
.PHONY: test
test: ## Run tests
	$(call print_section,Running tests)
	uv run pytest tests/ -v
	$(call print_success,Tests passed)
```

User: "Add database targets"

```makefile
.PHONY: db-start db-stop db-migrate

db-start: _check-docker ## Start database
	docker compose up -d postgres

db-stop: ## Stop database
	docker compose down

db-migrate: _check-postgres ## Run migrations
	uv run alembic upgrade head
```
