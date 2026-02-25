---
name: browser-onnx
description: "Implements high-performance local machine learning inference in the browser using ONNX Runtime Web. Use this skill when the user needs privacy-first, low-latency, or offline AI capabilities (e.g., image classification, object detection, or NLP) without server-side processing."
license: MIT
compatibility: "Requires a browser with WebAssembly (WASM) support for CPU or WebGPU for hardware acceleration."
metadata:
  version: "1.0.0"
  runtime: "onnxruntime-web"
---

# Browser-Based ONNX Inference

This skill provides a comprehensive workflow for executing ONNX models locally in the browser using **ONNX Runtime Web (ORT-Web)**. Local inference offers significant advantages in **data privacy**, **reduced server costs**, and **unlimited scalability** as each user brings their own compute power.

## 1. Setup and Installation

Install the required library via npm:

```bash
npm install onnxruntime-web
```
*Note: For experimental features like WebGPU or WebNN, use the nightly version `onnxruntime-web@dev`.*

## 2. Global Environment Configuration

Set global `ort.env` flags before creating a session to optimize the runtime environment.

- **WebAssembly (CPU):** Enable multi-threading by setting `ort.env.wasm.numThreads` (default is half of hardware concurrency) and use a **Proxy Worker** (`ort.env.wasm.proxy = true`) to keep the UI responsive.
- **WASM Paths:** If binaries are not in the same directory as the JS bundle, manually override paths using `ort.env.wasm.wasmPaths` to point to local assets or a CDN.
- **WebGPU (GPU):** Use `ort.env.webgpu.profiling = { mode: 'default' }` for performance diagnosis during development.

## 3. Creating an Inference Session

Initialize the session by choosing the appropriate **Execution Provider (EP)**:

```javascript
import * as ort from 'onnxruntime-web';

const session = await ort.InferenceSession.create('./model.onnx', {
  executionProviders: ['webgpu', 'wasm'], // Prioritize GPU, fallback to CPU
  graphOptimizationLevel: 'all' // Enable all graph-level optimizations
});
```

## 4. Data Preprocessing

Input data must match the model's training format (e.g., NCHW for vision models).

- **Image-to-Tensor:** Use libraries like **JIMP** or **OpenCV.js** to resize, normalize (divide by 255.0), and convert RGBA to RGB.
- **Tensor Creation:** Use `new ort.Tensor('float32', float32Data,)` to prepare the input feeds.

## 5. Optimized Inference Patterns

- **Graph Capture:** For models with static shapes on WebGPU, enable `enableGraphCapture: true` to reduce CPU overhead by replaying kernel executions.
- **IO Binding:** For transformer models, keep data on the GPU by using `ort.Tensor.fromGpuBuffer()` and setting `preferredOutputLocation: 'gpu-buffer'` to avoid expensive memory copies.
- **Quantization:** Prefer **uint8 quantized models** for CPU (WASM) inference to improve performance; avoid float16 on CPU as it lacks native support and is slow.

## 6. Large Model Handling (>2GB)

- **Platform Limits:** Browsers like Chrome limit `ArrayBuffer` to ~2GB. Models exceeding this must be exported with **external data**.
- **Loading External Data:** Explicitly link external weight files in the session options:
  ```javascript
  const session = await ort.InferenceSession.create(modelUrl, {
    externalData: [{ path: './model.data', data: dataUrl }]
  });
  ```

## 7. Common Edge Cases

- **Memory Management:** Explicitly call `tensor.dispose()` for GPU tensors to prevent memory leaks.
- **Zero-Sized Tensors:** ORT-Web treats tensors with a dimension of 0 as CPU tensors regardless of the selected EP.
- **Thermal Throttling:** Sustained inference on mobile devices may trigger frequency scaling, doubling latency. Use lightweight "tiny" models to maintain thermal equilibrium.

## 8. Examples

### Multilingual Translation
Offload heavy translation tasks to a separate **Web Worker** using a singleton pattern to ensure the model (e.g., NLLB-200) loads only once.

### Object Detection (YOLO)
Implement **Non-Max Suppression (NMS)**. If the browser lacks support for specific NMS ops, run a separate NMS ONNX model to filter overlapping boxes locally.
