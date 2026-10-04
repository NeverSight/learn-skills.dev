---
name: zhihu-cli
description: Use this skill whenever the user wants to interact with the Zhihu Open Platform through the `zhihu` command-line tool. This includes searching Zhihu content, performing global web search via Zhihu, using the Zhida chat/completion API, checking the Zhihu hot list, querying API quota, listing/searching/uploading-to knowledge bases, RAG search over knowledge bases, parsing PDF files, generating PPTs from Zhihu answers/articles, fetching Zhihu user data (contents, followees, collections, favlists), discovering questions to answer and reading answer summaries, viewing your own content's full text, comments, and creator stats, configuring credentials, or understanding CLI output. Use it even if the user only says "zhihu", "search zhihu", "zhida", "知乎", "热榜", "hot list", "额度", "quota", "知识库", "knowledge base", "RAG", "PDF 解析", "PPT 生成", "收藏夹", "favlist", "问题推荐", "创作数据", "creator stats", or mentions the project `zhihu-cli`.
---

# zhihu-cli Skill

This skill tells you how to use the `zhihu` command-line tool to call the Zhihu Open Platform APIs.

## Quick reference

- Binary name: `zhihu`
- Default output: raw JSON on stdout, suitable for piping to `jq` or other tools.
- Error output: JSON object on stdout, process exits with non-zero code.
- Authentication: `ZHIHU_ACCESS_SECRET` environment variable, or `~/.zhihu-cli/config.toml`.
- Repository: https://github.com/dawnswwwww/zhihu-cli

## Installation

In agent environments, install from npm:

```bash
npm install -g @dawnswwwww/zhihu-cli
```

Other options:

```bash
# Homebrew
brew tap dawnswwwww/tap
brew install zhihu-cli

# crates.io
cargo install zhihu-cli

# GitHub Releases (prebuilt binary)
# Download from https://github.com/dawnswwwww/zhihu-cli/releases
```

## Authentication

The CLI needs a Zhihu Open Platform Access Secret.

### Option 1: environment variable (preferred for agents)

```bash
export ZHIHU_ACCESS_SECRET="<your-secret>"
```

The environment variable takes precedence over the config file.

### Option 2: config file

```bash
zhihu auth set-secret "<your-secret>"
```

This writes `~/.zhihu-cli/config.toml`:

```toml
access_secret = "<your-secret>"
```

On Unix the file is created with `0o600` permissions.

### Option 3: interactive login

```bash
zhihu auth login
```

Then paste the secret when prompted.

### Check status

```bash
zhihu auth status
```

Returns JSON like:

```json
{
  "configured": true,
  "source": "env"
}
```

## Commands

### Search Zhihu (站内搜索)

```bash
zhihu search zhihu "QUERY" [--count N]
```

- `QUERY`: search keywords (required)
- `--count`: number of results, default 10, max 10; the CLI clamps out-of-range values to [1, 10]

Example:

```bash
zhihu search zhihu "RAG 评测" --count 5
```

### Search the global web (全网搜索)

```bash
zhihu search global "QUERY" [--count N] [--filter FILTER] [--db all|realtime|static]
```

- `QUERY`: search keywords (required)
- `--count`: number of results, default 10, max 20; the CLI clamps out-of-range values to [1, 20]
- `--filter`: advanced filter expression; the CLI passes it through, so quote it correctly in the shell
- `--db`: index database choice: `all` (default), `realtime`, `static`

Filter syntax examples:

```text
host=="example.com"
host=="example.com" AND publish_time>=1778494631
(host=="example.com" OR host=="news.example.com") AND publish_time>1778494631
```

Important: `host=="zhihu.com"` is not supported in global search; for Zhihu-only content use `zhihu search zhihu`.

Example:

```bash
zhihu search global "人工智能" --count 5 --filter 'host=="example.com"' --db all
```

### Zhihu hot list (热榜)

```bash
zhihu hot [--limit N]
```

- `--limit`: number of results, default 30, max 30; the CLI clamps out-of-range values to [1, 30]

Example:

```bash
zhihu hot --limit 10
```

### Zhida chat/completion (直答)

```bash
zhihu ask "QUERY" [--model fast|thinking|agent] [--stream]
```

