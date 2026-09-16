---
name: setup
description: Wire or repair this repository's Veris execution path, verify an application run, and save the working command for later development. Use for initial setup or changed wiring when the engineer names this command.
argument-hint: "[service names...]"
disable-model-invocation: true
---

Wire this repository to Veris, once. Re-running skips what is already done.
Setup owns transport selection and configuration. Save the chosen path's preparation,
execution, evidence and cleanup steps in **How to run** so `build` and `fix` can reuse
them without selecting a transport again.

Setup delivers both a proven application run and the handoff that `build` and `fix`
consume: `.veris/twin.yaml`, `.veris/NOTES.md` and `.veris/setup.json` (a verified
plugin session uses its session metadata instead of `twin.yaml`). Ledger helpers are
optional. Reuse a successful execution of the exact saved command for the handoff;
do not repeat it at finish. Without Git, create the same files and skip the commits.

Three rules, always:

- Never modify the application code, and never point it at a sandbox. The one
  exception is the direct tier in step 3, where the app already reads each vendor's
  URL from an environment variable and production sets that same variable. Everywhere
  else, the container or hosted tier redirects the app's traffic from outside the
  process, and the code keeps its production hostnames and credentials.
- Never print an API key. Login/status output masks platform keys, but data reads
  can return complete vendor credentials. Redirect credential-bearing data into
  a protected file and keep values out of commands, reports, and terminal output.
- Ask before creating an environment, installing anything, or promoting a sandbox.

The main CLI is `veris`; hosted runners have their own provider commands.
`veris <command> --help` lists its flags. You run without a terminal, so every answer
you mean to give has to be a flag. `--yes` confirms.
A command that would otherwise stop and ask refuses instead, and names the flag it needs.
Every `get` and `list` takes `--json`. `env get` and `env use` accept the shortened id a
table prints; `--from` needs the full id, which `--json` prints.

For credential-bearing tables, establish the destination **before the first read**:
`umask 077; CREDS_DIR=$(mktemp -d)`, then redirect the data command to a file under
`"$CREDS_DIR"`. Inspect field names with `jq 'map(keys)'`, not raw rows. Extract values
directly into the app's credential file or environment without displaying them.
Keep variable names and extraction commands in the handoff, never the extracted
values. JSON-selector errors can quote the rejected value, so redirect parser
stderr into that protected directory too. Moving a value into a protected file
after printing it does not undo the disclosure.

## 0. Check the current session

Before any local CLI, login or Docker checks, inspect the available plugin tools
and runtime context. If they indicate that this session already executes inside a
plugin-managed sandbox, read [../veris-reference/session.md](../veris-reference/session.md),
verify it live and follow its setup path. It replaces the provisioning/run/cleanup
steps below, then rejoins the shared notes and metadata. A plugin with no
attached twin has an unmet provider prerequisite; do not provision a replacement.
Missing Docker or an API key alone does not select this path.

## 1. Check the machine

Check `git rev-parse --verify HEAD` and `git remote -v` as well. Without a Git
commit, setup, `build` and `fix` can still run; only the optional source-record helper
needs a commit to pin its comparison base.
Without a PR remote, keep a local change description; do not initialize Git or add a
remote unless the engineer asks. Instructions to commit below apply when Git exists.

Run `veris doctor`. It prints one line per check, in this order: the binary's version,
login, control plane, gateway mode, the vendor hostnames the plane serves, Docker,
tunnel binary (cloudflared), certificate file, project file, environment, sandbox.

Some lines appear only when they apply. Gateway mode and the vendor hostnames need you
logged in and the plane answering, so on a fresh machine they are simply absent. The
environment line needs a project file. A live sandbox adds its clock and its callback
registration. A `VERIS_API_KEY` in your shell that overrides the profile's own key adds
a warning just after the login line.

`✓` passed, `!` worth knowing, `✗` will fail a run. Doctor changes nothing itself; a
`→` line names the command that would. It exits 1 when any check failed. `--json` puts
the same checks on stdout.

- `command not found`: `veris` is not installed, and nothing else here installs it. Ask
  the engineer, then run the line for their machine. macOS and Linux:

  ```sh
  curl -LsSf https://raw.githubusercontent.com/veris-ai/veris-cli/main/scripts/install.sh | sh
  ```

  Windows:

  ```powershell
  powershell -c "irm https://raw.githubusercontent.com/veris-ai/veris-cli/main/scripts/install.ps1 | iex"
  ```

  No root and no package manager are needed. On macOS and Linux the binary lands in
  `~/.local/bin`, so a second `command not found` means that directory is not on the
  PATH: say so and stop.
  Done when `veris doctor` prints its version line.
