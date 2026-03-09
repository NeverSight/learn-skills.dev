---
name: llm-monitoring-dashboard
description: Auto-generates an LLM usage monitoring page in a PM admin dashboard. Tokuin CLI-based token/cost/latency tracking + user ranking system + inactive user tracking + data-driven PM insights + Cmd+K global search + per-user drilldown navigation. Supports OpenAI/Anthropic/Gemini/OpenRouter.
metadata:
  tags: LLM, monitoring, dashboard, tokuin, pm-insights, ranking, user-tracking, cost-tracking, Next.js, React, admin
  platforms: Claude, ChatGPT, Gemini, Codex
---


# LLM Usage Monitoring Dashboard

> Tracks LLM API costs, tokens, and latency using **Tokuin CLI**, and auto-generates a data-driven admin dashboard with PM insights.

---

## When to use this skill

- **LLM cost visibility**: When you want to monitor API usage costs per team or individual in real time
- **PM reporting dashboard**: When you need weekly reports on who uses AI, how much, and how
- **User adoption management**: When you want to track inactive users and increase AI adoption rates
- **Model optimization evidence**: When you need data-driven decisions for model switching or cost reduction
- **Add monitoring tab to admin dashboard**: When adding an LLM monitoring section to an existing Admin page

---

## Prerequisites

### 1. Verify Tokuin CLI installation

```bash
# Check if installed
which tokuin && tokuin --version || echo "Not installed — run Step 1 first"
```

### 2. Environment variables (only needed for live API calls)

```bash
# Store in .env file (never hardcode directly in source)
OPENAI_API_KEY=sk-...          # OpenAI
ANTHROPIC_API_KEY=sk-ant-...   # Anthropic
OPENROUTER_API_KEY=sk-or-...   # OpenRouter (400+ models)

# LLM monitoring settings
LLM_USER_ID=dev-alice           # User identifier
LLM_USER_ALIAS=Alice            # Display name
COST_THRESHOLD_USD=10.00        # Cost threshold (alert when exceeded)
DASHBOARD_PORT=3000             # Dashboard port
MAX_COST_USD=5.00               # Max cost per single run
SLACK_WEBHOOK_URL=https://...   # For alerts (optional)
```

### 3. Project stack requirements

```
Option A (recommended): Next.js 15+ + React 18 + TypeScript
Option B (lightweight): Python 3.8+ + HTML/JavaScript (minimal dependencies)
```

---

## Instructions

### Step 0: Safety check (always run this first)

**⚠️ Run this script before executing the skill. Any FAIL items will halt execution.**

```bash
cat > safety-guard.sh << 'SAFETY_EOF'
#!/usr/bin/env bash
# safety-guard.sh — Safety gate before running the LLM monitoring dashboard
set -euo pipefail

RED='\033[0;31m'; YELLOW='\033[1;33m'; GREEN='\033[0;32m'; NC='\033[0m'
ALLOW_LIVE="${1:-}"; PASS=0; WARN=0; FAIL=0

log_pass() { echo -e "${GREEN}✅ PASS${NC} $1"; ((PASS++)); }
log_warn() { echo -e "${YELLOW}⚠️  WARN${NC} $1"; ((WARN++)); }
log_fail() { echo -e "${RED}❌ FAIL${NC} $1"; ((FAIL++)); }

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🛡  LLM Monitoring Dashboard — Safety Guard v1.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── 1. Check Tokuin CLI installation ────────────────────────────────
if command -v tokuin &>/dev/null; then
  log_pass "Tokuin CLI installed: $(tokuin --version 2>&1 | head -1)"
else
  log_fail "Tokuin not installed → install with the command below and re-run:"
  echo "  curl -fsSL https://raw.githubusercontent.com/nooscraft/tokuin/main/install.sh | bash"
fi

# ── 2. Detect hardcoded API keys ────────────────────────────────
HARDCODED=$(grep -rE "(sk-[a-zA-Z0-9]{20,}|sk-ant-[a-zA-Z0-9]{20,}|sk-or-[a-zA-Z0-9]{20,})" \
  . --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" \
  --include="*.html" --include="*.sh" --include="*.py" --include="*.json" \
  --exclude-dir=node_modules --exclude-dir=.git 2>/dev/null \
  | grep -v "\.env" | grep -v "example" | wc -l || echo 0)
if [ "$HARDCODED" -eq 0 ]; then
  log_pass "No hardcoded API keys found"
else
  log_fail "⚠️  ${HARDCODED} hardcoded API key(s) detected! → Move to environment variables (.env) immediately"
  grep -rE "(sk-[a-zA-Z0-9]{20,})" . \
    --include="*.ts" --include="*.js" --include="*.html" \
    --exclude-dir=node_modules 2>/dev/null | head -5 || true
fi

# ── 3. Check .env is in .gitignore ────────────────────────────
if [ -f .env ]; then
  if [ -f .gitignore ] && grep -q "\.env" .gitignore; then
    log_pass ".env is listed in .gitignore"
  else
    log_fail ".env exists but is not in .gitignore! → echo '.env' >> .gitignore"
  fi
else
  log_warn ".env file not found — create one before making live API calls"
fi

# ── 4. Check live API call mode ────────────────────────────
if [ "$ALLOW_LIVE" = "--allow-live" ]; then
  log_warn "Live API call mode enabled! Costs will be incurred."
  log_warn "Max cost threshold: \$${MAX_COST_USD:-5.00} (adjust via MAX_COST_USD env var)"
  read -p "  Allow live API calls? [y/N] " -r
  echo
  [[ $REPLY =~ ^[Yy]$ ]] || { echo "Cancelled. Re-run in dry-run mode."; exit 1; }
else
  log_pass "dry-run mode (default) — no API costs incurred"
fi

# ── 5. Check port conflicts ─────────────────────────────────────
PORT="${DASHBOARD_PORT:-3000}"
if lsof -i ":${PORT}" &>/dev/null 2>&1; then
  ALT_PORT=$((PORT + 1))
  log_warn "Port ${PORT} is in use → use ${ALT_PORT} instead: export DASHBOARD_PORT=${ALT_PORT}"
else
  log_pass "Port ${PORT} is available"
fi

# ── 6. Initialize data/ directory ──────────────────────────────
mkdir -p ./data
if [ -f ./data/metrics.jsonl ]; then
  BYTES=$(wc -c < ./data/metrics.jsonl || echo 0)
  if [ "$BYTES" -gt 10485760 ]; then
    log_warn "metrics.jsonl exceeds 10MB (${BYTES}B) → consider applying a rolling policy"
    echo "  cp data/metrics.jsonl data/metrics-$(date +%Y%m%d).jsonl.bak && > data/metrics.jsonl"
  else
    log_pass "data/ ready (metrics.jsonl: ${BYTES}B)"
  fi
else
  log_pass "data/ ready (new)"
fi

# ── Summary ─────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "Result: ${GREEN}PASS $PASS${NC} / ${YELLOW}WARN $WARN${NC} / ${RED}FAIL $FAIL${NC}"
if [ "$FAIL" -gt 0 ]; then
  echo -e "${RED}❌ Safety check failed. Resolve the FAIL items above and re-run.${NC}"
  exit 1
else
  echo -e "${GREEN}✅ Safety check passed. Continuing skill execution.${NC}"
  exit 0
fi
SAFETY_EOF
chmod +x safety-guard.sh

# Run (halts immediately if any FAIL)
bash safety-guard.sh
```

