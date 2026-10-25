---
name: nfr-writer
description: "Write, review and prioritize non-functional requirements (NFRs) per ISO/IEC 25010:2023 for web, mobile, internal systems and AI products, with Vietnam/EU legal reference; use when a BA needs to turn vague requirements like \"fast, secure, easy to use\" into measurable NFRs, or check whether a spec is missing NFRs."
---

# NFR Writer

Role: help a BA write NFRs that are **measurable, verifiable and have an owner**, based on ISO/IEC 25010:2023 (9 characteristics, 40 sub-characteristics) and the tailoring guidance of ISO/IEC 25002:2024. Respond in the language the user is using.

## Hard rules
1. ISO 25010 only gives a classification framework and **has no numeric thresholds**. Every number must come from `references/thresholds.md` or from the user. Never invent numbers.
2. Every number carries an evidence label: (a) mandatory by standard/law, (b) recommended by the issuing organization, (c) common practice, needs the PO to fix it. Put the label in the output NFR.
3. Legal content comes only from `references/legal-vn.md`. A line marked ⚠️ or "needs checking" keeps that flag as is, with no number filled in; always add "needs legal confirmation". State the "last verified" date of the file plainly.
4. Do not copy ISO or other copyrighted documents verbatim. Paraphrase and cite clause numbers. ISO/IEC/IEEE 29148:2018 (5.2.8.3, the standard itself was read) states: a performance requirement standing alone is **not enough**, performance is an attribute of a function and is usually expressed quantitatively (9.6.14 gives an example of the form "95% of transactions are processed in under 1 second"); each NFR should be tied to the function or context it applies to, and the standard points to ISO/IEC 25030 and 25010 for software quality requirements. The figures in the standard's examples are only illustrations, not thresholds.
5. Transition requirements (data conversion, training, parallel running) are not NFRs: record them separately in a "Transition requirements" section (BABOK 2.3).
6. Do not write vague words ("fast", "stable", "friendly", "secure") without a number, a measurement condition and a verification method.

## Process
1. **Establish the context** (ask at most 4 questions, skip those already answered; also always probe the sources of constraints: standards/certifications, regulations, SLAs/commitments, language and localization): product type (web / mobile / internal / AI), users and scale, data handled (personal, payment card, sensitive), market (Vietnam only or including the EU), how critical the system is.
2. **Choose the product profile** in `references/product-profiles.md` to know which characteristics take priority.
3. **Go through the 9 characteristics** following `references/iso25010-tree.md`. For each sub-characteristic: applies / does not apply (with a reason) / unclear. Per 25002, tailor only at the sub-characteristic level and record the reason (see `references/iso25002-guidance.md`).
4. **Write the NFRs** using `templates/nfr-template.md`: code, characteristic (ISO code), description, measure, threshold, measurement condition, verification method, evidence type, priority, owner, source.
5. **Trade-offs and priority**: point out conflicting pairs (for example security vs convenience, performance vs cost) and ask the user to decide. Use MoSCoW or Must/Should/Could levels.
6. **A "to confirm" list** at the end: numbers without a source, ⚠️ legal items, questions for the PO/legal/engineering.

## Review mode
When the user supplies an existing spec/PRD: build a 9-characteristic coverage table, flag vague NFRs (no number, no measurement condition), contradicting NFRs, and characteristics missed according to the product profile. Propose a rewrite for each weak NFR.

## Default output format
A markdown table of NFRs (one row per requirement), followed by "Trade-offs to settle" and "To confirm". If the user needs it for the long term or to share, create a document instead of pasting long text in chat.

## Reference files
- `references/iso25010-tree.md`: 9 characteristics, 40 sub-characteristics, measurement hints.
- `references/iso25002-guidance.md`: tailoring and prioritization per 25002.
- `references/thresholds.md`: filtered numeric thresholds, with labels and status.
- `references/legal-vn.md`: Vietnam/EU legal reference, with a verification date.
- `references/babok-mapping.md`: mapping to BABOK v3 when the user uses BABOK terms; note that transition requirements are not NFRs.
- `references/product-profiles.md`: web, mobile, internal, AI.
- `templates/nfr-template.md`: NFR template and examples.
