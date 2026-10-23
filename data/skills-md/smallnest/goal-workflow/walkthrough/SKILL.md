---
name: walkthrough
description: "Generate a Phase-2 Walkthrough artifact (walkthrough.md) once implementation and verification are complete. Captures a Change Summary, Verification Steps (commands + unit tests + automated browser testing outcomes), Visual Proof (screenshots/recordings embedded directly in the file), and a Review Gate (final diff + PR description for a Git staging-check) so you can catch up on what changed and what's proven to work before merging. Saves to tasks/walkthrough-[feature].md by default. Triggers on: /walkthrough, walkthrough, Phase 2 walkthrough, 生成 walkthrough, 生成走查文档, write the walkthrough."
user-invocable: true
# 本 skill 必须执行项目自己的测试/lint 命令去取真实证据，而命令因项目而异，故不限定 Bash 前缀。
allowed-tools:
  - Bash
metadata:
  author: smallnest
  version: 1.1.0
---

# walkthrough — Phase 2: The Walkthrough Plan

Once the agent finishes **execution** and **verification**, it outputs a walkthrough artifact: a single Markdown file that lets you quickly catch up on **what was changed** and **what is proven to work**, and lets you do a **staging-check with Git** before merging.

This is modeled on Google Antigravity's walkthrough plan: the agent is expected to prove the change works (unit tests + real browser behavior), capture visual evidence, and hand you a review gate — not just dump a diff.

## When to use

- After `/goal` (or any implementation) plus its verification pass are complete — e.g., after `/review-it` / `/verify` / manual testing
- Before `/ship-it`, as the last checkpoint before commit/PR/merge
- User says "walkthrough", "生成 walkthrough", "生成走查文档", "write the walkthrough", "/walkthrough", "Phase 2 walkthrough"

## The Job

1. **Determine the change scope** — which feature / Issue / branch is being walked through, and **which repos** it spans
2. **Write the plain-language opening** — before/after + why, readable by someone who has never seen the code
3. **Write the Change Summary** — the technical detail, for whoever will read the diff next
4. **Run and record Verification Steps** — execute the tests and commands, capture real output, **label each claim's provenance**
5. **Capture Visual Proof** — screenshot / record the UI behavior you verified
6. **Build the Review Gate** — stage-check the diff with Git, draft the PR description, spell out deploy-order prerequisites
7. **Save to `tasks/` and present** — write `walkthrough-[feature].md`, render it to HTML, summarize for the user

## Section-by-section

### 1. 先说人话 / Plain-language opening (读前必读)

The first thing in the file. A PM, QA, a neighbouring team, or you in three months must be able to read **only this section** and know what changed and why they should care.

Required content:

- **Before / after**, concretely — what the caller/user sees, not what the code does:

  | | 改之前 | 改之后 |
  |---|---|---|
  | {用户/调用方看到什么} | {old behaviour} | {new behaviour} |

- **Why it changed** — 2–3 reasons in plain words. If you cannot state a reason without naming a class, a flag, or a table, you do not understand the change well enough to write this section.
- **What the reader must do differently**, if anything (call a new endpoint, run a migration, change the client).

Rules:

- **Never open with an identifier.** `dryRun`, `draft_id`, `PriorityResolver` are not explanations. Introduce the concept in plain words first, name it second.
- A sentence like *"X 从「A」改为「B」"* is banned unless A and B are **both** explained in plain words.
- If the change has a user-visible effect, describe it from the user's side.

```markdown
BAD  (技术上没错，但读的人解不开)
> 把优先级的写入时机从「即时落库」改为「先返回 draft_id、确认后落库」

GOOD (同一件事)
> 用户改任务优先级时，以前客户端发一次就直接写进数据库；现在后端先把可选的优先级算出来
> 让用户挑一个，挑完才写。用户没挑就不写。
```

### 1b. Glossary — only if the doc uses internal jargon