---

### Step 1: Install Tokuin CLI and verify with dry-run

```bash
# 1-1. Install (macOS / Linux)
curl -fsSL https://raw.githubusercontent.com/nooscraft/tokuin/main/install.sh | bash

# Windows PowerShell:
# irm https://raw.githubusercontent.com/nooscraft/tokuin/main/install.ps1 | iex

# 1-2. Verify installation
tokuin --version
which tokuin   # expected: /usr/local/bin/tokuin or ~/.local/bin/tokuin

# 1-3. Basic token count test
echo "Hello, world!" | tokuin --model gpt-4

# 1-4. dry-run cost estimate (no API key needed ✅)
echo "Analyze user behavior patterns from the following data" | \
  tokuin load-test \
  --model gpt-4 \
  --runs 50 \
  --concurrency 5 \
  --dry-run \
  --estimate-cost \
  --output-format json | python3 -m json.tool

# Expected output structure:
# {
#   "total_requests": 50,
#   "successful": 50,
#   "failed": 0,
#   "latency_ms": { "average": ..., "p50": ..., "p95": ... },
#   "cost": { "input_tokens": ..., "output_tokens": ..., "total_cost": ... }
# }

# 1-5. Multi-model comparison (dry-run)
echo "Translate this to Korean" | tokuin --compare gpt-4 gpt-3.5-turbo claude-3-haiku --price

# 1-6. Verify Prometheus format output
echo "Benchmark" | tokuin load-test --model gpt-4 --runs 10 --dry-run --output-format prometheus
# Expected: "# HELP", "# TYPE", metrics with "tokuin_" prefix
```

---

### Step 2: Data collection pipeline with user context

```bash
# 2-1. Create prompt auto-categorization module
cat > categorize_prompt.py << 'PYEOF'
#!/usr/bin/env python3
"""Auto-categorize prompts based on keywords"""
import hashlib

CATEGORIES = {
    "coding":      ["code", "function", "class", "implement", "debug", "fix", "refactor"],
    "analysis":    ["analyze", "compare", "evaluate", "assess"],
    "translation": ["translate", "translation"],
    "summary":     ["summarize", "summary", "tldr", "brief"],
    "writing":     ["write", "draft", "create", "generate"],
    "question":    ["what is", "how to", "explain", "why"],
    "data":        ["data", "table", "csv", "json", "sql"],
}

def categorize(prompt: str) -> str:
    p = prompt.lower()
    for cat, keywords in CATEGORIES.items():
        if any(k in p for k in keywords):
            return cat
    return "other"

def hash_prompt(prompt: str) -> str:
    """First 16 chars of SHA-256 (stored instead of raw text — privacy protection)"""
    return hashlib.sha256(prompt.encode()).hexdigest()[:16]

def truncate_preview(prompt: str, limit: int = 100) -> str:
    return prompt[:limit] + ("…" if len(prompt) > limit else "")

if __name__ == "__main__":
    import sys
    prompt = sys.argv[1] if len(sys.argv) > 1 else ""
    print(categorize(prompt))
PYEOF

# 2-2. Create metrics collection script with user context
cat > collect-metrics.sh << 'COLLECT_EOF'
#!/usr/bin/env bash
# collect-metrics.sh — Run Tokuin and save with user context (dry-run by default)
set -euo pipefail

# User info
USER_ID="${LLM_USER_ID:-$(whoami)}"
USER_ALIAS="${LLM_USER_ALIAS:-$USER_ID}"
SESSION_ID="${LLM_SESSION_ID:-$(date +%Y%m%d-%H%M%S)-$$}"
PROMPT="${1:-Benchmark prompt}"
MODEL="${MODEL:-gpt-4}"
PROVIDER="${PROVIDER:-openai}"
RUNS="${RUNS:-50}"
CONCURRENCY="${CONCURRENCY:-5}"
TAGS="${LLM_TAGS:-[]}"

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
CATEGORY=$(python3 categorize_prompt.py "$PROMPT" 2>/dev/null || echo "other")
PROMPT_HASH=$(echo -n "$PROMPT" | sha256sum | cut -c1-16 2>/dev/null || echo "unknown")
PROMPT_LEN=${#PROMPT}

# Run Tokuin (dry-run by default)
RESULT=$(echo "$PROMPT" | tokuin load-test \
  --model "$MODEL" \
  --provider "$PROVIDER" \
  --runs "$RUNS" \
  --concurrency "$CONCURRENCY" \
  --output-format json \
  ${ALLOW_LIVE:+""} ${ALLOW_LIVE:-"--dry-run --estimate-cost"} 2>/dev/null)

# Save to JSONL with user context
python3 - << PYEOF
import json, sys

result = json.loads('''${RESULT}''')
latency = result.get("latency_ms", {})
cost = result.get("cost", {})

record = {
    "id": "${PROMPT_HASH}-${SESSION_ID}",
    "timestamp": "${TIMESTAMP}",
    "model": "${MODEL}",
    "provider": "${PROVIDER}",
    "user_id": "${USER_ID}",
    "user_alias": "${USER_ALIAS}",
    "session_id": "${SESSION_ID}",
    "prompt_hash": "${PROMPT_HASH}",
    "prompt_category": "${CATEGORY}",
    "prompt_length": ${PROMPT_LEN},
    "tags": json.loads('${TAGS}'),
    "is_dry_run": True,
    "total_requests": result.get("total_requests", 0),
    "successful": result.get("successful", 0),
    "failed": result.get("failed", 0),
    "input_tokens": cost.get("input_tokens", 0),
    "output_tokens": cost.get("output_tokens", 0),
    "cost_usd": cost.get("total_cost", 0),
    "latency_avg_ms": latency.get("average", 0),
    "latency_p50_ms": latency.get("p50", 0),
    "latency_p95_ms": latency.get("p95", 0),
    "status_code": 200 if result.get("successful", 0) > 0 else 500,
}

with open("./data/metrics.jsonl", "a") as f:
    f.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"✅ Saved: [{record['user_alias']}] {record['prompt_category']} | ${record['cost_usd']:.4f} | {record['latency_avg_ms']:.0f}ms")
PYEOF
COLLECT_EOF
chmod +x collect-metrics.sh

# 2-3. Set up cron (auto-collect every 5 minutes)
(crontab -l 2>/dev/null; echo "*/5 * * * * cd $(pwd) && bash collect-metrics.sh 'Scheduled benchmark' >> ./data/collect.log 2>&1") | crontab -
echo "✅ Cron registered (every 5 minutes)"

# 2-4. First collection test (dry-run)
bash collect-metrics.sh "Analyze user behavior patterns"
cat ./data/metrics.jsonl | python3 -m json.tool | head -30
```

---

### Step 3: Routing structure and dashboard frame

**Option A — Next.js (recommended)**

