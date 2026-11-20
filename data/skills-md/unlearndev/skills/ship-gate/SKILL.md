---
name: ship-gate
description: Read the staged git diff and flag anything that shouldn't be committed — secrets or API keys, leftover debug code (dd(), console.log, etc.), large commented-out blocks, and accidentally added large or binary files. For each problem show the file and line and why it's a problem, then end with a clear PASS or BLOCK. Use before committing, when the user asks to "check what's staged", "review my staged changes", "anything I shouldn't commit", "scan the diff before I commit", or wants a pre-commit safety check.
---

# Check the staged diff before committing

Scan everything that is currently **staged** for commit and flag anything that should not
be committed. This is a focused safety gate, not a code review — do **not** comment on
style, naming, architecture, or correctness. Find only the four classes of problem below,
report each with its file and line and why it matters, and finish with a single verdict.

## 1. Get the staged diff

Only inspect what is actually staged (`--cached`). Unstaged changes are out of scope.

```
git diff --cached --stat          # overview of staged files
git diff --cached                 # full staged diff (read this)
git diff --cached --numstat       # added/removed line counts; "-" marks binary files
git diff --cached --name-only --diff-filter=A   # newly ADDED files (for size/binary checks)
```

Read the **whole** staged diff. Only consider **added** lines (lines starting with `+`) for
debug code, secrets, and commented-out blocks — pre-existing lines shown as context are not
introduced by this commit and should not be flagged. For added/binary file checks, inspect
the working-tree files reported as added.

If nothing is staged, say so plainly and stop — there is nothing to check.

## 2. What to flag

Go through the staged diff against each lens. Most commits trigger only a few — that's
expected. Don't manufacture findings to fill a category; each finding must point at a real
added line or file.

### Secrets and API keys

Added lines that look like real credentials, not references to them. Look for:

- Assignments where the value is a literal secret: API keys, tokens, passwords, private
  keys, connection strings with embedded credentials.
- Recognisable key shapes: `AKIA…` (AWS access key), `sk-…` / `sk-ant-…` (OpenAI/Anthropic),
  `ghp_…` / `gho_…` (GitHub tokens), `xox[baprs]-…` (Slack), Google `AIza…`, Stripe
  `sk_live_…` / `rk_live_…`, JWTs (`eyJ…`), `-----BEGIN … PRIVATE KEY-----` blocks.
- Long high-entropy strings assigned to names like `*_KEY`, `*_SECRET`, `*_TOKEN`,
  `*_PASSWORD`, `PASSWD`, `*_DSN`, `AUTH`, `CREDENTIAL`.

Distinguish real secrets from safe non-secrets so you don't cry wolf:

- **Safe / don't flag:** placeholders (`your-api-key-here`, `xxxxx`, `changeme`, `example`,
  `<token>`), `.env.example` entries with empty or dummy values, values read from config
  (`env('STRIPE_SECRET')`, `process.env.X`, `config(...)`), obvious test fixtures.
- **Flag:** a concrete-looking secret value committed in source, **and** any secret that
  appears in a real `.env` file staged for commit (a `.env` with live values should almost
  never be committed — call that out specifically).

When unsure whether a string is a live secret, flag it as **suspected** and explain why —
better to surface it for a human to confirm than to stay silent.

### Leftover debug code

Added lines that are clearly debugging scaffolding left behind, judged against the file's
language:

- **PHP:** `dd(`, `dump(`, `ddd(`, `var_dump(`, `print_r(` (when not returned/used),
  `ray(`, `error_log(`, `\Log::debug(` added ad hoc, `Debugbar::`.
- **JS / TS / Vue:** `console.log(` / `console.debug(` / `console.warn(` added for
  debugging, `debugger;`, `alert(`.
- **General:** `TODO: remove`, `FIXME`, `XXX`, temporary `sleep(`, hardcoded test toggles
  like `if (true)` / `return; // skip`.

Use judgement: a `console.error` in a legitimate error handler or a logging call that's part
of the app's real logging is **not** debug litter. Flag what looks like a forgotten trace.

### Large commented-out blocks

Added runs of commented-out **code** (not explanatory prose). Flag a contiguous block of
roughly **5+ lines** of commented-out code — dead code that should be deleted rather than
committed. A short comment, a doc comment, or a one-line note is fine; don't flag those.
Identify it by the file's comment syntax (`//`, `#`, `/* … */`, `<!-- … -->`) wrapping
things that read as code (statements, function bodies, markup).

### Accidentally added large or binary files

From the newly **added** files (`--diff-filter=A`):

- **Binary files** — `git diff --cached --numstat` shows `-` for both add/remove columns on
  binary files. Flag added binaries that look unintended: compiled output, archives, images
  dumped into source, `.zip`, `.tar`, `.gz`, `.pdf`, `.sqlite`, `.db`, fonts, media. Use
  judgement — an intentional asset in an assets directory is fine.
- **Large files** — check the on-disk size of added files (e.g. `wc -c`, or
  `git cat-file -s :<path>` for the staged blob). Flag anything roughly **>1 MB**, and flag
  hard regardless of size if it's the kind of thing that shouldn't be in git at all
  (`vendor/`, `node_modules/`, `*.log`, build artefacts, `.env` with real values, OS junk
  like `.DS_Store`).

## 3. Report findings

Output Markdown. Lead with the findings grouped by the four categories above; include only
categories that actually have findings. For each finding give:

- **File and line** — `path/to/file.php:42`. Use the line number of the added line in the
  new file. For a commented-out block, give the start–end range. For a whole-file problem
  (binary/large/`.env`), the path alone is enough.
- **What** — the offending snippet (truncate/redact secrets — show enough to locate it, e.g.
  `STRIPE_SECRET=sk_live_51H…` — never echo a full live key).
- **Why** — one short clause on why it shouldn't be committed.

Keep each finding to a line or two. No preamble, no code-quality asides.

## 4. Verdict

End with a single bold verdict word — `**BLOCK**` or `**PASS**` — and nothing after it. No
trailing summary or explanation; the findings above already say why.

- **BLOCK** — if there is **any** secret/API key, or any other finding serious enough that
  committing would be a mistake (real `.env`, committed credentials, a stray binary/large
  file, obvious debug litter). When in doubt about a suspected secret, lean to **BLOCK**.
- **PASS** — only if nothing was found, or the only findings are clearly harmless.

Format:

```
**BLOCK**
```

or

```
**PASS**
```

Never soften a real secret finding — a leaked key in history is expensive to undo.
