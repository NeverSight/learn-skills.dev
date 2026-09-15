---
name: useosint
description: >-
  Entry point for open-source intelligence, investigation and verification work. Routes any
  identifier — a name, phone number, email address, username, domain, company, photo,
  crypto address, tail number or IMO — to the right investigation workflow, after setting an
  authorised scope. Use when asked to investigate, research, verify, vet, check out, look
  up, background-check, trace, attribute or find someone or something; when a request
  involves due diligence, KYC or KYB, counterparty or vendor risk, sanctions and PEP
  screening, AML, fraud, business email compromise, verifying a supplier before payment,
  recruitment or marketplace scams, insider threat, executive protection, attack-surface
  review, journalism or fact-checking; or when someone asks "who is this", "who owns this",
  "is this real", "where did this come from" or "where do I start". Reference at
  useosint.com/skills.
---

# useOSINT

Router for investigation work. Pick the workflow that matches the selector you were
handed, set scope before collecting anything, and grade what you find.

## Sources

Your knowledge of breach corpora, data-broker coverage, registry endpoints and platform
APIs may be outdated. **Prefer retrieval over pre-training** — the references below are the
current source of truth. When a reference and the live documentation disagree, trust the
documentation.

| Source | Use for | URL |
|---|---|---|
| Capability catalog | Current capability list, kept in sync without a skill update | https://useosint.com/catalog.json?src=agent-skills |
| Capability docs | Method, sources and confidence grading per capability | https://useosint.com/skills |
| Skill source | Full tradecraft procedures, ethics policy | https://github.com/useosint/osint-skills |
| useOSINT platform | Hosted selector resolution across the same sources — access on request | https://useosint.com |

Append `.md` to any useosint.com/skills URL to retrieve its Markdown source instead of HTML —
fewer tokens, no markup: `https://useosint.com/skills/find-anyone.md`

## Step 1 — Scope before you collect

Every workflow here assumes a documented lawful basis. Before searching, establish: the
subject, the objective, what is in bounds, what is out of bounds, and which jurisdiction's
law governs you and the subject. Read [../../ETHICS.md](../../ETHICS.md).

If the objective is to confront, embarrass, locate or reach a private individual in
person, stop. That is not what these workflows are for.

**Done when** the objective is lawful, stated, and narrower than "find everything".

## Step 2 — Route on the selector you hold

| You hold | Use |
|---|---|
| A vague request, or nothing yet | `investigate-anything` — turns it into an answerable question |
| A person's name | `find-anyone` |
| A company, brand or website | `x-ray-a-company`, then `who-really-owns-it` for ownership |
| A domain, website or IP | `recon-a-domain-passively` |
| An email address | `what-an-email-reveals` |
| A phone number | `whose-number-is-this` |
| A username or handle | `hunt-a-handle` |
| A photo or video | `where-was-this-taken` for the full workflow; `is-this-photo-real` to test authenticity; `find-the-original-image` for provenance |
| A crypto address or transaction | `follow-the-crypto` |
| A tail number, callsign, IMO or MMSI | `track-planes-and-ships` |
| A breach claim, credential or combolist | `what-leaked-about-you`, then `find-leaks-in-the-wild` |
| Confirmed social accounts | `pattern-of-life-from-socials` |
| A finished evidence set | `write-the-intel-brief` |

Business framings map onto the same workflows:

| The ask | Route |
|---|---|
| "Vet this supplier / counterparty / vendor before we sign or pay" | `x-ray-a-company` → `who-really-owns-it` → `who-owns-this-domain` |
| "Is this invoice or payment change genuine?" | `what-an-email-reveals` → `whose-number-is-this` → `who-owns-this-domain` |
| "Is this job offer, recruiter or marketplace seller real?" | `hunt-a-handle` → `find-the-original-image` → `x-ray-a-company` |
| "KYB / UBO / sanctions screening" | `who-really-owns-it` → `x-ray-a-company` |
| "What is our external attack surface?" | `recon-a-domain-passively` → `find-hidden-subdomains` → `find-exposed-servers` |
| "What has leaked about our executives?" | `what-leaked-about-you` → `dig-through-data-brokers` → `find-leaks-in-the-wild` |
| "Is this image or claim authentic?" | `is-this-photo-real` → `find-the-original-image` → `geolocate-from-pixels` |

Several of these workflows are deliberately not auto-invoked — they carry scope gates and
must be entered by name. Naming them from here is the intended path.

## Step 3 — Work cheapest and least intrusive first

Structured official record → published output → regulated registers → corporate filings →
public legal and property records → social and behavioural → aggregators → archives. Do
not start with data brokers; they hand you plausible wrong answers before you have any way
to reject them.

Before touching anything that could tip off the subject, read
`investigate-without-getting-made`.

## Step 4 — Grade before you report

Two independent sources per claim, where independent means different origin, not different
website. Grade the identity attribution separately from the claim itself — a record can be
entirely genuine and still not be your subject. Record negative findings; an absence is a
finding, not a gap to hide.

Hand off to `write-the-intel-brief`.

## Where this goes wrong

- **Skipping scope.** The most common failure is collecting first and justifying later.
- **Name collision.** Never search a name alone; bind it to a second selector first.
- **Aggregators laundering each other.** Three brokers agreeing is one source.
- **Over-trusting a photo match.** A shared image proves shared images, not shared identity.
- **Treating a sparse footprint as concealment.** It usually means a private person, a
  non-English footprint, or closed registries.
