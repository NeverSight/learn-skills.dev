---
name: castari-deploy
description: This skill should be used when the user asks to "deploy to castari", "deploy my agent", "deploy agent to production", "castari deploy", "push agent to castari", "ship my agent", "set up castari", or needs help with Castari CLI installation, authentication, agent scaffolding, or deployment to cloud sandboxes.
allowed-tools: [Bash, Read, Glob, Grep, Write, AskUserQuestion]
---

# Deploy to Castari

Deploy a Claude AI agent to production on Castari. This skill walks through the full flow: CLI installation, authentication, project scaffolding, and deployment.

## Workflow

Follow these steps in order. Skip any step whose prerequisite is already satisfied.

### Step 1: Check if the Castari CLI is installed

Run:

```bash
cast --version
```

If the command fails or is not found, install the CLI:

```bash
npm install -g @castari/cli
```

Then verify installation succeeded by running `cast --version` again.

### Step 2: Check authentication

Run:

```bash
cast whoami
```

If the user is not logged in (command fails or shows "not authenticated"), run:

```bash
cast login
```

This opens a browser for Clerk OAuth. Wait for the user to complete login, then verify with `cast whoami` again.

### Step 3: Check for castari.json

Look for `castari.json` in the current working directory:

```bash
ls castari.json
```

**If castari.json exists:** Read it and confirm the configuration with the user. Proceed to Step 4.

**If castari.json does not exist:** Help scaffold one:

1. Detect the likely entrypoint by checking for these files in order:
   - `src/index.ts`
   - `src/main.ts`
   - `index.ts`
   - `src/index.js`
   - `src/main.js`
   - `index.js`

2. Ask the user for the agent name using AskUserQuestion. Suggest the current directory name as the default.

3. Generate `castari.json` with this structure:

```json
{
  "name": "<agent-name>",
  "version": "0.1.0",
  "entrypoint": "<detected-entrypoint>",
  "runtime": "node"
}
```

Write the file and show the user what was created.

### Step 4: Deploy

Run the deployment:

```bash
cast deploy
```

This packages the project, uploads it, and deploys to an isolated cloud sandbox. The command may take up to a minute. Show the user the output including status and sandbox ID.

### Step 5: Verify deployment

After successful deployment, show the user a summary:
- Agent name/slug
- Deployment status
- Sandbox ID (if returned)

### Step 6: Offer to test

Ask the user if they want to test the deployed agent. If yes, ask for a test prompt and run:

```bash
cast invoke <agent-slug> "<test-prompt>"
```

## Error Handling

- **npm not found:** Ask the user to install Node.js (>= 18) first.
- **Authentication failure:** Suggest running `cast login` again or checking network connectivity.
- **No entrypoint detected:** Ask the user to specify their entrypoint file manually.
- **Deploy failure:** Show the full error output and suggest checking `castari.json` configuration or running `cast agents list` to verify the agent exists.

## Notes

- The CLI requires Node.js >= 18.
- Authentication uses Clerk OAuth (browser-based).
- Deployments run in isolated cloud sandboxes.
- The `castari.json` file is the project manifest — it must be in the repo root.
- Common entrypoints: `src/index.ts` for TypeScript projects, `index.js` for JavaScript.
