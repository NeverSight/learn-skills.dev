---
name: github-copilot-repo-instructions
description: >
  Add, audit, or fix GitHub Copilot repository custom instructions —
  `.github/copilot-instructions.md` (repo-wide) and
  `.github/instructions/*.instructions.md` (path-specific) — so Copilot Chat,
  Copilot code review, and the Copilot coding agent all pick up project-wide
  guidance. Also covers `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` as alternate
  agent instruction files. Use when the user says "add Copilot instructions",
  "set up copilot-instructions.md", "audit our Copilot config", "make Copilot
  follow our conventions", "configure Copilot code review", "add path-specific
  Copilot rules", "applyTo glob", "excludeAgent", "Copilot is ignoring our
  guidance", or invokes /github-copilot-repo-instructions. Do NOT use for
  personal (per-user) Copilot instructions; those are out of scope for this
  skill. For AGENTS.md authoring guidance beyond file layout, see the
  agents-md skill.
license: MIT
---

# github-copilot-repo-instructions

Repository-scoped Copilot guidance. Markdown files in `.github/` that GitHub
Copilot reads on every request against the repo.

> This skill writes and audits repository-scoped instruction files only. It
> does not cover personal (per-user) Copilot instructions, which apply to one
> user's github.com Chat sessions and live outside the repository. For
> AGENTS.md content and structure beyond the file-layout table below, use the
> agents-md skill.

---

## File layout

| File | Scope | Frontmatter | Notes |
|---|---|---|---|
| `.github/copilot-instructions.md` | Repo-wide, every request | None | Single file. Keep ≤ 2 pages. |
| `.github/instructions/<name>.instructions.md` | Path-glob | **Required** (`applyTo`) | Multiple files allowed. Filename must end `.instructions.md`. |
| `AGENTS.md` | Nearest-wins | None | Place anywhere in the tree; the file closest to the edited path wins. |
| `CLAUDE.md` | Repo root only | None | Single file at root. |
| `GEMINI.md` | Repo root only | None | Single file at root. |

The repo-wide file and path-specific files **combine** when a path matches —
both sets of instructions are sent to Copilot together.

---

## Frontmatter (path-specific files only)

```markdown
---
applyTo: "**/*.ts, **/*.tsx"
excludeAgent: "code-review"
---

- Prefer `interface` over `type` for object shapes.
- Use named exports.
```

| Field | Required | Values |
|---|---|---|
| `applyTo` | Yes | Glob pattern, or comma-separated globs (`*.py`, `src/**/*.rb`, `**/subdir/**/*.py`). |
| `excludeAgent` | No | `"code-review"` or `"cloud-agent"` — hides this file from that surface. |

---

## Surfaces

Copilot reads repo instructions across these surfaces:

- **Copilot Chat** — `github.com/copilot` (with repo attached) and IDE chat.
- **Copilot code review** — PR reviews. Toggleable per-repo. Reads from the
  PR's **head branch** (the branch with the changes), not the base branch.
- **Copilot coding agent (cloud agent)** — issue-driven implementations.

Path-specific files (`.github/instructions/*.instructions.md`) are fully
supported on github.com for code-review and the cloud agent. IDE support for
path-specific files lags — repo-wide file is the safer bet for IDE coverage.
See `references/code-review-knobs.md` for the 2025-09-03 change that added
path-scoped instruction support to Copilot code review specifically.

---

## Precedence

When multiple instruction sets exist, all are merged and sent to Copilot.
Stated priority order (highest → lowest):

1. **Personal** instructions (per-user, github.com Chat only).
2. **Repository** instructions (this skill).
3. **Organization** instructions.

Conflicts are not auto-resolved — Copilot sees them all. If quality drops,
temporarily disable a set rather than fighting overlap.

---

## Protocol

### Add repo-wide instructions

1. `mkdir -p .github`
2. Write `.github/copilot-instructions.md`. Markdown only, no frontmatter.
3. Keep it ≤ 2 pages. Whitespace is ignored, so use bullets liberally.
4. Content that pulls weight: stack summary, build/test commands, layout map,
   non-obvious conventions. Skip generic advice Copilot already knows.
5. Commit on a feature branch and open a PR. Code review reads the PR's head
   branch, so the review of that PR uses the new instructions.

### Add path-specific instructions

1. `mkdir -p .github/instructions`
2. Create `<name>.instructions.md` with `applyTo` frontmatter.
3. One file per scope (e.g. `python.instructions.md`, `frontend.instructions.md`).
4. Use `excludeAgent` to keep review-only or coding-agent-only guidance from
   leaking into the other surface.

### Enable Copilot code review

Repo Settings → **Code & automation** → **Copilot** → **Code review** →
toggle **"Use custom instructions when reviewing pull requests"**.

Default is enabled, but confirm — orgs sometimes flip it off.

### Enable automatic Copilot review on every PR

Two paths — pick one. Both create a branch ruleset; the API path is scriptable.

**UI** — Settings → **Rules** → **Rulesets** → **New branch ruleset**.
Under "Branch rules", select **Automatically request Copilot code review**.
Two sub-toggles: *Review new pushes* (re-review on each push, burns premium
requests) and *Review draft pull requests*.

