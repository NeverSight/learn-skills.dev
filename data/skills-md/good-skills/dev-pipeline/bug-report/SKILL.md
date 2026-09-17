---
name: bug-report
description: >-
  Transforms unstructured natural-language problem descriptions into concise,
  evidence-aware bug reports. Use when the user starts with /bug-report or asks
  to turn rough notes, symptoms, errors, or reproduction details into a bug
  report.
disable-model-invocation: true
version: 1.1.0
---

# Bug Report

When the user starts with `/bug-report`, attaches this skill, or explicitly asks
to convert natural input into a bug report, generate the report and stop.

**Purpose:** Turn incomplete, conversational problem descriptions into useful
bug reports without inventing facts or mistaking user claims for verified
repository evidence.

**Token policy:** Apply [../shared/caveman-token-policy.md](../shared/caveman-token-policy.md)
to internal extraction and repository localization. The final bug report is a
persisted human-facing artifact and must use clear normal prose.

## Activation

| Form | Behavior |
|------|----------|
| `/bug-report <text>` | Generate a compact Markdown bug report |
| `/bug-report --minimal <text>` | Generate the minimal template |
| `/bug-report --full <text>` | Generate the detailed template |
| `/bug-report --save [path] <text>` | Generate and save the report |
| `/bug-report --help` / `-h` | Display help message with usage, templates, evidence rubrics, and options |
| Natural language: “make this a bug report” | Generate a compact report |

If `--minimal` and `--full` are both present, ask which format to use. Saving
creates a report artifact; it does not submit an issue or modify product code.

## Evidence contract

Classify information before rendering:

- **Reported:** stated by the user but not independently verified.
- **Observed:** directly supported by attached output, repository content, or
  diagnostics inspected during this request.
- **Inferred:** a reasonable interpretation that is explicitly labeled.
- **Unknown:** missing information that must remain a placeholder or question.

Never upgrade Reported, Inferred, or Unknown information to Observed. Quote
exact error messages when available. Redact credentials, tokens, personal data,
and other secrets as `<REDACTED>`.

## Workflow

1. **Parse** — remove command flags and preserve the user's original meaning.
2. **Extract** — identify the symptom, affected area, sequence of events,
   expected result, actual result, frequency, impact, environment, evidence,
   and workaround.
3. **Inspect selectively** — if repository context is available and a narrow
   lookup can confirm names, versions, or relevant paths, inspect only those
   sources. For broad localization, use the compact read-only explorer contract
   from the token policy when available. Do not perform broad diagnosis unless
   requested.
4. **Separate evidence** — label Reported, Observed, Inferred, and Unknown
   claims; never invent reproduction steps or environment values.
5. **Assess severity** — use the rubric below. If evidence is insufficient,
   write `Needs triage` instead of guessing.
6. **Render** — use the requested template in clear professional prose. Omit
   empty optional sections in compact output; retain explicit unknowns that
   affect reproducibility. Do not apply Caveman fragments to the final report.
7. **Save if requested** — write UTF-8 Markdown to the supplied path, or
   `bug-reports/{slug}-{YYYYMMDD-HHMMSS}.md` when no path is supplied. Ask
   before overwriting an existing file unless overwrite was explicit.
8. **Stop** — do not fix the bug, create an external issue, commit, or push
   unless the user separately requests that action.

## Clarification

Generate a useful report from partial input whenever possible. Ask one focused
question only when:

- the described expected and actual behavior are indistinguishable;
- contradictory statements materially change the report;
- saving would overwrite a file; or
- the target output format is ambiguous because flags conflict.

Otherwise, record missing details under **Unknowns / questions**. Do not force
the user through a questionnaire before producing a draft.

## Severity rubric

| Severity | Use when evidence indicates |
|----------|-----------------------------|
| Critical | Security exposure, data loss, or a system-wide outage |
| High | Core workflow blocked with no practical workaround |
| Medium | Important behavior degraded; workaround exists |
| Low | Minor defect with limited functional impact |
| Needs triage | Impact or scope is not established |

Treat severity as **Inferred** unless the user explicitly assigns it or
repository evidence confirms the impact.

## Output formats

### Minimal

```markdown
# [Concise symptom-based title]

## Summary
[What happened, where, and impact. Mark claims as Reported when unverified.]

## Reproduction
1. [Known step]
2. [Known step]

**Expected:** [Expected behavior or Unknown]
**Actual:** [Actual behavior]

## Context
- Severity: [value and evidence status]
- Environment: [known values or Unknown]
- Evidence: [errors, logs, screenshots, or relevant paths]
- Unknowns / questions: [only material missing details]
```

### Compact (default)

```markdown
# [Concise symptom-based title]

## Summary
[Problem, affected area, frequency, and user impact.]

## Steps to reproduce
1. [Prerequisite or starting state]
2. [Action]
3. [Observed result]

## Expected behavior
[Expected result.]

## Actual behavior
[Actual result, including exact error text.]

## Environment
- Version/commit: [value or Unknown]
- Platform/runtime: [value or Unknown]
- Configuration: [relevant non-secret values or Unknown]

## Evidence
- [Reported/Observed] [log, screenshot, stack trace, path, or recording]

## Triage
- Severity: [Critical/High/Medium/Low/Needs triage]
- Frequency: [always/intermittent/once/Unknown]
- Workaround: [value/none known/Unknown]
- Suspected area: [Inferred value, only when useful]

## Unknowns / questions
- [Missing detail that materially helps reproduce or prioritize]
```

### Full

Use the compact template plus:

- **Preconditions**
- **Regression status** and last known working version
- **Scope**: affected and unaffected users, workflows, or components
- **Timeline**
- **Diagnostics attempted**
- **Attachments**
- **Related issues or changes**
- **Acceptance signal**: the observable condition that demonstrates resolution

Use `Unknown` for unavailable required details. Do not add `N/A` sections merely
to make the report look complete.

## Quality rules

- Prefer a symptom-and-context title, not “Bug” or the user's entire message.
- Preserve exact identifiers, versions, commands, and error text.
- Deduplicate internal notes before rendering; state each report fact once.
- Write reproduction steps only from provided or observed facts.
- Keep diagnosis separate from the report unless the user asks for diagnosis.
- Distinguish a suspected cause from a confirmed root cause.
- Avoid duplicate statements across Summary, Actual behavior, and Evidence.
- Keep compact reports short enough to scan while retaining actionable detail.

## Out of scope

- Submitting reports to GitHub, Jira, Linear, or another external system
- Implementing or validating a fix
- Broad repository investigation or root-cause analysis
- Fabricating missing reproduction, environment, impact, or severity details

## Definition of done

The report has an actionable title; expected and actual behavior are distinct;
known reproduction and environment details are preserved; evidence status is
honest; material unknowns are visible; sensitive data is redacted; and no
external side effect occurred unless separately authorized.

## Version

When `--version` or `-v` is detected as the only meaningful flag, emit the skill version (from the frontmatter) verbatim and stop. Do not inspect, reason, or generate.

