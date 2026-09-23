---
name: de-spin
description: >-
  Use when someone asks what is true, false, misleading, unsupported, unknown,
  or genuinely complicated in a persuasive message, article, pitch,
  advertisement, policy claim, or viral post. Analyze propaganda, spin,
  selective framing, urgency, social proof, deceptive marketing, and
  AI-generated persuasion by tracing claims to evidence and separating literal
  truth from implied conclusions. Do not use to read deception from demeanor,
  adjudicate intent, or replace broad domain research.
license: MIT
---

# De-Spin

Use this skill to determine whether a persuasive message earns its conclusion. The goal is calibrated judgment, not reflexive distrust: distinguish **supported**, **false**, **misleading**, **complicated**, and **unknown** without turning missing evidence into proof of deception.

## Non-negotiable rules

- Judge **claims and evidence**, not the speaker’s body language, confidence, political identity, or presumed motive.
- A literally true sentence may still be misleading when its likely implication, baseline, conditions, or typical outcome is withheld.
- Do not call a claim false unless credible evidence directly contradicts it. Use **unsupported** or **unknown** when evidence is absent or inaccessible.
- Treat repetition, reposts, and a network of affiliated outlets as one evidence stream until independent origins are established.
- Match verification effort to stakes. Slow down before health, financial, legal, security, reputational, or irreversible decisions.

## Workflow

### 1. Define the decision and claim boundary

State what decision the message is trying to move: belief, purchase, share, vote, authorization, or action. Extract each checkable claim separately. Do not audit a paragraph as one unit when it contains several factual assertions.

Classify each claim:

- **Factual:** observable or measurable now or historically.
- **Predictive:** about a future outcome; evaluate assumptions and base rates.
- **Causal:** says X caused Y; requires more than correlation or anecdote.
- **Normative:** value judgment; clarify values rather than pretending it is a fact.
- **Identity or motive:** usually cannot be resolved from the message alone; do not speculate.

### 2. Make the implied claim explicit

For each factual, predictive, or causal claim, write five fields:

| Field | Question |
|---|---|
| Literal claim | What exactly was said? |
| Likely implication | What would a reasonable person infer? |
| Missing context | Which denominator, baseline, timeframe, eligibility rule, or counterexample could change that impression? |
| Required evidence | What source, data, method, or record would make this checkable? |
| Disconfirming evidence | What would show the claim is wrong or materially incomplete? |

Load `references/claim-audit.md` when a claim uses statistics, comparison language, testimonials, research citations, or a causal story.

### 3. Trace provenance before evaluating content

Leave the originating page. Find the earliest available source, then check who owns it, what relevant expertise they have, what incentives apply, and whether independent sources corroborate the same underlying evidence.

Use **lateral reading**: open independent sources rather than judging credibility from the original site’s design, credentials, testimonials, or “About” page. Treat a user-supplied source as an artifact to inspect, not a fact to authenticate from memory. Do not declare a supplied video, document, utterance, or artifact fabricated, nonexistent, or false without directly verifying that conclusion against the supplied source or an authoritative record. If source authenticity remains unresolved, label its provenance **Unknown** and audit the quoted claim conditionally. Load `references/empirical-foundations.md` when choosing source tiers or explaining why an approach is reliable.

### 3a. Validate against the authoritative source of truth

For every material factual claim, identify the authority that can actually settle that claim: original data or the full study for empirical results; the relevant regulator, statute, filing, or official statistic for public claims; or the system owner’s documentation and direct measurement for product behavior. Retrieve that source directly and record its URL, access date, scope, and whether it supports, contradicts, or fails to answer the claim.

Do not treat the speaker’s own marketing, press release, repost, or testimonial as its final validator when an independent or canonical source exists. A material factual claim cannot receive **Supported**, **False**, or **Misleading** until this check is complete. If the appropriate source is unavailable or cannot settle the claim, use **Unsupported**, **Unknown**, or **Complicated** and explain the gap.

Before a final “not found” conclusion about an official record, use an external search restricted to the canonical publisher’s domain (for example, `site:publisher.example "exact entity" "distinct factual anchor"`), then retrieve any matching canonical page. A guessed URL, redirect, blocked result, or failed publisher search is evidence only about that path, not proof that the canonical source is absent. Record the discovery query or canonical URL used.

When evidence comes from a table, chart, PDF extraction, or visually ordered list, verify the label-to-value mapping from the authoritative artifact itself. Do not assign values from flattened extraction order alone. Quote the exact row, figure, or surrounding labels in the working ledger; if the mapping remains ambiguous, mark it **Unknown**.

