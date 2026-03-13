---
name: gh-fetch
description: Use the GitHub CLI to fetch content from GitHub URLs instead of web fetching. Activate when the user shares a GitHub issue, PR, repo, or discussion link.
---

# GitHub URL Handling

When the user shares a GitHub URL (issue, PR, repo, discussion, etc.), always use the `gh` CLI to fetch its content rather than web fetching or browsing.

Parse the owner, repo, and number from the URL, then use the appropriate command:

| URL type | Command |
|----------|---------|
| Issue | `gh issue view <number> --repo owner/repo` |
| Pull request | `gh pr view <number> --repo owner/repo` |
| PR diff | `gh pr diff <number> --repo owner/repo` |
| Issue comments | `gh issue view <number> --repo owner/repo --comments` |
| PR comments | `gh pr view <number> --repo owner/repo --comments` |
| PR review comments | `gh api repos/owner/repo/pulls/<number>/comments` |
| Repository | `gh repo view owner/repo` |
| Discussion | `gh api repos/owner/repo/discussions/<number> --jq '.title,.body'` |
| Release | `gh release view <tag> --repo owner/repo` |
| Actions run | `gh run view <id> --repo owner/repo` |
| Commit | `gh api repos/owner/repo/commits/<sha>` |
| File (blob) | `gh api repos/owner/repo/contents/<path>?ref=<branch>` |
| Compare | `gh api repos/owner/repo/compare/<base>...<head>` |
| Gist | `gh gist view <id>` |

Use `--json` and `--jq` flags when structured data would be more useful than the default output.

If `gh` is not installed or authenticated, fall back to web fetching.
