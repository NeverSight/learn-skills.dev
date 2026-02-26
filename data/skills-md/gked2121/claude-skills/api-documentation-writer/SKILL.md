---
name: api-documentation-writer
description: Generate comprehensive API documentation including endpoint descriptions, request/response examples, authentication guides, error codes, and SDKs. Creates OpenAPI/Swagger specs, REST API docs, and developer-friendly reference materials. Use when users need to document APIs, create technical references, or write developer documentation.
---

# API Documentation Writer

Create comprehensive, developer-friendly API documentation.

## Instructions

When a user needs API documentation:

1. **Gather API Information**:
   - API type (REST, GraphQL, WebSocket, gRPC)?
   - Authentication method (API key, OAuth, JWT)?
   - Base URL and versioning strategy?
   - Available endpoints and their purposes?
   - Request/response formats?
   - Rate limiting or usage restrictions?

2. **Generate Complete Documentation Structure**:

   **Overview Section**:
   - What the API does (1-2 sentences)
   - Key capabilities
   - Getting started checklist
   - Support and resources

   **Authentication**:
   - How to obtain credentials
   - Where to include auth tokens
   - Example authenticated request
   - Token refresh process (if applicable)

   **Base URL & Versioning**:
   - Production and sandbox URLs
   - Version format (path, header, query param)
   - Current version and changelog link

   **Endpoints** (for each endpoint):
   - HTTP method and path
   - Description of what it does
   - Path parameters
   - Query parameters
   - Request headers
   - Request body schema
   - Response codes and meanings
   - Response body schema
   - Example request (curl, JavaScript, Python)
   - Example response (formatted JSON)

   **Error Handling**:
   - Standard error response format
   - Common error codes and meanings
   - Troubleshooting guide

   **Rate Limiting**:
   - Limits and windows
   - Headers to check
   - How to handle rate limit errors

   **SDKs & Libraries**:
   - Official client libraries
   - Community libraries
   - Installation instructions

   **Webhooks** (if applicable):
   - Available webhook events
   - Setup process
   - Payload examples
   - Security verification

3. **Format Output** (REST API example):
   ```markdown
   # [API Name] Documentation

   ## Overview

   [Brief description of what the API does]

   **Base URL**: `https://api.example.com/v1`

   **Authentication**: API Key via `Authorization` header

   ## Quick Start

   1. [Step 1]
   2. [Step 2]
   3. [Step 3]

   ## Authentication

   All requests require an API key in the `Authorization` header:

   ```
   Authorization: Bearer YOUR_API_KEY
   ```

   Get your API key from [dashboard link].

   ## Endpoints

   ### GET /resource

   Retrieve a list of resources.

   **Parameters**:
   - `limit` (optional, integer): Number of results (max 100, default 10)
   - `offset` (optional, integer): Pagination offset (default 0)
   - `filter` (optional, string): Filter by field

   **Request Example**:
   ```bash
   curl -X GET "https://api.example.com/v1/resource?limit=10" \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```

   **Response** (200 OK):
   ```json
   {
     "data": [
       {
         "id": "123",
         "name": "Example",
         "created_at": "2024-01-15T10:00:00Z"
       }
     ],
     "total": 100,
     "limit": 10,
     "offset": 0
   }
   ```

   **Response Codes**:
   - `200` - Success
   - `400` - Bad request (invalid parameters)
   - `401` - Unauthorized (invalid API key)
   - `429` - Rate limit exceeded
   - `500` - Server error

   ### POST /resource

   Create a new resource.

   **Request Body**:
   ```json
   {
     "name": "string (required)",
     "description": "string (optional)",
     "metadata": "object (optional)"
   }
   ```

   **Request Example**:
   ```bash
   curl -X POST "https://api.example.com/v1/resource" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "My Resource",
       "description": "A test resource"
     }'
   ```

   **Response** (201 Created):
   ```json
   {
     "id": "124",
     "name": "My Resource",
     "description": "A test resource",
     "created_at": "2024-01-15T10:30:00Z"
   }
   ```

   ## Error Handling

   All errors follow this format:

   ```json
   {
     "error": {
       "code": "invalid_request",
       "message": "The 'name' field is required",
       "details": {
         "field": "name"
       }
     }
   }
   ```

   **Common Error Codes**:
   - `invalid_request` - Malformed request
   - `authentication_failed` - Invalid API key
   - `not_found` - Resource doesn't exist
   - `rate_limit_exceeded` - Too many requests
   - `internal_error` - Server error

   ## Rate Limiting

   **Limits**: 1000 requests per hour

   **Headers**:
   - `X-RateLimit-Limit`: Total requests allowed
   - `X-RateLimit-Remaining`: Requests remaining
   - `X-RateLimit-Reset`: Timestamp when limit resets

   When rate limited, you'll receive a `429` status code.

   ## Code Examples

   ### JavaScript (Node.js)
   ```javascript
   const response = await fetch('https://api.example.com/v1/resource', {
     headers: {
       'Authorization': 'Bearer YOUR_API_KEY'
     }
   });
   const data = await response.json();
   ```

   ### Python
   ```python
   import requests

   response = requests.get(
     'https://api.example.com/v1/resource',
     headers={'Authorization': 'Bearer YOUR_API_KEY'}
   )
   data = response.json()
   ```

   ## Support

   - Documentation: https://docs.example.com
   - Support: support@example.com
   - Status: https://status.example.com
   ```

4. **For GraphQL APIs**, adapt to show:
   - Schema definitions
   - Query examples
   - Mutation examples
   - Subscription examples
   - Variables and directives

5. **Documentation Best Practices**:
   - Start with working example (copy-paste ready)
   - Show both request and response
   - Use realistic example data
   - Include error cases
   - Explain every parameter
   - Provide code examples in multiple languages
   - Use consistent formatting
   - Add "Try it" interactive examples when possible
   - Link related endpoints
   - Include changelog and versioning

6. **Developer Experience Tips**:
   - Include a "Quick Start" with working example in 60 seconds
   - Provide Postman collection or OpenAPI spec
   - Show common use cases and workflows
   - Include troubleshooting section
   - Add testing/sandbox environment
   - Provide SDKs with installation instructions
   - Include rate limiting details upfront
   - Show pagination patterns
   - Explain filtering and sorting options

## Example Triggers

- "Write API documentation for my REST endpoints"
- "Create OpenAPI spec for my API"
- "Document this GraphQL schema"
- "Generate developer docs for my webhook API"
- "Write authentication guide for API"

## Output Quality

Ensure documentation:
- Starts with working example
- Explains every parameter and field
- Shows realistic request/response examples
- Includes error handling
- Provides code samples in multiple languages
- Uses consistent formatting
- Is organized logically (most common operations first)
- Includes authentication clearly
- Covers edge cases and limitations
- Follows REST/GraphQL best practices
- Is scannable with good use of headers
- Includes interactive examples when possible

Generate comprehensive, developer-friendly API documentation that makes integration effortless.
