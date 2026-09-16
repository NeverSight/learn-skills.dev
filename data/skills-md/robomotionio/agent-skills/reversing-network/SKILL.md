---
name: reversing-network
description: Reverses the network traffic behind a browser flow to replace slow browser automation with direct HTTP requests. Use when the user says "this browser flow is too slow", "find the API this page uses", "convert to HTTP", "can we call the API instead", or when `exploring-browser` reveals a clean REST/GraphQL endpoint.
---

# Reversing Network (Browser → HTTP)

Replace browser automation with faster, more reliable HTTP requests by reverse-engineering the underlying API with `robomotion-browser-mcp` network capture.

**Pairs with:** `exploring-browser` — capture traffic there during exploration, then come here to convert.

## When to Use This

| Use browser automation | Use network reversal |
|----------------------|---------------------|
| Site has heavy JS rendering | Site's data comes from API calls |
| No clear API endpoint | API endpoint is discoverable via DevTools |
| Login requires JS execution | Login returns a token in response headers/body |
| Site changes selectors frequently | API is stable and versioned |

## Step 1: Capture Network Traffic with Browser MCP

Open a browser with network capture enabled, then perform the target actions:

```
1. browser_open(stealth: true)
2. browser_start_network_capture(url_filter: "api.", capture_body: true)
3. browser_navigate(url: "https://example.com/search")
4. browser_snapshot()  — read the page to find interactive elements
5. browser_click / browser_type — perform the user action (search, login, etc.)
6. browser_get_requests(method: "POST")  — list captured API calls
7. browser_get_request_response(request_id: "...")  — inspect a specific pair
```

Use `browser_snapshot()` between actions to see the page state. Repeat click/type/snapshot until the target API calls appear in `browser_get_requests`.

## Step 2: Analyze the Captured Request

From the JSON returned by `browser_get_request_response`, inspect:

- **Request**: `request.method`, `request.url`, `request.headers`, `request.body`
- **Response**: `response.status`, `response.headers`, `response.body`, `response.mimeType`

Identify:
1. **Endpoint URL** — often contains version (`/api/v2/products`)
2. **Required headers** — Authorization, X-API-Key, cookies, Content-Type
3. **Request body format** — JSON, form-data, GraphQL
4. **Authentication flow** — does login return a Bearer token?

## Step 3: Build the HTTP Flow

```typescript
import { flow, Message, Custom, Credential } from '@robomotion/sdk';

const myFlow = flow.create('main', 'API Scraper', (f) => {
  f.node('start', 'Core.Trigger.Inject', 'Start', {})

  // Step 1: Authenticate (if needed)
  .then('auth', 'Core.Net.HttpRequest', 'Login', {
    optUrl: Custom('https://api.example.com/auth/login'),
    optMethod: 'post',
    inBody: Custom(JSON.stringify({ username: '...', password: '...' })),
    inCustomHeaders: [{ scope: 'Custom', name: { name: 'Content-Type', value: 'application/json' } }],
    outBody: Message('auth_body'),
    outStatus: Message('auth_status')
  })

  // Step 2: Extract token from response
  .then('token', 'Core.Programming.Function', 'Extract Token', {
    func: `
      msg.bearer_token = 'Bearer ' + msg.auth_body.token;
      return msg;
    `
  })

  // Step 3: Build headers object with token
  .then('headers', 'Core.Programming.Function', 'Build Headers', {
    func: `
      msg.headers = {
        'Authorization': msg.bearer_token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
      };
      return msg;
    `
  })

  // Step 4: Call the actual data API
  .then('api', 'Core.Net.HttpRequest', 'Get Data', {
    optUrl: Custom('https://api.example.com/products?page=1'),
    optMethod: 'get',
    inHeaders: Message('headers'),
    outBody: Message('api_body'),
    outStatus: Message('api_status')
  })

  // Step 5: Parse and process
  .then('parse', 'Core.Programming.Function', 'Parse Response', {
    func: `
      msg.products = msg.api_body.items;
      return msg;
    `
  })

  .then('stop', 'Core.Flow.Stop', 'Done', {});
});

myFlow.start();
```

## Step 4: Handle Pagination

For paginated APIs, use the loop pattern:

```typescript
// ForEach over page numbers or use cursor/offset from response
f.node('loop', 'Core.Programming.ForEach', 'Each Page', {
  optInput: Message('page_numbers'),  // [1, 2, 3, ...]
  optOutput: Message('page_num')
})
// ... make API call with page_num ...
f.node('goto', 'Core.Flow.GoTo', 'Next', {
  optNodes: { ids: ['LABEL_ID'], type: 'goto', all: false }
})
```

## Key Rules

1. **Always verify the API response format** before building the full flow
2. **Store credentials in vault** — never hardcode API keys or tokens
3. **Handle rate limits** — add `delayBefore` or retry loops for 429 responses
4. **Check token expiry** — some tokens expire; add refresh logic if needed
5. **Core.Net.HttpRequest is built-in** — no extra dependency needed (it's in the `Core` package)

## Common HTTP Node Properties

Verify exact names with `robomotion describe node Core.Net.HttpRequest`:

| Property | Value |
|----------|-------|
| URL (Option) | `optUrl: Custom('https://...')` or `Message('url')` |
| Method (Option) | `optMethod: 'get' \| 'post' \| 'put' \| 'delete' \| 'patch'` (lowercase enum) |
| Headers (Input) | `inHeaders: Message('headers')` (key-value object) or `inCustomHeaders: [{ scope: 'Custom', name: { name: 'X', value: 'Y' } }]` |
| Body (Input) | `inBody: Custom(JSON.stringify({...}))` or `Message('body')` |
| Response body (Output) | `outBody: Message('resp_body')` — parsed JSON when `Content-Type: application/json`, otherwise string |
| Response status (Output) | `outStatus: Message('status')` |
| Response headers (Output) | `outHeaders: Message('resp_headers')` |

## Cleanup

Always call `browser_stop_network_capture` and `browser_close` when done capturing, even if the flow build fails. Leaving the browser open wastes resources and can block subsequent runs.
