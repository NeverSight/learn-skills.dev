---
name: what-could-break
description: "Find what a change could break outside its own diff, then prove the one fact that makes it safe by running real code instead of writing an essay. Use before any multi-file edit or an edit to a shared path (API payload, config, stored data, a client other apps read, a prompt or policy file), when asked 'what could this break' or 'blast radius of X', for a small diff you do not trust, or when a task asserts something about existing code ('X already handles Y', 'just make X public') before you design against that assertion."
---

# What could break

Find what a change breaks somewhere else, before it ships. Run it before design,
not only before merge, whenever a task asserts something about existing code: that
assertion is a hypothesis, and the census of real consumers decides the design.

Listing callers is not the job. Grep does that in a second. The job is the breakage
grep will not show you, and one proof that the change is safe.

## Do not trust your own writeup

A risk analysis that sounds right is worthless. It reads as convincing whether or
not it is true. Find the one or two facts the whole change depends on and prove
them by running code.

For each such fact, get it as far down this ladder as is cheap, and say where it
stopped:

1. **You said so.** Worth nothing on its own.
2. **You pointed at it.** A real `file:line`, or the library's own source at the pinned version.
3. **You walked it.** You traced the bad case step by step and it does not reach.
4. **You ran it.** A script or test calls the real code and fails loud if you are wrong.
5. **You saw it live.** Reproduced in the running app, service or device.

Rung 4 is usually one small script that imports the same module production runs
and calls the exact function you are worried about, with the input you are worried
about.

## Steps

1. **Read the change.** The diff, the symbols it adds, changes and deletes, and what it now does differently, including what the diff does not spell out. `git log -S '<symbol>'` and `git log -L :<function>:<file>` show why the old shape exists; a guard that looks pointless often has a commit explaining the incident it stopped.
2. **Find the one fact it is safe because of.** Most risky-looking changes are safe because of one fact ("this only drops cache entries that are already expired", "no client reads this field"). Find it. If it holds, most risks clear at once. If you cannot find one, the change is not understood yet.
3. **Look where grep stops.** Walk the checklist below. Each item is a place the same rule, value or shape lives without sharing a symbol with your diff.
4. **Be honest about each risk.** A real chance and a real cost, or it does not make the list. Keep the confirmed ones. List the checked-and-cleared ones separately. Cite a real `file:line`. A search that found nothing is still an answer: write the search. Never invent a caller or an API.
5. **Prove the one fact.** Write the script or test that runs the real code, run it, and paste what happened. If you cannot run it, write "unproven" next to the fact.
6. **For a wide change, split it.** Repeat steps 2 to 5 per subsystem instead of stretching one writeup across everything.

## Where grep stops

Search for the literal value, the field name, the error text and the old behavior,
not only the symbol you renamed. Then check each of these by hand:

- **The same rule living twice.** A second config file (dev and prod, a Helm values file and an env file), a fallback path that hardcodes the old default, a copy synced into another repo or package, a constant duplicated in a migration or a test fixture, a feature flag default in the flag service.
- **Prompts and agent files that restate the rule.** System prompts, agent and skill files, `AGENTS.md`, `CLAUDE.md`, contributor docs, runbooks, onboarding scripts. An agent obeys the stale sentence, not your code.
- **Every other client.** Web, iOS, Android, desktop, CLI, browser extension, partner integrations, internal admin tools. A payload change breaks the client nobody rebuilt, and mobile clients in users' hands stay on the old version for weeks. Ask: what does an old client do with the new shape, and a new client with the old server?
- **Wire formats.** JSON field names and types, enum values, null versus missing, date formats, pagination shape, error codes, webhook payloads, queue message schemas, GraphQL and protobuf contracts, CSV exports someone imports.
- **Stored state.** Database columns and their defaults, rows written under the old shape that the new code will read, cache entries, files on disk, append-only logs, session and cookie contents, keys in a key-value store, search indexes. Old data outlives the deploy.
- **Environment and secrets.** An env var renamed in code but not in the deploy config, CI, the container image, or the second service that reads it.
- **Processes that restart separately.** Web server, background workers, cron jobs, schedulers, serverless functions, the mobile app, a sidecar. During a rollout one runs new code while another runs old code against the same data and queue. Can both versions coexist for an hour?
- **Timing and concurrency.** Two writers on the same file, row or key; a retry that now fires twice; a job that assumed it ran alone; ordering that only held because one step was slow.
- **Library source at its pinned version.** Read the dependency's code at the version in the lockfile, not your memory of its docs. Behavior differs between versions more often than names do.
- **Generated and vendored code.** Clients generated from an API schema, vendored copies, build artifacts committed to the repo, bundled assets with a cache-busting key that did not change.
- **Tests and fixtures that encode the old behavior.** A test that passes because its fixture still has the old shape proves nothing about the new one.
- **Observability.** Dashboards, alerts and log parsers matching on a message or metric name you changed.

## What to hand back

- **What it does.** What changed, including the part that is not obvious.
- **The one fact it is safe because of.** State it, name the rung it reached, show the proof (command and output). If you could not prove it, write "unproven" and say what would prove it.
- **Risks.** Each one: how it breaks, the `file:line`, how likely, how bad, and the check that would catch it.
- **Cleared.** What you checked, the search you ran, and why it is fine.
- **Before you ship.** The cheapest test or repro that catches the real bug, including the script you wrote, ready to rerun.

Keep secrets and private data out of the report and out of any script you leave
behind.

---

Includes material adapted from pstack by Lauren Tan (MIT). See LICENSE-pstack.txt.
