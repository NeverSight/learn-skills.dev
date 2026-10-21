---
name: opencode-session-visualizer
description: >
  将 OpenCode 会话导出为可视化的 HTML 网页，复刻官方 share 页面的暗色主题样式。
  从本地 SQLite 数据库提取完整对话数据（包括上下文压缩前的早期消息），
  生成的 HTML 包含 Markdown 渲染、代码高亮、工具调用折叠卡片（含完整 input/output）、
  思考过程折叠、左侧对话导航边栏、删除/截断对话功能。
  触发词：可视化会话、导出会话、会话分享、session visualizer、share session、
  导出完整对话、查看压缩前对话、生成会话网页、会话 HTML、conversation visualizer、
  opencode 会话导出、完整对话记录、删除对话、清理会话。
  当用户提到任何与会话导出、可视化、分享、完整记录查看相关的需求时都应使用此 skill。
  即使用户只说"帮我看下之前那个对话"或"导出这个会话"也应触发。
slug: nigo-opencode-session-visualizer
displayName: OpenCode会话可视化
version: 1.0.0
summary: 将 OpenCode 会话导出为可视化 HTML 网页，复刻官方 share 页面暗色主题，从本地 SQLite 提取完整对话数据含压缩前消息。
license: MIT
---

# OpenCode 会话可视化

将 OpenCode 会话从本地数据库导出，生成复刻官方 share 页面样式的单文件 HTML。

## 核心价值

OpenCode 的上下文压缩（compaction）是不可逆的——恢复会话时只能看到 checkpoint 之后的内容。
但数据库里**完整保存了所有消息**。这个 skill 直接从数据库提取完整数据，生成可分享的 HTML 网页。

## 跨平台说明

脚本支持 macOS、Linux 和 Windows。无需额外配置。

- **Python 命令**：macOS/Linux 用 `python3`，Windows 用 `python`（下方示例统一写 `python3`，Windows 用户自行替换）
- **脚本路径**：脚本通过 `__file__` 自动定位自身目录，无需关心 skill 安装在哪个路径。下方命令中的 `SKILL_DIR` 指本 skill 的安装目录（因 AI Agent 工具而异，如 `~/.claude/skills/opencode-session-visualizer/`、`~/.config/opencode/skills/opencode-session-visualizer/` 等）
- **数据库路径**（脚本自动搜索，无需手动指定）：
  - Linux: `~/.local/share/opencode/opencode.db`
  - macOS: `~/.local/share/opencode/opencode.db` 或 `~/Library/Application Support/opencode/opencode.db`
  - Windows: `%LOCALAPPDATA%\opencode\opencode.db` 或 `%APPDATA%\opencode\opencode.db`

## 工作流程

### 快速路径（推荐）

一行命令从数据库直接生成 HTML（`SKILL_DIR` = 本 skill 目录）：

```bash
python3 SKILL_DIR/scripts/generate_html.py --session <session_id> [output.html]
```

如果用户没有提供 session_id，先列出最近会话：

```bash
python3 SKILL_DIR/scripts/export_session.py --list -n 15
```

### 分步路径

1. **导出 JSON**：`python3 SKILL_DIR/scripts/export_session.py <session_id> session.json`
2. **生成 HTML**：`python3 SKILL_DIR/scripts/generate_html.py session.json [output.html]`

生成后提示用户在浏览器中打开（macOS: `open <path>`，Windows: `start <path>`，Linux: `xdg-open <path>`）。

## HTML 功能特性

生成的 HTML 是完全自包含的单文件，具备以下交互功能：

### 渲染
- **Markdown 渲染**：助手消息支持完整 Markdown（表格、代码块、列表、标题），用 marked.js
- **代码高亮**：highlight.js 语法高亮，深色主题
- **暗色主题**：背景 `#131315`，代码块 `#0b0b0c`，链接 `#89b4fa`，系统字体 13px

### 交互
- **左侧导航边栏**：列出所有用户消息摘要，点击平滑滚动跳转，滚动时自动高亮当前消息
- **工具调用卡片**：默认折叠，显示工具名+摘要（如 `read · format.ts`），点击展开显示完整 Input 和 Output（代码块样式，可滚动）
- **思考过程折叠**：reasoning 内容默认折叠，点击展开查看
- **压缩事件标记**：compaction checkpoint 显示为琥珀色卡片
- **回到顶部按钮**：长页面右下角浮动按钮

