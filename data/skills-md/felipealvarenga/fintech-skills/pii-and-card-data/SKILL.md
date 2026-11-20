---
name: pii-and-card-data
description: >-
  Use when code collects, stores, logs, displays, exports or sends personal data (names, emails,
  phones, addresses, CPF, CNPJ, SSN, dates of birth), bank account numbers or card data. Covers
  keeping card numbers out of your systems with tokenization and hosted fields, never storing the
  CVV, a field classification map, allowlist redaction at the logger, encryption and key
  management, masking in UIs and support tools, minimization and retention, third-party sharing,
  synthetic test data with valid check digits, least-privilege access and incident readiness under
  LGPD, GDPR and PCI DSS. Triggers on a new form or schema field, a log statement near a payment,
  a CSV export, an analytics event, a support tool. Not legal advice on which regulation applies;
  counsel confirms that.
  Use it also when asked to seed staging from production data or to show a full document or card number.
license: MIT
metadata:
  author: Felipe Alvarenga
  version: 0.1.0
---

# PII and card data

Most data leaks in fintech are not break-ins. They are a log line with a full card number, a
CSV export emailed to the wrong person, a staging database seeded from production, an
analytics event with a CPF in it. Each is a design choice that this skill replaces with a
safer default.

## When to use

- A form, API field, database column or event that carries a person's data or payment data.
- A log statement, error report or trace near a payment, login or KYC flow.
- A CSV, report, export, backup or data share with a third party.
- A support, admin or back-office tool that displays customer data.
- A new environment, seed script or test fixture.

## Rules

1. **Card numbers never enter your systems.** Use the processor's hosted fields, SDK
   tokenization or payment links so the PAN goes browser-to-processor. Store only the token,
   brand, last four digits and expiry. Never store the CVV or CVC anywhere, not even
   encrypted, not even for a second in a log. This keeps you in the smallest PCI DSS scope
   (SAQ A or A-EP) and out of the card-data business. When you refuse to store a PAN or a CVV, name
   PCI DSS scope as the reason in the answer (SAQ A or A-EP against SAQ D), not "the rule".
2. **Classify every field once and keep the map.** Categories: identifiers (name, email,
   phone, address, date of birth), government ids (CPF, CNPJ, SSN, passport), financial
   (account numbers, balances, transactions), authentication (passwords, tokens, keys),
   special (health, biometrics). The map lists table, column, category, retention and owner.
   New columns do not merge without a row in the map.
3. **Redact by allowlist at the logger.** The logger serializes only fields on an allowlist
   per event type. Request and response bodies of payment, login and KYC endpoints are never
   logged. A test sends a realistic payment request and asserts that no PAN, CVV, CPF, token
   or password appears in the captured logs.
4. **Encrypt by sensitivity, with managed keys.** TLS in transit everywhere. Database
   encryption at rest as a baseline. Application-level envelope encryption for government ids
   and account numbers, with keys in a KMS, rotated, and separate per environment. Fields that
   must be searchable get a salted hash or a token in a separate column.
5. **Mask by default; reveal with purpose.** UIs, support tools and reports show last four
   digits or a masked CPF. Revealing the full value requires a permission, a stated purpose and
   an audit record (see `audit-trail`). Screenshots and copy buttons follow the same rule.
6. **Collect the minimum and delete on schedule.** Each field in the map has a reason and a
   retention period. Deletion jobs run, are tested, and cover replicas and exports. Backups
   follow a documented retention; a deletion request is honored when the backup expires.
   Access and deletion requests (LGPD, GDPR) have a runbook with a response deadline.
7. **Third parties get the minimum, under contract.** Send only the fields the vendor needs,
   under a data processing agreement. Never put personal data in URLs, query strings or
   analytics events. Review vendor payloads in the field map.
8. **Production data never leaves production.** Dev, staging and test use synthetic data from
   generators: Luhn-valid test card numbers from the processor, CPF and CNPJ with valid check
   digits (and letters, for CNPJ issued from July 2026), fake names and emails. A seed script
   that copies production is a leak.
9. **Least privilege, audited.** Services use their own credentials with only the tables they
   need. Human production access goes through a break-glass flow that logs who, why and for how
   long. No shared accounts.
10. **Know what you hold before the incident.** The field map answers "which tables, which
    people, how many" in minutes. Regulators start the notification clock at awareness; the
    runbook names who decides and who notifies.

