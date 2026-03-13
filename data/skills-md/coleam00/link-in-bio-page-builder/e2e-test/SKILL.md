---
name: e2e-test
description: Comprehensive end-to-end testing command. Launches parallel sub-agents to research the codebase (structure, database schema, potential bugs), then uses the Vercel Agent Browser CLI to test every user journey — taking screenshots, validating UI/UX, and querying the database to verify records. Run after implementation to validate everything before code review.
disable-model-invocation: true
---

# End-to-End Application Testing

## Pre-flight Check

### 1. Platform Check

agent-browser requires **Linux, WSL, or macOS**. Check the platform:
```bash
uname -s
```
- `Linux` or `Darwin` → proceed
- Anything else (e.g., `MINGW`, `CYGWIN`, or native Windows) → stop with:

> "agent-browser only supports Linux, WSL, and macOS. It cannot run on native Windows. Please run this command from WSL or a Linux/macOS environment."

Stop execution if the platform is unsupported.

### 2. Frontend Check

Verify the application has a browser-accessible frontend. Check for:
- A `package.json` with a dev/start script serving a UI
- Frontend framework files (pages/, app/, src/components/, index.html, etc.)
- Web server configuration

If no frontend is detected:
> "This application doesn't appear to have a browser-accessible frontend. E2E browser testing requires a UI to visit. For backend-only or API testing, a different approach is needed."

Stop execution if no frontend is found.

### 3. agent-browser Installation

Check if agent-browser is installed:
```bash
agent-browser --version
```

If the command is not found, install it automatically:
```bash
npm install -g agent-browser
```

After installation (or if it was already installed), ensure the browser engine is set up:
```bash
agent-browser install --with-deps
```

The `--with-deps` flag installs system-level Chromium dependencies on Linux/WSL. On macOS it is harmless.

Verify installation succeeded:
```bash
agent-browser --version
```

If installation fails, stop with:
> "Failed to install agent-browser. Please install it manually with `npm install -g agent-browser && agent-browser install --with-deps`, then re-run this command."

## Phase 1: Parallel Research

Launch **three sub-agents simultaneously** using the Task tool. All three run in parallel.

### Sub-agent 1: Application Structure & User Journeys

> Research this codebase thoroughly. Return a structured summary covering:
>
> 1. **How to start the application** — exact commands to install dependencies and run the dev server, including the URL and port it serves on
> 2. **Authentication/login** — if the app has protected routes, how to create a test account or log in (credentials from .env.example, seed data, or sign-up flow)
> 3. **Every user-facing route/page** — each URL path and what it renders
> 4. **Every user journey** — complete flows a user can take (e.g., "sign up → create profile → view public page"). For each journey, list the specific steps, interactions (clicks, form fills, navigation), and expected outcomes
> 5. **Key UI components** — forms, modals, dropdowns, pickers, toggles, and other interactive elements that need testing
>
> Be exhaustive. Testing will only cover what you identify here.

### Sub-agent 2: Database Schema & Data Flows

> Research this codebase's database layer. Read `.env.example` to understand environment variables for database connections. DO NOT read `.env` directly. Return a structured summary covering:
>
> 1. **Database type and connection** — what database is used (Postgres, MySQL, SQLite, etc.) and the environment variable name for the connection string (from .env.example)
> 2. **Full schema** — every table, its columns, types, and relationships
> 3. **Data flows per user action** — for each user-facing action (form submit, button click, etc.), document exactly what records are created, updated, or deleted and in which tables
> 4. **Validation queries** — for each data flow, provide the exact query to verify records are correct after the action

### Sub-agent 3: Bug Hunting

> Analyze this codebase for potential bugs, issues, and code quality problems. Focus on:
>
> 1. **Logic errors** — incorrect conditionals, off-by-one errors, missing null checks, race conditions
> 2. **UI/UX issues** — missing error handling in forms, no loading states, broken responsive layouts, accessibility problems
> 3. **Data integrity risks** — missing validation, potential orphaned records, incorrect cascade behavior
> 4. **Security concerns** — SQL injection, XSS, missing auth checks, exposed secrets
>
> Return a prioritized list with file paths and line numbers.

**Wait for all three sub-agents to complete before proceeding.**

## Phase 2: Start the Application

Using Sub-agent 1's startup instructions:

1. Install dependencies if needed
2. Start the dev server **in the background** (e.g., `npm run dev &`)
3. Wait for the server to be ready
4. Open the app with `agent-browser open <url>` and confirm it loads
5. Take an initial screenshot: `agent-browser screenshot e2e-screenshots/00-initial-load.png`

## Phase 3: Create Task List

Using the user journeys from Sub-agent 1 and findings from Sub-agent 3, create a task (using TaskCreate) for each user journey. Each task should include:

- **subject:** The journey name (e.g., "Test profile creation flow")
- **description:** Steps to execute, expected outcomes, database records to verify, and any related bug findings from Sub-agent 3
- **activeForm:** Present continuous (e.g., "Testing profile creation flow")

Also create a final task: "Responsive testing across viewports."

## Phase 4: User Journey Testing

For each task, mark it `in_progress` with TaskUpdate and execute the following.

### 4a. Browser Testing

Use the Vercel Agent Browser CLI for all browser interaction:

```
agent-browser open <url>              # Navigate to a page
agent-browser snapshot -i             # Get interactive elements with refs (@e1, @e2...)
agent-browser click @eN               # Click element by ref
agent-browser fill @eN "text"         # Clear field and type
agent-browser select @eN "option"     # Select dropdown option
agent-browser press Enter             # Press a key
agent-browser screenshot <path>       # Save screenshot
agent-browser screenshot --annotate   # Screenshot with numbered element labels
agent-browser set viewport W H        # Set viewport (e.g., 375 812 for mobile)
agent-browser wait --load networkidle # Wait for page to settle
agent-browser console                 # Check for JS errors
agent-browser errors                  # Check for uncaught exceptions
agent-browser get text @eN            # Get element text
agent-browser get url                 # Get current URL
agent-browser close                   # End session
```

**Refs become invalid after navigation or DOM changes.** Always re-snapshot after page navigation, form submissions, or dynamic content updates (modals, tabs, theme changes).

For each step in a user journey:

1. Snapshot to get current refs
2. Perform the interaction
3. Wait for the page to settle
4. **Take a screenshot** — save to a descriptive path under `e2e-screenshots/` organized by journey (e.g., `e2e-screenshots/profile-creation/03-form-submitted.png`)
5. **Analyze the screenshot** — use the Read tool to view the screenshot image. Check for visual correctness, UX issues, broken layouts, missing content, error states
6. Check `agent-browser console` and `agent-browser errors` periodically for JavaScript issues

Be thorough. Go through EVERY interaction, EVERY form field, EVERY button. The goal is that by the time this finishes, every part of the UI has been exercised and screenshotted.

### 4b. Database Validation

After any interaction that should modify data (form submits, deletions, updates):

1. Query the database to verify records. Use the environment variable from Sub-agent 2's research for the connection string and the schema docs to know what to check.
   - **Postgres:** use `psql` directly — e.g., `psql "$DATABASE_URL" -c "SELECT theme FROM profiles WHERE username = 'testuser'"`
   - **SQLite:** use `sqlite3` directly — e.g., `sqlite3 db.sqlite "SELECT theme FROM profiles WHERE username = 'testuser'"`
   - **Other databases:** write a small ad hoc script in the application's language, run it, then delete it
2. Verify:
   - Records created/updated/deleted as expected
   - Values match what was entered in the UI
   - Relationships between records are correct
   - No orphaned or duplicate records

### 4c. Issue Handling

When an issue is found (UI bug, database mismatch, JS error):

1. **Document it:** what was expected vs what happened, screenshot path, relevant DB query results
2. **Fix the code** — make the correction directly
3. **Re-run the failing step** to verify the fix worked
4. **Take a new screenshot** confirming the fix

### 4d. Responsive Testing

For the responsive testing task, revisit key pages at these viewports:

- **Mobile:** `agent-browser set viewport 375 812`
- **Tablet:** `agent-browser set viewport 768 1024`
- **Desktop:** `agent-browser set viewport 1440 900`

At each viewport, screenshot every major page. Analyze for layout issues, overflow, broken alignment, and touch target sizes on mobile.

After completing each journey, mark its task as `completed` with TaskUpdate.

## Phase 5: Cleanup

After all testing is complete:
1. Stop the dev server background process
2. Close the browser session: `agent-browser close`

## Phase 6: Report

### Text Summary (always output)

Present a concise summary:

```
## E2E Testing Complete

**Journeys Tested:** [count]
**Screenshots Captured:** [count]
**Issues Found:** [count] ([count] fixed, [count] remaining)

### Issues Fixed During Testing
- [Description] — [file:line]

### Remaining Issues
- [Description] — [severity: high/medium/low] — [file:line]

### Bug Hunt Findings (from code analysis)
- [Description] — [severity] — [file:line]

### Screenshots
All saved to: `e2e-screenshots/`
```

### Markdown Export (ask first)

After the text summary, ask the user:

> "Would you like me to export the full testing report to a markdown file? It includes per-journey breakdowns, all screenshot references, database validation results, and detailed findings — useful as context for follow-up fixes or GitHub issues."

If yes, write a detailed report to `e2e-test-report.md` in the project root containing:
- Full summary with stats
- Per-journey breakdown: steps taken, screenshots, database checks, issues found
- All issues with full details, fix status, and file references
- Bug hunt findings from the code analysis sub-agent
- Recommendations for any unresolved issues
