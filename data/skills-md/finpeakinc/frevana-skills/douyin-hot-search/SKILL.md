---
name: douyin-hot-search
description: Fetch Douyin (抖音) hot search and trending boards (热搜/热榜), including 热点榜, 种草榜, 娱乐榜, 社会榜, and 挑战榜, through Frevana. Get ranked topics with available heat, view/video counts, and timing in JSON. Use for current board rankings; use douyin-search to find posts matching a keyword or hashtag.
---

# Douyin Hot Search

This skill retrieves ranked topics from Douyin's five public boards, not the videos or image-text posts behind a topic. To find posts for a returned topic, pass its `word` to `douyin-search`. The upstream [Douyin Hot Search Scraper](https://apify.com/zen-studio/douyin-hot-search-scraper) documents the board names and topic fields; Frevana may reuse a recent snapshot for the same parameters.

Use the bundled Bash script for task creation, status polling, and JSON result retrieval. It requires `bash`, `curl`, `jq`, and either `uuidgen` or `openssl` when generating a client task ID. Read [references/api.md](references/api.md) for request fields and states.

## Workflow

1. Use `run` for a complete task, or `create`, `status`, `wait`, and `result` for separate phases. Ask for a board only when the caller needs one; the API defaults to `hotspot`.
2. Treat creation as billable. Record the printed `client_task_id`. If the create request times out or its outcome is unclear, retry with the same ID and identical options; never generate a new task automatically.
3. Poll until `status=READY` and `billing_status=BILLED`. Stop on `FAILED`, `TIMED_OUT`, `ABORTED`, `RESULT_EXPIRED`, or `TRIGGER_UNKNOWN`.
4. Return the result JSON unchanged. Do not alter vendor fields or assume a particular item count.

## Commands

Resolve `{baseDir}` to this skill's directory.

```bash
bash {baseDir}/scripts/douyin_task.sh run --board hotspot
bash {baseDir}/scripts/douyin_task.sh run --board hotspot --board entertainment --max-results-per-board 20 --output ./out/hot.json
bash {baseDir}/scripts/douyin_task.sh create --client-task-id caller-stable-id --board social
bash {baseDir}/scripts/douyin_task.sh status --task-id TASK_UUID
bash {baseDir}/scripts/douyin_task.sh wait --task-id TASK_UUID
bash {baseDir}/scripts/douyin_task.sh result --task-id TASK_UUID
```

`create --wait` is equivalent to `run`. Use `--help` for all flags.

## Authentication and output

Use `FREVANA_TOKEN` or a one-time `--token` override. Never print the token. The default API base URL is `https://ai-factory.frevana.com`; override with `FREVANA_API_BASE_URL` or `--api-base-url` for another deployment or local testing.

`create` and `status` print the API response. `result`, `run`, and `wait` print the raw JSON result bytes; `run` and `wait` also save them under `./out/` by default. Use `--output` for an explicit path. The script sends only `Authorization: Bearer` to Frevana.

## Windows

Run the `.sh` entry point in Git Bash or WSL. Install `jq` if unavailable; Git for Windows includes Bash, and `winget install jqlang.jq` installs jq on Windows. Restart the terminal after installation and verify `command -v jq`. Git Bash accepts quoted Windows output paths such as `--output 'C:\Users\me\hot.json'`; WSL accepts them when `wslpath` is available. The script also accepts native POSIX paths. Keep the script's LF line endings when copying it outside Git.