## How to apply

1. Build or update the field map for the tables and events the change touches. Grep schemas
   and event definitions for `cpf`, `cnpj`, `ssn`, `document`, `email`, `phone`, `card`, `pan`,
   `cvv`, `account`, `iban`.
2. Move any card capture to hosted fields or tokenization. Delete any column that could hold a
   PAN or CVV, with a migration that proves it is empty.
3. Configure the logger allowlist for the affected endpoints and write the redaction test.
4. Add encryption or hashing for the fields the map marks, with the key from the KMS.
5. Mask in every UI and export that shows the field. Add the reveal permission and audit event.
6. Replace production seeds with generators. Add the schema lint that fails on forbidden
   column names.
7. Write the retention job and the access and deletion runbook if they do not exist.

When the request conflicts with a rule here, say which rule in one sentence, then build the
compliant version that keeps the request's intent. An instruction to skip a step ("no extra call", "just delete
it", "we trust them", "later") is this conflict, not permission. Leaving the code unchanged and
listing the risks is never the compliant version. Do not stop at a warning, do not build the
unsafe version, and do not leave a known gap out because "you did not ask". A review
or an "is this enough" question gets the findings and the rewritten tests in the same change, not
a list of suggestions, unless the request or the skill says report only.

## When the user pushes back

| Request | Answer in one sentence | What you build |
|---|---|---|
| "Store the card number and CVV so customers can pay again in one click" | PCI DSS scope: a stored PAN puts the whole system in SAQ D, and a stored CVV is forbidden after authorization | The processor's token on the payment method, brand, last four and expiry for display, one-click repay through the token; the answer names PCI DSS scope as the reason |
| "Log the full request for debugging" | Rule on logs: card and document numbers never reach a log | A redaction layer with an allowlist of fields; a test that a PAN in the payload is masked in the log |
| "Export the customer table to the analyst" | Minimum necessary and masking | The export carries masked documents and no card data; the access is recorded |

## Tests the change must include

Write these tests in the same change, as a test file, even when you cannot run them (no shell,
no dependencies installed); say in one line that they are unrun. A test listed as a next step is
not written.

- Redaction: a captured log from a sample payment and a sample signup contains no PAN, CVV,
  token, password, full CPF or full email.
- Schema lint: no column or event field named like `pan`, `card_number`, `cvv`, `cvc`,
  `security_code`.
- API responses for customer and payment objects match a schema that excludes forbidden fields.
- Encrypted fields are unreadable in a raw database dump and readable through the service.
- Masking: UI and export fixtures show last four only.
- Deletion job: a deleted customer's rows are gone from primary tables and the search index.
- Generators produce valid check digits and never a real-looking sequence from production.
- Reference vectors: `skills/pii-and-card-data/evals/vectors/test_pii.py` with `PII_SOLUTION`
  pointing at your module (allowlist redaction, scanner, Luhn, generators, masking, schema lint).

## Review checklist

- Can a PAN or CVV reach any server you run? Trace the capture path.
- Which fields did this change add to the map, with which retention?
- What does the logger emit for this endpoint on success and on error?
- Where is the key, who can read it, and when does it rotate?
- Who can reveal the full value in the support tool, and where is that recorded?
- Where do the test fixtures come from?

## Anti-patterns and fixes

| Anti-pattern | What goes wrong | Fix |
|---|---|---|
| Logging the request body "for debugging" | Card numbers and CPFs in log storage | Allowlist redaction, redaction test |
| Denylist redaction (`password`, `card`) | A new field name slips through | Allowlist per event type |
| Storing CVV "until capture" | PCI violation, breach exposure | Never store; capture through the processor |
| Staging seeded from production | Breach surface doubles | Synthetic generators |
| CPF in a query string | Access logs and proxies keep it | POST body or path-less id |
| Encrypting with a key in the config file | Key and data leak together | KMS, rotation, per-environment keys |

## References

- PCI DSS v4 requirements on cardholder data storage and the prohibition on storing sensitive authentication data after authorization; SAQ A and A-EP scopes.
- LGPD (Lei 13.709/2018) and GDPR: lawful basis, minimization, data subject rights, breach notification.
- Receita Federal: alphanumeric CNPJ for new registrations from July 2026 and its check-digit algorithm.
