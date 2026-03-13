---
name: zeabur-template-backup
description: Use when backing up a Zeabur template to git. Use when user provides a Zeabur template URL like zeabur.com/templates/XXXXXX. Use when user says "save this template", "backup template", or "download template YAML".
---

# Zeabur Template Backup

> **Always use `npx zeabur@latest` to invoke Zeabur CLI.** Never use `zeabur` directly or any other installation method. If `npx` is not available, install Node.js first.

Backup an online Zeabur template to the local git repository with standardized naming.

## When to Use

- User provides a Zeabur template URL (e.g., `https://zeabur.com/templates/85IQXQ`)
- User asks to backup/save a Zeabur template
- User wants to create a local copy of an online Zeabur template

## Repository Location

```
/Users/can/Documents/zeabur/zeabur-template/
```

## Naming Convention

```
{service-name}/zeabur-template-{service-name}-{TEMPLATE_CODE}.yaml
```

**Examples:**
- `elasticsearch-kibana/zeabur-template-elasticsearch-kibana-85IQXQ.yaml`
- `dify/zeabur-template-dify-1D4DOW.yaml`
- `postiz/zeabur-template-postiz-v2.12-X2L3BE.yaml`

## How to Download Template YAML

Zeabur templates can be directly downloaded by appending `.yaml` to the template URL:

```
https://zeabur.com/templates/{TEMPLATE_CODE}.yaml
```

**Example:**
- Template page: `https://zeabur.com/templates/1D4DOW`
- YAML download: `https://zeabur.com/templates/1D4DOW.yaml`

Use `curl` to download:

```bash
curl -sL https://zeabur.com/templates/{TEMPLATE_CODE}.yaml -o output.yaml
```

## Step-by-Step

### 1. Extract Template Code from URL

URL format: `https://zeabur.com/templates/{TEMPLATE_CODE}`

Example: `https://zeabur.com/templates/85IQXQ` → Code is `85IQXQ`

### 2. Download YAML and Extract Template Name

```bash
# Download YAML
curl -sL https://zeabur.com/templates/{TEMPLATE_CODE}.yaml -o /tmp/template.yaml

# Extract template name from YAML metadata.name field
grep -A1 'metadata:' /tmp/template.yaml | grep 'name:' | head -1
```

### 3. Derive Service Name

- Convert template name to lowercase kebab-case
- Example: "Elasticsearch Single Node with Kibana" → `elasticsearch-kibana`
- Keep it short and descriptive

### 4. Create Directory and Save

```bash
REPO=/Users/can/Documents/zeabur/zeabur-template

# Create directory
mkdir -p $REPO/{service-name}

# Move YAML with naming pattern
mv /tmp/template.yaml $REPO/{service-name}/zeabur-template-{service-name}-{TEMPLATE_CODE}.yaml
```

### 5. Git Commit

```bash
cd $REPO
git add {service-name}/
git commit -m "feat({service-name}): add {Template Name} template"
```

### 6. Push (if requested)

```bash
git push
```

## Quick Reference

| Step | Action |
|------|--------|
| 1 | Extract template code from URL |
| 2 | Download YAML via `curl -sL .../{CODE}.yaml` |
| 3 | Read template name from YAML `metadata.name` |
| 4 | Derive kebab-case service name |
| 5 | Save to `{service-name}/zeabur-template-{service-name}-{CODE}.yaml` |
| 6 | Git commit with conventional format |
| 7 | Push if user requests |

## Common Issues

| Issue | Solution |
|-------|----------|
| curl returns HTML instead of YAML | Verify the template code is correct |
| Template name has special chars | Use simple kebab-case for directory |
| Already exists | Compare with existing file, update if needed |

## See Also

- `zeabur-template` — template YAML reference and editing guide
