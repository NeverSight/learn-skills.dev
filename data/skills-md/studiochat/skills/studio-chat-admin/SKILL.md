---
name: studio-chat-admin
description: >
  Manage Studio Chat project configuration — knowledge bases, playbooks, training, schedule,
  and API tools. Use when asked to create, update, delete, or inspect KBs, playbooks, office hours,
  or any project settings. Covers all CRUD operations via the Studio Chat API.
---

# Studio Chat Admin

Read and write Studio Chat project configuration using the API. All calls are authenticated automatically via environment variables. The API base URL (`https://api.studiochat.io`) is hardcoded in the scripts.

## Setup

Set the following environment variables before using the scripts:

```bash
export STUDIO_API_TOKEN="sbs_your_api_key_here"
export STUDIO_PROJECT_ID="your-project-uuid"
```

API keys are available by request from the Studio Chat team at hey@studiochat.io.

## API Client

```bash
python3 scripts/api.py <path> [-X METHOD] [--body JSON] [--params k=v] [-o file]
```

Supports GET, POST, PUT, PATCH, DELETE. Auth injected from env vars.

## Full API Reference

See [references/api-reference.md](references/api-reference.md) for complete endpoint specs.

---

## Knowledge Bases

KBs are the information the assistant searches to answer customers. Types: TEXT, FAQ, SNIPPETS, FILE.

### List KBs

```bash
python3 scripts/api.py \
  "/projects/$STUDIO_PROJECT_ID/knowledgebases" \
  --params include_playbook_usage=true
```

### Get KB content

```bash
python3 scripts/api.py "/knowledgebases/KB_ID"
```

### Create Text KB

```bash
python3 scripts/api.py \
  "/projects/$STUDIO_PROJECT_ID/knowledgebases/text" \
  -X POST --body '{
    "title": "Product FAQ",
    "content": "Your plain text content here..."
  }'
```

### Create FAQ KB

```bash
python3 scripts/api.py \
  "/projects/$STUDIO_PROJECT_ID/knowledgebases/faq" \
  -X POST --body '{
    "title": "Common Questions",
    "faq_items": [
      {"questions": ["How do I reset my password?"], "answer": "Go to Settings > Security > Reset Password."},
      {"questions": ["What are your hours?"], "answer": "Monday-Friday 9am-5pm EST."}
    ]
  }'
```

### Create Snippets KB (product catalog)

```bash
python3 scripts/api.py \
  "/projects/$STUDIO_PROJECT_ID/knowledgebases/snippets" \
  -X POST --body '{
    "title": "Product Catalog",
    "snippet_items": [
      {"title": "Basic Plan", "content": "Price: $10/mo. Includes 100 conversations."},
      {"title": "Pro Plan", "content": "Price: $50/mo. Includes 1000 conversations."}
    ]
  }'
```

### Update KB

```bash
python3 scripts/api.py "/knowledgebases/KB_ID" \
  -X PATCH --body '{"content": "New text content..."}'
```

### Delete / Restore KB

```bash
python3 scripts/api.py "/knowledgebases/KB_ID" -X DELETE
python3 scripts/api.py "/knowledgebases/KB_ID/restore" -X POST
```

**After KB changes, train the project to apply them.**

---

## Playbooks

Playbooks define how the AI assistant behaves — instructions, linked KBs, and model.

### List playbooks

```bash
python3 scripts/api.py "/projects/$STUDIO_PROJECT_ID/playbooks"
```

### Create playbook

```bash
python3 scripts/api.py \
  "/projects/$STUDIO_PROJECT_ID/playbooks" \
  -X POST --body '{
    "name": "Support Bot",
    "content": "You are a helpful support assistant.\n\nRules:\n- Be concise and friendly\n- Escalate billing disputes",
    "kb_ids": ["KB_ID_1", "KB_ID_2"]
  }'
```

### Update playbook (creates new version automatically)

```bash
python3 scripts/api.py "/playbooks/PLAYBOOK_ID" \
  -X PATCH --body '{"content": "Updated instructions..."}'
```

### Version management

```bash
# Get version history
python3 scripts/api.py "/playbooks/PLAYBOOK_ID/history"

# Get currently active version (uses base_id)
python3 scripts/api.py "/playbooks/BASE_ID/active"

# Set active version
python3 scripts/api.py "/playbooks/BASE_ID/active" \
  -X PUT --body '{"version_number": 3}'
```

### Playbook settings

```bash
# Enable/disable playbook (kill switch)
python3 scripts/api.py "/playbooks/PLAYBOOK_ID/settings" \
  -X PATCH --body '{"is_disabled": true}'

# Configure winback
python3 scripts/api.py "/playbooks/PLAYBOOK_ID/settings" \
  -X PATCH --body '{"winback_enabled": true, "winback_delay_minutes": 30}'
```

---

## Training

After modifying KBs, the project must be trained to apply changes.

```bash
# Train the project
python3 scripts/api.py "/projects/$STUDIO_PROJECT_ID/train" -X POST

# Check training status
python3 scripts/api.py "/jobs/JOB_ID"
```

---

## Schedule (Office Hours)

```bash
# Get current schedule
python3 scripts/api.py "/projects/$STUDIO_PROJECT_ID/schedule"

# Create schedule
python3 scripts/api.py \
  "/projects/$STUDIO_PROJECT_ID/schedule" \
  -X POST --body '{
    "name": "Business Hours",
    "timezone": "America/New_York",
    "enabled": true,
    "weekly_schedule": {
      "monday": {"start_time": "09:00", "end_time": "17:00", "is_available": true},
      "saturday": {"is_available": false},
      "sunday": {"is_available": false}
    }
  }'

# Add a holiday override
python3 scripts/api.py \
  "/projects/$STUDIO_PROJECT_ID/schedule/overrides" \
  -X POST --body '{"date": "2025-12-25", "label": "Christmas Day", "is_available": false}'
```

---

## API Tools

Custom HTTP integrations the assistant can call during conversations.

```bash
# List tools
python3 scripts/api.py "/projects/$STUDIO_PROJECT_ID/api-tools" --params include_playbook_usage=true

# Create tool
python3 scripts/api.py \
  "/projects/$STUDIO_PROJECT_ID/api-tools" \
  -X POST --body '{
    "name": "Check Order Status",
    "description": "Look up order status by order ID",
    "url": "https://api.example.com/orders/{order_id}",
    "method": "GET",
    "parameters": [
      {"name": "order_id", "type": "string", "description": "The order ID", "required": true}
    ]
  }'
```

---

## Project Settings

```bash
# Get settings
python3 scripts/api.py "/projects/$STUDIO_PROJECT_ID/settings"

# Update personality tone
python3 scripts/api.py "/projects/$STUDIO_PROJECT_ID/settings" \
  -X PATCH --body '{"personality_tone": "friendly"}'
```

Personality tones: `professional`, `friendly`, `casual`, `expert`, `playful`.

---

## Important Notes

- **KB status flow**: ADDED -> (train) -> ACTIVE. After edits: ACTIVE -> EDITED -> (train) -> ACTIVE.
- **Always train after KB changes**: Creating, updating, or deleting KBs requires retraining.
- **Playbook versioning**: Every update creates a new version. Use `active` endpoint to control which version is live.
- **base_id vs playbook_id**: Active version endpoints use `base_id` (stable across versions). Other endpoints use `playbook_id` (specific version).
- **Soft deletes**: Delete operations are soft — use restore to undo.
