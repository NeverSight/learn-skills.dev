---
name: google-news-seo
description: Google News Diagnostic Engine — audit and optimize news articles for Google News SEO. Determines Layer 1 index eligibility and Layer 2 ranking competitiveness. Includes NewsArticle Schema review, AI content compliance checks, publisher trust detection, author authority scoring, freshness analysis, topic cluster compatibility, Top Stories detection, competitor gap analysis, and Google E-E-A-T scanning with structured report generation. Use when asked about Google News SEO, why a site is not indexed in Google News, why articles don't rank, NewsArticle Schema optimization, how AI content can get into Google News, or running an EEAT scan / audit. 检查和优化新闻文章的 Google News SEO，包括双层诊断引擎（Layer 1 索引准入 / Layer 2 排名竞争）、NewsArticle Schema 审查与修复、AI 生成内容合规性检查、发布者信任度检测、作者权威性评分、新鲜度分析、话题聚类兼容性、Top Stories 检测、竞争对手差距分析，以及 Google E-E-A-T 全维度扫描。
---

# Google News SEO Diagnostic Engine

> **Language / 语言**：Detect the user's language and respond in the same language throughout.
> 用户用中文提问则全程用中文回复；用英文提问则全程用英文回复。

---

## Google News System Model

Google News operates on a **two-layer architecture**. This skill evaluates both layers independently.

| Layer | Name | Function |
|-------|------|----------|
| **Layer 1** | News Index System | Determines whether a site enters the Google News index |
| **Layer 2** | News Ranking System | Determines whether articles rank in topic clusters and appear in Top Stories |

**Layer 1 must pass before Layer 2 matters.** If a site is not indexed, ranking optimization is premature.

Diagnostic routing:
- **Layer 1 fails** → focus on index eligibility (publisher trust, crawlability, Schema, sitemap)
- **Layer 1 passes, Layer 2 fails** → focus on ranking signals (freshness, content type, cluster compatibility, competitors)
- **Both pass** → surface remaining optimization opportunities via competitor gap analysis

---

## 0 · Initial Assessment 审计前评估

Before starting any checks, gather context by asking the following questions. **Skip any question already answered in the user's prompt.**

| # | Question / 问题 |
|---|----------------|
| 1 | **Site type / 站点类型** — Is this a dedicated news publisher, a corporate blog with a news section, or another site type? |
| 2 | **Target topics / keywords / 目标关键词或议题** — Which topics, keywords, or named entities are most important for this audit? |
| 3 | **Current status / 当前状态** — Any known issues, recent migrations, or Google Search Console alerts? |
| 4 | **Scope / 审计范围** — Full Google News Diagnostic (Layer 1 + Layer 2 + Competitor Analysis), article-level audit, or a specific area (Schema only / EEAT only / Technical only / On-Page only)? |

**Skip rule / 跳过规则：** If the user's prompt already implies answers (e.g., provides a URL + says "check the Schema"), skip the answered questions and proceed directly.

**Full Diagnostic trigger / 全站诊断触发：** If scope is "Full Diagnostic" or the user asks "why is my site not in Google News" / "why don't my articles rank" / "why do competitors outrank me", run all Layer 1 + Layer 2 checks and generate the Google News Diagnostic Report (Section 10).

**Acknowledgement / 确认语句：** Before starting checks, output one line:
```
Auditing [URL / article / site] — scope: [scope summary]. Starting checks...
```

---

## 0.5 · News Index Presence Detection 索引存在检测

> **Run this check first when performing a Full Diagnostic or when the user asks why their site is not appearing in Google News.**

### Step 1 — Simulate Google News index query

Use WebSearch to simulate a `site:<domain>` query in a Google News context. Construct the search as:
```
site:<domain> news articles
```
Analyze the returned results to determine whether the site's articles appear in Google News coverage.

### Step 2 — Classify index presence

| Result | Status | Definition |
|--------|--------|------------|
| 0 results detected | **Not Indexed** | No evidence of Google News indexing |
| 1–5 results | **Limited Presence** | Some articles indexed; inconsistent coverage |
| 6+ results across multiple days | **Strong Presence** | Active Google News publisher |

Also record:
- Total detected article count
- Timestamp of the most recently indexed article
- Whether results span multiple days/topics (diversity indicator)

### Step 3 — Route diagnostic focus

| Index Status | Diagnostic Focus |
|-------------|-----------------|
| Not Indexed | Prioritize Layer 1 checks; flag as root cause category |
| Limited Presence | Run both Layer 1 and Layer 2; present findings for each |
| Strong Presence | Note Layer 1 as passing; focus diagnostic output on Layer 2 ranking checks |

### Output format

```
News Index Status: [Not Indexed ❌ / Limited Presence ⚠️ / Strong Presence ✅]
Detected article count: [N]
Latest indexed article: [timestamp or "not detected"]
Diagnostic focus: [Layer 1 / Both Layers / Layer 2]
```

---

## 1 · Prerequisites 前置要求

**Determine input type first / 先判断产物类型：**

| Input | Action |
|-------|--------|
| Live URL / 线上 URL | Fetch page, extract JSON-LD Schema |
| Raw Schema JSON | Parse directly |
| URL or HTML + EEAT scan request / URL 或 HTML + EEAT 扫描请求 | Run full E-E-A-T analysis → see Sections 7–9 / 执行 EEAT 全维度分析 → 见第 7–9 节 |

### Schema Fetch Protocol / Schema 获取流程

Retrieve JSON-LD in three sequential phases. Only advance to the next phase if the current one yields no JSON-LD blocks.

> ⚠️ **Anti-pattern — do NOT do this:**
> Do NOT report "JSON-LD 无法通过抓取自动提取（前端渲染）" or "client-side rendered" based solely on a failed `web_fetch`. SSR/SSG sites (Next.js, Nuxt, Hugo, WordPress) pre-render JSON-LD into static HTML — `curl` can fetch it directly. A fetch failure alone is **not** evidence of CSR.

