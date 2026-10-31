---
name: finding-on-github
description: If you are now working with an open source project while I'm not a maintainer or author

  Load this skill when I ask things like `is there a bug?` and when you sense I am willing to contribute to it, or when I am confirming whether there is a problem. Load this skill when you are modifying an existing feature without a certain reason
---

# Finding on GitHub

Your job is to **prevent meaningless work** for both the user and agents. Before touching any code, investigate the history and community activity around the issue. Feel free to stop me if the work is already done or in progress.

Use `git` and `gh` CLI as your primary tools.

---

## Step 1 — Check if the behavior is intentional

Use `git blame` to find who last changed the relevant code, then trace the commit:

```bash
git blame <file> -L <line>,<line>
git show <commit-hash>
```

Search for related commits and PRs linked to that change:

```bash
gh search commits "<keyword>" --repo <owner>/<repo>
```

**Goal:** Determine whether this is a known intentional decision or an actual bug.

---

## Step 2 — Search existing Issues

Search for anyone who has already reported the same problem or requested the same feature:

```bash
gh issue list --repo <owner>/<repo> --search "<keyword>" --state all
```

Read through the top matches. If you find a relevant issue:

- Summarize what was discussed
- Note the current status (open, closed, won't fix, etc.)
- **If someone is actively working on a fix — stop me and report it**

---

## Step 3 — Search existing Pull Requests

Check if a fix or implementation is already in progress:

```bash
gh pr list --repo <owner>/<repo> --search "<keyword>" --state all
```

If an open PR addresses the same problem — **stop me and link it**. There is no point duplicating effort.

If you loaded this skill and did this inspect, leave a simple line in your response to make sure I can work on it.
