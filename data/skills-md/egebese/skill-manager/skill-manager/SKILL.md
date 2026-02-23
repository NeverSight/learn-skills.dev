---
name: skill-manager
description: Detect project tech stack and disable irrelevant skills to save context window space. Use when the user says "manage skills", "optimize skills", "disable irrelevant skills", "skill manager", or asks which skills are relevant for this project.
---

# Skill Manager

Analyze the current project's tech stack and disable irrelevant globally-installed skills by injecting a bounded section into the project's CLAUDE.md.

## When to Use

- User says "manage skills", "optimize skills", "skill manager"
- User says "disable irrelevant skills" or "which skills do I need?"
- User says "clean up skills for this project"
- User says "re-enable all skills"
- At the start of a new project to reduce context window waste

## Quick Start

Run the Python analysis script if available, otherwise follow the manual workflow below.

## Step 1: Detect Project Tech Stack

Check for these files in the project root (current working directory):

| File | Stack Signal |
|------|-------------|
| `package.json` | Node.js — read for framework (next, react, vue, angular, svelte, etc.) |
| `Podfile` or `*.xcodeproj` | iOS/macOS native |
| `Package.swift` | Swift Package (iOS/macOS) |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `requirements.txt` / `pyproject.toml` / `setup.py` | Python |
| `Gemfile` | Ruby |
| `composer.json` | PHP |
| `build.gradle` / `build.gradle.kts` | Android/JVM |
| `pubspec.yaml` | Flutter/Dart |
| `Dockerfile` / `docker-compose.yml` | Containerized |
| `vercel.json` / `netlify.toml` | Jamstack deployment |
| `tsconfig.json` | TypeScript |
| `.swift` files in root/Sources | Swift CLI/Server |

Read `package.json` dependencies to identify frameworks:
- `next` -> Next.js
- `react` -> React
- `vue` -> Vue
- `@angular/core` -> Angular
- `svelte` -> Svelte
- `stripe` -> Payment processing
- `express` / `fastify` / `hono` -> Node server
- `tailwindcss` -> Tailwind CSS
- `remotion` -> Video/media processing

**Monorepo detection**: If the project has `packages/`, `apps/`, or a workspace config in package.json, scan subdirectories too and union all detected stacks.

**Empty project**: If no recognizable files are found, warn the user and keep all skills active.

## Step 2: Read Installed Skills

Read `~/.agents/.skill-lock.json` to get the list of all globally installed skills. For each skill, note:
- `name` (the key)
- `source` (GitHub repo)
- `skillPath` (where the SKILL.md lives)

## Step 3: Score Each Skill

Assign each skill to a tier based on the detected tech stack.

### Tier Definitions

| Tier | Score Range | Meaning |
|------|------------|---------|
| **essential** | 80-100 | Directly relevant to detected stack |
| **useful** | 40-79 | Cross-platform utility, may be used |
| **irrelevant** | 0-39 | Wrong platform/domain entirely |
| **universal** | N/A | Never disabled regardless of stack |

### Universal Skills (NEVER disable these)

```
find-skills, skill-creator, writing-skills, brainstorming,
writing-plans, test-driven-development, dispatching-parallel-agents,
subagent-driven-development, using-superpowers, agentation, skill-manager
```

### Domain Mapping

**iOS/macOS Native Skills** — essential when Swift/Xcode detected:
- `mobile-ios-design` (iOS UI/SwiftUI)
- `asc-xcode-build` (Xcode build/archive)
- `asc-metadata-sync` (App Store metadata)
- `asc-localize-metadata` (App Store localization)
- `asc-subscription-localization` (IAP localization)
- `asc-ppp-pricing` (territory pricing)
- `asc-shots-pipeline` (screenshot automation)
- `asc-notarization` (macOS notarization)
- `app-store-optimization` (ASO)
- `aso-full-audit`, `aso-optimize`, `aso-competitor`, `aso-prelaunch`, `aso`

**Web/SaaS Marketing Skills** — essential when web framework detected:
- `page-cro`, `signup-flow-cro`, `onboarding-cro`, `popup-cro`, `form-cro`
- `copywriting`, `copy-editing`, `content-strategy`
- `seo-audit`, `programmatic-seo`, `schema-markup`
- `analytics-tracking`, `ab-test-setup`
- `email-sequence`, `social-content`
- `marketing-ideas`, `marketing-psychology`
- `free-tool-strategy`, `launch-strategy`
- `paid-ads`, `referral-program`
- `pricing-strategy`, `competitor-alternatives`
- `audit-website`

**Payment Skills** — essential when stripe/payment dependency detected:
- `stripe-integration`
- `paywall-upgrade-cro`
- `churn-prevention`

**Media/AI Generation Skills** — essential when media dependencies detected:
- `fal-audio`, `fal-generate`, `fal-image-edit`, `fal-platform`, `fal-upscale`, `fal-workflow`
- `remotion-best-practices`

### Cross-Domain Rules

- **Marketing skills** are scored "useful" (50) in non-web projects — users sometimes do marketing from any project
- **Stripe/payment** skills are "useful" (50) unless stripe is in dependencies, then "essential" (90)
- **ASO skills** are "essential" (95) for iOS, "irrelevant" (10) for non-mobile
- **fal-* skills** are "irrelevant" (10) unless media processing detected
- **asc-* skills** are "irrelevant" (5) for non-Apple projects
- **remotion-best-practices** is "essential" (90) if remotion is in dependencies, "irrelevant" (10) otherwise