```bash
# 3-1. Initialize Next.js project (skip this if adding to an existing project)
npx create-next-app@latest llm-dashboard \
  --typescript \
  --tailwind \
  --app \
  --no-src-dir
cd llm-dashboard

# 3-2. Install dependencies
npm install recharts better-sqlite3 @types/better-sqlite3

# 3-3. Set design tokens (consistent tone and style)
cat > app/globals.css << 'CSS_EOF'
:root {
  /* Background layers */
  --bg-base:     #0f1117;
  --bg-surface:  #1a1d27;
  --bg-elevated: #21253a;
  --border:      rgba(255, 255, 255, 0.06);

  /* Text layers */
  --text-primary:   #f1f5f9;
  --text-secondary: #94a3b8;
  --text-muted:     #475569;

  /* 3-level traffic light system (use consistently across all components) */
  --color-ok:      #22c55e;   /* Normal  — Green 500 */
  --color-warn:    #f59e0b;   /* Warning — Amber 500 */
  --color-danger:  #ef4444;   /* Danger  — Red 500   */
  --color-neutral: #60a5fa;   /* Neutral — Blue 400  */

  /* Data series colors (colorblind-friendly palette) */
  --series-1: #818cf8;  /* Indigo  — System/GPT-4    */
  --series-2: #38bdf8;  /* Sky     — User/Claude     */
  --series-3: #34d399;  /* Emerald — Assistant/Gemini*/
  --series-4: #fb923c;  /* Orange  — 4th series      */

  /* Cost-specific */
  --cost-input:  #a78bfa;
  --cost-output: #f472b6;

  /* Ranking colors */
  --rank-gold:     #fbbf24;
  --rank-silver:   #94a3b8;
  --rank-bronze:   #b45309;
  --rank-inactive: #374151;

  /* Typography */
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  --font-ui:   'Geist', 'Plus Jakarta Sans', system-ui, sans-serif;
}

body {
  background: var(--bg-base);
  color: var(--text-primary);
  font-family: var(--font-ui);
}

/* Numbers: alignment stability */
.metric-value {
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  font-feature-settings: 'tnum';
}

/* KPI card accent-bar */
.status-ok     { border-left-color: var(--color-ok); }
.status-warn   { border-left-color: var(--color-warn); }
.status-danger { border-left-color: var(--color-danger); }
CSS_EOF

# 3-4. Create routing structure
mkdir -p app/admin/llm-monitoring
mkdir -p app/admin/llm-monitoring/users
mkdir -p "app/admin/llm-monitoring/users/[userId]"
mkdir -p "app/admin/llm-monitoring/runs/[runId]"
mkdir -p components/llm-monitoring
mkdir -p lib/llm-monitoring

# 3-5. Initialize SQLite DB
cat > lib/llm-monitoring/db.ts << 'TS_EOF'
import Database from 'better-sqlite3'
import path from 'path'

const DB_PATH = path.join(process.cwd(), 'data', 'monitoring.db')

const db = new Database(DB_PATH)

db.exec(`
  CREATE TABLE IF NOT EXISTS runs (
    id              TEXT PRIMARY KEY,
    timestamp       DATETIME NOT NULL DEFAULT (datetime('now')),
    model           TEXT NOT NULL,
    provider        TEXT NOT NULL,
    user_id         TEXT DEFAULT 'anonymous',
    user_alias      TEXT DEFAULT 'anonymous',
    session_id      TEXT,
    prompt_hash     TEXT,
    prompt_category TEXT DEFAULT 'other',
    prompt_length   INTEGER DEFAULT 0,
    tags            TEXT DEFAULT '[]',
    is_dry_run      INTEGER DEFAULT 1,
    total_requests  INTEGER DEFAULT 0,
    successful      INTEGER DEFAULT 0,
    failed          INTEGER DEFAULT 0,
    input_tokens    INTEGER DEFAULT 0,
    output_tokens   INTEGER DEFAULT 0,
    cost_usd        REAL DEFAULT 0,
    latency_avg_ms  REAL DEFAULT 0,
    latency_p50_ms  REAL DEFAULT 0,
    latency_p95_ms  REAL DEFAULT 0,
    status_code     INTEGER DEFAULT 200
  );

  CREATE TABLE IF NOT EXISTS user_profiles (
    user_id    TEXT PRIMARY KEY,
    user_alias TEXT NOT NULL,
    team       TEXT DEFAULT '',
    role       TEXT DEFAULT 'user',
    created_at DATETIME DEFAULT (datetime('now')),
    last_seen  DATETIME,
    notes      TEXT DEFAULT ''
  );

  CREATE INDEX IF NOT EXISTS idx_runs_timestamp  ON runs(timestamp DESC);
  CREATE INDEX IF NOT EXISTS idx_runs_user_id    ON runs(user_id);
  CREATE INDEX IF NOT EXISTS idx_runs_model      ON runs(model);

  CREATE VIEW IF NOT EXISTS user_stats AS
  SELECT
    user_id,
    user_alias,
    COUNT(*)                          AS total_runs,
    SUM(input_tokens + output_tokens) AS total_tokens,
    ROUND(SUM(cost_usd), 4)           AS total_cost,
    ROUND(AVG(latency_avg_ms), 1)     AS avg_latency,
    ROUND(AVG(CAST(successful AS REAL) / NULLIF(total_requests, 0) * 100), 1) AS success_rate,
    COUNT(DISTINCT model)             AS models_used,
    MAX(timestamp)                    AS last_seen
  FROM runs
  GROUP BY user_id;
`)

export default db
TS_EOF
```

**Option B — Lightweight HTML (minimal dependencies)**

