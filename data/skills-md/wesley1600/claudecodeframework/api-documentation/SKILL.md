---
name: api-documentation
description: Create comprehensive API documentation with examples, parameter descriptions, and interactive code samples
---

# API Documentation Skill

Create professional API documentation that's clear, complete, and easy to use. This skill helps you generate well-structured API docs that serve both developers and non-technical stakeholders.

## Purpose

This skill assists in generating and organizing API documentation that includes:
- Endpoint descriptions and HTTP methods
- Request and response examples
- Parameter documentation and validation rules
- Authentication and authorization details
- Error codes and troubleshooting
- Code samples in multiple languages
- Interactive examples

## When to Use

Use this skill when you need to:
- Document REST or GraphQL APIs
- Create OpenAPI/Swagger specifications
- Generate SDK documentation
- Build internal API guides for your team
- Create developer portals
- Maintain up-to-date endpoint references
- Document webhook specifications

## Key Features

1. **Comprehensive Coverage** - Document endpoints, parameters, responses, and errors
2. **Multiple Formats** - Generate OpenAPI 3.0, Markdown, or HTML documentation
3. **Code Examples** - Include samples in Python, JavaScript, cURL, and more
4. **Interactive** - Add runnable examples and API explorers
5. **Organized** - Use consistent structure and clear categorization
6. **Version Control** - Track API changes and deprecations
7. **Team-Friendly** - Easy for developers to contribute and update

## Instructions

When using this skill:

1. **Provide API Details** - Give endpoint URLs, methods, and purposes
2. **Document Parameters** - Specify required/optional params, types, and constraints
3. **Include Examples** - Provide real-world request and response examples
4. **Define Errors** - List possible error codes and their meanings
5. **Add Context** - Explain authentication, rate limits, and usage patterns
6. **Generate Output** - Create documentation in your preferred format
7. **Review & Iterate** - Polish examples and clarify ambiguous sections

## Guidelines

- **Be Specific**: Use concrete examples, not generic placeholders
- **Stay Current**: Keep documentation in sync with actual API behavior
- **Think Like Users**: Document common workflows and use cases
- **Include Edge Cases**: Highlight error conditions and limitations
- **Use Standard Formats**: Follow OpenAPI/AsyncAPI specifications where applicable
- **Organize Logically**: Group related endpoints and resources together
- **Provide Multiple Paths**: Show both basic and advanced usage patterns

## Examples

### Example 1: REST API Endpoint Documentation

**Endpoint:** Create User
```
POST /api/v1/users
```

**Description:**
Creates a new user account with the provided information.

**Authentication:** Bearer Token (required)

**Request:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "role": "developer"
}
```

**Response (201 Created):**
```json
{
  "id": "usr_12345",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "developer",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "INVALID_EMAIL",
  "message": "The provided email is invalid",
  "field": "email"
}
```

### Example 2: Generate OpenAPI Specification

**Input:**
```yaml
endpoints:
  - path: /api/products
    method: GET
    description: List all products
    parameters:
      - name: limit
        type: integer
        required: false
        default: 20
```

**Output:**
OpenAPI 3.0 YAML specification with all endpoints, schemas, and examples properly formatted.

## Documentation Templates

This skill includes templates for:
- **endpoint-template.md** - Single endpoint documentation
- **api-overview.md** - Complete API guide
- **error-codes.md** - Error reference
- **authentication-guide.md** - Auth patterns and flows

## Code Examples

Helper scripts include:
- **validate-api.py** - Validate API endpoints against documentation
- **generate-openapi.py** - Convert specifications to OpenAPI format
- **format-examples.py** - Standardize code examples

## Best Practices

- Document all endpoints before release
- Keep examples current and tested
- Include SDKs and client library links
- Provide sandbox/testing endpoints
- Maintain a changelog for API versions
- Support multiple authentication methods
- Include webhook documentation if applicable

## Common API Documentation Patterns

| Pattern | Use Case | Complexity |
|---------|----------|-----------|
| REST | General purpose APIs | Low |
| GraphQL | Complex data queries | High |
| gRPC | High-performance services | High |
| WebSocket | Real-time communication | Medium |
| OpenAPI | Standardized specification | Medium |

## Related Resources

- [OpenAPI 3.0 Specification](https://spec.openapis.org/oas/v3.0.3)
- [API Documentation Best Practices](./references/api-best-practices.md)
- [Code Example Templates](./assets/templates/)
- [Validation Tools](./scripts/)

## Support

For help with API documentation:
1. Review the examples above
2. Check the templates in `assets/templates/`
3. Consult the validation tools in `scripts/`
4. Reference the best practices guide
