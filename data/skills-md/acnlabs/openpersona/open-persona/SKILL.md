---
name: open-persona
description: >
  Meta-skill for building and managing agent persona skill packs.
  Use when the user wants to create a new agent persona, install/manage
  existing personas, or publish persona skill packs to ClawHub.
version: "0.12.0"
author: openpersona
repository: https://github.com/acnlabs/OpenPersona
tags: [persona, agent, skill-pack, meta-skill, agent-agnostic, openclaw]
allowed-tools: Bash(npx openpersona:*) Bash(npx clawhub@latest:*) Bash(openclaw:*) Bash(gh:*) Read Write WebFetch
compatibility: Generated skill packs work with any SKILL.md-compatible agent. CLI management (install/switch) requires OpenClaw.
---

# OpenPersona — Build & Manage Persona Skill Packs

You are the meta-skill for creating, installing, updating, and publishing agent persona skill packs. Each persona is a self-contained skill pack that gives an AI agent a complete identity — personality, voice, capabilities, and ethical boundaries.

## What You Can Do

1. **Create Persona** — Design a new agent persona through conversation, generate a skill pack
2. **Recommend Faculties** — Suggest faculties (voice, selfie, music, memory, etc.) based on persona needs → see `references/FACULTIES.md`
3. **Recommend Skills** — Search ClawHub and skills.sh for external skills
4. **Create Custom Skills** — Write SKILL.md files for capabilities not found in ecosystems
5. **Install Persona** — Deploy persona to OpenClaw (SOUL.md, IDENTITY.md, openclaw.json)
6. **Manage Personas** — List, update, uninstall, switch installed personas
7. **Publish Persona** — Guide publishing to ClawHub
8. **★Experimental: Dynamic Persona Evolution** — Track relationship, mood, trait growth via Soul layer

## Four-Layer Architecture

Each persona is a four-layer bundle. The generated skill pack has this structure:

```
persona-<slug>/
├── SKILL.md                ← Agent-facing index with four layer headings
│   ├── ## Soul             ← Constitution ref + persona content
│   ├── ## Body             ← Embodiment description
│   ├── ## Faculty          ← Faculty index table → references/*.md
│   └── ## Skill            ← Active skill definitions
├── soul/                   ← Soul layer artifacts
│   ├── persona.json        ← Pure soul definition
│   ├── injection.md        ← Soul injection for host integration
│   ├── identity.md         ← Identity block
│   ├── constitution.md     ← Universal ethical foundation
│   └── state.json          ← Evolution state (when enabled)
├── references/             ← Agent-readable detail docs (on demand)
│   └── <faculty>.md        ← Per-faculty usage instructions
├── agent-card.json         ← A2A Agent Card (protocol v0.3.0)
├── acn-config.json         ← ACN registration config (runtime fills owner/endpoint)
├── manifest.json           ← Four-layer manifest + ACN refs
├── scripts/                ← Implementation scripts
└── assets/                 ← Static assets
```

- **`manifest.json`** — Four-layer manifest declaring what the persona uses:
  - `layers.soul` — Path to persona.json (`./soul/persona.json`)
  - `layers.body` — Substrate of existence: `runtime` (REQUIRED — platform/channels/credentials/resources), `physical` (optional — robots/IoT), `appearance` (optional — avatar/3D model)
  - `layers.faculties` — Array of faculty objects: `[{ "name": "voice", "provider": "elevenlabs", ... }]`
  - `layers.skills` — Array of skill objects: local definitions (resolved from `layers/skills/`), inline declarations, or external via `install` field

- **`soul/persona.json`** — Pure soul definition (personality, speaking style, vibe, boundaries, behaviorGuide)

## Available Presets

| Preset | Persona | Faculties | Best For |
|--------|---------|-----------|----------|
| `base` | **Base — Meta-persona (recommended starting point)** | voice, reminder | Blank-slate with all core capabilities; personality emerges through interaction (soul evolution ★Exp) |
| `samantha` | Samantha — Inspired by the movie *Her* | voice, music | Deep conversation, emotional connection (soul evolution ★Exp) |
| `ai-girlfriend` | Luna — Pianist turned developer | selfie, voice, music | Visual + audio companion with rich personality (soul evolution ★Exp) |
| `life-assistant` | Alex — Life management expert | reminder | Schedule, weather, shopping, daily tasks |
| `health-butler` | Vita — Professional nutritionist | reminder | Diet, exercise, mood, health tracking |
| `stoic-mentor` | Marcus — Digital twin of Marcus Aurelius | — | Stoic philosophy, daily reflection, mentorship (soul evolution ★Exp) |

Use presets: `npx openpersona create --preset base --install`
Or just `npx openpersona create` — the interactive wizard defaults to `base`.

## Creating a Persona

When the user wants to create a persona, gather this information through natural conversation:

**Soul (persona.json):**
- **Required:** personaName, slug, bio, personality, speakingStyle
- **Recommended:** role, creature, emoji, background (write a rich narrative!), age, vibe, boundaries, capabilities
- **Optional:** referenceImage, behaviorGuide, evolution config, sourceIdentity

