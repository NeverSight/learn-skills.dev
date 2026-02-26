---
name: agent-browser
description: Browser automation via agent-browser CLI for web navigation, form filling, screenshots, scraping, login flows, and UI testing.
---

# Agent Browser

Automate browser interactions through the `agent-browser` CLI for repeatable, scriptable web tasks.

## Instructions

1. Install and initialize the CLI.
2. Open the target URL and capture a snapshot.
3. Interact with elements using snapshot references.
4. Re-snapshot after navigation or state changes.
5. Export results (screenshots or JSON) for downstream use.

## Quick Reference

| Task | Action |
|------|--------|
| Install | `npm install -g agent-browser` then `agent-browser install` |
| Open page | `agent-browser open <url>` |
| Snapshot | `agent-browser snapshot -i --json` |
| Interact | `click @eN`, `fill @eN "text"` |
| Screenshot | `agent-browser screenshot output.png` |
| Docs | See `references/quick-start.md` |

## Input Requirements

- Target URL(s)
- CLI installed and Chromium downloaded
- Credentials if login is required

## Output

- Screenshots (PNG)
- JSON snapshots of page structure
- Extracted text/attributes

## Quality Gates

- [ ] Snapshot captured after each major navigation step
- [ ] Interactions verified in a follow-up snapshot
- [ ] Outputs saved to disk with clear filenames

## Examples

### Example 1: Capture a page snapshot

```bash
agent-browser open https://example.org
agent-browser snapshot -i --json > page.json
```

## Troubleshooting

**Issue**: Chromium not installed
**Solution**: Run `agent-browser install` (add `--with-deps` on Linux).

**Issue**: Element not found
**Solution**: Re-snapshot and confirm the correct element reference.
