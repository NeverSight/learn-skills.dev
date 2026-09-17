---
name: spacemit-robot-vision
description: SpacemiT Robot SDK entry point for vision and image development. Use when users ask to set up, build, run examples, call APIs, benchmark, or debug detection, classification, segmentation, tracking, pose, face recognition, OCR, image-text embedding (CLIP/SigLIP), or composed CV applications (fall/fire/intrusion/emotion detection) in local, remote, or hybrid modes.
metadata:
  sdk:
    module_paths:
      - components/model_zoo/vision
    primary_docs:
      - components/model_zoo/vision/README.md
      - components/model_zoo/vision/include/vision_service.h
      - components/model_zoo/vision/examples/<model>/README.md
      - components/model_zoo/vision/applications/<app>/README.md
    build_hint: single_package_first
---

# SpacemiT Robot Vision AI

> This directory's `SKILL.md` is the canonical vision skill (installed into robot-skills). Task details live under `references/`.

## Purpose

This skill is the domain entry point for SpacemiT Robot SDK vision and image tasks. It does not copy SDK READMEs or long command runbooks. It helps the agent decide which SDK files to read, where to run, how to build and execute, and which actions need user confirmation.

This skill is a good fit for:

- Single-model examples and API integration for detection, classification, segmentation, tracking, and pose.
- Face detection/recognition (ArcFace, AdaFace, buffalo_l pipelines), OCR, and image-text embedding (SigLIP2, MobileCLIP2).
- Composed CV apps under `applications/`: face recognition, fall detection, fire detection, intrusion detection, emotion detection.
- Model/asset cache setup, standalone CMake or SDK `mm` builds, and `vision_infer_benchmark` performance checks.
- Vision troubleshooting (wheel import failures, missing models, headless boards, camera occupancy).

## Contract

- Module path: `components/model_zoo/vision`
- Build hint: `single_package_first` (standalone `cmake -S . -B build`, or `mm` on this package inside the SDK)
- Docs entry: see References (this component has **no standalone `API.md`**; use README section 3 + `include/vision_service.h` + per-example/app READMEs)
- Base rules: resolve mode, SDK root (`SROBOTIS_ROOT`), and target with `spacemit-robot-shared`; build via `spacemit-robot-build`; remote/hybrid execution via `spacemit-robot-remote`; hybrid sync via `spacemit-robot-sync`.
- Do not hard-code SSH host, board, target, absolute user paths, or private directories.
- Do not call `scripts/test/robot-test` by default; use it only for CI, regression, or when the user explicitly asks.
- Before camera/video capture, OpenCV GUI (`imshow`/`highgui`), large model/asset downloads, `sudo apt` system installs, or writing result images/videos: explain impact and confirm with the user.

## User Goals

| User goal | Support | Doc entry |
| --- | --- | --- |
| Set up environment | Yes | `references/setup.md` + `README.md` §2.1–2.3 |
| Run examples | Yes | `examples/<model>/README.md`; quick index: `references/examples-index.md` |
| Run composed apps | Yes | `applications/<app>/README.md`; quick index: `references/applications-index.md` |
| Call APIs in an app | Yes | `references/api.md`, `include/vision_service.h`, `README.md` §3 |
| Collect performance data | Yes | `references/benchmarking.md`, `README.md` §8 |
| Troubleshoot | Yes | `README.md` §4, failure logs and real command output; summary: `references/troubleshooting.md` |

## Workflow

1. Decide whether the user is setting up, running a single-model example, running a composed app, integrating APIs, benchmarking, troubleshooting, doing CI/regression, or changing code.
2. Confirm mode and SDK root via `spacemit-robot-shared`; if the SDK is missing or incomplete, hand off to `spacemit-robot-sdk-bootstrap`.
3. Load only the minimal vision files that match the task from References; do not pre-read every example for completeness.
4. Check prerequisites before running:
   - Models: `~/.cache/models/vision/<type>/`; if missing, list the files and ask whether to run the matching download script or root `scripts/download_all_models.sh`;
   - Assets: default test images/videos under `~/.cache/assets/{image,video}/`; if missing, ask whether to run `scripts/download_assets.sh`;
   - Camera: when live capture is requested, confirm device index and occupancy impact;
   - Display: on headless boards / pure SSH, prefer saving images; do not default to `imshow`;
   - Python: before Python examples, confirm the `spacemit_vision` wheel is installed.
5. Hand builds to `spacemit-robot-build`; do not hard-code targets or full build commands in this skill.
6. In `remote` and `hybrid` modes, run all execution, benchmarks, and hardware commands on the board.
7. Return real commands, exit status, key output, artifact paths, metrics, logs, and failure points.

Task branches:

- **First-time vision environment check**: resolve mode and SDK root; check module path, dependencies, model/asset caches, and camera/display if needed; report ready vs missing items.
- **Run a single-model example**: read `examples/<model>/README.md` first (optionally via `references/examples-index.md`); confirm models and inputs; then run the minimal command.
- **Run a composed app**: read the app README and `references/applications-index.md`; confirm multi-model deps; confirm before camera use or writing files.
- **Build a vision app (API)**: read `references/api.md`, then `vision_service.h` / `README.md` §3 as needed; C++: `VisionService`; Python: `VisionServiceNative` (including `encode_text` / `infer_embedding` / `infer_sequence`).
- **Collect performance data**: only when the user explicitly asks; read `references/benchmarking.md` (with vs without pre/post tracks).

## References

List only files that exist. Read on demand.

Inside this skill package:

- `references/setup.md`: deps, wheel build, model/asset caches, download scripts, headless notes.
- `references/api.md`: `VisionService` / `VisionServiceNative` call points and image-text embedding (API entry; repo has no standalone `API.md`).
- `references/benchmarking.md`: `vision_infer_benchmark` vs `onnxruntime_perf_test` (with / without pre/post).
- `references/examples-index.md`: example → task type → model cache directory.
- `references/applications-index.md`: composed-app pipelines and multi-model deps.
- `references/troubleshooting.md`: common failures and where to fix them.

Inside the SDK module (paths relative to SDK root; when using a standalone clone of this repo, drop the `components/model_zoo/vision/` prefix):

- `components/model_zoo/vision/README.md`: setup, downloads, build/run, API (§3), FAQ (§4), perf and benchmark (§8).
- `components/model_zoo/vision/include/vision_service.h`: C++ API.
- `components/model_zoo/vision/examples/<model>/README.md`: single-model examples.
- `components/model_zoo/vision/applications/<app>/README.md`: composed apps.
- `components/model_zoo/vision/scripts/download_all_models.sh` / `scripts/download_assets.sh`: bulk prep (confirm before download).
- `components/model_zoo/vision/tests/benchmarks/`: inference benchmark.
- `components/model_zoo/vision/test.yaml`: CI / `robot-test` (only when explicitly required).
- `components/model_zoo/vision/package.xml`: system dependencies.

If the module has `AGENTS.md`, read that first, then README/headers as needed.

## Notes

- README, headers, example/app READMEs, and `package.xml` are the source of truth; this skill only routes and enforces safety boundaries.
- Do not invent boxes, identities, OCR text, similarities, FPS, or benchmark numbers without a real run; do not treat README perf tables as results from this session.
- If an optional real model is missing, report "real-model verification skipped" unless the user requires a real-model check.
- Do not write models or result images into the source tree; use the user cache paths by default.
- On headless setups, save images instead; composed apps fail if any required model is missing—check the app README cache dirs first.
- Do not add scripts for simple builds, ordinary SSH, or README lookups.
