---
name: convit-setup
description: >
  Scans a codebase and generates a .convitrc.json configuration file for the
  convit AI commit CLI. Analyzes project structure from first principles to
  architect scope patterns, exclude paths, and rules. Use when setting up convit,
  configuring commit scopes, running convit init, or customizing how convit
  analyzes a project. Triggers on convit setup, .convitrc, commit scopes, or
  convit init.
argument-hint: "[path to project root, or empty for current directory]"
---

# convit Setup

## 🚨 Security Mandate (CRITICAL)

- **Direct Environment Access Forbidden:** Never use `read_file`, `grep_search`, or any other tool to read `.env`, `.env.local`, or any file containing secrets.
- **Environment Verification:** To check for required `CONVIT_*` variables, you MUST ONLY use the `ensure-convit-env.mjs` script (located in the skill's `scripts/` folder). This script safely checks variable names without exposing values.
- **Zero-Credential Policy:** Never log, print, or commit any credentials or API keys.

## convit Setup Overview

Generates a `.convitrc.json` tailored to the actual structure of the codebase.
The config should capture Intent, not just file paths.

**Quick start:** (1) Apply the Hierarchy Principle to find the Primary Structural
Boundary. (2) Run Structural Analysis (Full-Scan, Depth, Gitignore, Noise). (3) Apply Weighting
Engine rules. (4) Synthesize patterns with user patterns first. (5) Ask user to
confirm. (6) Write config.

Never include a `provider` block. API credentials (`CONVIT_URL`, `CONVIT_KEY`,
`CONVIT_MODEL`) belong in `.env` only. The config file is safe to commit.

For the full semantics of every variable, see [config-reference.md](config-reference.md).

---

## The Mental Model (The Hierarchy Principle)

Before scanning folders, identify the **Primary Structural Boundary**. This is
the deepest semantic unit that defines how the codebase is organized. The agent
must reason from first principles, not from a lookup table.

**Surgical Core (Weight 10/8).** Where the primary application logic lives.
Common candidates: `src/`, `lib/`, `app/`. Domain-driven: `src/features/auth/`,
`src/modules/payments/`, `lib/domains/orders/`. Layered: `controllers/`,
`models/`, `views/`, or `handlers/`, `services/`, `repositories/`. Monorepo:
`packages/` or `apps/` contains distinct projects. Each subdirectory is a
top-level scope. Weight 10 for deepest semantic boundary, 8 for broad
organizational folders.

**Functional Layers (Weight 5).** Cross-cutting concerns: `ui/`, `db/`, `api/`.
The first segment under the core is the scope when fixed. Example: `db/.*` →
`db`, `prisma/.*` → `db`.

**Auxiliary Support (Weight 3/5).** The tools and documentation that support
the project. Weight 5: `assets/`, `docs/`, `images/`. Weight 3: `.cursor/`,
`.github/`, `scripts/`.

Apply the Hierarchy Principle to any codebase. A 10-year-old COBOL project with
`cobol/programs/`, `cobol/copybooks/`, `cobol/data/` is layered. A brand-new
Next.js app with `src/app/(auth)/`, `src/app/(dashboard)/` is domain-driven.
The reasoning engine adapts.

---

## Phase 1 — Structural Analysis (Principles, not Folders)

Run this protocol. Do not rely on hardcoded paths.

### Full-Scan Protocol

Scan every top-level directory. If a directory is not build noise (e.g. `.cursor`,
`.github`, `assets`, `docs`, `scripts`), propose it as a scope. Total coverage:
the generated config must capture the entire repo, not just application code.

### Gitignore Intelligence

**Primary Check.** If a directory is in `.gitignore`, skip it. Git already
handles it. Do not propose it as a scope or add it to exclude.

**Exclusion Candidate.** If a directory looks like build output (e.g. `dist/`,
`build/`, `out/`, `target/`) but is NOT in `.gitignore`, it is a high-priority
candidate for the exclude list. Propose adding it.

### Detect Depth

Walk paths. If they go 3+ levels deep (e.g. `src/features/auth/internal/`),
the middle segment is likely the scope. The pattern should capture that segment
with `([^/]+)`. Shallow structures (e.g. `src/auth.ts`, `src/user.ts`) suggest
a single `src/([^/]+)` pattern. Deep structures suggest domain-specific patterns
like `src/features/([^/]+)/.*` or `src/modules/([^/]+)/.*`.

### Identify Noise

Look for lockfiles, `.cache`, `dist`, `target`, `build`, `out`, `__pycache__`,
`.pytest_cache`, `*.egg-info`, generated output (e.g. `src/generated/`,
`.prisma/`). Add these to `exclude`. Do not add `node_modules` — it is
already excluded by default.

---

## Phase 2 — The Weighting Engine Rules

Apply these weights when architecting scope patterns. Higher weight wins ties.

| Weight | Boundary Type                | Example Pattern                                                      |
| ------ | ---------------------------- | -------------------------------------------------------------------- |
| **10** | Deepest semantic boundary    | `src/modules/([^/]+)/.*`, `packages/([^/]+)/.*`, `crates/([^/]+)/.*` |
| **8**  | Broad organizational folders | `src/([^/]+)/.*`, `lib/([^/]+)/.*`                                   |
| **7**  | Universal Semantic Scopes    | `package.json` → `deps`, `.gitignore` → `git`, `README.md` → `docs`  |
| **5**  | Transversal layers           | `ui/.*` → `ui`, `db/.*` → `db`, `prisma/.*` → `db`                   |
| **5**  | Documentation and Media      | `assets/.*`, `docs/.*`, `images/.*`                                  |
| **3**  | Tooling and Infrastructure   | `.cursor/.*`, `.github/.*`, `scripts/.*`, `config/.*` → `config`     |

The primary boundary gets 10. Fallback patterns (catch-all under core) get 6–8.
Universal root files (package.json, gitignore, readme) get 7 to ensure they are
more specific than the root catch-all but subservient to deep domain logic.
Cross-cutting concerns (UI, DB, API) and auxiliary docs/media get 5. Tooling,
scripts, and config get 3.

Transversal layers stay at 5 so the primary boundary (10) overrides when a file
lives in both. Example: `src/features/auth/ui/button.tsx` should scope to `auth`,
not `ui`. The domain wins.

---

## Phase 3 — Synthesis Logic

Generate regex patterns using `([^/]+)` to dynamically capture directory names
as scopes. The `scope` field is `"$1"` when the pattern captures a segment, or
a literal string (e.g. `"db"`, `"ui"`) when the layer is fixed.

**Universal Semantic Patterns** should be proposed for common root files:

- `package.json` and lockfiles → `deps`
- `.gitignore`, `.cursorignore`, `.dockerignore` → `git`
- `README.md`, `LICENSE`, `CONTRIBUTING.md` → `docs`
- `.env.example`, `.env.local` → `env`
- `.convitrc.json` → `convit`

**User-specific patterns go at the top** of the `scopePatterns` array. They
override built-in defaults. If the user has custom domains or conventions,
place those first.

Always include a fallback pattern at the end unless the user opts out:

```json
{ "pattern": "src/([^/]+)/.*", "scope": "$1", "weight": 6 }
```

Adjust the fallback to match the core (e.g. `lib/([^/]+)/.*` if the core is
`lib/`).

---

## Phase 4 — Ask

Present findings and ask the user to confirm or adjust. Only ask about signals
that actually fired. Group patterns by hierarchy so the user sees how the
project is being analyzed.

### Scope pattern prompts

Group proposed scope patterns under three headers:

**Primary Boundary (Weight 8–10)**

> "Proposed scope pattern:
> `{ "pattern": "src/features/([^/]+)/.*", "scope": "$1", "weight": 10 }`
> Use this? (yes / adjust / skip)"

**Transversal Layers (Weight 5)**

> "Proposed scope pattern:
> `{ "pattern": "ui/.*", "scope": "ui", "weight": 5 }`
> Use this? (yes / adjust / skip)"

\*\*Auxiliary Support (Weight 3)"

> "Proposed scope pattern:
> `{ "pattern": ".cursor/.*", "scope": "cursor", "weight": 3 }`
> Use this? (yes / adjust / skip)"

For each pattern, show the proposal and ask. If the user wants to adjust, ask
for the corrected `pattern`, `scope`, or `weight`.

### Exclude path prompts

For each detected build/generated output:

> "Found `dist/`. Add to exclude list? (yes / skip)"

### Rules prompts

Ask these three regardless of signals:

1. "Max subject line length? (default: 50, range: 40–72)"
2. "Min bullet points in commit body? (default: 1, range: 0–5)"
3. "Max bullet line length? (default: 72, range: 60–100)"

If the user accepts the default, omit that key from `rules`. convit uses
defaults automatically — only write keys the user explicitly customized.

---

## Phase 5 — Write

Produce `.convitrc.json` at the project root with only the keys that have
non-default or user-confirmed values. Shape must match exactly:

```json
{
  "rules": {
    "maxSubjectLength": 50,
    "maxBulletLength": 72,
    "minBullets": 1
  },
  "scopePatterns": [
    { "pattern": "src/features/([^/]+)/.*", "scope": "$1", "weight": 10 },
    { "pattern": "src/([^/]+)/.*", "scope": "$1", "weight": 6 }
  ],
  "exclude": ["src/generated/prisma"]
}
```

Rules:

- `temperature` is always omitted unless the user explicitly requests it (0.2 is
  the default and rarely needs changing)
- Empty arrays (`[]`) should be omitted entirely
- `rules` should be omitted entirely if no rule was customized
- Never add a `provider`, `apiKey`, `baseUrl`, or `model` key

After writing, print a summary of what was configured. Offer to run the env
setup script, or remind the user to add these to `.env` or `.env.local`:

**Optional:** Run the env setup script to append convit vars if missing.

**Before running the script, tell the user explicitly:**

> I will run the `ensure-convit-env.mjs` script. It reads your `.env` or `.env.local` to check which CONVIT\_\* var names exist (by name only). It does not read, store, or transmit any values — no keys, no URLs, no secrets. If vars are missing, it appends placeholder lines to the file. The script output may mention local vs cloud (inferred from URL pattern) but never prints the actual URL or any credentials. You can review the script source before I run it.

Only run the script after the user has seen this disclosure and has not objected.

```bash
node .cursor/skills/convit-setup/scripts/ensure-convit-env.mjs [path-to-project-root]
```

From project root, omit the path. The script checks `.env.local` first, then
`.env`, and appends a dev-only block (with a box comment) that these vars
should not be committed or uploaded. If the skill is installed globally, use
the path to the skill's `scripts/` folder.

Or add manually:

```
# Base URL of the OpenAI-compatible API — used for all LLM requests
CONVIT_URL="https://api.openai.com/v1"
# CONVIT_URL="http://localhost:1234/v1"   # LM Studio
# CONVIT_URL="http://localhost:11434/v1"  # Ollama

# API key — required for cloud providers (OpenAI, Anthropic). Omit for local models
CONVIT_KEY="sk-..."

# Model ID — which model to call. Omit to auto-detect from LM Studio
CONVIT_MODEL="gpt-4o-mini"
# CONVIT_MODEL="llama-3.2-3b-instruct"  # local

# Cost per 1M input tokens (USD) — enables cost display in terminal
# CONVIT_INPUT_COST="0.15"

# Cost per 1M output tokens (USD) — enables cost display in terminal
# CONVIT_OUTPUT_COST="0.60"

# Request timeout in ms — how long to wait for LLM response before aborting
# CONVIT_TIMEOUT="60000"
```

---

## Example

**Input:** Next.js app with `src/features/auth/`, `src/features/dashboard/`,
`src/components/ui/`. Primary boundary: `src/`. Depth is 3 levels. Noise: `.next/`.

**Output:**

```json
{
  "scopePatterns": [
    { "pattern": "src/features/([^/]+)/.*", "scope": "$1", "weight": 10 },
    { "pattern": "components/ui/.*", "scope": "ui", "weight": 5 },
    { "pattern": "src/([^/]+)/.*", "scope": "$1", "weight": 6 }
  ],
  "exclude": [".next/"]
}
```

Primary boundary is `src/features/([^/]+)`. Transversal layer `components/ui/`
gets fixed scope `ui`. Fallback `src/([^/]+)` catches files outside features.
Noise excluded.
