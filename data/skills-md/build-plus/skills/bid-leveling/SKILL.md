---
name: bid-leveling
description: Analyze and compare construction bids, proposals, estimates, and subcontractor quotes. Assigns line items to UniFormat II headings, compares absolute cost and cost per unit, produces a leveling spreadsheet (CSV or Excel) and a concise PDF report with scope overlap matrix, contractual term comparison, and a recommendation. Use when the user provides one or more bid documents (PDFs, spreadsheets, or text) to analyze or compare, or asks to "level bids", "compare bids", "bid tabulation", "bid comparison", "bid analysis", or "analyze this bid/quote/proposal" for a construction project.
license: ISC
metadata:
  author: Buildplus
  version: 1.0.0
  url: https://buildplus.app/resources/skills
---

# Bid Leveling

Compare construction bids by mapping line items to UniFormat II headings, producing a leveling spreadsheet and a concise analytical PDF report.

## Single Document vs. Multiple Documents

This skill handles both single-bid analysis and multi-bid comparison. The workflow is the same either way, with these differences when only **one document** is provided:

- **Skip Step 3** (scope overlap assessment) — there is nothing to compare
- **No recommendation** — omit `recommendations` and `overlap_comparison` from `analysis.json` entirely. The PDF will not render a Recommendation section.
- **No scope overlap matrix** — omit `scope_overlap` from `analysis.json`. The PDF page 1 will show project info and the bid summary table only.
- **The spreadsheet and PDF are still produced** — the spreadsheet shows the single bidder's costs broken down by UniFormat, and the PDF details the bid's contractual terms, scope, qualifications, and exclusions.

This is useful when the user wants to analyze a single proposal, extract its structure into UniFormat categories, and document its terms before additional bids come in.

## Workflow

1. Collect project info and output format preference
2. Read and extract data from each bid document
3. Assess scope overlap and comparability *(skip for single document)*
4. Determine unit of comparison
5. Assign line items to UniFormat codes; decide granularity
6. Build structured JSON data
7. Generate spreadsheet (run `generate_csv.py`)
8. Generate PDF (run `generate_pdf.py`)

## Step 1: Collect Project Info

Ask the user for:
- **Project name** (e.g., "Smith Residence")
- **Brief description** (e.g., "Custom home build", "Kitchen remodel", "Plumbing subcontract")
- **Output format**: CSV or Excel?

If the user has already provided this information, skip the questions.

### Excel Context

If the user is already working in an Excel document (they mention an `.xlsx` file, reference a spreadsheet, or are in a spreadsheet context), **add the leveling data as a new sheet in their existing workbook** instead of creating a new file. Pass the existing file as the third argument to `generate_csv.py`.

## Step 2: Read Bid Documents

Read each provided bid document. For each document, extract:
- Every identifiable cost line item (description + cost)
- All contractual terms listed in `references/bid-analysis-guide.md`

Preserve exact wording from source documents when extracting terms.

### Handling Different File Formats

**PDF (`.pdf`)**
Read with the Read tool. For multi-page PDFs, read in page ranges (max 20 pages per request). Bids are often formatted as tables — pay close attention to column alignment when extracting line items. If the PDF contains scanned/image-based content rather than selectable text, treat it as an image (see below).

**Image (`.png`, `.jpg`, `.heic`, etc.)**
Read with the Read tool (multimodal). Extract all visible text, tables, and line items from the image. Images are common for photos of handwritten bids, screenshots of emails, or scanned documents. Take extra care with:
- Handwritten numbers — confirm ambiguous digits (e.g., 1 vs 7, 5 vs 6) by cross-referencing totals
- Partial visibility — if parts of the document are cut off, ask the user for the missing portions
- Low resolution — flag any values you cannot read confidently

