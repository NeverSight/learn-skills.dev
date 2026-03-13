---
name: scrapling
description: |
  使用 scrapling 进行网页抓取和数据提取。根据目标网站特征自动选择最佳 Fetcher，
  生成并执行 Python 脚本完成任务。Use when:
  (1) 抓取/爬取网页内容或数据（scrape, crawl, fetch page, extract data）
  (2) 需要绕过 Cloudflare/WAF 等反爬保护
  (3) 登录后抓取受保护页面
  (4) 解析已有 HTML 提取结构化数据
  (5) 用户提供 URL 并要求获取页面内容或特定元素
  (6) 批量采集多个页面
allowed-tools: Bash(python*), Bash(pip*), Bash(scrapling*)
---

# Scrapling 网页抓取 Skill

## 步骤 0：检查版本

```bash
pip show scrapling
```

- 未安装 → 执行 `pip install "scrapling[fetchers]"` + `scrapling install`
- 有新版 → 执行 `pip install --upgrade "scrapling[fetchers]"` → 查 changelog 告知用户
- 已最新 → 继续

## 步骤 1：选择 Fetcher

```
目标网站 →
│
├─ 已有 HTML 字符串/文件，只需解析?
│   → Selector（纯解析，无网络请求）
│   → 模板: parse_only.py
│
├─ 静态页面，无 JS 渲染，无反爬?
│   → Fetcher（最快，基于 curl_cffi）
│   → 模板: basic_fetch.py
│
├─ 需要登录（HTTP 表单，非 JS 登录）?
│   → FetcherSession（保持会话 cookie）
│   → 模板: session_login.py
│
├─ 有 Cloudflare / WAF 保护?
│   → StealthyFetcher（Camoufox 浏览器，自动过 CF）
│   → 模板: stealth_cloudflare.py
│
├─ SPA 应用（React/Vue），需要 JS 渲染?
│   → DynamicFetcher（Playwright 浏览器）
│   → 基于模板即时生成
│
└─ 不确定?
    → 先用 Fetcher 试，403/空内容 → 升级到 StealthyFetcher
```

## 步骤 2：执行工作流

```
1. 检查版本（步骤 0）
2. 查阅 references/site-patterns.md — 匹配已有模式则直接复用
3. 无匹配 → 用决策树选择 Fetcher
4. 读取对应模板 → 替换参数 → 生成完整脚本
5. 执行脚本 → 返回结果
6. **沉淀经验（必做）**:
   - 新站点 → 追加到 site-patterns.md
   - 新 cookie / 用户提供了 cookie → 保存到 cookie-vault.md
   - **完成抓取后必须检查**：是否有新的 cookie 或 site pattern 需要保存
```

## Cookie 格式速查

| Fetcher 类型 | Cookie 格式 | 示例 |
|-------------|-------------|------|
| Fetcher / FetcherSession | `dict` | `{'name': 'value', 'token': 'abc'}` |
| StealthyFetcher / DynamicFetcher | `list[dict]` | `[{'name': 'n', 'value': 'v', 'domain': '.site.com', 'path': '/'}]` |

**浏览器 Fetcher cookie 必填字段**: `name`, `value`, `domain`, `path`

## 超时单位速查

| Fetcher 类型 | 超时单位 | 示例 |
|-------------|---------|------|
| Fetcher / FetcherSession | 秒 | `timeout=30` |
| StealthyFetcher / DynamicFetcher | 毫秒 | `timeout=60000` |

## 模板索引

| 模板 | 文件 | 何时读取 |
|------|------|---------|
| 基础 HTTP 抓取 | `templates/basic_fetch.py` | 目标为静态页面，无反爬 |
| Cloudflare 绕过 | `templates/stealth_cloudflare.py` | 目标有 CF/WAF 保护 |
| Session 登录 | `templates/session_login.py` | 需 HTTP 表单登录后抓取 |
| 纯 HTML 解析 | `templates/parse_only.py` | 已有 HTML 字符串，只需提取数据 |

## References 索引

| 文件 | 何时读取 |
|------|---------|
| `references/site-patterns.md` | **每次抓取前先查阅** — 检查目标站点是否有已记录的模式 |
| `references/api-quick-ref.md` | 生成脚本时查阅 — Fetcher/Selector 方法签名和参数 |
| `references/troubleshooting.md` | 执行报错时查阅 — 按错误信息查找原因和解决方案 |
| `references/cookie-vault.md` | 需要登录 cookie 时查阅 — 检查是否有历史记录可复用 |
| `references/maintenance.md` | 安装/升级/依赖问题时查阅 — 安装层级和验证命令 |
