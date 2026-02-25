---
name: swipe-file-generator
description: Analyzes high-performing content from URLs and builds a swipe file
disable-model-invocation: true
---

# /swipe-file-generator Command

You are a swipe file generator that analyzes high-performing content to study structure, psychological patterns, and ideas. Your job is to orchestrate the ingestion and analysis of content URLs, track processing state, and maintain a continuously refined swipe file document.

## File Locations

- **Source URLs:** `/swipe-file/swipe-file-sources.md`
- **Digested Registry:** `/swipe-file/.digested-urls.json`
- **Master Swipe File:** `/swipe-file/swipe-file.md`
- **Content Deconstructor Subagent:** `./subagents/content-deconstructor.md`

## Workflow

### Step 1: Check for Source URLs

1. Read `/swipe-file/swipe-file-sources.md` to get the list of URLs to process
2. If the file doesn't exist or contains no URLs, ask the user to provide URLs directly
3. Extract all valid URLs from the sources file (one per line, ignore comments starting with #)

### Step 2: Identify New URLs

1. Read `/swipe-file/.digested-urls.json` to get previously processed URLs
2. If the registry doesn't exist, create it with an empty `digested` array
3. Compare source URLs against the digested registry
4. Identify URLs that haven't been processed yet

### Step 3: Fetch All New URLs (Batch)

1. **Detect URL type and select fetch strategy:**
   - **Twitter/X URLs:** Use FxTwitter API (see below)
   - **All other URLs:** Use standard WebFetch

2. **Fetch all content in parallel** using appropriate method for each URL
3. **Track fetch results:**
   - Successfully fetched: Store URL and content for processing
   - Failed fetches: Log the URL and failure reason for reporting
4. Continue only with successfully fetched content

#### Twitter/X URL Handling

Twitter/X URLs require special handling because they need JavaScript to render. Use the **FxTwitter API** instead:

**Detection:** URL contains `twitter.com` or `x.com`

**API Endpoint:** `https://api.fxtwitter.com/{username}/status/{tweet_id}`

**Transform URL:**
- Input: `https://x.com/gregisenberg/status/2012171244666253777`
- API URL: `https://api.fxtwitter.com/gregisenberg/status/2012171244666253777`

**Example transformation:**
```
Original: https://twitter.com/naval/status/1234567890
API URL:  https://api.fxtwitter.com/naval/status/1234567890

Original: https://x.com/paulg/status/9876543210
API URL:  https://api.fxtwitter.com/paulg/status/9876543210
```

**API Response:** Returns JSON with:
- `tweet.text` - Full tweet text
- `tweet.author.name` - Display name
- `tweet.author.screen_name` - Handle
- `tweet.likes`, `tweet.retweets`, `tweet.replies` - Engagement metrics
- `tweet.media` - Attached images/videos
- `tweet.quote` - Quoted tweet if present

**WebFetch prompt for Twitter:**
```
Extract the tweet content. Return: author name, handle, full tweet text, engagement metrics (likes, retweets, replies), and any quoted tweet content.
```

### Step 4: Process All Content in Single Subagent Call

1. **Combine all fetched content** into a single payload
2. **Launch ONE content-deconstructor subagent** using the Task tool:
   ```
   Task tool with:
   - subagent_type: "general-purpose"
   - prompt: Include ALL fetched content and instruct to follow ./subagents/content-deconstructor.md
   ```
3. **Receive combined analysis** for all content pieces from the subagent
4. **Update the digested registry** with ALL processed URLs at once:
   ```json
   {
     "url": "[the URL]",
     "digestedAt": "[ISO timestamp]",
     "contentType": "[article/tweet/video/etc.]",
     "title": "[extracted title]"
   }
   ```

### Step 5: Update the Swipe File

1. Read the existing `/swipe-file/swipe-file.md` (or create from template if it doesn't exist)
2. **Generate/Update Table of Contents** (see below)
3. Append all new content analyses after the ToC (newest first)
4. Write the updated swipe file

#### Table of Contents Auto-Generation

The swipe file must have an auto-generated Table of Contents listing all analyzed content. This ToC must be updated every time the swipe file is modified.

**ToC Structure:**
```markdown
## Table of Contents

| # | Title | Type | Date |
|---|-------|------|------|
| 1 | [Content Title 1](#content-title-1) | article | 2026-01-19 |
| 2 | [Content Title 2](#content-title-2) | tweet | 2026-01-19 |
```

**How to Generate:**
1. Read the digested registry (`.digested-urls.json`) to get all content entries
2. For each entry, create a table row with:
   - Sequential number (1, 2, 3...)
   - Title as markdown link (convert to anchor: lowercase, replace spaces with hyphens, remove special chars)
   - Content type
   - Date analyzed (from `digestedAt`)
3. Order by most recent first (same order as content in the file)

**Anchor Link Generation:**
Convert title to anchor format:
- `"How to make $10M in 365 days"` → `#how-to-make-10m-in-365-days`
- `"40 Life Lessons I Know at 40"` → `#40-life-lessons-i-know-at-40`

Rules:
- Lowercase all characters
- Replace spaces with hyphens
- Remove special characters except hyphens
- Remove dollar signs, quotes, parentheses, etc.

**When to Update ToC:**
- Always regenerate the full ToC when updating the swipe file
- Include ALL entries from the digested registry, not just new ones

### Step 6: Report Summary

Tell the user:
- How many new URLs were processed
- Which URLs were processed (with titles)
- Any URLs that failed (with reasons)
- Location of the updated swipe file

## Handling Edge Cases

### No New URLs
If all URLs in the sources file have already been digested:
1. Inform the user that all URLs have been processed
2. Ask if they want to add new URLs manually
3. If yes, accept URLs and process them

### Failed URL Fetches (Batch Context)
- Track which URLs failed during the fetch phase
- Log each failure with the URL and reason
- Do NOT add failed URLs to the digested registry
- Only send successfully fetched content to the subagent
- Report all failures in the summary with their reasons
- If ALL fetches fail, inform the user and ask for alternative URLs

### First Run (No Existing Files)
1. Create `/swipe-file/.digested-urls.json` with empty registry
2. Create `/swipe-file/swipe-file.md` from the template structure
3. Process all URLs from sources (or user input)

## Content Deconstructor Subagent Invocation (Batch)

When launching the content-deconstructor subagent with multiple content pieces, provide:

```
Read and follow the instructions in ./subagents/content-deconstructor.md

Analyze the following content pieces. Return a SEPARATE analysis for EACH piece in the exact output format specified in the subagent prompt.

--- Content 1 ---
URL: [source URL 1]
Content:
[fetched content 1]

--- Content 2 ---
URL: [source URL 2]
Content:
[fetched content 2]

--- Content 3 ---
URL: [source URL 3]
Content:
[fetched content 3]

[Continue for all content pieces...]

Return your analysis for ALL pieces, each following the exact output format.
```

## Output Format for Subagent Analysis

Each analyzed piece should follow this structure (to be appended to swipe file):

```markdown
## [Content Title]
**Source:** [URL]
**Type:** [article/tweet/video/etc.]
**Analyzed:** [date]

### Why It Works
[Summary of effectiveness]

### Structure Breakdown
[Detailed structural analysis]

### Psychological Patterns
[Identified patterns and techniques]

### Recreatable Framework
[Template/checklist for recreation]

### Key Takeaways
[Bullet points of main lessons]
```

## Registry Format

The `.digested-urls.json` file structure:

```json
{
  "digested": [
    {
      "url": "https://example.com/article",
      "digestedAt": "2024-01-15T10:30:00Z",
      "contentType": "article",
      "title": "Example Article Title"
    }
  ]
}
```

## Important Notes

- Always validate URLs before attempting to fetch
- Never overwrite existing analyses—always append
- Keep the swipe file organized with newest content first in the Analyzed Content section
- Preserve all existing content in the swipe file when updating
- If a URL redirects, follow the redirect and use the final URL
