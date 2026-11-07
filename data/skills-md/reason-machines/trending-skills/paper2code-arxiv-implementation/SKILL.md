---
name: paper2code-arxiv-implementation
description: Agent skill to convert any arxiv paper into a citation-anchored, working Python implementation with ambiguity auditing
triggers:
  - "implement this arxiv paper"
  - "turn this paper into code"
  - "convert paper to implementation"
  - "generate code from arxiv"
  - "implement the paper at this URL"
  - "reproduce this ML paper"
  - "paper2code"
  - "create implementation from research paper"
---

# paper2code — Arxiv Paper to Working Implementation

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

paper2code is a Claude Code agent skill that converts any arxiv paper URL into a citation-anchored Python implementation. Every code decision references the exact paper section and equation it implements, and all gaps/ambiguities are explicitly flagged rather than silently filled in.

---

## Install

```bash
npx skills add PrathamLearnsToCode/paper2code/skills/paper2code
```

During install you'll choose:
- **Agents**: which coding agents get the skill (e.g., Claude Code)
- **Scope**: Global (recommended) or project-level
- **Method**: Symlink (recommended) or copy

Then launch your agent:

```bash
claude
```

---

## Core Commands

### Basic usage

```
/paper2code https://arxiv.org/abs/1706.03762
```

### With framework override

```
/paper2code https://arxiv.org/abs/2006.11239 --framework jax
/paper2code https://arxiv.org/abs/2006.11239 --framework pytorch   # default
/paper2code https://arxiv.org/abs/2006.11239 --framework tensorflow
```

### With mode flag

```
/paper2code 1706.03762 --mode minimal       # architecture only (default)
/paper2code 1706.03762 --mode full          # includes training loop + data pipeline
/paper2code 1706.03762 --mode educational   # extra comments + pedagogical notebook
```

### Bare arxiv ID (no URL required)

```
/paper2code 1706.03762
/paper2code 2106.09685
```

---

## Output Structure

Every run produces a directory named after the paper slug:

```
attention_is_all_you_need/
├── README.md                  # Paper summary + quick-start
├── REPRODUCTION_NOTES.md      # Ambiguity audit, unspecified choices, known deviations
├── requirements.txt           # Pinned dependencies
├── src/
│   ├── model.py               # Architecture — every layer cited to paper section
│   ├── loss.py                # Loss functions with equation references
│   ├── data.py                # Dataset skeleton with preprocessing TODOs
│   ├── train.py               # Training loop (full/educational mode)
│   ├── evaluate.py            # Metric computation
│   └── utils.py               # Shared utilities
├── configs/
│   └── base.yaml              # All hyperparams — each cited or flagged [UNSPECIFIED]
└── notebooks/
    └── walkthrough.ipynb      # Paper section → code → shape checks
```

---

## Citation Anchoring Convention

The core value of paper2code is traceability. Every non-trivial decision is tagged:

| Tag | Meaning |
|-----|---------|
| `§X.Y` | Directly specified in section X.Y |
| `§X.Y, Eq. N` | Implements equation N from section X.Y |
| `[UNSPECIFIED]` | Paper doesn't state this — choice made with alternatives listed |
| `[PARTIALLY_SPECIFIED]` | Paper mentions it but is ambiguous — quote included |
| `[ASSUMPTION]` | Reasonable inference — reasoning explained |
| `[FROM_OFFICIAL_CODE]` | Taken from authors' official implementation |

### Example — model.py with citation anchors

