---
name: fill-content
description: 筛出 mixdao 无正文条目（hasContent 为 false），按 URL 抓取正文；上传前用 AI 梳理为约 250 字案例描述（简体中文、突出人物/公司等）并以此替代正文回写。需 MIXDAO_API_KEY；更新时另需 ANTHROPIC_API_KEY。触发示例：「补全正文」「拉取无正文条目的正文并更新」「fill content」「无正文」「抓正文」「补全内容」「更新正文」「mixdao 正文」。
---

## 何时使用

用户说要**补全正文**、**拉取/抓取无正文条目的正文并更新到 mixdao**、或提到 **fill content / 无正文 / hasContent** 时使用本 skill。

# 补全正文（Fill Content）

根据 URL 抓取正文，上传前用 AI 梳理为约 250 字案例描述并替代正文回写到 mixdao，仅处理当前尚无正文的条目。

## 脚本

| 脚本 | 作用 |
|------|------|
| `scripts/01-fetch-no-content.js` | 拉取 mixdao `GET /api/latest`，过滤出 `hasContent === false` 的条目，写入 `temp/fill-content-{date}.json`。 |
| `scripts/02-fetch-content.js` | 读取 01 输出的 JSON，抓取每个 URL 的正文，保存到 `temp/{cachedStoryId}.txt`。 |
| `scripts/03-update-from-temp.js` | 从 temp 读取正文，上传前用 AI 梳理为约 250 字案例描述并以此替代正文 PATCH 更新。**list 必须传 JSON 路径**，输出元数据与正文摘要供 Agent 判断；**更新必须传至少一个 id**，可一次传多条。 |

## 流程

### 步骤 1：获取无正文条目

```bash
node scripts/01-fetch-no-content.js
```

输出：`temp/fill-content-{date}.json`（示例：`temp/fill-content-2026-02-17.json`）

### 步骤 2：批量抓取正文

```bash
node scripts/02-fetch-content.js temp/fill-content-2026-02-17.json
```

- 自动抓取每个 URL 的内容（先 curl，失败时用 Playwright 无头浏览器兜底）
- 保存到 `temp/{cachedStoryId}.txt`
- 过滤无效内容（404、登录页等）
- 可中途停止，下次运行会跳过已存在的文件

### 步骤 3：预览待更新内容（含元数据，供 Agent 做语义判断）

```bash
# 推荐：传入步骤 1 的 JSON 路径，输出每条 title、translatedTitle、text 与正文摘要
node scripts/03-update-from-temp.js list temp/fill-content-2026-02-17.json
```

- 必须传 JSON ：每条输出 `cachedStoryId`、`title`、`translatedTitle`、`text`（截断）、`contentLength`、`contentPreview`（正文前 300 字）。**是否与文章主题一致由 Agent 根据上述信息自行判断**；其中需排除内容仅为导航/框架、未包含实际正文的条目。存疑条目可在步骤 4 选择不更新。

### 步骤 4：更新到 mixdao

Agent 做好主题判断后，只更新判定为一致的条目，**一次传入多个 cachedStoryId**。脚本会先用 AI 将每条正文梳理为约 250 字（简体中文、突出人物/公司等），**提交到 mixdao 的是该梳理结果**，而非原始长正文。运行前需设置 `ANTHROPIC_API_KEY`（与 daily-briefing 一致）。

```bash
# 更新指定的一条或多条（推荐：判断后只传通过的 id）
node scripts/03-update-from-temp.js <id1> <id2> <id3>
```

示例：`node scripts/03-update-from-temp.js cmlpr8xsb005al70adaskpzl4 cmlpr8xd7002jl70ax1ytgrrt`
