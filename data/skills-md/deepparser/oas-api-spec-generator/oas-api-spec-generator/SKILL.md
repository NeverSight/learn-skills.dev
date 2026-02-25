---
name: oas-api-spec-generator
description: Generate OpenAPI 3.2.0 specifications for third-party APIs (OpenAI, Anthropic, Google, Microsoft, Stripe, GitHub, Slack, AWS, and more)
---

# OAS Third-Party API Spec Generator

A skill for generating OpenAPI Specification 3.2.0 documents for third-party APIs (Microsoft, Google, OpenAI, Anthropic, Stripe, GitHub, Slack, AWS, and more).

## When to Use This Skill

Use this skill when the user asks to:

- Generate an OpenAPI spec for a third-party API
- Create OAS/Swagger definitions for external services
- Document third-party API endpoints they're integrating with
- Convert API documentation into OpenAPI format
- Build client SDKs from third-party API specs
- Create API gateway configurations for external APIs

Trigger phrases: "create OAS for", "generate openapi spec", "openapi for [provider]", "swagger spec for", "API spec for"

## How This Skill Works

### Step 1: Identify the Target API

When the user requests a spec for a third-party API, identify:

1. **Provider** (e.g., OpenAI, Microsoft Graph, Google Cloud, Stripe)
2. **Specific endpoints/services** needed (e.g., "just the Chat Completions endpoint" vs "the full API")
3. **Use case** (SDK generation, API gateway, documentation, testing)

### Step 2: Fetch Current API Documentation

Use WebFetch to pull the latest API documentation from the provider:

```
Provider documentation URLs (use these as starting points):

OpenAI:         https://platform.openai.com/docs/api-reference
Anthropic:      https://docs.anthropic.com/en/api
Google AI:      https://ai.google.dev/api/rest
Microsoft Graph: https://learn.microsoft.com/en-us/graph/api/overview
Azure OpenAI:   https://learn.microsoft.com/en-us/azure/ai-services/openai/reference
Stripe:         https://stripe.com/docs/api
GitHub:         https://docs.github.com/en/rest
Slack:          https://api.slack.com/methods
AWS (various):  https://docs.aws.amazon.com/
Twilio:         https://www.twilio.com/docs/usage/api
SendGrid:       https://docs.sendgrid.com/api-reference
Cloudflare:     https://developers.cloudflare.com/api/
Vercel:         https://vercel.com/docs/rest-api
Supabase:       https://supabase.com/docs/reference
Firebase:       https://firebase.google.com/docs/reference/rest
```

Also check if the provider publishes an official OpenAPI spec:

```
Official OpenAPI specs (fetch and use as reference/base):

OpenAI:          https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml
GitHub:          https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.yaml
Stripe:          https://raw.githubusercontent.com/stripe/openapi/master/openapi/spec3.yaml
Microsoft Graph: https://raw.githubusercontent.com/microsoftgraph/msgraph-metadata/master/openapi/v1.0/openapi.yaml
Anthropic:       https://raw.githubusercontent.com/anthropics/anthropic-sdk-python/main/api.yaml (if available)
```

If an official spec exists, fetch it and upgrade/adapt it to OAS 3.2.0 rather than writing from scratch.

### Step 3: Generate the OAS 3.2.0 Spec

Generate a spec following the structure and patterns defined below. Always output as YAML (more readable than JSON for specs).

### Step 4: Validate

After generating, validate the spec structure against OAS 3.2.0 rules (see Validation section below).

---

## OAS 3.2.0 Spec Structure

Every generated spec MUST follow this top-level structure:

