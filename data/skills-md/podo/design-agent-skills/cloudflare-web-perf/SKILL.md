---
name: cloudflare-web-perf
description: |
  Audit Core Web Vitals and render-blocking resources. Official Cloudflare skill
  for identifying and fixing LCP, INP, CLS, TTFB issues with Cloudflare-specific
  optimization strategies.
triggers:
  - "web performance"
  - "Core Web Vitals"
  - "LCP"
  - "CLS"
  - "INP"
  - "render blocking"
  - "cloudflare performance"
das:
  category: accessibility-quality
  upstream: "https://github.com/cloudflare/skills"
  upstream_path: "skills/web-perf/SKILL.md"
  version: latest
  install: true
---

# cloudflare-web-perf

> Catalogue stub — full skill: [cloudflare/skills](https://github.com/cloudflare/skills/blob/main/skills/web-perf/SKILL.md)

## Decision tree

1. **Is the full skill already installed?**
   Check whether the skill at this location still has a `das:` block:
   - Global: `grep -q "^das:" ~/.agents/skills/cloudflare-web-perf/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - Project: `grep -q "^das:" .agents/skills/cloudflare-web-perf/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - No `das:` block → full skill installed, invoke it and proceed
   - `das:` block present → go to step 2

2. **Detect scope, then install:**

   To detect scope:
   ```bash
   [ -e ~/.agents/skills/cloudflare-web-perf ] && echo "global" || echo "project"
   ```

   **Global** (installed with `-g`):
   ```bash
   npx skills add cloudflare/skills --skill cloudflare-web-perf -g -y
   ```

   **Project** (installed without `-g`):
   ```bash
   npx skills add cloudflare/skills --skill cloudflare-web-perf -y
   ```
   > **Claude Code:** send either command as a chat message starting with `!` to run it without leaving the conversation.


## Invoke after install

- Skill name: `cloudflare-web-perf`
- Trigger phrases: "web performance", "Core Web Vitals", "LCP", "CLS", "render blocking"

## What it does

Official Cloudflare skill for auditing and fixing Core Web Vitals — LCP (Largest Contentful Paint), INP (Interaction to Next Paint), CLS (Cumulative Layout Shift), and TTFB. Identifies render-blocking resources, unoptimized images, and layout instability causes. Includes Cloudflare-specific fixes using Workers, Cache Rules, and Image Optimization.
