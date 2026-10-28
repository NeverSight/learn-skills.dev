---
name: taiwan-equity-research-coverage
description: Structured equity research database for 1,735 Taiwan-listed companies with wikilink knowledge graph, supply chain mapping, and financial data tools.
triggers:
  - "search Taiwan stocks for a buzzword or theme"
  - "add a new Taiwan ticker to the database"
  - "update financial data for Taiwan companies"
  - "find companies in a supply chain or technology ecosystem"
  - "generate thematic investment screens for Taiwan market"
  - "build wikilink network graph for Taiwan stocks"
  - "audit equity research report quality"
  - "refresh valuation multiples for Taiwan listed companies"
---

# Taiwan Equity Research Coverage (My-TW-Coverage)

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A structured equity research database covering **1,735 Taiwan-listed companies** (TWSE + OTC) across **99 industry sectors**. Each report contains a business overview, supply chain mapping, customer/supplier relationships, and financial data — all cross-referenced through **4,900+ wikilinks** forming a searchable knowledge graph.

## Installation

```bash
git clone https://github.com/Timeverse/My-TW-Coverage
cd My-TW-Coverage
pip install yfinance pandas tabulate
```

## Project Structure

```
My-TW-Coverage/
├── Pilot_Reports/             # 1,735 ticker reports across 99 sectors
│   ├── Semiconductors/        # 155 tickers
│   ├── Electronic Components/ # 267 tickers
│   ├── Computer Hardware/     # 114 tickers
│   └── ... (99 sector folders)
├── scripts/
│   ├── utils.py               # Shared utilities
│   ├── add_ticker.py          # Generate new ticker reports
│   ├── update_financials.py   # Refresh financial tables + valuation
│   ├── update_valuation.py    # Refresh valuation multiples only (fast)
│   ├── update_enrichment.py   # Update business descriptions from JSON
│   ├── audit_batch.py         # Quality auditing
│   ├── discover.py            # Buzzword → related companies search
│   ├── build_wikilink_index.py# Rebuild WIKILINKS.md index
│   ├── build_themes.py        # Generate thematic investment screens
│   └── build_network.py       # Generate D3.js network graph
├── WIKILINKS.md               # Auto-generated browsable wikilink index
├── network/index.html         # Interactive D3.js wikilink network
├── themes/                    # Thematic investment screens (auto-generated)
└── task.md                    # Batch definitions and progress tracking
```

## Report Format

Each ticker report is a markdown file at `Pilot_Reports/<Sector>/<TICKER>_<Name>.md`:

```markdown
# 2330 - [[台積電]]

## 業務簡介
**板塊:** Technology
**產業:** Semiconductors
**市值:** 47,326,857 百萬台幣
**企業價值:** 44,978,990 百萬台幣

台積電為全球最大晶圓代工廠，專注於 [[CoWoS]]、[[3奈米]] 先進製程...

## 供應鏈位置
**上游:** [[ASML]], [[Applied Materials]], [[SUMCO]]
**中游:** **台積電** (晶圓代工)
**下游:** [[Apple]], [[NVIDIA]], [[AMD]], [[Broadcom]]

## 主要客戶及供應商
### 主要客戶
- [[Apple]], [[NVIDIA]], [[AMD]], [[Qualcomm]]

### 主要供應商
- [[ASML]], [[Tokyo Electron]], [[Shin-Etsu]]

## 財務概況
### 估值指標
| P/E (TTM) | Forward P/E | P/S (TTM) | P/B | EV/EBITDA |
|-----------|-------------|-----------|-----|-----------|
| 28.5      | 22.1        | 9.3       | 7.2 | 16.4      |

### 年度財務數據
[Annual 3-year financial table with 14 metrics]

### 季度財務數據
[Quarterly 4-quarter financial table]
```

## Key Commands

### Add a New Ticker

```bash
# Basic (auto-detect sector)
python scripts/add_ticker.py 2330 台積電

# With explicit sector
python scripts/add_ticker.py 2330 台積電 --sector Semiconductors
```

### Update Financial Data

```bash
# Single ticker
python scripts/update_financials.py 2330

# Multiple tickers
python scripts/update_financials.py 2330 2454 3034

# By batch number (see task.md for batch definitions)
python scripts/update_financials.py --batch 101

# By sector
python scripts/update_financials.py --sector Semiconductors

# All 1,735 tickers (slow)
python scripts/update_financials.py
```