- `QUERY`: user message (required); sent as `messages=[{"role":"user","content":"QUERY"}]`
- `--model`: one of
  - `fast` → `zhida-fast-1p5`
  - `thinking` → `zhida-thinking-1p5` (default)
  - `agent` → `zhida-agent`
- `--stream`: enable streaming output (default off)

Example:

```bash
zhihu ask "什么是 RAG？" --model thinking
```

### Quota query (额度查询)

```bash
zhihu quota [--ids ID[,ID...]]
```

- `--ids`: comma-separated API IDs to filter; omit for all

Known IDs: `global_search`, `zhihu_search`, `hot_list`, `question_answers`, `user_data`, `zhida_openai`, `knowledge`, `tools`, `creator`. Knowledge-base APIs share the `knowledge` pool; PDF parse and PPT generation share the `tools` pool; question recommendations and creator APIs share the `creator` pool; question answers use the `question_answers` pool. The quota query itself consumes no quota.

Example:

```bash
zhihu quota --ids knowledge,tools
```

### Knowledge bases (知识库)

```bash
zhihu kb list [--scope all|created|subscribed]
zhihu kb items <KB_ID> [--cursor CURSOR] [--limit N]
zhihu kb upload <FILE> [--kb-id KB_ID]
zhihu kb search "QUERY" [--kb-id KB_ID]... [--scope personal|subscription|public]... [--limit N]
```

- `kb list`: knowledge bases you created or subscribed (`--scope`, default `all`)
- `kb items`: paged contents of a KB; `--limit` default 20 max 20; use `NextCursor` from the previous response as `--cursor`; stop when `HasMore` is false
- `kb upload`: upload a file (pdf, md, txt, ppt(x), xls(x), doc(x), webp, png, jpg, mobi, epub, csv, azw3; max 100 MB). Omit `--kb-id` for your default KB. Synchronous — large files take a while
- `kb search`: RAG search; requires at least one `--kb-id` or `--scope` (both allowed, union); `--limit` default 10 max 10, counts documents not fragments

Examples:

```bash
zhihu kb upload ./product-doc.pdf --kb-id 7526139256098382426
zhihu kb search "退款规则是什么？" --scope personal --limit 5
```

First-time users must initialize their knowledge base once at https://zhida.zhihu.com/repositories/square

### PDF parse (PDF 解析，异步)

```bash
zhihu pdf upload <FILE>                       # → file_id (valid 24h)
zhihu pdf task <FILE_ID> [--idempotency-key KEY]
zhihu pdf status <TASK_ID>
zhihu pdf parse <FILE> [--timeout-secs N] [--idempotency-key KEY]   # one-shot
```

- `pdf parse` chains upload → create task → poll (every 2s) and prints the final task JSON; the result link is `Data.result.url` (short-lived; re-run `pdf status` to refresh). `--timeout-secs` default 600
- PDF only, max 100 MB
- `--idempotency-key`: same key + same params returns the same task

Example:

```bash
zhihu pdf parse ./report.pdf --timeout-secs 300
```

### PPT generation (PPT 生成，异步)

```bash
zhihu ppt task <URL> --pages N [--idempotency-key KEY]
zhihu ppt status <TASK_ID>
zhihu ppt generate <URL> --pages N [--timeout-secs N] [--idempotency-key KEY]   # one-shot
```

- `URL`: a Zhihu answer (`https://www.zhihu.com/question/{qid}/answer/{aid}` or `https://www.zhihu.com/answer/{aid}`) or article (`https://zhuanlan.zhihu.com/p/{pid}`)
- `--pages`: required; clamped to [6, 21]
- `ppt generate` waits and prints the final task JSON; the PPTX link is `Data.result.url`

Example:

```bash
zhihu ppt generate "https://zhuanlan.zhihu.com/p/987654321" --pages 12
```

### Zhihu user data (知乎用户数据)

```bash
zhihu user contents [--type all|answer|article|zvideo|pin|question] [--offset N] [--limit N] [--sort-field ts|like_count] [--sort-order desc|asc]
zhihu user followees [--offset N] [--limit N]
zhihu user collections [--limit N]
zhihu user favlists [--limit N]
zhihu user favlist-contents <FAVLIST_URL_TOKEN> [--offset N] [--limit N]
```

- All user commands accept `--oauth-token <T>` to query that OAuth-authorized user's data instead of your own
- `contents`/`followees` clamp `--limit` to [1, 50]; page with `Paging.NextOffset` as the next `--offset`
- `favlist-contents` takes the `UrlToken` number from `zhihu user favlists`