```python
import torch
import torch.nn as nn
import math


class MultiHeadAttention(nn.Module):
    """§3.2 — Multi-Head Attention
    
    Implements Eq. 4: MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W^O
    where head_i = Attention(Q W_i^Q, K W_i^K, V W_i^V)
    """

    def __init__(self, d_model: int, num_heads: int, dropout: float = 0.1):
        super().__init__()
        # §3.2 — d_model = 512, h = 8 stated in Table 1
        assert d_model % num_heads == 0
        self.d_k = d_model // num_heads  # §3.2 — d_k = d_v = d_model / h = 64
        self.num_heads = num_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)  # §3.2, Eq. 4 — W^O projection

        # [UNSPECIFIED] Dropout rate for attention weights not stated in §3.2
        # Using 0.1 matching the model-wide dropout (§5.4, Table 3)
        self.dropout = nn.Dropout(dropout)

    def forward(self, q, k, v, mask=None):
        batch_size = q.size(0)

        # §3.2, Eq. 4 — project into h heads
        Q = self.W_q(q).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(k).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(v).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)

        # §3.2.1, Eq. 1 — Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)

        if mask is not None:
            # §3.2.3 — decoder masks future positions with -inf before softmax
            scores = scores.masked_fill(mask == 0, float('-inf'))

        attn_weights = torch.softmax(scores, dim=-1)
        attn_weights = self.dropout(attn_weights)

        out = torch.matmul(attn_weights, V)  # (batch, heads, seq, d_k)
        out = out.transpose(1, 2).contiguous().view(batch_size, -1, self.num_heads * self.d_k)
        return self.W_o(out)  # §3.2, Eq. 4 — W^O output projection


class TransformerBlock(nn.Module):
    """§3.1 — Encoder/Decoder layer structure"""

    def __init__(self, d_model: int, num_heads: int, d_ff: int, dropout: float = 0.1):
        super().__init__()
        self.attention = MultiHeadAttention(d_model, num_heads, dropout)

        # [ASSUMPTION] Using pre-norm based on stability; paper Figure 1 shows post-norm
        # Post-norm: x = LayerNorm(x + sublayer(x)) — §3.1
        # [PARTIALLY_SPECIFIED] "We apply layer normalization" — position ambiguous
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)

        # §3.3 — FFN(x) = max(0, xW_1 + b_1)W_2 + b_2
        self.ff = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),  # §3.3 — "ReLU activation"
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
        )
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        # §3.1 — residual connection around each sub-layer
        attn_out = self.attention(self.norm1(x), self.norm1(x), self.norm1(x), mask)
        x = x + self.dropout(attn_out)
        x = x + self.dropout(self.ff(self.norm2(x)))
        return x
```

### Example — configs/base.yaml with citations

```yaml
# base.yaml — All hyperparameters for attention_is_all_you_need
# Each value is either cited from the paper or flagged [UNSPECIFIED]

model:
  d_model: 512          # §3, Table 1 — "d_model = 512"
  num_heads: 8          # §3.2, Table 1 — "h = 8"
  d_ff: 2048            # §3.3, Table 1 — "d_ff = 2048"
  num_encoder_layers: 6 # §3, Table 1 — "N = 6"
  num_decoder_layers: 6 # §3, Table 1 — "N = 6"
  dropout: 0.1          # §5.4, Table 3 — "P_drop = 0.1"
  max_seq_len: 512      # [UNSPECIFIED] not stated; using 512 (common default)
                        # Alternatives: 256, 1024

training:
  batch_size: 25000     # §5.1 — "each batch ~25,000 source + target tokens"
  optimizer: adam       # §5.3 — "Adam optimizer"
  beta1: 0.9            # §5.3 — "β1 = 0.9"
  beta2: 0.98           # §5.3 — "β2 = 0.98"
  epsilon: 1.0e-9       # §5.3 — "ε = 10^-9"
  warmup_steps: 4000    # §5.3 — "warmup_steps = 4000"
  label_smoothing: 0.1  # §5.4 — "ε_ls = 0.1"
```

### Example — REPRODUCTION_NOTES.md structure

```markdown
# Reproduction Notes — Attention Is All You Need

## Ambiguity Audit

### SPECIFIED (high confidence)
| Choice | Value | Source |
|--------|-------|--------|
| d_model | 512 | §3, Table 1 |
| num_heads | 8 | §3.2, Table 1 |
| optimizer | Adam β1=0.9, β2=0.98 | §5.3 |

### PARTIALLY_SPECIFIED (judgment call made)
| Choice | Our Decision | Paper Quote | Alternatives |
|--------|-------------|-------------|--------------|
| Norm position | pre-norm | "layer norm before each sub-layer" (§3.1) conflicts with Figure 1 | post-norm |

### UNSPECIFIED (our defaults)
| Choice | Our Default | Rationale | Alternatives |
|--------|-------------|-----------|--------------|
| LayerNorm epsilon | 1e-6 | common default | 1e-5, 1e-8 |
| max_seq_len | 512 | common for WMT | 256, 1024 |

## Known Deviations
- data.py provides skeleton only; WMT14 preprocessing not implemented
- No beam search decoding (§5 mentions beam size 4, not fully implemented)
```

