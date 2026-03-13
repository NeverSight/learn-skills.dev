---
name: cursor-deeplinks
description: Generate Cursor deeplinks (prompt/command/rule and MCP install links) using the repo generator and the project output contract. Use when the user asks for a Cursor deeplink, cursor:// links, cursor.com/link links, or wants to create prompts/commands/rules via deeplinks.
---

# Cursor Deeplinks

This skill standardizes how to **create Cursor deeplinks** (per this repo’s conventions), including:
- prompt deeplinks
- command deeplinks (create `.cursor/commands/*.md` in the current project after approval)
- rule deeplinks (create `.cursor/rules/*.mdc` in the current project after approval)
- MCP install deeplinks

Primary reference in this repo: `doc/cursor-deeplinks.md`  
Preferred generator: `scripts/cursor-deeplink-gen.py`

## Quick start (recommended)

Use the generator script to avoid encoding mistakes and to verify the **8,000 char URL limit** (post-encoding):

```bash
python3 scripts/cursor-deeplink-gen.py prompt --text "Create a README for this repo" --md
python3 scripts/cursor-deeplink-gen.py command --name "run-all-tests" --text "Run the full test suite and fix failures" --md
python3 scripts/cursor-deeplink-gen.py rule --name "python-style" --text "Prefer ruff/black; avoid implicit Any." --md
python3 scripts/cursor-deeplink-gen.py mcp-install --name postgres --config-file mcp.json --md
```

## Output contract (always follow)

When asked to produce a deeplink, return:
1. **WEB link (primary)**: `https://cursor.com/link/...`
2. **APP link (secondary)**: `cursor://anysphere.cursor-deeplink/...`
3. **Expected result**: what Cursor will create/show after the user approves (e.g. where the file will be created)
4. A short safety note: **“Check secrets + 8,000 URL limit”**

## Deeplink formats (what to generate)

Cursor supports two equivalent bases:
- **WEB**: `https://cursor.com/link`
- **APP**: `cursor://anysphere.cursor-deeplink`

Supported paths and params:

### Prompt
- Path: `/prompt`
- Params: `text=<promptText>`

### Command
- Path: `/command`
- Params: `name=<commandName>`, `text=<commandContent>`
- Expected result: Cursor will propose creating a command file under `.cursor/commands/` in the current project after approval.

### Rule
- Path: `/rule`
- Params: `name=<ruleName>`, `text=<ruleContent>`
- Expected result: Cursor will propose creating a rule file under `.cursor/rules/` in the current project after approval.

### MCP install
- Path: `/mcp/install`
- Params: `name=<serverName>`, `config=<base64(JSON.stringify(transportConfig))>`
- The `transportConfig` is the per-server object (e.g. `{"command":"npx","args":[...]}`), not the whole `mcp.json` mapping.

## Manual construction (only if you cannot run the generator)

1. Choose base (**WEB** preferred) + path.
2. Build query params.
3. **URL-encode** all params (including newlines/spaces).
4. Ensure total URL length (after encoding) \(\le 8000\).

Notes:
- URL encoding is fragile; prefer the generator.
- For MCP install, `config` must be base64 of the stringified JSON. Base64 output must be safe for query params (must be URL-encoded; `+` becomes `%2B`).

## Safety + UX checks (must do)

- **Secrets**: never embed API keys, tokens, passwords, private keys, or other sensitive content in deeplink text/config.
- **Length**: enforce the **8,000 character** max (post-encoding). If over limit, shorten the content or generate artifacts via normal repo edits instead of a deeplink.
- **Expectation**: deeplinks **do not auto-execute**; the user must review and approve in Cursor.

## Examples (copy/paste patterns)

### Prompt deeplink (generator)

```bash
python3 scripts/cursor-deeplink-gen.py prompt --text "Write a short changelog entry for the last commit" --md
```

### Command deeplink (generator)

```bash
python3 scripts/cursor-deeplink-gen.py command --name "audit-config" --text "Review mcp.json for risky settings and propose fixes." --md
```

### Rule deeplink (generator)

```bash
python3 scripts/cursor-deeplink-gen.py rule --name "cursor-deeplinks" --text "When asked for a deeplink, output WEB+APP links + expected result + safety note." --md
```

### MCP install deeplink (generator)

```bash
python3 scripts/cursor-deeplink-gen.py mcp-install --name "github" --config-file mcp.json --md
```

## Additional resources

- Repo docs: `doc/cursor-deeplinks.md`
- Official docs:
  - `https://cursor.com/docs/integrations/deeplinks.md`
  - `https://cursor.com/docs/context/mcp/install-links.md`

