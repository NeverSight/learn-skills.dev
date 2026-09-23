---
name: gdpr-dev
description: "GDPR compliance for European developers. Use when building features that handle personal data: user registration, profiles, authentication, email sending, analytics, error tracking, payments, search indexes, background jobs, or any feature that stores, processes, or transmits information about people. Provides stack-aware gotchas, anti-patterns to avoid, and schema design principles. Does not ask questions — applies principles proactively based on what is being built."
---

# GDPR Dev

A reference for developers building GDPR-compliant web applications in Europe. These principles apply proactively — if personal data is involved, GDPR applies.

For the full list of anti-patterns, see [references/gotchas.md](references/gotchas.md). For schema design, see [references/schema-patterns.md](references/schema-patterns.md).

---

## Top 6 Gotchas

### 1. PII in logs
`console.log(user)` or logging request bodies sends personal data to error trackers and log aggregators. Sentry captures `console.log` calls as breadcrumbs — treat it as a PII risk. Log IDs, not objects.

```js
// Bad
console.log("Processing user:", user);
logger.info({ user });

// Good
logger.info({ userId: user.id });
```

### 2. JWT tokens containing PII
If email or name is in the JWT payload, that data cannot be erased when a user requests deletion — tokens already issued remain valid and cannot be recalled. Use opaque session tokens, or put only a user ID in JWTs with a very short expiry.

```js
// Bad — email is now unrevocable in every issued token
jwt.sign({ userId, email, name }, secret);

// Good
jwt.sign({ userId }, secret, { expiresIn: "15m" });
```

### 3. Soft deletes are not erasure
`deleted_at = now()` keeps all PII intact. The right to erasure means nulling or overwriting PII fields, not just marking a row deleted. Keep the row for referential integrity; erase the content.

```sql
-- Bad: PII still present
UPDATE users SET deleted_at = now() WHERE id = ?;

-- Good: PII removed, row preserved
UPDATE users SET email = null, name = null, erased_at = now() WHERE id = ?;
```

### 4. Backups bypass deletion
Erasing from the live database has no effect on backups. Either align backup retention with your erasure SLA, or prefer anonymization over deletion so backups contain no identifiable data.

### 5. IP addresses are PII
Access logs, rate-limiting records, and analytics all capture IP addresses. Under GDPR these are personal data. Apply the same retention and erasure policies as any other PII.

### 6. Error messages leak PII
Stack traces often include the data that triggered the error (`Error: User john@example.com not found`). These reach Sentry and log aggregators with PII attached. Sanitize error messages before logging.

```js
// Bad
throw new Error(`User ${email} not found`);

// Good
const err = new Error("User not found");
err.userId = userId; // internal reference only, not surfaced to Sentry
throw err;
```