### Update Valuation Only (~3x Faster)

Refreshes only P/E, Forward P/E, P/S, P/B, EV/EBITDA, and stock price — skips full financial statement re-fetch.

```bash
python scripts/update_valuation.py 2330
python scripts/update_valuation.py --batch 101
python scripts/update_valuation.py --sector Semiconductors
python scripts/update_valuation.py                          # All tickers
```

### Discover Companies by Buzzword

Find every Taiwan-listed company related to a theme or technology:

```bash
# Basic search
python scripts/discover.py "液冷散熱"

# Auto-detect relevant sectors (skips banks/insurance/real estate for tech terms)
python scripts/discover.py "液冷散熱" --smart

# Tag matching companies with [[wikilinks]] in their reports
python scripts/discover.py "液冷散熱" --apply

# Apply + rebuild themes + rebuild network graph
python scripts/discover.py "液冷散熱" --apply --rebuild

# Limit to a specific sector
python scripts/discover.py "液冷散熱" --sector Semiconductors
```

Common buzzword examples:
- `"CoWoS"` — TSMC advanced packaging supply chain
- `"HBM"` — High Bandwidth Memory ecosystem
- `"電動車"` — EV component suppliers
- `"AI 伺服器"` — AI server supply chain (148 companies)
- `"光阻液"` — Photoresist suppliers and consumers
- `"碳化矽"` — Silicon carbide (SiC) companies

### Update Enrichment Content (Bulk AI Research)

Prepare a JSON file, then apply to specific tickers, batches, or sectors:

```bash
python scripts/update_enrichment.py --data enrichment.json 2330
python scripts/update_enrichment.py --data enrichment.json --batch 101
python scripts/update_enrichment.py --data enrichment.json --sector Semiconductors
```

**Enrichment JSON format:**

```json
{
  "2330": {
    "desc": "台積電為全球最大晶圓代工廠，專注於 [[CoWoS]]、[[3奈米]] 先進製程，為 [[Apple]]、[[NVIDIA]] 等科技巨頭提供晶片製造服務。",
    "supply_chain": "**上游:**\n- [[ASML]] (EUV 微影設備)\n- [[Applied Materials]] (薄膜沉積)\n**中游:**\n- **台積電** (晶圓代工)\n**下游:**\n- [[Apple]]\n- [[NVIDIA]]",
    "cust": "### 主要客戶\n- [[Apple]] (約25%營收)\n- [[NVIDIA]]\n- [[AMD]]\n\n### 主要供應商\n- [[ASML]]\n- [[Tokyo Electron]]"
  },
  "2454": {
    "desc": "...",
    "supply_chain": "...",
    "cust": "..."
  }
}
```

### Audit Report Quality

```bash
# Single batch
python scripts/audit_batch.py 101 -v

# All batches
python scripts/audit_batch.py --all -v
```

Audit checks:
- Minimum 8 wikilinks per report
- No generic terms in brackets (e.g. `[[公司]]`, `[[產品]]`)
- No placeholder text remaining
- No English text in Chinese-language sections
- Metadata completeness (板塊, 產業, 市值, 企業價值)
- Section depth (業務簡介, 供應鏈位置, 主要客戶及供應商, 財務概況 all present)

### Rebuild Wikilink Index

```bash
python scripts/build_wikilink_index.py
```

Regenerates `WIKILINKS.md` — a browsable index of all 4,900+ wikilinks categorized as Technologies, Materials, Applications, and Companies. Run after any enrichment update.

### Generate Thematic Investment Screens

```bash
# Build all 20 themes
python scripts/build_themes.py

# Single theme
python scripts/build_themes.py "CoWoS"

# List available themes
python scripts/build_themes.py --list
```

Output in `themes/` — each page shows companies grouped by upstream/midstream/downstream role.

### Generate Interactive Network Graph

```bash
# Default: min 5 co-occurrences
python scripts/build_network.py

# Fewer edges for cleaner view
python scripts/build_network.py --min-weight 10

# Only top 200 nodes
python scripts/build_network.py --top 200
```

