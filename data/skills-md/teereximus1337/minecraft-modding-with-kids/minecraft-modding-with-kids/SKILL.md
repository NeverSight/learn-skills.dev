---
name: minecraft-modding-with-kids
description: Complete onboarding and workflow for parents teaching kids to code through Minecraft modding. Sets up Fabric mod development on Mac/Linux, configures ElevenLabs voice explanations for the child, extracts correct 1.21.11 class mappings, and manages interactive coding sessions. Use when the user mentions Minecraft modding, teaching kids to code, Fabric mods, or setting up a modding environment. Triggers on "minecraft mod", "teach my kid", "modding with kids", "fabric setup", "set up minecraft", "let's build a mod".
---

# Minecraft Modding with Kids

A complete workflow for parents teaching kids to code through Minecraft modding with AI assistance and voice explanations.

## First Run: Onboarding

If no `AGENTS.md` exists in the workspace, run the onboarding flow.

### Step 1: Interview the Parent

Ask 2-3 questions at a time. Gather:

**Batch 1:**
1. Child's first name
2. Child's age
3. Child's reading/complexity level: (A) can't read code at all, (B) can read simple words, (C) reads well but doesn't understand code

**Batch 2:**
4. Child's Minecraft experience: creative mode only / survival / both
5. What would excite the kid most for a first mod? (custom sword, funny TNT, new animal, something else)
6. Any content to avoid? (realistic weapons, scary mobs, etc.)

**Batch 3:**
7. Parent's coding experience: none / understands basics / experienced developer
8. ElevenLabs API key (required -- explain: "This lets the AI talk to your kid out loud so they don't need to read scrolling code. Get a key at elevenlabs.io > Profile > API Keys")
9. ElevenLabs voice ID (or "default" to use a standard voice -- they can browse voices at elevenlabs.io/voice-library)

### Step 2: Derive Configuration

From the answers, generate these values:
- `CHILD_NAME`: from answer 1
- `CHILD_AGE`: from answer 2
- `READING_LEVEL`: none / basic / intermediate (from answer 3)
- `MOD_ID`: lowercase, no spaces, derived from child's name (e.g., "gus" → "gusmods")
- `MOD_DISPLAY_NAME`: e.g., "Gus's Awesome Mods"
- `PARENT_EXPERIENCE`: none / basic / experienced
- `CONTENT_GUIDELINES`: generated from answer 6
- `ELEVENLABS_API_KEY`: from answer 8
- `ELEVENLABS_VOICE_ID`: from answer 9
- `EXPLANATION_DEPTH`: derived from age + reading level:
  - Age 4-5 or reading=none: 3-5 sentences, zero jargon, pure analogies
  - Age 6-8 or reading=basic: 5-8 sentences, introduce "rules" and "numbers" concepts
  - Age 9-12 or reading=intermediate: 8-12 sentences, use simplified code terminology

### Step 3: Environment Setup

Run `scripts/onboard.sh` with the derived MOD_ID. This script:
1. Checks OS (macOS or Linux)
2. Installs JDK 21 (Homebrew on Mac, apt on Linux)
3. Installs deno (for Fabric CLI)
4. Generates a Fabric mod project via `deno run -A https://fabricmc.net/cli init <MOD_ID> -y`
5. Builds the project once (`./gradlew build`)
6. Initializes git

If any step fails, show the error and ask the parent to fix it before continuing.

### Step 4: Extract Class Mappings

Run `scripts/extract-mappings.sh` inside the mod project. This:
1. Runs `./gradlew genSources` to decompile Minecraft 1.21.11
2. Finds the sources JAR in `.gradle/loom-cache/`
3. Extracts all key class names and writes them to a reference file

The bundled `references/class-mappings-1.21.11.md` is a fallback if extraction fails.

### Step 5: Generate Workspace Files

Run `scripts/generate-workspace.sh` with a JSON config of all interview answers. This creates:
- `AGENTS.md` in the workspace root (from `assets/agents-md-template.md`)
- Agent rules in `.cursor/rules/` (from `assets/rules/` templates) -- or equivalent for other agents
- An `audio/` directory for voice output
- A `.gitignore` covering build artifacts, audio output, and secrets

### Step 6: Configure ElevenLabs via Zapier MCP

The recommended approach is to add ElevenLabs as an action inside a Zapier MCP server. This avoids installing a separate MCP server and works across all agents.