- `✗ Not logged in`: run `veris login`. It prints a pairing code and a console link.
  Show both to the engineer and tell them to approve the pairing in the browser. Then
  wait: the command finishes by itself once the pairing is approved, and saves the key
  under the profile. `--no-browser` prints the link without opening a browser. For
  another control plane: `veris login --profile dev --api-base <url>`. In CI nobody can
  approve a pairing, so `veris login --key-stdin` reads an existing key from stdin.
  `veris whoami` shows which key, organisation and plane a command would use.
- `!` about Docker: the container tier in step 3 needs a running daemon. If the
  engineer requested hosted execution, check that tier's gateway and provider
  prerequisites instead. Otherwise ask them to start Docker; if this machine cannot
  run a daemon, the hosted tier in step 3 is the path. Never fall back to running
  without `--image` for code under test. The hosted tier's gateway check is in
  [../veris-reference/hosted.md](../veris-reference/hosted.md).
- `✗` with `no such host` for the control plane, or `!` with `permission denied` on
  `docker.sock`, on a machine where the engineer says both work: you are sandboxed.
  [../veris-reference/troubleshooting.md](../veris-reference/troubleshooting.md),
  **The agent is sandboxed**. Stop there.
- `!` about a missing project file or sandbox on a fresh repository is the expected
  state, not a problem.
- Any other `✗`: say which line and how to fix it, then stop.

## 2. Find what the code calls

Read the code, not the README: SDK imports, hostnames, base-URL settings. List every
vendor **hostname** on the tested path.

`veris services` is the catalog. It prints one line per twin: the twin's name, what it
stands in for, the variable its URL is handed to the app under, and the vendor
hostnames the proxy intercepts for it. The name is what `--services` takes.

A twin printed as `name (+issuer)` signs in through a family issuer, and the control
plane deploys that issuer with every sandbox holding the twin: google-calendar arrives
with google-identity. `--services` takes the bare name, and naming the issuer as well
changes nothing. So a sandbox holds twins the environment never named, and
`veris status` marks each one `+`. Neither the twin nor the mark is an error to fix.

A twin with no hostnames is not intercepted, for one of two reasons. It may be a data
plane: the app connects to it directly, using a URL the run hands to the app, instead
of having a hostname redirected. A database is the usual case. Or this control plane
serves no hostname for it yet. `veris doctor`'s vendor-hostnames line names every twin
in that state, and only postgres and yente belong there. List a data plane the app
itself needs as well — its own database, a self-hosted service — since a suite that
needs it fails without it.

Match hostnames, not vendors. A vendor may use several hosts, and a twin may cover only
some of them: Stripe's twin answers `api.stripe.com`, and the files and meter-events
hosts are not covered. Several twins may also answer the same hostname, as the three
Google twins all list `www.googleapis.com`. The sandbox routes those by path, so
include every twin whose paths the code calls.

A hostname with no twin is a limitation. Write it down in step 7, and do not mock it.

Names given with this command are the starting list. Show the engineer the final list
and ask before creating anything.

## 3. Pick the tier, then build the image

There are three ways to run the tests, and each one is called a tier. Decide before
building anything. An explicit request to run remotely selects the hosted paragraph
below, even when Docker works. Otherwise apply the direct-tier gate from the code,
then use `veris doctor` to choose between container and hosted execution.

Look at every vendor call on the tested path. If each one builds its URL from an
environment variable the app already reads, and production sets those same variables
with the real hostname only as the default, then setting those variables is the shipped
code path. No proxy is needed. That is the direct tier.

In the direct tier, go to
[../veris-reference/direct.md](../veris-reference/direct.md), do its gate and its
wiring, then rejoin here at step 7. Skip the rest of this step, and skip steps 5 and 6:
there is no image and no proving run. Step 4's environment rules still apply to the
environment that wiring makes, so read `veris env list --json` first and reuse one that
already has every service. Step 4's proxy flags do not apply.

One hardcoded vendor hostname, in the app or inside an SDK it calls, needs redirection
through the container or hosted tier. So does a vendor base URL the app registers
that no twin publishes an env hint for, unless no tested path reaches that base. In the direct tier
such a base keeps talking to the real vendor and nothing catches it. `veris services`
names the hint variable for every twin, and it needs no sandbox, so check for a
missing hint here, before anything is running.

