---
name: supaspec-builder
description: >
  Spec-driven development using Supaspec as the single source of truth. Use this skill
  whenever building, modifying, or maintaining code in a project that has a Supaspec
  specification (also referred to as "spec" or "supaspec"). Connects to Supaspec via MCP
  to read specs, track implementation status, and self-document all changes as bugs or
  features so future agents can reproduce the full implementation.
license: Apache-2.0
compatibility: Requires Supaspec MCP server connected via mcp_servers configuration
metadata:
  author: blackbird-lab
  version: "2.0"
  tags: "workflow, spec-driven, planning, supaspec, self-documenting"
---

# Supaspec Builder

You build software against specifications stored in Supaspec. The spec is the single source of truth. You self-document every change you make so any future agent can reproduce the full implementation.

When the user mentions "spec," "supaspec," or "specification" — they mean Supaspec. When they say "check the spec" or "what does the spec say" — they mean read from Supaspec via MCP.

---

## Part 1: Building From Spec

### Discovering What To Build

When the user asks you to build something, start by understanding what specs exist.

**List all projects:**
```
tool: project.list
```
This shows all Supaspec projects you have access to. The user may refer to a project by name or slug.

**Get a project with all sections:**
```
tool: project.get
params: { project: "project-name" }
```
This returns every section with its full content and status. Read this first to understand the full scope.

**Get a single section:**
```
tool: section.get
params: { project: "project-name", section: "section-slug" }
```
Use this when the user points you to a specific section to implement.

**Search across sections:**
```
tool: project.search
params: { project: "project-name", query: "payments" }
```
Use this when the user says something like "build the payments part" and you need to find the right section.

### Understanding Section Status

Each section has a status that tells you where it is in the workflow:

| Status | What it means | What you do |
|--------|--------------|-------------|
| `draft` | Still being written | Do NOT build. Tell the user it's not ready. |
| `wip` | Under review | Do NOT build. Tell the user it's still being reviewed. |
| `approved` | Ready to build | This is your green light. Start implementing. |
| `implementing` | Someone is building it | Check if it's you. If not, confirm with the user. |
| `implemented` | Build complete | Already done. Only touch if user asks for changes. |

### Starting a Build

When you start implementing an approved section:

1. **Set status to `implementing`:**
```
tool: section.set_status
params: { project: "project-name", section: "section-slug", status: "implementing", agent_name: "your-agent-name" }
```

2. **Read the full section content** and implement exactly what it describes.

3. **When done, set status to `implemented`:**
```
tool: section.set_status
params: { project: "project-name", section: "section-slug", status: "implemented", agent_name: "your-agent-name" }
```

### If the Spec Is Unclear

If you encounter ambiguity in the spec — something isn't specified or could be interpreted multiple ways — do NOT guess. Ask the user. You can also leave a comment on the section:

```
tool: comment.add
params: { project: "project-name", section: "section-slug", proposal: 1, agent_name: "your-agent-name", body: "The spec says 'handle payments' but doesn't specify whether to use Stripe Elements or Payment Element. Which one?" }
```

---

## Part 2: Self-Documenting Changes

This is critical. Every time you change code — whether fixing a bug or adding/modifying a feature — you must document what you did in Supaspec. This creates a living changelog that any future agent can read to understand what was built and why.

### Classifying Changes

When you make a change, determine: **is this a bug fix or a feature change?**

**Bug** — Something was broken and you fixed it. The intended behavior was already defined (in the spec, or obvious from context), but the code didn't match.

Examples:
- "The webhook handler crashes when Stripe sends a null event"
- "Login redirects to /undefined instead of /dashboard"
- "The API returns 500 when the email field is missing"

**Feature** — You added new behavior, changed existing behavior, or implemented something from the spec. This includes everything that's not a bug fix.

Examples:
- "Implemented the checkout flow per the spec"
- "Added email confirmation after payment"
- "Changed the loyalty points ratio to be merchant-configurable"
- "Refactored the auth module to use Stytch instead of custom JWT"

### Logging Bugs

When you fix a bug, log it in a section called `bugreports` in the project. If the section doesn't exist, create it.

**Check if bugreports section exists:**
```
tool: section.get
params: { project: "project-name", section: "bugreports" }
```

