---
name: aacpd
description: Archive an implemented issue, stage remaining tracked changes, commit code+archive together, push, and deploy to dev. Use when the user says "/aacpd", "aacpd #", or asks to archive+commit+push+deploy an issue (typically right after /tdd2 leaves changes staged).
---

# aacpd — archive, add -u, commit, push, deploy

Merges a `/tdd2`-staged issue into `main` and deploys it to dev, in one
commit. Companion skill: `/tdd2` (implements, stops at `git add`).
Combined skill that chains both, per issue, fully automatically:
`/autotdd`.

**Precondition**: code changes for the issue are already staged
(`git add`, not yet committed) — that's where `/tdd2` stops. This
skill does the rest.

## Stream conventions

Two issue streams are handled:

- **Stream IDs**: `issue-<N>` and `autofix-<N>`. Bare-number arguments
  (e.g., `aacp 22`) default to the `issue` stream; `aacp autofix-3`
  selects the autofix stream.
- **Archive target**: `issues/archive/<YYYY>/<MM>/<DD>/` for either
  stream — 파일명은 **그대로**(라이브·아카이브 단일 규약, 변환 없음)
  `git mv`로 옮긴다 (`git log --follow` 이력 추적 보존).
- **산출물 동반 아카이브** (issue-47, v3 마커 개명): 이 이슈의 살아있는
  출력 파일(`issue-N__code-review-by-*.md`, `issue-N__refix-plan.md`,
  `issue-N__agent-stats.json`)도 같은 커밋에서 함께 아카이브한다 —
  별도 호출 불요. `agent-stats.json`은 이동 직전, 대상 repo에
  `bin/log-cost-summary.py`가 있으면(없으면 스킵) 먼저 그걸 호출해
  `cost_details`(issue-50 — mvp/review/refix-plan/refix 4단계 5h/7d
  쿼터 계측 감사 로그)를 모델별로 합산한 `cost_summary`를 채우고, 그
  다음 `bin/agent-stats-archive.py`가 `archived`/`duration`
  필드를 채운다.
- **Commit prefix**: `<stream>-<N>: <summary>` (e.g., `issue-22: ...`,
  `autofix-3: ...`).
- **파일명 규약(v3)**: 단일 정본은 `docs/spec/spec-issue-filenames.md`.
  pending 판정은 마커 부재, 또는 `__must-fix-by-`/`__analysis-required`만
  존재 — `__tech-debt-by-`/`__STATE-manual`/`__STATE-agent-failed` 등
  파킹 파일과 `__code-review-by-`/`__refix-plan`/`__agent-stats` 산출물은
  pending 목록에서 제외된다.

## A naming note before anything else

`aacpd` is a sequence of **five** steps: **A**rchive the issue file,
git **A**dd -u, **C**ommit, **P**ush, **D**eploy. This skill's own
script only implements the first four — it's called `aacp.sh`
(`.ps1`/`.bat` too), named after exactly what it does. The fifth step,
Deploy, is **not** this skill's logic: it's each target repo's own
responsibility to provide a deploy entry point. `aacp.sh`'s last step
just looks for one and calls it — it never generates or scaffolds one.
They live in different places:

| | Path | What it is |
|---|---|---|
| This skill's script | `.claude/skills/aacpd/aacp.{sh,ps1,bat}` | What you invoke to run the whole archive→add→commit→push→deploy pipeline |
| Target repo's script (project-provided) | `<target-repo>/deploy-to-dev.{sh,ps1,bat}` (env-specific, no arguments) or `<target-repo>/deploy.{sh,ps1,bat}` (`--env dev`) | The project's own deploy hook, called by the skill's script at the very end, if it exists — `deploy-to-dev.*` takes priority when both are present |

Everywhere below, "this script" / "the aacpd script" means the former.

## Run it

### Explicit issue number — no prompts

```bash
bash .claude/skills/aacpd/aacp.sh <issue-number> <commit-summary...>
```

```bash
bash .claude/skills/aacpd/aacp.sh 42 "KP115 전력 캐시 만료 버그 수정"
```

On a Windows host without bash/WSL, use `aacp.ps1` (native
PowerShell port) or `aacp.bat` (thin dispatcher to `aacp.ps1`) —
same arguments, same behavior. `aacp.sh` is the canonical,
most-exercised implementation; the other two mirror it. See Gotchas.

### No issue number — find what's pending, then ask

When the user says `/aacpd` with no number:

1. Run `bash .claude/skills/aacpd/aacp.sh --pending` to list issue
   numbers whose `## 구현 결과` is already filled in (i.e. `/tdd2`
   finished them) but haven't been archived/deployed yet.
2. If empty: report there's nothing pending. Stop.
3. If one or more numbers: show them, ask the user to confirm
   deploying (compose the commit summary yourself from the issue's
   title / `구현 결과` content), then run the explicit-number form
   above for each confirmed issue.