The container tier is `veris run --image`: the tests run in a container with the proxy
beside it. It is the default for code needing redirection when Docker is available.
It covers every runtime and can patch an SDK's bundled certificates.

The hosted tier runs the tests in a remote box whose outbound proxy is the twin's
gateway. Choose it when the engineer requests remote execution, or when the code
needs redirection and `veris doctor` reports unavailable Docker that cannot be started
here. With no explicit hosted request, the direct-tier gate above comes first.
In it, go to [../veris-reference/hosted.md](../veris-reference/hosted.md), check its
gates and follow the chosen provider's recipe for *What it needs*. Then rejoin
here at step 4 with no image: leave `--image` out, so `proxy.image` stays unset.
Step 5 is unchanged, and step 6 uses the provider's run steps and the hosted receipt
rule. Skip the rest of this step.

Use any image that runs the tests: the repository's own test image or a Dockerfile
stage, or a stock toolchain image with the repository mounted. Build it now; step 4
records its tag. Nothing Veris-specific goes in the image: no key, no certificate, no
proxy settings. If deriving the image took real work, keep it as `Dockerfile.veris` at
the root with a comment naming the build tag. If the tests cannot run in a container
at all, stop and tell the engineer. Done when `docker image inspect <tag>` succeeds.

When the proving run in step 6 fails before the app reaches the vendor — a module the
interpreter cannot find, an import that does not resolve, a binary not on PATH — fix the
image and rebuild it. Do not repair the run line with `-e PYTHONPATH=…` or a mount over
the image's own copy: `.veris/NOTES.md` records commands that work against the image as
built, and every later run inherits the workaround. The usual cause is installing the
project before its source is in the image. With uv:

```dockerfile
FROM ghcr.io/astral-sh/uv:0.9-python3.12-bookworm-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project
COPY src ./src
COPY tests ./tests
RUN uv sync --frozen
```

Dependencies first, so they cache; the project last, once its source exists.

## 4. Create the environment

```
veris env create <project-name> --services stripe,asana --ttl 60 \
  --command '<the smallest test command that calls a vendor>' \
  --image <tag> --require-service stripe --default
```

An unknown service name is refused and the catalog is printed. Take the name from
`veris services`.

The `--ttl 60` above is a choice, not a requirement. Leave `--ttl` out and none is
recorded, and the control plane applies its own default. A number outside what the
server allows is refused, and the refusal names the bounds. Budget for image pulls,
builds and read-back; pull the workload image before `veris up`. A running sandbox
cannot be extended. Save evidence before expiry and before teardown.

`--boot`, `--snapshot`, `--data` and `--command` behave the same way: each is recorded
only when given, and nothing is written for the ones left out, so a sandbox boots the
bundle, seeds nothing, and `veris run` takes its command after `--`. Only the name and
`--services` (or `--from`) are required off a terminal, so pass a flag because you want
what it records, not to answer a question. The one pairing is `--boot snapshot`, which
is refused without `--snapshot ID|NAME`.

Before creating an environment, run `veris env list --json` and read the name and
services of every environment already on the server. **Adopt one only when it is this
project's: its services are exactly your list, or its server name is the project's.**
Then `veris env create <project-name> --from <full id>`, with the same remaining
flags. Otherwise create one named for the project, even when an existing environment
contains every service you need. A superset boots and bills twins the code never
calls, and another project's environment is shared with it: `env delete --server` and
`baseline promote` by either side land on both. When you adopt, the question you ask
before creating anything names the environment as the server does, with its id, and
says it is shared. `--from` and `--services` cannot be combined, so an adopted
environment keeps the server's service list and you cannot extend it here. Names are
not unique on the server, so say which id you used.

Confirm the complete service union for all entry points before creating the environment.
An omitted service requires a new environment; changing local defaults does not add it.

The name and services go to the server. Everything else is written to
`.veris/twin.yaml`, under the environment: the TTL if you gave one, boot source, data
files, the test command as `run.command`, and a `proxy:` block built from the proxy
flags:

```yaml
environments:
  <project-name>:
    proxy:
      image: <tag>
      require_service: [stripe]
```

Commit `.veris/twin.yaml`. `veris run` reads both settings from there, so the daily
command carries neither flag. `--require-callback`, `--expose <port>` and `--strict`
land in the same block.

