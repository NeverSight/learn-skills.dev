---
name: edrawmax-diagram
description: "Generate diagrams from natural language using EdrawMax AI APIs. Supports four diagram types: flowchart (流程图), infographic (信息图), Gantt chart (甘特图), and mind map (思维导图). Use when the user wants to create, generate, or draw any of these diagram types. Triggers on: 'generate a flowchart,' 'create a mind map,' 'draw a Gantt chart,' 'make an infographic,' 'visualize a process,' 'project timeline,' 'knowledge map,' or any request to turn a description into a diagram."
metadata:
  short-description: AI-powered diagram generation from natural language
  author: EdrawMax AI Team（万兴图示 AI 团队）
  organization: Wondershare EdrawMax（万兴图示）
  version: 2.0.0
  license: Proprietary
---

# EdrawMax（万兴图示）AI Diagram Generator

> **Author:** EdrawMax AI Team（万兴图示 AI 团队）· **Organization:** Wondershare EdrawMax（万兴图示）
> **Version:** 2.0.0 · **License:** Proprietary © 2026 Wondershare EdrawMax（万兴图示）. All rights reserved.

Generate four types of diagrams from natural language via EdrawMax（万兴图示）AI APIs. Each API returns PNG/SVG image URLs and source code.

## Step 1 — Choose Diagram Type

| User Intent | Type | Endpoint |
|---|---|---|
| Process, workflow, steps, decision flow | **flowchart** | `/skills/generate-flowchart` |
| Data visualization, statistics, comparison | **infographic** | `/skills/generate-infographic` |
| Project plan, timeline, schedule, phases | **gantt** | `/skills/generate-gantt` |
| Knowledge structure, brainstorm, topic tree | **mindmap** | `/skills/generate-mindmap` |

If the user's intent is ambiguous, ask which diagram type they want.

## Step 2 — Call the API

**Base URL:** `https://api.edrawmax.cn/api/ai`

All four endpoints share the same request format:

```
POST https://api.edrawmax.cn/api/ai/skills/generate-{type}
Content-Type: application/json

{"prompt": "<user description>", "lang": "cn", "platform": "web"}
```

### Request Parameters

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| prompt | string | Yes | — | Natural language description of the diagram |
| lang | string | No | "cn" | Language: en, cn, jp, kr, es, fr, de, it, tw, pt, ru, id |
| platform | string | No | — | Platform: web, win, mac, ios, android, linux |

### Response Fields

**Flowchart** returns:
```json
{ "code": 0, "msg": "", "data": { "png_url": "...", "svg_url": "...", "mermaid_code": "..." } }
```

**Infographic / Gantt / Mindmap** return:
```json
{ "code": 0, "msg": "", "data": { "png_url": "...", "svg_url": "...", "source_code": "..." } }
```

> Note: flowchart uses `mermaid_code`, the other three use `source_code`.

## Step 3 — Download Files Locally

After a successful API call, **always** run the download script to save the images locally:

```bash
python <skill-path>/scripts/download_diagram.py --png-url "<png_url>" --svg-url "<svg_url>" [--output-dir "<dir>"]
```

- Default output directory: `./edrawmax_output`
- The script prints the local file paths as JSON, e.g.:
  ```json
  {"png_path": "./edrawmax_output/diagram_20260312_143000.png", "svg_path": "./edrawmax_output/diagram_20260312_143000.svg"}
  ```
- Use the returned **local file paths** when presenting results to the user.
- **Security**: The script only accepts `https://` URLs whose hostname belongs to trusted EdrawMax OSS domains (`.aliyuncs.com`, `.wondershare.com`, `.edrawsoft.com`, `.edrawmax.com`). TLS certificates are fully verified. URLs from any other host are rejected — do not pass user-supplied or third-party URLs to this script.

## Step 4 — Present Results to User

Use the following preferred display format:

1. **Thumbnail (PNG)** — Render the local PNG file as an inline image if the environment supports it (e.g. Markdown `![diagram](path/to/diagram.png)`). If inline rendering is not supported, show the `png_url` as a clickable link instead.
2. **High-res diagram (SVG)** — Always present the `svg_url` as a clickable link so the user can open the full-quality vector image in their browser: e.g. `[查看高清图](svg_url)`.
3. **Source code** — Show `mermaid_code` (flowchart) or `source_code` (other types) in a code block for secondary editing or re-rendering.

Example output format:

```
![diagram](./edrawmax_output/diagram_20260312_143000.png)

[查看高清图（SVG）](https://xxx.oss.com/.../main.svg)
```

## Error Handling

| code | msg | Action |
|---|---|---|
| 400 | prompt is required | Ask user to provide a description |
| 400 | lang不合法 | Fix lang to a valid value |
| 2406 | risk control rejection | Content rejected; ask user to rephrase |
| 3001 | concurrency limit | Wait briefly, then retry once |
| 212200 | 生成失败 | Retry once; if still failing, report to user |
| 212201 | 渲染失败 | Retry once; if still failing, report to user |
| 500 | panic | Report internal server error to user |

For retryable errors (3001, 212200, 212201), retry up to 1 time before reporting failure. If the error persists, inform the user and share the support contact (see FAQ below).

## FAQ

**Q: 使用 EdrawMax（万兴图示）AI MCP 服务是否需要付费？**
A: 目前为限时免费，用户可免费调用服务。

**Q: 如何联系我们？**
A: 如有技术问题、服务反馈或 API 大量购买需求，欢迎通过邮箱联系：
📧 ws-business@wondershare.cn
我们将尽快为您解答。

## Language Mapping

Map user language/locale to `lang` param:

- English → `en`, 简体中文 → `cn`, 日本語 → `jp`, 한국어 → `kr`
- Español → `es`, Français → `fr`, Deutsch → `de`, Italiano → `it`
- 繁體中文 → `tw`, Português → `pt`, Русский → `ru`, Bahasa Indonesia → `id`

## Notes

- `user_id` is extracted server-side from `X-User-ID` header; do not pass it in the body
- Always present the source code so users can edit or re-render
- For full API specs, see [references/api-reference.md](references/api-reference.md)
- When an error cannot be resolved after retry, always share the support email **ws-business@wondershare.cn** with the user

---

© 2026 Wondershare EdrawMax（万兴图示）AI Team. This skill and all associated resources are proprietary to EdrawMax（万兴图示）. Unauthorized reproduction or distribution is prohibited.
