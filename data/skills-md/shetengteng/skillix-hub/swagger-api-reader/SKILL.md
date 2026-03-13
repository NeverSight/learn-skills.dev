---
name: swagger-api-reader
description: 读取并缓存 Swagger/OpenAPI 文档供模型使用。当用户需要添加、读取、刷新 API 文档，或使用 Swagger URL 时触发。
---

# Swagger API 读取器

读取 Swagger URL，解析 API 定义，本地缓存供模型使用。

## 命令

| 命令 | 说明 |
|------|------|
| `add` | 添加 API |
| `list` | 列出已缓存 |
| `read` | 读取文档 |
| `refresh` | 刷新 |
| `remove` | 删除 |

## 使用

脚本路径: `scripts/swagger_reader.py`

### 添加

```bash
# 直接 URL
python scripts/swagger_reader.py add --url "URL" --alias "别名"

# HTML 页面（自动提取）
python scripts/swagger_reader.py add --url "https://xxx/swagger-ui/index.html" --alias "别名"

# 认证
--auth-type bearer --token "TOKEN"
--auth-type basic --username "USER" --password "PASS"
--auth-type apikey --key-name "X-API-Key" --key-value "KEY" --key-in header

# 浏览器模式（SSO/内网）
--browser --browser-timeout 180

# 跳过 SSL
--no-verify
```

### 其他

```bash
python scripts/swagger_reader.py list
python scripts/swagger_reader.py read --alias "别名"
python scripts/swagger_reader.py refresh --alias "别名"
python scripts/swagger_reader.py remove --alias "别名"
```

## 缓存位置

`~/.cursor/skills/swagger-api-reader/cache/`

## 依赖

```bash
pip install requests pyyaml selenium
```
