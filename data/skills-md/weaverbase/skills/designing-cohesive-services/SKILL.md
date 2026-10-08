---
name: designing-cohesive-services
description: Use when adding or changing business behavior that an API, CLI, worker, scheduled job, or UI action calls; when deciding whether logic belongs in a service method, standalone function, query function, or helper; when a service is becoming a pass-through wrapper, a class per action, or a catch-all; when the same behavior is requested through a second transport; or when choosing what an operation returns and how it reports expected failures.
---

# Designing Cohesive Services

## Overview

An application operation owns one behavior and is callable unchanged by the entry points that need that behavior: HTTP handlers, CLI commands, workers, scheduled jobs, or UI actions. It is either a method on a cohesive service or a standalone function.

**Core principle:** Define the behavior as a transport-neutral operation first, then let each entry point call it. Group operations in a service because they share a feature, state, a resource, or an invariant. "Service-first" does not mean every function needs a service wrapper.

Name methods for actions (`orders.place`, `orders.cancel`). The method is the application operation itself, not a wrapper around a mandatory use-case layer.

These preferences apply to new or requested changes. Do not refactor, rename, or reorganize existing working code solely to match them. Explicit task instructions and the repository's own guides outrank these defaults.

## When to Use

- Adding behavior used by an API, CLI, worker, scheduled job, or UI action.
- Choosing between a cohesive service method, standalone function, query function, and pure helper.
- Someone proposes one service per action, an all-purpose service, or a new use-case layer over an existing operation.
- A function mixes orchestration, validation, formatting, persistence, and error mapping.
- Another transport needs behavior that already exists.

## Litmus Test

Before writing logic, ask: could another entry point call the same behavior without carrying transport objects into it?

- **Yes:** it is an application operation. Make it a method on a cohesive service or a standalone function (see the table below).
- **No, because it handles the transport:** parsing, extracting the actor, status codes, flags, and output formatting belong in the entry point. If business logic is coupled to these concerns, separate them rather than keeping the business logic in the handler. This test is about roles, not supporting every hypothetical transport or running server-side code in a browser.

## Quick Reference

| Observable need | Shape |
| --- | --- |
| Operations share state, resource lifecycle, or invariants | Methods on the same concrete service; each method is an application operation. |
| Behavior depends only on its inputs and shares no service responsibility | Standalone application function; entry points call it directly. |
| Complex read deserves a distinct home | Concrete query operation or module called by the entry point, never SQL in a handler. |
| Decision is clearer or reused when separated | Pure helper called by the owning operation. Extraction is optional. |
| A real implementation boundary varies or must be isolated | Small interface or port at that boundary, not an interface for every class. |
| Operation produces several values | Readable multiple typed returns (`order, receipt, err`) or a typed result (`OrderSummary`). Add a request or result type only when it makes the code clearer. |
| Function mixes orchestration, validation, formatting, persistence, and error mapping | Split by behavior. Do not split into a mandatory repository, core, or use-case layer. |

## Operation Contract

- **One behavior per operation.** When a function starts mixing responsibilities, split along behavior lines (place the order, build the receipt, query the history), not along architectural layers.
- **Native values in and out.** Never take or return transport objects: framework request or context objects, response bodies, HTTP statuses, or CLI output objects.
- **Typed results.** Return typed results or readable multiple returns. Do not return raw dicts, untyped objects, `any`, or framework responses, and do not defer result types to "later". Serializing to JSON is the entry point's job. Introduce a request or result DTO only when it is clearer than plain parameters or returns.
- **Current-state rules.** Enforce business validation, ownership, and authorization against current state inside the operation, even when an entry point or middleware already rejected some requests early.
- **Expected failures are typed errors.** Reuse the language's native sentinel or typed errors (for example, a sentinel `ErrOrderNotFound` matched with `errors.Is` in Go, or an `OrderNotFound` exception class in Python or TypeScript). The operation never constructs a transport response; the entry point maps the error.
- **Unexpected errors propagate.** Add context (wrap or chain) and let them travel to the boundary. Never swallow them inside the operation.
- **Writes own their transaction.** The operation that changes state defines the transaction boundary; helpers it calls do not commit on their own. External effects happen after commit, and retries must be idempotent.
- **A new transport changes nothing.** The same behavior through another transport calls the existing operation. If adding the transport forces an operation change (a request object, status code, or output format leaked in), the boundary was not clean: fix that. If the behavior genuinely differs, change the operation explicitly with a new parameter or method. Do not branch on the transport's name, and do not prebuild abstractions for hypothetical transports.

