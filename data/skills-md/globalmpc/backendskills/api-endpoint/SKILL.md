---
name: api-endpoint
description: Rules for HTTP API endpoints. Use when adding or changing any endpoint (route, request or response shape, status codes), especially login and ones that read or change other users' data.
---

# API endpoint

Examples are TypeScript with `pg`. The rules apply to any stack.

Anything that changes money, stock or balances, or calls a payment provider or email: also follow the
`data-integrity` skill (transactions, locks, idempotency).

## 1. Check who may call it, not just that they're logged in

Why: a logged-in user who changes the id in the URL reads or edits someone else's data (IDOR).

```ts
// Bad: any logged-in user can read any invoice
const { rows } = await pool.query("select * from invoices where id = $1", [id]);

// Good: scope the query to the caller; someone else's invoice looks the same as a missing one
const { rows } = await pool.query("select * from invoices where id = $1 and account_id = $2", [id, user.accountId]);
if (rows.length === 0) return sendError(res, 404, "not_found", "Invoice not found");
```

Admins or other roles get access through an explicit role check, never by skipping the filter.

## 2. Bad input is a 4xx, never a 500

Why: a 500 on bad input hides real errors in the noise. Bad values that slip through (negative amounts,
fractions) corrupt data.

- Validate the body and path params at the edge: types, integers where money and quantities are counted,
  ranges (`quantity >= 1`, `amountCents > 0`), required fields, ids that aren't numbers.
- Handle what a request can legally contain but your code doesn't expect, like the same item listed
  twice. Merge the duplicates or reject them with a 400, but don't let the request crash into a 500.
- Map expected database errors: unique violation (`23505`) → 409, foreign key violation (`23503`) → 404 or 400.

## 3. Limit how often anyone can try: login, codes, anything that sends or costs

Why: without a limit, a script guesses passwords or one-time codes until one works, or sends thousands of
emails and SMS on your bill.

```ts
// Bad: counts a failure only after checking it; 50 parallel guesses all see "0 failures so far"
if (failures.get(email) >= 10) return sendError(res, 429, ...);
if (!(await verifyPassword(password, hash))) failures.set(email, failures.get(email) + 1);

// Good: count the try first, in one atomic statement, in storage every server shares
const { rows: [c] } = await pool.query(
  `insert into attempts (key, n, since) values ($1, 1, now())
   on conflict (key) do update set n = attempts.n + 1 returning n`, [`login:${email.toLowerCase()}`]);
if (c.n > 10) return sendError(res, 429, "too_many_attempts", "Try again later");
```

- Key the limit on the account (and on the IP, with a looser limit), and make the window expire.
- Once the limit is hit, refuse even the right password until the window ends.
- An unknown account and a wrong password get the same response, so nobody can find out which accounts exist.
- In-memory counters only work with one server. Use the database or Redis.

## 4. Use what the repo already has, and test it

Why: a second auth check, error format or DB helper drifts from the first, and reviewers have to catch it.

- Use the repo's auth, error format and database access. Errors never return a bare string or a stack trace.
- Add tests with the repo's test setup: the happy path, someone else's resource, and bad input.

## Make it yours

Your team's choices. A line that says "not set" means: follow what the repo already does.

- **API docs or collection:** not set.
- **Error format:** not set.
- **Someone else's resource:** 404, so nobody learns it exists.