```yaml
openapi: 3.2.0

info:
  title: "{Provider Name} API"
  version: "{API version from provider docs}"
  description: |
    OpenAPI 3.2.0 specification for the {Provider Name} API.
    Auto-generated from official documentation.

    Source: {documentation URL}
    Generated: {date}
  contact:
    name: "{Provider Name} API Support"
    url: "{provider support URL}"
  license:
    name: "API Terms of Service"
    url: "{provider ToS URL}"
  x-generated-by: "OAS API Spec Generator Skill"
  x-source-documentation: "{documentation URL}"

servers:
  - url: "{base URL}"
    description: "Production"
  # Add sandbox/staging if available

security:
  - {default security scheme}: []

tags:
  # Use structured tags (OAS 3.2 feature)
  - name: "{Resource Group}"
    summary: "{Description}"
    kind: resource  # or: operation, webhook, admin
    # parent: "{Parent Tag}"  # For hierarchical grouping

paths:
  # Endpoint definitions...

webhooks:
  # If the API supports webhooks...

components:
  schemas:
    # Data models...
  parameters:
    # Reusable parameters...
  responses:
    # Standard error responses...
  securitySchemes:
    # Auth methods...
  mediaTypes:
    # Reusable media types (OAS 3.2 feature)

externalDocs:
  description: "Official {Provider} API Documentation"
  url: "{docs URL}"
```

---

## Provider-Specific Auth Patterns

### Bearer Token (API Key as Bearer)
Used by: OpenAI, Anthropic, Cohere, Mistral

```yaml
components:
  securitySchemes:
    apiKeyBearer:
      type: http
      scheme: bearer
      description: |
        API key passed as Bearer token.
        Obtain from: {provider dashboard URL}

security:
  - apiKeyBearer: []
```

### Custom Header API Key
Used by: Anthropic (x-api-key), OpenAI (also supports this)

```yaml
components:
  securitySchemes:
    apiKeyHeader:
      type: apiKey
      in: header
      name: "x-api-key"
      description: |
        API key passed in custom header.
        Obtain from: {provider dashboard URL}
```

### OAuth 2.0 Authorization Code
Used by: Microsoft Graph, Google APIs, GitHub, Slack, Stripe Connect

```yaml
components:
  securitySchemes:
    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: "{auth URL}"
          tokenUrl: "{token URL}"
          refreshUrl: "{refresh URL}"
          scopes:
            "scope.read": "Read access"
            "scope.write": "Write access"
      # OAS 3.2: OAuth2 metadata URL
      x-oauth2-metadata-url: "{provider}/.well-known/oauth-authorization-server"
```

### OAuth 2.0 Client Credentials
Used by: Microsoft Graph (app-only), AWS Cognito, Auth0

```yaml
components:
  securitySchemes:
    oauth2ClientCredentials:
      type: oauth2
      flows:
        clientCredentials:
          tokenUrl: "{token URL}"
          scopes:
            ".default": "Default scope"
```

### AWS Signature V4
Used by: AWS services

```yaml
components:
  securitySchemes:
    awsSigV4:
      type: apiKey
      in: header
      name: Authorization
      description: |
        AWS Signature Version 4.
        See: https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html
      x-amazon-apigateway-authtype: "awsSigv4"
```

### Multi-Auth (Provider + Org)
Used by: OpenAI (API key + Organization header), Azure OpenAI (API key + Azure AD)

```yaml
components:
  securitySchemes:
    apiKey:
      type: http
      scheme: bearer
    orgHeader:
      type: apiKey
      in: header
      name: "OpenAI-Organization"
      description: "Optional organization ID"

# Per-operation security can combine:
# security:
#   - apiKey: []
#     orgHeader: []
```

---

## Streaming Support (OAS 3.2.0)

This is critical for AI API specs. OAS 3.2.0 has first-class streaming support.

### Server-Sent Events (SSE)
Used by: OpenAI, Anthropic, Google AI (streaming responses)

```yaml
paths:
  /v1/chat/completions:
    post:
      operationId: createChatCompletion
      summary: Create chat completion
      tags: [Chat]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ChatCompletionRequest'
      responses:
        '200':
          description: Successful response
          content:
            # Non-streaming response
            application/json:
              schema:
                $ref: '#/components/schemas/ChatCompletionResponse'
            # Streaming response (OAS 3.2 native)
            text/event-stream:
              schema:
                type: string
              itemSchema:
                $ref: '#/components/schemas/ChatCompletionChunk'
              x-stream-delimiter: "\n\n"
```

