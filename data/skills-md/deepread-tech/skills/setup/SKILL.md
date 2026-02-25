---
name: setup
description: Get started with DeepRead. Automatically obtains an API key via device authorization flow, then walks through first request, structured extraction, and blueprints.
allowed-tools: Bash, Read, Write
user-invocable: true
---

# Setup DeepRead

You are an AI agent helping a developer get started with DeepRead — an AI-native OCR API that extracts text and structured data from documents (PDFs, images) with 97%+ accuracy.

**API:** `https://api.deepread.tech`
**Dashboard:** `https://www.deepread.tech`
**Docs:** `https://www.deepread.tech/docs`

---

## Step 1: Get an API Key (Device Authorization Flow)

You (the agent) obtain an API key on behalf of the user. The user never needs to copy/paste a key — it goes directly to you.

> **CRITICAL — run the entire device flow as ONE Bash tool call.**
> Shell variables do not persist between tool calls. If you split this across multiple calls, the `device_code` will be lost and you will accidentally call `/v1/agent/device/code` again, getting a new code the user has never seen. Do it all in one script.

The complete flow — get code, open browser, poll, print key — in a single script:

```bash
# Get device code
dr_response=$(curl -s -X POST https://api.deepread.tech/v1/agent/device/code \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "Claude Code"}')

dr_device_code=$(echo "$dr_response" | jq -r '.device_code')
dr_user_code=$(echo "$dr_response" | jq -r '.user_code')
dr_uri=$(echo "$dr_response" | jq -r '.verification_uri_complete')
dr_interval=$(echo "$dr_response" | jq -r '.interval')

# Validate the response before proceeding
if [ "$dr_device_code" = "null" ] || [ -z "$dr_device_code" ]; then
  echo "ERROR: API did not return a device_code. Response: $dr_response"
  exit 1
fi

echo "Opening browser: $dr_uri"
open "$dr_uri" 2>/dev/null || xdg-open "$dr_uri" 2>/dev/null || echo "Open manually: $dr_uri"
echo "Waiting for approval of code: $dr_user_code"

# Poll until approved (use dr_ prefix — 'status' is reserved in zsh)
dr_api_key=""
for dr_i in $(seq 1 72); do
  sleep "$dr_interval"
  dr_result=$(curl -s -X POST https://api.deepread.tech/v1/agent/device/token \
    -H "Content-Type: application/json" \
    -d "{\"device_code\": \"$dr_device_code\"}")
  dr_api_key=$(echo "$dr_result" | jq -r '.api_key')
  dr_error=$(echo "$dr_result" | jq -r '.error')
  dr_prefix=$(echo "$dr_result" | jq -r '.key_prefix')

  if [ "$dr_api_key" != "null" ] && [ -n "$dr_api_key" ]; then
    echo "SUCCESS key_prefix=$dr_prefix"
    echo "DEEPREAD_API_KEY=$dr_api_key"
    break
  elif [ "$dr_error" = "access_denied" ]; then echo "DENIED"; break
  elif [ "$dr_error" = "expired_token" ]; then echo "EXPIRED"; break
  else echo "attempt=$dr_i pending..."; fi
done
```

**Variable naming:** Always use a unique prefix (e.g. `dr_`) for all variables in this script. Never use bare `status`, `result`, or `interval` — these are reserved or commonly overloaded in zsh/bash and will cause `read-only variable` errors.

**Never show the `device_code` to the user.** Only show `user_code` and the browser URL.

Responses from the token endpoint (all fields always present — check `api_key != null` for success):

| `error` | `api_key` | Meaning | Action |
|---------|-----------|---------|--------|
| `"authorization_pending"` | `null` | User hasn't approved yet | Wait `interval` seconds, poll again |
| `null` | `"sk_live_..."` | User approved | Save the key, stop polling |
| `"access_denied"` | `null` | User clicked Deny | Stop, inform user |
| `"expired_token"` | `null` | Code expired (15 min) | Start over from the top |

