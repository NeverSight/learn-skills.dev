---
name: makefile-best-practices
description: Best practices for creating self-documenting Makefiles with auto-generated help. Use when creating or modifying Makefiles to ensure they follow conventions for discoverability and maintainability.
license: MIT
---

When creating or modifying Makefiles, follow these principles to ensure they are self-documenting and user-friendly.

## 1. Default Target Must Be `help`

Always set `help` as the default target so users can discover available commands:

```makefile
.DEFAULT_GOAL := help
```

This ensures running `make` without arguments shows available targets instead of executing an arbitrary first target.

## 2. Self-Documenting Help Target

The `help` target should automatically build itself from comments in the Makefile. Use the `##` comment pattern:

```makefile
target-name: ## Description of what this target does
	@command here

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
```

### Pattern Explanation

- `target: ## Description` - The `##` marks the description for that target
- `##@ Section` - Creates optional section headers in the help output
- The `awk` command parses these patterns and formats the output

### Benefits

- Documentation stays with the code
- Adding new targets automatically updates help
- No manual maintenance of help text
- Consistent format across all Makefiles

## Audit Mode

When asked to audit a Makefile, check for the following issues and report findings:

### Required
- [ ] `.DEFAULT_GOAL := help` is set
- [ ] `help` target exists
- [ ] `help` target uses the self-documenting awk pattern
- [ ] All targets have `## Description` comments

### Warnings
- [ ] Targets without descriptions (missing `##`)
- [ ] Missing `.PHONY` declarations for non-file targets
- [ ] `help` target is not using `$(MAKEFILE_LIST)` (won't work with includes)

### Report Format

```
Makefile Audit: <path>

PASS: .DEFAULT_GOAL set to help
PASS: help target exists
FAIL: 3 targets missing ## descriptions: build, test, deploy
WARN: Missing .PHONY for: build, test, clean

Summary: 2 passed, 1 failed, 1 warning
```

Provide specific line numbers and suggested fixes for each issue found.

## 3. Install/Uninstall Pattern for Scripts and Binaries

For one-off shell scripts or binaries that should be available in `~/bin`, use this symlink pattern:

### Variables

```makefile
SCRIPT_NAME := my-script.sh
INSTALL_DIR := $(HOME)/bin
INSTALL_PATH := $(INSTALL_DIR)/$(SCRIPT_NAME)
SOURCE_PATH := $(CURDIR)/$(SCRIPT_NAME)
```

### Install Target

```makefile
install: ## Install symlink to ~/bin
	@mkdir -p $(INSTALL_DIR)
	@if [ -L "$(INSTALL_PATH)" ]; then \
		echo "Removing existing symlink..."; \
		rm -f "$(INSTALL_PATH)"; \
	elif [ -e "$(INSTALL_PATH)" ]; then \
		echo "Error: $(INSTALL_PATH) exists and is not a symlink"; \
		exit 1; \
	fi
	@ln -s "$(SOURCE_PATH)" "$(INSTALL_PATH)"
	@echo "Installed: $(INSTALL_PATH) -> $(SOURCE_PATH)"
```

### Uninstall Target

```makefile
uninstall: ## Remove symlink from ~/bin
	@if [ -L "$(INSTALL_PATH)" ]; then \
		rm -f "$(INSTALL_PATH)"; \
		echo "Removed: $(INSTALL_PATH)"; \
	elif [ -e "$(INSTALL_PATH)" ]; then \
		echo "Error: $(INSTALL_PATH) exists but is not a symlink (not removing)"; \
		exit 1; \
	else \
		echo "Nothing to remove: $(INSTALL_PATH) does not exist"; \
	fi
```

### Check Target (Optional)

```makefile
check: ## Check installation status
	@echo "Source: $(SOURCE_PATH)"
	@if [ -L "$(INSTALL_PATH)" ]; then \
		echo "Status: Installed (symlink)"; \
		echo "Target: $$(readlink "$(INSTALL_PATH)")"; \
	elif [ -e "$(INSTALL_PATH)" ]; then \
		echo "Status: Exists but NOT a symlink"; \
	else \
		echo "Status: Not installed"; \
	fi
```

### Key Principles

1. **Always use symlinks** - Never copy files; symlinks ensure updates are automatic
2. **Safe removal** - Only remove if it's a symlink to prevent accidental deletion
3. **Idempotent install** - Running install multiple times should work
4. **Fail on conflicts** - If a non-symlink file exists, error rather than overwrite
5. **Create ~/bin if needed** - `mkdir -p` ensures the directory exists

### For Sourced Scripts

If the script needs to be sourced (not executed), add post-install instructions:

```makefile
install: ## Install symlink to ~/bin
	@mkdir -p $(INSTALL_DIR)
	# ... symlink creation ...
	@echo ""
	@echo "Add to your shell config:"
	@echo "  source ~/bin/$(SCRIPT_NAME)"
```

### Complete Example

```makefile
# my-tool Makefile

SCRIPT_NAME := my-tool.sh
INSTALL_DIR := $(HOME)/bin
INSTALL_PATH := $(INSTALL_DIR)/$(SCRIPT_NAME)
SOURCE_PATH := $(CURDIR)/$(SCRIPT_NAME)

.PHONY: help install uninstall check lint test all clean

.DEFAULT_GOAL := help

##@ General

help: ## Show this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Installation

install: ## Install symlink to ~/bin
	@mkdir -p $(INSTALL_DIR)
	@if [ -L "$(INSTALL_PATH)" ]; then \
		echo "Removing existing symlink..."; \
		rm -f "$(INSTALL_PATH)"; \
	elif [ -e "$(INSTALL_PATH)" ]; then \
		echo "Error: $(INSTALL_PATH) exists and is not a symlink"; \
		exit 1; \
	fi
	@ln -s "$(SOURCE_PATH)" "$(INSTALL_PATH)"
	@echo "Installed: $(INSTALL_PATH) -> $(SOURCE_PATH)"

uninstall: ## Remove symlink from ~/bin
	@if [ -L "$(INSTALL_PATH)" ]; then \
		rm -f "$(INSTALL_PATH)"; \
		echo "Removed: $(INSTALL_PATH)"; \
	elif [ -e "$(INSTALL_PATH)" ]; then \
		echo "Error: $(INSTALL_PATH) exists but is not a symlink (not removing)"; \
		exit 1; \
	else \
		echo "Nothing to remove: $(INSTALL_PATH) does not exist"; \
	fi

check: ## Check installation status
	@echo "Source: $(SOURCE_PATH)"
	@if [ -L "$(INSTALL_PATH)" ]; then \
		echo "Status: Installed (symlink)"; \
		echo "Target: $$(readlink "$(INSTALL_PATH)")"; \
	elif [ -e "$(INSTALL_PATH)" ]; then \
		echo "Status: Exists but NOT a symlink"; \
	else \
		echo "Status: Not installed"; \
	fi

##@ Development

lint: ## Run shellcheck on scripts
	shellcheck $(SCRIPT_NAME)

test: ## Run tests
	./test.sh

# Stubs to satisfy checkmake minphony rule
all: help
clean: uninstall
```
