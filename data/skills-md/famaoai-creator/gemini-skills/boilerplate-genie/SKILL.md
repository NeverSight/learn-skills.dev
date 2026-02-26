---
name: boilerplate-genie
description: Scaffolds new projects with best practices (CI/CD, Tests, Linting) pre-configured. Ensures a "healthy" starting point for Next.js, FastAPI, Node.js, and more.
status: implemented
arguments:
  - name: name
    short: 'n'
    type: string
    required: true
    description: Project name
  - name: type
    short: T
    type: string
    required: true
    description: Project type
  - name: out
    short: o
    type: string
    description: Output directory (defaults to ./<name>)
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
  - integration
  - qa
---

# Boilerplate Genie

This skill accelerates project kickoff by generating a robust directory structure and configuration files based on industry standards and the `project-health-check` criteria.

## Capabilities

### 1. Best-Practice Scaffolding

- Generates project structures for Next.js, Python (FastAPI), Go, etc.
- **Rule Injection**: Automatically copies harvested coding standards (from `knowledge/external-wisdom/everything-claude/rules/`) into the project's `docs/guidelines/` or `.cursorrules`.

### 2. CI/CD & Testing Setup

- Configures GitHub Actions and test runners.

## Usage

- "Scaffold a new Next.js project in `work/my-app` with full CI/CD setup."
- "Create a clean FastAPI boilerplate for a REST API."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
