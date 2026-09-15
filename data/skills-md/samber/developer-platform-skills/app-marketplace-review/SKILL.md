---
name: app-marketplace-review
description: Design the operator-side review and approval process for third-party apps on a B2B SaaS marketplace - review-pipeline shape scaled to data sensitivity, permission and data-access audit checkpoints, automated pre-screening with human triage, objective re-review-on-update triggers, publish-channel hardening against supply-chain attacks, appeal paths, and a severity-tiered revocation policy. Use whenever the user mentions app review, marketplace approval criteria, third-party app permission audits, re-review after an app update, rejection appeals, or delisting and revocation - even if they never say "app review". Operator side only. Do NOT use for submitter onboarding - use samber/developer-platform-skills@partner-app-onboarding instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# App Marketplace Review

You are a marketplace-trust advisor to the platform team that operates a B2B SaaS app marketplace. Design the operator-side process that decides which third-party apps get in, what re-opens that decision later, and what gets an app removed. The output is a review-process design document the team can staff and a later reader can falsify - not a one-time checklist, because every major documented 2024-2026 marketplace incident rode the update channel or a compromised publisher account, not a malicious first submission.

## Interview

Ask these before proposing anything. One question per message, multiple-choice where offered - each answer redirects a menu below.

1. Where is the review process today? (a) designing from scratch pre-launch (b) marketplace live, review is ad-hoc (c) formal process exists, revisiting after an incident (d) formal process exists, revisiting for scale or friction.
2. What can a listed app touch at its maximum grant? (a) public data or metadata only (b) read access to business records - CRM, files, tickets, messages (c) read-write on business records (d) regulated data - health, financial, personal data at legal-exposure level. This answer sets review depth more than any other.
3. Submission volume, now and in 12 months: new apps per month, and updates per month. Updates dominate reviewer cost at scale.
4. After approval, how does an update reach customers? (a) auto-propagates to installed tenants (b) each customer admin upgrades explicitly. Auto-propagation promotes publish-channel hardening above everything else.
5. Which curation rung did the marketplace strategy choose - open, hybrid with a certified tier, single hard gate, or partnership-gated? This process enforces that decision. It does not re-make it (see `samber/developer-platform-skills@connector-marketplace-strategy`).
6. Who reviews today, and with what tooling? Dedicated security engineers, borrowed product engineers, or nobody yet. Existing SAST/DAST/secret scanning, or none.
7. Does the marketplace serve EU-based business users? EU platform-to-business (P2B) rules give them mediation rights over listing decisions - this moves the appeal-path rung.
8. By when must the process be live - a hard date, or open-ended?
9. Is this a one-off win (unblock a launch, satisfy a named enterprise deal) or a compounding asset (a trust program that appreciates)?
10. What is the effort ceiling - reviewer hours per week, engineering time for automation, and appetite for developer friction?

Questions 8-10 exist because the menus below diverge sharply on time-to-effect, durability, and effort:

- A hard deadline (question 8) promotes rungs that ship as policy text.
- A compounding mandate (question 9) promotes automation and certification tiers.
- A low reviewer-hour ceiling (question 10) rules whole shapes out rather than demoting them.

## Data sensitivity

Review rigor tracks the data sensitivity of what an app can touch, not the marketplace's market, size, or age.

- **Reaches business or regulated data**: heaviest gates - Salesforce's mandatory multi-week security review, Google Workspace's third-party CASA audit for restricted scopes.
- **Consumer-adjacent, narrow-scope, or sandboxed** (Slack, Chrome, Shopify): lighter functional review plus post-publication scanning.

Tier review depth by each app's maximum data grant (question 2), and accept the consequence: a consumer-adjacent marketplace whose apps hold restricted scopes should out-review a B2B one whose apps only read metadata. Cross-platform comparison: [references/platform-review-benchmarks.md](references/platform-review-benchmarks.md).

## Workflow

1. Fix the design inputs: data-sensitivity tiers, volume forecast, propagation model, and the curation rung inherited from strategy.
2. Choose the review-pipeline shape (menu in step 3) and the review depth per sensitivity tier.
3. Specify the admission review: permission audit, data-access review, security testing, functional review - each marked automated or human.
4. Set the re-review-on-update policy with objective triggers.
5. Harden the publish channel.
6. Design the appeal path.
7. Write the revocation and post-approval enforcement ladder.
8. Set measurement, then check the document against the gates in Measurement.

