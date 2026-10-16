---
name: helipod-email
description: Send transactional email from an application through Helipod Email - set up and verify a sending domain, send with the API or templates, check delivery. Use when the user wants their app to send email (password resets, receipts, notifications) via Helipod.
---

# Helipod Email

Uses a separate **email API key** (dashboard → Email → API keys) as `HELIPOD_EMAIL_API_KEY`. Base URL: `https://mail.helipod.io/api/email`.

## Set up

1. `email_status`: the project needs an email plan (the Free plan is fine for testing).
2. `add_email_domain` with the domain to send from (often a subdomain like `mail.example.com`), then give the user the DNS records from the response exactly as listed (copy them verbatim). If the domain is on Helipod, use the `helipod-domains` skill to add them.
3. `verify_email_domain` until it is verified.

## Send from code

Never put the key in client-side code. Store it as a secret (on Helipod: `set_variables` with `secrets`).

```js
await fetch("https://mail.helipod.io/api/email/send", {
  method: "POST",
  headers: { Authorization: `Bearer ${process.env.HELIPOD_EMAIL_API_KEY}`, "Content-Type": "application/json" },
  body: JSON.stringify({
    from: "Acme <hello@mail.example.com>",
    to: ["user@example.com"],
    subject: "Reset your password",
    html: "<p>Click <a href='{{link}}'>here</a></p>",
    variables: { link: resetUrl },
    idempotencyKey: `reset-${userId}-${token}`,
  }),
});
```

- Templates: create them in the dashboard, then send with `templateId` + `templateData`.
- `idempotencyKey` makes retries safe; mark one-time codes with `sensitive: true`.
- Attachments are not supported.

## Check delivery

`list_emails` / `get_email` show status (delivered, bounced, complained). Bounced and complained addresses are suppressed automatically.
