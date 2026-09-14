---
name: job-application-operator
description: Run schema-driven, remote-backed, human-configurable job application workflows with field inventory, safe autofill, document upload, learning, logging, and optional autonomous submission when policy allows.
---

# Job Application Operator

## Purpose

Use this skill when applying to jobs, inspecting application forms, filling application fields, uploading documents, saving learned answers, or logging application outcomes.

This skill is for the application execution stage: one selected job/application URL, private profile policy, documents, logging, and submit-or-stop decisions. Use discovery, tracking, or database skills before this stage to select exactly one application URL.

This skill is generic. It must not contain personal values. Personal values are loaded from private files prepared by `private-context-bootstrap`.

## Data Sources

Load private data from these paths unless environment variables override them:

```bash
AGENTDESK_PROFILE_PATH="$HOME/.config/AgentDesk/private/job-applications/application-profile.yaml"
AGENTDESK_DOCUMENT_MANIFEST_PATH="$HOME/.config/AgentDesk/private/job-applications/document-manifest.yaml"
AGENTDESK_FIELD_POLICY_PATH="$HOME/.config/AgentDesk/private/job-applications/field-answer-policy.yaml"
AGENTDESK_APPLICATION_LOG_PATH="$HOME/.config/AgentDesk/private/job-applications/application-log.jsonl"
```

Before running an application workflow, verify that these files exist and validate them. If they do not exist, invoke the `private-context-bootstrap` workflow.

Reference schemas and fake examples live in `references/`. Load them when creating or validating private files.

## Separation Of Concerns

The skill contains process rules, safety rules, field classification rules, loading rules, logging rules, and submission rules.

The shared personal profile contains identity, contact details, address, employment, housing, and generic form facts using the `bitwarden-personal-profile` schema. Domain files contain only job-specific extensions: citizenship/work authorization policy, salary policy, location preferences, work-mode preferences, document paths, reusable job answers, default field policies, and submission mode preferences.

## Browser Backends

Use available browser automation in this order:

1. Native Codex browser/computer-control if available.
2. `agent-browser` CLI.
3. Playwright MCP.
4. Browser harness fallback.

Never use CAPTCHA-solving services, stealth browser patches, proxy rotation, fake identities, account evasion, or automated bypass of MFA/login walls.

## Application Modes

The private field policy may define:

- `inventory_only`: inspect fields and log required actions. Do not fill or submit.
- `assisted_review`: fill safe known fields. Stop before submit and ask the user.
- `auto_submit_when_fully_answerable`: submit only when every condition below passes.
- `never_submit`: never submit, even if all fields are known.

Default to assisted review unless private policy enables autonomous submission.

Autonomous submission is allowed only when `submission.defaultMode` is `auto_submit_when_fully_answerable` and all required fields, documents, filters, and blocker checks pass.

Standard known fields may be filled and submitted without asking when the private field policy explicitly sets `autoFill: true` and `autoSubmitAllowed: true`.

## Auto-Submit Requirements

The agent may submit only if all conditions are true:

- the role passes user-defined filters
- all required fields are answered by validated policy
- all required uploads are available
- no CAPTCHA, MFA, login, or account-creation blocker appears
- no unknown required custom question appears
- no legal, export-control, nationality, or eligibility edge case appears
- no field conflicts with the user's private policy
- the current site does not prohibit the intended automation mode according to available instructions or terms surfaced during the flow

## Hard Stops

Always stop and ask the user if any of these occur:

- CAPTCHA
- MFA
- login required and no active session exists
- account creation required
- payment or billing
- unclear legal question
- export-control or defense nationality restriction
- request to certify something not represented in private policy
- unknown required question
- missing required document
- upload failure
- page error
- field ambiguity that changes legal, compensation, or eligibility meaning
- browser automation would need stealth, proxy, CAPTCHA solving, or terms evasion
- policy conflict

If a required company-specific motivation or cover-letter question appears and no approved reusable answer exists, do not invent one. Mark the application as manual or deprioritized.

## Field Handling Policy

Classify every field as one of:

