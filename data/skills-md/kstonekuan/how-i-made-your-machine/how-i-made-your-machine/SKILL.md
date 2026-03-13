---
name: how-i-made-your-machine
description: Apply the "How I Made Your Machine" coding style guide to implementation, refactoring, and code review tasks across TypeScript, Rust, and Python. Use when a request asks for this style guide, when improving maintainability and type safety, when modeling domain concepts with explicit variants/types, or when enforcing behavior-first testing.
---

# How I Made Your Machine

_A guide to writing software for humans and agents: the story of how I made your machine._

## Agent Usage

1. Read this guide before implementing, refactoring, or reviewing code.
2. Treat these rules as defaults unless the user requests a different tradeoff.
3. Model finite values and mutually exclusive states with explicit variants/enums/unions.
4. Prefer domain-specific types and function signatures over generic primitives.
5. Preserve behavior-first testing: test business outcomes, not framework internals or third-party behavior.
6. Call out justified exceptions explicitly when constraints force weaker typing or non-ideal structure.
7. Keep unrelated code unchanged; apply the guide to the task scope instead of broad rewrites.

## Agent Workflow

1. Identify which sections below apply to the current task.
2. Implement or refactor using the relevant patterns.
3. Review the result against the Core Principles and Type Design Signals.
4. Explain key changes in terms of maintainability, type safety, and behavior correctness.

## Purpose

This guide lays out how we should write code for maintainability, type safety, and behavior-first testing across projects.
It sets strong defaults, with room for justified exceptions when the tradeoff is clear.

## Core Principles

- Make invalid states hard to represent.
- Model domain concepts explicitly instead of using ad-hoc primitives.
- Use the type system and compiler as first-line quality gates.
- Optimize for readable intent over clever implementation.
- Test business behavior rather than framework or library internals.

## Type Safety and Relying on the Compiler

Using a type-safe language is not enough on its own.
We have to be intentional about how we model data and behavior so the compiler and static analysis can do real work for us.
It is easy to write code that technically type-checks while still side-stepping most of those guarantees.

Here are some patterns that are useful to follow:

- Prefer domain types over raw strings and loosely typed containers.
- Use unions/enums/typed variants when valid values are finite.
- Favor exhaustive pattern matching where possible.
- Represent unknown external values explicitly (`Unknown*`) instead of falling back silently.
- Avoid weakening types (`any`, broad casts, untyped flows) unless unavoidable.

### Type Design Signals

- If the value set is finite, use a union/enum instead of `string`.
- If states are mutually exclusive, use one state union/enum instead of multiple booleans.
- If function inputs represent domain concepts, use those domain types directly.

### Example 1: Finite Value Set as Variants

<Tabs groupId="finite-values">
  <TabItem value="pseudocode" label="Pseudocode" default>

```text
Under-modeled:
  status: string

Better modeled:
  Status = "draft" | "published" | "archived"
  status: Status
```

  </TabItem>
  <TabItem value="typescript" label="TypeScript">

```ts
// Bad: unconstrained string allows invalid values.
const underModeledStatus: string = "draff";

// Good: finite union prevents invalid states.
type Status = "draft" | "published" | "archived";
const modeledStatus: Status = "draft";
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
// Bad: free-form string can carry invalid values.
let under_modeled_status = "draff";

// Good: enum constrains the value set.
enum Status {
    Draft,
    Published,
    Archived,
}

let modeled_status = Status::Draft;
let _ = (under_modeled_status, modeled_status);
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
# Bad: unconstrained string allows invalid values.
under_modeled_status: str = "draff"

# Good: StrEnum constrains valid values.
from enum import StrEnum

class Status(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

modeled_status: Status = Status.DRAFT
```

  </TabItem>
</Tabs>

### Example 2: Boolean Combinations to State Variants

<Tabs groupId="boolean-state">
  <TabItem value="pseudocode" label="Pseudocode" default>

```text
Under-modeled:
  is_draft: boolean
  is_published: boolean
  is_archived: boolean

Better modeled:
  ContentState = "draft" | "published" | "archived"
  content_state: ContentState
```

  </TabItem>
  <TabItem value="typescript" label="TypeScript">

