---
name: xiaohongshu-workflow
description: |
  小红书全流程运营工作流。使用场景：
  - 账号配置和登录设置
  - 内容策划与发布（图文、视频）
  - 热点追踪与话题监控
  - 互动管理与自动回复
  - 数据分析与运营优化
  - "帮我配置小红书账号"
  - "发布一篇小红书笔记"
  - "跟踪小红书上的XX热点"
  - "生成小红书运营报告"
  - "分析我的小红书账号表现"
---

# 小红书全流程运营工作流

基于 [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) 构建的完整运营工作流。

## 工作流决策树

```
用户请求
├── 配置/登录 → 【账号配置】
├── 发布内容 → 【内容发布】
├── 搜索/监控 → 【热点追踪】
├── 互动管理 → 【互动管理】
└── 数据分析 → 【数据分析】
```

## 1. 账号配置

### 1.1 安装 MCP 服务

```bash
# 下载 xiaohongshu-mcp（Linux x64）
wget https://github.com/xpzouying/xiaohongshu-mcp/releases/latest/download/xiaohongshu-mcp-linux-amd64.tar.gz
wget https://github.com/xpzouying/xiaohongshu-mcp/releases/latest/download/xiaohongshu-login-linux-amd64.tar.gz

# 解压到 ~/.local/bin
mkdir -p ~/.local/bin
tar -xzf xiaohongshu-mcp-*.tar.gz -C ~/.local/bin/
tar -xzf xiaohongshu-login-*.tar.gz -C ~/.local/bin/

# 重命名并添加执行权限
cd ~/.local/bin
mv xiaohongshu-mcp-* xiaohongshu-mcp
mv xiaohongshu-login-* xiaohongshu-login
chmod +x xiaohongshu-mcp xiaohongshu-login
```

### 1.2 登录获取 Cookies

**方式一：本地桌面环境**
```bash
xiaohongshu-login  # 打开浏览器，用小红书 App 扫码登录
```

**方式二：Linux 服务器（无桌面）**

在本地电脑（Windows/Mac）获取 cookies：
```bash
# 下载 Windows 版本
wget https://github.com/xpzouying/xiaohongshu-mcp/releases/latest/download/xiaohongshu-login-windows-amd64.zip
unzip xiaohongshu-login-windows-amd64.zip

# 运行登录
.\xiaohongshu-login-windows-amd64.exe
# Cookies 保存在 C:\Users\<用户名>\AppData\Local\Temp\cookies.json

# 复制到服务器
scp /mnt/c/Users/<用户名>/AppData/Local/Temp/cookies.json user@server:~/.xiaohongshu/
```

### 1.3 启动 MCP 服务

```bash
# 启动服务（headless 模式）
xiaohongshu-mcp

# 检查状态
curl http://localhost:18060/mcp

# 查看日志
tail -f ~/.xiaohongshu/mcp.log
```

### 1.4 配置到 OpenClaw

将 skill 目录链接到 OpenClaw workspace：
```bash
ln -s /path/to/xiaohongshu-workflow ~/.openclaw/workspace/skills/xiaohongshu-workflow
```

---

## 2. 内容发布

### 2.1 发布流程

```
策划主题 → 收集素材 → 撰写内容 → 生成图片 → 发布 → 监控
```

### 2.2 内容规范

| 项目 | 限制 |
|------|------|
| 标题 | ≤20 字符 |
| 正文 | ≤1000 字符 |
| 图片 | 最多 18 张 |
| 视频 | ≤15 分钟 |
| 每日发布 | ≤50 条 |

### 2.3 发布图文笔记

使用 MCP 工具 `publish_content`：

```bash
# 通过脚本调用
./scripts/publish.sh \
  --title "标题" \
  --content "正文内容" \
  --images "/path/to/image1.jpg,/path/to/image2.jpg" \
  --tags "标签1,标签2"
```

**Python 调用示例：**
```python
import requests

def publish_note(title, content, images, tags=None):
    """发布小红书图文笔记"""
    payload = {
        "title": title,
        "content": content,
        "images": images,  # 图片路径列表
        "tags": tags or []
    }
    
    response = requests.post(
        "http://localhost:18060/mcp",
        json={"tool": "publish_content", "params": payload}
    )
    return response.json()
```

### 2.4 内容策略

**发布主题类型：**
1. 教程类：使用指南、技巧分享
2. 案例类：实际应用、成功故事
3. 热点类：行业动态、趋势分析
4. 互动类：问答、投票、征集

**最佳发布时间：**
- 工作日：9:00-11:00, 18:00-20:00
- 周末：10:00-12:00, 19:00-21:00

**内容质量原则：**
- 标题吸引眼球（数字、疑问、感叹）
- 首图决定点击率
- 正文简洁有价值
- 标签精准覆盖

---

## 3. 热点追踪

### 3.1 搜索内容

```bash
# 通过脚本搜索
./scripts/search.sh "关键词" --limit 20

# MCP 调用
curl -X POST http://localhost:18060/mcp \
  -H "Content-Type: application/json" \
  -d '{"tool": "search_feeds", "params": {"keyword": "关键词", "limit": 20}}'
```

### 3.2 热点报告生成

```bash
# 生成热点追踪报告
./scripts/track-topic.sh "话题" --limit 10 --output report.md
```

**报告内容包括：**
- 概览统计（帖子数、点赞数、评论数）
- 热帖详情（标题、作者、正文、热门评论）
- 评论区热点关键词
- 趋势分析

