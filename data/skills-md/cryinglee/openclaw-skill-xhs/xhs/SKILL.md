---
name: xhs
description: 小红书 (Xiaohongshu/RedNote) research - search, analyze posts in depth, view images, read comments, output Chinese recommendations. Combines CLI tool usage with research methodology.
metadata: {"clawdbot":{"emoji":"📕","requires":{"bins":["rednote-mcp"]}}}
---

# 小红书 Research 📕

Research tool for Chinese user-generated content — travel, food, lifestyle, local discoveries.

## When to Use

- Travel planning and itineraries
- Restaurant/cafe/bar recommendations
- Activity and weekend planning
- Product reviews and comparisons
- Local discovery and hidden gems
- Any question where Chinese perspectives help

## Recommended Model

When spawning as a sub-agent: **Sonnet 4.5** (`model: "claude-sonnet-4-5-20250929"`)

- Fast enough for the slow XHS API calls
- Good at Chinese content understanding
- More cost-effective than Opus for research grunt work
- Opus overkill for search → synthesize workflow

---

## Context Management (Always Use)

**ALWAYS use dynamic context monitoring** — even 5 posts with images can hit 75-300k tokens.

### The Problem
- Each post with images = 15-60k tokens
- 200k context fills fast
- Context is append-only (can't "forget" within session)

### The Solution: Monitor + Checkpoint + Continue

**1. After EACH post, do two things:**

```markdown
a) Write findings to disk immediately:
   /research/{task-id}/findings/post-{n}.md

b) Check context usage:
   session_status → look for "Context: XXXk/200k (YY%)"
```

**2. When context hits 70%, STOP and checkpoint:**

```markdown
Write state file:
/research/{task-id}/state.json
{
  "processed": 15,
  "pendingUrls": ["url16", "url17", ...],
  "summaries": ["Post 1: 火塘...", ...]
}

Return to caller:
{
  "complete": false,
  "processed": 15,
  "remaining": 25,
  "statePath": "/research/{task-id}/state.json",
  "findingsDir": "/research/{task-id}/findings/"
}
```

**3. Caller spawns fresh sub-agent to continue:**
```
spawn_subagent(
  task="Continue XHS research from /research/{task-id}/state.json",
  model="claude-sonnet-4-5-20250929"
)
```

New sub-agent has fresh 200k context, reads state.json, continues from post 16.

### State File Schema

```json
{
  "taskId": "kunming-food-2026-02-01",
  "query": "昆明美食",
  "searchesCompleted": ["昆明美食", "昆明美食推荐"],  // Keywords already searched
  "processedUrls": ["url1", "url2", ...],             // Explicit URL tracking (prevents duplicates)
  "pendingUrls": ["url3", "url4", ...],               // Remaining URLs to process
  "nextPostNumber": 16,                                // Next post-XXX.md number
  "summaries": [                                       // 1-liner per post for final synthesis
    "Post 1: 火塘餐厅 | 🟢 | ¥80 | 本地人推荐",
    "Post 2: 野生菌火锅 | 🟢 | ¥120 | 菌子新鲜"
  ],
  "batchNumber": 1,
  "contextCheckpoint": "70%"
}
```

**Critical fields for handoff:**
- `processedUrls`: Prevents re-processing same post across sub-agents
- `pendingUrls`: Exact work remaining
- `nextPostNumber`: Ensures sequential file naming
- `searchesCompleted`: Prevents duplicate searches

### Workflow for Large Research

**Caller should use longer timeout:**
```
sessions_spawn(
  task="...",
  model="claude-sonnet-4-5-20250929",
  runTimeoutSeconds=1800  // 30 minutes for research tasks
)
```
Default is 600s (10 min) — too short for XHS research with slow API calls.

**Interleave search and processing** (don't collect all URLs first):
```
[XHS Sub-agent 1]
    ├── Check for state.json (none = fresh start)
    ├── Search keyword 1 → get 20 URLs
    ├── Process 5-10 posts immediately (writing each to disk)
    ├── Search keyword 2 → get more URLs (dedupe)
    ├── Process more posts
    ├── Context hits 70% → write state.json
    └── Return {complete: false, remaining: N}
```

This prevents timeout from losing all work — each post is saved as processed.

**Full continuation pattern:**
```
[Caller]
    ↓ spawn (runTimeoutSeconds=1800)
[XHS Sub-agent 1]
    ├── Search + process interleaved
    ├── Context hits 70% → write state.json
    └── Return {complete: false, remaining: 25}
    
[Caller sees incomplete]
    ↓ spawn continuation (runTimeoutSeconds=1800)
[XHS Sub-agent 2]  ← fresh 200k context!
    ├── Read state.json (has processedUrls, pendingUrls)
    ├── Continue processing + more searches if needed
    ├── Context hits 70% → write state.json
    └── Return {complete: false, remaining: 10}
    
[Caller sees incomplete]
    ↓ spawn continuation
[XHS Sub-agent 3]
    ├── Read state.json
    ├── Process remaining posts
    ├── All done → write synthesis.md
    └── Return {complete: true, synthesisPath: "..."}
```

### Output Directory Structure

```
/research/{task-id}/
├── state.json              # Checkpoint for continuation
├── findings/
│   ├── post-001.md         # Full analysis + image paths
│   ├── post-002.md
│   └── ...
├── images/
│   ├── post-001/
│   │   ├── 1.jpg
│   │   └── 2.jpg
│   └── ...
├── summaries.md            # All 1-liners (for quick scan)
└── synthesis.md            # Final output (when complete)
```

### Key Rules (ALWAYS FOLLOW)

1. **Write after EVERY post** — crash-safe, no work lost
2. **Check context after EVERY post** — use `session_status` tool
3. **Stop at 70%** — leave room for synthesis + buffer
4. **Return structured result** — caller decides next step
5. **Read all images** — they're pre-compressed (600px, q85)
6. **Skip videos** — already marked in fetch-post

⚠️ **This is not optional.** Even small research can overflow context with image-heavy posts.

---

## Scripts (Mechanical Tasks)

These scripts handle the repetitive CLI work:

| Script | Purpose |
|--------|---------|
| `bin/preflight` | Verify tool is working before research |
| `bin/search "keywords" [limit] [timeout] [sort]` | Search for posts (sort: general/newest/hot) |
| `bin/get-content "url"` | Get full note content (text only) |
| `bin/get-comments "url"` | Get comments on a note |
| `bin/get-images "url" [dir]` | Download images only |
| `bin/fetch-post "url" [cache] [retries]` | Fetch content + comments + images (with retries) |

All scripts are at `/root/clawd/skills/xhs/bin/`

### Preflight (always run first)

```bash
/root/clawd/skills/xhs/bin/preflight
```

Checks: rednote-mcp installed, cookies valid, stealth patches, test search.
**Don't proceed until preflight passes.**

### Search

```bash
/root/clawd/skills/xhs/bin/search "昆明美食推荐" [limit] [timeout] [sort]
```

Returns JSON with post results. 

**Parameters:**
| Param | Default | Description |
|-------|---------|-------------|
| keywords | (required) | Search terms in Chinese |
| limit | 10 | Max results (scroll pagination when >20) |
| timeout | 180 | Seconds before giving up |
| sort | general | Sort order (see below) |

**Sort options:**
| Value | XHS Label | When to use |
|-------|-----------|-------------|
| `general` | 综合 | **Default** — XHS algorithm balances relevance + engagement. Best for most research. |
| `newest` | 最新 | 舆情监控, breaking news, recent experiences, time-sensitive topics |
| `hot` | 最热 | Finding viral/popular posts, trending content |

**Examples:**
```bash
# Default sort (recommended for most research)
bin/search "昆明美食推荐" 20

# Recent posts first (舆情, current events)
bin/search "某品牌 评价" 20 180 newest

# Most popular posts
bin/search "网红打卡地" 15 180 hot
```

**Scroll pagination enabled** (patched): When `limit > 20`, the tool scrolls to load more results via XHS infinite scroll. Actual results depend on available content.

**For maximum coverage**, combine:
1. Higher limits (e.g., `limit=50`) to scroll for more
2. Multiple keyword variations for different result sets:
   - 香蕉攀岩, 香蕉攀岩馆, 香蕉攀岩体验, 香蕉攀岩评价
   - 昆明美食, 昆明美食推荐, 昆明必吃, 昆明本地人推荐

**Results vary by query** — popular topics may return 30-50+, niche topics fewer.

**Choosing sort order:**
- **Most research** → `general` (default). Let XHS's algorithm surface the best content.
- **舆情监控 / sentiment tracking** → `newest`. You want recent opinions, not old viral posts.
- **Trend discovery** → `hot`. See what's currently popular.

### Get Content

```bash
/root/clawd/skills/xhs/bin/get-content "FULL_URL_WITH_XSEC_TOKEN"
```

⚠️ Must use full URL with `xsec_token` from search results.

### Get Comments

```bash
/root/clawd/skills/xhs/bin/get-comments "FULL_URL_WITH_XSEC_TOKEN"
```

### Get Images

Download all images from a post to local files:

```bash
/root/clawd/skills/xhs/bin/get-images "FULL_URL" /tmp/my-images
```

### Fetch Post (Deep Dive with Images)

Fetch content, comments, and images in one call — with built-in retries:

```bash
/root/clawd/skills/xhs/bin/fetch-post "FULL_URL" /path/to/cache [max_retries]
```

**Features:**
- Retries on timeout (60s → 90s → 120s)
- Clear error reporting in JSON output
- Images cached locally, bypassing CDN protection

**Returns JSON:**
```json
{
  "success": true,
  "postId": "abc123",
  "content": { 
    "title": "...", 
    "author": "...", 
    "desc": "...", 
    "likes": "983", 
    "tags": [...],
    "postDate": "2025-09-04"  // ← Added via patch!
  },
  "comments": [{ "author": "...", "content": "...", "likes": "3" }, ...],
  "imagePaths": ["/cache/images/abc123/1.jpg", ...],
  "errors": []
}
```

**Date filtering:** Use `postDate` to filter out old posts. Skip posts older than your threshold (e.g., 6-12 months for restaurants).

**Workflow:**
```
1. fetch-post → JSON + cached images
2. Read each imagePath directly (Claude sees images natively)
3. Combine text + comments + what you see into findings
```

**Viewing images:**
```
Read("/path/to/1.jpg")  # Claude sees it directly - no special tool needed
```

Look for: visible text (addresses, prices, hours), atmosphere, food presentation, crowd levels.

---

## Research Methodology (Judgment Tasks)

This is where you think. Scripts do the fetching; you do the analyzing.

### Depth Levels

| Depth | Posts | When to Use |
|-------|-------|-------------|
| Minimum | 5+ | Quick checks, simple queries |
| Standard | 8-10 | Default for most research |
| Deep | 15+ | Complex topics, trip planning |

**Minimum is 5** — unless fewer exist. Note limited coverage if <5 results.

### Research Workflow

#### Step 0: Preflight
Run `bin/preflight`. Don't proceed until it passes.

#### Step 1: Plan Your Searches
Think: "What would a Chinese user search on 小红书?"

- Include location when relevant
- Add qualifiers: 推荐, 攻略, 测评, 探店, 打卡, 避坑
- Consider synonyms and variations
- Plan 2-3 different search angles

**Date filtering:**
Posts include `postDate` field (e.g., "2025-09-04"). **The calling agent specifies the date filter** based on research type:

| Research Type | Suggested Filter | Why |
|---------------|------------------|-----|
| 舆情监控 (sentiment) | 1-4 weeks | Only current discourse matters |
| Breaking news/events | 1-7 days | Time-critical |
| Travel planning | 6-12 months | Recent but reasonable window |
| Product reviews | 1-2 years | Longer product cycles |
| Trend analysis | Custom range | Compare specific periods |
| Historical/general | No limit | Want the full archive |

**Caller should specify** in task description, e.g.:
- "Only posts from last 30 days" (舆情)
- "Posts from 2025 or later" (travel)
- "No date filter" (general research)

**If no filter specified:** Default to 12 months (safe middle ground).

**Fallback when `postDate` is null:** Use keyword hints: `2025`, `最近`, `最新`

**Language strategy:**
| Location | Language | Example |
|----------|----------|---------|
| China | Chinese | `昆明攀岩` |
| English-named venues | Both | `Rock Tenet 昆明` |
| International | Chinese | `巴黎旅游` |

#### Step 2: Search & Scan
Run your searches. Results are **already ranked by XHS's algorithm** (relevance + engagement).

**Use judgment based on preview** — like a human deciding what to click:

Think: "Given my research goal, would this post likely contain useful information?"

| Research Type | What to prioritize |
|---------------|-------------------|
| 舆情监控 (sentiment) | Any opinion/experience, even low engagement — complaints matter! |
| Travel planning | High engagement + detailed experiences |
| Product reviews | Mix of positive AND negative reviews |
| Trend analysis | Variety of perspectives |

| Preview Signal | Action |
|----------------|--------|
| Relevant content in preview | ✅ Fetch |
| Matches research goal | ✅ Fetch |
| Low engagement but relevant opinion | ✅ Fetch (esp. for 舆情) |
| High engagement but off-topic | ❌ Skip |
| Official announcements only | ⚠️ Context-dependent |
| 广告/合作 markers | ⚠️ Note as sponsored if fetching |
| Clearly off-topic | ❌ Skip |
| Duplicate content | ❌ Skip |

**Key insight:** For 舆情监控, a 3-like complaint post may be more valuable than a 500-like promotional post. Engagement ≠ relevance for all research types.

#### Step 3: Deep Dive Each Post

For each selected post, use `fetch-post` to get everything:

```bash
bin/fetch-post "url_from_search" {{RESEARCH_DIR}}/xhs
```

Returns JSON with content, comments, and cached images. Has built-in retries. Then:

**A. Review content**
- Extract key facts from title/description
- Note author's perspective/bias
- Check tags for categorization

**B. View images** (critical!)
For each `imagePath` in the result, just read it:
```
Read("/path/to/1.jpg")  # You see it directly
```
- Look for text overlays: addresses, prices, hours
- Note visual details: ambiance, crowd levels, food presentation

**⚠️ Don't describe images in isolation.** Synthesize what you see with the post content and comments to form a holistic view. An image of a crowded restaurant + author saying "周末排队1小时" + comments confirming "人超多" = that's your finding about crowds.

**C. Review comments** (gold for updates)
- "已经关门了" = already closed
- Real experiences vs sponsored hype
- Tips not in main post

**D. Return picked images**
Include paths to the best/most informative images in your findings. The calling agent decides whether and how to use them (embed in reports, reference, etc.). You're curating — pick images that show something useful (venue exterior, menu with prices, actual food, atmosphere) not just decorative shots.

#### Step 4: Synthesize

- What do multiple sources agree on?
- Any contradictions?
- What's the overall consensus?
- What would you actually recommend?

#### Step 5: Output

**Facts + Flavor** — structured findings that preserve the XHS voice.

```markdown
## XHS Research: [Topic]

### Search Summary
| Search | Results | Notes |
|--------|---------|-------|
| 昆明攀岩 | 10 | Good coverage |

### Findings

#### [Venue Name] (中文名)
- **Type:** Restaurant / Activity / Attraction
- **Address:** [from post or image]
- **Price:** ¥XX/person
- **Hours:** [if found]
- **The vibe:** [atmosphere, energy — preserved voice]
- **Why people like it:** [opinions, impressions]
- **Watch out for:** [warnings from comments]
- **Source:** [full URL]
- **Engagement:** X likes
- **Images:** [paths for calling agent to use]
  - `/path/to/1.jpg` — exterior/entrance
  - `/path/to/3.jpg` — menu with prices

> "引用原文..." — @username

### Overall Impressions
- Consensus across posts
- Patterns in preferences
- Things only locals know
- Disagreements worth noting
```

**The XHS value is the human perspective.** A recommendation that says "环境一般但是味道绝了" tells you more than "Rating: 4.2/5".

Think: "What would a friend who just spent an hour on XHS tell me?"

---

## Quality Signals

**Trustworthy:**
- 100+ likes with real comments
- Detailed personal experience
- Multiple photos from actual visit
- Specific details (prices, hours)
- Recent posts (look for date mentions in content: "上周", "昨天", "2025年X月")
- Year in title (e.g., "2025上海咖啡必喝榜")

**Checking recency:**
- Look for dates in post text/title
- Check if prices seem current
- Comments mentioning "还在吗" or "现在还有吗" = might be outdated
- Comments with recent dates confirm post is still relevant

**Suspicious:**
- 广告/合作/赞助 markers
- Overly positive, no specifics
- Stock photos only
- No comments or generic ones
- Very old posts

---

## Timing & Efficiency

### XHS is SLOW — Plan Accordingly

The rednote-mcp CLI is slow (30-90s per search). Don't rapid-fire poll.

**When running searches via `exec`:**
```bash
# GOOD: Give it time to complete
exec(command, yieldMs: 60000)  # Wait 60s before checking
process(poll)  # Then poll every 30s if still running
```

**DON'T:**
- Poll every 2-3 seconds (wastes tokens, no benefit)
- Start multiple searches simultaneously (overloads)
- Wait indefinitely without writing partial results

### Write Incrementally

Don't wait until you've analyzed everything to start writing. After each batch of 3-5 posts:
- Append findings to your output file
- This protects against timeout/termination losing all work

```markdown
## Findings (in progress)

### Batch 1: 美食搜索 (3 posts analyzed)
[findings...]

### Batch 2: 攻略搜索 (analyzing...)
```

### Time Budget Awareness

If you've been running 15+ minutes:
- Prioritize writing what you have
- Note incomplete searches in output
- Better to deliver 80% findings than lose 100% to termination

## Retry Pattern

rednote-mcp is slow. If a command times out:

```
Attempt 1: default timeout
Attempt 2: +60s
Attempt 3: +120s
```

If all fail, **report the failure**. Do NOT fall back to web_search — defeats the purpose.

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Timeout | Network/XHS slow | Retry with longer timeout |
| Login/cookie error | Session expired | `xvfb-run -a rednote-mcp init` |
| 404 / xsec_token | Missing token | Use full URL from search |
| Empty results | No posts | Try different keywords |

---

## Setup & Maintenance

### First-Time Setup
```bash
npm install -g rednote-mcp
npx playwright install
/root/clawd/skills/xhs/patches/apply-all.sh
xvfb-run -a rednote-mcp init
```

### Re-login (when cookies expire)
```bash
xvfb-run -a rednote-mcp init
```

### After rednote-mcp updates
```bash
/root/clawd/skills/xhs/patches/apply-all.sh
```

---

## Role Clarification

**This skill** = Research tool that outputs structured findings
**Calling agent** = Synthesizes XHS + other sources into final reports, decides which images to embed

**You return:**
- Synthesized findings (text + images + comments → holistic view)
- Curated image paths (calling agent decides how to use them)
- Preserved human voice (opinions, vibes, tips)

**You don't:**
- Describe images in isolation ("I see a restaurant...")
- Generate final reports (that's the caller's job)
- Decide image layout/placement

XHS is like having a Chinese-speaking friend spend an hour researching for you. They'd give you facts, but also opinions, vibes, and insider tips. That's what you're capturing.

---

**Remember:** Research like a curious human. Explore, cross-reference, look at pictures, read comments. The "这家真的绝了" matters as much as the address.