### JSON Lines / NDJSON Streaming
Used by: Some batch/export APIs

```yaml
responses:
  '200':
    content:
      application/x-ndjson:
        schema:
          type: string
        itemSchema:
          $ref: '#/components/schemas/BatchResultLine'
```

---

## Common Response Patterns

### Paginated List Response
Used by: Most REST APIs (Stripe, GitHub, Microsoft Graph)

```yaml
components:
  schemas:
    # Cursor-based (Stripe, Slack)
    PaginatedList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/{Resource}'
        has_more:
          type: boolean
        next_cursor:
          type: string
          nullable: true

    # Offset-based (GitHub, many REST APIs)
    PaginatedListOffset:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/{Resource}'
        total_count:
          type: integer
        page:
          type: integer
        per_page:
          type: integer

    # OData-style (Microsoft Graph)
    ODataCollection:
      type: object
      properties:
        value:
          type: array
          items:
            $ref: '#/components/schemas/{Resource}'
        '@odata.count':
          type: integer
        '@odata.nextLink':
          type: string
          format: uri
          nullable: true
```

### Standard Error Response

```yaml
components:
  schemas:
    # OpenAI/Anthropic style
    APIError:
      type: object
      required: [error]
      properties:
        error:
          type: object
          required: [message, type]
          properties:
            message:
              type: string
            type:
              type: string
              enum: [invalid_request_error, authentication_error, permission_error, not_found_error, rate_limit_error, api_error]
            param:
              type: string
              nullable: true
            code:
              type: string
              nullable: true

    # Microsoft Graph style
    ODataError:
      type: object
      properties:
        error:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
            innerError:
              type: object

    # Stripe style
    StripeError:
      type: object
      properties:
        error:
          type: object
          properties:
            type:
              type: string
              enum: [api_error, card_error, idempotency_error, invalid_request_error]
            message:
              type: string
            code:
              type: string
            param:
              type: string

  responses:
    BadRequest:
      description: Invalid request parameters
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/APIError'
    Unauthorized:
      description: Authentication required or invalid
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/APIError'
    Forbidden:
      description: Insufficient permissions
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/APIError'
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/APIError'
    RateLimited:
      description: Rate limit exceeded
      headers:
        Retry-After:
          schema:
            type: integer
          description: Seconds to wait before retrying
        X-RateLimit-Limit:
          schema:
            type: integer
        X-RateLimit-Remaining:
          schema:
            type: integer
        X-RateLimit-Reset:
          schema:
            type: integer
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/APIError'
    ServerError:
      description: Internal server error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/APIError'
```

---

## Provider Quick-Reference

When generating specs for these providers, use these specific patterns:

### OpenAI API
- **Base URL**: `https://api.openai.com`
- **Auth**: Bearer token (`Authorization: Bearer sk-...`)
- **Optional headers**: `OpenAI-Organization`, `OpenAI-Project`
- **Streaming**: SSE with `stream: true` in request body
- **Key endpoints**: `/v1/chat/completions`, `/v1/embeddings`, `/v1/images/generations`, `/v1/audio/transcriptions`, `/v1/models`, `/v1/files`, `/v1/assistants`, `/v1/threads`
- **Official spec**: Fetch from `https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml`
- **Pagination**: Cursor-based with `after` parameter
- **Versioning**: Date-based via `OpenAI-Beta` header for beta features

### Anthropic API
- **Base URL**: `https://api.anthropic.com`
- **Auth**: `x-api-key` header + `anthropic-version` header (required, e.g., `2024-10-22`)
- **Streaming**: SSE with `stream: true`
- **Key endpoints**: `/v1/messages`, `/v1/messages/batches`, `/v1/models`
- **Special**: Tool use support, vision (base64 images), PDF support
- **Rate limits**: Via `anthropic-ratelimit-*` headers
- **Pagination**: Cursor-based

