---
name: gherkin
description: Create and manage Gherkin feature specifications (.feature files) following the Cucumber BDD standard. Use this skill whenever the user mentions "gherkin", "feature file", "BDD scenarios", "behavior specs", "acceptance criteria", or asks to write test scenarios in Given/When/Then format. Works for any project in any language — from a brand-new repo to a mature codebase. Even if no .feature files exist yet, this skill helps scaffold the first ones. Also use when the user wants to review, organize, or expand existing Gherkin specifications.
---

# Gherkin Scenario Creator

Write Gherkin specifications that capture business behavior clearly and completely. This skill walks users through the process interactively — understanding what they want to specify, thinking through the scenarios they might not have considered, checking for conflicts with existing specs, and producing well-structured `.feature` files.

## How It Works

When a user asks to create Gherkins for a feature, follow this sequence:

### 1. Understand the Feature

Start by understanding what the user wants to specify. They might say something broad like "create gherkins for the login flow" or something specific like "add a scenario for password reset."

**For broad requests, ask before you propose.** You'll be tempted to immediately list every scenario you can think of — resist that urge. The user has context you don't: who the actors are, what edge cases matter in their domain, what's already handled elsewhere. Ask 2-3 targeted questions first to shape your thinking. Good questions:

- **Actors:** "Who uses this feature? Just regular users, or admins too?" Different actors often mean different scenario sets.
- **State:** "What's the starting state? Are there cases where the user is already partially through this flow?"
- **Error handling philosophy:** "When something goes wrong (like invalid input), should the system show specific errors or generic messages?"
- **Scope boundaries:** "Does this include [related capability], or is that a separate feature?"

Pick the 2-3 most useful questions for this particular feature. Don't ask about things you can reasonably infer. After the user answers, *then* propose your scenario checklist.

**Present your suggested scenarios as a checklist** and ask which ones they want to include. Add any they suggest that you missed. This collaborative expansion is the core value of the skill — users often think of the happy path and a couple of error cases, but a thorough spec covers edge cases too.

**For specific requests**, confirm the scope and still consider whether there are closely related scenarios worth including. Mention them briefly — don't force them, just surface them.

### 2. Scan for Existing Gherkins

Before writing anything, check what already exists in the project.

**Search for existing `.feature` files:**
```
Glob: **/*.feature
```

**Search for Gherkin-style content in other files** (some projects keep specs in markdown or docs):
```
Grep: "Feature:|Scenario:|Given |When |Then " across the project
```

If existing Gherkin files are found:
- Read them to understand the project's style and conventions (indentation, tag usage, naming patterns, level of detail)
- Check whether any existing scenarios already cover the behavior the user is asking for
- **Match the project's existing style** — if they use `Scenario` instead of `Example`, two-space indentation, specific tag conventions, or particular step phrasing patterns, follow those conventions

If a **conflict** is detected (an existing scenario covers the same behavior, even if worded differently), flag it clearly:

> **Heads up:** I found an existing scenario in `features/catalogue/pricing.feature` that already covers this behavior:
>
> ```gherkin
> Scenario: Discount cannot be applied to already-reduced items
>   Given a product marked as "On Sale"
>   When a staff member applies a loyalty discount to it
>   Then they should see "Promotional discounts cannot be combined"
> ```
>
> Your new scenario achieves the same thing. Want to skip it, replace the existing one, or keep both?

Conflict detection is about **behavioral equivalence**, not identical wording. Two scenarios that test "wrong password shows error" are duplicates even if the steps are phrased differently.

For file placement and naming conventions, read `references/organization.md`.

### 3. Write the Scenarios

When writing Gherkin, apply these reference files:

- **Syntax and keywords:** `references/gherkin-syntax.md` — structure, keyword definitions, step arguments, Scenario Outline syntax, and the `# language: xx` header for non-English scenarios
- **Writing quality:** `references/best-practices.md` — one behavior per scenario, step count, naming, Background, Outline, Rules, and tag guidance
- **Review pass:** `references/anti-patterns.md` — before presenting to the user, scan for technical language in steps, dependent scenarios, vague step names, and mixed Given/When intent

### 4. Present and Confirm

