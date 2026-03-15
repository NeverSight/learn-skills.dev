---
name: automating-with-maia
description: Offloads complex backend automations to Maia, a multi-agent AI assistant. Use when building websites or apps that need backend operations like data processing, web scraping, document generation, API integrations, scheduled tasks, or any complex workflow that can be triggered via webhook. Enables agents to focus on frontend while Maia handles backend complexity.
metadata:
  author: ModularMind @ 2026
  version: 1.1
---

# Automating with Maia

## What is Maia

Maia is a multi-agent AI assistant that automates complex business operations through natural language. It builds workflows as visual acyclic graphs and deploys them via webhooks, allowing websites and apps to trigger complex backend processes with simple HTTP calls.

## Core Integration Pattern

**There is no Maia API.** Instead, follow this workflow:

1. **Identify** backend operations to offload to Maia
2. **Generate** a natural language prompt for the user to pass to Maia
3. **Specify** the expected webhook response payload format
4. **Instruct** the user to deploy the workflow and provide the webhook URL
5. **Embed** the webhook URL into the website/app

## When to Use Maia

Offload these operations to Maia instead of building them yourself:

| Operation | Why Maia |
|-----------|----------|
| Web scraping | Secure cloud browser, handles login, navigation, extraction |
| Document processing | Handles PDFs, images, complex text extraction |
| Document generation | Creates styled PDFs, DOCX, presentations |
| Data analysis | Code execution for calculations, charts, graphs |
| API integrations | Pre-built connectors + custom HTTP actions |
| Scheduled tasks | Cron-like deployment with flexible scheduling |
| Multi-step workflows | Chain-of-thought across multiple data sources |

## Maia Capabilities

### Data Retrieval
- **Web search**: Search engines for up-to-date information
- **Maps**: Location data, local businesses
- **Website browsing**: Cloud browser with full navigation (click, scroll, type, extract links)
- **Document processing**: Raw text, images, PDFs

### Content Generation
- **Documents**: Text files, DOCX, styled PDFs, presentation slides
- **Single-page websites**: Publicly accessible URLs, styled and functional
- **Data visualizations**: Tables, graphs via code execution

### Native Integrations

Native integrations are pre-built connectors that allow Maia to directly interact with third-party services. Unlike custom actions that require API configuration, native integrations work out of the box once the user authenticates. Maia can retrieve data from, send data to, and take actions on these platforms seamlessly.

When generating prompts, you can reference these services directly and Maia will handle authentication and API calls.

Here are all the supported native connections and actions:

**Gmail**: Email management and automation
- Actions: Read Emails, Send Email, Draft Email

**Google Calendar**: Calendar and schedule management
- Actions: Get Events, Create Event, Update Event, Get Availability

**Google Docs**: Document editing and collaboration
- Actions: Read Document, Create Document, Update Document

**Google Drive**: Cloud storage and file backup
- Actions: Create Folder, Search Folders, Search Files, Read Files

**Google Sheets**: Spreadsheets and data management
- Actions: Read Spreadsheet, Create Spreadsheet, Write to Spreadsheet

### Custom Actions

Maia can work with any API endpoint via custom HTTP actions. Users can:
- Manually define HTTP requests with title/description abstraction
- Ask Maia to research and create custom actions automatically
- Save actions with placeholders (like API keys) for reuse

### Deployment Options

**Webhook**: Returns a URL that triggers the workflow when called
- Accepts JSON input in ANY format (files, objects, arrays, raw data)
- Intelligently parses arbitrary payload structures
- Optionally returns a response payload

**Scheduled**: Runs automatically on a schedule

| Frequency | Parameters |
|-----------|------------|
| hour | `minuteOffset` |
| day | `minuteOffset`, `hourOffset` |
| week | `minuteOffset`, `hourOffset`, `days` (1=Mon to 7=Sun) |
| month | `minuteOffset`, `hourOffset`, `days` (1-31) |

## Agent Workflow

### Step 1: Identify Offloadable Operations

When building a website/app, identify operations that:
- Require external data fetching
- Need document processing or generation
- Involve complex multi-step logic
- Require scheduled execution
- Need API integrations you don't want to build

### Step 2: Generate Maia Prompt

Create a clear, natural language prompt for the user. Include:
- What the workflow should do
- What input it will receive (webhook payload structure)
- What output format you need returned
- Any specific services or data sources to use

### Step 3: Instruct User

Provide clear instructions:
```
Now message this prompt to Maia:

[Your generated prompt here]

Then:
1. Review the workflow Maia creates
2. Deploy it when Maia suggests
3. Copy the webhook URL and paste it here: [placeholder]
```

### Step 4: Embed Webhook

