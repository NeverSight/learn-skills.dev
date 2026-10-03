---
name: ingfah
description: "Answer questions about Ingfah (อิงฟ้า) from its bundled user guide (คู่มือ), write FAQ files for its knowledge base (คลังความรู้), and work with the Ingfah client platform through client API-key authenticated APIs. Use when the user asks anything about Ingfah — services, how to do something in the dashboard, telephony, onboarding, settings, billing, release notes — wants an FAQ or knowledge document for an AI Agent, asks to inspect or manage products, AI agents, chat sessions, tools, customer templates, outbound batches, or analytics, or reports something wrong in what they see (a bad call summary or title, wrong outcome labels, an agent saying the wrong thing, missed calls) and wants it fixed, including in the dashboard's English or Thai words: AI Agent Team / ทีม AI Agent, batch / Batch โทรออก, calls / สายทั้งหมด, chats / แชท, templates / เทมเพลตข้อมูลลูกค้า, tools / Tool, knowledge / คลังความรู้, post-call results / ผลลัพธ์หลังวางสาย. Do not use backoffice APIs or JWT-only client APIs."
---

# Ingfah

This skill does three things:

1. **Answers questions about Ingfah** from the bundled user guide — see
   "Answering questions about Ingfah" below. No API key needed.
2. **Writes FAQ files for the knowledge base** (คลังความรู้) — read
   `references/faq-authoring.md` first. No API key needed.
3. **Calls the Ingfah client API** with the user's client API key, using only
   the routes listed below.

The default Ingfah API base URL is `https://api.ingfah.ai`. Use another base URL only when the user explicitly provides one.

This file holds the rules that apply to every task. The detail for each area
is in `references/`; **read the matching file before working in that area**:

| Task | Read first |
|---|---|
| Answer a question about Ingfah or how to use the dashboard | `references/user-guide/INDEX.md`, then the matching page |
| Write, convert, or update an FAQ or knowledge file | `references/faq-authoring.md` |
| Write or edit an agent's prompt | `references/prompt-authoring.md` — a prompt that bakes per-call data into its body is incorrect, not merely suboptimal. Its Jinja section lists engine traps that fail silently, and "Testing a change" has the go-live checklist |
| Create or edit an agent, a revision, or an AI Agent Team | `references/agents-and-teams.md` — every revision must re-send the agent's tool ids, which the revision read does not return |
| Design, build, or change a team of several agents that hand a call between them | `references/multi-agent-teams.md` — handoff tools are minted from the team's edges and named after the target agent's slug; each agent still binds its own tools |
| Create, pause, resume, or cancel an outbound batch | `references/outbound-batches.md` |
| Read, write, or test-run a Tool | `references/tools.md` |
| Design disposition outcomes or an outcome metadata schema | `references/outcome-design.md` |
| Set up automated tests for an agent, or run them before publishing | `references/testing.md`, with the template in `templates/promptfoo-suite/`. The user supplies a model API key and each run costs money |
| Create or edit a postprocessor | `references/postprocessors.md` |
| Set up a Chat Automation (webhook, do-not-contact) | `references/automations.md` |
| Translate a field name the user reads in the dashboard | `references/dashboard-terms.md` |
| The user complains about something they see (a wrong summary, label, answer, or voice; missed calls) | `references/troubleshooting.md` |
| Analytics, text chat inbox, channels, or why outbound calls failed | `references/reporting.md` |
| Create, edit, or delete a customer template | `references/outbound-batches.md` |

## Answering questions about Ingfah

