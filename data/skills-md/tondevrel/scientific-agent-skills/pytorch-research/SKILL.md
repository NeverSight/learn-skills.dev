---
name: pytorch-research
description: Advanced sub-skill for PyTorch focused on deep research and production engineering. Covers custom Autograd functions, module hooks, advanced initialization, Distributed Data Parallel (DDP), and performance profiling.
version: 2.2
license: BSD-3-Clause
---

# PyTorch - Advanced Research & Engineering

Research-grade PyTorch requires moving beyond `nn.Sequential`. You need to control how gradients flow, how weights are initialized, and how computation is distributed across multiple GPUs. This guide covers the "internals" of the framework.

## When to Use

- Implementing custom layers with non-standard mathematical derivatives.
- Debugging vanishing or exploding gradients using Hooks.
- Scaling models to multiple GPUs (Distributed Data Parallel).
- Fine-tuning model performance using the PyTorch Profiler.
- Creating complex learning rate schedules (Cyclic, OneCycle).
- Deploying models for high-performance inference (TorchScript, FX).
- Researching Weight Initialization and Normalization techniques.

## Reference Documentation

- **Autograd Mechanics**: https://pytorch.org/docs/stable/notes/autograd.html
- **Distributed Training**: https://pytorch.org/docs/stable/distributed.html
- **Profiler**: https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html
- **Search patterns**: `torch.autograd.Function`, `register_forward_hook`, `DistributedDataParallel`, `torch.nn.init`

## Core Principles

### Beyond the Computational Graph

PyTorch is a "define-by-run" framework, but for research, you often need to intervene in the backward pass or inspect intermediate tensors without breaking the graph.

### The Life of a Gradient

Understanding that gradients are accumulated in `.grad` attributes and that `backward()` consumes the graph unless `retain_graph=True` is specified.

### Memory vs. Speed

In research, you often trade memory (activations) for speed (recomputation) using techniques like checkpointing.

## Quick Reference

### Standard Imports

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data.distributed import DistributedSampler
```

### Basic Pattern - Custom Autograd Function

```python
class MySignFunction(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input):
        # Save input for backward pass
        ctx.save_for_backward(input)
        return torch.sign(input)

    @staticmethod
    def backward(ctx, grad_output):
        # Straight-through estimator (STE) logic
        input, = ctx.saved_tensors
        grad_input = grad_output.clone()
        # Custom logic: gradients pass through as if it were an identity
        return grad_input

# Usage
my_sign = MySignFunction.apply
```

## Critical Rules

### ✅ DO

- **Use register_full_backward_hook** - To inspect or modify gradients as they flow through a specific module.
- **Initialize Weights Explicitly** - Use `torch.nn.init` (Xavier, Kaiming) inside a `model.apply(fn)` loop.
- **Use DistributedDataParallel (DDP)** - Instead of DataParallel (DP). DDP is faster and handles multi-process communication correctly.
- **Profile Before Optimizing** - Use `torch.profiler` to find which operator (e.g., a slow `view()` or `cat()`) is actually slowing down the model.
- **Use torch.cuda.empty_cache() sparingly** - It doesn't free physical memory to the OS, but it fragments the PyTorch memory manager. Only use it in long-running loops if needed.

### ❌ DON'T

- **Don't use inplace=True in custom layers** - This often breaks Autograd's ability to compute gradients correctly.
- **Don't use item() inside the loop** - Calling `.item()` on a GPU tensor forces a CPU-GPU sync, which kills performance.
- **Don't forget to set shuffle=False for DistributedSampler** - Let the sampler handle the shuffling logic in a multi-GPU environment.
- **Avoid Global Variables** - PyTorch models should be self-contained for easy serialization and deployment.

## Advanced Custom Layers

### Hooks for Debugging and Feature Extraction

```python
def print_grad_norm(module, grad_input, grad_output):
    print(f"Module: {module.__class__.__name__}, Grad Norm: {grad_output[0].norm().item()}")