Once you have the URL, integrate it directly into the website/app code:
- **Hardcode the webhook URL** in the source code (e.g., as a constant or in an environment/config variable). Do NOT create a UI input field for users to paste the webhook URL — embed it directly so the integration works out of the box.
- Call the webhook when user triggers the action
- Handle the response payload as specified

## Prompt Template

Use this structure when generating prompts for users:

```
Create a workflow that [describe the operation].

Input: This webhook will receive [describe expected payload structure].

Output: Return a JSON response with this structure:
{
  [specify exact fields and types you need]
}

Field descriptions:
- fieldName (required/optional): Description of what this field contains
- nestedField.property (required/optional): Description of nested properties

[Any additional requirements: scheduling, specific services to use, etc.]
```

**Always document response fields** with their type, description, and whether they're required or optional. This helps Maia understand exactly what data to return and in what format.

## Examples

### Example 1: Contact Form Processing

**Scenario**: Building a website with a contact form that needs email notification and CRM logging.

**Generated prompt for user**:
```
Create a workflow that processes contact form submissions.

Input: This webhook will receive:
{
  "name": "string",
  "email": "string",
  "message": "string",
  "company": "string (optional)"
}

Actions:
1. Send an email notification to [owner's email] with the form details
2. Log the contact in [CRM name] as a new lead

Output: Return:
{
  "success": boolean,
  "leadId": string
}

Field descriptions:
- success (required): True if the form was processed and logged successfully
- leadId (required): The CRM lead ID created for this contact submission
```

**Instructions to user**:
```
Now message this prompt to Maia. Review the workflow it creates,
deploy it, then paste the webhook URL here so I can connect it
to your contact form's submit button.
```

### Example 2: Product Data Aggregation

**Scenario**: E-commerce site needs to fetch competitor pricing.

**Generated prompt for user**:
```
Create a workflow that fetches competitor prices for a product.

Input: This webhook will receive:
{
  "productName": "string",
  "competitors": ["url1", "url2", "url3"]
}

Actions:
1. Browse each competitor URL
2. Extract the current price for the matching product
3. Calculate average and lowest price

Output: Return:
{
  "prices": [
    { "competitor": string, "price": number, "url": string }
  ],
  "lowestPrice": number,
  "averagePrice": number
}

Field descriptions:
- prices (required): Array of competitor price data
- prices[].competitor (required): Name or domain of the competitor
- prices[].price (required): Current price found on the competitor's site
- prices[].url (required): Direct URL to the product page
- lowestPrice (required): The lowest price found across all competitors
- averagePrice (required): Average of all competitor prices
```

### Example 3: Scheduled Report Generation

**Scenario**: Dashboard needs weekly PDF reports.

**Generated prompt for user**:
```
Create a workflow that generates a weekly sales report.

Input: This webhook will receive:
{
  "startDate": "ISO date string",
  "endDate": "ISO date string",
  "salesData": [array of sales records]
}

Actions:
1. Analyze the sales data
2. Generate charts for revenue trends and top products
3. Create a styled PDF report with executive summary

Output: Return:
{
  "reportUrl": string,
  "summary": {
    "totalRevenue": number,
    "topProduct": string,
    "growthPercent": number
  }
}

Field descriptions:
- reportUrl (required): Public URL to the generated PDF report
- summary (required): Key metrics extracted from the report
- summary.totalRevenue (required): Total revenue for the reporting period
- summary.topProduct (required): Name of the best-selling product
- summary.growthPercent (required): Revenue growth percentage compared to previous period

Deploy this on a weekly schedule (Monday at 9:00 AM).
```

## Multiple Workflows

If a project requires multiple backend automations:

1. **Separate each workflow** into its own Maia session
2. **Instruct user clearly**:
```
This project needs 3 backend automations. Create a new Maia
session for each:

Workflow 1 - Contact Form:
[prompt]

Workflow 2 - Newsletter Signup:
[prompt]

Workflow 3 - Order Processing:
[prompt]

Deploy each workflow and provide me with all 3 webhook URLs.
```

## Webhook Connection Protocol

Maia webhooks behave differently depending on whether the workflow is configured to return a response. The webhook URL format is:

```
https://hooks.modularmind.app/hooks/<hook-id>
```

### Fire-and-Forget (No Response)

When the workflow has no response configured, the webhook is a standard HTTP POST that returns immediately:

```
POST https://hooks.modularmind.app/hooks/<hook-id>
Content-Type: application/json

{ ...payload }
```

Response:
```json
{ "type": "success", "message": "Workflow execution triggered successfully." }
```

### Streaming Response (SSE)