---

**Phase 1 — web_fetch（优先）**

Use `web_fetch` to retrieve the page. If the response contains one or more `<script type="application/ld+json">` blocks → extract and proceed to Schema analysis. **Stop here.**

---

**Phase 2 — curl fallback（web_fetch 无结果时）**

> **Note**: Attempting curl fallback — SSR/SSG sites pre-render JSON-LD into static HTML; curl can retrieve it directly without JS execution.

If Shell tool is unavailable, skip directly to Phase 3.

```bash
# Step A: fetch raw HTML with Googlebot UA
# Note: macOS mktemp doesn't support extensions; use a plain suffix
TMPFILE=$(mktemp /tmp/page_XXXXXX)
curl -sL \
  -H "User-Agent: Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" \
  --max-time 15 \
  "<URL>" > "$TMPFILE" 2>&1
echo "File size: $(wc -c < "$TMPFILE") bytes"
```

- **403 / 429**: retry once with Chrome UA:
  `-H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"`
- **Timeout / non-zero exit / file size 0**: skip to Phase 3

```bash
# Step B: extract JSON-LD — write Python script via heredoc to avoid quoting issues
cat > /tmp/extract_jsonld.py << 'PYEOF'
import re, json
html = open('/tmp/page_XXXXXX.html').read()  # replace XXXXXX with actual suffix from $TMPFILE
pattern = re.compile(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.DOTALL | re.IGNORECASE)
blocks = pattern.findall(html)
print(f'Total blocks found: {len(blocks)}')
for i, b in enumerate(blocks, 1):
    print(f'=== JSON-LD Block {i} ===')
    try:
        print(json.dumps(json.loads(b.strip()), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f'Parse error: {e}')
        print(b.strip()[:500])
PYEOF
# Replace the filename placeholder with the actual $TMPFILE path, then run:
sed -i '' "s|/tmp/page_XXXXXX.html|$TMPFILE|g" /tmp/extract_jsonld.py
python3 /tmp/extract_jsonld.py
```

```bash
# Step B fallback — grep (if Python 3 unavailable)
grep -oE '<script[^>]+type="application/ld\+json"[^>]*>.*?</script>' "$TMPFILE" | sed 's/<[^>]*>//g'
```

```bash
# Step C: clean up
rm -f "$TMPFILE" /tmp/extract_jsonld.py
```

If extraction returns results → use for Schema analysis; note **"Schema retrieved via curl fallback"**.

- **Multiple blocks**: extract all; use the block with `"@type": "NewsArticle"` for Schema analysis
- **Malformed JSON**: output raw block, flag as "partially retrievable", continue best-effort analysis

---

**Phase 3 — 🔍 Manual（仅在两阶段均无结果时）**

Mark Schema detection as 🔍 Manual. Output exactly:

```
Schema could not be auto-detected (web_fetch and curl both returned no JSON-LD).
Verify manually: 🔗 https://search.google.com/test/rich-results?url=<URL>
```

❌ Do NOT say: "前端渲染" / "client-side rendering" / "JavaScript-rendered"
✅ Only say: "could not be auto-detected"

---

**3 hard requirements for Google News inclusion / 三项硬性门槛：**

1. **Dedicated news publisher / 专属新闻网站** — the site's core purpose must be news, not a product with a news section
2. **Content policy compliance / 内容政策合规** — no dangerous / deceptive / manipulated-media content; AI-generated content must be transparently disclosed
3. **Technical compliance / 技术合规** — permanent URLs, HTML-rendered content, `robots.txt` must not block Googlebot-News

---

## 1.5 · Publisher Trust Detection 发布者信任度检测

> **Layer 1 check.** Google evaluates whether the site operates as a legitimate news publisher before indexing it.

### Step 1 — Verify trust pages

Use WebFetch to check each URL. A page passes if it returns HTTP 200 with non-trivial content (not a redirect to homepage).

| Page | URL pattern | Points |
|------|-------------|--------|
| About | `<domain>/about` | 8 pts |
| Editorial Policy | `<domain>/editorial-policy` | 8 pts |
| Contact | `<domain>/contact` | 8 pts |
| Team | `<domain>/team` | 8 pts |
| Authors | `<domain>/authors` | 8 pts |

**Subtotal (pages): 40 pts**

### Step 2 — Detect newsroom description

Scan the About page text for presence of keywords indicating a professional newsroom:
`newsroom` · `editorial team` · `journalism` · `reporters` · `editor-in-chief` · `press` · `media organization`

- Keywords present → **30 pts**
- Absent → **0 pts**, flag as P1: "No editorial identity statement found on About page"

### Step 3 — Detect Organization Schema

Check homepage and About page JSON-LD for `@type: Organization` or `@type: NewsMediaOrganization` with fields: `name`, `url`, `logo`.

| Condition | Points |
|-----------|--------|
| All three fields present | 30 pts |
| 1–2 fields present | 15 pts |
| Schema absent | 0 pts |

### Publisher Trust Score Output

```
Publisher Trust Score: [0-100]

| Check | Result | Notes |
|-------|--------|-------|
| /about | Pass ✅ / Fail ❌ | |
| /editorial-policy | Pass ✅ / Fail ❌ | |
| /contact | Pass ✅ / Fail ❌ | |
| /team | Pass ✅ / Fail ❌ | |
| /authors | Pass ✅ / Fail ❌ | |
| Newsroom description | Pass ✅ / Fail ❌ | |
| Organization Schema | Pass ✅ / Partial ⚠️ / Fail ❌ | [missing fields] |
```

---

## 1.6 · Author Authority Detection 作者权威性检测

> **Layer 1 check.** Google builds an author credibility graph. Unverifiable or AI-generated author attribution is a strong negative signal.

