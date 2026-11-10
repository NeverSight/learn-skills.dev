---
name: digitalocean-costs
description: >-
  Price DigitalOcean changes before billable actions, and read balance, invoices,
  and billing history. Use for "how much will this cost", "my DO bill", "invoice",
  or "balance".
---
# DigitalOcean costs and billing

Load **digitalocean-safety** before any write. This skill is read-heavy; writes
to billing are rare.

## Connectors

- **digitalocean-accounts:** `balance-get`, `billing-history-list`, `invoice-list`,
  `get-invoice`, `account-get-information`
- **digitalocean-droplets:** `size-list`, `region-list` (pricing inputs for Droplets)

Ensure **digitalocean-accounts** is connected; connect **digitalocean-droplets**
for size/region pricing.

## Price-before-create workflow (Tier 4)

1. Call `size-list` (and `region-list` if region matters).
1. Compute or quote **hourly and monthly** for the chosen plan/size and quantity.
1. State that **billing starts immediately** on create/resize/backup enable/snapshot.
1. Only after explicit user confirmation, invoke the Tier 4 tool (see
   **digitalocean-safety**).

## Invoices and balance

- Summarize invoice line items; do not dump full PDFs into chat unless asked.
- Redact account identifiers if the user is sharing a screen.

## Inference & Agents (Serverless Inference)

Apps that call **Serverless Inference** (for example
`https://inference.do-ai.run/v1/chat/completions`) bill against **Inference & Agents**
balance, separate from generic account balance in some views.

Before deploy or when the user adds inference to an app, warn that:

- **$0 balance with auto reload off** can block the account for inference; API
  responses may show **`402 Payment Required`** and **`This account has been blocked`**
  after an initial period of working calls.
- Fix is **billing**, not redeploying the app: add credit or turn on **auto reload**
  at [Account billing](https://cloud.digitalocean.com/account/billing) on the same
  DigitalOcean team as the app.

Use `balance-get` and billing history on **digitalocean-accounts** to summarize
state; do not retry inference requests in a loop expecting a code fix.

## Triggers

Balance, invoices, billing history, and "what will this cost" questions route here
from **digitalocean**.
