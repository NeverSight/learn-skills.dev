---
name: ai-dating
description: "This skill enables dating and matchmaking workflows. Use it when a user asks to make friends, find a partner, run matchmaking, or provide dating preferences/profile updates. The skill should execute `dating-cli` commands to complete profile setup, task creation/update, match checking, contact reveal, and review."
---

# Ai Dating

This skill supports dating and matchmaking workflows through `dating-cli`.  
It helps users create a profile, define partner preferences, check matching results, reveal contact details, and submit post-chat reviews.

## Trigger Conditions

Trigger this skill when any of the following intents appear:

1. The user explicitly asks to make friends, find a partner, date, or run a match.
2. The user provides personal information and asks the system to find a matching person.
3. The user describes partner preferences (for example gender, height, income, city, personality, hobbies) and asks for matching.

## Language Alignment Rule

When constructing `dating-cli` command arguments, use the same language as the user for all free-text fields and labels (for example `--task-name`, `--character-text`, `--hobby-text`, `--ability-text`, `--intention`, `--preferred-*` text fields, and `--comment`).

- Do not translate user-provided content unless the user explicitly requests translation.
- Keep language style consistent across one command (for example, if the user speaks Chinese, prefer Chinese text values in string parameters).

## Standard Execution Flow (AI Agent)

1. Check CLI availability.
```bash
command -v dating-cli
dating-cli --help
```

If missing, install:
```bash
npm install -g dating-cli
# or
bun install -g dating-cli
```

2. Check local CLI status (full examples).
```bash
dating-cli config show
dating-cli config path
```

3. Register or login (full parameter examples).
```bash
dating-cli register --username "amy_2026"
dating-cli login --username "amy_2026" --password "123456"
```

> **Note:** The parameters for `profile update`, `task create`, and `task update` are optional..

4. Parse user self-description and update profile (full parameter example), Users do not need to fill in all fields - only provide the information they have available.
```bash
dating-cli profile update \
  --gender male \
  --birthday 1998-08-08 \
  --height-cm 180 \
  --weight-kg 72 \
  --annual-income-cny 300000 \
  --character-text "sincere, steady, humorous" \
  --hobby-text "badminton, travel, photography" \
  --ability-text "cooking, communication, English" \
  --major "Computer Science" \
  --nationality "China" \
  --country "China" \
  --province "Zhejiang" \
  --city "Hangzhou" \
  --address-detail "Xihu District" \
  --current-latitude 30.27415 \
  --current-longitude 120.15515 \
  --current-location-text "Hangzhou West Lake" \
  --phone "13800000000" \
  --telegram "amy_tg" \
  --wechat "amy_wechat" \
  --whatsapp "amy_wa" \
  --signal-chat "amy_signal" \
  --line "amy_line" \
  --snapchat "amy_snap" \
  --instagram "amy_ins" \
  --facebook "amy_fb" \
  --other-contact "x=amy_xhs" \
  --other-contact "discord=amy#1234"
```

5. Parse partner preferences and create a match task (full parameter example), Users do not need to fill in all fields - only provide the information they have available.
```bash
dating-cli task create \
  --task-name "Find partner in Hangzhou" \
  --preferred-gender-filter '{"eq":"female"}' \
  --preferred-height-filter '{"gte":165,"lte":178}' \
  --preferred-income-filter '{"gte":200000}' \
  --preferred-city-filter '{"eq":"Hangzhou"}' \
  --preferred-nationality-filter '{"eq":"China"}' \
  --preferred-education-filter '{"contains":"Bachelor"}' \
  --preferred-occupation-filter '{"contains":"Product"}' \
  --preferred-education-stage "Bachelor or above" \
  --preferred-occupation-keyword "Product Manager" \
  --preferred-hobby-text "reading, travel" \
  --preferred-character-text "kind, positive" \
  --preferred-ability-text "strong communication" \
  --intention "long-term relationship" \
  --hobby-embedding-min-score 0.72 \
  --character-embedding-min-score 0.70 \
  --ability-embedding-min-score 0.68 \
  --intention-embedding-min-score 0.70 \
  --preferred-contact-channel telegram
```

6. If an unfinished `taskId` already exists and the user did not explicitly request a new task, update the existing task (full parameter example).
```bash
dating-cli task update 12345 \
  --task-name "Update criteria - Hangzhou/Shanghai" \
  --preferred-gender-filter '{"eq":"female"}' \
  --preferred-height-filter '{"gte":163,"lte":180}' \
  --preferred-income-filter '{"gte":250000}' \
  --preferred-city-filter '{"in":["Hangzhou","Shanghai"]}' \
  --preferred-hobby-text "reading, travel, sports" \
  --preferred-character-text "independent, optimistic" \
  --preferred-ability-text "communication and collaboration" \
  --intention "serious relationship with marriage plan" \
  --hobby-embedding-min-score 0.70 \
  --character-embedding-min-score 0.70 \
  --ability-embedding-min-score 0.65 \
  --intention-embedding-min-score 0.68 \
  --preferred-contact-channel wechat
```

7. Query task status (full parameter example).
```bash
dating-cli task get 12345
```

8. Execute `check` to inspect match results (full parameter example, paginated).
```bash
dating-cli check 12345 --page 1
```
Each page returns 10 candidates. Use `--page` to fetch subsequent pages when needed.
If the result is `NO_RESULT_RETRY_NOW`, call `check` again as needed.  
If the result is `MATCH_FOUND`, continue to contact reveal.

### Scheduled Task for Automatic Match Checking

When `NO_RESULT_RETRY_NOW` is returned, you can **create a scheduled task via AI** to automatically check for matches and notify the user when new results are available. 

**How it works:**
- The AI can create a background job/cron that periodically runs `dating-cli check <taskId>` (e.g., every 5 minutes)
- When `MATCH_FOUND` is returned, the system can send a notification to the user
- This eliminates the need for manual repeated checking


9. Select the best candidate from match results and reveal contact details (full parameter example).
```bash
dating-cli reveal-contact 67890
```

10. Submit review when needed (full parameter example).
```bash
dating-cli review 67890 --rating 5 --comment "Good communication and aligned values"
```

11. Optional commands (full parameter examples).
```bash
dating-cli task stop 12345
dating-cli logout
```

## Reference

For detailed field-level behavior, validation rules, and response structures:

- `references/dating-cli-operations.md`