### 编辑（浏览器内操作）
- **删除消息** 🗑：悬浮用户消息显示删除按钮，删除该消息及其后续连续的助手回复
- **截断对话** ✂️：悬浮用户消息显示截断按钮，删除该消息之后的所有内容（批量删除尾部对话）
- **导出清理后的 HTML**：执行删除/截断操作后，导航栏出现导出按钮，点击下载清理后的单文件 HTML

## 数据结构

导出的 JSON 结构：

```json
{
  "session": {
    "id": "ses_xxx",
    "title": "会话标题",
    "stats": { "total_messages": 222, "user_messages": 59, ... }
  },
  "messages": [
    {
      "id": "msg_xxx",
      "role": "user|assistant",
      "timestamp": "2026-07-23 16:18:45",
      "agent": "Orchestrator",
      "model": "glm-5.1",
      "parts": [
        {"type": "text", "data": {"text": "markdown内容"}},
        {"type": "tool", "data": {"type": "tool", "tool": "bash", "callID": "...", "state": {"status": "completed", "input": {"command": "..."}, "output": "...", "title": "...", "time": {"start": 123, "end": 456}}}},
        {"type": "reasoning", "data": {"text": "思考内容"}},
        {"type": "step-start", "data": {...}},
        {"type": "step-finish", "data": {...}},
        {"type": "compaction", "data": {...}},
        {"type": "patch", "data": {...}}
      ]
    }
  ]
}
```

**Part 类型处理：**
- `text`：渲染为 Markdown（用户消息和助手消息的正文）
- `tool`：折叠卡片，显示工具名+摘要，展开显示 Input 参数和 Output 结果
- `reasoning`：折叠卡片，点击展开查看思考过程
- `step-start` / `step-finish`：步骤分隔标记（不在页面显示）
- `compaction`：琥珀色压缩事件卡片
- `patch`：代码补丁卡片
- `agent`：agent 切换标记

**Tool 的 input 字段因工具而异：**
- `read`/`edit`/`write`：`{filePath: "/path/to/file"}`
- `bash`：`{command: "ls -la"}`
- `grep`：`{pattern: "...", include: "*.ts"}`
- `glob`：`{pattern: "**/*.py"}`
- `task`：`{description: "...", prompt: "..."}`

## 文件结构

```
opencode-session-visualizer/
├── SKILL.md                      # 本文件
├── scripts/
│   ├── export_session.py         # 数据库导出脚本（session_id → JSON）
│   └── generate_html.py          # HTML 生成脚本（JSON/DB → HTML）
└── assets/
    └── template.html             # HTML 模板（含 __SESSION_DATA__ 占位符）
```

### 脚本说明

**export_session.py** — 从 opencode.db 导出完整会话数据
- `python3 export_session.py <session_id> [output.json]` — 导出指定会话
- `python3 export_session.py --list -n 15` — 列出最近 15 个会话
- session_id 支持部分匹配

**generate_html.py** — 将会话数据注入模板生成 HTML
- `python3 generate_html.py --session <session_id> [output.html]` — 直接从数据库生成（推荐）
- `python3 generate_html.py <session.json> [output.html]` — 从导出的 JSON 生成
- 模板路径自动解析为同目录下 `assets/template.html`

**template.html** — HTML 模板
- 占位符 `__SESSION_DATA__` 位于 `<script id="conv-data">` 内
- generate_html.py 将 JSON 数据注入占位符位置
- 包含完整的 CSS/JS（暗色主题、Markdown 渲染、交互功能、删除/截断/导出）
- CDN 依赖：marked.js、highlight.js、JetBrains Mono 字体

## 注意事项

- 数据库路径由脚本自动检测（见上方「跨平台说明」），通常 5GB+，查询务必带 `WHERE session_id`
- session_id 支持部分匹配（脚本会自动补全）
- 大会话（200+ 条消息）生成的 HTML 可能 5MB+，浏览器可正常处理
- 删除/截断功能在浏览器端操作，不影响原始数据库数据
- 导出清理后的 HTML 时，只包含未被删除的消息

---

> 作者：nigo
> 微信公众号：逆行的狗