If the doc uses **any** of: internal flag/field names (`dryRun`), numeric interface ids (`1001`), domain terms an outsider can't decode (「归一化」「草稿」), or module names not inferable from the file tree — add a two-column mapping from *the doc's wording* to *plain language*.

```markdown
| 文中说法 | 说人话 |
|---|---|
| `dryRun` | 开关：`true` = 只算不写，不传 = 老行为 |
| 「草稿」 | 算出来、还没落库的中间结果 |
```

- Do **not** gloss standard terms (HTTP, SQL, PR) — that reads as padding.
- Pay special attention to **pairs that look alike but mean different things**. If two similarly-named concepts are easy to confuse, say so explicitly in the table — that is where readers actually get lost.

### 2. Change Summary

The technical description, for a reader who is about to open the diff. This is where identifiers belong — the plain-language section already paid for them.

- Read the diff (`git diff`, `git log`) and the Issue/PRD it serves
- Summarize in 3–6 bullets: what was built, refactored, added, or removed
- List the key files and components, and the shape of what's new (modules, pages, APIs, data structures)
- State the requirement it satisfies and link the Issue / PRD if present

### 3. Verification Steps

Proof that the implementation actually works — evidence, not assertion. Record **what you ran and what it output**.

- **Terminal commands & unit tests**: run the test suite (or the targeted tests), lint/build, and any smoke commands. Paste the exact command and its successful output (truncate noise, keep pass counts).
  ```bash
  go test ./... -run TestPriority
  ```
  ```
  ok  	github.com/example/app 0.042s
  ```
- **Automated browser testing outcomes** (if the change has UI): open the app in a sandbox/headless browser, click through the demo path, and record the outcome. For each scenario: the action performed, the observed result, pass/fail.
  ```
  Scenario: user sets a task's priority
    1. open /tasks — renders list
    2. click priority select on task #3 → pick "High"
    3. reload — task still shows High  ✓
  ```
- If a step was skipped (no tests, no UI), say so explicitly — don't invent evidence.

**Label the provenance of every claim.** Three levels, and say which one applies:

| Label | Means | Example |
|---|---|---|
| **已实测** | You ran it, you have the output | `95 PASSED / 0 FAILED` |
| **代码推断** | Read from the code or a unit test, **not executed** | 「没有优先级时回落 normal」（`PriorityResolverTest` 里有对应用例，但没跑） |
| **未验证** | Neither — and it must be said out loud | 「本机无数据库/缓存/外部服务，服务级行为未在本环境验证」 |

Never present 代码推断 or 未验证 as if it were 已实测. A walkthrough that overstates its evidence is worse than one with gaps, because the gaps are what the reader would have checked.

**Record how you made the command run at all.** If it needed a workaround — offline mode, a config override, an init script, a narrowed test filter — record it, otherwise the reader cannot reproduce your evidence.

```bash
./gradlew test --offline --rerun -I /tmp/no-failfast.gradle \
  --tests "com.example.tasks.*" --console=plain
# 依赖仓库在本机不可达，必须加 --offline；构建脚本设了 failFast=true，
# 不覆盖的话第一条失败就停，看不到完整清单
```

Also record a **baseline caveat** whenever the runner's defaults would mislead: `failFast` hiding later failures, a test cache replaying stale results (`--rerun`), a suite that is already red before your change.

**If the broader suite is red, trace every failure — do not write "unrelated".** For each one, give:

- the file/class, the commit that last touched it, and its date
- whether that commit is an **ancestor of your base** (→ pre-existing)
- whether it falls **inside your own commit range** (→ yours)

```markdown
| 失败用例 | 所属类最后修改提交 | 是 base 祖先？ | 在本分支提交内？ |
|---|---|---|---|
| `PriorityResolverTest > defaultsToNormal()` | `1a2b3c4d` 2026-01-15 | 是 | 否 |
```

