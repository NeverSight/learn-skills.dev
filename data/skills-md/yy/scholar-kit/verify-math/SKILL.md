---
name: verify-math
description: Verify algebra, calculus, identities, equation solving, and nontrivial derivation steps with SymPy. Use when a mathematical result needs programmatic checking.
---

# Verify mathematics with SymPy

Use the bundled script to check nontrivial symbolic transformations. When the user requests a fully audited derivation, verify each substantive step. Do not add tool calls after routine arithmetic or notation changes.

State relevant domains and assumptions before interpreting a result. SymPy may return expressions that are equal only under conditions involving signs, branches, singularities, or parameter values. Report those conditions instead of treating every simplified equality as a universal proof.

## Commands

```bash
# Check two expressions are equal
./verify.py eq "EXPR1" "EXPR2"

# Compute derivative
./verify.py diff "EXPR" [VAR]

# Compute integral
./verify.py int "EXPR" [VAR]

# Simplify/expand expression
./verify.py simp "EXPR"

# Solve equation (EXPR = 0)
./verify.py solve "EXPR" [VAR]
```

> Paths are relative to this skill's directory.

## Expression Syntax

- Powers: `x**2` or `x^2`
- Functions: `sin(x)`, `cos(x)`, `exp(x)`, `log(x)`, `sqrt(x)`
- Pre-defined symbols: `x y z t s n k a b c C`
- Reserved symbols handled: `E I S N O` (treated as variables, not SymPy constants)
