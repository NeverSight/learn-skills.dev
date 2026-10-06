---
name: py-covert-scan
description: "Detect covert/evasive tactics in Python: hidden code execution (exec/eval/compile of base64/hex/zlib/marshal output, pickle deserialization, dynamic import, chr()/\\x string building), environment-keyed evasion (platform/VM/sandbox/analyst detection, timezone/locale, debugger/tracer checks), and Unicode steganography. Emits judgment-free parallax atoms (XFRM.UNICODE / XFRM.ENCODE / LOAD.EVAL / LOAD.DESER / LOAD.REFLECT / ENVI.ENVCHECK / ENVI.SANDBOX / ENVI.DEBUG), each tagged method=\"covert-scan\" so the consumer's lens makes the obfuscation/evasion call by provenance, and flags family co-occurrence. Static and read-only."
---

# Python Covert-Tactics Scanner

The Python sibling of `js-covert-scan`: detect the tactics Python code uses to hide
what it does, and emit atoms. Static, read-only, pure-stdlib.

## When to use

A `.py` (or a package, or source recovered by `pyc-decompile`) that might be a
dropper or be behaving differently under analysis. This surfaces the *tactics*; it
doesn't decide intent.

## What it detects — real parallax atoms, tagged `method="covert-scan"`

Every finding is emitted as a **judgment-free parallax atom** with `method:
"covert-scan"`; the downstream lens makes the obfuscation/evasion judgment from that
provenance. The per-tactic `note` preserves exactly which tactic was seen (so a
`LOAD.EVAL` finding still says "decode-then-execute" vs plain "exec()/eval()", and a
`LOAD.DESER` finding still says "marshalled code object" vs "pickle deserialization").

**LOAD.EVAL / LOAD.DESER / LOAD.REFLECT** — hidden code execution (the hallmark of
Python malware):
- `LOAD.EVAL` — decode-then-execute (`exec`/`eval`/`compile` fed by
  `base64`/`hex`/`zlib`/`gzip`/`lzma`/`marshal` output — **the strongest single
  tell**), and plain `exec()` / `eval()`.
- `LOAD.DESER` — `marshal.loads` (marshalled code object) and `pickle.load(s)`
  (deserialization can execute code).
- `LOAD.REFLECT` — `__import__()` / `getattr(__builtins__, …)` / `importlib`.

**XFRM.ENCODE** — strings built from `chr()` / long `\xNN` escapes.

**ENVI.ENVCHECK / ENVI.SANDBOX / ENVI.DEBUG** — environment-keyed / anti-analysis:
- `ENVI.ENVCHECK` — platform branching (`sys.platform` / `platform.system()`) and
  timezone/locale checks (`time.tzname` / `locale.getlocale` / `ZoneInfo`).
- `ENVI.SANDBOX` — VM/sandbox/analyst detection (`gethostname`, `getpass.getuser`,
  `/sys/class/dmi`, VMware/VirtualBox/QEMU markers).
- `ENVI.DEBUG` — debugger/tracer detection (`sys.gettrace()` / `ptrace` /
  `IsDebuggerPresent`).

**XFRM.UNICODE** — invisible/zero-width/bidi chars and confusable-homoglyph
punctuation/letters (same detection as the JS scanner — it's about the source bytes).

**Combination is the signal.** Decode-then-exec next to a sandbox check is an evasive
dropper; the scan reports a co-occurrence `assessment` across families.

## Usage

```bash
rekit run py-covert-scan ./setup.py
rekit run py-covert-scan ./package --format json
```

JSON: `{filesScanned, findingCount, summary, families, assessment, findings:[{atom,
family, method:"covert-scan", confidence, file, line, col, snippet, note}]}` — the
atoms are the real XFRM/LOAD/ENVI parallax atoms; `method="covert-scan"` lets the
consumer's lens make the obfuscation/evasion judgment.

## Prerequisites

- **python3 ≥ 3.8** — pure stdlib, nothing to vendor.
