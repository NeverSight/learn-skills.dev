---
name: gmail-label
description: Auto-label Gmail emails into Action Required, Waiting On, and Reference categories. Use when user asks to label emails, triage inbox, categorize emails, or organize Gmail.
---

# Gmail Auto-Label

## Goal
Fetch inbox emails, classify them via parallel subagents into Action Required / Waiting On / Reference, and apply labels in bulk via Gmail API.

## Scripts
- `./scripts/gmail_label_fetch.py` - Fetch email summaries as compact JSON
- `./scripts/gmail_label_split.py` - Split emails into N chunks for parallel classification
- `./scripts/gmail_label_merge.py` - Merge classified chunks into single labels.json
- `./scripts/gmail_label_apply.py` - Apply label classifications in bulk

## Subagent
- `email-classifier` — defined in `.claude/agents/email-classifier.md`
- Model: Sonnet 4.5 (fast, cost-efficient classification)
- Each subagent reads one chunk, writes one classified output file

## Flow (Parallel — default)

### Step 1: Fetch emails
```bash
python3 .claude/skills/gmail-label/scripts/gmail_label_fetch.py \
  --account ACCOUNT --query "in:inbox" --limit 100 --output .tmp/emails.json
```

### Step 2: Split into chunks
```bash
python3 .claude/skills/gmail-label/scripts/gmail_label_split.py \
  --input .tmp/emails.json --chunks 10 --output-dir .tmp/chunks
```

### Step 3: Classify in parallel (spawn 10 subagents)
Spawn 10 `email-classifier` subagents in background, one per chunk. Each subagent:
- Reads `.tmp/chunks/chunk_N.json`
- Classifies each email
- Writes `.tmp/chunks/classified_N.json`

Use the Task tool with `run_in_background: true` and `model: "sonnet"`. Launch ALL 10 in a single message for true parallelism:

```
For each chunk 0-9, spawn a Task with:
  subagent_type: "email-classifier"
  model: "sonnet"
  run_in_background: true
  prompt: "Read /absolute/path/.tmp/chunks/chunk_N.json, classify each email, write results to /absolute/path/.tmp/chunks/classified_N.json"
```

**CRITICAL: Do NOT use TaskOutput to read subagent results.** The subagents write their results to files — the main agent never needs to see the classification data. Reading TaskOutput will flood the context window and cause "prompt too long" errors with large batches (500+ emails).

Instead, poll for file existence:
```bash
# Wait until all classified files exist (timeout after 120s)
for i in $(seq 0 9); do
  while [ ! -f ".tmp/chunks/classified_$i.json" ]; do sleep 2; done
done
```

Then proceed directly to Step 4 (merge).

### Step 4: Merge classifications
```bash
python3 .claude/skills/gmail-label/scripts/gmail_label_merge.py \
  --input-dir .tmp/chunks --output .tmp/labels.json
```

### Step 5: Apply labels
```bash
python3 .claude/skills/gmail-label/scripts/gmail_label_apply.py \
  --account ACCOUNT --input .tmp/labels.json
```

## Classification Guidelines

**Action Required:**
- Security alerts that need verification
- Expiring credit cards / domain renewals with deadlines
- Slack @mentions asking questions
- New team members to greet (Slack join notifications)
- Client emails needing response
- Business listing updates (Google Business Profile, Bing Places)
- Stripe action-required notices

**Waiting On:**
- Outbound sales emails awaiting reply
- Support tickets awaiting resolution
- Proposals sent, pending response

**Reference:**
- Marketing newsletters (DigitalMarketer, etc.)
- Charity/nonprofit newsletters (RAPS, etc.)
- Google Business Profile performance reports
- Promotional offers (Blinkist, sales, etc.)
- Platform update notifications (Google Play, Apify, etc.)
- Confirmation codes (already used)
- Real estate newsletters (Westbank, etc.)
- Gaming account emails (Riot Games, etc.)
- Informational security alerts (2FA turned on, etc.)
- Health advisories
- Legal/policy update notices

## Account Registry
Accounts are stored in `gmail_accounts.json` at workspace root. Each account needs:
- `email` - Gmail address
- `token_file` - Path to OAuth token

## Adding New Accounts
```bash
python3 .claude/skills/gmail-inbox/scripts/gmail_multi_auth.py --account ACCOUNT_NAME --email EMAIL
```

## Performance
- **Serial flow**: ~36s for 100 emails (fetch 1s + classify 34s + apply 1s)
- **Parallel flow**: ~30s for 100 emails (classify 19s + merge <1s + apply ~10s)
- Classification is the bottleneck; 10 parallel subagents cut it from 34s to 19s (~1.8x speedup)
- Agent startup overhead (~4s stagger) limits theoretical gains
- Apply step may vary due to Gmail API throttling

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `account` | string | Yes | Gmail account name from registry |
| `query` | string | No | Gmail search query (default: 'in:inbox') |
| `limit` | integer | No | Max emails to classify (default: 100) |
| `chunks` | integer | No | Parallel classification chunks (default: 10) |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `labels_applied` | object | Count per category: Action Required, Waiting On, Reference |

### Credentials
| Name | Source |
|------|--------|
| `credentials.json` | file |
| `token_*.json` | file (auto-generated) |

### Composable With
Skills that chain well with this one: `gmail-inbox`

### Cost
Claude Sonnet API for classification
