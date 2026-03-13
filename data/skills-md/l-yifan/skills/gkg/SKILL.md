---
name: gkg
description: Global Knowledge Graph for codebase analysis. This skill should be used when searching for code definitions (functions, classes, methods), finding references to symbols, understanding code structure, analyzing import usage, generating repository maps, or performing impact analysis before refactoring. Supports TypeScript, JavaScript, Python, Java, and more.
---

# Global Knowledge Graph (GKG)

## Overview

GKG provides semantic code analysis tools for exploring and understanding codebases. It indexes projects to enable fast symbol lookup, reference finding, and structural analysis.

## Quick Start

Run from this skill directory. Use `--raw` with JSON for parameters:

```bash
bun ./scripts/gkg.ts <command> --raw '<json>'
```

## Core Commands

### list-projects
List all indexed projects in the knowledge graph.

```bash
bun ./scripts/gkg.ts list-projects
```

### index-project
Rebuild the knowledge graph index for a project.

```bash
bun ./scripts/gkg.ts index-project \
  --raw '{"project_absolute_path":"/path/to/project"}'
```

### search-codebase-definitions
Find functions, classes, methods, constants across the codebase.

```bash
bun ./scripts/gkg.ts search-codebase-definitions \
  --raw '{"search_terms":["functionName","ClassName"],"project_absolute_path":"/path/to/project"}'
```

### get-references
Find all usages of a symbol across the codebase.

```bash
bun ./scripts/gkg.ts get-references \
  --raw '{"absolute_file_path":"/path/to/file.ts","definition_name":"myFunction"}'
```

### read-definitions
Read complete implementation of definitions.

```bash
bun ./scripts/gkg.ts read-definitions \
  --raw '{"definitions":[{"names":["myFunc"],"file_path":"/path/to/file.ts"}]}'
```

### get-definition
Go to definition for a symbol on a specific line.

```bash
bun ./scripts/gkg.ts get-definition \
  --raw '{"absolute_file_path":"/path/to/file.ts","line":"const result = myFunc()","symbol_name":"myFunc"}'
```

### repo-map
Generate a compact API-style map of repository structure.

```bash
bun ./scripts/gkg.ts repo-map \
  --raw '{"project_absolute_path":"/path/to/project","relative_paths":["src","lib"]}'
```

### import-usage
Analyze import usages across the project.

```bash
bun ./scripts/gkg.ts import-usage \
  --raw '{"project_absolute_path":"/path/to/project","packages":[{"import_path":"react"}]}'
```

## Common Workflows

### Refactoring Impact Analysis
1. Use `search-codebase-definitions` to find the symbol
2. Use `get-references` to find all usages
3. Review each usage location before making changes

### Understanding Unfamiliar Code
1. Use `repo-map` to get project structure overview
2. Use `search-codebase-definitions` to find relevant functions
3. Use `read-definitions` to read implementations

### Tracing Dependencies
1. Use `import-usage` to find where packages are imported
2. Use `get-references` to trace function call chains

## Resources

### scripts/
- `gkg.ts` - CLI tool for all knowledge graph operations

### references/
- `api_reference.md` - Detailed parameter documentation for each command
