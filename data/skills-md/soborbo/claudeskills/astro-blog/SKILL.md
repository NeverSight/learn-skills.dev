---
name: astro-blog
description: Orchestrator for 5-phase blog article creation workflow
---

# Astro Blog - Workflow Orchestrator

This skill orchestrates a 5-phase workflow for creating SEO-optimized blog articles.

---

## 5-Phase Workflow

Use these skills in sequence:

### Phase 1: Research
**Skill:** `astro-blog-research`
**What:** SEO & intent research, keyword targeting, SERP analysis
**Output:** Intent type, primary keyword, unique angle, CTA type, pillar/cluster designation

### Phase 2: Structure
**Skill:** `astro-blog-structure`
**What:** Content outline, component placement, linking strategy
**Output:** Full outline with H2s, components, links, images, CTAs

### Phase 3: Write
**Skill:** `astro-blog-write`
**What:** Write article with human voice, featured snippet optimization
**Output:** Full article draft with citations and intentional imperfections

### Phase 4: Technical
**Skill:** `astro-blog-technical`
**What:** Frontmatter, schema markup, performance optimization
**Output:** Complete frontmatter, schema, performance settings

### Phase 5: Validate
**Skill:** `astro-blog-validate`
**What:** Quality checks, readability scores, performance audit
**Output:** All checks passed, ready to publish

---

## How to Use

**Option 1 - Full workflow:**
1. Start with `astro-blog-research`
2. Then `astro-blog-structure`
3. Then `astro-blog-write`
4. Then `astro-blog-technical`
5. Finally `astro-blog-validate`

**Option 2 - Jump to specific phase:**
- Already have research? Start with `astro-blog-structure`
- Already have outline? Start with `astro-blog-write`
- Article written? Start with `astro-blog-technical`
- Need validation only? Use `astro-blog-validate`

---

## When to Use Each Skill

| Situation | Use This Skill |
|-----------|----------------|
| Starting new article from scratch | `astro-blog-research` |
| Have keyword, need outline | `astro-blog-structure` |
| Have outline, need to write | `astro-blog-write` |
| Article written, need technical setup | `astro-blog-technical` |
| Article complete, need validation | `astro-blog-validate` |

---

## Reference Files

All skills are self-contained. Read detailed references only for edge cases:

- `references/CHECKLIST.md` - Complete checklist (all phases)
- `references/human-voice.md` - AI pattern avoidance
- `references/seo-intent.md` - Skyscraper, SERP strategies
- `references/content-structure.md` - Component examples
- `references/writing-rules.md` - Advanced formatting
- `references/technical.md` - Complex schema, monitoring
- `references/validation.md` - Detailed criteria
- `references/visual-design.md` - Component styling
