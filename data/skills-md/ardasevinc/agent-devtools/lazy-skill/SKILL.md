---
name: lazy-skill
description: Browse and load skills on-demand from ~/.claude/lazy-skills/. Use when you need a skill that isn't always loaded.
argument-hint: [search query or blank to browse]
version: 1.0.0
---

# Lazy Skill Loader

On-demand skill loading to reduce context bloat. Skills in `~/.claude/lazy-skills/` are only read when explicitly requested.

## Index

Skills available for lazy loading (name: keywords - description):

- **threejs-skills** [collection]: threejs, 3d, webgl, graphics - "Three.js skills for 3D graphics (10 skills)"

<!-- Add more entries:
- **name**: keyword1, keyword2 - "Brief description"
- **name** [collection]: keywords - "Description" (for skill repos with multiple skills)
-->

## Behavior

### On Invocation

1. If `$ARGUMENTS` provided, filter index to matching keywords
2. If blank, show full index
3. **Always ask user** which skill to load before reading - never read all skills
4. Use Read tool to load the selected skill file

### Path Resolution

**Single skills** - try in order:
1. `~/.claude/lazy-skills/<name>.md`
2. `~/.claude/lazy-skills/<name>/SKILL.md`

**Collections** (marked with `[collection]` in index):
1. Read `~/.claude/lazy-skills/<name>/README.md` to show available skills
2. Ask user which specific skill to load
3. Read `~/.claude/lazy-skills/<name>/skills/<skill-name>/SKILL.md`

### After Loading

- Skill content is now in context
- Follow the loaded skill's instructions
- No separate "invoke" step - it's just knowledge now

## Adding Skills to Index

Edit this file's Index section:
```markdown
- **skillname**: keyword1, keyword2, keyword3 - "One-line description"
```

Then place the skill file at either:
- `~/.claude/lazy-skills/skillname.md` (single file)
- `~/.claude/lazy-skills/skillname/SKILL.md` (full skill folder, e.g., cloned repo)

## Examples

**Single skill:**
```
User: /lazy-skill stripe

Claude: Found 1 matching skill:
- **stripe**: payments, billing, checkout - "Stripe API operations"

Want me to load it?

User: yes

Claude: [Reads ~/.claude/lazy-skills/stripe.md]
Loaded stripe skill. What would you like to do?
```

**Collection:**
```
User: /lazy-skill threejs

Claude: Found 1 matching collection:
- **threejs-skills** [collection]: threejs, 3d, webgl - "Three.js skills (10 skills)"

Want me to show the available skills in this collection?

User: yes

Claude: [Reads ~/.claude/lazy-skills/threejs-skills/README.md]

Available skills in threejs-skills:
| Skill | Description |
|-------|-------------|
| threejs-fundamentals | Scene setup, cameras, renderer |
| threejs-geometry | Shapes, BufferGeometry, instancing |
| threejs-materials | PBR, shader materials |
... (7 more)

Which one should I load?

User: fundamentals

Claude: [Reads ~/.claude/lazy-skills/threejs-skills/skills/threejs-fundamentals/SKILL.md]
Loaded threejs-fundamentals. Ready to help with Three.js scene setup.
```

<instructions>$ARGUMENTS</instructions>
