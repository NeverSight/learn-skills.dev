---
name: gate-info-addresstracker
version: "2026.3.12-1"
updated: "2026-03-12"
description: "Address tracker and analysis. Use this skill whenever the user provides an on-chain address or asks to track or query an address. Trigger phrases include: track this address, who owns this address, fund flow, check address. MCP tools: info_onchain_get_address_info, info_onchain_get_address_transactions, info_onchain_trace_fund_flow."
---

# gate-info-addresstracker

> The on-chain detective Skill. The user inputs an on-chain address; the system first calls the address info Tool to get the profile, then based on user intent depth (simple query vs. fund tracing) decides whether to additionally call transaction history and fund flow tracing Tools.

**Trigger Scenarios**: User provides an on-chain address (0x... / bc1... / T... format) or explicitly expresses intent to track/query an address.

---

## Routing Rules

| User Intent | Keywords/Pattern | Action |
|-------------|-----------------|--------|
| Query address info | "who owns this address" "check 0x..." | Execute this Skill (Basic Mode) |
| Track fund flow | "track" "fund flow" "where did this money go" | Execute this Skill (Deep Tracking Mode) |
| Token on-chain analysis | "ETH chip analysis" "what are smart money buying" | Route to `gate-info-tokenonchain` |
| Address risk check | "is this address safe" "is this a blacklisted address" | Route to `gate-info-riskcheck` |
| Single transaction query | "what is this transaction" "decode this tx" | Call `info_onchain_get_transaction` directly |
| Entity/institution tracking | "Jump Trading holdings" "this institution's address" | Route to `gate-info-whaletracker` |

---

## Execution Workflow

### Step 1: Intent Recognition & Parameter Extraction

Extract from user input:
- `address`: On-chain address (auto-detect format)
- `chain` (optional): Chain type (ETH/BSC/TRX/BTC, etc. — can be auto-inferred from address format)
- `intent_depth`: User intent depth
  - `basic` — just asking "who is this" / "how much do they hold"
  - `deep` — requesting "track funds" / "show transactions" / "where did the money go"

**Automatic Address Format Detection**:

| Address Prefix | Inferred Chain |
|---------------|----------------|
| `0x` | Ethereum (default; could also be BSC/Polygon/Arbitrum or other EVM chains) |
| `bc1` / `1` / `3` | Bitcoin |
| `T` | Tron |
| Other | Prompt user to specify the chain |

### Step 2: Phase 1 — Address Profile (Required)

| Step | MCP Tool | Parameters | Retrieved Data |
|------|----------|------------|----------------|
| 1 | `info_onchain_get_address_info` | `address={address}, chain={chain}, scope="with_defi"` | Address profile: balance, labels, risk score, DeFi positions, PnL |

### Step 3: Decision Branch

```
get_address_info response
    │
    ├── User only wants a simple query (intent_depth = basic)
    │   └── → Output address profile report directly (skip to Step 5)
    │
    └── User requests deep tracking (intent_depth = deep)
        └── → Proceed to Step 4 parallel calls
```

**Conditions for automatic upgrade to deep mode**:
- Address has known labels (e.g., exchange, hacker, whale) → likely worth investigating
- Address balance > $1M
- Address has risk flags

### Step 4: Phase 2 — Deep Tracking (Conditionally Triggered)

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 2a | `info_onchain_get_address_transactions` | `address={address}, chain={chain}, min_value_usd=10000, limit=20` | Large transactions (> $10k) | Yes |
| 2b | `info_onchain_trace_fund_flow` | `start_address={address}, chain={chain}, depth=3, min_value_usd=100000` | Fund flow tracing (3-level depth, > $100k) | Yes |

> Both Tools called in parallel. `min_value_usd` thresholds are adaptively adjusted based on address size.

**Adaptive Threshold Logic**:

| Address Total Balance | `info_onchain_get_address_transactions` min_value | `info_onchain_trace_fund_flow` min_value |
|----------------------|--------------------------------------------------|-----------------------------------------|
| < $100K | $1,000 | $10,000 |
| $100K – $1M | $10,000 | $100,000 |
| $1M – $100M | $100,000 | $1,000,000 |
| > $100M | $1,000,000 | $10,000,000 |

### Step 5: LLM Aggregation

---

## Report Template

### Basic Mode