```bash
# Use this when there's no existing project or you need a quick prototype
mkdir -p llm-monitoring/data

cat > llm-monitoring/index.html << 'HTML_EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🧮 LLM Usage Monitoring</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    /* Design tokens */
    :root {
      --bg-base: #0f1117; --bg-surface: #1a1d27; --bg-elevated: #21253a;
      --text-primary: #f1f5f9; --text-secondary: #94a3b8; --text-muted: #475569;
      --color-ok: #22c55e; --color-warn: #f59e0b; --color-danger: #ef4444;
      --series-1: #818cf8; --series-2: #38bdf8; --series-3: #34d399; --series-4: #fb923c;
      --rank-gold: #fbbf24; --rank-silver: #94a3b8; --rank-bronze: #b45309;
      --font-mono: 'JetBrains Mono', monospace;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: var(--bg-base); color: var(--text-primary); font-family: system-ui, sans-serif; padding: 24px; }
    header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; }
    header h1 { font-size: 1.5rem; font-weight: 700; color: #60a5fa; }
    .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
    @media (max-width: 768px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 480px) { .kpi-grid { grid-template-columns: 1fr; } }
    .kpi-card {
      background: var(--bg-surface);
      border: 1px solid rgba(255,255,255,0.06);
      border-left: 3px solid var(--color-neutral, #60a5fa);
      border-radius: 12px;
      padding: 20px;
    }
    .kpi-card.ok     { border-left-color: var(--color-ok); }
    .kpi-card.warn   { border-left-color: var(--color-warn); }
    .kpi-card.danger { border-left-color: var(--color-danger); }
    .kpi-label { font-size: 0.625rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted); margin-bottom: 8px; }
    .kpi-value { font-family: var(--font-mono); font-size: 2rem; font-weight: 700; font-variant-numeric: tabular-nums; }
    .kpi-sub   { font-size: 0.75rem; color: var(--text-secondary); margin-top: 4px; }
    .chart-row { display: grid; grid-template-columns: 2fr 1fr; gap: 16px; margin-bottom: 24px; }
    @media (max-width: 900px) { .chart-row { grid-template-columns: 1fr; } }
    .chart-card { background: var(--bg-surface); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 20px; }
    .chart-card h3 { font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 16px; text-transform: uppercase; letter-spacing: 0.05em; }
    .ranking-table { width: 100%; border-collapse: collapse; }
    .ranking-table th { font-size: 0.625rem; text-transform: uppercase; color: var(--text-muted); padding: 8px 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.06); }
    .ranking-table td { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.04); font-family: var(--font-mono); font-size: 0.875rem; }
    .ranking-table tr:hover td { background: var(--bg-elevated); }
    .user-link { color: #60a5fa; text-decoration: none; cursor: pointer; }
    .user-link:hover { text-decoration: underline; }
    .badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; }
    .badge-ok     { background: rgba(34,197,94,0.1);  color: var(--color-ok); }
    .badge-warn   { background: rgba(245,158,11,0.1); color: var(--color-warn); }
    .badge-danger { background: rgba(239,68,68,0.1);  color: var(--color-danger); }
    .rank-1 { color: var(--rank-gold); }
    .rank-2 { color: var(--rank-silver); }
    .rank-3 { color: var(--rank-bronze); }
    .insight-box { background: rgba(96,165,250,0.05); border: 1px solid rgba(96,165,250,0.15); border-radius: 8px; padding: 16px; margin-top: 8px; }
    .insight-box h4 { font-size: 0.75rem; color: #60a5fa; margin-bottom: 8px; }
    .insight-box ul { font-size: 0.8rem; color: var(--text-secondary); padding-left: 16px; }
    .insight-box ul li { margin-bottom: 4px; }
    .section-title { font-size: 1rem; font-weight: 600; margin: 24px 0 12px; }
    #user-detail { display: none; background: var(--bg-surface); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 24px; margin-top: 16px; }
    .back-btn { background: none; border: 1px solid rgba(255,255,255,0.1); color: var(--text-secondary); padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 0.8rem; margin-bottom: 16px; }
    .back-btn:hover { background: var(--bg-elevated); }
  </style>
</head>
<body>
  <header>
    <div>
      <h1>🧮 LLM Usage Monitoring</h1>
      <p style="font-size:0.75rem;color:#475569;margin-top:4px;">Powered by Tokuin CLI</p>
    </div>
    <div style="display:flex;gap:8px;align-items:center;">
      <span id="last-updated" style="font-size:0.75rem;color:#475569;"></span>
      <button onclick="loadData()" style="background:rgba(96,165,250,0.1);border:1px solid rgba(96,165,250,0.2);color:#60a5fa;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:0.8rem;">↻ Refresh</button>
    </div>
  </header>

  <!-- Main dashboard -->
  <div id="main-dashboard">
    <!-- 4 KPI cards -->
    <div class="kpi-grid">
      <div class="kpi-card" id="kpi-requests">
        <div class="kpi-label">Total Requests</div>
        <div class="kpi-value metric-value" id="val-requests">-</div>
        <div class="kpi-sub" id="sub-requests">Loading data...</div>
      </div>
      <div class="kpi-card" id="kpi-success">
        <div class="kpi-label">Success Rate</div>
        <div class="kpi-value metric-value" id="val-success">-</div>
        <div class="kpi-sub" id="sub-success">-</div>
      </div>
      <div class="kpi-card" id="kpi-latency">
        <div class="kpi-label">p95 Latency</div>
        <div class="kpi-value metric-value" id="val-latency">-</div>
        <div class="kpi-sub" id="sub-latency">-</div>
      </div>
      <div class="kpi-card" id="kpi-cost">
        <div class="kpi-label">Total Cost</div>
        <div class="kpi-value metric-value" id="val-cost">-</div>
        <div class="kpi-sub" id="sub-cost">-</div>
      </div>
    </div>

    <!-- Chart row -->
    <div class="chart-row">
      <div class="chart-card">
        <h3>Cost Trend Over Time</h3>
        <canvas id="trend-chart" height="160"></canvas>
      </div>
      <div class="chart-card">
        <h3>Category Distribution</h3>
        <canvas id="category-chart" height="160"></canvas>
      </div>
    </div>

    <!-- User ranking -->
    <h2 class="section-title">🏆 User Ranking</h2>
    <div class="chart-card" style="margin-bottom:24px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
        <h3 style="margin-bottom:0;">Ranked by Cost</h3>
        <input id="user-search" type="text" placeholder="🔍 Search users..." 
          style="background:var(--bg-elevated);border:1px solid rgba(255,255,255,0.08);color:var(--text-primary);padding:6px 12px;border-radius:6px;font-size:0.8rem;width:200px;"
          oninput="filterRanking(this.value)">
      </div>
      <table class="ranking-table" id="ranking-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>User</th>
            <th>Cost</th>
            <th>Requests</th>
            <th>Top Model</th>
            <th>Success Rate</th>
            <th>Last Active</th>
          </tr>
        </thead>
        <tbody id="ranking-body">
          <tr><td colspan="7" style="text-align:center;color:#475569;padding:24px;">Loading data...</td></tr>
        </tbody>
      </table>
    </div>

    <!-- Inactive user tracking -->
    <h2 class="section-title">💤 Inactive Users</h2>
    <div class="chart-card" style="margin-bottom:24px;">
      <table class="ranking-table" id="inactive-table">
        <thead>
          <tr><th>User</th><th>Inactive For</th><th>Last Active</th><th>Status</th></tr>
        </thead>
        <tbody id="inactive-body">
          <tr><td colspan="4" style="text-align:center;color:#475569;padding:24px;">No tracking data</td></tr>
        </tbody>
      </table>
    </div>

    <!-- PM insights -->
    <h2 class="section-title">📊 PM Auto Insights</h2>
    <div id="pm-insights">
      <div class="insight-box">
        <h4>💡 Analyzing automatically...</h4>
      </div>
    </div>
  </div>

  <!-- Per-user detail page (shown on link click) -->
  <div id="user-detail">
    <button class="back-btn" onclick="showMain()">← Back to Dashboard</button>
    <div id="user-detail-content"></div>
  </div>

  <script>
  let allData = [];
  let allUsers = {};

  async function loadData() {
    try {
      const res = await fetch('./data/metrics.jsonl');
      const text = await res.text();
      allData = text.trim().split('\n').filter(Boolean).map(l => JSON.parse(l));
      document.getElementById('last-updated').textContent = 'Last updated: ' + new Date().toLocaleTimeString();
      renderDashboard();
    } catch(e) {
      // Show sample data if JSONL file is missing
      allData = generateSampleData();
      renderDashboard();
    }
  }

  function generateSampleData() {
    const users = ['dev-alice', 'team-backend', 'analyst-bob', 'pm-charlie'];
    const models = ['gpt-4', 'claude-3-sonnet', 'gemini-pro'];
    const categories = ['coding', 'analysis', 'translation', 'summary', 'writing'];
    const data = [];
    for (let i = 0; i < 50; i++) {
      const user = users[Math.floor(Math.random() * users.length)];
      const daysAgo = Math.floor(Math.random() * 30);
      const ts = new Date(Date.now() - daysAgo * 86400000 - Math.random() * 86400000);
      data.push({
        id: 'sample-' + i,
        timestamp: ts.toISOString(),
        model: models[Math.floor(Math.random() * models.length)],
        provider: 'openai',
        user_id: user,
        user_alias: user,
        prompt_category: categories[Math.floor(Math.random() * categories.length)],
        input_tokens: Math.floor(Math.random() * 2000) + 100,
        output_tokens: Math.floor(Math.random() * 1000) + 50,
        cost_usd: (Math.random() * 0.05).toFixed(4) * 1,
        latency_avg_ms: Math.floor(Math.random() * 1500) + 200,
        latency_p95_ms: Math.floor(Math.random() * 2500) + 500,
        successful: 1,
        total_requests: 1,
        is_dry_run: true,
        status_code: Math.random() > 0.05 ? 200 : 429,
      });
    }
    return data;
  }

  function renderDashboard() {
    if (!allData.length) return;

    // Calculate KPIs
    const totalReqs  = allData.reduce((s, r) => s + (r.total_requests || 1), 0);
    const totalSucc  = allData.filter(r => r.status_code === 200).length;
    const successRate = ((totalSucc / allData.length) * 100).toFixed(1);
    const avgLatency = (allData.reduce((s, r) => s + (r.latency_avg_ms || 0), 0) / allData.length).toFixed(0);
    const p95Latency = (allData.reduce((s, r) => s + (r.latency_p95_ms || 0), 0) / allData.length).toFixed(0);
    const totalCost  = allData.reduce((s, r) => s + (r.cost_usd || 0), 0).toFixed(4);

    // Update KPI cards
    document.getElementById('val-requests').textContent = totalReqs.toLocaleString();
    document.getElementById('sub-requests').textContent = allData.length + ' run records';

    document.getElementById('val-success').textContent = successRate + '%';
    document.getElementById('sub-success').textContent = (allData.length - totalSucc) + ' failures';
    const kpiSuccess = document.getElementById('kpi-success');
    kpiSuccess.className = 'kpi-card ' + (successRate >= 95 ? 'ok' : successRate >= 90 ? 'warn' : 'danger');

    document.getElementById('val-latency').textContent = p95Latency + 'ms';
    document.getElementById('sub-latency').textContent = 'avg ' + avgLatency + 'ms';
    const kpiLatency = document.getElementById('kpi-latency');
    kpiLatency.className = 'kpi-card ' + (p95Latency < 1000 ? 'ok' : p95Latency < 2000 ? 'warn' : 'danger');

    document.getElementById('val-cost').textContent = '$' + totalCost;
    document.getElementById('sub-cost').textContent = 'dry-run estimate';

    // Trend chart
    renderTrendChart();
    // Category distribution
    renderCategoryChart();
    // User ranking
    renderRanking();
    // Inactive users
    renderInactive();
    // PM insights
    renderInsights(successRate, p95Latency, totalCost);
  }

  function renderTrendChart() {
    const ctx = document.getElementById('trend-chart').getContext('2d');
    const byDate = {};
    allData.forEach(r => {
      const d = r.timestamp.substring(0, 10);
      byDate[d] = (byDate[d] || 0) + (r.cost_usd || 0);
    });
    const labels = Object.keys(byDate).sort().slice(-14);
    const values = labels.map(d => byDate[d].toFixed(4));
    if (window._trendChart) window._trendChart.destroy();
    window._trendChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Daily Cost ($)',
          data: values,
          borderColor: '#818cf8',
          backgroundColor: 'rgba(129,140,248,0.1)',
          fill: true,
          tension: 0.4,
          pointRadius: 4,
          pointBackgroundColor: '#818cf8',
        }]
      },
      options: {
        plugins: { legend: { labels: { color: '#94a3b8' } } },
        scales: {
          x: { ticks: { color: '#475569' }, grid: { color: 'rgba(255,255,255,0.04)' } },
          y: { ticks: { color: '#475569' }, grid: { color: 'rgba(255,255,255,0.04)' } }
        }
      }
    });
  }

  function renderCategoryChart() {
    const ctx = document.getElementById('category-chart').getContext('2d');
    const cats = {};
    allData.forEach(r => { cats[r.prompt_category || 'other'] = (cats[r.prompt_category || 'other'] || 0) + 1; });
    const colors = ['#818cf8','#38bdf8','#34d399','#fb923c','#f472b6','#94a3b8'];
    if (window._catChart) window._catChart.destroy();
    window._catChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: Object.keys(cats),
        datasets: [{ data: Object.values(cats), backgroundColor: colors, borderWidth: 0 }]
      },
      options: {
        plugins: { legend: { position: 'right', labels: { color: '#94a3b8', font: { size: 11 } } } },
        cutout: '65%'
      }
    });
  }

  function renderRanking(filter = '') {
    const userMap = {};
    allData.forEach(r => {
      const uid = r.user_id || 'anonymous';
      if (!userMap[uid]) userMap[uid] = { alias: r.user_alias || uid, cost: 0, runs: 0, models: {}, success: 0, last: r.timestamp };
      userMap[uid].cost  += r.cost_usd || 0;
      userMap[uid].runs  += 1;
      userMap[uid].models[r.model] = (userMap[uid].models[r.model] || 0) + 1;
      if (r.status_code === 200) userMap[uid].success++;
      if (r.timestamp > userMap[uid].last) userMap[uid].last = r.timestamp;
    });
    allUsers = userMap;
    const sorted = Object.entries(userMap)
      .filter(([uid, u]) => !filter || u.alias.toLowerCase().includes(filter.toLowerCase()))
      .sort((a, b) => b[1].cost - a[1].cost);
    const tbody = document.getElementById('ranking-body');
    if (!sorted.length) { tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;color:#475569;padding:16px;">No results found</td></tr>'; return; }
    const rankEmoji = ['🥇','🥈','🥉'];
    tbody.innerHTML = sorted.map(([uid, u], i) => {
      const topModel = Object.entries(u.models).sort((a,b) => b[1]-a[1])[0]?.[0] || '-';
      const sr = ((u.success / u.runs) * 100).toFixed(1);
      const srClass = sr >= 95 ? 'badge-ok' : sr >= 90 ? 'badge-warn' : 'badge-danger';
      const lastAgo = Math.floor((Date.now() - new Date(u.last)) / 86400000);
      const rankClass = i === 0 ? 'rank-1' : i === 1 ? 'rank-2' : i === 2 ? 'rank-3' : '';
      return `<tr>
        <td class="${rankClass}">${rankEmoji[i] || (i+1)}</td>
        <td><a class="user-link" onclick="showUserDetail('${uid}')">${u.alias}</a></td>
        <td class="metric-value">$${u.cost.toFixed(4)}</td>
        <td class="metric-value">${u.runs.toLocaleString()}</td>
        <td><span style="font-size:0.75rem;color:#94a3b8;">${topModel}</span></td>
        <td><span class="badge ${srClass}">${sr}%</span></td>
        <td style="color:#475569;font-size:0.75rem;">${lastAgo === 0 ? 'Today' : lastAgo + 'd ago'}</td>
      </tr>`;
    }).join('');
  }

  function filterRanking(val) { renderRanking(val); }

  function renderInactive() {
    const sevenDaysAgo = new Date(Date.now() - 7 * 86400000);
    const activeUsers = new Set(
      allData.filter(r => new Date(r.timestamp) > sevenDaysAgo).map(r => r.user_id)
    );
    const lastSeen = {};
    allData.forEach(r => {
      if (!lastSeen[r.user_id] || r.timestamp > lastSeen[r.user_id].ts) {
        lastSeen[r.user_id] = { ts: r.timestamp, alias: r.user_alias || r.user_id };
      }
    });
    const inactive = Object.entries(lastSeen).filter(([uid]) => !activeUsers.has(uid));
    const tbody = document.getElementById('inactive-body');
    if (!inactive.length) {
      tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#22c55e;padding:16px;">✅ All users active within 7 days</td></tr>';
      return;
    }
    tbody.innerHTML = inactive.map(([uid, info]) => {
      const daysAgo = Math.floor((Date.now() - new Date(info.ts)) / 86400000);
      const cls = daysAgo >= 30 ? 'badge-danger' : daysAgo >= 14 ? 'badge-warn' : 'badge-ok';
      return `<tr>
        <td><a class="user-link" onclick="showUserDetail('${uid}')">${info.alias}</a></td>
        <td class="metric-value">${daysAgo}d</td>
        <td style="color:#475569;font-size:0.75rem;">${new Date(info.ts).toLocaleDateString()}</td>
        <td><span class="badge ${cls}">${daysAgo >= 30 ? 'Critical' : daysAgo >= 14 ? 'Warning' : 'Monitor'}</span></td>
      </tr>`;
    }).join('');
  }

  function renderInsights(successRate, p95Latency, totalCost) {
    const insights = [];
    const sevenDaysAgo = new Date(Date.now() - 7 * 86400000);
    const activeUsers = new Set(allData.filter(r => new Date(r.timestamp) > sevenDaysAgo).map(r => r.user_id));
    const totalUsers = new Set(allData.map(r => r.user_id)).size;
    const adoptionRate = totalUsers ? Math.round(activeUsers.size / totalUsers * 100) : 0;
    const inactiveCount = totalUsers - activeUsers.size;

    if (inactiveCount > 0) insights.push(`■ <strong>${inactiveCount}</strong> inactive user(s) — consider onboarding/support`);
    if (successRate < 95) insights.push(`■ Success rate ${successRate}% → below SLA 95% — investigate error causes`);
    if (p95Latency > 2000) insights.push(`■ p95 latency ${p95Latency}ms → exceeds SLA — consider lighter models`);
    if (adoptionRate < 80) insights.push(`▲ Team adoption ${adoptionRate}% → below 80% target (${activeUsers.size}/${totalUsers} active)`);
    if (totalCost > 50) insights.push(`▲ Total cost $${totalCost} — review model optimization for top users`);

    const categories = {};
    allData.forEach(r => { categories[r.prompt_category || 'other'] = (categories[r.prompt_category || 'other'] || 0) + 1; });
    const topCat = Object.entries(categories).sort((a,b) => b[1]-a[1])[0];
    if (topCat) insights.push(`● Top usage pattern: <strong>${topCat[0]}</strong> (${topCat[1]} times) — specialized model may improve efficiency`);

    const insightDiv = document.getElementById('pm-insights');
    insightDiv.innerHTML = `<div class="insight-box">
      <h4>💡 PM Auto Insights — as of ${new Date().toLocaleDateString()}</h4>
      <ul>${insights.map(i => `<li>${i}</li>`).join('')}</ul>
    </div>`;
  }

  function showUserDetail(userId) {
    const u = allUsers[userId];
    if (!u) return;
    const userRuns = allData.filter(r => r.user_id === userId);
    const categories = {};
    userRuns.forEach(r => { categories[r.prompt_category || 'other'] = (categories[r.prompt_category || 'other'] || 0) + 1; });
    const totalCost = userRuns.reduce((s, r) => s + (r.cost_usd || 0), 0).toFixed(4);
    const topModel = Object.entries(
      userRuns.reduce((m, r) => { m[r.model] = (m[r.model] || 0)+1; return m; }, {})
    ).sort((a,b) => b[1]-a[1])[0]?.[0] || '-';

    document.getElementById('user-detail-content').innerHTML = `
      <div style="background:var(--bg-elevated);border-radius:8px;padding:16px;margin-bottom:20px;">
        <h2 style="font-size:1.25rem;margin-bottom:8px;">👤 ${u.alias}</h2>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:12px;">
          <div><div style="font-size:0.625rem;color:#475569;text-transform:uppercase;margin-bottom:4px;">Total Cost</div><div class="metric-value" style="font-size:1.5rem;">$${totalCost}</div></div>
          <div><div style="font-size:0.625rem;color:#475569;text-transform:uppercase;margin-bottom:4px;">Total Requests</div><div class="metric-value" style="font-size:1.5rem;">${u.runs.toLocaleString()}</div></div>
          <div><div style="font-size:0.625rem;color:#475569;text-transform:uppercase;margin-bottom:4px;">Top Model</div><div style="font-size:1rem;margin-top:4px;">${topModel}</div></div>
          <div><div style="font-size:0.625rem;color:#475569;text-transform:uppercase;margin-bottom:4px;">Category Breakdown</div><div style="font-size:0.8rem;color:#94a3b8;">${Object.entries(categories).map(([k,v]) => k+' '+v+'x').join(', ')}</div></div>
        </div>
      </div>
      <h3 style="font-size:0.875rem;color:#94a3b8;margin-bottom:12px;">Recent Run Log</h3>
      <table class="ranking-table">
        <thead><tr><th>Time</th><th>Model</th><th>Category</th><th>Cost</th><th>Latency</th><th>Status</th></tr></thead>
        <tbody>
          ${userRuns.slice(-10).reverse().map(r => {
            const sc = r.status_code === 200 ? 'badge-ok' : 'badge-danger';
            return `<tr>
              <td style="color:#475569;font-size:0.75rem;">${new Date(r.timestamp).toLocaleString()}</td>
              <td style="font-size:0.8rem;">${r.model}</td>
              <td><span class="badge badge-ok" style="font-size:0.65rem;">${r.prompt_category||'other'}</span></td>
              <td class="metric-value">$${(r.cost_usd||0).toFixed(4)}</td>
              <td class="metric-value">${(r.latency_avg_ms||0).toFixed(0)}ms</td>
              <td><span class="badge ${sc}">${r.status_code||200}</span></td>
            </tr>`;
          }).join('')}
        </tbody>
      </table>
      <div class="insight-box" style="margin-top:16px;">
        <h4>💡 Personal Insights</h4>
        <ul>
          <li>Top model: <strong>${topModel}</strong> — switching to a lighter model with similar performance could reduce costs</li>
          <li>Primary usage pattern: <strong>${Object.entries(categories).sort((a,b)=>b[1]-a[1])[0]?.[0]||'none'}</strong></li>
          <li>${u.runs} total runs — compare activity against team average</li>
        </ul>
      </div>
    `;
    document.getElementById('main-dashboard').style.display = 'none';
    document.getElementById('user-detail').style.display = 'block';
    window.scrollTo(0, 0);
  }

  function showMain() {
    document.getElementById('user-detail').style.display = 'none';
    document.getElementById('main-dashboard').style.display = 'block';
  }

  // Keyboard shortcuts
  document.addEventListener('keydown', e => {
    if (e.key === 'r' || e.key === 'R') loadData();
    if (e.key === 'Escape') showMain();
  });

  // Initial load
  loadData();
  // Auto-refresh every 5 minutes
  setInterval(loadData, 5 * 60 * 1000);
  </script>
</body>
</html>
HTML_EOF

echo "✅ Lightweight HTML dashboard created: llm-monitoring/index.html"
# Start local server
cd llm-monitoring && python3 -m http.server "${DASHBOARD_PORT:-3000}" &
echo "✅ Dashboard running: http://localhost:${DASHBOARD_PORT:-3000}"
```