### Step 1 — Verify author presence and schema match

Check both:
1. Visible byline on the page (author name in HTML)
2. `author.name` in NewsArticle Schema

| Condition | Result |
|-----------|--------|
| Both present and matching | Pass ✅ — 30 pts |
| Schema author missing | Fail ❌ — 0 pts (P1) |
| Mismatch between Schema and page byline | Fail ❌ — 0 pts (P0) |

### Step 2 — Fetch author profile page

Use WebFetch on the URL from `author.url` (Schema) or the byline hyperlink.

A complete author profile requires:
- Author name visible
- Biography ≥ 50 words
- At least one of: job title, social media link, publication count

| Condition | Points |
|-----------|--------|
| Full profile (name + bio 50w+ + credential) | 40 pts |
| Partial profile (name + bio only) | 20 pts |
| Profile missing or 404 | 0 pts (P1) |

### Step 3 — Detect suspicious AI author names

Scan `author.name` (Schema) and page byline for:
> `AI Agent` · `Bot` · `System Writer` · `Auto Writer` · `AI Writer` · `GPT` · `Claude` · `Gemini`

- Match detected → flag as **P0**: "Suspicious AI author name detected — replace with human editor name" *(mark as needs human confirmation)*
- No match → **10 pts**

### Step 4 — Detect social / credential signals

Check author profile for: Twitter/X link, LinkedIn link, professional email, years of experience mentioned in bio, or domain expertise statement.

- 1+ signals present → **20 pts**
- No signals → **0 pts**

### Author Authority Score Output

```
Author Authority Score: [0-100]

| Check | Result | Notes |
|-------|--------|-------|
| Author byline present | Pass ✅ / Fail ❌ | |
| Schema author.name matches byline | Pass ✅ / Mismatch ⚠️ / Fail ❌ | |
| Author profile page | Full ✅ / Partial ⚠️ / Missing ❌ | |
| No suspicious AI name | Pass ✅ / Flag ❌ | [matched keyword if flagged] |
| Social / credential signal | Present ✅ / Absent ⚠️ | |
```

---

## 2 · NewsArticle Schema Checklist Schema 审查清单

### Critical — affects indexing / 必检项（影响收录）

```
- [ ] @context = "https://schema.org"  (not http://)
- [ ] @type = "NewsArticle"  (matches actual content type)
- [ ] dateModified >= datePublished  (must not be earlier)
- [ ] image URL contains no AI-tool markers  (qwen_generated / ChatGPT Image / dall-e / midjourney)
- [ ] author.name matches the byline shown on the page  (Schema ≠ AI agent while page shows human)
- [ ] author is a real person with a verifiable author page  (not a team name or AI Agent)
- [ ] publisher.logo exists and is a valid ImageObject
```

### Recommended — affects rich results / 建议补充项（影响富摘要）

```
- [ ] mainEntityOfPage points to the article URL
- [ ] description field present  (populated from article summary)
- [ ] articleSection set
- [ ] BreadcrumbList last item has an "item" URL
```

---

## 3 · AI Content Checks AI 内容专项

| Issue / 问题 | Risk / 风险 | Fix / 修复 |
|---|---|---|
| Image filename contains AI tool name | Manipulated media policy violation | Rename on upload; strip AI-tool prefixes |
| Schema `author` ≠ page byline | Deceptive markup | Use the same real editor name in both |
| No human editor byline | Insufficient E-E-A-T | Establish human editorial attribution |
| AI Agent listed as `author` | Unverifiable authority | Replace with the reviewing editor |

**Recommended attribution pattern for AI content / AI 内容推荐署名模式：**
- Schema `author` → real editor's `Person` node
- Page display → "Generated by AI, reviewed by [Editor Name]" / "AI 生成，经 [编辑姓名] 审校"
- Editor's author page must include: real name, professional bio, contact

---

## 4 · Schema Fix Template 修复模板

```json
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/news/article-slug/"
  },
  "headline": "Article title / 文章标题",
  "description": "100-200 char summary / 文章摘要",
  "datePublished": "2026-03-03T19:55:26-05:00",
  "dateModified": "2026-03-03T20:10:00-05:00",
  "image": ["https://cdn.example.com/images/article-cover.jpg"],
  "author": [{
    "@type": "Person",
    "name": "Editor Name / 编辑姓名",
    "url": "https://example.com/author/editor-slug/",
    "jobTitle": "Senior Editor"
  }],
  "publisher": {
    "@type": "Organization",
    "name": "Publication Name",
    "url": "https://example.com",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png",
      "width": 600,
      "height": 60
    }
  },
  "articleSection": "Markets",
  "isAccessibleForFree": true
}
```

---

## 5 · Systemic Bugs 系统性 Bug（批量修复）

If the same issue appears across multiple articles, fix at the template level.
若多篇文章存在相同问题，需从模板层修复，不要逐篇处理。

| Bug | Root cause / 根因 | Fix / 修复 |
|-----|-------------------|-----------|
| `dateModified` < `datePublished` | Field assignment order / 赋值顺序错误 | Set `modified` to last-edited timestamp |
| `"http://schema.org"` | Hardcoded old protocol / 模板写死旧协议 | Global replace → `"https://schema.org"` |
| `publisher.logo` missing | Not in template / 模板缺字段 | Add `logo` ImageObject to Schema template |
| `description` missing | Not mapped from summary / 未映射摘要 | Auto-populate from `summary` / `excerpt` |
| BreadcrumbList last item has no `item` | Template omission / 模板漏写 | Set last item's `item` = article URL |
| AI-tool name in image filename | No rename on upload / 上传未重命名 | Strip AI-tool prefixes in upload pipeline |

---

## 5.5 · Technical SEO 技术检查

