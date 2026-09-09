---
name: alerts-composer
description: Translates natural-language alert intent into a validated Tradovate alert-DSL expression. Submits the expression via create_alert.expression. Covers 37 numeric functions across Account (netLiq, dollarOpenPL, dailyLossLimit, ...) and Contract (lastPrice, percentChange, settlementPrice, ...) entities. Also covers Position (netPos, posOpenPLUsd, posInitMarginUsd, ...) and Currency (currentRate) entities. Supports arithmetic (plus, minus, times, divide, parens), comparison (gt, gte, lt, lte, eq, neq), and top-level AND/OR/XOR logic. Validates the expression offline (subject syntax, function catalog, paren balance, flat-logic rule) before submission. Use when the user says "alert", "notify", "notify me", "watch for", "wake me when", "tell me when", "heads up when", "ping me if", "set a trigger", or "let me know if". Also use when the user asks about a sibling skill's proposed alert expression. position-watchdog, event-watch, and pretrade-risk also submit their proposed expressions through this skill.
compatibility: This skill requires the NinjaTrader MCP server, connected through a client with MCP support.
---

# alerts-composer

## Purpose

Turn "alert me when X" into a valid alert-DSL expression. Validate the expression offline, check for duplicates, and submit it via `create_alert.expression`.

The DSL has:
- **37 numeric functions** across 4 entity types (Account 14, Contract 9, Position 13, Currency 1) — see `references/dsl-functions.md`.
- Arithmetic `+ - * /` with parens for grouping.
- Single comparison per compare-expression.
- Flat `AND` / `OR` / `XOR` chain at the top level — **no parenthesized sub-expressions in logic**.

See `references/dsl-grammar.md` for the full grammar.

## Environment routing

Demo (simulation) and live are two separate MCP servers. Account names are unique to one server. Once a workflow resolves an account on a server, every downstream call must go through that same server. This includes `my_portfolio`, `market_snapshot`, `place_order`, `create_alert`, history tools, etc. Cross-routing fails or hits the wrong environment.

## MCP tools used

Tool names below are bare. The NinjaTrader MCP server provides them. Your client adds its own prefix. See `AGENTS.md` at the repo root.

- `search_contracts` — resolves a bare code to a symbol (the DSL subject must be an exact contract symbol).
- `my_portfolio` — gives account name context. Prune with `fields=["account.name"]` for just the account name.
- `list_alerts` — checks for duplicates.
- `create_alert` with the `expression` param — the submit path (Mode B).
- `market_snapshot` — gives price context when you translate a "near current price" intent into an absolute level. Prune with `fields=["snapshots[].symbol","snapshots[].lastPrice","snapshots[].tickSize"]`.

## Workflow

### 1. Classify the intent

Use `references/pattern-library.md` as a routing table. It has 18 patterns that cover most cases: price cross, breakeven, P&L floor, margin, session break, divergence, FX, and more. Pick the closest template.

If the user's intent needs a multi-bar indicator (ATR, RSI, MA, or similar), the DSL cannot express it. Snapshot the value now and emit a fixed-price bracket (e.g., `entry ± 2×ATR_now`). Tell the user this explicitly.

### 2. Resolve the symbol

The subject must be an **exact** contract symbol: `ESU6`, not `ES`. If the user gave a bare code, resolve it first:

```
search_contracts(text=<code>)
```

Use the `symbol` field. `contract-intel` also does this end-to-end.

### 3. Compose the expression

Paste a template from `references/pattern-library.md`. Substitute the symbol, account, and numeric thresholds. Or build the expression from the grammar in `references/dsl-grammar.md`.

### 4. Validate offline

```bash
echo '<expression>' | python3 scripts/validate.py
```

Checks:
- Balanced parens
- Comparison operator present
- No quoted subjects
- Flat-logic rule
- Function names in the 37-function catalog
- Subject regex `[\$@]?[\w\s\-\+/|]+`

Output: `{"valid": true|false, "errors": [...], "warnings": [...], "functions_used": [...], "subjects_used": [...]}`.

If the expression is invalid, fix it and validate it again. **Always validate before you submit.** A typo still passes `create_alert`, because the server parser accepts it. But the alert never fires, because the function or subject does not resolve.

### 5. Check for duplicates — required in every mode, including drafts

```
list_alerts(status="Active")
```

This duplicate check belongs to alert composition, not to alert submission. When the user asks for a draft or a validate-only check ("don't submit it"), still run `list_alerts`. Report the duplicate status in the answer. A validated draft that collides with an active alert is a footgun: the user may submit it blind later. Never present a draft or submit an alert without this check.

`list_alerts` does not return the raw expression string. Compare the new alert against each existing alert's `symbol`, `trigger`, and `price` fields instead. If an existing alert matches on all three, ask the user for a decision. Offer to replace the alert or keep both. Never auto-dismiss the duplicate.