Opens `network/index.html` in browser — D3.js force-directed graph. Node colors:
- 🔴 Red = Taiwan company
- 🔵 Blue = International company
- 🟢 Green = Technology
- 🟠 Orange = Material
- 🟣 Purple = Application

## Wikilink Graph — Core Feature

The wikilink graph is what makes this database powerful. Every `[[entity]]` in every report creates edges in a knowledge graph.

**Search by entity to find related companies:**

| Search | Results | Insight |
|--------|---------|---------|
| `[[Apple]]` | 207 companies | Apple's full Taiwan supplier network |
| `[[NVIDIA]]` | 277 companies | NVIDIA's Taiwan supply chain |
| `[[台積電]]` | 469 companies | Taiwan semiconductor ecosystem |
| `[[CoWoS]]` | 39 companies | TSMC advanced packaging players |
| `[[AI 伺服器]]` | 148 companies | AI server supply chain |
| `[[PCB]]` | 263 companies | Printed circuit board ecosystem |
| `[[電動車]]` | 223 companies | EV component suppliers |

**Browse:** Open `WIKILINKS.md` for the full categorized index.

## Code Examples

### Read and Parse a Report

```python
import re
from pathlib import Path

def get_report(ticker: str, reports_dir: str = "Pilot_Reports") -> dict:
    """Find and parse a ticker report."""
    base = Path(reports_dir)
    # Find the file across all sector subdirectories
    matches = list(base.rglob(f"{ticker}_*.md"))
    if not matches:
        return {}
    
    content = matches[0].read_text(encoding="utf-8")
    
    # Extract all wikilinks
    wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)
    
    # Extract sector metadata
    sector_match = re.search(r'\*\*產業:\*\*\s*(.+)', content)
    board_match = re.search(r'\*\*板塊:\*\*\s*(.+)', content)
    
    return {
        "ticker": ticker,
        "file": str(matches[0]),
        "sector": sector_match.group(1).strip() if sector_match else None,
        "board": board_match.group(1).strip() if board_match else None,
        "wikilinks": list(set(wikilinks)),
        "wikilink_count": len(set(wikilinks)),
        "content": content
    }

# Usage
report = get_report("2330")
print(f"Sector: {report['sector']}")
print(f"Wikilinks ({report['wikilink_count']}): {report['wikilinks'][:10]}")
```

### Build a Custom Wikilink Index

```python
import re
from pathlib import Path
from collections import defaultdict

def build_wikilink_index(reports_dir: str = "Pilot_Reports") -> dict:
    """
    Returns: {entity: [list of tickers that mention it]}
    """
    index = defaultdict(list)
    
    for md_file in Path(reports_dir).rglob("*.md"):
        # Extract ticker from filename (e.g. "2330_台積電.md" -> "2330")
        ticker = md_file.stem.split("_")[0]
        content = md_file.read_text(encoding="utf-8")
        wikilinks = set(re.findall(r'\[\[([^\]]+)\]\]', content))
        
        for link in wikilinks:
            index[link].append(ticker)
    
    # Sort by mention count
    return dict(sorted(index.items(), key=lambda x: len(x[1]), reverse=True))

# Find all companies in Apple's supply chain
index = build_wikilink_index()
apple_suppliers = index.get("Apple", [])
print(f"Apple supply chain: {len(apple_suppliers)} companies")
print(apple_suppliers[:20])

# Find companies involved in CoWoS
cowos_companies = index.get("CoWoS", [])
print(f"\nCoWoS ecosystem: {len(cowos_companies)} companies: {cowos_companies}")
```

### Find Supply Chain Overlaps Between Two Entities

```python
def supply_chain_overlap(entity_a: str, entity_b: str, reports_dir: str = "Pilot_Reports"):
    """Find tickers that appear in both entities' supply chains."""
    index = build_wikilink_index(reports_dir)
    
    set_a = set(index.get(entity_a, []))
    set_b = set(index.get(entity_b, []))
    overlap = set_a & set_b
    
    print(f"{entity_a}: {len(set_a)} companies")
    print(f"{entity_b}: {len(set_b)} companies")
    print(f"Overlap: {len(overlap)} companies — {sorted(overlap)}")
    return overlap

# Companies in both NVIDIA and Apple supply chains
supply_chain_overlap("NVIDIA", "Apple")

# Companies in both AI server and EV supply chains
supply_chain_overlap("AI 伺服器", "電動車")
```

