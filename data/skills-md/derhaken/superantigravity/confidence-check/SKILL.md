---
name: confidence-check
description: Use before implementing a feature or making significant changes to verify you have enough context and understanding to proceed — prevents wasted effort from proceeding with wrong assumptions
---

# Confidence Check

## Overview

A quick self-assessment before implementation. If confidence is below threshold,
gather more information first. Don't build on shaky understanding.

## When to Use

- Before starting implementation of a feature
- When requirements feel ambiguous
- After reading existing code that you're about to modify
- When you're unsure about a technical approach

## The Check

Score yourself 0-10 on each:

**Understanding (0-10)**
- Do I understand what this is supposed to do?
- Do I understand why it needs to exist?
- Do I understand who uses it and how?

**Context (0-10)**
- Do I know which files I need to touch?
- Do I understand the existing code patterns I'm building on?
- Do I know the data flow end-to-end?

**Approach (0-10)**
- Do I know which approach I'll take and why?
- Have I considered at least one alternative?
- Do I know how to test this?

## Anti-Gaming Protocol

This check fails its purpose if you score yourself 30/30 automatically.

**REQUIRED: For any dimension scoring 8 or higher, write one specific piece of evidence.**

The evidence must name a concrete artifact — a file, a line range, a function name, a
specific behavior you observed. General statements do not count.

Examples of valid evidence:
- "Context: 9/10 — I have read auth.js:45-120 and understand the JWT validation flow,
  including how the middleware chain passes the decoded token to route handlers."
- "Understanding: 8/10 — The requirement says 'users can reset their password via email.'
  I know it means: generate a one-time token, email a reset link, validate the token on
  return, and expire it after 1 hour per the spec in JIRA-442."
- "Approach: 8/10 — I will use crypto.randomBytes(32) for token generation (Node.js docs
  confirm this is cryptographically secure), store the SHA-256 hash in the DB (not the
  raw token), and check expiry with a simple timestamp column."

Examples of invalid evidence (too vague):
- "Context: 9/10 — I understand the codebase well."
- "Understanding: 8/10 — The requirement is clear."
- "Approach: 9/10 — I know what to do."

**If you cannot name specific evidence for a dimension scored 8+, the maximum score for
that dimension is 6.**

This rule cannot be overridden. It is not a suggestion.

## Scoring

| Score | Action |
|-------|--------|
| 27-30 | Proceed with implementation |
| 20-26 | Fill gaps before starting — identify and resolve unclear items |
| Below 20 | Stop — load brainstorming skill or discuss with user before any code |

## External Validation at 20-26

Before proceeding when total score is in the 20-26 range:

State your understanding out loud in one paragraph. Write it as if explaining to the user
what you are about to build, why, and how. Be specific.

If the user does not correct it within their next response, proceed with implementation.

If the user does correct it, re-run the confidence check from the beginning with the
updated understanding. Do not proceed until either (a) the check returns 27+ or (b) you
are in the 20-26 range with validated understanding.

## Context Change Handling

If your confidence drops below 20 mid-implementation due to discovered complexity, unexpected
code patterns, contradictory requirements, or any other reason:

**STOP immediately. Do not continue writing code.**

Announce: "Confidence has dropped to [X]/30 due to [specific reason]. Pausing implementation
to [specific gap-filling action]."

Then execute the gap-filling action. Do not resume implementation until confidence returns
to 20 or above (with external validation if below 27) or to 27+ for autonomous continuation.

Examples:
- "Confidence has dropped to 15/30 due to discovering that the email service uses a
  different interface than I assumed. Pausing implementation to read email-service/client.js
  before continuing."
- "Confidence has dropped to 18/30 due to finding three competing authentication patterns
  in the codebase. Pausing implementation to ask: which auth pattern should the password
  reset endpoint follow?"

## What to Do With Low Scores

**Low on Understanding:** Restate the requirement in your own words and ask the user to
confirm before proceeding. Do not assume you understood — make the understanding explicit
and get it validated.

**Low on Context:** Read the relevant files before proceeding. Do not write code that touches
files you have not read. Use the deep-research skill for external unknowns (third-party APIs,
library behavior, compatibility questions).

**Low on Approach:** Load the architecture-design skill. Explore 2-3 options before committing
to one. Do not begin writing code until you have chosen an approach with reasoning.

## Red Flags

| Thought | Reality |
|---------|---------|
| "I'll figure it out as I go" | Proceeding with low confidence wastes everyone's time. |
| "It's probably fine" | Probably is not good enough before writing code. |
| "I can't get higher confidence" | Then escalate to the user — don't proceed blind. |
| "I know this codebase well enough" | Score it. If you can't name specific evidence for 8+, cap at 6. |
| "The check is a formality" | A confidence check you skip is not a confidence check. |

## Worked Example

The following is a complete self-assessment demonstrating correct application of this skill.

---

**Scenario:** Implementing a password reset endpoint

---

**Understanding: 8/10**

Evidence: "I know the endpoint needs to: (1) accept an email address, (2) generate a
time-limited reset token, (3) send an email with a reset link containing the token, (4)
accept the token on a second request, (5) validate it has not expired (1-hour TTL per the
product spec discussed in today's conversation), and (6) allow the user to set a new password.
I understand why it exists: users forget passwords and cannot self-recover otherwise. I know
who uses it: any unauthenticated user who has an account."

Score justification: 8 not 10 because I do not yet know whether the token should be
single-use (invalidated after first use) or whether it should allow multiple password-reset
attempts within the 1-hour window. This is a behavior I need to confirm.

---

**Context: 6/10**

Evidence: "I have read user.model.js and understand the User schema (id, email,
passwordHash, createdAt). I have not yet located the email service — I can see it referenced
in order.controller.js as `emailService.sendOrderConfirmation()` but I have not read the
email service implementation. I do not know the interface I need to call to send the reset
email."

Score justification: 6 because a key file (email service) is unread. Cannot score higher
without reading it. Per anti-gaming protocol: cannot claim 7+ without naming specific
evidence of email service understanding.

---

**Approach: 7/10**

Evidence: "I will use crypto.randomBytes(32).toString('hex') to generate the token
(cryptographically secure, standard Node.js). I will store the SHA-256 hash of the token
in a password_reset_tokens table (not the raw token — so a leaked DB does not enable
account takeover). I will set an expires_at column to NOW() + 1 hour. On the validation
request, I will hash the incoming token, look it up, check expiry, and delete the record.
I am unsure about the email provider interface, which affects the approach for the 'send
email' step."

Score justification: 7 because the token generation and validation approach is clear, but
the email dispatch step is uncertain pending reading the email service.

---

**Total: 8 + 6 + 7 = 21/30**

**Action: Fill gaps before starting.**

Gaps identified:
1. Read the email service implementation to understand the dispatch interface. (Low Context)
2. Confirm with user: should the token be single-use, or can it be used multiple times
   within the 1-hour window? (Low Understanding — specific ambiguity)

**External validation (20-26 range):**

Stating understanding: "I am about to implement a password reset endpoint that generates a
cryptographically secure token, stores its hash in a `password_reset_tokens` table with a
1-hour expiry, sends a reset link via the email service, and validates the token on return.
The main gap is the email service interface, which I will read before starting. I also need
to confirm whether tokens are single-use."

Waiting for user confirmation or correction before proceeding.
