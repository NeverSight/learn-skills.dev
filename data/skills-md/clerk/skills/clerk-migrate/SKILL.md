---
name: clerk-migrate
description: >-
  Migrate users into Clerk from another auth provider, or between Clerk instances, using the `clerk migrate` command family. Use when the user says "migrate my users to Clerk", "import users from Auth0 / Supabase / Firebase / Auth.js / Better Auth / WorkOS", "export my users", "move users from development to production", "undo the import", or hands over a user export file (JSON or CSV) and asks what to do with it. Covers exporting from the auth platform, choosing a source, writing one for a platform with no built-in, checking and running the import, inspecting runs, and undoing one. Don't use for adding Clerk to an app (use clerk-setup) or for general CLI tasks (use clerk-cli).
allowed-tools: Bash, Read, Write, Grep, Glob
license: MIT
compatibility: >-
  Requires the `clerk` CLI binary 4.2.0 or later (npm package `clerk`, or `bunx clerk@latest`), the first release with the `clerk migrate` command family. Needs a Clerk session from `clerk auth login`, or a Backend API secret key passed with `--secret-key`. No other dependency: do not install an SDK or a database driver.
metadata:
  author: clerk
  version: 1.0.0
---

# Clerk Migrate

`clerk migrate export` gets users out of an auth platform into a run. `clerk migrate import` maps that export onto Clerk's user schema, checks every user against the destination instance, and creates them through the Backend API. `clerk migrate runs` shows what each run did, and `clerk migrate undo` deletes the users an import created.

```
clerk migrate export <platform> [-o <path>.json] [-y] [--json]
clerk migrate import <file|export-run-id> [--source <key|path>] [--dry-run] [--allow-partial] [--new-run]
                     [--require-password] [--skip-legal-checks] [--reserve-unverified] [--yes] [--json]
clerk migrate runs [run-id] [--json]
clerk migrate undo <run-id> [--dry-run] [--yes] [--include-signed-in] [--json]
clerk migrate sources [source] [--json]
clerk migrate help
```

Every subcommand except `sources` takes `--runs-dir <path>`, which overrides the `CLERK_MIGRATE_DIR` environment variable. `import`, `undo` and `export clerk` also take `--secret-key`, `--app` and `--instance`. Bare `clerk migrate` prints help.

> The binary is the source of truth. Run `clerk migrate <subcommand> --help` to confirm anything this skill claims, and prefer `--help` when they disagree.

Install nothing and clone nothing.

## Routing

