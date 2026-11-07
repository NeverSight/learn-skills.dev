---
name: writing-error-messages
description: Use when writing, reviewing, or rewriting user-facing error messages, validation messages, form errors, empty/error states, auth errors, failure notifications, retry/support copy, CLI errors, or API errors humans will read. Helps make errors specific, actionable, non-blaming, accessible, and safe without leaking sensitive details.
---

# Writing Error Messages

## Quick Start

Before writing, identify:

1. **Audience:** end user, admin, developer, support agent, or operator.
2. **Failure:** what action failed and what still happened successfully.
3. **Cause:** known, unknown, user-correctable, service-side, third-party, or security-sensitive.
4. **Recovery:** what the reader can do now, what the system will do next, and where they can get help.

Then write this shape:

```text
[What happened]
[Reassurance if useful]. [Why it happened, if known and safe]. [Specific next action]. [Backup path if it keeps happening].
```

Example:

```text
Unable to connect your account
Your changes were saved, but we couldn't connect the account because of an issue on our end. Try connecting again. If this keeps happening, contact support.
```

## Core Rules

| Rule | Do | Avoid |
|------|----|-------|
| Say what happened | "We couldn't save your file." | "Something went wrong." |
| Say what was not affected | "Your draft was saved." | Leaving the user to wonder if data was lost |
| Give the next action | "Check the card number and try again." | "OK" / "Close" as the only path |
| Use plain language | "We couldn't connect to Dropbox." | "Fetch failed" / "credentials denied" |
| Avoid blame | "Store name is required." | "You forgot to enter a store name." |
| Match the stakes | Calm, direct, respectful | "Oops!" / jokes / cutesy tone |
| Be specific when safe | "Enter a date in the past." | "Invalid input." |
| Be generic when security requires it | "Invalid email or password." | "That email exists, but the password is wrong." |

## Message Anatomy

Use only the pieces the situation needs.

| Piece | Purpose | Pattern |
|-------|---------|---------|
| Title | Summarize the failed action | "Couldn't save changes" |
| Body | Explain consequence and cause | "Your changes are still open, but we couldn't save them because the connection dropped." |
| Primary action | Tell the reader what to do | "Try again", "Update details", "Choose another file" |
| Backup path | Provide a way out | "If this keeps happening, contact support." |
| Diagnostic detail | Help technical readers or support | Error code, request ID, expected/received values, log location |

Keep UI body copy to 1-2 sentences when possible. Put longer diagnostic details in expandable text, logs, or support context.

## References

- Open `references/source-backed-patterns.md` when auditing many messages, resolving wording tradeoffs, or checking source-backed rationale.
- Open `references/rewrite-examples.md` when rewriting multiple messages or testing whether the skill is producing the right shape.

## Validation and Form Errors

For field-level errors:

- Put the message next to the field and summarize errors at the top for long forms.
- Match the field label or question so the reader can connect the message to the control.
- Say how to fix it, not only that it is wrong.
- Preserve the user's input so they can correct it.
- Do not validate before the user has had a fair chance to finish typing.

Good patterns:

```text
Enter an email address
Enter a date in the past
Password must be at least 12 characters
Choose a file smaller than 10 MB
```

Avoid:

```text
This field is required
Invalid input
You entered an illegal value
Validation failed
```

## Placement, Accessibility, and Empty States

- Put the error where the reader is looking: near the field, control, toast source, or failed item.
- Do not rely on color alone. Include visible text, icons or labels, and machine-readable semantics when working in UI code.
- For form pages, move focus to the error summary or first error according to the product's accessibility pattern.
- Preserve the user's work whenever possible.
- Do not turn an empty result into an error. If nothing failed, write an empty state: "No invoices found" plus the next useful action.

## Security and Privacy Gate

Specificity is not always better. Use a generic message when detail could reveal account existence, permissions, private data, system internals, fraud signals, or security policy.

Use generic copy for login and account recovery:

```text
Invalid email or password
If an account exists for that email address, we'll send password reset instructions.
```

Do not reveal:

```text
That email exists, but the password is wrong
This account is locked
No account found for this email
```

If the user needs help, give a safe path: support, recovery instructions, request ID, or an audit-safe explanation.

## Developer-Facing and CLI Errors

When the reader can act on technical details, include them in a structured way:

```text
Could not read config file
Expected TOML at ./app.config.toml, but found invalid syntax on line 12: missing closing quote.
Fix the syntax and run `app deploy` again.
```

Useful details:

- What command, file, field, or resource failed.
- What was expected and what was received.
- The smallest fix or next diagnostic command.
- A request ID, error code, or log path when support/debugging needs it.

Still avoid stack traces, raw exception names, and internal service names unless the audience can use them.

## When Asked for a Generic Error

Do not accept "just write a generic error" without checking whether the product can do better. Ask:

- What action was the user trying to complete?
- What triggered this error in the code or service?
- Is the cause known, unknown, intermittent, or security-sensitive?
- Was anything saved, sent, charged, deleted, or left unchanged?
- Can the user fix it, retry, wait, use another path, or contact support?
- How often does it happen, and does it block the main flow?

If the cause is truly unknown, use a generic-but-actionable fallback:

```text
Something went wrong
Refresh the page and try again. If this keeps happening, contact support with request ID {request_id}.
```

## Final Check

Before shipping, verify the message answers the reader's questions:

1. What happened?
2. Did I lose anything or create a duplicate?
3. Why did this happen, if it is safe to say?
4. What can I do next?
5. What happens if I do nothing?
6. Where can I get help if the fix does not work?
