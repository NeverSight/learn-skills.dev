---
name: lista
description: Lista Lending assistant — position report, market overview, yield scan, liquidation risk check, daily digest, and loop strategy on BSC and Ethereum
---

# Lista Lending

Your Lista Lending (Moolah) assistant on BSC and Ethereum. Choose a function below.

## Skill Routing Boundary (Required)

Use this skill for report-style, read-only analysis.

- Use `lista` for position report, market overview, vault yield scan, risk check, daily digest, and loop strategy.
- Do not use `lista` for lending execution flows (`deposit`, `withdraw`, `supply`, `borrow`, `repay`) or operation target selection.
- For lending-only actionable views (`holdings`, `vaults`, `markets` for follow-up operations), route to `lista-lending`.
- For wallet connection/signing/session troubleshooting, route to `lista-wallet-connect`.

Conflict resolution for similar intents:

- `check my positions` without operation intent: stay in `lista` and generate the standard report.
- `check my lending positions` or `show my vaults/markets` with likely operation follow-up: route to `lista-lending`.
- `market rates` or `vault APY` narrative overview: `lista`.
- `market list` or `vault list` for selection/filtering/execution: `lista-lending`.

## Data sources — silent fallback

Try each source in order. Move to the next silently on any error (connection error, tool not found, command not recognized). NEVER ask the user to install, configure, or set up anything.

1. MCP tools (preferred): `lista_get_position`, `lista_get_borrow_markets`, `lista_get_lending_vaults`, `lista_get_oracle_price`, `lista_get_staking_info`, `lista_get_dashboard`, `lista_get_rewards`
2. moolah.js (Node.js, no install needed): `node skills/lista/scripts/moolah.js [--chain bsc|eth] <command>`
3. REST API (curl): `curl -s "https://api.lista.org/api/moolah/<endpoint>"`

Each reference file lists the exact fallback commands per data step.

> Performance tip (optional): For the best experience, connect the Lista MCP server. This is NOT required — the skill works without it.
> - Claude Code: `claude mcp add lista --transport sse https://mcp.lista.org/mcp`
> - OpenClaw: `{ "mcpServers": { "lista": { "transport": "streamable-http", "url": "https://mcp.lista.org/mcp" } } }`
> - Other MCP clients: `{ "mcpServers": { "lista": { "url": "https://mcp.lista.org/mcp" } } }`

---

## Step 0 — Language

### Load saved language

```bash
cat ~/.lista/language.txt 2>/dev/null
```

If the file exists and contains a valid choice (en, zh-CN, zh-TW, or a custom language name), use it silently — do NOT ask again.

### Ask if no saved language

Do NOT run any commands until the user has answered this question:

> Which language should I use for the output?
> 請問輸出以哪種語言生成？
>   1) English
>   2) 简体中文
>   3) 繁體中文
>   4) Other (specify)

Save the choice:

```bash
mkdir -p ~/.lista && echo "<CHOICE>" > ~/.lista/language.txt
```

Where `<CHOICE>` is one of: `en`, `zh-CN`, `zh-TW`, or the user's custom language name.

### Change language

When the user says "change language" / "換語言" / "换语言", ask again and overwrite `~/.lista/language.txt`.

**Language handling rules:**
- **en / English** — use the English template exactly.
- **zh-CN / 简体中文** — use the 繁體中文 template, then convert all Traditional Chinese characters to Simplified Chinese. Do NOT alter numbers, symbols, separators, or field layout.
- **zh-TW / 繁體中文** — use the 繁體中文 template exactly.
- **Other** — translate all label text into the user's language. Use natural, idiomatic phrasing (not word-for-word). Keep every separator line (━━━, ─────, - - - - -), number format, spacing, and indentation identical to the English template. Do NOT add bullet points, reformat rows, or change the structural layout.

Use the selected language for all output below.

---

## FORMAT ENFORCEMENT — applies to every report below

**You MUST follow these rules strictly for ALL output. No exceptions.**

1. **Plain text only.** No markdown bold (`**`), italics (`_`), headers (`#`), or links. Output is intended for Telegram/Discord paste.
2. **Copy template structure character-for-character.** Every separator line (━━━, ─────, - - - - -), every field label, every indentation level must match the template exactly.
3. **Do NOT rename, reorder, add, or omit fields** unless the template explicitly says a section is conditional (e.g. "if risk alerts exist").
4. **＄ in templates = $ in output.** Templates use fullwidth ＄ for escaping; replace with normal $ when generating.
5. **Round all numbers to 2 decimal places.** Token amounts (e.g. `4933.97 slisBNB`), USD values (e.g. `~$3.19M`), percentages (e.g. `71.2%`), and health factor (e.g. `1.21`) all display at most 2 decimal places. Do NOT output raw MCP precision (e.g. `4933.97414194585166222` is wrong; `4933.97` is correct).
6. **Do NOT add commentary, disclaimers, or extra text** outside the template structure. The report IS the output.
7. **Data source label (`<DATA_SOURCE>`):** Use `Lista MCP` if all data was fetched via `lista_*` MCP tools; use `Lista API` if all data was fetched via moolah.js or curl (both hit api.lista.org). If multiple sources were used, combine labels (e.g. `Lista MCP + API`).
8. **Network label (`<NETWORK>`):** Resolve from inferred chain:
   - `"bsc"` → EN: `BSC Mainnet` / ZH: `BSC 主網`
   - `"ethereum"` → EN: `Ethereum Mainnet` / ZH: `ETH 主網`
   - `"bsc,ethereum"` → EN: `BSC + Ethereum` / ZH: `BSC + ETH`
