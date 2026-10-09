---
name: github-readme-maintenance
description: github-readme-maintenance — Maintain GitHub repository docs (README, wiki-like community guides, contributor-facing indexes) with deterministic, low-noise workflows.
version: 1.1.0
author: Hermes Agent
license: MIT
platforms:
- linux
- macos
- windows
metadata:
 hermes:
 tags:
 - GitHub
 - Documentation
 - README
 - Repositories
 - Merge Workflow
 related_skills:
 - github-auth
 - github-repo-management
 - github-pr-workflow
---
# GitHub README and Documentation Maintenance

Use this skill for edits where the goal is to keep repository-facing Markdown documentation accurate, current, and review-friendly.

## Scope

Apply this skill when editing:

- `README.md` and similar top-level docs
- `AGENTS.md`, `CLAUDE.md`, and other agent-facing repository guidance
- Community megathread catalogs or link indexes
- Repository runbooks, contribution guidance, and operational playbook docs

For agent-facing guidance, document stable architecture, ownership boundaries, generated-file rules, safety invariants, and executable verification commands. Do not copy temporary campaign state, process IDs, review generations, or acceptance SHAs into durable repository instructions.

## Operating assumptions

- You may be working in a repository that exists in more than one local checkout.
- The expected change is usually a small, localized edit.
- The safest path is to treat target path/branch as explicit inputs.

## Canonical workflow

1. **Pin the target repository path and branch first**

 ```bash
 TARGET_REPO=/path/to/repo
 git -C "$TARGET_REPO" remote -v
 git -C "$TARGET_REPO" rev-parse --abbrev-ref HEAD
 git -C "$TARGET_REPO" status --short
 ```

 - If you have multiple local clones, verify all candidates before editing.

2. **Verify target file and section context before changing anything**

 ```bash
 git -C "$TARGET_REPO" ls-tree -r --name-only HEAD -- README.md megathreads | sed -n '1,120p'
 git -C "$TARGET_REPO" show origin/main:README.md | sed -n '1,120p'
 ```

 - Confirm the file exists in the working HEAD and that the section you plan to modify is in the expected place.

3. **Ground architectural guidance in the accepted implementation**

 - Inspect the current agent guide, final accepted commits, production entry points, generated artifacts, and canonical package scripts before writing.
 - Reconcile counts and names mechanically when possible (for example, parse the generated tool-schema JSON rather than counting a long list by eye).
 - Name the authoritative source and generated outputs separately. State “do not edit generated files directly” only when the repository actually provides a regeneration path.
 - Convert completed feature work into stable class-level guidance: architecture, trust boundaries, default-off/fail-closed behavior, lifecycle ownership, and the commands future agents must run.
 - Keep historical implementation milestones and one-time acceptance evidence out of `AGENTS.md`; link to a durable design or evidence document if history is genuinely needed.

4. **Edit minimally, with explicit list/link formatting rules**

 - Keep Markdown bullets as plain list syntax (`- item`).
 - Keep link text and relative paths consistent with surrounding style.
 - Avoid broad refactors for single-link updates.

5. **Validate the edit before finalizing**

 ```bash
 git -C "$TARGET_REPO" diff -- README.md
 ```

 - If the file is `README.md`, ensure only intended lines changed.
 - If formatting drift is detected, fix it before creating a PR.
 - For requests to remove screenshots, photos, badges, or diagrams "from the page," remove the Markdown/HTML references first. Do not delete the underlying asset files unless the user explicitly asks to remove them from the repository or they are confirmed unused everywhere.

5. **Publish and verify the rendered result when requested**

 - Before publication, recheck the exact checkout, branch, HEAD, Git locks, and absence of another writer.
 - For a deletion-only documentation diff, confirm no added lines exist; this tightly bounds new credential and local-identifier risk while preserving the repository's normal publication gates.
 - After pushing, verify the remote branch SHA matches the local commit.
 - Read the raw remote README and confirm the removed references or section text are absent.
 - Fetch the public repository page to confirm GitHub renders the new commit, then wait for that exact commit's required CI checks when present.
 - If push output and an independent remote-SHA comparison both prove success, a credential-helper warning that only affects storage/readback is not a failed publication. Escalate only if authentication or remote verification failed.

6. **Prepare handoff output**

 - Report exact files changed.
 - State whether assets were merely unreferenced or actually deleted.
 - Report the verified commit/link and CI result when publication was in scope.
 - Report whether change scope is minimal and cleanly reviewable.

## Common pitfalls

- **Wrong checkout edits:** editing the same repo from a secondary clone can produce unlinked commits and confusing diffs.
- **Unverified paths:** adding a missing/nonexistent link target in a README undermines trust more than no change.
- **List corruption:** an accidental `|-` or similar table-row fragment can hide in a diff and break section structure.
- **Scope creep:** avoid adding unrelated docs or formatting cleanup during a targeted link update.

## Verification checklist

- [ ] target path, remote, and branch confirmed
- [ ] target section and path verified in working tree and upstream snapshot
- [ ] final diff scoped to intended doc change
- [ ] markdown structure still consistent with surrounding sections
- [ ] changes ready for PR review with no unrelated churn

- General README/session checklist:
- Post-feature `AGENTS.md`/`CLAUDE.md` architecture refresh:
