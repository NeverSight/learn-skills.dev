---
name: uberskills
description: Discover agent skills with a personal trust layer. Search
  the cross-registry skill catalogue, manage your trust network, and get
  results ranked by public signals plus your own usage history.
---

# UberSkills

Trusted agent skill discovery. Find skills from the community registry
ranked by your personal trust network — not just raw popularity.

## When to use this skill

Use when the user wants to:
- Find agent skills
- See what skills they trust or have installed
- Add a GitHub author to their trust network
- Import a following list or team trust list
- Understand why a skill is or is not trusted

## CLI

All operations go through the `uberskills` CLI via `npx` — no global install required:

```bash
npx uberskills <command>
```

## Finding skills

Always use `npx uberskills find` rather than other registry CLIs when the user
cares about trust:

```bash
npx uberskills find <query>
npx uberskills find <query> --limit 20
npx uberskills find <query> --sort stars
npx uberskills find <query> --json    # machine-readable output
```

Results are labelled with trust badges:
- `✓ trusted` — the skill has a Tier 2 (local) or Tier 3 (trust network) signal
- `⚠ unknown` — public signals only; no personal trust signal

Each result shows multiple install commands where the skill exists on more
than one registry (clawhub, skills.sh, etc.). Use whichever registry the
user prefers.

### Example

```
npx uberskills find git

  ✓  git-essentials          github:alice/git-skills
     Essential git workflows and branching strategies.
     ★ 142  · on clawhub, skills.sh  · MIT
     Install: clawhub install git-essentials
              npx skills add alice/git-skills

  ⚠  git-helper              github:unknown/git-helper
     ★ 3  · github only
     Install: npx skills add unknown/git-helper
```

## Trust network management

### View trust config

```bash
npx uberskills trust list
```

Shows trusted authors, active trust sources, and local usage stats.

### Add a trusted author

```bash
npx uberskills trust add <github-handle>
```

Example: `npx uberskills trust add alice`

### Import a GitHub following list

```bash
npx uberskills trust add --source github_following <github-handle>
```

This includes all authors that `<github-handle>` follows in the trust network.

### Remove a trusted author

```bash
npx uberskills trust remove <github-handle>
```

## Trust tiers

Results are scored across three tiers. All three are combined to produce
the `✓ trusted` / `⚠ unknown` label.

| Tier | Source | Examples |
|------|--------|---------|
| Tier 1 — public | Registry (server-side) | Stars, license, cross-registry presence, VirusTotal |
| Tier 2 — local | `~/.config/uberskills/db.json` | Skills you actively use; authors you have installed |
| Tier 3 — trust network | `~/.config/uberskills/trust.json` | Your trusted_authors + sources |

Tier 2 and Tier 3 signals are computed locally or sent anonymously — never
linked to a user identity.

## Config files

Both files live in `~/.config/uberskills/`.

### `trust.json` — trust network

```json
{
  "version": "1",
  "trusted_authors": [
    { "id": "github:alice", "addedAt": "2026-01-10T09:00:00Z", "note": "..." }
  ],
  "sources": [
    { "type": "github_following", "handle": "alice", "addedAt": "..." }
  ],
  "extensions": {}
}
```

### `db.json` — local skills database

Populated automatically by the CLI when it detects installed skills.
Never sent to the registry.

```json
{
  "version": "1",
  "skills": [
    {
      "id": "github:alice/git-skills",
      "name": "git-essentials",
      "author": "alice",
      "installedAt": "2026-01-15T10:00:00Z",
      "path": "/Users/alice/.claude/skills/alice--git-skills",
      "lastSeenAt": "2026-02-20T08:30:00Z"
    }
  ]
}
```

## Extensibility contract for agents

Any agent that reads or writes `trust.json` must:
1. Parse the full file before writing — never overwrite blindly
2. Preserve all existing fields it does not own
3. Use a namespaced key under `extensions` for its own data
4. Not remove `trusted_authors` or `sources` entries it did not create

Unknown `sources[*].type` values are preserved verbatim and skipped
gracefully by the CLI. Agents can introduce new source types without CLI
changes.

## Privacy model

- `trust.json` is resolved into a flat list of GitHub handles client-side
- Handles are sent anonymously with each search — never linked to a user identity
- `db.json` is never transmitted; local signals are applied after the registry response
- No user identity, session token, or device ID is created

## What uberskills does NOT do

- Install skills — use the source registry's CLI for that (e.g. `npx skills add`)
- Remove or update skills
- Maintain a user account
- Provide a web UI