| Check / 检查项 | Pass Condition / 通过条件 | Priority | Auto / Manual |
|---------------|--------------------------|----------|---------------|
| robots.txt accessible | `<domain>/robots.txt` returns HTTP 200 | P1 | Auto |
| Googlebot-News not blocked | No `Disallow` rule under `User-agent: Googlebot-News` covering the article path | P0 | Auto |
| News Sitemap exists | Sitemap URL (from robots.txt or `<domain>/news-sitemap.xml`) is accessible and contains `<news:news>` tags | P1 | Auto |
| News Sitemap has `<news:news>` tags | Sitemap is valid per Google News Sitemap spec | P1 | Auto |
| News Sitemap freshness | At least one `<news:publication_date>` within the last 48 hours | P1 | Auto |
| News Sitemap Health Score | accessible (30 pts) + valid news namespace (40 pts) + 48h freshness (30 pts) | — | Auto |
| Crawlability Score | article text in HTML (30 pts) + server-rendered Schema (30 pts) + canonical valid (20 pts) + robots not blocking (20 pts) | — | Auto |
| Core Web Vitals — LCP | LCP < 2.5s (Good); 2.5–4s (Needs Improvement ⚠️); > 4s (Poor ❌) | P1 | 🔍 Manual |
| Core Web Vitals — INP | INP < 200ms (Good); 200–500ms (⚠️); > 500ms (❌) | P1 | 🔍 Manual |
| Core Web Vitals — CLS | CLS < 0.1 (Good); 0.1–0.25 (⚠️); > 0.25 (❌) | P1 | 🔍 Manual |
| HTTPS | Article URL uses `https://` | P0 | Auto |

**CWV verification / CWV 验证：** Use PageSpeed Insights: `https://pagespeed.web.dev/report?url=<url>`

**News Sitemap Health Score calculation:**
```
Score = (accessible ? 30 : 0) + (news namespace valid ? 40 : 0) + (article within 48h ? 30 : 0)
```

---

## 5.6 · On-Page SEO 文章页检查

### Title Tag / 标题标签

| Check | Pass Condition | Priority |
|-------|---------------|----------|
| Title tag present | `<title>` element exists and is non-empty | P0 |
| Length 50–70 characters | Title length between 50 and 70 characters | P1 |
| Primary keyword near start | Key topic/entity within the first 60 characters | P1 |
| Unique (not duplicated) | Title is not identical to other pages (🔍 Manual) | P1 |
| No keyword stuffing | Same keyword not repeated > 2 times | P2 |

### Meta Description

| Check | Pass Condition | Priority |
|-------|---------------|----------|
| Meta description present | `<meta name="description">` exists and non-empty | P1 |
| Length 120–160 characters | Description length between 120 and 160 characters | P2 |
| Contains primary keyword | Primary topic/entity appears in description | P2 |

### Canonical Tag

| Check | Pass Condition | Priority |
|-------|---------------|----------|
| Canonical tag present | `<link rel="canonical">` exists | P1 |
| Points to correct URL | Canonical URL matches the article URL (self-referencing) or a valid canonical version | P1 / P0 if target returns non-200 |

### Heading Structure

| Check | Pass Condition | Priority |
|-------|---------------|----------|
| Exactly one H1 | Page contains exactly one `<h1>` element | P1 |
| H1 matches headline | H1 text consistent with article headline | P1 |
| Logical hierarchy | No heading levels skipped (e.g., no H1 → H3 without H2) | P2 |
| H1 contains primary keyword | Primary topic/entity appears in H1 | P2 |

---

## 5.7 · Crawlability and Rendering Check 爬取与渲染检测

> **Layer 1 check.** Verifies that Googlebot can access and read the article content without JavaScript execution.

### Step 1 — Fetch with Googlebot UA

```bash
TMPFILE=$(mktemp /tmp/crawl_XXXXXX)
curl -sL \
  -H "User-Agent: Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" \
  --max-time 15 \
  "<ARTICLE_URL>" > "$TMPFILE" 2>&1
echo "File size: $(wc -c < "$TMPFILE") bytes"
```

### Step 2 — Detect article body in initial HTML

```bash
cat > /tmp/check_body.py << 'PYEOF'
import re
html = open('TMPFILE_PATH').read()
clean = re.sub(r'<(script|style)[^>]*>.*?</(script|style)>', '', html, flags=re.DOTALL|re.IGNORECASE)
clean = re.sub(r'<[^>]+>', ' ', clean)
clean = re.sub(r'\s+', ' ', clean).strip()
print(f"Visible text length: {len(clean)} chars")
print(f"First 300 chars: {clean[:300]}")
PYEOF
sed -i '' "s|TMPFILE_PATH|$TMPFILE|g" /tmp/check_body.py
python3 /tmp/check_body.py
```

- ≥ 200 chars of visible text → **article text present** → 30 pts
- < 200 chars → flag: "Article text not detected in initial HTML — recommend verifying with [Rich Results Test](https://search.google.com/test/rich-results)"

> ❌ Do NOT label as "client-side rendered" — only say "article text not detected in initial HTML"

### Step 3 — Detect server-rendered Schema

Check whether raw HTML contains `<script type="application/ld+json">` with `"@type": "NewsArticle"` before any dynamically loaded bundles.

| Result | Points | Note |
|--------|--------|------|
| NewsArticle Schema in raw HTML | 30 pts | Server-rendered ✅ |
| JSON-LD found but no NewsArticle type | 15 pts | Partial |
| No JSON-LD in raw HTML | 0 pts | Flag: "Potential hydration-only Schema — verify Next.js/Nuxt SSR is configured to pre-render Schema (use `getServerSideProps` or static export)" |

### Step 4 — Verify canonical and robots

- Canonical tag present and pointing to article URL → **20 pts**
- Not blocked by robots.txt for Googlebot or Googlebot-News → **20 pts**

### Crawlability Score Output

