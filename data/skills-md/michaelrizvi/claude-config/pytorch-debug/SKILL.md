---
name: pytorch-debug
description: Debug PyTorch errors including dtype mismatches, device errors, shape issues, gradient problems, and OOM. Use when the user hits a PyTorch runtime error or wants help tracing a bug.
---

# PyTorch Debug Assistant

Help the user diagnose and fix PyTorch errors systematically.

## Debugging Method: Trace the Full Data Flow

Always trace tensors from source to error point:

1. **Start at the source** — where does the tensor originate? (model output, checkpoint, dataloader)
2. **Track all transformations** — follow every op that touches the data
3. **Note dtype/device conversions** — explicit (`.float()`, `.cuda()`) and implicit (promotions, AMP)
4. **Identify the divergence** — where does actual vs expected dtype/device/shape differ?

## Common Issues

### Dtype Mismatches
- Mixed precision (`autocast`) exits can leave tensors in fp16/bf16 unexpectedly
- Softmax, layer norm, and division often promote to fp32 for numerical stability
- Checkpoint loading may introduce dtype mismatches if saved in a different precision
- **Don't assume dtypes are preserved** — verify with print statements or breakpoints

### Shape Errors
- Check batch dimension, sequence length, and feature dims separately
- Watch for unsqueeze/squeeze mismatches and transposed dimensions
- Verify dataloader collation matches model expectations

### Device Errors
- `device_map="auto"` distributes unevenly — use `max_memory` to cap per-GPU
- Watch for tensors created on CPU inside a model that lives on GPU (e.g. `torch.zeros()` without `.to(device)`)

### Gradient Issues
- `model.parameters()` not returning the params you expect (frozen vs unfrozen)
- Detached tensors breaking the computation graph (`.detach()`, `.data`, `.item()`)
- Vanishing/exploding gradients — check with `torch.nn.utils.clip_grad_norm_`

### OOM
- Reduce batch size first, then try gradient accumulation
- Check for tensors accumulating in a loop (missing `.detach()` on logged values)
- Use `torch.cuda.memory_summary()` to identify memory hogs

## Diagnostic Snippets

When suggesting debugging steps, prefer quick print-based checks:
```python
print(f"tensor: dtype={t.dtype}, device={t.device}, shape={t.shape}")
```

## Scope

$ARGUMENTS
