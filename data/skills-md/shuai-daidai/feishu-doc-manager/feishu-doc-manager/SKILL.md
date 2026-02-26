---
name: feishu-doc-manager
description: |
  📄 Feishu Doc Manager | 飞书文档管理器
  
  Seamlessly publish Markdown content to Feishu Docs with automatic formatting.
  Solves key pain points: Markdown table conversion, permission management, batch writing.
  
  将 Markdown 内容无缝发布到飞书文档，自动渲染格式。
  解决核心痛点：Markdown 表格转换、权限管理、批量写入。
  
homepage: https://github.com/Shuai-DaiDai/feishu-doc-manager
metadata: {
  "clawdbot": {
    "emoji": "📄",
    "requires": {
      "channels": ["feishu"]
    }
  }
}
---

# 📄 Feishu Doc Manager | 飞书文档管理器

> Seamlessly publish Markdown content to Feishu Docs with automatic formatting.
> 
> 将 Markdown 内容无缝发布到飞书文档，自动渲染格式。

## 🎯 Problems Solved | 解决的痛点

| Problem | Solution | 问题 | 解决方案 |
|---------|----------|------|----------|
| **Markdown tables not rendering** | Auto-convert tables to formatted lists | Markdown 表格无法渲染 | 自动转换为格式化列表 |
| **Permission management complexity** | One-click collaborator management | 权限管理复杂 | 一键协作者管理 |
| **400 errors on long content** | Auto-split long documents | 长内容 400 错误 | 自动分段写入 |
| **Inconsistent formatting** | `write`/`append` auto-render Markdown | 格式不一致 | write/append 自动渲染 |
| **Block-level updates lose formatting** | Clear distinction between write vs update | 块级更新丢失格式 | 区分写入 vs 更新 |

---

## ✨ Key Features | 核心功能

### 1. 📝 Smart Markdown Publishing | 智能 Markdown 发布
- **Auto-render**: `write`/`append` actions automatically render Markdown to Feishu structured docs
- **Table handling**: Tables auto-converted to formatted lists (Feishu limitation workaround)
- **Syntax support**: Headers, lists, bold, italic, code, quotes, dividers

**自动渲染**：`write`/`append` 操作自动将 Markdown 渲染为飞书结构化文档
**表格处理**：表格自动转换为格式化列表（飞书限制解决方案）
**语法支持**：标题、列表、粗体、斜体、代码、引用、分隔线

### 2. 🔐 Permission Management | 权限管理
- Add/remove collaborators
- Update permission levels (view/edit/full_access)
- List current permissions
- Transfer document ownership

添加/删除协作者、更新权限级别、列出现有权限、转移文档所有权

### 3. 📄 Document Operations | 文档操作
- Create new documents
- Write full content with Markdown
- Append to existing documents
- Update specific blocks (plain text only)
- Delete blocks
- List document structure

创建新文档、写入完整 Markdown 内容、追加内容、更新指定块、删除块、列出文档结构

---

## 🚀 Quick Start | 快速开始

### Installation | 安装

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/Shuai-DaiDai/feishu-doc-manager.git
```

### Usage Examples | 使用示例

#### Create Document | 创建文档

```json
{
  "action": "create",
  "title": "Project Report | 项目报告",
  "folder_token": "optional_folder_token"
}
```

#### Write Markdown Content | 写入 Markdown 内容

**⚠️ Critical**: Use `write` for Markdown rendering, NOT `update_block`
**⚠️ 关键**：使用 `write` 进行 Markdown 渲染，不要用 `update_block`

```json
{
  "action": "write",
  "doc_token": "UWpxdSnmXo6mPdxwOyCcWTPUndD",
  "content": "# Project Overview | 项目概览\n\n## Key Metrics | 关键指标\n\n- **Revenue | 收入**: $100K\n- **Users | 用户**: 10K\n- **Growth | 增长**: 25%\n\n> Important note | 重要提示\n> This is a blockquote | 这是引用块"
}
```

#### Add Collaborator | 添加协作者

```bash
curl -X POST "https://open.feishu.cn/open-apis/drive/v1/permissions/{doc_token}/members?type=docx" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "member_type": "openid",
    "member_id": "ou_xxx",
    "perm": "edit"
  }'
```

---

## 📋 Supported Markdown | 支持的 Markdown

| Markdown | Feishu Result | Markdown | 飞书效果 |
|----------|---------------|----------|----------|
| `# Title` | Heading 1 | `# 标题` | 标题1 |
| `## Title` | Heading 2 | `## 标题` | 标题2 |
| `### Title` | Heading 3 | `### 标题` | 标题3 |
| `- Item` | Bullet list | `- 项目` | 无序列表 |
| `1. Item` | Numbered list | `1. 项目` | 有序列表 |
| `**bold**` | Bold | `**粗体**` | 粗体 |
| `*italic*` | Italic | `*斜体*` | 斜体 |
| `` `code` `` | Inline code | `` `代码` `` | 行内代码 |
| `> quote` | Blockquote | `> 引用` | 引用块 |
| `---` | Divider | `---` | 分隔线 |

### ⚠️ Not Supported | 不支持

- **Tables**: Convert to lists | 表格：转换为列表
- **Images**: Use separate upload | 图片：单独上传
- **Complex HTML**: Use Markdown | 复杂 HTML：使用 Markdown

---

## 🔧 Important Distinctions | 重要区分

### `write`/`append` vs `update_block`

| Feature | `write`/`append` | `update_block` |
|---------|------------------|----------------|
| Markdown rendering | ✅ Yes | ❌ No (plain text only) |
| Use case | Initial content, additions | Quick text updates |
| Formatting | Full Markdown support | Plain text only |
| 功能 | 初始内容、追加 | 快速文本更新 |
| 格式支持 | 完整 Markdown | 仅纯文本 |

**Best Practice**: Always use `write` or `append` for Markdown content.
**最佳实践**：Markdown 内容始终使用 `write` 或 `append`。

---

## 🐛 Troubleshooting | 故障排除

### 400 Bad Request | 400 错误
**Cause**: Content too long | 原因：内容过长
**Solution**: Split into smaller chunks | 解决：分段写入

### Markdown Not Rendering | Markdown 不渲染
**Cause**: Used `update_block` instead of `write` | 原因：使用了 `update_block` 而非 `write`
**Solution**: Use `write` or `append` for Markdown | 解决：Markdown 使用 `write` 或 `append`

### Permission Denied | 权限错误
**Cause**: Missing `docs:permission.member` scope | 原因：缺少 `docs:permission.member` 权限
**Solution**: Add permission in Feishu app console | 解决：在飞书应用控制台添加权限

---

## 📦 Required Permissions | 必需权限

```json
{
  "scopes": {
    "tenant": [
      "docx:document",
      "docx:document:create",
      "docx:document:write_only",
      "docs:permission.member",
      "contact:user.base:readonly"
    ]
  }
}
```

---

## 📝 License | 许可证

MIT
