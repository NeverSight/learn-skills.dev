---
name: lark-docs
description: Access and search Lark/Feishu cloud documents with user permissions (飞书云文档权限访问)
---

# Lark Docs Access (飞书云文档权限)

以用户身份访问和搜索飞书云文档，包括文档、表格、多维表格和知识库等。

Access and search Lark cloud documents as the authenticated user, including docs, sheets, bitables, and wiki spaces.

## Quick Start

### Search for Documents (搜索文档)

```
搜索包含'OKR'的文档
Search for documents containing 'product roadmap'
```

### Access Document Content (访问文档内容)

```
获取这个文档的内容：https://example.feishu.cn/docx/abc123
Get the content of this document: https://example.feishu.cn/wiki/xyz789
```

### Search Wiki Spaces (搜索知识库)

```
在知识库中搜索关于'架构设计'的内容
Search wiki for 'system architecture' documentation
```

## Key Features

### 1. Document Search (文档搜索)

Search across all document types that the user has access to:
- **Documents (文档)**: docx format documents
- **Sheets (表格)**: spreadsheet documents
- **Bitables (多维表格)**: database/table documents
- **Wiki (知识库)**: wiki pages and spaces

**Available MCP Tools:**
- `mcp__lark__docx_builtin_search` - Search cloud documents
- `mcp__lark__wiki_v1_node_search` - Search wiki content

**Search Parameters:**
- `search_key` (required): Keyword to search for
- `docs_types`: Filter by document type (doc, sheet, bitable, mindnote, file)
- `owner_ids`: Filter by document owner's open_id
- `chat_ids`: Filter by group where document is located
- `count`: Number of results (max 50, default 10)
- `offset`: Pagination offset

### 2. Document Content Access (文档内容访问)

Retrieve the actual content of documents:

**Available MCP Tools:**
- `mcp__lark__docx_v1_document_rawContent` - Get plain text content
- `mcp__lark__wiki_v2_space_getNode` - Get wiki node information

**Parameters:**
- `document_id`: The unique document identifier
- `lang`: Language for @mentions (0=Chinese, 1=English)

### 3. Permission Management (权限管理)

Check and manage document permissions:

**Available MCP Tools:**
- `mcp__lark__drive_v1_permissionMember_create` - Add permissions

**Permission Roles:**
- `view`: Read-only access
- `edit`: Can edit the document
- `full_access`: Full management access

## Common Workflows

### Workflow 1: Search and Read Documents

```markdown
1. User: "搜索包含'产品路线图'的文档"
2. Assistant uses: mcp__lark__docx_builtin_search
   - search_key: "产品路线图"
   - count: 10
3. Display results with titles and URLs
4. User: "打开第一个文档"
5. Assistant uses: mcp__lark__docx_v1_document_rawContent
   - document_id: extracted from URL
6. Display document content
```

### Workflow 2: Wiki Navigation

```markdown
1. User: "Show me the engineering wiki"
2. Assistant uses: mcp__lark__wiki_v1_node_search
   - query: "engineering"
3. Display wiki pages and their hierarchy
4. User: "Get the content of the API documentation page"
5. Assistant uses: mcp__lark__wiki_v2_space_getNode
   - token: wiki_page_token
6. Display wiki content
```

### Workflow 3: Document Discovery by Owner

```markdown
1. User: "张三创建的所有文档"
2. First get user ID: mcp__lark__contact_v3_user_batchGetId
   - emails: ["zhangsan@company.com"]
3. Then search: mcp__lark__docx_builtin_search
   - search_key: ""
   - owner_ids: [user_open_id]
4. Display documents created by that user
```

## Examples (示例)

### Example 1: Basic Search (基础搜索)

**User (Chinese):**
```
帮我搜索包含'季度OKR'的文档
```

**Assistant Response:**
```markdown
I'll search for documents containing '季度OKR'.

<uses mcp__lark__docx_builtin_search>
- search_key: "季度OKR"
- count: 10

Found 3 documents:

1. **2024 Q4 OKR Review** (docx)
   - Owner: 张三
   - Updated: 2024-01-10
   - Link: https://example.feishu.cn/docx/abc123

2. **Team OKR Template** (docx)
   - Owner: 李四
   - Updated: 2024-01-08
   - Link: https://example.feishu.cn/docx/def456

3. **Q1 2025 OKR Planning** (sheet)
   - Owner: 王五
   - Updated: 2024-01-12
   - Link: https://example.feishu.cn/sheets/ghi789

Would you like me to open any of these documents?
```

