---
name: minimax-search-vlm
description: 使用 MiniMax Coding Plan API 进行网络搜索（web_search）和图像理解（understand_image）。需配置 MINIMAX_CP_API_KEY（MiniMax API Key，一般为 sk-cp- 开头）。触发示例：「MiniMax 搜索」「图像理解」「web search」「understand image」「minimax 搜一下」「描述这张图」。
---

# MiniMax 搜索与图像理解

通过 MiniMax Coding Plan API 执行**网络搜索**与**图像理解**。执行前需设置环境变量 `MINIMAX_CP_API_KEY`（Coding Plan 的 API Key，从 [Coding Plan 订阅页](https://platform.minimaxi.com) 获取，一般为 `sk-cp-` 开头）。Base URL 通过 `MINIMAX_CP_BASE_URL` 设置，**未设置时默认为国内** `https://api.minimaxi.com`；国际请设为 `https://api.minimax.io`。

---

## 1. 网络搜索（web_search）

**端点**：`POST {base}/v1/coding_plan/search`

**请求**：
- Headers：`Authorization: Bearer $MINIMAX_CP_API_KEY`，`Content-Type: application/json`，`MM-API-Source: Minimax-MCP`
- Body：`{"q": "搜索关键词"}`

**示例（curl，避免转义用单引号）**：
```bash
BASE_URL="${MINIMAX_CP_BASE_URL:-https://api.minimaxi.com}"
curl -X POST "$BASE_URL/v1/coding_plan/search" \
  -H "Authorization: Bearer $MINIMAX_CP_API_KEY" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP" \
  -d '{"q": "Python asyncio 教程"}'
```

Agent 调用时从环境变量读取 token，在 curl 的 `-H` 中直接使用已 export 的 `$MINIMAX_CP_API_KEY` 即可。**切勿在输出、日志或回复中打印、echo 或展示 API Key 或其它环境变量的值。**

---

## 2. 图像理解（understand_image）

**端点**：`POST {base}/v1/coding_plan/vlm`

**请求**：
- Headers：同上（Authorization、Content-Type、MM-API-Source）
- Body：`prompt`（必填）+ `image_url`（必填，见下）

**image_url 两种形式**：
- **图片 URL**：直接传可公网访问的图片地址，例如 `"image_url": "https://example.com/your-image.jpg"`
- **本地文件**：先转 Base64，再传 `data:image/<类型>;base64,<base64 字符串>`，例如 JPEG 为 `data:image/jpeg;base64,<BASE64>`。

**示例（图片 URL）**：
```bash
BASE_URL="${MINIMAX_CP_BASE_URL:-https://api.minimaxi.com}"
curl -X POST "$BASE_URL/v1/coding_plan/vlm" \
  -H "Authorization: Bearer $MINIMAX_CP_API_KEY" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP" \
  -d '{"prompt": "描述这张图片的内容", "image_url": "https://example.com/your-image.jpg"}'
```

**示例（本地图片转 Base64）**：
```bash
BASE_URL="${MINIMAX_CP_BASE_URL:-https://api.minimaxi.com}"
BASE64=$(base64 -i image.jpg | tr -d '\n')
curl -X POST "$BASE_URL/v1/coding_plan/vlm" \
  -H "Authorization: Bearer $MINIMAX_CP_API_KEY" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP" \
  --data-raw "{\"prompt\": \"描述这张图片\", \"image_url\": \"data:image/jpeg;base64,$BASE64\"}"
```

---

## 注意事项

- 执行前确认已设置：`export MINIMAX_CP_API_KEY="你的MiniMax_API_Key"`；可选 `MINIMAX_CP_BASE_URL`（未设置时默认国内 `https://api.minimaxi.com`）。
- Coding Plan 的 key 一般为 `sk-cp-` 开头，从 Coding Plan 订阅页获取。
- **安全**：不要打印、echo、log 或向用户展示 `MINIMAX_CP_API_KEY`、`MINIMAX_CP_BASE_URL` 等环境变量的值，仅用于请求头或请求体，避免泄露。
- 更多 curl 示例与说明见 [reference.md](reference.md)。