---

### Step 4: PM insights tab and ranking system

(For Option A / Next.js)

```bash
# Create PM dashboard API route
cat > app/api/ranking/route.ts << 'TS_EOF'
import { NextRequest, NextResponse } from 'next/server'
import db from '@/lib/llm-monitoring/db'

export async function GET(req: NextRequest) {
  const period = req.nextUrl.searchParams.get('period') || '30d'
  const days   = period === '7d' ? 7 : period === '90d' ? 90 : 30

  // Cost-based ranking
  const costRanking = db.prepare(`
    SELECT
      user_id, user_alias,
      ROUND(SUM(cost_usd), 4)           AS total_cost,
      COUNT(*)                           AS total_runs,
      GROUP_CONCAT(DISTINCT model)       AS models_used,
      ROUND(AVG(latency_avg_ms), 0)      AS avg_latency,
      ROUND(
        AVG(CAST(successful AS REAL) / NULLIF(total_requests, 0)) * 100, 1
      )                                  AS success_rate,
      MAX(timestamp)                     AS last_seen
    FROM runs
    WHERE timestamp >= datetime('now', '-' || ? || ' days')
    GROUP BY user_id
    ORDER BY total_cost DESC
    LIMIT 20
  `).all(days)

  // Inactive user tracking (registered users with no activity in the selected period)
  const inactiveUsers = db.prepare(`
    SELECT
      p.user_id, p.user_alias, p.team,
      MAX(r.timestamp)  AS last_seen,
      CAST((julianday('now') - julianday(MAX(r.timestamp))) AS INTEGER) AS days_inactive
    FROM user_profiles p
    LEFT JOIN runs r ON p.user_id = r.user_id
    GROUP BY p.user_id
    HAVING last_seen IS NULL
       OR days_inactive >= 7
    ORDER BY days_inactive DESC
  `).all()

  // PM summary
  const summary = db.prepare(`
    SELECT
      COUNT(DISTINCT user_id)    AS total_users,
      COUNT(DISTINCT CASE WHEN timestamp >= datetime('now', '-7 days') THEN user_id END) AS active_7d,
      ROUND(SUM(cost_usd), 2)    AS total_cost,
      COUNT(*)                   AS total_runs
    FROM runs
    WHERE timestamp >= datetime('now', '-' || ? || ' days')
  `).get(days) as Record<string, number>

  return NextResponse.json({ costRanking, inactiveUsers, summary })
}
TS_EOF
```