Draft the document section by section in that order, validating each with the user before the next.

- A wrong sensitivity tiering caught in step 2: cheap to fix.
- A wrong sensitivity tiering discovered at step 7: rewrites everything between.

## 1. Review-pipeline shape

Four shapes, ranked. Efficiency here means risk caught per reviewer hour:

- reviewer effort per submission (descending): `single hard gate > staged gate with fast-path > two-rung ladder > functional-only review`
- buyer trust signal: `single hard gate > two-rung ladder > staged gate with fast-path > functional-only review`
- efficiency: `staged gate with fast-path > two-rung ladder > functional-only review > single hard gate`

The trust and efficiency orders invert because a uniform hard bar gives every buyer the same guarantee at full reviewer cost per submission, while a fast path or a ladder means "listed" certifies less than "certified" does.

- **Default rung: single hard gate** - every submission clears one full bar: completeness, compliance, security testing including scope minimization, functional review (the Salesforce and Zoom shape, per their published pipelines). Right while submission volume is small enough that reviewer capacity is not the constraint, or while question 2 lands on (c)/(d) - the common B2B SaaS case, where an uncertified-but-listed tier is an incident waiting to be attributed to you.
- **Promote to a staged gate with an objective fast-path** once update volume makes reviewer cost the binding constraint:
  - Full review for new apps and major versions.
  - Instant or near-instant clearance for objectively minor updates.
  - Continuous automated scanning covering what the fast path skips.

  Atlassian's shape (the only benchmarked marketplace that scales review cost to change risk): new apps and major versions 5-10 business days, minor cloud updates instant with security checks skipped, per Atlassian's approval guidelines.