Examples:

```bash
zhihu user contents --type answer --limit 10 --sort-field like_count
zhihu user favlists --limit 5
zhihu user favlist-contents 123456789 --limit 20
```

### Question discovery (问题发现)

```bash
zhihu question recommend [--query TOPIC] [--count N]
zhihu question answers <QUESTION_URL> [--offset N] [--limit N]
```

- `question recommend`: recommends questions worth answering. Omit `--query` for profile-based recommendations; pass `--query TOPIC` for topic-based (a blank value is rejected). `--count` default 5, clamped to [1, 20]. No pagination
- `question answers`: answer summaries under a question (`Summary` is the service-provided excerpt, not an AI summary or the full text). `--limit` default 20, clamped to [1, 50]; page with `Paging.NextOffset` as the next `--offset`, stop when `Paging.IsEnd` is true

Examples:

```bash
zhihu question recommend --query "AI Agent" --count 10
zhihu question answers "https://www.zhihu.com/question/123456789" --limit 20
```

### Creator capabilities (创作能力)

```bash
zhihu creator detail <CONTENT_URL>
zhihu creator comments <CONTENT_URL> [--offset N] [--limit N] [--order score|reverse|ascending]
zhihu creator account-stats [--type all|answer|article|pin|zvideo] [--start-date YYYY-MM-DD --end-date YYYY-MM-DD]
zhihu creator content-stats <CONTENT_URL> [--start-date YYYY-MM-DD --end-date YYYY-MM-DD]
```

- All creator commands read only the current Access Secret account's own data; they do not accept `--oauth-token`
- `creator detail`: full text (`Body`, may contain HTML) of your own published answer/article/pin/zvideo; drafts and unpublished content are not supported
- `creator comments`: root comments plus their child comments; `--limit` default 20, clamped to [1, 50], counts root comments; `--order`: `score` (default, by popularity), `reverse` (newest first), `ascending` (oldest first)
- `account-stats` / `content-stats`: `--start-date`/`--end-date` must be given together (YYYY-MM-DD, end not before start); omit both for the service default range. Optional metrics are omitted by the API rather than zero-filled
- Creator commands share the daily `creator` quota pool with `question recommend`

Examples:

```bash
zhihu creator detail "https://zhuanlan.zhihu.com/p/123456789"
zhihu creator comments "https://www.zhihu.com/question/123/answer/456" --order reverse --limit 10
zhihu creator account-stats --type article --start-date 2026-09-01 --end-date 2026-09-24
zhihu creator content-stats "https://zhuanlan.zhihu.com/p/123456789"
```

## Output format

### Success

Search and hot-list commands return the API's raw JSON response (PascalCase fields):

```json
{
  "Code": 0,
  "Message": "success",
  "Data": {
    "HasMore": false,
    "SearchHashId": "...",
    "Items": [...]
  }
}
```

`zhihu hot` returns a hot-list shaped response:

```json
{
  "Code": 0,
  "Message": "success",
  "Data": {
    "Total": 10,
    "Items": [
      {
        "Title": "如何评价某个热点问题？",
        "Url": "https://www.zhihu.com/question/123456789",
        "ThumbnailUrl": "...",
        "Summary": "..."
      }
    ]
  }
}
```

`zhihu ask` without `--stream` returns the OpenAI-style chat completion JSON:

```json
{
  "id": "chatcmpl-xxxx",
  "object": "chat.completion",
  "model": "zhida-thinking-1p5",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "reasoning_content": "...",
        "content": "..."
      },
      "finish_reason": "stop"
    }
  ]
}
```

### Streaming

With `--stream`, `zhihu ask` prints newline-delimited JSON (NDJSON) chunks:

```text
{"delta":{"reasoning_content":"先分析..."}}
{"delta":{"content":"RAG 是..."}}
{"finish_reason":"stop"}
```

When calling from an agent, prefer omitting `--stream` to get a single complete JSON object.

### Errors

All errors are emitted as JSON:

```json
{
  "error": "Set ZHIHU_ACCESS_SECRET or run 'zhihu auth set-secret'",
  "code": 20001
}
```

Common error codes:

| Code | Meaning |
|------|---------|
| 0 | Success |
| 10001 | Bad request parameters |
| 20001 | Authentication failed (CLI-local missing-secret sentinel is also 20001) |
| 30001 | Rate limited |
| 30002 | Quota exhausted (user-data / pdf / ppt / question / creator APIs) |
| 30003 | Request rejected by risk control (question / creator APIs) |
| 40001 | Idempotency key conflicts with different params (pdf/ppt) |
| 40002 | Uploaded file missing, expired, or inaccessible (pdf) |
| 40003 | Too many active tasks; wait for existing tasks (pdf/ppt) |
| 40004 | Knowledge base not found (kb) |
| 40005 | Same file still processing (kb upload) |
| 40006 | File parse failed (kb upload) |
| 50002 | Knowledge search failed; retry later |
| 90001 | Internal server error |

Task commands (`pdf parse` / `ppt generate`) may also fail with a `TaskTimeout` error (no `code` field) when `--timeout-secs` elapses before the task finishes.

## Tips for agents

1. Always check `ZHIHU_ACCESS_SECRET` is set before calling non-auth commands.
2. For search, default `--count` is usually enough; use `--count` only when the user asks for more results.
3. For `zhihu hot`, default `--limit` (30) is usually enough; use a smaller value only when the user asks for fewer items.
4. For `zhihu ask`, default to `--model thinking` unless the user asks for a quick answer (`fast`) or a complex multi-step task (`agent`).
5. Do not use `global` search with `host=="zhihu.com"`; use `zhihu search zhihu` instead.
6. Parse output as JSON; on non-zero exit code, show the `error` field to the user.
7. When the user asks a general knowledge question in Chinese, consider using `zhihu ask` or `zhihu search zhihu` to get Zhihu-style answers.
8. When the user asks about current trending topics on Zhihu, use `zhihu hot`.
9. Before long-running upload/parse jobs, check remaining quota with `zhihu quota --ids knowledge,tools`.
10. For PDF/PPT one-shots, prefer `zhihu pdf parse <FILE>` / `zhihu ppt generate <URL> --pages N` over manually chaining upload/task/status. Download links expire quickly; if a link is stale, re-run the matching `status` command to get a fresh one.
11. For `kb search`, at least one `--kb-id` or `--scope` is required; `--scope personal` covers your own (including default) knowledge bases.
12. User-data commands return your own data by default; only pass `--oauth-token` when you hold that user's OAuth token.
13. Use `zhihu question recommend` (optionally with `--query TOPIC`) when the user looks for questions worth answering; follow up with `zhihu question answers <QUESTION_URL>` to read answer summaries.
14. Creator commands (`zhihu creator ...`) only read the current account's own data — no `--oauth-token`; dates must be passed as a `--start-date`/`--end-date` pair. Check the `creator` pool with `zhihu quota --ids creator` before heavy use.

## Examples

Search Zhihu:

```bash
zhihu search zhihu "如何理解 rave 文化" --count 5
```

Global search with filter:

```bash
zhihu search global "ChatGPT" --count 10 --filter 'host=="openai.com"' --db realtime
```

Check Zhihu hot list:

```bash
zhihu hot --limit 10
```

Ask Zhida:

```bash
zhihu ask "总结 RAG 的核心思路" --model agent
```

Check quota, then upload and RAG-search a knowledge base:

```bash
zhihu quota --ids knowledge
zhihu kb upload ./handbook.pdf
zhihu kb search "退款政策" --scope personal
```

Parse a PDF in one shot:

```bash
zhihu pdf parse ./whitepaper.pdf --timeout-secs 300
```

Generate a PPT from an answer and grab the link:

```bash
zhihu ppt generate "https://www.zhihu.com/question/1892249263213356127/answer/2021688002292752412" --pages 10
```

Find questions to answer, then read the answers under one of them:

```bash
zhihu question recommend --query "AI Agent" --count 5
zhihu question answers "https://www.zhihu.com/question/123456789" --limit 10
```

Read your own article's full text, comments, and stats:

```bash
zhihu creator detail "https://zhuanlan.zhihu.com/p/123456789"
zhihu creator comments "https://zhuanlan.zhihu.com/p/123456789" --limit 10
zhihu creator content-stats "https://zhuanlan.zhihu.com/p/123456789" --start-date 2026-09-01 --end-date 2026-09-24
```

## References

For full API endpoint and field details, read `references/api-reference.md` bundled with this skill.