**Excel (`.xlsx`, `.xls`, `.csv`)**
Read with the Read tool. Spreadsheet bids often have the clearest structure — look for:
- A schedule of values or line-item tab with description + cost columns
- Summary/totals tabs or rows
- Hidden sheets or columns that may contain additional detail
- Named ranges or formulas that compute subtotals

If the bid is in an Excel file the user is actively working in, this is also an Excel context — see Step 1 for output handling.

**Word (`.docx`, `.doc`)**
Read with the Read tool. Word documents are common for formal proposals and contracts. Cost information may appear as:
- Inline tables (schedule of values, cost breakdowns)
- Paragraph text with embedded dollar amounts ("...for a total of $45,000...")
- Appendices or exhibits attached at the end

For Word docs, also extract contractual language carefully — terms like exclusions, retainage, payment schedules, and insurance requirements are often embedded in the body text rather than in a structured table.

## Step 3: Assess Scope Overlap

Before leveling, determine if the bids are comparable:
- Do they cover the same trade or scope of work?
- Do they share UniFormat Level 2 categories?
- Are totals in a reasonable range relative to each other?

If bids have minimal overlap, **report this prominently** and explain why a direct comparison may be misleading. Still produce outputs with a clear caveat.

### Line-Item Detail Mode

When comparing bids with **highly similar, itemized scopes** (e.g., window schedules, appliance packages, panelized systems, fixture lists), check:
- Do >60% of line items have per-unit pricing that can be compared directly?
- Can equivalent items be matched across bids?

If yes, use `granularity: "line_items"` to break down to actual summarized line item descriptions for an apples-to-apples comparison. Build the `detail_rows` array (see Step 6) with best-effort matching of equivalent line items across bids. Only use this mode when items are truly comparable at the unit level.

## Step 4: Determine Unit of Comparison

Choose the most meaningful unit for per-unit cost comparison. Use the **same unit across all line items** in the output.

| Scope type | Unit | Rationale |
|---|---|---|
| Plumbing, electrical, appliance quotes | `$/fixture` | Count of fixtures is the natural quantity |
| HVAC quotes | `$/zone` | Zones are the natural unit |
| Insulation, drywall, painting, flooring | `$/SF` (scope area) | Area of the specific scope being quoted |
| Framing material purchases, mixed-unit material quotes | `$/SF` (whole house) | No single unit; whole-house SF is the fallback |
| Whole-building / GC bids spanning many UniFormat categories | `$/SF` (whole house) | Broad scope; house SF is appropriate |
| Window or door schedules | `$/unit` | Per-window or per-door |
| Roofing | `$/square` (100 SF) or `$/SF` | Roofing-specific unit |

**Rules:**
- **Never use $/lump or $/lumpsum** — this is not a meaningful comparison unit. There is always a better option.
- Derive the unit and quantity from the bids themselves when possible
- **Default fallback is always `$/SF` (total construction square footage)** — use this when no scope-specific unit can be determined
- If the bids quote a specific scope area (e.g., "1,200 SF of tile"), use that area, not whole-house SF
- The unit must be consistent across all rows in the output

Set `unit_of_comparison` in `bid_data.json`:
```json
"unit_of_comparison": {"label": "$/fixture", "quantity": 14}
```

## Step 5: Assign UniFormat Codes and Choose Granularity

Map each line item to a UniFormat Level 3 code using `references/uniformat_headings.csv`.

Rules:
- Always assign the most specific Level 3 code (e.g., `D2010` not `D20`) — the script handles roll-up
- If a line item spans categories, assign to the dominant one or split if amounts are clear
- General conditions, overhead, profit, bonds, permits = **UNCLASSIFIED** (do not map)

### Choosing Output Granularity

| Scope type | Granularity | When |
|---|---|---|
| Single-trade subcontract | `"level3"` | Plumbing, electrical, HVAC — fine-grained comparison is valuable |
| Multi-trade or partial scope | `"level2"` | Kitchen remodel, TI — roll up to sub-group level |
| Whole-building / GC bids | `"level2"` | Ground-up build — L2 categories give a clear picture |
| Highly similar itemized quotes (>60% overlap) | `"line_items"` | Window schedules, appliance packages, fixture lists |