### Google AI (Gemini)
- **Base URL**: `https://generativelanguage.googleapis.com`
- **Auth**: API key as query param (`?key=`) or OAuth2
- **Streaming**: SSE via `streamGenerateContent` endpoints
- **Key endpoints**: `/v1beta/models/{model}:generateContent`, `/v1beta/models/{model}:streamGenerateContent`, `/v1beta/models/{model}:embedContent`
- **Special**: Function calling, grounding with Google Search

### Microsoft Graph
- **Base URL**: `https://graph.microsoft.com/v1.0` (stable), `/beta` (preview)
- **Auth**: OAuth2 (authorization code or client credentials) via Azure AD
- **Token URL**: `https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token`
- **Key endpoints**: `/me`, `/users`, `/groups`, `/drives`, `/sites`, `/teams`
- **Pagination**: OData `@odata.nextLink`
- **Query**: OData query params (`$select`, `$filter`, `$expand`, `$top`, `$skip`, `$orderby`)
- **Official spec**: Available in `microsoftgraph/msgraph-metadata` repo
- **Batch**: `POST /$batch` with JSON batch requests

### Stripe
- **Base URL**: `https://api.stripe.com`
- **Auth**: Bearer token (secret key) or Basic auth
- **Content-Type**: `application/x-www-form-urlencoded` (NOT JSON for requests)
- **Key endpoints**: `/v1/customers`, `/v1/charges`, `/v1/payment_intents`, `/v1/subscriptions`, `/v1/invoices`
- **Versioning**: Date-based via `Stripe-Version` header
- **Pagination**: Cursor-based with `starting_after` / `ending_before`
- **Webhooks**: Signed with `Stripe-Signature` header
- **Idempotency**: `Idempotency-Key` header
- **Official spec**: Available in `stripe/openapi` repo

### GitHub REST API
- **Base URL**: `https://api.github.com`
- **Auth**: Bearer token (PAT or OAuth), also supports Basic auth
- **Key endpoints**: `/repos/{owner}/{repo}`, `/users/{username}`, `/orgs/{org}`, `/issues`, `/pulls`
- **Pagination**: Link header with `rel="next"`, `per_page` param (max 100)
- **Rate limits**: Via `X-RateLimit-*` headers
- **Versioning**: API version header `X-GitHub-Api-Version: 2022-11-28`
- **Official spec**: Available in `github/rest-api-description` repo

### Slack Web API
- **Base URL**: `https://slack.com/api`
- **Auth**: Bearer token (Bot or User token)
- **Content-Type**: Mix of `application/x-www-form-urlencoded` and `application/json`
- **Key endpoints**: `/chat.postMessage`, `/conversations.list`, `/users.list`, `/files.upload`
- **Pagination**: Cursor-based with `cursor` and `next_cursor`
- **Rate limits**: Tier-based (1-4), `Retry-After` header

### AWS APIs (General Pattern)
- **Auth**: AWS Signature V4 (`Authorization` header)
- **Endpoints**: Regional (`{service}.{region}.amazonaws.com`)
- **Key services**: S3, Lambda, DynamoDB, SES, SNS, SQS, Bedrock
- **Special**: Many AWS APIs use custom protocols (JSON RPC, Query, REST-XML)
- **Official specs**: AWS publishes Smithy models, some have OpenAPI exports

### Cloudflare
- **Base URL**: `https://api.cloudflare.com/client/v4`
- **Auth**: Bearer token or `X-Auth-Email` + `X-Auth-Key` headers
- **Key endpoints**: `/zones`, `/dns_records`, `/workers`, `/accounts`
- **Pagination**: Page-based with `page` and `per_page`
- **Response envelope**: `{ success, errors, messages, result }`

### Vercel
- **Base URL**: `https://api.vercel.com`
- **Auth**: Bearer token
- **Key endpoints**: `/v9/projects`, `/v6/deployments`, `/v1/domains`, `/v1/teams`
- **Pagination**: Varies by endpoint (cursor or offset)

