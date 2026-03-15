---
name: setup-agent-tail
description: Configure agent-tail log aggregation for the current project. Auto-detects framework (Vite, Next.js, plain Node, monorepo) and sets up CLI runner, browser log plugins, and output destinations. Use when setting up agent-tail, configuring dev server logging, or piping logs for AI agent consumption.
---

<objective>
Configure [agent-tail](https://github.com/gillkyle/agent-tail) for the current project. Agent-tail pipes logs from dev servers and browser consoles into unified log files that AI coding agents can read and grep. This skill auto-detects the project type, proposes a configuration, and sets everything up after user confirmation.
</objective>

<quick_start>
Run the auto-detect workflow below. The skill will:

1. Detect project framework and structure
2. Propose a configuration
3. Install agent-tail after user confirms
4. Configure framework plugins, CLI scripts, and gitignore
</quick_start>

<essential_principles>
- Logs are written to `tmp/logs/latest/` — this is agent-tail's standard output directory
- The `tmp/` directory must be gitignored
- Browser log capture requires a framework plugin (Vite or Next.js) in addition to the CLI
- For monorepos, use `agent-tail-core init` at root and `agent-tail-core wrap` in each package
- Always confirm the proposed configuration with the user before making changes
</essential_principles>

<process>
**Step 1: Detect project type**

Read these files to determine the project setup:

- `package.json` — check for framework dependencies (vite, next, react, etc.) and existing scripts
- `vite.config.ts` / `vite.config.js` — Vite project indicator
- `next.config.ts` / `next.config.js` / `next.config.mjs` — Next.js project indicator
- `turbo.json` / `nx.json` / `pnpm-workspace.yaml` / `lerna.json` — monorepo indicators
- `.gitignore` — check if `tmp/` is already ignored

Classify the project as one of:
- **vite** — Vite-based project (React, Vue, Svelte, etc.)
- **nextjs** — Next.js project
- **monorepo** — Turborepo, Nx, pnpm workspaces, or Lerna
- **node-cli** — Plain Node.js / any other project (CLI-only setup)

**Step 2: Gather user preferences**

Use AskUserQuestion to confirm detection and gather preferences:

```
Question 1: "I detected a [framework] project. Is this correct?"
  - Yes, proceed
  - No, it's actually [other options]

Question 2: "Which services should agent-tail manage?"
  - Based on detected scripts in package.json (e.g., "dev", "api", "worker")
  - Let user add custom service names and commands

Question 3: "Configure output destinations?"
  - Default (tmp/logs/latest/) (Recommended)
  - Custom directory
  - Custom directory with combined.log disabled

Question 4: "Set up browser console log capture?"
  - Yes (Recommended) — if Vite or Next.js detected
  - No, server logs only
  - [Skip this question for node-cli projects]
```

**Step 3: Install agent-tail**

```bash
# Detect package manager from lockfile
# bun.lock → bun
# pnpm-lock.yaml → pnpm
# yarn.lock → yarn
# package-lock.json → npm

<pkg-manager> add -D agent-tail agent-tail-core
```

**Important**: The `agent-tail` umbrella package has a broken `bin` field that prevents the CLI from being linked. You must also install `agent-tail-core` explicitly — this is the package that provides the actual `agent-tail-core` CLI binary. Use `agent-tail-core` (not `agent-tail`) as the command name in all scripts.

**Step 4: Configure framework plugin**

For each detected framework, apply the appropriate configuration. See references/framework-configs.md for exact code.

- **Vite**: Add `agentTail()` plugin to vite.config
- **Next.js**: Wrap config with `withAgentTail()`, add `AgentTailScript` to layout, create browser log API route
- **Monorepo**: Add `agent-tail init` to root dev script, wrap each package with `agent-tail wrap`
- **Node CLI**: No plugin needed, just CLI configuration

**Step 5: Configure package.json scripts**

Update `package.json` scripts to use agent-tail-core CLI. Transform existing dev scripts:

```json
{
  "scripts": {
    "dev": "agent-tail-core run '<service1>: <original-command>' '<service2>: <original-command>'"
  }
}
```

If user specified excludes or muting, add flags:

```json
{
  "scripts": {
    "dev": "agent-tail-core run --exclude '[HMR]' --mute worker '<services>'"
  }
}
```

**Step 6: Update .gitignore**

Add `tmp/` to `.gitignore` if not already present.

**Step 7: Verify setup**

After configuration, tell the user:
- Run their dev script to verify logs appear in `tmp/logs/latest/`
- Check that individual service logs and `combined.log` are created
- If browser logging was enabled, verify console output appears in the browser log file
</process>

<configuration_options>
These options can be presented to the user during setup:

**Output directory**: Where logs are written (default: `tmp/logs/latest/`)

**Excludes**: Filter noisy log lines by substring or regex:
- Common Vite excludes: `[HMR]`, `[vite]`, `Download the React DevTools`
- Common Next.js excludes: `[Fast Refresh]`, `compiled successfully`

**Service muting**: Hide specific services from terminal output while preserving log files:
- Useful for noisy frontend dev servers when focused on backend work

**Browser log capture**: Capture `console.*`, unhandled errors, and unhandled promise rejections from the browser

**Log format**: All logs use timestamp + level + message format:
`[10:30:00.123] [LOG    ] Message here`

**Gitignore warning**: Agent-tail warns on startup if `tmp/` is not gitignored. Disable with `warnOnMissingGitignore: false` in plugin options.
</configuration_options>

<anti_patterns>
<pitfall name="forgetting-browser-setup">
For Vite/Next.js projects, the CLI alone does not capture browser console logs. The framework plugin is required for browser log capture.
</pitfall>

<pitfall name="monorepo-without-init">
In monorepos using Turborepo/Nx, you must run `agent-tail-core init` before `turbo dev` (or equivalent). Without init, `agent-tail-core wrap` in child packages has no session to join.
</pitfall>

<pitfall name="using-agent-tail-cli-instead-of-agent-tail-core">
The `agent-tail` umbrella package has a broken `bin` field — it references a nested path that package managers don't resolve correctly. Always use `agent-tail-core` as the CLI command in scripts, and always install `agent-tail-core` as an explicit devDependency alongside `agent-tail`.
</pitfall>

<pitfall name="overwriting-existing-scripts">
When modifying package.json scripts, preserve the original command inside the agent-tail runner. Do not replace the command, wrap it.
</pitfall>
</anti_patterns>

<success_criteria>
Setup is complete when:
- agent-tail is installed as a dev dependency
- Framework plugin configured (if Vite or Next.js)
- package.json dev script wraps services with agent-tail
- `tmp/` is in .gitignore
- User has been told how to verify the setup works
</success_criteria>

<reference_guides>
**Framework-specific configuration code**: See references/framework-configs.md
</reference_guides>
