---
name: jev-assist
description: "You MUST use this before searching a codebase you have not read, whenever the question asks which files share a property no single pattern can match — what still does X, what has not been migrated to Y, what breaks a convention no linter encodes (`drift` judges every file one at a time), or where a change would land (`rerank` ranks a pool against a task). `gate` judges a staged diff for auth, PII, data-loss and swallowed-error risk before you commit. `validate` measures recall here. Applies one judgment to every file in a pool too large to read, in any language. One `node` call, nothing to install."
---

# jev-assist

Jev answers closed questions about code as probabilities, not prose. It applies one judgment across
a pool too large to read, in one of two shapes: **ranking** the pool against a task (`rerank` —
reach for it when grep has no literal to narrow with, or narrowed to a flood you cannot order), or
**classifying** every file in it one at a time (`drift` — when grep narrowed but cannot tell the
real hits from the noise). Neither is a second opinion on your own reasoning; it does not reason
better than the agent driving it. Use it where the pool is large; decide yourself where the pool is
small.

## Commands

| Command | Answers | Cost | Run it |
|---|---|---|---|
| `jev rerank "<task>"` | Which files does this task touch? | 1 call / 60 files; ~94k input tokens and 5–16s at ~705 files | Once per task |
| `jev drift [glob]` | Which files broke a convention? | 1 call / file; ~250ms at 2KB, ~950ms at 18KB | On demand |
| `jev gate [ref]` | Does this diff touch something dangerous? | 1 call / diff; 745–1770ms | Pre-commit |
| `jev validate [n]` | Is `rerank` accurate on this repo? | n × a full `rerank` | Once per repo |
| `jev check` | Is the key and config well-formed? | Free, offline | After editing config |
| `jev key <API_KEY>` | — stores a key at 0600 | Free, offline | Once per machine |

Exit codes: `gate` returns 1 on any flag, `check` returns 1 on any config problem or a missing
key. Every command returns 1 on a usage, config or API error, so a non-zero exit is not by itself
a finding — read the output.

## Which command — route on the probe, not the wording

**Always grep first.** One probe, and its outcome picks the command. Nothing here runs on a task's
phrasing: a vague question whose words match the code is still grep's job, and a precise question
whose words don't match is not.

| The probe came back | You cannot | Use |
|---|---|---|
| Converging on one neighborhood | — | Neither. Read the files. |
| Empty — no literal to search | find the entry point | `rerank` |
| Flooded — hundreds of hits | **rank** them: which matter most for this task | `rerank` |
| Flooded — hundreds of hits | **classify** them: which are real instances vs noise | `drift` |
| A diff, about to be committed | see what a linter cannot | `gate` |

**Rank vs classify is the distinction that gets missed.** Both start from a flood. Ask which
question the flood failed to answer:

- *"Which of these 200 files matter for the change I'm making?"* → one task, many candidates,
  needs an ordering → **`rerank`**.
- *"Which of these 200 hits are actually the thing I'm looking for?"* → one question, many files,
  needs a yes/no per file → **`drift`**.

**The tell is what the exclusion asks, not how many you wrote.** Iterating on a pattern is normal —
fixing a word boundary, narrowing a path, changing the output format. Those stay in grep. The
signal is an exclusion that needs to know *what a file is* or *what a match means*: is this string
user-facing copy or a comment, is this file a fixture or the real thing, is this `catch {}`
deliberate. A pattern cannot carry that context, so each such exclusion is a judgment you are
hand-coding against a proxy. Those belong in a convention's `ok` field, as prose, evaluated per
file.

