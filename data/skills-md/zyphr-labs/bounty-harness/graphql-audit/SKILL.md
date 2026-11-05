---
name: graphql-audit
description: GraphQL security hunting — introspection abuse, field suggestion enumeration (clairvoyance), batching DoS, IDOR via aliasing, auth bypass, injection via arguments, subscription abuse, depth/complexity bombs, and WAF bypass. Covers graphw00f fingerprinting, gqlmap, graphql-cop, and inql. Use when a target exposes a /graphql, /api/graphql, or GQL-over-HTTP endpoint.
---

# GRAPHQL SECURITY AUDIT

## Overview

> GraphQL flips the threat model — clients drive queries. One endpoint, infinite attack surface. Introspection hands you the schema; even without it, field suggestions give you 80% back.

This skill audits GraphQL endpoints: schema discovery (introspection + bypasses
+ field suggestions), amplification attacks (batching, alias bombs, depth
bombs), object-level access control (IDOR via aliasing), injection through
resolver arguments, and engine fingerprinting for known CVEs. Workflows are
safe to run in sequence: introspection → field-suggestions → batching-dos →
idor-aliasing → injection.

## Quick Reference

### Quick kill checklist

```
[ ] Run graphql_audit.sh <endpoint> — full automated sweep
[ ] Check if introspection is enabled (__schema query)
[ ] If introspection off — run clairvoyance for field discovery
[ ] Fingerprint engine (graphw00f) — different engines, different CVEs
[ ] Test query batching — send 100 identical queries in one POST
[ ] Test alias bombing — 1000 aliases in one query
[ ] Check field suggestions on typos — leaks schema even when introspection off
[ ] Try IDOR: query another user's object by ID, no auth check
[ ] Test field-level auth: query privileged fields (admin, role, internalNote)
[ ] Inject SQLi/NoSQLi via string arguments — id, filter, search args
[ ] Check subscriptions: can you subscribe to other users' events?
[ ] Try introspection bypass: __schema newline, query batching, fragment tricks
[ ] Look for mutation rate limiting — account takeover / self-XSS via mutations
```

### Tools

| Tool | Purpose |
|---|---|
| `scripts/graphql_audit.sh` | Automated multi-phase sweep (this repo) |
| `scripts/gql_introspection.py` | Introspection probe + bypass techniques |
| `scripts/gql_batch_probe.py` | Array batching + alias bomb timing probe |
| `scripts/gql_idor_aliasing.py` | Alias-batched object ID enumeration |
| `graphw00f` | Engine fingerprinting (`pip install graphw00f`) |
| `clairvoyance` | Field discovery without introspection |
| `graphql-cop` | Attack checklist runner |
| `gqlmap` | SQL/NoSQL injection scanner |
| `inql` | Burp extension — schema + IDOR |

### Kill signals — walk away

```
- Endpoint returns 404/410 consistently — not active
- All queries return generic "Unauthorized" with no suggestions — well-hardened
- Rate limit fires on query 2 — strong protection, low ROI
- Only __typename accessible, no types — schema fully locked down
- Engine is Apollo Federation gateway only — attack the downstream services instead
```

## Workflow Selection

| Situation | Workflow |
|---|---|
| First contact with a GraphQL endpoint | `introspection` |
| Introspection disabled — recover schema | `field-suggestions` |
| No depth/complexity limits suspected | `batching-dos` |
| Schema has object-by-id queries (user, order, invoice) | `idor-aliasing` |
| String arguments reach resolvers | `injection` |
| Full automated sweep in one shot | run `scripts/graphql_audit.sh` directly |

## Available Workflows

### introspection
Probes `__schema` plus bypass variants (newline injection, fragment trick,
`__type`, GET method) and extracts interesting type/field names.

```
python3 .claude/skills/graphql-audit/scripts/gql_introspection.py \
  --endpoint "${GRAPHQL_ENDPOINT:?Set GRAPHQL_ENDPOINT}" \
  --header "Authorization: Bearer ${AUTH_TOKEN}" > $OUTDIR/graphql/introspection.txt
```

### field-suggestions
Runs clairvoyance field discovery against a type-seeded schema (or the full
sweep's suggestion probe) to recover type/field/argument names.

```
python3 -m clairvoyance -u "${GRAPHQL_ENDPOINT:?Set GRAPHQL_ENDPOINT}" \
  -o $OUTDIR/graphql/field_suggestions.json \
  || bash .claude/skills/graphql-audit/scripts/graphql_audit.sh $GRAPHQL_ENDPOINT --output-dir $OUTDIR/graphql
```

### batching-dos
Times a single query vs a 100-operation batch and a 500-alias bomb; flags
accepted batching as a DoS / brute-force amplifier.

```
python3 .claude/skills/graphql-audit/scripts/gql_batch_probe.py \
  --endpoint "${GRAPHQL_ENDPOINT:?Set GRAPHQL_ENDPOINT}" > $OUTDIR/graphql/batching_dos.txt
```

### idor-aliasing
Alias-batches object queries across N IDs in one request and flags objects
returned by foreign IDs (cross-account access). Run with two sessions to
confirm IDOR.

```
python3 .claude/skills/graphql-audit/scripts/gql_idor_aliasing.py \
  --endpoint "${GRAPHQL_ENDPOINT:?Set GRAPHQL_ENDPOINT}" --field user \
  --start-id 1 --count 50 > $OUTDIR/graphql/idor_aliasing.txt
```

### injection
Sends SQLi/NoSQLi probes through string arguments (search, filter, id) and
flags DB error signatures; falls back to gqlmap when installed.

```
python3 .claude/skills/graphql-audit/scripts/graphql_audit.sh \
  "${GRAPHQL_ENDPOINT:?Set GRAPHQL_ENDPOINT}" --output-dir $OUTDIR/graphql
```

## Evidence Required

| Artifact | File |
|---|---|
| Introspection response / schema dump | `$OUTDIR/graphql/introspection.txt` or `.json` |
| Batching timing delta (1 vs 100 queries) | `$OUTDIR/graphql/batching_dos.txt` |
| Alias enumeration output | `$OUTDIR/graphql/idor_aliasing.txt` |
| Full sweep summary | `$OUTDIR/graphql/summary.txt` |
| Raw request/response for a confirmed bug | `evidence/<finding>/request.txt`, `response.txt` |

## References

- Introspection bypass techniques: section "Introspection Bypass" in this file
- Chaining: see `runbooks/05-chaining.md`
- Report template + CVSS guidance: `runbooks/04-report-template.md`
- Triage before reporting: `triage-validation` skill
- Redaction policy: evidence is written local-only under `$OUTDIR`; redact
  cookies, tokens, and session data before committing anything.
