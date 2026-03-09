---
name: api-documentation
description: Use when you need to generate comprehensive API documentation for REST/HTTP, gRPC, GraphQL, and RPC APIs
license: MIT
compatibility: opencode
metadata:
  audience: developers, technical-writers
  category: documentation
---

# API Documentation

Generate comprehensive, interactive API documentation for multiple API protocols including REST/HTTP, gRPC, GraphQL, and RPC. This skill helps create documentation that is accurate, up-to-date, and useful for both developers and consumers.

## When to use me

Use this skill when:
- You need to document APIs for internal or external consumers
- You have multiple API protocols (REST, gRPC, GraphQL, RPC) that need consistent documentation
- You want to generate documentation from code or API definitions automatically
- You need interactive documentation with testing capabilities
- You're preparing API documentation for public release or developer portals
- You need to maintain documentation consistency across multiple API versions
- You want to improve API discoverability and usability

## What I do

- **Multi-protocol support**: Generate documentation for REST/HTTP, gRPC, GraphQL, and RPC APIs
- **Code-first documentation**: Extract documentation from code annotations, OpenAPI/Swagger, Protobuf, GraphQL schemas
- **Interactive examples**: Create executable API examples with testing capabilities
- **Version management**: Handle multiple API versions with migration guides
- **Consistency checking**: Ensure consistency between API implementation and documentation
- **Documentation generation**: Generate HTML, Markdown, PDF, and interactive API consoles
- **Authentication documentation**: Document authentication methods (OAuth, API keys, JWT)
- **Error handling documentation**: Document error codes, messages, and troubleshooting
- **Rate limiting documentation**: Document rate limits, quotas, and usage policies

## Examples

```bash
# Generate OpenAPI documentation from code
./scripts/analyze-api-docs.sh --source src/ --format openapi

# Generate gRPC documentation from Protobuf files
./scripts/analyze-api-docs.sh --source proto/ --format grpc

# Generate GraphQL schema documentation
./scripts/analyze-api-docs.sh --source schema.graphql --format graphql

# Generate comprehensive API portal
./scripts/analyze-api-docs.sh --portal --output docs/api-portal

# Check documentation consistency
./scripts/analyze-api-docs.sh --consistency-check --api implementations/
```

## Output format

```
API Documentation Analysis
─────────────────────────────────────
API Protocol: REST/HTTP
Source Files: 42
Endpoints Documented: 127/142 (89%)

DOCUMENTATION QUALITY METRICS:
───────────────────────────────
✅ Complete: Authentication documented (OAuth 2.0, API keys)
✅ Complete: Error responses documented (25 error codes)
✅ Complete: Request/response examples provided
⚠️ Needs Improvement: Rate limiting documentation missing
⚠️ Needs Improvement: 15 endpoints missing parameter descriptions
❌ Missing: Version migration guide for v1 → v2

API DISCOVERABILITY:
────────────────────
• Endpoints grouped by resource (Users, Products, Orders)
• Search functionality available
• Interactive testing console enabled
• SDK generation for 5 languages (JavaScript, Python, Go, Java, C#)

MULTI-PROTOCOL ANALYSIS:
────────────────────────
REST/HTTP APIs: 142 endpoints
  • OpenAPI specification: Complete
  • Interactive docs: Available via Swagger UI
  • Testing examples: 85%

gRPC APIs: 28 services
  • Protobuf documentation: Complete
  • gRPC reflection: Enabled
  • Client libraries: Generated for 3 languages

GraphQL APIs: 1 schema
  • GraphQL schema: Documented
  • GraphiQL interface: Available
  • Queries/Mutations: 47 operations documented

RPC APIs: 12 methods
  • JSON-RPC documentation: Partial
  • WebSocket support: Documented
  • Binary protocols: Not documented

CONSISTENCY ISSUES (3):
────────────────────────
1. Endpoint /api/v1/users/{id}/profile missing from OpenAPI spec
2. gRPC service "PaymentService" missing authentication documentation
3. GraphQL field "Product.inventory" description inconsistent with REST API

RECOMMENDATIONS:
────────────────
1. HIGH PRIORITY: Document rate limiting policies for all endpoints
2. HIGH PRIORITY: Add version migration guide for upcoming v2 release
3. MEDIUM PRIORITY: Complete JSON-RPC documentation for remaining 5 methods
4. MEDIUM PRIORITY: Generate SDKs for additional languages (Ruby, PHP, Swift)
5. LOW PRIORITY: Add deprecation notices for endpoints scheduled for removal

GENERATED ARTIFACTS:
────────────────────
• OpenAPI 3.0 specification: openapi.yaml
• Interactive API console: docs/api-console/index.html
• Client SDKs: sdk/javascript/, sdk/python/, sdk/go/
• API reference PDF: docs/api-reference.pdf
• Postman collection: docs/postman-collection.json
• cURL examples: docs/curl-examples.md
```

## Notes

- Documentation should be generated as close to the code as possible
- Interactive documentation increases API adoption and reduces support requests
- Consistency between API implementation and documentation is critical
- Consider documentation as part of the API development lifecycle
- Different API protocols may require different documentation approaches
- Version management helps consumers migrate between API versions
- Authentication and error handling are the most commonly referenced sections
- Regular documentation reviews help maintain accuracy and completeness