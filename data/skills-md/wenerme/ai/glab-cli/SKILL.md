---
name: glab-cli
description: "Use when interacting with GitLab via the glab CLI: creating/reviewing merge requests, managing issues, monitoring CI/CD pipelines, making API calls, or performing any GitLab operation from the terminal. Triggers on glab, gitlab cli, merge request, MR create, pipeline status, ci lint."
---

# GitLab CLI (glab)

## Rules

- ALWAYS verify auth before first command: `glab auth status`
- ALWAYS use `-R owner/repo` when not inside the target git repo
- For self-hosted GitLab, set `GITLAB_HOST` or use `--hostname`
- Use `--output=json` when parsing output programmatically
- NEVER hardcode tokens in commands — use `glab auth login` or `GITLAB_TOKEN` env var
- Pagination params go in URL, not flags: `glab api "projects/:id/jobs?per_page=100"` (NOT `--per-page`)
- When creating MRs, ALWAYS add `--remove-source-branch --squash-before-merge` unless the user explicitly says otherwise

## Auth

```bash
glab auth login                                    # Interactive
glab auth login --hostname gitlab.example.org      # Self-hosted
glab auth status                                   # Verify
```

## MR Workflow

```bash
git push -u origin feature-branch
glab mr create --title "Fix bug" --description "Closes #123" \
  --remove-source-branch --squash-before-merge --reviewer=alice,bob
glab mr list --reviewer=@me                        # MRs to review
glab mr checkout 42                                # Test locally
glab mr approve 42
glab mr merge 42 --remove-source-branch
```

## Issue Workflow

```bash
glab issue create --title "Bug" --label=bug --assignee=@me
glab issue list --assignee=@me
glab issue close 123 -m "Fixed in MR !42"
```

## CI/CD

```bash
glab ci status                    # Current pipeline status
glab ci status --live             # Watch until pipeline completes
glab pipeline ci view             # Watch pipeline (interactive)
glab ci trace                     # View job logs
glab ci lint                      # Validate .gitlab-ci.yml
glab ci run                       # Trigger pipeline
glab ci retry                     # Retry failed pipeline
```

**Wait for pipeline in scripts** (glab has no built-in blocking wait):

```bash
while true; do
  status=$(glab api "projects/:id/pipelines?ref=$(git branch --show-current)&per_page=1" \
    | jq -r '.[0].status')
  case "$status" in
    success) echo "Pipeline passed"; break ;;
    failed|canceled) echo "Pipeline $status"; exit 1 ;;
    *) echo "Status: $status, waiting..."; sleep 15 ;;
  esac
done
```

**Auto-merge when pipeline succeeds:**

```bash
glab mr merge <MR_ID> --when-pipeline-succeeds
```

## API

```bash
glab api projects/:id/merge_requests
glab api --paginate "projects/:id/pipelines/123/jobs?per_page=100"
glab api --method POST projects/:id/issues --field title="Bug"
```

## Quick Fixes

| Error | Fix |
|-------|-----|
| `401 Unauthorized` | `glab auth login` |
| `404 Project Not Found` | Check repo name + access permissions |
| `not a git repository` | `cd` to repo or use `-R owner/repo` |
| `source branch already has MR` | `glab mr list` to find existing |
| `pipeline must succeed` | `glab ci status` then fix/retry |

## References

- [references/commands.md](references/commands.md) — Full command reference (MR, Issue, CI/CD, Repo, API, Labels, Releases, Variables, etc.)
- [references/pipeline-debug.md](references/pipeline-debug.md) — Pipeline 排查流程、Job 日志、重试/取消、Artifacts、批量清理
- [references/config.md](references/config.md) — 认证管理、多实例、环境变量、配置文件、Shell 补全、Aliases
- [references/troubleshooting.md](references/troubleshooting.md) — Auth, network, SSL, config 常见错误和解决方案
