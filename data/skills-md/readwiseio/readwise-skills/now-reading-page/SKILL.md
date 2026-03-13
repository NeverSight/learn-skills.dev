---
name: now-reading-page
description: Generate a personal "Now Reading" webpage from your Reader library
---

You are generating a beautiful standalone HTML page showing what the user is currently reading and has recently read. The output is a single HTML file they can open in a browser or host on their personal site.

## Readwise Access

Check if Readwise MCP tools are available (e.g. `mcp__readwise__reader_list_documents`). If they are, use them throughout (and pass this context to the subagent). If not, use the equivalent `readwise` CLI commands instead (e.g. `readwise list`, `readwise read <id>`). The instructions below reference MCP tool names — translate to CLI equivalents as needed.

## Process

Launch a **Task subagent** to fetch all the data and generate the HTML file. The subagent should:

### 1. Fetch Data

Run ALL of these in parallel:

- **Shortlist:** `mcp__readwise__reader_list_documents` with `location="shortlist"`, `limit=50`, `response_fields=["title", "author", "category", "reading_progress", "first_opened_at", "last_opened_at", "image", "url", "site_name", "word_count", "saved_at"]`
- **Later:** `mcp__readwise__reader_list_documents` with `location="later"`, `limit=50`, `response_fields=["title", "author", "category", "reading_progress", "first_opened_at", "last_opened_at", "image", "url", "site_name", "word_count", "saved_at"]`
- **Inbox:** `mcp__readwise__reader_list_documents` with `location="new"`, `limit=50`, `response_fields=["title", "author", "category", "reading_progress", "first_opened_at", "last_opened_at", "image", "url", "site_name", "word_count", "saved_at"]`
- **Archive page 1:** `mcp__readwise__reader_list_documents` with `location="archive"`, `limit=50`, `response_fields=["title", "author", "category", "reading_progress", "last_opened_at", "image", "url", "site_name", "saved_at", "word_count"]`

### 2. Paginate Archive Deeply

After the first archive fetch, use `nextPageCursor` to keep fetching more pages (limit=50 each). Fetch at least 6 more pages (~350 total docs) so the heatmap covers 6 months of reading activity. Keep paginating until the oldest `last_opened_at` is 6+ months ago OR pages are exhausted.

### 3. Categorize

From the fetched data, build two lists:

- **Currently Reading:** Items from shortlist, later, or inbox where `reading_progress` is between 0.05 and 0.99 (started but not finished). Sort by `last_opened_at` descending.
- **Recently Read:** Items from archive where `reading_progress` > 0.9 (actually finished). Sort by `last_opened_at` descending. Group by month. Show as many months as the data covers.

Also collect ALL `last_opened_at` dates from archive items with `reading_progress > 0.9` for the heatmap.

**There is no "Up Next" section.** Only show things the user is reading or has read.

### 4. Generate HTML

Create a `now-reading/` directory in the current working directory (if it doesn't exist) and write the HTML file to `now-reading/index.html`.

**Design direction:** Warm, sepia-toned, editorial. Think personal reading log, not media dashboard.

**Fonts:** Google Fonts — Newsreader (serif, for headings) + DM Sans (sans, for body). Include via `<link>` tag.

**Color palette (CSS variables):**
```
--bg: #f6f1eb          (warm parchment background)
--surface: #ede6dc     (card/heatmap empty cell background)
--surface-hover: #e4dbd0
--border: #d9d0c4
--text: #4a4239        (main body text)
--text-muted: #8a7e72
--text-dim: #b0a597
--heading: #2c251e
--accent: #a0724a      (warm brown — progress bars, active states)
--accent-dim: rgba(160, 114, 74, 0.12)
```

**Layout:** Max-width 760px, centered. Responsive.

**Sections in order:**

1. **Header:** "What I'm reading" in Newsreader, light weight, large. Subtitle: "Powered by Readwise Reader" with accent-colored link.

2. **Currently Reading** — section label in small caps. Gallery of cards using CSS grid (`repeat(auto-fill, minmax(160px, 1fr))`) so they fill the container. Each card:
   - `aspect-ratio: 3/2`, rounded corners, hover lift effect
   - Cover image if available (`image` field). Gradient placeholder if not (hash title → hue).
   - Dark gradient overlay at bottom with white title + author
   - Progress bar at card bottom: 5px tall track (dark semi-transparent) with accent-colored fill
   - Cards link to the Reader URL

3. **Reading Activity** — GitHub-style heatmap filling full container width. Use CSS flex with `flex: 1` on weeks and cells so it stretches. Warm amber color scale (`rgba(160, 114, 74, 0.2/0.4/0.65/1.0)`). Month labels above, day-of-week labels (Mon/Wed/Fri) on left. Show 6 months.

4. **Recently Read** — Category filter pills (All, Articles, Books, Tweets, RSS, Email) with JS toggle. Then entries grouped by month (e.g., "FEBRUARY 2026" in small caps). Each entry as a row:
   - Date on left (tabular nums, muted)
   - Category emoji (📄 article, 📚 book, 🐦 tweet, 📰 rss, ✉️ email, 🎬 video, 🎙 podcast, 📑 pdf)
   - Title (linked, medium weight) + author/source (dim, smaller)

**Styling notes:**
- All CSS in a `<style>` tag with CSS variables
- Subtle page-load fade-up animation on sections
- Divider lines between sections (`1px solid var(--border)`)
- Responsive: 2-column card grid on mobile

### 5. Return

Return the absolute path to the generated HTML file and a summary: how many currently reading, how many recently read, date range of activity data.

## After Subagent Returns

1. Tell the user the file was generated and where it is
2. Offer to open it in their browser: `open now-reading/index.html`
3. Ask if they want to adjust anything
