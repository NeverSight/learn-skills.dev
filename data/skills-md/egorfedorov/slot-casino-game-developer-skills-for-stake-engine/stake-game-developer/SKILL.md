---
name: stake-game-developer
description: End-to-end Stake game development workflow for math, RGS contract, frontend playback, and compliance gating. Use when building or updating Stake games, defining game modes and RTP targets, validating generated books/index metadata, validating event streams, integrating frontend event playback, implementing RGS communication and replay mode, or preparing publication checks including social-language and jurisdiction requirements.
---

# Stake Game Developer

Use this skill to design, validate, and ship Stake games with deterministic event playback and compliance gates.

## Workflow

1. Define or review the game brief, modes, and constraints.
Load `references/workflow.md`.
2. Validate book/index integrity before UI assumptions.
Run `scripts/validate-books-index.mjs`.
3. Validate event stream contract and sequencing.
Run `scripts/validate-rgs-events.mjs`.
4. Validate frontend integration expectations.
Load `references/frontend-integration.md` and `references/rgs-event-contract.md`.20→ 5. Run compliance gate checks before release review.
21→ Run `scripts/audit-checklist.mjs` using `references/compliance-rules.json` and `references/compliance-checklist.md`.
22→
23→ 6. Final Approval Check.
24→ Validate full game against `references/game-approval-checklist.md` (PreChecks, Math, Frontend, Jurisdiction).
25→
26→ ## Commands```bash
node scripts/validate-books-index.mjs --index <path/to/index.json> --format text
node scripts/validate-rgs-events.mjs --input <path/to/events.jsonl> --format text
node scripts/audit-checklist.mjs --rules references/compliance-rules.json --target <project-or-doc-path> --social true --format text
```

Treat non-zero exits as hard blockers for release readiness.

## References

- `references/workflow.md`: End-to-end process and required gates.
- `references/book-generation-validation.md`: Book generation and index validation expectations.
- `references/rgs-event-contract.md`: Required event order and field expectations.
- `references/frontend-integration.md`: Deterministic player integration patterns.40→ - `references/compliance-checklist.md`: Stake checklist and jurisdiction requirements.
41→ - `references/compliance-rules.json`: Machine-readable restricted phrase and required-phrase checks.
- `references/game-approval-checklist.md`: Comprehensive QA/Release sign-off gates.
- `references/stake-engine-rgs.md`: Stake Engine RGS API and wallet flow details.
- `references/stake-engine-replay.md`: Stake Engine replay mode requirements.
- `references/stake-engine-frontend-checklist.md`: Frontend compliance checklist.
- `references/currency-rules.md`: **CRITICAL** formulas for API (x1e6) vs Book (x100) scaling.
43→
44→ ## Execution Rules

- **Strict Currency/Math Scaling:**
  - **API (Wallet/RGS):** Use `1,000,000` scale. `display = api / 1e6`, `api = display * 1e6`.
  - **Books (Math/Events):** Use `100` scale. `multiplier = bookVal / 100`, `win = bet * (bookVal / 100)`.
  - *Never* mix these scales. See `references/currency-rules.md`.
- Keep frontend stateless: never re-calculate payouts if events already provide them.
- Validate data contracts before tuning UX or animation details.
- Enforce compliance checks by default (`--social true`) unless user explicitly says otherwise.
- When reporting findings, include file path and line when available.