```
Crawlability Score: [0-100]

| Check | Result | Points | Notes |
|-------|--------|--------|-------|
| Article text in initial HTML | Pass ✅ / Fail ❌ | 30 / 0 | |
| Server-rendered Schema | Full ✅ / Partial ⚠️ / Absent ❌ | 30/15/0 | |
| Canonical tag valid | Pass ✅ / Fail ❌ | 20 / 0 | |
| Not blocked by robots | Pass ✅ / Fail ❌ | 20 / 0 | |
```

---

## 5.8 · URL Structure Analysis URL 结构分析

> **Layer 1 check.** URL patterns affect Googlebot's ability to recognize and categorize news content.

### Recommended patterns ✅

- `/news/<descriptive-slug>`
- `/article/<descriptive-slug>`
- `/<year>/<month>/<descriptive-slug>`
- `/<category>/<descriptive-slug>`

### Problematic patterns ❌

| Pattern | Example | Priority | Recommendation |
|---------|---------|----------|----------------|
| Query-parameter article ID | `?id=123`, `?article_id=456`, `?p=789`, `?postid=1` | P1 | Migrate to path-based URL; implement 301 redirect |
| Numeric-only slug | `/news/12345` (no keywords) | P2 | Add descriptive keywords to URL slug |
| Session ID in URL | `?session=abc`, `?PHPSESSID=` | P0 | Remove session parameters from indexable URLs |
| Tracking params without canonical | `?utm_source=` without self-referencing canonical | P1 | Ensure canonical points to clean URL |

### Output

```
URL Structure: [Recommended ✅ / Needs Improvement ⚠️ / Problematic ❌]
Detected pattern: [pattern description]
Issues found: [list or "None"]
```

---

## 5.9 · Freshness Signal Analysis 新鲜度信号分析

> **Layer 2 check.** Google News heavily weights freshness; publication timing is a competitive ranking factor.

### Step 1 — Validate datePublished / dateModified

| Check | Pass Condition | Priority | Points |
|-------|---------------|----------|--------|
| datePublished present | ISO 8601 timestamp in Schema | P0 | required |
| dateModified ≥ datePublished | Modified timestamp not earlier than published | P0 | 30 pts if valid |
| No excessive modification | Not modified > 5× within 24 hours | P1 | deduct 15 if flagged |

### Step 2 — Estimate publication speed

Compare `datePublished` with the article's `<news:publication_date>` in the News Sitemap (if available), or use HTTP `Last-Modified` / `Date` response headers as proxy.

| Speed | Condition | Points |
|-------|-----------|--------|
| Fast | Sitemap entry within 30 min of datePublished | 40 pts |
| Moderate | 30 min – 1 hour gap | 20 pts |
| Slow | > 1 hour gap | 0 pts |

### Step 3 — Flag manipulation signals

- `dateModified` updated repeatedly with no detectable content change → flag as "possible freshness manipulation" (P1)
- `datePublished` set in the future → flag as P0 error

### Freshness Score Output

```
Freshness Score: [0-100]

| Signal | Result | Points |
|--------|--------|--------|
| datePublished / dateModified valid | Pass ✅ / Fail ❌ | 30 / 0 |
| Publication speed | Fast ✅ / Moderate ⚠️ / Slow ❌ | 40/20/0 |
| No manipulation signals | Pass ✅ / Flagged ⚠️ | 30 / 15 |
```

---

## 5.10 · Content Type Classification 内容类型分类

> **Layer 2 check.** Content type affects cluster placement, ranking duration, and competitive differentiation.

### Step 1 — Classify article type

Evaluate based on headline, body length, quote count, and source references:

| Type | Signals | Base Score |
|------|---------|------------|
| **Breaking News** | Published within 2h of event; headline includes "Breaking", "Just In", "Developing"; body < 600 words | 90–100 |
| **Analysis** | Body 800+ words; 3+ named sources or citations; analytical headline ("Why", "How", "What This Means For") | 70–90 |
| **Digest / Roundup** | 5+ outbound links to sources; "Roundup", "Weekly", "Today's News" in headline | 40–60 |
| **Aggregation** | No direct quotes; no named reporter byline; summarizes other sources only | 20–40 |

### Step 2 — Detect AI template patterns

Scan H2/H3 headings within the article body for:
> `Key Takeaways` · `Pros and Cons` · `Opposing Views` · `Summary` · `FAQ` · `Related Topics` · `Bottom Line`

- Any pattern detected → flag as "AI template structure detected" (P1) → **deduct 20 pts** from base score
- Recommend restructuring to inverted-pyramid news format

### Content Type Score Output

```
Content Type: [Breaking News / Analysis / Digest / Aggregation]
AI Template Detected: [Yes ⚠️ / No ✅]
Content Type Score: [0-100]
```

---

## 5.11 · Publisher Authority Estimation 发布者权威估算

> **Layer 2 check.** Google evaluates publisher-level authority when ranking articles in topic clusters.

Estimate publisher authority using available signals:

| Signal | How to check | Points |
|--------|-------------|--------|
| Article volume | Count total articles in News Sitemap; 10+ = strong, 3–9 = moderate, < 3 = low | 25 pts |
| Organization Schema | `@type: Organization` or `NewsMediaOrganization` present on homepage | 25 pts |
| Brand mentions | WebSearch `"<publisher name>" news` — check result count and source quality | 25 pts |
| Internal link structure | Article pages link to author pages, topic hubs, related articles | 25 pts |

### Publisher Authority Score Output

```
Publisher Authority Score: [0-100]

| Signal | Result | Notes |
|--------|--------|-------|
| Article volume | Strong ✅ / Moderate ⚠️ / Low ❌ | [count] |
| Organization Schema | Present ✅ / Absent ❌ | |
| Brand mentions | Strong ✅ / Moderate ⚠️ / Weak ❌ | |
| Internal link structure | Good ✅ / Partial ⚠️ / Poor ❌ | |
```

---

## 5.12 · Topic Cluster Compatibility 话题聚类兼容性

