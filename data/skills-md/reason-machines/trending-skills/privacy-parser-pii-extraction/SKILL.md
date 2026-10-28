---
name: privacy-parser-pii-extraction
description: Extract structured PII spans from text using the OpenAI Privacy Filter 1.5B model reversed — returns what, where, and which type instead of masking.
triggers:
  - extract PII from text
  - parse personal information from string
  - find emails phones addresses in text
  - detect sensitive data spans
  - privacy parser pii extraction
  - structured pii spans from text
  - identify account numbers and secrets in text
  - reverse privacy filter extract pii
---

# Privacy Parser — PII Span Extraction

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

**privacy-parser** is the inverse of OpenAI's Privacy Filter. Where the filter masks PII with `<REDACTED>`, this library returns structured spans — label, text, and character offsets — using the same 1.5B `opf` model weights and label taxonomy.

## Installation

```bash
# Clone the repo (includes both subpackages)
git clone https://github.com/chiefautism/privacy-parser
cd privacy-parser

uv venv
uv pip install -e ./privacy-filter   # installs the opf model + weights loader
uv pip install -e ./pii_parser       # installs the parser library
```

First run downloads the `opf` 1.5B checkpoint (~3 GB) to `~/.opf/privacy_filter/`.

## Quick Start

```python
from pii_parser.hybrid import HybridPIIParser

parser = HybridPIIParser(device="cpu")  # or "cuda" / "mps"
result = parser.parse(
    "Hi Quindle Testwick (quindle.testwick@openai.com / +1-415-555-0102), "
    "account 40702810500001234567, 14 Beautiful Ct, Anytown USA, "
    "password Priv4cy-Filt3r-2026."
)

for span in result.spans:
    print(f"{span.label:18}  {span.text}")
```

Output:
```
private_person      Quindle Testwick
private_email       quindle.testwick@openai.com
private_phone       +1-415-555-0102
account_number      40702810500001234567
private_address     14 Beautiful Ct, Anytown USA
secret              Priv4cy-Filt3r-2026
```

## Three Backends

Choose the backend based on your speed/accuracy tradeoff:

| Backend           | Weights | Speed      | F1    | When to use                        |
|-------------------|---------|------------|-------|------------------------------------|
| `PIIParser`       | none    | µs         | 1.000 | Tests, known-format structured data |
| `ModelPIIParser`  | 1.5B    | ~500ms CPU | 0.733 | Model-only, no post-processing      |
| `HybridPIIParser` | 1.5B    | ~600ms CPU | 0.929 | **Production — ship this one**      |

```python
# Regex-only (no model, instant, high precision on structured formats)
from pii_parser import PIIParser
parser = PIIParser()

# Model-only (raw BIOES logits → Viterbi → spans)
from pii_parser.model import ModelPIIParser
parser = ModelPIIParser(device="cpu")

# Hybrid: model + span-merge + regex backstop (recommended)
from pii_parser.hybrid import HybridPIIParser
parser = HybridPIIParser(device="cpu")
```

## Span Object

Each `span` in `result.spans` has:

```python
span.label    # str — one of the 8 label types
span.text     # str — the extracted substring
span.start    # int — char offset in original string
span.end      # int — char offset (exclusive)
```

## Label Taxonomy (opf v2)

```
private_person    — full names of individuals
private_email     — email addresses
private_phone     — phone numbers (any format)
private_address   — street/postal addresses
private_url       — personal/private URLs
private_date      — dates tied to individuals
account_number    — bank/card/account identifiers
secret            — passwords, tokens, API keys
```

## Common Patterns

### Batch processing

```python
from pii_parser.hybrid import HybridPIIParser

parser = HybridPIIParser(device="cpu")

texts = [
    "Email Bob at bob@example.com",
    "SSN: 123-45-6789, DOB: 1990-03-15",
    "Token: ghp_abc123XYZ",
]

for text in texts:
    result = parser.parse(text)
    if result.spans:
        print(f"Text: {text!r}")
        for s in result.spans:
            print(f"  [{s.start}:{s.end}] {s.label} → {s.text!r}")
        print()
```

### Filter by label type

```python
result = parser.parse(long_document)

emails   = [s for s in result.spans if s.label == "private_email"]
phones   = [s for s in result.spans if s.label == "private_phone"]
secrets  = [s for s in result.spans if s.label == "secret"]
accounts = [s for s in result.spans if s.label == "account_number"]
```

### Redact after inspection

```python
def redact(text: str, spans) -> str:
    """Replace extracted PII with [LABEL] tokens."""
    result = list(text)
    for span in sorted(spans, key=lambda s: s.start, reverse=True):
        result[span.start:span.end] = f"[{span.label.upper()}]"
    return "".join(result)

result = parser.parse("Call Alice at 555-0100 re: account 9988776655.")
clean  = redact("Call Alice at 555-0100 re: account 9988776655.", result.spans)
# "Call [PRIVATE_PERSON] at [PRIVATE_PHONE] re: account [ACCOUNT_NUMBER]."
```

### Export to JSON

```python
import json

result = parser.parse("Jane Doe, jane@corp.io, +44 20 7946 0958")
payload = [
    {"label": s.label, "text": s.text, "start": s.start, "end": s.end}
    for s in result.spans
]
print(json.dumps(payload, indent=2))
```

### GPU acceleration

```python
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
parser = HybridPIIParser(device=device)
```

## CLI

```bash
# Parse a string directly
python -m pii_parser.cli_model "Alice paid 40702810500001234567 on 2026-05-17."

# Pipe text from a file
cat dump.txt | python -m pii_parser.cli_model -
```

## Architecture

```
text
  ↓
opf 1.5B → BIOES logits → Viterbi (tuned transitions) → char spans
  ↓
span-merge  (glues multi-token names: "Quindle" + "Testwick" → one span)
  ↓
regex backstop  (URL, secret, account_number — fills model gaps)
  ↓
result.spans[]
```

- **BIOES tagging**: Beginning / Inside / Outside / End / Single — standard NER scheme
- **Viterbi**: enforces valid tag transitions (no I- without B-)
- **Span-merge**: heuristic that joins adjacent same-label spans separated only by whitespace
- **Regex backstop**: high-precision patterns for labels the 1.5B model under-predicts (secrets, account numbers, URLs)

## Running Tests / Benchmarks

```bash
# Full fixture suite + latency benchmark
python pii_parser/tests/test_hybrid.py
```

Expected output:
```
Fixture F1:  0.929
Scenarios:   8/8 passed
Latency:     ~600 ms CPU
```

## Troubleshooting

**Slow first run** — The checkpoint (~3 GB) downloads to `~/.opf/privacy_filter/` on first use. Subsequent runs load from cache.

**CUDA out of memory** — Use `device="cpu"` or reduce batch size; the 1.5B model requires ~3 GB VRAM on GPU.

**Low recall on secrets/URLs** — Use `HybridPIIParser` (not `ModelPIIParser`); the regex backstop specifically covers these labels.

**Span text doesn't match offsets** — Offsets are byte-safe character indices into the original string passed to `parse()`. Do not preprocess/strip the string before parsing if you need offsets to remain valid.

**Import error on `privacy_filter`** — Ensure you installed both packages: `uv pip install -e ./privacy-filter` AND `uv pip install -e ./pii_parser`.

**Model not found** — Delete `~/.opf/privacy_filter/` and re-run to trigger a fresh download.
