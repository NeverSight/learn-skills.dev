---
name: evolving-skill-creator
description: Guide for creating evolving skills - detailed workflow plans that capture what you'll do, what tools you'll create, and learnings from execution. Use this when starting a new task that could benefit from a reusable workflow.
---

# Evolving Skill Creator

Create **evolving skills** - detailed workflow plans that become reusable through iteration.

## What is an Evolving Skill?

An evolving skill is a workflow plan that:
1. Documents specific steps to accomplish a goal
2. Lists Python scripts you'll create as reusable tools
3. Captures learnings after execution for future improvement

Unlike static skills, evolving skills are refined through use.

## Directory Structure

```
tasks/evolving_skill/
├── SKILL.md              # Your workflow plan
└── scripts/              # Python tools you create during execution
    ├── scrape_data.py
    └── generate_output.py
```

## SKILL.md Format

**IMPORTANT: YAML Frontmatter is Required**

Every evolving skill MUST start with YAML frontmatter containing `name` and `description`. These fields are critical for skill discovery - they determine how the skill is identified when loaded in future sessions.

```yaml
---
name: descriptive-skill-name    # REQUIRED - used for identification
description: Clear explanation of what this workflow does and when to use it  # REQUIRED - used for discovery
---
# Task Name

## Overview
Brief description of the problem this skill solves.

## Workflow
Detailed numbered steps:
1. First step - be specific
2. Second step - include commands/tools to use
3. ...

## Tools to Create
Python scripts you'll write. Document BEFORE writing them:

### scripts/example_tool.py
- **Purpose**: What it does
- **Inputs**: What it takes (args, files, etc.)
- **Outputs**: What it produces
- **Dependencies**: Required packages

## Tools to Use
(Discover what's available, list ones you'll use)
- servers/name: MCP server tools
- custom_tools/name: Python tool implementations

## Skills
- skill_name: how it will help

## Packages
- package_name (pip install package_name)

## Expected Outputs
- Files this workflow produces
- Formats and locations

## Learnings
(Add after execution)

### What Worked Well
- ...

### What Didn't Work
- ...

### Tips for Future Use
- ...
```

## Tools to Create Section

This is the key differentiator. When your workflow involves writing Python scripts, document them upfront:

```markdown
## Tools to Create

### scripts/fetch_artist_data.py
- **Purpose**: Crawl Wikipedia and extract artist biographical data
- **Inputs**: artist_name (str), output_path (str)
- **Outputs**: JSON file with structured bio data
- **Dependencies**: crawl4ai, json

### scripts/build_site.py
- **Purpose**: Generate static HTML from artist data
- **Inputs**: data_path (str), theme (str), output_dir (str)
- **Outputs**: Complete website in output_dir/
- **Dependencies**: jinja2
```

After execution, the actual scripts live in `scripts/` and can be reused.

## Creating an Evolving Skill

1. **Create directory**: `mkdir -p tasks/evolving_skill`
2. **Write SKILL.md** with proper YAML frontmatter first:
   - `name`: Use a descriptive, reusable name (e.g., `artist-website-builder`, not `bob-dylan-site`)
   - `description`: Explain what the workflow does and when to use it
3. **Execute workflow** following your plan
4. **Create scripts** as documented in Tools to Create
5. **Update SKILL.md** with Learnings after completion

### Naming Guidelines

Choose names that describe the **type of task**, not the specific instance:
- **Good**: `artist-website-builder`, `data-scraper-to-static-site`, `pdf-report-generator`
- **Bad**: `bob-dylan-project`, `session-12345`, `my-task`

The name should make it clear what the skill does when discovered in future sessions.

## Updating After Execution

After completing your work:

1. **Refine Workflow** - Update steps based on what actually worked
2. **Move scripts** - Ensure working scripts are in `scripts/`
3. **Add Learnings** - Document what worked, what didn't, tips

## Example: Complete Evolving Skill

```yaml
---
name: artist-website-builder
description: Build static biographical websites for artists by scraping public sources and generating themed HTML.
---
# Artist Website Builder

## Overview
Create professional artist websites by gathering biographical data and generating themed static HTML.

## Workflow
1. Research artist - gather name variations, active years
2. Scrape data using scripts/fetch_artist_data.py
3. Review and clean extracted data
4. Generate site using scripts/build_site.py with "minimalist-dark" theme
5. Review in browser, check mobile responsiveness
6. Iterate on styling if needed

## Tools to Create

### scripts/fetch_artist_data.py
- **Purpose**: Crawl Wikipedia and extract artist biographical data
- **Inputs**: artist_name (str)
- **Outputs**: artist_data.json
- **Dependencies**: crawl4ai

### scripts/build_site.py
- **Purpose**: Generate static HTML from artist data
- **Inputs**: artist_data.json, theme_name
- **Outputs**: Complete website in output/
- **Dependencies**: jinja2

## Tools to Use
- servers/context7: fetching crawl4ai and jinja2 documentation
- servers/browser: capturing site previews for review
- custom_tools/image_optimizer: compressing generated assets

## Skills
- web-scraping-patterns: structuring the crawl4ai approach

## Packages
- crawl4ai (pip install crawl4ai)
- jinja2 (pip install jinja2)

## Expected Outputs
- output/index.html
- output/discography.html
- output/assets/

## Learnings

### What Worked Well
- Wikipedia infoboxes have consistent structure
- crawl4ai async mode is 3x faster than sync
- "minimalist-dark" theme works best for musicians

### What Didn't Work
- AllMusic requires JS rendering - use Discogs API instead
- Initial theme had poor mobile layout

### Tips for Future Use
- Always check robots.txt before scraping
- Cache scraped data - re-running is slow
- Test on mobile early
```

## Key Principles

1. **Be specific** - Workflow steps should be actionable, not vague
2. **Document tools upfront** - Plan scripts before writing them
3. **Test like a user** - Verify artifacts through interaction, not just observation (click buttons, play games, navigate pages, run with edge cases, etc)
4. **Update with learnings** - The skill improves through use
5. **Keep scripts reusable** - Design tools to work in similar future tasks