> **Layer 2 check.** Google News groups articles about the same event into topic clusters; these signals determine cluster membership.

### Step 1 — Headline entity analysis

Check whether the headline contains at least one named entity (person, organization, location, financial instrument, or event name).

- Named entity present → **25 pts**; note the detected entity
- Generic headline (no named entities) → **0 pts** (P1): "Add specific entity names to headline for cluster matching"

### Step 2 — Entity density in body

Count named entities per 100 words in the article body (use recognizable proper nouns as proxy):

- ≥ 1 entity per 100 words → **25 pts**
- < 1 entity per 200 words → **0 pts** (P1): "Increase named entity density — add specific company names, people, or locations"

### Step 3 — Timeliness check

- Article published within 6 hours of the referenced event → **25 pts**
- Published 6–24 hours after → **15 pts**
- Published > 24 hours after → **0 pts**

### Step 4 — Original reporting signals

Check for any of:
- Direct quoted speech with attribution (`"…" said [Name]`)
- Exclusive data, statistics, or documents
- Bylined reporter with a domain-specific author profile

- 1+ signals present → **25 pts**
- None detected → **0 pts** (P1): "Add original reporting signals — direct quotes or exclusive data"

### Topic Cluster Compatibility Score Output

```
Topic Cluster Compatibility Score: [0-100]

| Signal | Result | Points |
|--------|--------|--------|
| Headline named entity | Present ✅ / Absent ❌ | 25 / 0 |
| Entity density | High ✅ / Low ❌ | 25 / 0 |
| Timeliness | < 6h ✅ / 6-24h ⚠️ / > 24h ❌ | 25/15/0 |
| Original reporting | Present ✅ / Absent ❌ | 25 / 0 |
```

---

## 5.13 · Top Stories Detection Top Stories 检测

> **Layer 2 check.** Determines whether the article topic triggers a Google Top Stories carousel and whether the analyzed site appears in it.

### Step 1 — Extract topic keyword

From the article headline, identify the primary entity or event name. Use the most specific named entity (e.g., "Apple WWDC 2026" rather than "tech event").

### Step 2 — Search for Top Stories carousel

Use WebSearch to search the topic keyword. Analyze results for:
- A "Top Stories", "News", or "In the News" carousel module
- Publisher names and headlines appearing in the carousel
- Timestamps of carousel articles

| Result | Output |
|--------|--------|
| Top Stories carousel found | Topic triggers Top Stories; extract publisher list |
| No carousel found | "No Top Stories carousel detected for this topic" |

### Step 3 — Compare site against carousel publishers

Check whether the analyzed domain appears in the list of carousel publishers.

| Result | Status |
|--------|--------|
| Analyzed site in carousel | Top Stories Presence: **Confirmed** ✅ |
| Analyzed site absent, competitors present | Top Stories Presence: **Gap detected** ❌ |
| No carousel exists | Top Stories Presence: **Topic not triggering carousel** ⚠️ |

### Output

```
Top Stories Presence: [Confirmed ✅ / Gap detected ❌ / Not triggering ⚠️]

Competitors in carousel:
| Publisher | Headline | Published |
|-----------|----------|-----------|
| [name] | [headline] | [time] |
```

---

## 6 · Output Report Format 总结报告格式

After analysis, output the report in the following structure.
分析完成后按对应结构输出。

**Full Diagnostic mode** (Section 10 triggered):
System Model → Dual-Layer Scorecard → Executive Summary → Detailed Check Tables → Competitor Gap Analysis → Priority Fix List

**Article / Scoped audit mode**:
Executive Summary → Detailed Check Tables → Priority Fix List

---

### Dual-Layer Scorecard (Full Diagnostic only)

Output at the top of Full Diagnostic reports, before the Executive Summary.

```
## Google News Diagnostic Report

**Google News SEO Score: XX / 100**  [🟢 Strong / 🟡 Developing / 🔴 At Risk]

| Layer | Score | Status |
|-------|-------|--------|
| Layer 1 — Index Eligibility | XX/100 | Pass ✅ / Partial ⚠️ / Fail ❌ |
| Layer 2 — Ranking Potential | XX/100 | Pass ✅ / Partial ⚠️ / Fail ❌ |

**Diagnosis**: [plain-language statement — see Section 10 for routing logic]
```

---

### Executive Summary 执行摘要

Output this section first (after Dual-Layer Scorecard if present), before all detailed tables.

**Overall Health / 总体健康度：**

| Condition | Rating |
|-----------|--------|
| 0 P0 issues AND ≤ 2 P1 issues | 🟢 **Good** |
| 1–2 P0 issues OR 3–5 P1 issues | 🟡 **Needs Work** |
| 3+ P0 issues OR 6+ P1 issues | 🔴 **Critical** |

**Top Issues / 优先问题（最多 5 项）：**
```
- [P0] **[Area]**: Brief description of issue
- [P1] **[Area]**: Brief description of issue
```
If more than 5 issues exist, show the 5 most severe and add: *"See full findings below for all issues."*
If no issues found: *"No critical issues found ✅"*

**Quick Wins / 快速修复（最多 3 项，低成本高收益）：**
```
- **[Fix name]**: One-sentence instruction (e.g., "Add publisher.name to NewsArticle Schema")
```
Quick Win criteria: fixable in < 30 minutes, no code deployment required (e.g., CMS field edit, meta tag addition, file rename).
If none qualify: *"No quick wins identified — remaining issues require development work."*

---

**Executive Summary template / 执行摘要模板：**

```
### Executive Summary

**Overall Health**: 🟢 Good / 🟡 Needs Work / 🔴 Critical
**Scope**: [what was audited]

**Top Issues**
- [P0] **Schema**: dateModified is earlier than datePublished
- [P1] **On-Page**: Meta description missing on article page
- [P1] **Technical**: No News Sitemap found

**Quick Wins**
- **Fix dateModified**: Set dateModified to the last-edited timestamp in your CMS Schema output
- **Add meta description**: Map the article excerpt/summary field to meta description in your theme template
```

