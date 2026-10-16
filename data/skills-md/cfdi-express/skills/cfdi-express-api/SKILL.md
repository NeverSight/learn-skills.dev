---
name: cfdi-express-api
description: >-
  Integrate the CFDI Express REST API to issue Mexican CFDI 4.0 invoices from
  any system: PUE/PPD/global invoices, credit notes, payment complements (REP /
  Pagos 2.0), payroll receipts (nómina / Nómina 1.2), cancellations with SAT
  acknowledgment, issuer (RFC/CSD)
  management, SAT catalogs and prepaid balance. Stripe-style conventions.
  Use when the user needs to stamp, list, fetch or cancel CFDIs (including
  recibos de nómina), register issuers or upload CSD certificates, search SAT
  product/unit/usos/regimen/nómina codes, check balance and usage, or receive
  webhooks about stamped documents against api.cfdi.express.
metadata:
  short-description: Integrate the CFDI Express invoicing REST API
---

# CFDI Express API

REST API that stamps CFDI 4.0 documents against the SAT from any system that
speaks HTTPS: PUE, PPD and global invoices, credit notes, payment complements
(REP), payroll receipts (nómina) and cancellations with acknowledgment. Stripe-style conventions:
secret keys, idempotency keys, cursor pagination, RFC 7807 errors.

$1 MXN per stamp, prepaid balance, free unlimited sandbox.

## Authoritative sources — always fetch exact schemas, never guess

- OpenAPI spec (generate clients from it): https://api.cfdi.express/openapi.json
- Interactive docs (try endpoints live): https://api.cfdi.express/docs
- Agent-friendly reference index: https://cfdi.express/docs/api/llms.txt
- Per-endpoint markdown: append `/llms.txt` to any guide URL,
  e.g. https://cfdi.express/docs/api/timbrar-factura/llms.txt

Read the relevant `llms.txt` page before writing code against an endpoint.

## Base URL and auth

- Base: `https://api.cfdi.express`, all v1 endpoints under `/v1`. HTTPS only.
- Every request: `Authorization: Bearer sk_test_...` or `sk_live_...`
- `sk_test_` stamps in the PAC sandbox for free; `sk_live_` issues real
  CFDIs. Modes never share balance, issuers or documents (`livemode` field).
- Keys are secret: server-side only, never browsers or mobile apps.
- Get keys at https://dash.cfdi.express

```bash
curl https://api.cfdi.express/v1/balance \
  -H "Authorization: Bearer sk_test_..."
```

## Core rules

- **Idempotency**: stamping/cancel endpoints require an `Idempotency-Key`
  header with a stable value per logical operation (your order id, etc.).
  Replays return the original response with `Idempotency-Replayed: true`.
  Same key + different body → `422`; concurrent same key → `409`.
- **Errors**: `application/problem+json` with stable `code`:
  `validation_error` (400, includes `errors[]` with field paths),
  `unauthorized` (401), `forbidden` (403), `not_found` (404),
  `insufficient_credits` / `monthly_limit_reached` (402),
  `request_in_flight` (409), `idempotency_key_reuse` / `sat_rejected` (422),
  `rate_limited` (429, honor `Retry-After`),
  `pac_unavailable` (503, safe to retry with same key), `internal_error` (500).
- **Pagination**: cursor-based. `limit` (max 100) + `starting_after=<last id>`
  while `has_more` is `true`.
- **Limits**: 300 req/min per account; 1 MB body; 1,000 concepts per invoice.
- **Signed URLs**: XML/PDF/ZIP/acknowledgment URLs expire after 15 minutes —
  refetch the resource when you need fresh ones.
- **Credits**: each stamp reserves 1 credit and commits it on UUID issuance;
  SAT rejection or PAC failure auto-refunds. Cancellations also consume 1.

## Integration flow

1. Register an issuer: `POST /v1/merchants` (RFC, régimen fiscal, ZIP, serie)
2. Upload its CSD: `POST /v1/merchants/{id}/csd` (.cer/.key base64 + password)
3. Stamp: `POST /v1/invoices` (tax engine computes IVA/IEPS for you)
4. Deliver XML/PDF via signed URLs from `GET /v1/invoices/{id}`

For refunds/discounts: `POST /v1/credit_notes`. For PPD collections:
`POST /v1/invoices/{id}/payments` stamps the REP complement. For payroll:
`POST /v1/nominas` stamps one recibo de nómina (CFDI N + complemento Nómina 1.2)
per employee and pay period — send `employee`, `percepciones`, `deducciones`
(ISR = tipo 002), `otrosPagos` (subsidio al empleo = tipo 002) and the API
derives every SAT total; claves come from `GET /v1/catalogs/nomina/{catalog}`.

## Endpoints

| Resource | Endpoints |
|---|---|
| Invoices | `POST /v1/invoices` · `GET /v1/invoices` · `GET /v1/invoices/{id}` · `POST /v1/invoices/{id}/cancel` |
| Credit notes | `POST /v1/credit_notes` |
| Payments (REP) | `POST /v1/invoices/{id}/payments` · `GET /v1/payments` · `GET /v1/payments/{id}` · `POST /v1/payments/{id}/cancel` |
| Nómina (payroll) | `POST /v1/nominas` · `GET /v1/nominas` (filters `employeeRfc`, `fechaPagoFrom/To`) · `GET /v1/nominas/{id}` · `POST /v1/nominas/{id}/cancel` |
| Issuers | `GET/POST /v1/merchants` · `GET/PATCH/DELETE /v1/merchants/{id}` · `POST/PUT/GET /v1/merchants/{id}/csd` · `PUT/DELETE /v1/merchants/{id}/logo` |
| SAT catalogs | `GET /v1/catalogs/{products,units,usos-cfdi,regimenes,formas-pago}` · `GET /v1/catalogs/nomina/{tipo-percepcion,tipo-deduccion,tipo-otro-pago,tipo-contrato,tipo-regimen,periodicidad-pago,tipo-jornada,riesgo-puesto,tipo-incapacidad,tipo-horas,origen-recurso,estado,banco,tipo-nomina}` |
| Balance & billing | `GET /v1/balance` · `POST /v1/billing/checkout_sessions` · `POST /v1/billing/portal_sessions` · `GET /v1/billing/usage` · `GET /v1/billing/transactions` |
| Meta | `GET /health` · `GET /ready` |

Guide for each endpoint: https://cfdi.express/docs/api (append `/llms.txt` for markdown).

## Alternative for AI agents: MCP

Instead of raw REST, agents can connect to the MCP server at
`https://api.cfdi.express/mcp` (sandbox: `/mcp/test`) — 18 tools covering
stamping, cancellation, queries and catalogs, auth via API key or OAuth 2.1.
Guide: https://cfdi.express/docs/api/mcp
