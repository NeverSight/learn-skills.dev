---
name: js-string-decode
description: "Statically decode constant-key XOR / charCode string obfuscation in JavaScript so a downstream scanner can read the hidden strings (C2 URLs, victim domains, timezone names, shell commands). Finds decode sites with regex/heuristics — a `String.fromCharCode(x ^ KEY)` / `x ^ KEY` applied over a STATIC encoded literal (int array, string, or `\\xNN`/`\\uNNNN` blob, incl. a `Buffer.from(p,\"base64\")`/`atob(p)` front transform) — resolves KEY when it is a small int literal OR a variable assigned a small int nearby (best-effort constant propagation), applies the XOR, and writes the recovered plaintext to outdir/decoded-strings.js for rescanning. READ-ONLY: reads bytes and does arithmetic; never parses as code or executes the input."
---

# JavaScript Constant-Key String Decoder

Statically recover strings that JavaScript hides with a **constant-key XOR /
charCode** scheme, and write them out as plaintext so a downstream scanner can read
them. Pure-Python stdlib, **read-only** — it never runs a JS engine or executes any
part of the input.

## When to use

A file (often a carved single-file-executable bundle) keeps its telltale strings —
C2 URLs, victim domains, timezone names like `Asia/Shanghai`, shell commands — out
of a plain `strings` dump by XORing each character with a constant byte and
reassembling them with `String.fromCharCode`. `js-covert-scan` *flags* that an XOR /
charCode tactic is present; this skill **decodes** it, statically, and hands the
plaintext back for rescanning.

It is the zero-execution complement to `js-deobfuscate` (which recovers encoded
string arrays by running the decoder inside a sandbox). Reach for this one when the
scheme is the constant-key case and you want no execution at all.

## What it does

`python3 scripts/decode.py <input.js> [outdir]`:

1. **Scan** the JS with regex/heuristics (no JS engine, no execution). It finds
   constant-key XOR/charCode decode sites: a `String.fromCharCode(<x> ^ <KEY>)` or
   `<c> ^ <KEY>` applied over a **static** encoded literal.
2. **Resolve `<KEY>`** when it is a small int literal (`0x91`, `145`) **or** a
   variable assigned a small int nearby (`var kk5=91`) — best-effort constant
   propagation by nearest-preceding assignment (so reused minified names resolve to
   the right scope).
3. **Decode** each site (apply the XOR to the encoded data → plaintext).
4. **Write** the recovered strings to `<outdir>/decoded-strings.js`:
   ```
   // decoded from <input>
   /* key=91 base64/fn:c57 off=4835057 */ "cn,sankuai.com,netease.com,163.com,…"
   ```
   one per line as JS string literals, so the fold rescans it as source and sees the
   plaintext URLs / hostnames / commands.
5. **Emit JSON to stdout** (the default — no flag needed):
   ```json
   {"ok": true, "outputDir": "<abs>", "decoded": [{"key": 91, "count": 2,
     "sample": "cn,sankuai.com,…"}], "siteCount": 2}
   ```
   Nothing to decode → `{"ok": true, "outputDir": "<abs>", "decoded": [], "siteCount": 0}`.
   Bad input → `{"ok": false, "error": "…"}` and a non-zero exit.

## Shapes it handles

- **Decoder function over a parameter**, called with the encoded data (the canonical
  single-file-malware shape), e.g.
  `function c57(H){let $=Buffer.from(H,"base64"),q="";for(let K of $)q+=String.fromCharCode(K^kk5);return q}`
  — including a `Buffer.from(p,"base64")` / `atob(p)` front transform, so the payload
  can be a **base64 blob**. Payloads and keys passed as **variables** are resolved.
- `arr.map(c=>c^KEY)` over an inline int array.
- `s.split('').map((c,i)=>String.fromCharCode(c.charCodeAt(0)^KEY))` over a string.
- `for(const K of DATA) …fromCharCode(K^KEY)` over an inline array or string, and
  `\xNN` / `\uNNNN` **escape blobs** (unescaped before the XOR).

## Usage

```bash
rekit run js-string-decode ./bundle.js ./decoded      # JSON to stdout, file to ./decoded
rekit run js-string-decode ./bundle.js --format text  # human summary, no file
```

## Prerequisites

- **python3 ≥ 3.8** — pure stdlib (`re`, `base64`, `mmap`), nothing to vendor.

## Limits / what it can't do

Custom obfuscation is inherently heuristic. This decoder is deliberately scoped to
the **constant-key** case and best-effort:

- **Constant key only.** A running/keystream XOR (`a.charCodeAt(i) ^ b.charCodeAt(i)`
  where both operands are strings/buffers — RC4/OTP-style) is *not* decoded, by
  design: there is no constant to resolve. Multi-byte or rotating keys are out of
  scope.
- **Simple constant propagation only.** The key/payload variable must be a nearby
  literal assignment. A key computed at runtime, read from config, or built by
  arithmetic won't resolve.
- **Keys 1–255.** Byte-XOR only; key `0` (a no-op) is ignored.
- **Static literals only.** Encoded data must be an inline array/string/base64/escape
  literal or a variable pointing at one — data assembled or fetched at runtime is not
  reachable without execution (use `js-deobfuscate` for that).
- **Regex, not an AST.** Unusual spacing/nesting or exotic decoder shapes can be
  missed; false positives are suppressed by requiring the decode to be mostly
  printable text. Everything is bounded (read cap, site cap, decoded-byte cap) so a
  huge minified file stays memory- and time-light.