```ts
// Bad: boolean combinations allow impossible states.
const isDraft = true;
const isPublished = true;
const isArchived = false;

// Good: one variant encodes one valid state.
type ContentState = "draft" | "published" | "archived";
const contentState: ContentState = "published";
void [isDraft, isPublished, isArchived];
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
// Bad: booleans can contradict each other.
struct UnderModeledContentState {
    is_draft: bool,
    is_published: bool,
    is_archived: bool,
}

// Good: enum enforces one state at a time.
enum ContentState {
    Draft,
    Published,
    Archived,
}

let under_modeled_content_state = UnderModeledContentState {
    is_draft: true,
    is_published: true,
    is_archived: false,
};
let modeled_content_state = ContentState::Published;
let _ = (
    under_modeled_content_state.is_draft,
    under_modeled_content_state.is_published,
    under_modeled_content_state.is_archived,
    modeled_content_state,
);
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
# Bad: booleans can represent impossible combinations.
is_draft = True
is_published = True
is_archived = False

# Good: Literal constrains to one valid state.
from typing import Literal

ContentState = Literal["draft", "published", "archived"]

content_state: ContentState = "published"
_ = (is_draft, is_published, is_archived, content_state)
```

  </TabItem>
</Tabs>

### Example 3: Functions Consume Domain Types

<Tabs groupId="function-inputs">
  <TabItem value="pseudocode" label="Pseudocode" default>

```text
Under-modeled:
  schedule_message(channel: string, is_immediate: boolean, is_scheduled: boolean)

Better modeled:
  Channel = "email" | "sms" | "push"
  DeliveryMode = "immediate" | "scheduled"
  schedule_message(channel: Channel, delivery_mode: DeliveryMode)
```

  </TabItem>
  <TabItem value="typescript" label="TypeScript">

```ts
// Bad: primitives hide domain intent and allow contradictions.
function scheduleMessageUnderModeled(
  channel: string,
  isImmediate: boolean,
  isScheduled: boolean,
): void {
  void [channel, isImmediate, isScheduled];
}

// Good: explicit domain types make valid states clear.
type Channel = "email" | "sms" | "push";
type DeliveryMode = "immediate" | "scheduled";

function scheduleMessage(channel: Channel, deliveryMode: DeliveryMode): void {
  void [channel, deliveryMode];
}
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
// Bad: primitives allow invalid channels and conflicting mode flags.
fn schedule_message_under_modeled(channel: &str, is_immediate: bool, is_scheduled: bool) {
    let _ = (channel, is_immediate, is_scheduled);
}

// Good: domain enums constrain function inputs.
enum Channel {
    Email,
    Sms,
    Push,
}

enum DeliveryMode {
    Immediate,
    Scheduled,
}

fn schedule_message(channel: Channel, delivery_mode: DeliveryMode) {
    let _ = (channel, delivery_mode);
}
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
# Bad: primitive inputs accept invalid values and contradictory flags.
def schedule_message_under_modeled(
    channel: str,
    is_immediate: bool,
    is_scheduled: bool,
) -> None:
    _ = (channel, is_immediate, is_scheduled)

# Good: domain literals constrain allowed values.
from typing import Literal

Channel = Literal["email", "sms", "push"]
DeliveryMode = Literal["immediate", "scheduled"]

def schedule_message(channel: Channel, delivery_mode: DeliveryMode) -> None:
    _ = (channel, delivery_mode)
```

  </TabItem>
</Tabs>

## Self-Documenting Code

Self-documenting code is usually better than writing comments everywhere.
Comments go stale quickly, while clear naming and structure have to evolve with the program.

- Prefer descriptive, domain-aligned names even when verbose.
- Keep function and type names intention-revealing.
- Add comments only for non-obvious decisions, invariants, or tradeoffs.
- Avoid comments that restate what code already makes obvious.

### Example 4: Document the Why, Not the Obvious What

<Tabs groupId="documenting-why">
  <TabItem value="pseudocode" label="Pseudocode" default>

```text
Low-value comment:
  // Increment retry count
  retry_count = retry_count + 1

High-value comment:
  // Billing provider closes refunds at next-day midnight, so keep a one-day grace period.
  refund_grace_period_days = 1
  is_refund_eligible = days_since_purchase <= refund_window_days + refund_grace_period_days
```

  </TabItem>
  <TabItem value="typescript" label="TypeScript">

