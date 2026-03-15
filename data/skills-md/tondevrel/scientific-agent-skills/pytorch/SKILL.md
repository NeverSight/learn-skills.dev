---
name: pytorch
description: Leading deep learning framework. Provides Tensors and Dynamic Computational Graphs with strong GPU acceleration. Widely used for research, neural networks, and differentiable programming.
version: 2.2
license: BSD-3-Clause
---

# PyTorch - Deep Learning & Tensors

PyTorch is a Python-based scientific computing package that uses the power of Graphics Processing Units (GPUs) and provides maximum flexibility and speed through its dynamic computational graph system.

## When to Use

- Building and training Deep Neural Networks (CNN, RNN, Transformers).
- Researching new AI architectures with dynamic graph needs.
- Accelerating tensor math on NVIDIA (CUDA) or Mac (MPS) hardware.
- Solving Physics-Informed Neural Networks (PINNs).
- Implementing Generative models (GANs, Diffusion).
- Large-scale optimization using Autograd (automatic differentiation).
- Production-grade AI deployment (via TorchScript/ONNX).

## Reference Documentation

**Official docs**: https://pytorch.org/docs/  
**Tutorials**: https://pytorch.org/tutorials/  
**Search patterns**: `torch.nn`, `torch.optim`, `torch.utils.data`, `Autograd`, `Tensor.to(device)`

## Core Principles

### The Tensor

The central data structure, similar to NumPy's ndarray, but with two key additions: it can live on a GPU and it supports automatic differentiation.

### Dynamic Computational Graph (Autograd)

PyTorch builds the graph "on the fly" as code executes. This allows for standard Python control flow (if/for) inside your models.

### Modules and Parameters

`nn.Module` is the base class for all neural network components. It automatically tracks `nn.Parameter` objects (weights/biases) for optimization.

## Quick Reference

### Installation

```bash
# CPU
pip install torch torchvision
# GPU (Check pytorch.org for specific CUDA versions)
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

### Standard Imports

```python
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
```

### Basic Pattern - Simple Linear Regression (The "PyTorch Way")

```python
import torch

# 1. Data (Tensors)
X = torch.tensor([[1.0], [2.0], [3.0]], requires_grad=True)
y = torch.tensor([[2.0], [4.0], [6.0]])

# 2. Simple Model
model = torch.nn.Linear(1, 1) # y = w*x + b

# 3. Loss and Optimizer
criterion = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# 4. Training Loop
for epoch in range(100):
    prediction = model(X)
    loss = criterion(prediction, y)
    
    optimizer.zero_grad() # Clear previous gradients
    loss.backward()       # Compute gradients (Autograd)
    optimizer.step()      # Update weights
```

## Critical Rules

### ✅ DO

- **Always zero_grad()** - PyTorch accumulates gradients by default. Forget this, and your model will fail to converge.
- **Use .to(device)** - Explicitly move your model AND your data to the same device (CPU or CUDA).
- **Use DataLoader** - Never feed data manually in a loop; DataLoader handles batching, shuffling, and multi-process loading.
- **Set model.train() / model.eval()** - This is vital for layers like Dropout and BatchNorm that behave differently during inference.
- **Use torch.no_grad() for inference** - This saves significant memory and compute by not building a graph.
- **Specify dtypes** - Be conscious of float32 (standard) vs float64 (scientific precision) vs float16 (speed/GPU).

### ❌ DON'T

- **Mix CPU and GPU Tensors** - `RuntimeError: Expected all tensors to be on the same device` is the most common error.
- **Use standard Python loops for math** - Use vectorized tensor operations for performance.
- **Forget .item()** - When getting a scalar value from a tensor for logging, use `loss.item()` to detach it from the graph.
- **Overuse float64 on GPU** - Many consumer GPUs have poor double-precision performance; use float32 if possible.

## Anti-Patterns (NEVER)

```python
import torch

# ❌ BAD: Mixing Python lists/arrays with Tensors in a loop
# for x in data:
#     res = model(torch.tensor(x)) # Extremely slow re-allocation!

# ✅ GOOD: Batching
# data_tensor = torch.stack([torch.tensor(x) for x in data])
# res = model(data_tensor)

# ❌ BAD: Calculating loss without zeroing gradients
loss.backward()
optimizer.step()
# Next iteration... gradients will be double what they should be!

# ✅ GOOD:
optimizer.zero_grad()
loss.backward()
optimizer.step()

