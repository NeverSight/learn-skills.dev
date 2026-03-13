---
name: krx-cli
description: Query KRX (Korea Exchange) market data via CLI. This skill should be used when the user asks about Korean stock market data including stock prices, indices, ETF/ETN/ELW, bonds, derivatives, commodities, or ESG data. Triggers on tasks involving 주가, 시세, 종가, 코스피, 코스닥, KOSPI, KOSDAQ, KRX, 지수, ETF, 채권, 선물, 옵션, 금시세, 배출권, ESG. Do NOT web search — use the `krx` CLI via Bash tool instead.
required_env:
  - KRX_API_KEY
install: npm install -g krx-cli
binary: krx
metadata:
  author: kyo504
  version: "1.6.0"
invariants:
  - Always use YYYYMMDD format for --date (e.g., 20260310)
  - Data is T-1 (previous trading day), available from 2010 onwards
  - Default output is JSON to stdout, errors go to stderr
  - Rate limit is 10,000 API calls per day
  - Each API category requires separate approval from KRX
  - All response field values are strings (including numbers)
---

# krx-cli

Agent-native CLI for querying KRX (Korea Exchange) Open API data. Use the `krx` CLI via Bash tool — do NOT web search for Korean market data.

## When to Apply

Use this skill when the user asks about:

- 주식 시세/가격 (삼성전자 주가, 종목별 종가 등)
- 지수 조회 (코스피, 코스닥, KRX 지수 등)
- ETF, ETN, ELW 시세
- 채권 시세 (국채, 일반채권, 소액채권)
- 파생상품 (선물, 옵션)
- 일반상품 (금, 석유, 배출권)
- ESG 지수/채권 정보

## Setup

```bash
# Install
npm install -g krx-cli

# Set API key (get from https://openapi.krx.co.kr/)
krx auth set <your-api-key>

# Check which services are approved
krx auth status
```

## Commands

### Authentication

```bash
krx auth set <api-key>       # Save API key
krx auth status               # Check all service approvals (JSON)
krx auth check <category>     # Check specific category: index, stock, etp, bond, derivative, commodity, esg
```

### Index (지수)

```bash
krx index list --date 20260310 --market kospi     # KOSPI index
krx index list --date 20260310 --market kosdaq     # KOSDAQ index
krx index list --date 20260310 --market krx        # KRX index
krx index list --date 20260310 --market bond       # Bond index
krx index list --date 20260310 --market derivative # Derivative index
```

### Stock (주식)

```bash
krx stock list --date 20260310 --market kospi   # KOSPI stocks
krx stock list --date 20260310 --market kosdaq   # KOSDAQ stocks
krx stock list --date 20260310 --market konex    # KONEX stocks
krx stock info --market kospi                     # Stock base info
```

### ETP (ETF/ETN/ELW)

```bash
krx etp list --date 20260310 --type etf   # ETF
krx etp list --date 20260310 --type etn   # ETN
krx etp list --date 20260310 --type elw   # ELW
```

### Bond (채권)

```bash
krx bond list --date 20260310 --market kts       # Government bonds
krx bond list --date 20260310 --market general    # General bonds
krx bond list --date 20260310 --market small      # Small bonds
```

### Derivative (파생상품)

```bash
krx derivative list --date 20260310 --type futures          # Futures
krx derivative list --date 20260310 --type options           # Options
krx derivative list --date 20260310 --type futures-kospi     # KOSPI stock futures
krx derivative list --date 20260310 --type futures-kosdaq    # KOSDAQ stock futures
krx derivative list --date 20260310 --type options-kospi     # KOSPI stock options
krx derivative list --date 20260310 --type options-kosdaq    # KOSDAQ stock options
```

### Commodity (일반상품)

```bash
krx commodity list --date 20260310 --type gold       # Gold
krx commodity list --date 20260310 --type oil         # Oil
krx commodity list --date 20260310 --type emission    # Emission trading
```

### ESG

```bash
krx esg list --date 20260310 --type index       # ESG index
krx esg list --date 20260310 --type etp          # ESG ETP
krx esg list --date 20260310 --type sri-bond     # SRI bonds
```

