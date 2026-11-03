---
name: xiaomi-ocr
description: Run Xiaomi-OCR-0 locally through MCP to parse document images and PDFs, extract key fields (KIE), or answer questions about document images (VQA).
---

# Xiaomi-OCR-0

Use this Skill when a task needs OCR, document parsing, KIE, or OCR-VQA. Inference runs
on the user's machine with the Hugging Face checkpoint `SeerRay-Lab/Xiaomi-OCR-0` and
SGLang, vLLM, or the experimental Ollama backend. The MCP service owns prompts, image/PDF preparation, optional layout
segmentation, crop processing, concurrency, and output formatting. Call the task tool;
do not recreate these steps with separate tools or direct model requests.

## Set up local inference

### Choose the inference backend

Respect an explicit backend/model preference and the user's accuracy requirements. Otherwise:

- **Existing local service:** reuse a working Xiaomi-OCR-0 endpoint and its configured
  backend/model. Inspect MCP configuration, the running service, and its model list;
  an OpenAI-compatible URL alone does not identify the runtime. Keep a working backend
  unless it conflicts with the user's requirements.
- **Supported GPU environment:** prefer SGLang or vLLM with the original
  `SeerRay-Lab/Xiaomi-OCR-0` checkpoint, especially for accuracy-sensitive work. Reuse a
  compatible installed runtime and cached weights. For a fresh setup, check current
  official runtime support for the host and `Qwen3_5ForConditionalGeneration`; choose
  vLLM when supported, or SGLang when it is the compatible option.
- **Desktop/local setup where SGLang/vLLM is unavailable or unsuitable:** use a
  Qwen3.5-compatible Ollama if the host has enough memory for the BF16 model. This is
  the convenient local route, including compatible macOS setups. Read
  [the Ollama setup notes](../../OLLAMA.md) from the complete repository. Use
  `longwayxu/xiaomi-ocr-0:bf16` by default; reuse it if present, otherwise pull it under
  the user's setup/download authorization. Do not silently substitute a quantized tag.

Ollama remains experimental: explain the documented formula differences when selecting
it. BF16 weights do not establish HF output parity. If the user requires HF-equivalent
results, prefer the original checkpoint through SGLang/vLLM; if that route is unavailable,
explain the constraint and resolve the accuracy tradeoff with the user before choosing
Ollama. Do not promise numerical equivalence from any backend name alone.

Set all three variables before running the MCP installer so values from a previous
backend are not accidentally retained:

| Service | `XIAOMI_OCR_BACKEND` | `XIAOMI_OCR_LOCAL_URL` (default) | `XIAOMI_OCR_MODEL` (default) |
| --- | --- | --- | --- |
| SGLang / vLLM | `openai` | `http://127.0.0.1:8000/v1` | `SeerRay-Lab/Xiaomi-OCR-0` |
| Ollama | `ollama` | `http://127.0.0.1:11434/v1` | `longwayxu/xiaomi-ocr-0:bf16` |

For an existing service, use its actual loopback port and served model name. The installer
persists these values in MCP configuration. Keep image preparation and task prompts
inside this MCP service, including for Ollama.

### Install and connect

1. Inspect existing services, runtime installations, cached weights, and available memory;
   select the backend using the rules above. Explain the selected route and any needed
   environment creation or downloads. Use existing setup authorization when it covers
   these changes; ask only for missing authorization or an unresolved compatibility/accuracy
   choice. The user does not need to select a runtime just to start installation.
2. If the selected runtime is missing, check the OS, GPU, driver and relevant CUDA/PyTorch
   environment against its current official installation guide. For SGLang/vLLM, require
   support for `Qwen3_5ForConditionalGeneration`. For Ollama, follow the linked setup notes.
   Reuse compatible installations instead of replacing another runtime by default.
3. Start the selected service bound to loopback. For Ollama, follow the linked notes and
   use the model tag above. For SGLang/vLLM, examples are below (adjust tensor parallelism
   and memory limits to the hardware):

   ```bash
   python -m sglang.launch_server \
     --model-path SeerRay-Lab/Xiaomi-OCR-0 \
     --host 127.0.0.1 --port 8000 --context-length 16384
   ```

   ```bash
   vllm serve SeerRay-Lab/Xiaomi-OCR-0 \
     --host 127.0.0.1 --port 8000 \
     --trust-remote-code --max-model-len 16384
   ```

   If the engine cannot load the model or accept images, consult its current compatibility
   notes. Obtain authorization for upgrades if existing setup authorization does not cover
   them. Do not switch to a hosted endpoint. After connecting MCP, verify a real image
   request before reporting inference ready.
