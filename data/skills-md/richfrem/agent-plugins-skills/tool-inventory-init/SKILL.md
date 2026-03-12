---
name: tool-inventory-init
description: "Interactive Tool Inventory bootstrap. Use this when initializing a new project repo to configure the semantic tracking of Python/JS tools. It creates a dedicated RLM profile specifically for tools and performs the first intelligent distillation pass."
dependencies: ["plugin:rlm-factory", "skill:rlm-curator"]
---
# Tool Inventory Init: The Librarian's Setup 🛠️

Initialize the semantic Tool Inventory for a new project. This is the **first-run** workflow for tracking executable scripts. 

> **Architecture Note**: This skill delegates the actual data storage and generation to the `rlm-factory` plugin, but it strongly enforces a pre-configured schema specifically for `plugins/` and `plugins/` scripts.

## When to Use

- Setting up Agent Skills inside a new root project repository.
- Rebuilding the tool inventory ledger from scratch after severe corruption.
- Moving from legacy JSON-only tracking to modern RLM tracking.

## Interactive Setup Protocol

### Step 1: Execute Initialization Script 

Run the automated bootstrapping script. This script will ensure `.agent/learning/rlm_profiles.json` exists and will inject a `tools` profile if it doesn't. 

```bash
python3 ./tool-inventory-init/scripts/tool_inventory_init.py
```

### Step 2: Serial Agent Distillation

The script above creates the target manifest, but **YOU** (the Agent) will execute the initial distillation pass if Ollama is unavailable, or you can delegate to batch mode if the project is massive.

Check what needs to be cached using the auditor:
```bash
# Hand off to the rlm-factory namespace
Trigger the 'rlm-curator' skill
```

*If there are uncached tools:*

**Option A (Agent Distillation) - Recommended for < 20 tools:**
For each file identified as missing:
1. Read the tool script.
2. Summarize its purpose, layer, and CLI usage.
3. Trigger the 'rlm-curator' skill to inject the summary

**Option B (Batch Distillation) - Recommended for > 20 tools:**
```bash
# Hand off to the rlm-factory namespace
Trigger the 'rlm-distill-agent' skill
```

### Step 3: Verify

Run the audit again to confirm 100% coverage:
```bash
# Hand off to the rlm-factory namespace
Trigger the 'rlm-curator' skill
```

## After Init

- The semantic registry is now active. You no longer need to run this command.
- Use `manage_tool_inventory.py` (inside the `tool-inventory` skill) to register single new scripts organically during development.
