---
name: orderly-plugin-gen
description: Generate Orderly SDK plugin scaffolding with unique ID, registration boilerplate, and typed interceptors. Use when the user mentions creating, developing, registering, implementing, or generating a plugin (e.g. 'create a plugin', 'generate a plugin', 'develop a plugin', 'register a plugin', 'implement a plugin', 'build a plugin', 'add a plugin', 'scaffold a plugin', 'new plugin').
---

# Orderly Plugin Generator

Quickly generate plugin project scaffolding in the Orderly SDK monorepo.

## Trigger

When the user's message contains the following keywords, **proactively ask** whether to use this Skill to generate a plugin template:

- create a plugin / generate a plugin / develop a plugin / register a plugin

Example prompt: "Detected that you want to create an Orderly plugin. Would you like to use the orderly-plugin-gen scaffold to generate a template?"

## Workflow

### Step 1: Gather information

Ask the user for the following (using the AskQuestion tool):

1. **Plugin name** (required): e.g. `orderbook-flash`, `pnl-card`. Only lowercase letters, numbers, and hyphens are allowed.
2. **Plugin type** (required): `widget` / `page` / `layout`
3. **Output path** (optional): Parent path for the plugin directory. Defaults to the current project's `packages/` directory.

### Step 2: Run the script

Run the generation script with the Shell tool (Node.js >=20.19.0 required):

```bash
node ~/.cursor/skills/orderly-plugin-gen/scripts/create-plugin.mjs \
  --name <plugin-name> \
  --type <widget|page|layout> \
  --path <absolute-parent-path>
```

### Step 3: Report results

After the script runs, report to the user:

1. The generated plugin ID
2. The list of created files
3. Follow-up steps:
   - Run `pnpm install` to install dependencies
   - Edit `src/index.tsx` to add business logic
   - Register the plugin in the host app via the `plugins` prop of `OrderlyProvider`

## Generated Structure

```
plugin-<name>/
├── package.json
├── tsconfig.json
├── tsup.config.ts
└── src/
    ├── index.tsx
    └── components/
        └── .gitkeep
```

## Additional Resources

- For plugin system API reference, see [reference.md](reference.md)
