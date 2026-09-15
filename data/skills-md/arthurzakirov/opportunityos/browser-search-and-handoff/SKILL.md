---
name: browser-search-and-handoff
description: "Human-in-the-loop workflow for browser-based sourcing, shortlisting, and next-step preparation across marketplaces and portals. Use when Codex needs to search websites for entities that match user-defined criteria, collect results in a tracker, find each entity's follow-up action page or application form, prefill low-risk fields where appropriate, and stop for human-only steps such as CAPTCHA, OTP, legal acceptance, payment, identity verification, or final submission. Typical triggers include apartment hunting, job search, dating or partner discovery, vendor sourcing, and similar search-then-contact or search-then-apply workflows."
---

# Browser Search and Handoff

## Overview

Run a repeatable search workflow across websites where the user defines target attributes, Codex gathers matching entities, and the process ends in a controlled handoff before sensitive or anti-bot steps. Use this skill to separate what the AI can do reliably from what the human must confirm or complete manually.

## Workflow

### 1. Define the search target and intake criteria

Start by determining:

- The domain: apartment, job, partner search, vendor, or another entity type
- The action goal: shortlist, contact, apply, register, or prepare a first outreach
- The search scope: which portals or marketplaces to search first
- The requested output: local file, CSV, markdown table, or Google Sheet

If the user has not already provided criteria, stop and ask for them before opening sites. Extract:

- Hard constraints: requirements that disqualify an entity
- Soft preferences: factors that improve ranking but do not disqualify
- Exclusions: deal-breakers or categories to avoid
- Geography and distance rules
- Time constraints: move-in date, availability, start date, response deadline
- User profile fields that are safe to reuse in forms
- Stop conditions: how many matches to collect and when to stop browsing

Use [criteria-patterns.md](references/criteria-patterns.md) for domain-specific intake patterns.

### 2. Create or choose a tracking format

Default to a local CSV derived from [tracker-template.csv](assets/tracker-template.csv) unless the user explicitly asks for a different storage target. Prefer a local file first because it is easy to inspect, diff, and resume.

Use Google Sheets only when the user asks for it or when collaborative editing matters.

Track both discovery and follow-up state in the same record. Each row should represent one candidate entity plus its next-action page.

Use [tracker-fields.md](references/tracker-fields.md) for the default schema.

### 3. Search portals and collect candidate entities

For live browser work, prefer the `agent-browser` skill and its CLI workflows over ad hoc browsing instructions.

While searching:

- Capture the listing URL, source portal, and key evidence that the entity matches the criteria
- Normalize important attributes into the tracker instead of relying on prose notes
- Record uncertainty explicitly when a page does not state a value
- De-duplicate across portals and repeated listings
- Stop after the requested quota or when results clearly stop matching the user's thresholds

Do not over-filter too early. Keep borderline matches if the user may want to review them later.

### 4. Score fit and explain why a result is included

For every promising entity, store:

- Which hard constraints are satisfied
- Which preferences are satisfied
- What is missing or uncertain
- A concise summary explaining why the result is worth the user's time

Prefer transparent reasoning over opaque scoring. A simple `high`, `medium`, `low` fit label is usually enough if paired with evidence.

### 5. Find the next-action page for each promising entity

After finding a matching listing, locate the page where the real action happens:

- Application form
- Contact form
- Off-platform company or landlord website
- Registration flow
- Profile page that must be completed before outreach

Store both the discovery URL and the action URL. They are often different and both matter for resuming work later.

Also capture blockers:

- Account required
- Email verification required
- Phone verification required
- CV or attachment required
- Student-only or region-only restriction
- Paywall or premium feature

### 6. Respect the automation boundary

Treat this skill as human-in-the-loop by default.

AI-safe tasks usually include:

- Filling known, low-risk fields the user has already provided
- Drafting cover letters, short bios, or first-message variants for approval
- Selecting dropdown values that directly map to user-provided data
- Saving progress up to the point where a human checkpoint appears

Human-only tasks usually include:

- CAPTCHA or anti-bot checks
- OTP, 2FA, email-code, or phone-code steps
- Legal acceptance, consent, waivers, or attestations
- Payments
- Identity verification
- Final submit when the action has real-world consequences

Handle credentials conservatively:

- Prefer the user to enter passwords directly
- If the user explicitly asks for a generated password, propose one but do not silently reuse or submit it without confirmation
- Do not invent profile facts to get through forms

### 7. Prepare the handoff cleanly

When automation must pause, return a compact handoff package:

- The shortlist, sorted by fit
- The current status of each item
- The action URL that needs human attention
- The exact blocker or checkpoint
- The next 1 action the human should take

If the user wants to resume later, continue from the tracker rather than rediscovering the same listings.

## Domain Notes

Use [criteria-patterns.md](references/criteria-patterns.md) to adapt the intake and scoring model to apartments, jobs, partner search, or another domain.

Use [tracker-fields.md](references/tracker-fields.md) to decide which columns must be populated before handing off a shortlist.

For job applications, this skill owns discovery, scoring, shortlist tracking, and action URL collection. Once the user selects a specific job/application URL to execute, switch to `job-application-operator` for schema-driven field inventory, private-profile loading, document upload, logging, and submit-or-stop decisions.

## Failure Modes

Expect these problems and account for them explicitly:

- The user gives goals but not measurable criteria
- Portal filters are weaker than the user's actual requirements
- A listing page hides critical attributes behind expansion panels or galleries
- The action page lives on a different domain
- The portal requires login before exposing the action path
- Anti-bot systems block fully automated submission
- The user asks for actions that should remain under explicit human control

When blocked, document the blocker in the tracker and move to the next candidate instead of losing momentum.

## Output Conventions

Prefer concise, structured outputs over long prose dumps.

For each result, capture at minimum:

- Entity name or title
- Listing URL
- Action URL
- Fit summary
- Blockers
- Recommended next step

Use the tracker as the source of truth. Summaries should be derived from it, not the other way around.
