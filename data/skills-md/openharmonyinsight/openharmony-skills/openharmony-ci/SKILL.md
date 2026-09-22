---
name: openharmony-ci
description: Use when investigating OpenHarmony PR CI status from `openharmony_ci` comments, DCP event IDs, build labels, artifact links, or CI log URLs.
---

# OpenHarmony CI

## Overview
Use the bundled script first. It resolves the latest DCP event from an OpenHarmony PR, summarizes per-job CI status, and fetches logs only for failed jobs unless explicitly told otherwise.

## Permission Preflight
- Treat this workflow as network-required by default.
- Before running the bundled script for `--pr`, `--pr-url`, `--event-id`, artifact paths, or CI log URLs, request network permission up front.
- Mention the likely endpoints in the permission request when helpful: GitCode via `oh-gc`, `dcp.openharmony.cn`, and `cidownload.openharmony.cn`.
- Do not intentionally run a first attempt just to confirm that network is required. The failure is usually predictable from the workflow itself.

## Primary Path
Run the bundled script:

```bash
python3 scripts/openharmony_ci.py --pr <pr_number> --repo <repo>
```

The script sets `XDG_CACHE_HOME=/tmp/openharmony-ci-cache` for `oh-gc` by default so it does not try to write under `~/.cache` in sandboxed environments. If you already need a different cache location, set `XDG_CACHE_HOME` before invoking the script and the script will respect it.

Supported inputs:
- `--pr <number>`
- `--pr-url <gitcode_pr_url>`
- `--event-id <dcp_event_id>`

Useful flags:
- `--log-mode auto`
  Only fetch logs for failed jobs. This is the default and should remain the normal mode.
- `--log-mode never`
  Status only.
- `--log-mode always`
  Fetch logs for every job that exposes artifacts or log links.
- `--json`
  Machine-readable output.
- `--download-dir <dir>`
  Save downloaded log archives/files locally.

## Expectations
- Prefer `--pr` or `--pr-url` when the task starts from a GitCode PR.
- The script reads `openharmony_ci` comments with `oh-gc`, extracts the newest DCP event id, then queries DCP APIs.
- In sandboxed or restricted environments, request network access before invoking the script because the primary path depends on external services.
- In restricted environments, prefer the bundled script over raw `oh-gc` calls because it already redirects the `oh-gc` cache to a writable temporary directory.
- Judge pass/fail from DCP event data, not labels alone.
- If there are multiple failed jobs, report all of them.
- Treat jobs with a start time but no end result as `running`, not failed.
- On failures, follow artifact listings to logs automatically. `build.log` may redirect to another URL, and `build.log.zip` may actually be a tar archive.
- In the final answer, report both the DCP `overall` result and the per-job failures. If `overall=success` but some jobs are marked `skip` or `failed`, say that explicitly instead of flattening it into a single verdict.
- If a failed job shows `skip build` or a similar reason, include that reason verbatim and avoid implying that the whole PR failed unless the DCP overall result is also failed.

## Fallback
If the script cannot be used, fall back to the manual workflow:
1. Extract the DCP event id from the latest `openharmony_ci` build-start comment.
2. Query `https://dcp.openharmony.cn/api/codecheckAccess/ci-portal/v1/event/<event_id>`.
3. If a failed job has `Artifacts`, query `https://dcp.openharmony.cn/api/dataService/ci-portal/v1/files?directoryUrl=<ArtifactsPath>`.
4. Download the chosen log from `https://cidownload.openharmony.cn/<path>`.

## Quick Examples
```bash
python3 scripts/openharmony_ci.py --pr 82764 --repo openharmony/arkui_ace_engine
python3 scripts/openharmony_ci.py --pr-url 'https://gitcode.com/openharmony/arkui_ace_engine/pull/82764' --json
python3 scripts/openharmony_ci.py --event-id 69c51ede64650f998b1d01a4 --log-mode auto
XDG_CACHE_HOME=/tmp/custom-oh-gc-cache python3 scripts/openharmony_ci.py --pr 82764 --repo openharmony/arkui_ace_engine
```