---

### Detailed Findings / 逐项检查表

**Table / 表格：**

| Check item / 检查项 | Result / 结果 | Notes / 说明 |
|---|---|---|
| (item) | Pass ✅ / Fail ❌ / Manual 🔍 | Issue description or fix suggestion |

---

### Priority Fix List / 优先级修复列表

- **P0** — blocks indexing or violates content policy / 影响收录或违反内容政策
- **P1** — affects rich results or EEAT signal strength / 影响富摘要或 EEAT 信号
- **P2** — best practice / 规范性

---

## 6.5 · Competitor Gap Analysis 竞争对手差距分析

> **Run during Full Diagnostic or when the user asks "why do competitors rank higher?" / "为什么竞争对手排名更高？"**

### Step 1 — Identify top competitors

Use WebSearch to search: `"<article topic>" news`

Extract the top 3–5 news publisher results: domain, headline, publish timestamp.

```
Competitors detected:
| Rank | Publisher | Headline | Published |
|------|-----------|----------|-----------|
| 1 | [domain] | [headline] | [time] |
```

### Step 2 — Fetch competitor articles

For each competitor URL, use the three-phase fetch protocol (WebFetch → curl → Manual) to extract:
- `datePublished` from Schema or page
- NewsArticle Schema completeness: count present required fields out of 9 (`@type`, `headline`, `image`, `datePublished`, `dateModified`, `author`, `publisher`, `publisher.logo`, `mainEntityOfPage`)
- Author authority: named author with linked profile page (Yes / Partial / No)

### Step 3 — Compute gap metrics

**Publication speed gap:**
```
Your site: datePublished → [timestamp]
Earliest competitor: [publisher] → [timestamp]
Gap: [X minutes / hours] → [Advantage ✅ / Disadvantage ❌]
```

**Full comparison table:**
```
| Publisher | Schema Completeness | Author Authority | Publish Speed |
|-----------|---------------------|------------------|---------------|
| Your site | XX% (X/9 fields) | Full / Partial / None | [timestamp] |
| [Competitor 1] | XX% | Full / Partial / None | [timestamp] |
| [Competitor 2] | XX% | Full / Partial / None | [timestamp] |
```

### Step 4 — Output gap analysis summary

```
## Competitor Gap Analysis

**Topic**: [search topic]
**Competitors analyzed**: [N]

### Key Gaps

**Publication Speed**
Your site: [X min after event]
Competitors avg: [Y min after event]
Gap: [difference] → [recommendation if gap > 15 min]

**Schema Completeness**
Your site: [XX%]
Competitors avg: [XX%]
Gap: [difference] → [recommendation if gap > 10%]

**Author Authority**
[Competitors provide full author profiles / Your site matches competitor standard]

### Recommendations
- [Specific action to close each identified gap]
```

---

## 7 · EEAT Scan 触发与输入处理

**Trigger words / 触发词**：
`EEAT 扫描` / `Run EEAT scan` / `扫描 EEAT` / `EEAT audit` / `EEAT 审计` / `做个 EEAT 扫描`

**Step 1 — Read the signal checklist / 第一步：读取检查项清单**

Before scanning, read `eeat-reference.md` (same directory as this file) to load all 24 signal definitions.

```
Read: eeat-reference.md
```

**Step 2 — Determine input type / 第二步：判断输入类型**

| Input | Action |
|-------|--------|
| Live URL / 线上 URL | Use WebFetch to fetch the page; extract full page HTML, JSON-LD, and visible text |
| Raw HTML / 原始 HTML | Parse provided HTML directly; no fetch needed |
| URL unreachable / 无法抓取 | Mark all signals that require live page inspection as 🔍 Manual; proceed with available information |

**Step 3 — Execute dimensional scans / 第三步：按维度执行扫描**

Run the four dimensions in order: **Experience → Expertise → Authoritativeness → Trustworthiness**

For each signal in `eeat-reference.md`:
1. Check the pass condition against the fetched page content
2. Record result: **Pass ✅** / **Fail ❌** / **🔍 Manual**
3. For Fail results, note what was found and what is expected
4. For Manual signals, note what requires manual verification

---

## 8 · EEAT 评分算法

**Per-dimension score / 维度评分：**

```
维度分 = floor(该维度通过项数 / 该维度有效项数 × 100)
```

- 有效项数 = 总项数 − 🔍 Manual 项数（Manual 项从分母中排除）
- 四个维度各自独立计算

**Total score / 总分：**

```
总分 = floor((经验分 + 专业度分 + 权威性分 + 可信度分) / 4)
```

**Rating labels / 评级标签：**

| Score range | Label |
|-------------|-------|
| 80–100 | 良好 ✅ |
| 50–79 | 需改进 ⚠️ |
| 0–49 | 差 ❌ |

---

## 9 · EEAT 报告格式

After completing all scans, output the report in the following structure.
Use the **same language as the user's prompt** throughout (Chinese prompt → Chinese report; English prompt → English report).

---

**Report template / 报告模板：**

