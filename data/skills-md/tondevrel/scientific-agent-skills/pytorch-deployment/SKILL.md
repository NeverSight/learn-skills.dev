---
name: pytorch-deployment
description: Advanced sub-skill for PyTorch focused on model productionization and deployment. Covers TorchScript (JIT/Tracing), ONNX export, LibTorch (C++ API), and inference optimization (Quantization, Pruning).
version: 2.2
license: BSD-3-Clause
---

# PyTorch - Deployment & Production Engineering

Deploying a model in a high-performance environment often means removing the Python dependency. This guide covers how to serialize models into formats that can be loaded in C++, optimized for edge devices, or executed in high-throughput inference engines like TensorRT.

## When to Use

- Moving a model from a Jupyter Notebook to a production web server (FastAPI/Go/Rust).
- Embedding a neural network into a C++ application (LibTorch).
- Running inference on mobile devices (iOS/Android) or edge hardware (NVIDIA Jetson).
- Accelerating inference speed using specialized hardware backends (OpenVINO, TensorRT).
- Ensuring model reproducibility across different versions of PyTorch.

## Core Principles

### 1. Scripting vs. Tracing

- **Tracing**: PyTorch runs the model once with "example data" and records all operations. Fast, but ignores Python control flow (if, for).
- **Scripting**: PyTorch compiles the Python source code of the module. Slower to prepare, but preserves logic and control flow.

### 2. The ONNX Bridge

ONNX (Open Neural Network Exchange) is a cross-platform format. A model exported to ONNX can be run by Microsoft's ONNX Runtime, which is often faster than standard PyTorch for inference.

### 3. Quantization

Reducing weights from float32 (4 bytes) to int8 (1 byte). This shrinks the model size by 4x and can speed up inference by 2-3x on CPUs.

## Quick Reference: Export Patterns

```python
import torch

model = MyModel().eval()
example_input = torch.randn(1, 3, 224, 224)

# 1. Tracing (Most common)
traced_model = torch.jit.trace(model, example_input)
traced_model.save("model_jit.pt")

# 2. Scripting (For dynamic logic)
scripted_model = torch.jit.script(model)
scripted_model.save("model_script.pt")

# 3. ONNX Export
torch.onnx.export(model, example_input, "model.onnx", 
                  input_names=['input'], output_names=['output'],
                  dynamic_axes={'input': {0: 'batch_size'}})
```

## Critical Rules

### ✅ DO

- **Call model.eval() before export** - This freezes BatchNorm and Dropout layers. Forgetting this leads to incorrect predictions.
- **Use torch.no_grad()** - Always wrap your export logic in a `no_grad` context to avoid saving unnecessary gradient-tracking metadata.
- **Define dynamic_axes in ONNX** - If your model will handle different batch sizes or image resolutions, you must specify them during export.
- **Verify Export Accuracy** - Always compare the output of the original Python model and the exported model using `torch.allclose()`.
- **Use torch.compile for Python Deployment** - If you are deploying within Python, use `torch.compile` (PyTorch 2.0+) instead of JIT for better performance.

### ❌ DON'T

- **Don't use JIT Tracing for models with if/else** - The tracer will only capture the branch taken during the example run.
- **Don't include preprocessing in the model (usually)** - Keep image resizing/normalization outside the core model for better flexibility, unless using TorchScript-compatible operations.
- **Don't ignore quantization warnings** - Some layers (like custom activations) don't support int8 and will fall back to float32, reducing gains.

## Advanced Optimization

### Post-Training Quantization (Static)

```python
import torch.quantization

# 1. Set backend (x86 or ARM)
model.qconfig = torch.quantization.get_default_qconfig('fbgemm')

# 2. Prepare and Calibrate (Run some data through the model)
model_prepared = torch.quantization.prepare(model)
# ... run calibration loop ...

# 3. Convert
model_int8 = torch.quantization.convert(model_prepared)
```

## LibTorch (C++ Deployment)

To load a TorchScript model in C++:

```cpp
#include <torch/script.h>

int main() {
    // Load model
    torch::jit::script::Module module = torch::jit::load("model_jit.pt");
    
    // Create input tensor
    auto input = torch::randn({1, 3, 224, 224});
    
    // Run inference
    at::Tensor output = module.forward({input}).toTensor();
    std::cout << output.slice(1, 0, 5) << std::endl;
}
```

## Practical Workflows

### 1. Optimizing for Mobile (Lite Interpreter)

For mobile deployment, standard TorchScript is too heavy. Use the "Mobile" optimizer.

```python
from torch.utils.mobile_optimizer import optimize_for_mobile
optimized_model = optimize_for_mobile(traced_model)
optimized_model._save_for_lite_interpreter("model_mobile.ptl")
```

### 2. Deploying via ONNX Runtime

```python
import onnxruntime as ort

session = ort.InferenceSession("model.onnx", providers=['CUDAExecutionProvider'])
outputs = session.run(None, {"input": example_input.numpy()})
```

## Common Pitfalls and Solutions

### The "Missing Attribute" Error in JIT

TorchScript can't see attributes added to the model after initialization.

```python
# ✅ Solution: Define all needed attributes in __init__ or use @torch.jit.export
```

### Dynamic Shape Failures

If your model uses `x.shape[0]` in a calculation, tracing might hardcode that value.

```python
# ✅ Solution: Use Scripting or ensure calculations use tensor methods 
# like .size(0) which JIT understands.
```

PyTorch Deployment is the bridge between science and the real world. Mastering these tools ensures that your discoveries don't just stay in a notebook, but power the next generation of intelligent systems.