# Attach to a specific layer
model.fc1.register_full_backward_hook(print_grad_norm)

# Extract activations (Forward Hook)
activations = {}
def get_activation(name):
    def hook(model, input, output):
        activations[name] = output.detach()
    return hook

model.conv1.register_forward_hook(get_activation('conv1'))
```

## Advanced Training Patterns

### Distributed Data Parallel (DDP) Skeleton

```python
import torch.multiprocessing as mp

def setup(rank, world_size):
    dist.init_process_group("nccl", rank=rank, world_size=world_size)

def train(rank, world_size):
    setup(rank, world_size)
    
    model = MyModel().to(rank)
    ddp_model = DDP(model, device_ids=[rank])
    
    # Use DistributedSampler to ensure each GPU sees different data
    sampler = DistributedSampler(dataset, num_replicas=world_size, rank=rank)
    loader = DataLoader(dataset, sampler=sampler, batch_size=32)
    
    optimizer = torch.optim.Adam(ddp_model.parameters(), lr=0.001)
    # ... training loop ...
    
    dist.destroy_process_group()

# mp.spawn(train, args=(world_size,), nprocs=world_size)
```

## Performance & Profiling

### Using the Profiler

```python
from torch.profiler import profile, record_function, ProfilerActivity

with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], 
             record_shapes=True) as prof:
    with record_function("model_inference"):
        model(inputs)

print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
```

### Gradient Checkpointing (Memory Saving)

If you have a very deep model and limited memory, trade computation for space.

```python
from torch.utils.checkpoint import checkpoint

class DeepModel(nn.Module):
    def forward(self, x):
        # Instead of storing all activations, recompute them during backward
        x = checkpoint(self.heavy_layer_1, x)
        x = checkpoint(self.heavy_layer_2, x)
        return x
```

## Practical Workflows

### 1. Custom Weight Initialization

```python
def init_weights(m):
    if isinstance(m, nn.Linear):
        # Kaiming initialization for ReLU networks
        torch.nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
        if m.bias is not None:
            torch.nn.init.constant_(m.bias, 0)
    elif isinstance(m, nn.Conv2d):
        torch.nn.init.xavier_uniform_(m.weight)

model.apply(init_weights)
```

### 2. Gradient Clipping (Stability)

```python
# Inside training loop
loss.backward()

# Clip to prevent exploding gradients (standard in RNNs/Transformers)
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

optimizer.step()
```

### 3. Dynamic Learning Rate (OneCycleLR)

```python
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
scheduler = torch.optim.lr_scheduler.OneCycleLR(optimizer, max_lr=0.1, 
                                                steps_per_epoch=len(train_loader), 
                                                epochs=10)

for epoch in range(10):
    for batch in train_loader:
        train_batch()
        scheduler.step() # Step every batch for OneCycle
```

## Common Pitfalls and Solutions

### In-place Modification Error

`RuntimeError: one of the variables needed for gradient computation has been modified by an inplace operation.`

```python
# ❌ Problem: x += 1 (breaks backward pass)
# ✅ Solution: y = x + 1 (creates a new tensor)
```

### CUDA Out of Memory (OOM) Strategies

- **Batch Size**: Reduce it.
- **Gradient Accumulation**: Compute loss for small batches, but only `step()` every N steps.
- **Empty Cache**: Use `torch.cuda.empty_cache()` between independent evaluations.
- **Mixed Precision**: Use `torch.cuda.amp` (saves 50% memory).

### Silent Failure: zero_grad() position

If you call `zero_grad()` after `backward()` but before `step()`, your model will never learn.

```python
# ✅ Correct order:
optimizer.zero_grad()
loss.backward()
optimizer.step()
```

Research PyTorch is about mastery over the mathematical engine. By leveraging custom gradients, hooks, and distributed infrastructure, you can move from training standard models to inventing the next generation of scientific AI.
