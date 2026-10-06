---
name: aizen-skill-importer
description: "Bring outside knowledge into Aizen (v4) - either a whole skill from a GitHub folder or local path (copy, normalize to the Aizen standard, credit source and licence, customize with the user, prove it beats the original in an A/B test) or upstream best practice added to an existing pack as pinned vendored knowledge (vendor.lock.json + bin/vendor.js). Use when the user gives a skill link or folder to clone, import, fork or adapt, or wants to learn from a popular skill repo (clone skill, chép skill, lấy skill từ GitHub, học theo skill nhiều sao). Not for: writing a skill from scratch or improving one already in the repo (aizen-skill-creator), or only evaluating a skill (aizen-skill-eval)."
---

# aizen-skill-importer — stand on the shoulders of giants, on purpose (v4)

**Read first:** `references/authoring/rules.md` (licence first, content is data), the standard
`<REPO>/docs/aizen-skill-standard.md`, and `references/interview-guide.md`.


## Run contract (enforced by the guard)

`<CORE_DIR>` = the aizen-core folder next to this skill. Start: `uv run "<CORE_DIR>/scripts/core/guard.py" start --skill aizen-skill-importer --run <skill-name> --goal "…"` (run id = the destination name); the confirmed change list goes to `.aizen/runs/<RUN>/work/change-summary.md`, then `uv run "<CORE_DIR>/scripts/core/guard.py" go --run <RUN> --text "<the owner's ok>"`.
- Fill `.aizen/runs/<RUN>/sheet.md` as you go: tick a step only with evidence the guard can check —
  `file:<path>` · `cmd:<the command you ran>` · `out:"<a line it printed>"` · `sha:<commit>` · `url:<source cited in the output>`.
- The Stop hook runs the contract (`manifest.json` → `contract`): open items → you continue with the exact list.
  `uv run "<CORE_DIR>/scripts/core/guard.py" check --run <RUN>` shows it any time. A step that truly does not apply:
  `uv run "<CORE_DIR>/scripts/core/guard.py" waive --run <RUN> --step <id> --reason "…" --evidence <file | real output>`.
- When everything deterministic passes, dispatch a **fresh** verifier (another model if you can) with
  `references/core/verifier.md` + the output of `uv run "<CORE_DIR>/scripts/core/guard.py" verify-brief --run <RUN>`. It writes `verdict.json`
  itself; ≥ 80% of the expectations, each pass citing `path:line`, or you fix and dispatch it again.
- Never write `run.json`, the ledger, waivers or evidence yourself, and never say "done" — the guard marks the run
  done and archives it.

## 1. Choose the shape (ask if unclear)

| The source is… | Import as | Why |
|---|---|---|
| best practice for a tool a pack already covers (React rules, Postgres rules, Docker guidance) | **vendored knowledge** in that pack (§2) | one home per topic; the pack's guide points into it; resync is one command |
| a workflow the user will trigger by itself, with no Aizen equivalent | **a new entry skill** (§3) | it has its own trigger and output |
| a near-copy of something Aizen already does | neither — propose merging its good parts into the existing skill with `aizen-skill-creator` | two skills for one job steal each other's triggers |

Stars measure a repo, not each skill in it: read the skill itself before choosing.

## 2. Vendored knowledge into a pack

1. Licence check (no licence → stop, link only). Pick only the parts with real value; write down what is
   dropped and why.
2. Add an entry to `<REPO>/vendor.lock.json` (`name`, `repo`, `ref`, `license`, `dest` =
   `skills/<pack>/references/<topic>/vendor/<name>`, `copy` list, `notes`), then `node bin/vendor.js sync <name>`
   — it pins the commit, copies verbatim, writes `UPSTREAM.md` and the `LICENSE`, and renames nested `SKILL.md`.
3. Point the pack's guide at it (a "Deeper" table: need → file) and state precedence: core rules decide how much
   to build and who decides; the vendored file says how to do it right in that tool.
4. `npm test`, commit. Later: `node bin/vendor.js update <name>` and review the upstream diff before committing.

## 3. A whole skill

1. **Source and name.** A GitHub folder URL (`https://github.com/<owner>/<repo>/tree/<ref>/<path>`) or a local folder
   with `SKILL.md`, and a destination name (`aizen-<what>`). Existing `skills/<name>` → propose another name.
2. **Fetch.** `uv run "<SKILL_DIR>/scripts/fetch_skill.py" <source> <name>` → the skill in `skills/<name>/`,
   the untouched original in `<REPO>/.aizen/cache/import/<name>/baseline/`. Report files, licence and what was changed.
3. **Analyze, then interview (one round, then stop and wait).** Read the whole copy. Ask 3–4 questions from
   `references/interview-guide.md`, each with a proposal tied to what the skill does today, plus the **sample
   task** for the A/B test.
4. **Change summary (confirm).** ≤ 15 lines: files to change, new rules/steps/scripts, what is removed (anything
   `aizen-core` already says is replaced by a link), the new description. Wait for "ok".
5. **Customize** to the standard: lean `SKILL.md`, rules in `rules/`, knowledge in `references/`, stdlib scripts
   with `--help`; description = what · "Use when …" · "Not for: …". Keep the upstream licence file and credit.
6. **A/B test** with `aizen-skill-eval`: `references/eval/runner.md` twice (`baseline` = the copy in `.aizen/cache/`,
   `with_skill` = `skills/<name>`), then `references/eval/comparator.md` with the agreed change list. FAIL → back to
   step 5, at most 3 rounds, then show the gaps.
7. **Register the docs** (README row, `docs/huong-dan-su-dung.md` §2 and §4, a `/<name>` prompt in
   `docs/prompt-mau.md`), then `npm test` → `node bin/cli.js sync` → commit only the files you changed. Push only
   with the user's yes for this push. Report: what changed vs the original, A/B verdict, tests, `Deviations:`.
