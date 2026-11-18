---
name: traj
description: "Operate `traj`, the Trajectonomics ledger and projection CLI, on someone's own money: record what they earned and spent, read balances and reports, and answer what-if and financial-independence questions. Use when the user talks about their accounts, spending, budget, net worth, savings plan, Thai tax, or planning a purchase."
---

# traj

`traj` is a deterministic ledger and projection CLI. It computes exactly and **never calls an LLM**, so every number you give the user is one `traj` produced. You supply the judgement; `traj` supplies the arithmetic.

Its command surface changes as features land, so this document deliberately carries none. Read the tool.

## Run the CLI

Run `traj --version`. A version that prints is a `traj` you can trust and reuse for the whole session: the release tag, the npm package and the binary's stdout are one version by construction.

If that fails, run the scoped npm package, which needs only Node 20 or later, or Bun:

```
npx -y @trajectonomics/cli@latest <args>
bunx @trajectonomics/cli@latest <args>
```

Either way, get the version once and pin it: the number from `traj --version`, or from `npx -y @trajectonomics/cli@latest --version` when you are on the fallback. Put that number into the npm spec as `@<version>` and use it for every later call, so one session cannot end up running two releases. The first npm run downloads about 100 MB of binary and narrates that download on stderr; a line about downloading is not an error.

The npm package is `@trajectonomics/cli`; the unscoped package of the same short name belongs to someone else.

`npx -y` runs code neither of you reviewed, so say why it is the safe choice here: the launcher verifies the published SHA-256 of the release binary. Nothing about it sends the user's data anywhere — and you send nothing either, never uploading or pasting their ledger, documents or exports.

When the user wants `traj` kept on `PATH`, give them the one-line install command for their platform from the CLI's README and let them run it. Handing them a remote script to pipe into a shell is their decision, not yours.

## Where the data lives

All state is one directory, `~/.traj` on every platform, holding `traj.db` and a cache of downloaded binaries. `TRAJ_HOME` overrides it, which is how you isolate a scratch run. On a machine that has never run it, run `traj init` first and pass `--json` like every other call.

## Read the tool before you act

1. `traj schema --json` lists every command with a one-line summary, plus the error registry: each `code` with its `exitCode` class and message.
2. `traj schema <command> --json` gives that command's flags, its input and output JSON Schema, the document schema it accepts when it has one, and the error codes it can raise. Do this before the first use of a command, every session.
3. `traj help <command>` adds worked examples.

Take every flag, required field, document shape and enum value from that output, not from memory and not from this document.

## The contract

- Pass `--json` on every call, or set `TRAJ_FORMAT=json`. The format is never inferred from a terminal, so tell the CLI and its pipe and terminal cannot disagree by accident.
- Commands never prompt. Nothing will come back asking a question.
- A JSON error is an envelope on stderr: `{"error":{"code","exitCode","message","path?","hint?","details?"}}`. Read `exitCode` for the class, `code` for which failure, `hint` for what to try next.
- Exit classes: `0` ok, `1` unexpected, `2` invalid input you must fix, `3` the domain refused it, `4` not found, `5` conflict such as a name already taken. A launcher failure, before the binary starts, is plain text rather than an envelope: read it, tell the user what it said, and stop retrying.
- Money is a decimal string on the wire (`"120.50"`) with a currency, standing for an integer of minor units: keep both ends integer, and keep the unit the user's. Restating one amount in a different unit is a second number you invented.
- Dates are `YYYY-MM-DD` Gregorian, in English. A Buddhist Era year is the same day under a different year number: convert it, and ask the user when the source does not say which calendar it is.

## Keep every fact explicit

`traj` has no clock and no opinions, so everything it should know, you state:

- Every date, including every as-of date, is an argument you supply. "Today" is a date you were given or one you ask for; it is never read off the machine.
- Every account is a name, exact and case-sensitive. Read the chart of accounts before you write to one; an account the user has not created is a question, not a guess.
- Every amount, date and account comes from what the user told you. When a fact is missing, or two readings of what they said both fit, ask.