### Step 1d: Store the key safely

The `api_key` is returned exactly once — the server clears it after retrieval. Save it immediately.

**Safe `.env` append** — always use `printf` to guarantee a leading newline:

```bash
printf "\nDEEPREAD_API_KEY=%s\n" "$dr_api_key" >> .env
```

Never use `echo "KEY=val" >> .env` — if the file doesn't end with a newline, the key merges with the previous line.

### What happens on the user's side

**Already logged in:** Opens the URL → code is auto-validated → sees your agent name + Approve/Deny → clicks Approve → redirected to dashboard. The key arrives on your next poll.

**Not logged in:** Signs in or creates an account → redirected back with code pre-filled → clicks Approve.

In both cases the key goes directly to you — it never appears in chat.

---

## Step 2: Send Your First Document

> **IMPORTANT: Split submit and poll into SEPARATE Bash tool calls.**
> Long-running poll loops block the conversation and give the user no way to interact.
> Submit first, confirm the job ID, then poll separately.

### Step 2a: Submit the document (one Bash call)

```bash
DR_API_KEY=$(grep ^DEEPREAD_API_KEY .env | cut -d= -f2)

dr_submit=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DR_API_KEY" \
  -F "file=@document.pdf")

echo "$dr_submit"
```

Tell the user the job ID and that processing takes 2-3 minutes. Then move on to polling.

### Step 2b: Poll for results (separate Bash call)

> **Prefer `run_in_background: true`** for the poll loop so the conversation isn't blocked. If the user rejects a long-running poll, just do a single status check instead.

> **Guard against empty job ID.** If `dr_job_id` is empty or "null", stop immediately — don't loop.

> **Use `python3` for parsing results, not `jq`.** Job responses can be 200KB+ and `jq` may choke with parse errors on large payloads. Always save to a temp file first.

```bash
DR_API_KEY=$(grep ^DEEPREAD_API_KEY .env | cut -d= -f2)
dr_job_id="THE_JOB_ID"

# Guard: bail if job ID is empty
if [ -z "$dr_job_id" ] || [ "$dr_job_id" = "null" ]; then
  echo "ERROR: No job ID — submit may have failed. Check the submit response."
  exit 1
fi

for dr_i in $(seq 1 40); do
  sleep 5
  dr_poll=$(curl -s "https://api.deepread.tech/v1/jobs/$dr_job_id" -H "X-API-Key: $DR_API_KEY")
  dr_job_status=$(echo "$dr_poll" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status','unknown'))")
  echo "attempt=$dr_i status=$dr_job_status"
  if [ "$dr_job_status" = "completed" ] || [ "$dr_job_status" = "failed" ]; then
    echo "$dr_poll" > /tmp/deepread_result.json
    python3 -c "
import json
with open('/tmp/deepread_result.json') as f:
    data = json.load(f)
print(json.dumps({
    'status': data.get('status'),
    'preview_url': data.get('preview_url'),
    'page_count': len(data.get('result', {}).get('pages', [])) if data.get('result') else 0,
    'text_preview': (data.get('result', {}).get('text', '') or '')[:500],
}, indent=2))
"
    break
  fi
done
```

### If the user says "check now" or the poll was rejected

Don't start a new poll loop — just do a single fetch:

```bash
DR_API_KEY=$(grep ^DEEPREAD_API_KEY .env | cut -d= -f2)
curl -s "https://api.deepread.tech/v1/jobs/JOB_ID" -H "X-API-Key: $DR_API_KEY" > /tmp/deepread_result.json
python3 -c "
import json
with open('/tmp/deepread_result.json') as f:
    data = json.load(f)
print('Status:', data.get('status'))
if data.get('status') == 'completed':
    print(json.dumps({
        'preview_url': data.get('preview_url'),
        'page_count': len(data.get('result', {}).get('pages', [])) if data.get('result') else 0,
        'text_preview': (data.get('result', {}).get('text', '') or '')[:500],
    }, indent=2))
elif data.get('status') == 'failed':
    print('Error:', data.get('error'))
"
```

