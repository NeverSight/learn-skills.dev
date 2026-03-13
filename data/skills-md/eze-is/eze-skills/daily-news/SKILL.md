---
name: daily-news
description: |
  每日资讯日报生成器。三阶段工作流：获取元数据、生成摘要、输出日报。
  触发场景：每日新闻、资讯日报、信息监控、新闻聚合、daily news、生成日报。
  也用于添加新信源（自动分析网页并生成 method 文件）。
---

# Daily News

三阶段工作流：**获取元数据** → **生成摘要** → **输出日报**

## 工作目录

首次运行询问工作目录路径（如 `~/daily-news`），后续记住。

```
<workspace>/
├── profile.yaml          # 用户画像（关于我、关注什么）
├── settings.yaml         # 日报设置（语言、格式偏好）
├── methods/              # 信源获取方法
├── data/news.db          # SQLite 数据库
└── output/YYYY-MM-DD.md  # 日报输出
```

初始化：
```bash
mkdir -p <workspace>/methods <workspace>/data <workspace>/output
cp references/examples/settings.example.yaml <workspace>/settings.yaml
cp references/examples/profile.example.yaml <workspace>/profile.yaml
python3 scripts/db.py init --db <workspace>/data/news.db
```

初始化完成后：
1. 将工作目录写入用户的 `~/.claude/CLAUDE.md`，追加一行：
   ```
   - daily-news skill 的项目目录在：<workspace>
   ```
   这样后续新会话无需再询问目录位置。
2. 询问用户是否需要调整画像。

---

## 阶段 0：选择抓取日期范围（新增）

在执行抓取前，询问用户日期范围，从源头减少非必要工作量。

### 日期范围选项

```
请选择抓取时间范围：
1. 今天（默认）                    → published_at >= 今天
2. 昨天                            → published_at >= 昨天
3. 最近3天                         → published_at >= 3天前
4. 最近7天                         → published_at >= 7天前
5. 从上次抓取至今（增量）          → published_at >= last_fetched_date
6. 自定义日期范围                  → 输入开始日期
```

### 增量抓取逻辑

**每个信源独立追踪抓取日期**：

```yaml
# methods/twitter-karpathy.yaml
source_id: twitter-karpathy
...

# 自动维护的元数据
last_fetched_date: "2026-01-27"    # 上次抓取日期
last_fetched_count: 5               # 上次抓取数量
total_items_fetched: 127            # 累计总数
```

**数据库记录**：
- `source_status` 表：快速查询上次抓取日期
- `source_sync_log` 表：详细同步日志

### 日期筛选执行流程

```bash
# 1. 获取上次抓取日期
python3 scripts/db.py source-status --db <db> --source <source_id>

# 2. 执行增量抓取
# 在 method 执行时传入 since 参数

# 3. 记录同步日志
python3 scripts/db.py add-items-incremental \
  --db <db> \
  --source <source_id> \
  --items '<json>' \
  --since "2026-01-27"
```

---

## 阶段 1：获取元数据（增量优化）

遍历 `<workspace>/methods/` 目录，执行每个 method 文件。

### 增量抓取检查

对每个 method，执行前检查：

```bash
# 1. 读取 method 文件中的 last_fetched_date
python3 -c "
import yaml
with open('methods/<source>.yaml') as f:
    config = yaml.safe_load(f)
print(config.get('last_fetched_date', 'never'))
"

# 2. 或查询数据库
python3 scripts/db.py source-status --db <db> --source <source_id>
```

### 根据日期范围执行

**情况 A：method 有上次日期，且用户选择"增量"**
```bash
# 只抓取 last_fetched_date 之后的内容
# 在 method 执行时传入 since 参数
```

**情况 B：method 首次抓取，或用户选择"今天/最近N天"**
```bash
# 使用用户指定的日期范围
```

### 双层去重机制

**第一层：抓取时过滤**（阶段 1）
```bash
# 在 method 执行时，只返回 published_at > since 的内容
```

**第二层：入库前检查**（阶段 1.5）
```bash
# 批量检查 URL 是否已存在
python3 scripts/db.py check-existing \
  --db <db> \
  --urls '["url1", "url2", ...]'

# 返回已存在的 URL 列表
```

**第三层：数据库 UNIQUE 约束**（最终保护）
```sql
-- items 表的 url 字段有 UNIQUE 约束
INSERT INTO items ...  -- 重复 URL 会触发 IntegrityError
```

### 入库并记录

```bash
python3 scripts/db.py add-items-incremental \
  --db <db> \
  --source <source_id> \
  --items '<json>' \
  --since "2026-01-27"
```

此命令会：
1. 批量检查 URL 是否存在（预去重）
2. 插入新条目
3. 记录同步日志到 `source_sync_log` 表
4. 更新 `source_status` 表的 `last_fetched_date`
5. 更新 method 文件的元数据字段

### Browser MCP 检查与自动配置

执行前先检查是否有信源需要 Browser MCP（`extends: browser-smart` 或 `detail_method: browser`）：

**如果有，执行以下检查流程：**

#### 1. 检查 MCP 是否已配置

