---
name: decodo-scraper
description: Search Google, scrape web pages, Amazon product pages, YouTube subtitles, or Reddit (post/subreddit) using the Decodo Scraper OpenClaw Skill.
homepage: https://decodo.com
credentials:
  - DECODO_AUTH_TOKEN
env:
  required:
    - DECODO_AUTH_TOKEN
---

# Decodo Scraper OpenClaw Skill

Use this skill to search Google, scrape any URL, or fetch YouTube subtitles via the [Decodo Web Scraping API](https://help.decodo.com/docs/web-scraping-api-google-search). **Search** outputs a JSON object of result sections; **Scrape URL** outputs plain markdown; **Amazon** and **Amazon search** output parsed product-page or search results (JSON). Amazon search uses `--query`. **YouTube subtitles** outputs transcript/subtitles. **Reddit post** and **Reddit subreddit** output post/listing content (JSON).

**Authentication:** Set `DECODO_AUTH_TOKEN` (Basic auth token from Decodo Dashboard → Scraping APIs) in your environment or in a `.env` file in the repo root.

**Errors:** On failure the script writes a JSON error to stderr and exits with code 1.

---

## Tools

### 1. Search Google

Use this to find URLs, answers, or structured search results. The API returns a JSON object whose `results` key contains several sections (not all may be present for every query):

| Section | Description |
|--------|--------------|
| `organic` | Main search results (titles, links, snippets). |
| `ai_overviews` | AI-generated overviews or summaries when Google shows them. |
| `paid` | Paid/sponsored results (ads). |
| `related_questions` | “People also ask”–style questions and answers. |
| `related_searches` | Suggested related search queries. |
| `discussions_and_forums` | Forum or discussion results (e.g. Reddit, Stack Exchange). |

The script outputs only the inner `results` object (these sections); pagination info (`page`, `last_visible_page`, `parse_status_code`) is not included.

**Command:**
```bash
python3 tools/scrape.py --target google_search --query "your search query"
```

**Examples:**
```bash
python3 tools/scrape.py --target google_search --query "best laptops 2025"
python3 tools/scrape.py --target google_search --query "python requests tutorial"
```

Optional: `--geo us` or `--locale en` for location/language.

---

### 2. Scrape URL

Use this to get the content of a specific web page. By default the API returns content as **Markdown** (cleaner for LLMs and lower token usage).

**Command:**
```bash
python3 tools/scrape.py --target universal --url "https://example.com"
```

**Examples:**
```bash
python3 tools/scrape.py --target universal --url "https://example.com"
python3 tools/scrape.py --target universal --url "https://news.ycombinator.com/"
```

---

### 3. Amazon product page

Use this to get parsed data from an Amazon product (or other Amazon) page. Pass the product page URL as `--url`. The script sends `parse: true` and outputs the inner **results** object (e.g. `ads`, product details, etc.).

**Command:**
```bash
python3 tools/scrape.py --target amazon --url "https://www.amazon.com/dp/PRODUCT_ID"
```

**Examples:**
```bash
python3 tools/scrape.py --target amazon --url "https://www.amazon.com/dp/B09H74FXNW"
```

---

### 4. Amazon search

Use this to search Amazon and get parsed results (search results list, delivery_postcode, etc.). Pass the search query as `--query`.

**Command:**
```bash
python3 tools/scrape.py --target amazon_search --query "your search query"
```

**Examples:**
```bash
python3 tools/scrape.py --target amazon_search --query "laptop"
```

---

### 5. YouTube subtitles

Use this to get subtitles/transcript for a YouTube video. Pass the **video ID** (e.g. from `youtube.com/watch?v=VIDEO_ID`) as `--query`.

**Command:**
```bash
python3 tools/scrape.py --target youtube_subtitles --query "VIDEO_ID"
```

**Examples:**
```bash
python3 tools/scrape.py --target youtube_subtitles --query "dFu9aKJoqGg"
```

---

### 6. Reddit post

Use this to get the content of a Reddit post (thread). Pass the full post URL as `--url`.

**Command:**
```bash
python3 tools/scrape.py --target reddit_post --url "https://www.reddit.com/r/SUBREDDIT/comments/ID/..."
```

**Examples:**
```bash
python3 tools/scrape.py --target reddit_post --url "https://www.reddit.com/r/nba/comments/17jrqc5/serious_next_day_thread_postgame_discussion/"
```

---

### 7. Reddit subreddit

Use this to get the listing (posts) of a Reddit subreddit. Pass the subreddit URL as `--url`.

**Command:**
```bash
python3 tools/scrape.py --target reddit_subreddit --url "https://www.reddit.com/r/SUBREDDIT/"
```

**Examples:**
```bash
python3 tools/scrape.py --target reddit_subreddit --url "https://www.reddit.com/r/nba/"
```

---

## Summary

| Action             | Target               | Argument   | Example command |
|--------------------|----------------------|------------|-----------------|
| Search             | `google_search`      | `--query`  | `python3 tools/scrape.py --target google_search --query "laptop"` |
| Scrape page        | `universal`          | `--url`    | `python3 tools/scrape.py --target universal --url "https://example.com"` |
| Amazon product     | `amazon`             | `--url`    | `python3 tools/scrape.py --target amazon --url "https://www.amazon.com/dp/B09H74FXNW"` |
| Amazon search      | `amazon_search`     | `--query`  | `python3 tools/scrape.py --target amazon_search --query "laptop"` |
| YouTube subtitles  | `youtube_subtitles`  | `--query`  | `python3 tools/scrape.py --target youtube_subtitles --query "dFu9aKJoqGg"` |
| Reddit post        | `reddit_post`        | `--url`    | `python3 tools/scrape.py --target reddit_post --url "https://www.reddit.com/r/nba/comments/17jrqc5/..."` |
| Reddit subreddit   | `reddit_subreddit`   | `--url`    | `python3 tools/scrape.py --target reddit_subreddit --url "https://www.reddit.com/r/nba/"` |

**Output:** Search → JSON (sections). Scrape URL → markdown. Amazon / Amazon search → JSON (results e.g. ads, product info, delivery_postcode). YouTube → transcript. Reddit → JSON (content).
