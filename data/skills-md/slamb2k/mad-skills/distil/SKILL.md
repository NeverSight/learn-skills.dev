---
name: distil
description: Generate multiple unique web design variations for any website or web application. Accepts site specifications from a file (--spec path) or pasted text block. Creates a Vite + React + TypeScript + Tailwind project with Bun and produces N different creative designs accessible at /1, /2, /3, etc. Use when prototyping or exploring design directions for any web interface.
argument-hint: <count> --port <port> [--spec <path>] [--favorites <1,2,3>]
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent, WebFetch, AskUserQuestion
---

# Distil - Design Variation Generator

When this skill is invoked, IMMEDIATELY output the banner below before doing anything else.
Pick ONE tagline at random — vary your choice each time.
CRITICAL: Reproduce the banner EXACTLY character-for-character. The first line of the art has 4 leading spaces — you MUST preserve them.

```
{tagline}

⠀   ██╗██████╗ ██╗███████╗████████╗██╗██╗
   ██╔╝██╔══██╗██║██╔════╝╚══██╔══╝██║██║
  ██╔╝ ██║  ██║██║███████╗   ██║   ██║██║
 ██╔╝  ██║  ██║██║╚════██║   ██║   ██║██║
██╔╝   ██████╔╝██║███████║   ██║   ██║███████╗
╚═╝    ╚═════╝ ╚═╝╚══════╝   ╚═╝   ╚═╝╚══════╝
```

Taglines:
- 🔥 Heating up the column...
- 🧪 Fractioning the design space!
- 💎 Condensing pure creativity!
- 🔬 Separating signal from noise!
- ⚗️ Extracting the essence!
- 🔄 Refining through iteration!
- ✨ Distilling N variations of brilliance!
- 🎨 From crude concept to pure design!

---

## Output Formatting

After the banner, display parsed input:
```
┌─ Input ────────────────────────────────────────
│  {Field}:  {value}
│  Flags:    {parsed flags or "none"}
└────────────────────────────────────────────────
```

Pre-flight results:
```
── Pre-flight ───────────────────────────────────
  ✅ {dep}           {version or "found"}
  ⚠️ {dep}           not found → {fallback detail}
  ❌ {dep}           missing → stopping
──────────────────────────────────────────────────
```

Stage/phase headers: `━━ {N} · {Name} ━━━━━━━━━━━━━━━━━━━━━━━━━`

Status icons: ✅ done · ❌ failed · ⚠️ degraded · ⏳ working · ⏭️ skipped

---

Generate multiple unique, creative web interface designs for any website or
web application. The primary agent acts as a thin orchestrator — all heavy
reading and file creation is delegated to subagents to protect the primary
context window.

## Arguments

Parse the following from the skill invocation:
- **count** (required): Number of designs to create (e.g., 5)
- **--spec** (optional): Path to a file containing site specification
- **--url** (optional): URL to existing site to review for context
- **--port** (required): Port for the Vite dev server
- **--favorites** (optional): Comma-separated list of design numbers for iteration mode

### Examples
```
/distil 5 --spec ./site-spec.md --port 5173
/distil 3 --favorites 2,4 --port 5173
```

If `--favorites` is provided, follow `references/iteration-mode.md` instead
of the steps below.

---

## Pre-flight

Before starting, check all dependencies in this table:

| Dependency | Type | Check | Required | Resolution | Detail |
|-----------|------|-------|----------|------------|--------|
| npm | cli | `npm --version` | yes | stop | https://bun.sh or use npm |
| bencium-innovative-ux-designer | skill | `~/.claude/skills/bencium-innovative-ux-designer/SKILL.md` | no | ask | `npx skills add bencium/bencium-claude-code-design-skill@bencium-innovative-ux-designer -g -y` |
| web-animation-design | skill | `~/.claude/skills/web-animation-design/SKILL.md` | no | ask | `npx skills add connorads/dotfiles@web-animation-design -g -y` |
| design-system | skill | `~/.claude/skills/design-system/SKILL.md` | no | ask | `npx skills add lobbi-docs/claude@design-system -g -y` |

