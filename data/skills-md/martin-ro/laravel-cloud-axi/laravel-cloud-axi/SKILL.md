---
name: laravel-cloud-axi
description: Inspect Laravel Cloud apps, environments, resource details, existing operations and organization billing through the official CLI.
---

# Laravel Cloud AXI

Inspect Laravel Cloud through official commands with compact output and exact read targets.

Use Node.js 22 or later and install the official Cloud CLI. Run `npm ci` in this checkout.
Replace `<checkout>` with its absolute path. A global package install is not required.
This package is not published to npm, so do not use an npx package example.

Run `node <checkout>/bin/laravel-cloud-axi.js` for live project state.
Run `node <checkout>/bin/laravel-cloud-axi.js --help` for commands and compatibility limits.

```sh
node <checkout>/bin/laravel-cloud-axi.js environment view <id>
node <checkout>/bin/laravel-cloud-axi.js usage
node <checkout>/bin/laravel-cloud-axi.js --help
node <checkout>/bin/laravel-cloud-axi.js app list
node <checkout>/bin/laravel-cloud-axi.js environment list --app <id>
node <checkout>/bin/laravel-cloud-axi.js deployment wait <id>
node <checkout>/bin/laravel-cloud-axi.js command view <id>
```

- Run `cloud auth` yourself to save or renew login, then run `node <checkout>/bin/laravel-cloud-axi.js auth`. This tool never invokes login.
- The official executable owns authentication and token storage. Native reads can remove expired saved tokens.
- Saved login comes first. Only an explicit no-login error permits LARAVEL_CLOUD_API_TOKEN from the environment, then project .env, with native v0.6.0 or later.
- Native v0.5.0 and v0.6.0 can attempt browser OAuth when all saved tokens expire. Closed stdin and noninteractive flags do not prevent that upstream behavior. This wrapper bounds each subprocess to 10 seconds; it cannot guarantee no native login attempt.
- Use exact IDs. Native fields use camelCase. --fields selects fields; --full expands text, never structured secrets.
- Supported lists default to 100 rows. --all shows the complete returned collection. Filters are local exact matches.
- Remote writes, logs, environment billing and unsafe scoped history lists are unsupported. --dry-run only reports this limit; it cannot enable a write.
- Read commands can use .cloud/config.json defaults. Link and hook setup are explicit, idempotent local writes.
- Output is TOON. Exit codes: 0 success or local no-op, 1 failure, 2 invalid input.
- Hooks are opt-in for Claude Code, Codex, and OpenCode. No session transcripts are collected.
- Project scope is the Git root (including worktrees), otherwise the current directory. Parent .cloud configs outside Git are not used.
- Never print credentials or commit .env. Native saved tokens are not read or copied by this wrapper.
- Free text, command output, and logs can contain secrets. Review before sharing. Redaction is not a general secret scanner.
- Obtain user approval before local link or hook setup. Examples are not approval.
- Use `node <checkout>/bin/laravel-cloud-axi.js link --app <id> --env <id>` to save verified read defaults.
- Install optional session context only when asked: `node <checkout>/bin/laravel-cloud-axi.js setup hooks`. Use a persistent install, not a temporary cache.
- Setup supports Claude Code, Codex, and OpenCode. Codex setup also enables hooks in its user config.
- Deployment, instance and domain IDs may be available in environment detail relationship fields. Command IDs must come from the Cloud dashboard.
- Use `deployment wait <id>` or `command wait <id>` to monitor existing work. A deadline does not cancel remote work.