```ts
// Bad: restates obvious code behavior without context.
function incrementRetryCount(retryCount: number): number {
  // Increment retry count.
  return retryCount + 1;
}

// Good: documents a non-obvious business constraint.
function isRefundEligible(
  daysSincePurchase: number,
  refundWindowDays: number,
): boolean {
  // Billing provider closes refunds at next-day midnight, so we keep a one-day grace period.
  const refundGracePeriodInDays = 1;
  return daysSincePurchase <= refundWindowDays + refundGracePeriodInDays;
}
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
// Bad: restates obvious behavior.
fn increment_retry_count(retry_count: u32) -> u32 {
    // Increment retry count.
    retry_count + 1
}

// Good: documents a non-obvious business constraint.
fn is_refund_eligible(days_since_purchase: u32, refund_window_days: u32) -> bool {
    // Billing provider closes refunds at next-day midnight, so we keep a one-day grace period.
    let refund_grace_period_in_days = 1;
    days_since_purchase <= refund_window_days + refund_grace_period_in_days
}

let _ = increment_retry_count(0);
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
# Bad: restates obvious behavior.
def increment_retry_count(retry_count: int) -> int:
    # Increment retry count.
    return retry_count + 1

# Good: documents a non-obvious business constraint.
def is_refund_eligible(days_since_purchase: int, refund_window_days: int) -> bool:
    # Billing provider closes refunds at next-day midnight, so we keep a one-day grace period.
    refund_grace_period_in_days = 1
    return days_since_purchase <= refund_window_days + refund_grace_period_in_days

_ = increment_retry_count(0)
```

  </TabItem>
</Tabs>

## Testing Business Logic First

Tests are important for verifying behavior and preventing regression at both unit and integration levels.
But we should avoid writing tests for the sake of writing tests: they add maintenance cost and create noise when they assert outcomes that do not matter to business behavior.

- Test business outcomes and domain behavior first.
- Prioritize tests for state transitions, input-to-output rules, defaults, and fallback behavior.
- Do not test third-party/library internals.
- Avoid mocks by default.
- Use mocks only for unstable boundaries (network, filesystem, time, OS/process boundaries).
- Assert externally meaningful behavior, not private implementation details.

### Example 5: Test State Transitions and Outcomes

<Tabs groupId="testing-behavior">
  <TabItem value="pseudocode" label="Pseudocode" default>

```text
Brittle:
  assert transition_helper_called_once()

Behavior-focused:
  result = transition_order_state("draft", "publish")
  assert result == "published"
```

  </TabItem>
  <TabItem value="typescript" label="TypeScript">

```ts
import { describe, expect, it } from "vitest";

describe("transitionOrderStateUnderTest", () => {
  it("bad: asserts an implementation detail", () => {
    const transitionHelperCallCount = 1;
    expect(transitionHelperCallCount).toBe(1);
  });
});

describe("transitionOrderState", () => {
  it("good: asserts observable state transition", () => {
    const nextState = transitionOrderState("draft", "publish");
    expect(nextState).toBe("published");
  });
});
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
#[test]
fn bad_asserts_implementation_detail_only() {
    let transition_helper_call_count = 1;
    assert_eq!(transition_helper_call_count, 1);
}

#[test]
fn good_transitions_draft_to_published_when_publish_is_requested() {
    let next_state = transition_order_state("draft", "publish");
    assert_eq!(next_state, "published");
}
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
def test_bad_asserts_implementation_detail_only() -> None:
    transition_helper_call_count = 1
    assert transition_helper_call_count == 1

def test_good_transition_order_state_moves_draft_to_published() -> None:
    next_state = transition_order_state("draft", "publish")
    assert next_state == "published"
```

  </TabItem>
</Tabs>

### Example 6: Mock Only Unstable Boundaries

<Tabs groupId="testing-mocks">
  <TabItem value="pseudocode" label="Pseudocode" default>

```text
Preferred:
  fake_clock = FixedClock("2025-01-01T00:00:00Z")
  assert discount_is_active(fake_clock)

Avoid:
  assert internal_helper_called("calculate_discount_window")
```

  </TabItem>
  <TabItem value="typescript" label="TypeScript">

