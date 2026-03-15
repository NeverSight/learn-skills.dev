---
name: digikey
description: Search DigiKey for electronic components and download datasheets — primary source for prototype orders and the preferred API-based method for fetching datasheets. Find parts by keyword or part number, check pricing/stock, download datasheets directly via API, analyze specifications. Sync and maintain a local datasheets directory for a KiCad project — extract components from schematics, download all missing datasheets, keep them up to date. Use with KiCad for BOM creation and part selection. Use this skill when the user asks about electronic components, part specifications, datasheets, footprints, pricing, stock availability, or needs to download/read a datasheet — even if they don't mention "DigiKey" by name. Also use when the user says "sync datasheets", "download datasheets for my board/project", or mentions a datasheets directory. DigiKey is the default distributor for prototyping and the preferred datasheet source because its API returns direct PDF links without web scraping. For package cross-reference tables and BOM workflow, see the `bom` skill.
---

# DigiKey Parts Search & Analysis

DigiKey is the **primary source for prototype orders** (Mouser is secondary). Its API returns direct PDF datasheet links, making it the preferred datasheet source. For production orders, see `lcsc`/`jlcpcb`. For BOM management and export workflows, see `bom`.

## API Credential Setup

The DigiKey API requires OAuth 2.0 credentials. Here's how to set them up:

1. **Create a DigiKey account** at [digikey.com](https://www.digikey.com) if you don't have one
2. **Register an API app** at [developer.digikey.com](https://developer.digikey.com):
   - Sign in with your DigiKey account
   - Go to "My Apps" → "Create App"
   - App name: anything (e.g., "claude-code")
   - Select **"Product Information v4"** API
   - OAuth type: **Client Credentials** (2-legged, no user login needed)
   - Callback URL: `https://localhost` (not used for client credentials, but required)
   - After creation, note the **Client ID** and **Client Secret**
3. **Set the environment variables** before running the scripts:
   ```bash
   export DIGIKEY_CLIENT_ID=your_client_id_here
   export DIGIKEY_CLIENT_SECRET=your_client_secret_here
   ```
   If credentials are stored in a central secrets file (e.g., `~/.config/secrets.env`), load them first:
   ```bash
   export $(grep -v '^#' ~/.config/secrets.env | grep -v '^$' | xargs)
   ```

The client credentials flow has no user interaction — once configured, API calls work automatically.

## DigiKey Product Information API v4

The API is the preferred way to search DigiKey. It returns structured JSON with full product details, pricing, stock, datasheets, and parametric data.

**Base URL:** `https://api.digikey.com`

### Authentication

All API requests require OAuth 2.0. Use the **client credentials flow** (2-legged). Credentials must be loaded as environment variables (see "API Credential Setup" above).

```bash
curl -s -X POST https://api.digikey.com/v1/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=${DIGIKEY_CLIENT_ID}&client_secret=${DIGIKEY_CLIENT_SECRET}&grant_type=client_credentials"
```

The response returns an `access_token` valid for **10 minutes**. Cache the token in a shell variable and reuse it for subsequent calls in the same session. If you get a 401 error mid-session, the token has expired — re-authenticate to get a fresh one.

### Required Headers

Every API call needs:
```
X-DIGIKEY-Client-Id: ${DIGIKEY_CLIENT_ID}
Authorization: Bearer <access_token>
```

Optional locale headers:
- `X-DIGIKEY-Locale-Language`: `en` (default), `ja`, `de`, `fr`, `ko`, `zhs`, `zht`, `it`, `es`
- `X-DIGIKEY-Locale-Currency`: `USD` (default), `CAD`, `EUR`, `GBP`, `JPY`, etc.
- `X-DIGIKEY-Locale-Site`: `US` (default), `CA`, `UK`, `DE`, etc.

### KeywordSearch — Find Parts

```
POST /products/v4/search/keyword
```

This is the primary search endpoint. Search by MPN, DigiKey part number, description, or keywords.

Request body:
```json
{
  "Keywords": "GRM155R71C104KA88D",
  "Limit": 25,
  "Offset": 0,
  "FilterOptionsRequest": {
    "MinimumQuantityAvailable": 1,
    "SearchOptions": ["InStock", "HasDatasheet", "RoHSCompliant"],
    "ManufacturerFilter": [{"Id": "..."}],
    "CategoryFilter": [{"Id": "..."}],
    "StatusFilter": [{"Id": "..."}],
    "MarketPlaceFilter": "ExcludeMarketPlace"
  },
  "SortOptions": {
    "Field": "Price",
    "SortOrder": "Ascending"
  }
}
```

Key request fields:
- `Keywords` (string, max 250 chars) — search term (MPN, DK PN, description)
- `Limit` (int, 1-50) — results per page
- `Offset` (int) — pagination offset
- `SearchOptions` — array of: `InStock`, `HasDatasheet`, `RoHSCompliant`, `NormallyStocking`, `Has3DModel`, `HasCadModel`, `HasProductPhoto`, `NewProduct`
- `SortOptions.Field` — `Price`, `QuantityAvailable`, `Manufacturer`, `ManufacturerProductNumber`, `DigiKeyProductNumber`, `MinimumQuantity`
- `MarketPlaceFilter` — `NoFilter`, `ExcludeMarketPlace`, `MarketPlaceOnly`

Response — key fields in each `Products[]` item:
```json
{
  "ManufacturerProductNumber": "GRM155R71C104KA88D",
  "Manufacturer": {"Id": 563, "Name": "Murata Electronics"},
  "Description": {
    "ProductDescription": "CAP CER 100NF 16V X7R 0402",
    "DetailedDescription": "..."
  },
  "UnitPrice": 0.01,
  "QuantityAvailable": 248000,
  "ProductUrl": "https://www.digikey.com/...",
  "DatasheetUrl": "https://...",
  "PhotoUrl": "https://...",
  "ProductVariations": [
    {
      "DigiKeyProductNumber": "490-10698-1-ND",
      "PackageType": {"Name": "Cut Tape"},
      "StandardPricing": [
        {"BreakQuantity": 1, "UnitPrice": 0.01, "TotalPrice": 0.01},
        {"BreakQuantity": 10, "UnitPrice": 0.008, "TotalPrice": 0.08}
      ],
      "QuantityAvailableforPackageType": 248000,
      "MinimumOrderQuantity": 1,
      "StandardPackage": 10000
    }
  ],
  "Parameters": [
    {"ParameterText": "Capacitance", "ValueText": "100nF"},
    {"ParameterText": "Voltage Rated", "ValueText": "16V"},
    {"ParameterText": "Temperature Coefficient", "ValueText": "X7R"},
    {"ParameterText": "Package / Case", "ValueText": "0402 (1005 Metric)"}
  ],
  "ProductStatus": {"Status": "Active"},
  "Category": {"Name": "Ceramic Capacitors"},
  "Classifications": {"RohsStatus": "ROHS3 Compliant"},
  "Discontinued": false,
  "EndOfLife": false,
  "NormallyStocking": true
}
```

### ProductDetails — Full Details for One Part

```
GET /products/v4/search/{productNumber}/productdetails
```

Use this for expanded information on a specific part. `{productNumber}` can be a DigiKey part number or manufacturer part number.

Query parameters:
- `manufacturerId` (optional) — disambiguate MPNs that match multiple manufacturers (e.g., "CR2032")

Returns the full `Product` object with all parameters, pricing (including MyPricing if authenticated with account), media links, and related products.

### Other Useful Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/products/v4/search/{pn}/productdetails` | GET | Full product info for one part |
| `/products/v4/search/productpricing/{pn}` | GET | Pricing with MyPricing for a part |
| `/products/v4/search/{pn}/media` | GET | All media (images, datasheets) for a part |
| `/products/v4/search/manufacturers` | GET | All manufacturers (use IDs in KeywordSearch filters) |
| `/products/v4/search/categories` | GET | All categories (use IDs in KeywordSearch filters) |
| `/products/v4/search/{pn}/alternatepackaging` | GET | Alternate packaging options |
| `/products/v4/search/{pn}/substitutions` | GET | Substitute parts |
| `/products/v4/search/{pn}/recommendedproducts` | GET | Recommended/associated parts |

### Rate Limits

Per-minute and daily quotas apply. HTTP 429 with `Retry-After` header on exceed.

### Error Responses

All errors return `DKProblemDetails`:
```json
{"type": "...", "title": "...", "status": 401, "detail": "Invalid token", "correlationId": "..."}
```

## Fallback: WebFetch to DigiKey Website

If API credentials are not available or authentication fails, search DigiKey by fetching product pages directly with WebFetch:

```
https://www.digikey.com/en/products/result?keywords=<url-encoded-query>
```

Examples:
- `https://www.digikey.com/en/products/result?keywords=GRM155R71C104KA88D` (by MPN)
- `https://www.digikey.com/en/products/result?keywords=100nF+0402+X7R+16V` (by specs)

WebFetch results from DigiKey can be noisy (JS-heavy pages). Look for the product table rows containing: DigiKey part number, MPN, description, unit price, stock quantity, and datasheet links. If results are truncated or empty, try searching by exact MPN rather than keywords.

## Datasheet Download & Analysis

DigiKey's API provides **direct PDF URLs** for datasheets — this is the preferred method for downloading datasheets because it avoids web scraping and returns reliable, stable links. Other skills (kicad, bom) should use DigiKey API as the first-choice datasheet source.

### Datasheet Directory Sync (Primary Workflow)

Use `sync_datasheets_digikey.py` to maintain a `datasheets/` directory alongside a KiCad project. It extracts components from the schematic, searches DigiKey for datasheet URLs, downloads missing PDFs, and writes an `index.json` manifest. Subsequent runs are incremental — only new or changed parts are fetched.

```bash
# Sync datasheets for a KiCad project (creates datasheets/ next to the schematic)
python3 <skill-path>/scripts/sync_datasheets_digikey.py <file.kicad_sch>

# Preview what would be downloaded
python3 <skill-path>/scripts/sync_datasheets_digikey.py <file.kicad_sch> --dry-run

# Retry previously failed downloads
python3 <skill-path>/scripts/sync_datasheets_digikey.py <file.kicad_sch> --force

# Custom output directory
python3 <skill-path>/scripts/sync_datasheets_digikey.py <file.kicad_sch> -o ./my-datasheets

# Use pre-computed analyzer JSON instead of running the analyzer
python3 <skill-path>/scripts/sync_datasheets_digikey.py analyzer_output.json

# Parallel downloads (3 workers)
python3 <skill-path>/scripts/sync_datasheets_digikey.py <file.kicad_sch> --parallel 3
```

The script:
- **Runs the kicad schematic analyzer** automatically to extract components and MPNs
- **Filters generic passives** — skips entries without real MPNs (e.g., "100nF", "10K")
- **Tries schematic URLs first** — uses the datasheet URL embedded in the KiCad symbol before hitting the DigiKey API, saving API calls
- **Writes `index.json` manifest** — maps each MPN to its PDF file, manufacturer, description, download status, and URL. The kicad skill reads this during design review to cross-reference datasheets with the schematic.
- **Tracks failures** — failed downloads are recorded with error details and not retried on subsequent runs unless `--force` is used
- **Rate-limited** — 1 second between DigiKey API calls (configurable with `--delay`)
- **Saves progress incrementally** — if interrupted, already-downloaded files are preserved

The `index.json` manifest structure:
```json
{
  "schematic": "/path/to/file.kicad_sch",
  "last_sync": "2026-03-09T04:44:30+00:00",
  "parts": {
    "TPS61023DRLR": {
      "file": "TPS61023DRLR.pdf",
      "manufacturer": "Texas Instruments",
      "description": "Boost converter",
      "datasheet_url": "https://...",
      "status": "ok",
      "references": ["U3", "U2"],
      "size_bytes": 2392725
    }
  }
}
```

### Single Datasheet Download

Use `fetch_datasheet_digikey.py` for one-off datasheet downloads. It handles manufacturer-specific quirks automatically.

```bash
# Search by MPN (uses DigiKey API, requires credentials)
python3 <skill-path>/scripts/fetch_datasheet_digikey.py --search "TPS61023" -o datasheet.pdf

# Direct URL download
python3 <skill-path>/scripts/fetch_datasheet_digikey.py "https://www.ti.com/lit/gpn/tps61023" -o datasheet.pdf

# JSON output for script integration
python3 <skill-path>/scripts/fetch_datasheet_digikey.py --search "ADP1706" --json
```

The script:
- **OS-agnostic** — uses Python `requests` library (no wget/curl dependency). Falls back to `urllib` if `requests` isn't installed.
- **Normalizes redirect URLs** — DigiKey's `DatasheetUrl` for TI parts points to a JS redirect page; the script extracts the direct PDF link. Also fixes protocol-relative `//mm.digikey.com/...` URLs.
- **Sets proper User-Agent** — many manufacturer sites (Nexperia, Lite-On, STMicro, Molex) block bare `urllib` or `curl` requests but serve PDFs fine with a browser User-Agent
- **Validates PDF headers** — rejects HTML error pages or Cloudflare challenge pages that masquerade as downloads
- **Falls back to alternative sources** — tries known URL patterns for Microchip when the primary URL fails
- **Headless browser fallback** — if `playwright` is installed, automatically uses a headless Chromium browser as a last resort for sites that serve PDFs via JavaScript (Broadcom doc viewer, Espressif download redirects). Intercepts download events and reads response bodies directly.
- **Exit codes**: 0 = success, 1 = download failed, 2 = search/API error
- **Dependencies**:
  - `pip install requests` (strongly recommended; urllib fallback can't handle HTTP/2 sites like analog.com)
  - `pip install playwright && playwright install chromium` (optional; enables headless browser fallback for JS-heavy sites)

### Manufacturer Compatibility

Tested against 240 components across 8 open-source KiCad projects (96% download success rate, 94% without Playwright):

| Manufacturer | Status | Notes |
|---|---|---|
| TI | Works | URL normalization strips JS redirect wrapper |
| ADI / Analog | Works | `requests` handles HTTP/2 transparently |
| STMicro | Works | Requires User-Agent header |
| Nexperia | Works | Requires User-Agent header |
| Lite-On | Works | Requires User-Agent header |
| Molex | Works | Requires User-Agent header |
| Renesas | Works | Direct download |
| ON Semi | Works | Direct download |
| NXP | Works | Direct download |
| Diodes Inc | Works | Direct download |
| Microchip | Works | Direct download via API URLs |
| YAGEO, Samsung, Murata | Works | DigiKey-hosted PDFs (`mm.digikey.com`) |
| Broadcom | Works* | Requires Playwright — `docs.broadcom.com` serves PDFs via JS download |
| Espressif | Works* | Requires Playwright — download redirect needs JS execution |
| Lattice | Mixed | Some URLs require cookies/auth |

\* Requires `playwright` package — falls back gracefully to user notification if not installed.

### When Download Fails

If the script or inline download fails (exit code 1), **tell the user and provide the URL** so they can open it in a real browser. Some manufacturer sites (Lattice, TDK InvenSense) require interactive login, cookies, or CAPTCHA that even a headless browser can't handle. With Playwright installed, Broadcom and Espressif now download automatically.

Example message to the user:
> I couldn't download the datasheet for ICE40UP5K-SG48I automatically — Lattice's site requires browser authentication. Here's the direct link:
> https://www.latticesemi.com/-/media/LatticeSemi/Documents/DataSheets/iCE/FPGA-DS-02008-1-9-iCE40-Ultra-Plus-Family-Data-Sheet.ashx
>
> You can open it in your browser and save it locally, then I can read and analyze it.

The `--json` output always includes the `datasheet_url` field even on failure, so you can extract the URL programmatically.

### Manual Download Workflow

If the script isn't available or you need to do it inline:

1. **Search for the part** using KeywordSearch or ProductDetails
2. **Extract `DatasheetUrl`** from the API response
3. **Normalize the URL** — if it starts with `//`, prepend `https:`. If it contains `ti.com/general/docs/suppproductinfo`, extract the `gotoUrl` query parameter.
4. **Download with `requests`** (Python) or `wget`/`curl` with a browser User-Agent
5. **Verify it's a PDF**: first 4 bytes should be `%PDF`

If the `DatasheetUrl` field is empty or all download methods fail:
- Provide the URL to the user for manual browser download
- Try the `/products/v4/search/{pn}/media` endpoint for alternative media links
- WebSearch as a last resort: `"<MPN> datasheet filetype:pdf"`

### What to Extract from Datasheets

When analyzing a datasheet for a KiCad design review (see `kicad` skill):
- **Absolute maximum ratings** — voltage, current, temperature limits
- **Recommended operating conditions** — typical operating ranges
- **Pinout and pin descriptions** — verify against KiCad symbol
- **Package dimensions** — verify against KiCad footprint
- **Typical application circuit** — compare against the user's schematic
- **Thermal characteristics** — θJA, θJC for power dissipation calculations
- **Electrical characteristics** — key parameters (Vout, Iq, PSRR, etc.)

## Tips

- DigiKey PN suffixes: `-ND` standard, `-1-ND` cut tape, `-2-ND` digi-reel, `-6-ND` full reel
- Use `ExcludeMarketPlace` filter to avoid third-party seller listings
- Price breaks in `ProductVariations[].StandardPricing[]` — check `BreakQuantity` thresholds
- Check `ProductStatus` and `Discontinued`/`EndOfLife` before selecting parts