# ❌ BAD: Standard NumPy for inference
# with torch.no_grad():
#    pred = model(X).numpy() # Can be slow on GPU if not handled

# ✅ GOOD: Explicit move to CPU
# pred = model(X).detach().cpu().numpy()
```

## Tensors and Device Management

### Moving between CPU and GPU

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Create tensor on device
x = torch.randn(3, 3, device=device)

# Move model to device
model = MyModel().to(device)

# Move data to device during loop
for inputs, labels in dataloader:
    inputs, labels = inputs.to(device), labels.to(device)
    # ...
```

## Building Models (nn.Module)

### Flexible Architectures

```python
class ScientificNet(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.layer1 = nn.Linear(input_dim, hidden_dim)
        self.layer2 = nn.Linear(hidden_dim, 1)
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = self.dropout(x)
        x = torch.sigmoid(self.layer2(x))
        return x

model = ScientificNet(10, 50)
```

## Custom Datasets (torch.utils.data)

### Handling Scientific Files (e.g., HDF5 or CSV)

```python
class MyScientificDataset(Dataset):
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)
        
    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, idx):
        # Convert row to tensor
        sample = torch.tensor(self.data.iloc[idx, :-1].values, dtype=torch.float32)
        label = torch.tensor(self.data.iloc[idx, -1], dtype=torch.float32)
        return sample, label

dataset = MyScientificDataset("experiment_results.csv")
loader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)
```

## Advanced Autograd

### Gradients for Physics (Jacobians/Hessians)

```python
x = torch.linspace(-5, 5, 100, requires_grad=True)
y = x**3

# First derivative dy/dx
# create_graph=True allows for higher-order derivatives
dy_dx = torch.autograd.grad(y.sum(), x, create_graph=True)[0]

# Second derivative (Hessian) d2y/dx2
d2y_dx2 = torch.autograd.grad(dy_dx.sum(), x)[0]
```

## Practical Workflows

### 1. Physics-Informed Neural Network (PINN) Fragment

```python
def pde_loss(model, x):
    """Simple ODE: u'(x) = u(x)."""
    x.requires_grad = True
    u = model(x)
    u_x = torch.autograd.grad(u.sum(), x, create_graph=True)[0]
    return F.mse_loss(u_x, u)

# Training loop combines data_loss + pde_loss
```

### 2. Early Stopping for Scientific Training

```python
best_loss = float('inf')
patience = 10
counter = 0

for epoch in range(1000):
    train_loss = train_one_epoch()
    val_loss = validate()
    
    if val_loss < best_loss:
        best_loss = val_loss
        torch.save(model.state_dict(), 'best_model.pth')
        counter = 0
    else:
        counter += 1
        if counter >= patience:
            print("Early stopping triggered")
            break
```

### 3. Feature Extraction for Chemistry

```python
def extract_embeddings(model, loader):
    model.eval()
    embeddings = []
    with torch.no_grad():
        for batch in loader:
            # Assume model has a .get_features() method
            features = model.get_features(batch.to(device))
            embeddings.append(features.cpu())
    return torch.cat(embeddings)
```

## Performance Optimization

### Using torch.compile (PyTorch 2.0+)

Significant speedups for modern models with one line:

```python
model = MyModel()
compiled_model = torch.compile(model)
```

### Mixed Precision (torch.cuda.amp)

Saves memory and speeds up training on modern GPUs (Tensor Cores).

```python
scaler = torch.cuda.amp.GradScaler()

for inputs, labels in loader:
    with torch.cuda.amp.autocast():
        output = model(inputs)
        loss = criterion(output, labels)
    
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

## Common Pitfalls and Solutions

### Vanishing/Exploding Gradients

```python
# ❌ Problem: Loss becomes 'nan' or weights don't update
# ✅ Solution: Use Gradient Clipping
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

### Dead ReLU

If a neuron's output is always <= 0, it stops learning.

```python
# ✅ Solution: Use LeakyReLU or ELU
self.act = nn.LeakyReLU(0.01)
```

### Memory Leak (Tensors staying in Graph)

Logging loss directly keeps the whole graph in memory.

```python
# ❌ BAD: total_loss += loss
# ✅ GOOD: total_loss += loss.item()
```

PyTorch is the engine of the AI revolution. For scientists, it provides the bridge from classical data analysis to the world of differentiable models, allowing for the discovery of patterns that were previously invisible.
