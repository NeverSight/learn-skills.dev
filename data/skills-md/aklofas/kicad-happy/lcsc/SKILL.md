---
name: lcsc
description: Search LCSC Electronics for electronic components — find parts by LCSC number (Cxxxxx) or MPN, check stock/pricing, download datasheets, analyze specifications. Sister company to JLCPCB, same parts library. Sync and maintain a local datasheets directory for a KiCad project. No API key needed — uses the free jlcsearch community API. Use this skill when the user mentions LCSC, JLCPCB parts library, JLCPCB assembly parts, production sourcing, Cxxxxx part numbers, needs to find LCSC equivalents for parts, is preparing a BOM for JLCPCB assembly, or wants to download datasheets and LCSC is available. For package cross-reference tables and BOM workflow, see the `bom` skill.
---

# LCSC Electronics — Component Search, Datasheets & Ordering

LCSC is JLCPCB's sister company — they share the same parts library and `Cxxxxx` part numbers. Use LCSC for **production sourcing** (assembled boards from JLCPCB/PCBWay). DigiKey/Mouser are for prototyping. For BOM management and export workflows, see `bom`.

## Key Differences from DigiKey/Mouser

- **No API key needed** — jlcsearch community API is free and open
- **Lower prices** — especially for passives and Chinese-manufactured ICs
- **JLCPCB integration** — same LCSC part numbers used in JLCPCB assembly BOMs
- **Direct PDF downloads** — LCSC's CDN (wmsc.lcsc.com) serves datasheets without bot protection
- **Low MOQ** — many parts available in quantities as low as 1
- **Warehouses** — Shenzhen (JS), Zhuhai (ZH), Hong Kong (HK)
- **Website**: `https://www.lcsc.com`

## LCSC Part Numbers

Format: `Cxxxxx` (e.g., `C14663`). This is the universal identifier across both LCSC and JLCPCB. Use it for:
- Direct ordering on LCSC
- BOM matching in JLCPCB assembly (see `jlcpcb` skill)
- Cross-referencing between platforms

## jlcsearch API Reference

The jlcsearch community API is the recommended way to search LCSC. **No authentication required.**

**Base URL:** `https://jlcsearch.tscircuit.com`

### General Search

```
GET /api/search?q=<query>&limit=20&full=true
```

Parameters:
- `q` — search query (matches MPN, LCSC code, or description keywords)
- `package` — optional footprint filter (e.g., `0402`)
- `limit` — max results (default 100)
- `full` — set to `true` to include all fields (datasheet URL, specs, stock per warehouse)

### Category-Specific Search

```
GET /resistors/list.json?search=10k+0402
GET /capacitors/list.json?search=100nF+0402
GET /microcontrollers/list.json?search=STM32
GET /voltage_regulators/list.json?search=3.3V
```

### Response Format

Results are returned as `{"components": [...]}`. With `full=true`, each component has:

```json
{
  "lcsc": 14663,
  "mfr": "GRM155R71C104KA88D",
  "package": "0402",
  "description": "",
  "datasheet": "https://www.lcsc.com/datasheet/...",
  "stock": 2751535,
  "price": [{"qFrom": 1, "qTo": 9, "price": 0.0069}, ...],
  "basic": 0,
  "extra": {
    "number": "C71629",
    "mpn": "GRM155R71C104KA88D",
    "manufacturer": {"id": 4, "name": "Murata Electronics"},
    "package": "0402",
    "description": "16V 100nF X7R ±10% 0402 ...",
    "quantity": 2751535,
    "whs-js": 1234567,
    "whs-zh": 567890,
    "whs-hk": 0,
    "moq": 100,
    "order_multiple": 100,
    "packaging": "Tape & Reel (TR)",
    "packaging_num": 10000,
    "datasheet": {"pdf": "https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/...pdf"},
    "images": [{"96x96": "...", "224x224": "...", "900x900": "..."}],
    "rohs": true,
    "url": "https://www.lcsc.com/product-detail/...",
    "attributes": {
      "Capacitance": "100nF",
      "Voltage Rated": "16V",
      "Temperature Coefficient": "X7R",
      "Tolerance": "±10%"
    },
    "prices": [{"min_qty": 100, "max_qty": 499, "currency": "USD", "price": 0.0048}, ...]
  }
}
```

