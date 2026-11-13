---
name: no-leaky-scan
description: Scan this machine's coding agent transcripts for secrets that already leaked, and walk the user through what to rotate. Run when the user types /no-leaky-scan or asks whether their agent leaked secrets.
disable-model-invocation: true
---

# /no-leaky-scan

1. Find the scan script: `scripts/scan.py` inside the `no-leaky-secrets` skill folder.
2. Run `python3 <that path> --report no-leaky-report.md`. Add `--since YYYY-MM-DD` if the user named a date. It takes one to two minutes on a few GB of transcripts.
3. The output never holds a value. Do not try to look one up: no grep of the transcripts for a fingerprint's value, no reading of the source file.
4. Walk the user through the report from the top:
   - **Certain**: say how many, then each row: what it is, where it came from, how many sessions, the fix. Group rows that share a provider.
   - **Likely**: these need a human eye. Ask the user to confirm each one is real before they rotate it.
   - **Public by design**: say they need no action.
   - **Coverage**: name any agent marked "not found" so nobody reads the result as "clean everywhere".
5. For rows the user has rotated or ruled out, offer an `ignore` entry in `~/.config/no-leaky/config.json`:
   `{"ignore": [{"fp": "<fp>", "reason": "rotated", "date": "<today>"}]}`. Write it only after they say yes.
6. If the guard hooks are not installed, say what each would have stopped (the "would stop it" column) and offer `python3 <skill dir>/scripts/install.py`.
