---
name: tech-doc-style-chinese
description: Writing skill for Chinese technical documentation and product copy — enforces clarity, correct typography, and avoids buzzwords.
triggers:
  - rewrite this Chinese technical copy
  - improve Chinese documentation style
  - fix Chinese tech doc formatting
  - optimize Chinese product copy
  - check Chinese typography rules
  - apply Chinese writing guidelines
  - lint Chinese technical writing
  - clean up Chinese API documentation
---

# Chinese Tech Doc Style

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A reusable writing skill for Chinese technical documentation, product copy, and UI text. Enforces clarity, correct typography, proper spacing between CJK and Latin characters, and avoids common translation pitfalls and internet buzzwords.

## What This Project Does

This skill provides opinionated, practical rules for writing Chinese technical content:

- **Typography**: Correct spacing between Chinese, English, and numbers; use of corner brackets `「」` instead of curly quotes
- **Tone**: No direct address (`你`/`您`/`同学`), no marketing fluff, no buzzwords (`赋能`/`抓手`/`闭环`)
- **Translation**: Avoid mechanical translation of English status words (`Success` → `已完成`, not `成功`)
- **Structure**: Information density rules for landing pages, API docs, FAQs, changelogs
- **Linting**: Built-in zero-dependency Python script to catch violations automatically

## Installation

### Via npx (Recommended)

```bash
# Interactive install
npx skills add https://github.com/Fenng/tech-doc-style-chinese

# Non-interactive, global install to Codex
npx -y skills add https://github.com/Fenng/tech-doc-style-chinese -a codex -g
```

### Pin a specific release

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills"

git clone --depth 1 --branch v0.1.0.2.4 \
  https://github.com/Fenng/tech-doc-style-chinese.git \
  "$CODEX_HOME/skills/tech-doc-style-chinese"
```

### Local / development install

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills/tech-doc-style-chinese"
cp -R ./* "$CODEX_HOME/skills/tech-doc-style-chinese/"

# Verify
test -f "$CODEX_HOME/skills/tech-doc-style-chinese/SKILL.md" && echo "installed"
```

## Running the Lint Script

```bash
# Lint everything
python scripts/lint_copy_rules.py

# Lint specific files or directories
python scripts/lint_copy_rules.py SKILL.md NoCode-Skill.md references/
```

CI runs automatically on `pull_request` and pushes to `main` via `.github/workflows/skill-lint.yml`.

## Repository Structure

```
tech-doc-style-chinese/
├── SKILL.md                        # Skill entry point for Codex
├── NoCode-Skill.md                 # Human-readable spec (share this)
├── README.md
├── agents/
│   └── openai.yaml                 # Skill metadata
└── references/
    └── Project-Overrides.md        # Per-project customization example
```

## Core Rules Reference

### Typography & Spacing

Add a space between Chinese and English/numbers in visible body text:

```
# Wrong
支持JSON格式和XML格式

# Correct
支持 JSON 格式和 XML 格式
```

```
# Wrong
版本号为1.2.3，发布于2024年

# Correct
版本号为 1.2.3，发布于 2024 年
```

**Exception**: Do NOT apply spacing rules to code literals, JSON keys, URLs, API paths, database field names, or any machine-readable identifiers.

### Quotation Marks

Use corner brackets `「」` for visible Chinese body text, not curly quotes:

```
# Wrong
这是一个"示例"说明

# Correct
这是一个「示例」说明
```

### Avoid Direct Address

```
# Wrong
您可以通过以下步骤完成配置。
你好同学，欢迎使用本产品。

# Correct
通过以下步骤完成配置。
欢迎使用本产品。
```

### Status Word Translation

Avoid mechanical translation of English HTTP/API status terms:

| English       | Wrong         | Correct              |
|---------------|---------------|----------------------|
| Success       | 成功          | 请求已完成 / 操作成功 |
| Invalid       | 无效的        | 参数格式不正确       |
| Bad Request   | 坏请求        | 请求参数有误         |
| Forbidden     | 被禁止的      | 无访问权限           |
| Not Found     | 没有找到      | 资源不存在           |

### Banned Buzzwords

The linter flags these terms as errors in visible body text:

```
赋能  抓手  闭环  打通  沉淀  赋能  链路  颗粒度
生态  矩阵  倒逼  落地  变现  复盘  对齐  拉齐
```

### Common Chinese Typos (Lint Catches These)

| Wrong  | Correct |
|--------|---------|
| 阀值   | 阈值    |
| 登陆   | 登录    |
| 布署   | 部署    |
| 配制   | 配置    |
| 起用   | 启用    |
| 反回   | 返回    |
| 回朔   | 回溯    |
| 标示   | 标识    |
| 帐户   | 账户    |
| 帐号   | 账号    |
| 截止   | 截至    |

