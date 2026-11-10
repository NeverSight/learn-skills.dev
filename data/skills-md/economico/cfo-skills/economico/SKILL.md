---
name: economico
description: "Model a business in Economico: discover pricing from code, Stripe and email; find patterns and saved rights; compose plans or bespoke contracts; record evidenced economics and payments; prove the books. Use to connect or set up Economico, explore business models, create custom agreements, resume the books, turn pricing into contracts, set up vendors, record receipts or invoices, or understand Economico."
---

# Economico

Economico is a double-entry ledger with one append-only, hash-chained history per business.
Writes use commands from one catalog over MCP, REST or CLI.
Contracts describe priced rights with independent billing, recognition and payment. Billing
creates claims; registered-account payments settle them. Who pays does not change the right;
lifecycle events are not additional activities. Use only the founder's authorized source access.

## Ground rules

1. **Never touch a real business to experiment.** Rehearse on a disposable business. Before the
   first write, say which business slug you are writing to and why.
2. **Describe before you execute.** `catalog {action: "describe", name}` is the schema of record.
   The recipes in this skill are known-good shapes, not a substitute for the live schema.
3. **Propose, then record.** Discovery produces a written business model the founder reviews.
   Nothing that posts money is recorded until they agree, unless they told you to proceed.
   For setup, ask scope before discovery; the next question round is after the brief is written,
   `model_preview` passes and the model is shown. Keep missing facts as gaps. Ask only decisions,
   recommendation and reason first, through the host's question tool. Read
   [asking the founder](references/asking-the-founder.md) immediately before each round.
4. **Money is a string of minor units.** When reporting, scale exactly once by `10^decimals`,
   using the ledger's `decimals` from `ledgers {action: "get", ledger_id}`. For USD (2 decimals),
   `"4900"` is $49.00; for JPY (0 decimals), `"4900"` is ¥4,900. Dates are `YYYY-MM-DD`;
   instants are UTC with `Z`. The founder's stated business date governs recording and reports.
5. **Preserve supplied IDs exactly.** Copy source IDs into `sourceFactId` and agreement IDs into
   document `externalId`; never reorder or suffix them. Create IDs only when none were supplied.
   Store evidence with `documents.receive`; use stable `idempotency_key`s.
6. **Never invent a number.** Prices, dates and amounts come from code, Stripe, a signed order form
   or a receipt. Missing facts stay gaps in the brief; request their evidence in the final message.
7. **Refusals are information.** A refusal names the rule it applied. Read `code` and `message`,
   fix the input, and do not work around a refusal by changing the economics.
8. **Report what the books say.** After verification, reread
   [show the founder](references/show-the-founder.md) immediately before composing the final
   response. Repeat the tables and decisions here; a brief link does not count.
9. **Complete this batch in the foreground.** Do not delegate to background agents or schedule
   wakeups. Run independent tool reads in parallel, then record, verify and report in this session.

## The one-session run

For setup, read [first session](references/first-session.md) before discovery or questions.
Resolve its unanswered scope choices first. If `business-model.md` already exists, read its
standing answers and gaps, then resume [a later session](references/first-session.md#a-later-session).

| # | Phase | Output | Read |
|---|---|---|---|
| 1 | Connect and settle scope | A verified target and unanswered scope choices resolved before source reads | [connect](references/connect.md), [scope](references/first-session.md#0-agree-the-scope-one-round-of-questions), [questions](references/asking-the-founder.md) |
| 2 | Understand the machine | The mental model you will map the business onto | [how Economico works](references/how-economico-works.md) |
| 3 | Discover | Notes on product, pricing, customers, costs, entity | [codebase](references/explore-codebase.md), [Stripe](references/explore-stripe.md), [email](references/explore-email.md) |
| 4 | Propose | `business-model.md`, passing `model_preview`, then founder review with price book and costs shown | [first session](references/first-session.md), [brief template](references/business-model-brief.md) |
| 5 | Record | The legal form and the owners (the cap table, even for a sole owner), parties, accounts, templates, contracts, activity, evidence; the contracts shown as one table | [products](references/modeling-products.md), [customers](references/customer-contracts.md), [vendors](references/vendor-contracts.md), [evidence](references/evidence.md), [accounts](references/accounts.md), [payments](references/payments.md), [company](references/company-setup.md) |
| 6 | Prove | A final message that opens with the price book, the contracts, the income statement, the balance sheet and the cap table as views, then a short summary | [verify](references/verify.md) |

At phases 4, 5 and 6, show the views in [show the founder](references/show-the-founder.md),
inline when the host renders them, otherwise as text.

## When the request is narrower

| The founder asks to… | Go to |
|---|---|
| connect an agent, log in, pick or create a business, run headless | [connect](references/connect.md) |
| understand how Economico works, or why something was refused | [how Economico works](references/how-economico-works.md) |
| explore business model patterns, reuse rights, combine offerings or draft a bespoke contract | [business model patterns](references/business-model-patterns.md) |
| turn pricing (code, Stripe or a pricing page) into plans | [modeling products](references/modeling-products.md) |
| add a customer, record a signed deal, bill or collect | [customer contracts](references/customer-contracts.md) |
| set up vendors, process receipts or invoices from email | [explore email](references/explore-email.md), [vendor contracts](references/vendor-contracts.md) |
| record payments, reimbursements, transfers or payment corrections | [payments](references/payments.md) |
| choose an account for a cost or a revenue line | [accounts](references/accounts.md) |
| set the company profile, bank accounts, cards, legal identity, founders' shares or the cap table | [company setup](references/company-setup.md) |
| import existing books | [import](references/import.md) |
| check the books after a change | [verify](references/verify.md) |
| see a statement, the contracts or who owes what | [show the founder](references/show-the-founder.md) |
| write an investor update | [investor update](references/investor-update.md) |

## What is not available today

Say so plainly, never approximate: there is no standing Stripe sync, no email listener and
no bank feed (you gather facts with your own access and record them); no planning scenarios or
forecast overlays; no stock options; no tax returns or filings. Economico never moves money, sends
an invoice or signs anything; it records what happened elsewhere.
