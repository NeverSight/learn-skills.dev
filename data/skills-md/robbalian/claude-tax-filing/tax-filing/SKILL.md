---
name: tax-filing
description: Prepare and fill federal and state tax return PDF forms
user_invocable: true
triggers:
  - do my taxes
  - prepare tax return
  - fill tax forms
  - file taxes
  - tax preparation
---

# Tax Filing Skill

Prepare federal and state income tax returns: read source documents, compute taxes, fill official PDF forms.

**Year-agnostic** — always look up current-year brackets, deductions, and credits. Never reuse prior-year values.

## Folder Structure

Organize all work into subfolders of the working directory:

```
working_dir/
  source/              ← user's source documents (W-2, 1099s, prior return, CSVs)
  work/                ← ALL intermediate files (extracted data, field maps, computations)
    tax_data.txt       ← extracted figures from source docs
    computations.txt   ← all tax math (federal, state, capital gains)
    f1040_fields.json  ← field discovery dumps
    f8949_fields.json
    f1040sd_fields.json
    ca540_fields.json
    expected_*.json    ← verification expected values
  forms/               ← blank downloaded PDF forms
    f1040_blank.pdf
    f8949_blank.pdf
    f1040sd_blank.pdf
    ca540_blank.pdf
  output/              ← final filled PDFs + fill script
    fill_YEAR.py       ← the fill script
    f1040_filled.pdf
    f8949_filled.pdf
    f1040sd_filled.pdf
    ca540_filled.pdf
```

Create these folders at the start. Keep the working directory clean — no loose files.

## Context Budget Rules

These rules prevent context blowouts that cause compaction:

1. **NEVER read PDFs with the Read tool.** Each page becomes ~250KB of base64 images (a 9-page return = 1.8 MB). Extract text instead:
   ```bash
   python3 -c "
   import pdfplumber
   with pdfplumber.open('source/document.pdf') as pdf:
       for p in pdf.pages: print(p.extract_text())
   "
   ```
2. **NEVER read the same document twice.** Save extracted figures to `work/tax_data.txt` on first read.
3. **Run field discovery ONCE per form** as a bulk JSON dump to `work/`. Do NOT use `--search` repeatedly.
4. **Save all computed values to `work/computations.txt`** so they survive compaction.

## Workflow

### Step 1: Gather Source Documents

Ask the user what documents they have. Read files from `source/` (move them there if needed). Use pdfplumber for PDFs, Read tool for CSVs.

Save all extracted figures to `work/tax_data.txt` immediately — one section per document with every relevant number.

### Step 2: Confirm Filing Details — MANDATORY

**You MUST ask the user every one of these questions and WAIT for answers before proceeding.** Do NOT skip this step even if you think you know the answers from memory or source documents. Tax returns are legal documents.

- Filing status (Single, MFJ, MFS, HOH, QSS)
- Dependents (number, names)
- State of residence
- Standard vs. itemized deduction preference
- Digital asset / cryptocurrency transactions (Yes/No) — stock trades are NOT digital assets
- Health coverage status (for CA)
- Any estimated tax payments made
- Any other credits or adjustments

**Do NOT proceed to Step 3 until the user has answered.** "Same as last year" counts as confirmation.

### Step 3: Look Up Year-Specific Values

Research from IRS.gov and FTB.ca.gov:
- Federal tax brackets, standard deduction, QDCG 0%/15%/20% thresholds
- State tax brackets, standard deduction, personal exemption credit

Save to `work/computations.txt`.

### Step 4: Compute Federal Return

1. Gross Income: W-2 wages (1a) + interest (2b) + dividends (3b) + capital gain/loss (7)
2. Adjustments → AGI (Line 11)
3. Deductions → Taxable Income (Line 15)
4. Tax: use QDCG worksheet if qualified dividends/capital gains exist
5. Credits, other taxes → Total Tax (Line 24)
6. Payments (withholding, estimated) → Refund/Owed
7. If refund: collect direct deposit info (routing, account, type)

Save all line values to `work/computations.txt`.

### Step 5: Compute Capital Gains (if applicable)

1. Form 8949: individual transactions (Part I short-term, Part II long-term)
2. Schedule D: totals, $3,000 loss limitation, carryover calculation
3. Net gain/loss → 1040 Line 7

### Step 6: Compute State Return (CA Form 540)

