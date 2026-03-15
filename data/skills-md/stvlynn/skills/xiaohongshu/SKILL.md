---
name: xiaohongshu
description: 小红书搜索、发布、获取帖子详情。使用本地 MCP 服务器访问小红书内容，需要先登录。适用于搜索旅游攻略、美食推荐、获取帖子详情等场景。
---

# 小红书 Skill

通过本地 MCP 服务器访问小红书内容。

## 前置条件

需要部署 [xiaohongshu-mcp](https://github.com/peanut996/xiaohongshu-mcp) 服务。

**首次使用必须先登录：**

```bash
cd /path/to/xiaohongshu-mcp
./xiaohongshu-login
```

登录成功后会保存 cookies 到 `cookies/cookies.json`。

## 启动服务

```bash
cd /path/to/xiaohongshu-mcp
./start.sh
```

服务会在后台运行，监听 `http://localhost:18060/mcp`。

## 可用功能

### 1. 搜索内容

```bash
curl -X POST http://localhost:18060/api/search \
  -H "Content-Type: application/json" \
  -d '{"keyword": "弥勒旅游"}'
```

返回搜索结果，包括帖子 ID、标题、用户信息、点赞数等。

### 2. 获取帖子详情

```bash
curl -X POST http://localhost:18060/api/feed/detail \
  -H "Content-Type: application/json" \
  -d '{
    "note_id": "帖子ID",
    "xsec_token": "从搜索结果获取"
  }'
```

返回完整帖子内容，包括图片、文字、评论等。

### 3. 获取推荐列表

```bash
curl -X POST http://localhost:18060/api/feeds
```

返回小红书首页推荐内容。

### 4. 检查登录状态

```bash
curl http://localhost:18060/api/check-login
```

## 使用示例

### 搜索

```bash
# CLI 搜索
python3 scripts/xhs_search.py "弥勒旅游景点"

# 限制结果数
python3 scripts/xhs_search.py "美食推荐" 5
```

### curl 工作流

```bash
# 1. 搜索
curl -X POST http://localhost:18060/api/search \
  -H "Content-Type: application/json" \
  -d '{"keyword": "弥勒旅游景点"}' | jq .

# 2. 获取帖子详情（从搜索结果中选择）
curl -X POST http://localhost:18060/api/feed/detail \
  -H "Content-Type: application/json" \
  -d '{
    "note_id": "从搜索结果获取",
    "xsec_token": "从搜索结果获取"
  }' | jq .
```

## 工作流

1. **启动服务**：启动 xiaohongshu-mcp
2. **搜索关键词**：获取帖子列表
3. **选择帖子**：从列表中选择感兴趣的帖子
4. **获取详情**：使用 `note_id` 和 `xsec_token` 获取完整内容
5. **总结信息**：提取关键信息（景点、拍摄机位、tips 等）

## 注意事项

- **首次使用必须登录**：运行 `./xiaohongshu-login`
- **Cookies 过期**：如果返回需要登录，重新运行登录工具
- **服务端口**：默认 18060，确保端口未被占用
- **同时登录限制**：小红书不允许同一账号在多个网页端登录
- 移动端不受影响：可以同时使用小红书 App

## 故障排查

| 问题 | 解决方法 |
|------|----------|
| 服务无法启动 | `lsof -i :18060` 检查端口占用 |
| 搜索返回空结果 | `curl http://localhost:18060/api/check-login` 检查登录状态 |
| Cookies 过期 | 删除 `cookies/cookies.json` 后重新运行 `./xiaohongshu-login` |

## API 响应格式

### 搜索结果

```json
{
  "items": [
    {
      "id": "帖子ID",
      "note_card": {
        "display_title": "标题",
        "user": { "nickname": "作者昵称" },
        "interact_info": { "liked_count": "点赞数" }
      },
      "xsec_token": "用于获取详情的 token"
    }
  ]
}
```

### 帖子详情

```json
{
  "note_card": {
    "title": "标题",
    "desc": "正文内容",
    "image_list": [{ "url": "图片URL" }],
    "interact_info": {
      "liked_count": "点赞数",
      "collected_count": "收藏数",
      "comment_count": "评论数"
    }
  },
  "comments": {
    "comments": [
      { "content": "评论内容", "sub_comments": [] }
    ]
  }
}
```