4. Reuse or clone the complete GitHub repository. The MCP imports its shared `evaluation_pipeline/`
   and `postprocess/` modules. Run the installer in `skills/xiaomi-ocr/` in that checkout
   (`bash install.sh --agent=codex` for Codex, `bash install.sh` for other agents).
   If using a detached Skill, set `XIAOMI_OCR_REPO` to the complete checkout.
   Before running `bash install.sh`, explain that it creates a private `.venv`, downloads
   the packages in `requirements.txt`, and registers one MCP entry in Codex config when applicable. Reuse an
   existing compatible MCP environment when available. Get the user's authorization before
   creating the environment or downloading dependencies if that authorization has not already
   been given. For other agents, merge the generated `mcp-config.json` entry into the current
   agent's MCP settings without replacing unrelated entries, then restart/rescan it. The MCP
   service connects only to the model's loopback listener.
5. Include printed-document region mode when completing a full agent-assisted installation,
   unless the user requests page-only setup. Explain the PaddlePaddle/PaddleX packages and
   possible PP-DocLayoutV3 weight download as part of the setup plan. Use existing setup
   authorization when it covers these downloads; ask only if it does not.

   Check the OS, Python version, CPU/GPU support and available GPU memory against the official
   [PaddlePaddle installation guide](https://paddlepaddle.github.io/PaddleX/latest/en/installation/paddlepaddle_install.html)
   and [PaddleX installation guide](https://paddlepaddle.github.io/PaddleX/latest/en/installation/installation.html).
   Install the compatible PaddlePaddle wheel in the MCP environment, then use that environment's
   Python to run `-m pip install -r <repo>/requirements-paddlex.txt`. This includes `paddlex[cv]`
   and `shapely`; plain `paddlex` alone is insufficient for PP-DocLayoutV3. Reuse compatible
   packages and cached weights. If GPU memory is limited, use a supported CPU build and set
   `XIAOMI_OCR_LAYOUT_DEVICE=cpu` in the MCP environment. If the Demo uses a separate Python
   environment, install its region dependencies there too when setting up the Demo.

   Load PP-DocLayoutV3 locally (the first use may download its
   [weights](https://huggingface.co/PaddlePaddle/PP-DocLayoutV3)), then verify one real
   `ocr_image` call with `mode="region"` before reporting region mode ready. Region detection,
   cropping and OCR stay inside the MCP server. If the platform is unsupported or setup fails,
   report the failing step and retain the verified page OCR, KIE and VQA capabilities;
   do not silently present page mode as region mode.

Official runtime references:
[SGLang Qwen3.5 guide](https://github.com/sgl-project/sglang/blob/main/docs_new/cookbook/autoregressive/Qwen/Qwen3.5.mdx) ·
[vLLM Qwen3.5 model implementation](https://docs.vllm.ai/en/latest/api/vllm/model_executor/models/qwen3_5/) ·
[vLLM supported models](https://docs.vllm.ai/en/latest/models/supported_models/).

## Choose the right task and document mode

- **Printed, regular documents**: use `ocr_image` or `ocr_pdf` with `mode="region"`. The
  MCP runs PP-DocLayoutV3 locally, crops regions, sends independent requests concurrently,
  then restores reading order and combines output. Model prompts request OTSL; MCP converts tables to HTML inside the returned Markdown and formats LaTeX formulas.
- **Scene text, handwritten notes, calligraphy, historical books, or irregular layouts**:
  use `mode="page"`. Region detection may split a line, column, or connected handwriting
  incorrectly; that can lose context and compound recognition errors. Whole-page mode
  preserves those relationships.
- **Key information extraction**: call `kie_image`. Pass `fields` when the output keys are
  known; the MCP builds the schema prompt and returns parsed JSON. Leave fields empty for
  general key-value extraction.
- **Question answering about a document image**: call `vqa_image` with the image and
  question. The MCP applies the concise answer format.
- **PDF**: call `ocr_pdf`, choosing page/region by the same document guidance. Prefer local
  file paths over base64 to avoid payload truncation.

Available MCP tools are `ocr_image`, `ocr_pdf`, `kie_image`, and `vqa_image`. Page/region
preprocessing and postprocessing are internal to these calls.

## Output handling

Keep the model's reading order and Markdown. Do not fill in unreadable content; retain the
model's uncertainty. Table conversion and document assembly happen inside MCP. Do not ask the agent to invoke a separate postprocessor. For KIE, preserve
JSON keys and values; for VQA, return the concise answer without adding unsupported detail.

If MCP reports that the local model is unavailable, inspect the configured service first,
then follow the backend selection and setup authorization rules above. If region mode reports missing
PaddleX/PaddlePaddle, explain the extra packages and possible layout-weight download, then
use existing authorization or ask if it does not cover the installation; whole-page mode
remains available in the meantime.
