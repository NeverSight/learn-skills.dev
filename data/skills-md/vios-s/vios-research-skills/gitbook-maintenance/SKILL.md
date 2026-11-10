---
name: gitbook-maintenance
description: Use this skill when maintaining the Vios Research Skills library structure — adding new skills, updating SUMMARY.md, fixing frontmatter, or helping contributors follow the skill template. Triggers include "add a new skill to the library", "update the skills library", "scaffold a new skill", "fix SUMMARY.md", "check skill frontmatter", "how do I contribute a skill", or "help me write the frontmatter for my skill". Do not use for writing the research content of skills — this skill is about library structure and contributor tooling only.
license: MIT
metadata:
  category: "Community & Infrastructure"
  version: "0.1.0"
  author: "VIOS Lab, University of Edinburgh"
---

# GitBook Maintenance

A skill for maintaining the Vios Research Skills library — scaffolding new skills, keeping `SUMMARY.md` in sync, and ensuring the GitHub ↔ GitBook two-rail architecture stays healthy.

## When to invoke this skill

- A lab member wants to add a new skill and needs the correct file structure
- `SUMMARY.md` is out of date after a new skill was merged
- A skill fails the CI frontmatter lint and needs to be fixed
- The GitBook sidebar is not showing a skill or is showing it in the wrong section
- You want to understand the contribution workflow before opening a PR

## The two-rail architecture (recap)

```
GitHub (source of truth) ──── git push ────▶ GitBook (human UI)
     ▲                                              │
     └──────────── GITBOOK-N commit ────────────────┘
```

- **Skills live at** `skills/<name>/SKILL.md` — both Agent Skills installers and GitBook read from here.
- **GitBook writes to** `skills/` only (constrained by `.gitbook.yaml`). It does not touch `scripts/`, `.github/`, or `CONTRIBUTING.md`.
- **`SUMMARY.md` is managed by** `scripts/generate_summary.py`. Never edit it by hand; never create pages in the GitBook UI (that bypasses the generator and will break CI).

## Workflow: adding a new skill

### Step 1. Choose a name and category

- Name: `kebab-case`, matches the folder name exactly.
- Category: one of the valid categories listed in CONTRIBUTING.md.
- Check that no existing skill already covers the same trigger — use `npx skills list` to browse.

### Step 2. Scaffold the file

```bash
mkdir skills/<your-skill-name>
```

Create `skills/<your-skill-name>/SKILL.md` using this exact template:

```markdown
---
name: your-skill-name
description: Use this skill when [trigger]. Triggers include "[example 1]", "[example 2]". Handles [scope]. Do not use for [out-of-scope].
license: MIT
metadata:
  category: "<one of the valid categories>"
  version: "0.1.0"
  author: "Your Name, VIOS Lab"
---

# Human-Readable Title

One-paragraph intro for GitBook readers (human-facing).

## When to invoke this skill

[Triggers and counter-triggers.]

## Workflow

[Numbered or structured steps.]

## Anti-patterns

[What NOT to do.]

## See also

[Cross-references to related skills.]
```

### Step 3. Validate locally

```bash
pip install pyyaml          # once only
python scripts/lint_skills.py
python scripts/generate_summary.py   # regenerates SUMMARY.md
python scripts/generate_summary.py --check   # verify
```

All three must pass before committing.

### Step 4. Open a PR

```bash
git checkout -b skill/<your-skill-name>
git add skills/<your-skill-name>/ skills/SUMMARY.md
git commit -m "Add <your-skill-name> skill (Category: <category>)"
git push -u origin skill/<your-skill-name>
gh pr create --base main
```

CI will run `lint_skills.py` and `generate_summary.py --check` on the PR. Both must be green before merging.

## Troubleshooting

**Skill appears in GitHub but not GitBook sidebar:**
1. Check `skills/SUMMARY.md` — is the skill listed?
2. Check the GitBook space settings — has a sync been triggered?
3. Check `.gitbook.yaml` — `root: ./skills/` and `structure.summary: SUMMARY.md` must be present.

**CI fails with "SUMMARY.md is out of date":**
```bash
python scripts/generate_summary.py   # regenerate
git add skills/SUMMARY.md
git commit -m "Regenerate SUMMARY.md"
```

**CI fails with frontmatter lint errors:**
Common issues:
- `description` shorter than 100 characters — expand it
- `description` does not start with "Use this skill" — fix the opening phrase
- `name` does not match folder name — rename one or the other
- `metadata.category` is not one of the valid values — pick from the list in CONTRIBUTING.md
- `unexpected top-level field(s)` — only `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools` may sit at the top level (Agent Skills spec); move `category`, `version` and `author` under `metadata:`

**GitBook committed a file that changed SUMMARY.md format:**
GitBook should not modify SUMMARY.md (it is managed by the generator script). If it does:
```bash
git pull origin main
python scripts/generate_summary.py
git add skills/SUMMARY.md
git commit -m "Restore SUMMARY.md to generator-managed format"
git push origin main
```

**GitBook created a new page (new folder/file) via the UI:**
This bypasses the PR flow and will cause CI to fail on the next developer push (SUMMARY.md will be missing the new entry in the generator's format). To fix:
1. Pull the GitBook commit.
2. Run `python scripts/generate_summary.py`.
3. Add `category:` and fix frontmatter if missing.
4. Commit and push.
Remind the contributor to use GitHub PRs for new skills going forward.

## GitBook editing constraints

When editing existing skills via the GitBook UI:
- **Do** edit text content freely — it syncs to GitHub as a `GITBOOK-N: ...` commit.
- **Do not** use GitBook-specific blocks in SKILL.md files: `{% hint %}`, `{% tabs %}`, `{% stepper %}` etc. are GitBook-only syntax and will appear as raw text when an AI agent reads the file.
- **Do not** rename pages or create new pages via the GitBook UI — this changes file paths and breaks installer references.
- **Do not** edit frontmatter via GitBook's raw editor unless you understand the lint requirements — broken frontmatter will fail CI silently until the next push.

## See also

- `CONTRIBUTING.md` for the full contributor workflow.
- `FORKING.md` for setting up a private fork of this library.
- `arxiv-digest` and `literature-review` as reference examples of well-formed skills.
