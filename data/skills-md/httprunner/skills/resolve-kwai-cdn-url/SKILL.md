---
name: resolve-kwai-cdn-url
description: Resolve Kuaishou (快手 / Kwai) share links or share text into video CDN URLs. Use for single links, share text, or CSV inputs when output must be JSONL with CDNURL/error_msg. Prefer videodl (videofetch); fall back to GraphQL/mobile-page extraction with cookies when needed.
---

# Resolve Kwai CDN URL

Extract CDN URLs from Kuaishou share links with two paths:
- videodl (videofetch): primary path, supports cookies/proxy (Playwright + requests).
- GraphQL/mobile-page: fallback when videodl fails.

## Path Convention

Canonical install and execution directory: `~/.agents/skills/resolve-kwai-cdn-url/`. Run commands from this directory:

```bash
cd ~/.agents/skills/resolve-kwai-cdn-url
```

One-off (safe in scripts/loops from any working directory):

```bash
(cd ~/.agents/skills/resolve-kwai-cdn-url && uv run python scripts/kwai_videodl_resolve.py --help)
```

## Fast path (videodl)

```bash
uv venv .venv
uv sync
uv run python scripts/kwai_videodl_resolve.py "https://v.kuaishou.com/8qIlZu" > single.jsonl
uv run python scripts/kwai_videodl_resolve.py --input-csv data.csv --csv-url-field URL --output output.jsonl --workers 10
uv run python scripts/kwai_videodl_resolve.py --input-csv data.csv --csv-url-field URL --output output.jsonl --workers 10 --resume
uv run python scripts/kwai_videodl_resolve.py "https://v.kuaishou.com/8qIlZu" --proxy "http://user:pass@host:port"
uv run python scripts/kwai_videodl_resolve.py "https://v.kuaishou.com/8qIlZu" --cookie "<YOUR_COOKIE>"
uv run python scripts/kwai_videodl_resolve.py "https://v.kuaishou.com/8qIlZu" --cookie-file cookie.json
```

## Fallback path (GraphQL/mobile-page)

```bash
uv run python scripts/kwai_extract_cdn.py "https://www.kuaishou.com/short-video/3xu6tezif2v55m2" --cookie "<YOUR_COOKIE>"
uv run python scripts/kwai_extract_cdn.py "https://www.kuaishou.com/short-video/3xu6tezif2v55m2" --cookie-file cookie.json
uv run python scripts/kwai_extract_cdn.py "https://www.kuaishou.com/short-video/3xu6tezif2v55m2" --proxy "http://user:pass@host:port"
uv run python scripts/kwai_csv_to_jsonl.py data.csv --url-col URL --cdn-col CDNURL --cookie "<YOUR_COOKIE>" --workers 10 --output output.jsonl
uv run python scripts/kwai_csv_to_jsonl.py data.csv --url-col URL --cdn-col CDNURL --cookie-file cookie.json --workers 10 --output output.jsonl
uv run python scripts/kwai_csv_to_jsonl.py data.csv --url-col URL --cdn-col CDNURL --cookie "<YOUR_COOKIE>" --workers 10 --output output.jsonl --resume
uv run python scripts/kwai_csv_to_jsonl.py data.csv --url-col URL --cdn-col CDNURL --proxy "http://user:pass@host:port" --workers 10 --output output.jsonl
```

## Output

- videodl: `{"url": "...", "cdn_url": "...", "error_msg": ""}`
- CSV mode (both paths): original columns + `CDNURL` + optional `error_msg`

## Notes

- videodl auto-extracts the first URL from share text and follows `v.kuaishou.com` redirects.
- videodl Playwright path honors `proxy/cookie/headers` passed via `requests_overrides` in `kwai_videodl_resolve.py`.
- GraphQL path tries GraphQL, then mobile `INIT_STATE`, then HTML state parsing.
- If blocked, try without cookies first; if still blocked, pass a real browser cookie via `--cookie` or `--cookie-file`.
- `--cookie` expects a raw Cookie header string, e.g. `kpf=PC_WEB; clientid=3; did=...`.
- `--cookie-file` accepts either a raw Cookie header string or a JSON cookie array export (list of `{name,value}` objects).
- When no cookie is provided, videodl will fetch an anonymous cookie from the homepage (incognito-like).
- `--proxy` applies to all HTTP requests, e.g. `http://user:pass@host:port`.
- `--resume` rewrites output JSONL to keep only successful rows, then retries missing/failed rows and appends new results.
- CSV progress logs are batch-based success counts; stats are emitted on completion or Ctrl+C.
- `live.kuaishou.com` and `captcha.zt.kuaishou.com` are treated as failures; `error_msg` includes the reason.

## Resources

- `scripts/kwai_videodl_resolve.py`: videodl-based resolver.
- `scripts/kwai_extract_cdn.py`: GraphQL/mobile-page resolver.
- `scripts/kwai_csv_to_jsonl.py`: CSV -> JSONL (GraphQL/mobile-page).
- `scripts/kwai_common.py`: shared helpers for resume and JSONL processing.
- `references/videodl_api.md`: minimal videodl API.
- `references/kuaishou_graphql.md`: GraphQL endpoints/payload notes.