```bash
# 检查 ~/.claude.json 中是否有 browsermcp 配置
grep -q '"browsermcp"' ~/.claude.json && echo "configured" || echo "not configured"
```

**如果未配置，自动添加：**

```bash
# 读取现有配置，在 mcpServers 中添加 browsermcp
# 使用 Python 或 jq 修改 JSON
python3 -c "
import json
config_path = '$HOME/.claude.json'
with open(config_path, 'r') as f:
    config = json.load(f)
if 'mcpServers' not in config:
    config['mcpServers'] = {}
if 'browsermcp' not in config['mcpServers']:
    config['mcpServers']['browsermcp'] = {
        'command': 'npx',
        'args': ['@browsermcp/mcp@latest'],
        'type': 'stdio'
    }
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    print('Browser MCP 配置已添加，请重启 Claude Code 生效')
else:
    print('Browser MCP 已配置')
"
```

#### 2. 测试连接状态

```
调用 mcp__browsermcp__browser_snapshot 测试连接
```

**判断结果：**
- 返回包含 `Page URL:` → 已连接，继续执行
- 返回 `No connection to browser extension` → 未连接
- 返回 `mcp__browsermcp__browser_snapshot is not a function` 或类似错误 → MCP 未加载

#### 3. 根据状态处理

**MCP 未加载（刚添加配置）：**
```
Browser MCP 配置已添加。请：
1. 重启 Claude Code（Ctrl+C 退出后重新运行）
2. 重启后再次运行日报生成
```

**MCP 已加载但未连接：**
```
Browser MCP 未连接到浏览器。请：
1. 安装 Chrome 扩展：https://chromewebstore.google.com/detail/bjfgambnhccakkhmkepdoekmckoijdlc
2. 在 Chrome 中点击扩展图标，点击 "Connect" 按钮
3. 然后重新运行

或者跳过这些信源，只处理 RSS/WebFetch 信源？
```

用户可选择跳过或等待连接后继续。

**必须使用 `mcp__browsermcp__*`**，因为它复用用户浏览器的登录态，可访问需要登录的内容。其他浏览器工具（playwright/chrome-devtools）会启动独立实例，无法使用已登录的账号。

### Method 执行逻辑

读取 method 文件的元数据，根据 `extends` 字段决定执行方式：

**有 extends（引用通用方法）：**
```bash
# extends: rss（最快，有 RSS 源时首选）
python3 references/methods/rss.py --url "<source_url>"

# extends: webfetch-smart（快，适用大多数网站）
# 读取 references/methods/webfetch-smart.md 按指引操作

# extends: browser-smart（Browser MCP，JS渲染/需登录）
# 读取 references/methods/browser-smart.md 按指引操作
# 注意：需要用户先点击 Browser MCP 扩展连接
```

**无 extends（完整定制）：**
- `*.py`: 直接执行 `python3 <file>`
- `*.md`: 读取内容，按指引操作浏览器

### 入库

```bash
python3 scripts/db.py add-items \
  --db <workspace>/data/news.db \
  --source <source_id> \
  --items '<JSON>'
```

---

## 阶段 2：生成摘要

```bash
python3 scripts/db.py list-pending --db <workspace>/data/news.db
```

对每条内容，根据 method 文件的 `detail_method` 字段获取正文：

| detail_method | 获取方式 |
|---------------|---------|
| `fetch` | WebFetch 工具（快） |
| `browser` | Browser MCP（慢，需手动连接） |
| 未指定 | 默认 `fetch` |

按 `references/prompts/summary.md` 生成摘要，更新数据库：
```bash
python3 scripts/db.py update-summary \
  --db <workspace>/data/news.db \
  --id <item_id> \
  --data '<摘要JSON>'
```

---

## 阶段 3：生成日报

```bash
python3 scripts/db.py list-today --db <workspace>/data/news.db
```

读取 `<workspace>/profile.yaml`，按 `references/prompts/report.md` 生成日报。
输出到 `<workspace>/output/YYYY-MM-DD.md`。

---

## 用户画像

画像用于评估内容相关度，自然语言描述，没有固定格式。

### 首次设置

初始化时已创建空白 `profile.yaml`，询问用户是否需要调整：
- 你是做什么的？
- 最近在关注什么？
- 有什么不想看的？

根据回答更新 `<workspace>/profile.yaml`。

### 更新画像

用户说"更新画像"时：
- 询问最近有什么变化
- 工作方向？新的兴趣点？
- 更新 profile.yaml

### 画像格式

```yaml
about: |
  （关于我：身份、工作）

focus: |
  （当前关注：最近在意的话题）

low_priority: |
  （不太关心：降低优先级的内容）
```

---

## 添加信源

按优先级依次尝试：

1. **检查 RSS**
   - 尝试 `/feed`、`/rss`、`/atom.xml` 等常见路径
   - 或检查页面 `<link rel="alternate" type="application/rss+xml">`
   - 有则用 `extends: rss`

2. **测试 WebFetch**
   - 用 WebFetch 工具获取页面，看能否提取文章列表
   - 成功则用 `extends: webfetch-smart`