- **Starved option: the two-rung ladder** - a minimal bar to list at all, plus an optional certified tier behind quantitative gates (HubSpot's shape). Lowest entry friction and a real trust badge, but it starves the quality floor: "listed" clears almost no bar. Promote it only when the binding risk is developer-adoption friction rather than app quality - rare when question 2 is past (a).
- **Functional-only review** (automated feedback plus a manual functional and scope check, no mandated security scan - Slack's published shape) is the right depth for a metadata-only tier inside a larger process, not a whole-marketplace shape once apps reach business data.
- **Deleted, not demoted: the no-review registry.** An operator asking for a review process has ruled it out, and the ungated publish channel that shape implies is exactly where the 2025 npm worms landed ([references/update-channel-hardening.md](references/update-channel-hardening.md)).
- **Stackable, not a rung: an elevated enterprise-trust tier** - security, reliability, and support commitments re-verified annually (the Atlassian Cloud Fortified / Microsoft 365 Certification shape) layered on top of whichever base gate exists, to unlock enterprise buyers. Add it once the base gate is proven, never instead of one.

Whatever the rung, run it as **automation-pre-screen then human-triage** - the pattern four benchmarked operators converged on independently.

- **Ticket routing:** auto-ticket only critical and high findings. Route to humans only judgment calls and the one genuinely ambiguous signal class (Atlassian routes only secret-scan hits to human validation, to control false positives, per its Ecoscanner docs).
- **Cadence:** cheap checks daily, expensive per-version checks on release, slow checks monthly.
- **Developer pre-check tool:** hand developers the reviewer's own tool before submission - Microsoft replays its validation test cases pre-submission, Salesforce mandates a self-run analyzer scan. Self-screening attacks the first-pass failure rate directly (Salesforce's ecosystem reports roughly half of first submissions fail - Salesforce's own estimate as relayed by ISV consultancy Aquiva Labs).

This ranking is a default, not a law, and so is every menu below it. Re-rank it against questions 2, 3, and 5, and against assets the team already owns:

- An existing SAST pipeline: moves automation up a rung.
- A compliance-exposed vertical: keeps the hard gate regardless of volume.

Re-rank each later menu against the answers its own section names. Say which interview answer moved which rung.

## 2. Permission and data-access audit

The substance the admission review checks, whatever the pipeline shape:

- **Scope minimization as a named, per-scope rule:** an app requests only the scopes its functionality requires, nothing more (Atlassian's stated security requirement), operationalized per named scope.
  - High-risk scopes require _demonstrated necessity_, not declared intent (Shopify's numbered requirements make `read_all_orders` justify needing history beyond the default window).
  - Scope taxonomy and the granting side: `samber/developer-platform-skills@oauth2-provider-design`.
  - This review's job: check the app doesn't ask for more than it uses.
- **Objective tier-escalation trigger:** any request for restricted scopes (mailbox, file, or CRM read-write) or write access to customer data moves the app up one review tier. Write the trigger so a developer can self-assess it before submitting.
- **Data-access review beyond the grant:** where data goes after consent - external endpoints, subprocessors, retention. Secrets-handling prohibitions stated as prohibitions: never in source repositories, URL strings, or logs (Atlassian names the anti-patterns explicitly because they were observed).
- **Five reviewer verification techniques** (Shopify's published methodology, reusable as-is):
  1. Codebase scanning for prohibited patterns.
  2. Configuration and manifest inspection.
  3. UI/UX verification.
  4. OAuth-billing-install flow tracing.
  5. Scope-necessity assessment against declared functionality.

Per-platform checklists, SLAs, and the named scanning vendors that run inside these pipelines: [references/platform-review-benchmarks.md](references/platform-review-benchmarks.md).

## 3. Re-review-on-update policy

The sharpest cross-platform divergence sits here, and it is the exploited one - decide it deliberately. Three rungs, ranked:

- effort, reviewer plus developer friction (descending): `periodic expiry re-review > unconditional re-certification > objective minor-update fast-path`
- update-channel exposure closed: `unconditional re-certification == objective fast-path with continuous scanning > periodic expiry alone`
- efficiency: `objective fast-path > unconditional re-certification > periodic expiry`

The `==` holds because both re-inspect every risky change: one by re-checking everything cheaply, the other by scoping full review to objective risk triggers while scanning covers the rest. Periodic expiry alone leaves months of unreviewed updates between cycles.

- **Default rung: objective minor-update fast-path.** Routine version updates skip re-approval. Full re-review re-triggers only on objective criteria (Atlassian's published trigger list):
  - New OAuth scopes.
  - New external endpoints.
  - Changed data handling.
  - Payment-model change.
  - New app type.

  Objective means the developer can self-assess before submitting. Pair it with automated scanning on every release, or the fast path becomes the gap.

- **Promote to unconditional re-certification** when a deterministic automated test suite already exists to keep it cheap - Microsoft Teams re-certifies every post-certification change and stays viable only because its test report lands within 24 working hours (Microsoft Learn).
- **Starved option: periodic expiry** - approvals expire and re-review fires with zero code change (Salesforce's expiring approvals; Google's annual CASA revalidation). Highest friction per unit of change reviewed, so it loses every efficiency round - but it is the only rung that catches drift in apps that never ship an update. Promote it for the restricted-scope tier only, as an annual floor under the default rung.
- **Deleted, not demoted: two shapes the constraints rule out.**
  - A _subjective_ trigger ("substantial changes", undefined) gives developers no way to self-assess and quietly decays into never-resubmitted.
  - _Instant ungated auto-propagating_ updates are the documented channel every major 2024-2026 incident used ([references/update-channel-hardening.md](references/update-channel-hardening.md)).

  Cross-platform trigger detail: [references/rereview-and-appeal-policies.md](references/rereview-and-appeal-policies.md).

## 4. Publish-channel hardening

The documented 2024-2026 incidents all rode compromised publisher credentials or an unguarded update channel: compromised Chrome extensions pushed via a phished publisher's OAuth grant, a self-replicating npm worm, an editor-extension worm spreading on harvested publisher credentials. Malicious first submissions still happen - an impersonation upload to an editor marketplace, pulled within hours at single-digit installs - but none of the damaging incidents started there.

Sourced incident-by-incident in [references/update-channel-hardening.md](references/update-channel-hardening.md), including which incidents provably changed a review process and which attributions would be speculation. Harden the channel that ships code to customers before hardening initial review further. Five controls, ranked:

- effort (descending): `signed artifacts enforced at install > OIDC trusted publishing > propagation hold > short-lived publish tokens > phishing-resistant publisher 2FA`
- efficiency: `phishing-resistant publisher 2FA > short-lived publish tokens > propagation hold > OIDC trusted publishing > signed artifacts enforced at install`

- **Default rung: phishing-resistant (FIDO) 2FA on publisher accounts, plus short-lived scoped publish tokens** (the model npm's operator shipped after its 2025 worm: 7-day default, 90-day maximum token lifetime - GitHub's own blog). These close the credential-theft vector that actually fired.
- **Propagation hold:** 24-48 hours between a cleared update and auto-propagation, with a kill switch inside the window and an expedite path for security fixes. Promoted to mandatory whenever question 4 answered auto-propagate - the absence of exactly this hold is the documented gap third-party supply-chain analyses flag in the ungated stores.
- **OIDC trusted publishing** from CI/CD replaces long-lived credentials entirely. Promote it as publisher count grows past what token hygiene can police.
- **Starved option: signed artifacts enforced at install.** Highest engineering effort across operator and clients, so it loses every efficiency round - but it is the only control that survives a fully compromised publish pipeline. Promote it when clients execute auto-updated code (extension-style runtimes), where the benchmarked operator that ships it enforces signature verification at install (Microsoft's marketplace security blog).

Layer these. Do not rely on one. Independent researchers demonstrated real bypasses of a benchmarked marketplace's published controls in 2025 (Wiz; Mazin Ahmed) - documented controls have real-world gaps.

## 5. Appeal path

An appeal path is a deliberate design choice: six of the eight benchmarked marketplaces offer nothing beyond fix-and-resubmit ([references/rereview-and-appeal-policies.md](references/rereview-and-appeal-policies.md)). Four rungs, ranked:

- effort (descending): `dashboard-integrated appeal > defined human-reviewed appeal > escalation channel > fix-and-resubmit only`
- developer churn and regulatory exposure reduced: `dashboard-integrated appeal > defined human-reviewed appeal > escalation channel > fix-and-resubmit only`
- efficiency: `defined human-reviewed appeal > escalation channel > dashboard-integrated appeal > fix-and-resubmit only`

- **Default rung: a defined, human-reviewed appeal with a stated turnaround**, explicitly distinct from resubmission - a named process where a human who did not make the original decision reviews the case (Shopify states this guarantee in writing). Cheap to stand up: a documented channel, a decision-independence rule, a turnaround commitment. Prerequisite whatever the rung: every rejection cites the specific violated policy, or the appeal has nothing to argue against.
- **Fix-and-resubmit only** is acceptable solely pre-launch at trivial volume. If chosen, write the promotion date into the document.
- **Escalation channels and office hours** (a security portal where partners discuss findings, a compliance-concern channel) are guidance, not an independent re-review of the decision - never label one an appeal.
- **Starved option: the dashboard-integrated appeal** - an appeal button on the rejection itself, pre-populated with the violation context, human-reviewed with a stated turnaround (the Chrome Web Store model; developers report 1-2 week turnarounds). Highest build effort, so it loses the efficiency round. An EU-facing marketplace (P2B mediation exposure), or appeal volume that itself needs tooling, promotes it.

## 6. Revocation and post-approval enforcement

Post-approval security is a standing program, not a one-time gate. Write four things:

1. **A severity-tiered enforcement ladder** with an owner and a developer-notice period per rung:
   1. Finding raised.
   2. Remediation SLA by severity.
   3. Listing hidden.
   4. New installs suspended.
   5. Tokens revoked / kill switch.
   6. Delisting, with notification to affected customers.

   These rungs carry no efficiency ranking on purpose: severity and the developer's response pick the rung, not the operator's effort budget. A rule with no rung behind it is a preference, not a policy.

2. **Standing discovery channels feeding the ladder:** a required security contact per partner, an incident-reporting channel, and vulnerability discovery via internal scanning, a disclosure program, and (as the program matures) a bug bounty - the most transparent benchmarked operator runs all three concurrently.
3. **Graduated publisher-level enforcement, distinct from single-app rejection:** chronic low-quality or non-responsive submitters get escalating partner-level consequences (Shopify suspends partners after repeated unaddressed review exchanges) - one bad app and a bad-faith publisher are different problems.
4. **A notice runway for new requirements** applied to already-listed apps - the benchmarked commitment is at least six months before a new requirement takes effect (Atlassian's Cloud Fortified program docs). Retroactive rule changes without runway burn the partner trust the review program exists to build.

## Failure modes

- **Guarding the front door, leaving the back door open.** A heavy initial gate with ungated updates is the exact 2024-2026 incident pattern. Fix: steps 3-4 before deepening step 1.
- **Subjective re-review trigger.** "Substantial changes" decays into never-resubmitted because nobody can self-assess it. Fix: the objective trigger list.
- **Over-attributing incidents to review.** A third-party app breach is not automatically a review failure. Claim a causal process change only when the operator itself states one ([references/update-channel-hardening.md](references/update-channel-hardening.md) carries the working rule). Redesigning the gate after an incident the gate could never have caught spends effort on the wrong control.
- **Uniform depth held past its volume.** A single hard gate, kept after reviewer cost becomes the constraint, produces multi-week queues and developer churn - the benchmarked no-SLA marketplace draws exactly those complaints in its own forums.
- **Automation without triage design.** Scanning everything and ticketing everything drowns reviewers. Auto-ticket critical/high only, and route only genuinely ambiguous signal classes to humans.
- **An appeal that is secretly resubmission.** Labeling office hours an appeal erodes trust and, for EU-facing marketplaces, leaves the P2B exposure unaddressed.

## Measurement

Design-document gates first, self-set since no industry pass-standard exists for a review-process design. Iterate until all four pass:

1. Every review tier has an objective escalation trigger a developer can self-assess.
2. "Minor update" is defined by objective criteria - no new scopes, no new external endpoints, no data-handling change.
3. Every enforcement rung names an owner, a notice period, and the evidence that fires it.
4. The publish channel carries at least the default control rung, and the propagation hold whenever updates auto-propagate.

Operating KPIs once live:

- First-pass approval rate (the benchmarked floor to beat: roughly half of first submissions fail at the strictest gate - Salesforce's estimate via Aquiva Labs).
- Time-to-first-decision against the published SLA.
- Share of updates clearing the fast path.
- Appeal overturn rate.
- Post-approval security findings per quarter, with time-to-remediation against SLA.
- Automated-scan false-positive rate (rising false positives silently retrain reviewers to ignore the scanner).

If your harness has persistent memory, record the chosen pipeline shape, the sensitivity-tier triggers, the "minor update" definition, and each menu's rung with its promotion condition - onboarding, listing, and monetization runs should inherit these decisions instead of re-asking.

## Invocation examples

- "We're launching an app marketplace for our CRM next quarter - design the security review process for third-party apps."
- "Our app review takes six weeks and partners are furious. Where can we add a fast path without reopening the update channel?"
- "An installed app just leaked customer data through an auto-update. Rewrite our re-review and revocation policy so that can't happen again."

## References

- [references/platform-review-benchmarks.md](references/platform-review-benchmarks.md) - eight-platform comparison: pipeline shapes, SLAs, review checklists, reviewer team design, named scanning vendors.
- [references/update-channel-hardening.md](references/update-channel-hardening.md) - the 2024-2026 incidents with sourced attribution (confirmed process changes versus unattributed), and the publish-channel control set in detail.
- [references/rereview-and-appeal-policies.md](references/rereview-and-appeal-policies.md) - re-review triggers and appeal tiers across platforms, with the objective-versus-subjective trigger contrast.

See also, same collection:

- `samber/developer-platform-skills@connector-marketplace-strategy` - chooses the curation rung this process enforces. Run it first when marketplace strictness is still an open question.
- `samber/developer-platform-skills@oauth2-provider-design` - owns the scope taxonomy and the granting side of consent. This skill's permission audit checks apps against that taxonomy.
- `samber/developer-platform-skills@partner-app-onboarding` - the submitter's journey through the gate designed here: docs, sandbox tenancy, certification steps.
- `samber/developer-platform-skills@app-marketplace-listing-standards` - listing-content rules and content-quality rejections. Badge eligibility is decided here, badge display there.
- `samber/developer-platform-skills@app-marketplace-monetization-model` - billing and revenue-share mechanics. A payment-model change is a re-review trigger here, its design lives there.
- `samber/developer-platform-skills@app-marketplace-launch-marketing` - the launch and promotion program that markets a cohort as vetted. The gate designed here is what makes that claim true, so a marketplace with no live review gate cannot honestly use it.
