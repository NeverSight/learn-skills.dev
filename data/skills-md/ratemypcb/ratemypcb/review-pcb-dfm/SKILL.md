---
name: review-pcb-dfm
description: Run an evidence-backed, local PCB manufacturing preflight with the RateMyPCB CLI. Use when reviewing KiCad `.kicad_pcb` projects, PCB repositories, fabrication ZIPs, Gerber/drill packages, BOMs, placement files, DFM readiness, pre-release PCB checks, or CI manufacturing gates. Recognize Altium artifacts but do not claim source-aware Altium DRC.
---

# Review PCB DFM

Use the deterministic RateMyPCB CLI as the source of truth. Do not infer geometry,
manufacturing clearance, or checks that the report marks `not_run`.

## Run the review

1. Locate `ratemypcb` on `PATH` or in the repository's release/tooling directory.
2. If it is unavailable, explain that a precompiled RateMyPCB CLI is required
   and ask before downloading anything. After consent, run
   `python3 scripts/install.py` from this skill directory, then use the installed
   path it prints. The installer selects only the current OS/architecture and
   verifies its release SHA-256. Never install system dependencies automatically.
   Never run the installer without explicit consent.
3. Inspect candidate PCB paths without modifying them. If several KiCad boards
   exist, select one only when the request or repository structure is
   unambiguous; otherwise show the CLI's candidates and ask which board to use.
4. Run:

   ```sh
   ratemypcb review <path> --format json --native auto
   ```

5. Treat exit `0` as a completed review, exit `1` as a completed CI-threshold
   failure, exit `2` as invalid or ambiguous input, and exit `3` as an execution
   failure. Parse stdout as JSON for exits `0` and `1`.
6. For a CI request, rerun with the requested threshold, for example
   `--fail-on high`. Do not invent a default organization policy.

## Report results

Lead with the score, verdict, confidence, and strongest active finding. Then
summarize findings in severity order with their evidence and remediation.

Always include:

- checks that passed, need attention, were not run, or lacked input;
- whether native KiCad DRC ran and which version produced it;
- ambiguity or unsupported-format limitations;
- the report's manufacturing disclaimer.

Do not say a board is “DRC clean,” “fab ready,” or “safe to manufacture” when
exact DRC or required evidence did not run. A high score with medium/low
confidence is still a partial review.

Read [references/report-contract.md](references/report-contract.md) when
integrating JSON output, writing automation, or interpreting coverage states.