Supports PDF, PNG, JPG, JPEG. Max 15MB (free) / 50MB (paid).

---

## Step 3: Extract Structured Data

Add a `schema` parameter with a JSON Schema. Field descriptions guide the AI — the better the description, the better the extraction.

### Step 3a: Submit with schema (one Bash call)

```bash
DR_API_KEY=$(grep ^DEEPREAD_API_KEY .env | cut -d= -f2)

dr_submit=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DR_API_KEY" \
  -F "file=@invoice.pdf" \
  -F 'schema={
    "type": "object",
    "properties": {
      "vendor": {"type": "string", "description": "Company or vendor name on the invoice"},
      "total": {"type": "number", "description": "Total amount due in dollars"},
      "due_date": {"type": "string", "description": "Payment due date"}
    }
  }')

echo "$dr_submit"
```

### Step 3b: Fetch structured results (separate Bash call)

Same split pattern as Step 2 — poll separately or do a single check when the user says the job is done:

```bash
DR_API_KEY=$(grep ^DEEPREAD_API_KEY .env | cut -d= -f2)
curl -s "https://api.deepread.tech/v1/jobs/JOB_ID" -H "X-API-Key: $DR_API_KEY" > /tmp/deepread_structured_result.json
python3 -c "
import json
with open('/tmp/deepread_structured_result.json') as f:
    data = json.load(f)
print('Status:', data.get('status'))
if data.get('status') == 'completed':
    print()
    print('=== STRUCTURED DATA ===')
    fields = data.get('result', {}).get('data', {})
    if fields:
        print(json.dumps(fields, indent=2))
    else:
        print('No structured data returned')
    print()
    meta = data.get('metadata', {})
    print('=== METADATA ===')
    print(json.dumps({k: meta[k] for k in ['page_count','pipeline','review_percentage','fields_requiring_review','total_fields'] if k in meta}, indent=2))
    print()
    print('Preview:', data.get('preview_url', 'N/A'))
elif data.get('status') == 'failed':
    print('Error:', data.get('error'))
"
```

Each extracted field comes with quality metadata:

```json
{
  "vendor": {"value": "Acme Inc", "hil_flag": false, "found_on_page": 1},
  "due_date": {"value": "2025-03-15", "hil_flag": true, "reason": "Multiple dates found", "found_on_page": 1}
}
```

- `hil_flag: false` — extracted confidently, safe to auto-accept
- `hil_flag: true` — needs human review, check `reason` for why

---

## Step 4: Blueprints (Better Accuracy)

Blueprints are optimized schemas that improve accuracy by 20-30%. You give DeepRead sample documents + expected values, it enhances field descriptions automatically.

1. Go to `https://www.deepread.tech/dashboard/optimizer`
2. Upload 4+ sample docs + ground truth JSON
3. DeepRead runs 3-5 optimization iterations
4. Use the optimized blueprint:

```bash
curl -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: sk_live_YOUR_KEY" \
  -F "file=@invoice.pdf" \
  -F "blueprint_id=YOUR_BLUEPRINT_ID"
```

Use `schema` OR `blueprint_id`, not both.

---

## Plans

| Plan | Pages/month | Max file | Per-doc limit | Price |
|------|-------------|----------|---------------|-------|
| Free | 2,000 | 15 MB | 50 pages | $0 |
| Pro | 50,000 | 50 MB | Unlimited | $99/mo |
| Scale | 1,000,000 | 50 MB | Unlimited | Custom |

---

## What's Next

Use `/api` for the full reference — all endpoints, webhooks, error handling, blueprints API, and code examples in Python, JavaScript, and cURL.

## Help the Developer

- No API key yet → run the device flow above (Step 1)
- Has API key → help send first request (Step 2)
- Wants structured data → help write a JSON Schema with good field descriptions (Step 3)
- Wants better accuracy → explain blueprints and optimizer (Step 4)
- Wants full integration → use `/api` for complete reference
