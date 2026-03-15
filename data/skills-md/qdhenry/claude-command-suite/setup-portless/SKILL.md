---
name: setup-portless
description: Sets up Portless for a project to replace port numbers with stable named .localhost URLs. Use when configuring local development routing, fixing port conflicts, or setting up monorepo dev environments.
---

<objective>
Set up [Portless](https://github.com/vercel-labs/portless) for the current project. Portless replaces `localhost:PORT` with stable named URLs like `myapp.localhost:1355`, eliminating port conflicts, cookie collisions, and port-guessing issues for both developers and AI agents.

**Requirements:** Node.js 20+, macOS or Linux.
</objective>

<quick_start>
Run these commands to get started:

```bash
# Install globally
npm install -g portless

# Start the proxy daemon
portless proxy start

# Run your app with a named route
portless myapp next dev
# => http://myapp.localhost:1355
```
</quick_start>

<process>

**Step 1: Verify prerequisites**

Check Node.js version is 20+ and platform is macOS or Linux:

```bash
node --version
uname -s
```

If Node.js < 20, inform the user they need to upgrade before proceeding.

**Step 2: Detect project context**

Read `package.json` to understand:
- Project name (use as default app name)
- Existing dev scripts (to know what command to wrap)
- Whether this is a monorepo (look for `workspaces` field, or `pnpm-workspace.yaml`, `turbo.json`, `lerna.json`)
- Framework in use (Next.js, Vite, Express, etc.) from dependencies

**Step 3: Install Portless**

```bash
npm install -g portless
```

**Step 4: Choose app name(s)**

Ask the user what name they want for their app URL. Suggest based on project name.

For monorepos, suggest subdomain naming:
- `api.projectname` for backend
- `web.projectname` or `projectname` for frontend
- `docs.projectname` for documentation

**Step 5: Update package.json scripts**

Wrap the existing dev script with portless. For example, if the current script is:

```json
{ "dev": "next dev" }
```

Update to:

```json
{ "dev": "portless myapp next dev" }
```

For monorepos, update each workspace's `package.json` similarly.

**Step 6: Verify setup**

Run the dev script and confirm the app is accessible at the named URL:

```bash
npm run dev
```

The proxy auto-starts if not already running. Confirm output shows the `.localhost:1355` URL.

Verify routes are registered:

```bash
portless list
```

</process>

<common_patterns>

<pattern name="single-app">
**Single application:**

```json
{
  "scripts": {
    "dev": "portless myapp next dev"
  }
}
```

Access at: `http://myapp.localhost:1355`
</pattern>

<pattern name="monorepo">
**Monorepo with multiple services:**

```bash
# In packages/web/package.json
"dev": "portless web.myapp next dev"

# In packages/api/package.json
"dev": "portless api.myapp node server.js"

# In packages/docs/package.json
"dev": "portless docs.myapp next dev"
```

Access at:
- `http://web.myapp.localhost:1355`
- `http://api.myapp.localhost:1355`
- `http://docs.myapp.localhost:1355`
</pattern>

<pattern name="custom-proxy-port">
**Custom proxy port (e.g., port 80 for clean URLs):**

```bash
sudo portless proxy start -p 80
# Then: http://myapp.localhost (no port needed)
```
</pattern>

</common_patterns>

<environment_variables>

| Variable | Purpose | Default |
|----------|---------|---------|
| `PORTLESS=0` or `PORTLESS=skip` | Bypass portless, use default port | (not set) |
| `PORTLESS_PORT` | Override proxy port | `1355` |
| `PORTLESS_STATE_DIR` | Custom state directory | `~/.portless` or `/tmp/portless` |

</environment_variables>

<cli_reference>

| Command | Purpose |
|---------|---------|
| `portless <name> <cmd> [args...]` | Run app with named route |
| `portless list` | Show active routes |
| `portless proxy start` | Start daemon proxy on port 1355 |
| `portless proxy start -p <port>` | Start on custom port |
| `portless proxy start --foreground` | Run in foreground (debugging) |
| `portless proxy stop` | Stop the proxy daemon |

</cli_reference>

<anti_patterns>

<pitfall name="forgetting-proxy">
The proxy auto-starts when you run `portless <name> <cmd>`, so there is no need to manually start it. Only use `portless proxy start` for custom port configuration.
</pitfall>

<pitfall name="windows">
Portless does not support Windows. Only set up on macOS or Linux.
</pitfall>

<pitfall name="old-node">
Portless requires Node.js 20+. Do not attempt installation on older versions.
</pitfall>

</anti_patterns>

<success_criteria>
Setup is complete when:
- Portless is installed globally (`portless --version` succeeds)
- Project `package.json` dev script(s) are wrapped with `portless <name>`
- Running `npm run dev` (or equivalent) shows the app accessible at `<name>.localhost:1355`
- For monorepos, each workspace has its own named route
</success_criteria>
