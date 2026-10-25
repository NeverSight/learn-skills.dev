---
name: orthotect-gates
description: Execute deterministic quality gates to verify contrast, logical properties, state machines, and core web vitals budgets before merging.
---

# Skill: Orthotect Deterministic Quality Gates

Execute the full suite of quality gates against your project to mathematically verify code integrity.

## Commands
```bash
# Run all quality gates
python3 gates/run_all_gates.py

# Run individual gate
python3 gates/gate_contrast_wcag.py
python3 gates/gate_bidi_logical.py <path>
python3 gates/gate_fsm_integrity.py
python3 gates/gate_no_slop.py <path>
node gates/gate_cwv_budget.mjs <path>
```
