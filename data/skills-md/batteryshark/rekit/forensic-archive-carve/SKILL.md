---
name: forensic-archive-carve
description: "Recover structurally complete classic ZIP and RAR4 archives from raw disk images or media blobs, preserving absolute byte offsets, SHA-256 identities, validation method, and duplicate relationships in a JSONL manifest. Use after disk-image-scan or for direct archive carving from unallocated space. Pure Python; reads the source image without mounting or modifying it."
---

# Forensic Archive Carver

Carve archive byte ranges only after their framing has been validated. This is narrower
and more evidence-oriented than `binwalk-carve`: it records exact source offsets and
content identities instead of recursively invoking a broad extractor ecosystem.

## Workflow

1. Run `disk-image-scan` and retain its `scan.jsonl`.
2. Carve from that hit set:

```bash
bin/rekit run forensic-archive-carve evidence.img ./forensics/archives \
  --hits ./forensics/scan/scan.jsonl
```

Omit `--hits` to scan the image directly for classic ZIP EOCD and RAR4 signatures.
The output directory must be empty so an earlier recovery cannot be silently mixed with
a new run.

3. Inspect `manifest.jsonl`. Each record includes `start`, `endExclusive`, `size`,
`sha256`, structural validation details, and `duplicateOf` when another carved range has
identical bytes.
4. Treat carving and archive extraction as separate evidence steps. Use `unpack` on a
copy or dedicated output directory; retain the original carved bytes and manifest.

Classic ZIP and RAR4 are supported. ZIP64 and RAR5 signatures are reported as unsupported
rather than guessed. `--max-size` and `--max-candidates` bound reads and output growth.
