---
name: zsxq-sync
description: 同步知识星球（zsxq.com）的帖子和评论到本地 markdown 文件夹（含图片下载）。当用户说"抓一下星球 X 的新内容"、"同步星球"、"更新孤独大脑"、"把星球的最新帖子拉下来"、或想把某个知识星球做成本地知识库时触发。支持多个 group 并行配置，每次默认增量抓取。
---

# zsxq-sync — 知识星球同步

## 这个 skill 是什么

把一个或多个知识星球（zsxq.com）的帖子（含评论、图片、专栏文章、文件附件）增量同步到本地 markdown 文件夹，可直接被 Obsidian/其他 markdown 工具读取。每个 group 维护一个游标，下次只抓新内容。遇到风控会指数退避并冷却。

覆盖类型：talk / solution / task / q&a / 专栏文章（article）

## 安装

```bash
git clone https://github.com/dueti/zsxq-sync.git ~/.claude/skills/zsxq-sync
ln -sf ~/.claude/skills/zsxq-sync/zsxq-sync /usr/local/bin/zsxq-sync   # 可选，方便命令行直接调
```

## 推荐：让用户用 web 面板

模型遇到"我想把 X 星球同步到本地"或"加一个新星球"时，**首选**让用户用浏览器面板，而不是教他敲 keychain 命令。

```bash
zsxq-sync web
```

这条命令会启动 localhost:8765 并自动开浏览器。用户在网页里：
1. 点「+ 添加星球」
2. 粘链接、token、选输出目录
3. 点同步

token 直接进 macOS keychain，永不出本机也永不进对话。

模型该做的就是：
- 检查 `zsxq-sync list` 看有没有已配置的 group
- 如果用户想加新的 → 跑 `zsxq-sync web`，告诉他"浏览器里加完就好"
- 如果用户想同步已有的 → 直接 `zsxq-sync sync <group_id>` 跑完汇报

## 高级：纯命令行流程

如果用户明确说想用命令行（或在远程服务器/无桌面环境下），用这条路径：

### 1. 解析星球链接，初始化配置

```bash
zsxq-sync init <link> --non-interactive --name "孤独大脑" --output ~/Documents/Obsidian/zsxq-孤独大脑
```

### 2. 让用户保存 token（不要让用户把 token 贴进对话）

引导用户在终端跑（替换 `<group_id>` 和 token）：

```bash
security add-generic-password -s zsxq_sync_<group_id> -a $USER -w '<zsxq_access_token>'
```

token 来源：浏览器登录 wx.zsxq.com 后，从 Cookie 里拷 `zsxq_access_token` 的值。

> **重要**：模型不要要求用户把 token 发到对话里——指引他们在自己终端跑命令保存，或用 web 面板的密码框。token 只通过 keychain 或 ZSXQ_TOKEN 环境变量进入脚本，永不进入 LLM 上下文。

### 3. 首次抓取（全量）

```bash
zsxq-sync sync <group_id> --full
```

后续日常就用：

```bash
zsxq-sync sync <group_id>
```

只抓游标之后的新内容。

## 模型该怎么用这个 skill

**触发关键词**：抓星球、同步星球、更新某某星球、孤独大脑新内容、zsxq、星球到 obsidian。

**调用顺序**：
1. `zsxq-sync list` — 看有没有已配置的 group。
2. 如果用户提到的星球已存在：直接 `zsxq-sync sync <group_id>`，跑完汇报新增条数。
3. 如果是新星球：先 `zsxq-sync init <链接>`，再提示用户保存 token，再 `zsxq-sync sync <group_id> --full`。
4. 抓完读 `zsxq-sync status <group_id>` 或检查输出目录列文件，确认结果。

**风控处理**：
- 短重试（5/10/15s ×3）由脚本内置，模型无需操心。
- 超出短重试 → 进入 30 分钟长冷却。如果用户在场，模型应当告知"账号触发风控了，已冷却暂停，建议过半小时再跑"，而不是干等。
- 评论拉不到不致命，会保留 `full_comments=null`，下次再跑会跳过该条目（但帖子本身已写入），评论可能永远缺。如要补可手动重跑该条评论接口。

**不要做的事**：
- 不要要求用户在对话里粘贴 token。
- 不要无限重试。三次长冷却后必须停。
- 不要试图"加快"速度，sleep 间隔是为了避免账号被封，调短了反而更容易触发风控。

## 数据布局

- 配置：`~/.zsxq-sync/groups/<group_id>.json`（含游标、上次同步时间）
- 缓存：`~/.zsxq-sync/cache/<group_id>.json`（最近一次抓取的原始 JSON）
- 输出：用户 init 时指定的目录，每帖一个 `.md`，图片放 `_assets/`
- token：macOS keychain，service=`zsxq_sync_<group_id>`

## 自动化

加入 cron / launchd 实现每天自动同步：

```cron
0 9 * * *  /path/to/zsxq-sync sync 28512414455411 >> ~/.zsxq-sync/log 2>&1
```

token 从 keychain 取，无需在 cron 中暴露密钥。
