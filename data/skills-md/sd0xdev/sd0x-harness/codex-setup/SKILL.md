---
name: codex-setup
description: "Initialize sd0x-dev-flow infrastructure for Codex CLI and other non-Claude agents. Generates AGENTS.md, installs the commit-msg hook, copies runner scripts. The pre-push gate is opt-in via --with-push-gate. Use when setting up a new project or after updating skills."
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(node:*), Bash(git:*), Bash(ls:*), Bash(mkdir:*), Bash(cp:*), Bash(chmod:*), Bash(bash:*), Bash(cat:*), Bash(wc:*)
---

# Codex Setup

## Trigger

- Keywords: codex setup, codex init, agents.md, setup codex, initialize codex, codex doctor, codex sync
- After: `npx skills add sd0xdev/sd0x-harness`

## Subcommands

| Command | Purpose |
|---------|---------|
| `init` | First-time setup: generate AGENTS.md + install the `commit-msg` hook + copy scripts |
| `doctor` | Verify installation integrity: files exist, AGENTS.md hash matches, and each recorded hook is **active** — hook *bytes* are `sync`'s axis, not this one (§ doctor) |
| `sync` | Re-generate AGENTS.md + update installed hooks/scripts after skill update |

Default (no subcommand): `init`

## Arguments

| Flag | Applies to | Effect |
|------|-----------|--------|
| `--with-push-gate` | `init`, `sync` | Install `pre-push-gate.sh` as the `pre-push` hook. **Off by default** |

The `pre-push` gate is the one hook that **waits for a human** — it reads `/dev/tty`,
so from a non-interactive context it stalls or fails on a terminal that is not there.
That is why it is opt-in, and why every path below reads that choice from state rather
than re-deciding it. `commit-msg` stays a default install because it never prompts:
it guards the attribution anchor (CLAUDE.md rule 3) by reading the message and
deciding, with no `/dev/tty` and no input. **It does still reject** — exit 1 on a
policy violation, exit 3 when the policy cannot be evaluated — and it rejects
interactive and non-interactive commits alike (`scripts/commit-msg-guard.sh`). The
distinction that makes it safe to install by default is *prompts vs. rejects*, not
*blocks vs. does not block*.

**The flag is the opt-in interface — there is no prompt.** `init` must not ask
interactively whether to install the gate: this skill runs under Codex sandboxes and
in non-interactive setup flows where an unanswered prompt would either hang or be
silently defaulted, and a silent default is exactly what opt-in exists to prevent.

## init

### Phase 1: Detect Host Context

1. Find repo root: `git rev-parse --show-toplevel`
2. Read `package.json` if present → extract `name`, `scripts.test`
3. Read `.claude/CLAUDE.md` or `CLAUDE.md` → extract test command pattern
4. Detect plugin root: find `scripts/build-codex-artifacts.js` relative to this skill

### Phase 2: Generate AGENTS.md Kernel

```bash
node <plugin-root>/scripts/build-codex-artifacts.js \
  --project-dir <repo-root> \
  --output <repo-root>/AGENTS.md
```

If the file already exists, warn and ask before overwriting.

Verify output:
- File exists and is non-empty
- Size ≤ 24 KiB (`wc -c < AGENTS.md` ≤ 24576)
- No unresolved placeholders (`{PROJECT_NAME}`, `{VERSION}`, `{TEST_COMMAND}`)

### Phase 3: Multi-Mode Hook Install

Install the git hooks using priority-ordered detection. The mode detection is
identical for both hooks; only *which* hooks are installed differs:

| Priority | Condition | Action |
|----------|-----------|--------|
| 1 | `.husky/` directory exists | Copy the hook's script to `.claude/scripts/`, **then prepend** that hook's executing stanza below to `.husky/<hook>` — `commit-msg-guard.sh` into `.husky/commit-msg`, and (only under `--with-push-gate`) `pre-push-gate.sh` into `.husky/pre-push`. **Two stanzas, not one**: they are shaped by what git hands each hook, and § The Husky commit-msg stanza says where they differ |
| 2 | `git config core.hooksPath` is set | Install to that path |
| 3 | `.git/hooks/` is writable | Direct write |
| 4 | Fallback | Write to `.githooks/` + print `git config core.hooksPath .githooks` — **the write alone does not arm the hook**; see below |

#### Modes 2–4 write the hook **as** the file, so check who owns it first

Mode 1 prepends into a shared container; modes 2–4 put the gate — or the guard — at the resolved
hook path **as that file's whole content**. A write there is a delete of whatever was there, and
the operator's own `pre-push` may be the only thing standing between them and something this
skill knows nothing about. `--with-push-gate` is a request to *add* a guard; taking one away to
honour it is not a lesser reading of that request, it is the opposite of it.

So before any dedicated-file mode writes a hook, classify the destination — **by content, never by
existence**:

| Destination | Action |
|-------------|--------|
| Absent, or present and empty | Write. Nothing is lost |
| **sd0x-owned** — one of the first 20 lines is exactly `# <script> - ` followed by that script's own summary, where `<script>` is `pre-push-gate.sh` or `commit-msg-guard.sh` per hook | Overwrite. This is a refresh of our own file, which is what `sync` exists to do |
| Anything else | **Do not write.** Record `pending`, and report: `<hook>: <resolved> already exists and is not sd0x-owned — the gate was not installed; move or rename that hook, then re-run` |

The marker is the shipped scripts' own second line, so an older shipped version is still recognised
as ours and a refresh across versions is not blocked. It is matched as a prefix of a line rather
than against the whole file because the byte-for-byte alternative refuses every past version — the
one case a refresh most needs to succeed on.

**The predicate is deliberately strict in one direction.** A hand-edited header stops matching and
the install refuses; a foreign file matches only if someone copied our header into it. Refusing an
install costs a re-run, and the operator is told which file to move; clobbering costs a hook nobody
can get back. The asymmetry decides, exactly as it does for `uninstall` below — that row already
said "only after verifying it is sd0x-owned", and this is the same predicate, stated once, on the
side where the file is still there to protect.

**`pending` is the honest record for a refused write**: the operator opted in, the wiring did not
finish, and the transition matrix already treats `pending` as a gate to keep — so a later
`sync` retries rather than reading the refusal as a decline. Recording `declined` would turn
their request into an opt-out they never made.

#### The Husky stanza — prepended, executed, and it hands stdin back

Mode 1 does not write its own file: it goes into `.husky/<hook>`, beside whatever the project
already put there. Two properties of that neighbourhood decide the shape of the stanza, and both
were got wrong by the words this section used to carry ("append sourcing"):