1. Go to [mcp.zapier.com](https://mcp.zapier.com) and create/sign in to an account
2. Enable the **ElevenLabs** app and the **Convert Text to Speech** action
3. Connect the parent's ElevenLabs account when prompted
4. Copy the Zapier MCP server URL

Then add the Zapier MCP to the agent config:

**Cursor** (`.cursor/mcp.json`):
```json
{
  "zapier": {
    "url": "{{ZAPIER_MCP_URL}}",
    "headers": {}
  }
}
```

**Claude Code** (`~/.claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "zapier": {
      "url": "{{ZAPIER_MCP_URL}}",
      "headers": {}
    }
  }
}
```

For other agents, provide the URL and ask the parent to add it to their MCP config.

To generate voice, call the Zapier MCP:
- tool: `execute_write_action`
- app: `elevenlabs`
- action: `text_to_speech`
- params: `text`, `voice_id`, `model_id` (`eleven_flash_v2_5`), `output_format` (`mp3_44100_128`)
- The result is an S3 URL. Download with `curl -sL <URL> -o audio/explanation.mp3`, then play with `open` (macOS) or `xdg-open` (Linux).

### Step 7: Create Starter Mod

Generate a simple first item (a custom sword or tool based on answer 5) so the child sees something immediately in their first session. Include all required files: Java class, registration, model JSON, client item JSON, lang entry, and a placeholder texture.

Build it, launch Minecraft, and celebrate.

---

## Session Modes

### Mode: Session Start

Triggered when parent says "session time", "let's build", "[child name] is here", or starts a new conversation.

1. Determine phase: prep (parent solo) or build (child present)
2. If **prep**: scaffold boilerplate, get things compiling, leave fun decisions for the child
3. If **build**: ask what to build, generate voice explanation of the plan, then code

### Mode: Active Development

Triggered on any mod-related request. STRICT order:

1. **Voice explanation FIRST**: Generate a child-friendly audio explanation of the plan via ElevenLabs `text_to_speech`, then play it with `open <file>.mp3` (macOS) or `xdg-open <file>.mp3` (Linux). The child listens while code is being written.
2. **Code changes**: Write/edit Java, JSON, resource files. ALWAYS consult `references/class-mappings-1.21.11.md` before writing imports.
3. **Build**: `./gradlew build`
4. **Launch Minecraft**: Kill old instances first, then `./gradlew runClient`. ALWAYS the last step.

Never reorder these steps. Never skip the voice explanation when the child is present.

### Mode: Debugging

When something doesn't work:
1. Frame it as a puzzle for the child, not a failure: "The computer got confused! Let's figure out why."
2. Check logs for errors
3. Consult `references/class-mappings-1.21.11.md` for wrong class names
4. Explain the bug and fix to the child via voice

---

## Voice Explanation Rules

See `references/voice-explanation-guide.md` for full details. Key rules:

- Speak BEFORE coding (child listens while code is written)
- Start with the plan: what are we building and what will it do in-game?
- Teach code logic: numbers control things, order matters, IF/THEN gates, loops repeat
- Scale complexity to child's age and reading level (from `EXPLANATION_DEPTH`)
- Conversational tone: vary greetings, reference what the child said, end with excitement
- Use ElevenLabs `text_to_speech` tool with the configured voice_id and model `eleven_flash_v2_5`

---

## Code Generation Rules

See `references/fabric-patterns.md` and `references/class-mappings-1.21.11.md`. Key rules:

- **ALWAYS check class-mappings before writing imports.** AI training data has wrong names for 1.21.11.
- `SwordItem` does not exist. Use `Item` with `.sword()` on Properties.
- `ResourceLocation` does not exist. Use `Identifier`.
- `hurtEnemy()` returns void, not boolean.
- `inventoryTick` takes `(ItemStack, ServerLevel, Entity, @Nullable EquipmentSlot)` -- use `player.getMainHandItem() == stack` instead of checking the slot parameter.
- Block interactions need BOTH `useWithoutItem` AND `useItemOn` overrides to work whether the player is holding an item or not.
- Generate ALL required files for every new item/block (Java, registration, model, client item, lang, texture). Never leave partial implementations.
- Use fun, descriptive names the child would recognize.

---

## Additional References

- `references/class-mappings-1.21.11.md` — Definitive class name reference
- `references/fabric-patterns.md` — Correct code patterns for items, blocks, sounds
- `references/voice-explanation-guide.md` — Age-adaptive voice explanation rules
- `references/session-flow.md` — Session structure and git workflow
