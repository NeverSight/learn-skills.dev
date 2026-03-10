---
name: code-analyzer
description: "Comprehensive codebase analysis for building mental model of project structure, dependencies, and implementation context. Use when needing to: (1) Understand project architecture before review or documentation, (2) Find dependencies and shared modules, (3) Locate implementation markers (AICODE-*), (4) Prepare context for review, memory generation, or agent creation. Triggers on: analyze code, load code context, scan codebase, understand project structure."
allowed-tools: Read, Bash (*)
---

# Code Analyzer

Analyze codebase to build comprehensive mental model for downstream operations.

## Workflow Overview

1. **Scan** — Collect facts via bash script (deterministic)
2. **Understand** — Interpret structure and stack
3. **Build** — Construct dependency graph and mental model
4. **Confirm** — Ready for operations

## Step 1: Scan Project

Run codebase scanner to collect facts:

```bash
.claude/skills/code-analyzer/scripts/scan-codebase.sh
```

Scanner auto-detects project root (git root or pwd) and collects:
- Structure: file count, extensions, configs, directories, src modules
- Markers: AICODE-NOTE, AICODE-TODO, AICODE-FIX with locations
- Git: branch, modified/added/deleted files

Outputs JSON. No external dependencies required.

### Exclusions (automatic)
- node_modules, .git, dist, build
- __pycache__, .venv, venv
- ai-docs, .next, .nuxt, coverage, .cache

## Step 2: Understand Structure

Interpret scan results to determine:
- **Stack**: Language(s) from extensions, framework from configs
- **Entry points**: Main/index/app files in directories
- **Modules**: Domain boundaries from src_modules or directories
- **Conventions**: Naming patterns, structure style

## Step 3: Build Mental Model

Extract and internalize from scan results:

**From structure:**
- Stack: `[language] | [framework] | [build-tool]`
- Entry points with types
- Module list with inferred domains
- Directory organization

**From markers:**
- AICODE-NOTE → Implementation context (why decisions were made)
- AICODE-TODO → Planned work (incomplete areas)
- AICODE-FIX → Known issues (from previous reviews)

**From git:**
- Current branch → feature context
- Changed files → review/focus scope

**From reading key files:**
- Import patterns → dependency relationships
- Shared modules → components with 3+ incoming connections
- Circular dependencies → architectural issues

## Step 4: Confirm Readiness

Output minimal confirmation:
```
✅ Code context loaded: [project-name]
   Stack: [language] | [framework]
   Modules: [count] ([list])
   Markers: [N] NOTE, [N] TODO, [N] FIX
   Ready for: review | documentation | agent-generation
```

## Error Handling

- **Empty project**: Report "No source files found"
- **No git repo**: Continue without git section (is_repo: false)
- **Permission denied**: Report file, continue with available

## Usage Notes

This skill prepares context for:
- Code review (scope, markers, dependencies)
- Documentation generation (structure, stack)
- Agent creation (domains, boundaries)
- Architecture queries

Context remains in memory for entire conversation.