---
name: coreml-optimizer
description: Optimize CoreML models for iOS and macOS deployment. Covers quantization, palettization, pruning, Neural Engine targeting, compute unit selection, and performance profiling. Use when converting ML models to CoreML, optimizing model size/latency, debugging Neural Engine issues, or benchmarking on-device inference.
---

# CoreML Optimizer

Expert guidance for optimizing machine learning models for Apple's CoreML framework on iOS and macOS devices.

## When to Use This Skill

Use this skill when:
- Converting PyTorch/TensorFlow models to CoreML format
- Optimizing CoreML model size and inference latency
- Targeting the Neural Engine for maximum performance
- Debugging slow model inference or compute unit issues
- Applying quantization, palettization, or pruning
- Profiling model performance with Instruments
- Troubleshooting accuracy degradation after compression

## Speed Optimization Checklist

**The critical path to fast CoreML inference:**

### 1. Verify Compute Unit Configuration

Many "slow" models are accidentally CPU-bound. Configure via `MLModelConfiguration.computeUnits`:

| Option | Description |
|--------|-------------|
| `.all` | Uses all available compute units including Neural Engine (default, recommended) |
| `.cpuAndNeuralEngine` | CPU + Neural Engine, excludes GPU |
| `.cpuAndGPU` | CPU + GPU, excludes Neural Engine |
| `.cpuOnly` | Forces CPU-only execution (for debugging/consistency) |

In Swift:

```swift
let config = MLModelConfiguration()
config.computeUnits = .all  // .cpuAndNeuralEngine, .cpuAndGPU, .cpuOnly
let model = try MLModel(contentsOf: modelURL, configuration: config)
```

**Benchmark each configuration** - if `.all` isn't faster than `.cpuAndGPU`, your model may not be hitting the Neural Engine.

### 2. Apply Weight Compression with coremltools

CoreML execution commonly uses float16 where possible. Use `coremltools.optimize` for further compression:

```python
import coremltools as ct
import coremltools.optimize as cto

# 8-bit quantization (2-4x speedup for memory-bound models)
config = cto.coreml.OptimizationConfig(
    global_config=cto.coreml.OpLinearQuantizerConfig(
        mode="linear_symmetric",
        dtype="int8",
        granularity="per_channel"
    )
)

model = ct.models.MLModel("Model.mlpackage")
quantized = cto.coreml.linear_quantize_weights(model, config=config)
quantized.save("Model_int8.mlpackage")
```

### 3. Consider 4-bit Quantization

Recent coremltools releases support 4-bit quantization for even more aggressive compression:

```python
config = cto.coreml.OptimizationConfig(
    global_config=cto.coreml.OpLinearQuantizerConfig(
        mode="linear_symmetric",
        dtype="int4",
        granularity="per_block"
    )
)
```

### 4. Profile the FULL Pipeline

Pre/post-processing (image resize, tokenization, NMS, etc.) is often the real bottleneck. Profile the entire pipeline, not just `prediction()`.

```swift
// Profile everything
let startTotal = CFAbsoluteTimeGetCurrent()

// Preprocessing
let startPreprocess = CFAbsoluteTimeGetCurrent()
let input = preprocessImage(image)
let preprocessTime = CFAbsoluteTimeGetCurrent() - startPreprocess

// Inference
let startInference = CFAbsoluteTimeGetCurrent()
let output = try model.prediction(from: input)
let inferenceTime = CFAbsoluteTimeGetCurrent() - startInference

// Postprocessing
let startPostprocess = CFAbsoluteTimeGetCurrent()
let result = postprocess(output)
let postprocessTime = CFAbsoluteTimeGetCurrent() - startPostprocess

let totalTime = CFAbsoluteTimeGetCurrent() - startTotal

print("Preprocess: \(preprocessTime * 1000)ms")
print("Inference: \(inferenceTime * 1000)ms")
print("Postprocess: \(postprocessTime * 1000)ms")
print("Total: \(totalTime * 1000)ms")
```

## Hardware Recommendations (iOS 18 / macOS 15)

