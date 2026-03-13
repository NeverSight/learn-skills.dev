---
name: invoice
description: Generate professional invoices for clients using standardized templates with automatic invoice numbering and client management. This skill should be used when creating invoices for American Laboratory Trading, Empirico, Versa Computing, or other clients with tracked invoice histories.
---

# Invoice Generation Skill

## Overview

Generate professional HTML invoices using pre-configured templates for hourly and subscription billing. Track client information, automatically increment invoice numbers, and maintain invoice history across all clients.

## When to Use This Skill

Use this skill when:
- Creating a new invoice for an existing client by name
- Adding a new client to the invoice system
- Viewing client information or invoice history
- Generating invoices with work log entries (hourly) or subscription billing

## Core Capabilities

### 1. Generate Invoice for Existing Client

When the user requests an invoice for a client by name:

1. **Load client data** from `clients.json` to retrieve:
   - Client details and billing information
   - Invoice type (hourly or subscription)
   - Last invoice number for auto-increment

2. **For hourly invoices:**
   - Request work log entries from the user (they will paste as text)
   - Parse work log format: `Date - Project - Hours - Description`
   - For Versa Computing, parse: `Date - Project - Hours - Description` with separate Project and Description columns
   - Calculate total hours and amount (hours × hourly_rate)

3. **For subscription invoices:**
   - No work log needed
   - Use subscription_name and subscription_amount from client data

4. **Increment invoice number:**
   - New number = last_invoice_number + 1
   - Format: `{invoice_prefix}-2025-{new_number:03d}`

5. **Calculate dates:**
   - Invoice date: Use current date (check system date in environment)
   - Due date: Invoice date + payment_terms_days

6. **Load appropriate template:**
   - Hourly: `assets/hourly-invoice-template.html`
   - Subscription: `assets/subscription-invoice-template.html`

7. **Replace placeholders** with client data:
   - `{{INVOICE_NUMBER}}`, `{{INVOICE_DATE}}`, `{{DUE_DATE}}`
   - `{{CLIENT_NAME}}`, `{{CLIENT_ATTENTION}}`, `{{CLIENT_ADDRESS_LINE1}}`, `{{CLIENT_CITY_STATE_ZIP}}`
   - `{{PAYMENT_TERMS}}` (e.g., "30" for Net 30)
   - `{{PROJECT_REFERENCE}}` or `{{PO_NUMBER}}` as applicable
   - For hourly: `{{TOTAL_HOURS}}`, `{{HOURLY_RATE}}`, `{{SUBTOTAL}}`, `{{TOTAL_AMOUNT}}`
   - For subscription: `{{SUBSCRIPTION_NAME}}`, `{{BILLING_MONTH}}`, `{{AMOUNT}}`
   - Work log entries (populate table rows in HTML)

8. **Special handling for Versa Computing:**
   - Use 4-column work log table: DATE | PROJECT | DESCRIPTION | HOURS
   - Separate project name from description in work log entries
   - Project names go in the PROJECT column, descriptions in DESCRIPTION column

9. **Save invoice:**
   - Filename format: `Invoice-{invoice_number}-{short_name}-{month}-2025.html`
   - Location: User's Desktop (`/Users/arlenagreer/Desktop/`)

10. **Update clients.json:**
    - Set last_invoice_number to new number
    - Set last_invoice_date to invoice date
    - Save changes to maintain accurate history

### 2. Add New Client

To add a new client to the system:

1. Request necessary information:
   - Company name and contact details (attention, address)
   - Invoice type (hourly or subscription)
   - Invoice number prefix (3-letter abbreviation)
   - Billing rate (for hourly) or subscription amount
   - Payment terms in days
   - Special requirements (e.g., project column, PO number)

2. Add new client object to `clients.json` following the existing structure

3. Confirm client has been added successfully

### 3. View Client Information

To view or list clients:
- Read `clients.json` and display client details
- Show invoice history (last invoice number and date)
- List all tracked clients

## Client Database Structure

Client information is stored in `clients.json` in the skill folder. Each client entry includes:

**Required fields (all clients):**
- `name`: Full client name
- `short_name`: Abbreviated name for filenames
- `invoice_prefix`: 3-letter invoice number prefix
- `invoice_type`: "hourly" or "subscription"
- `company_name`: Company name for invoice
- `attention`: Contact attention line
- `address_line1`: Street address
- `city_state_zip`: City, state, and ZIP
- `last_invoice_number`: Last invoice number sent (integer)
- `last_invoice_date`: Date of last invoice (YYYY-MM-DD)
- `payment_terms_days`: Payment terms in days (e.g., 30 for Net 30)

