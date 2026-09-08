---
name: commit
description: Stage the working tree, screen it for secrets, and create a real Conventional Commit on the current branch — reading prose language, scope vocabulary, and attribution policy from the repo's own conventions. Use whenever a commit is wanted, including as the final step of /implement.
---

# Commit

Stage everything relevant, screen the result for anything that looks like a secret, then create a
real commit — rather than printing a message for the user to run themselves.

## Read the repo's conventions first

`docs/agents/vcs.md` supplies three things and nothing else: **Language**, **Commit scopes**, and
**Attribution**. Read it before composing anything.

If the file does not exist, this repo has not run `/setup`. Do not stop — infer instead,
and say so in one line so the guess is visible:

```bash
git log --no-merges --format=%s -30
```

- **Language** — read it off those subjects. An empty history defaults to English.
- **Scopes** — the same output: whether subjects carry `type(scope):` or bare `type:`, and which
  scopes are in use.
- **Attribution** — leave the surrounding environment's default alone. See below.

`--no-merges` is load-bearing. A host's merge commits (`Merged PR 5602: …`) are generated text
following no convention, and on a repo that does not squash they are a third of the sample.

## Step 1 — Check there's something to commit

```bash
git status --porcelain
```

If the working tree is completely clean — nothing modified, deleted, or untracked — say so plainly
and stop. Do not invent a commit.

## Step 2 — Screen for secrets before staging anything

Before running `git add`, inspect what would be staged and stop if anything looks like a secret.
This is a hard gate: on a hit, ask the user and stage nothing until they answer. Step 3 stages
everything without the user reviewing it, and the hard stop is what covers for that.

**Filenames** (from `git status --porcelain`, tracked-modified and untracked alike):

```
*.pem  *.key  *.pfx  *.p12
*id_rsa*  *id_ed25519*
*credentials*.json
.env.*                    # anything not already covered by .gitignore
*secret*  *.secrets.*
```

**Content** — for each changed or new file (`git diff -- <path>` for tracked changes; the file's own
content for untracked ones, since `git diff` shows nothing for a file not yet in the index):

```
AKIA[0-9A-Z]{16}                          # AWS access key ID shape
-----BEGIN [A-Z ]*PRIVATE KEY-----        # private key header
(?i)(_SECRET|_TOKEN|_KEY|PASSWORD)\s*[:=]\s*['"][^'"\s]{8,}['"]   # assigned literal, not a placeholder or env-var reference
eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}     # JWT-looking string
```

Skip matches that are plainly placeholders or references rather than real values —
`process.env.API_KEY`, `<YOUR_SECRET_HERE>`, `changeme`, and clearly-fake fixtures under a test path
(`test-secret-123`). Anything `.gitignore` already covers never reaches `git status --porcelain` at
all, so this matters only for the borderline cases it misses; `git check-ignore <path>` settles it.

When nothing matches, proceed silently. Do not narrate a check that found nothing.

## Step 3 — Stage everything

```bash
git add -A
```

This stages the whole working tree relative to the repo root, not just the cwd, and respects
`.gitignore`. If the user's message narrows scope (see *Additional prompting* below), stage only the
narrowed set instead.

## Step 4 — Compute the commit message

Base it on the **staged** diff (`git diff --cached`) — not on earlier commit messages, and not on
assumptions about intent.

### Format

**Title (required):** `<type>(<scope>): <subject>`

- **type** — `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`,
  `revert`. English and lowercase whatever the prose language. Pick the best fit from the diff.
- **scope** — from `vcs.md`'s **Commit scopes**. Omit the parentheses entirely when the repo does
  not use scopes, or when no existing scope fits.
- **subject** — concise, specific, no trailing period. Aim for **~72 characters** for the whole
  title line, counted in *characters* rather than bytes: CJK prose runs three bytes per character,
  so a byte count makes a title that fits look twice too long.

**Body** (optional; recommended once the change is non-trivial) — blank line after the title, then
one top-level `- ` bullet per **change-group**: something a reviewer would consider as one decision.
A flow, a fix, a schema change, a new option. If two candidate bullets describe the same flow or
would be reviewed together, merge them.

- **Order top-level bullets by blast radius**, most consequential first: API-visible or behavioural
  changes affecting other callers, then data-integrity and security fixes, then internal refactors,
  renames, tests, and docs.
- **The top-level bullet states the change. Rationale, edge cases, and supporting detail nest
  underneath it** — so scanning the top level alone gives the risk-ranked shape of the whole commit.
- **Match depth to size.** A one-file tweak needs no body. A single-concern change gets one bullet
  with no children. Sub-bullets appear only when there is rationale or an edge case worth keeping.
