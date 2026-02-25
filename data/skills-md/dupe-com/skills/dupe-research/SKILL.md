---
name: dupe-research
description: Start AI-powered product research tasks on dupe.com. Kick off deep product research with archetype-based personas, track progress, and get comprehensive reports with product recommendations, pricing, and editorial articles. Use when the user wants to research, compare, or find the best products in a category.
compatibility:
  - Requires curl, python3, and internet access
  - One-time browser sign-in required for user authentication (token saved locally for 30 days)
  - Agent must solve a BOTCHA speed challenge to authenticate — no SDKs or packages needed
metadata:
  author: dupe.com
  version: 1.2.0
---

# Dupe.com AI Product Research

Launch deep product research tasks from your terminal or AI agent — the same research pipeline that powers the dupe.com web app.

## What This Skill Does

This skill lets AI agents:

1. **Start a research task** — provide a search query and shopper archetype
2. **Track progress** — poll the task status as it moves through research phases
3. **Get results** — receive product candidates, a research article, and a link to the published report

Research tasks run an AI-powered pipeline that discovers products, gathers reviews, analyzes video content, structures data, and writes a comprehensive research article.

## When to Use

Use this skill when the user wants to:

- Research the best products in a category ("best wireless earbuds under $100")
- Compare products with specific priorities (value, quality, reviews, etc.)
- Get AI-powered product recommendations with reasoning
- Generate a detailed research report for a product category

## When NOT to Use

- For finding visual dupes/lookalikes of a specific product URL — use the `dupe` skill instead
- For quick price comparisons without deep research

## Background or Foreground?

Research takes 2-5 minutes. After the user picks an archetype, ask them:

> "Research takes a few minutes. Want me to run it in the background so we can keep chatting, or wait here for results?"

**If background:**
1. Spawn a background agent / subagent / task to handle Steps 0-5
2. Tell the user: "Research is running in the background. I'll share results when it's ready."
3. Continue the conversation — the background task will complete on its own
4. **For Claude Code:** Use the `Task` tool with `subagent_type: "general"` and pass the full research prompt (query, archetype, instructions from Steps 0-5)
5. **For other agents:** Use whatever background task or subagent mechanism is available

**If foreground:**
1. Run Steps 0-5 directly in the conversation thread
2. Warn the user that polling will block the thread for a few minutes

## Instructions

### Step 0: Authenticate User (One-Time)

Before using the API, check if the user has a saved auth token. This is a one-time browser sign-in that produces a 30-day JWT.

**Check for existing token:**

```bash
USER_TOKEN=$(python3 -c "
import json, os, time, base64
path = os.path.expanduser('~/.dupe/auth.json')
if not os.path.exists(path):
    exit(1)
data = json.load(open(path))
token = data.get('token', '')
# Check expiry (JWT payload is base64-encoded second segment)
payload = json.loads(base64.urlsafe_b64decode(token.split('.')[1] + '=='))
if payload.get('exp', 0) < time.time():
    exit(1)
print(token)
" 2>/dev/null) || USER_TOKEN=""
```

**If no token (or expired), run the auth flow:**

```bash
if [ -z "$USER_TOKEN" ]; then
  # Step 1: Initiate auth session
  AUTH_RESPONSE=$(curl -s -X POST "https://api.dupe.com/api/cli-auth/initiate")
  SESSION_ID=$(echo "$AUTH_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['sessionId'])")
  AUTH_URL=$(echo "$AUTH_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['authUrl'])")
  POLL_URL=$(echo "$AUTH_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['pollUrl'])")

  # Step 2: Tell the user to open the URL in their browser
  echo "Please open this URL to sign in: $AUTH_URL"

  # Step 3: Poll until verified (15 minute timeout)
  while true; do
    STATUS_RESPONSE=$(curl -s "$POLL_URL")
    STATUS=$(echo "$STATUS_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))")
    if [ "$STATUS" = "verified" ]; then
      USER_TOKEN=$(echo "$STATUS_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
      mkdir -p ~/.dupe
      echo "{\"token\": \"$USER_TOKEN\"}" > ~/.dupe/auth.json
      echo "Authenticated successfully."
      break
    fi
    sleep 3
  done
fi
```

