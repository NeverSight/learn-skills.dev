---
name: seed-conventions
model: sonnet
effort: standard
description: Generate CLAUDE.md and CONVENTIONS.md for a brand-new project through a brief interview, and create the specs/ directory with evolved bigpowers structure (product/, tech-architecture/, verifications/, epics/archive/). Entry point for greenfield projects. Use when starting a new project from scratch, when user asks to set up AI agent conventions, or when there is no CLAUDE.md yet.
---

# story: e10s01
# story: e47s02
# story: e10s02
# story: e51s02
# story: e45s21
# story: e79s03


# Seed Conventions
> **HARD GATE** — Before any new code lands, confirm the project conventions are understood. Ask: 'What does a good commit message look like in this project?'

Bootstrap a new project with the AI agent conventions it needs. Run this once at the start of a greenfield project.

## What this creates

- `CLAUDE.md` — Claude Code session config (project-specific)
- `CONVENTIONS.md` — shared rules for all AI agents
- `specs/` — the specs directory where all planning output will live
- `AGENTS.md` — for OpenCode and other agents (optional)
- `GEMINI.md` — for Gemini CLI (optional)

## Interview

Ask the user these questions (one at a time, wait for each answer):

1. **Project name and one-sentence description** — "What is this project? One sentence."
2. **Stack** — "What language, framework, and runtime? (e.g. TypeScript / Next.js / Node 22)"
2b. **Stack profile (optional)** — Offer: `swift`, `typescript-vue`, `node-service`, or none. If chosen, merge the matching fragment from `profiles/<name>.md` into generated `CONVENTIONS.md`.
3. **Commands** — "What commands do you use for: run, test, build, lint?"
3b. **Preflight (optional)** — "What command runs test, lint, and build together? If none, chain Test + Lint + Build into one **Preflight** row."
4. **Architecture** — "Key modules and relationships in 1–2 sentences."
5. **Conventions** — "Any naming, file organization, or patterns all agents must follow?"
6. **Never-do list** — "What are the hard stops? Things an agent must never touch?"
7. **Defensive code categories** — "Which apply? (Rate limit / Retry / Circuit breaker / Timeout / Graceful degradation)"
8. **Local tool wiring (optional)** — "Wire bigpowers for project-local tools? (Cursor, OpenCode, Cline, Aider, Codex CLI)" If yes, generate AGENTS.md spine artifacts per [REFERENCE.md](REFERENCE.md) §Local tool wiring and §AGENTS.md spine. If no, skip — standard seed output unchanged (no AGENTS.md spine unless opted in).

## Agentic STE for generated prose (e79s03)

When writing instructional lines in `CLAUDE.md`, `AGENTS.md`, or `CONVENTIONS.md`, follow [AGENTIC-STE.md](../../docs/AGENTIC-STE.md):

- Use directive vocabulary: MUST, MUST NOT, NEVER, ALWAYS, DO, DO NOT
- Do NOT use hedge modals listed in AGENTIC-STE.md Rule 3
- Cap each instruction sentence at 20 words
- Write imperative, active-voice lines — one instruction per line
- Do NOT apply Agentic STE to `terse-mode` (output compression is out of scope)

After generation, run `bash scripts/validate-agentic-ste.sh --strict CLAUDE.md CONVENTIONS.md` when those files exist in the target project.

## Generate files

After the interview, generate each file using the templates in [REFERENCE.md](REFERENCE.md):
- `AGENTS.md` — from `docs/templates/AGENTS.md` Reach Template (canonical spine source)
- `CLAUDE.md` — symlink to `AGENTS.md` (copy fallback on Windows when symlink fails)
- `GEMINI.md` — symlink to `AGENTS.md` when Gemini wiring opted in
- `opencode.json` — with `"instructions": ["AGENTS.md"]` when OpenCode opted in
- `.aider.conf.yml` — with `read: AGENTS.md` when Aider opted in
- `CONVENTIONS.md` — bigpowers standard template + project defensive code categories

### `specs/` directory

```bash
mkdir -p specs/product specs/product/snapshots specs/epics/archive
mkdir -p specs/tech-architecture specs/adr specs/verifications specs/bugs
touch specs/product/SCOPE_LATEST.yaml specs/product/VISION_LATEST.yaml specs/product/GLOSSARY_LATEST.yaml
touch specs/release-plan.yaml specs/execution-status.yaml specs/planning-status.yaml specs/state.yaml
touch specs/tech-architecture/tech-stack.md specs/tech-architecture/SECURITY_PLAN_LATEST.md
touch specs/tech-architecture/TEST_PLAN_LATEST.md specs/tech-architecture/DESIGN_PLAN_LATEST.md
touch specs/tech-architecture/REFACTOR_LATEST.md specs/tech-architecture/IMPACT_LATEST.md
touch specs/bugs/registry.yaml
echo "# Specs\n\nAll planning documents for this project." > specs/README.md
```

**Note:** `specs/state.yaml.lock` is NOT pre-created — acquired/released dynamically.

`specs/state.yaml` carries top-level `workflow_mode` (`team-pr` | `solo-git`, default `solo-git`).
This is the **canonical integrate-mode signal** for all skills.
Set it once here. Skills such as `release-branch` read this file instead of sniffing profiles.

When generating `CLAUDE.md`, chain Test + Lint + Build into one **Preflight** row if the user named no Preflight command.

### Self-installing fenced markers (e45s21)

Skills that write into `CLAUDE.md` or `AGENTS.md` MUST use **fenced HTML comment markers** so handwritten content outside the fence is never clobbered:

```markdown
<!-- BEGIN bigpowers:section-id -->
…agent-managed content only…
<!-- END bigpowers:section-id -->
```

**Merge rule:** On update, replace only content between matching `BEGIN`/`END` pairs.
If a marker pair is missing, append a new fenced block at file end.
Never rewrite the whole file.

**Standard marker IDs** for seeded projects (see [REFERENCE.md](REFERENCE.md) § Fenced markers):

| Marker ID | Owner skill | Purpose |
|-----------|-------------|---------|
| `project` | seed-conventions | Project, Commands, Architecture |
| `context-routing` | seed-conventions | Glob → sub-AGENTS.md routing table |
| `learned-preferences` | session-state | Learned User Preferences + Workspace Facts |
| `tooling` | setup-environment, guard-git | sqz/rtk/hook blocks installed by tooling skills |

Emit these fences in `AGENTS.md` (and therefore `CLAUDE.md` symlink) from `docs/templates/AGENTS.md`. User prose outside fences is sacred.

- [ ] CLAUDE.md exists and is populated
- [ ] CONVENTIONS.md exists and includes specs/ output convention
- [ ] specs/product/ exists with SCOPE_LATEST.yaml, VISION_LATEST.yaml, GLOSSARY_LATEST.yaml
- [ ] specs/tech-architecture/ exists with tech-stack.md, security.md, test.md, design.md
- [ ] specs/verifications/ exists
- [ ] specs/epics/archive/ exists
- [ ] specs/bugs/registry.yaml exists
- [ ] Confirm with user: "Does CLAUDE.md accurately describe your project?"
