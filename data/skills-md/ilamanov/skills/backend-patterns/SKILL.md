---
name: backend-patterns
description: Generally-applicable backend/data best practices. Use whenever writing or modifying backend/data code — API routes, server actions, DB writes, background jobs, agent tools, import flows, webhooks, paste handlers, or anywhere data enters the system. Consult BEFORE writing the code so the patterns are baked in, not retrofitted. If a scenario described in the skill body matches the work, apply the pattern — don't ask, just follow it (call out the choice in one line so the user can override).
---

# Backend Patterns

Generally-applicable best practices for backend/data work. **Read every pattern below. If any matches what you're about to build, apply it.** Don't ask permission for things that are codified here — just follow the rule and note in one line that you did.

## When to consult this skill

Any time you are writing or editing code that:

- Saves, inserts, or persists a URL/link to a database
- Accepts a link from a user, agent, webhook, import, or paste handler
- Forwards a link to another system
- Adds a link to any knowledge-keeping surface (e.g. Kanban, Task Console, Knowledge Base, bookmarks, notes)
- Builds an agent tool that creates records containing links
- Queries or writes to the database (reads, inserts, updates, deletes)
- Changes the database schema, or runs migration/generate/push commands

If none of the patterns below match the scenario, return to the original task without comment.

## Patterns

- Whenever we are saving a social media link, it has to go through our auto-archiver (this mini-app will be added in the future).
  - If the auto-archiver doesn't exist in the codebase yet, do **not** silently store the raw link. Centralize all link-writes through a single helper (e.g. `saveLink(url, context)`) with a clearly-marked `TODO: route through auto-archiver once available`, so future wire-up is one change in one place.
- Prefer the ORM for database work; avoid raw SQL whenever possible. Reach for raw SQL only when it's genuinely necessary (something the ORM can't express), and call out why in one line when you do.
- Prefer server actions over API routes for mutations and form handling. Reach for an API route only when something genuinely requires it (e.g. a webhook receiver, a public/third-party HTTP endpoint, a non-form client that needs a REST/JSON surface). Consult the `next-best-practices` skill for guidance.
- Never apply schema changes to the connected database without explicit user confirmation first. Editing schema **source** files (e.g. the Prisma/Drizzle schema) is fine, but before running anything that mutates the connected DB's schema — `pnpm db:generate`, `pnpm db:migrate`, `pnpm db:push`, or direct schema-mutating SQL — stop and ask the user to confirm. This is the one place in this skill where you **do** ask first rather than acting.

## How to behave when this skill applies

1. Identify which pattern(s) match the work.
2. Apply them. Don't propose alternatives unless there's a concrete reason the pattern doesn't fit.
3. In one short line, tell the user which pattern you applied so they can override if needed.
4. If a piece of infrastructure the pattern requires (e.g. the archiver itself) doesn't exist yet, say so explicitly and explain what you did instead.

## Future patterns

This skill will grow over time. New patterns should be added as bullet points in the **Patterns** section above, phrased as rules the agent can apply mechanically.