**Draft-only mode stops here.** Report the expression, the validation result, and the duplicate status. Do not call `create_alert`.

### 6. Submit — wait for user approval first

Show the validated expression and the exact payload below. Then stop and wait for the user's approval. Never call `create_alert` from this skill before the user approves that payload. After the user approves it, submit the payload:

```
create_alert(
  expression="<validated>",
  message="<optional human-readable>",
  validUntil=<optional ISO timestamp>,
  triggerLimits=<optional int>
)
```

Use `message` for the plain-English translation, so the user sees it in the alerts list. Use `validUntil` for time-of-day conditions, because the DSL cannot express them.

### 7. Echo back the plain-English translation

> "Created alert 4321: `lastPrice(ESU6) > 7200 AND posOpenPLUsd(ESU6) < -300`
> — fires when ES prints above 7200 *and* your ES position is losing
> more than $300. Valid until 16:00 ET."

## Integration — alert-proposal handoff from sibling skills

Three skills propose alert expressions:

- **`pretrade-risk`** — after the user approves a bracket, it proposes a breakeven-trip or target-approach alert. See `../pretrade-risk/references/risk-rules.md` § alert-proposal hook.
- **`event-watch`** — proposes a reaction-window bracket around a known volatility event.
- **`position-watchdog`** — proposes stop-proximity or P&L-floor guards on live positions.

When those skills emit an expression string, the user typically says "submit it" or "go ahead." Run the expression through `validate.py` first. Then submit the expression through `create_alert` as Mode B. **Trust but verify.** Never skip validation just because another skill produced the expression.

## Output idioms

- Happy path: "I'll submit `posOpenPLUsd(ESU6) < -300` — fires when
  the open loss on your ES position exceeds $300. Sound right?"
- Draft-only: "Draft validated: `lastPrice(ESU6) > 7600` — fires when
  ESU6 prints above 7600. No duplicate among your 3 active alerts.
  Not submitted — say the word and I'll create it."
- Invalid intent (indicator): "The alert DSL has no RSI function. I
  can snapshot RSI now and emit a fixed-price alert, or you could use
  a session-break alert (`lastPrice(ESU6) > highPrice(ESU6)`)."
- Invalid intent (cross-account): "Aggregate P&L across sub-accounts
  can't be expressed in a single alert. Options: one alert per account,
  or raise/lower `dailyLossLimit` on each upstream via
  `update_risk_settings`."
- Duplicate: "You already have alert 4218 with this expression. Keep
  both, replace, or cancel the new one?"

## Disambiguation

- **vs direct `create_alert` Mode A** (a simple price cross: `symbol + trigger + price`): for a literal "alert me when ES crosses 7200 up", Mode A is simpler. The server composes the DSL internally in that mode. Use this skill instead when the intent needs any arithmetic, logic, or any non-price function.
- **vs sibling-skill proposals**: those skills own the intent-to-expression translation for their own domain (risk, events, watchdog). This skill owns DSL composition, validation, and submission for any ad-hoc intent that does not come from another skill.

## Known gotchas

**Subject has NO quotes.** Despite what the `create_alert` MCP docstring shows, the parser rejects `lastPrice("ESU6")`. Write `lastPrice(ESU6)` instead.

**No parens around logic.** The parser rejects `(A > B) OR (C < D)`. Write `A > B OR C < D` instead.

## Explicit non-goals

- **No alert cancellation logic.** `dismiss_alert` is a separate MCP tool. This skill composes + submits only.
- **No modification.** There is no `modify_alert` — dismiss and recreate.
- **No timer / scheduling.** The DSL has no time arithmetic. Use `validUntil` at submission, or gate upstream with a human workflow.
- **No indicator / historical-bar math.** The catalog is spot-quote and current-state only. Snapshot a value now and emit a fixed-price bracket when the user wants an indicator-driven alert.
- **Never invent functions.** Stick to the 37 in `dsl-functions.md`.

## Resource layout

- `scripts/validate.py` — offline DSL lint. Stdin or `--expression`. Returns JSON with errors/warnings/functions/subjects. Exit code 0 on valid, 1 on errors.
- `references/dsl-grammar.md` — full grammar (subject regex, operators, precedence, JSON shorthand, runtime statuses, known gotchas). Load it when you build an expression from scratch, not from a pattern.
- `references/dsl-functions.md` — the canonical 37-function catalog. It groups functions by entity (Account/Contract/Position/Currency) and includes an intent-to-function routing table. Load it when you pick a function.
- `references/pattern-library.md` — 18 ready-to-paste patterns (price cross, breakeven, P&L floor, session break, divergence, spread, FX, reaction window, position flip, etc.). Load it when you classify the intent or compose the expression.
