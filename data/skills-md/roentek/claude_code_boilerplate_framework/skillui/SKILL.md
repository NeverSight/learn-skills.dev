---
name: skillui
description: "Extract a complete design system from any website, local directory, or public GitHub repo using the skillui CLI. Generates SKILL.md, DESIGN.md, and token files (colors.json, spacing.json, typography.json) that Claude reads automatically. Use when the user wants to extract a design system or design tokens from an existing site or codebase before building a UI, wants a reference design system to match, or says things like 'extract the design system from', 'get the tokens from', 'pull styles from this site', 'clone the look of', or provides a URL/repo and wants to match its visual language."
---

# SkillUI — Design System Extractor

Extracts design systems from live websites, local projects, or public repos into Claude-readable files (`SKILL.md`, `DESIGN.md`, token JSON). Use this before building any UI when you want to match an existing site's visual language.

## When to Use

- User provides a URL and wants to match or clone its design style
- User wants to extract colors, fonts, spacing from an existing site
- User has a local project or repo and wants its design tokens extracted
- User says "pull the design from", "match this site", "get the tokens from", "extract styles from"

## Modes

| Mode | Command | Use When |
| ------ | --------- | ---------- |
| URL (static) | `npx skillui --url <url>` | Fast extraction — HTML/CSS/fonts/colors |
| URL (ultra) | `npx skillui --url <url> --mode ultra --screens 10` | Full extraction with screenshots, animations, interactions. Requires Playwright. |
| Local directory | `npx skillui --dir ./path/to/project --name "ProjectName"` | Scan a local Next.js/React/Tailwind project |
| Public repo | `npx skillui --repo https://github.com/user/repo` | Clone and analyze any public GitHub repo |

## Workflow

### Step 1 — Run the extractor

```bash
# Basic (recommended first try)
npx skillui --url https://example.com

# With output folder
npx skillui --url https://example.com --out ./design-systems/example

# Ultra mode (full extraction with screenshots)
npx skillui --url https://example.com --mode ultra --screens 10
```

### Step 2 — Open the output in Claude Code

The generated folder contains:

- `SKILL.md` / `CLAUDE.md` — Claude reads these automatically when you open the folder
- `DESIGN.md` — Full design system documentation
- `tokens/colors.json`, `tokens/spacing.json`, `tokens/typography.json`
- `screens/` — Screenshots (ultra mode only)
- `fonts/` — Bundled Google Fonts (woff2)

Open the generated folder:

```bash
cd <generated-folder-name> && claude
```

Or reference the `DESIGN.md` directly in the current session by reading it with the Read tool.

### Step 3 — Use the design system

Once the output is generated, read the token files and `DESIGN.md` into context, then apply them when building UI. Pass the relevant tokens to the `frontend-design` skill and `ui-ux-pro-max` design system generator.

## Notes

- No API keys or cloud dependencies — runs entirely locally
- For ultra mode, Playwright must be installed: `npm install playwright && npx playwright install chromium`
- Output folder name is auto-derived from the site/repo name
- The `.skill` ZIP archive in the output can be shared or archived
