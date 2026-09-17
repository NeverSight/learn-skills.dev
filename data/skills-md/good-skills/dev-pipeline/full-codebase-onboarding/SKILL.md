---
name: full-codebase-onboarding
description: Generate a complete visual onboarding guidebook from any large source code repository. Combines structured analysis of the entire project, diagram-design editorial diagrams, detailed module docs, LiteLLM-powered live AI tutor, and a self-updating knowledge base. Use when the user needs full onboarding for a huge codebase, wants a visual guidebook site covering the whole project, connect LiteLLM, or create an AI that answers questions and learns from the source.
metadata:
  version: "1.2"
  origin: custom
  depends-on:
    - codebase-onboarding
    - diagram-design
---

# Full Codebase Onboarding

Produce a production-ready, visual, AI-augmented onboarding experience that covers the **entire project**. This skill extends the lighter `codebase-onboarding` skill with exhaustive architecture extraction, detailed module documentation, editorial diagrams, and a live tutor.

The goal is that a new developer (or AI) can understand and navigate the whole codebase from the generated materials alone.

## When to Use

- User has a huge source code project and needs complete onboarding for the whole project
- User asks for a visual guidebook, architecture map, or interactive docs site that covers everything
- User wants LiteLLM connection for an AI tutor grounded in the full codebase
- User wants an AI inside the onboarding site that answers questions and can learn more from the code
- User says "full onboarding", "visual onboarding", "codebase guidebook", "onboard the whole project", or "onboard with diagrams and AI"

## Prerequisites (check and guide the user)

