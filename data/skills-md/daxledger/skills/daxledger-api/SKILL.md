---
name: daxledger-api
description: >
  Use the DAX Ledger API to authenticate, list portfolios, retrieve portfolio KPIs,
  list findings, retrieve position snapshots, and list/filter transactions with pagination.
---

# DAX Ledger API

Base URL  
https://app.daxledger.io

---

# Environment Variables

| Variable             | Description                     |
| -------------------- | ------------------------------- |
| DAXLEDGER_API_KEY    | API key used to authenticate    |
| DAXLEDGER_API_SECRET | API secret used to authenticate |

---

# Authentication

POST /api/auth/external_api

Body:

{
"APIKey": "{{DAXLEDGER_API_KEY}}",
"APISecret": "{{DAXLEDGER_API_SECRET}}"
}

Response:

{
"token": "your_access_token_here"
}

Header for authenticated calls:

Authorization: Bearer {{token}}

---

# Pick Your Endpoint

| You need                                    | Endpoint                                                                  | Ref                |
| ------------------------------------------- | ------------------------------------------------------------------------- | ------------------ |
| Authenticate                                | POST /api/auth/external_api                                               | references/apis.md |
| List portfolios                             | GET /api/portfolios                                                       | references/apis.md |
| Get KPIs                                    | GET /api/portfolio/{portfolioId}/kpis/portfolio                           | references/apis.md |
| Get findings (problems in portfolio)        | GET /api/portfolio/{portfolioId}/findings?page=1&pageSize=20              | references/apis.md |
| Get finding by rule id                      | GET /api/portfolio/{portfolioId}/finding/{ruleId}                          | references/apis.md |
| Get position snapshot (balances and values) | GET /api/portfolio/{portfolioId}/position_snapshot?page=1&pageSize=20     | references/apis.md |
| Get token position graph                    | GET /api/portfolio/{portfolioId}/position_snapshot/graph/{ticker}?span=30 | references/apis.md |
| Get DeFi positions                          | GET /api/portfolio/{portfolioId}/positions_report/defi                     | references/apis.md |
| Get capital gains report                    | GET /api/portfolio/{portfolioId}/capital_gains_report?page=1&pageSize=20  | references/apis.md |
| Get capital gains available filters         | GET /api/portfolio/{portfolioId}/capital_gains_report/filters              | references/apis.md |
| Get sanity check report                     | GET /api/portfolio/{portfolioId}/sanity_check_report?page=1&pageSize=20   | references/apis.md |
| Get calculation summary report              | GET /api/portfolio/{portfolioId}/calculation_summary_report?page=1&pageSize=20 | references/apis.md |
| Get fiscal report                           | GET /api/portfolio/{portfolioId}/fiscal_report?page=1&pageSize=20         | references/apis.md |
| List transactions                           | GET /api/portfolio/{portfolioId}/transactions?page=1&pageSize=20          | references/apis.md |
| Filter transactions                         | GET /api/portfolio/{portfolioId}/transactions?filter=<BASE64>             | references/apis.md |

---

# Transactions

Endpoint

GET /api/portfolio/{portfolioId}/transactions

Query params

page  
pageSize  
filter

---

# Findings

## List Findings

Endpoint

GET /api/portfolio/{portfolioId}/findings

Query params

page  
pageSize

Use this endpoint when the user asks for problems or findings in a portfolio.

---

## Finding By Rule Id

Endpoint

GET /api/portfolio/{portfolioId}/finding/{ruleId}

Use this endpoint when the user asks for findings tied to a specific rule/identifier returned in findings.

---

# Position Snapshot

## Positions Snapshot (balances and values)

Endpoint

GET /api/portfolio/{portfolioId}/position_snapshot

Query params

page  
pageSize  
filter  
sort

Use this endpoint when the user asks about token balance or token value.

---

## Position Snapshot Graph By Ticker

Endpoint

GET /api/portfolio/{portfolioId}/position_snapshot/graph/{ticker}

Query params

span (7, 30, 365, -1)

Use this endpoint when the user asks about a specific token holding over time or on a specific date range.

---

## DeFi Positions

Endpoint

GET /api/portfolio/{portfolioId}/positions_report/defi

Use this endpoint when the user asks to retrieve all DeFi positions.

---

# Reports

## Capital Gains Report

Endpoint

GET /api/portfolio/{portfolioId}/capital_gains_report

Available filters endpoint

GET /api/portfolio/{portfolioId}/capital_gains_report/filters

Query params

page  
pageSize  
filter  
sort

Use this endpoint when the user asks for gains/losses by asset and realized/unrealized values.

Capital gains filters:

- digitalAssetTicker (operator: contains_in)
- report_year (operator: =)
- portfolioConnection (operator: =)

If `isSeparateSetting=true` in capital gains response, run the endpoint with several filters using the values from `/capital_gains_report/filters` to retrieve separate results.

---

## Sanity Check Report

Endpoint

GET /api/portfolio/{portfolioId}/sanity_check_report

Query params

page  
pageSize

Use this endpoint when the user asks for balance mismatches between calculated and reported balances.

---

## Calculation Summary Report

Endpoint

GET /api/portfolio/{portfolioId}/calculation_summary_report

Query params

page  
pageSize  
filter  
sort

Use this endpoint when the user asks for high-level calculated totals and summary metrics.

---

## Fiscal Report

Endpoint

GET /api/portfolio/{portfolioId}/fiscal_report

Query params

page  
pageSize  
filter  
sort

Use this endpoint when the user asks for fiscal/tax line items with acquisition, sale, and holding details.

---

# Transaction Filters

Filters must be encoded with Base64 before sending.

---

## Transaction Hash

Operator: contains

{"transactionHash":{"operator":"contains","value":"123456789"}}

---

## Transaction Date

Operator: between

{"transactionDate":{"operator":"between","value":{"startDate":"2026-03-01T00:00:00Z","endDate":"2026-03-02T23:59:59Z"}}}

---

## Transaction Type

Operator: contains_in

{"transactionType":{"operator":"contains_in","value":["computed-reward"]}}

Available transaction types:

- airdrop
- bonus
- computed-deposit
- computed-reward
- deposit
- other
- reward
- staking
- trade
- unknown
- unstaking
- withdrawal

---

# Combining Multiple Filters

Multiple filters can be applied in the **same JSON object**.

Example combining:

- transaction hash
- transaction type
- transaction date

Example JSON:

{
"transactionHash": { "operator": "contains", "value": "123456" },
"transactionType": { "operator": "contains_in", "value": ["trade","deposit"] },
"transactionDate": {
"operator": "between",
"value": {
"startDate": "2026-03-01T00:00:00Z",
"endDate": "2026-03-31T23:59:59Z"
}
}
}

Encode this JSON to Base64 and pass it as:

GET /api/portfolio/{portfolioId}/transactions?filter=<BASE64>&page=1&pageSize=20

---

# Encoding Filters

Browser

btoa(JSON.stringify(filter))

Node

Buffer.from(JSON.stringify(filter)).toString("base64")

---

# Epoch Fields

If an API field is an epoch timestamp, convert it to ISO date before returning it to the user.

Rule:

- 10 digits -> seconds
- 13 digits -> milliseconds

Example (Node):

new Date(Number(epoch) < 1e12 ? Number(epoch) * 1000 : Number(epoch)).toISOString()

---

# Pagination

page starts at 1

pageSize default = 20

Continue requesting pages while:

items.length < total

---

# References

references/apis.md