| Technique | Best Hardware | Use Case |
|-----------|--------------|----------|
| Weight palettization (1-8 bit) | Neural Engine | Runtime memory + latency gains |
| W8A8 quantization | Neural Engine (A17 Pro, M4) | Compute-bound models |
| INT4 per-block quantization | GPU (Mac) | Large models on Mac |
| Pruning (sparse weights) | Neural Engine, CPU | Memory-bound models |

## Core Compression Techniques

### Quantization

Reduces precision from float16/32 to int8/int4:

```python
import coremltools.optimize as cto

# Data-free 8-bit quantization (fastest, works well for most models)
config = cto.coreml.OptimizationConfig(
    global_config=cto.coreml.OpLinearQuantizerConfig(
        mode="linear_symmetric",
        dtype="int8",
        granularity="per_channel",
        weight_threshold=512  # Only quantize layers with >512 params
    )
)

quantized = cto.coreml.linear_quantize_weights(model, config=config)
```

**Expected results:**
- INT8: ~75% size reduction, 2-3x speedup
- INT4: ~87.5% size reduction, 3-4x speedup

### Palettization

Clusters weights into a small lookup table:

```python
config = cto.coreml.OptimizationConfig(
    global_config=cto.coreml.OpPalettizerConfig(
        mode="kmeans",  # or "uniform"
        nbits=4,        # 16 unique values
        granularity="per_channel"
    )
)

palettized = cto.coreml.palettize_weights(model, config=config)
```

**When to use:** Models sensitive to quantization often tolerate palettization better.

### Pruning

Zeros out unimportant weights:

```python
config = cto.coreml.OptimizationConfig(
    global_config=cto.coreml.OpMagnitudePrunerConfig(
        target_sparsity=0.5  # Remove 50% of weights
    )
)

pruned = cto.coreml.prune_weights(model, config=config)
```

**Note:** Training-aware pruning yields better results than post-training pruning.

### Combined Compression

For maximum compression, combine techniques:

```python
# Pruning + Quantization
pruned = cto.coreml.prune_weights(model, prune_config)
final = cto.coreml.linear_quantize_weights(pruned, quant_config)
```

## Neural Engine Optimization

### Querying Neural Engine Capabilities (iOS 17+)

```swift
// Get all available compute devices
let devices = MLComputeDevice.allComputeDevices

for device in devices {
    switch device {
    case .cpu(let cpuDevice):
        print("CPU available")

    case .gpu(let gpuDevice):
        print("GPU available")

    case .neuralEngine(let neDevice):
        print("Neural Engine available")
        print("Total cores: \(neDevice.totalCoreCount)")

    @unknown default:
        break
    }
}
```

### Checking Neural Engine Usage

```swift
// Method 1: Compare compute unit performance
let configs: [(String, MLComputeUnits)] = [
    ("All", .all),
    ("CPU+GPU", .cpuAndGPU),
    ("CPU+NE", .cpuAndNeuralEngine),
    ("CPU", .cpuOnly)
]

for (name, units) in configs {
    let config = MLModelConfiguration()
    config.computeUnits = units
    let model = try MLModel(contentsOf: url, configuration: config)
    let time = benchmark(model: model)
    print("\(name): \(time)ms")
}
```

```swift
// Method 2: Use MLComputePlan (iOS 17.4+)
let plan = try await MLComputePlan.load(contentsOf: modelURL, configuration: config)
// Examine deviceUsage for each operation
```

```
// Method 3: Check for H11ANEServicesThread in debugger
// Pause app during inference - if this thread exists, ANE is in use
```

### Operations That Block Neural Engine

These operations fall back to CPU/GPU:
- Dynamic tensor shapes (use fixed shapes)
- TopK, Scatter, GatherND
- Custom layers without ANE implementation
- Very large spatial dimensions (>4096)
- Odd channel counts (prefer multiples of 8/16)

### Optimal Tensor Shapes