## What the script does

Run from anywhere inside the target repo — it resolves the repo root
itself.

0. **Lightweight safety check**: verifies the working tree is a git repository (<0.1s).
   All code quality, linting, unit tests, and regression tests are handled by the
   preceding `tdd2` and `code-quality-gate` phases; `aacpd` is purely responsible
   for archive, commit, push, and deploy.
1. Stages `issues/issue-<#>.md` (its own edits, e.g. the `## 구현 결과` section).
   If the issue file has a slug (`issue-N-slug.md`), the script resolves
   it automatically: it tries `issue-N.md` first, then falls back to the
   unique tag-less `issue-N-<slug>.md` match. Fails fast if neither
   exists or if the slug form is ambiguous.
2. Archives it: `git mv` to `issues/archive/YYYY/MM/DD/issue-<#>.md`.
   The original filename (including slug, if any) is preserved as-is —
   "파일명은 그대로" convention (`git log --follow` 이력 추적 보존).
3. `git add -u` — stages the rest of the already-tracked changes. Never touches untracked files.
4. Commits code + archiving as **one commit**, message `issue-<#>: <summary>` with the `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>` trailer appended automatically — don't add it yourself.
5. `git push`.
6. Deploy — **dev only, always**; this skill never touches qa/prod, and
   never generates or scaffolds a deploy script. It just looks for one
   in the target repo, same-platform, in this order:
   - `deploy-to-dev.{sh,ps1,bat}` — already env-specific, so it's run
     with **no arguments**.
   - else `deploy.{sh,ps1,bat}` — run as `deploy.{sh,ps1,bat} --env dev`.
   - else neither exists: deploy is skipped (not a failure) with a
     note telling you to add one. Setting up that script is on the
     **target project**, not this skill — see Gotchas.

Fails fast (`set -e`, exit 1) with no git side effects if
`issues/issue-<#>.md` doesn't exist — check the issue number first,
and ensure code has passed `tdd2` and `code-quality-gate` before calling `aacpd`.

## Verification responsibility

`aacpd` does not duplicate test or linter checks. Quality gates are decoupled
into `tdd2` (targeted tests) and `code-quality-gate` (unified/discovered project checks)
prior to running `aacpd`. This ensures single responsibility and eliminates redundant checks.

## How "pending" is detected

No separate state file. An issue counts as pending-deploy once its
`## 구현 결과` section's `**구현 완료 일시**:` line is no longer the
`(미정)` placeholder — that's the existing issue-template completion
marker, already written by `/tdd2` when it finishes. `--pending` greps
every `issues/issue-*.md` (archived ones are excluded — they live
under `issues/archive/`, a different path) for that signal.

## Gotchas

- **`aacp.ps1` and `aacp.bat` were not run in this environment — no
  PowerShell available here.** `aacp.ps1` is a careful, line-by-line
  manual port of the exercised `aacp.sh` (same steps, same guarantees)
  but hasn't been executed for real; verify it on an actual
  Windows/PowerShell host before relying on it for anything important.
  `aacp.bat` is intentionally thin — it just locates `pwsh` (preferred)
  or `powershell` on `PATH` and forwards to `aacp.ps1`, rather than
  reimplementing ~150 lines of archive/commit/push/gate logic a third
  time in raw batch. It does **not** pass `-ExecutionPolicy Bypass`; if
  your system's execution policy blocks local scripts, set it yourself
  (`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`) or use
  `aacp.sh` under WSL/git-bash instead.
- **The target repo's deploy script is a per-project convention this
  skill never creates.** Deploy is step 5 of `aacpd` in name only —
  it's the one step this skill deliberately doesn't implement. Setting
  up `deploy-to-dev.{sh,ps1,bat}` (no arguments — already env-specific)
  or `deploy.{sh,ps1,bat}` (accepting `--env dev`) in the target repo is
  the target project's job (see the Quickstart in the `autotdd` repo's
  README); `deploy-to-dev.*` takes priority when both exist. If neither
  exists when `aacp` reaches step 6, it prints a note and exits 0 — a
  project with no deploy automation yet doesn't fail the whole merge,
  it just doesn't deploy.
- **Commit message trailer is baked into the script.** Don't pass a
  message that already includes `Co-Authored-By` — you'll get it
  twice.
- **The `<stream>-<N>:` prefix is also baked in.** The script builds
  the commit message itself as `<stream>-<N>: <summary>` (see step 4
  above). `<commit-summary...>` must be **just the summary text** —
  don't pass something that already starts with `issue-<N>:` or you'll
  get it twice (`issue-380: issue-380: ...`). Compose the summary as
  plain description text only.
- **`git add -u` is deliberate, not `git add -A`.** Untracked files
  (scratch files, new files the issue didn't ask for) are never staged
  by this skill.
