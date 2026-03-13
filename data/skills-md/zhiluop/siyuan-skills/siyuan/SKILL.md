---
name: siyuan
description: 思源笔记基础知识库，提供核心概念（内容块、块引用、嵌入块）、通用 API 调用方法、模板语法、闪卡系统等基础知识。当询问思源笔记的基本概念、API 原理、块操作语法、模板开发或通用操作时使用此技能（基础层，不包含特定任务的实现）。
license: Complete terms in LICENSE.txt
---

# 思源笔记技能指南

思源笔记是一款基于内容块的隐私优先知识管理工具。本技能提供了思源笔记的核心操作指南，涵盖内容块管理、模板开发、API交互和闪卡系统等功能模块。

## 核心概念

- **内容块（Block）**：思源笔记的基本单位，每个块通过全局唯一 ID 标识。ID 由时间戳和 7 位随机字符组成，形如 `202008250000-a1b2c3d`。
- **默认 API 端口**：`http://127.0.0.1:6806`
- **数据存储**：SQLite 数据库，主表为 `blocks`

## 功能模块

| 模块 | 描述 | 参考文档 |
|------|------|----------|
| 内容块操作 | 内容块的创建、查询、修改和删除，以及块引用和嵌入块的使用 | [block.md](references/block.md) |
| 模板开发 | 模板片段的创建和使用，支持动态内容生成和变量替换 | [template.md](references/template.md) |
| API 交互 | 思源笔记 API 的调用方法，包括 RESTful 接口和 WebSocket | [api.md](references/api.md) |
| 闪卡系统 | 间隔重复记忆系统的使用，卡片创建、复习和管理 | [flashcard.md](references/flashcard.md) |

## 快速参考

### 块类型代码（用于 SQL 查询）

| 代码 | 类型 |
|------|------|
| `d` | 文档块 |
| `h` | 标题块 |
| `l` | 列表块（包含有序/无序/任务） |
| `i` | 列表项块 |
| `b` | 引述块 |
| `callout` | 提示块 |
| `s` | 超级块 |
| `p` | 段落块 |
| `c` | 代码块 |
| `m` | 公式块 |
| `t` | 表格块 |
| `av` | 数据库块 |
| `query_embed` | 嵌入块 |

#### 子类型（subtype）

- **列表块/列表项块**：`o`（有序）、`u`（无序）、`t`（任务）
- **标题块**：`h1`~`h6`

### 常用语法

#### 块引用
```markdown
((块ID "锚文本"))
((块ID))
```

#### 嵌入块
```markdown
{{SELECT * FROM blocks WHERE content LIKE '%关键词%'}}
```

#### API 调用
```http
POST http://127.0.0.1:6806/api/xxx
Content-Type: application/json

{
  "key": "value"
}
```

### API 示例

#### 获取块 Kramdown 源码
```bash
curl -X POST http://127.0.0.1:6806/api/block/getBlockKramdown \
  -H "Content-Type: application/json" \
  -d '{"id": "202008250000-a1b2c3d"}'
```

#### SQL 查询
```bash
curl -X POST http://127.0.0.1:6806/api/query/sql \
  -H "Content-Type: application/json" \
  -d '{"stmt": "SELECT * FROM blocks WHERE type=\"d\""}'
```

### 模板示例

**注意**：思源笔记模板使用 `.action{action}` 语法（而非 `{{action}}`）来避免语法冲突。

#### 简单日期模板
```markdown
今天是 `.action{ now | date "2006-01-02" }`。

# `.action{ .title }`

文档ID：`.action{ .id }`
```

#### 查询块模板
```template
.action{ $blocks := queryBlocks "SELECT * FROM blocks WHERE content LIKE '?' LIMIT ?" "%关键词%" "5" }
.action{ range $blocks }
- ((`.action{ .id }`))
.action{ end }
```

#### 带条件的模板
```template
.action{ $before := (div (now.Sub (toDate "2006-01-02" "2020-02-19")).Hours 24) }
距离 2020-02-19 已经过去 `.action{ $before }` 天
```

## 经验教训与最佳实践

### API 调用注意事项

#### 1. API 调用与输出是分离的
**问题**：脚本在输出成功消息时崩溃，但 API 调用已经完成，导致重复创建文档。

**原因**：
```python
# API 调用成功
result = self._request("/api/filetree/createDocWithMd", data)

# 输出崩溃（但这不影响前面的 API 调用）
print(f"✅ 文档创建成功!")  # Windows GBK 编码无法显示 emoji
```

**解决方案**：
- API 调用成功后立即返回，将输出放在 try-catch 中
- 或者将 API 调用和输出分离，确保 API 操作完成后再处理输出
- 在重复操作前先检查是否已存在