```python
# Good for Neural Engine
ct.TensorType(shape=(1, 3, 224, 224))     # Batch=1
ct.TensorType(shape=(1, 64, 56, 56))      # Channels=64 (power of 2)
ct.TensorType(shape=(1, 16, 112, 112))    # Channels=16

# Avoid
ct.TensorType(shape=(4, 3, 224, 224))     # Batch>1 reduces efficiency
ct.TensorType(shape=(1, 13, 224, 224))    # Odd channel count
ct.TensorType(shape=(1, 3, 2048, 2048))   # Very large spatial dims
```

## Model Introspection

Inspect model structure before optimization:

```swift
let model = try MLModel(contentsOf: modelURL)
let description = model.modelDescription

// Input/output features
print("Inputs:")
for (name, feature) in description.inputDescriptionsByName {
    print("  \(name): \(feature.type)")
}

print("Outputs:")
for (name, feature) in description.outputDescriptionsByName {
    print("  \(name): \(feature.type)")
}

// Metadata
if let metadata = description.metadata[.author] {
    print("Author: \(metadata)")
}

// Check if updatable
print("Updatable: \(description.isUpdatable)")
```

## Model Conversion Best Practices

### Always Use ML Program Format

```python
import coremltools as ct

mlmodel = ct.convert(
    traced_model,
    inputs=[ct.TensorType(shape=(1, 3, 224, 224))],
    convert_to="mlprogram",  # NOT "neuralnetwork"
    minimum_deployment_target=ct.target.iOS16,
    compute_units=ct.ComputeUnit.ALL
)

mlmodel.save("Model.mlpackage")
```

### Embed Preprocessing

```python
mlmodel = ct.convert(
    model,
    inputs=[ct.ImageType(
        name="image",
        shape=(1, 3, 224, 224),
        scale=1/255.0,
        bias=[0, 0, 0],
        color_layout=ct.colorlayout.RGB
    )],
    convert_to="mlprogram"
)
```

### Handle Flexible Shapes

```python
# Range of sizes
ct.TensorType(
    name="input",
    shape=ct.Shape(shape=(1, 3, ct.RangeDim(224, 1024), ct.RangeDim(224, 1024)))
)

# Specific enumerated sizes
ct.TensorType(
    name="input",
    shape=ct.EnumeratedShapes(shapes=[(1,3,224,224), (1,3,512,512)])
)
```

## Performance Profiling

### Python Benchmarking

```python
import time
import numpy as np

model = ct.models.MLModel("Model.mlpackage")
input_data = {"input": np.random.rand(1, 3, 224, 224).astype(np.float32)}

# Warm up
for _ in range(5):
    _ = model.predict(input_data)

# Benchmark
times = []
for _ in range(100):
    start = time.time()
    _ = model.predict(input_data)
    times.append((time.time() - start) * 1000)

print(f"Mean: {np.mean(times):.2f}ms, Std: {np.std(times):.2f}ms")
print(f"P50: {np.percentile(times, 50):.2f}ms, P99: {np.percentile(times, 99):.2f}ms")
```

### Swift Benchmarking

```swift
func benchmark(model: MLModel, iterations: Int = 100) throws -> Double {
    let input = try MLDictionaryFeatureProvider(dictionary: [
        "input": MLMultiArray(shape: [1, 3, 224, 224], dataType: .float32)
    ])

    // Warm up
    for _ in 0..<5 { _ = try model.prediction(from: input) }

    // Benchmark
    let start = CFAbsoluteTimeGetCurrent()
    for _ in 0..<iterations { _ = try model.prediction(from: input) }
    return (CFAbsoluteTimeGetCurrent() - start) / Double(iterations) * 1000
}
```

### Xcode Instruments

1. Product > Profile (Cmd+I)
2. Select "Core ML" template
3. Record trace during inference
4. Analyze:
   - Layer-by-layer execution time
   - Compute unit usage (ANE/GPU/CPU icons)
   - Memory allocation patterns

## Advanced Optimization APIs (iOS 17.4+)

### MLOptimizationHints

Configure optimization behavior for different usage patterns:

```swift
let config = MLModelConfiguration()

// For models with variable input shapes (default)
config.optimizationHints.reshapeFrequency = .frequent

// For models with stable input shapes (faster inference)
config.optimizationHints.reshapeFrequency = .infrequent
```

**ReshapeFrequency options:**
- `.frequent` - Minimizes latency when shapes change often. Individual predictions may be slower, but shape transitions are fast.
- `.infrequent` - Re-optimizes for new shapes when they change. Initial delay but faster subsequent predictions for that shape.

### MLComputePlan (Pre-Execution Analysis)

Analyze compute unit allocation and cost before running inference:

```swift
// iOS 17.4+
let computePlan = try await MLComputePlan.load(
    contentsOf: modelURL,
    configuration: config
)

// Check device usage for each operation
for operation in computePlan.modelStructure.mainFunction.operations {
    if let deviceUsage = computePlan.deviceUsage(for: operation) {
        print("Operation: \(operation.name)")
        print("Device: \(deviceUsage)")
    }

    if let cost = computePlan.estimatedCost(of: operation) {
        print("Estimated cost: \(cost)")
    }
}
```

This helps identify which operations run on which compute units without executing inference.

### MLState (Stateful Models - iOS 18+)

For recurrent models and transformers that maintain state:

```swift
// iOS 18+
let model = try await MLModel.load(contentsOf: modelURL)
let state = model.newState()

// Sequential predictions with shared state
for input in inputSequence {
    let output = try model.prediction(from: input, using: state)
    // State is automatically updated between predictions
}
```

**Important constraints:**
- Don't read/write state buffers during prediction
- Predictions using the same MLState must be sequential (not concurrent)

### Memory Optimization with outputBackings

Pre-allocate output buffers to reduce memory allocation overhead:

```swift
let options = MLPredictionOptions()
options.outputBackings = [
    "output": try MLMultiArray(shape: [1, 1000], dataType: .float32)
]

let result = try model.prediction(from: input, options: options)
```

## Thread Safety

**Critical:** Use an MLModel instance on one thread or one dispatch queue at a time. For concurrent predictions, create multiple model instances or use a serial queue.

```swift
// Safe: Serial queue
let modelQueue = DispatchQueue(label: "com.app.coreml")
modelQueue.async {
    let result = try? model.prediction(from: input)
}

// Safe: Multiple instances for concurrency
let models = (0..<4).map { _ in
    try! MLModel(contentsOf: modelURL)
}
```

## Common Issues & Solutions

### Slow First Inference

**Problem:** First prediction takes 5-10x longer than subsequent ones.

**Solutions:**