### Stock Search (종목 검색)

```bash
krx stock search 삼성전자     # Search by name (KOSPI + KOSDAQ)
krx stock search SK           # Partial match
```

### Market Summary (시장 요약)

```bash
krx market summary                    # Today's market overview
krx market summary --date 20260310    # Specific date
```

Returns: KOSPI/KOSDAQ indices, top 5 gainers/losers, advancing/declining/unchanged counts, total volume/value.

### Watchlist (관심종목)

```bash
krx watchlist add 삼성전자          # Search and add to watchlist
krx watchlist remove 삼성전자       # Remove by exact name
krx watchlist remove KR7005930003   # Remove by ISU_CD
krx watchlist list                   # List all watchlist entries
krx watchlist show                   # Show prices for watchlist stocks
krx watchlist show --date 20260310  # Specific date
```

### Cache Management

```bash
krx cache status    # Show cache size, files, dates
krx cache clear     # Clear all cached data
```

### Version & Update

```bash
krx version    # Show current version and check for updates
krx update     # Update to the latest version (npm install -g krx-cli)
```

### MCP HTTP Server

```bash
krx serve                        # Start on http://127.0.0.1:3000/mcp
krx serve --port 8080            # Custom port
krx serve --host 0.0.0.0        # Bind to all interfaces (for ngrok)
```

### Schema (introspection)

```bash
krx schema --all              # All 31 endpoint schemas (JSON)
krx schema index.kospi_dd_trd # Specific endpoint schema
```

## Global Flags

```
--output, -o <format>    json (default) | table | ndjson | csv
--fields, -f <fields>    Filter output fields: --fields ISU_NM,TDD_CLSPRC,FLUC_RT
--code <isuCd>           Filter by stock code (ISU_CD)
--sort <field>           Sort results by field name
--asc                    Sort ascending (default: descending)
--limit <n>              Limit number of results
--from <date>            Start date for range query (YYYYMMDD)
--to <date>              End date for range query (YYYYMMDD)
--no-cache               Bypass cache and fetch fresh data
--filter <expression>    Filter results (e.g. "FLUC_RT > 5", "MKT_NM == KOSPI")
--dry-run                Show request details without calling API
--save <path>            Save output to file instead of stdout
--retries <n>            Max retries on network error (default: 3)
--verbose, -v            Verbose logging to stderr
```

## Exit Codes

```
0 = Success
1 = General error
2 = Usage error (bad arguments)
3 = No data found
4 = Auth failure (no/invalid API key)
5 = Rate limit exceeded (10,000/day)
6 = Service not approved (category not activated)
```

## Common Patterns

### Get KOSPI closing price for a specific date

```bash
krx index list --date 20260310 --market kospi --fields IDX_NM,CLSPRC_IDX,FLUC_RT
```

### Get Samsung Electronics stock price (by search)

```bash
krx stock search 삼성전자     # Find ISU_CD first
krx stock list --date 20260310 --market kospi --code KR7005930003
```

### Top 5 gainers

```bash
krx stock list --date 20260310 --market kospi --sort FLUC_RT --limit 5 --fields ISU_NM,TDD_CLSPRC,FLUC_RT
```

### Date range query (multi-day)

```bash
krx index list --market kospi --from 20260301 --to 20260310 --fields IDX_NM,BAS_DD,CLSPRC_IDX
```

### Quick market overview

```bash
krx market summary --date 20260310
```

### Track and monitor stocks

```bash
krx watchlist add 삼성전자           # Add to watchlist
krx watchlist show --date 20260310  # View prices for all watchlist stocks
```

### Check API availability before querying

```bash
krx auth status -o json
```

### Dry run to verify request

```bash
krx stock list --date 20260310 --market kospi --dry-run
```

## Response Fields

Use `krx schema <command>` to get full field definitions for any endpoint. All values are strings.

### Index (kospi/kosdaq/krx)

