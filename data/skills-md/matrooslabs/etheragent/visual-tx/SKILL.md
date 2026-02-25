---
name: visual-tx
description: Analyze Ethereum transactions by fetching semantic trace data and generating a visual HTML explanation. Use this skill whenever the user provides a transaction hash, asks to analyze a transaction, wants to understand what happened in a tx, or asks about internal calls, token transfers, swaps, or any on-chain activity within a transaction. Trigger on phrases like "scan this tx", "what happened in this transaction", "trace this tx", "explain this transaction", or any 0x-prefixed 66-character hash.
allowed-tools: Bash(curl *), Bash(open *), Bash(xdg-open *), Bash(mkdir *), Read, Write
---

# Transaction Scanner

Fetch semantic trace data for an Ethereum transaction and generate a self-contained HTML page that visually explains every internal call, token movement, and DeFi action that occurred.

## Workflow

### 1. Fetch the trace tree

Fetch the trace tree JSON using the transaction hash from `$ARGUMENTS`:

```bash
curl -sf "https://mevscan.matroos.xyz/api/tree/<tx_hash>"
```

Save the JSON output to a temp file for processing. If the request fails (API unreachable, invalid hash), tell the user and stop.

Read `./references/tree-json.md` to understand the JSON schema — it documents every field, action kind, and type you'll encounter.

### 2. Parse and extract

Walk the JSON and extract these layers of information:

**Transaction header:**
- `tx_hash`, `block_number`, `tx_idx`
- `from` (sender EOA) and `to` (recipient contract)
- Gas details: `gas_used`, `effective_gas_price`, `priority_fee`, `coinbase_transfer`
- `timeboosted` flag (if true, note it)

**Trace tree traversal — build a flat action list:**
Recursively walk `trace_tree` → `children`. For each node with a non-null `action_kind`, extract:
- The `trace_address` (depth in the call stack)
- The `action_kind` (Swap, Transfer, EthTransfer, Mint, Burn, etc.)
- Key fields from the `action` object (addresses, tokens, amounts)
- Token amounts are already human-readable decimals — use them directly

**Collect unique addresses:**
Gather every address that appears as a `from`, `to`, `recipient`, `pool`, `liquidator`, `debtor`, `solver`, `settlement_contract`, or `receiver_contract`. These become the "actors" in the visualization. Shorten addresses to `0x1234...abcd` format for display, with full address in a tooltip or data attribute.

### 3. Generate the HTML

Read the reference template and patterns before generating:
- Read `./templates/reference.html` for all layout patterns (hero card, KPI row, trace tree, data table, Mermaid diagram, zoom controls)
- Read `./references/css-patterns.md` for theming, depth tiers, animations, and table styles
- Read `./references/libraries.md` if using Mermaid for the call tree diagram

The HTML page should have these sections only:

---

#### Section A: Transaction Overview (hero card)

A prominent card at the top showing:
- **Tx Hash** — full hash, monospace, truncated display with copy button
- **Block** — block number with link placeholder
- **From → To** — sender and recipient addresses (shortened, with full in tooltip)
- **Gas** — gas used, effective gas price (in Gwei), total cost (in ETH)
- **Status indicators** — timeboosted badge if applicable

Use the `section--hero` depth pattern. Monospace font for all hex values.

---

#### Section B: Action Summary (KPI row)

A row of small metric cards showing counts:
- Total actions found
- Swaps count
- Transfers count
- ETH transfers count
- Other action types (Mint, Burn, Liquidation, FlashLoan, etc.) — only show if present

Use the KPI card pattern from css-patterns.md. Each card gets an icon or colored dot matching the action type's color in the legend.

---

#### Section C: Call Trace Tree

This is the core visualization. Two approaches depending on complexity:

**For transactions with < 20 trace nodes:** Use a nested HTML tree with indentation.
- Each node is a card with left-border color coded by `action_kind`
- Indent children with `padding-left` proportional to `trace_address` depth
- Show `trace_idx` as a small index badge
- Show the action kind as a colored badge
- Show the key action details inline (e.g., "Swap 1.5 ETH → 3000 USDC on Uniswap V3")

**For transactions with >= 20 trace nodes:** Use a Mermaid `graph TD` diagram.
- Each node labeled with its action kind and a short summary
- Color-coded by action type using `classDef`
- Edges show the parent-child call relationship
- Include zoom controls (+/−/reset) — see the zoom pattern in css-patterns.md
- See the Mermaid section in `./templates/reference.html` for the setup pattern

---

#### Section D: Token Flow Table

A data table showing every token movement in the transaction:

| # | Action | From | To | Token | Amount | Protocol |
|---|--------|------|----|-------|--------|----------|

