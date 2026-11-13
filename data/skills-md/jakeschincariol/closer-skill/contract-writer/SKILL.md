---
name: contract-writer
description: >-
  Contract Writer. Creates the contract and sends it over for you, after your yes. Turns what was
  agreed on the call into a plain-English services agreement (services, fee, term, launch, payment,
  ownership, liability, signature lines), checks the fee against what was actually said on the call
  or in the proposal, writes a print-ready PDF, drafts the email to send it, and marks the deal won
  when the signed copy comes back. Use when the user says "write the contract", "send the agreement",
  "draft a services agreement", "send the paperwork", "they said yes", or "they signed".
argument-hint: "[draft <deal> | pdf <deal> | signed <deal>]"
---

# contract-writer

The Contract Writer closes the loop the same day: the call ends, the agreement goes out within the
hour while they still remember why they said yes.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/contract.py" draft --deal harbor-lane-website \
    --services "A booking-ready website and a managed Google Ads campaign for Harbor Lane Dental." \
    --fee "\$399 per month, no setup fee, billed monthly." \
    --term "Month to month. Cancel anytime with 30 days notice." \
    --launch "Website live within 14 days of signing." --date "October 29, 2026"
python3 "${CLAUDE_SKILL_DIR}/contract.py" pdf --deal harbor-lane-website
python3 "${CLAUDE_SKILL_DIR}/contract.py" record --deal harbor-lane-website --approval "yes" --at 2026-10-29T14:31
python3 "${CLAUDE_SKILL_DIR}/contract.py" signed --deal harbor-lane-website --today 2026-11-02
```

## Steps

1. Read the call notes (`/record-keeper timeline`) and the proposal if there was one. Write the four
   deal sections from what was agreed, in plain words: Services, Fee, Term, Launch.
2. `contract.py draft`. It adds the standard sections (payment, ownership, confidentiality, liability,
   changes) and signature lines, and writes `closer/contracts/<company>-agreement.md` and `.html`.
3. Read any `CHECK:` line out loud to the user. The fee must be an amount that was said on the call or
   in the proposal. If it is not, ask; never "fix" it silently.
4. Show the agreement. Ask: "Is this exactly what you agreed with Dana? Reply yes or no."
5. `contract.py pdf` (headless Chrome), or the user opens the .html and prints to PDF.
6. Draft the email: short, warm, what is attached, what happens next. "Hi Dana, great talking today!
   Here's the agreement for the $399 monthly plan. Sign whenever you're ready and we'll start Monday."
   Ask: "Send this to Dana with the agreement attached? Reply yes or no."
7. On a yes: a Gmail draft with the PDF attached from the user's account, which the user sends (or sent
   through the Gmail connector right after that yes). Then `contract.py record --approval "<their yes>"`.
8. For e-signature, the user can upload the PDF to the e-sign tool they already use; this skill never
   signs for anyone. When the signed copy comes back, `contract.py signed`.

## The user's own terms

The standard sections in `contract.py` (STANDARD) are a sensible starting point for a small services
business, not legal advice. The first time, suggest the user has a lawyer read them once and edit
STANDARD to match. Every agreement after that uses the same reviewed terms.

## Example from the reel

At 2:31 PM, seventeen minutes after Dana's "too expensive", the Services Agreement between Your Agency
and Harbor Lane Dental, dated October 29, 2026: a booking-ready website and a managed Google Ads campaign;
$399 per month, no setup fee, billed monthly; month to month, cancel anytime with 30 days notice; website
live within 14 days of signing. Sent as Harbor-Lane-Dental-Agreement.pdf with the subject "Your agreement
with Your Agency". (Illustrative: both businesses are fictional.)

## What it never does

- Never sends the agreement without the user's yes for that exact email and attachment.
- Never signs, or adds anyone's signature, name-as-signature or initials.
- Never puts a price, discount or promise in the agreement that was not agreed.

## Consent and truth

- Nothing is sent, booked or signed without the user's explicit yes for that exact message, invite or
  document. Claude drafts, the user says "yes", then it goes out from the user's own accounts.
  One yes per message. Never "yes to all".
- Contracts are templates, not legal advice.
- Never invent a number, a result, a client or a deadline. Fill in only what is true and ask when
  something is missing.