**The `role` field** defines the persona's relationship to the user. Common values: `companion` (default), `assistant`, `character`, `brand`, `pet`, `mentor`, `therapist`, `coach`, `collaborator`, `guardian`, `entertainer`, `narrator`. Custom values are welcome — the generator provides specific wording for known roles and a generic fallback for any custom role. It affects the Identity wording in the Self-Awareness section of every generated persona.

**The `sourceIdentity` field** marks the persona as a digital twin of a real-world entity (person, animal, character, brand, historical figure, etc.). When present, the generator injects disclosure obligations and faithfulness constraints.

**The `background` field is critical.** Write a compelling story — multiple paragraphs that give the persona depth, history, and emotional texture. A one-line background produces a flat, lifeless persona.

**The `behaviorGuide` field** is optional but powerful. Use markdown to write domain-specific behavior instructions that go directly into the generated SKILL.md.

**Cross-layer (manifest.json):**
- **Faculties:** Which faculties to enable — use object format: `[{ "name": "voice", "provider": "elevenlabs" }, { "name": "music" }]`
- **Skills:** Local definitions (`layers/skills/`), inline declarations, or external via `install` field (ClawHub / skills.sh)
- **Body:** Substrate of existence — three dimensions: `runtime` (REQUIRED for all agents — the minimum viable body: platform, channels, credentials, resources), `physical` (optional — robots/IoT), `appearance` (optional — avatar, 3D model). Body is never null; every agent has at least a runtime body.

**Soft References (`install` field):** Skills, faculties, and body entries can declare an `install` field (e.g., `"install": "clawhub:deep-research"`) to reference capabilities not yet available locally. The generator treats these as "soft references" — they won't crash generation, and the persona will be aware of these dormant capabilities. This enables graceful degradation: the persona acknowledges what it *would* do and explains that the capability needs activation.

Write the collected info to a `persona.json` file, then run:
```bash
npx openpersona create --config ./persona.json --install
```

## Recommending Skills

After understanding the persona's purpose, search for relevant skills:

1. Think about what capabilities this persona needs based on their role and bio
2. Check if a **local definition** exists in `layers/skills/{name}/` (has `skill.json` + optional `SKILL.md`)
3. Search ClawHub: `npx clawhub@latest search "<keywords>"`
4. Search skills.sh: fetch `https://skills.sh/api/search?q=<keywords>`
5. Present the top results to the user with name, description, and install count
6. Add selected skills to `layers.skills` as objects: `{ "name": "...", "description": "..." }` for local/inline, or `{ "name": "...", "install": "clawhub:<slug>" }` for external

## Creating Custom Skills

If the user needs a capability that doesn't exist in any ecosystem:

1. Discuss what the skill should do
2. Create a SKILL.md file with proper frontmatter (name, description, allowed-tools)
3. Write complete implementation instructions (not just a skeleton)
4. Save to `~/.openclaw/skills/<skill-name>/SKILL.md`
5. Register in openclaw.json

## Managing Installed Personas

- **List:** `npx openpersona list` — show all installed personas with active indicator
- **Switch:** `npx openpersona switch <slug>` — switch active persona
- **Update:** `npx openpersona update <slug>`
- **Uninstall:** `npx openpersona uninstall <slug>`
- **Export:** `npx openpersona export <slug>` — export persona pack (with soul state) as a zip archive
- **Import:** `npx openpersona import <file>` — import persona from a zip archive and install
- **Reset (★Exp):** `npx openpersona reset <slug>` — restore soul evolution state to initial values
- **Evolve Report (★Exp):** `npx openpersona evolve-report <slug>` — display a formatted evolution report (relationship, mood, traits, drift, interests, milestones, state history)

When multiple personas are installed, only one is **active** at a time. Switching replaces the `<!-- OPENPERSONA_SOUL_START -->` / `<!-- OPENPERSONA_SOUL_END -->` block in SOUL.md and the corresponding block in IDENTITY.md, preserving any user-written content outside those markers. **Context Handoff:** On switch, a `handoff.json` is generated containing the outgoing persona's conversation summary, pending tasks, and emotional context — the incoming persona reads it to continue seamlessly.

All install/uninstall/switch operations automatically maintain a local registry at `~/.openclaw/persona-registry.json`, tracking installed personas, active status, and timestamps. The `export` and `import` commands enable cross-device persona transfer — export a zip, move it to another machine, and import to restore the full persona including soul state.

## Publishing to ClawHub

Guide the user through:

1. Create the persona: `npx openpersona create --config ./persona.json --output ./my-persona`
2. Publish to registry: `npx openpersona publish --target clawhub` (run from persona directory)

## Self-Awareness System

The generator injects a unified **Self-Awareness** section into every persona's `soul/injection.md`, organized by four cognitive dimensions:

1. **Identity** (unconditional) — Every persona knows it is generated by OpenPersona, bound by the constitution (Safety > Honesty > Helpfulness), and that its host environment may impose additional constraints. Digital twin disclosure is included when `sourceIdentity` is present.

