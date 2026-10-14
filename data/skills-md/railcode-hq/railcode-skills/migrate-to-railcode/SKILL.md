---
name: migrate-to-railcode
description: Migrate an existing project that was built for another host (Vercel, a Node server, a Docker container, a docker-compose stack) onto Railcode. Use when the user has a working app and wants it running on Railcode, including a Next.js app or a containerized backend in any language. Covers taking inventory of what the project depends on, mapping each dependency to a Railcode primitive, rebuilding the pieces that have no direct equivalent in a different way, porting, testing with railcode dev, keeping or connecting the project's existing database (Postgres or any other) and where schema migrations run, deploying beside the original, and reporting what Railcode cannot host yet. Do not use for a new app from an idea, or for moving a Railcode v1 app to apps v2 — both belong to create-railcode-app.
version: 0.2.1
---

# Migrate to Railcode

A migration is a port, not a rewrite: the project already works somewhere, and the job is to
keep what it does for its users while replacing what the old host provided (auth, a database,
env vars, cron, file storage) with what Railcode provides.

Most internal tools fit. Usually one or two pieces have no direct equivalent, and almost all
of those can be rebuilt a different way that the user will not notice — see
[Find another way](#find-another-way). A short list of things cannot be hosted at all today —
see [What Railcode cannot host today](#what-railcode-cannot-host-today). Know both lists
before you promise anything.

Guides by source project:

| Source project | Guide | Status |
|---|---|---|
| Next.js (App Router) | [references/nextjs.md](references/nextjs.md) | Supported as `"type": "next"`, built by `@railcode/next`. Proven on a real app, with gaps listed in the guide |
| A container: a `Dockerfile` or docker-compose stack running a server in any language | [references/containers.md](references/containers.md) | Method and mappings built from the platform's documented behaviour; not yet backed by a recorded migration |

For any other source, follow the method below and build the app with `create-railcode-app`.

Railcode's own `db` is meant for fast, simple use. It has limits for a lot of data or complex
queries (no joins, aggregates or transactions; paged reads), so a project that needs those
keeps its database. [references/databases.md](references/databases.md) covers those limits,
connecting a database as a data source, using it directly with a secret, databases Railcode
has no connector for, where schema migrations run, and how to register interest in a managed
Postgres through `railcode agent-feedback`.

## Update First

Before running a `railcode` command, update the skills and the CLI and confirm what is
published:

```bash
npx skills add Railcode-HQ/railcode-skills
npm install -g railcode@latest
railcode --version
npm view railcode version
```

If npm is unreachable, say so and do not claim this guidance is current. This version was
written against **CLI 0.3.8**, **`@railcode/sdk` 0.4.0** and **`@railcode/next` 0.1.0**.

This skill does not restate the SDK, the manifest or the deploy flow. Those live in
`create-railcode-app` (`references/worker-sdk.md`, `references/cli-workflow.md`,
`references/deployment.md`, `references/app-patterns.md`); read them when a step below names
an SDK surface.

## What Railcode is, for someone arriving from another host

Four facts shape every migration. Check the project against them first.

- **Every viewer is a signed-in member of the organization.** There are no anonymous visitors
  and no self-signup. Railcode hosts internal tools.
- **The backend is one worker module** on a Workers runtime (`nodejs_compat`), not a Node
  server and not a container. It runs once per request and keeps nothing in memory between
  requests. No filesystem, no child processes, no native addons, no raw TCP.
- **The worker runs only when a signed-in member's browser calls it, or on the app's own
  cron.** Nothing on the public internet can call it.
- **Authentication is ambient.** The platform signs the user in before any app code runs and
  hands the worker a verified `ctx.user`. The project's own login goes away, and that is
  usually the largest deletion in the migration.

In exchange the app gets, with no setup: sign-in, a store (`db`), file storage (`files`), an
LLM gateway (`llm`), email sending, per-app secrets, cron, connectors to the org's databases
and SaaS accounts, managed agents, deploy history and logs.

## Method

Work in this order. Do the inventory before touching code: most failed migrations port the UI
first and discover on day two that the data layer has no equivalent.

### 1. Inventory

Read the project and write down, with file paths:

| What | Where to look |
|---|---|
| Auth | NextAuth/Auth.js, Clerk, Supabase auth, Passport, a session cookie, a `/login` route |
| Data | An ORM (Prisma, Drizzle, SQLAlchemy, ActiveRecord), a database URL, a hosted KV or blob store |
| Secrets and config | `.env*`, `process.env.*`, `ENV` lines in a Dockerfile, the old host's dashboard |
| Scheduled and background work | `vercel.json` crons, a queue and its workers, a `setInterval` in a server, a cron container |
| Outbound calls | Every host the server code fetches |
| Inbound calls | Webhooks, public API routes, OAuth callbacks, anything not called by the app's own frontend |
| Files | Uploads, generated documents, an S3 client, a mounted volume |
| Processes and binaries | Every service in docker-compose, every `apt-get install`, every binary the code shells out to |
| Host-specific packages | `@vercel/*`, platform SDKs, edge-only APIs |

### 2. Map each item

| The project has | On Railcode |
|---|---|
| Its own login and sessions | Delete the authentication machinery. Read `ctx.user` (`id`, `email`, `name`, `is_admin`, `roles`). `appUsers` lists the org's members |
| A user table | Keep what is application data (profiles, preferences, app-level roles): move it to `db`. Railcode user ids are **not** the old ids — see step 4 before importing anything keyed by user |
| Per-user rows in its own database | `db` collections — one flat store per app, so put the user id in the key (`<userId>:<id>`) and enforce access in server code. Suited to small, simple data; for large tables or complex queries keep the database |
| A database it reads (Postgres, BigQuery, Turso) | Connect it as a data source: a data connector an org admin sets up. **Read-only.** Prefer saved queries (`query(name, params)`); direct SQL is `data(name).runSQL(...)` with `adhoc_sql:` in the manifest |
| A database it reads **and writes** | Keep it and use it directly: the connection credential in `railcode secrets`, the host under `egress:`, and a client that speaks HTTPS (no raw TCP). Or move the app's own tables into `db`. See [references/databases.md](references/databases.md) |
| A database Railcode has no connector for (MySQL, MongoDB, DynamoDB, Redis and so on) | The same: set its credentials as secrets, allow its host, and use it as before over its HTTPS API |
| Schema migrations (Prisma, Drizzle, Alembic, Rails) | Run them in the build or deploy script, on the machine that runs it, never in the worker. See [references/databases.md](references/databases.md#schema-migrations-run-in-the-build-script) |
| `process.env.SECRET` | `railcode secrets set NAME`, read as `secrets.NAME` |
| Cron jobs | `crons:` in `manifest.yaml`, each calling one of the app's own routes with `POST` |
| Outbound fetches | List each host under `egress:` |
| File uploads, a mounted volume | `files` |
| An LLM provider key and client | `llm`, with `llm: true` in the manifest |
| Transactional email | `email`, with `email: true` in the manifest |
| A SaaS API it calls with its own OAuth flow or API key | A connector an admin or the user links, called with `connector(name)`; or a secret plus an `egress:` host |
| A queue, websockets, a webhook receiver, a native binary, a search index | No direct equivalent. Go to [Find another way](#find-another-way) |

For every item with no direct equivalent, tell the user **before** porting: what the project
does today, how you propose to rebuild it, and what changes for them (for example "new
payments show up within a minute instead of instantly"). Get a yes on each one. A different
implementation the user agreed to is a good migration; an approximation they discover later
is a bug.

### 3. Port

1. Add the Railcode files (`railcode.json`, `manifest.yaml`) and get an unchanged page
   rendering under `railcode dev`.
2. Replace auth.
3. Replace the data layer, one entity at a time.
4. Move secrets, crons and egress into the manifest and `railcode secrets`.
5. Rebuild the pieces from [Find another way](#find-another-way).
6. Remove the old host's packages and config.

Keep each step runnable. A migration that only works when all six are done is one you cannot
debug.

`railcode dev` keeps `db` and `files` in local scratch storage, but SQL, connectors, email,
`llm` and agents are forwarded to the real instance. Testing a route that sends email sends
email.

### 4. Deploy beside the original

Deploy to a **new app slug** and leave the original running. Nothing about a first deploy is
destructive, and the user can compare the two. Only move data and switch people over once the
new app has been checked.

Existing data does not move by itself. If it matters, write a one-off import (a script that
reads the old store and writes through a temporary admin-only route, or
`railcode app kv` from the CLI), run it once, and delete it.

Records owned by a user need their owner translated. The old app's user ids mean nothing on
Railcode, so importing rows under their old ids leaves them unreachable. Build the mapping
first — old id → email → the Railcode member with that email (`appUsers`) — show the user who
did not match, and only then import, writing each record under the Railcode id.

### 5. Verify, then report

Load the deployed app as a real user and exercise each migrated feature; a green deploy says
only that the bundle uploaded. `railcode logs app --app <slug>` lists every invocation, and
`railcode logs app <invocation-id>` shows its console output and errors.

Report in this order: what works and how it was checked, what was rebuilt differently and
what changed for the user, what was left out and why, what the user must still do (secrets to
set, connectors to link, data to import).

## Find another way

When a piece of the project has no direct equivalent, do not stop and do not drop it. Ask what
the piece is **for**, not what it is built from. A queue exists so that slow work finishes
without the user waiting. A webhook exists so the app learns about a payment. A websocket
exists so a list looks current. Each of those outcomes can usually be reached with a cron, the
store, and a frontend that polls.

The building blocks you have:

- **A cron that fires as often as once a minute** and can use `db`, `files`, `llm`, `email`,
  `secrets`, egress, SQL and org connectors.
- **A store you can use as a queue, a cache, a lock or a cursor.**
- **A frontend that can call the worker as often as it likes.** A browser tab has no
  subrequest budget and stays open, so it can drive long work one step at a time.
- **Managed agents** for work that is long, needs code execution, or reads files with AI.
- **Connectors** to the org's existing databases and SaaS accounts.
- **Outbound HTTP to any host you declare**, so a hosted API can do what a local binary did.

Shapes that work:

| The project does this | Build it like this | What changes for the user |
|---|---|---|
| Receives a webhook to learn that something happened (a payment, a new issue, a form entry) | A cron polls the provider's list or events API. Keep the last-seen id or timestamp in `db` as a cursor, and make processing idempotent | Up to a minute of delay |
| Runs a job queue (BullMQ, Celery, Sidekiq) | A `jobs` collection. Routes insert rows with `status: "queued"`; a cron route takes a small batch, processes it, marks each row done. Cron runs are at-least-once and may overlap, so stamp claimed rows with `ctx.invocationId` and keep side effects safe to repeat | Jobs start within a minute, not instantly |
| Does one long task in a request (a big import, a report over thousands of rows) | Split it into steps with a cursor in `db`. The frontend calls a step route in a loop and shows progress, or a cron advances it. Keep each step well under the ~100 subrequest budget | A progress bar instead of a spinner |
| Pushes live updates over websockets or SSE | The frontend polls a cheap route every few seconds, only while the tab is visible. Return an `updated_at` so an unchanged poll is a tiny response | Updates arrive within the poll interval |
| Streams text to the browser | Return a streamed `Response`; `toNdjson()` in the SDK does the framing | Nothing |
| Joins and filters in SQL on its own database | Design keys for the reads the screens make (`<userId>:<id>`, `prefix()`), store a little duplicated data, filter with `query().where()`, and paginate until a short page. If the data is shared with other systems, leave it in that database and read it through a data connector | Nothing, if the keys match the screens |
| Writes to a relational database that must stay relational (transactions, constraints, other systems read it) | Keep the database and use it directly from the worker with a secret and an HTTPS driver ([references/databases.md](references/databases.md)). Data connectors are read-only, so they cover the reads only. If the database has no HTTPS interface, put one in front of it or keep a small write service on the old host | Nothing, when an HTTPS driver exists |
| Caches in Redis or in process memory | A `db` collection with an `expires_at` field checked on read. In-memory caches do not survive between requests | Nothing |
| Rate-limits or locks with Redis | A `db` row per key holding a counter and a window start. It is not atomic, so use it for fairness, not for money | Nothing |
| Full-text search over its own records | For a few thousand records, load and filter in the worker or the browser. Beyond that, query the source database through a connector, or call a hosted search API through `egress:` | Nothing |
| Shells out to a binary (ffmpeg, ImageMagick, Chromium, pandoc) | First look for a pure-JavaScript library that fits in the worker bundle; PDF and spreadsheet generation usually do. Otherwise call a hosted API through `egress:`, or hand the job to a managed agent, which can run code | Possibly a slower or asynchronous result |
| Runs its own OAuth flow against Google, Slack, GitHub and so on | A connector. An admin links an org account, or each user links their own; the worker calls `connector(name)` and never sees a token | Users link the account once in Railcode instead of in the app |
| Receives email, or sends from a real person's or team's address | A Gmail connector for that account: polled on a cron with a stored cursor when org-owned, or read by a personal managed agent on a schedule for one person's own inbox | Up to a minute of delay on inbound mail |
| Needs embeddings, vision or another model feature the `llm` gateway lacks | Call that provider directly: the key in `secrets`, the host in `egress:` | Nothing |
| Sends push or chat notifications | `email`, or a Slack connector posting to a channel | The notification arrives in email or Slack |
| Has one public page among many internal ones (a public form, a status page) | Split it. Leave the public page on the old host writing to its database; the Railcode app reads that database through a data connector | Two deployments instead of one |
| Renders HTML on the server with templates (Jinja, ERB, EJS) | A static frontend that fetches JSON from `/api/*` routes | Nothing |
| Has several services in docker-compose | One worker with several route groups. If two parts have different audiences, make them two apps | Nothing |

Rules for doing this well:

- **Say what changes.** Every row trades something, usually latency. State it in one sentence
  and get agreement before building.
- **Prefer the simplest block.** A frontend poll beats a cron; a cron beats an agent.
- **Check the cron limits before designing around one**: one-minute minimum, five schedules
  per app, no caller (`ctx.user` is `null`), and it cannot start or read managed agent runs.
  One cron route can dispatch several kinds of work when five schedules is not enough.
- **Do not fake a guarantee.** If the original relied on a transaction, exactly-once delivery
  or an instant response to a third party, a polling version does not provide it. That
  belongs in the next section.

If the user needs something that is not in this table, design it from the building blocks,
tell them it is a new pattern, and report it (see [Feedback](#feedback)) so it can be added.

## What Railcode cannot host today

Some things have no workaround, because they need the internet to reach the app, a process
that stays alive, or a runtime the platform does not offer. Recognise these during the
inventory, not after the port.

| The project needs | Why it does not fit |
|---|---|
| **Inbound webhooks that must be answered** — Slack slash commands and interactive buttons, Twilio voice or SMS replies, a provider that retries until it gets an acknowledgement and offers no API to poll | Nothing outside the organization can call the worker. A webhook that only *notifies* can be replaced by polling (above); one that expects the app's response cannot |
| **A public API or public endpoints** for customers, partners, mobile apps or other servers | Same reason. Requests come from a signed-in member's browser or from Railcode's own agents, never from an outside system |
| **Public or customer-facing pages**: a marketing site, a storefront, self-signup, anything meant for search engines | Every viewer is a signed-in org member |
| **Its own identity system**: logging in people who are not org members, issuing its own API keys or tokens to third parties | Identity is the organization's membership |
| **True real time**: collaborative editing, presence, multiplayer, a websocket server | There is no push surface. Polling covers "looks current", not "keystroke by keystroke" |
| **A long-lived process**: a daemon, a bot holding a socket open, a stream consumer (Kafka, Postgres `LISTEN`), work that must fire more often than once a minute | The worker runs per request and then stops |
| **Non-HTTP protocols**: a database driver over TCP (`pg`, `mysql2`, `ioredis`), an SMTP server, gRPC | No raw TCP in or out. Databases are reached through a data connector (reads) or an HTTPS driver with a secret (reads and writes); see [references/databases.md](references/databases.md). A database with only a socket interface and nothing in front of it cannot be reached |
| **The container itself**: a Python, Go, Ruby, Java or PHP server run as it is, system packages, native addons, a GPU, a local model | The backend is one JavaScript module. Other languages are ported, not hosted — see the [container guide](references/containers.md) |
| **A large or multi-file backend bundle**: `.wasm` modules, a worker over the size cap (10 MB; 5 MB on a server without `worker_routes`) | The worker is a single ESM module |
| **A custom domain, a native mobile app, browser push notifications** | Apps are web apps at `<app>.<parent>` |
| **Its own mail domain**: an inbound mail server, an address the app owns, or `email.send()` from a custom sender | `email` is send-only from a platform sender. Mail through a Gmail account someone owns is supported; see [Find another way](#find-another-way) |

When the project needs one of these:

1. **Tell the user at once, plainly.** Name the feature, and say in a sentence that it cannot
   run on Railcode today and why. Do not present a polling imitation of something that needs
   a response as if it were equivalent.
2. **Offer what is still possible.** Usually the rest of the project migrates and the one
   piece stays where it is, sharing a database that Railcode reads through a connector. If
   the missing piece is the core of the project (a public storefront, a Slack bot), say the
   project should stay on its current host for now.
3. **Submit the request with the CLI.** The Railcode team decides what to build next from
   these reports. Send one for each distinct missing capability, even when part of the
   project migrated:

   ```bash
   railcode agent-feedback --category suggestion \
     --message "Migration blocked on inbound webhooks. The project receives POST /webhooks/slack for slash commands and must reply within 3 seconds; there is no API to poll instead. Request: a way for an app to expose a public, signature-verified endpoint." \
     --context "Source: Express + Postgres in a container, about 40 routes. Everything else mapped to db, secrets and crons. The Slack routes stayed on the old host; the rest was migrated." \
     --agent "<your assistant name>" --model "<your model>"
   ```

   Write it so someone who has never seen the project understands the need: what the project
   is (stack and rough size), exactly what it needed, what you did instead, and whether the
   migration went ahead. Leave out credentials, customer data, source code and anything that
   identifies the user's customers. The command needs an existing login and prints
   `Feedback accepted.`; all options are in `create-railcode-app` under "Report Railcode
   feedback". If it fails, tell the user the report was not sent and carry on.
4. **Tell the user you sent it**, and what it said.

Do not file a request for something the platform already does a different way; check
[Find another way](#find-another-way) and `create-railcode-app` first.

## Machine safety

Framework builds are heavy, and a migration runs many of them.

- Run one build or dev server at a time, and stop every process you start before finishing a
  turn. Check with `ps` rather than assuming.
- Never point a `package.json` `build` script at something that calls the framework's adapter
  if that adapter runs `npm run build` itself. That is an unbounded chain of builds. The
  Next.js guide has the specific rule.
- Do not start the project's docker-compose stack to see how it works unless the user asks.
  Read the code.

## Feedback

After every migration, report concrete friction with `railcode agent-feedback` (usage above
and in `create-railcode-app`), one report per finding: what the source project used, what had
no equivalent, which rebuilt pattern you used, and what broke that the guide did not predict.
A missing capability is `--category suggestion`; a wrong or unclear step in this skill is
`--category friction`. That is how the next guide gets written.
