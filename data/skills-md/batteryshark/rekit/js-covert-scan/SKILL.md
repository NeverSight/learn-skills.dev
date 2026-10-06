---
name: js-covert-scan
description: "Detect covert/evasive tactics in JavaScript/TypeScript: Unicode steganography (invisible/zero-width/bidi chars, confusable-homoglyph punctuation and letters), XOR/char-code/escape string hiding, and environment-keyed conditional behavior (timezone/locale/geo/proxy). Emits judgment-free parallax atoms (XFRM.UNICODE / XFRM.BITWISE / XFRM.ENCODE / LOAD.EVAL / ENVI.ENVCHECK), each tagged method=\"covert-scan\" so the consumer's lens makes the obfuscation/evasion call by provenance, and flags when atom families co-occur. Static and read-only."
---

# JavaScript Covert-Tactics Scanner

Detect the tactics code uses to **hide what it does** in JavaScript/TypeScript, and
emit atoms a caller can reason over. Static, read-only, pure-stdlib.

## When to use

You suspect a file is doing something it doesn't advertise — behaving differently
for some users, smuggling signal through text, or hiding strings/logic from a casual
read or a `strings` dump. This scanner surfaces the *tactics*; it does not decide
intent. Run it on a file or a whole package.

## What it detects — real parallax atoms, tagged `method="covert-scan"`

Every finding is emitted as a **judgment-free parallax atom** with `method:
"covert-scan"`; the downstream lens makes the obfuscation/evasion judgment from that
provenance. The per-tactic `note` preserves exactly which hiding tactic was seen (so
`XFRM.UNICODE` findings still say "bidi control char" vs "confusable homoglyph", and
`ENVI.ENVCHECK` findings still say "timezone-conditional" vs "geolocation check").

**XFRM.UNICODE** — hidden in text you can't see or can't tell apart:
- zero-width / format / control characters (U+200B, U+FEFF, soft hyphen, word
  joiner, variation selectors, tag chars…).
- bidirectional control characters (the "Trojan Source" reordering attack: source
  that reads differently than it compiles).
- confusable characters standing in for ASCII: fancy apostrophes / quotes (e.g.
  `U+2019 ’`, `U+02BC ʼ`, `U+02B9 ʹ`), non-breaking / ideographic spaces, look-alike
  dashes, and Cyrillic/Greek/fullwidth letters posing as Latin.

**XFRM.BITWISE** — XOR of character codes (a common way to keep strings out of a
plain `strings` dump).

**XFRM.ENCODE** — machine-hidden strings:
- strings assembled from `String.fromCharCode(…)` number lists.
- long `\xNN` / `\uNNNN` escaped string blobs.

**LOAD.EVAL** — `eval(…)` / `new Function(…)` dynamic execution.

**ENVI.ENVCHECK** — environment-keyed conditional behavior (act differently for
specific victims / dodge analysis):
- timezone checks: `Intl.DateTimeFormat().resolvedOptions().timeZone`, timezone
  name literals.
- locale checks: `navigator.language`, resolved locale.
- geolocation / IP-geo checks.
- proxy / `*_PROXY` env checks.

**The real signal is combination.** Any one atom can be innocent. Steganographic
punctuation *next to* a timezone check *next to* an XOR decoder is the shape of
covert, targeted, conditional behavior. The scan reports isolated findings and a
co-occurrence `assessment` across families.

## Usage

```bash
rekit run js-covert-scan ./suspicious.js
rekit run js-covert-scan ./some-package --format json
```

Text mode prints ranked atoms with location, codepoint (for STEGO), and the line.
JSON mode returns `{ok, filesScanned, findingCount, summary, families, assessment,
findings:[{atom, family, method:"covert-scan", confidence, file, line, col,
codepoint?, snippet, note}]}`. The XFRM/LOAD/ENVI atoms retain
`method="covert-scan"` so downstream analysis can weigh their provenance.

## Prerequisites

- **python3 ≥ 3.8** — pure stdlib (`unicodedata` + `re`), no vendored runtime.

## Notes / limits

Regex + Unicode heuristics, not a full parser: strong on the textual tactics
(steganography especially), best-effort on logic-level obfuscation. Homoglyph
*letters* and confusable punctuation can occur in legitimate natural-language
strings, so they carry lower confidence — weigh them with the co-occurrence
assessment.
