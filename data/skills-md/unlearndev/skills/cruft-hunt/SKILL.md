---
name: cruft-hunt
description: Hunt a codebase for what coding agents leave behind (abandoned approaches, duplicate helpers, one-use abstractions, unused packages, just-in-case code and litter) and return a short, ranked, evidence-backed list of deletion candidates. Runs the stack's dead-code tool first, then investigates what tools can't see. Read-only. Use when the user asks to "hunt for cruft", find dead or unused code, find what could be deleted, or clean up after agents.
argument-hint: "[path or area]"
disable-model-invocation: true
allowed-tools: "Bash(git log:*), Bash(git show:*), Bash(git status:*), Bash(git ls-files:*), Bash(git grep:*), Bash(git rev-parse:*), Bash(npx -y knip:*), Bash(npx knip:*), Bash(vendor/bin/composer-unused:*), Bash(composer unused:*), Bash(vendor/bin/phpstan analyse:*), Bash(uvx vulture:*), Bash(uvx deptry:*), Bash(vulture:*), Bash(deptry:*), Bash(go run golang.org/x/tools/cmd/deadcode@latest:*), Bash(cargo machete:*), Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(grep:*), Bash(wc:*), Read, Grep, Glob"
---

# Cruft hunt

## Arguments

Raw arguments: $ARGUMENTS

If arguments are provided, treat them as the **area to hunt in** (a path like `server/` or a feature like "billing"). Otherwise hunt the whole repository.

## Goal

Produce a **short, ranked list of deletion candidates** with evidence for each, grouped by the kind of leftover. The user will pick a few and prove them with `/is-it-dead` before deleting anything.

**This skill is read-only.** Never delete, edit, install, uninstall or commit anything. Never call anything "safe to delete": these are candidates, not verdicts.

The six leftovers:

- **Ghosts**: abandoned approaches. The first attempt, left behind when the agent switched to a second one.
- **Twins**: duplicate helpers. The agent wrote a new one instead of finding the existing one.
- **Scaffolding**: abstractions with one use. Interfaces with one implementation, factories that build one thing, base classes with one subclass.
- **Baggage**: packages nobody needs. Never imported, only used by other cruft, or a whole library for something the platform already does.
- **Just-in-case**: options nobody passes, guards for states the types rule out, compatibility shims for data that's already been migrated, fallbacks nobody hits.
- **Litter**: commented-out code, debug logging, agent-written summary files, TODOs for finished work, tests for code nothing calls.

## Instructions

### 1. Get your bearings

Read `README*`, `AGENTS.md` / `CLAUDE.md` and the dependency manifests. Note anything that changes what "unused" means here: folders loaded by scanning (jobs, plugins, migrations), file-based routing, generated code, public files served as-is, a library's exported API.

### 2. Run the stack's dead-code tool

Run the deterministic tool for each stack you find, **without adding it to the project**. Tools can't hallucinate, so start with them. Run each in the background if your agent supports it, and work on step 3 while it runs.

- **JS/TS** (`package.json`): `npx -y knip --no-progress`, then `npx -y knip --production --no-progress`. Production mode ignores tests, so it catches code that only its own tests use. If the repo has a knip config it's picked up automatically.
- **PHP** (`composer.json`): `vendor/bin/composer-unused` or `composer unused` if installed. `vendor/bin/phpstan analyse` only if shipmonk/dead-code-detector is already configured.
- **Python**: `uvx vulture . --min-confidence 80` and `uvx deptry .`
- **Go**: `go run golang.org/x/tools/cmd/deadcode@latest ./...`
- **Rust**: `cargo machete` if installed.

If a tool isn't available or fails, say so in one line at the end and carry on. Treat tool output as **candidates, not verdicts**: tools miss anything reached another way, and they can't see ghosts or scaffolding.

### 3. Hunt what the tools can't see

Look for each leftover with these signals:

- **Ghosts**: names like `old`, `legacy`, `v1`/`v2`, `new`, `temp`, `backup`, `deprecated`. Two implementations of one job where only one is wired up. Commit messages that say "switch to", "replace", "move X to", "instead of": check the old version was actually removed (`git log --oneline`, `git show --stat <hash>`).
- **Twins**: helpers with the same job in different places (`formatDate`, `slugify`, `isValidEmail`, `debounce`, `formatMoney`, API clients). Compare the bodies. **Note any behaviour difference** (time zone, rounding, accents, null handling, error handling): that makes a merge riskier, and the difference may be a bug.
- **Scaffolding**: an interface or abstract class with one implementation, a factory with one product, a base class with one subclass, a registry or config with one entry, a generic wrapper used once.
- **Baggage**: packages the tool reports as unused, packages imported only by other candidates, and packages used once for something the platform does (`moment` to format one date, a micro-package like `is-number`, a whole UI kit for one component).
- **Just-in-case**: parameters and options no caller passes (check every call site), defaults never overridden, guards for impossible states, shims for an old data format (check git history: did the migration run?), fallbacks for config that's always set.
- **Litter**: commented-out blocks of code, debug logging (`console.log('DEBUG`, `dd(`, `var_dump(`, `print(`), files like `IMPLEMENTATION_SUMMARY.md`, `*_NOTES.md`, `CHANGES.md` that an agent wrote and nothing links to, stale TODOs, tests whose subject is itself a candidate.

**A test is not a caller.** Something only its own tests use is still a candidate.

Skip generated code (lockfiles, build output, generated routes or types), migrations, vendored code and anything in `.gitignore`.

### 4. Sniff every candidate for other ways in

This isn't a full proof (that's `/is-it-dead`), just a quick check so nothing risky looks easy. For each candidate ask:

- **Every other way in?** Is it reached by a string, a folder scan or glob, config, a `package.json`/`composer.json` script, CI, or a framework convention?
- **Anyone outside?** Is it a route, webhook, public file, email link, or exported API that something outside the repo could call?
- **Data from production?** If the repo holds runtime evidence (logs, analytics or flag exports, an `ops/` or `logs/` folder), does it show this running? Does the code run on a cycle longer than that evidence covers?

If any answer is "maybe", move the candidate to **⚠️ Check first** and say which question it raised.

### 5. Rank

Within each section, order by **payoff** (how much it removes from what people and agents read and copy, supply-chain surface for packages, confusion it causes) against **risk** (ways in, behaviour differences, public surface). High payoff and low risk first.

### 6. Output the report

Use this format exactly:

```
### Ghosts
- `src/billing/invoicePdfV1.ts` + its test. First PDF approach, replaced by `renderInvoice.ts` in 4c2e9a1. Only its own test imports it. Payoff high · risk low

### Twins
- `formatPrice` (src/utils/money.ts:3) and `toCurrency` (src/components/CartRow.tsx:8). Same job, but one rounds half-up and one rounds half-even. Payoff medium · risk medium

### Baggage
- `moment`. One import (src/pages/Bookings.tsx:2) to format a date that `Intl.DateTimeFormat` already handles. Payoff medium · risk low

### Litter
- `console.log('DEBUG cart', …)` at src/api/cart.ts:41. Payoff low · risk low

### ⚠️ Check first
- `public/widget.js`. knip: unused file. Nothing in the app loads it, but it's served publicly. Anyone outside?
- `src/cron/expire-holds.ts`. knip: unused file. `src/cron/index.ts` loads this folder by scanning it. Another way in.

**Start with:** invoicePdfV1.ts, moment, the price twins.

9 candidates, 2 to check first.
```

Section order is fixed: Ghosts, Twins, Scaffolding, Baggage, Just-in-case, Litter, ⚠️ Check first. Omit empty sections.

**Start with** names the three best candidates to prove next: high payoff, low risk, ideally of different kinds.

If a tool couldn't run, add one line before the summary: `Not run: knip (no network).`

If you find nothing, output exactly:

```
✅ No cruft found. Nothing worth proving dead.
```

## Rules

- **Read-only.** Never delete, edit, install, uninstall or commit.
- **Candidates, not verdicts.** Never write "safe to delete", "dead" or "unused" as a conclusion. Say what the evidence shows.
- **Evidence on every line.** Tool output, a `file:line`, a search result or a commit hash. No evidence, no candidate.
- **A test is not a caller.** Neither is another candidate.
- **One line per candidate.** Path or name first, then what it is, the evidence, then `Payoff · risk`.
- **Anything with a plausible other way in goes under ⚠️ Check first**, with the question it raised.
- **Fifteen candidates at most.** If you find more, keep the highest payoff ones and end the summary with `+N more`.
- **No preamble.** Start with the first section heading.
- **No closing advice** beyond the "Start with" line and the summary.
