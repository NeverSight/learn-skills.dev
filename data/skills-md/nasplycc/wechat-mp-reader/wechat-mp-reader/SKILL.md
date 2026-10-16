---
name: wechat-mp-reader
description: Fetch WeChat Official Account articles from either a public account name or a WeChat article URL. Use when the user wants to extract full article content, identify the account behind an article, list recent or historical articles for an account, or build article archives from WeChat public accounts. Prioritize article-URL-based resolution first, then account-name search, with graceful fallback when search is unreliable.
---

# WeChat MP Reader

Use this skill for 微信公众号文章抓取、公众号反查、文章列表拉取、全文提取。

## What this skill should do

Support these user intents:
- 给一篇公众号文章链接，提取全文
- 给一篇公众号文章链接，识别公众号并列出该号文章
- 给一个公众号名称，查找候选公众号并抓取文章列表
- 检查、保存、复用微信公众号后台 session
- 将文章内容标准化为 markdown / structured JSON

## Operating principles

1. **URL-first is the default path.** If the user gives an article URL, resolve from it first.
2. **Name search is best-effort.** If account-name search is unreliable, ask for any article URL from that account.
3. **Full text matters more than stats.** Article extraction is core; read/like stats are optional.
4. **Use layered fallbacks.** Try plain HTTP first, but for WeChat articles treat browser fallback as normal whenever the page looks non-canonical (verification page, shell page, or mixed JS page). The current fallback is local Playwright WebKit only.
5. **Keep outputs structured.** Return normalized account/article objects rather than loose text.
6. **Recover fakeid via search when needed.** Article pages often expose `biz`/account name, but not a stable `fakeid`; when MP backend session is available, try search-based recovery.
7. **Treat session validity as first-class state.** Report whether session is present/valid, instead of hiding failures in generic warnings.

## Default workflow

### Path A — article URL provided
1. Parse the article URL and extract `__biz`, `mid`, `idx`, `sn`.
2. Fetch the article page.
3. Extract account metadata from HTML / embedded JS.
4. Load MP backend session from env or session file.
5. Validate session and report `session.present / session.valid / session.reason`.
6. If `fakeid` is missing and session is valid, search by account name and match candidates using `biz` / name.
7. Extract and clean full article content.
8. If requested and `fakeid` is available, list more articles for that account.

### Path B — account name provided
1. Load and validate MP backend session.
2. Attempt account-name search via the search adapter.
3. Return ranked candidates.
4. If a confident match exists, fetch article list.
5. If search fails or is ambiguous, ask for any article URL from that account and switch to Path A.

### Path C — session operations
Use the bundled CLI to:
- `session check` — validate current env/file-backed session
- `session show` — report non-sensitive session presence/length/status
- `session save` — persist env-provided session to local cache file
- `session login-start` — start QR login, return scan state, and write a real scannable QR PNG under `scripts/cache/wechat-login-qr-real.png`
- `session login-status` — poll login status and capture fresh session when ready

## Expected outputs

### Session object
```json
{
  "present": true,
  "valid": false,
  "reason": "invalid session",
  "base_resp": {}
}
```

### Account object
```json
{
  "name": "",
  "biz": "",
  "fakeid": "",
  "avatar": "",
  "signature": ""
}
```

### Article object
```json
{
  "title": "",
  "url": "",
  "publish_time": "",
  "publish_time_raw": "",
  "author": "",
  "account_name": "",
  "content_html": "",
  "content_markdown": "",
  "images": []
}
```

## Implementation notes

- Prefer the bundled Python prototype at `scripts/wechat_mp_reader.py`.
- Default live validation path: use the skill's own session commands (`session check`, `session login-start`, `session login-status`) and then run `article <url> --with-account-articles` directly via `scripts/wechat_mp_reader.py`; helper bridge scripts are no longer the default path.
- `session login-start` now persists a real scannable QR image to `scripts/cache/wechat-login-qr-real.png` and returns its path in `qr_image_path`.
- Session resolution order is: env vars first, then saved session file.
- The current article pipeline is URL-first and will automatically fall back to local Playwright WebKit when direct HTTP HTML looks non-canonical.
- Treat article body extraction as the MVP.
- Treat account-name search and historical article listing as adapters that can evolve.
- Treat engagement stats as optional and isolated from the main flow.
- Cache article HTML and parsed results when repeated fetching is likely.
- Cache resolved account mappings (`biz` / `name` -> `fakeid`) locally to reduce repeated searchbiz lookups.

## Files to use

- `scripts/wechat_mp_reader.py` — Python prototype and CLI
- `scripts/wechat_mp_reader/auth.py` — session validation helpers
- `scripts/wechat_mp_reader/session_store.py` — session load/save helpers
- `references/design.md` — architecture, implementation phases, and caveats

Read `references/design.md` when you need the detailed design, adapter responsibilities, or future roadmap.
Read `references/usage.md` when you need the human-facing usage guide, CLI examples, or natural-language invocation patterns for triggering this skill through an agent.
