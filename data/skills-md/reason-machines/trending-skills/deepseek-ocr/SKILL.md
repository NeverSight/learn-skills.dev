---
name: deepseek-ocr
description: Expert skill for using DeepSeek-OCR, a vision-language model for optical character recognition with context optical compression supporting documents, PDFs, and images.
triggers:
  - use deepseek ocr
  - extract text from image with deepseek
  - ocr pdf with deepseek
  - convert document to markdown deepseek
  - deepseek ocr inference
  - run deepseek ocr on images
  - deepseek optical character recognition
  - document ocr with vllm deepseek
---

# DeepSeek-OCR

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

DeepSeek-OCR is a vision-language model for Optical Character Recognition with "Contexts Optical Compression." It supports native and dynamic resolutions, multiple prompt modes (document-to-markdown, free OCR, figure parsing, grounding), and can be run via vLLM (high-throughput) or HuggingFace Transformers. It processes images and PDFs, outputting structured text or markdown.

---

## Installation

### Prerequisites
- CUDA 11.8+, PyTorch 2.6.0
- Python 3.12.9 (via conda recommended)

### Setup

```bash
git clone https://github.com/deepseek-ai/DeepSeek-OCR.git
cd DeepSeek-OCR

conda create -n deepseek-ocr python=3.12.9 -y
conda activate deepseek-ocr

# Install PyTorch with CUDA 11.8
pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 \
  --index-url https://download.pytorch.org/whl/cu118

# Download vllm-0.8.5 whl from https://github.com/vllm-project/vllm/releases/tag/v0.8.5
pip install vllm-0.8.5+cu118-cp38-abi3-manylinux1_x86_64.whl

pip install -r requirements.txt
pip install flash-attn==2.7.3 --no-build-isolation
```

### Alternative: upstream vLLM (nightly)

```bash
uv venv
source .venv/bin/activate
uv pip install -U vllm --pre --extra-index-url https://wheels.vllm.ai/nightly
```

---

## Model Download

Model is available on HuggingFace: `deepseek-ai/DeepSeek-OCR`

```python
from huggingface_hub import snapshot_download
snapshot_download(repo_id="deepseek-ai/DeepSeek-OCR")
```

---

## Inference: vLLM (Recommended for Production)

### Single Image — Streaming

```python
from vllm import LLM, SamplingParams
from vllm.model_executor.models.deepseek_ocr import NGramPerReqLogitsProcessor
from PIL import Image

llm = LLM(
    model="deepseek-ai/DeepSeek-OCR",
    enable_prefix_caching=False,
    mm_processor_cache_gb=0,
    logits_processors=[NGramPerReqLogitsProcessor]
)

image = Image.open("document.png").convert("RGB")
prompt = "<image>\nFree OCR."

sampling_params = SamplingParams(
    temperature=0.0,
    max_tokens=8192,
    extra_args=dict(
        ngram_size=30,
        window_size=90,
        whitelist_token_ids={128821, 128822},  # <td>, </td> for table support
    ),
    skip_special_tokens=False,
)

outputs = llm.generate(
    [{"prompt": prompt, "multi_modal_data": {"image": image}}],
    sampling_params
)

print(outputs[0].outputs[0].text)
```

### Batch Images

```python
from vllm import LLM, SamplingParams
from vllm.model_executor.models.deepseek_ocr import NGramPerReqLogitsProcessor
from PIL import Image

llm = LLM(
    model="deepseek-ai/DeepSeek-OCR",
    enable_prefix_caching=False,
    mm_processor_cache_gb=0,
    logits_processors=[NGramPerReqLogitsProcessor]
)

image_paths = ["page1.png", "page2.png", "page3.png"]
prompt = "<image>\n<|grounding|>Convert the document to markdown. "

model_input = [
    {
        "prompt": prompt,
        "multi_modal_data": {"image": Image.open(p).convert("RGB")}
    }
    for p in image_paths
]

sampling_params = SamplingParams(
    temperature=0.0,
    max_tokens=8192,
    extra_args=dict(
        ngram_size=30,
        window_size=90,
        whitelist_token_ids={128821, 128822},
    ),
    skip_special_tokens=False,
)

outputs = llm.generate(model_input, sampling_params)

for path, output in zip(image_paths, outputs):
    print(f"=== {path} ===")
    print(output.outputs[0].text)
```

### PDF Processing (via vLLM scripts)