### Term Casing (Lint Enforces)

```
# Wrong
id  http  url  json  api  ai  JS  Js  H5  llm  aigc  rag

# Correct
ID  HTTP  URL  JSON  API  AI  JavaScript  HTML5  LLM  AIGC  RAG
```

## Content Type Guidelines

### Landing Pages & First Screens

```
# Wrong — vague, marketing-heavy
我们致力于打造业界领先的、赋能开发者的一站式 AI 平台解决方案。

# Correct — concrete, scannable
支持 REST 和 GraphQL 接口，5 分钟完成接入，每月免费额度 100 万次调用。
```

- Lead with what the product does, not what it "empowers"
- Put concrete numbers (latency, limits, pricing) above the fold
- One primary CTA per screen; button text must name the next action

### API & Parameter Docs

```markdown
## 请求参数

| 参数名    | 类型   | 必填 | 说明                          |
|-----------|--------|------|-------------------------------|
| user_id   | string | 是   | 用户唯一标识，长度 8–32 位    |
| page      | int    | 否   | 页码，从 1 开始，默认为 1     |
| page_size | int    | 否   | 每页条数，范围 1–100，默认 20 |
```

Rules:
- State type, whether required, default value, and constraints explicitly
- Use `是` / `否` for required, not `required` / `optional`
- Error codes must explain cause AND recovery action

### Error Code Docs

```markdown
## 错误码说明

| 错误码 | 说明                         | 处理建议                              |
|--------|------------------------------|---------------------------------------|
| 40001  | 缺少必填参数 `user_id`       | 检查请求体是否包含 `user_id` 字段     |
| 40301  | 当前账号无访问该资源的权限   | 联系管理员确认角色权限配置            |
| 50001  | 服务端处理超时               | 稍后重试，如持续出现请提交工单        |
```

### FAQ Pages

```
# Wrong — repeats the question
Q: 如何重置密码？
A: 重置密码的方法如下……

# Correct — answers immediately
Q: 如何重置密码？
A: 进入「账号设置」→「安全」→「修改密码」，输入手机验证码后设置新密码。
```

### Changelogs

```markdown
## v2.3.0 — 2024-03-15

### 新增
- 支持通过 API 批量导入用户，单次上限 1000 条

### 修复
- 修复在 Safari 16 下登录页闪烁的问题

### 变更
- `GET /v1/users` 返回结构新增 `created_at` 字段
```

### Button & UI Copy

```
# Wrong — abstract, duplicates surrounding heading
立即体验  了解更多  点击查看

# Correct — names the next action
开始免费试用  查看接口文档  下载 SDK
```

## Project-Level Overrides

Keep the core skill generic. Put project-specific conventions in `references/Project-Overrides.md`:

```markdown
# Project Overrides for [Your Project]

## 版本展示约定
版本号格式统一为 `vMAJOR.MINOR.PATCH`，不加「版本」二字。

## 术语表
- 「工作流」：指 Workflow 功能模块，不用「流程」
- 「智能体」：指 Agent，不用「代理」

## 文档结构偏好
- 每个功能页必须包含「适用场景」和「限制说明」两节
```

Then invoke both in your agent task:

```text
Use $tech-doc-style-chinese and references/Project-Overrides.md to rewrite this Chinese technical copy.
```

## Invoking the Skill

After installation, reference it explicitly in your task:

```text
Use $tech-doc-style-chinese to rewrite this Chinese technical copy.
Use $tech-doc-style-chinese to clean up this API error code table.
Use $tech-doc-style-chinese to optimize this landing page copy.
Use $tech-doc-style-chinese to review the FAQ section for style violations.
```

## Troubleshooting

**Lint script reports false positives on code blocks**
The script targets visible body text. Wrap code samples in fenced blocks (` ``` `); the linter skips content inside them.

**Spacing rules applied to URLs or JSON keys**
These are explicitly out of scope. If the linter flags them, they are likely outside a code block — move them inside one.

**Skill not loading after install**
Restart Codex after installation. Verify with:
```bash
test -f "$CODEX_HOME/skills/tech-doc-style-chinese/SKILL.md" && echo "OK"
```

**Team members get different lint results**
Pin to a release tag to ensure everyone runs the same version:
```bash
git clone --depth 1 --branch v0.1.0.2.4 \
  https://github.com/Fenng/tech-doc-style-chinese.git \
  "$CODEX_HOME/skills/tech-doc-style-chinese"
```

## License

MIT — see [LICENSE](./LICENSE).
