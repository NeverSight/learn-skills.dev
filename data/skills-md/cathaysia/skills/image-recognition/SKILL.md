---
name: image-recognition
description: Give non-multimodal models image "vision" by recognizing and describing images from a file path or the clipboard with a local OpenAI-compatible vision model (qwen/qwen3-vl-4b at http://127.0.0.1:1234). Use when the user asks what is in an image or screenshot, wants text read/transcribed from an image (OCR), or refers to a picture they pasted/copied, and the current model cannot see images directly.
---

# Image Recognition

Delegates image understanding to a local vision model served over an
OpenAI-compatible endpoint, so any model can answer questions about an image.
The image never leaves the machine: it is sent as a base64 data URL to
`http://127.0.0.1:1234/v1`.

## Prerequisites

- A local model server (LM Studio, llama.cpp, etc.) running at
  `http://127.0.0.1:1234` with the model `qwen/qwen3-vl-4b`.
- Python 3 with Pillow for clipboard reads and image normalization:
  `python3 -c "import PIL"` (install with `pip3 install Pillow` if missing).
- Verify the endpoint before first use:
  `python3 scripts/recognize_image.py --list-models`

## Usage

Entry point: `scripts/recognize_image.py`

- From a file: `python3 scripts/recognize_image.py --path screenshot.png`
- From the clipboard: `python3 scripts/recognize_image.py --clipboard`
- No argument at all defaults to the clipboard:
  `python3 scripts/recognize_image.py`
- Ask a specific question: `... --prompt "What color is the submit button?"`
- Full JSON response (usage, finish reason, etc.): `... --json`
- Overrides: `--model`, `--base-url`, `--max-tokens`, `--temperature`
- List served models: `... --list-models`

Exit code is 0 on success, 1 on runtime errors, 2 on usage errors.

## Workflow for the agent

1. Locate the script from this SKILL.md (the skill may be installed elsewhere;
   resolve the path first).
2. Pick the input source:
   - File: confirm the path exists before calling; screenshots often land in
     `~/Desktop` or `~/Downloads`.
   - Clipboard: use `--clipboard` when the user "copied"/"pasted" an image or
     said "this picture". The script errors clearly if the clipboard is empty.
3. Run the script, then relay the recognition result to the user in the
   conversation, quoting the transcribed text where relevant.
4. If the server is unreachable, tell the user the local model server at
   `127.0.0.1:1234` must be running.
5. If the model id is wrong, run `--list-models` and pass the correct id via
   `--model`.

## Notes

- The default prompt asks for detailed recognition and full transcription
  of any visible text. Override with `--prompt` for other styles or languages.
- Dependency-light by design: only Pillow is required; HTTP uses stdlib
  `urllib`. PNG/JPEG/GIF/WebP/BMP/TIFF are supported via file paths.