| Property | Consequence | Measured 2026-08-21 |
|----------|-------------|---------------------|
| git delivers the ref list on **stdin, once** | An earlier consumer in the same hook takes it, and the gate then reads EOF — zero refs, nothing protected, nothing rewritten, **exit 0** | An existing `while read …` loop ahead of the gate turned a protected-branch rewrite that the gate refuses with exit 1 into an allowed push |
| `.`/`source` does not change `$0` | The gate's privileged re-exec, which then read `exec … bash -p "$0" "$@"`, named **the Husky hook** rather than the gate | The parent hook's first line printed twice — once at `$-`=`hB`, once at `hpB` — i.e. the user's whole `pre-push` re-ran under a privileged shell, and the gate never ran as the gate. The gate has since switched that word to `${BASH_SOURCE[0]:-$0}`, which resolves correctly under `source`, and an ordinary `source` of the gate now refuses (2026-08-22) — so no *supported* caller reaches this defect. Not "closed entirely": the refusal compares against `$0`, which a sourcing caller supplies, and a forged one walks past it (`4-implementation.md` § 4.3, Round 54). Row 1 above was already reason enough on its own |

So: **prepend**, and **execute**. Prepending alone would fix the first and break the project's own
hook, which then reads the EOF instead — the same fail-open one file over. The stanza therefore
captures the stream once and hands it back:

