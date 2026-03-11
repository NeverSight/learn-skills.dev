---
name: yuque-document-management
description: 通过YuQue MCP工具管理语雀知识库文档。适用于创建、搜索、更新、移动或删除语雀文档；组织知识库结构；批量文档操作；管理文档模板；实现协作工作流。提供MCP工具集成模式和使用要点。
---

# 语雀文档管理

通过YuQue MCP工具管理语雀知识库文档。本技能专注于MCP工具的使用要点和常见操作模式。

## MCP工具概览

所有操作都通过YuQue MCP工具完成：

- `mcp_YuQueMCP_get_default_repository` - 获取默认知识库信息
- `mcp_YuQueMCP_get_repository_toc_tree` - 获取完整目录树结构
- `mcp_YuQueMCP_search` - 搜索文档
- `mcp_YuQueMCP_create_document` - 创建新文档
- `mcp_YuQueMCP_get_document` - 读取文档内容
- `mcp_YuQueMCP_update_document` - 更新文档内容或标题
- `mcp_YuQueMCP_move_document` - 移动文档到其他目录
- `mcp_YuQueMCP_delete_document` - 删除文档

## 基本操作要点

### 创建文档

**步骤：**
1. 获取目录结构：`mcp_YuQueMCP_get_repository_toc_tree` 了解组织方式
2. 确定位置：选择合适的 `parentUuid` 或使用根目录（null）
3. 准备内容：使用Markdown格式
4. 创建文档：调用 `mcp_YuQueMCP_create_document`，参数：
   - `title`（必需）：文档标题
   - `body`（可选）：Markdown格式的文档内容
   - `parentUuid`（可选）：父目录UUID

**要点：**
- 同一目录下标题必须唯一
- 内容使用标准Markdown语法
- 不指定parentUuid则创建在根目录

### 搜索文档

**使用：**
```
mcp_YuQueMCP_search query="搜索关键词" type="DOC" page=1
```

**参数说明：**
- `query`（必需）：搜索关键词
- `type`（可选）：文档类型过滤
- `page`（可选）：分页页码

**要点：**
- 使用具体关键词而非通用术语
- 可组合多个关键词提高精确度
- 大结果集使用分页

### 更新文档

**使用：**
```
mcp_YuQueMCP_update_document docId="文档ID" body="新内容" title="新标题"
```

**参数说明：**
- `docId`（必需）：文档ID
- `body`（可选）：新的文档内容
- `title`（可选）：新的文档标题

**要点：**
- 至少提供body或title之一
- 更新后验证更改是否生效
- 确认文档ID正确

### 移动文档

**使用：**
```
mcp_YuQueMCP_move_document docId="文档ID" parentUuid="目标父目录UUID"
```

**要点：**
- parentUuid为null则移到根目录
- 确认目标目录存在
- 避免循环引用（不能移到自己的子目录）

### 删除文档

**使用：**
```
mcp_YuQueMCP_delete_document docId="文档ID"
```

**要点：**
- 删除操作不可逆，需确认
- 验证文档ID正确
- 删除前可先备份内容

## 常见工作流

### 文档创建流程

1. **查看结构**：`get_repository_toc_tree` 了解现有组织
2. **确定位置**：选择合适的父目录UUID
3. **准备内容**：编写Markdown格式内容
4. **创建文档**：调用 `create_document`
5. **验证结果**：确认文档出现在预期位置

### 文档组织流程

1. **获取当前结构**：`get_repository_toc_tree` 查看完整目录树
2. **识别需要移动的文档**：确定重组目标
3. **执行移动**：使用 `move_document` 重新定位
4. **验证结构**：移动后重新获取目录树确认

## 错误处理要点

### 常见错误

**文档创建失败：**
- 检查标题在目标目录是否唯一
- 验证Markdown语法正确
- 确认parentUuid存在

**搜索无结果：**
- 尝试更广泛或替代关键词
- 检查拼写和术语
- 验证文档可见性/权限

**移动失败：**
- 确认目标parentUuid存在
- 检查源文档是否存在
- 验证无循环引用

### 错误处理模式

```python
try:
    result = mcp_YuQueMCP_create_document(title="标题", body="内容")
except Exception as e:
    # 记录错误
    # 实现重试逻辑
    # 提供用户反馈
```

## 使用最佳实践

### 操作前准备

1. **获取知识库信息**：先调用 `get_default_repository` 了解知识库
2. **查看目录结构**：使用 `get_repository_toc_tree` 规划组织方式
3. **搜索验证**：创建前搜索确认文档不存在

### 内容规范

- 使用清晰、描述性的标题
- 内容使用标准Markdown格式
- 保持文档大小适中（避免超大文档）
- 相关文档组织在同一目录

### 协作注意

- 设置合适的可见性权限
- 重大变更使用版本命名
- 移动文档前与团队协调
- 定期清理过时内容

## 工具参数速查

| 工具 | 必需参数 | 可选参数 | 说明 |
|------|----------|----------|------|
| `create_document` | `title` | `body`, `parentUuid` | 创建文档 |
| `get_document` | `docId` | - | 读取文档 |
| `update_document` | `docId` | `body`, `title` | 更新文档 |
| `move_document` | `docId` | `parentUuid` | 移动文档 |
| `delete_document` | `docId` | - | 删除文档 |
| `search` | `query` | `type`, `page` | 搜索文档 |
| `get_repository_toc_tree` | - | - | 获取目录树 |
| `get_default_repository` | - | - | 获取知识库信息 |

## 参考文档

需要详细信息时查看：

- **references/mcp-tools.md** - 完整MCP工具参考
- **references/troubleshooting.md** - 错误排查指南