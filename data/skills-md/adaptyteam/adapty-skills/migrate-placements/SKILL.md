---
name: migrate-placements
description: Use when someone wants to move an app from paywall placements to Flow Builder flows — "migrate my placements to flows", "switch my paywalls to flows", "we have 40 placements on paywalls and want flows", or a bulk request across many apps or paywalls. Creates NEW flow placements alongside the existing paywall ones and hands back the old→new mapping plus the SDK call change. Never converts a placement in place — the backend refuses a type change. Complements `flow-generator` (which builds and publishes flows) and `adapty-integration` (which owns the app-side call sites).
---

# migrate-placements

## What this does, and what it cannot do

Two facts decide the whole shape of this skill, and both are measured
([api-surface.md](references/api-surface.md#why-every-migration-is-a-create)):

**A placement's content type cannot be changed after creation.** `placements update` with a flow
audience on a paywall placement is refused — `Placement type can not be changed.` — on an
environment that has the audience union deployed, so this is the backend's rule and not a missing
CLI feature. **There is no conversion.** Every migration is a `placements create`, and the
existing paywall placement stays exactly as it is.

**A placement ID is permanent.** The docs, verbatim: *"Placement IDs are unique across every
placement in the app, whatever the type, so the same ID can't serve a flow in one place and a
paywall in another."* ([placements.md](https://adapty.io/docs/placements.md)) Placement delete is
out of scope, so a new placement cannot reuse the old ID and **a wrongly-created placement stays in
the app forever**. Every ID is shown in full and approved before anything is created.

**So the deliverable is placements plus a code-change handoff, and it does not complete in the
dashboard.** This skill produces new flow placements and a table of
`old paywall placement ID → new flow placement ID`. **Nothing reaches users until the app ships the
call change** — which is also the safety property worth saying out loud: the old placements keep
serving until then, so shipping nothing is the rollback.

**And some of the work may already be done, so look before you build.** A user part-way through
migrating already has flows for some of their paywalls, and a run that does not look creates a
second, emptier one — permanently, since there is no `flows delete`. Phase 2 reads them; phase 4
decides what to do with each.

Boundaries. This skill does not design or build flow content — that is `flow-generator`, which owns
`flows config update`, the preview loop and publish. It does not convert a paywall into a flow —
that is the dashboard button above, the user's click, with no CLI equivalent; this skill's job is
to find the flow it produced and put a placement on it. It does not implement the app-side call
sites — that is `adapty-integration`. It does not delete or modify any existing placement, paywall
or flow.

## Phase 1 — Resolve and probe

This migration needs `flows publish`. Resolve `$ADAPTY` once, the way the sibling skills do —
**install `latest` once and keep using it**, falling back to `npx` only when the global prefix is
not writable — then check that the command is there:

```bash
npm i -g adapty@latest >/dev/null 2>&1 \
  && ADAPTY="adapty" \
  || ADAPTY="npx --yes adapty@latest"
$ADAPTY --version
$ADAPTY auth whoami
```

**Do not gate this on a version number you read somewhere — check the command.** `$ADAPTY flows
publish --help` either describes a command or it does not, and that is the only test that cannot go
stale; a numeric floor has already been wrong here once, because `flows publish` shipped in
`0.8.3-beta.0` and `0.8.3-beta.1`, was **absent from `0.8.3`**, and came back after it. If the
command is missing after installing `latest`, try `npx --yes adapty@beta` once, and if it is missing
there too the route is not released yet: say so and hand the user the dashboard steps
([Migrate to flows](https://adapty.io/docs/migrate-to-flows.md)) rather than a version to chase.

**Install once; do not wrap every call in `npx`.** The wrapper costs ~1 s *per call* against 0.07 s
installed, and this skill makes one call per placement. On the `npx` fallback `--yes` is
load-bearing: without it npx stops to ask permission to install, and a headless run has nobody to
answer. In `zsh` (the macOS default) a multi-word `$ADAPTY` is not word-split, so run
`setopt shwordsplit` once in the same shell; `command not found: npx --yes adapty@latest` is that
shell problem, never a missing CLI. If
`auth whoami` fails, `$ADAPTY auth login` opens a browser — that is the user's to complete. Then
`$ADAPTY apps list --json` for the app UUID.

**Then probe the capability, before spending 152 reads on an inventory you cannot act on.** The
read-only discriminator is `content_type`: an environment with the audience union deployed returns it
on every audience, and one without it omits the field entirely. So the probe needs a placement that
**has** an audience — an arbitrary one proves nothing, because an empty `audiences` array yields
"absent" for a reason with nothing to do with deployment:

```bash
$ADAPTY placements list --app "$APP" --page-size 20 --json    # summaries only — no audiences here
$ADAPTY placements get --app "$APP" <ID> --json               # repeat until one has a non-empty audiences[]
```

Stop `get`-ing after a handful; the point is one witness, not a survey. **Three outcomes, and the
third is not the second:**

- **`content_type` present** ⇒ the union is deployed. Proceed.
- **`content_type` absent on an audience that exists** ⇒ confirmed absent. Stop. Say that a write
  would come back `audiences.0.paywall_id: Field required` and that the migration is a dashboard
  action on this deployment: https://app.adapty.io/placements. **Two things gate it and neither is
  the account** — the **CLI version** above, and the **API deployment**, so this is every account on
  that deployment alike and switching accounts does not help. **This branch is no longer the
  expected one:** production models the audience union, so reaching here means the server you are
  talking to is behind, not that the capability does not exist.
- **No placement carries an audience at all** — a new app, or every one empty ⇒ **could not
  determine.** Do *not* stop: phase 2 is read-only and always safe to run. Run it, say the
  capability is unconfirmed, and let the first write be where it is settled. (If the app has **no
  placements**, there is nothing to migrate — end there for that reason, not this one.)

That signal is a correlation, not a proof, so the same finding can arrive late — and **the late
stops protect placements, not flows.** If `flows publish` returns `http_404` in phase 5 — its route
is unverified, so run it rather than assuming either way —
`flows create` has already run once per distinct paywall, and there is **no `flows delete`**: those
flow rows survive and have to be removed from the dashboard. A phase-7
`audiences.0.paywall_id: Field required` lands later still, with those flows created *and*
published. What both stops do preserve is the thing that cannot be undone at all: **no placement has
been created**, and the paywall placements are untouched.

## Phase 2 — Inventory

Read-only and exhaustive. `references/migrate.py` owns the pagination loop, because `--page-size`
defaults to **20** and the response's `meta.pagination {count, page, pages}` is the only thing that
says so:

```bash
python3 <skill>/references/migrate.py inventory --app "$APP" --adapty "$ADAPTY" \
  --scope active --out inventory.json          # or --scope all; see below
```

> **Never read page 1 alone.** `--page-size` defaults to 20, so one call plus a count of its rows
> silently under-reports a 150-placement app by 130, and the output looks exactly like a small app.

**How to read `migrate.py`'s exit codes**, here and in every later phase: **2** means it did not
work and the cause was not positively identified as internal — the message says what it knows, so
read it and check your input; **3** means an invariant inside the script broke and your input is
almost certainly fine, so stop and report it rather than editing files. A vague message on a 2 is
the script declining to guess, not a bug.

`placements list` returns `{developer_id, id, title}` with **no audiences** — only `placements get`
returns them, so classifying N placements costs N GETs and there is no bulk read
([api-surface.md](references/api-surface.md#summary-vs-detail)).

**The same command also reads `flows list` and `paywalls list`** — the flows the account already
has, and the paywall **titles** to match them against, since an audience carries `paywall_id` and
no name ([api-surface.md](references/api-surface.md#finding-a-flow-the-user-already-has)). Two
paged reads whatever the account size, against the N GETs already being spent. `--no-existing`
skips them; reach for it only when they fail, and then say the question went unanswered rather
than reporting a zero.

**Pass `--scope active`, and read what comes back rather than predicting it.** `is_active` is
present in production, on `placements list` as well as `placements get`
([api-surface.md](references/api-surface.md#is_active--the-scope-filter)), so the filter genuinely
filters and this is the ordinary line:

```
30 placement(s) read -> inventory.json
scope=active: 30 kept, 120 filtered out (30 active, 118 inactive, 2 unknown) -- 2 placement(s)
carry no readable is_active and were withheld as unknown, not as inactive; offer --scope all
```

**A deployment that is behind still falls back, and the fallback is a result rather than a fault:**

```
150 placement(s) read -> inventory.json
scope=active: 150 kept, 0 filtered out (0 active, 0 inactive, 150 unknown) -- fell back to all:
no placement carries is_active, so activity is unknown rather than inactive; --scope active was
ignored and every placement kept
```

**An absent `is_active` is not `false`.** On that line, say the account cannot be filtered and use
the scale gate below — it is then the only thing there is to scope on. Do not report an empty
migration; the tool will not hand you one, and neither should you. **Never report either line
without having run the command**: this skill once told agents up front that the field was absent
everywhere and the fallback was what they would see, which is exactly the shape of caveat that
becomes an excuse not to look.

**Report both halves of that line to the user.** A filter that hides work is worse than no filter:
if `is_active` turns out narrower than the placement status it is documented to be, the withheld
rows are placements that needed migrating and nobody would see them. `migrate.py` produces the
withheld count from the same code that withholds, and `plan` repeats it in `summary.scope`, so
there is nothing to remember — just do not drop it from your message.

**The mixed case has its own flag, so it is not something to spot.** Rows carrying no readable
`is_active` are withheld under `active` — they are not known-active — but they are counted apart
from the inactive ones, because *"you disabled these"* and *"I could not tell"* are different things
to tell a user. When any exist, the scope block sets **`unknown_withheld: true`** with a reason;
that flag is what triggers phase 4's offer to widen.

**Why the filter is an argument to `inventory` rather than something applied to its output.**
the API source declares `is_active` on the summary that `list` returns, which costs 2 calls, while
audiences come only from `get`, which costs one per placement — so filtering the `list` result is what turns `2 + 150` into
`2 + 30`. Filtering after the GET loop produces a byte-identical file and saves nothing.

**The scale gate.** Redundant once the field is present; the only option while it is absent, which
is today. Note it scopes the **placement-first** enumeration — do not reach for
`paywalls placements` as a cheaper narrow path, because it is filtered to live, paywall-typed rows
and so **cannot see an inactive placement at all**
([api-surface.md](references/api-surface.md#summary-vs-detail)). Read `meta.pagination.count` first. Past **25** placements, state the cost — one `get` per
placement — and offer to scope before spending it: a `developer_id` substring, or an explicit list
of placements. "All of them" is then an informed choice rather than an accidental sweep.

> **Widening is a full re-read, not a top-up.** There is no resume and no merge, and `--out`
> overwrites — so `--scope all` after a narrow pass costs the whole `2 + N` again, on top of what
> the first pass already spent. Narrow-first is therefore a **bet that the suggestion is right**: it
> wins outright when the user accepts active-only, and costs one extra `list` plus the active GETs
> when they do not. Take the bet — the reads are cheap and idempotent, and the count that actually
> matters is the *flows* a wider scope adds, one per extra distinct paywall, each of which someone
> has to fill in by hand. Do not tell the user widening is free.

## Phase 3 — Classify and group

```bash
python3 <skill>/references/migrate.py plan --inventory inventory.json
```

Per audience: `paywall_id` → migratable; `flow_id` → already done; neither → skip. Migratable
audiences group by `paywall_id`, and that grouping **is** the flow plan: **one reusable flow per
distinct paywall**, shared by every placement and audience that uses it, so the user later refines
one flow instead of many.

**Report the counts and the grouping, never one row per placement** — migratable placements,
migratable audiences, distinct paywalls, already-flow, no-audience. A 150-row dump is not a report.
Name the distinct paywall count as the number of flows the next phase creates.

**When `summary.unwritable_multi_segment` is not zero, report it here and treat those placements as
blocked.** An audience carrying more than one `segment_id` is **readable and unwritable** — the API
caps it at one per entry on write while its read path deliberately bypasses that cap so legacy rows
survive a round-trip ([api-surface.md](references/api-surface.md#what-the-write-requires-and-why-we-carry-values-verbatim)).
`plan` emits no `command` for such a placement and says why. **Do not offer to split or drop a
segment**: that changes who sees what, which is the user's decision. Say it must be resolved in the
dashboard first, and that the rest of the migration can proceed without it.

**And disclose what the counts are counts OF, once:** `placements get` returns only paywall and
flow audiences and **silently omits any other kind** — an A/B-test audience, for instance — so a
placement may hold more audiences than the read shows. **This is not detectable from the API**:
nothing in the response says an entry was skipped, so there is no check to run and none is
attempted. It matters because the new flow placement will not carry an audience the read never
revealed. Say the counts are of what the API returned, and that a placement known to run an A/B
test should be checked in the dashboard.

**And report `summary.scope` in the same line, when it is there** — how many placements the
inventory withheld and why. The counts above describe what you read; that block is the only thing
that describes what you did not.

`summary.exposure` is the third block and it is **not** a duplicate of either: the activity split
over the placements this plan would create. Do not print it here — phase 6 is where it is used, and
that is the one place its number means anything.

**`summary.existing` is the fourth, and this one you do report, because it changes what phase 4
asks.** Every `flows_needed` row carries the paywall's `paywall_title` and, where a flow in the
account has a matching name, `existing_flow_candidates` — each with its `status` and a `next_step`
of `attach` (it is already `published`) or `publish_then_attach` (a converted flow is left
`draft`). Say how many of the distinct paywalls already have a candidate, and name them.

**Every candidate is a PROPOSAL and the user confirms each one.** The match is on the name alone —
nothing in the API records which paywall a flow came from — so a match may be a coincidence, and
**no match is not evidence that nothing was converted**, because a renamed flow leaves nothing to
match on. Ask, with the flow list to hand — https://app.adapty.io/flows.

## Phase 4 — Two questions

Ask both in one message, then stop. The second is per paywall, so put it as **one table with a
recommended route per row** — not one message per paywall, and not one route for the account.

**1. Scope.** A real three-way choice when `is_active` is present, not "enumerate everything and
deselect":

| Option | Filter | When it is right |
|---|---|---|
| **Active only** | `is_active: true` | the default suggestion — migrate what is actually serving |
| **All** | no filter | move the whole account, disabled placements included |
| **A named list** | user-supplied ids | a staged migration, or one app area |

**Suggest active only, and say why:** a disabled placement serves nobody, so a flow for it is work
whose result no user sees — and each extra distinct paywall in scope is another flow somebody fills
in by hand. **Say what widening costs, and do not call it free:** a re-run with `--scope all` is a
full re-read of the account, because there is no resume and `--out` overwrites.

**If the scope block has `unknown_withheld: true`, put the widen option to the user explicitly**,
with the unknown count. Those rows were withheld because their status could not be read, not because
anyone disabled them, and that is the one exclusion the user is most likely to want reversed.

**Phase 2 already applied `--scope active` before this question was asked, and that is deliberate
rather than a decision taken on the user's behalf.** The choice cannot be put usefully before the
read — until `list` comes back nobody knows whether the field even exists, or that 118 of 150
placements are disabled. So the first pass is narrow, its withheld counts are on screen, and this
question is where the user widens it. Nothing has been written and nothing has been hidden; what a
widen costs is a second read, which is stated above rather than hidden.

**When the field is absent — today, on every account — say the account cannot be filtered** and ask
the original question instead: all of them, with the count shown, or a named subset. That is the
phase-2 scale gate being answered, not a second ask about the same thing.

**2. Where the flow content comes from**, per distinct paywall — and **ask it per paywall, not
once for the account**, because phase 3 has just told you that some of them already have a flow and
some do not. Four routes, in the order to offer them:

- **Reuse** — a flow already in the account, from `existing_flow_candidates` or named by the user.
  **Offer this first wherever a candidate exists**, because it is the only route that costs nothing
  and the flow it reuses is the user's own work. Confirm the flow with them, re-read `flows get`,
  and act on its status: `published` attaches as-is; anything else is published first (phase 5's
  publish half, without its `flows create` half).
- **Convert** — the dashboard's **Move to new builder** on the paywall's own overview page, which
  recreates it as a draft flow in one click: layout, copy in **every** locale, and products with
  prices as variables ([docs](https://adapty.io/docs/convert-paywall-to-flow.md)). **This is the
  right default for a paywall built in the legacy Paywall Builder** — Adapty's own guidance is to
  convert rather than rebuild — and it is the user's click, not yours: there is no CLI command for
  it. Point them at it, wait, then re-run `inventory` and take the Reuse route on what appears. The
  builder opens an **Import review** panel listing whatever did not carry over, and working through
  that panel is theirs too.
- **Build** — hand the paywall to `flow-generator`, which reads it and designs the flow. The route
  for a paywall the conversion cannot serve, or a screen the user wants redesigned rather than
  reproduced.
- **Stub** — one minimal publishable flow from `references/stub-flow.json`. **The last resort, not
  the fast path.** It shows users a placeholder, which is why it carries a disclosure they must
  accept in phase 6; offer it only once the three above are ruled out, or for a placement nobody
  is served from.

**Whether Convert is even available is not readable from the CLI.** `paywalls list`/`get` return
`{id, title, product_ids}` and nothing about which builder made the paywall, and **Move to new
builder** appears only on legacy Paywall Builder paywalls. So do not tell a user the button is
there — say what it does and where to look for it, and let them report back.

Never pick for them. The four differ in what users will see, which is not the agent's call. **What
you may not do is create a flow for a paywall that already has one** without the user having
declined to reuse it: that is a duplicate the account keeps, since there is no `flows delete`.

### A rehearsal order, when `is_active` is present

Not a phase — a recommendation to offer once, on a large or first-time migration: **do the inactive
placements first.** The whole `create → publish → attach` chain then runs end to end with **no live
exposure**, and what it leaves behind is a real account state rather than a simulation — the one
call the skill depends on, `placements create` with a published flow, is
[unverified](references/api-surface.md#what-is-still-unverified), so the first real run of it is
better spent where a mistake costs nobody a purchase. Then repeat for the active ones with the
mechanics already known-good.

The cost is honest and worth saying: it is two passes, and every placement it creates is permanent
either way. Offer it; do not impose it. With the field absent there is nothing to order on, so skip
this entirely rather than guessing which placements are quiet.

> **The premise is that `is_active: false` means nobody is being served, and the field means
> exactly one thing:** the [activation state the API source documents](references/api-surface.md#is_active--the-scope-filter)
> — Live versus Inactive, the dashboard's own toggle, nothing finer. What that does *not* tell you
> is whether a shipped app still calls the placement. An inactive placement serves no paywall, so a
> stub on it shows nobody a placeholder; but if the user says a placement is live traffic,
> **believe them over the flag** and treat it as active.

## Phase 5 — Realize the flows

**A paywall the user chose to Reuse skips most of this phase.** There is nothing to create and
nothing to write: re-read `flows get`, and if the status is `published` record it in the ledger and
move on; if it is not, run the publish and the poll below and nothing else. `flows create` and
`config update` are for a paywall that has no flow yet — running them over a reused flow is how you
get the duplicate this whole route exists to avoid, and there is no `flows delete` to undo it. A
paywall waiting on the user's **Move to new builder** click is not ready for this phase at all:
leave it out of the ledger, and pick it up on the next `inventory`.

Per distinct paywall that needs a new flow, in this order. The ordering is forced by measurement: a
placement naming a draft flow is refused — `Cannot attach a draft flow to a placement — publish it first.`, exit 2, or
on an older CLI the backend's own `Flow must be published before placing in a placement.` — and
publication is **asynchronous**.

```bash
$ADAPTY flows create --app "$APP" --name "<paywall title> (flow)" --json      # row only; draft
$ADAPTY flows config validate <FLOW> --app "$APP" \
  --config-file <skill>/references/stub-flow.json --json                      # expect valid: true
$ADAPTY flows config update <FLOW> --app "$APP" \
  --config-file <skill>/references/stub-flow.json --json                      # or flow-generator's config
$ADAPTY flows publish --app "$APP" <FLOW> --yes
$ADAPTY flows get <FLOW> --app "$APP" --json                                  # poll until published
```

**Validate runs on the local file before the write, never after it.** That is `flow-generator`'s
ordering and it is load-bearing for the same reason here: validate reads a **config file** and needs
only the flow to *exist*, so running it after `config update` checks bytes that are already saved.
`create` still comes first, because validate resolves a flow id.

`flows publish` reports `status: publishing`, **never** `published` — so **poll `flows get` until
the status reads `published`** and do not report the flow as live off the publish response. The
command prints that poll itself, and prints the diagnosis call beside it; on
`publication_failed`, `flows config get` carries `publication_status`, `transform_error` and
`publication_error`, and `transform_error` is the transform service's objection in its own words —
quote it, do not invent a cause. `--yes` is passed here only because the user is choosing flow
content in phase 4 and the placements are still gated in phase 6; without it a non-TTY run refuses
with exit 2 rather than hanging. `flow-generator` owns the publish contract, the 400 path and the
failure diagnosis — delegate to it rather than re-deriving them.

**A `http_404` from `flows publish` stops the run here, and it is not a clean stop.** The route is
not deployed to production, so every account gets it; but `flows create` has already run for this
paywall and there is no `flows delete`, so **say how many flow rows exist and that they have to be
removed from the dashboard** — https://app.adapty.io/flows. Do not keep creating flows for the
remaining paywalls once publish has 404'd.

`references/stub-flow.json` is shipped rather than authored per run because it carries evidence a
runtime pass cannot inherit: **`valid: true` from the real transform service and a clean
`verify-config.py`**. Below that floor the failure message is the location-free `Generated JSON
failed schema validation`, which names no field
([api-surface.md](references/api-surface.md#the-publishable-floor)). One screen, one `text`. Do not
hand-write a smaller one.

### The flow ledger — `flows.json`

**One file, written as you go, and it is the only ledger phase 5 has.** A JSON object mapping
`paywall_id` → `flow_id`, rewritten in full **after each flow reaches `published`** — not once at
the end:

```json
{
  "9f3c1a20-...": "6b41e0d7-...",
  "c07e4b19-...": "a2d55f81-..."
}
```

**Incremental is the whole point.** `flows create` does **not** deduplicate and there is no
`flows delete`, so a run that dies between flow 3 and flow 4 must leave 3 recorded — otherwise a
re-run creates a second flow per paywall and every duplicate is a permanent row somebody removes by
hand. Write it after the `flows get` that confirmed `published`, so a line in the file means a flow
that can actually be attached.

**A reused or converted flow is an entry like any other.** The ledger records what phase 7 will
attach, not what this phase created, so a flow the user already had goes in the same file once
`flows get` reads `published` — and phase 7 then cannot tell the difference, which is the point.

**On re-entry, read it first.** For each `paywall_id` already present, confirm with
`flows get <FLOW> --app "$APP"` that the recorded flow still reads `published`, then skip that
paywall. A recorded id whose status is *not* `published` is not a skip — finish publishing it, do
not create a second flow.

Keep `flows.json` beside `inventory.json` in the working directory and name the path when you print
progress. Phase 7 reads it; nothing else does.

## Phase 6 — The approval gate

Print this block, filled in, and wait for an explicit yes. `--yes` goes on nothing until it lands.
Echo the resolved values — never a prose reminder that IDs are permanent. **The yes authorises
`placements create` and nothing else:** phase 5 has already run, so the block says what still has
not happened rather than claiming nothing has.

> **No placements exist yet — that is what this yes authorises.**
>
> **App:** `<app title>` (`<app id>`)
> **Placements to create:** `<n>` — the irreversible step
> **Flows:** `<flow line — pick by path, below>`
>
> | Existing paywall placement | New flow placement | Flow |
> |---|---|---|
> | `<developer_id>` | `<proposed developer_id>` | `<flow name>` |
>
> **Permanent:** a placement cannot be deleted. If one of these IDs is wrong,
> it stays in the app forever — read the middle column before saying yes.
>
> **Your paywall placements are not touched.** They keep serving until your app
> ships the change below, which is also how you roll back: ship nothing.
>
> `<undo line — stub and build paths only, below>`
>
> **This does not reach users yet.** Your app must call
> `getFlow("<new developer_id>")` where it currently calls the old placement.

**Those two slots turn on one fact: did *this run* create the flows?** Stub and build did;
**existing** did not — the user handed over flows that were already published, so this run created
nothing, and "on your account now, removable only in the dashboard" would be a false claim about
what the run did.

- **Stub or build.** Flow line, and the undo line verbatim:

  > **Flows already created and published:** `<n>`, one per distinct paywall — on your
  > account now, and removable only in the dashboard

  > **Saying no does not undo the flows.** Those `<n>` rows stay either way; no CLI
  > command deletes a flow.

- **Existing.** Flow line, and the undo slot is **omitted entirely** — saying no leaves the account
  exactly as this run found it, and there is nothing to warn about:

  > `<n>` you supplied, verified `published` — this run created none

Everything else in the block is unconditional: the permanence line, the untouched-placements line
and the call-change line hold on all three paths.

Proposed IDs come from `migrate.py`'s `propose_developer_id` — `<original-id>-flow`, pre-checked
against every `developer_id` in the inventory, because a collision is permanent. Show the full list;
never abbreviate it to a count.

**If the flow content is a stub, print this too and get a separate yes.** A stub-backed placement is
not a smaller version of the migration — it is a different outcome for users.

**When `is_active` is known, name the exposure as a count rather than asking for a blind
acknowledgment** — a mechanical guard over a caveat, which is what this repo prefers. An inactive
placement carries no such cost at all.

> **Read the count from `summary.exposure`, never from `summary.scope`.** They are different
> numbers and only one of them is the exposure. `scope` partitions the whole account as `list`
> returned it; `exposure` partitions **the placements this plan would actually create**, which
> excludes every already-flow and every empty placement. Measured on a 3-row account:
> `scope.active` is `3` and `exposure.active` is `1`. Quoting `scope` here **overstates the live
> exposure**, which is precisely the harm this block exists to prevent.

**There are two forms of this block and you print exactly one.** `exposure.status_readable`
decides which, and nothing else does:

| `exposure.status_readable` | Print | Slots |
|---|---|---|
| `true` | **the COUNT form** (immediately below) | `<n>` = `exposure.placements`, `<a>` = `exposure.active` |
| `false` — today, every account | **the NO-COUNT form** (the second block, after this one) | none; it is verbatim |

**The COUNT form:**

> **A stub is a one-line placeholder screen** — once your app points at it, it
> *is* the content: users see the placeholder and cannot purchase.
>
> **`<a>` of the `<n>` placements you are migrating are active.** Attaching a
> stub to those stops purchases there the moment your app ships the call
> change, until you fill the flow in. The other `<n-a>` are inactive and serve
> nobody, so a stub on them costs nothing.
>
> Say yes only if you will fill the flows in before shipping the call change.
> Otherwise say no — the flows are already published, so I stop here and create
> no placement. Fill them in, **publish again**, then say yes whenever you are
> ready — a placement can only be attached to a flow that reads `published`.

**The NO-COUNT form.** When `exposure.status_readable` is false — today, on every account — the
count cannot be stated and the acknowledgment is all there is. Use this wording verbatim, and do
not substitute a guess for the number:

> **A stub is a one-line placeholder screen.** Once your app points at it, it
> *is* the content — users see the placeholder and cannot purchase. Fine for a
> placement nothing calls yet; a revenue stop for one you are about to ship.
> Say yes only if you will fill the flow in before shipping the call change.
> Otherwise say no — the flows are already published, so I stop here and create
> no placement. Fill them in, **publish again**, then say yes whenever you are
> ready — a placement can only be attached to a flow that reads `published`.

**The re-publish is not a nicety, and the escape hatch is untrue without it.** Filling the stub in
is a config write, and a write to a published flow marks it **`dirty`** — whether a `dirty` flow can
be attached is explicitly unverified
([api-surface.md](references/api-surface.md#what-is-still-unverified)), so `published` is the only
status treated as attachable. An offer that stops at "fill them in and say yes" therefore leads
straight back to `Cannot attach a draft flow to a placement`, the one error the phase ordering
exists to avoid. On the return trip, re-read `flows get` and check the status the way phase
5 does rather than assuming the edit left it alone.

## Phase 7 — Create

**Do not type a `placements create` by hand. Re-run `plan` with the ledger and run what it emits.**

```bash
python3 <skill>/references/migrate.py plan --inventory inventory.json --flows flows.json > plan.json
```

With `--flows`, every placement row gains a **`command`** — the exact argv, built by
`build_create_command` from audiences built by `to_flow_audience`. Print them one per line and run
them, unchanged:

```bash
python3 - plan.json <<'PY'
import json, shlex, sys
for row in json.load(open(sys.argv[1]))['placements']:
    cmd = row.get('command')
    print(shlex.join(cmd) if cmd else '# NO COMMAND: ' + row['command_unavailable'])
PY
# then, one at a time, prefixed with $ADAPTY:
$ADAPTY placements create --app ... --title ... --developer-id ... --audiences '[...]'
```

**Generating the argv is what makes the guards unavoidable rather than merely available**, and this
is the one irreversible command in the skill, so it is the last place to trust retyping:

- **Every audience on a new placement is `flow`.** Mixed paywall+flow audiences are a backend 400,
  and `build_create_command` **raises** rather than emitting one — including on an all-paywall
  array, the same invariant from the other side. Hand-written argv gets no such refusal.
- **`content_type` is required on every entry** and the CLI exits **2** with no request sent if it
  is missing. A read from a pre-union environment omits it; `normalize_audience` injects it on this
  path, every time.
- **`segment_ids` and `priority` are carried over verbatim** by `to_flow_audience` — they are the
  targeting, and changing them silently changes who sees what. Retyping them is exactly how a digit
  goes missing.
- **A row whose paywall is not in `flows.json` carries no `command`**, only `missing_flows` and a
  reason. Do not fill the gap in by hand: finish phase 5 for that paywall and re-run `plan`.
- **A row with `multi_segment_audiences` carries no `command` either, and this one you cannot
  resolve by re-running.** Its audience holds more than one `segment_id`, which the API returns on
  read and refuses on write. Report it, name the placement, and leave it to the user — writing it
  anyway fails, and editing the segments changes their targeting.
- **There is no prompt and no preview on `placements create`** — unlike `flows publish`. Whatever
  argv you send is sent. Phase 6 is the only gate there is
  ([api-surface.md](references/api-surface.md#confirmation-asymmetry)).

### The placement ledger — `placements.json`

**The second and last ledger, and it has the same discipline as `flows.json`:** a JSON object
mapping the new `developer_id` → the created placement's `id`, rewritten after **each** successful
create.

```json
{ "main-flow": "1f8e...", "onboarding-flow": "77b2..." }
```

**Only successes go in it.** A key means that placement exists and must never be created again — a
second create under a proposed ID that is already taken is either refused or, worse, a second
permanent row. So on re-entry, read `placements.json` and skip every approved entry whose
`developer_id` is already a key. **Failures are deliberately not recorded**: a failed entry has to
be retried, and a ledger that skipped it would strand it silently.

**One failure does not abort the run** — record it in your own working notes, continue to the next
entry, and report every failure with its reason in phase 8.

**One error is the exception to that: `audiences.0.paywall_id: Field required` aborts everything.**
It is not this entry's problem — it is the phase-1 probe's answer arriving late, so every remaining
entry will fail identically. Stop, and report the position honestly: no placement was created, and
the flows from phase 5 exist, are published, and cannot be deleted from the CLI.

## Phase 8 — Report and handoff

Created, skipped and failed with reasons, then the two things the user acts on:

> | Old paywall placement | New flow placement |
> |---|---|
> | `<old developer_id>` | `<new developer_id>` |

And the call change: the app fetches the new placement with `getFlow("<new developer_id>")` where it
currently fetches the old one. **Flows render on Adapty SDK v4.0 or later**, so on an older SDK the
call change is a version upgrade first; `getFlow` reads flow *and* paywall placements, so the app
calls one method either way ([Migrate to flows](https://adapty.io/docs/migrate-to-flows.md)). Hand
the implementation to `adapty-integration`, which owns the per-platform call sites and the render —
do not write app code here.

**Say that the old placement stays live, and why.** Users on already-shipped versions have the old
placement ID compiled in and cannot reach the flow until they update, so retiring the paywall
placement early takes the paywall away from everyone who has not updated. Both placements run side
by side, each measured on its own metrics, until v4 adoption is high enough.

**No rollback file is needed, and say why rather than leaving it unsaid:** nothing existing was
modified, so **the untouched paywall placements are the rollback.** Until the app ships the call
change, users are on the old paywalls; if the new flows are wrong, ship nothing and fix the flows in
the builder — https://adapty.io/docs/adapty-flow-builder.md.

**Rollback covers placements, not flows** — say so rather than letting "nothing was modified" carry
more weight than it earns. Every flow the run created is a new row that **cannot be deleted from the
CLI**, so a run that stopped early leaves them behind: name the count and where to remove them,
https://app.adapty.io/flows.

Close by naming what is still outstanding, once: flows still holding a stub, placements that failed,
flow rows to clean up, and the fact that nobody sees any of this until the app ships.

## What you print

The user reads your messages, not this file. Keep them short.

**Two fixed blocks, and nothing else is fixed:** the approval gate and — when the content is a
stub — the stub acknowledgment, both in phase 6. Fill their slots and do not pad them. The old→new
table in phase 8 is the same data as the gate's middle column, so print the table and do not
re-narrate it.

**Everything else is one line or omitted.** The phase-3 counts are one line. The phase-4 questions
are one message, asked once. Per-flow progress in phase 5 is a count, not a running commentary. A
capability stop is one line plus the dashboard link. **Say each thing once**: if the gate already
named the permanence, phase 8 does not repeat it.