**Important:**
- The user only needs to do this once per 30 days
- The token is saved to `~/.dupe/auth.json` and reused automatically
- Tell the user to open the URL — do NOT open it silently
- The auth session expires after 15 minutes if not completed

### Step 1: Choose an Archetype

Before starting a research task, ask the user which research style they prefer. Present these options:

| # | Label | Pass this as `archetype` |
|---|-------|--------------------------|
| 1 | **Best Value (Deal Hunter)** | `Shoppers who prioritize getting the best price-to-quality ratio. They compare prices across retailers, look for sales and discounts, and want products that deliver good performance without overpaying. Budget-conscious but quality-aware. Typical budget: $50-$150.` |
| 2 | **Highest Quality Only** | `Shoppers who only want the absolute best version of a product. They prioritize premium materials, superior construction, and long-term durability. Price is secondary to quality. They read expert reviews and trust established premium brands. Typical budget: $200+.` |
| 3 | **Just Tell Me Which One** | `Busy shoppers who want a clear, confident recommendation without spending hours researching. They trust expert guidance and want a single "best" option that works for most people. They value convenience and quick decision-making over deep analysis.` |
| 4 | **Social Proof Focused** | `Shoppers who heavily rely on customer reviews, ratings, and real user experiences. They read both positive and negative reviews, look for patterns in feedback, and trust the wisdom of the crowd over marketing claims. They want products with 4+ star ratings and hundreds of reviews.` |
| 5 | **Deep Research & Comparison** | `Detail-oriented shoppers who want comprehensive breakdowns of specs, features, pros/cons, and side-by-side comparisons. They enjoy the research process and want all the data before deciding. They compare multiple options across different criteria.` |

If the user doesn't specify a preference, default to option 5 (Deep Research & Comparison).

### Step 2: Authenticate with BOTCHA