### 3.3 定时监控

配置 OpenClaw Heartbeat 进行定时监控：

```markdown
# 在 HEARTBEAT.md 中添加
## 小红书监控

**触发条件：** 每 4-6 小时

- [ ] 检查账号帖子表现
- [ ] 搜索相关话题动态
- [ ] 记录数据变化
- [ ] 发现热点时通知
```

---

## 4. 互动管理

### 4.1 获取帖子详情

```bash
./scripts/post-detail.sh <note_id> <xsec_token>
```

### 4.2 发表评论

```bash
./scripts/comment.sh <note_id> <xsec_token> "评论内容"
```

### 4.3 回复策略

**需要回复：**
- 真实提问
- 技术咨询
- 功能建议
- 使用问题

**不需要回复：**
- 垃圾广告
- 纯表情符号
- 无意义评论
- 重复评论

**回复模板：**
```
👋 感谢关注！

[针对问题简要回答]

📚 更多信息：
- 文档：[链接]
- 社区：[链接]

如有其他问题，欢迎继续交流！
```

---

## 5. 数据分析

### 5.1 监控指标

| 指标 | 说明 | 监控频率 |
|------|------|----------|
| 点赞数 | 用户认可度 | 每日 |
| 收藏数 | 内容价值 | 每日 |
| 评论数 | 互动活跃度 | 每日 |
| 分享数 | 传播范围 | 每日 |
| 粉丝增长 | 账号影响力 | 每周 |

### 5.2 数据记录格式

```json
{
  "history": [
    {
      "time": "2026-02-17 21:54:46",
      "post_id": "xxx",
      "title": "帖子标题",
      "liked_count": 0,
      "comment_count": 0,
      "collected_count": 2,
      "shared_count": 0
    }
  ]
}
```

### 5.3 报警规则

- 点赞突增：短时间内 >100
- 评论突增：短时间内 >50
- 收藏突增：短时间内 >20
- 负面评论：检测到负面关键词

---

## 6. 记忆导出

将小红书收藏/点赞导出为 AI 可搜索的知识库。

### 6.1 安装 XHS-Downloader

```bash
git clone https://github.com/JoeanAmier/XHS-Downloader.git
cd XHS-Downloader
pip install -r requirements.txt
```

### 6.2 提取收藏链接

1. 安装 [Tampermonkey](https://www.tampermonkey.net/) 浏览器扩展
2. 安装用户脚本：[XHS-Downloader.js](https://raw.githubusercontent.com/JoeanAmier/XHS-Downloader/refs/heads/master/static/XHS-Downloader.js)
3. 打开小红书网页版 → 个人主页 → 收藏/点赞
4. 点击 Tampermonkey 图标 → 选择提取链接
5. 粘贴到 `links.md` 文件

### 6.3 批量下载导出

```bash
# 复制工具脚本到 XHS-Downloader 目录
cp scripts/xhs-downloader/*.py /path/to/XHS-Downloader/

# 批量下载
python batch_download.py links.md

# 导出为 OpenClaw 记忆
python export_to_workspace.py
# 输出到 ~/.openclaw/workspace/xhs-memory/
```

### 6.4 配置记忆搜索

编辑 `~/.openclaw/openclaw.json`：
```json
{
  "memorySearch": {
    "extraPaths": [
      "~/.openclaw/workspace/xhs-memory"
    ]
  }
}
```

---

## 7. 运营最佳实践

### 7.1 内容日历

| 星期 | 内容类型 | 发布时间 |
|------|----------|----------|
| 周一 | 教程/干货 | 9:00 |
| 周三 | 案例分享 | 18:00 |
| 周五 | 热点追踪 | 12:00 |
| 周日 | 互动/问答 | 10:00 |

### 7.2 账号安全

- 避免多设备同时登录
- 手机 App 仅用于查看
- Cookies 有效期约 30 天
- 定期检查登录状态

### 7.3 数据驱动优化

1. 记录每篇帖子的数据
2. 分析高表现内容特征
3. 复制成功模式
4. 持续迭代优化

---

## 资源目录

### scripts/

| 脚本 | 用途 |
|------|------|
| `install-check.sh` | 检查依赖是否安装 |
| `start-mcp.sh` | 启动 MCP 服务 |
| `stop-mcp.sh` | 停止 MCP 服务 |
| `status.sh` | 检查登录状态 |
| `search.sh` | 搜索内容 |
| `recommend.sh` | 获取推荐列表 |
| `post-detail.sh` | 获取帖子详情 |
| `comment.sh` | 发表评论 |
| `user-profile.sh` | 获取用户主页 |
| `publish.sh` | 发布图文笔记 |
| `track-topic.sh` | 热点追踪报告 |

### references/

详细参考文档：
- `api-reference.md` - MCP API 完整参考
- `content-strategy.md` - 内容策略指南
- `troubleshooting.md` - 常见问题解决

### assets/

资源文件：
- `templates/` - 内容模板
- `images/` - 示例图片

---

## 注意事项

1. **首次运行**会下载 headless 浏览器（约 150MB）
2. **发布限制**：标题≤20字符，正文≤1000字符，每日≤50条
3. **账号安全**：避免多设备同时登录，Cookies 约 30 天过期
4. **合规使用**：遵守小红书平台规则，不发布违规内容

---

## 声明

本 skill 基于 [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) 构建，仅提供 API 调用封装。请遵守小红书平台使用条款。