```
## EEAT 扫描报告

**扫描对象**：https://example.com/article/ （或 "Raw HTML input"）
**扫描日期**：YYYY-MM-DD
**总分：XX / 100**

---

### 维度总览

| 维度 | 得分 | 评级 |
|------|------|------|
| 经验 (Experience) | XX | 良好 ✅ / 需改进 ⚠️ / 差 ❌ |
| 专业度 (Expertise) | XX | ... |
| 权威性 (Authoritativeness) | XX | ... |
| 可信度 (Trustworthiness) | XX | ... |

---

### 经验 (Experience) — XX/100

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 第一手内容标识 | Pass ✅ | 符合要求 |
| 经历日期明确 | Fail ❌ | 未注明具体经历时间 |
| 作者署名可见 | Pass ✅ | 符合要求 |
| 作者简介链接存在 | 🔍 Manual | 需手动核查作者页是否可访问 |
| 原创媒体 | Fail ❌ | 图片文件名含 "dall-e" |

### 专业度 (Expertise) — XX/100

| 检查项 | 结果 | 说明 |
|--------|------|------|
| ... | ... | ... |

### 权威性 (Authoritativeness) — XX/100

| 检查项 | 结果 | 说明 |
|--------|------|------|
| ... | ... | ... |

### 可信度 (Trustworthiness) — XX/100

| 检查项 | 结果 | 说明 |
|--------|------|------|
| ... | ... | ... |

---

### 行动建议

**P0 — 立即修复（影响收录或违反内容政策）**
- **[经验]** 原创媒体 — 将图片文件名中的 "dall-e" 前缀去除，上传流程中禁止保留 AI 工具名称
- **[可信度]** HTTPS — 将站点迁移至 HTTPS 并配置 301 重定向

**P1 — 应尽快修复**
- **[专业度]** 作者资质说明 — 在作者简介中补充职业背景或领域经验描述
- **[权威性]** 发布方名称缺失 — 在 NewsArticle Schema 的 publisher.name 字段填写机构名称

**P2 — 建议跟进**
- **[专业度]** 内容深度 — 文章不足 500 字，建议扩充至覆盖 3 个以上子议题
```

---

## 10 · Google News Diagnostic Report 完整诊断报告

> **Trigger**: Run this section when scope is "Full Diagnostic", or when the user asks why their site is not in Google News / why articles don't rank / why competitors outrank them.

### Score Aggregation / 评分聚合

**Google News SEO Score = Layer 1 Score × 60% + Layer 2 Score × 40%**

**Layer 1 — Index Eligibility (60% weight)**

| Sub-check | Weight |
|-----------|--------|
| Publisher Trust Score | 15% |
| Author Authority Score | 15% |
| Schema Health (completeness %) | 15% |
| News Sitemap Health Score | 10% |
| Crawlability Score | 5% |

**Layer 2 — Ranking Potential (40% weight)**

| Sub-check | Weight |
|-----------|--------|
| Freshness Score | 15% |
| Content Type Score | 10% |
| Topic Cluster Compatibility Score | 10% |
| Top Stories Presence (binary: 5 or 0 pts) | 5% |

**Rating labels:**

| Score | Label |
|-------|-------|
| 80–100 | 🟢 Strong |
| 50–79 | 🟡 Developing |
| 0–49 | 🔴 At Risk |

---

### Diagnosis Routing / 诊断结论路由

| Condition | Diagnosis Statement |
|-----------|-------------------|
| Layer 1 score < 50 | "Primary issue: This site is likely not eligible for Google News indexing. Fix Layer 1 issues before optimizing for ranking." |
| Layer 1 50–69 (Partial) | "Site has partial Google News index presence. Resolve remaining Layer 1 gaps to achieve consistent indexing, then address Layer 2 ranking." |
| Layer 1 ≥ 70, Layer 2 < 50 | "Site is indexed but articles are not competitive in Google News clusters. Focus on Layer 2 ranking improvements." |
| Layer 1 ≥ 70, Layer 2 ≥ 70 | "Site and articles meet Google News baseline requirements. Competitor gap analysis shows remaining optimization opportunities." |

---

### Full Diagnostic Report Template / 完整诊断报告模板

```
## Google News Diagnostic Report

**Analyzed**: [URL or domain]
**Date**: [YYYY-MM-DD]
**Google News SEO Score**: XX / 100  🟢 Strong / 🟡 Developing / 🔴 At Risk

---

### Dual-Layer Scorecard

| Layer | Score | Status |
|-------|-------|--------|
| Layer 1 — Index Eligibility | XX/100 | Pass ✅ / Partial ⚠️ / Fail ❌ |
| Layer 2 — Ranking Potential | XX/100 | Pass ✅ / Partial ⚠️ / Fail ❌ |

**Diagnosis**: [statement from routing table above]

---

### Layer 1 — Index Eligibility

| Check | Score | Status |
|-------|-------|--------|
| News Index Status | — | Not Indexed ❌ / Limited ⚠️ / Strong ✅ |
| Publisher Trust | XX/100 | Pass / Partial / Fail |
| Author Authority | XX/100 | Pass / Partial / Fail |
| Schema Health | XX% complete | Pass / Partial / Fail |
| News Sitemap Health | XX/100 | Pass / Partial / Fail |
| Crawlability | XX/100 | Pass / Partial / Fail |
| URL Structure | — | Recommended ✅ / Issues ⚠️ |

---

### Layer 2 — Ranking Potential

| Check | Score | Status |
|-------|-------|--------|
| Freshness | XX/100 | Fast ✅ / Moderate ⚠️ / Slow ❌ |
| Content Type | [type] / XX pts | Breaking / Analysis / Digest / Aggregation |
| Publisher Authority | XX/100 | Strong / Moderate / Weak |
| Topic Cluster Compatibility | XX/100 | High / Medium / Low |
| Top Stories Presence | — | Confirmed ✅ / Gap ❌ / Not triggering ⚠️ |

---

### Competitor Gap Analysis Summary

[See Section 6.5 output]

---

### Priority Fix List

**P0 — Fix immediately (blocks indexing)**
- [item]

**P1 — Fix soon (affects ranking)**
- [item]

**P2 — Best practice**
- [item]
```

---

## References 参考资源

- Google News ranking factors, optimization strategies, AI content policy, News Sitemap examples, two-layer architecture model, Topic Cluster signals:
  见 [reference.md](reference.md)
- EEAT signal definitions and priority table:
  见 [eeat-reference.md](eeat-reference.md)
