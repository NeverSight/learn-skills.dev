---
name: scan-project-structure
version: 1.0.0
description: '[Documentation] Scan project and populate/sync docs/project-reference/project-structure-reference.md with service architecture, ports, directory tree, tech stack, and module registry.'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/scan-and-update-reference-doc-protocol.md`
- `.claude/skills/shared/understand-code-first-protocol.md`

## Quick Summary

**Goal:** Scan the project codebase and populate `docs/project-reference/project-structure-reference.md` with accurate service architecture, API ports, directory tree, tech stack, and module codes.

**Workflow:**

1. **Read** — Load current target doc, detect init vs sync mode
2. **Scan** — Discover services, apps, ports, tech stack via parallel sub-agents
3. **Report** — Write findings to external report file
4. **Generate** — Build/update the reference doc from report
5. **Verify** — Spot-check paths and ports

**Key Rules:**

- Generic — discover everything dynamically, never hardcode project-specific values
- Use `docs/project-config.json` for hints if available, fall back to filesystem scanning
- All examples must reference real files found in this project

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Scan Project Structure

## Phase 0: Read & Assess

1. Read `docs/project-reference/project-structure-reference.md`
2. Detect mode: **init** (placeholder only) or **sync** (has real content)
3. If sync: note which sections exist and their line counts

## Phase 1: Plan Scan Strategy

Check if `docs/project-config.json` exists for module lists and service maps. Plan these scan areas:

- **Backend services** — Find `.csproj`, `Dockerfile`, `Program.cs`, `launchSettings.json` for ports
- **Frontend apps** — Find `angular.json`, `nx.json`, `package.json`, `vite.config`, `next.config`
- **Infrastructure** — Find `docker-compose.yml`, `Dockerfile`, K8s manifests, CI/CD config
- **Tech stack** — Parse `package.json` dependencies, `.csproj` PackageReferences, build tool configs

## Phase 2: Execute Scan (Parallel Sub-Agents)

Launch **3 Explore agents** in parallel:

### Agent 1: Backend Services

- Glob for `**/*.csproj` and `**/Dockerfile` to find services
- Grep `launchSettings.json` or `appsettings*.json` for port numbers
- Grep for `[ApiController]` or `MapControllers` to find API services
- List service directories with their ports

### Agent 2: Frontend Apps

- Glob for `**/angular.json`, `**/nx.json`, `**/package.json` (not in node_modules)
- Find app entry points (`main.ts`, `index.tsx`, `App.vue`)
- Extract dev server ports from configs (`serve` commands, proxy configs)
- Identify framework versions from package.json

### Agent 3: Infrastructure & Tech Stack

- Find `docker-compose*.yml` — extract service definitions and port mappings
- Find CI/CD configs (`.github/workflows/*.yml`, `azure-pipelines.yml`, `Jenkinsfile`)
- Parse primary package managers (`package.json`, `*.csproj`) for key dependencies
- Identify databases, message brokers, caching from connection strings or Docker services

Write all findings to: `plans/reports/scan-project-structure-{YYMMDD}-{HHMM}-report.md`

## Phase 3: Analyze & Generate

Read the report file. Build these sections:

### Target Sections

| Section                    | Content                                                                |
| -------------------------- | ---------------------------------------------------------------------- |
| **Service Architecture**   | Table: Service Name, Type (API/Worker/App), Port, Dockerfile path      |
| **Infrastructure Ports**   | Table: Service (DB/MQ/Cache), Port, Credentials (if in docker-compose) |
| **API Service Ports**      | Table: API service name, Port, Dockerfile path                         |
| **Project Directory Tree** | Top 2-3 levels of `src/` directory structure                           |
| **Tech Stack**             | Table: Category (Backend/Frontend/Infra), Technology, Version          |
| **Module Codes**           | Table: Module code abbreviation, Full name, Service path               |

### Content Rules

- Use tables for structured data (not prose)
- Include actual port numbers found in configs
- Directory tree: show only meaningful structure (skip node_modules, bin, obj)
- Tech stack: include version numbers from package.json/csproj

## Phase 4: Write & Verify

1. Write updated doc with `<!-- Last scanned: YYYY-MM-DD -->` at top
2. Verify: spot-check 3 service paths exist on filesystem
3. Verify: port numbers match actual config files
4. Report: sections updated vs unchanged

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using TaskCreate
- Always add a final review todo task to verify work quality and identify fixes/enhancements
