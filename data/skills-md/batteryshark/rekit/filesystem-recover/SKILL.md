---
name: filesystem-recover
description: "Recover allocated, deleted, or all files from an ext, NTFS, FAT, or other Sleuth Kit-supported filesystem at an explicit image sector offset. Use after disk-image-scan validates a filesystem start. Runs tsk_recover without mounting the source, emits an fls metadata-address/MFT record-to-name map, safely renames unambiguous OrphanFile-record placeholders from surviving metadata, and hashes recovered files."
---

# Filesystem Recovery

Recover through Sleuth Kit without mounting the evidence image. The output directory must
be new or empty; recovered files go beneath `files/`, while logs and `manifest.jsonl`
remain separate.

## Workflow

1. Run `disk-image-scan` and verify the candidate filesystem offset.
2. Use the candidate's `lba512` or `inferredStartLba` as `--offset`. Sleuth Kit offsets
   are sector counts, not byte offsets.
3. Select provenance explicitly:
   - `allocated`: named allocated files (`tsk_recover -a`);
   - `deleted`: recoverable unallocated files (Sleuth Kit default);
   - `all`: allocated and deleted files (`tsk_recover -e`).

```bash
bin/rekit run filesystem-recover evidence.img ./forensics/partition-1 \
  --offset 1590435 --mode all
```

4. Preserve `recovery.json`, `tsk-recover.stdout.log`,
   `tsk-recover.stderr.log`, `metadata-names.jsonl`, `metadata-renames.jsonl`, and
   `manifest.jsonl`. The manifest hashes every recovered regular file unless `--no-hash`
   is set.
5. Compare recovered trees with `intellidiff folder-compare ... --binary`. Analyse
   recovered artifacts with the format-specific Rekit skills; never execute them merely
   because recovery succeeded.

## NTFS MFT names

Keep metadata naming enabled by default. `tsk_recover` writes paths exposed by the
filesystem. The runner also invokes `fls -r -p` and records every Sleuth Kit metadata
address; for NTFS, the first numeric component is the MFT record number.

When recovery produces `$OrphanFiles/OrphanFile-<record>`, rename it only if the same MFT
record has exactly one safe, non-reallocated regular-file path in the `fls` results.
Record ambiguous names, collisions, unsafe paths, and missing names without guessing or
overwriting another recovered file. Use `--no-metadata-names` only when explicitly
accepting the loss of this map and rename pass. Bound the parsed map with
`--max-name-records`.

Use `--fstype` only when Sleuth Kit auto-detection is wrong. `--sector-size` describes the
device sector size used by Sleuth Kit; `--offset` is still counted in those sectors.
Timeout and manifest-file limits are bounded and reported honestly.
