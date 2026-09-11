---
name: shunk031-github-comment-attach-files
description: Attach local files to a GitHub issue or pull request comment via Playwright CLI and return the hosted attachment URLs without submitting the comment. Use when you need GitHub-hosted image or document URLs on github.com or GitHub Enterprise Server.
---

> [!NOTE]
> After reading this `SKILL.md`, say: `📎 I read shunk031-github-comment-attach-files.`

# GitHub Comment Attach Files

## When To Use

Use this skill when you need GitHub to host local files and give back anonymized attachment URLs, but you do not want the agent to submit the issue or pull request comment itself.

Typical cases:

- Upload PNG, JPG, PDF, Markdown, or other GitHub-supported attachments to a PR or issue comment box.
- Replace broken local image URLs in a draft report with GitHub-hosted URLs.
- Work against either `github.com` or GitHub Enterprise Server.

Do not use this skill when the task is to actually post, edit, or rewrite a comment. This skill stops after URL acquisition.

## Prerequisites

- `npx @playwright/cli` must be available.
- If you use `--repo ... --issue ...` or `--repo ... --pr ...`, `gh` must be installed and authenticated.
- If GitHub redirects to login or SSO, finish authentication in the opened browser window while the script is polling for the comment composer.

## Workflow

1. Resolve the target page from either a direct URL or `gh` metadata.
2. Stage the requested files under `./.playwright-cli/gh-comment-attach-files/...`.
3. Open the issue or pull request page with a persistent Playwright CLI browser profile.
4. Find the main comment composer and attach files one by one.
5. Read the inserted Markdown and return JSON with `target_url`, `source_path`, `staged_name`, and `attachment_url`.
6. Close the browser unless `--leave-open` is used.

## Command

Direct URL:

```bash
uv run python ~/.agents/skills/shunk031-github-comment-attach-files/scripts/attach_comment_files.py \
  --url https://github.com/OWNER/REPO/pull/123 \
  docs/report.md assets/chart.png
```

Resolve the page with `gh`:

```bash
uv run python ~/.agents/skills/shunk031-github-comment-attach-files/scripts/attach_comment_files.py \
  --repo OWNER/REPO \
  --pr 123 \
  results/report.md results/chart.png
```

Large uploads that may need multiple runs:

```bash
uv run python ~/.agents/skills/shunk031-github-comment-attach-files/scripts/attach_comment_files.py \
  --repo OWNER/REPO \
  --pr 123 \
  --resume-manifest attachments.jsonl \
  --sleep-between-files 2 \
  --max-files-per-run 60 \
  results/*.png
```

When `--resume-manifest` is set, each successful upload is appended as JSONL.
Rerunning the same command skips files that already have a `source_path` entry in the manifest and returns those existing URLs in the normal JSON output.

## Output

The script prints JSON only:

```json
{
  "target_url": "https://github.com/OWNER/REPO/pull/123",
  "attachments": [
    {
      "source_path": "/abs/path/results/chart.png",
      "staged_name": "chart--e5b6d4a1.png",
      "attachment_url": "https://github.com/user-attachments/assets/..."
    }
  ]
}
```

## Notes

- The script does not submit the comment.
- `staged_name` may differ from the original basename so duplicate filenames stay distinct.
- The default persistent profile lives under `./.playwright-cli/gh-comment-attach-files/profile`.
- Use `--leave-open` when you want to keep the browser and draft comment visible after the URLs are collected.
- Use `--max-files-per-run` with `--resume-manifest` to chunk large attachment sets without losing completed URLs.
- Diagnostic progress, retry information, and the final run directory on failure are printed to stderr.

## Resources

### scripts/

- `scripts/attach_comment_files.py`: resolves the target page, stages files, drives Playwright CLI, and returns hosted attachment URLs as JSON.