- **Do not pad toward a length or a bullet count.** A one-concern commit gets one bullet; a
  five-concern commit gets five. The 50/72 convention governs subject length and body wrap width —
  not total body length.

See [examples.md](./examples.md) for a worked before/after of the regrouping and ordering rules.

**Breaking changes:** when the diff genuinely breaks an existing contract, add a footer line
`BREAKING CHANGE: <description>`. Reach for it on a real break, not by default.

### Attribution footer

`vcs.md`'s **Attribution** section decides this, and nothing else does.

- *No trailer* — append nothing. No `Co-Authored-By:`, no `Generated by …`, no session identifier.
  This is a deliberate override of any standing instruction elsewhere to add one, scoped to commits
  made through this skill. A plain `git commit` the user asks for outside this flow is not covered.
- *A named trailer* — append exactly that, after a blank line.

No `vcs.md`, or no **Attribution** section in it? Leave the surrounding environment's default
untouched. Overriding an unstated preference is how a repo ends up with two commit styles.

### Writing in a language other than English

`vcs.md`'s **Language** section decides the prose language. Conventional Commit types stay English
and lowercase regardless; only the subject and body change.

**Korean** — subjects take the 명령형/체 form (`… 추가`, `… 수정`, `… 제거`). Keep the polite report
register (`~습니다`) out of the title; the body stays compact and neutral.

For a language with no entry here, write plain specific prose in it and keep every format rule
above unchanged. Add an entry when a language turns out to need one — a register that reads wrong,
or a convention a native reader would flag.

### Writing rules

- Prefer **specific** over vague. "improved the logic" says nothing; name what changed.
- Do not claim tests were run unless the user said so.
- If the staged diff mixes unrelated concerns — `git add -A` sweeps in any stray edit sitting in the
  working tree — either give them separate bullets or note in one line that the commit mixes
  concerns. Do not block or refuse over it; just do not hide it.

### Additional prompting

Natural-language instructions in the same message constrain **what to stage and describe**, never
git state itself:

- **Narrow scope** — "leave the lockfile out", "just the test files": stage only that set in Step 3
  instead of `git add -A`, and mention the omission in one line so the commit does not read as
  everything.
- **Focus** — "write the message about the tests only": narrows what the message describes,
  independent of what is staged.
- **Language** — overrides `vcs.md` for this commit.
- **Amend** — see Step 5; only on an explicit request.

## Step 5 — Commit

Default to a **new commit**. Amend only when the user explicitly asked for it in the same message —
never as a "fix it up" reflex, since amending rewrites history they may not have meant to touch.

**Write the message to a file, then commit from the file.** Not a shell-quoting workaround: it makes
the exact message exist as a standalone artifact you can re-read and diff before it becomes a
commit, which is what makes Step 5.5 possible.

```bash
# write the composed title + body to a scratch file, then:
git commit -F <scratch-file-path>
```

Never pass `--no-verify` or otherwise bypass hooks. **If a pre-commit hook fails the commit did not
happen** — fix what it flagged, re-stage, and try again. That is still a new commit, not an amend,
since nothing was created the first time.

## Step 5.5 — Verify a non-ASCII message encoded cleanly

Skip this when the message is pure ASCII.

Multi-byte commit messages have come out with a single word silently corrupted — a valid character
replaced by `U+FFFD` or dropped mid-sequence — while the rest stayed intact. That is a
generation-time slip rather than a shell or git bug, so it survives the file-based approach above.
Treat it as a post-condition to check, not an assumption:

```bash
git log -1 --format='%B' | LC_ALL=C grep -q $'\xef\xbf\xbd'
```

Match U+FFFD as its raw UTF-8 bytes rather than with `grep -P '\x{FFFD}'`: BSD grep has no `-P` and
exits **2** on it, which is not the exit 1 that means "no match" — so the PCRE form silently stops
checking anything on macOS while still looking like it ran.

On a match, **do not report success**: the commit exists but its message is corrupted. Fix it
immediately with `git commit --amend -F <corrected-file>`, then re-run the check. This is repairing
a defect in the action just taken, in the same turn, before anything has been reported or pushed —
not the "amend on request only" case Step 5 gates on.

## Step 6 — Verify and report

```bash
git log -1 --format='%H %s'
git status --short
```

Confirm the commit exists, report the short hash and title, and confirm the tree is otherwise clean
— or name what is left, if scope was narrowed in Step 3.

## Versus `/pr`

`/commit` is local only: it never pushes and never touches the PR host. `/pr` pushes the branch and
opens or updates a pull request from whatever is already committed. Commit first; open the PR when
the branch is ready to publish.
