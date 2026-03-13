---
name: quickbooks
description: "Query QuickBooks Online — invoices, customers, payments, accounts, and reports via the REST API."
metadata: {"thinkfleetbot":{"emoji":"📒","requires":{"bins":["curl","jq"],"env":["QUICKBOOKS_ACCESS_TOKEN","QUICKBOOKS_REALM_ID"]}}}
---

# QuickBooks Online

Query invoices, customers, payments, and reports via the QuickBooks API.

## Environment Variables

- `QUICKBOOKS_ACCESS_TOKEN` - OAuth 2.0 access token
- `QUICKBOOKS_REALM_ID` - Company ID (realm ID)

## Query customers

```bash
curl -s -H "Authorization: Bearer $QUICKBOOKS_ACCESS_TOKEN" \
  -H "Accept: application/json" \
  "https://quickbooks.api.intuit.com/v3/company/$QUICKBOOKS_REALM_ID/query?query=SELECT%20*%20FROM%20Customer%20MAXRESULTS%2010" | jq '.QueryResponse.Customer[] | {Id, DisplayName, PrimaryEmailAddr, Balance}'
```

## List invoices

```bash
curl -s -H "Authorization: Bearer $QUICKBOOKS_ACCESS_TOKEN" \
  -H "Accept: application/json" \
  "https://quickbooks.api.intuit.com/v3/company/$QUICKBOOKS_REALM_ID/query?query=SELECT%20*%20FROM%20Invoice%20MAXRESULTS%2010" | jq '.QueryResponse.Invoice[] | {Id, DocNumber, CustomerRef, TotalAmt, Balance, DueDate}'
```

## Create invoice

```bash
curl -s -X POST -H "Authorization: Bearer $QUICKBOOKS_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://quickbooks.api.intuit.com/v3/company/$QUICKBOOKS_REALM_ID/invoice" \
  -d '{"CustomerRef":{"value":"1"},"Line":[{"Amount":100,"DetailType":"SalesItemLineDetail","SalesItemLineDetail":{"ItemRef":{"value":"1"}}}]}' | jq '.Invoice | {Id, DocNumber, TotalAmt}'
```

## Get profit/loss report

```bash
curl -s -H "Authorization: Bearer $QUICKBOOKS_ACCESS_TOKEN" \
  -H "Accept: application/json" \
  "https://quickbooks.api.intuit.com/v3/company/$QUICKBOOKS_REALM_ID/reports/ProfitAndLoss?start_date=2024-01-01&end_date=2024-12-31" | jq '.Header, .Rows.Row[:5]'
```

## Notes

- Use sandbox URL `https://sandbox-quickbooks.api.intuit.com` for testing.
- Always confirm before creating invoices or payments.
