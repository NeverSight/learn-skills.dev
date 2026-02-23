---
name: website-to-skill-folder
description: >
  Converts any website into an installable AI skill folder by crawling all pages
  and packaging them as searchable markdown with frontmatter summaries. Use when
  asked to: create a website search skill, index a website for AI agents, scrape
  a site into a searchable knowledge base, turn a website into an offline-searchable
  skill, or make website content available to AI agents without live browsing.
  Outputs an installable skill folder plus the exact npx command to add it to any
  AI agent.
---

# Website-to-Skill Pipeline

Runs `scripts/pipeline.py` to crawl a website and produce an installable skill folder.
The script handles everything — no need to read it.

## 1. Locate the Skill

```bash
SKILL_DIR="$HOME/.agents/skills/website-to-skill-folder"
[ -d "$SKILL_DIR" ] || SKILL_DIR=$(find "$HOME/.agents/skills" "$HOME/.claude/skills" \
  -maxdepth 2 -type d -name "website-to-skill-folder" 2>/dev/null | head -1)
echo "Skill dir: $SKILL_DIR"
```

## 2. Pre-flight Checks

Run these in order before the pipeline. Fix anything missing before proceeding — do not skip.

### Python (required: 3.8+)

```bash
python --version 2>&1 || python3 --version 2>&1
```

- If `python` is Python 2 or not found, use `python3` for all commands below.
- If neither is found: tell the user to install Python 3.8+ and stop.

### Python packages (one-time)

```bash
python -c "import requests, pydantic, tenacity; print('OK')" 2>&1
```

If `ModuleNotFoundError`: install and retry before proceeding.

```bash
pip install requests pydantic tenacity
```

### Firecrawl API key

```bash
python -c "import os; print('set' if os.environ.get('FIRECRAWL_API_KEY') else 'missing')"
```

If missing: **stop and ask the user for their Firecrawl API key.**

Tell them: "A Firecrawl API key is needed to crawl websites. Get a free key at https://firecrawl.dev — no credit card required."

Once they provide it, use it inline in the run command below (Step 3).

## 3. Run the Pipeline

Inline both the skill path and the API key so the command is self-contained:

```bash
FIRECRAWL_API_KEY="fc-their_key_here" python "$HOME/.agents/skills/website-to-skill-folder/scripts/pipeline.py" https://example.com
```

If the skill was installed to a different location (check Step 1 output), substitute that path:

```bash
FIRECRAWL_API_KEY="fc-their_key_here" python "$SKILL_DIR/scripts/pipeline.py" https://example.com
```

**Options:**

| Flag | Purpose |
|------|---------|
| `--description "..."` | One-line site description for the generated SKILL.md |
| `--max-pages 100` | Limit pages scraped — directly controls Firecrawl credit cost |
| `--skip-scrape` | Reassemble from cache — zero API calls |
| `--force-refresh` | Ignore cache, re-scrape all pages |

## 4. Install the Output Skill

When the pipeline finishes, it prints the exact install command with the real absolute path
to the skill folder it just built. It looks like this (path will differ on your machine):

```
  Install / update skill in agents:

    Claude Code:
    npx skills add "/Users/yourname/path/to/output/example-com-website-search-skill" -g -y -a claude-code

    All agents:
    npx skills add "/Users/yourname/path/to/output/example-com-website-search-skill" -g -y
```

**Before running:** Show the user the command printed by the pipeline and ask:

> "The skill folder is ready. Shall I install it now so your agents can search [domain] offline?"

Only run the install command after the user confirms. Use the exact path from the pipeline
output — do not use the example path shown above.

### If `npx` fails

`npx skills` requires Node.js. Check:

```bash
node --version 2>&1
```

If not found: tell the user "Node.js is required to install the skill. Download it from
https://nodejs.org (LTS version) — it includes npx." Once they install it, re-run the
install command.

After installing, the user's agents can answer questions about the website offline.
Re-run the pipeline and re-run the install command any time to pick up new pages.

## Cost

1 Firecrawl credit (map) + ~5 credits per page scraped.
Example: 100-page site ≈ 501 credits.
Incremental re-runs only pay for new or changed pages.
