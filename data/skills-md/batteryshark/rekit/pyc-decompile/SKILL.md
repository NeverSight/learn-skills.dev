---
name: pyc-decompile
description: "Decompile Python bytecode (.pyc / compiled code objects) back to source with decompyle3. Best for CPython 3.7-3.8 bytecode (e.g. PyInstaller-extracted payloads); reports honestly when the bytecode version is out of range. Static: reads bytecode, never runs it."
---

# Python Bytecode Decompiler

Decompile Python bytecode (`.pyc` / compiled code objects) back to source with
[decompyle3](https://github.com/rocky/python-decompile3).

## When to use

You have compiled Python but not the source: a stray `.pyc`, the `__pycache__` of a
suspicious package, or (most commonly) bytecode carved out of a **PyInstaller** /
py2exe bundle. Decompiling recovers readable source you can then scan for the real
behaviour.

When inventory finds `.pyc` artifacts with no matching source, decompile them and
rescan the recovered `.py`.

## What it does

Reads the bytecode statically (unmarshals the code object, disassembles it) and
reconstructs equivalent Python source. It does **not** import, exec, or run the
`.pyc` — safe on hostile bytecode.

Best on **CPython 3.7–3.8** bytecode (decompyle3's target range). The runner detects
the bytecode's version and tells you whether it's in range; for older bytecode use
`uncompyle6`, and 3.9+ needs a version-matched decompiler.

## Usage

```bash
rekit run pyc-decompile ./payload.pyc ./out
# or
python3 skills/pyc-decompile/scripts/run.py ./payload.pyc ./out
```

Writes `out/decompiled.py` and prints a JSON result:

```json
{"ok": true, "outputFile": "out/decompiled.py", "detectedVersion": "3.8",
 "supported": true, "bytesOut": 412}
```

On an out-of-range or corrupt `.pyc` it fails honestly with the detected version and
a pointer to the right tool — it does not emit a half-guessed decompilation.

## Prerequisites

- **python3 ≥ 3.8** — to run the decompiler. The *target* `.pyc` may be a different
  version; decompyle3 (and its pure-Python deps) is installed under `scripts/site`,
  so no network/install at analysis time.

## Rebuilding the payload

`scripts/site` is populated from a pinned `scripts/requirements.txt` by
`scripts/build.sh` (`uv pip install --target`, build time only). Pure-Python, so the
vendored tree is portable across OS/arch.
