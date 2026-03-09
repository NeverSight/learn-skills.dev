---
name: domain-discover
description: Discover and document domain knowledge from a codebase into a structured knowledge file
agent: general-purpose
model: sonnet
argument-hint: Domain name [OUT_DIR] (e.g. "payments", "auth ./out")
allowed-tools: Read, Bash, Write, Edit
context: fork
---

# Discover Domain Knowledge

You are tasked with creating a comprehensive domain knowledge file for a codebase that will help future Claude Code instances work effectively with this repository.

## Arguments
- `$ARGUMENTS[0]` — Domain name used as the output filename (`{domain}.md`)
- `$ARGUMENTS[1]` — (optional) Output directory for the domain knowledge file. Defaults to `.` (project root / current working directory)

When invoked by the orchestrator (e.g. `implement`), `$ARGUMENTS[1]` is provided. When used standalone, it defaults to the project root for backward compatibility.

## Output Location

- Creates or updates `$ARGUMENTS[1]/{$ARGUMENTS[0]}.md` (e.g. `./payments.md`)
- Run `mkdir -p $ARGUMENTS[1]` before writing to ensure the directory exists.

## Objective

Analyze the provided codebase and create or update a `{DOMAIN}.md` file containing essential information for productive development.

## Analysis Approach

1. First, scan the repository structure to understand the project type and technology stack
2. Read key configuration files (package.json, requirements.txt, Makefile, etc.) to identify build/test commands
3. Examine main application files to understand the high-level architecture
4. Review existing documentation (README.md, docs/) for important context

## Execution

Follow [references/rules.md](references/rules.md) for content requirements, guidelines, and safety rules.
Use [references/output-format.md](references/output-format.md) for the output template and validation criteria.

<tags>
   <mode>standard</mode>
   <custom>yes</custom>
</tags>