For each row, in order:
1. Run the Check command (for cli/npm) or test file existence (for agent/skill)
2. If found: continue silently
3. If missing: apply Resolution strategy
   - **stop**: notify user with Detail, halt execution
   - **url**: notify user with Detail (install link), halt execution
   - **install**: notify user, run the command in Detail, continue if successful
   - **ask**: notify user, offer to run command in Detail, continue either way (or halt if required)
   - **fallback**: notify user with Detail, continue with degraded behavior
4. After all checks: summarize what's available and what's degraded

---

## Site Specification

The specification can be provided via:

1. **--spec flag**: Read the file at the provided path
2. **Pasted text**: Check conversation for a description of the site
3. **--url flag**: Use WebFetch to analyze an existing site

**If no specification is found, ask the user before proceeding.**

---

## Step 1: Load Site Specification

Parse and store the site context for use when generating each design.
This is the only file the primary agent reads directly (specs are typically small).

## Step 2: Reconnaissance (launch in parallel)

Launch two subagents **in parallel** to gather context without bloating
the primary agent.

### 2a: Verify Design Skills

Design skill availability is checked in the Pre-flight section above.
Use the results from pre-flight to populate SKILL_REPORT:
- For each design skill: name, installed (yes/no)
- If any skill was missing and the user declined to install, note it as unavailable

### 2b: Scan Existing Project

```
Task(
  subagent_type: "Explore",
  model: "haiku",
  description: "Scan existing design project",
  prompt: "Check if src/designs/ directory exists. If it does:
    1. List all DesignN.tsx files (glob for src/designs/Design*.tsx)
    2. For each file, read ONLY the first 10 lines to extract the
       metadata comment (style name, key traits)
    3. Determine the highest design number
    Return PROJECT_REPORT (max 20 lines):
    - project_exists: true/false
    - package_manager: detected from lockfile (bun.lockb/pnpm-lock/yarn.lock/package-lock)
    - design_count: N
    - highest_number: N
    - designs: list of (number, style_name) pairs
    If no src/designs/ directory, return project_exists: false."
)
```

### Parse Recon Results

From SKILL_REPORT: Gate on missing skills before proceeding.
From PROJECT_REPORT:
- If `project_exists`: set `START_INDEX = highest_number + 1`, skip Step 3
- If not: set `START_INDEX = 1`, proceed to Step 3

## Step 3: Initialize Project

**Skip this step if an existing project was detected in Step 2b.**

Launch **Bash subagent** (haiku) to set up the project:

```
Task(
  subagent_type: "Bash",
  model: "haiku",
  description: "Initialize distil project",
  prompt: "Follow the project setup instructions:
    1. Detect package manager (bun -> pnpm -> yarn -> npm)
    2. Create Vite React-TS project
    3. Install dependencies: tailwindcss, postcss, autoprefixer,
       react-router-dom, lucide-react
    4. Configure Tailwind (content paths, index.css directives)
    5. Copy {skill_dir}/assets/DesignNav.tsx to src/components/DesignNav.tsx
    Return SETUP_REPORT (max 10 lines): status, package_manager, errors."
)
```

Parse SETUP_REPORT. If setup fails, fall back through the package manager
chain (bun -> pnpm -> yarn -> npm).

## Step 4: Create Designs via Subagent

Launch a **general-purpose subagent** to create all new designs.

**CRITICAL**: The subagent reads skill files and design guides directly.
Do NOT read them in the primary agent — pass file paths only.

