---
name: github-repo-cards
description: "Fetching GitHub repo or trending info via gh CLI and rendering beautiful SVG/PNG card images. Use when asked to visualize repo stats, trending repos, or generate GitHub-style cards."
---

# GitHub Repo Cards

Generate beautiful GitHub-style SVG card images for repositories or trending projects, then convert them to PNG.

## Capabilities

1. **Repo Card** — given `<org>/<repo>`, produce a card showing:
   - Basic info (name, description, language, license)
   - Star & commit activity sparkline
   - Top N contributors (avatars + commit counts)
   - A customisable "analysis" text block

2. **Trending Card** — fetch today's trending repos and render a list card with:
   - Repo name, description, language badge
   - Star / fork counts
   - Recent commit activity sparkline (mini bar chart)

## Workflows

### Generate a Repo Card

```
uv run scripts/gh_repo_card.py <org>/<repo> [--top-n 5] [--analysis "Your analysis text here"] [--output card.svg]
```

The script path is relative to this skill directory:
`skills/github-repo-cards/scripts/gh_repo_card.py`

This will:
1. Call `gh` to fetch repo metadata, stargazer counts, commit activity, and top contributors.
2. Render an SVG card with all the information.
3. Convert the SVG to PNG via `rsvg-convert` (falls back to ImageMagick `convert`).

### Generate a Trending Card

```
uv run scripts/gh_trending_card.py [--language python] [--since daily] [--limit 10] [--output trending.svg]
```

The script path is relative to this skill directory: `scripts/gh_trending_card.py`

This will:
1. Scrape GitHub trending page (or use `gh api` search with recent star sorting).
2. Render a multi-row SVG list card.
3. Convert to PNG.

## Output

SVG and PNG files are written to the current working directory (or the path given by `--output`). The PNG file shares the same base name.

## Requirements

- `gh` CLI authenticated (`gh auth status`)
- `rsvg-convert` (librsvg) **or** ImageMagick `convert` for SVG→PNG
- Python ≥ 3.12, run via `uv run` (PEP 723 inline metadata)
