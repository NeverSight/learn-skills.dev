---
name: content-extract
description: Robust URL-to-Markdown extraction for OpenClaw workflows. Use when the user wants to "extract/summarize/convert a webpage to markdown" (especially WeChat mp.weixin.qq.com) and web_fetch/browser is blocked or messy. Uses a cheap probe via web_fetch first, then falls back to the official MinerU API (via the local mineru-extract skill) and returns a traceable result contract with source links.
---

# content-extract — 上层内容解析入口（MCP 语义对齐，但不跑 MCP Server）

目标：把“给我一个 URL → 产出可读 Markdown + 可追溯入口”变成一个**统一入口**，供后续所有业务 skill（github-explorer、写作类 skills、日报等）复用。

核心原则（来自你发的 Excel Skill 拆解文章的启发）：

- **行为规约层**：永远给出可追溯入口（原文 URL + 解析产物路径/链接），绝不编造来源。
- **Token 探针**：先用低成本 probe 判断可不可以直接抓；不行再走重解析（MinerU）。
- **反弹机制**：失败时返回“下一步动作建议”，而不是一堆异常栈。

## 工作流（Decision Tree）

输入：`url`

0) **Domain Whitelist（跳过 probe）**：若 URL 属于高概率反爬/动态站点（微信/知乎等），直接走 MinerU

- 白名单文件：`references/domain-whitelist.md`
- 对命中白名单的 URL：强制 `model_version=MinerU-HTML`

1) **Probe（低成本）**：优先用 `web_fetch(url)`

- 目标：拿到正文 markdown（便宜、快）
- 判断“失败/不合格”条件（见 `references/heuristics.md`）包括：
  - 403/401/反爬
  - 只有“环境异常/验证码/请在微信打开”等提示
  - 内容极短/明显导航页/丢正文

2) **Fallback（高保真）**：走 MinerU 官方 API

- 调用下游 driver：`skills/mineru-extract/scripts/mineru_parse_documents.py`
- 对 HTML 页面（微信等）：强制 `model_version=MinerU-HTML`

3) **输出统一结果合同（Result Contract）**

无论用 probe 还是 MinerU，都返回同一套结构：

```json
{
  "ok": true,
  "source_url": "...",
  "engine": "web_fetch" ,
  "markdown": "...",
  "artifacts": {
    "out_dir": "...",
    "markdown_path": "...",
    "zip_path": "..."
  },
  "sources": [
    "原文URL",
    "（如使用MinerU）MinerU full_zip_url",
    "（如使用MinerU）本地markdown_path"
  ],
  "notes": ["任何重要限制/失败原因/下一步建议"]
}
```

> 注意：`engine` 可能是 `web_fetch` 或 `mineru`。

## MinerU 调用（给 agent 的确定性脚本）

当需要 MinerU 时，用这个命令（返回 JSON，且可把 markdown 内联进 JSON，便于下游总结）：

```bash
python3 mineru-extract/scripts/mineru_parse_documents.py \
  --file-sources "<URL>" \
  --model-version MinerU-HTML \
  --emit-markdown --max-chars 20000
```

> **路径说明**: 上述命令假设你在 skills 安装根目录下执行。如果 mineru-extract 安装在其他位置，请替换为实际路径。

## 交付规范（强制）

- 输出必须包含 `sources`（原文入口 + 解析产物入口）。
- 如果 MinerU 成功：必须把 `markdown_path`（本地路径）写进 `sources`，方便复查。
- 如果两条链路都失败：必须明确失败原因，并给出下一步（例如：让 Boss 提供可访问镜像链接 / 允许我用浏览器 relay 导出 HTML / 走上传 HTML 文件解析的兜底方案）。

## 本 skill 自身不做什么

- 不跑 MCP Server（避免常驻服务与运维负担）
- 不试图绕过登录/验证码（这属于访问层问题；我们只做解析层和工作流路由）

## References

- MinerU API docs: https://mineru.net/apiManage/docs
- MinerU output files: https://opendatalab.github.io/MinerU/reference/output_files/
