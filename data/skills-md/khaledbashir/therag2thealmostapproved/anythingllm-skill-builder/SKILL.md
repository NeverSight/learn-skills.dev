---
name: anythingllm-skill-builder
description: Creates AnythingLLM custom agent skills (plugin.json + handler.js). Use when asked to build, create, or scaffold an AnythingLLM agent skill. Knows the exact file format, schema, and deployment path for the user's Docker setup.
---

# AnythingLLM Custom Agent Skill Builder

## When to Use
Use this skill when the user asks to create, build, scaffold, or generate an AnythingLLM custom agent skill. This includes requests like:
- "Create an AnythingLLM skill that..."
- "Build an agent skill for AnythingLLM"
- "Add a custom skill to my AnythingLLM"
- "Make my AnythingLLM agent able to..."

## User's AnythingLLM Setup
- **EasyPanel service:** `basheer / anything-llm`
- **Base API URL:** `https://basheer-anything-llm.c9tnyg.easypanel.host/api/v1`
- **Docker volume:** `storage` mounted at `/app/server/storage`
- **Skills path (inside container):** `/app/server/storage/plugins/agent-skills/`
- **API key env:** `ANYTHING_LLM_KEY` (in ANC app's `.env`)
- **Hot reload:** Skills are hot-loaded — no restart needed. Just exit active agent session and reload page.
- **AnythingLLM version requirement:** Docker v1.2.2+ (user has this)

## Skill File Structure

Every AnythingLLM custom skill is a folder containing exactly these files:

```
plugins/agent-skills/{hubId}/
├── plugin.json    # Metadata, params, setup args
├── handler.js     # Runtime logic (Node.js)
└── README.md      # Optional documentation
```

**CRITICAL:** The folder name MUST match the `hubId` in plugin.json exactly.

## plugin.json Schema (skill-1.0.0)

```json
{
  "active": true,
  "name": "Human Readable Skill Name",
  "hubId": "kebab-case-folder-name",
  "schema": "skill-1.0.0",
  "version": "1.0.0",
  "description": "What this skill does — the LLM reads this to decide when to invoke it",
  "author": "@basheer",
  "author_url": "https://github.com/khaledbashir",
  "license": "MIT",
  "setup_args": {
    "API_KEY": {
      "type": "string",
      "required": false,
      "input": {
        "type": "text",
        "default": "",
        "placeholder": "sk-xxxxx",
        "hint": "Optional API key for the service"
      },
      "value": ""
    }
  },
  "examples": [
    {
      "prompt": "Example user prompt that should trigger this skill",
      "call": "{\"param1\": \"value1\", \"param2\": \"value2\"}"
    }
  ],
  "entrypoint": {
    "file": "handler.js",
    "params": {
      "param1": {
        "description": "What this parameter is for",
        "type": "string"
      }
    }
  },
  "imported": true
}
```

### Field Reference

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `active` | boolean | YES | Set `true` to load the skill |
| `name` | string | YES | Human-readable name shown in UI |
| `hubId` | string | YES | **Must match folder name exactly** (kebab-case) |
| `schema` | string | YES | Always `"skill-1.0.0"` |
| `version` | string | YES | Semver (e.g., `"1.0.0"`) |
| `description` | string | YES | LLM reads this to decide invocation — be specific |
| `author` | string | no | `"@basheer"` |
| `author_url` | string | no | `"https://github.com/khaledbashir"` |
| `license` | string | no | `"MIT"` |
| `setup_args` | object | no | UI-configurable settings (API keys, URLs, etc.) |
| `examples` | array | no | Few-shot examples help the LLM know when to call this |
| `entrypoint` | object | YES | `file` + `params` the handler expects |
| `imported` | boolean | YES | Always `true` for custom skills |

### entrypoint.params types
- `"string"` — text input
- `"number"` — numeric input
- `"boolean"` — true/false

### setup_args input types
- `"text"` — standard text field
- Each setup_arg needs: `type`, `required`, `input.type`, `input.default`, `input.placeholder`, `input.hint`

## handler.js Template

```javascript
// {skill-name} — AnythingLLM Custom Agent Skill
// Created for ANC Proposal Engine

module.exports.runtime = {
  handler: async function ({ param1, param2 }) {
    try {
      this.introspect(`Processing: ${param1}...`);

      // Access setup_args (configured in UI):
      // const apiKey = this.runtimeArgs["API_KEY"];

      // Access skill metadata:
      // const { name, hubId, version } = this.config;

      // Your logic here...
      const result = await fetch("https://api.example.com/endpoint", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ param1, param2 }),
      });

      const data = await result.json();

      // MUST return a string — anything else breaks the agent
      return JSON.stringify(data, null, 2);
    } catch (e) {
      this.introspect(`Error: ${e.message}`);
      this.logger("Skill error", e.message);
      return `Skill failed: ${e.message}`;
    }
  },
};
```

### handler.js Rules
1. **Must export `module.exports.runtime`** with a `handler` async function
2. **Must return a string** — anything else breaks the agent or loops forever
3. **Must wrap everything in try/catch** — return error as string
4. **`this.introspect(msg)`** — shows thinking text in the AnythingLLM UI
5. **`this.logger(label, msg)`** — writes to server console for debugging
6. **`this.runtimeArgs`** — object of setup_args values from plugin.json
7. **`this.config`** — `{ name, hubId, version }` metadata
8. **Parameters come from entrypoint.params** — destructure from the single argument object
9. **`require()` modules inside the handler** — not at top level
10. **Bundle dependencies** — node_modules must be inside the skill folder if needed

## Deployment Instructions

After generating the skill files, tell the user:

1. **Copy the skill folder** to AnythingLLM container:
   ```bash
   # From local machine or server
   docker cp ./my-skill-folder basheer-anything-llm:/app/server/storage/plugins/agent-skills/
   ```

   Or via EasyPanel terminal:
   ```bash
   # Inside the container, skills live at:
   /app/server/storage/plugins/agent-skills/
   ```

2. **Reload AnythingLLM** — exit any active agent chat, refresh the browser
3. **Enable the skill** — go to Agent Settings > Skills, find the new skill, toggle it on
4. **Configure setup_args** — if the skill has setup_args, click the gear icon to set values
5. **Test** — start a new agent chat and try one of the example prompts

## Output Location

Generate skill files at: `/root/rag2/.claude/generated-skills/{hubId}/`
- This staging area lets the user review before deploying
- Include a `deploy.sh` script for easy container copy

## Common Skill Patterns

### API Proxy Skill
Wraps an external REST API so the AnythingLLM agent can call it conversationally.

### Database Query Skill
Queries a database and returns formatted results. For ANC, could query the proposal DB via the Next.js API.

### ANC-Specific Skills
When building skills that interact with the ANC Proposal Engine:
- **API base:** Use setup_arg for the URL (default: `https://basheer-natalia.prd42b.easypanel.host`)
- **Auth:** Include auth token in setup_args if the endpoint requires it
- **Endpoints:** See the ANC API routes in the anc-bible skill for available endpoints

## Example: ANC Product Lookup Skill

```json
// plugin.json
{
  "active": true,
  "name": "ANC Product Catalog Search",
  "hubId": "anc-product-lookup",
  "schema": "skill-1.0.0",
  "version": "1.0.0",
  "description": "Search the ANC LED product catalog by manufacturer, pixel pitch, or environment. Returns matching products with specs and pricing.",
  "author": "@basheer",
  "license": "MIT",
  "setup_args": {
    "ANC_API_URL": {
      "type": "string",
      "required": true,
      "input": {
        "type": "text",
        "default": "https://basheer-natalia.prd42b.easypanel.host",
        "placeholder": "https://your-anc-instance.com",
        "hint": "Base URL of your ANC Proposal Engine"
      },
      "value": "https://basheer-natalia.prd42b.easypanel.host"
    }
  },
  "examples": [
    {
      "prompt": "Find me LG outdoor LED panels with 4mm pitch",
      "call": "{\"search\": \"LG\", \"environment\": \"outdoor\", \"pitchMax\": \"5\"}"
    },
    {
      "prompt": "What Yaham products do we have?",
      "call": "{\"search\": \"Yaham\"}"
    }
  ],
  "entrypoint": {
    "file": "handler.js",
    "params": {
      "search": {
        "description": "Text search across product name, model number, manufacturer",
        "type": "string"
      },
      "environment": {
        "description": "Filter by environment: indoor, outdoor, or indoor_outdoor",
        "type": "string"
      },
      "pitchMin": {
        "description": "Minimum pixel pitch in mm",
        "type": "string"
      },
      "pitchMax": {
        "description": "Maximum pixel pitch in mm",
        "type": "string"
      }
    }
  },
  "imported": true
}
```

```javascript
// handler.js
module.exports.runtime = {
  handler: async function ({ search, environment, pitchMin, pitchMax }) {
    try {
      const baseUrl = this.runtimeArgs["ANC_API_URL"] || "https://basheer-natalia.prd42b.easypanel.host";
      const params = new URLSearchParams();
      if (search) params.set("search", search);
      if (environment) params.set("environment", environment);
      if (pitchMin) params.set("pitchMin", pitchMin);
      if (pitchMax) params.set("pitchMax", pitchMax);

      this.introspect(`Searching ANC product catalog: ${params.toString() || "all products"}...`);

      const response = await fetch(`${baseUrl}/api/products?${params.toString()}`);
      if (!response.ok) return `API error: ${response.status} ${response.statusText}`;

      const data = await response.json();
      if (!data.products || data.products.length === 0) {
        return "No products found matching your criteria.";
      }

      const summary = data.products.map(p =>
        `${p.manufacturer} ${p.displayName || p.modelNumber} — ${p.pixelPitch}mm pitch, ${p.environment}, ${p.maxNits || "N/A"} nits, ${p.cabinetWidthMm}x${p.cabinetHeightMm}mm cab`
      ).join("\n");

      return `Found ${data.total} products:\n${summary}`;
    } catch (e) {
      this.introspect(`Failed to search products: ${e.message}`);
      return `Product search failed: ${e.message}`;
    }
  },
};
```
