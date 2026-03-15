---
name: symbol-datestamp-correction
description: Correct NSE and MCX symbol formats and datestamp conversions for OpenAlgo. Standardizes expiry dates to DD-MMM-YY format, constructs proper futures/options symbols, and validates symbol structure. Use when processing broker data, fixing symbol format errors, converting dates, or validating trading symbols.
---

# NSE and MCX Symbol and Datestamp Correction

## Quick Start

When correcting symbols and datestamps:

1. **Convert expiry dates** to OpenAlgo format: `DD-MMM-YY` (e.g., `28-MAR-24`)
2. **Construct symbols** using correct format based on exchange and instrument type
3. **Validate** symbol structure matches OpenAlgo standards
4. **Format strike prices** (remove `.0`, keep decimals like `292.5`)

## Date Format Standards

### Database Expiry Format
- **Format**: `DD-MMM-YY` (with hyphens)
- **Example**: `28-MAR-24`, `15-APR-25`
- **Use**: Stored in database `expiry` column

### Symbol Expiry Format
- **Format**: `DDMMMYY` (no hyphens, uppercase)
- **Example**: `28MAR24`, `15APR25`
- **Use**: Embedded in trading symbols

## Date Conversion

Convert various input formats to `DD-MMM-YY`:

```python
from datetime import datetime
import pandas as pd

def convert_date_format(date_str):
    """Convert date from various formats to DD-MMM-YY format (e.g., 26-FEB-24)."""
    if pd.isnull(date_str) or date_str == "" or date_str is None:
        return None
    
    try:
        date_str = str(date_str).strip()
        
        # Try different date formats (order matters - try most specific first)
        date_formats = [
            "%Y-%m-%d",      # 2024-02-26
            "%d-%m-%Y",      # 26-02-2024
            "%d/%m/%Y",      # 26/02/2024
            "%d/%m/%y",      # 26/02/24
            "%y/%m/%d",      # 24/02/26
            "%d%b%Y",        # 26FEB2024
            "%d%b%y",        # 26FEB24
            "%Y%m%d",        # 20240226
            "%d-%b-%Y",      # 26-FEB-2024
            "%d-%b-%y",      # 26-FEB-24
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt).strftime("%d-%b-%y").upper()
            except ValueError:
                continue
        
        # If already in correct format, just uppercase it
        return date_str.upper()
    except Exception:
        return str(date_str).upper() if date_str else None
```

## Symbol Format Standards

### NSE/NFO Futures
- **Format**: `NAME + EXPIRY(no dashes) + FUT`
- **Example**: `BANKNIFTY26FEB24FUT`, `NIFTY30JAN25FUT`
- **Pattern**: `[A-Z]+[0-9]{2}[A-Z]{3}[0-9]{2}FUT`

### NSE/NFO Options
- **Format**: `NAME + EXPIRY(no dashes) + STRIKE + CE/PE`
- **Example**: `NIFTY26FEB241480CE`, `BANKNIFTY30JAN2525000PE`
- **Pattern**: `[A-Z]+[0-9]{2}[A-Z]{3}[0-9]{2}[0-9]+(CE|PE)`

### MCX Futures
- **Format**: `NAME + EXPIRY(no dashes) + FUT`
- **Example**: `GOLD28NOV24FUT`, `CRUDEOILM20MAY24FUT`
- **Pattern**: `[A-Z]+[0-9]{2}[A-Z]{3}[0-9]{2}FUT`

### MCX Options
- **Format**: `NAME + EXPIRY(no dashes) + STRIKE + CE/PE`
- **Example**: `GOLD28NOV2472000CE`, `SILVER15APR2585000PE`
- **Pattern**: `[A-Z]+[0-9]{2}[A-Z]{3}[0-9]{2}[0-9]+(CE|PE)`

## Symbol Construction

### For Futures
```python
# Convert expiry to symbol format (remove hyphens)
expiry_for_symbol = expiry.str.replace("-", "", regex=False).str.upper()

# Construct symbol
symbol = name + expiry_for_symbol + "FUT"
```

### For Options
```python
# Format strike price (remove .0, keep decimals)
def format_strike(strike_series):
    return strike_series.astype(str).str.replace(r"\.0$", "", regex=True)

# Convert expiry to symbol format
expiry_for_symbol = expiry.str.replace("-", "", regex=False).str.upper()

# Construct symbol
symbol = name + expiry_for_symbol + format_strike(strike) + instrumenttype  # CE or PE
```

