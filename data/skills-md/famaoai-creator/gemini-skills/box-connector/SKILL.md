---
name: box-connector
description: Securely connects to Box using the Node.js SDK (JWT). downloads files, searches content, and manages folder structures.
status: implemented
arguments:
  - name: action
    short: a
    type: string
    description: Action to perform
  - name: folder
    short: f
    type: string
    description: Box folder ID
  - name: query
    short: q
    type: string
    description: Search query
  - name: config
    short: c
    type: string
    description: Path to Box JWT config
  - name: dry-run
    type: boolean
    description: Simulate without API calls
  - name: out
    short: o
    type: string
    description: Output file path
category: Integration & API
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Box Connector

This skill automates file operations on Box, bridging your cloud storage with local workflows.

## Capabilities

### 1. Secure Authentication

- Uses `knowledge/personal/box_config.json` (JWT config) to authenticate without hardcoding credentials.
- Supports "App User" and "Enterprise" contexts.

### 2. File Retrieval

- **Download**: Fetches specific files by ID or name.
- **Search**: Finds files based on queries and downloads the latest version.

## Usage

- "Download the file 'Q3_Financials.xlsx' from Box."
- "Search Box for 'Project_X_Specs' and save it to `work/docs/`."

## Knowledge Protocol

- Adheres to `knowledge/tech-stack/box_api.md`.