3. **使用浏览器**
   - WebFetch 失败（JS 渲染/反爬/需登录）
   - 用 `extends: browser-smart`
   - 使用 Browser MCP，直接用用户浏览器的登录态

创建 method 文件，详见 `references/schemas/method.md`

---

## 参考资料

| 资料 | 路径 | 加载时机 |
|------|------|---------|
| Method 规范 | `references/schemas/method.md` | 添加信源时 |
| 摘要提示词 | `references/prompts/summary.md` | 阶段 2 |
| 日报提示词 | `references/prompts/report.md` | 阶段 3 |
| 通用方法 | `references/methods/` | 阶段 1（被 extends 引用） |
| 日报设置示例 | `references/examples/settings.example.yaml` | 初始化 |
| 画像格式参考 | `references/examples/profile.example.yaml` | 初始化时 |
| **网站模板** | **`references/website-template/`** | **创建网站时** |
| **Method 元数据示例** | **`references/examples/method-with-metadata.example.yaml`** | **增量抓取配置参考** |

## 数据库命令参考

### 增量抓取相关

```bash
# 批量检查 URL 是否已存在
python3 scripts/db.py check-existing --db <db> --urls '["url1", "url2"]'

# 增量添加条目（自动记录日志）
python3 scripts/db.py add-items-incremental \
  --db <db> --source <id> --items '<json>' --since "2026-01-27"

# 查看信源同步状态
python3 scripts/db.py source-status --db <db> --source <id>

# 查看同步日志
python3 scripts/db.py sync-log --db <db> --source <id> --limit 10
```

### 数据库迁移

```bash
# 升级到 V2（添加增量抓取支持）
sqlite3 <db> < scripts/migrate_v2.sql
```

---

## 依赖

```bash
pip install pyyaml feedparser requests beautifulsoup4
```

浏览器方式（browser-smart）使用 Browser MCP，需安装 Chrome 扩展。

---

## 网站部署（可选）

日报生成后，可自动部署到网站。

### 快速开始

使用内置网站模板：

```bash
# 复制模板到工作目录
cp -r references/website-template <workspace>/website
cd <workspace>/website
python3 build.py
```

### 目录结构

```
<workspace>/
├── output/              # 日报 Markdown 输出
└── website/             # 网站项目
    ├── build.py         # 构建脚本（来自模板）
    ├── dist/            # 生成的静态网站
    └── README.md        # 部署指南
```

### 模板位置

- **模板路径**: `references/website-template/`
- **包含文件**:
  - `build.py` - 将 Markdown 转换为终端风格 HTML
  - `README.md` - 部署指南

### 模板特点

- **终端风格** - 黑色 header + 白色内容区
- **响应式设计** - 适配手机和桌面
- **日期导航** - 支持历史日报切换
- **零依赖** - 纯 Python，无需第三方库

### 部署平台支持

- Cloudflare Pages（推荐）
- GitHub Pages
- Vercel
- Netlify
- 任何静态托管服务

### 首次创建网站

选择"创建网站"时自动执行：

1. **复制模板**:
   ```bash
   cp -r references/website-template <workspace>/website
   cd <workspace>/website
   python3 build.py
   ```

2. **初始化 Git**:
   ```bash
   git init
   git add -A
   git commit -m "Initial commit"
   gh repo create daily-news-web --public --source=. --push
   ```

3. **配置 Cloudflare Pages**:
   - Build command: `python3 build.py`
   - Build output: `dist`

### 日报生成后的流程

**阶段 3 完成后**，检查是否存在 website 目录：

#### 情况 A：website 不存在

询问用户是否需要创建网站：
```
日报已生成：output/2026-01-28.md

是否需要部署到网站？
1. 是，创建网站（Cloudflare Pages）
2. 否，仅保存 Markdown
```

#### 情况 B：website 已存在

询问用户如何更新：
```
日报已生成：output/2026-01-28.md

网站更新选项：
1. 立即构建并推送（自动部署到 Cloudflare）
2. 仅构建，稍后手动推送
3. 不更新网站
```

### 自动推送命令

选择"立即构建并推送"时执行：

```bash
cd <workspace>/website
python3 build.py
git add -A
git commit -m "Add daily report for $(date +%Y-%m-%d)"
git push origin main
```

Cloudflare Pages 检测到 `main` 分支推送后自动重新部署。

### 手动推送流程

如果用户选择稍后手动推送：

```bash
# 随时手动执行
cd <workspace>/website
python3 build.py                    # 重新构建网站
git add -A
git commit -m "Add report for YYYY-MM-DD"
git push origin main                # 触发 Cloudflare 部署
```

### 网站配置

首次创建网站时需配置：

1. **GitHub 仓库**：推送 website 目录到 GitHub
2. **Cloudflare Pages**：
   - 连接 GitHub 仓库
   - Build command: `python3 build.py`
   - Build output: `dist`
3. **自定义域名**（可选）：在 Cloudflare Pages 设置中添加

详细配置见 `<workspace>/website/README.md`

### 自定义模板

如需修改网站样式，编辑 `<workspace>/website/build.py` 中的 CSS 变量。

原始模板保留在 `references/website-template/` 供参考。
