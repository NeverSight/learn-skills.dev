---
name: docgen-generate
description: Generate professional PDF business documents (invoices, receipts) by calling the DocGen Engine API. Use this skill whenever the user wants to create an invoice, receipt, or any business document as a PDF — even if they say things like "buatkan invoice", "buat kwitansi", "generate faktur", "I need an invoice PDF", "create a receipt for my client", or "tolong bikin invoice buat klien". Also use this when the user provides raw data (a list of items, client name, amounts) and wants a formatted document out of it. If the user uploads a PDF and wants to regenerate or reformat it, use this skill too.
---

# DocGen Generate Skill

You are interacting with the **DocGen Engine** — a REST API that generates PDF business documents from templates and JSON data.

**Base URL**: `https://docgen-production-503d.up.railway.app`  
**API prefix**: `/api/v1`

## Your Job

Help the user generate a professional PDF document (invoice or receipt) by:
1. Collecting the necessary data from the user (or extracting it from what they provide)
2. Calling the DocGen API to generate the PDF
3. Saving the PDF to disk and confirming to the user

You don't need to ask for every single field upfront — make reasonable assumptions for optional fields and proceed. The goal is to get a PDF in the user's hands quickly, not to run an interrogation.

---

## Step 0: If the user uploads a PDF file

**Do NOT say the model can't read PDFs. Do NOT ask the user to paste data manually.**

Instead, immediately call the scan endpoint — the API will extract the data for you:

```
POST /api/v1/scan
Content-Type: multipart/form-data
```

- Field name: `file` — the uploaded PDF
- Query param: `?templateId=invoice` or `?templateId=receipt` (use whichever fits, or omit for auto-detect)

The response returns `extracted` fields and `rawText`. Use the `extracted` fields to pre-fill the generate request. For any required fields missing from `extracted`, make reasonable assumptions or ask once.

Then proceed directly to Step 3 (generate the PDF) using the extracted data.

**This is the correct flow for PDF uploads — always use it.**

---

## Step 1: Pick the template

Two templates are available:
- **`invoice`** — for billing clients (has invoice number, due date, line items, tax)
- **`receipt`** — for payment confirmation (has receipt number, payer name, payment method)

If unclear from context, ask once: "Invoice atau kwitansi?" / "Invoice or receipt?"

Verify available templates with: `GET /api/v1/templates`

---

## Step 2: Collect data

### Required fields for `invoice`

| Field | Type | Notes |
|-------|------|-------|
| `invoice_number` | string | e.g. `INV-2026-001` — generate one if not provided |
| `issue_date` | string | today's date if not specified |
| `due_date` | string | 30 days from issue_date if not specified |
| `client_name` | string | who you're billing |
| `items` | array | at least 1 item |
| `subtotal` | number | sum of qty × unit_price |
| `total` | number | subtotal + tax − discount |

### Required fields for `receipt`

| Field | Type | Notes |
|-------|------|-------|
| `receipt_number` | string | generate if not provided |
| `receipt_date` | string | today if not specified |
| `payer_name` | string | who paid |
| `items` | array | at least 1 item |
| `subtotal` | number | |
| `total` | number | |

### Line item shape

```json
{ "description": "string", "qty": 1, "unit_price": 500000 }
```

### Calculating totals

Always calculate these yourself before sending — the API does not auto-calculate:
- `subtotal` = sum of `qty × unit_price` for all items
- `total` = `subtotal + (tax ?? 0) − (discount ?? 0)`

If the user gives you a `tax_rate` (e.g., 11%), compute `tax = subtotal × tax_rate / 100`.

---

## Step 3: Call the API

> **Important**: Use the exact `snake_case` field names listed in Step 2 — do NOT guess or convert to camelCase. The API will return a 422 with missing field names if you use wrong keys. Do not make exploratory calls to discover the schema; the schema is fully documented here.



```
POST /api/v1/generate
Content-Type: application/json
```

```json
{
  "templateId": "invoice",
  "data": { ...all fields... },
  "options": {
    "useLLM": false,
    "outputFormat": "pdf"
  }
}
```

The response is a **raw binary PDF** — save it directly to disk, don't try to parse it as JSON.

Save the file as: `<templateId>-<invoice_number or receipt_number>.pdf`  
Default save location: current working directory.

### Watermark (optional)

Add a watermark if the user says "draft", "contoh", "sample", or similar. Always use these exact defaults unless the user specifies otherwise:
```json
"watermark": { "enabled": true, "text": "DRAFT", "opacity": 0.12, "fontSize": 80, "color": "#cc0000", "angle": -45 }
```
Do not change `opacity` from `0.12` unless the user explicitly requests it.

### LLM field mapping (optional)

If the user's field names don't match the template (e.g., they say `customer` instead of `client_name`), set `"useLLM": true` to let the API remap fields automatically. Only do this when clearly needed — it adds ~2s latency.

---

## Step 4: Error handling

| HTTP code | Meaning | What to do |
|-----------|---------|------------|
| 400 | Validation error in request body | Fix the fields listed in `details` |
| 404 | Template not found | Check templateId spelling |
| 422 | Missing required fields | Add the fields listed in `missingFields` |
| 500 | Server error | Report error message to user |

If the server is not reachable, tell the user: "DocGen server tidak dapat dihubungi. Cek status deployment di https://railway.app atau coba lagi beberapa saat."

---

## Step 5: Confirm to the user

After saving the PDF, tell the user:
- File name and full path
- Template used and document number
- Total amount (formatted, e.g., "Rp 5.550.000")
- Number of line items

Keep it short — one concise message is enough.

---

## What NOT to do

- Don't tell the user the model can't read PDFs — use `/api/v1/scan` instead
- Don't ask the user to paste PDF data manually when they've already uploaded a file
- Don't ask for optional fields (company_address, company_email, notes) unless the user volunteers them
- Don't show the raw JSON request/response to the user unless they ask
- Don't generate the PDF more than once for the same request
- Don't fail silently — always report errors clearly

---

## Reference

Full API documentation: see `references/api.md`
