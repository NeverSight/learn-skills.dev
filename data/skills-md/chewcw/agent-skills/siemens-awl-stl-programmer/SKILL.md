---
name: siemens-awl-stl-programmer
description: Generate Siemens S7-300/S7-400/S7-1500 Statement List (STL/AWL) programs compatible with Step7 Classic and TIA Portal. Use this skill whenever the user asks to write, generate, create, or modify any PLC logic, function blocks, organization blocks, data blocks, or control programs in STL/AWL format. Also trigger for any questions about Siemens S7 memory addressing, timers, counters, accumulators, block structure, or Step7/TIA Portal imports. Always use this skill even if the user just mentions "STL", "AWL", "Step7", "TIA Portal", "S7-300", "S7-400", "S7-1500", "PLC block", "OB", "FB", "FC", or "DB".
metadata:
  version: "1.0"
---

# Siemens S7 STL (AWL) Programming Skill

## Overview

Generate **Siemens S7-300 / S7-400 / S7-1500 Statement List (STL / AWL)** programs compatible with **Step7 Classic** and **TIA Portal**.

Core model knowledge:
- Accumulator-based execution (ACCU1 / ACCU2)
- RLO (Result of Logic Operation) for boolean logic
- S5 timers, IEC timers (TON/TOF/TP), counters, INT and REAL arithmetic
- OB / FB / FC / DB block hierarchy
- Standard scan cycle model (Read → Execute → Write)

For full instruction syntax, see [references/STL_Core_Instructions.md](references/STL_Core_Instructions.md).

---

## Critical Rule: Omit Block Number (`NAME`) Line

**Always omit the `NAME : '<number>'` line** unless the user specifically requests a fixed block number. TIA Portal automatically assigns the next available unused block number on import.

---

## Block Structure

### Organization Block (OB)

```
ORGANIZATION_BLOCK "OB1"
TITLE = Main Program Cycle
{ S7_Optimized_Access := 'TRUE' }
VERSION : 0.1

VAR_TEMP
      TempVar : Int;
END_VAR

BEGIN
NETWORK
TITLE = Example Network
      L     PIW256;
      T     #TempVar;
END_ORGANIZATION_BLOCK
```

### Function (FC) — Stateless

```
FUNCTION "FC_Name" : Void
{ S7_Optimized_Access := 'TRUE' }
VERSION : 0.1

VAR_INPUT
    IN : Int;
END_VAR

VAR_OUTPUT
    OUT : Real;
END_VAR

BEGIN
NETWORK
TITLE = Convert and Scale
      L     #IN;
      ITD;
      DTR;
      T     #OUT;
END_FUNCTION
```

### Function Block (FB) — Stateful

```
FUNCTION_BLOCK "FB_Name"
{ S7_Optimized_Access := 'TRUE' }
VERSION : 0.1

VAR_INPUT
    StartPB : BOOL;
    StopPB  : BOOL;
END_VAR

VAR_OUTPUT
    MotorOut : BOOL;
END_VAR

VAR
    RunLatch : BOOL;
    Delay    : TON;
END_VAR

BEGIN
NETWORK
TITLE = Start Latch
      A     #StartPB;
      AN    #StopPB;
      S     #RunLatch;

NETWORK
TITLE = Output
      A     #RunLatch;
      =     #MotorOut;
END_FUNCTION_BLOCK
```

### Data Block (DB)

```
DATA_BLOCK "DB_Name"
{ S7_Optimized_Access := 'TRUE' }
VERSION : 0.1
NON_RETAIN

VAR
    Value : Int;
END_VAR

BEGIN
END_DATA_BLOCK
```

---

## Key Formatting Rules

- Always include `{ S7_Optimized_Access := 'TRUE' }` after block keyword
- Use symbolic quoted names (`"BlockName"`) — never numeric references
- Prefix local variables with `#` (e.g., `#StartPB`)
- Each instruction ends with `;`
- Use `NETWORK` + `TITLE = ...` + `// comment` for each logical group

**Timer Selection:**
- Inside FC: Use S5 timers (`SE`, `SP`, `SD`, `SA`, `SS`)
- Inside FB: Use IEC timers (`TON`, `TOF`, `TP`)

---

## Code Generation Constraints

**MUST:**
- Use symbolic quoted names for all block references
- Generate complete, compilable blocks
- Separate logical groups into individual NETWORKs
- Use uppercase STL mnemonics (A, AN, O, =, S, R, L, T, FP, ITD, DTR, etc.)
- Generate matching instance DB when generating an FB

**MUST NOT:**
- Mix LAD, SCL, or non-STL syntax
- Use numeric-only block references unless user explicitly requests
- Include `NAME : '<number>'` in generated blocks

---

## When to Consult Documentation

If the user's request involves instructions or patterns **not covered here**, consult:

- **TIA Portal STL Reference:** `https://docs.tia.siemens.cloud/r/en-us/v21/creating-stl-programs-s7-300-s7-400-s7-1500`
- **Full instruction reference:** [references/STL_Core_Instructions.md](references/STL_Core_Instructions.md)
- **Block templates:** [references/REFERENCE.md](references/REFERENCE.md)
- **Formatting rules:** [references/FORMATTING.md](references/FORMATTING.md)

Typical cases requiring documentation lookup:
- Interrupt OBs (OB35, OB40, OB80) and their startup VAR_TEMP
- System function calls (SFC, SFB) such as `CALL SFC14`
- String handling, DATE_AND_TIME types
- `BLKMOV`, `FILL`, `UBLKMOV` block move instructions
- Less common accumulator operations (`CAD`, `CAW`, `TAK`, `PUSH`, `POP`)