1. Federal AGI → CA adjustments → CA taxable income
2. Tax from brackets − exemption credits → total tax
3. Withholding → Refund/Owed

### Step 7: Download Blank PDF Forms

Save to `forms/` directory.

**IRS**: Use `/irs-prior/` for prior-year forms (`/irs-pdf/` is always current year):
```
https://www.irs.gov/pub/irs-prior/f1040--YEAR.pdf
https://www.irs.gov/pub/irs-prior/f8949--YEAR.pdf
https://www.irs.gov/pub/irs-prior/f1040sd--YEAR.pdf
```

**CA**: `ftb.ca.gov/forms/YEAR/` for state forms.

Verify each download has `%PDF-` header (not an HTML error page).

### Step 8: Discover Field Names & Fill Forms

#### Discovery — ONCE per form, use `--compact`

```bash
python scripts/discover_fields.py forms/f1040_blank.pdf --compact > work/f1040_fields.json
python scripts/discover_fields.py forms/f8949_blank.pdf --compact > work/f8949_fields.json
python scripts/discover_fields.py forms/f1040sd_blank.pdf --compact > work/f1040sd_fields.json
python scripts/discover_fields.py forms/ca540_blank.pdf --compact > work/ca540_fields.json
```

`--compact` outputs a minimal `{field_name: description}` mapping — each field name is paired with its tooltip/speak description so you can map line numbers to field names directly without manual inspection. Radio buttons include their option values (e.g. `{"/2": "Single", "/1": "MFJ"}`).

Do NOT use `--search` repeatedly or `--json` (which dumps raw metadata and wastes context).

**HARD FAIL**: If discovery returns 0 human-readable descriptions, STOP. Do not guess field names.

#### Fill Script

Write `output/fill_YEAR.py` using `scripts/fill_forms.py`:

- **`add_suffix(d)`** — appends `[0]` to text field keys. Required for IRS forms.
- **`fill_irs_pdf(in, out, fields, checkboxes, radio_values)`** — IRS forms. `radio_values` for filing status, yes/no, checking/savings.
- **`fill_pdf(in, out, fields, checkboxes)`** — CA forms. Matches by `/Parent` chain + `/AP/N` keys.

Output filled PDFs to `output/`.

### Step 9: Verify

```bash
python scripts/verify_filled.py output/f1040_filled.pdf work/expected_f1040.json
```

Fix any failures, re-run fill script.

### Step 10: Present Results

Show a summary table, verification checklist, capital loss carryover (if any), then:

- **Sign your returns** — unsigned returns are rejected
- **Payment instructions** (if owed) — IRS Direct Pay, FTB Web Pay, deadline April 15
- **Direct deposit** — recommend it for refunds; ask for bank info if not provided
- **Filing options** — e-file (Free File, CalFile) or mailing addresses

## Key Gotchas

### Context
- NEVER use Read tool on PDFs — use pdfplumber
- NEVER read same document twice — save to `work/tax_data.txt`
- Field discovery once per form with `--compact` — no `--json` (wastes context), no repeated `--search`

### Field Discovery
- Field names change between years — always discover fresh
- XFA template is in `/AcroForm` → `/XFA` array, NOT from brute-force xref scanning
- Do NOT use `xml.etree` for XFA — use regex (IRS XML has broken namespaces)

### PDF Filling
- Remove XFA from AcroForm, set NeedAppearances=True, use auto_regenerate=False
- Checkboxes: set both `/V` and `/AS` to `/1` or `/Off`
- IRS fields need `[0]` suffix — use `add_suffix()`
- IRS checkboxes match by `/T` directly; radio groups match by `/AP/N` key via `radio_values`

### Form-Specific
- **1040**: First few fields (`f1_01`-`f1_03`) are fiscal year headers, not name fields. SSN = 9 digits, no dashes. Digital assets = crypto only, not stocks.
- **8949**: Box A/B/C checkboxes are 3-way radio buttons. Totals at high field numbers (e.g. `f1_115`-`f1_119`), not after last data row. Schedule D lines 1b/8b (from 8949), not 1a/8a.
- **Schedule D**: Some fields have `_RO` suffix (read-only) — skip those.
- **CA 540**: Field names are `540-PPNN` (page+sequence, NOT line numbers). Checkboxes end with `" CB"`, radio buttons use named AP keys.
- **Downloads**: Prior-year IRS = `irs.gov/pub/irs-prior/`, current = `irs.gov/pub/irs-pdf/`