## Step 4: Check for Overrides

If `.claude/skill-manager.json` already exists, read the `overrides` section:

```json
{
  "overrides": {
    "forceEnable": ["seo-audit"],
    "forceDisable": ["fal-audio"]
  }
}
```

- `forceEnable`: Move these skills to "essential" tier regardless of scoring
- `forceDisable`: Move these skills to "irrelevant" tier regardless of scoring

## Step 5: Generate `.claude/skill-manager.json`

Create the `.claude/` directory if it doesn't exist. Write the analysis file:

```json
{
  "version": 1,
  "generatedAt": "2026-02-23T12:00:00Z",
  "detectedStack": {
    "primary": "Next.js",
    "languages": ["TypeScript", "JavaScript"],
    "frameworks": ["Next.js", "React", "Tailwind CSS"],
    "platforms": ["Web"],
    "signals": {
      "package.json": true,
      "tsconfig.json": true,
      "next.config.ts": true
    }
  },
  "skills": {
    "page-cro": { "tier": "essential", "score": 95, "reason": "Web CRO directly applicable" },
    "mobile-ios-design": { "tier": "irrelevant", "score": 5, "reason": "No iOS stack detected" }
  },
  "disabled": ["mobile-ios-design", "asc-xcode-build"],
  "enabled": ["page-cro", "stripe-integration"],
  "universal": ["find-skills", "brainstorming"],
  "overrides": {
    "forceEnable": [],
    "forceDisable": []
  },
  "stats": {
    "total": 53,
    "essential": 20,
    "useful": 10,
    "irrelevant": 12,
    "universal": 11
  }
}
```

## Step 6: Update CLAUDE.md

### If "re-enable all" was requested:
1. Remove the `<!-- SKILL-MANAGER:START -->` ... `<!-- SKILL-MANAGER:END -->` block from CLAUDE.md
2. Delete `.claude/skill-manager.json`
3. Confirm to user: "All skills re-enabled."
4. Stop here.

### Normal flow:

Build the injection block:

```markdown
<!-- SKILL-MANAGER:START -->
## Disabled Skills

The following skills are **not relevant** to this project and should be **ignored** (do not invoke them):

- `mobile-ios-design` — No iOS stack detected
- `asc-xcode-build` — No Xcode project detected
- ...

**Stack**: Next.js / TypeScript / React / Tailwind CSS
**Last analyzed**: 2026-02-23
**Re-run**: Say "manage skills" or "/skill-manager" to re-analyze
**Re-enable all**: Say "re-enable all skills" to remove this section
<!-- SKILL-MANAGER:END -->
```

### Injection rules:

1. **Read** the current CLAUDE.md (or note it doesn't exist)
2. **If markers exist**: Replace everything between `<!-- SKILL-MANAGER:START -->` and `<!-- SKILL-MANAGER:END -->` (inclusive) with the new block
3. **If no markers**: Append the block to the end of CLAUDE.md with a blank line separator
4. **If no CLAUDE.md**: Create it with only the skill-manager block

**IMPORTANT**: Do NOT modify any other content in CLAUDE.md. Only touch the bounded marker section.

## Step 7: Suggest New Skills (Optional)

If the detected stack suggests skills that aren't installed, mention them:

> Based on your Next.js project, you might also want:
> - `npx skills find nextjs` for Next.js-specific skills
> - `npx skills find react` for React patterns

Only suggest if there's a clear gap. Don't overwhelm with suggestions.

## Step 8: Report Summary

Print a summary table:

```
Skill Manager Analysis Complete

Stack: Next.js / TypeScript / React
Total skills: 53
  Essential: 20 (kept active)
  Useful: 10 (kept active)
  Irrelevant: 12 (disabled in CLAUDE.md)
  Universal: 11 (always active)

Disabled skills written to CLAUDE.md
Full analysis: .claude/skill-manager.json
```

## Automated Mode (Python Script)

If Python 3.9+ is available, you can run the analysis script for faster, deterministic results:

```bash
python3 skills/skill-manager/scripts/analyze_project.py --analyze "$(pwd)"
```

Or just detect the stack:

```bash
python3 skills/skill-manager/scripts/analyze_project.py --detect-stack "$(pwd)"
```

The script path is relative to where the skill is installed. Find it via:
```bash
# The skill is installed at ~/.agents/skills/skill-manager/
python3 ~/.agents/skills/skill-manager/scripts/analyze_project.py --analyze "$(pwd)"
```

The script outputs JSON to stdout. Use the output to populate `.claude/skill-manager.json` and the CLAUDE.md injection block.

If Python is not available, follow the manual steps above — they produce the same result.

## Idempotency

- Running this skill multiple times is safe
- The CLAUDE.md section is replaced, never duplicated
- The JSON file is overwritten with fresh analysis
- User overrides in the JSON are preserved across re-runs

## Edge Cases

- **Monorepo**: Union all detected stacks from subdirectories. More skills stay enabled.
- **Empty project**: Keep all skills active. Warn user: "No stack detected."
- **New skills installed since last run**: Automatically picked up on re-run.
- **Skill uninstalled**: Removed from disabled list on re-run.
- **CLAUDE.md has other content**: Only the marker-bounded section is touched.