`references/user-guide/` is a copy of the public Thai user guide
(https://docs.ingfah.ai), one Markdown file per page: overview and services,
plans and standards, onboarding, telephony (IP Peering, SIP Registration),
every dashboard guide (AI Agent, Flow, prompting, Tools, knowledge base,
inbound and outbound, results, all calls, settings), and the release notes.

- **Find the page, then read it.** Start from `INDEX.md`, which lists every
  page with its description. For a specific term, search the folder, e.g.
  `grep -ril "say-as" references/user-guide`. Read the whole page before
  answering; steps and caveats are often in a later section or a `:::caution`.
- **Answer only from the guide** (and the other references in this skill).
  Do not fill gaps from general knowledge about voice AI, other products, or
  guesses about pricing, limits, or timelines. When the guide does not cover
  it, say so and suggest asking the Ingfah team.
- **Answer in the user's language**, in the dashboard's words. The guide is
  in Thai; for English speakers translate, and give the Thai menu name the
  first time (e.g. Knowledge — คลังความรู้) since the dashboard shows Thai.
- **Link the page.** End with the public URL from the page's `Source:` line
  so the user can see the screenshots, which are not copied here.
- **Give steps as menu paths**, e.g. ทีม AI Agent → เปิดทีม → ตั้งค่าผลลัพธ์หลังวางสาย.
- **"What's new" or "when did X ship"** — read `release-notes.md`.
- **Offer to do it.** When the answer is a task the client API can perform
  (the routes below), offer to do it for the user; when it is
  dashboard-only, say so (see "Dashboard-only tasks").

For how the platform behaves through the API — field names, state rules,
request bodies — the other `references/` files are more precise than the
guide, which describes the dashboard.

## Client API

Use `scripts/ingfah_api.py` for every request. It is dependency-free and enforces the route allowlist and the mutation confirmation rule. Do not substitute `curl`, `requests`, or an ad-hoc script, even if asked to for speed: doing so bypasses both guardrails, and requests without the script's `User-Agent` header are rejected by Cloudflare with a 403 error-1010.

## Naming: what the user calls things

The API's names and the dashboard's names differ, and most users speak in
dashboard words — often Thai. Translate their words to the API entity below,
and **answer in their words**, not the API's: say "ทีม AI Agent" or "AI Agent
Team", not "product". When a term is ambiguous, name both ("the AI Agent Team
— `product` in the API") once, then stay in their language.

| API entity | Dashboard (EN) | Dashboard (TH) |
|---|---|---|
| `product` | AI Agent Team | ทีม AI Agent |
| automation | Chat Automation | Chat Automation |
| agent | AI Agent | AI Agent |
| revision (unpublished) | Draft / Has Draft | แบบร่าง / มีแบบร่าง |
| revision (published) | Published / Currently Published | เผยแพร่ / เผยแพร่อยู่ |
| publish a revision | Publish | เผยแพร่ |
| chat session (voice) | Call — All Calls | สาย — สายทั้งหมด |
| chat session (text) | Chat — Chats | แชท |
| transcript / messages | Conversation | การสนทนา |
| outbound batch | Batch — Batch Listing | Batch — รายการ Batch |
| outbound option | Template — Manage Templates | เทมเพลตข้อมูลลูกค้า — จัดการเทมเพลต |
| plugin function | Tool | Tool |
| phone tool | Tool (Calling category) | Tool (หมวดการโทร) |
| `direction: inbound` | Inbound | สายเข้า / รับสาย |
| `direction: outbound` | Outbound | สายออก / โทรออก |
| `channel_type: audio` | Voice | เสียง |
| `channel_type: text` | Text | ข้อความ |
| `visibility` | Private / Public | ส่วนตัว / สาธารณะ |
| `starting_agent_id` | Start (starting agent) | จุดเริ่มต้น |
| SIP number | Phone Numbers | เบอร์โทรศัพท์ |
| knowledge base | Knowledge | คลังความรู้ |
| API key | API Keys | จัดการ API Keys |

Field-level dashboard names — postprocessor, agent prompt, and Tool fields, and
the batch and record status words — are in `references/dashboard-terms.md`.

## Working with the user

Most users are not developers. They know the dashboard, not the API, so the
work should end where they can see it.

### When the user reports a problem

Users describe what they see, not which setting to change. Before saying
something cannot be done, **trace what they see back to the setting that
produces it**, then consult: look at the current setting and a few example
calls, name the cause in dashboard words, propose one concrete change with
its exact text, and apply it only after they confirm. The full map and the
common complaints are in `references/troubleshooting.md`. The ones most often
missed:

| What they see | Change this, not the agent's prompt |
|---|---|
| Call title (หัวข้อสนทนา) or summary is wrong, generic, or misreads the business | the team's `summary` postprocessor `instruction`. With none, the team uses a global default that knows nothing about the business, so add one. |
| Outcome label (ผลลัพธ์) is wrong, or everything is สรุปไม่ได้ | each outcome's `prompt` (criteria) in the `disposition` postprocessor |
| A Metadata field is empty or badly formatted | that key's `description` in the `outcome_metadata` `json_schema` |
| "I changed it but nothing changed" | changes apply to new calls only; check that the revision was **published** |
| The agent reads a tool name aloud (`transfer_to_human_agent{}`), promises a transfer that never happens, or repeats its goodbye without hanging up | the agent's tool bindings (`GET /client/agents/{slug}` `phone_tools`) first; a revision posted without them unbinds every tool. Then the prompt around the tool |
| Many outbound calls unanswered or busy | `GET /client/outbound/call-data-records` for the SIP reason, then the batch schedule |

If you told the user earlier that something was not possible and a route
exists for it, correct yourself plainly.

- **Point to where the change shows up.** After a write, name the dashboard
  page the user can open to check it — e.g. "ทีม AI Agent → เปิดทีม →
  ตั้งค่าผลลัพธ์หลังวางสาย" for a postprocessor, or the **Metadata** column on
  สายทั้งหมด for extracted results.
- **Suggest a test before going live, and more than one run.** After drafting or publishing an agent,
  tell the user to open the agent, pick **แบบร่าง** or **เผยแพร่**, and use the
  arrow beside **ทดลอง** → **ตั้งค่าและทดลอง**. Test calls are free and use no
  real phone line. Choosing the job type **รับสาย** there shows every variable,
  so customer context can be filled in by hand. Their transcripts are then
  readable with `GET /client/agents/{slug}/chat-session-tests`. The agent
  varies between calls, so one test call proves little: suggest the same
  scenario two or three times, the main paths as well as the edited one, and
  the go-live checklist in `references/prompt-authoring.md` → "Testing a change".
  For an agent that will be edited more than once, also offer an automated
  test suite (`references/testing.md`).
- **Say when something is dashboard-only.** Some tasks have no client API
  route. Give the user the path in the table below instead of trying another
  endpoint.

### Before building a new agent

Collect these first, and ask for whatever is missing rather than inventing it:

- the agent's role, **gender**, personality, and tone
- the company or brand it represents
- who it will call or answer, e.g. customers who are overdue or just ordered
- what it must say on every call, e.g. a recording consent notice, the due
  date, the amount owed
- the goal — what the customer should agree to or provide
- hard rules — things it must never do or always do
- what should be recorded after the call — the outcome, a promised date, and
  so on; this becomes the disposition outcomes and outcome metadata

### Dashboard-only tasks

| Task | Where in the dashboard |
|---|---|
| Create, rename, or delete an API key | การตั้งค่า → API Keys |
| Assign a phone number to an inbound team | เบอร์โทรศัพท์ → ⋮ → แก้ไข → ทีมรับสายเข้า |
| Upload knowledge files | คลังความรู้ → อัปโหลด; attach in the agent → แก้ไขแบบร่าง → คลังความรู้ icon → บันทึกแบบร่าง |
| Copy a customer template (create, edit, and delete work through the API) | สายออก → จัดการเทมเพลต |
| Upload a batch from a CSV file | สายออก → สร้าง Batch |
| Make a test call or chat | the agent → ทดลอง → ตั้งค่าและทดลอง |
| Add a cloned voice | a service requested from the Ingfah team |
| Data retention, billing, activity logs, guest access | การตั้งค่า — **Owner** only |
| Add or edit a text channel (LINE, Facebook, …) | การตั้งค่า → Channels — **Owner** only |
| Mute the bot, reply as a human, or reassign a chat | แชท |

Knowledge files must be `.pdf`, `.docx`, `.txt`, or `.md`, and must reach
**พร้อมใช้งาน** before they are attached; FAQ files work best as `.md` or
`.txt` written per `references/faq-authoring.md`. A batch CSV must be at most 25 MB,
with column names matching its template.

A missing phone number on เบอร์โทรศัพท์ or on batch creation means no line is
connected yet: the user connects their own telephony or asks the Ingfah team
for a number, which is billed separately.

## Authentication

- Send the key only in the `X-Api-Key` request header.
- If no key is available, ask the user to provide their Ingfah client API key.
  If they have none, tell them to create one at **การตั้งค่า → API Keys →
  สร้าง API Key** on https://ingfah.ai/login. The key is shown **once** only; a
  lost key cannot be recovered, so they create a new one and delete the old.
  A new key has the full access of its account.
- Never echo, log, save, commit, or include the key in generated files, URLs, or error messages.
- Do not ask the user to put the key in this repository.
- Treat the key as available only for the current task unless the user explicitly requests persistent configuration.
- Use HTTPS and the configured Ingfah API base URL.
- Before making a request, explain when the requested operation requires a write scope.
- Ask for explicit confirmation immediately before creating, deleting, pausing, resuming, or cancelling anything.
- Redact secrets from all displayed request and response details.

The script reads `INGFAH_API_KEY` from the process environment. When the user provides a key conversationally, pass it to the script only for the current process; never write it to a file or include it in a command shown to the user.

Examples:

```bash
python3 scripts/ingfah_api.py GET /client/products
python3 scripts/ingfah_api.py GET /client/outbound/batches/7/records --query '?per_page=20&status=called'
python3 scripts/ingfah_api.py --confirm POST /client/outbound/batches --json request.json
python3 scripts/ingfah_api.py --confirm POST /client/outbound/batches/7/pause
python3 scripts/ingfah_api.py GET /client/chat-sessions/{uuid}/record/download --output call.ogg
```

`--json` accepts either a path to a JSON file or an inline JSON document. `--output` saves the response body to a new file instead of printing it; binary responses are refused without it. Run the script from the skill directory, or give its absolute path.

## Client API-key scopes and routes

### `client_products:read`

- `GET /client/ai-agent-teams`
- `GET /client/disposition-outcomes`
- `GET /client/ai-agent-teams/{id}/customer-context-variables`
- `GET /client/products`
- `GET /client/products/{id}`
- `GET /client/products/{id}/automations`
- `GET /client/text-channel-configs`
- `GET /client/text-channel-configs/{id}`
- `GET /client/text-channel-config-providers`
- `GET /client/text-chats/channel-configs`, `/providers`, `/{id}` (same data as the three above)

### `client_products:write`

- `POST /client/products`
- `POST /client/products/{id}/automations`
- `PUT /client/products/{id}/automations/{automationId}`
- `DELETE /client/products/{id}/automations/{automationId}`
- `PUT /client/products/{id}`
- `PUT /client/products/{id}/visibility`
- `DELETE /client/products/{id}`
- `POST /client/products/{id}/postprocessors`
- `PUT /client/products/{id}/postprocessors/{postprocessorId}`
- `DELETE /client/products/{id}/postprocessors/{postprocessorId}`

### `ai_agents:read`

- `GET /client/ai-agents`
- `GET /client/agent-templates`
- `GET /client/agents/{slug}`
- `GET /client/agents/{slug}/revisions`
- `GET /client/agents/{slug}/revisions/{id}`
- `GET /client/phone-tools`
- `GET /client/plugin-functions`
- `GET /client/plugin-functions/{id}`
- `GET /client/plugin-function-integrations`
- `GET /client/voices`

### `ai_agents:write`

- `POST /client/agents`
- `DELETE /client/agents/{slug}`
- `PUT /client/agents/{slug}/profile`
- `PUT /client/agents/{slug}/description`
- `PUT /client/agents/{slug}/visibility`
- `POST /client/agents/{slug}/revisions`
- `POST /client/agents/{slug}/revisions/{id}/publish`
- `POST /client/agents/{slug}/publish` (publishes the newest revision; prefer the route above, which fails if someone drafted after you)
- `DELETE /client/agents/{slug}/revisions/{id}`
- `POST /client/plugin-functions`
- `PUT /client/plugin-functions/{id}`
- `DELETE /client/plugin-functions/{id}`
- `POST /client/plugin-functions/{id}/duplicate`
- `POST /client/plugin-functions/{id}/test-run`

### `chat_sessions:read`

- `GET /client/chat-sessions`
- `GET /client/chat-sessions/{uuid}`
- `GET /client/chat-sessions/{uuid}/record`
- `GET /client/chat-sessions/{uuid}/record/download`
- `GET /client/chat-sessions/{uuid}/record/checksum`
- `GET /client/chat-sessions-list`
- `GET /client/chat-sessions-list/csv`
- `GET /client/agents/{slug}/chat-session-tests`
- `GET /client/agents/{slug}/chat-session-tests/{uuid}`
- `GET /client/text-chats/conversations`
- `GET /client/text-chats/conversations/{uuid}`
- `GET /client/text-chats/chat-sessions-list`
- `GET /client/text-chats/chat-sessions-list/csv`

### `analytics:read`

- `GET /client/analytics/summary`
- `GET /client/analytics/short-calls`
- `GET /client/analytics/hourly-charts`
- `GET /client/analytics/duration-histogram`
- `GET /client/analytics/heatmap`
- `GET /client/analytics/speech-ratio`
- `GET /client/analytics/report/download` (XLSX; use `--output`)
- `GET /client/text-analytics/summary`
- `GET /client/text-analytics/messages-hourly`
- `GET /client/text-analytics/heatmap`

### `client_outbound_options:read`

- `GET /client/outbound/options`
- `GET /client/outbound/options/{id}`

### `client_outbound_options:write`

- `POST /client/outbound/options`
- `PUT /client/outbound/options/{id}`
- `DELETE /client/outbound/options/{id}`

### `client_outbound_batches:read`

- `GET /client/outbound/batches/{id}`
- `GET /client/outbound/batches/{id}/records`
- `GET /client/outbound/batches/{id}/records/download`
- `GET /client/outbound/call-data-records`

### `client_outbound_batches:write`

- `POST /client/outbound/batches`
- `POST /client/outbound/batches/{id}/pause`
- `POST /client/outbound/batches/{id}/resume`
- `POST /client/outbound/batches/{id}/cancel`

## Scope handling

Before calling an endpoint, identify its required scope and check the user's intended action against that scope. If the API returns an authorization or insufficient-scope error, explain the missing scope without exposing the API key.

The automation routes are live but absent from the OpenAPI spec; see
`references/automations.md`. Do not call backoffice routes, API-key management routes, or client routes not listed in this file. Do not infer that a JWT-only route is available to an API-key caller.

## Rules that apply in every area

The reference files hold the detail; these are the rules not to miss even
without opening one.

- **Real-world effects need a preview and explicit confirmation immediately
  before sending.** Creating a batch places real calls. Publishing a revision
  changes a live agent. Test-running a Tool sends its real request. An
  automation sends customer data to a third party on every matching call.
- **Read before writing.** Revisions, Tool updates, postprocessor updates, and
  team `transferabilities` replace what they are given rather than patching it.
  Read the current state, change only the fields being edited, and send the
  whole body.
- **Never publish a revision that unbinds tools.** A revision stores only the
  tool ids it is sent (`phone_tools`, `ai_plugin_function_ids`), and the
  revision read does not return them. Copy them from `GET /client/agents/{slug}`
  into every revision body, list them in the preview, and re-read the agent
  after publishing. The script refuses a revision that would drop a bound
  tool; `--allow-tool-drop` is only for removing a tool on purpose. Getting
  this wrong leaves an agent that reads out
  `transfer_to_human_agent{}` instead of transferring, and cannot hang up.
- **Verify after writing.** Read the object back and report what was actually
  stored, not what the write response implied. `POST /client/agents` in
  particular drops the prompt fields sent with it. For a revision, compare the
  agent's `phone_tools` and `ai_plugin_functions` too, not only the prompt.
- **Report state rules as state rules.** A `403` on visibility means the key's
  admin did not create the object; a `409` or `422` on delete means something
  still uses it. Neither is an authentication failure.
- **Postprocessor and automation changes apply to new calls only.** Calls that
  already ended are not reprocessed.
- **Redact.** Never show API keys, webhook auth headers, or `hmac_secret`.
  Treat outcome metadata and transcripts as personal data.

## Response handling

Return concise, structured summaries. Preserve identifiers, statuses, timestamps, and relevant error details, but remove credentials and unrelated personal or sensitive data. For downloads, save or present the result only when the user explicitly requests it.

### Call recordings

A voice call's recording is read three ways, all under `chat_sessions:read`:

- `GET /client/chat-sessions/{uuid}/record` returns a link to the audio,
  valid for 15 minutes, with its SHA-256 checksum. Anyone holding the link can
  play the call until it expires, so treat it like personal data: do not paste
  it into shared places, and give it only to the user who asked.
- `GET /client/chat-sessions/{uuid}/record/download` returns the Ogg file
  itself. Save it with `--output` only when the user asks for the file.
- `GET /client/chat-sessions/{uuid}/record/checksum` returns only the
  checksum, for checking a download.

Opening a recording through the link or the download route is written to the
account's activity log under the API key. A `404` with `no audio recording
available` means no recording is stored for that session, as with any
text chat.

Recordings, transcripts, and batch data are deleted automatically once they
pass the account's data-retention period, set by an Owner under การตั้งค่า →
การเก็บรักษาข้อมูล. When an old call has no recording or transcript, mention
retention as a likely reason rather than reporting a fault.
