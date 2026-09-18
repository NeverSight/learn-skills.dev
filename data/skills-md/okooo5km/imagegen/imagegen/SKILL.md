---
name: imagegen
description: Generate and edit raster images with the imagegen CLI through APIMart, manage local generation defaults, and compare available image models and prices. Use for image creation, reference-based edits, transparency or APIMart model selection; prefer existing vector or code assets for edits native to those formats.
license: Apache-2.0; see LICENSE.txt
metadata:
  author: okooo5km(十里)
  version: "2.0.1"
---

# Imagegen

Use the native Rust **imagegen** CLI. It does not require Python, Node.js, Rust, an SDK or an image-processing runtime on the user's machine. The host must support running local commands and accessing APIMart over HTTPS.

## Installation and configuration

Check `imagegen --version`. If the command is missing, check the configured `IMAGEGEN_INSTALL_DIR` or the default executable path (`~/.local/bin/imagegen` on macOS/Linux, `%LOCALAPPDATA%\imagegen\bin\imagegen.exe` on Windows) before reinstalling; expand paths for the actual shell. If no executable is installed, carry out the matching prebuilt CLI installation from [references/setup.md](references/setup.md) in the task's execution environment, within the host's permissions. Do not merely give the user installation commands when you can perform this setup. Respect host approval requirements; if execution, downloads or installation are blocked, explain the specific limitation and provide the setup commands instead.

After installation, use the resolved absolute executable path when PATH has not refreshed. Run `--version` and `doctor`, then continue the original task. Do not retry a failing installation repeatedly or claim installation succeeded without running the binary. Installers verify SHA-256 checksums; do not bypass a failed checksum or use the removed Python scripts. Importing this skill alone does not execute an installer.

Run from the user's project directory so relative outputs belong to the project. Quote paths containing spaces. Use `--prompt-file` for multiline or complex prompts.

For generation, edits, batch submission, task recovery and live model discovery, run `imagegen auth status` to check local key presence. If missing, show the registration/key links and ask the user to run `imagegen auth set` in their own terminal using [references/setup.md](references/setup.md). Never ask for a key in chat. After setup or replacement, run `imagegen auth check`, then resume the original task when verification succeeds. Do not repeatedly verify before every image. On HTTP 401, guide replacement; on 403, explain account/endpoint restrictions; on network errors or rate limits, retain the key and retry later without submitting an image.

Public prices, offline models, local configuration, chroma-key removal and `--dry-run` need no key: complete those tasks without registration prompts. Online verification checks model-list access only, not balance or permission to generate with every model.

Read `imagegen config show` before assuming defaults. The built-in model is **gpt-image-2.5-flare**, 1K, medium quality, one image. Explicit CLI options override saved defaults; `APIMART_IMAGE_MODEL` sits between an explicit model and the saved model. Change persistent defaults only when the user requests it. See [references/configuration.md](references/configuration.md) for size/ratio precedence, supported defaults and migration.

## Generate and edit

```text
imagegen generate --prompt "A ceramic teapot in soft studio light" --aspect-ratio 16:9 --resolution 2k --out output/teapot.png
imagegen edit --image "product photo.png" --prompt "Change only the background to warm gray; preserve the product and lettering" --out output/product-edited.png
```

Local references upload to APIMart as temporary public URLs before generation; use only authorized input images. GPT Image 2.5 accepts up to 16 references. Edits preserve the input proportions by default, ignoring saved size/aspect ratio. An explicit `--size`, `--aspect-ratio`, or `--use-default-size` changes that behavior. `--size` takes **exact pixels or auto**, not a ratio.

`--dry-run` validates without a key, HTTP calls, uploads or output directory creation. Unsupported parameters fail locally; no silent model switch or parameter removal. Prompt guidance: [references/prompting.md](references/prompting.md). Examples: [references/sample-prompts.md](references/sample-prompts.md).

Use `--background transparent --output-format png` (or WebP) for native GPT Image 2.5 transparency. Inspect alpha and edges. The optional local `remove-chroma-key` command is also native Rust; read [references/chroma-key.md](references/chroma-key.md) when needed. Masks require the `gpt-image-2-official` profile and are validated locally/in memory.

## Models, batches and recovery

`imagegen models` lists runnable profiles offline. `models --live --prices --json` queries account-visible image models and public prices. Discovery-only models cannot be generated until a verified profile is implemented. `prices --model MODEL --json` needs no key. Read [references/models-and-pricing.md](references/models-and-pricing.md) for rate units and billing limits.

For distinct prompts, use `batch --input jobs.jsonl --out-dir output/images`, with `--dry-run` first. Read [references/cli.md](references/cli.md) for JSONL format and recovery. Saved defaults apply to every job unless overridden; default concurrency is two and every submitted job can incur a charge.

The CLI prints a task ID and records output paths after submission. It never retries a paid submission. On timeout or download failure, run `imagegen fetch TASK_ID`; local receipts restore the original output paths/count. On another machine, pass `--out`/`--out-dir` and `--n`. If submission fails without an ID, check APIMart history before retrying. Resume only unfinished work, not an entire successful batch.

Report the model and absolute saved paths. Inspect subject, text, composition and requested invariants before declaring the visual complete. Existing files are protected unless replacement via `--force` is intended. Further paid iterations must stay within the user's scope.
