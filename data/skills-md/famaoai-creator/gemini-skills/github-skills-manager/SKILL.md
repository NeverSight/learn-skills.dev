---
name: github-skills-manager
description: Comprehensive management suite for Gemini skills. Features an interactive dashboard to create, install, sync (git), and manage dependencies for skills in a monorepo or individual repositories.
status: implemented
category: Utilities
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# GitHub Skills Manager

## Overview

This skill acts as a central command center for your Gemini skills ecosystem. It simplifies the lifecycle of skill development by providing an interactive dashboard to manage Git repositories, install skills into your workspace, resolve dependencies, and create new skills from templates.

Whether you maintain a single monorepo of skills or multiple standalone repositories, this manager streamlines the process.

## Quick Start

The most powerful way to use this skill is via its interactive dashboard:

```bash
node scripts/dashboard.cjs
```

This launches a Text User Interface (TUI) where you can perform almost all available actions.

## Capabilities

### 1. Interactive Dashboard (Recommended)

Launch a unified menu system to manage your skills.

- **Command**: `node scripts/dashboard.cjs`
- **Features**:
  - **List & Status**: See all skills, their installation status (`[INSTALLED]`), and Git modification status.
  - **One-Click Install**: Install any skill (or ALL skills) into your workspace with a single keypress.
  - **Dependency Management**: Automatically detects `package.json` and offers to run `npm install`.
  - **Create & Delete**: Generate new skills from templates or safely remove them.

### 2. Batch Operations

Manage your entire skill library at once via the dashboard main menu.

- **Sync All**: Run `git pull` across the root repository to update all skills.
- **Install All**: Loop through every skill directory and install it to your workspace.
- **Push All**: Commit and push changes for the entire monorepo.

### 3. Skill Creation

Rapidly prototype new ideas.

- **Command**: `node scripts/create_skill.cjs <skill-name>` (or use Dashboard "Create New Skill")
- **Effect**: Initializes a new skill directory with the standard structure (`SKILL.md`, `scripts/`, `references/`) using `skill-creator`.

### 4. Git Integration

Keep your skills version-controlled.

- **Status Checks**: Instantly see which skills have uncommitted changes.
- **Sync**: Pull latest changes from GitHub.
- **Publish**: Push your local improvements to the remote repository.

## Workflow Example

1. Run `node scripts/dashboard.cjs`.
2. Select **"c. Create New Skill"** and name it `my-new-tool`.
3. Select the new skill from the list.
4. Choose **"1. Install Skill"** to make it available to Gemini.
5. Edit the skill files in your editor.
6. In the dashboard, choose **"3. Git Push"** to save your work.

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
