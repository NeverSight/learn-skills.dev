---
name: using-neon
description: "Neon serverless Postgres: branching, autoscaling, scale-to-zero, connection methods, Neon API and CLI. Read for Neon-specific questions; plain Postgres questions go to skills/postgresql/SKILL.md."
---

# Neon

Neon is Postgres with separated compute and storage: autoscaling, scale-to-zero, branching, instant restore. Anything that works with Postgres works with Neon; this skill covers only what is Neon-specific.

## Do not guess Neon details. Fetch the docs.

Features, limits, pricing and API shapes change often. Before making a Neon-specific claim or writing code against the Neon API, fetch the page:

```bash
# Index of every doc page
curl https://neon.com/llms.txt

# Any page as markdown
curl -H "Accept: text/markdown" https://neon.com/docs/<path>
```

Find the path in `llms.txt`; do not invent URLs.

## Things that bite

- **Connections**: serverless and edge runtimes use `@neondatabase/serverless` (HTTP or WebSocket). Long-running servers use a normal Postgres driver. For many short-lived connections use the pooled connection string (`-pooler` host), which goes through PgBouncer in transaction mode, so session features (prepared statements by name, `SET`, advisory locks held across statements) are not available on it.
- **Scale-to-zero**: the first query after idle pays a cold start. Disable it for latency-sensitive production computes.
- **Branches** are copy-on-write snapshots of data and schema. Use one per preview deployment or per migration test, then delete them. Branches are not replicas and do not sync back.
- **Migrations**: test on a branch created from production, then run against main.