---

## What paper2code Will NOT Do

Understanding limits prevents wasted debugging time:

- **Won't guarantee correctness** — matches what the paper describes; if the paper is wrong, the code is wrong
- **Won't invent details silently** — gaps are always `[UNSPECIFIED]`, never filled confidently
- **Won't download datasets** — `data.py` gives a `Dataset` skeleton with instructions
- **Won't set up training infrastructure** — no distributed training, no experiment tracking
- **Won't implement baselines** — only the paper's core contribution
- **Won't reimplement standard components** — imports them or notes the dependency

---

## Common Patterns

### Pattern 1 — Implement a new architecture paper

```
/paper2code https://arxiv.org/abs/2010.11929 --mode minimal
```

Focus: `src/model.py` will contain the full architecture. Review `REPRODUCTION_NOTES.md` to understand every ambiguous choice before running.

### Pattern 2 — Reproduce a training method

```
/paper2code https://arxiv.org/abs/2006.11239 --mode full --framework pytorch
```

Focus: `src/train.py` will contain the full training loop. `configs/base.yaml` will list every hyperparameter with paper citations.

### Pattern 3 — Educational deep-dive

```
/paper2code 1706.03762 --mode educational
```

Focus: `notebooks/walkthrough.ipynb` walks through each paper section, shows corresponding code, and runs CPU-safe shape checks.

### Pattern 4 — Quick architecture prototype

```
/paper2code 2106.09685  # ViT
```

Then inspect and run:

```bash
cd vision_transformer/
pip install -r requirements.txt
python -c "
from src.model import VisionTransformer
import torch
model = VisionTransformer()  # toy config
x = torch.randn(2, 3, 224, 224)
print(model(x).shape)
"
```

---

## Troubleshooting

### Skill not triggering
- Confirm install completed: `npx skills list` should show `paper2code-arxiv-implementation`
- Use the explicit trigger: `/paper2code <url>`
- Try bare arxiv ID format: `/paper2code 1706.03762`

### Generated code has import errors
- Run `pip install -r requirements.txt` first
- Check `REPRODUCTION_NOTES.md` for noted dependencies
- Standard components (e.g., HuggingFace transformers) are imported, not reimplemented — install them separately

### "Paper not found" or fetch errors
- Confirm the arxiv ID exists: `https://arxiv.org/abs/<ID>`
- Try the full URL instead of bare ID
- Some very new papers (hours old) may not be indexed yet

### Silent assumptions in generated code
- This should not happen by design — if you find one, it's a bug
- Check `REPRODUCTION_NOTES.md` first; the assumption may be documented there
- Report via the repo issues if a gap was genuinely filled silently

### Framework-specific issues
- Default framework is PyTorch — omitting `--framework` gives PyTorch output
- JAX output requires `jax`, `flax`, `optax` — listed in `requirements.txt`
- TensorFlow output requires `tensorflow>=2.x`

---

## Contributing

### Add a worked example
1. Run: `/paper2code https://arxiv.org/abs/XXXX.XXXXX`
2. Save output to `skills/paper2code/worked/{paper_slug}/`
3. Write `review.md` evaluating correctness, flagged ambiguities, and any mistakes
4. Submit PR

### Improve guardrails
Add patterns where the skill makes silent assumptions to `guardrails/`.

### Add domain knowledge
Papers in your subfield reference common components? Add a knowledge file to `knowledge/` (e.g., `knowledge/graph_neural_networks.md`).

---

## Resources

- **Repo**: https://github.com/PrathamLearnsToCode/paper2code
- **Worked examples**: `skills/paper2code/worked/` in the repo
- **Issues**: https://github.com/PrathamLearnsToCode/paper2code/issues
- **License**: MIT