```ts
import { expect, it, vi } from "vitest";

it("bad: mocks an internal helper and asserts internals", () => {
  const calculateDiscountWindow = vi.fn().mockReturnValue(true);
  calculateDiscountWindow();
  expect(calculateDiscountWindow).toHaveBeenCalledTimes(1);
});

it("good: mocks only unstable network boundary and asserts behavior", async () => {
  const fetchExchangeRate = vi.fn().mockRejectedValue(new Error("timeout"));
  const gateway = createCurrencyGateway({ fetchExchangeRate });

  const rate = await gateway.getRateOrFallback("USD", "EUR");

  expect(rate).toBe(0.92);
});
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
#[test]
fn bad_asserts_internal_helper_behavior() {
    let internal_helper_call_count = 1;
    assert_eq!(internal_helper_call_count, 1);
}

#[test]
fn good_uses_cached_rate_when_live_lookup_fails() {
    let gateway = CurrencyGateway::new(FailingRateClient, CachedRateStore::with_rate(0.92));
    let rate = gateway.get_rate_or_fallback("USD", "EUR");
    assert_eq!(rate, 0.92);
}
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
def test_bad_asserts_internal_helper_behavior() -> None:
    internal_helper_call_count = 1
    assert internal_helper_call_count == 1

def test_good_uses_cached_rate_when_live_lookup_fails() -> None:
    gateway = CurrencyGateway(
        rate_client=FailingRateClient(),
        cache_store=CachedRateStore(rate=0.92),
    )

    rate = gateway.get_rate_or_fallback("USD", "EUR")

    assert rate == 0.92
```

  </TabItem>
</Tabs>

## Exceptions

We can make exceptions when strict modeling creates disproportionate complexity, external contracts require looser typing, or performance/interoperability constraints apply.

When we take an exception, we should document:

- Which rule is being bent
- Why
- Which safeguards are in place (validation, logging, tests)

### Example 7: External Contract Requires Looser Typing

<Tabs groupId="exceptions">
  <TabItem value="pseudocode" label="Pseudocode" default>

```text
Rule being bent:
  "Finite value set -> union/enum instead of string"

Why:
  Partner webhook sends undocumented status values.

Safeguards:
  validate known values
  map unknown values to UnknownPartnerStatus
  log raw unknown values
  test known and unknown inputs
```

  </TabItem>
  <TabItem value="typescript" label="TypeScript">

```ts
// Bad: assumes external input already matches strict known values.
type UnderModeledPartnerStatus = "accepted" | "rejected";

function parsePartnerStatus(rawPartnerStatus: UnderModeledPartnerStatus): UnderModeledPartnerStatus {
  return rawPartnerStatus;
}

// Good: accept string input, validate known values, and map unknown values explicitly.
type KnownPartnerStatus = "accepted" | "rejected";
type PartnerStatus = KnownPartnerStatus | "unknown_partner_status";

function mapPartnerStatus(rawPartnerStatus: string): PartnerStatus {
  if (rawPartnerStatus === "accepted" || rawPartnerStatus === "rejected") {
    return rawPartnerStatus;
  }

  console.warn("unknown partner status", { rawPartnerStatus });
  return "unknown_partner_status";
}
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
// Bad: panics on unexpected partner status values.
enum UnderModeledPartnerStatus {
    Accepted,
    Rejected,
}

fn parse_partner_status(raw_partner_status: &str) -> UnderModeledPartnerStatus {
    match raw_partner_status {
        "accepted" => UnderModeledPartnerStatus::Accepted,
        "rejected" => UnderModeledPartnerStatus::Rejected,
        _ => panic!("unsupported partner status: {raw_partner_status}"),
    }
}

// Good: capture unknown values explicitly and continue safely.
enum PartnerStatus {
    Accepted,
    Rejected,
    UnknownPartnerStatus,
}

fn map_partner_status(raw_partner_status: &str) -> PartnerStatus {
    match raw_partner_status {
        "accepted" => PartnerStatus::Accepted,
        "rejected" => PartnerStatus::Rejected,
        _ => {
            eprintln!("unknown partner status: {raw_partner_status}");
            PartnerStatus::UnknownPartnerStatus
        }
    }
}

let _ = parse_partner_status("accepted");
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
from typing import Literal

# Bad: assumes the partner only ever sends known values.
UnderModeledPartnerStatus = Literal["accepted", "rejected"]

def parse_partner_status(raw_partner_status: UnderModeledPartnerStatus) -> UnderModeledPartnerStatus:
    return raw_partner_status

# Good: accept raw string input and map unknown values explicitly.
PartnerStatus = Literal["accepted", "rejected", "unknown_partner_status"]

def map_partner_status(raw_partner_status: str) -> PartnerStatus:
    if raw_partner_status in {"accepted", "rejected"}:
        return raw_partner_status

    print(f"unknown partner status: {raw_partner_status}")
    return "unknown_partner_status"
```

  </TabItem>
</Tabs>
