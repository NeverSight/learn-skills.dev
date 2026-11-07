---
name: utm-campaign-plan
description: Use when a campaign needs a consistent, approved way to label links so the team can distinguish sources and make later reporting possible. Trigger phrases include "plan our UTMs", "name campaign links", "make tracking links", "how should we tag creator links?", and "set up attribution for this launch". Do not use this to claim analytics access, create tracking without consent or policy review, or decide campaign strategy; use campaign-brief for the campaign source, paid-social-brief for media requirements, and social-analytics-report to interpret available data.
---

# UTM Campaign Plan

Create a small, consistent link taxonomy that answers real reporting questions without turning every URL into ungoverned tracking noise.

## 1. Start with the reporting question

Ask what decision the data should support, which destinations are approved, which channels and partners are involved, what analytics system consumes the links, and what naming convention already exists. If no reporting owner or system is known, document that limitation before issuing links.

## 2. Define the controlled vocabulary

Set clear allowed values for source, medium, campaign, content, and term only when each has a decision use. Use human-readable, stable naming. Separate owned social, paid social, creators, partners, and experiments so later reporting does not blend unlike traffic.

## 3. Issue a link register

For every link, provide the destination, intended placement, UTM values, owner, start and end context, and approval status. Include examples and invalid examples. Reserve a process for changes so a creator or operator does not silently alter the taxonomy.

## 4. Validate before use and review after

Check that URLs resolve to the approved destination, parameters are encoded correctly, and the same source is not represented by several names. After the campaign, compare link usage against the register and record any taxonomy correction for the next brief.

## Hard rules

- Do not create tracking links for unapproved destinations or campaigns.
- Never put personal data, sensitive information, customer names, or private identifiers in UTM values.
- Do not treat UTM tags as proof of conversion or causation.
- Preserve existing analytics conventions unless an authorised owner approves a change.
- Keep affiliate, paid, organic, creator, and partner traffic distinguishable.

## Failure modes

| Failure | Do this instead |
| --- | --- |
| Every team member invents names | Publish one controlled vocabulary and a shared register. |
| Parameters contain personal or sensitive data | Use a non-identifying campaign label and keep sensitive data out of URLs. |
| A short link hides an unverified destination | Validate the final redirect and approved landing page before sharing. |
| Reports blend creator and paid traffic | Assign separate medium/source values and preserve them in the register. |

## Where it sits

Use campaign-brief to establish the campaign and paid-social-brief or influencer-partnerships to identify placements. Use this skill before cross-platform-distribution goes live. Use social-analytics-report and launch-retrospective to interpret the resulting labelled traffic honestly.
