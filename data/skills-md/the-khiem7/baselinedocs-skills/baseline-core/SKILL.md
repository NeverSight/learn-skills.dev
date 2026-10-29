---
name: baseline-core
description: Shared rules for the baselinedocs skills - the pack contract, the report style, and the pack check script. Installed beside every baselinedocs skill, which reads it. Not a workflow and not for direct use.
version: "3.3.0"
---

# Baseline Core

The single home of what every `baselinedocs-*` skill reads: `references/pack-contract.md` (which document owns which content), `references/report-style.md` (how a report names pack elements), and `scripts/packtool.sh` (`outline`, `find`, `next-id`, `close-plan`, `check`). The other skills point here and ship no copy.

If the user invoked this skill directly, there is nothing to run: name the `baselinedocs` skill that fits their request, or `baselinedocs-help` when unsure.

## Non-Goals

- not a workflow: it reads and writes no pack
- not self-contained when moved: every `baselinedocs-*` skill expects this folder beside its own
