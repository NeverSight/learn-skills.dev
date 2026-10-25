---
name: computer-vision-expert
description: "Computer vision pipeline design and evaluation. Specialized in YOLO26, Segment Anything 3 (SAM 3), Vision Language Models, and real-time spatial analysis."
risk: critical
source: community
date_added: "2026-02-27"
---

# Computer Vision Pipeline Review

**Role**: Advanced Vision Systems Architect & Spatial Intelligence Expert

## Purpose
To provide expert guidance on designing, implementing, and optimizing state-of-the-art computer vision pipelines. From real-time object detection with YOLO26 to foundation model-based segmentation with SAM 3 and visual reasoning with VLMs.

## When to Use
- Designing high-performance real-time detection systems (YOLO26).
- Implementing zero-shot or text-guided segmentation tasks (SAM 3).
- Building spatial awareness, depth estimation, or 3D reconstruction systems.
- Optimizing vision models for edge device deployment (ONNX, TensorRT, NPU).
- Needing to bridge classical geometry (calibration) with modern deep learning.

## Capabilities

### 1. Unified Real-Time Detection (YOLO26)
- **NMS-Free Architecture**: Mastery of end-to-end inference without Non-Maximum Suppression (reducing latency and complexity).
- **Edge Deployment**: Optimization for low-power hardware using Distribution Focal Loss (DFL) removal and MuSGD optimizer.
- **Improved Small-Object Recognition**: Expertise in using ProgLoss and STAL assignment for high precision in IoT and industrial settings.

### 2. Promptable Segmentation (SAM 3)
- **Text-to-Mask**: Ability to segment objects using natural language descriptions (e.g., "the blue container on the right").
- **SAM 3D**: separate Objects/Body repositories and checkpoints address 3D reconstruction; they are not an automatic SAM 3 segmentation capability. See [SAM 3D Body](https://github.com/facebookresearch/sam-3d-body).
- **Unified Logic**: Use [SAM 3’s documented task interfaces](https://github.com/facebookresearch/sam3) and task-specific benchmark conditions; do not generalize an upstream metric into “2x accuracy” for every dataset.

### 3. Vision Language Models (VLMs)
- **Visual Grounding**: Leveraging Florence-2, PaliGemma 2, or Qwen2-VL for semantic scene understanding.
- **Visual Question Answering (VQA)**: Extracting structured data from visual inputs through conversational reasoning.

### 4. Geometry & Reconstruction
- **Depth Anything V2**: State-of-the-art monocular depth estimation for spatial awareness.
- **Sub-pixel Calibration**: Chessboard/Charuco pipelines for high-precision stereo/multi-camera rigs.
- **Visual SLAM**: Real-time localization and mapping for autonomous systems.

## Patterns

### 1. Text-Guided Vision Pipelines
- Use SAM 3's text-to-mask capability to isolate specific parts during inspection without needing custom detectors for every variation.
- Combine YOLO26 for fast "candidate proposal" and SAM 3 for "precise mask refinement".

### 2. Deployment-First Design
- Leverage YOLO26's simplified ONNX/TensorRT exports (NMS-free).
- Evaluate MuSGD against a fixed baseline on the actual dataset; convergence improvements are empirical, not guaranteed. [Official YOLO26 guide](https://docs.ultralytics.com/models/yolo26) documents architecture/training choices.

### 3. Progressive 3D Scene Reconstruction
- Monocular depth has scale/domain ambiguity; homographies model planar geometry, not arbitrary metric 3D scenes. Calibrate and use camera geometry/multiple views when measurement accuracy matters.

## Anti-Patterns

- **Manual NMS Post-processing**: Stick to NMS-free architectures (YOLO26/v10+) for lower overhead.
- **Click-Only Segmentation**: Forgetting that SAM 3 eliminates the need for manual point prompts in many scenarios via text grounding.
- **Legacy DFL Exports**: Using outdated export pipelines that don't take advantage of YOLO26's simplified module structure.

## Sharp Edges (2026)

| Issue | Severity | Solution |
|-------|----------|----------|
| SAM 3 VRAM Usage | Medium | Use quantized/distilled versions for local GPU inference. |
| Text Ambiguity | Low | Use descriptive prompts ("the 5mm bolt" instead of just "bolt"). |
| Motion Blur | Medium | Optimize shutter speed or use SAM 3's temporal tracking consistency. |
| Hardware Compatibility | Low | Verify the exact exporter, operators, precision and device runtime; a simplified architecture does not guarantee NPU/TPU support. |

## Related Skills
`ai-engineer`, `robotics-expert`, `research-engineer`, `embedded-systems`

## Example

**User request:**

> Design high-performance real-time detection systems (YOLO26).

## Limitations
- Model names are choices to evaluate, not a universal SOTA claim. Preserve dataset splits, version/checkpoint, preprocessing, latency hardware/precision and measured task metrics. Review each model/code/data license before distribution or deployment; do not infer commercial permission from a public repository.
- No models/checkpoints are bundled or downloaded here. Image/person data and safety-critical/medical uses require approved processing, consent and appropriate validation; model output is not guaranteed ground truth.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
