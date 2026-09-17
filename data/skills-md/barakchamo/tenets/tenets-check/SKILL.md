---
name: tenets-check
description: |
  Audits a repository's tenets project guide for completeness, staleness, quality bars, valid rule
  anchors, and template version, and reports a pass/fail checklist with a fix list.

  Use only when the user explicitly asks to check or audit the project guide, or runs /tenets-check
  — including after refactors that change commands or workspaces, or when upgrading the ruleset. Not
  for auditing code against the rules: that is tenets-audit.
disable-model-invocation: true
allowed-tools: Read Glob Grep Bash(git ls-files:*)
metadata:
  version: '1.0.0'
  requires: 'tenets >= 2.0.0'
---

# Tenets check

Audit this repository's tenets project guide. Read `<ruleset>/templates/project-guide.md`
for comparison; if that path does not resolve, stop: `State: BLOCKED — install the tenets ruleset
skill`.

Locate it via `tenets.json`'s `guide` field at the repository root, else the `Project guide:` line
in AGENTS.md/CLAUDE.md, else the default `docs/project-guide.md`; missing guide → report that and
suggest `/tenets-init`.

## Locate the ruleset

`<ruleset>` below is the `tenets` skill directory installed beside this one — **not** a path
relative to the working directory. Resolve it once, in this order, and use it for every path after:
`.claude/skills/tenets/`, `.agents/skills/tenets/`, then a glob for `**/skills/tenets/SKILL.md`
outside `node_modules`. Nothing found → stop: `State: BLOCKED — install the tenets ruleset skill
(skills add BarakChamo/tenets --all)`.

## Checks

1. **Structure:** every template heading present (compare against `templates/project-guide.md` in
   the `tenets` skill); `Template-Version` stamp matches the skill's
   `metadata.template-version` — mismatch means re-run `/tenets-init` against the new template.
2. **Freshness:** every command in the guide exists in the root manifest; every workspace in the map
   exists; primitive and store locations resolve; the stated test runner and suffixes match real
   test files.
3. **Profile:** `tenets.json`'s `profile` (default `typescript`) resolves to a
   `profiles/<name>.md` file in the skill, matches the repository's actual language, and every
   anchor it waives or appends to exists in the rule files. Flag guide content the profile already
   fixes (strictness settings, doc tags, test declaration form) as duplication.
4. **Quality bars:** each section satisfies its QUALITY BAR from the template; the guide stays under
   ~600 words; no section restates what code, README, or rules already say.
5. **Anchors:** every `Rule N.M` cited by the guide exists in the ruleset's rule files, and so does
   every anchor cited by an installed `tenets-*` workflow skill — a stale anchor in a workflow skill
   produces confident findings against a rule that no longer says that.
6. **Deviations:** the section is present and explicit (`none recorded` counts); flag any known
   divergence between repo practice and the rules that is not recorded there.

Report findings as a checklist with pass/fail per check and a fix list, most severe first. Apply
fixes only when asked.