When the workflow is configured to return a response, the webhook uses **Server-Sent Events (SSE)** to stream the result back. The connection stays open with periodic heartbeats while the workflow executes, then delivers the result as an SSE event.

**The agent MUST use an SSE-compatible client** (e.g., `EventSource` or manual `fetch` with stream reading) — not a standard `fetch` expecting a JSON body.

**SSE event types:**

| Event | Data | Description |
|-------|------|-------------|
| `: heartbeat` | *(comment, no data)* | Sent every ~15s to keep connection alive |
| `response` | `{ status, contentType, body, encoding? }` | The workflow result |
| `done` | `{}` | Signals the stream is complete |
| `error` | `{ type, message }` | Workflow execution failed |

**Response event payload:**
- `status` — HTTP status code (e.g., `200`)
- `contentType` — MIME type of the body (e.g., `application/json`)
- `body` — The response content as a string. For text/JSON responses this is the raw UTF-8 string. For binary responses this is base64-encoded.
- `encoding` — Only present for binary responses, set to `"base64"`

**Example frontend integration (JavaScript):**

```javascript
const eventSource = new EventSource('https://hooks.modularmind.app/hooks/<hook-id>');

eventSource.addEventListener('response', (event) => {
  const payload = JSON.parse(event.data);
  // payload.body contains the workflow result
  // For JSON responses: JSON.parse(payload.body)
  const result = JSON.parse(payload.body);
  handleResult(result);
});

eventSource.addEventListener('done', () => {
  eventSource.close();
});

eventSource.addEventListener('error', (event) => {
  try {
    const error = JSON.parse(event.data);
    handleError(error.message);
  } catch {
    handleError('Connection lost');
  }
  eventSource.close();
});
```

> **Note**: `EventSource` only supports GET requests. If you need to POST a payload to the webhook (which is the common case), use `fetch` with `getReader()` on the response stream and parse SSE events manually, or use an SSE library that supports POST (e.g., `@microsoft/fetch-event-source`).

**Example with POST payload:**

```javascript
import { fetchEventSource } from '@microsoft/fetch-event-source';

await fetchEventSource('https://hooks.modularmind.app/hooks/<hook-id>', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ /* your input payload */ }),
  onmessage(event) {
    if (event.event === 'response') {
      const payload = JSON.parse(event.data);
      const result = JSON.parse(payload.body);
      handleResult(result);
    }
    if (event.event === 'done') {
      // Stream complete
    }
  },
  onerror(err) {
    handleError(err);
  }
});
```

## Important Notes

- **Embed webhook URLs in code, not in UI**: When integrating webhook URLs, always hardcode them directly in the application source code (as constants, config values, or environment variables). Never create a user-facing input field or settings panel for pasting webhook URLs — the integration should be seamless and require no manual URL entry by end users.
- **User approves deployments**: Maia suggests deployments but users must manually approve
- **Manual browser control**: Users can control Maia's browser to sign into platforms
- **Flexible input parsing**: Webhooks accept ANY JSON structure - no strict schema required
- **Visual workflow editing**: Users can edit the workflow graph and fill placeholders before deployment
- **Prefer in-house database persistence**: Keep data in the app's own database rather than relying on Maia for storage. When possible, use serverless functions (or equivalent) to call Maia webhooks and write the response back to the database—this decouples automations from the browser session. Maia can also write directly to the app's database, but only if the prompt includes the full HTTP request details: endpoint URL, request method, headers (including auth), path/query parameters, and body structure.
- **Webhook timeout considerations**: Deployed workflows may take significant time to execute (up to an hour for complex flows). The SSE streaming protocol keeps the connection alive with heartbeats, but the agent should still present appropriate loading/progress UI to the user while waiting for the `response` event. If long wait times create poor user experience, consider instructing the user to ask Maia for an asynchronous flow pattern instead—where the webhook immediately acknowledges receipt and sends results via a callback URL or stores them for later retrieval.

## Response Payload Specification

Always specify the exact response format you need. This allows Maia to automatically structure its output for your website/app to consume.

**For each response field, document:**
- **Type**: string, number, boolean, array, object, or union types
- **Description**: What the field contains and how it should be used
- **Required/Optional**: Whether the field will always be present or only in certain conditions

**Be specific** — provide the JSON structure followed by field documentation:
```
Output: Return:
{
  "status": "success" | "error",
  "data": {
    "items": [{ "id": string, "value": number }],
    "total": number
  },
  "message": string
}

Field descriptions:
- status (required): Indicates whether the operation succeeded or failed
- data.items[].id (required): Unique identifier for each item
- data.items[].value (required): The computed numeric value for the item
- data.total (required): Sum of all item values
- message (optional): Error description, only present when status is "error"
```

**Not vague**:
```
Output: Return the results.
```