```bash
cd DeepSeek-OCR-master/DeepSeek-OCR-vllm
# Edit config.py: set INPUT_PATH, OUTPUT_PATH, model path, etc.
python run_dpsk_ocr_pdf.py   # ~2500 tokens/s on A100-40G
```

### Benchmark Evaluation

```bash
cd DeepSeek-OCR-master/DeepSeek-OCR-vllm
python run_dpsk_ocr_eval_batch.py
```

---

## Inference: HuggingFace Transformers

```python
import os
import torch
from transformers import AutoModel, AutoTokenizer

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

model_name = "deepseek-ai/DeepSeek-OCR"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModel.from_pretrained(
    model_name,
    _attn_implementation="flash_attention_2",
    trust_remote_code=True,
    use_safetensors=True,
)
model = model.eval().cuda().to(torch.bfloat16)

# Document to markdown
res = model.infer(
    tokenizer,
    prompt="<image>\n<|grounding|>Convert the document to markdown. ",
    image_file="document.jpg",
    output_path="./output/",
    base_size=1024,
    image_size=640,
    crop_mode=True,
    save_results=True,
    test_compress=True,
)
print(res)
```

### Transformers Script

```bash
cd DeepSeek-OCR-master/DeepSeek-OCR-hf
python run_dpsk_ocr.py
```

---

## Prompt Reference

| Use Case | Prompt |
|---|---|
| Document → Markdown | `<image>\n<|grounding|>Convert the document to markdown. ` |
| General OCR | `<image>\n<|grounding|>OCR this image. ` |
| Free OCR (no layout) | `<image>\nFree OCR. ` |
| Parse figure/chart | `<image>\nParse the figure. ` |
| General description | `<image>\nDescribe this image in detail. ` |
| Grounded REC | `<image>\nLocate <\|ref\|>TARGET_TEXT<\|/ref\|> in the image. ` |

```python
PROMPTS = {
    "document_markdown": "<image>\n<|grounding|>Convert the document to markdown. ",
    "ocr_image":         "<image>\n<|grounding|>OCR this image. ",
    "free_ocr":          "<image>\nFree OCR. ",
    "parse_figure":      "<image>\nParse the figure. ",
    "describe":          "<image>\nDescribe this image in detail. ",
    "rec":               "<image>\nLocate <|ref|>{target}<|/ref|> in the image. ",
}
```

---

## Supported Resolutions

| Mode | Resolution | Vision Tokens |
|---|---|---|
| Tiny | 512×512 | 64 |
| Small | 640×640 | 100 |
| Base | 1024×1024 | 256 |
| Large | 1280×1280 | 400 |
| Gundam (dynamic) | n×640×640 + 1×1024×1024 | variable |

```python
# Transformers: control resolution via infer() params
res = model.infer(
    tokenizer,
    prompt=prompt,
    image_file="image.jpg",
    base_size=1024,   # 512, 640, 1024, or 1280
    image_size=640,   # patch size for dynamic mode
    crop_mode=True,   # True = Gundam dynamic resolution
)
```

---

## Configuration (vLLM)

Edit `DeepSeek-OCR-master/DeepSeek-OCR-vllm/config.py`:

```python
# Key config fields (example)
MODEL_PATH = "deepseek-ai/DeepSeek-OCR"   # or local path
INPUT_PATH = "/data/input_images/"
OUTPUT_PATH = "/data/output/"
TENSOR_PARALLEL_SIZE = 1                   # GPUs for tensor parallelism
MAX_TOKENS = 8192
TEMPERATURE = 0.0
NGRAM_SIZE = 30
WINDOW_SIZE = 90
```

---

## Common Patterns

### Process a Directory of Images

```python
import os
from pathlib import Path
from PIL import Image
from vllm import LLM, SamplingParams
from vllm.model_executor.models.deepseek_ocr import NGramPerReqLogitsProcessor

def batch_ocr(image_dir: str, output_dir: str, prompt: str = "<image>\nFree OCR."):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    llm = LLM(
        model="deepseek-ai/DeepSeek-OCR",
        enable_prefix_caching=False,
        mm_processor_cache_gb=0,
        logits_processors=[NGramPerReqLogitsProcessor],
    )
    sampling_params = SamplingParams(
        temperature=0.0,
        max_tokens=8192,
        extra_args=dict(ngram_size=30, window_size=90, whitelist_token_ids={128821, 128822}),
        skip_special_tokens=False,
    )
    
    image_files = list(Path(image_dir).glob("*.png")) + list(Path(image_dir).glob("*.jpg"))
    
    inputs = [
        {"prompt": prompt, "multi_modal_data": {"image": Image.open(f).convert("RGB")}}
        for f in image_files
    ]
    
    outputs = llm.generate(inputs, sampling_params)
    
    for img_path, output in zip(image_files, outputs):
        out_file = Path(output_dir) / (img_path.stem + ".txt")
        out_file.write_text(output.outputs[0].text)
        print(f"Saved: {out_file}")

batch_ocr("/data/scans/", "/data/results/")
```