Show the complete `.feature` file to the user before writing it. Walk through any design decisions you made:
- Why you grouped scenarios the way you did
- Where you used Scenario Outlines vs individual scenarios
- Any edge cases you included and why

Ask the user to review and suggest changes before finalizing.

### 5. Write or Append

**If an existing `.feature` file covers this feature area**, append the new scenarios to it. Place them logically — under the appropriate `Rule` block if one exists, or at the end of the file.

**If no existing file covers this area**, create a new `.feature` file.

For directory layouts, naming conventions, when to create vs. append, and how to set up structure for brand-new projects, read `references/organization.md`.

### 6. Glossary Check

After writing the `.feature` file, check if the project has a glossary (`glossary/glossary.config.yml`). If it does:

1. Read the relevant glossary context files (based on scope) plus `core.glossary.yml`
2. Scan the new scenarios for domain terms — nouns in Given/When/Then steps that look like business concepts (e.g., "Cart", "Order", "Wishlist", "Coupon")
3. Compare against existing glossary terms (checking `name`, `aliases`, `code_name`, and `ui_label`)
4. If you find terms that aren't in the glossary, mention them at the end of your summary:

> I noticed these terms in the new scenarios that aren't in your glossary yet:
> - **Wishlist** — used in 3 scenarios
> - **Gift Card** — used in 1 scenario
>
> Want to add definitions for any of these?

If the user says yes, hand off to the glossary skill (or walk through the add flow if the glossary skill isn't available).

If the project has no glossary, skip this step silently — don't suggest creating one here.

### 7. Summary

After writing, provide a brief summary:
- How many scenarios were added
- Which file was created or updated
- Any conflicts that were flagged and how they were resolved
- Any new terms suggested for the glossary (if applicable)
- Suggested next scenarios to consider (if the feature has more depth to explore)

## Example

User says: "Create gherkins for the password reset flow"

**Step 1 — Ask first:**

> Before I draft the scenarios, a couple of quick questions:
>
> 1. **Who can reset?** Only registered users, or can admins trigger a reset on behalf of someone?
> 2. **Security posture:** If someone requests a reset for an email that doesn't exist, should we show a generic "check your email" message (more secure) or tell them the account wasn't found (more helpful)?

**Step 1 — After user answers, propose the checklist:**

> Based on your answers, here's what I'd cover:
>
> - [x] User requests a password reset (happy path)
> - [x] User clicks the reset link and sets a new password
> - [x] Reset link has expired
> - [x] Reset link has already been used
> - [x] User enters mismatched passwords
> - [x] New password doesn't meet requirements
> - [x] User requests reset for non-existent email (generic message, per your security preference)
>
> Which of these do you want to include? Any others I'm missing?

**Step 3 — After confirmation, write the scenarios:**

```gherkin
Feature: Password Reset
  Users who forget their password can request a reset link via email
  and use it to set a new password.

  Rule: Requesting a reset

    Scenario: User requests a password reset for a registered email
      Given a registered user with email "morgan@example.com"
      When they request a password reset
      Then they should receive a reset email at "morgan@example.com"
      And they should see "Check your email for reset instructions"

  Rule: Using the reset link

    Scenario: User resets password with a valid link
      Given a valid password reset link for "morgan@example.com"
      When they set a new password "NewSecure123!"
      Then their password should be updated
      And they should be redirected to the login page

    Scenario: User attempts to use an expired reset link
      Given a password reset link that expired 2 hours ago
      When they attempt to set a new password
      Then they should see "This reset link has expired"
      And they should be prompted to request a new one

    Scenario: User attempts to reuse a reset link
      Given a password reset link that has already been used
      When they attempt to set a new password
      Then they should see "This reset link has already been used"

  Rule: Password requirements

    Scenario: User enters mismatched passwords
      Given a valid password reset link
      When they enter "Password1" and confirm with "Password2"
      Then they should see "Passwords do not match"

    Scenario Outline: New password does not meet requirements
      Given a valid password reset link
      When they set a new password "<password>"
      Then they should see "<error>"

      Examples:
        | password | error                                      |
        | short    | Password must be at least 8 characters     |
        | nodigits | Password must contain at least one number  |
```