### Twilio
- **Base URL**: `https://api.twilio.com/2010-04-01`
- **Auth**: Basic auth (Account SID:Auth Token)
- **Content-Type**: `application/x-www-form-urlencoded` (requests)
- **Key endpoints**: `/Accounts/{sid}/Messages`, `/Accounts/{sid}/Calls`
- **Pagination**: Page-based with `PageSize` and `PageToken`

### SendGrid
- **Base URL**: `https://api.sendgrid.com/v3`
- **Auth**: Bearer token
- **Key endpoints**: `/mail/send`, `/marketing/contacts`, `/templates`

---

## Multi-File Organization

For large API specs (50+ endpoints), split into multiple files:

```
specs/
├── {provider}/
│   ├── openapi.yaml           # Entry document
│   ├── paths/
│   │   ├── {resource}.yaml    # Per-resource paths
│   │   └── ...
│   ├── components/
│   │   ├── schemas/
│   │   │   ├── {Model}.yaml
│   │   │   └── ...
│   │   ├── parameters/
│   │   │   └── common.yaml
│   │   ├── responses/
│   │   │   └── errors.yaml
│   │   └── securitySchemes/
│   │       └── auth.yaml
│   └── README.md              # Provider-specific notes
```

Use `$ref` for cross-file references:
```yaml
paths:
  /users:
    $ref: './paths/users.yaml#/~1users'

components:
  schemas:
    User:
      $ref: './components/schemas/User.yaml'
```

---

## Validation Rules

After generating a spec, verify these rules:

### MUST (Errors)
1. `openapi` field is exactly `3.2.0`
2. `info.title` and `info.version` are present
3. At least one of `paths`, `components`, or `webhooks` is present
4. Every `$ref` points to a valid target
5. Every `operationId` is unique across the spec
6. All required `schema` properties are listed in the `required` array
7. Path parameters in the URL template have matching parameter definitions
8. Security schemes referenced in `security` arrays are defined in `components/securitySchemes`
9. HTTP methods are lowercase (`get`, `post`, `put`, `patch`, `delete`)
10. Response status codes are strings (`'200'`, not `200`)

### SHOULD (Warnings)
1. Every operation has an `operationId` (needed for SDK generation)
2. Every operation has a `summary` or `description`
3. Every operation has at least one response defined
4. Schemas use `$ref` for reuse when a type appears 2+ times
5. Error responses (4xx, 5xx) include response body schemas
6. Pagination endpoints document pagination parameters
7. Rate-limited endpoints document rate limit headers
8. Streaming endpoints use `text/event-stream` or `application/x-ndjson` media types with `itemSchema`
9. Tags are used to group related operations
10. `examples` are provided for complex request/response bodies

### RECOMMENDED (Best Practices)
1. Use `operationId` naming: `{verb}{Resource}` (e.g., `createUser`, `listOrders`)
2. Group related endpoints under the same tag
3. Use structured tags with `kind` and `parent` (OAS 3.2)
4. Document all authentication methods the provider supports
5. Include `externalDocs` linking to the provider's official documentation
6. Add `x-generated-by` and `x-source-documentation` to `info`
7. For AI APIs: document token limits, model availability, and pricing tiers in descriptions

---

## Generation Workflow

When the user requests a spec, follow this exact workflow:

1. **Check for official spec**: Try to fetch the provider's official OpenAPI spec first
2. **If official spec exists**: Upgrade it to OAS 3.2.0, clean up, add missing features (streaming, structured tags)
3. **If no official spec**: Fetch the provider's API documentation via WebFetch
4. **Extract endpoints**: Identify all endpoints, methods, parameters, request/response bodies
5. **Map auth**: Determine authentication method(s) and create security schemes
6. **Generate spec**: Build the YAML following the structure above
7. **Add streaming**: If the API supports streaming (especially AI APIs), use OAS 3.2 streaming patterns
8. **Validate**: Check against the validation rules
9. **Write file**: Save to `specs/{provider}/openapi.yaml` (or user-specified path)
10. **Report**: Summarize what was generated (endpoint count, schemas, auth methods)

---

## Example: Generating a Minimal OpenAI Spec

