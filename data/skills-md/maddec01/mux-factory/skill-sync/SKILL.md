---
name: skill-sync
description: Review upstream changes to the skills copied into mux-factory and take the ones Pedro picks. Use when the user runs /skill-sync.
disable-model-invocation: true
---

The copied skills in `maddec01/mux-factory` change only through this skill.
`UPSTREAM.md` records the upstream commit each copy matches.

1. Work in a fresh branch `chore/skill-sync-<date>` of the mux-factory checkout
   (`~/Developer/Mux/mux-factory`), updated from `origin/main`.
2. Run `bash <this skill>/scripts/upstream-changes.sh <checkout>`. It prints, per
   copy, whether upstream changed since the recorded commit, the upstream commits
   and the diff.
3. For each changed copy, summarise in two or three lines what changed and what
   it would do to the factory, and give your recommendation (take, skip, or take
   part). Ask Pedro to pick, using numbered questions so he can answer in one
   message. Ask whether he wants any new upstream skills copied too.
4. Apply exactly what he picked: copy the upstream files over the copy (or apply
   the chosen hunks), and set that row's commit in `UPSTREAM.md` to the upstream
   commit you took. A skipped change keeps the old commit, so it shows up again
   next time; say so.
5. Commit as `chore(skills): sync <names> from upstream`, push, and open a PR
   listing what was taken and skipped. Pedro merges it.
6. Tell him to pull `main` after merging and run `bash scripts/install.sh`. It
   updates the skills and the checklists in `references/`.

Never edit a copy for Mux reasons. Mux rules belong in `mux-work` or a repo's
`AGENTS.md`.