### Example 2: Get Document Content (获取文档内容)

**User (English):**
```
Get the content of this document: https://example.feishu.cn/docx/abc123
```

**Assistant Response:**
```markdown
I'll retrieve the content of that document.

<uses mcp__lark__docx_v1_document_rawContent>
- document_id: abc123

Here's the document content:

# 2024 Q4 OKR Review

## Engineering Team

### Objective 1: Improve System Reliability
- KR1: Achieve 99.9% uptime ✓ (Completed: 99.95%)
- KR2: Reduce MTTR to under 30 minutes ✓ (Completed: 25 min)
- KR3: Complete disaster recovery testing ⚠ (In Progress: 80%)

### Objective 2: Enhance Developer Productivity
- KR1: Reduce build time by 40% ✓ (Completed: 45% reduction)
- KR2: Implement automated code review ✓ (Completed)
- KR3: Launch internal developer portal ✗ (Delayed to Q1 2025)

[... more content ...]

Would you like me to summarize the key points or search for related documents?
```

### Example 3: Wiki Search (知识库搜索)

**User (Chinese):**
```
在工程知识库中搜索关于'微服务架构'的文档
```

**Assistant Response:**
```markdown
我会在工程知识库中搜索'微服务架构'相关内容。

<uses mcp__lark__wiki_v1_node_search>
- query: "微服务架构"

找到 5 个相关页面:

1. **微服务架构设计指南**
   - 路径: 工程文档 > 架构设计 > 微服务
   - 更新时间: 2024-01-10
   - [查看页面](https://example.feishu.cn/wiki/page1)

2. **服务拆分最佳实践**
   - 路径: 工程文档 > 架构设计 > 最佳实践
   - 更新时间: 2024-01-08
   - [查看页面](https://example.feishu.cn/wiki/page2)

3. **API Gateway 配置说明**
   - 路径: 工程文档 > 基础设施 > 网关
   - 更新时间: 2024-01-12
   - [查看页面](https://example.feishu.cn/wiki/page3)

需要我打开其中某个页面查看详细内容吗?
```

## Important Notes

### Permission Boundaries (权限边界)
- All operations respect the user's actual Lark permissions
- If a document is not accessible, you'll receive a permission error
- Cannot access private documents or groups the user is not a member of

### Document ID Extraction (文档ID提取)
Document URLs have this format:
- Docx: `https://*.feishu.cn/docx/{document_id}`
- Wiki: `https://*.feishu.cn/wiki/{wiki_token}`
- Sheets: `https://*.feishu.cn/sheets/{spreadsheet_id}`
- Bitable: `https://*.feishu.cn/base/{app_token}`

Extract the ID/token from the URL when accessing content.

### Search Limitations (搜索限制)
- Maximum 50 results per search (count parameter)
- Use pagination (offset) for more results
- Search is case-insensitive
- Results are sorted by relevance

### Content Format (内容格式)
- `docx_v1_document_rawContent` returns plain text (no formatting)
- @mentions are converted to display names based on lang parameter
- For rich formatted content, use the API to get structured data

## Error Handling

Common errors and solutions:

1. **"Permission denied" (权限被拒绝)**
   - The user doesn't have access to this document
   - Ask the document owner to grant permission

2. **"Document not found" (文档未找到)**
   - Document ID is invalid or document was deleted
   - Verify the document URL is correct

3. **"Invalid token" (无效令牌)**
   - MCP server authentication failed
   - Check LARK_APP_ID and LARK_APP_SECRET environment variables
   - Ensure OAuth token is valid

## Tips for Effective Use

1. **Start with search**: Use keyword search before asking for specific documents
2. **Be specific**: Include relevant keywords to narrow down results
3. **Use filters**: Filter by document type or owner to find documents faster
4. **Check permissions**: Verify access before trying to read document content
5. **Bilingual support**: Works with both Chinese and English queries

## Related Skills

- `lark-messages`: Access Lark messages and groups
- Future: `lark-approval`, `lark-calendar`, `lark-drive`