For multiple entry points, keep one default and record a full command per flow in
NOTES, including each flow's `--require-service` and any callback flags.
`require_service` is a list, and explicit `--require-service` flags replace the list
for that run. A different command after `--` does not replace the requirements.
For incompatible defaults, such as a webhook flow and a flow with no receiver,
record separately named local entries using `veris env create <flow> --from <full-id>` with each flow's own flags, and select one with `veris run --env <flow>`.
Read its settings back with `veris env get <flow>`.
Adoption writes local defaults without creating another server environment.
Do not claim another entry point is verified because the default went green.

Mounts, `-e` variables, `--patch-bundled-cas` and `--cap-add` have no key in the file.
They go in the `veris run` line you record in `.veris/NOTES.md` at step 7. Data files
are none unless `--data` names them. The command also adds `.veris/twin.local.yaml` to
`.gitignore`; that file is per-machine and is never committed. Done when `veris env get`
shows each setting, where it came from, and the server's record.

## 5. Bring up a sandbox

Run `veris up`. It creates a sandbox of the environment and remembers its id for this
folder at once. Then it waits until the control plane reports the sandbox ready and
every twin answers. It adds the environment's data files, and prints each twin's URL
and the variable that URL is handed to the app under. A twin the environment never
named is a sign-in issuer the platform added (step 2), and the line beside its hint
says so.

Done when it exits 0 and lists the twins. `veris status` shows the sandbox at any time:
its state, boot source and expiry, and every twin's status, env hint, URL and table
counts. A sandbox lives for its TTL, then disappears.

On failure, read the exit code. A sandbox that failed is exit 1, with the reason. A
sandbox still provisioning when the wait runs out is exit 4. That wait is five minutes
by default, and `--timeout 10m` gives more. Exit 4 keeps the sandbox and it may still
come up, so check `veris status` later. A data file the twin refused is exit 1 with the
sandbox kept: fix the file, then add it with `veris sandbox data add <file>`.

## 6. Prove it

```
veris run --patch-bundled-cas -- <the smallest test that calls the vendor>
```

Add what the command needs, the same way `docker run` would.

On the hosted tier there is no `veris run`. Use the provider's recipe to run the test
command in the provisioned box. Its receipt is the twin's trace read since a watermark:
[../veris-reference/hosted.md](../veris-reference/hosted.md), *Provider recipe* and
*The receipt*. Its done-when is there. The rest of this step is the container tier's;
rejoin at step 7.

- `-v` to mount the repository where the image expects the code, when the image does
  not already contain it. `docker image inspect <tag>` names the image's WORKDIR.
- `-v <dir>:/run/keys:ro -e KEYS_DIR=/run/keys` for a credentials directory the app
  reads. Read the twin's Credentials section before filling it. Use its published
  synthetic credential or an issuer-provided token when required; permissive mode
  does not make an invented token valid. The auth guidance below explains the handoff.
- `-e` for any variable the test expects.

Mount nothing but the repository, a dependency cache, or a credentials directory.

`--patch-bundled-cas` appends the proxy's certificate to every SDK-bundled CA file it
knows: certifi, botocore, stripe, httplib2. Stripe, botocore and httplib2 need it, and
it costs nothing when the image bundles none. `--receipt <file>` writes the receipt to
that file as JSON, and never to stdout.

The run prints two counts per twin:

```
veris: the sandbox received 6 request(s):          ← what the proxy saw leave the app
  stripe   6
veris: the sandbox recorded 6 request(s) since the watermark:   ← what the twin logged
  stripe   6
veris: ✓ required stripe ≥1: saw 6   ✓ ledgers agree (6 = 6)
```

Those two counts are the run's two ledgers. The counts, and the verdict line under
them, are the run's receipt.

Sandbox totals can exceed proxy totals: a product twin may verify a token with its
sibling issuer inside the sandbox. Concurrent traffic can also contribute. Compare
per-twin traces before diagnosing a mismatch. Agreement alone does not prove the
application succeeded, and a difference needs an explanation from the traces.

**Done when the run exits 0, its requirements pass, and the receipt and read-back
identify traffic from the intended application flow.** A data plane may appear only
in the sandbox ledger. Internal issuer traffic alone does not prove the app ran.