---

### Step 5: Auto-generate weekly PM report

```bash
cat > generate-pm-report.sh << 'REPORT_EOF'
#!/usr/bin/env bash
# generate-pm-report.sh — Auto-generate weekly PM report (Markdown)
set -euo pipefail

REPORT_DATE=$(date +"%Y-%m-%d")
REPORT_WEEK=$(date +"%Y-W%V")
OUTPUT_DIR="./reports"
OUTPUT="${OUTPUT_DIR}/pm-weekly-${REPORT_DATE}.md"
mkdir -p "$OUTPUT_DIR"

python3 << PYEOF > "$OUTPUT"
import json, sys
from datetime import datetime, timedelta
from collections import defaultdict

# Load data from the last 7 days
try:
    records = [json.loads(l) for l in open('./data/metrics.jsonl') if l.strip()]
except FileNotFoundError:
    records = []

week_ago = (datetime.now() - timedelta(days=7)).isoformat()
week_data = [r for r in records if r.get('timestamp', '') >= week_ago]

# Aggregate
total_cost    = sum(r.get('cost_usd', 0) for r in week_data)
total_runs    = len(week_data)
active_users  = set(r['user_id'] for r in week_data)
all_users     = set(r['user_id'] for r in records)
inactive_users = all_users - active_users

# Per-user cost ranking
user_costs = defaultdict(lambda: {'cost': 0, 'runs': 0, 'alias': '', 'categories': defaultdict(int)})
for r in week_data:
    uid = r.get('user_id', 'unknown')
    user_costs[uid]['cost']  += r.get('cost_usd', 0)
    user_costs[uid]['runs']  += 1
    user_costs[uid]['alias']  = r.get('user_alias', uid)
    user_costs[uid]['categories'][r.get('prompt_category', 'other')] += 1

top_users = sorted(user_costs.items(), key=lambda x: x[1]['cost'], reverse=True)[:5]

# Model usage
model_usage = defaultdict(int)
for r in week_data:
    model_usage[r.get('model', 'unknown')] += 1
top_model = max(model_usage, key=model_usage.get) if model_usage else '-'

# Success rate
success_count = sum(1 for r in week_data if r.get('status_code', 200) == 200)
success_rate  = (success_count / total_runs * 100) if total_runs else 0

print(f"""# 📊 LLM Usage Weekly Report — {REPORT_DATE} ({REPORT_WEEK})

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Cost | \${total_cost:.2f} |
| Total Runs | {total_runs:,} |
| Active Users | {len(active_users)} |
| Adoption Rate | {len(active_users)}/{len(all_users)} ({len(active_users)/len(all_users)*100:.0f}% if all_users else 'N/A') |
| Success Rate | {success_rate:.1f}% |
| Top Model | {top_model} |

## 🏆 Top 5 Users (by Cost)

| Rank | User | Cost | Runs | Top Category |
|------|------|------|------|--------------|
{"".join(f"| {'🥇🥈🥉'[i] if i < 3 else i+1} | {u['alias']} | \${u['cost']:.4f} | {u['runs']} | {max(u['categories'], key=u['categories'].get) if u['categories'] else '-'} |" + chr(10) for i, (uid, u) in enumerate(top_users))}

## 💤 Inactive Users ({len(inactive_users)})

{"None — all users active within 7 days" if not inactive_users else chr(10).join(f"- {uid}" for uid in inactive_users)}

## 💡 PM Recommended Actions

{"- " + str(len(inactive_users)) + " inactive user(s) — consider onboarding/support" if inactive_users else ""}
{"- Success rate " + f"{success_rate:.1f}%" + " — SLA 95% " + ("achieved ✅" if success_rate >= 95 else "not met ⚠️ investigate error causes") }
{"- Total cost \$" + f"{total_cost:.2f}" + " — review model optimization opportunities vs. prior week"}

---
*Auto-generated by generate-pm-report.sh | Powered by Tokuin CLI*
""")
PYEOF

echo "✅ PM report generated: $OUTPUT"
cat "$OUTPUT"

# Slack notification (if configured)
if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
  SUMMARY=$(grep -A5 "## Executive Summary" "$OUTPUT" | tail -5)
  curl -s -X POST "$SLACK_WEBHOOK_URL" \
    -H 'Content-type: application/json' \
    -d "{\"text\":\"📊 Weekly LLM Report ($REPORT_DATE)\n$SUMMARY\"}" > /dev/null
  echo "✅ Slack notification sent"
fi
REPORT_EOF
chmod +x generate-pm-report.sh

# Schedule to run every Monday at 9am
(crontab -l 2>/dev/null; echo "0 9 * * 1 cd $(pwd) && bash generate-pm-report.sh >> ./data/report.log 2>&1") | crontab -
echo "✅ Weekly report cron registered (every Monday 09:00)"

# Run immediately for testing
bash generate-pm-report.sh
```

