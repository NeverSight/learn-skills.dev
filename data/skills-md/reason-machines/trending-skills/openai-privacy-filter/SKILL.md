---
name: openai-privacy-filter
description: OpenAI Privacy Filter — bidirectional token-classification model for PII detection and masking in text
triggers:
  - detect PII in text
  - redact personally identifiable information
  - mask private data with OpenAI privacy filter
  - run privacy filter on a file
  - finetune PII detection model
  - evaluate privacy filter on labeled data
  - filter sensitive information from text
  - anonymize text with privacy filter
---

# OpenAI Privacy Filter

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

OpenAI Privacy Filter is a bidirectional token-classification model (1.5B params, 50M active) for detecting and masking PII spans in text. It runs in a single forward pass with constrained Viterbi decoding, supports a 128k-token context window, and is licensed Apache 2.0.

## Installation

```bash
pip install -e .
# or from a cloned repo:
git clone https://github.com/openai/privacy-filter
cd privacy-filter
pip install -e .
```

After install, the `opf` CLI is available. On first use it downloads the model checkpoint to `~/.opf/privacy_filter` unless `OPF_CHECKPOINT` is set.

```bash
export OPF_CHECKPOINT=/path/to/local/checkpoint_dir
```

## Detected PII Categories

| Label | Description |
|---|---|
| `account_number` | Bank/card/account numbers |
| `private_address` | Physical addresses |
| `private_email` | Email addresses |
| `private_person` | Personal names |
| `private_phone` | Phone numbers |
| `private_url` | Personal URLs |
| `private_date` | Dates of birth / personal dates |
| `secret` | Credentials, tokens, API keys |

## CLI Usage

### One-shot redaction

```bash
# Redact inline text
opf "Alice was born on 1990-01-02 and her email is alice@example.com."

# Force CPU inference
opf --device cpu "Alice was born on 1990-01-02."

# Use a specific checkpoint
opf --checkpoint /path/to/checkpoint_dir "Alice Johnson, SSN 123-45-6789"

# Redact an entire file
opf -f /path/to/document.txt

# Pipe input
cat document.txt | grep "sensitive" | opf

# Interactive mode (no input provided)
opf
```

### Evaluation

```bash
# Evaluate on a labeled JSONL dataset
opf eval examples/data/sample_eval_five_examples.jsonl

# See all eval options
opf eval --help
```

### Finetuning

```bash
# Finetune on your labeled dataset
opf train /path/to/train.jsonl --output-dir /path/to/finetuned_checkpoint

# See all training options
opf train --help
```

## Python API

```python
from opf import PrivacyFilter

# Load with default checkpoint (~/.opf/privacy_filter or OPF_CHECKPOINT)
pf = PrivacyFilter()

# Or specify a checkpoint explicitly
pf = PrivacyFilter(checkpoint="/path/to/checkpoint_dir")

# Redact a single string
result = pf.redact("Alice Johnson called from +1-800-555-0199.")
print(result.redacted_text)
# "██████████████ called from ██████████████."

# Access detected spans
for span in result.spans:
    print(span.label, span.text, span.start, span.end)
```

### Batch processing

```python
from opf import PrivacyFilter

pf = PrivacyFilter(device="cuda")  # or "cpu"

texts = [
    "Contact Bob Smith at bob@example.com",
    "Her SSN is 123-45-6789 and DOB is 1985-03-15",
    "API key: sk-abc123xyz789",
]

results = pf.redact_batch(texts)
for r in results:
    print(r.redacted_text)
    print(r.spans)
```

### Precision/Recall tuning via operating points

```python
from opf import PrivacyFilter

# High recall (broader masking, more false positives)
pf_recall = PrivacyFilter(operating_point="high_recall")

# High precision (stricter masking, fewer false positives)
pf_precision = PrivacyFilter(operating_point="high_precision")

# Default balanced
pf_default = PrivacyFilter()
```

## Data Format

### Input for eval and training (JSONL)

Each line is a JSON object:

```jsonl
{"text": "Alice was born on 1990-01-02.", "spans": [{"start": 0, "end": 5, "label": "private_person"}, {"start": 18, "end": 28, "label": "private_date"}]}
{"text": "Email bob@corp.com for details.", "spans": [{"start": 6, "end": 18, "label": "private_email"}]}
```

### JSON output schema

