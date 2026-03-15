---
name: personalize-skills
description: Customize Operator Skills for your environment. Use when first installing skills or when you want to update your personal values.
---

# Personalize Skills

Walk through all customization points in your Operator Skills and set your personal values.

## When to Use

- After first installing Operator Skills
- When you want to update your personal info
- After updating to a new version of the skills

## How It Works

1. Scan all skills for `[YOUR_*]` placeholders
2. Ask you for each value (grouped by type)
3. Update all occurrences across all skills
4. Confirm what was changed

## Invocation

`/personalize-skills` — Full interactive setup
`/personalize-skills --list` — Just show what needs customizing
`/personalize-skills --reset` — Clear customizations (restore placeholders)

---

## Workflow

### Step 1: Scan for Placeholders

Scan `~/.claude/skills/` for all `[YOUR_*]` patterns.

Group by placeholder type:
```
Found 12 placeholders across 6 skills:

Identity:
  [YOUR_NAME] — used in 3 skills
  [YOUR_EMAIL] — used in 2 skills

Paths:
  [YOUR_CLOUD_PATH] — used in 2 skills
  [YOUR_KNOWLEDGE_ARCHIVE] — used in 1 skill

URLs:
  [YOUR_NOTION_URL] — used in 1 skill
```

### Step 2: Collect Values

For each placeholder, ask the user:

```
[YOUR_NAME]
Used in: coach, writeup, inbox-commander
Description: Your name for personalized interactions
Example: Danny

What's your name? > ___
```

Group related questions:
- All identity questions together
- All path questions together
- All URL questions together

### Step 3: Apply Changes

For each value provided:
1. Find all occurrences of the placeholder
2. Replace with the user's value
3. Track what was changed

```
Applying changes...

✓ [YOUR_NAME] → "Alex" in 3 files
  - coach/SKILL.md (2 occurrences)
  - writeup/SKILL.md (1 occurrence)
  - inbox-commander/references/known-senders.md (1 occurrence)

✓ [YOUR_EMAIL] → "alex@startup.com" in 2 files
  - inbox-commander/SKILL.md
  - inbox-commander/references/known-senders.md
```

### Step 4: Confirm

Show summary:
```
Personalization complete!

Values set: 5
Files updated: 8
Placeholders remaining: 2 (optional)

Optional placeholders not set:
- [YOUR_KNOWLEDGE_ARCHIVE] — Only needed if you have a personal knowledge base
- [YOUR_NOTION_URL] — Only needed if you use Notion

You can set these later by running /personalize-skills again.
```

---

## Placeholder Reference

Common placeholders and what they're for:

### Identity
| Placeholder | Description | Example |
|-------------|-------------|---------|
| `[YOUR_NAME]` | Your name | Alex |
| `[YOUR_EMAIL]` | Your email address | alex@company.com |
| `[YOUR_COMPANY]` | Your company name | Acme Inc |

### Paths
| Placeholder | Description | Example |
|-------------|-------------|---------|
| `[YOUR_CLOUD_PATH]` | Cloud storage folder | ~/Dropbox/ |
| `[YOUR_KNOWLEDGE_ARCHIVE]` | Personal knowledge base | ~/Documents/knowledge/ |
| `[YOUR_DRAFTS_FOLDER]` | Where to save drafts | ~/Documents/drafts/ |

### URLs
| Placeholder | Description | Example |
|-------------|-------------|---------|
| `[YOUR_NOTION_URL]` | Notion workspace URL | your-workspace.notion.site |

---

## Tips

### Skip optional placeholders
If a placeholder is marked optional, you can skip it. The skill will work without it.

### Update later
Run `/personalize-skills` again anytime to update your values.

### Back up first
Before personalizing, consider backing up your skills directory:
```bash
cp -r ~/.claude/skills ~/.claude/skills-backup
```

### Check the guide
See CUSTOMIZATION-GUIDE.md in the repo for detailed explanations of each placeholder.