```sh
# >>> sd0x-dev-flow pre-push gate >>>
# No bare command word may decide anything or carry a refusal. This hook runs with the pusher's
# whole environment, and an exported BASH_FUNC_name%% answers `git`, `cat`, `bash`, `mktemp`,
# `[`, `test`, `exec` and `exit` alike. Three things are immune, and every construct here that
# runs BEFORE the verdict, or that enforces it, is built out of only those three:
# `case` (a reserved word, resolved by the grammar), `${x:?}` (fails during expansion, before
# command lookup), and an ABSOLUTE path — bash refuses to import a function whose name contains
# a slash. Everything else that runs before the verdict is inside `bash -p`, which imports no
# functions at all. The two bare words that DO appear — `exec 0<` and `rm -f` — sit after
# `__sd0x_rc` already holds the verdict, and what a shadowed one costs is stated under
# "Two residuals" below rather than wished away by an absolute claim here.
__sd0x_refs=$(/usr/bin/env -u SHELLOPTS -u BASHOPTS -u BASH_ENV -u ENV -u SD0X_PRIV_REEXEC \
  /bin/bash -p -c 'umask 077; f=$(mktemp) || exit 1; cat >"$f" || exit 1; printf %s "$f"')
case "$__sd0x_refs" in
  /*) ;;
  *) __sd0x_abort=''
     : "${__sd0x_abort:?sd0x pre-push gate: could not capture the ref stream}" ;;
esac
/usr/bin/env -u SHELLOPTS -u BASHOPTS -u BASH_ENV -u ENV -u SD0X_PRIV_REEXEC \
  /bin/bash -p -c 'test -r "$1" || exit 0; g=$1; r=$2; shift 2; exec "$BASH" -p -- "$g" "$@" <"$r"' \
  sd0x-pre-push ./.claude/scripts/pre-push-gate.sh "$__sd0x_refs" "$@"
__sd0x_rc=$?
exec 0< "$__sd0x_refs"        # hand git's one-shot stream back to the rest of the hook
rm -f "$__sd0x_refs"          # unlinked, still open on fd 0
case "$__sd0x_rc" in
  0) ;;
  *) __sd0x_abort=''
     : "${__sd0x_abort:?sd0x pre-push gate: refused this push}" ;;
esac
# <<< sd0x-dev-flow pre-push gate <<<
```

**Why the shape is this and not the obvious one.** The obvious stanza — `__sd0x_gate="$(git
rev-parse --show-toplevel)/…"`, `[ -r … ]`, `cat`, `bash "$gate"`, `exit "$rc"` — is what this
section shipped for one round, and every command word in it is a hole. Measured 2026-08-21:

| Injected | What the obvious stanza did |
|----------|------------------------------|
| `BASH_FUNC_git%%='() { echo /definitely-missing; }'` | resolved the gate to a path that does not exist, so `[ -r … ]` was false and the hook continued **with no gate and exit 0** |
| `BASH_FUNC_cat%%='() { :; }'` | discarded the ref stream; the gate then read an empty file, found no refs, and exited 0 |
| `BASH_FUNC_bash%%='() { return 0; }'` | never launched the gate at all, and reported success |
| `BASH_FUNC_exec%%` / `BASH_FUNC_exit%%` | `exec` and `exit` are builtins, so both are shadowable: the refusal path became a no-op |

That is the same class the gate closes for **itself** with its privileged re-exec — the stanza
simply sat in front of it, outside that protection, and handed the attacker every decision the
gate was about to make. The replacement removes the decisions rather than hardening them:

| Construct | Why it cannot be intercepted |
|-----------|------------------------------|
| `/usr/bin/env` written out absolutely | `bash: error importing function definition for '/usr/bin/env'` — the **import** is refused outright, and a bare `env` **is** shadowable (measured both ways). Narrower than it reads: a slash is illegal in an *imported* name, not in a *defined* one, so a definition **sourced** into this shell carries it fine (`function /usr/bin/env { … }` — measured). That leaves `$BASH_ENV`, sourced before the hook's first line, outside what this row covers; see the residual below |
| `./.claude/scripts/pre-push-gate.sh` — relative, no `git rev-parse` | git runs `pre-push` with the working tree root as cwd, measured to hold even when the push was issued from a subdirectory. A path needs no command to produce, so there is nothing to intercept |
| Everything real inside `/bin/bash -p -c` | `-p` imports no `BASH_FUNC_*` and reads no `$BASH_ENV`, so `mktemp`, `cat`, `test` and the gate itself resolve normally |
| `case` for both decisions | A reserved word: the grammar resolves it, never command lookup |
| `: "${x:?…}"` for both refusals | Expansion fails *before* command lookup and kills a non-interactive shell (rc 127, measured with `:` **and** `exit` both shadowed). `exit "$rc"` could be answered; this cannot |
| `exec "$BASH" -p -- "$g"` rather than `exec "$g"` | Does not depend on the gate carrying its executable bit, and does not resolve the gate's `#!/usr/bin/env -S bash -p` shebang through PATH. Supplying `-p` here is what keeps that bypassed shebang from mattering — the two must stay in step, and a `-p` dropped from either line reopens `$BASH_ENV` for this path |
| `-u SD0X_PRIV_REEXEC` | The gate establishes privileged mode through that marker. Leaving an inherited one in place would make the gate skip its own re-exec — a bypass handed over by the caller |

A third residual sits above all of them and is not this stanza's to close: these lines run in the
project's own `.husky/pre-push` shell, whose shebang the project owns. If that shell is bash and the
pusher's `$BASH_ENV` defines `/usr/bin/env`, the first line here is answered before `bash -p` is
ever reached. The gate's own file closed the same hole for itself by putting `-p` in its shebang
(`scripts/pre-push-gate.sh`, 2026-08-22) — the one statement early enough, and the one this stanza
does not get to write.

Two further residuals, both stated rather than hidden, and both pinned by the hostile-environment test in
`test/skills/codex-setup.test.js` rather than left as prose. A shadowed `rm` leaks one 0600 temp
file per push and cannot open a gate. A shadowed `exec` leaves the rest of the project's hook
reading an already-drained stream — measured `TAIL-SAW 0` — because handing stdin back needs a
redirection, redirection needs `exec`, and no POSIX construct reopens fd 0 without it. What that
costs is bounded and is not this gate: ours has already decided and enforced by then, and what
degrades is the project's own hook. A hook that refuses on an empty ref list still refuses; one
that passes on it passes — which is the same exposure it already had before this stanza existed.
`PATH` is outside this boundary for the reason § 4.3 of the implementation doc gives: it cannot be
unset, has no trustworthy substitute, and a hostile one is a strictly larger compromise than
anything the gate protects.

Line by line, each for a reason that has a failure behind it:

| Line | Why not the shorter form |
|------|--------------------------|
| Executing the gate, never `. "$gate"` | The gate **refuses to be sourced** — measured 2026-08-22: `. ./scripts/pre-push-gate.sh` prints `pre-push-gate: must be executed, not sourced` and takes the sourcing shell down with rc 127. So this line is not a preference the stanza expresses. It is not a *defence*, either — the refusal compares `${BASH_SOURCE[0]}` against `$0`, and a sourcing caller chooses `$0`, so a forged one is not stopped (measured; `4-implementation.md` § 4.3, Round 54). What it reliably catches is the accidental `source` in a hand-written wrapper, which is what this row is about. The reasons this row used to give are both retired: the `$0` defect was fixed in the gate (`${BASH_SOURCE[0]:-$0}`), and the `set -euo pipefail` leak is unreachable — the refusal **precedes** the `set`, so sourcing never reaches the options it was said to leak (stated as an order rather than as line numbers, which the header migration had already moved once) |
| `__sd0x_rc=$?` — and `__sd0x_cm_rc=$?` in the commit-msg stanza, the same shape for the same reason — on its own line | Two containers, one refusal. Under `set -e` the hook exits **at** the failing gate carrying the gate's own status, and the `case` below is never reached (the temp file leaks — a refused push, not an allowed one). Without `set -e` the assignment captures the status and the `case` refuses. Writing it as `\|\| __sd0x_rc=$?` would put the gate in a condition context and suppress the first path, leaving only the second |
| `exec 0<` **before** `rm` | Reversed, the rest of the hook gets a closed descriptor. Unlink-after-open is what keeps the bytes reachable with nothing left on disk |
| `test -r "$1" \|\| exit 0` **inside** the privileged child | An uninstalled or half-removed gate must leave the push alone, so the project's hook behaves exactly as it did before. Install-time verification is what keeps that from silently covering a *misinstalled* gate — see the Active predicate below |
| Marker comments on their own lines | They are the detection and uninstall boundary (§ sync, § Uninstall). `doctor`'s "sd0x stanza present" test greps for the opening marker — a **presence** probe, and nothing more. Every decision that can record `installed` reads the **pair**: an opening marker alone is also what a truncated stanza leaves behind, and § sync's marker matrix has a terminal answer for that case which "present" would silently overrule |

**Definition — an `intact sd0x block`**, used by every test in this file that can record
`installed`, so the three of them cannot drift apart. `.husky/<hook>` holds one when **all** of:

| Clause | Why it is not droppable |
|--------|-------------------------|
| Exactly one opening marker and exactly one closing marker | Two of either gives the block two candidate boundaries, and replacing one leaves the other running |
| The opening precedes the closing | Same counts, no block — the markers bound nothing, and "count is right" would certify it |
| The lines **between** them invoke `.claude/scripts/<this hook's script>` — `pre-push-gate.sh` for `pre-push`, `commit-msg-guard.sh` for `commit-msg` | Marker balance is a property of two comment lines. A pair whose body was emptied, commented out, or points at the *other* hook's script is perfectly balanced and runs no gate — and every clause above would still pass it |

The third clause is what "carries the sd0x stanza" always meant; stating it as marker balance alone
was a round-79 narrowing that would have let `doctor` report `installed × Active` over a hook that
executes nothing. Presence and intactness are different questions: `doctor`'s "sd0x stanza present"
probe greps the opening marker and answers the first, which is all a *report* needs.

The stanza is prepended even when the Husky hook is created by this skill — writing it first is what
makes "prepended" a property of the file rather than of the order two installs happened to run in.

#### The Husky commit-msg stanza

`commit-msg` is the hook a flagless `init` installs (§ Modes), so under Husky it needs its own
written-out path — and it is **not** the push-gate stanza with a name changed. What git hands the
two hooks is different, and the whole capture-and-hand-back apparatus above exists for a property
`commit-msg` does not have:

| | `pre-push` | `commit-msg` |
|---|---|---|
| How the input arrives | the ref list on **stdin**, readable once | the message file's **path**, as `$1` |
| So the stanza must | capture the stream, pass the copy, hand fd 0 back | pass `"$@"` through and nothing else |
| Leftover state | a 0600 temp file to unlink | none |

Everything else carries over unchanged, because the threat does: this hook runs with the
committer's whole environment, and an exported `BASH_FUNC_name%%` answers `test`, `bash`, `exec`
and `exit` alike. So the same three immune constructs, for the same reasons the table under the
push-gate stanza gives — `case`, `${x:?}`, and an absolute `/usr/bin/env` — with everything real
inside `/bin/bash -p`.

```sh
# >>> sd0x-dev-flow commit-msg guard >>>
# Executed, never sourced — and the reason is NOT the push-gate stanza's, because the guard behaves
# differently and the difference is what matters. The guard re-execs itself privileged through
# `${BASH_SOURCE[0]:-$0}`, which under `.` resolves to the guard, so the re-exec names the right
# file — and then `exec` REPLACES the sourcing shell with it. Measured 2026-08-22: a parent hook
# that sources this guard runs its own first line, hands the process over, and never reaches a
# single line after the `.` — and this stanza is PREPENDED, so everything the project put in its
# own commit-msg hook is what silently stops running. `-u SD0X_PRIV_REEXEC` for the same reason as
# under the push-gate stanza: the guard
# establishes privileged mode through that marker, so an inherited one would make it skip its own
# re-exec. `ALLOW_AI_COAUTHOR` is deliberately NOT unset — it is the narrow opt-in the attribution
# anchor defines, and the guard, not this stanza, is what decides what it may do.
/usr/bin/env -u SHELLOPTS -u BASHOPTS -u BASH_ENV -u ENV -u SD0X_PRIV_REEXEC \
  /bin/bash -p -c 'test -r "$1" || exit 0; g=$1; shift; exec "$BASH" -p -- "$g" "$@"' \
  sd0x-commit-msg ./.claude/scripts/commit-msg-guard.sh "$@"
__sd0x_cm_rc=$?
case "$__sd0x_cm_rc" in
  0) ;;
  *) __sd0x_cm_abort=''
     : "${__sd0x_cm_abort:?sd0x commit-msg guard: refused this commit message}" ;;
esac
# <<< sd0x-dev-flow commit-msg guard <<<
```

`test -r "$1" || exit 0` carries the same meaning as in the push stanza and no more: an
uninstalled or half-removed guard leaves the commit alone, so the project's hook behaves as it did
before. It is not a substitute for the Active predicate below — a *misinstalled* guard is what that
check is for.

**Writing a hook file is not installing it. Verify that git will actually run it before recording
`installed`.** Priority 4 only *prints* the `core.hooksPath` command; until someone runs it, git
still looks in `.git/hooks/` and neither the `commit-msg` guard nor an opted-in push gate ever
fires. Recording that as `installed` would make `doctor` green over a repository with no active
guard at all — the exact failure both hooks exist to prevent. So every mode ends with the same
check, and it is a check on **git's own answer**, not on the file existing:

```bash
# What does git itself resolve this hook to?
resolved=$(git rev-parse --git-path "hooks/${hook}")
```

The comparison depends on the mode, and **`-ef` against `$written_path` is only correct where git
runs the written file directly**. Husky is the case that breaks it: the normal modern shape is
`core.hooksPath=.husky/_`, so git runs `.husky/_/<hook>` — a Husky-owned shim — which *sources*
`.husky/<hook>`, the container the sd0x stanza was written into. Those are two different files, so
an `-ef` test reports a fully active hook chain as inactive.

**The mode numbers below are the priority numbers above — the same four modes, not a second
scheme.** Mode 1 is Husky, so it takes the Husky row and never the direct-file row; an earlier
version of this table grouped "1–3" as direct-file *and* carried a separate `Husky` row, leaving a
literal reader with two rows claiming mode 1.

| Mode | Active ⇔ | Record when active | Record when **not** active, and what to report |
|------|----------|--------------------|-----------------------------------------------|
| 1 (Husky) | `test -x "$resolved"` **and** `$resolved` reaches the sourcing container **and** `test -r "$repo_root/.claude/scripts/$script"` where `$script` is **this hook's** script — `commit-msg-guard.sh` for `commit-msg`, `pre-push-gate.sh` for `pre-push` — i.e. the shim git resolved exists and executes, `$written_path` still holds an **intact sd0x block** (§ The Husky stanza — all three clauses; marker balance alone would pass an emptied block, and the opening marker alone is only a presence probe), and the file that block invokes is actually there | `installed` | **`pending`** + `<hook>: sd0x stanza present in $written_path but git resolves to $resolved, which does not reach it — re-run husky install`; or `<hook>: sd0x stanza present but .claude/scripts/$script is missing — re-run codex-setup sync` (add `--with-push-gate` when `$script` is the gate) |
| 2 (`core.hooksPath` set) | `test "$resolved" -ef "$written_path"` **and** `test -x "$resolved"` **and** `$resolved` is **sd0x-owned** — the § Phase 3 predicate, re-run against the file git resolved | `installed` | **`pending`** + `<hook>: written to $written_path but git resolves to $resolved — check core.hooksPath`; or, when the first two hold and ownership does not, the **terminal** row below |
| 3 (`.git/hooks/` direct) | same three tests | `installed` | **`pending`** + `<hook>: written to $written_path but git resolves to $resolved — the hook is not the one git runs`; ownership failure → the terminal row below |
| 4 (fallback dir) | same three tests; false while `core.hooksPath` is unset | `installed` | **`pending`** + `<hook>: written to .githooks/ but NOT active — run: git config core.hooksPath .githooks`; ownership failure → the terminal row below |
| 2–4, **foreign collision** — the resolved file is the written path, executes, and is **not** sd0x-owned | never active | — | **`pending` (terminal)** + `<hook>: $resolved exists, git runs it, and it is not sd0x-owned — the gate was not installed. Move or rename that hook, then re-run`. **Do not re-copy** (§ Transition matrix) |

**`$script` is per hook, and hard-coding it was a live defect.** This row named
`pre-push-gate.sh` unconditionally, which was survivable only while `pre-push` was the sole hook
with a Husky path. It is not any more (§ The Husky commit-msg stanza), and the hard-code breaks in
both directions on the **default** installation: a flagless `init` installs `commit-msg` and
deliberately leaves the gate absent, so a perfectly working attribution guard records `pending`;
and a repository still carrying an old `pre-push-gate.sh` records `commit-msg` as `installed`
after `commit-msg-guard.sh` has been deleted — `doctor` green over commits that skip the guard
entirely. Each hook's predicate must name its own script.

**Identity is not executability.** `-ef` proves the file git resolved is the file we wrote; it
says nothing about whether git will run it, and `githooks(5)` is explicit that a hook without the
executable bit is ignored. Mode 1 already required `test -x`; modes 2–4 did not, so a `chmod -x`
— or a `sync` overwriting an existing non-executable destination — left `doctor` reporting a pass
over a hook git silently skips. Both halves are now required everywhere.

**And identity is not ownership** (round 60). `-ef` asks whether the file git resolved is the file
at `$written_path`; it does not ask whose file that is — and after a refused write those are the
**same foreign file**. Phase 3 classifies the destination by content, declines to clobber a hook it
does not own, and records `pending`; the activation predicate then re-derived `$resolved`, found it
identical to `$written_path` and executable, and promoted that `pending` straight back to
`installed`. The sequence needs no adversary: opt in on a repository that already has a `pre-push`
hook, `sync`, and `doctor` goes green over a gate that was never installed — the precise inversion
of the refusal that produced it. So **the ownership predicate is part of the activation predicate**,
run against the file git resolved rather than the path we intended to write, and it is the same
predicate stated in Phase 3 rather than a second one that could drift.

That outcome is **terminal `pending`**, and the difference from every other `pending` is what a
later `sync` may do about it. The ordinary ones are wiring failures — the file is ours, the remedy
re-copies it. This one is a file that belongs to somebody else, so re-copying *is* the clobber the
refusal exists to prevent. The remedy is the operator's: move or rename that hook. Until they do,
the honest record is `pending` and the honest `doctor` verdict is Fail — never a re-copy, and never
a promotion to `installed`.

**Every mode's inactive outcome is `pending`, and the remedy is what differs.** The earlier table
left modes 1–3 with `—` in that column, which is not "cannot happen" — mode 2's `core.hooksPath`
can point elsewhere, mode 3's `.git/hooks/<hook>` can be shadowed — it was simply unstated, so an
activation failure there reached a state the schema has no value for. `mode` is recorded beside
`status` precisely so the remedy can be selected later: `doctor` prints **the recorded mode's**
line, never a generic one.

⚠️ **The `.githooks` remedy is mode 4's, and must never be printed for Husky.** `git config
core.hooksPath .githooks` abandons `.husky/_`, which stops **every** Husky hook in the repository —
a wider break than the one being reported. A Husky activation failure is repaired inside Husky.

Source scripts from plugin:

| Source | Hook | Installed |
|--------|------|-----------|
| `commit-msg-guard.sh` | `commit-msg` | Always |
| `pre-push-gate.sh` | `pre-push` | With `--with-push-gate`, **or** where the matrix below says so |

The flag is what makes a *first* install happen. It is **not** the only thing that writes the
hook, and reading it that way is what produced the two defects the matrix below closes: without
the flag this skill must still refresh a gate that is already wired, and restore one that was
recorded as installed and has since gone missing. Neither is a new install — both are keeping an
existing choice true.

So: without the flag and with **no** gate to keep — the recorded status is absent or `unknown`,
and nothing sd0x-owned is on disk — do **not** write a `pre-push` hook and do not leave a partial
or disabled one behind. "No gate to keep" means **no recorded opt-in of any kind**, not merely no
recorded `installed`: `pending` is an opt-in whose wiring never finished, so it is a gate to keep
and takes its own row below. Reading this sentence as "not `installed` ⇒ decline" is what would
write `declined` over an operator's `pending` — the exact overwrite the table exists to refuse.
The table below is the authority for every combination; this paragraph names only the one row that
declines. Record the choice in Phase 5 and report it:

```
pre-push gate: not installed (opt-in). To add it: /codex-setup sync --with-push-gate
```

Print that line whenever the gate is skipped, so an operator who expected the old
unconditional behaviour learns why the hook is absent at the moment it is skipped,
rather than the next time a push is not stopped.

**"Skipped" is not "declined" — resolve from disk before recording either.** A flagless
`init` re-run on a repository that already has the gate wired must not write `declined`
over it. Nothing on disk changed, so recording a decline would state a choice the
operator never made, and the consequences compound rather than surface: `doctor` reports
the `declined` × present row as a disagreement, and a later plain `sync` follows the
recorded decline and stops re-copying an **installed safety hook**. So Phase 5 records:

**Read the recorded status first, then the disk.** Disk alone cannot tell "never chosen" from
"chosen, and the wiring has since gone missing", and those two owe opposite actions. Wiring is
resolved by the same evidence test `sync` uses for `unknown`: Husky stanza present, or a
hook file present **and** verified sd0x-owned.

| Recorded `pre-push.status` | sd0x wiring on disk | Action, then recorded |
|----------------------------|---------------------|-----------------------|
| `installed` | Present | **Re-copy the shipped hook and record the new hash** → `installed` with its mode. Say `pre-push gate: already installed, refreshed` |
| `installed` | **Absent** | **Re-install and record the hash** → `installed`. The recorded status *is* the operator's earlier opt-in; wiring that has since disappeared is damage, not a decision. Same answer `sync`'s `installed` row gives — "never removed; the flag's absence is not a request to uninstall" |
| absent / `unknown` | Present | Re-copy and record the hash → `installed`. Say `pre-push gate: already installed, refreshed` |
| absent / `unknown` | Absent | `declined`, and print the skip line above |
| `pending` | either | **Re-copy, then re-resolve activation** (§ Phase 3 mode table): active → `installed`; still not active → leave `pending` and reprint the recorded mode's remedy. **Classify the destination before re-copying** — the re-copy is a write, so § Phase 3's content classification governs it exactly as it governs the first one; a destination that is not sd0x-owned is the **terminal** `pending`, where the remedy is the operator's move-or-rename and the only thing this step does is reprint it. `pending` records an opt-in that already happened and a wiring step that had not completed — never a decline, so a flagless `init` must not write `declined` over it for the same reason the `installed` rows above must not |
| `declined` | either | Leave `declined` as it stands. A recorded decline is a choice, and a flagless `init` is not a request to revisit it; `doctor` reports the `declined` × present disagreement and names the two reconciliations |

Two things this table refuses to do, both of which the disk-only version did. It never writes
`declined` over a recorded `installed` — that states an opt-out the operator never made and
disarms a gate they had chosen, after which `doctor` reads `declined` × absent as *healthy* and a
plain `sync` skips it forever. And it never merely relabels: classification is not the update, so
every row that concludes `installed` also refreshes the bytes. An upgraded project is exactly
where the wired gate is oldest, and `doctor` checks **activation, not bytes** — stale bytes are
perfectly active, so they pass it. Activation and hashing are different axes (§ doctor); checking
the first is not a reason to skip refreshing the second here.

`--with-push-gate` is unaffected by the table above: whatever the recorded status was, the flag
installs. What it does **not** do is decide the record — the flag says *install it*, and the record
still says *what is actually wired up*, which only the mode table's activation test can answer:
active → `installed`, not active → `pending` with that mode's remedy. Recording `installed` on the
flag's word would put the one status meaning "git will run this hook" on a hook git does not run,
which is the same over-claim the mode table exists to prevent — and it would do it precisely where
the operator asked for the gate, so the wrong record would look like a granted request. This
mirrors `sync`'s `unknown` row rather than inventing a second rule — the question both answer is
the same one, *what is actually wired up*, and only the flag expresses a choice.

### Phase 4: Copy Runner Scripts

Copy these scripts to the host project:

| Source | Target |
|--------|--------|
| `scripts/precommit-runner.js` | `.sd0x/scripts/precommit-runner.js` |
| `scripts/verify-runner.js` | `.sd0x/scripts/verify-runner.js` |
| `scripts/lib/utils.js` | `.sd0x/scripts/lib/utils.js` |
| `scripts/lib/tree-digest.js` | `.sd0x/scripts/lib/tree-digest.js` |
| `scripts/pre-push-gate.sh` (mode 1 only, and only when the gate is being installed) | `.claude/scripts/pre-push-gate.sh` |

Ensure target directories exist (`mkdir -p`).

The `scripts/pre-push-gate.sh` row is conditional because only **mode 1** needs it: modes 2–4 install the gate *as* the
hook file, so the copy is the install. Mode 1's stanza instead runs the gate out of line, at
`.claude/scripts/pre-push-gate.sh` — the path `/install-scripts` also uses. Without this row that
path was named by the stanza and written by nothing, so a fresh `init --with-push-gate` on a Husky
project recorded `installed` while every push evaluated `test -r` as false and sailed through. The
Active predicate above is the other half: the copy can fail, and a recorded `installed` must mean
the gate is reachable, not that a copy was attempted.

### Phase 5: Write State File

Write `.sd0x/install-state.json` to repo root:

```json
{
  "sd0x_version": "<from plugin.json>",
  "agents_md_hash": "<git hash-object AGENTS.md>",
  "agents_md_size": <bytes>,
  "hooks_installed": {
    "commit-msg": { "status": "installed", "hash": "<sha1>", "mode": "<husky|hooksPath|direct|fallback>" },
    "pre-push": { "status": "declined" }
  },
  "scripts_installed": {
    "precommit-runner.js": "<sha1>",
    "verify-runner.js": "<sha1>",
    "lib/utils.js": "<sha1>",
    "lib/tree-digest.js": "<sha1>"
  },
  "generated_at": "<ISO8601>"
}
```

The template above shows the **no-flag run, with the `commit-msg` hook active**. When
`init --with-push-gate` installed the hook in Phase 3, the `pre-push` entry is written like
`commit-msg`: `{ "status": "installed", "hash": "<sha1>", "mode": "<husky|hooksPath|direct|fallback>" }` —
the state file must record what this run actually did, never the template verbatim.

**`commit-msg` is not exempt from the activation test**, and the `installed` in the template is the
active outcome rather than a constant: it is written through the same Phase 3 mode table as
`pre-push`, so a `commit-msg` hook that was written but that git does not resolve to is recorded
`pending` with its mode, exactly like any other. Reading the template as a fixed value is the
specific misreading to avoid — it would hard-code the one status meaning "git will run this hook"
onto a hook git does not run, and `doctor` would report a repository whose attribution guard never
fires as healthy.

**`status` is written explicitly; absence never carries meaning.** Every hook entry
records one of these, and `doctor` and `sync` both branch on it rather than on
whether a hash happens to be present:

| `status` | Meaning | Written when |
|----------|---------|--------------|
| `installed` | The hook is wired up; `hash` and `mode` accompany it | The hook was written this run, or is being carried forward |
| `declined` | Deliberately not installed | `init` ran without `--with-push-gate` **and no sd0x wiring was found on disk** (Phase 3 — a flagless re-run over an installed gate records `installed` instead, and refreshes the hook while doing so); `sync` resolved an `unknown` entry to an absent hook; or the entry was set to `declined` to uninstall (see `sync`) |
| `pending` | The opt-in happened and **no sd0x-owned hook is what git runs** — either git does not resolve to the file we wrote (in **any** mode, not only the fallback), or it resolves to a file that is not ours because Phase 3 refused to clobber it. `mode` accompanies it so the remedy can be selected, and the second case is **terminal**: its remedy is the operator's, not a re-copy | Phase 3's activation check failed. It is neither installed (nothing fires) nor declined (nobody opted out), and collapsing it into either would misreport: `installed` makes `doctor` green over an inert guard, `declined` states a choice the operator never made |

A deliberate opt-out and a broken install are different states, and a missing field
cannot tell them apart — which is why `declined` is recorded rather than inferred
from an absent `pre-push` key.

**Reading a state file written before this contract** (entry present, no `status`):
read it as `installed`. Those files were only ever written after the hook was
installed unconditionally, so `installed` is the true reading, and it is also the
safe one — the opposite reading would make `sync` skip an installed hook and let it
drift. An entirely **absent** `pre-push` key is `unknown`, not `declined`: see
`doctor` and `sync` below, which resolve it rather than guessing.

### Sandbox Adaptation

| Codex sandbox | Behavior |
|---------------|----------|
| `workspace-write` / `danger-full-access` | Execute all phases automatically |
| `read-only` | Output command list for manual execution |

Detect sandbox: if `mkdir -p` or file write fails, switch to read-only output mode.

## doctor

### Checks

| Check | Method | Pass | Fail |
|-------|--------|------|------|
| AGENTS.md exists | `test -f AGENTS.md` | File found | Missing |
| AGENTS.md hash match | Compare `git hash-object` vs state file | Match | Drift detected |
| AGENTS.md size ≤ 24 KiB | `wc -c` | ≤ 24576 | Oversized |
| Hooks installed | Per hook, branch on its `status` (below) | **Active**, or `declined` **and absent** | Missing, or present but not active |
| Scripts installed | Check `.sd0x/scripts/` files exist | Present | Missing |
| Version match | Compare state `sd0x_version` vs current plugin | Match | Update available |
| Instruction files | Walk the working directory and its ancestors for `CLAUDE.md`, `.claude/CLAUDE.md`, `CLAUDE.local.md`, `AGENTS.md` and `.claude/AGENTS.md`; check native AGENTS.md availability, then read the effective `instructionFiles` mode (§ Instruction files and AGENTS.md freshness) | Reported — informational: which files a Claude Code session loads | — |
| AGENTS.md freshness | Regenerate the expected kernel with `build-codex-artifacts.js` into a temporary file and compare its bytes with the installed `AGENTS.md` | Match | ⚠️ Stale — the installed kernel predates this plugin version; run `/codex-setup sync` |

**The hook check reads state first, filesystem second.** A hook whose absence was
chosen is not a broken install, and reporting it as one would make `doctor` red on
a correctly configured project — which teaches operators to ignore the report:

The disk axis below is **sd0x wiring, not the container file**: in Husky mode the
wiring is the sd0x stanza inside `.husky/pre-push` (the file itself may
carry the user's own commands and proves nothing either way); in the
`hooksPath`/`direct`/`fallback` modes it is the sd0x-owned hook file.

**And the axis is `Active`, not `Present`** — the same distinction § Phase 3 draws
above, applied here rather than restated: `doctor` evaluates that mode table's
`Active ⇔` column, re-deriving `resolved=$(git rev-parse --git-path "hooks/<hook>")`
at report time. A presence-only pass certifies a guard that cannot run: an
sd0x-owned `.githooks/pre-push` survives `core.hooksPath` being unset or repointed,
git then resolves `.git/hooks/pre-push`, nothing fires — and the file is still
there for a presence check to find. `doctor` is the one command an operator runs
to ask whether the gate works, so of every check in this skill this is the one that
must not answer from the filesystem alone.

| State `status` | sd0x wiring on disk | Result |
|----------------|---------------------|--------|
| `installed` | **Active** (§ Phase 3 mode table) | ✅ Pass — activation only; no hash |
| `installed` | Present but **not active** | ❌ **Fail — written but not active.** Same condition as the `pending` row below, reached from a different state; report that row's remedy, **for the recorded mode** |
| `installed` | Absent | ❌ Fail — Missing (in Husky mode this includes a surviving `.husky/pre-push` whose sd0x stanza is gone) |
| `declined` | Absent | ✅ Pass — reported as `pre-push: not installed (opt-in)`; a stanza-free `.husky/pre-push` left in place by the mode-aware uninstall is this row, not the one below |
| `declined` | Present | ⚠️ Warn — state and disk disagree; name both and offer the two real reconciliations: `/codex-setup sync --with-push-gate` to adopt the hook and record `installed`, or remove the sd0x wiring per the mode-aware uninstall procedure below to honour the recorded decline (a plain `sync` skips a `declined` entry and repairs nothing — see the `sync` table) |
| `pending` | **Not active** | ❌ **Fail — no sd0x-owned hook is what git runs.** Either git does not resolve to the file we wrote, so nothing of ours fires; or it resolves to a **foreign** hook Phase 3 refused to clobber, in which case something fires and it is not the gate — report *that* row's remedy (move or rename the hook, then re-run) and never a re-copy. Otherwise report the remedy **for the recorded mode** (§ Phase 3 mode table — each mode has its own; `git config core.hooksPath .githooks` is mode 4's and is never printed for mode 1, where it would disable every Husky hook in the repository). Never green: a wiring-presence pass here would certify a guard that cannot run |
| `pending` | **Active** | ⚠️ Warn — the remedy worked and **our** gate fires; the state file is merely stale. `Active` is the § Phase 3 three-test predicate, ownership included, so a foreign hook that runs perfectly well never reaches this row — it is not active *as the gate*, which is the only sense this table has ever measured. Say so and name `/codex-setup sync` to record `installed`. **Not a Fail**: `pending` is a claim about the disk, not a choice, and reporting an active gate as broken teaches the operator to ignore the check |
| absent key (`unknown`) | Either | ⚠️ Warn — pre-dates the opt-in contract; suggest `/codex-setup sync` to record it |

Activation is the whole check for an installed hook: hash comparison applies to
AGENTS.md only (the row above), and this row adds no hook hash verification.
Activation and hashing are different axes — the first asks whether git will run the
file, the second whether the file is the shipped bytes — so checking the first is
not the second creeping in by another name.

**The residual is stated, not hidden.** A hook that is active but carries stale or
locally edited bytes passes `doctor`: it is a working gate, just not certainly the
shipped one. Which is why the § Subcommands row for `doctor` says *active* and not
*hash match* — the one place that advertisement is read by someone deciding which
command to run. The axis that answers bytes is `sync`, and every path in its tables
re-copies them (§ sync, § Phase 5 `pre-push` table), so the remedy for a gate whose
contents are in doubt is `/codex-setup sync --with-push-gate` — not a redder
`doctor`, which would have to re-derive at report time a comparison `sync` performs
by simply overwriting.

### Instruction files and AGENTS.md freshness

Claude Code 2.1.277 and later can read `AGENTS.md` natively, so which instruction files a session
loads is a question `doctor` answers rather than assumes (`docs/features/claude-code-2-1-288-compat/2-tech-spec.md`
§ 3.3). It answers in three steps, and a later step never overrules an earlier one.

**1. Availability.** The mode table applies only where native support is available. Read the version
with `bash -c 'claude --version'` — the CLI on `PATH`, which is not necessarily the running session.
Below 2.1.277 report `unavailable`: AGENTS.md loads under no mode, except through an `@AGENTS.md`
import in a `CLAUDE.md`. An unreadable version reports `unverified`. At or above it, report
`available` and name the conditions `doctor` cannot observe, any of which leaves only CLAUDE.md
loading: the built-in `agents-md` plugin disabled in `/plugin`, the first session after an upgrade
from 2.1.276 or earlier, and — before 2.1.281 — some sessions such as Amazon Bedrock or telemetry
disabled.

**2. Mode.** The host reads `pluginConfigs["agents-md@builtin"].options.instructionFiles` from
**user** settings (`~/.claude/settings.json`), a **`--settings`** file, or **managed** settings,
and ignores it in project and local settings, so `doctor` does too. `doctor` cannot see the flags
a session was launched with, so it never reads a `--settings` file: report the mode with the source
it came from, and say that a `--settings` launch file overrides a user-settings value. When neither
user nor managed settings can be read, report `claude-md-or-agents-md (default assumed)` — never a
guessed mode.

**3. Files.** Where the mode lets AGENTS.md load, every `AGENTS.md` and `.claude/AGENTS.md` in the
working directory and its ancestors is eligible; `AGENTS.local.md`, `AGENTS.override.md` and
anything under `.agents/` never are. An eligible file loads unless a `claudeMdExcludes` glob matches
its absolute path. The patterns merge across user, project, local and managed settings: apply the
ones `doctor` can read, report a file as `loads unless excluded` when any of those sources cannot be
read, and say that a `--settings` launch file can add patterns.

| Mode | AGENTS.md loads when (support available) |
|------|----------------------|
| `claude-md-or-agents-md` (default) | No `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` exists in the working directory or any ancestor — a `CLAUDE.local.md` alone suppresses it |
| `claude-md-and-agents-md` | Whenever support is available, after each directory's CLAUDE.md files and deduplicated — a local file suppresses nothing, and both files count toward launch context |
| `claude-md` | Never |
| `managed-only` | Never — only managed instructions load |

The freshness row regenerates rather than re-hashing. The install-time hash in
`.sd0x/install-state.json` proves only that the file was not hand-edited since install; an upgraded
plugin with an untouched old kernel matches it exactly. The regenerated bytes are compared, never
written — the remedy is `/codex-setup sync`.

Output a summary table with pass/fail status for each check. A `declined` hook is
listed with its real status rather than omitted — an operator who did not expect the
opt-out needs to see it, and a row that silently disappears cannot tell them.

## sync

1. Re-run `build-codex-artifacts.js` → overwrite AGENTS.md
2. Re-copy hook scripts (overwrite if changed) — **per hook, per the table below**
3. Re-copy runner scripts (overwrite if changed)
4. Update `.sd0x/install-state.json` with new hashes, preserving each hook's `status`

**`sync` updates what is installed; it never changes what was chosen.** Re-installing
a declined hook would silently undo the opt-out, and the operator would find out by
having a push blocked rather than by choosing it:

| Hook state | `--with-push-gate` | Action |
|------------|--------------------|--------|
| `installed` | either | Re-copy and update the hash. **Never removed** — the flag's absence is not a request to uninstall |
| `pending` | either | **Classify the destination first** (§ Phase 3): not sd0x-owned ⇒ the terminal `pending` — reprint the move-or-rename remedy and write nothing, because the re-copy would be exactly the clobber the original refusal prevented. Otherwise re-copy and update the hash, then **re-resolve activation** (§ Phase 3 mode table): active → `installed`; still not active → leave `pending` and reprint the recorded mode's remedy. This is the transition out of `pending`, and without it a hook the operator activated by hand stays recorded as broken forever while `doctor` keeps flagging a gate that fires |
| `declined` | not passed | Skip. Leave `status: "declined"` as it is |
| `declined` | passed | Install now and rewrite `status` per the Phase 3 activation test — this is the opt-in path |
| `unknown` (pre-contract state file) | not passed | Resolve from disk **sd0x integration evidence**, not container-file existence: Husky mode — an **intact sd0x block** (§ The Husky stanza) in `.husky/pre-push` → `installed`; markers present but not intact is **not** an answer this row may give, and never `declined` either: it routes to § sync's marker procedure, whose terminal `pending` is the recorded value (a truncated or emptied block certifies a boundary nothing can replace); dedicated-file modes — hook file present **and** verified sd0x-owned → `installed`; anything else (including an unrelated `.husky/pre-push` or a foreign hook file) → `declined`. Record the resolved value and say which was written. **Resolving to `installed` enters the `installed` row in the same run** — re-copy and update the hash, do not merely relabel: a pre-contract state file is exactly the case where the wired hook is oldest, and recording it as installed while leaving stale bytes on disk produces a `doctor` pass — activation is what `doctor` checks, and stale bytes are perfectly active — over a gate that is not the shipped one |
| `unknown` (pre-contract state file) | passed | Install now and record per the Phase 3 activation test. The flag is a request, and an unresolved entry is not a recorded opt-out to protect — resolving from disk first would answer `declined` and silently drop the request |

### Husky mode: "re-copy" names one artifact, and the wiring is two

Every "re-copy and update the hash" above is about `.claude/scripts/<script>`. In modes 2–4 that is
the whole of the sd0x wiring, so the sentence is complete. In **mode 1 it is half**: the other half
is the marker-delimited stanza this skill wrote into `.husky/<hook>`, which is executable text of
ours living in a file that is the project's. The `unknown` row above already refuses to record
`installed` over stale script bytes; the stanza needs the same sentence, because a stanza and a gate
that disagree is the one combination where `sync` can leave a repository **worse** than it found it
— the gate refuses to be sourced (§ The Husky stanza, measured 2026-08-22), so a re-copied gate
under a sourcing wrapper fails every push in the repository.

`sync` therefore reads `.husky/<hook>` before writing, and the marker pair — the same boundary
§ Uninstall uses — decides what happens. **This is a procedure, not a set of independent
predicates**, and the order is load-bearing: written as four parallel rows it was not a partition
at all, because "counts" and "order" are different questions and a row keyed on one cannot contain
an example that differs only by the other.

| Step | Ask | Then |
|------|-----|------|
| 1 | How many opening and closing markers? | **One each** → step 2. **Zero each** → step 3. **Anything else** — two or more of either kind, or one of one kind and none of the other → step 4 |
| 2 | Is it an **intact sd0x block** (§ The Husky stanza — opening first, and the bounded lines invoke this hook's script)? | **Yes** → **replace that block in place** with the current stanza, keeping its position and every byte outside it. Not "prepend again": the file would then carry two gates, and the older one still runs. **No** — closing before opening, or a body that invokes nothing → step 4 |
| 3 | Is there a **non-comment** line invoking or sourcing `.claude/scripts/<script>`? | **No** → prepend the current stanza, the § Phase 3 install shape unchanged. **Yes** → step 5 |
| 4 | — | **Terminal refuse** — write nothing, record `pending`, report `<hook>: the sd0x block in .husky/<hook> is duplicated, unbalanced, out of order or empty — repair by hand, then re-run`. A boundary that cannot be read cannot be replaced, and guessing which of two to overwrite is how one gate survives unnoticed |
| 5 | — | **Legacy wiring from before this contract** — an appended `.`/`source` line, which had no markers to be bounded by. It is evidence of a prior install, so it is **not** a decline; but it has no boundary this skill may edit inside, and deleting an unmarked line from the project's own hook is the clobber § Phase 3 refuses elsewhere. Write nothing, record **`pending`**, and report: `<hook>: .husky/<hook> sources .claude/scripts/<script> from before markers existed; the gate refuses to be sourced, so this hook fails every push. Delete that line, then re-run codex-setup sync` (add `--with-push-gate` when `<script>` is the gate) |

Every hook file reaches exactly one of steps 3–5, and the two clauses that carry that are the ones
a shorter form loses. **Order is asked separately from count** (step 2, not step 1): one opening and
one closing in the wrong order have the same counts as a well-formed pair and bound nothing, so a
count-only selector would send them to the replace arm. **"Referencing" is not "wiring"** (step 3):
a comment such as `# gate location: .claude/scripts/pre-push-gate.sh` is documentation, and reading
it as a sourcing line refuses an install that would have succeeded while telling the operator to
delete a line the file does not contain. A line is a reference only where it is not a comment —
leading whitespace stripped, first character `#`. That test is deliberately coarse in the safe
direction: a path named inside a live command still counts as wiring, because the cost of a false
"legacy" is a refusal the operator can read, and the cost of a false "clean" is a surviving source
line that fails every push with no remedy printed.

Step 4 is fail-closed in the same direction as the foreign-collision row: an unreadable boundary
refuses rather than picking. Step 5 amends the `unknown` row's disk-evidence test for mode 1 — a
legacy sourcing line answers "was this ever installed" with *yes*, so resolving it to `declined`
would both drop an opt-in the operator made and leave the broken line in place.

**`commit-msg` runs this same procedure.** What it is exempt from is the *opt-in* table above — it
is always installed and always re-copied, with no flag and no `declined` state. That exemption is
about **whether** the wiring is written; the procedure is about **how**, and mode 1 gives
`commit-msg` two artifacts exactly as it gives `pre-push` two: the copied script and a
marker-delimited stanza (§ The Husky commit-msg stanza). It needs the procedure more, not less —
the legacy installer appended sourcing to Husky hooks generally, and sourcing *this* guard is worse
than sourcing the gate: the gate refuses and takes the shell down loudly, while the guard `exec`s
and **replaces** the sourcing shell, so everything the project put in its own `commit-msg` hook
stops running silently (measured 2026-08-22 — § The Husky commit-msg stanza). Re-copying the script
under that wrapper preserves it; prepending beside it leaves it there. Step 5 is the only answer
that does neither. Its status still comes from the same Phase 3 activation test as every other
hook, so a `commit-msg` written where git does not resolve to it is recorded `pending`, never
`installed`. Every "record `installed`" in this file is shorthand for "run the activation test and
record what it answers"; there is no path that records `installed` without it.

Uninstalling an installed gate is deliberately not a flag on this skill. Removal is
**mode- and ownership-aware**, because the installer's Husky mode **prepends an
executing** stanza to a hook file that may carry the user's own commands (mode table above) — it
does not source, and it does not append: both were the retired construction, whose stdin-consumption
and `$0` fail-open defects § The Husky stanza records:

| Recorded `mode` | Safe removal |
|-----------------|--------------|
| `husky` | Remove **only the sd0x stanza** from `.husky/pre-push`; never delete the file — the rest of it belongs to the user |
| `hooksPath` / `direct` / `fallback` | Delete the hook file **only after verifying it is sd0x-owned** (it matches the shipped `pre-push-gate.sh` wiring and nothing else); otherwise warn and require manual reconciliation |

Then set the entry to `{"status": "declined"}` — the wiring removal **and** the state
entry, both, because the entry is what `sync` and `doctor` branch on: removing the
wiring alone leaves `installed`, so
`sync`'s first row re-copies the gate and `doctor` reports ❌ Missing in the
meantime — in every mode: the doctor's disk axis is sd0x wiring, so in Husky mode
it reads the missing stanza as Absent even though the shared `.husky/pre-push`
file still exists.
That divergence is the two commands working correctly on a state file that no longer
describes the disk, not a case either should paper over by guessing which side to
believe. A `--without-push-gate` would make an unnoticed flag change able to disarm a
push guard, which is the same silent-default failure the opt-in prevents.

## References

- `references/agents-kernel.md` — AGENTS.md kernel template
