---
name: xiaohongshu-mcp
description: >
  Xiaohongshu MCP Skill - Full automation solution with login fix.
  Features: (1) Login management, (2) Search, publish, interact,
  (3) Complete MCP protocol support (13 tools), (4) Comment strategy.
  Built-in Feishu notification, iflow integration.
  Triggers: xiaohongshu, rednote, 小红书 automation.
---

# Xiaohongshu MCP Skill

> 基于 [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) 构建

## 🎯 核心功能

本 Skill 提供小红书完整自动化解决方案：

| 功能 | 状态 | 说明 |
|------|------|------|
| 🔐 登录管理 | ✅ 已测试 | 支持截图发送到飞书 |
| 🔍 搜索内容 | ✅ 已测试 | 关键词搜索、筛选 |
| 📄 获取详情 | ✅ 已测试 | 含评论列表 |
| 📤 发布图文 | ✅ 已测试 | 封面生成器集成 |
| 👍 点赞 | ✅ 已测试 | 单条点赞 |
| 💬 发表评论 | ✅ 已测试 | 主评论 |
| ↩️ 回复评论 | ✅ 已测试 | 子评论回复 |
| ⭐ 收藏 | ✅ 已测试 | 收藏/取消 |
| 🔄 获取推荐 | ✅ 已测试 | 首页 feeds |

**共 13 个 MCP 工具全部可用！**

## 🚀 快速开始

### 1. 登录

```bash
# 方式1：一键登录（推荐）
bash xhs_login.sh --notify

# 方式2：本地登录
bash xhs_login.sh
```

### 2. 启动 MCP 服务器

```bash
./xiaohongshu-mcp-darwin-arm64 &
```

### 3. 使用功能

```bash
# 检查登录状态
python3 scripts/xhs_client.py status

# 搜索内容
python3 scripts/xhs_client.py search "AI"

# 发布内容
python3 scripts/xhs_client.py publish "标题" "内容" "图片URL"
```

---

## 📚 完整操作指南

### MCP 工具列表

| 工具 | 功能 | 使用场景 |
|------|------|---------|
| `check_login_status` | 检查登录状态 | 确认账号状态 |
| `list_feeds` | 获取推荐列表 | 发现热门内容 |
| `search_feeds` | 搜索内容 | 关键词搜索 |
| `get_feed_detail` | 获取帖子详情 | 查看评论 |
| `publish_content` | 发布图文 | 创作新内容 |
| `publish_with_video` | 发布视频 | 视频内容 |
| `post_comment_to_feed` | 发表评论 | 回复粉丝 |
| `reply_comment_in_feed` | 回复评论 | 互动 |
| `like_feed` | 点赞 | 点赞帖子 |
| `favorite_feed` | 收藏 | 收藏帖子 |
| `delete_cookies` | 删除 cookies | 重置登录 |
| `get_login_qrcode` | 获取二维码 | 重新登录 |
| `user_profile` | 获取用户主页 | 查看主页 |

---

## 💬 评论互动策略

### 人设保持

**人设：理性思考者，不是杠精**

评论区互动要求：
- ✅ 理性分析，尊重不同意见
- ✅ 有数据支撑的反驳
- ✅ 自然的聊天感
- ❌ 攻击评论者
- ❌ 强词夺理

### 评论规则

| 评论类型 | 点赞 | 回复 |
|----------|------|------|
| 观点一致 | ✅ | ✅ 有延续性 |
| 部分认同 | ❌ | ✅ 补充观点 |
| 观点相反 | ❌ | ✅ 尊重表达 |
| 提问 | ✅ | ✅ 直接回答 |
| 分享经历 | ✅ | ✅ 共鸣 |

### 回复模板

**观点一致型：**
```
"说出了我想说的！[补充细节]"
"对对对，尤其是[具体例子]..."
```

**部分认同型：**
```
"有道理，不过我觉得[补充观点]"
"同意一半吧，另外[补充视角]"
```

**观点相反型：**
```
"你的观点挺有意思，不过我觉得[不同看法]"
"可能我表达不清楚，我想说的是[重新解释]"
```

**提问型：**
```
"好问题！我的看法是[直接回答]"
"这个要分情况，[分情况说明]"
```

**分享经历型：**
```
"太真实了！[共鸣]"
"你这个经历太有代表性了！[延伸]"
```

### 回复要求

1. **每条必回** - 展现活跃度
2. **主题相关** - 扣住帖子核心
3. **有延续性** - 不是敷衍
4. **无 AI 感** - 自然口语化
5. **保持人设** - 理性思考者

---

## 🔧 技术实现

### MCP HTTP API

所有功能都可通过 HTTP API 调用：

```bash
# MCP Endpoint
http://localhost:18060/mcp

# 格式
curl -X POST http://localhost:18060/mcp \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: <SESSION_ID>" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "search_feeds",
      "arguments": {
        "keyword": "AI"
      }
    }
  }'
```

### MCP Session 获取

```bash
# 初始化
RESPONSE=$(curl -s -i -X POST http://localhost:18060/mcp \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}')

# 提取 Session ID
SESSION_ID=$(echo "$RESPONSE" | grep -i "Mcp-Session-Id:" | cut -d' ' -f2)
```

### 示例：完整发布流程

