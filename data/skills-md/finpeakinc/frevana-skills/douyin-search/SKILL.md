---
name: douyin-search
description: Search public Douyin (抖音) posts by keywords, phrases, hashtags, brands, or people through Frevana. Find videos and image-text posts with creator and media metadata; use videoMeta.playUrl to play a video, videoMeta.downloadUrl to download it, and url for its original Douyin page. Use douyin-hot-search for ranked 热搜/热榜 topics.
---

# Douyin Search

This skill searches Douyin posts, including videos and image-text results, rather than returning ranked hot-search boards. A hot-board topic's `word` can be used as a keyword here. The upstream [Douyin Search Scraper](https://apify.com/zen-studio/douyin-search-scraper) documents the result fields and search filters. This Frevana skill exposes keyword and filter options; its default is 10 results per keyword, and its JSON result may contain Frevana URLs in place of recognized temporary media URLs. The upstream Actor's optional MP4, cover, and slideshow download switches are not exposed by this Frevana script.

Use the bundled Bash script for task creation, status polling, and JSON result retrieval. It requires `bash`, `curl`, `jq`, and either `uuidgen` or `openssl` when generating a client task ID. Read [references/api.md](references/api.md) for all filters and task states.

## Workflow

1. Require one to fifty keywords. Default to 10 videos per keyword and keep the number of unique keywords multiplied by `max_results_per_query` at most 1999. Use `run` for a complete task, or `create`, `status`, `wait`, and `result` for separate phases.
2. Treat creation as billable. Record the printed `client_task_id`. If the create request times out or its outcome is unclear, retry with the same ID and identical options; never generate a new task automatically.
3. Poll until `status=READY` and `billing_status=BILLED`. Stop on `FAILED`, `TIMED_OUT`, `ABORTED`, `RESULT_EXPIRED`, or `TRIGGER_UNKNOWN`.
4. Return the result JSON unchanged. The server archives recognized media to Frevana S3; do not rewrite or reorder result items.

## Result links

For a video result, use the fields in the returned JSON according to the user's intent:

| Intent | Field | Meaning |
| --- | --- | --- |
| Play the video | `videoMeta.playUrl` | Play from this video media URL. Do not confuse it with `musicMeta.playUrl`, which is audio. |
| Download the video | `videoMeta.downloadUrl` | Retrieve the video bytes from this URL when asked to download; the bundled task script only fetches JSON. |
| Open or cite the original post | `url` | Original Douyin post page, such as `https://www.douyin.com/video/<id>`. |

Use these fields only when present. Image-text posts may have no video playback or download URL. Upstream Douyin CDN links can expire within hours; `videoMeta.cdnUrlExpiresAt` records their expiry when available. Frevana may replace recognized temporary media URLs with archived URLs, so use the returned values rather than constructing links from an ID.

## Commands

Resolve `{baseDir}` to this skill's directory.

```bash
bash {baseDir}/scripts/douyin_task.sh run --keyword '露营'
bash {baseDir}/scripts/douyin_task.sh run --keyword '露营' --keyword '户外' --sort latest --publish-time one_week --duration under_1m --max-results-per-query 100 --output ./out/search.json
bash {baseDir}/scripts/douyin_task.sh create --client-task-id caller-stable-id --keyword '露营'
bash {baseDir}/scripts/douyin_task.sh status --task-id TASK_UUID
bash {baseDir}/scripts/douyin_task.sh wait --task-id TASK_UUID
bash {baseDir}/scripts/douyin_task.sh result --task-id TASK_UUID
```

`create --wait` is equivalent to `run`. Use `--help` for all flags.

The script explicitly sends `max_results_per_query: 10` when the flag is omitted. Override it with `--max-results-per-query` for a narrower or deeper search.

## Authentication and output

Use `FREVANA_TOKEN` or a one-time `--token` override. Never print the token. The default API base URL is `https://ai-factory.frevana.com`; override with `FREVANA_API_BASE_URL` or `--api-base-url` for another deployment or local testing.

`create` and `status` print the API response. `result`, `run`, and `wait` print the raw JSON result bytes; `run` and `wait` also save them under `./out/` by default. Use `--output` for an explicit path. The script sends only `Authorization: Bearer` to Frevana.

## Windows

Run the `.sh` entry point in Git Bash or WSL. Install `jq` if unavailable; Git for Windows includes Bash, and `winget install jqlang.jq` installs jq on Windows. Restart the terminal after installation and verify `command -v jq`. Git Bash accepts quoted Windows output paths such as `--output 'C:\Users\me\search.json'`; WSL accepts them when `wslpath` is available. The script also accepts native POSIX paths. Keep the script's LF line endings when copying it outside Git.
