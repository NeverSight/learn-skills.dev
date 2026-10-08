---
name: keeping-entry-points-thin
description: Use when implementing or changing HTTP handlers or routes, server actions, CLI commands, UI event handlers, queue consumers, scheduled jobs, or workers that parse input, query a database, run subprocesses, enforce authorization, or translate application errors into status codes, exit codes, messages, or acknowledgements; also when tempted to put SQL or a workflow in a route because it is read-only, urgent, or one-off, or to return exception text to callers.
---

# Keeping Entry Points Thin

## Overview

An entry point adapts a transport to an application operation. It handles its transport only: no business decisions and no direct database access. Server-side, read-only, and one-off do not change that boundary.

**Core principle:** An entry point parses input, calls the operation, and maps the result or error to its interface. HTTP handlers, CLI commands, UI events, and workers call the same operation for the same behavior.

These rules apply to new or requested changes. Do not refactor untouched legacy handlers solely to match them.

## Boundary Contract

| Entry point | Application operation |
| --- | --- |
| Parse HTTP, command, or message shape; authenticate; extract actor and context | Validate state-dependent rules and authorize against current state |
| Call an operation with transport-neutral values | Load or query data, decide, and own its transaction |
| Translate result and errors into status and body, exit code and output, or acknowledgement | Return native values and expected errors, never HTTP or CLI response objects |
| Wire resources at startup; a CLI may parse flags, read secrets, open a database and migrate, and assemble dependencies | Use prepared dependencies, not hidden startup side effects |

For a **new or changed** endpoint, including read-only aggregates, put data access in a concrete operation or query function, not the handler. No new service class is required. Static liveness needs no operation; passing a clock value does not make its interpretation a handler rule.

Use boundary schemas for input shape and format (for example Pydantic or Zod), then pass the validated values into the operation.

Do not put queries, `subprocess` calls, or workflows that implement business behavior in a route, command, UI handler, or job handler. Startup dependency wiring and database migration are the CLI exception described above. Keep entry points focused on transport adaptation; operations own business orchestration and persistence.

In one line, for writes: the operation owns the transaction; external effects happen after commit; retries must be idempotent.

## Error Mapping

- The operation raises or returns expected errors as native typed errors. The entry point translates them into an HTTP status, exit code, UI message, or job failure state (`errors.Is`/`errors.As` in Go, `instanceof` in TypeScript, `except` in Python).
- Return safe, user-facing messages only. Never expose stack traces, raw exception text, secrets, SQL, internal payloads, file paths, or upstream service details.
- Propagate unexpected errors with context, log them once at the boundary, and answer with a generic failure (a 500, a nonzero exit, a failed job). Never swallow them and never return their raw details. Exclude secrets, tokens, passwords, and personal data from logs as well as responses.
- Middleware may reject a request early. The operation still rechecks current authorization and ownership.

## Example

A read endpoint: the handler parses the range and maps errors; the operation owns the data access.

```typescript
import { z } from "zod";

type ReportStore = { count(days: number): Promise<number> };
type Request = { query: { range?: string } };
type Response = { status(code: number): { json(body: unknown): void } };
class ReportUnavailable extends Error {}
const RangeSchema = z.enum(["7", "30"]).transform(value => Number(value));

async function getUsage(store: ReportStore, days: number) {
  return { requests: await store.count(days) };
}

async function usageHandler(req: Request, res: Response, store: ReportStore) {
  const range = RangeSchema.safeParse(req.query.range);
  if (!range.success) return res.status(400).json({ error: "invalid range" });
  try {
    return res.status(200).json(await getUsage(store, range.data));
  } catch (error) {
    if (error instanceof ReportUnavailable) {
      return res.status(503).json({ error: "usage unavailable" });
    }
    throw error;
  }
}
```

A write endpoint in Python: the schema validates shape at the boundary, the route calls a service operation, and a domain error becomes a safe 409.

```python
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr, Field

router = APIRouter()


class CreateUser(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    email: EmailStr
    name: str = Field(min_length=1, max_length=100)


class CreatedUser(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UUID
    email: EmailStr
    name: str


class DuplicateUserError(Exception):
    pass


class Users:
    async def register(self, user: CreateUser) -> CreatedUser:
        ...  # may raise DuplicateUserError; other user operations live here too


def get_users() -> Users:
    return Users()


@router.post("/users", response_model=CreatedUser)
async def create_user(
    user: CreateUser,
    users: Annotated[Users, Depends(get_users)],
) -> CreatedUser:
    try:
        return await users.register(user)
    except DuplicateUserError as exc:
        raise HTTPException(status_code=409, detail="User already exists") from exc
```

Bad: the route owns the workflow, runs subprocesses, and reports success without checking anything.

```python
@router.post("/deploy/{stack}")
def deploy(stack: str):
    subprocess.run(["docker", "compose", "pull"], cwd=f"/stacks/{stack}")
    subprocess.run(["docker", "compose", "up", "-d"], cwd=f"/stacks/{stack}")
    return {"status": "ok"}
```

Fix: move the workflow, path validation, and result into an operation such as `stacks.deploy(stack)` that returns a typed result, and let the route call it and map its errors.

Preserve the roles, not these types or file layout, in other stacks.

## Testing

Test operation decisions and failures, plus boundary parsing and error mapping. Do not repeat every business case at every boundary.

## Common Mistakes

| Temptation | Decision |
| --- | --- |
| "It is only a SELECT, so SQL in the new route is harmless." | Read-only data access is still not an HTTP concern. Use one query function, not a whole hierarchy. |
| "Ship new route-level SQL now; extract later." | Add the small query boundary before shipping the new endpoint. |
| "This is urgent, so keep it directly in the route, component, or command." | Urgency does not move the boundary. A thin entry point calling one operation is the fastest compliant path. |
| "Middleware checked admin, so pass `isAdmin` into the write." | Pass actor identity; the operation rechecks current permissions in its own transaction. |
| "Thin CLI means it cannot open its database." | Startup wiring belongs at the entry point; business rules do not. |
| "The CLI needs this slightly differently, so copy the rule into the command." | Call the same operation. Change the operation only if behavior genuinely differs, not for a hypothetical transport. |
| "Return a status code or response map from the operation to shorten the handler." | The operation returns native values and errors; the entry point owns translation. |
| "Expose the raw exception detail so production is easier to debug." | Log internals once, with context, at the boundary. Return a safe message. |
| "Catch everything and return an empty or default result." | Map only expected errors. Unexpected errors propagate; never swallow them. |

## Red Flags

Stop and reconsider if you see:

- SQL, an ORM call, or `subprocess` implementing business behavior inside a route, command, UI handler, or job handler, rather than startup wiring.
- A domain decision (pricing, eligibility, permissions beyond identity) made in an entry point.
- An operation signature that takes a request, response, or context object, or returns a status code.
- `str(exc)`, a stack trace, a file path, or an upstream response body in a response.
- The same rule copied into a second entry point.
