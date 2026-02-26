---
name: knowledge-harvester
description: Clones external Git repositories and analyzes them to extract valuable knowledge. Converts discovered prompts, rules, and patterns into local knowledge assets.
status: implemented
arguments:
  - name: repo
    short: r
    type: string
    required: true
    description: Git repository URL
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Knowledge Harvester

This skill allows the ecosystem to "learn" from other open-source projects.

## Capabilities

### 1. Repository Analysis

- Clones a target repo to a temp directory.
- Maps the file structure using `codebase-mapper`.
- Identifies "high-value" files (prompts, .md guides, config files).

### 2. Knowledge Extraction

- summarizing key concepts from READMEs and documentation.
- Converting external rule files (e.g., `.clauderc`) into Gemini-compatible knowledge formats in `knowledge/external-wisdom/`.

### 3. Skill Prototyping

- If executable scripts are found, suggests how to wrap them into a new Gemini Skill.

## Usage

- "Harvest knowledge from https://github.com/affaan-m/everything-claude-code."
- "Analyze this repo and extract its TDD best practices."

## Knowledge Protocol

- Respects licenses (MIT, Apache 2.0).
- Stores harvested data in `knowledge/external-wisdom/`.
