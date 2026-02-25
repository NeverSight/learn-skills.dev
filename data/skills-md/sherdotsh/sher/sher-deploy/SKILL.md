---
name: sher-deploy
description: Deploy frontend projects to instant preview URLs using sher. After building a project, run sher link to get a live, shareable URL in seconds.
---

# sher — deploy to a live preview URL

sher is a CLI that builds your frontend project, uploads it, and returns a live preview URL. One command. No accounts. No config.

Use it after you've built or scaffolded a frontend project and the user wants to see it live.

## Install

Global (recommended for agents):

```bash
npm i -g shersh
```

Or one-off with npx:

```bash
npx shersh link
```

## Deploy

From the project root:

```bash
sher link
```

That's it. sher auto-detects the framework, runs the build, uploads the output, and returns a URL.

### Options

| Flag | Description |
|------|-------------|
| `--dir <path>` | Upload a specific directory (skips framework detection) |
| `--ttl <hours>` | Set link expiry in hours (default: 24) |
| `--no-build` | Skip the build step (use if already built) |
| `--pass [password]` | Password-protect the preview (Pro only) |

### Examples

```bash
# Standard deploy
sher link

# Deploy a pre-built project
sher link --no-build

# Deploy a specific output directory
sher link --dir ./dist

# Short-lived link (2 hours)
sher link --ttl 2
```

## Parsing the output

The CLI prints the live URL to stdout in this format:

```
  https://a8xk2m1p.sher.sh  (copied)
  expires 2/19/2026, 11:00 AM
```

The URL always matches the pattern `https://[a-z0-9]{8}.sher.sh`. Extract it with:

```
https://[a-z0-9]{8}\.sher\.sh
```

The URL is also automatically copied to the clipboard.

## After deploying

Present the URL to the user:

> Your preview is live at https://a8xk2m1p.sher.sh

If you set a `--ttl`, mention when it expires. If using `--pass`, share the password too.

## Supported frameworks

sher auto-detects and builds:

- **Vite** — outputs to `dist/`
- **Next.js** — auto-configures static export, outputs to `out/`
- **Astro** — outputs to `dist/`
- **Create React App** — outputs to `build/`
- **Any project** with a build script that produces `dist/`, `build/`, or `out/`
- **Static HTML** — no build needed, use `--dir .` to upload directly

## Agent-friendly by default

- No browser opens after deploy
- No interactive prompts
- No account required for basic usage (1 deploy, 10MB max, 6h TTL)
- Authenticated users get 25 deploys, 50MB, 24h TTL
- Exit code 0 on success, non-zero on failure

## Troubleshooting

If `sher link` fails:

1. **No build script** — the project needs a `build` script in `package.json`, or use `--dir` to point to pre-built output
2. **Build error** — fix the build error first, then retry
3. **Size limit** — the upload is too large (10MB anonymous, 50MB authenticated, 100MB Pro)
4. **No output directory** — ensure the build produces `dist/`, `build/`, or `out/`, or specify `--dir`
