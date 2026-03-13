---
name: tools-catppuccin
description: Agent skill for creating and validating Catppuccin theme ports
---

# Catppuccin Port Creation Skill

## Overview

Agent skill for automated Catppuccin theme generation, color validation, and port preparation. The agent handles technical theme generation while users handle manual repository and submission tasks.

## Quick Start

For immediate help:
- **Agent generates**: Theme files, color mappings, validation reports
- **User handles**: Repository setup, testing, GitHub submissions
- **Colors defined in**: references/official-palette.json
- **Port template**: https://github.com/catppuccin/template

## Agent Capabilities

### Target Analysis
When given an application/library name (e.g., "XYZ"), the agent can:
- Research the application's theming system and documentation
- Identify if it uses CSS, JSON, XML, or proprietary theme formats
- Find existing theme examples and configuration files
- Locate color customization APIs or styling hooks
- Determine theming architecture (component-level, global, hybrid)

### Theme Generation
- Converts color schemes to CSS, SCSS, JSON, XML formats
- Creates all four flavor variants (Latte, Frappé, Macchiato, Mocha)
- Applies semantic color mappings for consistency
- Generates component-specific color definitions

### Color Validation
- Validates against official Catppuccin palette
- Calculates WCAG contrast ratios
- Identifies color conflicts and suggests fixes
- Generates compliance reports

### Analysis & Preparation
- Extracts colors from existing themes
- Identifies unthemed elements from screenshots
- Generates preview compositions
- Creates submission-ready documentation

## User Responsibilities

### Repository Setup
```bash
git clone https://github.com/catppuccin/template.git <port-name>
cd <port-name>
rm -rf .git
git init
```

### Testing & Submission
- Test all four flavors in target application
- Take screenshots for preview generation
- Create GitHub issues/PRs for submission
- Respond to review feedback

## Workflow

### Phase 1: Target Analysis
When user requests a port for "XYZ":
- **Agent**: Researches XYZ's theming documentation, identifies styling system
- **Agent**: Finds existing themes and color customization methods
- **User**: Confirms target application and provides any special requirements

### Phase 2: Theme Generation
- **Agent**: Generates theme files based on XYZ's theming system
- **Agent**: Creates all four flavor variants with proper semantic mapping
- **User**: Tests themes in XYZ application, provides feedback

### Phase 3: Preparation
- **Agent**: Creates documentation specific to XYZ's installation process
- **User**: Takes screenshots of themed XYZ application
- **Agent**: Generates preview compositions from user screenshots

### Phase 4: Submission
- **User**: Creates GitHub issue/PR for XYZ port
- **Agent**: Assists with any reviewer-requested changes

## Common Issues

### Color Problems
- **Agent can**: Detect mismatched colors, suggest fixes, generate corrected files
- **User should**: Provide screenshots, test fixes in application

### Repository Issues
- **Agent can**: Generate proper structure, create README files
- **User should**: Initialize repository, update metadata

### Submission Issues
- **Agent can**: Check for duplicates, validate package completeness
- **User should**: Create GitHub issue/PR, respond to feedback

## Resources

For detailed guidelines, color references, and community support:
- Official documentation: https://github.com/catppuccin/catppuccin
- Color palette: references/official-palette.json (this directory)
- Community discussions: https://discord.com/servers/catppuccin-907385605422448742
- Userstyles submissions: https://github.com/catppuccin/userstyles
- Application port reviews: https://github.com/catppuccin/catppuccin/issues/new?assignees=&template=port-review.yml