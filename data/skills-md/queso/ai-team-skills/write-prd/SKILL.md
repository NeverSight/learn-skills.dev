---
name: write-prd
description: Creates a new Product Requirements Document (PRD) with auto-numbered filenames in the project's PRD directory. Gathers business context, defines the problem, and produces a structured PRD.
---

# Write PRD

Create a new Product Requirements Document in the project's PRD directory.

## Step 1: Find the PRD Directory and Next Number

Look for an existing PRD directory in the project. Common locations: `docs/prds/`, `prds/`, `docs/prd/`, `prd/`. If none exists, ask the user where PRDs should live.

List existing PRD files and determine the next sequence number. Files follow the pattern `NNNN-slug.md` (e.g., `0019-user-onboarding.md`). The next file would be `0020-<slug>.md`. If no PRDs exist yet, start at `0001`.

## Step 2: Gather Context

Before writing, you need to understand:

1. **What feature or change is this for?** — Get a short description from the user if not already provided.
2. **Business context** — Why does this matter? What problem does it solve? Who asked for it? If the user hasn't provided this, ask directly: *"What's the business reason for this? What problem are we solving and for whom?"*
3. **Success criteria** — How will we know this worked? Ask if not obvious: *"How should we measure success? What changes for the user?"*

Do not proceed without a clear business justification. A PRD without business context is just a feature spec.

## Step 3: Generate the Filename

Combine the next sequence number with 2-4 kebab-case keywords from the feature description:

- `0020-fix-social-sharing.md`
- `0021-add-team-billing.md`
- `0022-migrate-auth-to-oauth2.md`

Confirm the filename with the user before writing.

## Step 4: Write the PRD

Use the template structure from the references. The PRD should be:

- **Problem-first** — Lead with why, not what
- **Measurable** — Every goal has a success metric
- **Scoped** — Explicit about what's in and what's out
- **User-centered** — Written from the user's perspective, not the developer's
- **Implementation-free** — Describe what, not how (no architecture, no code)

Consult `references/prd-best-practices.md` for good and bad examples.
Consult `references/prd-template.md` for the document structure.

## Step 5: Review and Refine

After writing the first draft, review it against the quality checklist in the references:

- Does every requirement have a clear "why"?
- Are success metrics specific and measurable?
- Is scope clearly bounded (in/out)?
- Are edge cases and error states considered?
- Are dependencies and risks called out?

Present the draft to the user for feedback before finalizing.