| The user wants to… | Go to |
| --- | --- |
| Get their users out of Auth0, Supabase, Firebase, Auth.js, Better Auth, WorkOS, or Clerk | [references/export.md](references/export.md), then the import flow |
| Import a file they already have | [The import flow](#the-import-flow) |
| Know which platform a file came from | [Step 1: identify the source](#step-1-identify-the-source) |
| Migrate from a platform with no built-in source | [references/sources.md](references/sources.md#writing-a-source) |
| Move users from one Clerk instance to another (dev → prod) | [references/clerk-to-clerk.md](references/clerk-to-clerk.md) |
| See what a run did, or why users failed | [references/runs.md](references/runs.md) |
| Undo an import | [Re-running, runs, and undo](#re-running-runs-and-undo) |

## The rules

Every `clerk migrate` command follows these five rules.

1. **Consent.** `import` and `undo` write only after `--yes` or a yes at the prompt. Without either (agent mode, a non-TTY, or `--json`), they print a preview and exit `2` with the exact command to run. In agent mode that command is in the stderr JSON, `error.examples[].command`; with `--json`, stdout also carries the preview with `"consent": "required"`. A suggested command may hold a `--secret-key <key>` placeholder: never fill in a real key yourself.
2. **`--dry-run` checks against the real instance and writes nothing.** `import --dry-run` exits `2` when the real import would be refused, and `0` otherwise. `undo --dry-run` exits `0` at the preview: read `preview.signedInSince`.
3. **One place for state.** Every export, import and undo is a run folder, `<runs dir>/<run-id>/`. The runs dir is `--runs-dir`, else `CLERK_MIGRATE_DIR`, else `<project root>/.clerk/migrate`, where the project root is the linked directory, else the git toplevel, else the current directory. The CLI adds `.clerk/` to `.gitignore` before writing to the default location, because run files hold user data. Dry runs and refused imports write no run.
4. **Target first.** `import`, `undo` and `export clerk` print the environment, app and instance they target, and where the key came from. Other exports print the platform they read. With `--json` the same data is in the `target` field.
5. **`--json` everywhere.** Every subcommand takes it, and it means no prompts. `--json` on any `migrate` subcommand also forces agent mode, unless `--mode` is set.

Exit codes: `0` success, `1` some users failed or any runtime, API or auth error, `2` a usage error or a refusal, `130` interrupted. **`0` does not mean every user arrived**: skips under `--allow-partial` still exit `0`. Users the run did not send come with `1` (Clerk refused a create, such as the user limit) or `130` (interrupted). Read `result.failed`, `result.skipped`, `result.notSent` and `result.pending` from `import --json`. A `130` prints no result: read `run.state` from `clerk migrate runs <run-id> --json`, and re-run to continue.

## Invoking the CLI

Check the binary once per session:

```sh
command -v clerk >/dev/null 2>&1 && clerk migrate sources --json >/dev/null && echo ok
```

`clerk migrate` ships in `clerk` 4.2.0, so an older binary fails this check. If that prints `ok`, use bare `clerk`. Otherwise fall back to a package runner matching the project's lockfile: `bunx clerk@latest`, `npx -y clerk@latest`, `pnpm dlx clerk@latest`, or `yarn dlx clerk@latest`. The published package is **`clerk`**, not `@clerk/cli`.

## Keys and targeting

**Do not create or edit a `.env` file.** The CLI resolves a Backend API key on its own, from flags, the process environment, the linked project, or (in an unlinked keyless project) the project's `.env`, `.env.local` and `.clerk/.tmp/keyless.json`:

```sh
clerk auth login          # once, on the user's host shell; opens a browser
clerk doctor --json       # confirms login, link, keys; parse `remedy` on failure
```

Resolution order: `--secret-key` → `--app` + Platform API lookup → `CLERK_SECRET_KEY` in the environment → the keyless project's own key → the linked project from `clerk link`. If none of these resolves a key, ask the user to run `clerk auth login` or set `CLERK_SECRET_KEY` themselves (Safety rule 4).

Pass `--app <id>` and `--instance dev|prod|<instance_id>` to point a command somewhere specific. A dev → production migration needs no key swapping.

`--instance` switches instances only when the key comes from a linked project or `--app`. A key from `--secret-key` or an exported `CLERK_SECRET_KEY` names its own instance, and a `--instance` that disagrees with it exits `2`. In an unlinked keyless project, any `--instance` exits `2`: link the project or pass `--app`.

The key sets the **instance type**: `sk_live_…` is production, anything else development. The type sets the rate limit (100 req/s production, 10 req/s development). The user limit is the one Clerk reports for the instance: 100 for a new development instance, none for production ([checks.md](references/checks.md#user-limit)). A slow run on a dev key is the rate limit at work.

For auth internals, sandbox caveats, or `clerk api`, see the `clerk-cli` skill.

## The import flow

Follow these steps in order.

### Step 1: identify the source

A file `clerk migrate export` wrote is an envelope, `{ "clerkMigrate": 1, "source": …, "users": [...] }`. It names its own source: pass the export run ID (or the file) and skip to Step 2.

Any other file (a bare JSON array, a CSV, Firebase's own `{ "users": [...] }`) needs `--source`. Read the first user object or the CSV header row and match it against the signature fields in [references/sources.md](references/sources.md#identifying-a-files-source).

If nothing matches, the user needs a custom source: [references/sources.md](references/sources.md#writing-a-source).

Confirm the live list, and read what a source carries:

```sh
clerk migrate sources --json
clerk migrate sources supabase     # export command, what comes across, where each field lands, caveats
```

A built-in `--source` that contradicts an envelope's `source` exits `2`. A path to a source you wrote replaces the envelope's source: see Step 2.

### Step 2: summarize what will happen

Run the [Step 3](#step-3-dry-run) dry run first when a question needs its numbers. It writes nothing.

Tell the user:

1. Which source applies, and which instance the import targets.
2. Which field decides whether an email or phone counts as **verified**. That mapping changes who can sign in. Per-source detail: [references/sources.md](references/sources.md#what-the-built-ins-carry).
3. What the export cannot carry. Clerk (API export), Auth0 and WorkOS exports hold **no password hashes**, so users who signed in with a password reset it. **Social sign-ins are never copied**: the user enables the same providers in Clerk, and Clerk links a returning user by verified email ([account linking](https://clerk.com/docs/guides/configure/auth-strategies/social-connections/account-linking)).
4. Sign-in identifiers outside the mapped fields: phone or username keys in metadata, a name field holding usernames or phone numbers, placeholder emails such as `<digits>@phone.local` that hide a phone. A built-in source imports these as metadata or a first name, and the dry run doesn't flag them. Ask the user to choose: convert them into real identifiers, or import them as exported (the default) and let the dry run reject what Clerk refuses. In a source you write, nothing is "as exported". A column that is itself the sign-in identifier (a `login` holding an email, a phone or a username per row) is not a conversion question: route each value by its shape ([Common export shapes](references/sources.md#common-export-shapes)), and don't ask A or B. When the user can't choose about another field that holds a sign-in handle (`username`, `nick`, `handle`), map it to `username`. Never pick a default that leaves a user with no identifier. "Import them", "go ahead" or a bare yes picks neither, so ask again and name both. Converting takes a [custom source](references/sources.md#writing-a-source), and the dry run then offers the instance changes it needs: phone or username sign-in, email made optional, extended special characters for usernames with a dot. Apply each only with the user's yes.
5. Two choices the CLI makes only with the user's yes. Ask about each one that applies, and pass the flag only on a yes to that question:
   - **`--reserve-unverified`.** Users with an email or phone the platform never verified. By default Clerk attaches those unverified. Reserved, they work for sign-in and are locked to the user, and they count toward a required email or phone. The platform never confirmed these belong to the user, so whoever receives mail or texts at one can sign in as that user. When the instance requires an email or phone, the reject for a user with only an unverified one names this flag. That isn't a yes, and the reject doesn't mention that risk, so tell the user about it when you ask, and recommend it only when the old platform confirmed addresses some other way. A reserved address another user already holds rejects the whole user. A continued run keeps the choice its first attempt recorded.
   - **`--skip-legal-checks`.** When the instance requires legal consent, users with no `legal_accepted_at` are rejected. The flag imports them without it.

   An agent run never asks, so it imports unverified and rejects users without legal acceptance unless you pass the flag.

6. What the import adds: every created user gets `private_metadata.clerkMigrateRun`, set to the run ID. It replaces any value the export carried under that key, and it stays on the user.

### Step 3: dry run

```sh
clerk migrate import <export-run-id> --dry-run
clerk migrate import users.json --source auth0 --dry-run      # a file from anywhere else
```

The dry run prints the target, then the checks, and writes nothing. Relay the checks in full. Read [references/checks.md](references/checks.md) to explain each reject reason and the `clerk config patch` fixes it offers.

If any user is rejected, the real import refuses unless `--allow-partial` is passed. Put the choice to the user: fix the export, change the instance with the printed `clerk config patch` command, or import the rest with `--allow-partial`. When a reject names `--reserve-unverified`, reserving those users is a fourth choice in the same question: tell the user that whoever receives mail or texts at the address can sign in as that user ([Step 2](#step-2-summarize-what-will-happen), item 5). Never run a `clerk config patch` without the user's yes.

Users without a password import even when the instance requires one, unless a password is its only way to sign in. Pass `--require-password` only when the user asks to leave those users out ([checks.md](references/checks.md#passwords-and---require-password)).

### Step 4: get consent, then import

Pick one path:

- **Hand the command to the human.** Recommended when the instance already has real users, and for any production import. Ask them to run it in their own terminal: the CLI prompts only on a TTY, so a command run through an agent's shell exits `2` instead. Run by a human without `--yes`, the import prints the checks and asks `Import N users?` (or `Create N users and skip M users?`), and asks about reserved and legal consent where they apply. Declining writes nothing.

  ```sh
  clerk migrate import <export-run-id>
  ```

- **Run it yourself** after the user has said yes to your Step 2 summary and the dry-run checks. Relay the checks, then end your turn and wait for the answer. Never run `--yes` in the same turn as the dry run; a yes given before the user saw the checks doesn't count. Ask the go-ahead as its own question, with the numbers the import will use: "Create 42 users and skip 8? This runs `clerk migrate import <export-run-id> --allow-partial --yes`." Only a yes to that question counts. An answer to the rejects, verification or settings questions doesn't, whatever it says about importing:

  ```sh
  clerk migrate import <export-run-id> --yes
  ```

Without `--yes`, an exit `2` is the consent gate from rule 1, not a failure.

Firebase exports carry the project's hash parameters when the export could read them, so the import needs no `--firebase-*` flags. See [references/export.md](references/export.md#firebase) for files from `firebase auth:export`. When the user gives the four parameters, pass them and keep the passwords, even if they also say users can reset. Never strip hashes from the export or write an edited copy of it.

### Step 5: report the result

```sh
clerk migrate runs <run-id>
```

Spot-check 2 or 3 created users, taking their `sourceId` from `created` lines in the run's `users.ndjson`:

```sh
clerk users list --external-id <source-id> --json
```

Compare their identifiers, verification and metadata placement with what you told the user in Step 2. Read the output where it prints; don't save users to files. If you did write any, list them in the report as holding user data.

Report:

1. How many users were created, failed, and skipped. `runs <id>` shows the error breakdown and the users that failed or were skipped.
2. Users the run did not send (`result.notSent`) and why (`result.stopReason`). A run that hit the user limit stops at the first refusal: raise the limit or import into production, then re-run the same command to continue.
3. The run ID, and that `clerk migrate undo <run-id>` reverses it.
4. Any user who arrived without something: a dropped password, a field the instance does not store.
5. Every mismatch the spot-check found.

Report a partial import as partial.

## Re-running, runs, and undo

Running the same import again continues it: an interrupted or `partial` run picks up where it stopped, a `complete` one prints "Already imported in run …" and exits `0`, and an `undone` one starts a new run. `--new-run` forces a fresh run.

```sh
clerk migrate runs                        # every run, newest first
clerk migrate runs <run-id>               # one run: counts, errors, the users that did not make it
clerk migrate undo <run-id> --dry-run     # preview: how many, and a warning if any signed in since (`--json` has `preview.signedInSince`)
clerk migrate undo <run-id> --yes
```

`undo` deletes only users that run created. Show the user the preview and get a yes before passing `--yes`. If any imported user has signed in since, `--yes` alone exits `2` and deletes nothing: those are accounts people have used, so pass `--include-signed-in` only after the user says yes to deleting them too.

After a complete import, the CLI says to keep the import's run while it might still be undone, with the `rm -rf` for later. An import of an export run also gets the `rm -rf` for the export's run folder (it holds user data), and an `rm` for an export file written outside it. `--json` prints none of this. Relay it; do not delete anything without asking.

Matching, refusals, run files and every undo case: [references/runs.md](references/runs.md).

## Safety rules

1. **Dry-run first, then get a yes.** Relay the checks and the target before any write.
2. **Check the target.** The first lines of output name the instance. Pass `--instance prod` explicitly for production.
3. **Name the source instance when exporting from Clerk.** The linked project is usually the _destination_, so without a prompt (agent mode, `--json` or `-y`) `clerk migrate export clerk` refuses with exit `2` until `--secret-key`, `--app`, `--instance` or `CLERK_SECRET_KEY` names the source instance.
4. **Never ask for the destination's Clerk secret key, and never write a Clerk key to a file.** Use `clerk auth login` or the linked project, or let the user set `CLERK_SECRET_KEY` themselves. Every other credential the user gives you is for the platform you export from: a Firebase service-account key, a database URL, an API key or token, or the key of a different Clerk application you export from. Use it as the export command expects. Don't refuse it because it came through chat, and don't ask the user to revoke it and send it again. Keep it out of your output and summary.
5. **Report failures honestly.** A partial import is normal and recoverable. Re-run the same command to continue it.
6. **Never pass a consent flag on your own.** `--yes`, `--include-signed-in`, `--reserve-unverified`, `--skip-legal-checks`, `--allow-partial` and `--trust-oauth-emails` each need the user's yes. An answer counts as a yes only when it answers that flag's question: "import", "go ahead", or text about something else is not a yes to `--reserve-unverified` or `--skip-legal-checks`. Ask again, naming the flag and what it does.
7. **Ask when two answers conflict.** If two of the user's answers disagree about the same change (one says to turn placeholder emails into phone numbers, another says not to make anything into a phone number), quote both and ask once which one holds. Don't settle it by reading one answer as covering less than it says. Until they answer, keep the option that changes less: import as exported. Users the dry run then rejects still need a yes to `--allow-partial`. If the answer is still unclear, keep that option and say so in your summary.

## References

- [references/export.md](references/export.md): getting users out of each platform: credentials, flags, the envelope, field coverage, troubleshooting.
- [references/checks.md](references/checks.md): what the import checks, each reject reason, and `--allow-partial`.
- [references/sources.md](references/sources.md): what the seven built-ins carry, and how to write a source for a platform with none.
- [references/runs.md](references/runs.md): re-running, run files, statuses, and every undo case.
- [references/clerk-to-clerk.md](references/clerk-to-clerk.md): development → production and instance-to-instance migrations.