```
Task(
  subagent_type: "general-purpose",
  description: "Create design variations",
  prompt: "
    You are creating {COUNT} new web design variations for a distil project.

    ## Site Specification
    {SITE_SPEC from Step 1}

    ## Design Knowledge — Read These Files
    Load design principles and the 50+ style catalog from these skill files:
    - ~/.claude/skills/bencium-innovative-ux-designer/SKILL.md
    - ~/.claude/skills/bencium-innovative-ux-designer/MOTION-SPEC.md
    - ~/.claude/skills/web-animation-design/SKILL.md
    - ~/.claude/skills/design-system/SKILL.md
    - ~/.claude/skills/design-system/references/style-guide.md

    Also read the project design guide:
    - {skill_dir}/references/design-guide.md

    ## Existing Designs (avoid these styles)
    {Compact list from PROJECT_REPORT: number + style_name pairs,
     or 'None — fresh project'}

    ## Task
    Create designs numbered {START_INDEX} through {START_INDEX + COUNT - 1}.

    For each design, create `src/designs/Design{N}.tsx`:
    - Pick a DISTINCT style from the 50+ style catalog in the design-system skill
    - Do NOT reuse styles already used by existing designs
    - Apply the site specification to all content and sections
    - Follow anti-AI-slop rules strictly (no Inter, no default blue, no cookie-cutter layouts)
    - Include purposeful animations with proper easing
    - Each design must be self-contained in a single file
    - Import and render DesignNav from '../components/DesignNav'

    After creating all designs, update:
    1. `src/App.tsx` — Add import and route for EVERY design (existing + new)
    2. Each design file's DesignNav `designs` array — Include ALL designs (existing + new)

    ## Design File Requirements
    Each design file must have:
    - A metadata comment at the top: style name, key visual traits, color palette
    - Import DesignNav from '../components/DesignNav'
    - A `designs` array listing ALL designs (existing + new) with id and name
    - ALL sections from the site specification with realistic content
    - Custom color palette (not default Tailwind)
    - Animations with proper easing (ease-out for entrances, ease-in-out for movement)
    - Responsive layout (mobile-first)
    - Lucide React icons for iconography

    ## App.tsx Requirements
    The App.tsx must:
    - Import ALL design components (existing + new)
    - Have a route for each: <Route path='/{N}' element={<DesignN />} />
    - Default route redirects to /1

    Return DESIGN_REPORT (max 30 lines):
    - List each design created: number, style name, key visual traits
    - Total design count (existing + new)
    - Files created and modified
    - Any issues encountered
  "
)
```

Parse DESIGN_REPORT. If any design failed, report the error and offer retry.

## Step 5: Start Dev Server

Launch as a **background Bash** to avoid blocking the primary agent:

```
Task(
  subagent_type: "Bash",
  run_in_background: true,
  description: "Start Vite dev server",
  prompt: "{package_manager} run dev --port {PORT}"
)
```

If the dev server is already running, HMR should pick up the new files
automatically — skip this step.

## Step 6: Present Designs

Present the final summary:

```
┌─ Distil · Report ──────────────────────────────
│
│  ✅ Distil complete — {N} designs generated
│
│  🌐 Server: http://localhost:{PORT}
│
│  🎨 Designs
│     /1  {style name} — {key visual traits}
│     /2  {style name} — {key visual traits}
│     /3  {style name} — {key visual traits}
│     {mark new vs existing}
│
│  📊 Total: {total designs} ({new} new + {existing} existing)
│
│  ⚡ Next steps
│     1. Browse designs at http://localhost:{PORT}/1
│     2. Use --favorites 1,3 to iterate on selected designs
│
└─────────────────────────────────────────────────
```

## Context Protection Summary

| Step | Agent | Model | Why |
|---|---|---|---|
| 1: Load spec | Primary | — | Small file, needed for subagent prompt |
| 2a: Skill check | Explore | haiku | Avoids reading 2000+ lines of skill content |
| 2b: Project scan | Explore | haiku | Avoids reading existing design files |
| 3: Init project | Bash | haiku | Shell commands only |
| 4: Create designs | general-purpose | default | Heavy lifting: reads skills, writes files |
| 5: Dev server | Bash (background) | — | Non-blocking, no output in primary |
| 6: Present | Primary | — | User-facing, uses compact DESIGN_REPORT |

## Troubleshooting

- If package manager commands fail, try the next in the fallback chain
- If port is in use, suggest killing the process or using a different port
- If design imports fail, check file naming consistency
- If no site spec is found, always ask the user before proceeding
- If a design skill is missing, offer to install it before proceeding
- If the subagent fails, check error details and retry with adjusted parameters