**API** (`gh`) — the rule type is `copilot_code_review`. It is **not** listed
on the [rulesets schema page](https://docs.github.com/rest/repos/rules#create-a-repository-ruleset)
as of writing, but the endpoint accepts it. Targets work like any other ruleset.

```bash
gh api repos/<owner>/<repo>/rulesets -X POST --input - <<'JSON'
{
  "name": "copilot-auto-review",
  "target": "branch",
  "enforcement": "active",
  "conditions": { "ref_name": { "include": ["~ALL"], "exclude": [] } },
  "rules": [
    {
      "type": "copilot_code_review",
      "parameters": {
        "review_on_push": false,
        "review_draft_pull_requests": false
      }
    }
  ]
}
JSON
```

`~ALL` targets PRs to every branch. Use `~DEFAULT_BRANCH` to cover only PRs
that target the default branch.

Defaults shown are conservative: review once on PR open, skip drafts.
Flip `review_on_push` to `true` to re-review on every push — useful for
agentic workflows, expensive on premium-request quota.

Requires Copilot Business/Enterprise on the org, or Copilot Pro for personal
repos. The ruleset still installs without a license; reviews just don't fire.

For the full knob inventory across repo / org / per-PR — including what
Copilot review **cannot** do (no "request changes" mode, no severity
threshold, no API re-request), the removed 4000-character instruction limit,
and path-scoped instruction support — read `references/code-review-knobs.md`.

Any live change made through `gh api` against the rulesets endpoint mutates
repository settings. Show the rendered payload and get explicit user
authorization before sending the request.

### Verify Copilot is reading the file

1. Open `github.com/copilot` and attach the repo.
2. Ask any Copilot Chat question.
3. Expand the **References** list at the top of the response.
4. `.github/copilot-instructions.md` should appear; click to confirm it's the
   version you expect. Path-specific files appear when relevant paths are
   mentioned or attached.

For PR review verification, look at the review comment metadata or trigger a
review on a PR that touches a glob covered by a path-specific file.

---

## Audit checklist

When the user says "audit our Copilot config":

1. `ls -la .github/copilot-instructions.md .github/instructions/ AGENTS.md CLAUDE.md GEMINI.md 2>/dev/null` (silence missing files).
2. Read each present file and check:
   - Repo-wide file ≤ 2 pages.
   - Every path-specific file has `applyTo` frontmatter.
   - Filenames end `.instructions.md` (path-specific only).
   - `excludeAgent` values are exactly `"code-review"` or `"cloud-agent"`.
   - No instructions baked into the repo-wide file that should be path-scoped
     (e.g. "always add type hints" — that's Python-only, hoist it).
3. Check which branch has the current instructions. Code review reads the
   PR's head branch, so a PR sees its own instruction edits. PRs from other
   branches see the edits only after the edits merge into the base and those
   branches merge or rebase from it.
4. Flag conflicts with org-level or expected personal instructions.

---

## Rules

- **Repo-wide file: no frontmatter.** GitHub does not document frontmatter on
  `.github/copilot-instructions.md`. Don't add `applyTo` there.
- **Path-specific file: frontmatter is mandatory.** Without `applyTo` the file
  is ignored.
- **Don't put task-specific instructions in either** ("fix bug X", "do
  refactor Y") — they're long-lived configuration, not ticket scope.
- **Don't duplicate org instructions.** If your org already says "use
  Conventional Commits", don't repeat it at repo level.
- **Code review reads the head branch.** Instruction changes in a PR apply to
  that PR's own review, so you can test them before merge.
- **Don't include secrets, tokens, or internal URLs.** These files are part
  of the repo — anyone with read access sees them.

---

## Gotchas

- A path-specific file with malformed YAML frontmatter is silently dropped.
  Validate frontmatter before committing.
- If a glob isn't matching as expected, prefix with `**/` to cover nested
  paths (`**/*.py` covers nested files; `*.py` may only cover the root,
  depending on the glob engine).
- The IDE may cache instructions; reload the window after editing.
- `AGENTS.md` is recursive — a deeply nested `AGENTS.md` overrides a higher
  one for files near it. Useful, but confusing if the user expects merging.
- `CLAUDE.md` and `GEMINI.md` are *also* read by Copilot now, even though they
  originated as other-vendor files. If you maintain both, expect Copilot to
  see all three.
- Personal instructions take precedence over repo guidance for that one
  user on github.com Chat — symptoms look like "Copilot ignores our rules
  for Alice but works for everyone else". Personal instructions are
  per-user and configured outside the repository; this skill does not
  manage them.
- The repo-wide file's only documented size guidance is "≤ 2 pages". Treat
  that as the ceiling — long instructions crowd out the actual question.

---

## What this skill is not

- Not a setup wizard — it advises and edits existing files, not an
  interview-driven generator.
- Not personal instructions — those are per-user, configured outside the
  repository, and out of scope here.
- Not org-level instructions — those are configured in GitHub Enterprise
  org settings, outside any repo.
- Not AGENTS.md content authoring — use the agents-md skill for that; this
  skill only documents AGENTS.md's place in the file-layout table.

---

## Source

- [Add repository custom instructions for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)