```markdown
## Address Analysis Report

> Address: `{address}`
> Chain: {chain}
> Query time: {timestamp}

### 1. Address Profile

| Metric | Value |
|--------|-------|
| Address Label | {label} (e.g., Exchange Hot Wallet / Whale / Unknown / Hacker-linked) |
| Risk Score | {risk_score}/100 ({Low Risk/Medium Risk/High Risk}) |
| First Transaction | {first_tx_time} |
| Total Transactions | {tx_count} |
| Current Balance | ${total_balance_usd} |

### 2. Asset Holdings

| Token | Amount | Value (USD) | Share |
|-------|--------|-------------|-------|
| {token_1} | {amount} | ${value} | {pct}% |
| {token_2} | ... | ... | ... |
| ... | ... | ... | ... |

**Holding Characteristics**: {LLM analyzes the holding structure, e.g., "Highly concentrated in ETH", "Diversified across multiple DeFi tokens", "Possible market maker"}

### 3. DeFi Positions (if available)

| Protocol | Type | Amount | Status |
|----------|------|--------|--------|
| {protocol} | {Lending/LP/Staking} | ${value} | {Healthy/Near Liquidation} |
| ... | ... | ... | ... |

### 4. PnL Summary (if available)

| Metric | Value |
|--------|-------|
| Realized PnL | ${realized_pnl} |
| Unrealized PnL | ${unrealized_pnl} |
| Win Rate | {win_rate}% |
```

### Deep Tracking Mode (appended to Basic Mode)

```markdown
### 5. Large Transaction History

> Filter: Amount > ${min_value_usd} | Most recent {count} transactions

| Time | Type | Amount | Counterparty | Counterparty Label |
|------|------|--------|--------------|-------------------|
| {time} | {In/Out/Contract Interaction} | ${value} | `{counterparty}` | {label/unknown} |
| ... | ... | ... | ... | ... |

**Transaction Pattern Analysis**:
{LLM analyzes transaction records and identifies patterns:}
- Frequent interactions with an exchange → likely depositing/withdrawing
- Large one-way outflows → possibly liquidating
- Interacting with many new addresses → possibly dispersing funds
- Regular fixed-amount transfers → possibly payroll/OTC

### 6. Fund Flow Tracing

> Trace depth: {depth} levels | Minimum amount: ${min_value_usd}

```
{address} (origin)
  ├── ${amount} → {addr_1} ({label_1})
  │     ├── ${amount} → {addr_1a} ({label})
  │     └── ${amount} → {addr_1b} ({label})
  ├── ${amount} → {addr_2} ({label_2})
  │     └── ${amount} → {addr_2a} ({label})
  └── ${amount} → {addr_3} ({label_3})
```

**Fund Flow Analysis**:
{LLM analysis based on tracing results:}
- Ultimate destination of funds (exchange? mixer? DeFi protocol?)
- Any suspicious patterns (split transfers, circular transfers, obfuscation paths)
- Associated known entities

### ⚠️ Risk Warnings

{If the address has risk flags, prominently display:}
- ⚠️ This address is flagged as: {risk_label}
- ⚠️ Associated addresses involved in: {risk_detail}
```

---

## Decision Logic

| Condition | Assessment |
|-----------|------------|
| risk_score > 70 | High-risk address — warn user to exercise caution |
| risk_score 40-70 | Medium risk — note some risk factors present |
| risk_score < 40 | Low risk |
| Holding concentration > 80% in a single token | Flag "Highly concentrated holding" |
| DeFi lending health factor < 1.2 | Near liquidation |
| Large outflow in past 24h > 50% of total balance | Flag "Recent large outflow" |
| Fund flow includes mixer addresses | Flag "Mixer involvement — high risk" |
| Fund flow includes OFAC-sanctioned addresses | Flag "Associated with sanctioned address" |
| trace_fund_flow returns empty | Possibly a new address or no large-enough transactions — handle normally |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| Invalid address format | Prompt user to check the format; provide correct format examples |
| Cannot identify chain | Prompt user to specify the chain ("Which chain is this address on? ETH/BSC/TRX/BTC...") |
| `info_onchain_get_address_info` returns empty | Address may be new or have no on-chain activity; inform the user |
| `info_onchain_trace_fund_flow` unavailable (P1 phase) | Inform user "Fund tracing is still under development"; show transaction history only |
| `info_onchain_get_address_transactions` timeout | Reduce limit and retry, or show address profile only |
| All Tools fail | Return error message; suggest the user try again later |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "Is this address safe?" | `gate-info-riskcheck` |
| "On-chain data for this token" | `gate-info-tokenonchain` |
| "Which institution owns this address?" | `gate-info-whaletracker` |
| "Analyze XX coin for me" | `gate-info-coinanalysis` |
| "Why was there a large outflow?" | `gate-news-eventexplain` |

---

## Safety Rules

1. **Privacy protection**: Do not link on-chain addresses to specific natural persons (unless publicly labeled as institutional addresses)
2. **Clear risk warnings**: High-risk addresses must have prominent, unmistakable risk labels with reasons
3. **No definitive characterization**: Do not use terms like "criminal address" or "dirty money" — use objective language like "flagged as high risk" or "associated with suspicious activity"
4. **Data source transparency**: Label data sources (BlockInfo / Nansen / Arkham) must be attributed
5. **Flag missing data**: Fund tracing rolls out in phases; when unavailable, explicitly state it
6. **Do not encourage stalking**: If a user attempts to track many personal addresses for harassment purposes, prompt responsible use