**Narrow before judging.** `drift` is the usual place the two compose: when a literal search can
cheaply rule out most of the repo, run it first and pass the survivors as a glob or path list
rather than scanning everything at 1 call per file. (The reverse order, grep *after* `rerank`, is
[Combining with grep](#combining-with-grep).)

## Invoking

`jev` is on PATH only after `npm link`. Installed as a skill it is not, so call the script by
absolute path. **Nothing sets `$SKILL_DIR` for you** — substitute the real path, quoted if it
contains a space:

```sh
node "/absolute/path/to/jev-assist/scripts/jev.mjs" validate 20
```

Below, `jev` is shorthand for that command. The working directory is always the repo being
judged, never the skill directory.

## What the script touches and sends

`scripts/jev.mjs` is the only code this skill runs — one ~370-line file, zero npm
dependencies, maintained at github.com/glud123/jev-assist where every change sits in the
git history. Its side-effect surface is greppable in a minute: exactly one `fetch` (in
`ask()`, to the endpoint the key prefix selects — the provider table in Setup — or
`JEV_API_URL`); `execFile` spawns only `git`; no `eval`, no dynamic imports. The only
writes are the key file, stored outside every repo at 0600, and `.jev-rerank.json` in the
repo root when `rerank --json` opts into it.

What leaves the machine: `rerank` sends file paths, the config's `description` and the
task text; `drift` sends each file's contents; `gate` sends the diff. Every call carries
the API key. That is the tool working, not a leak — if a repo must not leave the machine,
do not point jev at it.

## Setup

Requires an API key plus `jev.config.json` in the repo root.

**Key first, and stop for it.** If the user has not given you a key and none is stored
(`jev check` says `no API key`), ask for it and wait. Do not write the config, do not run
`validate`, do not proceed with the surrounding task — every command that calls the API fails
without a key, so any work you do first is work you did not need to do yet. One question up
front beats a finished task that ends in "now paste your key".

Everything else you can derive by reading the repo. The key you cannot.

### Key

```sh
jev key sk-or-v1-...
```

- Store it for the user; do not ask them to run `export`.
- Lands in `~/.config/jev/key` at 0600 (`$XDG_CONFIG_HOME` honoured), outside the repo — a key in
  the working tree eventually gets committed.
- `JEV_API_KEY` in the environment wins when set.
- Never write a key into `jev.config.json`, a shell rc, or any tracked file. Never echo it in
  full; `jev key` prints it masked.

Provider is derived from the key prefix. The `{state, model, questions}` body and `{answers}`
response are identical either way, so nothing else changes:

| Key prefix | Endpoint | Model |
|---|---|---|
| `sk-or-` | OpenRouter Decisions | `~typesafe/jev-latest` |
| anything else | TypeSafe direct | `jev-latest` |

`JEV_API_URL` / `JEV_MODEL` override both, for a self-hosted gateway or a pinned version. Read
`jev check` before debugging a call: a wrong-provider key fails as a plain 401.

### Config

If the repo has no `jev.config.json`, **write one, then hand it to the user to review.** Do not
copy the example across unedited — its conventions name i18next, TanStack Query and
`src/services`, so in a repo without those it asks three questions that cannot be true.

Read `jev.config.example.json` in this skill's directory for the shape. Derive content from the
repo:

| Field | Required | Content | Failure mode if wrong |
|---|---|---|---|
| `description` | yes | One line: what the app is, which libraries the conventions name. Read `package.json` / `go.mod` / `pyproject.toml` rather than guessing. | Model lacks context for every question |
| `include` | yes | Globs covering source the repo actually has. Confirm each with `git ls-files <glob> \| wc -l`. | A glob matching nothing makes `rerank` silently score zero files |
| `conventions` | yes | Only rules this codebase actually follows, found by reading it. Anchor each `ask` to a concrete module (`the wrapper in src/services`), never a principle. Three or four real ones beat ten aspirational ones. | A convention the repo never adopted flags every file, teaching the user to ignore output |
| `gates` | yes | Risks that fit this repo. `auth_or_crypto` and `data_loss` travel well; name the actual surface (which module holds payments, what counts as PII here). | Generic gates flag nothing useful |
| `exemptions` | no | Path fragments where a convention is legitimately violated: mocks, fixtures, the wrapper module itself. | Known-good files flag forever |

Optional numbers, all with working defaults — leave them alone unless something measured says
otherwise:

| Knob | Default | Meaning |
|---|---|---|
| `batchSize` | `60` | Files scored per `rerank` call |
| `topN` | `20` | Rows `rerank` prints (a fixed count, not a relevance filter) |
| `threshold` | `0.7` | Probability at or above which `drift` and `gate` count a hit |
| `validateK` | `[20, 40]` | Cutoffs `validate` reports recall at |

When a flag is noisy, fix the `ask`/`ok` text, not `threshold` — the noise scores high too.

### Hook

Once per machine, at setup. Run it without asking — it is additive, idempotent and backs the file
up first:

```sh
node "/absolute/path/to/jev-assist/scripts/install-hook.mjs"
```

This registers two hooks in `~/.claude/settings.json`. Neither is related to `jev gate`, which
judges a diff. The installer only copies the skill directory, so nothing else registers them for
you.

- **`SessionStart`** puts `hooks/preflight.md` in context at the start of every session — a short
  reminder covering both shapes.
- **`PreToolUse`** (`scripts/pretool.mjs`) asks for confirmation the first time a session runs a
  repo-wide file-enumerating search: `grep -rl`/`-rc`/`--include`, or the `Grep` tool in a
  file-listing mode. Once per session, keyed on session id, so a long grep chain costs one
  keypress. Anything it cannot classify passes silently.

The second hook exists because the first was not enough. A session with the full preflight in
context, the full description in its skill listing, and a memory saying to use the skill still
answered "which files have no i18n yet" with nine hand-written greps and never called the Skill
tool — the injected text sat 40 messages behind the moment the reflex fired, and the first action
was `ls`, which no reminder about grep covers. The preflight is the argument; `PreToolUse` is what
puts it in front of you at the moment you are making the decision.

The installer refuses to write if the settings file is missing or unparseable, keeps any other
hooks on both events, and leaves a `.jev-bak` beside the file. **They take effect in the next
session**, so do not expect either in the one that ran the installer. Report that to the user
rather than letting them conclude it failed.

### Verify

Once per repo at setup, not at the start of each session:

```sh
jev check         # shape: placeholders, empty groups, exemptions naming no convention
jev drift         # a first pass — read the flags yourself before showing anyone
jev validate 20   # is rerank accurate on this repo at all?
```

`jev check` is mechanical and passes a config that asks confidently wrong questions: it gates the
handoff, it does not substitute for it. Run `drift` against a handful of files whose answer you
already know — a convention flagging nearly everything or nothing is miscalibrated. Hand the user
the config plus what that pass found, and state which conventions you inferred from reading code
versus which you guessed. The guesses are what they should check first.

### Uninstall

Read this when the user asks to remove, uninstall or disable jev-assist. Deleting the skill
directory is not enough: everything below was written outside it, and two hooks name the script
by path — the pre-commit hook breaks every commit once it is gone, the `SessionStart` hook breaks
every session.

Work the list in order. Report what you removed and what you found nothing of.

1. **The pre-commit hook, first.** A hook calling `jev gate` fails every commit once the script
   is gone. Check `.git/hooks/pre-commit` and any Husky or pre-commit config (`.husky/`,
   `.pre-commit-config.yaml`). Delete the hook only if `jev gate` is all it does; otherwise
   remove that line and leave the rest.
2. **The `SessionStart` and `PreToolUse` hooks**, before the skill directory goes: both name a
   script by absolute path, so once that path is gone every session starts with a failing hook and
   every `Bash`/`Grep` call hits a second one. Run
   `node "/absolute/path/to/jev-assist/scripts/install-hook.mjs" --remove` while the scripts still
   exist; one run removes both. It leaves `~/.claude/settings.json.jev-bak` behind — mention it; it
   is a copy of their settings, theirs to keep or delete. If the skill directory is already gone,
   edit `~/.claude/settings.json` by hand and drop the entries whose command contains
   `session-start.mjs` or `pretool.mjs`.
3. **The key.** `rm -f ~/.config/jev/key` (`$XDG_CONFIG_HOME/jev/key` when set), then
   `rmdir ~/.config/jev` if empty. It is a credential — deleting it is the point, not a
   courtesy. If the key is live and used elsewhere, say so rather than silently dropping it.
4. **Environment variables.** Grep the user's shell rc files and any `.env` for `JEV_API_KEY`,
   `JEV_API_URL`, `JEV_MODEL`. A `JEV_API_KEY` left in a rc file is an undeleted credential.
   Show the lines and let the user remove them — do not edit a shell rc yourself.
5. **Per-repo output**, in every repo the skill ran against: `rm -f .jev-rerank.json`, and
   `jev.config.json` after showing it to the user. The config is hand-tuned and worth keeping if
   they may reinstall.
6. **`.gitignore`.** Drop the `jev.config.json` and `.jev-rerank.json` lines the setup added.
7. **The command on PATH**, if `npm link` was ever run: `npm unlink -g jev-assist`. Check with
   `which jev` — a dangling symlink is a confusing failure later.
8. **The skill directory itself**, plus the entry in whatever registry installed it.

## `jev rerank "<task>"`

Scores every tracked file for relevance, prints the top N. Decide per task, not per session:
nothing runs on its own, and ranking 705 files is wasted on a task whose scope you already know.

**Skip it when:**
- The task names the file, or an exact symbol, string or route grep finds in a second.
- The repo is small enough to read.
- `validate`'s `worst:` line shows this class of task has no semantic signal (dependency bumps,
  sweeping renames).

**Reach for it when:**
- The task's words and the code's don't overlap: a different natural language, UI copy that lives only in i18n keys, a concept the code names differently, a behavior described with no shared noun.
- The files that matter likely share no token with the task.
- The probe flooded — grep returned hundreds of hits with no way to rank them.

Grep first — one probe, three outcomes: convergence (done), empty, or a flood you cannot rank. Only the last two are rerank's business, and the probe settles most cases in seconds.

**Measured** on one private 705-file React app, 10 consecutive commits as tasks, ground truth
from what each commit changed: **recall@20 0.68, recall@40 0.80** over 41 files.

**Where it wins:** files sharing no keyword with the task. A shared upload service ranked 6th for
an image-upload task in an unrelated feature — grep on either the feature name or `upload` would
have missed or buried it.

**Where it fails:** files changed only because a reference changed rank low (one ground-truth
file landed at 121/705). Semantic scoring cannot see structural coupling, which shows up as a
size effect: every task touching 1–4 files scored full marks, while an 11-file change reached
5/11. Treat the top 20 as the core of a change, never the whole of it — see
[Combining with grep](#combining-with-grep) for closing the rest.

**Reading the list:** `topN` is a fixed row count. A task touching 3 files still prints 20 rows,
and the rest are the least unrelated files in the repo rather than candidates.

Scores are levels, not probabilities: **0–3**, where 3 is "likely must be read or edited", 2 is
"shows the existing pattern to follow", 1 is background and 0 is unrelated. **Read everything at
2.5 or above.** Cut at a gap below that if there is one, but do not wait for a gap — a top 20
spanning 0.4 means nothing stood out, not that all 20 are candidates.

Ranking is per file, not per symbol. A file holding both a live and a stale declaration of the
same name ranks once, on the strength of the file; you still have to disambiguate by reading. A
high rank is not evidence that the thing you are looking for in that file is the live one.

**Output:** stdout only, nothing written to disk. Add `--json` only when something must read past
the cutoff; it also dumps every row to `.jev-rerank.json` in the repo root, so tell the user to
gitignore it if they do not already.

Run once per task, not per edit. The cost that rules out a loop is ~94k input tokens per run, not
the latency — it can come back in under 5s, which makes rerunning it feel cheaper than it is.

## Combining with grep

`rerank` finds the entry point. grep closes the change. Neither does the other's job, and the
failure mode of using only `rerank` is not a missed file in the ranking — it is a ranked file you
read and then under-changed.

1. **`rerank` once**, with the task phrased concretely — what gets added or changed. Use the
   repo's terms where you know them and the user's words where you don't; rerank matches meaning,
   not tokens. Read everything at 2.5 or above.
2. **Name the symbol** you are about to add or change: the prop, the option field, the exported
   type, the component.
3. **`git grep -n <that symbol>`**, and again for the component callers actually import. This is
   the class `rerank` structurally cannot rank — files that change only because a reference
   changed. The two that bite every time are the shared type definition and the compatibility
   wrapper the rest of the app still calls.
4. **Done means every public surface a caller touches accepts the new option.** A hook taking an
   option that no exported prop type declares is unreachable code: it typechecks, it passes
   tests, and no caller can reach it.

Skip step 1 when the task already names a file or an exact symbol. Never skip step 3.

Measured, one task, same repo and model, `rerank`-led against grep-only: the `rerank` arm spent
14% fewer tokens and 24% less wall clock, ranked all four ground-truth files inside the top 20 —
and still shipped the option unreachable, because two of those four ranked files (the shared type
at #3, the wrapper at #16) were read but not edited. Recall is not completeness. Steps 2–4 are
where the grep-only arm spent its extra tokens, and they are not optional.

## `jev validate [n]`

Replays recent commits as tasks and scores `rerank` against what each commit actually changed.
Run once per repo, before relying on a ranking you cannot check.

```sh
jev validate 20
```

`n` is how many commits it must **score**, not how far back it looks. It reads up to `3n`, skips
merges and any commit touching no file in `include`, and stops once `n` qualify — so with narrow
`include` globs the sample can reach much further back than `n` commits.

Recall does not transfer between repos. A number from a 705-file React app says nothing about a
Go monolith, and a confident 0.87 on a file is unfalsifiable alone; this makes it falsifiable
using history the repo already has.

Read the `worst:` line as carefully as the recall figure. Dependency bumps and sweeping renames
have no semantic signal and score low by nature — a fact about the task, not a defect. That line
is what tells you when to skip `rerank` entirely.

Two adjustments a hand-rolled comparison misses, so do not reimplement this with
`git show --name-only`:
- Files a commit **added** are excluded — they did not exist when the task was written, and
  counting them inflates recall.
- Files it **deleted** cannot be ranked against today's tree at all.

## `jev drift [glob]`

Asks every convention in the config against every file. Catches drift grep cannot, because grep
only finds what you already thought to look for.

**Reach for it when:**
- The user asks a sweep: "which files still do X", "what hasn't been migrated to Y yet", "is Z
  consistent across the app". One question, every file, a yes/no each.
- A literal search floods and you cannot classify the hits — the pattern matches, but it answers a
  different question than you asked. The tell is an exclusion that needs context a pattern cannot
  carry: is this string user-facing copy or a code comment, is this file a fixture or the real
  thing, is this `catch {}` deliberate.

**Skip it when:**
- A linter, type checker or test can decide it. Those are cheaper and actually authoritative.
- The literal search already converged — the hits are the answer, with no noise to separate.
- No convention in `jev.config.json` covers the question. Add one first (they cost nearly nothing
  to add) or you are running the wrong questions against the right files.

**Scope it.** `drift` is 1 call per file, so the glob is the cost knob: `jev drift 'src/features/**'`
beats a bare `jev drift` when you already know where the answer lives. When a literal search can
cheaply exclude most of the repo, run it first and pass the survivors.

Question count barely affects cost or latency — output tokens are free and questions evaluate in
parallel. **Ask everything you care about in one pass:** ten conventions cost about what one
does.

Probabilities read as magnitude, not just against a threshold. A file importing a UI library two
different ways scored 0.62 while a single-style file scored 0.97 — the middling value correctly
described a mixed state rather than indecision. Treat 0.4–0.7 as "partially true" and go look.

## `jev gate [ref]`

Judges a staged diff, or a given ref, against the config's gates. Exits 1 on any flag so it hooks
into pre-commit.

Measured on four real commits:

| Change | Result |
|---|---|
| Decryption feature | `auth_or_crypto` 0.99 |
| Double-submit fix | `silent_catch` 0.91 |
| CSS tweak | clean (≤0.64) |
| Comment-only | clean (≤0.03) |

At 745–1770ms per diff it fits in a commit hook without being felt. It catches a class nothing
else in a typical toolchain does: `tsc`, ESLint and unit tests all pass a change that quietly
touches decryption or drops user input.

## Reading the output

Flags are prompts for a human look, never verdicts. Two failure modes matter more than false
positives.

**Correct but not actionable.** `silent_catch` fired at 0.91 on a deliberate `catch {}` that
carried a comment explaining why the failure was safe — literally right and useless. Fix the
criteria, not the threshold: that gate's `ok` text now ends with "OR the catch is accompanied by
a comment explaining why the failure is safe to ignore." Same for hardcoded copy firing on mock
chart data, fixed by excluding fixtures in the `ok` text and `exemptions`. Tune for this early —
an audit that cries wolf gets ignored, and an ignored gate is worse than no gate, costing money
while buying a false sense of coverage.

**Typed output guarantees shape, not correctness.** A confident number can be confidently wrong.
Run `jev validate` before trusting `rerank` on a new repo, and check a convention or gate against
files whose answer you verified by hand. Without that step you are reading probabilities you
cannot calibrate.

## Why the config is per-project

The flow transfers across repos; the questions do not. Every convention needs its own exemptions,
and the same question needs different phrasing in different codebases — `hardcoded_copy` criteria
that works in an i18next app is wrong in an app with no i18n. Keep `jev.config.json` in the repo
it describes and tune it there.

Validation is per-project for the same reason: a repo with meaningful commit history carries its
own ground truth. A shallow clone or squashed history gives `validate` nothing to work with, and
there you are guessing at recall.

## When not to use this

- **Scope you already know.** A named file, an exact symbol, a repo small enough to read: grep or
  just open it. `rerank` costs ~94k input tokens to tell you what you knew.
- **One-off judgments where you are the one waiting.** Three options in front of you: decide. A
  round trip adds latency and no information.
- **Judging candidates you just generated.** If state and options both come from the agent, the
  probability measures the agent's own self-consistency, not an outside opinion. It will look
  like validation and will not be.
- **Anything a compiler, type checker, or test can decide.** Those are cheaper, faster and
  actually authoritative. Use Jev for what they structurally cannot see.