Key fields:
- `lcsc` — numeric LCSC ID (without "C" prefix)
- `extra.number` — full LCSC code with prefix (e.g., `C71629`)
- `extra.mpn` — manufacturer part number
- `extra.manufacturer.name` — manufacturer
- `extra.datasheet.pdf` — **direct PDF URL** (wmsc.lcsc.com CDN, downloads without auth)
- `extra.attributes` — parametric specs (capacitance, voltage, etc.)
- `extra.quantity` — total stock across all warehouses
- `extra.whs-js`, `extra.whs-zh`, `extra.whs-hk` — stock per warehouse
- `basic` — `1` if JLCPCB basic part (no setup fee), `0` if extended
- `extra.moq` — minimum order quantity
- `extra.order_multiple` — must order in multiples of this
- `extra.rohs` — RoHS compliance (boolean)

### Rate Limits

The jlcsearch API is community-run with no documented rate limits, but be respectful — use delays of 0.5s between calls.

## Datasheet Download & Sync

LCSC's CDN serves datasheet PDFs directly — no bot protection, no special headers needed. This makes LCSC a reliable datasheet source alongside DigiKey.

### Datasheet Directory Sync

Use `sync_datasheets_lcsc.py` to maintain a `datasheets/` directory alongside a KiCad project. Same workflow and `index.json` format as the DigiKey and Mouser skills. **No API key required.**

```bash
# Sync datasheets for a KiCad project
python3 <skill-path>/scripts/sync_datasheets_lcsc.py <file.kicad_sch>

# Preview what would be downloaded
python3 <skill-path>/scripts/sync_datasheets_lcsc.py <file.kicad_sch> --dry-run

# Retry previously failed downloads
python3 <skill-path>/scripts/sync_datasheets_lcsc.py <file.kicad_sch> --force

# Custom output directory
python3 <skill-path>/scripts/sync_datasheets_lcsc.py <file.kicad_sch> -o ./my-datasheets
```

The script:
- **Runs the kicad schematic analyzer** to extract components, MPNs, and LCSC codes
- **Accepts any identifier** — MPN, LCSC code, or other distributor PNs from KiCad symbol properties
- **Prefers LCSC code** for search (exact match) — falls back to MPN keyword search
- **Downloads from LCSC CDN** — direct PDF URLs, no bot protection
- **Writes `index.json` manifest** — same format as DigiKey/Mouser skills
- **Verifies PDF content** — checks MPN, manufacturer, and description keywords
- **Rate-limited** — 0.5s between API calls (configurable with `--delay`)
- **Saves progress incrementally** — safe to interrupt

### Single Datasheet Download

Use `fetch_datasheet_lcsc.py` for one-off downloads.

```bash
# Search by MPN
python3 <skill-path>/scripts/fetch_datasheet_lcsc.py --search "GRM155R71C104KA88D" -o datasheet.pdf

# Search by LCSC code
python3 <skill-path>/scripts/fetch_datasheet_lcsc.py --search "C14663" -o datasheet.pdf

# Direct URL download
python3 <skill-path>/scripts/fetch_datasheet_lcsc.py "https://wmsc.lcsc.com/..." -o datasheet.pdf

# JSON output
python3 <skill-path>/scripts/fetch_datasheet_lcsc.py --search "C14663" --json
```

The script:
- **OS-agnostic** — uses `requests` → `urllib` → `playwright` fallback chain (no wget/curl)
- **Validates PDF headers** — rejects HTML error pages
- **Falls back to alternative manufacturer sources** when LCSC URL fails
- **Exit codes**: 0 = success, 1 = download failed, 2 = search/API error
- **Dependencies**:
  - `pip install requests` (recommended; urllib fallback works fine for LCSC)
  - `pip install playwright && playwright install chromium` (optional; rarely needed for LCSC)

## LCSC Official API (Requires Approval)

**Base URL:** `https://ips.lcsc.com`. Requires API key + signature authentication. Contact `support@lcsc.com` for access. Rarely needed — jlcsearch covers most use cases.

## Web Search Fallback

If the jlcsearch API is unavailable, search LCSC via WebFetch:

```
https://www.lcsc.com/search?q=<query>
```

## Cross-Referencing & Missing Equivalents

LCSC part numbers are specific to the LCSC/JLCPCB ecosystem. Use the `extra.mpn` field to cross-reference on DigiKey/Mouser.

When an MPN has no exact LCSC match:
1. Search by key parameters (e.g., "100nF 0402 X7R 16V")
2. Look for pin-compatible alternatives from Chinese manufacturers
3. Verify specs and footprint match — pad dimensions can vary even within the same package size
4. As a last resort, mark as "consigned" and source separately

## Tips

- `basic` field matters — JLCPCB basic parts have no setup fee; extended parts cost $3 each
- Check stock per warehouse (`whs-js`, `whs-zh`, `whs-hk`) — availability varies
- `moq` and `order_multiple` — many parts require minimum quantities or specific multiples
- Datasheet quality varies for Chinese manufacturers — cross-reference MPN on DigiKey for better docs