Counts above zero are not enough on their own. If both counts are above zero but the
run failed, read the application error and the failed requirement. A vendor refusal,
a missing callback, or a later application assertion can each fail after traffic
arrived. Read the twin's auth mode with `veris sandbox data get <twin> auth`.
Permissive credential checking does not remove a family issuer's token-provenance
requirement: product twins such as Google Calendar still need a token from their issuer.
An `enforced` twin checks credentials against its known state. Read the twin's own
Credentials section with
`veris sandbox services manual <twin> --raw`; it says where those published credentials
live. Use `veris sandbox data get <twin> <table> --json` because the table
view truncates long cells. Redirect that JSON into a new file in an owner-only temporary directory
outside the repository (`mktemp -d`, with `umask 077`), then extract only the fields the app needs
into its environment or a read-only credential file. Do not echo values or save them
in evidence, and remove temporary credential files after the run. If a tool refuses
credential access, resolve that permission; do not reroute it to bypass the refusal.
Then give the app a credential the twin takes, or prove the wiring with a twin
whose credential you have. Either way, it goes in step 7 under **Credentials and
versions**.

Then record the full command in `.veris/NOTES.md` at step 7. `twin.yaml` holds only the
image, the required twin and the command after `--`. Only a mount that produced a
receipt goes in *How to run*. So if a later task will need a mount this run did not use
— the repository over the image's baked copy, a fixture tree — prove that mount here
too.

The command and the required twin that finally went green may not be the ones step 4
recorded. If they are not, re-record them with
`veris env create <name> --from <full id> --force`. Carry every flag the entry already
has: the corrected `--command` and `--require-service`, plus the same `--image` and
`--default`, and the same `--ttl`, `--boot` and `--data` when the entry records them.
The entry is replaced, not merged, so a flag you leave out is dropped. Drop
`--require-service` and every later run stops asserting the twin, then passes green on
an empty receipt. Without `--from` the command would also create a second environment on
the server. Re-run `veris env get` afterwards and check step 4's done-when again.

Your own `veris sandbox` reads do not count toward a run's totals. A run sets a
watermark when it starts and counts only what the sandbox recorded after it. Any
`/veris/*` reads you make while the run is going appear on a separate
`control-plane (/veris/*)` line, marked not counted.

A check passes when either count meets it. When one side alone decided a `✓`, the line
says which: `(engine; …)` or `(sandbox ledger; …)`. Exit 4 means neither count could
settle a check, so the outcome is unknown. Run it again. If it repeats, check
`veris status` and report it.

For an inbound flow, use `--expose <port>` and `--require-callback <path>` as well as
`--require-service`. Follow [../veris-reference/webhooks.md](../veris-reference/webhooks.md)
for registration, signing and delivery read-back. Prove the receiver's own assertion;
a successful payment does not prove receipt of its webhook.

Exit 3 means a requirement was unmet. If it names a callback, follow the webhook
reference before changing outbound wiring. For an unmet service requirement, check:

1. The test never calls the vendor: an in-process mock still active, a filter that
   skipped it. Pick a test that does.
2. The vendor's hostname is not one the environment's twins answer for: compare the
   code's hostnames with `veris services` and `veris env get`.
3. The SDK refused the certificate: `CERTIFICATE_VERIFY_FAILED`, `SSLError`, or a
   connection error against a vendor host. When a host rejected every handshake, the
   run prints a line naming the host and a `Next:` step. Follow it.
   `--patch-bundled-cas` fixes bundled CA files. Container runs (`--image`)
   automatically inject the JVM truststore. `--java-truststore` is host-tier only
   and cannot be combined with `--image`. An SDK that pins certificates cannot be patched: stop and
   report it. The full procedure is in
   [../veris-reference/troubleshooting.md](../veris-reference/troubleshooting.md),
   **An SDK refuses the proxy's certificate**.
4. The twin is a data plane with no hostname, such as a database or a self-hosted
   service like Yente. Those are not proxied. The run hands the twin's URL to the app
   under the variable `veris up` printed for it, and says so:
   `veris: yente: not proxied; handed YENTE_API_BASE=…`. The app must read that
   variable, and a `-e` of your own for the same variable wins. Traffic to a data plane
   shows only in the sandbox's count, never in the proxy's, and the verdict says
   `(sandbox ledger; not proxied)`. That is expected.