| Field         | Description         |
| ------------- | ------------------- |
| BAS_DD        | 기준일자 (YYYYMMDD) |
| IDX_CLSS      | 계열구분            |
| IDX_NM        | 지수명              |
| CLSPRC_IDX    | 종가                |
| CMPPREVDD_IDX | 전일대비            |
| FLUC_RT       | 등락률(%)           |
| OPNPRC_IDX    | 시가                |
| HGPRC_IDX     | 고가                |
| LWPRC_IDX     | 저가                |
| ACC_TRDVOL    | 거래량              |
| ACC_TRDVAL    | 거래대금            |
| MKTCAP        | 상장시가총액        |

### Stock (kospi/kosdaq/konex)

| Field         | Description         |
| ------------- | ------------------- |
| BAS_DD        | 기준일자 (YYYYMMDD) |
| ISU_CD        | 종목코드            |
| ISU_NM        | 종목명              |
| MKT_NM        | 시장구분            |
| SECT_TP_NM    | 소속부              |
| TDD_CLSPRC    | 종가                |
| CMPPREVDD_PRC | 전일대비            |
| FLUC_RT       | 등락률(%)           |
| TDD_OPNPRC    | 시가                |
| TDD_HGPRC     | 고가                |
| TDD_LWPRC     | 저가                |
| ACC_TRDVOL    | 거래량              |
| ACC_TRDVAL    | 거래대금            |
| MKTCAP        | 시가총액            |
| LIST_SHRS     | 상장주식수          |

### ETF

| Field          | Description     |
| -------------- | --------------- |
| ISU_CD         | 종목코드        |
| ISU_NM         | 종목명          |
| TDD_CLSPRC     | 종가            |
| FLUC_RT        | 등락률(%)       |
| NAV            | 순자산가치(NAV) |
| ACC_TRDVOL     | 거래량          |
| MKTCAP         | 시가총액        |
| IDX_IND_NM     | 기초지수명      |
| OBJ_STKPRC_IDX | 기초지수종가    |

### Futures

| Field          | Description    |
| -------------- | -------------- |
| PROD_NM        | 상품명         |
| ISU_NM         | 종목명         |
| TDD_CLSPRC     | 종가           |
| SPOT_PRC       | 현물가         |
| SETL_PRC       | 정산가         |
| ACC_OPNINT_QTY | 미결제약정수량 |

### Options

| Field          | Description      |
| -------------- | ---------------- |
| PROD_NM        | 상품명           |
| RGHT_TP_NM     | 권리유형 (콜/풋) |
| ISU_NM         | 종목명           |
| TDD_CLSPRC     | 종가             |
| IMP_VOLT       | 내재변동성       |
| ACC_OPNINT_QTY | 미결제약정수량   |

### Bond

| Field      | Description |
| ---------- | ----------- |
| ISU_NM     | 종목명      |
| CLSPRC     | 종가        |
| CLSPRC_YD  | 종가수익률  |
| ACC_TRDVOL | 거래량      |
| ACC_TRDVAL | 거래대금    |

### Commodity (gold/emission)

| Field      | Description |
| ---------- | ----------- |
| ISU_NM     | 종목명      |
| TDD_CLSPRC | 종가        |
| FLUC_RT    | 등락률(%)   |
| ACC_TRDVOL | 거래량      |

### Commodity (oil)

| Field      | Description  |
| ---------- | ------------ |
| OIL_NM     | 유종명       |
| WT_AVG_PRC | 가중평균가격 |
| ACC_TRDVOL | 거래량       |

### ESG Index

| Field       | Description |
| ----------- | ----------- |
| IDX_NM      | 지수명      |
| CLSPRC_IDX  | 종가        |
| PRV_DD_CMPR | 전일대비    |
| UPDN_RATE   | 등락률(%)   |

### Schema Introspection

For full response field definitions including all fields per endpoint:

```bash
krx schema index.kospi_dd_trd    # Shows params + responseFields
krx schema stock.stk_bydd_trd   # Stock endpoint fields
krx schema --all                  # All 31 endpoints
```

## MCP Resources

Read-only state data exposed as MCP Resources (for MCP clients):

| Resource               | Description                         |
| ---------------------- | ----------------------------------- |
| `krx://watchlist`      | Watchlist entries (JSON)            |
| `krx://rate-limit`     | Daily API call status (JSON)        |
| `krx://service-status` | Per-category approval status (JSON) |