```json
{
  "redacted_text": "██████ was born on ██████████.",
  "spans": [
    {
      "label": "private_person",
      "text": "Alice",
      "start": 0,
      "end": 5,
      "score": 0.987
    },
    {
      "label": "private_date",
      "text": "1990-01-02",
      "start": 18,
      "end": 28,
      "score": 0.973
    }
  ]
}
```

See `OUTPUT_SCHEMAS.md` in the repo for full payload spec.

## Finetuning Workflow

```bash
# Prepare labeled JSONL (see data format above)
# Run finetuning
opf train train.jsonl \
  --output-dir ./my_finetuned_model \
  --eval-file eval.jsonl \
  --epochs 3 \
  --batch-size 8

# Use the finetuned model
opf --checkpoint ./my_finetuned_model "redact this text"
```

See `FINETUNING.md` and `examples/scripts/finetuning/` for runnable demo harnesses.

## Environment Variables

| Variable | Purpose |
|---|---|
| `OPF_CHECKPOINT` | Path to model checkpoint directory (overrides default `~/.opf/privacy_filter`) |

## Project Structure

```
opf/
├── __main__.py          # CLI entrypoint (redact, eval, train)
├── _api.py              # Python-facing API
├── _cli/                # Argument parsing, terminal rendering
├── _core/               # Runtime loading, span conversion, decoding
├── _eval/               # Dataset loading, metrics, eval runners
├── _train/              # Finetuning argument parsing and runners
├── _model/              # Transformer impl, checkpoint config, weight loading
examples/
├── data/                # Sample eval/finetune JSONL fixtures
├── scripts/finetuning/  # Runnable finetuning demo scripts
```

## Common Patterns

### Pipeline: sanitize files before uploading to an LLM

```python
from opf import PrivacyFilter
import json

pf = PrivacyFilter()

def sanitize_for_llm(raw_text: str) -> str:
    result = pf.redact(raw_text)
    return result.redacted_text

with open("raw_data.txt") as f:
    clean = sanitize_for_llm(f.read())

print(clean)
```

### Audit: log all detected PII spans without redacting

```python
from opf import PrivacyFilter

pf = PrivacyFilter()

def audit_pii(text: str) -> list[dict]:
    result = pf.redact(text)
    return [
        {"label": s.label, "text": s.text, "start": s.start, "end": s.end}
        for s in result.spans
    ]

findings = audit_pii("Bob Jones (DOB: 1978-06-15) owes $1,200.")
print(json.dumps(findings, indent=2))
```

### Filter specific label types only

```python
from opf import PrivacyFilter

pf = PrivacyFilter()

def redact_only(text: str, labels: list[str]) -> str:
    result = pf.redact(text)
    # Rebuild text redacting only chosen labels
    chars = list(text)
    for span in result.spans:
        if span.label in labels:
            for i in range(span.start, span.end):
                chars[i] = "█"
    return "".join(chars)

# Only redact emails and phones, keep names
output = redact_only(
    "Call Alice at 555-1234 or alice@example.com",
    labels=["private_phone", "private_email"]
)
print(output)
# "Call Alice at ████████ or █████████████████"
```

## Troubleshooting

**Model not found / auto-download fails**
- Set `OPF_CHECKPOINT` to a local checkpoint directory, or ensure internet access for the first run.
- Checkpoint is downloaded from https://huggingface.co/openai/privacy-filter.

**CUDA out of memory**
- Use `--device cpu` or reduce batch size with `--batch-size 1`.

**Low recall on domain-specific identifiers**
- Finetune on representative labeled examples using `opf train`.
- Try `operating_point="high_recall"` for broader masking.

**Fragmented span boundaries**
- Expected in heavy-punctuation or mixed-format text; the Viterbi decoder mitigates this but is not perfect.
- Finetuning on in-domain data is the recommended fix.

**Non-English / non-Latin text**
- The model is primarily English; multilingual performance is not guaranteed. Evaluate on your target language before production use.

## References

- [Model weights (HuggingFace)](https://huggingface.co/openai/privacy-filter)
- [Live demo](https://huggingface.co/spaces/openai/privacy-filter)
- [Model card (PDF)](https://cdn.openai.com/pdf/c66281ed-b638-456a-8ce1-97e9f5264a90/OpenAI-Privacy-Filter-Model-Card.pdf)
- `FINETUNING.md` — finetuning workflow
- `OUTPUT_SCHEMAS.md` — JSON response formats
- `EVAL_AND_OUTPUT_MODES.md` — output and eval mode details