A missing citation, URL, or provenance trail in the **message** is itself a finding about that message. It does not make the **audit** unsupported when you have directly retrieved the authoritative source of truth. Record both separately: what the message supplied, and what the audit independently established.

### 4. Run the manipulation scan

Name techniques without treating them as proof of falsity:

| Signal | Test |
|---|---|
| Urgency or scarcity | What changes if the decision waits long enough to verify? |
| Authority or prestige | Does the authority have expertise in this exact domain? |
| Social proof | Are apparent supporters independent and representative? |
| Repetition | Is familiarity being mistaken for corroboration? |
| Emotional loading | What concrete proposition remains after fear, anger, disgust, or flattery is removed? |
| False choice | Which viable options or trade-offs were omitted? |
| Pseudo-precision | Are numbers paired with a denominator, method, uncertainty, and comparison? |
| Qualified language | Do “up to,” “as low as,” “starting at,” or “studies show” describe typical conditions? |
| Evidence theater | Is the cited study, expert, graph, or testimonial actually relevant and independently checkable? |
| Inconsistency flood | Are multiple incompatible stories used to create doubt rather than explain reality? |

A signal triggers investigation, not a verdict. The reliable question is: **what evidence would settle the concrete claim?**

### 5. Build the strongest contrary case

Find the best credible evidence against the message’s conclusion, not merely an opposing opinion. Search for primary data, original studies, official records, methodology, and relevant critiques. Record whether the evidence is independent, directly relevant, and current.

Re-evaluate the verdict after this pass. If contrary evidence directly outweighs the message’s support, do not retain **Supported**; use **False**, **Misleading**, **Complicated**, **Unsupported**, or **Unknown** according to the evidence gap and scope.

If sources conflict, explain the mechanism of disagreement: different populations, timeframes, measures, incentives, definitions, or causal assumptions. Do not flatten real disagreement into a false binary.

### 5a. Reconcile delegated checks before publication

Treat subagent and specialist findings as leads, not evidence. Re-open each material source they cite and verify the claim, URL, metric definition, and label-to-value mapping before incorporating it.

Keep a completion ledger for every commissioned check: **pending**, **reconciled**, **rejected**, or **cancelled**. Resolve disagreements against the authoritative source and record why a finding was rejected.

**Publication gate:** do not publish, send, file, or present a final verdict while any commissioned check is pending. Drafting may continue, but the irreversible/public action waits until every check is reconciled or explicitly cancelled. If the delegation mechanism is asynchronous and cannot be awaited in the current turn, defer publication rather than publish-and-amend.

### 6. Report a structured truth assessment

Use `assets/claim-audit.md`. The output must contain these exact sections:

1. **Bottom line** — one calibrated verdict: Supported, False, Misleading, Complicated, Unsupported, or Unknown.
2. **What is true** — narrowly supported parts, each linked to evidence.
3. **What is false** — only directly contradicted claims, with the contradicting evidence.
4. **What is complicated, and why** — important qualifiers, uncertainty, competing evidence, scope limits, and value judgments.
5. **How the message steers perception** — named techniques and the specific inference each invites; do not infer intent.
6. **Authoritative-source check** — the direct source of truth, access date, scope, and whether it supports, contradicts, or cannot settle each material factual claim.
7. **Evidence ledger** — claim, source, source tier, support/contradiction, limitation, and confidence.
8. **Decision-safe next step** — the smallest action that would materially reduce uncertainty.

For a high-stakes claim, retain source URLs and access dates. Load `references/claim-audit.md` for claim decomposition patterns, effort budgeting, and high-stakes escalation rules.

## Verdict definitions

| Verdict | Standard |
|---|---|
| **Supported** | Direct, credible evidence supports the claim within its stated scope. |
| **False** | Direct, credible evidence contradicts the claim. |
| **Misleading** | Literal wording may be true, but omitted context or implication would predictably lead a reasonable reader to a materially wrong conclusion. |
| **Complicated** | Credible evidence is mixed, conditional, or answers a narrower question than the message suggests. Explain why. |
| **Unsupported** | The message makes a checkable claim without adequate accessible evidence. |
| **Unknown** | The needed evidence is unavailable, inaccessible, or insufficient to decide. |

## When not to use

- Use `research-methodology` for a broad, multi-source investigation not driven by a specific persuasive message.
- Use a domain expert or primary technical verification for specialized claims requiring reproduction, diagnosis, legal interpretation, or medical advice.
- Do not use this skill to determine whether a person is lying from video, voice, eye contact, or body language.

## Exit criteria

Stop when every material claim has a verdict or an explicit evidence gap, the report separates truth from implication, the next verification step is proportionate to the decision stakes, and every commissioned check is reconciled, rejected, or cancelled. Public or irreversible delivery remains blocked while any check is pending.