1. **Async model loading** (recommended - doesn't block UI):

```swift
Task {
    let config = MLModelConfiguration()
    config.computeUnits = .all

    // Async loading - compiles and caches on first load
    let model = try await MLModel.load(contentsOf: modelURL, configuration: config)

    // Now predictions are fast
}
```

2. **Warm up with dummy predictions**:

```swift
Task {
    let dummy = try MLDictionaryFeatureProvider(dictionary: [
        "input": MLMultiArray(shape: [1, 3, 224, 224], dataType: .float32)
    ])
    for _ in 0..<3 {
        _ = try? model.prediction(from: dummy)
    }
}
```

3. **Pre-compile at build time** (Xcode compiles `.mlpackage` to optimized `.mlmodelc`)

### Accuracy Drop After Quantization

**Solutions:**
1. Use per-channel quantization (default)
2. Try palettization instead
3. Use calibration data:

```python
compressed = cto.coreml.linear_quantize_weights(
    model,
    config=config,
    calibration_data=representative_samples
)
```

4. Mixed precision - skip sensitive layers:

```python
config = cto.coreml.OptimizationConfig()
config.set_op_type("conv", cto.coreml.OpLinearQuantizerConfig(dtype="int8"))
config.set_op_name("final_layer", None)  # Keep in FP16
```

### Model Not Using Neural Engine

**Debug steps:**
1. Compare `.all` vs `.cpuAndGPU` performance
2. Check for unsupported operations
3. Verify tensor shapes are ANE-friendly
4. Use ML Program format (not NeuralNetwork)
5. Check thread names in debugger for `H11ANEServicesThread`

## Optimization Workflow

### Recommended Order

1. **Convert to ML Program format** with `compute_units=ALL`
2. **Establish baseline** - measure size, latency, accuracy
3. **Apply 8-bit quantization** (usually safe, 2-3x faster)
4. **Test on device** - verify accuracy and speed
5. **Try 4-bit or palettization** if more compression needed
6. **Profile full pipeline** - optimize pre/post-processing
7. **Test thermal behavior** under sustained load

### Size vs Speed vs Accuracy Tradeoffs

| Compression Level | Size | Speed | Accuracy Impact |
|-------------------|------|-------|-----------------|
| None (FP16) | Baseline | Baseline | None |
| 8-bit symmetric | -75% | +2-3x | Minimal (<1%) |
| 4-bit per-block | -87.5% | +3-4x | Low (1-3%) |
| 4-bit palettization | -87.5% | +2-3x | Variable |
| Pruning 50% + INT8 | -87.5% | +3-5x | Moderate (2-5%) |

## Quick Reference

### Installation

```bash
pip install coremltools
pip install coremltools==9.0b1  # For latest 4-bit features
```

### Conversion Template

```python
import coremltools as ct
import torch

model.eval()
traced = torch.jit.trace(model, torch.rand(1, 3, 224, 224))

mlmodel = ct.convert(
    traced,
    inputs=[ct.TensorType(shape=(1, 3, 224, 224))],
    convert_to="mlprogram",
    minimum_deployment_target=ct.target.iOS16,
    compute_units=ct.ComputeUnit.ALL
)
mlmodel.save("Model.mlpackage")
```

### Quantization Template

```python
import coremltools.optimize as cto

config = cto.coreml.OptimizationConfig(
    global_config=cto.coreml.OpLinearQuantizerConfig(
        mode="linear_symmetric",
        dtype="int8",
        granularity="per_channel"
    )
)

model = ct.models.MLModel("Model.mlpackage")
quantized = cto.coreml.linear_quantize_weights(model, config=config)
quantized.save("Model_int8.mlpackage")
```

## Resources

### Apple Documentation
- [Core ML Framework](https://developer.apple.com/documentation/coreml)
- [MLModel](https://developer.apple.com/documentation/coreml/mlmodel)
- [MLModelConfiguration](https://developer.apple.com/documentation/coreml/mlmodelconfiguration)
- [MLComputeUnits](https://developer.apple.com/documentation/coreml/mlcomputeunits)
- [MLOptimizationHints](https://developer.apple.com/documentation/coreml/mloptimizationhints)
- [MLComputePlan](https://developer.apple.com/documentation/coreml/mlcomputeplan)
- [Reducing App Size](https://developer.apple.com/documentation/coreml/reducing-the-size-of-your-core-ml-app)

### CoreML Tools (Python)
- [CoreML Tools GitHub](https://github.com/apple/coremltools)
- [Optimization Overview](https://apple.github.io/coremltools/docs-guides/source/opt-overview.html)
- [Quantization Guide](https://apple.github.io/coremltools/docs-guides/source/opt-quantization-overview.html)

### WWDC Sessions
- [WWDC24: Bring your machine learning and AI models to Apple silicon](https://developer.apple.com/videos/play/wwdc2024/10159/)
- [WWDC23: Improve Core ML integration with async prediction](https://developer.apple.com/videos/play/wwdc2023/10049/)
- [WWDC23: Use Core ML Tools for model compression](https://developer.apple.com/videos/play/wwdc2023/10047/)
- [WWDC22: Optimize your Core ML usage](https://developer.apple.com/videos/play/wwdc2022/10027/)

### Community
- [Neural Engine Docs (community)](https://github.com/hollance/neural-engine)
- [CoreML Profiler](https://github.com/fguzman82/CoreMLProfiler)