5. The control plane serves no vendor hostname for an ordinary vendor twin. The run
   then hands that twin's URL to the app the same way, and prints the same `not proxied`
   line as item 4. Here that line is **not** expected. `veris doctor`'s vendor-hostnames
   line names every twin the plane serves no hostname for, and a vendor twin in that
   list is the cause. **Done when** doctor lists only data planes there, postgres and
   yente, or `--route <twin>=<host>` names the hostname for the run.
6. The app talks to the vendor from a process the run did not start (a compose
   sidecar): [../veris-reference/troubleshooting.md](../veris-reference/troubleshooting.md).

Never fix an exit 3 by changing the test's vendor call or its base URL.

## 7. Write down what you measured

Create `.veris/NOTES.md` and commit it. `build` and `fix` read it first, so anything a
later task would otherwise work out again goes here. Fill it from what you did: the
manual, the auth mode, and the proving run. The manual is
`veris sandbox services manual <twin> --raw`; `--raw` puts the markdown on stdout, and
without it the manual renders on stderr. The auth mode is
`veris sandbox data get <twin> auth`.

Use the headings below. Write *measured* or *not measured* under each one; an empty
heading is itself a finding. **Identity and matching** and **Errors and the dedup key**
are the exception. One happy-path run collapses nothing, and no manual describes record
identity, so *not measured* is the expected entry for both at setup. `build` or `fix`
fills them in on first use, with the reads in
[../veris-reference/twin.md](../veris-reference/twin.md).

