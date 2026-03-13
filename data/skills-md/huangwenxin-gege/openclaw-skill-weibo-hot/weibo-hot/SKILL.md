---
name: weibo-hot
description: 抓取并展示微博实时热搜榜前十名。当用户询问“微博热搜”、“最近大家在聊什么”或“帮我看看微博趋势”时使用。支持输出标题和热度。
---

# 微博热搜 (Weibo Hot Search)

此技能通过执行 Python 脚本直接从微博官网获取实时热搜数据。

## 使用方法

1.  **环境检查**：确保本地环境已安装 `requests` 和 `beautifulsoup4`。
2.  **执行抓取**：运行技能附带的脚本获取数据。

### 命令参考
```bash
# 执行抓取脚本
python3 scripts/get_hot.py
```

## 注意事项
- 如果请求被拦截（提示访客系统），可能需要更新 `scripts/get_hot.py` 中的 `Cookie`。
- 脚本会自动过滤掉置顶广告，只显示有排名的前 10 条。
