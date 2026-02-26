---
name: doppler
description: Fetch secrets from Doppler for API keys and credentials.
homepage: https://doppler.com
metadata: {"clawdbot":{"emoji":"🔐","requires":{"bins":["doppler"],"env":["DOPPLER_TOKEN"]},"install":[{"id":"brew","kind":"brew","formula":"dopplerhq/cli/doppler","bins":["doppler"],"label":"Install doppler (brew)"},{"id":"script","kind":"bash","command":"curl -sLf https://cli.doppler.com/install.sh | sh","bins":["doppler"],"label":"Install doppler (script)"}]}}
---

# doppler

Use `doppler` to fetch secrets. Requires `DOPPLER_TOKEN` env var (service token scoped to project).

## Setup
1. Create project in Doppler dashboard
2. Add secrets (GEMINI_API_KEY, BREX_TOKEN, etc.)
3. Generate service token for project/config
4. Set `DOPPLER_TOKEN` on server

## Common commands

Get a single secret:
```bash
doppler secrets get GEMINI_API_KEY --plain
```

List all secrets (names only):
```bash
doppler secrets --only-names
```

List secrets with values:
```bash
doppler secrets
```

Run a command with secrets injected:
```bash
doppler run -- some-command
```

Download secrets as JSON:
```bash
doppler secrets download --no-file --format json
```

## Notes
- Service tokens are scoped to a single project + config (e.g., `dev`, `prod`)
- `--plain` strips quotes/newlines for scripting
- Never log or echo secret values
- Prefer `doppler secrets get <NAME> --plain` for single secrets