- **How to run.** Save the chosen path's working preparation/start/reconnect steps,
  required services, source/build command and application test command, including how
  to select an affected test. Record how to check expiry and refresh the current
  sandbox binding, URLs or credentials when needed; setup's old ids are observations.
  Record how that execution's receipt or trace is collected, including before/after
  reads where the selected path needs them. Name the lifecycle owner and its cleanup
  or change-handoff steps. Link that path's reference for interpreting receipts,
  exit codes or connection failures.
  For container execution, save the full verified `veris run` line with its receipt
  file, mounts and variables. Use real paths. For an external mount, say what is in
  it and how to create it. Prove dependency-cache preparation from an empty directory
  using the same cache mount; an offline build cannot populate an empty cache. Record
  the image and build command, and how the app gets credentials without saving secrets.
  For direct execution, save the variable initialization and application command,
  plus the per-service watermark and after-run trace reads in
  [direct.md](../veris-reference/direct.md#what-the-direct-tier-is-not).
  For hosted execution, save the provider's preparation/run/teardown commands and
  evidence procedure from [hosted.md](../veris-reference/hosted.md#what-goes-in-the-files).
  For a plugin-managed session, save the application command, provider tools and
  evidence/handoff procedure from [session.md](../veris-reference/session.md).
  Keep the existing evidence that established this recipe; recording it needs no
  additional application run.
- **What the twin cannot represent.** Hostnames without a twin, data-plane twins,
  anything the smoke could not exercise.
- **Identity and matching.** Which fields the vendor treats as the same record, and
  any normalizing, truncating or joining it does on the way.
- **Errors and the dedup key.** Which failures bind to an idempotency key and replay
  on reuse, and which leave the key free. A fix that retries is built on this answer.
- **Credentials and versions.** The key shape each twin accepts, the API version
  pinned, and anything a made-up value gets away with.
- **Where the repo's own tests do not reach the vendor.** Suites that mock in-process
  pass green with an empty receipt. In most repositories the vendor-facing tests cannot
  produce a receipt at all, so naming the one test that can is worth more than a
  paragraph about the ones that cannot.
- **Anything the twin got wrong.**

## 8. Files, only if the app works with them

Skip this step unless the app uploads or reads files: Drive, Dropbox, attachments.
State that is only rows is cheap to seed per task and does not need a baseline.

The app may work with files and still have nothing to seed — no fixtures, or no
credential the file-capable twin accepts. Write that under **What the twin cannot
represent** and move on: a half-seeded baseline is worse than none.

Otherwise seed the files once, so that every later sandbox starts with them. The steps
are in [../veris-reference/state.md](../veris-reference/state.md), **Files**. Read the
files back and check each row's SHA-256 against the local file. Ask the engineer, then
run `veris baseline promote`. It captures this folder's sandbox, pins it as the
environment's baseline, and deletes the source sandbox afterwards. `--keep-source`
keeps that sandbox instead, frozen and scrubbed. Promote is the last thing you do with
that sandbox. Done when `veris baseline get` shows the pin. Every later `veris up`
starts from that state, and this is the only place setup promotes. Write what is in the
sandbox into `.veris/NOTES.md`: owners, paths, hashes.

## 9. Save build facts and artifact preferences

Keep `.veris/setup.json` in sync with the repository's build definition. Reuse valid
existing facts; update them when the build or working command changes:

```json
{"source_roots": ["api/app"], "build_command": "make build", "build_outputs": ["dist"]}
```

`source_roots` is where production source lives. `build_command` and `build_outputs`
are the repository's own build command and the directories that build writes. Without
them a later task cannot tell a fresh build from a stale one, and it says so rather
than pretend. If the application is baked into a test image, `build_command` builds
that image and `build_outputs` is `[]`; put the image tag in `.veris/NOTES.md`.
If a stock toolchain image compiles mounted source, record that compilation command
with its source and cache mounts, and the output directories it writes back to the
repository (for example, Maven's `target`). Use the exact command you proved.
An interpreted language often writes no build directory at all, and
`[]` is the honest answer there. Do not name a build that has nothing to do with the
code under test.

Preserve an existing `artifact_policy` and the engineer's ignore/retention choices.
If no preference is recorded, use `pr-body`; do not ask again on each task:

- `pr-body`: a concise verification summary and selected redacted evidence in the
  change description. Saved task artifacts stay local.
- `local`: artifacts stay on disk. A remote session needs an explicit export to
  keep them after its sandbox expires.
- `commit`: include the selected redacted task artifacts/evidence in Git.

For a new setup using `pr-body` or `local`, append the following missing ignore
entries. For an existing setup, preserve deliberate choices. Never ignore `.veris/`
as a whole: that would hide `twin.yaml` and `NOTES.md` too.

```gitignore
.veris/bin/
.veris/tasks/
.veris/evidence/
```

For `commit`, leave `.veris/bin/` ignored and make the selected task/evidence paths
trackable. Do not commit task artifacts merely because they are unignored.

### Optional audit helpers

Skip staging unless the engineer requested an audit or the investigation needs the
[record/ledger helpers](../veris-reference/proof.md#optional-audit-helpers).
Copy the needed `record.sh`/`ledger.sh` from this installation's
`veris-reference/scripts/` into `.veris/bin/`. Derive the path from this skill;
in OpenCode, read the installed script with `verisSkill` and verify its SHA-256 after
staging. Use the provider's remote write tool or
[remote bash fallback](../veris-reference/session.md#stage-through-remote-bash),
not host `apply_patch`. Verify or refresh a staged helper before using it after an
upgrade; ordinary setup/build/fix does not depend on having a copy.

## 10. Finish

For CLI-owned setup, run the installed plugin's `veris-reference/scripts/check-setup.py` with Python 3,
using its absolute path and `--project` pointing to this repository. It checks the
handoff files and build metadata without executing anything
from the project. Repair any reported omissions. If Python 3 is unavailable, check
the same files and metadata from steps 7 and 9 manually; do not install a runtime
just for this check. This is a structural check, not a substitute for step 6's
application verification. An earlier successful execution of the exact saved
**How to run** command satisfies it. Reuse the flow configuration read-back from
`veris env get <flow> --json` too. Rerun only if the saved recipe changes or a required
setup condition remains untested; for example, a warm-cache run does not establish a
claimed cold-cache recipe. State any untested recipe or missing read-back precisely.
Plugin sessions use the equivalent session metadata and handoff in
[session.md](../veris-reference/session.md#persist-setup-observations); they do not
need a CLI configuration file or local checker run.

Review **How to run** as a fresh session: include commands to
recreate temporary credential files and external caches, with no credential values
or undefined shell variables. `RUN.md` and `COVERAGE.md`, when requested, accompany
the handoff; they do not replace `.veris/NOTES.md` or `.veris/setup.json`.

Save redacted evidence before cleanup, including after a failed proving run.
`veris down --yes` deletes this folder's sandbox. After a promote in step 8 there is
none left to delete. On the hosted tier, delete the hosted box first using the
provider's teardown command ([../veris-reference/hosted.md](../veris-reference/hosted.md#cleanup)).
Tell the engineer what to commit: `.veris/twin.yaml`, `.veris/NOTES.md`,
`.veris/setup.json`, and `Dockerfile.veris` if you wrote one. Report the receipt line
from step 6; in the direct and hosted tiers, report the trace entry that stood in
for it. `build` or `fix` takes the task from here. Ask before sending repository code
anywhere new.