## Step 6: Build Structured JSON

Create two JSON files in the working directory.

### `bid_data.json` (for spreadsheet generation)

```json
{
  "project_name": "Smith Residence",
  "granularity": "level3",
  "unit_of_comparison": {"label": "$/fixture", "quantity": 14},
  "bidders": [
    {
      "name": "ABC Plumbing",
      "line_items": [
        {"description": "Rough-in plumbing fixtures", "uniformat_code": "D2010", "cost": 18500.00}
      ]
    }
  ],
  "detail_rows": []
}
```

- `granularity`: `"level1"`, `"level2"`, `"level3"`, or `"line_items"`
- `unit_of_comparison`: `{"label": "$/fixture", "quantity": 14}` — the label and divisor for per-unit cost
- `detail_rows`: required only when `granularity` = `"line_items"`:

```json
"detail_rows": [
  {
    "description": "36-inch farmhouse sink",
    "uniformat_code": "D2010",
    "costs": {"ABC Plumbing": 1200.00, "XYZ Plumbing": 1350.00}
  }
]
```

### `analysis.json` (for PDF generation)

All detail fields are **arrays of concise bullet strings**, not paragraphs.

```json
{
  "project_name": "Smith Residence",
  "project_description": "Custom home build",
  "scope_description": "Roofing and exterior scope: roof coverings, exterior walls, drainage",
  "unit_of_comparison": {"label": "$/SF", "quantity": 3200},
  "recommendations": [
    {
      "scope": "Roofing (B3010)",
      "recommended_bidder": "Rolvin Carpentry",
      "rationale": "On overlapping scope (roofing only), Rolvin is $35,000 vs Perry $110,250 — 68% less"
    },
    {
      "scope": "Exterior Walls (B2010), Drainage (D2040)",
      "recommended_bidder": "Rolvin Carpentry",
      "rationale": "Only Rolvin covers these scopes; Perry does not quote exterior walls or drainage"
    }
  ],
  "overlap_comparison": {
    "shared_categories": ["B3010 ROOF COVERINGS"],
    "overlap_totals": {"Perry Verrone LLC": 110250.00, "Rolvin Carpentry Inc": 35000.00},
    "notes": "Perry's total ($110,250) appears lower than Rolvin's ($140,000) but Perry only covers roofing. On the shared scope, Rolvin is 68% cheaper."
  },
  "scope_overlap": [
    {"description": "Roof coverings", "uniformat_code": "B3010", "bidders": {"Perry Verrone LLC": true, "Rolvin Carpentry Inc": true}},
    {"description": "Exterior walls", "uniformat_code": "B2010", "bidders": {"Perry Verrone LLC": false, "Rolvin Carpentry Inc": true}},
    {"description": "Rain water drainage", "uniformat_code": "D2040", "bidders": {"Perry Verrone LLC": false, "Rolvin Carpentry Inc": true}}
  ],
  "bidders": [
    {
      "name": "ABC Plumbing",
      "brief_summary": "Comprehensive bid at $34,300 — fixtures, heater, waste, drainage",
      "total_cost": 34300.00,
      "unit_cost": 2450.00,
      "scope_differences": [
        "Includes rain water drainage (D2040) — XYZ excludes",
        "Water heater $4,500 vs XYZ $5,200 for domestic water"
      ],
      "duration_and_schedule": ["6-8 weeks", "Monthly progress billing, Net 30"],
      "preconditions": ["Framing + rough electrical complete", "Slab on grade poured"],
      "substantial_completion": ["All fixtures operational", "Pressure test passed"],
      "lien_waiver_requirements": ["Conditional with each progress payment", "Unconditional at final"],
      "qualifications": ["CA License #987654 (C-36)", "$2M GL, $1M auto"],
      "exclusions_and_terms": ["Excludes permits/inspections", "10% retainage, released at final"]
    }
  ]
}
```

