---
name: backend-api-documenter
description: "Automatically generate comprehensive backend API documentation in AGENTS.md format. Use when the user requests to: (1) Document backend API endpoints, (2) Update backend API specifications after code changes, (3) Create or refresh backend/AGENTS.md with complete API documentation including request/response schemas, business rules, and authentication details, (4) Generate API documentation from FastAPI route files"
---

# Backend API Documenter

Generate comprehensive backend API documentation by reading FastAPI route files and schema definitions, then creating detailed specifications in `backend/AGENTS.md`.

## Core Workflow

### 1. Scan API Structure

Read all backend API route files to identify:
- API modules and their base paths
- All endpoints (GET, POST, PUT, PATCH, DELETE)
- Route decorators and parameters
- Summary and description annotations

**Key files to read:**
- `backend/app/api/v1/*.py` - All API route files
- `backend/app/schemas/*.py` - Request/response schema definitions
- `backend/CLAUDE.md` - Backend-specific specifications (if exists)

Optional helper script:
```bash
python3 scripts/scan_api_routes.py ./backend
```

### 2. Extract Endpoint Details

For each endpoint, extract:
- HTTP method and path
- Request headers (Authorization, X-API-Key, etc.)
- Request body schema (from Pydantic models)
- Response body schema
- Query parameters
- Path parameters
- Error responses and status codes
- Business rules from docstrings and code logic

### 3. Organize Documentation

Structure documentation following this hierarchy:

```
1. Module Overview
   Base路径: /api/v1/module

   1.1 Endpoint Name
   - 接口 (Interface)
   - 描述 (Description)
   - 请求头 (Request Headers)
   - 请求体 (Request Body) with field descriptions
   - 响应体 (Response Body) with field descriptions
   - 错误响应 (Error Responses)
   - 权限要求 (Authorization)
   - 业务规则 (Business Rules)
```

### 4. Include Standard Appendices

Always include these appendices at the end:

- **附录A: 统一响应格式** - Standard response format and business codes
- **附录B: 国际化支持** - i18n headers and locale handling
- **附录C: 认证方式** - JWT Token and API Key authentication
- **附录D: 错误处理最佳实践** - Client-side error handling patterns

See [doc_template.md](references/doc_template.md) for complete template structure.

### 5. Write Documentation

Write the complete documentation to `backend/AGENTS.md`:
- Start with project context inheritance: `> **Inherits from**: [Root AGENTS.md](../AGENTS.md)`
- Include table of contents with anchor links
- Use consistent formatting (Chinese labels, English technical terms)
- Provide concrete JSON examples for all requests/responses
- Document all field types, constraints, and validation rules
- Include business logic and special cases

## Field Description Best Practices

For every field in request/response schemas, document:

1. **Name and type**: `field_name` (string, int, float, bool, array, object)
2. **Required/Optional**: Always specify
3. **Constraints**: Length limits, value ranges, formats, enums
4. **Description**: What it represents and how it's used
5. **Examples**: Concrete values when helpful

Example:
```markdown
- `email` (string, optional): User email address, must be valid email format, max 255 characters
- `reward_amount` (float, required): Task reward amount, must be > 0, max 100000
- `status` (string, required): Task status, possible values: published/in_progress/completed/expired
- `location` (object, optional): GeoJSON Point format with coordinates [longitude, latitude]
```

## Common Patterns

### Authentication Documentation

```markdown
**请求头**:
```
Authorization: Bearer {access_token}
```
或
```
X-API-Key: {api_key}
```

**权限要求**: 需要人类用户认证(JWT Token) 或 需要代理认证(API Key)
```

### Error Response Documentation

```markdown
**错误响应**:

验证失败(400):
```json
{
  "success": false,
  "code": "INVALID_INPUT",
  "message": "输入参数无效",
  "data": null
}
```

未授权(401):
```json
{
  "success": false,
  "code": "UNAUTHORIZED",
  "message": "未授权",
  "data": null
}
```
```

### Business Rules Documentation

```markdown
**业务规则**:
- 只有任务所有者可以更新
- 创建任务时会锁定相应金额
- 任务发布后立即可见
- 评分范围: 1.0-5.0
```

## Documentation Quality Standards

- **Completeness**: Document every field in every request/response
- **Accuracy**: Match actual code behavior, not ideal behavior
- **Clarity**: Use clear, concise language with concrete examples
- **Consistency**: Follow same format for all endpoints
- **Bilingual**: Chinese labels with English technical terms
- **Currency**: Keep documentation in sync with code changes

## Notes

- This skill generates documentation for FastAPI-based backends
- Assumes Pydantic models for request/response schemas
- Follows unified response format with success/code/message/data structure
- Supports both JWT Token (human users) and API Key (agents) authentication
- Documentation should be comprehensive but concise - include all necessary details without redundancy