A failure traceable to a commit **before your base** is pre-existing — say so **with the hash**, so the reader can re-check. A failure inside your range is yours, however unrelated it looks.

### 4. Visual Proof

Screenshots or short screen recordings captured during browser testing, **embedded directly into the file** so it renders anywhere (GitHub, VS Code, browser).

- **Screenshots**: capture during the browser walkthrough above. Embed as base64 data URIs for a fully self-contained file (recommended):
  ```markdown
  ![Task priority — set to High](data:image/png;base64,<base64>)
  ```
  On macOS you can capture a window with `screencapture`; for web pages prefer browser automation tooling (e.g. Playwright: `npx playwright screenshot <url> tasks/shot.png`, then read the PNG and embed it).
- **Recordings**: if you captured a screen recording, note its path and link it in the file (`![Demo](tasks/recording-demo.mov)`).
- Prefer 2–4 focused screenshots that prove the demo path (before → action → after), not a screenshot dump.
- If the change has no visual surface, write "None — change is backend/CLI only" rather than forcing a screenshot.

### 5. Review Gate

The final diff / PR description where you (or the user) staging-check the code with Git before merging.

- **Diff stat + file list**: `git status`, `git diff --stat HEAD`, `git diff --name-status`
- **High-risk notes**: call out force-pushed history, migrations, config changes, wide refactors, submodule pointer bumps
- **Deploy-order prerequisites** (required whenever the change ships a DDL / migration / config key / feature flag) — state (a) exactly what must be applied, (b) **how** (manual vs automatic), (c) **the failure mode if the order is wrong**:

  ```markdown
  > `0042-add-priority-to-tasks.sql` 给 `tasks` 表加 `priority` 列。
  > **不会被任何 compose 自动执行**（唯一挂载的 initdb 目录指向的是另一个路径），
  > 必须手工应用到所有环境。实体已映射该列且 ddl-auto=none →
  > 代码先上线会让**每一次** Task 查询抛 SQLGrammarException，
  > 即整个服务的任务查询全挂，而非仅新功能不可用。
  ```

  "记得跑一下 migration" is not enough. The reader needs the blast radius, because that is what determines whether they schedule it carefully or wing it.
- **Draft PR description**: a ready-to-paste PR body (summary, test plan, `Closes #N`), mirroring `/ship-it`
- **Merge checklist**: confirm tests green, review pass done, no stray artifacts in `git status`, commit messages reference the Issue

**Multi-repo changes.** If the work spans more than one repo:

- one file list + verification section **per repo**, each with its own branch state (local == remote? pushed? PR open?)
- state explicitly that the branches **must merge together**, and what breaks if only one lands
- verify each repo's checkout individually. **A repo you did not open is not a repo you verified** — do not conclude "the other half isn't implemented" from a single checkout; the same repo often exists at several paths on different branches.

## Output

Two files, same basename:

| File | Role |
|---|---|
| `tasks/walkthrough-[feature-name].md` | **Source.** What you author and edit. Kebab-case, e.g. `walkthrough-priority-system.md` |
| `tasks/walkthrough-[feature-name].html` | **Deliverable.** What you hand to a reviewer. Generated from the `.md`, never hand-edited |

The HTML is **not optional** — it is the artifact people actually read. It is light-themed
(warm off-white, serif headings, terracotta accent), self-contained (no CDN, no external
assets), and carries a **fixed table-of-contents sidebar on the left** built from the
document's `h2`/`h3`.

Render it with the script bundled with this skill:

```bash
python3 scripts/md2html.py tasks/walkthrough-[feature-name].md
# or, once installed:
python3 ~/.claude/skills/walkthrough/scripts/md2html.py tasks/walkthrough-[feature-name].md
```