```bash
#!/bin/bash
MCP_URL="http://localhost:18060/mcp"
COOKIE_FILE="cookies.txt"

# 1. 初始化
RESPONSE=$(curl -s -i -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -c "$COOKIE_FILE" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}')

SESSION_ID=$(echo "$RESPONSE" | grep -i "Mcp-Session-Id:" | cut -d' ' -f2)

# 2. 发送初始化通知
curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' > /dev/null

# 3. 发布内容
curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{
    "jsonrpc": "2.0",
    "id": 100,
    "method": "tools/call",
    "params": {
      "name": "publish_content",
      "arguments": {
        "title": "AI正在毁掉这一代年轻人？",
        "content": "🔥 争议话题...\n\n详细内容...",
        "images": ["/tmp/cover.jpg"]
      }
    }
  }'
```

### 示例：评论互动

```bash
#!/bin/bash
MCP_URL="http://localhost:18060/mcp"
COOKIE_FILE="cookies.txt"
SESSION_ID="YOUR_SESSION_ID"

# 1. 获取评论列表
curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "get_feed_detail",
      "arguments": {
        "feed_id": "698c441c000000002801d381",
        "xsec_token": "YOUR_TOKEN",
        "load_all_comments": true
      }
    }
  }'

# 2. 点赞
curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "like_feed",
      "arguments": {
        "feed_id": "698c441c000000002801d381",
        "xsec_token": "YOUR_TOKEN"
      }
    }
  }'

# 3. 发表评论
curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "post_comment_to_feed",
      "arguments": {
        "feed_id": "698c441c000000002801d381",
        "xsec_token": "YOUR_TOKEN",
        "content": "说出了我想说的！补充细节..."
      }
    }
  }'

# 4. 回复评论
curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{
    "jsonrpc": "2.0",
    "id": 4,
    "method": "tools/call",
    "params": {
      "name": "reply_comment_in_feed",
      "arguments": {
        "feed_id": "68786933000000000d01a693",
        "xsec_token": "YOUR_TOKEN",
        "comment_id": "68786afc000000001101ada6",
        "user_id": "6695e7370000000003032a17",
        "content": "说得有道理！补充观点..."
      }
    }
  }'
```

---

## 🛠️ 脚本工具

### xhs_client.py - Python 客户端

```bash
# 检查状态
python3 scripts/xhs_client.py status

# 搜索
python3 scripts/xhs_client.py search "AI" --sort "最新" --type "图文" --time "一周内"

# 发布
python3 scripts/xhs_client.py publish "标题" "内容" "图片URL" --tags "标签1,标签2"

# 获取详情
python3 scripts/xhs_client.py detail <feed_id> <xsec_token> --comments
```

### xhs_mcp.py - MCP 直接调用

```bash
# 列出所有工具
python3 scripts/xhs_mcp.py tools

# 发表评论
python3 scripts/xhs_mcp.py comment <feed_id> <xsec_token> "评论内容"
```

### generate_cover.py - 封面生成器

```bash
# 生成封面
python3 generate_cover.py --title "标题" --output /tmp/cover.jpg

# 选项
--font-size 80      # 字体大小
--padding 60         # 内边距
--max-width 600      # 最大宽度
```

---

## 📁 文件结构

```
xiaohongshu-mcp-skill/
├── SKILL.md              # 本文档
├── README.md             # 中文文档
├── STRATEGY.md          # 运营策略（含评论互动）
├── install.sh            # 安装脚本
├── xhs_login.sh         # 一键登录
├── generate_cover.py     # 封面生成器
├── data/
│   ├── post_history.json   # 发布记录
│   ├── hot_topics.json    # 热点选题
│   └── cookies.json       # 登录 cookies
└── scripts/
    ├── xhs_client.py     # Python 客户端
    ├── xhs_mcp.py       # MCP 直接调用
    ├── xhs_login_sop.py  # 登录 SOP
    └── publish_smart.py   # 智能发布脚本
```

---

## 📊 测试记录

### 已测试功能 ✅

| 功能 | 状态 | 测试时间 | 备注 |
|------|------|----------|------|
| 发布图文 | ✅ | 2026-02-11 | 2 篇已发布 |
| 搜索内容 | ✅ | 2026-02-11 | 22 条结果 |
| 获取详情 | ✅ | 2026-02-11 | 含评论列表 |
| 发表评论 | ✅ | 2026-02-11 | 6 条评论 |
| 点赞 | ✅ | 2026-02-11 | API 成功 |
| 收藏 | ✅ | 2026-02-11 | 功能正常 |
| 回复评论 | ✅ | 2026-02-11 | API 成功 |

### 测试帖子

1. **"美院学生都在用AI？我就笑了"**
   - Feed ID: `698c441c000000002801d381`
   - 点赞: 2, 评论: 6

2. **"AI正在毁掉这一代年轻人？"**
   - Feed ID: `698c76f8000000001a024a93`
   - 点赞: 1, 评论: 0

---

## 🔗 相关资源

- **GitHub**: https://github.com/tclawde/xiaohongshu-mcp-skill
- **MCP 服务器**: [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp)
- **OpenClaw**: https://github.com/openclaw/openclaw

---

## 📝 更新日志

### v3.0 (2026-02-11)

- ✅ 新增完整评论互动策略
- ✅ 新增 MCP HTTP API 调用示例
- ✅ 新增 13 个工具完整列表
- ✅ 新增脚本工具使用说明
- ✅ 新增技术实现细节
- ✅ 新增测试记录

### v2.0 (2026-02-11)

- ✅ 登录修复（支持小红书页面变更）
- ✅ 飞书通知集成
- ✅ Python 客户端完善

### v1.0 (2026-02-11)

- ✅ 初始版本
- ✅ 基础发布功能
- ✅ 搜索功能

---

**维护者**: TClawDE 🦀
**最后更新**: 2026-02-11