Every figure you report is one `traj` returned: to check one, run the read again. The tool owns balances, projections, FI dates and tax; you own asking the user for the facts that feed them. That split is the whole reason the tool exists.

Two write behaviours to use on purpose:

- **Dry run first**, wherever `traj schema` lists a dry-run flag on the command. It runs the real write and rolls it back, reporting `dryRun: true` and generated ids as `null`, so the rows it returns are the rows the real write would create. Show the user those rows, then write.
- **Set an external reference on every write**, wherever `traj schema` lists one. Replaying the same reference reports a duplicate at exit `0` instead of writing twice, which is what makes a retried write safe.

A flag that carries a document takes a path or `-`. `-` is the only way to send a document on stdin; it is never inferred from a pipe.

## Scenarios

A Scenario document's shape belongs to `sim-core`, not to the CLI. Read the validator name and pinned version that `traj schema scenario apply` prints, then that version's public documentation in `trajectonomics/sim-core` alongside the `check()` errors a dry run returns, and iterate the document against those errors. Never invent a field or carry a shape from memory. Its amounts are integers of minor units like every other amount in `traj`, and `check()` accepts a document whose amounts are a hundred times too small, so the unit is yours to get right. A Scenario's accounts declare the Ledger's own account ids — read them from the chart of accounts or the Baseline, never a name you made up — or the projection refuses the Baseline as undeclared. A fork whose `contentHash` equals its parent's holds no change: if you cannot express the user's what-if in the document, say so and do not present that fork as the what-if. An Override path is dotted object keys, with list items addressed by their stable `id`.

## Plans and what-ifs

A projection starts at an as-of date and ends at a horizon, and both are the user's to give. Ask for them when they are missing; never take either from the clock. The plan is the Scenario, so a what-if is an Override or a second Scenario, and the difference the tool reports is the answer — never a figure you worked out yourself.

Report the financial-independence date together with the horizon and the assumptions it was computed under, because it is a property of that plan and that window, not of the person. The 25× figure that sits beside it is a labelled rule-of-thumb reference and is not the date. When a projection reports contributions it could not fund, or a date the plan runs out of money, say so plainly: the figures it gives are then not the plan the user described, and a what-if built on it is not the what-if either.

## What this version covers

Phase 1 is record, project and answer. V1 is THB and Thailand; the United States follows later, and multi-currency does not.

`traj schema` is the honest answer to "what can it do": read it before you promise anything. When a capability is absent from it — a second jurisdiction, an allowance optimiser, or projections and financial independence in an older release — say that this version of `traj` cannot answer it, offer the record-and-report part you can do, and leave the missing number missing rather than approximating it.

Every result you give the user states the as-of date it was read at, and whether tax is in it. A figure without those two is one they will misread.

## Tax

Tax belongs to the Scenario, not to a projection call: `traj scenario tax <name> --tax th-2026` writes Thailand's 2026 personal income tax into it, and every projection of that Scenario then reports `tax: applied`. A Scenario without it is projected pre-tax and every result says `not_applied`.

The Levy tallies labels and never guesses them, so an income Flow with no label tax-core recognises is income it charges nothing for. `traj scenario tax` refuses that by name, and `--label <flow>=<label>` is how you classify it: `income.section40_1` for employment, `income.section40_2` for service and hire of work, and the rest of Section 40 from `traj schema scenario tax`. Ask the user which class their income is; never pick one to make the command pass. Retirement contributions take their own labels (`allowance.retirement.rmf` and friends) and raise the allowance they feed.

Read the taxpayer's facts from the user: filing status, children, and how many of those children were born in 2018 or later. `--none` removes the Levy and its labels, so a Scenario can go back to pre-tax. Re-applying a Scenario's document replaces it, Levy included: after `scenario apply`, run `scenario tax` again.

You never estimate tax yourself, and you never apply it silently. When a result says `not_applied`, say the figures are before tax and offer to apply it; when it says `applied`, report that with the figures, because the tax is already in them.