9. **No free summaries.** Do NOT paraphrase, summarise, or add analyst commentary. The template output is the complete and only permitted response.
10. **No preamble or trailing remarks.** Do NOT write "Here is your report", "Sure", "Let me check", "Done", or any text before or after the report block.
11. **Line-per-field layout is mandatory.** Each data point appears on its own labeled line. Data groups are wrapped with `- - - - -` at start and end, separated by 2 blank lines. Do NOT use markdown tables (`| col | col |`), bullet points, or compress multiple fields onto one line.
12. **No invented sections.** Do NOT add overview blocks, summary paragraphs, or extra headings that are not present in the reference template. Every section heading and block in the output must correspond to a section in the template.

---

## Step 1 — Report type

Ask the user (or infer from their request):

> Which report would you like?
> 你需要哪種報告？
>   1) Position Report — collateral, debt, health factor, LTV, liquidation price
>   2) Market Lending Rates — Supply APY, Borrow APY, liquidity per market
>   3) Vault Yield — APY, TVL, underlying assets per vault
>   4) Risk Check — liquidation risk alerts with thresholds
>   5) Daily Digest — positions + yield + market snapshot
>   6) Loop Strategy — leverage loop simulation, net APY, liquidation risk

If the user's original message already implies a type (e.g. "check my positions" → 1, "USDT borrow rate" → 2, "vault APY" → 3, "am I safe" → 4, "daily report" → 5, "loop slisBNB" → 6), skip the question and proceed directly.

---

## Step 2 — Wallet address (for types 1, 4, 5)

Reports 1, 4, 5 require a wallet address. Reports 2, 3, 6 do not — skip this step for them.

For report type 6 (Loop Strategy), ask the user for collateral asset, borrow asset, and initial amount if not already provided.

### Load saved address

```bash
cat ~/.lista/wallet.txt 2>/dev/null
```

If the file exists and contains a valid address, use it. Inform the user:

> **EN:** Using saved wallet: 0xAbCd...5678. Say "change address" to update.
> **中文：** 使用已儲存的錢包：0xAbCd...5678。輸入「換個地址」可更新。

### Ask if no saved address

> **EN:** What is your wallet address? I will save it locally so you don't need to enter it again.
> **中文：** 請問你的錢包地址是什麼？我會儲存到本地，下次不用再輸入。

### Save address

```bash
mkdir -p ~/.lista && echo "<ADDRESS>" > ~/.lista/wallet.txt
```

### Change address

When the user says "change address" / "换个地址" / "換個地址", ask for the new address and save it:

```bash
echo "<NEW_ADDRESS>" > ~/.lista/wallet.txt
```

### Multiple addresses

The user may provide multiple addresses (comma/space/line separated). Save all to the file (one per line) and process each.

---

## Step 2.5 — Chain inference

Resolve the active chain from the user's message before dispatching any report. Do NOT save this to disk — resolve fresh per request.

| User says | Chain |
|---|---|
| "ethereum", "eth", "on ETH", "在以太坊", "ETH positions" | `"ethereum"` |
| "bsc", "bnb", "binance" | `"bsc"` |
| "both chains", "兩條鏈", "bsc and ethereum" | `"bsc,ethereum"` |
| No keyword / ambiguous | `"bsc"` (default) |

Pass the resolved chain to all MCP tool calls in the selected report reference.

---

## Step 3 — Dispatch

**MANDATORY GATE — must complete before any data fetch or output:**

1. Call the Read tool on **every** reference file listed in the table below for the selected report type.
2. Do NOT generate any output from memory or prior context. If you have not read the file in this session using the Read tool, read it now.
3. Follow the fallback chain in "Data sources" above. Move to the next source silently on any error. Never ask the user to configure a data source.

| Report type | Read these files |
|---|---|
| 1 — Position Report | `references/domain.md`, `references/position.md` |
| 2 — Market Lending Rates | `references/market.md` |
| 3 — Vault Yield | `references/yield.md` |
| 4 — Risk Check | `references/domain.md`, `references/risk.md` |
| 5 — Daily Digest | `references/domain.md`, `references/digest.md` |
| 6 — Loop Strategy | `references/domain.md`, `references/loop.md` |

Follow the instructions in the referenced files to fetch data, compute metrics, and generate the report using the selected language.

---

## Step 4 — Pre-output self-check (MANDATORY)

Before writing the first character of report output, verify every item below. If any check fails, fix it first.

- [ ] I called the Read tool on every reference file listed in Step 3 for this report type.
- [ ] I fetched live data via at least one source (MCP, moolah.js, or curl).
- [ ] I am using the correct language template (EN or 繁體中文 based on Step 0).
- [ ] My first line of output is character-for-character identical to the first line of the reference template (e.g. `Lista Lending — Position Report` or `Lista Lending — 持倉報告`). If it is not, STOP and restart output.
- [ ] Every data row uses the line-per-field format — no markdown tables (`| col |`), bullet points (•), or prose substitutions. Data groups are wrapped with `- - - - -`.
- [ ] Every separator line (━━━, ─────, - - - - -) is copied character-for-character.
- [ ] No field has been renamed, reordered, added, or omitted unless the template marks it conditional.
- [ ] No overview block, summary paragraph, or section heading exists in my output that is not in the reference template.
- [ ] No commentary, free summary, or disclaimer appears anywhere in the output.
- [ ] `<DATA_SOURCE>` is replaced with the correct label (`Lista MCP` / `Lista API` / `Lista MCP + API`).
- [ ] `<NETWORK>` is replaced with the correct network label for the inferred chain.
- [ ] No markdown bold (`**`), italics (`_`), headers (`#`), or links appear anywhere in the output.
