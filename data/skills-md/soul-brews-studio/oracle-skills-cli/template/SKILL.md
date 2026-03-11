---
name: template
description: Skill template with Bun Shell pattern. Copy this folder to create new skills.
---

# /template - Skill Template

Copy this folder to create a new skill.

## Usage

```
/your-skill [args]
```

## Step 0: Timestamp

```bash
date "+🕐 %H:%M %Z (%A %d %B %Y)"
```

## Step 1: Run Script

```bash
bun scripts/main.ts "$ARGUMENTS"
```

Or fallback (if Bun not available):
```bash
npx tsx scripts/main.ts "$ARGUMENTS"
```

## Step 2: Process Output

Display results from script.

---

## Creating a New Skill

1. Copy `_template/` folder
2. Rename to your skill name
3. Update `SKILL.md`:
   - Change `name:` in frontmatter
   - Change `description:` in frontmatter
   - Update usage instructions
4. Edit `scripts/main.ts` with your logic
5. Test locally with `bun scripts/main.ts`

## File Structure

```
your-skill/
├── SKILL.md          ← Instructions for Claude
└── scripts/
    └── main.ts       ← Bun Shell logic
```

## Frontmatter Required

```yaml
---
name: your-skill-name
description: One line description. Use when user says "X", "Y", or "Z".
---
```

**Note**: Description is the trigger signal. Include action words and use cases.

---

ARGUMENTS: $ARGUMENTS