- Writes `walkthrough-[feature-name].html` beside the input; pass a second path to override.
- `--title "…"` overrides the page title (default: the document's `# H1`).
- Needs the `markdown` package: `python3 -m pip install --user markdown`. If it is missing the
  script exits with that instruction — relay it, do not silently skip the HTML.
- Embedded `data:` image URIs pass through untouched, so Visual Proof screenshots survive.
- **Re-render after every edit to the `.md`.** A stale HTML beside an updated Markdown is
  worse than no HTML: the reviewer reads the stale one.

If the user passes a name (`/walkthrough user-auth`) or an Issue number (`/walkthrough #42`), use that. If the current branch is `feat/issue-42-*` or `feat/priority-system`, derive the feature name from it. Otherwise ask.

## Template

````markdown
# Walkthrough — {Feature / Issue Title}

> Phase 2 walkthrough artifact · generated {date} · {author}
> {跨哪几个仓 / 分支名，若只有一仓则省略}

## Change Summary

### 先说人话：这次到底改了什么

{2–4 句，不含任何标识符。改之前什么样、改之后什么样。}

| | 改之前 | 改之后 |
|---|---|---|
| {用户/调用方看到什么} | {old behaviour} | {new behaviour} |

{为什么改，2–3 条大白话。}
{读的人需要做什么不同的事吗？}

### 术语表

| 文中说法 | 说人话 |
|---|---|
| {identifier / 数字接口号 / 领域词} | {plain meaning} |

### 技术摘要

{2–4 sentence high-level description — 到这里才允许出现标识符}

- {bullet: what was built/refactored/added/removed}
- {key files, components, pages, APIs}
- {requirement satisfied — link Issue/PRD}

## Verification Steps

### Terminal commands & unit tests

```bash
{exact command, including any workaround needed to make it run}
```
```
{actual output — pass counts, ok lines}
```

**provenance:** {已实测 / 代码推断 / 未验证} — {对每条重要结论标注}
{若跑不了：本机缺什么（DB/Redis/外部服务），因此哪一层未被验证}

{若更宽的测试面是红的，逐条列表并给出「是 base 祖先吗 / 在本分支内吗」}

### Automated browser testing

| # | Scenario | Action | Observed result | Status |
|---|----------|--------|-----------------|--------|
| 1 | {demo step} | {clicks / inputs} | {what happened} | ✅ / ❌ |

## Visual Proof

![{caption}](data:image/png;base64,{base64})

_{or: None — change is backend/CLI only}_

## Review Gate

```bash
git status
git diff --stat HEAD
git diff --name-status
```
{output}

### High-risk notes

{force-pushed history / migrations / config / submodule bumps}

**部署顺序前置** {仅当涉及 DDL / migration / 配置项 / 开关}
- 要应用什么：{文件路径}
- 怎么应用：{手工 / 自动；若「不会被任何东西自动执行」就直说}
- **顺序错了会怎样**：{blast radius，不是「功能不可用」而是「什么会一起挂」}

### Draft PR

{ready-to-paste PR body — Summary / Test plan / Closes #N}

### Merge checklist

- [ ] Unit tests / build pass (evidence in Verification Steps)
- [ ] Browser testing done where UI changed (evidence in Visual Proof)
- [ ] Review pass complete (/review-it)
- [ ] No stray artifacts in `git status`
- [ ] Commit messages reference the Issue
- [ ] 每条结论都标了 provenance（已实测 / 代码推断 / 未验证）
- [ ] 若有更宽测试面的红，逐条追溯到 commit 并说明是否在本次范围内
- [ ] 部署顺序前置已写清（含 blast radius），若有
- [ ] 多仓时：每个仓各自的文件清单/证据/分支状态都齐了
````

## Determining the feature name

1. If the user provides it (`/walkthrough user-auth`), use it
2. If on a branch `feat/issue-42-*` / `feat/priority-system` / `fix/issue-42-*`, derive from the branch (strip the `feat/` prefix and issue number)
3. If a PRD/SPEC exists in `tasks/` (`prd-*.md`, `spec-*.md`), reuse its feature name
4. Otherwise ask: "What feature name should the walkthrough use?"

## Edge cases

| Scenario | Handling |
|----------|----------|
| No changes detected (`git diff` empty, nothing new) | Say so plainly; do not fabricate a walkthrough |
| No tests exist | Note "no automated tests in repo" and rely on manual/browser verification evidence |
| Change has no UI | Visual Proof = "None — backend/CLI only"; browser-testing section marked N/A |
| Screenshot embedding fails | Fall back to `tasks/*.png` relative paths and note the files to commit alongside |
| `tasks/` directory missing | Auto-create it |
| Walkthrough already exists for this feature | Ask: update in place or overwrite? default = overwrite (fresh snapshot) |
| Verification couldn't be completed | Record it as a blocker in the Review Gate — never mark unverified work as proven |
| Broader test suite is red | Trace each failure to a commit (ancestor of base?) before writing anything. "unrelated" without a hash is not evidence |
| Change spans multiple repos | One section per repo + explicit "must merge together"; check each checkout — a repo you didn't open isn't verified |
| Change ships a DDL / migration / flag | Deploy-order prerequisite with blast radius is mandatory |
| Only part of the change is testable locally (no DB/Redis/external service) | Say which layer is unverified **in this environment**; a doc that overstates evidence is worse than one with declared gaps |
| Doc is heavy with internal identifiers | Add the plain-language opening + glossary. If the opening paragraph contains a flag name, it isn't written yet |
| `markdown` package not installed | Relay the script's install hint (`python3 -m pip install --user markdown`); do not silently skip the HTML |
| Markdown edited after rendering | Re-run the renderer. Never leave a stale `.html` next to a newer `.md` |
| Document will be shared outside the team / into a public repo | Replace every repo-specific example (paths, class/table/column names, commit hashes, internal hosts) with a neutral one **before** writing |

## Relationship to other skills

```
/goal → /review-it → /note-it → /walkthrough → /ship-it
   │         │           │           │             │
 execute   find/fix   rationale   proven +      commit + PR
                                  review gate
```

- **/review-it** — fixes issues and confirms the change is sound; walkthrough assumes this (or equivalent) already ran
- **/note-it** — captures design rationale per Issue; walkthrough captures proof + summary, complementary
- **/understand** — explains what new code does; walkthrough is the formal artifact you hand to a reviewer
- **/ship-it** — consumes the walkthrough: the Review Gate's draft PR and checklist feed straight into it

## Checklist

Before saving:

- [ ] **Plain-language opening exists** and contains **no identifiers** — a non-engineer can read it standalone
- [ ] It says what changed **before vs after**, and **why**
- [ ] Glossary present if the doc uses internal ids / flags / domain jargon; confusable concept pairs called out
- [ ] Change Summary is written for a fresh reader (not a diff dump)
- [ ] Every Verification Step shows the actual command + actual output
- [ ] Where the command needed a workaround to run, that's recorded
- [ ] Every claim labelled 已实测 / 代码推断 / 未验证
- [ ] Red tests on the broader suite traced to a commit (hash + is-it-before-base), not hand-waved as "unrelated"
- [ ] Browser scenarios recorded with pass/fail outcomes, where UI exists
- [ ] Visual Proof embedded (base64) or explicit "None"
- [ ] Review Gate shows `git status` / `git diff --stat` + draft PR + merge checklist
- [ ] Deploy-order prerequisites + blast radius, if the change ships a migration/config/flag
- [ ] Multi-repo: every repo has its own file list, evidence, and branch state
- [ ] Unverified claims are marked as unverified — nothing invented
- [ ] Saved to `tasks/walkthrough-[feature-name].md`
- [ ] **Rendered to `.html`** and re-rendered after the last Markdown edit (left TOC sidebar present)
- [ ] No repo-internal specifics leaked into examples if this document is destined for a shared/public place