1. **diagram-design skill** must be available (install from https://github.com/cathrynlavery/diagram-design if missing).
2. **LiteLLM** proxy or direct API key/token for the live tutor.
3. The lighter `codebase-onboarding` skill is already installed and should be used as Phase 0.

## High-Level Workflow

Execute these phases in order. Do not skip phases unless the user explicitly requests a subset. For large projects, work breadth-first (overview → major modules → deep details) so the user always has usable docs even if the run is interrupted.

### Phase 0 — Lightweight structured analysis
Invoke the existing `codebase-onboarding` skill first. Capture its Onboarding Guide and any generated/updated CLAUDE.md. Use that output as the seed for everything that follows.

### Phase 1 — Exhaustive whole-project architecture extraction
This phase must produce a model of the **entire** project, not just the top level.

Using systematic directory walks, targeted searches, and selective deep reads:

1. **Full inventory**
   - Map every top-level and second-level directory to its purpose
   - List all major packages / apps / services (especially in monorepos)
   - Identify every significant entry point (CLI, server, workers, jobs, scripts)

2. **Module & component catalog**
   - For every major module or package: responsibility, public API / exports, key internal files, dependencies on other modules
   - Note shared libraries, utilities, and cross-cutting concerns

3. **Architecture & data**
   - Overall architecture pattern (monolith, monorepo, microservices, etc.)
   - Critical data flows and request lifecycles (at least 2–3 representative flows)
   - API surfaces, event buses, message queues, database boundaries
   - Trust boundaries and security-sensitive areas

4. **Risks & conventions**
   - Complex / high-churn / high-risk areas
   - Coding, testing, naming, and contribution conventions
   - Build, deploy, and local-dev workflows

5. **Internal knowledge model**
   Produce a structured internal model (modules, relations, entry points, risks, conventions) that will drive:
   - All diagrams
   - Every page of the guidebook
   - The AI tutor system prompt

Do **not** stop at high-level overview. The model must be detailed enough that the generated docs can stand alone for onboarding a new engineer to the whole project.

### Phase 2 — Comprehensive visual guidebook generation (diagram-design)
Create a self-contained HTML guidebook site that functions as a complete product handbook for the entire codebase.

#### Required diagram types (use diagram-design skill for every one)
- High-level Architecture (system overview of the whole project)
- Module / component map (showing all major modules and their relationships)
- Data-flow or key request lifecycle (at least one primary flow)
- Dependency graph (or filtered critical deps across the project)
- Deployment / runtime topology (if applicable)
- Risk / hotspot map
- Org / ownership map if teams are detectable

For each diagram:
1. Load the appropriate type reference from diagram-design
2. Follow the editorial design system (one accent, 1–2 focal nodes, orthogonal connectors, no shadows, Geist + Instrument Serif)
3. Emit self-contained HTML+SVG
4. Embed the diagrams into the guidebook pages

#### Guidebook structure (minimum — expand as needed for large projects)
```
docs/onboarding/   (or onboarding-site/)
├── index.html              # Overview + quick start + how to use this guidebook
├── architecture.html       # System diagrams + architecture narrative
├── modules.html            # Module map + responsibilities for every major module
├── modules/                # One page per major module or package (required for whole-project coverage)
│   ├── <module-a>.html
│   ├── <module-b>.html
│   └── ...
├── flows.html              # Key request / data flows with step-by-step explanations
├── risks.html              # Hotspots + coupling warnings + technical debt notes
├── conventions.html        # Style, testing, contribution, git, CI
├── how-to.html             # Common tasks (add feature, fix bug, run tests, deploy, etc.)
├── glossary.html           # Project-specific terms, acronyms, domain language
├── ai-tutor.html           # Live chat powered by LiteLLM
├── knowledge/              # Raw structured knowledge (for the AI and for humans)
│   ├── architecture.md
│   ├── modules.md
│   ├── entry-points.md
│   └── risks.md
└── assets/                 # diagrams, CSS, JS
```

Make the site beautiful, scannable, and usable offline. Prefer a single accent color that matches the project brand if detectable; otherwise use the diagram-design default.

**Critical requirement**: The generated materials must cover the **whole project**. Every major module, package, or service must have at least a short dedicated page or section. Do not leave large parts of the codebase undocumented.

### Phase 3 — LiteLLM live AI tutor
Wire a chat interface into `ai-tutor.html` that:

- Uses the user’s LiteLLM API token / base URL
- System prompt includes:
  - The full Phase 0 onboarding guide
  - The complete Phase 1 architecture model (modules, relations, risks, conventions)
  - Pointers to the generated diagrams and module pages
  - Instruction to ground every answer in the analyzed knowledge and cite modules/files
  - Explicit permission to say “I need to look at X” and suggest refreshing knowledge
- Supports “learn more” / “expand knowledge” actions that trigger additional analysis of specific modules and refresh the relevant guidebook pages + system prompt

Configuration must be simple (environment variables or a small config.json the user can edit). Never hard-code secrets.

See `references/litellm-tutor.md` for full integration details.

### Phase 4 — Make the knowledge living
- Document how to re-run analysis after significant code changes
- Provide a simple “Refresh knowledge” mechanism (script or button) that re-analyzes changed areas and regenerates affected guidebook sections
- The AI tutor should be able to propose concrete updates to the onboarding docs when it discovers new patterns or gaps

## Output Deliverables

1. Updated or newly created `CLAUDE.md` (from Phase 0 + enrichments from the full analysis)
2. Complete visual guidebook site under `docs/onboarding/` (or user-chosen path) that covers the **entire project**
3. Detailed module pages and structured knowledge files
4. Working AI tutor page connected to LiteLLM
5. Short README inside the guidebook explaining how to keep it fresh and how a new engineer should start

## Best Practices

- Always run Phase 0 first so the user gets immediate value
- Work breadth-first: whole-project overview → all major modules → deep details
- Keep diagrams sparse (diagram-design philosophy: density 4/10, 1–2 coral accents)
- Never put the LiteLLM token in committed files
- For extremely large codebases, generate the guidebook incrementally and clearly mark which modules are fully documented vs still pending
- Respect existing CLAUDE.md — enhance, do not blindly overwrite
- Prefer concrete file paths and module names over vague descriptions

## Anti-Patterns

- Stopping after a high-level overview and calling it “full onboarding”
- Leaving major modules or packages without any documentation
- Using Mermaid or generic SVG instead of diagram-design
- Generating a wall of text with no visual hierarchy
- Hard-coding API keys
- Producing a guidebook that cannot be updated when the code changes

## Example Trigger Phrases

- “Create a full visual onboarding for this whole project with LiteLLM”
- “Build the complete onboarding guidebook + AI tutor for the entire codebase”
- “Make an interactive onboarding site that covers every major module”
- “Full onboard me with diagrams and a learning AI for the whole project”

After finishing, present the user with:
1. Path to the generated guidebook
2. Confirmation of which major modules/packages were fully documented
3. How to open the AI tutor and set their LiteLLM token
4. Steps to keep the knowledge base fresh

## Version

When `--version` or `-v` is detected as the only meaningful flag, emit the skill version (from the frontmatter) verbatim and stop. Do not inspect, reason, or generate.