## Example

A cohesive service: deploy, stop, and status share the stack directory lookup, its path validation, and the compose client. Each method is an application operation with typed results and a typed expected error.

```python
from dataclasses import dataclass
from pathlib import Path


class StackNotFound(Exception):
    pass


@dataclass(frozen=True)
class DeployResult:
    stack: str
    services_started: int


@dataclass(frozen=True)
class StackStatus:
    stack: str
    running: bool


class Stacks:
    """Deploy, stop, and inspect stacks that live under one root directory."""

    def __init__(self, root: Path, compose: ComposeClient) -> None:
        # ComposeClient is a concrete wrapper around the compose CLI.
        self._root = root.resolve()
        self._compose = compose

    def deploy(self, stack: str) -> DeployResult:
        started = self._compose.up(self._directory(stack))
        return DeployResult(stack=stack, services_started=started)

    def stop(self, stack: str) -> None:
        self._compose.down(self._directory(stack))

    def status(self, stack: str) -> StackStatus:
        running = self._compose.is_running(self._directory(stack))
        return StackStatus(stack=stack, running=running)

    def _directory(self, stack: str) -> Path:
        directory = (self._root / stack).resolve()
        if directory.parent != self._root or not directory.is_dir():
            raise StackNotFound(stack)
        return directory
```

An input-only calculation needs no service state, so an HTTP endpoint and a batch job can both call it without an `OrderService.shippingBand` delegate:

```typescript
export function shippingBand(weightGrams: number): "standard" | "heavy" {
  if (!Number.isSafeInteger(weightGrams) || weightGrams < 0) {
    throw new RangeError("weight must be nonnegative whole grams");
  }
  return weightGrams < 2_000 ? "standard" : "heavy";
}
```

An operation that changes an order and enforces its current-state invariants belongs instead on the order-owning service. Let that operation load state, decide, and write within its transaction; a mandatory pure core or second use-case class adds no value by itself.

Bad: one class per action, each a pass-through that repeats the same lookup and shares the same client. The shape is wrong because the responsibilities are shared, not because each class has one method.

```python
class StackDeployer:
    def deploy(self, stack: str) -> DeployResult:
        return self._compose.up(self._root / stack)


class StackStopper:
    def stop(self, stack: str) -> None:
        self._compose.down(self._root / stack)  # lookup and validation duplicated or missing
```

## Common Mistakes

| Temptation | Decision |
| --- | --- |
| "An unwritten rule says all logic must be a service method." | Preference alone is not evidence. An independent calculation does not belong on an unrelated service. Check the actual project instructions and responsibilities. |
| "The team lead suggested a wrapper, so add one." | A suggestion does not make a pass-through useful. Follow explicit project instructions; otherwise skip the wrapper. |
| "Make one service per method, or put everything in one big service." | Group by shared responsibility. Add a method only when it shares the service's state, resource, or invariant. |
| "A service with one method must be wrong, so add more." | A single-method service is fine when it is the cohesive home of its behavior or owns real state. Do not invent methods to reach a count, and do not split or merge services to hit one either. |
| "Return a raw dict or untyped object first; add result types later." | The result shape is the contract. Return a typed result or readable multiple returns now. |
| "Invent request/result DTOs or an error hierarchy to mirror the framework." | Use native input, result, and error types. Add a DTO only when it is clearer. |
| "Add a repository layer, functional core, or use-case class for symmetry." | Extract a helper or abstraction only for a demonstrated reason. Do not import another language's class hierarchy or directory layout. |
| "The CLI needs it slightly differently, so copy the rule into the command." | Call the same operation. Change the operation explicitly only if the behavior genuinely differs. |
| "Pass the request object (or status code) through so the handler is shorter." | Operations take and return native values; the entry point owns translation. |
| "Let the function grow; it all happens together anyway." | Split by behavior once it mixes orchestration, validation, formatting, persistence, and error mapping. |

## Red Flags

Stop and reconsider if you think or see:

- A service method whose body only forwards to another method or function.
- A service whose methods share no state, resource, or invariant.
- "Return a raw untyped dict/object first and add result types later."
- Framework request, response, or context types in an operation signature.
- An operation that builds an HTTP status, response body, or CLI exit code.
- A new transport that requires editing the operation solely to accommodate request or response types.
- A swallowed error inside an operation.
