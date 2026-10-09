---
name: web-tools-guide
description: "MANDATORY before calling web_search, web_fetch, browser, or opencli. Contains required error-handling procedures (web_search failure → must guide user to configure API), fallback chain (opencli CLI covers 70+ sites as structured fallback before browser), and site-specific login URLs. Without reading this skill, you WILL handle failures incorrectly and miss available tools. Trigger on: 搜索/上网/查资料/打开网站/抓取网页/新闻/热点/web search/fetch/browser/opencli."
---

<!-- baseDir = /root/.openclaw/workspace/skills/web-tools-guide -->

# Web 工具策略

遵循 ReAct 范式。**四个工具不是层级关系，是分支决策**：

```
┌─ 没有 URL，需要搜索 ──────→ web_search   （关键词搜索）
│
├─ 已知 URL，静态内容 ──────→ web_fetch    （直取页面）
│
├─ 以上失败 / 不适用 ──────→ opencli      （CLI 结构化访问，70+ 站点）
│
└─ 全都不行 ───────────────→ browser      （浏览器自动化，兜底）
```

先按场景选 web_search 或 web_fetch；失败时先试 opencli，最后才上 browser。
每次切换工具告知用户原因，不要静默降级。

---

## 决策流程

```
有明确 URL？
├─ YES → 静态内容（文章/文档/API/RSS）？
│        ├─ YES → web_fetch
│        │        失败（空白/403/CAPTCHA）？→ opencli → browser
│        └─ NO（需要 JS/登录/交互/截图）→ opencli → browser
└─ NO  → web_search
         ├─ 成功 → 对结果 URL 按上述逻辑选 fetch/opencli/browser
         ├─ 失败（API 错误）→ 引导配置（见"web_search 失败处理"）
         └─ 无结果/不适用 → opencli → browser
```

---

## web_search

**何时用**：没有明确 URL，需要搜索信息（新闻、热点、查资料、比较信息）。

**怎么用**：直接调用 `web_search`，传入搜索关键词。

**结果处理**：返回的 URL 按决策流程选 `web_fetch`、`opencli` 或 `browser` 深入获取。

**失败时**：见下方"web_search 失败处理"。

---

## web_fetch

**何时用**：已知 URL，页面为静态内容——新闻文章、博客、技术文档、API 端点、RSS 源。

**怎么用**：直接调用 `web_fetch`，传入 URL。

**失败信号**：返回空白页、403、CAPTCHA、骨架 HTML → 尝试 `opencli`，仍不行再升级到 `browser`。

---

## opencli（Fallback，优先于 browser）

**何时用**：web_search / web_fetch 失败或不适用时，先试 opencli 再考虑 browser。覆盖 70+ 主流网站，秒级返回结构化数据。

**首次使用前**：如果执行 `opencli` 提示 command not found，需要先运行安装脚本（幂等，可重复运行）：
```bash
bash {baseDir}/scripts/setup-opencli.sh
```
该脚本会自动完成：安装 opencli CLI → 编译 Browser Bridge 插件 → 重启浏览器加载插件。

**渐进式发现（不需要记命令）**：
```bash
opencli --help                    # 有没有这个站？
opencli <site> --help             # 这个站能做什么？
opencli <site> <command> --help   # 这个命令怎么用？
```

**详细用法**：`read {baseDir}/references/opencli-guide.md`

**失败时**：告知用户 opencli 失败原因，降级到 browser。

---

## browser（最后手段）

这是最重量级的工具，也是当前问题最多的场景。以下是详细操作指引。

### 何时用

- **JS 渲染页面**：SPA、动态加载内容（微博 feed、知乎回答、小红书瀑布流）
- **需要登录态**：登录后才可见的内容、管理后台
- **页面交互**：点击按钮、填写表单、翻页、滚动加载更多
- **截图需求**：需要页面视觉信息
- **其他工具全部失败的兜底**

### 操作流程

**信息获取（只读）：**
1. 导航到目标 URL
2. 等待关键元素出现（不要用固定时间等待）
3. 提取所需内容（文本、链接、图片等）
4. 返回结果给用户

**登录操作：**
1. 查找登录页 URL → `read {baseDir}/references/well-known-sites.json`
2. **告知用户即将执行登录操作，获取确认**
3. 导航到登录页
4. 填写凭证（用户提供）或提示用户扫码
5. 等待登录成功，确认后继续后续操作

**页面交互：**
1. 导航到目标页面
2. 使用 CSS 选择器定位元素（辅以文本内容匹配）
3. 执行交互：点击、输入、选择、滚动
4. 等待响应/页面变化
5. 提取结果或截图

### 关键注意事项

- **登录操作必须获得用户授权** — 任何涉及账号登录的操作前，先告知用户并等待确认
- **敏感操作必须二次确认** — 发帖、删除、支付等不可逆操作
- **优先 CSS 选择器** — 比 XPath 更稳定，辅以文本匹配
- **智能等待** — 等待目标元素出现，而非 `sleep(3)` 式固定等待
- **CAPTCHA/验证码** — 无法自动处理时告知用户需手动介入
- **页面加载超时** — 设置合理超时，失败时告知用户并建议重试
- **多步操作保持状态** — 登录后的后续操作复用同一浏览器上下文，不要重新打开

---

## web_search 失败处理

**当 `web_search` 返回错误时，不要静默降级，必须引导配置：**

1. **`read {baseDir}/references/web-search-config.md`**
2. 按文件中 Step 1 **原样输出**配置引导给用户（不要改写表格或省略内容）
3. 等待用户回复：
   - 用户提供 API Key → 再次 `read {baseDir}/references/web-search-config.md`，按 Step 2-5 执行
   - 用户说"暂不配置" → 进入降级方案
   - 其他回复 → 正常响应
4. **降级方案**（仅在用户明确拒绝配置后）：
   - `read {baseDir}/references/well-known-sites.json` 获取常用网站 URL
   - 用 `web_fetch` 直接获取目标网站内容
   - 仍不行 → 升级到 `browser`

---

## 常用网站

需要常用网站 URL 时（登录页、搜索引擎、热搜榜等）：

```
read {baseDir}/references/well-known-sites.json
```

通过 key 查找（如 `social.weibo.login`、`search.baidu`）。带 `{query}` 的 URL 替换为实际搜索词。