## Common Corrections

### Exchange Mapping
```python
# Map MFO (MCX Futures & Options) to MCX
df.loc[df["exchange"] == "MFO", "exchange"] = "MCX"
```

### Equity Symbol Cleanup
```python
# Remove broker suffixes (-EQ, -BE, -MF, -SG)
df.loc[df["instrumenttype"] == "EQ", "symbol"] = df["symbol"].str.replace(
    "-EQ|-BE|-MF|-SG", "", regex=True
)
```

### Strike Price Formatting
```python
# Keep decimals like 292.5, remove .0
def format_strike(strike_series):
    return strike_series.astype(str).str.replace(r"\.0$", "", regex=True)
```

## Validation Checklist

When correcting symbols and datestamps:

- [ ] Expiry date is in `DD-MMM-YY` format for database
- [ ] Symbol expiry uses `DDMMMYY` (no hyphens) format
- [ ] Futures symbols end with `FUT`
- [ ] Options symbols end with `CE` or `PE`
- [ ] Strike prices formatted correctly (no trailing `.0`)
- [ ] Exchange codes are correct (NFO, MCX, not MFO)
- [ ] Equity symbols don't have broker suffixes
- [ ] All dates are uppercase
- [ ] Month abbreviations are valid (JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC)

## Example Corrections

### Date Conversion
```
Input:  "2024-02-26"     → Output: "26-FEB-24"
Input:  "26/02/2024"     → Output: "26-FEB-24"
Input:  "26FEB2024"      → Output: "26-FEB-24"
Input:  "26FEB24"        → Output: "26-FEB-24"
Input:  "26-FEB-24"      → Output: "26-FEB-24" (already correct)
```

### Symbol Construction
```
Name: "NIFTY", Expiry: "26-FEB-24", Strike: 24000, Type: "CE"
→ Symbol: "NIFTY26FEB2424000CE"

Name: "BANKNIFTY", Expiry: "30-JAN-25", Type: "FUT"
→ Symbol: "BANKNIFTY30JAN25FUT"

Name: "GOLD", Expiry: "28-NOV-24", Strike: 72000, Type: "PE"
→ Symbol: "GOLD28NOV2472000PE"
```

### Common Fixes
```
"BANKNIFTY26FEB24"           → "BANKNIFTY26FEB24FUT" (missing FUT)
"NIFTY26FEB24-24000CE"       → "NIFTY26FEB2424000CE" (extra hyphen)
"GOLD28-NOV-2472000CE"       → "GOLD28NOV2472000CE" (hyphens in expiry)
"INFY-EQ"                    → "INFY" (remove broker suffix)
"24000.0"                    → "24000" (remove .0)
"292.5"                      → "292.5" (keep decimal)
```

## Pandas DataFrame Processing

When processing broker data:

```python
import pandas as pd

# 1. Convert expiry dates
df["expiry"] = df["expiry"].apply(convert_date_format)

# 2. Format strike prices
def format_strike(strike_series):
    return strike_series.astype(str).str.replace(r"\.0$", "", regex=True)

# 3. Get expiry without dashes for symbol construction
expiry_for_symbol = df["expiry"].fillna("").str.replace("-", "", regex=False).str.upper()

# 4. Construct futures symbols
fut_mask = df["instrumenttype"].isin(["FUTIDX", "FUTSTK", "FUT"])
df.loc[fut_mask, "symbol"] = df["name"].fillna("") + expiry_for_symbol + "FUT"

# 5. Construct options symbols
opt_mask = df["instrumenttype"].isin(["OPTIDX", "OPTSTK", "CE", "PE"])
df.loc[opt_mask, "symbol"] = (
    df["name"].fillna("") + expiry_for_symbol + format_strike(df["strike"]) + df["instrumenttype"]
)
```

## Error Detection

Common errors to watch for:

1. **Missing FUT suffix**: `BANKNIFTY26FEB24` → should be `BANKNIFTY26FEB24FUT`
2. **Hyphens in symbol expiry**: `NIFTY26-FEB-24FUT` → should be `NIFTY26FEB24FUT`
3. **Wrong date format**: `26/02/2024` → should be `26-FEB-24` in database
4. **Trailing .0 in strike**: `24000.0` → should be `24000` in symbol
5. **Broker suffixes**: `INFY-EQ` → should be `INFY`
6. **Wrong exchange**: `MFO` → should be `MCX`
7. **Invalid month**: `26XYZ24` → month must be valid 3-letter abbreviation
