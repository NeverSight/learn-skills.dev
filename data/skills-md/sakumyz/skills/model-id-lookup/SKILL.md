---
name: model-id-lookup
description: 查询 AI 模型 ID 的 skill。当用户需要查找或验证 AI 模型 ID 时使用此 skill。支持从本地缓存优先查询，如果找不到则从在线 models.dev 更新本地数据后再查询。
---

# Model ID Lookup Skill

此 skill 用于查询和验证 AI 模型的 ID。

## 数据源

- **本地缓存**：`references/model-schema.json`
- **在线源**：`https://models.dev/model-schema.json`

## 工作流程

### 1. 优先本地搜索

使用 `grep` 工具直接在本地 JSON 中全文检索：

```
grep -i "关键词" references/model-schema.json
```

**搜索规则**：

- 使用大小写不敏感搜索
- 支持部分匹配（如 "gpt-4" 可匹配所有 gpt-4 变体）
- 用户可能记错模型名称，请根据你对市面上模型的了解进行智能匹配

### 2. 如果本地未找到

1. 使用 `webfetch` 工具获取在线数据：

   ```
   webfetch("https://models.dev/model-schema.json")
   ```

2. 使用 `write` 工具更新本地缓存：

   ```
   write(filePath="references/model-schema.json", content=获取的内容)
   ```

3. 重新使用 `grep` 搜索

### 3. 如果仍未找到

- 向用户报告未找到结果
- 提供可能的建议（检查拼写、尝试其他关键词）
- 告知用户当前可用的模型列表来源

## JSON 数据结构

本地 JSON 文件结构如下：

```json
{
  "$defs": {
    "Model": {
      "description": "AI model identifier in provider/model format",
      "enum": [
        "openai/gpt-4o",
        "anthropic/claude-sonnet-4-20250514",
        ...
      ]
    }
  }
}
```

模型 ID 列表位于 `["$defs"]["Model"]["enum"]` 数组中，格式为 `provider/model-name`。

## 输出格式

搜索结果应按以下格式呈现：

```
找到 X 个匹配的模型 ID：

1. provider/model-name-1
2. provider/model-name-2
...

如果以上不是您要找的模型，请尝试：
- 使用更精确的关键词
- 检查模型名称拼写
- 指定提供商名称（如 openai/、anthropic/ 等）
```

## 注意事项

1. **始终优先本地搜索** - 避免不必要的网络请求
2. **缓存更新** - 仅在本地找不到时才更新
3. **保留完整数据** - 更新时保留 JSON 的完整结构（不要只保存 enum 列表）
4. **错误处理** - 网络请求失败时告知用户并回退到本地数据

## 手动更新（可选）

如果需要手动更新模型列表，可以运行：

```bash
python scripts/update_models.py
```