**Hourly invoice fields:**
- `hourly_rate`: Billing rate per hour
- `project_reference`: Default project name
- `requires_project_column`: (optional) true if work log needs separate project column

**Subscription invoice fields:**
- `subscription_name`: Name of subscription service
- `subscription_amount`: Monthly subscription amount

### Current Clients

- **American Laboratory Trading** (INV prefix, hourly billing)
- **Empirico** (EMP prefix, subscription billing)
- **Versa Computing** (VER prefix, hourly billing with project column)

## Invoice Templates

### Hourly Invoice Template

Located at: `assets/hourly-invoice-template.html`

Features:
- Two-page layout: invoice summary (page 1) and detailed work log (page 2)
- Standard work log table: DATE | HOURS | DESCRIPTION
- For clients requiring project column: DATE | PROJECT | DESCRIPTION | HOURS
- Professional styling with Inter font and blue color scheme (#2563eb)
- Print-optimized CSS

Placeholders to replace:
- `{{INVOICE_NUMBER}}`, `{{INVOICE_DATE}}`, `{{DUE_DATE}}`
- `{{CLIENT_NAME}}`, `{{CLIENT_ATTENTION}}`, `{{CLIENT_ADDRESS_LINE1}}`, `{{CLIENT_CITY_STATE_ZIP}}`
- `{{PAYMENT_TERMS}}`, `{{PROJECT_REFERENCE}}`, `{{PO_NUMBER}}`
- `{{TOTAL_HOURS}}`, `{{HOURLY_RATE}}`, `{{SUBTOTAL}}`, `{{TOTAL_AMOUNT}}`
- Work log table rows (HTML tbody content)

### Subscription Invoice Template

Located at: `assets/subscription-invoice-template.html`

Features:
- Single-page layout
- Simplified line items table: Description and Amount only
- Same professional styling as hourly template

Placeholders to replace:
- `{{INVOICE_NUMBER}}`, `{{INVOICE_DATE}}`, `{{DUE_DATE}}`
- `{{CLIENT_NAME}}`, `{{CLIENT_ATTENTION}}`, `{{CLIENT_ADDRESS_LINE1}}`, `{{CLIENT_CITY_STATE_ZIP}}`
- `{{PAYMENT_TERMS}}`, `{{SUBSCRIPTION_NAME}}`, `{{PO_NUMBER}}`
- `{{BILLING_MONTH}}`, `{{AMOUNT}}`

## Workflow Example

**User:** "Generate an invoice for Versa Computing"

**Process:**
1. Read `clients.json` and locate Versa Computing client data
2. Determine invoice type: hourly (requires work log)
3. Prompt: "Please provide the work log entries for this invoice"
4. User pastes work log text
5. Parse entries, extracting: date, project, description, hours
6. Calculate totals: sum hours × hourly_rate
7. Increment invoice number: VER-2025-011 → VER-2025-012
8. Calculate dates: invoice_date (today), due_date (today + 30 days)
9. Load `assets/hourly-invoice-template.html`
10. For Versa, use 4-column work log table format
11. Replace all placeholders with client data and formatted work log entries
12. Save to: `/Users/arlenagreer/Desktop/Invoice-VER-2025-012-VersaComputing-Nov-2025.html`
13. Update `clients.json`: set last_invoice_number to 12, last_invoice_date to today
14. Confirm: "Invoice VER-2025-012 generated and saved to Desktop. Ready for review."

## Important Notes

- **Date handling:** Always check the system date in `<env>` context (Today's date)
- **Work log parsing:** Accept pasted text format, parse carefully to extract all components
- **Decimal hours:** Use decimal format (0.5, 1.0, 2.5) not time format
- **Invoice numbering:** Always auto-increment based on last_invoice_number
- **File location:** Save all invoices to `/Users/arlenagreer/Desktop/`
- **No email sending:** Skill only generates HTML files; user reviews and sends manually
- **Database updates:** Always update `clients.json` after successful invoice generation
- **Template format:** For Versa, modify table structure to include PROJECT column between DATE and DESCRIPTION