- `safe_known`: can be filled from profile without asking if policy permits.
- `sensitive_known`: can be filled if explicit policy exists, but must be logged carefully.
- `strategic_known`: can be filled if policy exists.
- `unknown_required`: required and not answerable from policy; stop.
- `unknown_optional`: optional and not answerable from policy; skip unless policy says otherwise.
- `custom_question`: company-specific or long-form question.
- `voluntary_disclosure`: demographic or optional disclosure.
- `document_upload`: upload field; use the manifest.
- `legal_edge_case`: unclear or out-of-scope legal meaning; stop.
- `blocker`: prevents completion.

Examples of `safe_known`: name, email, phone, address, generic employment facts, and other fields present in the shared personal profile if policy permits.

Examples of `sensitive_known`: gender, disability, veteran/military status, nationality, citizenship, and demographic survey answers.

Examples of `strategic_known`: salary expectation, relocation willingness, work mode preference, travel willingness, start date, notice period, work authorization, and visa sponsorship.

Use reusable answers only if the private policy explicitly maps the question or permits generic answers.

## Company-Specific Motivation

Company-specific motivation fields are often low-ROI.

If a required field asks for a tailored answer such as "Why this company?" and no reusable approved answer exists:

- classify as `custom_question`
- mark application as `manual_or_deprioritized`
- do not spend long drafting unless user policy says this company is exceptional
- if optional, leave blank unless policy says to fill

## Policy-Specific Decisions

Do not decide salary, location, relocation, work authorization, visa, notice period, or start date inside the skill. Load the private policy.

If a salary field asks for a different compensation type than the policy defines, stop. Different compensation types include gross annual base, total compensation, hourly rate, monthly salary, salary range, equity expectation, OTE, and commission.

For work authorization and visa questions, answer only for countries explicitly covered by private policy. Do not infer unsupported countries.

If exact contractual notice period is unknown, do not invent one. Use the policy's conservative answer if available. If a form requires an exact date and policy cannot compute it, stop.

## Document Upload Policy

Use the document manifest. Never hardcode document filenames or paths.

For each upload field:

1. Read label and accepted file types.
2. Match label against manifest rules.
3. Upload only the matching document.
4. Stop if no confident match exists.
5. Stop if the requested file is missing.
6. Do not upload extra documents by default.

Supported document roles: `resume`, `degree`, `transcript`, `references`, `supportingBundle`, `coverLetter`, `portfolioPdf`, and `other`.

## Field Inventory Output

For every application, write a field inventory:

```yaml
applicationUrl:
platform:
roleTitle:
company:
fieldInventory:
  - label:
    type:
    required:
    options:
    currentValue:
    fieldClass:
    matchedProfileKey:
    action:
    confidence:
documentsRequested:
blockers:
submissionMode:
finalStatus:
```

## Learning New Answers

If the user provides a new reusable answer, ask whether it should be saved.

Save it to the private field policy, not to the skill. Include canonical key, aliases, answer, field type, sensitivity, allowed contexts, auto-fill permission, submission permission, and date learned.

Never save passwords or one-time codes.

## Logging

Append one JSON object per application to the application log:

```json
{
  "timestamp": "",
  "applicationUrl": "",
  "company": "",
  "roleTitle": "",
  "platform": "",
  "mode": "",
  "status": "",
  "fieldsFilled": [],
  "fieldsSkipped": [],
  "unknownRequiredFields": [],
  "customQuestions": [],
  "documentsUploaded": [],
  "blockers": [],
  "submitted": false,
  "notes": ""
}
```

Do not log full sensitive answers unless private policy explicitly allows it.

## Application Workflow

1. Ensure private context is bootstrapped.
2. Load profile, document manifest, and field policy.
3. Validate all files.
4. Open one job application URL.
5. Identify platform.
6. Inventory fields.
7. Classify fields.
8. Check job against location, work-mode, role, and country filters.
9. Fill all fields permitted by policy.
10. Upload matching documents.
11. Skip unknown optional fields.
12. Stop or deprioritize on unknown required fields.
13. If mode is assisted review, stop before submit.
14. If mode is auto-submit and every required condition is satisfied, submit.
15. Log outcome.
16. Save new reusable field mappings if approved.

## Output

Return application URL, platform, company and role if known, mode used, fields filled, fields skipped, unknown required fields, custom questions, documents uploaded, blockers, submitted yes/no, log path, and next action.