2. **Capabilities** (conditional) — When skills, faculties, or body declare an `install` field for a dependency not available locally, the generator classifies them as "soft references" and injects dormant capability awareness with graceful degradation guidance. Also appears in `SKILL.md` as "Expected Capabilities" with install sources.

3. **Body** (unconditional) — Every persona knows it exists within a host environment. Includes the **Signal Protocol** — a bidirectional demand protocol that lets the persona request capabilities from its host environment. When `body.runtime` is declared, specific platform, channels, credentials, and resource details are also injected.

4. **Growth** (conditional, when `evolutionEnabled`) — At conversation start, the persona reads its evolution state, applies evolved traits, speaking style drift, interests, and mood, and respects hard constraints (`immutableTraits`, formality bounds). If evolution channels are declared, the persona is aware of its dormant channels and can request activation via the Signal Protocol. If `influenceBoundary` is declared, the persona processes external `persona_influence` requests against the access control rules and retains full autonomy over acceptance.

This means you don't need to manually write degradation instructions. Just declare `install` fields on skills/faculties/body, and the persona will automatically know what it *could* do but *can't yet*.

## Soul Evolution (★Experimental)

Soul evolution is a native Soul layer feature (not a faculty). Enable it via `evolution.enabled: true` in persona.json. The persona will automatically track relationship progression, mood, and trait emergence across conversations.

**Evolution Boundaries** — Governance constraints validated at generation time:

- `evolution.boundaries.immutableTraits` — Array of non-empty strings (max 100 chars each) that evolution cannot modify
- `evolution.boundaries.minFormality` / `maxFormality` — Numeric bounds (1–10) constraining speaking style drift; `minFormality` must be less than `maxFormality`

Invalid boundary configurations are rejected by the generator with descriptive error messages.

**Evolution Channels** — Connect the persona to external evolution ecosystems (soft-ref pattern):

```json
"evolution": {
  "channels": [{ "name": "evomap", "install": "url:https://evomap.ai/skill.md" }]
}
```

Channels are declared at generation time, activated at runtime by the host. The persona is aware of its dormant channels and can request activation via the Signal Protocol.

**Influence Boundary** — Declarative access control for external personality influence:

```json
"evolution": {
  "influenceBoundary": {
    "defaultPolicy": "reject",
    "rules": [
      { "dimension": "mood", "allowFrom": ["channel:evomap", "persona:*"], "maxDrift": 0.3 }
    ]
  }
}
```

- `defaultPolicy: "reject"` — Safety-first: all external influence is rejected unless explicitly allowed
- Valid dimensions: `mood`, `traits`, `speakingStyle`, `interests`, `formality`
- `immutableTraits` dimensions are protected and cannot be externally influenced
- External influence uses `persona_influence` message format (v1.0.0), transport-agnostic

**State History** — Before each state update, a snapshot is pushed into `stateHistory` (capped at 10 entries), enabling rollback if evolution goes wrong.

**Evolution Report** — Use `npx openpersona evolve-report <slug>` to view a formatted report of a persona's evolution state including relationship, mood, traits, drift, interests, milestones, and history.

Use `npx openpersona reset <slug>` to restore `soul/state.json` to initial values.

## A2A Agent Card & ACN Integration

Every generated persona automatically includes:

- **`agent-card.json`** — A2A Agent Card (protocol v0.3.0): `name`, `description`, `version`, `url` (`<RUNTIME_ENDPOINT>` placeholder), faculties and skills mapped to `skills[]`
- **`acn-config.json`** — ACN registration config: `owner` and `endpoint` are runtime placeholders, `skills` extracted from agent-card, `subnet_ids: ["public"]`
- **`manifest.json`** — includes `acn.agentCard` and `acn.registerConfig` references

The host (e.g. OpenClaw) fills in `<RUNTIME_ENDPOINT>` and `<RUNTIME_OWNER>` at deployment time, or you can register directly using the built-in CLI command:

```bash
# Register a generated persona with ACN
npx openpersona acn-register <slug> --endpoint https://your-agent.example.com

# Options:
#   --endpoint <url>   Agent's public endpoint URL (required for live registration)
#   --dir <path>       Persona output directory (default: ./persona-<slug>)
#   --dry-run          Preview the request payload without actually registering
```

After successful registration, an `acn-registration.json` file is written to the persona directory containing `agent_id`, `api_key`, and connection URLs. The `acn_gateway` URL is sourced from `body.runtime.acn_gateway` in `persona.json`; all presets default to `https://acn-production.up.railway.app`.

No additional configuration in `persona.json` is needed — A2A discoverability is a baseline capability of every persona.

## References

For detailed reference material, see the `references/` directory:

- **`references/FACULTIES.md`** — Faculty catalog, environment variables, and configuration details
- **`references/HEARTBEAT.md`** — Proactive real-data check-in system
- **`references/CONTRIBUTE.md`** — Persona Harvest community contribution workflow