#### 2. 跨平台编码问题
**问题**：Windows 控制台默认使用 GBK 编码，无法显示某些字符（如 emoji）。

**解决方案**：
```python
# 方法 1：使用 UTF-8 编码运行脚本
python -X utf8 script.py

# 方法 2：在代码中设置输出编码
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 方法 3：避免使用特殊字符
print("[成功] 文档创建成功!")  # 而不是 ✅
```

#### 3. 文档路径的正确使用
**问题**：删除文档时使用了错误的路径格式。

**关键区别**：
- **系统路径**：`/20260125135312-pkzku0u.sy` （用于 `removeDoc`）
- **人类可读路径**：`/测试文档-20260125-135311` （用于显示）

**正确用法**：
```python
# 错误 - 使用人类可读路径
api.removeDoc(notebook_id, '/测试文档-20260125-135311')

# 正确 - 使用系统路径（.sy 文件）
api.removeDoc(notebook_id, '/20260125135312-pkzku0u.sy')

# 获取系统路径的方法
query = f"SELECT path FROM blocks WHERE id = '{doc_id}'"
result = api.query_sql(query)
system_path = result[0]['path']  # /20260125135312-pkzku0u.sy
```

#### 4. API 端点验证
**问题**：使用了不存在的 API 端点（如 `/api/block/getBlockInfo`），导致请求失败。

**解决方案**：
- 在使用 API 前，参考官方文档验证端点是否存在
- 常见错误端点：
  - ❌ `/api/block/getBlockInfo` → ✅ `/api/block/getBlockKramdown`
  - ❌ `/api/filetree/getDoc` → ✅ 使用 SQL 查询获取文档内容
  - ❌ `/api/search/searchBlock` → ✅ 使用 `/api/query/sql` 执行搜索

#### 5. 避免重复操作
**问题**：由于脚本崩溃或重复运行，导致创建重复文档。

**解决方案**：
```python
def ensure_doc_exists(notebook_id, path, markdown_content):
    """确保文档存在，不存在则创建"""
    # 先检查是否存在
    query = f"""
    SELECT id, content
    FROM blocks
    WHERE box = '{notebook_id}'
    AND hpath = '{path}'
    AND type = 'd'
    """
    result = api.query_sql(query)

    if result:
        doc_id = result[0]['id']
        print(f"文档已存在: {path} (ID: {doc_id})")
        return doc_id
    else:
        return api.create_doc(notebook_id, path, markdown_content)
```

### Markdown 图片格式规范

**重要：思源笔记中的图片必须使用标准 Markdown 格式 `![alt](url)`**

#### 正确格式 ✅
```markdown
![图片说明](https://example.com/image.jpg)
![封面图](https://mmbiz.qpic.cn/xxx/0?wx_fmt=jpeg)
![本地图片](assets/image.png)
```

#### 错误格式 ❌
```markdown
!图片 https://example.com/image.jpg
图片：https://example.com/image.jpg
<img src="https://example.com/image.jpg">
```

#### 图片 URL 类型

| 类型 | 示例 | 说明 |
|-----|------|------|
| **网络图片** | `https://example.com/img.jpg` | 直接使用 URL，无需下载 |
| **微信图片** | `https://mmbiz.qpic.cn/...` | 使用原始 URL |
| **本地图片** | `assets/image.png` | 相对于文档的本地路径 |

**注意：不要下载图片后上传，直接使用原始 URL 链接即可。**

#### 修复错误格式的图片

如果图片格式错误，使用以下方法修复：

```python
# 1. 查询包含图片的块
query = f"SELECT id, content FROM blocks WHERE content LIKE '%http%' AND type='p'"
result = api.query_sql(query)

# 2. 找到格式错误的图片并修复
for block in result:
    content = block['content']
    if 'mmbiz.qpic.cn' in content or 'example.com' in content:
        # 提取URL（假设格式为 "文本 URL"）
        url = content.split()[-1] if ' ' in content else content
        # 转换为标准格式
        new_content = f'![图片]({url})'
        # 更新块
        api.update_block(block['id'], new_content)
```

### 测试与调试

#### 推荐的测试流程
1. **先测试连接**：列出笔记本验证 API 连接
2. **使用测试笔记本**：在专门的测试笔记本中操作
3. **创建临时文档**：使用带时间戳的文档名
4. **验证结果**：查询数据库确认操作成功
5. **清理测试数据**：测试完成后删除临时文档

#### 调试技巧
```python
# 1. 保存 API 响应到文件以便检查
with open('debug_response.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# 2. 使用 SQL 查询验证数据状态
query = "SELECT * FROM blocks WHERE id = 'xxx' ORDER BY created DESC LIMIT 5"

# 3. 记录操作日志
import logging
logging.basicConfig(filename='siyuan_api.log', level=logging.DEBUG)
```