### Batch Financial Update with Error Handling

```python
import subprocess
import sys

def update_sector_financials(sector: str, valuation_only: bool = False):
    """Update financials for all tickers in a sector."""
    script = "update_valuation.py" if valuation_only else "update_financials.py"
    cmd = [sys.executable, f"scripts/{script}", "--sector", sector]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(result.stdout)
    
    return result.returncode

# Update valuation multiples for semiconductors (fast)
update_sector_financials("Semiconductors", valuation_only=True)

# Full financial update for a sector
update_sector_financials("Electronic Components", valuation_only=False)
```

### Prepare Enrichment JSON

```python
import json

def build_enrichment_entry(ticker: str, company_name: str,
                           description: str, upstream: list[str],
                           midstream: str, downstream: list[str],
                           customers: list[str], suppliers: list[str]) -> dict:
    """
    Build a properly formatted enrichment entry.
    All entity names in lists will be wrapped in [[wikilinks]].
    """
    def wikify(items):
        return "\n".join(f"- [[{item}]]" for item in items)
    
    supply_chain = (
        f"**上游:**\n{wikify(upstream)}\n"
        f"**中游:**\n- **{company_name}** ({midstream})\n"
        f"**下游:**\n{wikify(downstream)}"
    )
    
    cust_section = (
        f"### 主要客戶\n{wikify(customers)}\n\n"
        f"### 主要供應商\n{wikify(suppliers)}"
    )
    
    return {
        "desc": description,
        "supply_chain": supply_chain,
        "cust": cust_section
    }

# Build enrichment for multiple tickers
enrichment = {
    "2330": build_enrichment_entry(
        ticker="2330",
        company_name="台積電",
        description="台積電為全球最大晶圓代工廠，專注於 [[CoWoS]]、[[3奈米]] 先進製程，為全球領先科技公司提供晶片製造服務。",
        upstream=["ASML", "Applied Materials", "SUMCO", "Tokyo Electron"],
        midstream="晶圓代工",
        downstream=["Apple", "NVIDIA", "AMD", "Broadcom", "Qualcomm"],
        customers=["Apple", "NVIDIA", "AMD", "Qualcomm", "MediaTek"],
        suppliers=["ASML", "Tokyo Electron", "Shin-Etsu", "Applied Materials"]
    )
}

# Save to file
with open("enrichment.json", "w", encoding="utf-8") as f:
    json.dump(enrichment, f, ensure_ascii=False, indent=2)

print("enrichment.json ready. Apply with:")
print("python scripts/update_enrichment.py --data enrichment.json 2330")
```

### Audit a Batch Programmatically

```python
import subprocess
import json

def audit_and_report(batch_id: int) -> dict:
    """Run audit and parse results."""
    result = subprocess.run(
        ["python", "scripts/audit_batch.py", str(batch_id), "-v"],
        capture_output=True, text=True
    )
    
    output = result.stdout
    
    # Parse pass/fail counts from output
    passed = output.count("✓") 
    failed = output.count("✗")
    
    return {
        "batch": batch_id,
        "passed": passed,
        "failed": failed,
        "pass_rate": passed / (passed + failed) if (passed + failed) > 0 else 0,
        "output": output
    }

results = audit_and_report(101)
print(f"Batch 101: {results['passed']} passed, {results['failed']} failed")
print(f"Pass rate: {results['pass_rate']:.1%}")
```

## Common Workflows

### Workflow 1: Research a New Investment Theme

```bash
# 1. Search for related companies
python scripts/discover.py "液冷散熱" --smart

# 2. Apply wikilinks to matching reports
python scripts/discover.py "液冷散熱" --apply

# 3. Rebuild themes to include new theme
python scripts/build_themes.py "液冷散熱"

# 4. Rebuild wikilink index and network
python scripts/build_wikilink_index.py
python scripts/build_network.py

# 5. Browse results
open themes/液冷散熱.md
open network/index.html
```

### Workflow 2: Onboard a New Ticker

```bash
# 1. Add the report (Python script, free)
python scripts/add_ticker.py 6669 緯穎 --sector Computer Hardware

# 2. Update financial data
python scripts/update_financials.py 6669

# 3. Prepare enrichment JSON (use AI research or manual)
# Edit enrichment.json with business description, supply chain, customers

# 4. Apply enrichment
python scripts/update_enrichment.py --data enrichment.json 6669

# 5. Audit quality
python scripts/audit_batch.py --all -v

# 6. Rebuild index
python scripts/build_wikilink_index.py
```

