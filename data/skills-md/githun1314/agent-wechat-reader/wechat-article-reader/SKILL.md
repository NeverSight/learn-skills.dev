---
name: wechat-article-reader
description: Automatically read one or more public WeChat Official Account articles whenever user input contains exact-host https://mp.weixin.qq.com URLs, including a lone URL or a batch of links, without requiring a fixed prompt or the skill name. Use for reading, summarizing, extracting, analyzing, comparing, quoting, archiving, or transforming those articles; when no operation is stated, ingest each WeChat link and return its title, author, status, and a concise summary. For mixed-domain link lists, apply this skill only to the WeChat URLs. Save clean Markdown plus metadata and a trace, with verification-page detection and bounded retry but no cookies, credentials, browser control, or third-party reader services.
---

# WeChat Article Reader

Use the bundled script whenever a message contains one or more exact-host `https://mp.weixin.qq.com` links. Do not require the user to name this skill or use a fixed command. It accepts only public HTTPS article URLs, writes responses to temporary directories, and prints paths instead of flooding the conversation.

## Workflow

1. Extract and deduplicate every exact-host `https://mp.weixin.qq.com` URL from the user's message. For mixed-domain lists, leave non-WeChat URLs to the appropriate general reader.

2. Run once for each WeChat URL:

   ```bash
   python3 "$SKILL_DIR/scripts/read_wechat_article.py" "<URL>" --quiet
   ```

   Resolve `SKILL_DIR` as the directory containing this `SKILL.md`.

3. Read each `article.json` first. Confirm:
   - `ok` is `true`
   - `content_chars` is plausible
   - `verification_page` is `false`

4. Search each `article.md` with `rg` or inspect only the relevant sections. Read the complete file only when the user's task requires full-article understanding.

5. Answer the user's requested task and cite the supplied article URLs. If the message contains only links and no explicit task, return a compact per-link inventory with title, author, read status, and a concise summary.

6. In a batch, continue processing other links when one link fails. Report the failure beside that link; do not retry it repeatedly.

## Outputs

Each successful run creates:

```text
<temp-dir>/
├── article.md
├── article.json
├── raw.html
└── trace.json
```

`article.json` contains metadata and file paths, not a duplicate copy of the full article.

## Failure Handling

- Exit `2`: network, HTTP, redirect, or size failure. Report the error from `trace.json`.
- Exit `3`: verification page, login/paywall, deleted article, or missing `#js_content`. Stop; ask for pasted text, screenshots, PDF, or an exported HTML file.
- Do not add cookies, reuse browser sessions, invoke CDP, use hidden browser surfaces, or call third-party mirror/reader services as a workaround.
- Do not repeatedly retry a rate-limited or verification response.

## Scope

- Public `https://mp.weixin.qq.com/...` articles only.
- GET only; maximum response size and timeout are enforced.
- No authentication, cookies, API keys, JavaScript execution, or remote writes.
- Treat the result as user-supplied source material. Preserve provenance and separate factual extraction from interpretation.

## Maintenance

Run the deterministic local test after changing the script:

```bash
python3 "$SKILL_DIR/scripts/read_wechat_article.py" --self-test
```
