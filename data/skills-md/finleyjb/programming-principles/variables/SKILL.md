---
name: variables
description: Use when writing, editing, or reviewing variable declarations and names — locals, parameters, and constants.
---

Declare variables where they are first used and give every one a name a reader can understand at that point without help.

## Placement

Place variables as close to where they are first used as possible while maintaining the correct scope. A declaration far from its use forces the reader to hold it in mind across unrelated code. Parameters are given at the call site; fields and module-level constants cannot move — name those well instead.

## Naming

1. A variable name MUST contain a noun. Booleans MAY instead read as predicates: `isEmpty`, `hasPermission`, `canRetry`, `shouldRetry`.
2. A variable name MUST NOT exceed 3 words. Count words at the language's word boundaries — camelCase humps, underscores, dashes. An acronym counts as one word.
3. A variable name MUST NOT abbreviate words, with these exceptions only:

| Group | Abbreviations |
| --- | --- |
| General | `msg` (message), `val` (value), `temp` (temporary), `num` (number), `inc` (increment), `dec` (decrement), `iter` (iterator), `impl` (implementation) |
| Platform | `id` (identifier), `js` (JavaScript), `tz` (timezone) |
| Errors | `e`, `err` (error) — catch/except bindings only |

   An allowlisted abbreviation may also serve as one word of a longer name — `userId`, `msgCount`, `numRetries`. `temp` is the exception: it names a lifetime, not a thing, so it MUST modify another word (`tempName`) and never stand alone.

   Acronyms that are the universal name for the thing (`url`, `json`, `html`, `sql`, `api`, `http`, `csv`) are words, not abbreviations.

4. A variable name MUST NOT be a single letter, with these exceptions only:
   - `i`, `j`, `k` in loops
   - `x`, `y`, `z` coordinates
   - `r`, `g`, `b`, `a` for RGB color channels and alpha
   - `h`, `s`, `l` for HSL colors
   - `l`, `c`, `h` for OKLCH and LCH colors
   - parameters of a single-expression lambda or a function of at most 3 lines: `nums.map(x => x + 1)`
   - `e` in catch/except clauses

The bar for anything unlisted: it must be as universally understood as the entries above. `cust` for customer, `qty` for quantity, and `cfg` for configuration fail that bar — write the word out.

## Examples

```ts
// AVOID: abbreviated, single-letter, declared far from use
function renderInvoice(ord: Order, usr: User) {
  const d = new Date();
  const t = ord.total;
  let s = "";
  // ...40 unrelated lines...
  s = `Total: ${t} on ${d.toISOString()}`;
}

// PREFER
function renderInvoice(order: Order, user: User) {
  // ...unrelated lines...
  const isPaid = order.total > 0;
  const totalText = `Total: ${order.total}`;
}
```

```go
// AVOID: abbreviations Go does not require
func fetchEvents(c *Client) ([]Event, error) {
    evs := []Event{}
    for _, ev := range c.all() {
        if ev.ok {
            evs = append(evs, ev)
        }
    }
    return evs, nil
}

// PREFER
func fetchEvents(client *Client) ([]Event, error) {
    events := []Event{}
    for _, event := range client.all() {
        if event.valid {
            events = append(events, event)
        }
    }
    return events, nil
}
```

## Gotchas

- Extending the abbreviation list on your own authority — `res`, `cnt`, `ptr`, `buf`, `str` are not on it.
- `temp` standing alone — it names a lifetime, not a thing. It modifies another word (`tempName`); `tmp` and numbered variants like `temp2` are not spellings of it.
- Shrinking a name to fit the 3-word limit by abbreviating (`customerEmailAddress` → `custEmailAddr`) trades one violation for two.
- A single letter in a 10-line function because "it's a small lambda" — the 3-line limit is the whole allowance.
- Moving a declaration up "for grouping" — grouping is what pushes it away from its use, and out of the scope it belongs in.
- `seen` — a past participle, not a noun. Name the things: `seenKeys`, `seenNames`.

## Conventions and style rules

Language conventions and style rules MUST supersede these instructions. Where a project's style guide, linter, or language conventions dictate their own variable rules (Go's `err`, `ctx`, and handler parameters like `w` and `r`; Python's `self` and `cls`), follow those instead.