### Workflow 3: Refresh Valuation for Earnings Season

```bash
# Fast valuation refresh only (no full financial re-fetch)
python scripts/update_valuation.py --sector Semiconductors
python scripts/update_valuation.py --sector Electronic Components
python scripts/update_valuation.py --sector Computer Hardware

# Or refresh everything (slow, run overnight)
python scripts/update_valuation.py
```

### Workflow 4: Map a Supply Chain

```python
# Find all Taiwan companies connected to a specific technology
from collections import defaultdict
import re
from pathlib import Path

def map_supply_chain(technology: str, reports_dir: str = "Pilot_Reports"):
    results = {"upstream": [], "midstream": [], "downstream": []}
    
    for md_file in Path(reports_dir).rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        
        if f"[[{technology}]]" not in content:
            continue
        
        ticker = md_file.stem.split("_")[0]
        company = md_file.stem.split("_", 1)[1] if "_" in md_file.stem else ""
        
        # Detect position in supply chain
        if f"**上游:**" in content and f"[[{technology}]]" in content.split("**上游:**")[1].split("**中游:**")[0]:
            results["upstream"].append(f"{ticker} {company}")
        elif f"[[{technology}]]" in content and "**中游:**" in content:
            mid_section = content.split("**中游:**")[1].split("**下游:**")[0] if "**下游:**" in content else ""
            if f"[[{technology}]]" in mid_section:
                results["midstream"].append(f"{ticker} {company}")
        else:
            results["downstream"].append(f"{ticker} {company}")
    
    return results

chain = map_supply_chain("CoWoS")
print(f"Upstream: {chain['upstream']}")
print(f"Midstream: {chain['midstream']}")
print(f"Downstream: {chain['downstream']}")
```

## Token Cost Reference

| Operation | Tokens Used | Command |
|-----------|-------------|---------|
| Update financials | **Free** (yfinance) | `python scripts/update_financials.py` |
| Update valuation | **Free** (yfinance) | `python scripts/update_valuation.py` |
| Discover (with results) | **Free** | `python scripts/discover.py "term"` |
| Audit | **Free** | `python scripts/audit_batch.py` |
| Build themes/network/index | **Free** | `python scripts/build_*.py` |
| `/add-ticker` (Claude Code) | Medium | AI research per ticker |
| `/update-enrichment` (Claude Code) | Medium | 3–5 web searches per ticker |
| `/discover` (no results found) | Low–High | AI researches online |

**Rule of thumb:** Use Python scripts for bulk data operations. Use Claude Code slash commands only when AI research is needed for a specific ticker.

## Troubleshooting

**`yfinance` returns no data for a Taiwan ticker:**
```python
import yfinance as yf
# Taiwan tickers need .TW suffix for TWSE, .TWO for OTC
tsmc = yf.Ticker("2330.TW")
print(tsmc.info.get("marketCap"))
```

**Report not found by scripts:**
- Filename must match pattern: `{TICKER}_{CompanyName}.md`
- Must be inside a subfolder of `Pilot_Reports/`
- Use `python scripts/utils.py` to test file discovery

**Audit fails "too few wikilinks":**
- Minimum 8 unique `[[wikilinks]]` required per report
- Use `update_enrichment.py` to add richer content
- Run `discover.py --apply` to auto-tag relevant wikilinks

**`build_network.py` produces empty graph:**
```bash
# Ensure reports exist and have wikilinks first
python scripts/build_wikilink_index.py  # Check WIKILINKS.md has entries
python scripts/build_network.py --min-weight 2  # Lower threshold
```

**Enrichment JSON rejected:**
- Ensure file is valid UTF-8 with `ensure_ascii=False`
- Keys must be ticker strings (`"2330"`, not `2330`)
- Required keys per entry: `desc`, `supply_chain`, `cust`
- Content must be in Traditional Chinese; English only for proper nouns

**Finding batch numbers:**
- See `task.md` for batch definitions and which tickers are in each batch
- Batches are used for incremental processing of the 1,735 tickers