### Convert PDF Pages to Markdown

```python
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO
from vllm import LLM, SamplingParams
from vllm.model_executor.models.deepseek_ocr import NGramPerReqLogitsProcessor

def pdf_to_markdown(pdf_path: str) -> list[str]:
    doc = fitz.open(pdf_path)
    llm = LLM(
        model="deepseek-ai/DeepSeek-OCR",
        enable_prefix_caching=False,
        mm_processor_cache_gb=0,
        logits_processors=[NGramPerReqLogitsProcessor],
    )
    sampling_params = SamplingParams(
        temperature=0.0,
        max_tokens=8192,
        extra_args=dict(ngram_size=30, window_size=90, whitelist_token_ids={128821, 128822}),
        skip_special_tokens=False,
    )
    
    prompt = "<image>\n<|grounding|>Convert the document to markdown. "
    inputs = []
    for page in doc:
        pix = page.get_pixmap(dpi=150)
        img = Image.open(BytesIO(pix.tobytes("png"))).convert("RGB")
        inputs.append({"prompt": prompt, "multi_modal_data": {"image": img}})
    
    outputs = llm.generate(inputs, sampling_params)
    return [o.outputs[0].text for o in outputs]

pages = pdf_to_markdown("report.pdf")
full_markdown = "\n\n---\n\n".join(pages)
print(full_markdown)
```

### Grounded Text Location (REC)

```python
import torch
from transformers import AutoModel, AutoTokenizer

model_name = "deepseek-ai/DeepSeek-OCR"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModel.from_pretrained(
    model_name,
    _attn_implementation="flash_attention_2",
    trust_remote_code=True,
    use_safetensors=True,
).eval().cuda().to(torch.bfloat16)

target = "Total Amount"
prompt = f"<image>\nLocate <|ref|>{target}<|/ref|> in the image. "

res = model.infer(
    tokenizer,
    prompt=prompt,
    image_file="invoice.jpg",
    output_path="./output/",
    base_size=1024,
    image_size=640,
    crop_mode=False,
    save_results=True,
)
print(res)  # Returns bounding box / location info
```

---

## Troubleshooting

### `transformers` version conflict with vLLM
vLLM 0.8.5 requires `transformers>=4.51.1` — if running both in the same env, this error is safe to ignore per the project docs.

### Flash Attention build errors
```bash
# Ensure torch is installed before flash-attn
pip install flash-attn==2.7.3 --no-build-isolation
```

### CUDA out of memory
- Use smaller resolution: `base_size=512` or `base_size=640`
- Disable `crop_mode=False` to avoid multi-crop dynamic resolution
- Reduce batch size in vLLM inputs

### Model output is garbled / repetitive
Ensure `NGramPerReqLogitsProcessor` is passed to `LLM` — this is required for proper decoding:
```python
from vllm.model_executor.models.deepseek_ocr import NGramPerReqLogitsProcessor
llm = LLM(..., logits_processors=[NGramPerReqLogitsProcessor])
```

### Tables not rendering correctly
Add table token IDs to the whitelist:
```python
whitelist_token_ids={128821, 128822}  # <td> and </td>
```

### Multi-GPU inference
```python
llm = LLM(
    model="deepseek-ai/DeepSeek-OCR",
    tensor_parallel_size=4,  # number of GPUs
    enable_prefix_caching=False,
    mm_processor_cache_gb=0,
    logits_processors=[NGramPerReqLogitsProcessor],
)
```

---

## Key Files

```
DeepSeek-OCR-master/
├── DeepSeek-OCR-vllm/
│   ├── config.py                  # vLLM configuration
│   ├── run_dpsk_ocr_image.py      # Single image inference
│   ├── run_dpsk_ocr_pdf.py        # PDF batch inference
│   └── run_dpsk_ocr_eval_batch.py # Benchmark evaluation
└── DeepSeek-OCR-hf/
    └── run_dpsk_ocr.py            # HuggingFace Transformers inference
```