**If it doesn't exist, create it:**
```
tool: section.create
params: { 
  project: "project-name", 
  title: "Bug Reports", 
  content: "# Bug Reports\n\nAutomatically logged bugs found and fixed during implementation.\n",
  agent_name: "your-agent-name",
  message: "Initialize bug reports log"
}
```

**Append your bug to the section:**
```
tool: section.update
params: {
  project: "project-name",
  section: "bugreports",
  agent_name: "your-agent-name",
  message: "Log bug: brief description",
  content: "<existing content plus new entry>"
}
```

Each bug entry should follow this format in the section:

```markdown
## [DATE] Brief title of the bug

**Issue:** What was broken. Be specific — what happened vs what should have happened.

**Cause:** Why it was broken. The root cause, not just the symptom.

**Fix:** What you changed to fix it.
```

Example entry:

```markdown
## [2026-02-25] Webhook handler crashes on null Stripe event

**Issue:** The payment webhook handler threw an unhandled TypeError when Stripe sent 
a test event with a null `data.object` field. This caused all subsequent webhook 
deliveries to fail.

**Cause:** No null check on `event.data.object` before accessing `.id` property. 
Stripe sends null objects for certain test event types.

**Fix:** Added null guard in `handleWebhook()`. If `data.object` is null, log the 
event type and return 200 without processing.
```

### Logging Features

When you implement or change a feature, log it in a section called `features-{DD-Mon-YYYY}` using today's date. This groups features by the day they were implemented. If the section for today doesn't exist, create it.

**Check if today's features section exists:**
```
tool: section.get
params: { project: "project-name", section: "features-25-Feb-2026" }
```

**If it doesn't exist, create it:**
```
tool: section.create
params: {
  project: "project-name",
  title: "Features 25-Feb-2026",
  content: "# Features — 25-Feb-2026\n\nFeatures implemented or changed today.\n",
  agent_name: "your-agent-name",
  message: "Initialize features log for 25-Feb-2026"
}
```

**Append your feature to the section:**
```
tool: section.update
params: {
  project: "project-name",
  section: "features-25-Feb-2026",
  agent_name: "your-agent-name",
  message: "Log feature: brief description",
  content: "<existing content plus new entry>"
}
```

Each feature entry should follow this format:

```markdown
## Brief title of the feature

**What:** What this feature does from the user's perspective.

**Why:** Why it was added — reference the spec section if it came from the spec, 
or note that the user requested it during implementation.

**How:** How it was implemented. Key architectural decisions, libraries used, 
patterns followed.

**Spec section:** Which spec section this implements (if applicable).
```

Example entry:

```markdown
## Stripe Connect merchant onboarding

**What:** Merchants can now connect their Stripe account to receive payments 
directly. The onboarding flow uses Stripe's hosted onboarding page and redirects 
back to the merchant dashboard on completion.

**Why:** Implements the "Merchant Onboarding" requirement from the Payments spec section.

**How:** Created a Connect onboarding endpoint that generates an AccountLink and 
redirects the merchant. A webhook listener handles `account.updated` events to 
track onboarding status. Merchant model extended with `stripeAccountId` and 
`stripeOnboardingStatus` fields.

**Spec section:** payments → Stripe Connect Onboarding
```

### When You're Not Sure: Bug or Feature?

Use this quick test:

- **"Was it supposed to work and didn't?"** → Bug
- **"Is this new behavior or changed behavior?"** → Feature
- **"I'm refactoring but behavior stays the same"** → Neither — don't log it unless the refactor is significant, in which case log as a feature with a note that it's a refactor.

### Multiple Changes in One Session

If you fix 3 bugs and implement 2 features in one session, log each one separately. Don't batch them into a single entry. Each change gets its own entry so future agents can understand each change independently.

---

## Summary: The Complete Workflow

```
1. User says "build X"
2. You read the spec from Supaspec (project.get or section.get)
3. You set status to "implementing"
4. You implement the spec
5. For each change you make:
   - Bug fix → log in "bugreports" section
   - Feature → log in "features-{date}" section
6. You set status to "implemented"
```

On subsequent iterations (user gives feedback, finds bugs, requests changes):

```
1. User gives feedback
2. You make the change
3. You classify: bug or feature
4. You log it in the appropriate section
5. Repeat
```

The bugreports and features sections become the project's living changelog. Any agent that reads these sections knows exactly what was built, what broke, and how everything was fixed — without having to read through chat histories.
