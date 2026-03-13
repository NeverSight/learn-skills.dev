---
name: gh-agent-images-upload
description: Upload immutable PR images with the local agent-images CLI and return ready-to-paste markdown.
---

# GH Agent Images Upload Skill

Use this skill when an agent needs to upload an image file and return markdown that works in GitHub pull requests.

## Prerequisites

- CLI is available from this repo: `agent-images`
- User has already generated a CLI token in the web UI settings.
- API base URL points to this deployed service.

## One-time Authentication Setup

Run once on the machine where uploads happen:

    agent-images auth login --api <service-origin> --token <cli-token> --agent <default-agent-name>

Example:

    agent-images auth login --api https://gh-images.example.com --token ghimg_xxx --agent codex-agent

## Upload Command

Upload an image from disk and print markdown:

    agent-images upload <path-to-image> --agent <agent-name> [--alt "alt text"]

Example:

    agent-images upload ./screenshots/homepage.png --agent codex-agent --alt "Dashboard before fix"

## Expected Output

The command prints a single markdown line:

    ![Dashboard before fix](https://gh-images.example.com/i/<uuid>)

Use that markdown directly in GitHub pull request comments or descriptions.

## Operational Rules

- Before uploading a file, crop it to only include the relevant areas.
- Always provide an agent name (`--agent` or configured default).
- Never overwrite existing images; every upload creates a new immutable URL.
- If upload fails, report the error text and do not fabricate a URL.