The schema supports two recommendation styles:
- **Single recommendation**: When overlap is high, use a single entry in `recommendations`
- **Per-scope recommendations**: When scopes diverge, make separate recommendations per UniFormat area

The `overlap_comparison` object shows the apples-to-apples subtotals for shared categories and a note explaining why total comparison is misleading. Use this when grand totals would give a false impression.

### Scope Overlap Matrix

The `scope_overlap` array drives the PDF's page-1 comparison table. Enumerate scopes **more granularly than the CSV** to show exactly what each bidder includes/excludes. Tag each with a UniFormat code. Make a best effort to interpret which line items across bids are equivalent.

### Recommendation Logic

**Never compare totals across bids with different scopes.** A lower total does not mean a better price if the bidder covers less work.

#### Step 1: Identify overlapping vs. non-overlapping scope

Using the scope overlap matrix, separate line items into:
- **Overlapping**: Both bidders include this scope (apples-to-apples)
- **Unique to Bidder A**: Only one bidder covers this
- **Unique to Bidder B**: Only the other bidder covers this

#### Step 2: Compare on overlapping scope only

Compute an **overlap-only subtotal** for each bidder — the sum of costs for only the UniFormat categories both bidders cover. Compare bidders on this number, not on their grand totals.

Example: If Bidder A quotes roofing at $110,250 and Bidder B quotes roofing at $35,000 + exterior walls at $93,333 + drainage at $11,667, the apples-to-apples comparison for roofing is $110,250 vs. $35,000 — Bidder B is dramatically cheaper on the shared scope, even though their total is higher.

#### Step 3: Make scope-aware recommendations

- **High overlap (>70% of line items shared)**: Make a single recommendation based on overlapping cost comparison, thoroughness, and contractual terms
- **Partial overlap**: Make **separate recommendations per scope area** when appropriate (e.g., "For roofing, Bidder B is significantly cheaper; Bidder A does not cover exterior walls or drainage")
- **Minimal overlap (<30% shared)**: Do **not** recommend one bidder over the other — state that the scopes are too different to compare directly and describe what each covers

#### Step 4: Factor in unique scope

When one bidder includes scope the other doesn't, call this out explicitly:
- What would the owner need to procure separately?
- Does the additional scope justify a higher total?

#### Weights (for overlapping scope)

1. **Apples-to-apples price** — cost for overlapping categories only
2. **Scope completeness** — additional coverage reduces separate procurement
3. **Contractual clarity** — clear terms, reasonable conditions, adequate insurance

## Step 7: Generate Spreadsheet

**CSV:**
```bash
uv run scripts/generate_csv.py bid_data.json bid_level.csv
```

**New Excel file:**
```bash
uv run scripts/generate_csv.py bid_data.json bid_level.xlsx
```

**Add sheet to existing Excel file:**
```bash
uv run scripts/generate_csv.py bid_data.json bid_level.xlsx existing_workbook.xlsx
```

Output format is detected from file extension. The script reads `references/uniformat_headings.csv` automatically.

## Step 8: Generate PDF

```bash
uv run scripts/generate_pdf.py analysis.json bid_level.pdf
```

The PDF is structured as:
- **Page 1**: Project info, recommendation, bid summary table, scope overlap matrix with checkmarks
- **Page 2+**: Per-bidder details as concise bulleted lists (scope diffs, schedule, preconditions, completion, lien waivers, qualifications, exclusions)

## Resources

- `references/uniformat_headings.csv` — Full UniFormat II Level 1/2/3 heading hierarchy
- `references/bid-analysis-guide.md` — Extraction guide for bid documents and contractual terms
- `scripts/generate_csv.py` — Spreadsheet generation (CSV or Excel) from bid data JSON
- `scripts/generate_pdf.py` — PDF report generation from analysis JSON