- **#** — sequential index
- **Action** — colored badge (Swap, Transfer, Mint, Burn, etc.)
- **From / To** — shortened addresses
- **Token** — symbol with small address tooltip
- **Amount** — human-readable decimal number
- **Protocol** — if the action has a `protocol` field

For **Swap** actions, show two rows or a combined row: token_in amount → token_out amount.

Use the data table patterns from `./templates/reference.html`:
- Sticky header
- Alternating row backgrounds
- Status-colored action badges
- Responsive horizontal scroll

---

#### Section E: Address Interaction Map (optional, for complex txs)

If the transaction involves 3 or more unique addresses, show a summary of interactions:
- List each address with a color-coded dot
- Show what actions it participated in and its role (sender, receiver, pool, etc.)
- Optionally use a Mermaid sequence diagram for the interaction flow

This section helps answer "who interacted with whom and how."

---

Do not add additional section not mentioned.

### 4. Style

**Palette:** Use a blockchain/crypto-themed palette. Dark-first aesthetic (the audience is developers and researchers). Suggested direction:

- Deep navy/charcoal background with cyan/teal accents for primary elements
- Color-code action types consistently throughout the page:
  - **Swap** — cyan/teal
  - **Transfer** — green
  - **EthTransfer** — blue-purple
  - **Mint** — emerald
  - **Burn** — amber/orange
  - **Liquidation** — red/rose
  - **FlashLoan** — purple
  - **Batch/Aggregator** — indigo
  - **Unclassified** — gray
  - **Revert** — red with strikethrough or muted treatment
- Support both light and dark themes via `prefers-color-scheme`

**Typography:** Pick a distinctive pairing. Suggestions:
- JetBrains Mono for hex values and technical data
- Space Grotesk or Outfit for headings and body text

**Animations:** Staggered fade-in for sections. Keep it subtle — this is a data-heavy tool page, not a marketing site.

### 5. Deliver

```bash
mkdir -p ~/.agent/diagrams
```

Write to `~/.agent/diagrams/tx-<short_hash>.html` where `<short_hash>` is the first 8 chars of the tx hash (after 0x).

Open in browser:
- macOS: `open ~/.agent/diagrams/tx-<short_hash>.html`
- Linux: `xdg-open ~/.agent/diagrams/tx-<short_hash>.html`

Tell the user the file path.

## Action Kind Reference

When rendering actions, use these display patterns. The **Mermaid Arrow** column specifies which arrow style to use for edges in the call trace tree diagram — this makes the diagram scannable at a glance because arrow shape encodes the action type.

| Action Kind | One-line Summary Format | Mermaid Arrow | Key Fields |
|---|---|---|---|
| Swap | `Swap {amount_in} {token_in} → {amount_out} {token_out}` | `<==>` (thick bidirectional — value flows both ways) | from, recipient, pool, protocol |
| SwapWithFee | `Swap {amount_in} {token_in} → {amount_out} {token_out} (fee: {fee_amount} {fee_token})` | `<==>` (thick bidirectional) | nested swap + fee |
| Transfer | `Transfer {amount} {token} from → to` | `-->` (solid arrow — one-way value movement) | from, to, token, amount |
| EthTransfer | `Send {value} ETH from → to` | `==>` (thick arrow — native ETH, visually heavier) | from, to, value (convert from hex wei) |
| Mint | `Mint {amounts} into {pool}` | `-.->` (dotted arrow — tokens created, no prior source) | protocol, pool, tokens[], amounts[] |
| Burn | `Burn {amounts} from {pool}` | `-.->` (dotted arrow — tokens destroyed, no destination) | protocol, pool, tokens[], amounts[] |
| Collect | `Collect {amounts} from {pool}` | `-->` (solid arrow — withdrawal from pool) | protocol, pool, tokens[], amounts[] |
| FlashLoan | `FlashLoan {amounts} via {protocol}` | `<-->` (bidirectional — borrow and repay in same tx) | pool, assets[], child_actions |
| Liquidation | `Liquidate {debtor}: repay {debt} for {collateral}` | `--x` (arrow with cross — forced closure) | liquidator, debtor, assets |
| Batch | `Batch settlement via {solver}` | `o--o` (circle endpoints — multi-party settlement) | user_swaps[], solver_swaps[] |
| Aggregator | `Aggregate via {protocol}` | `==>` (thick arrow — aggregated flow) | child_actions[] |
| Unclassified | `Call {from} → {to}` | `~~~` (wavy line — unknown action) | raw trace data |
| Revert | `Reverted call` | `--x` (arrow with cross — failed, use red style) | show in muted/red style |

## Quality Checks

Before delivering:
- All addresses display in shortened format with full value accessible
- Action badges are color-coded consistently
- Both light and dark themes work
- Table scrolls horizontally on narrow viewports
- Mermaid diagrams (if used) have zoom controls
- No console errors when opening the file
- The page tells a clear story: "Here's what this transaction did"
