---
name: upstream-recon
description: >
  Investigate an open-source project before interacting with it — PRs, issues, or comments.
  Use BEFORE: filing an issue, submitting a PR, or commenting on an existing thread.
  Triggers on: "upstream recon", "should I PR this", "will they merge",
  "check the project", "investigate the repo", "PR strategy", "file an issue",
  "check existing issues", "should I comment", or any time the user wants to
  interact with a repo they don't maintain.
  Also use proactively when about to file an issue or PR — checking existing
  threads prevents duplicates and wasted effort.
---

# Upstream Recon

Investigate a repo's culture and existing threads before interacting. Prevents
duplicate issues, wasted PR effort, and uninformed comments.

**Arguments**: `<owner/repo> [topic-keyword]`

## Procedure

Use `gh` CLI throughout. Run independent queries in parallel.

1. **Repo metadata** — stars, forks, license, last push date, archived status
2. **Top 10 contributors** — commit counts. Is it one person with 90%+ commits?
3. **Existing issues search** — search open AND closed issues for the topic keyword.
   Check for duplicates, prior art, and maintainer responses. Report what was found.
4. **Recent 30 PRs** (all states) — get the lay of the land
5. **Merged PRs** (last 20) — who merges them? How fast? What types get accepted?
6. **Closed-without-merge PRs** (last 50, filter `mergedAt == null`) — deep-dive
   2-3 notable rejections: read comments for maintainer reasoning
7. **Open PRs** — how many sit with 0 reviews? For how long?
8. **Topic deep-dive** (if keyword given) — read comments on 2-3 most relevant
   existing issues/PRs to understand maintainer sentiment and community workarounds

## Analysis Dimensions

- **Governance**: Solo maintainer / small team / community-driven
- **External PR reception**: Welcoming / selective (bugs yes, features no) / closed shop
- **Issue responsiveness**: How fast do maintainers respond to issues? Do they engage or auto-close?
- **Merge velocity**: Days from open to merge for external contributors
- **Rejection patterns**: Ghosted? "Building it myself"? "File issue first"? Bot auto-closed?
- **Topic overlap**: Has this been attempted or discussed before? Active workarounds?

## Recommendation

End the report with one of:

- **MERGE-LIKELY** — project merges external feature PRs, no competing work, maintainer receptive
- **MERGE-UNLIKELY** — maintainer builds features themselves, similar PRs closed/ignored, feature contradicts direction
- **FILE-ISSUE-FIRST** — feature not yet discussed, maintainer is selective but responsive to issues, gauge interest before coding
- **COMMENT-ON-EXISTING** — existing issue/PR already covers this, add your workaround or +1 there instead
- **DUPLICATE-EXISTS** — exact issue already filed, do not create another

Include concrete next steps (e.g., "comment on #13738 with your workaround",
"start with a bug fix PR to build credibility", "file an issue referencing #189",
"fork and maintain independently").