---

### Step 6: Cost alert setup

```bash
cat > check-alerts.sh << 'ALERT_EOF'
#!/usr/bin/env bash
# check-alerts.sh — Detect cost threshold breaches and send Slack alerts
set -euo pipefail

THRESHOLD="${COST_THRESHOLD_USD:-10.00}"

CURRENT_COST=$(python3 << PYEOF
import json
from datetime import datetime, timedelta

today = datetime.now().date().isoformat()
try:
    records = [json.loads(l) for l in open('./data/metrics.jsonl') if l.strip()]
    today_cost = sum(r.get('cost_usd', 0) for r in records if r.get('timestamp', '')[:10] == today)
    print(f"{today_cost:.4f}")
except:
    print("0.0000")
PYEOF
)

python3 - << PYEOF
import sys
cost, threshold = float('$CURRENT_COST'), float('$THRESHOLD')
if cost > threshold:
    print(f"ALERT: Today's cost \${cost:.4f} has exceeded the threshold \${threshold:.2f}!")
    sys.exit(1)
else:
    print(f"OK: Today's cost \${cost:.4f} / threshold \${threshold:.2f}")
    sys.exit(0)
PYEOF

# Send Slack alert on exit 1
if [ $? -ne 0 ] && [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
  curl -s -X POST "$SLACK_WEBHOOK_URL" \
    -H 'Content-type: application/json' \
    -d "{\"text\":\"⚠️ LLM cost threshold exceeded!\nToday's cost: \$$CURRENT_COST / Threshold: \$$THRESHOLD\"}" > /dev/null
fi
ALERT_EOF
chmod +x check-alerts.sh

# Check cost every hour
(crontab -l 2>/dev/null; echo "0 * * * * cd $(pwd) && bash check-alerts.sh >> ./data/alerts.log 2>&1") | crontab -
echo "✅ Cost alert cron registered (every hour)"
```

---

## Privacy Policy

```yaml
# Privacy policy (must be followed)

prompt_storage:
  store_full_prompt: false      # Default: do not store raw prompt text
  store_preview:     false      # Storing first 100 chars also disabled by default (requires explicit admin config)
  store_hash:        true       # Store SHA-256 hash only (for pattern analysis)

user_data:
  anonymize_by_default: true   # user_id can be stored as a hash (controlled via LLM_USER_ID env var)
  retention_days: 90            # Recommend purging data older than 90 days
  
compliance:
  # Never log API keys in code, HTML, scripts, or log files.
  # Always add .env to .gitignore.
  # Restrict prompt preview access to admins only.
```

> ⚠️ **Required steps when enabling `store_preview: true`**
> 
> Prompt preview storage can only be enabled after an **admin explicitly** completes the following steps:
> 
> 1. Set `STORE_PREVIEW=true` in the `.env` file (do not modify code directly)
> 2. Obtain team consent for personal data processing (notify users that previews will be stored)
> 3. Restrict access to **admin role only** (regular users must not be able to view)
> 4. Set `retention_days` explicitly to define the retention period
> 
> Enabling `store_preview: true` without completing these steps is a **MUST NOT** violation.

---

## Output Format

Files generated after running the skill:

```
./
├── safety-guard.sh          # Safety gate (Step 0)
├── categorize_prompt.py     # Prompt auto-categorization
├── collect-metrics.sh       # Metrics collection (Step 2)
├── generate-pm-report.sh    # PM weekly report (Step 5)
├── check-alerts.sh          # Cost alerts (Step 6)
│
├── data/
│   ├── metrics.jsonl        # Time-series metrics (JSONL format)
│   ├── collect.log          # Collection log
│   ├── alerts.log           # Alert log
│   └── reports/
│       └── pm-weekly-YYYY-MM-DD.md  # Auto-generated PM report
│
├── [If Next.js selected]
│   ├── app/admin/llm-monitoring/page.tsx
│   ├── app/admin/llm-monitoring/users/[userId]/page.tsx
│   ├── app/api/runs/route.ts
│   ├── app/api/ranking/route.ts
│   ├── app/api/metrics/route.ts        # Prometheus endpoint
│   ├── components/llm-monitoring/
│   │   ├── KPICard.tsx
│   │   ├── TrendChart.tsx
│   │   ├── ModelCostBar.tsx
│   │   ├── LatencyGauge.tsx
│   │   ├── TokenDonut.tsx
│   │   ├── RankingTable.tsx
│   │   ├── InactiveUsers.tsx
│   │   ├── PMInsights.tsx
│   │   └── UserDetailPage.tsx
│   └── lib/llm-monitoring/db.ts
│
└── [If lightweight HTML selected]
    └── llm-monitoring/
        ├── index.html       # Single-file dashboard (charts + ranking + user detail)
        └── data/
            └── metrics.jsonl
```

---

## Constraints

### MUST

- **Always run Step 0 (`safety-guard.sh`) first**
- Use `--dry-run` as the default; explicitly pass `--allow-live` for live API calls
- Manage API keys via environment variables or `.env` files
- Add `.env` to `.gitignore`: `echo '.env' >> .gitignore`
- Use the 3-level color system (`--color-ok`, `--color-warn`, `--color-danger`) consistently across all status indicators
- Implement drilldown navigation so clicking a user link opens their personal detail page
- Generate PM insights automatically from data (no hardcoding)

### MUST NOT

- Never hardcode API keys in source code, HTML, scripts, or log files
- Never set live API calls (`--allow-live`) as the default in automated scripts
- Never use arbitrary colors — always use design token CSS variables
- Never show status as text only — always pair with color and badge
- Never store raw prompt text in the database (hashes only)

---

## Examples

### Example 1: Quick start (dry-run, no API key needed)

```bash
# 1. Safety check
bash safety-guard.sh

# 2. Install Tokuin
curl -fsSL https://raw.githubusercontent.com/nooscraft/tokuin/main/install.sh | bash

# 3. Collect sample data (dry-run)
export LLM_USER_ID="dev-alice"
export LLM_USER_ALIAS="Alice"
bash collect-metrics.sh "Analyze user behavior patterns"
bash collect-metrics.sh "Write a Python function to parse JSON"
bash collect-metrics.sh "Translate this document to English"

# 4. Run lightweight dashboard
cd llm-monitoring && python3 -m http.server 3000
open http://localhost:3000
```

### Example 2: Multi-user simulation (team test)

```bash
# Simulate multiple users with dry-run
for user in "alice" "backend" "analyst" "pm-charlie"; do
  export LLM_USER_ID="$user"
  export LLM_USER_ALIAS="$user"
  for category in "coding" "analysis" "translation"; do
    bash collect-metrics.sh "${category} related prompt example"
  done
done

# Check results
wc -l data/metrics.jsonl
```

### Example 3: Generate PM weekly report immediately

```bash
bash generate-pm-report.sh
cat reports/pm-weekly-$(date +%Y-%m-%d).md
```

### Example 4: Test cost alert

```bash
export COST_THRESHOLD_USD=0.01   # Low threshold for testing
bash check-alerts.sh
# Expected: ALERT message if cost exceeds threshold, otherwise "OK"
```

---

## References

- **Tokuin GitHub**: https://github.com/nooscraft/tokuin
- **Tokuin install script**: https://raw.githubusercontent.com/nooscraft/tokuin/main/install.sh
- **Adding models guide**: https://github.com/nooscraft/tokuin/blob/main/ADDING_MODELS_GUIDE.md
- **Provider roadmap**: https://github.com/nooscraft/tokuin/blob/main/PROVIDERS_PLAN.md
- **Contributing guide**: https://github.com/nooscraft/tokuin/blob/main/CONTRIBUTING.md
- **OpenRouter model catalog**: https://openrouter.ai/models
- **Korean blog guide**: https://digitalbourgeois.tistory.com/m/2658
