---
name: feature-writing
description: >-
  Review and write feature announcements using a 4-part framework
  (Context, Solution, Usage, Resources). Use when writing or reviewing
  blog posts, release notes, changelogs, customer emails, internal comms,
  product updates, or feature marketing content. Covers problem-led
  messaging, benefit-focused language, audience tone matching, and
  scannable structure. Triggers on any task involving feature descriptions,
  product announcements, or upgrade communications.
---

# Feature Writing

Review and write feature announcements using the 4-part framework: Context, Solution, Usage, Resources.

## Workflow

Determine whether the task is a **review** of existing text or **creation** of new text, then follow the appropriate workflow.

### Review workflow

1. Read the target file(s)
2. Load `references/feature-writing-guide.md`
3. Check the text against the 4-part framework:
   - Does it establish context and articulate the problem?
   - Does it describe the solution clearly?
   - Does it explain how to use the feature?
   - Does it link to supporting resources?
4. Check the text against the writing rules:
   - Leads with pain, not features
   - Uses specific and concrete language
   - Avoids unexplained acronyms
   - Uses active voice
   - Focuses on benefits, not capabilities
   - Uses scannable formatting
   - Matches tone to the target audience
5. Report each finding in this format:
   ```
   file:line — "original text" — [Rule N.N name] — Suggested: "improved text"
   ```
6. Summarize findings grouped by framework gaps and rule violations

### Creation workflow

1. Identify the output type (blog post, release note, changelog, customer email, internal communication)
2. Load `references/feature-writing-guide.md`
3. Collect the following from the user (ask if missing):
   - What problem does this feature solve?
   - What was shipped?
   - How does a user start using it?
   - What resources should be linked?
4. Draft using the 4-part framework:
   - **Context**: State the problem and why it matters
   - **Solution**: Describe what was built to solve it
   - **Usage**: Explain how to get started
   - **Resources**: Link to docs, related posts, and references
5. Adapt tone and structure to the output type (see Section 3 of the full guide)
6. Self-check the draft against all writing rules
7. Present the draft with a brief rationale citing the rules applied

## Quick reference

Key rules to check first:

| Rule | Summary |
|------|---------|
| Lead with pain | Open with the problem, not the feature name |
| Be specific | Use concrete numbers, steps, and scenarios |
| No unexplained acronyms | Spell out on first use or avoid entirely |
| Active voice | "You can now deploy" not "Deployment can be done" |
| Benefits over capabilities | "Save 2 hours per release" not "Supports automation" |
| Scannable structure | Use headings, bullets, and short paragraphs |
| Match tone to audience | Technical for devs, outcome-focused for executives |
| 4-part completeness | Every piece must cover Context, Solution, Usage, Resources |
| Link to resources | Always point readers to docs and related materials |

## Full guide

For the complete framework details, writing rules with Do/Don't examples, and output type templates, load `references/feature-writing-guide.md`.