The API is protected by [BOTCHA](https://botcha.ai) — a reverse CAPTCHA for AI agents. Run this **single command** to get a token. It fetches the challenge, solves all 5 SHA-256 hashes, and submits the answer — all in one shot:

```bash
TOKEN=$(python3 -c "
import urllib.request, json, hashlib
APP_ID = 'app_b397bc17769877f7'
headers = {'User-Agent': 'dupe-research-skill/1.1', 'Content-Type': 'application/json'}
req = urllib.request.Request(f'https://botcha.ai/v1/token?app_id={APP_ID}', headers=headers)
with urllib.request.urlopen(req) as r:
    data = json.loads(r.read())
ch = data['challenge']
answers = [hashlib.sha256(str(p['num']).encode()).hexdigest()[:8] for p in ch['problems']]
payload = json.dumps({'id': ch['id'], 'answers': answers, 'audience': 'https://api.dupe.com', 'app_id': APP_ID}).encode()
req2 = urllib.request.Request('https://botcha.ai/v1/token/verify', data=payload, headers=headers, method='POST')
with urllib.request.urlopen(req2) as r2:
    result = json.loads(r2.read())
print(result.get('access_token', ''))
")
echo "Token obtained: ${TOKEN:0:20}..."
```

**Critical details:**
- The `audience` field MUST be `"https://api.dupe.com"` — without it the token will be rejected by the API
- The `User-Agent` header is required — BOTCHA returns 403 without it
- The entire solve must complete within 500ms of receiving the challenge — python3 handles this easily in a single script
- Tokens expire in 1 hour. If you get a `401`, re-run this command
- Uses only `python3` (available on macOS and Linux) — no `jq`, `node`, or other dependencies

### Step 3: Start the Research Task

```bash
RESULT=$(curl -s -X POST "https://api.dupe.com/api/research/agent-skill/start" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-User-Auth: $USER_TOKEN" \
  -d "{
    \"title\": \"<USER_SEARCH_QUERY>\",
    \"archetype\": \"<FULL_ARCHETYPE_DESCRIPTION>\",
    \"count\": 10
  }")
TASK_ID=$(echo "$RESULT" | sed -n 's/.*"taskId":"\([^"]*\)".*/\1/p')
REPORT_URL=$(echo "$RESULT" | sed -n 's/.*"reportUrl":"\([^"]*\)".*/\1/p')
echo "Task: $TASK_ID"
echo "Report will be at: $REPORT_URL"
```

**Request body fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | The user's search query (min 5 characters) |
| `archetype` | string | Yes | Full archetype description from table above (NOT the label) |
| `count` | number | No | Number of products to research (2-20, default: 10) |

If a task with the same title already exists for this month, the API returns the existing task (200) so you can resume polling.

### Step 4: Poll Until Complete

Run this polling loop. It checks every 10 seconds and exits when research reaches a terminal state:

```bash
while true; do
  STATUS_JSON=$(curl -s "https://api.dupe.com/api/research/agent-skill/$TASK_ID/status" \
    -H "Authorization: Bearer $TOKEN" \
    -H "X-User-Auth: $USER_TOKEN")
  PROGRESS=$(echo "$STATUS_JSON" | sed -n 's/.*"progress":\([0-9]*\).*/\1/p')
  TASK_STATUS=$(echo "$STATUS_JSON" | sed -n 's/.*"status":"\([^"]*\)".*/\1/p')
  PHASE=$(echo "$STATUS_JSON" | sed -n 's/.*"currentPhase":"\([^"]*\)".*/\1/p')
  echo "[$PROGRESS%] $PHASE — $TASK_STATUS"
  case "$TASK_STATUS" in
    researched|published|complete|failed|cancelled) break ;;
  esac
  sleep 10
done
echo "Final status: $TASK_STATUS"
echo "$STATUS_JSON"
```

**Research phases (in order):**

| Phase | Description |
|-------|-------------|
| `initializing` | Setting up the research task |
| `brief` | Writing research brief |
| `discovery` | Discovering products |
| `gather` | Gathering detailed product info |
| `video_insights` | Analyzing video reviews |
| `social_insights` | Analyzing social media |
| `schema` | Structuring product data |
| `writing_article` | Writing the research article |
| `finalize` | Final processing |

**Terminal statuses** — stop polling when you see one of these:

| Status | Meaning |
|--------|---------|
| `researched` | Research is complete, article is ready |
| `published` | Research report website is deployed |
| `complete` | Everything is done |
| `failed` | Research failed (check error message) |
| `cancelled` | Task was cancelled |

### Step 5: Present Results

When the task reaches a terminal status, parse the final `STATUS_JSON` and present:

```
## Research Complete: <title>

Found <productsTotal> products.

### Top Picks

1. **<candidate.name>** (<candidate.brand>)
   - Price: $<candidate.priceLow> - $<candidate.priceHigh>
   - [View product details]

2. ...

### Full Report

Read the complete research article: <reportUrl>

---
Powered by dupe.com AI Research
```

If `article` is present in the response, you can also display or summarize the full article content directly.

If `reportUrl` is available, always include it — it links to a beautifully formatted research report page.

## Error Handling

| Status Code | Meaning | Action |
|-------------|---------|--------|
| 401 | BOTCHA token missing/invalid/expired | Re-run the BOTCHA auth command from Step 2 |
| 400 | Invalid request body | Check title (min 5 chars) and archetype (min 10 chars) |
| 404 | Task not found | Verify the taskId is correct |
| 500 | Server error | Retry after a few seconds |

## Links

- **dupe.com**: [https://dupe.com](https://dupe.com)
- **BOTCHA (agent auth)**: [https://botcha.ai](https://botcha.ai)
- **dupe.com skills repo**: [github.com/dupe-com/skills](https://github.com/dupe-com/skills)