```yaml
openapi: 3.2.0

info:
  title: OpenAI API
  version: "2.3.0"
  description: |
    OpenAPI 3.2.0 specification for the OpenAI API.
    Covers Chat Completions, Embeddings, and Models endpoints.

    Source: https://platform.openai.com/docs/api-reference
  contact:
    name: OpenAI Support
    url: https://help.openai.com
  license:
    name: MIT
    identifier: MIT
  x-generated-by: "OAS API Spec Generator Skill"

servers:
  - url: https://api.openai.com
    description: Production

security:
  - bearerAuth: []

tags:
  - name: Chat
    summary: Chat completions
    kind: resource
  - name: Embeddings
    summary: Text embeddings
    kind: resource
  - name: Models
    summary: Model management
    kind: resource

paths:
  /v1/chat/completions:
    post:
      operationId: createChatCompletion
      summary: Create a chat completion
      tags: [Chat]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ChatCompletionRequest'
            examples:
              basic:
                summary: Basic chat request
                value:
                  model: gpt-4o
                  messages:
                    - role: user
                      content: "Hello!"
              streaming:
                summary: Streaming request
                value:
                  model: gpt-4o
                  messages:
                    - role: user
                      content: "Hello!"
                  stream: true
      responses:
        '200':
          description: Chat completion response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ChatCompletionResponse'
            text/event-stream:
              schema:
                type: string
              itemSchema:
                $ref: '#/components/schemas/ChatCompletionChunk'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '429':
          $ref: '#/components/responses/RateLimited'

  /v1/embeddings:
    post:
      operationId: createEmbedding
      summary: Create embeddings
      tags: [Embeddings]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/EmbeddingRequest'
      responses:
        '200':
          description: Embedding response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/EmbeddingResponse'

  /v1/models:
    get:
      operationId: listModels
      summary: List available models
      tags: [Models]
      responses:
        '200':
          description: List of models
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ModelList'

  /v1/models/{model_id}:
    get:
      operationId: getModel
      summary: Retrieve a model
      tags: [Models]
      parameters:
        - name: model_id
          in: path
          required: true
          schema:
            type: string
          description: The ID of the model (e.g., gpt-4o)
      responses:
        '200':
          description: Model details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Model'

components:
  schemas:
    ChatCompletionRequest:
      type: object
      required: [model, messages]
      properties:
        model:
          type: string
          description: Model ID (e.g., gpt-4o, gpt-4o-mini)
        messages:
          type: array
          items:
            $ref: '#/components/schemas/ChatMessage'
        temperature:
          type: number
          minimum: 0
          maximum: 2
          default: 1
        max_tokens:
          type: integer
          nullable: true
        stream:
          type: boolean
          default: false
        tools:
          type: array
          items:
            $ref: '#/components/schemas/Tool'
        tool_choice:
          oneOf:
            - type: string
              enum: [none, auto, required]
            - $ref: '#/components/schemas/ToolChoice'

    ChatMessage:
      type: object
      required: [role, content]
      properties:
        role:
          type: string
          enum: [system, user, assistant, tool]
        content:
          oneOf:
            - type: string
            - type: array
              items:
                $ref: '#/components/schemas/ContentPart'
        name:
          type: string
        tool_calls:
          type: array
          items:
            $ref: '#/components/schemas/ToolCall'
        tool_call_id:
          type: string

    ContentPart:
      oneOf:
        - type: object
          required: [type, text]
          properties:
            type:
              type: string
              const: text
            text:
              type: string
        - type: object
          required: [type, image_url]
          properties:
            type:
              type: string
              const: image_url
            image_url:
              type: object
              required: [url]
              properties:
                url:
                  type: string
                  format: uri
                detail:
                  type: string
                  enum: [auto, low, high]

    ChatCompletionResponse:
      type: object
      properties:
        id:
          type: string
        object:
          type: string
          const: chat.completion
        created:
          type: integer
        model:
          type: string
        choices:
          type: array
          items:
            type: object
            properties:
              index:
                type: integer
              message:
                $ref: '#/components/schemas/ChatMessage'
              finish_reason:
                type: string
                enum: [stop, length, tool_calls, content_filter]
        usage:
          $ref: '#/components/schemas/Usage'

    ChatCompletionChunk:
      type: object
      properties:
        id:
          type: string
        object:
          type: string
          const: chat.completion.chunk
        created:
          type: integer
        model:
          type: string
        choices:
          type: array
          items:
            type: object
            properties:
              index:
                type: integer
              delta:
                type: object
                properties:
                  role:
                    type: string
                  content:
                    type: string
                    nullable: true
                  tool_calls:
                    type: array
                    items:
                      $ref: '#/components/schemas/ToolCallDelta'
              finish_reason:
                type: string
                nullable: true
                enum: [stop, length, tool_calls, content_filter]

    Usage:
      type: object
      properties:
        prompt_tokens:
          type: integer
        completion_tokens:
          type: integer
        total_tokens:
          type: integer

    Tool:
      type: object
      required: [type, function]
      properties:
        type:
          type: string
          const: function
        function:
          type: object
          required: [name]
          properties:
            name:
              type: string
            description:
              type: string
            parameters:
              type: object

    ToolChoice:
      type: object
      required: [type, function]
      properties:
        type:
          type: string
          const: function
        function:
          type: object
          required: [name]
          properties:
            name:
              type: string

    ToolCall:
      type: object
      properties:
        id:
          type: string
        type:
          type: string
          const: function
        function:
          type: object
          properties:
            name:
              type: string
            arguments:
              type: string

    ToolCallDelta:
      type: object
      properties:
        index:
          type: integer
        id:
          type: string
        type:
          type: string
        function:
          type: object
          properties:
            name:
              type: string
            arguments:
              type: string

    EmbeddingRequest:
      type: object
      required: [model, input]
      properties:
        model:
          type: string
        input:
          oneOf:
            - type: string
            - type: array
              items:
                type: string
        encoding_format:
          type: string
          enum: [float, base64]
          default: float
        dimensions:
          type: integer

    EmbeddingResponse:
      type: object
      properties:
        object:
          type: string
          const: list
        data:
          type: array
          items:
            type: object
            properties:
              object:
                type: string
                const: embedding
              index:
                type: integer
              embedding:
                type: array
                items:
                  type: number
        model:
          type: string
        usage:
          type: object
          properties:
            prompt_tokens:
              type: integer
            total_tokens:
              type: integer

    Model:
      type: object
      properties:
        id:
          type: string
        object:
          type: string
          const: model
        created:
          type: integer
        owned_by:
          type: string

    ModelList:
      type: object
      properties:
        object:
          type: string
          const: list
        data:
          type: array
          items:
            $ref: '#/components/schemas/Model'

    APIError:
      type: object
      required: [error]
      properties:
        error:
          type: object
          required: [message, type]
          properties:
            message:
              type: string
            type:
              type: string
            param:
              type: string
              nullable: true
            code:
              type: string
              nullable: true

  responses:
    BadRequest:
      description: Invalid request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/APIError'
    Unauthorized:
      description: Invalid or missing API key
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/APIError'
    RateLimited:
      description: Rate limit exceeded
      headers:
        retry-after:
          schema:
            type: integer
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/APIError'

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      description: |
        OpenAI API key as Bearer token.
        Get your key at: https://platform.openai.com/api-keys

externalDocs:
  description: OpenAI API Reference
  url: https://platform.openai.com/docs/api-reference
```

---

## Output Format

Always generate specs as **YAML files** (not JSON). YAML is more readable and is the standard format for OpenAPI specs.

When the user requests a spec:
1. Ask which endpoints/services they need (or generate all)
2. Generate the full YAML spec
3. Save it to the filesystem at a sensible path
4. Provide a summary of what was generated

Summary format:
```
Generated OAS 3.2.0 spec for {Provider} API:
- Endpoints: {count}
- Schemas: {count}
- Auth: {method(s)}
- Streaming: {yes/no}
- File: {path}
```
