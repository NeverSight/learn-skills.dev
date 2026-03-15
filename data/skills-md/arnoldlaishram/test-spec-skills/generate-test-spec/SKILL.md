---
name: generate-test-spec
description: Generate test specifications for native mobile apps and mobile web apps as local markdown files under a .test folder.
---

# Test Spec Generation

Generate user-focused test specifications for native mobile apps and mobile web apps, and save them as markdown files under a `.test/` folder in the project root.

## Core Principles

**Test user-facing functionality only:**
- ✅ User interactions, gestures, and navigation (tap, swipe, scroll, back navigation)
- ✅ End-to-end screen and feature functionality
- ✅ Form input, validation, search, filters, and interactive UI elements
- ✅ Mobile-specific behaviors (keyboard input, screen transitions, orientation changes)
- ✅ If sign-in is required for a flow, include login as a precondition and verify the in-app outcome after authentication
- ✅ App relaunch is allowed only when the scenario explicitly requires it; specs must explain why relaunch is needed and what must be re-validated after relaunch
- ❌ APIs, backend endpoints, or server-side logic
- ❌ Validating third-party authentication provider internals (OAuth, Google, Facebook, GitHub)
- ❌ App internals, logs, background services, or implementation details
- ❌ Non-existent screens or functionality not accessible to users

**Quality over quantity:**
- Maximum 5 tests per feature (adjust to actual complexity)
- Understand the user flow thoroughly before generating tests
- Check for existing `.test/*.md` files to avoid duplicate coverage
- Focus on critical workflows users actually need

## User Input & Credentials

Test specs often reference user-specific data such as login credentials, form values, or environment-specific details. Follow these rules:

1. **Never guess or fabricate** credentials, emails, passwords, or account-specific values when writing specs.
2. **Ask the user** if any required test input is unknown.
3. **Ask during Step 2 (Auth & Preconditions Intake)**.
4. **Use the exact values provided** by the user in test specs.

## Workflow Steps

### Step 1 — Analyze the Feature
Read relevant source files to understand the user-facing functionality and UI elements.

### Step 2 — Auth & Preconditions Intake (Required)
Collect setup requirements, credentials, and account state from the user.

### Step 3 — Plan & Review
Present the planned tests (Name and Summary) to the user and finalize the plan before writing any files. **You must briefly justify the idempotency strategy for each test in your plan.**

### Step 4 — Write Test Spec Files
Create markdown files in `.test/` using the template below. Use `snake_case` filenames.

## Setup & Idempotent Cleanup Rule

> [!IMPORTANT]
> **EVERY Setup & Cleanup Flow MUST BE IDEMPOTENT.** 
> Before writing any setup steps, you must ensure the test can run successfully **regardless of the prior state of the app**. If a previous run changed data (added an item, enabled a setting), this setup flow MUST clean that up first.

**Cleanup is NOT redundant.** Even if the cleanup steps involve navigating to the same screens as the test flow, you **MUST** include them.

| If the test validates... | The Setup & Cleanup Flow MUST... |
|---|---|
| **Adding** an item | Check if the item exists and **Delete/Remove** it first. |
| **Deleting** an item | Check if the item exists and **Add/Create** it first if missing. |
| **Enabling** a toggle | **Disable** the toggle first if it's already on. |
| **Moving/Reordering** | Ensure the list is in a **known default state** first. |

## Test Spec Markdown Template

Every test spec file must follow this exact structure:

```markdown
# Test Case: <Title>

## Objective
<One or two sentences describing what the test validates.>

## Preconditions
<Bulleted list of assumed ENVIRONMENTAL state only (e.g., "App is installed", "Network is ON"). NOT actionable steps.>

## Setup & Cleanup Flow
<Numbered list of plain-english, actionable steps to guarantee a clean starting state.
CRITICAL: You MUST include cleanup of data/state from prior runs. 

Example for "Add Spanish Language":
1. Tap the **Settings** tab.
2. Tap **My languages**.
3. If **Spanish** is present in the list, swipe to delete or use the **Edit** menu to remove it.
4. Return to the starting screen.
> 

## Test Flow
<Numbered list of sequential user actions to perform.>

## Assertions
<Bulleted list of specific, observable checks to confirm the test passed. Single source of truth for "Pass".>

## Fail Criteria
<Bulleted list of specific failure signals (crashes, errors, missing elements).>
```

## Writing Good Test Flows
- **Be specific**: Reference actual UI labels and icons (e.g. **Settings (gear icon)**).
- **Bold UI elements**: **Save Button**, **Home Screen**.
- **Idempotency is the priority**: Assume the test has already run and failed once; the setup flow must fix it.

## Example Test Spec (Wikipedia App)

**File:** `.test/add_spanish_language.md`

```markdown
# Test Case: Add Spanish Language via Settings

## Objective
Verify that a user can successfully add "Spanish" to their preferred languages list.

## Preconditions
- App is installed and launched.
- Device has network connectivity.

## Setup & Cleanup Flow
1. If the onboarding screen is visible, tap **Skip**.
2. Tap the **Settings** tab (gear icon) in the bottom navigation bar.
3. Tap **My languages**.
4. If **Spanish** is already in the **Your languages** list:
    a. Tap **Edit** in the top-right corner.
    b. Tap the **Delete (minus)** icon next to **Spanish**.
    c. Tap **Delete** to confirm.
    d. Tap **Done** in the top-right corner.
5. Tap the back button to return to the **Settings** screen.
6. Tap **Explore** in the bottom navigation bar.

## Test Flow
1. Tap the **Settings** tab (gear icon).
2. Tap **My languages**.
3. Tap **Add language**.
4. In the search field, type "Spanish".
5. Tap **Spanish** from the search results.
6. Wait for navigation back to **Wikipedia languages**.

## Assertions
- **Spanish** is displayed in the **Your languages** list.
- No error alerts appeared during the addition.

## Fail Criteria
- **Spanish** does not appear in the list after selection.
- The app crashes when searching for or selecting the language.
```

## Anti-Patterns
❌ **Non-idempotent setup**: Only handles "Skip onboarding" but leaves old data in the app.
✅ **Idempotent setup**: Actively checks for and removes the target data before starting the test.

❌ **Vague navigation**: "Go to settings".
✅ **Specific navigation**: "Tap the **Settings** icon in the bottom navigation bar".
icon in the bottom navigation bar".
