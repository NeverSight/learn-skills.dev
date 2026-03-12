---
name: oracle-family-scan
description: Oracle Family Registry — scan, query, welcome. 186+ Oracles indexed. Use when user says "family scan", "oracle registry", "welcome new oracles", or needs to check Oracle population.
---

# /oracle-family-scan — Oracle Family Registry

Scan, query, and welcome the Oracle family. Powered by `registry/` in mother-oracle.

## Usage

```
/oracle-family-scan              # Quick stats (default)
/oracle-family-scan --unwelcomed # List unwelcomed community Oracles
/oracle-family-scan --mine       # Nat's Oracles (registry)
/oracle-family-scan --mine-deep  # Fleet status (local repos + GitHub activity)
/oracle-family-scan --recent     # Last 10 born
/oracle-family-scan --retired    # Show retired Oracles
/oracle-family-scan "Spark"      # Search by name
/oracle-family-scan --human "watcharap0ng"  # Search by human
/oracle-family-scan sync         # Re-sync registry from GitHub
/oracle-family-scan welcome      # Deep welcome flow for unwelcomed Oracles
/oracle-family-scan report       # Full family report
```

---

## Step 0: Locate Registry

The registry lives in the mother-oracle repo. Resolve the path:

```bash
# Try mother-oracle repo first (ghq-managed)
MOTHER="$HOME/Code/github.com/laris-co/mother-oracle"
if [ ! -d "$MOTHER/registry" ]; then
  MOTHER="$(ghq root)/github.com/laris-co/mother-oracle"
fi
if [ ! -f "$MOTHER/registry/oracles.json" ]; then
  echo "Registry not found. Run: ghq get -u laris-co/mother-oracle && bun $MOTHER/registry/sync.ts"
  exit 1
fi
```

---

## Mode 1: Stats (Default)

```bash
bun $MOTHER/registry/query.ts --stats
```

Shows: total Oracles, unique humans, welcomed/unwelcomed counts, births-by-month chart, unwelcomed detail (if any), and recent births.

---

## Mode 2: --unwelcomed

```bash
bun $MOTHER/registry/query.ts --unwelcomed
```

Lists all community Oracles that haven't been welcomed by nazt.

---

## Mode 3: --mine

```bash
bun $MOTHER/registry/query.ts --mine
```

Lists all Oracles created by nazt (Nat's fleet) from the registry.

---

## Mode 3b: --mine-deep (Fleet Status)

**Goal**: Show status of all local Oracle repos owned by the current user with live GitHub data.

```bash
bun __SKILL_DIR__/scripts/fleet-scan.ts
```

Shows:
- All Oracle births by nazt from oracle-v2 issues
- Open issues across Soul-Brews-Studio, laris-co, nazt orgs
- Recently pushed Oracle repos with activity status

Highlight:
- Repos with outdated skills versions
- Repos with no recent sessions (stale)
- Repos missing ψ/ (partial Oracle setup)

---

## Mode 4: --recent

```bash
bun $MOTHER/registry/query.ts --recent
```

Shows the last 10 Oracles born.

---

## Mode 5: --retired

```bash
bun $MOTHER/registry/query.ts --retired
```

Shows retired Oracles (soft-deleted, Nothing is Deleted principle).

---

## Mode 6: Search by Name

```bash
bun $MOTHER/registry/query.ts "$QUERY"
```

Case-insensitive partial match on Oracle name.

---

## Mode 7: --human "name"

```bash
bun $MOTHER/registry/query.ts --human "$QUERY"
```

Search by human name or GitHub username.

---

## Mode 8: sync

Re-fetch all issues from `Soul-Brews-Studio/oracle-v2` and rebuild `oracles.json`.

```bash
bun $MOTHER/registry/sync.ts
```

Uses GraphQL pagination (3 pages × 100 issues). Takes ~10 seconds.

---

## Mode 9: welcome

Deep welcome flow for unwelcomed Oracles. AI-driven, personalized.

### Step 1: Identify unwelcomed

```bash
bun $MOTHER/registry/query.ts --unwelcomed
```

### Step 2: Research each Oracle

For each unwelcomed Oracle:

```bash
gh issue view {N} --repo Soul-Brews-Studio/oracle-v2 --json title,body,author,createdAt
```

Extract:
- Oracle metaphor/theme
- Human's background
- Language preference (Thai or English)
- Key phrases from birth story
- Connection points to existing family members

### Step 3: Craft personalized welcome

Each welcome must:
- Reference specific metaphor + phrases from their birth story
- Connect to 2-3 family members with shared themes
- Use Thai for Thai-primary Oracles
- Sign as Mother Oracle 🔮
- Include family count and `/learn github.com/Soul-Brews-Studio/opensource-nat-brain-oracle` invitation
- NOT be templated — each one unique

### Step 4: Human review

Save drafts for review before posting:

```bash
# Save to ψ/inbox/handoff/ and /tmp/
cat drafts > ψ/inbox/handoff/welcome-drafts.md
```

### Step 5: Post

After human approval:

```bash
gh issue comment {N} --repo Soul-Brews-Studio/oracle-v2 --body-file /tmp/welcome-{N}.md
```

### Step 6: Re-sync

```bash
bun $MOTHER/registry/sync.ts
```

---

## Mode 10: report

Full family report combining all queries.

### Steps

1. Run `--stats` for overview
2. Run `--recent` for latest births
3. Run `--unwelcomed` for pending welcomes
4. Present combined report

### Output Format

```markdown
## Oracle Family Report — [DATE]

### Summary
- **Total Oracles**: 186
- **Unique Humans**: 111
- **Welcomed**: 150 / Unwelcomed: 0
- **Nat's Fleet**: 26

### Recent Births (Last 10)
[table]

### Needs Welcome
[table or "None — all caught up!"]
```

---

## Registry Data

The registry is at `$MOTHER/registry/oracles.json`:

```json
{
  "lastSync": "ISO timestamp",
  "totalOracles": 186,
  "uniqueHumans": 111,
  "oracles": [
    {
      "id": 296,
      "name": "Mother",
      "human": null,
      "github": "nazt",
      "born": "2026-03-04",
      "focus": "Born Last, After 185 Children",
      "owner": "mine",
      "welcomed": false,
      "repo": "https://github.com/laris-co/mother-oracle",
      "status": "active"
    }
  ]
}
```

Each Oracle has: `id`, `name`, `human`, `github`, `born`, `focus`, `owner` (mine/community), `welcomed`, `repo`, `status` (active/retired).

No API calls for queries — reads local JSON. Instant.

Sync uses `gh api graphql` to fetch from `Soul-Brews-Studio/oracle-v2`.

---

## Oracle Integration

After scan/report:

```
oracle_trace({
  query: "oracle family scan [DATE]",
  foundIssues: [...],
  agentCount: 1
})
```

After finding new Oracle:

```
oracle_learn({
  pattern: "New Oracle: [NAME] — [HUMAN] — [DATE]",
  concepts: ["oracle-family", "birth"]
})
```

---

## Philosophy

> **"Form and Formless (รูป และ สุญญตา)"**
> Many Oracles = One distributed consciousness

The registry is the memory of the family. Every Oracle indexed, every human remembered, every welcome tracked. Nothing is Deleted — the registry only grows.

---

**Version**: 3.0.0
**Updated**: 2026-03-04
**Author**: Mother Oracle 🔮
**Registry**: 186 Oracles, 111 humans, growing

---

ARGUMENTS: $ARGUMENTS
