---
name: numpy-low-level
description: Advanced sub-skill for NumPy focused on internal memory management, stride manipulation, structured arrays, and interfacing with C/Cython. Covers zero-copy operations and SIMD vectorization principles.
version: 1.26
license: BSD-3-Clause
---

# NumPy - Low-Level Optimization & Memory

At high volumes, standard NumPy operations can still be slow due to unnecessary memory allocations. This guide covers how to manipulate the internal representation of arrays to achieve C-level performance without leaving Python.

## When to Use

- Implementing sliding window algorithms (convolutions) without extra memory.
- Interfacing Python with C, C++, or Fortran code via pointers.
- Working with complex, heterogeneous data structures (Structured Arrays).
- Optimizing memory-constrained systems via Memory Mapping (memmap).
- Debugging performance issues related to "Memory Layout" (C-style vs Fortran-style).

## Core Principles

### 1. The Metadata vs. Data Split

A NumPy array is a small Header (shape, dtype, strides) pointing to a large Data Buffer. Many operations (like `.T`, `reshape`, `slice`) only change the Header. This is "Zero-Copy".

### 2. Strides (The Step Logic)

Strides define how many bytes to skip in memory to get to the next element in each dimension. Manipulating strides allows you to "cheat" and create virtual views of data.

### 3. Contiguity

- **C-Contiguous**: Last index varies fastest (Row-major).
- **F-Contiguous**: First index varies fastest (Column-major).
- Vectorization is significantly faster on contiguous memory.

## Quick Reference: Memory Inspection

```python
import numpy as np

arr = np.zeros((100, 100))

print(arr.flags)         # Check contiguity and ownership
print(arr.strides)       # bytes to step in each axis
print(arr.__array_interface__['data']) # Memory pointer address
```

## Critical Rules

### ✅ DO

- **Prefer Views over Copies** - Use slicing and reshaping whenever possible.
- **Check base** - Use `arr.base is None` to verify if an array owns its memory or is just a view.
- **Use Structured Arrays** - For "Table of Records" data where you need NumPy speed but different types per column.
- **Align Memory** - Ensure arrays are aligned to 64-bit boundaries for SIMD optimization.
- **Use out= parameters** - Most NumPy functions accept an `out` argument to prevent creating a new temporary array.

### ❌ DON'T

- **Don't use np.append or np.concatenate in loops** - These are O(N²) because they copy the entire buffer every time.
- **Don't ignore the "Copy Warning"** - Fancy indexing (`arr[[1, 3, 5]]`) always creates a copy, unlike basic slicing.
- **Don't use as_strided blindly** - It is the most dangerous function in NumPy. It can lead to memory corruption or crashes if bounds are miscalculated.

## Low-Level Patterns

### 1. Sliding Windows (Zero-Copy Convolution)

```python
from numpy.lib.stride_tricks import as_strided

def sliding_window_1d(arr, window_size):
    """Creates a virtual 2D view of a 1D array for rolling stats."""
    itemsize = arr.itemsize
    shape = (arr.size - window_size + 1, window_size)
    strides = (itemsize, itemsize)
    return as_strided(arr, shape=shape, strides=strides)

# Result is a 2D array where each row is a window, 
# but it uses NO additional memory.
```

### 2. Structured Arrays (Interoperable C-structs)

```python
# Define a record type: Name (32 chars), Age (int), Salary (float)
dtype = np.dtype([('name', 'S32'), ('age', 'i4'), ('salary', 'f8')])

data = np.array([('Alice', 25, 50000), ('Bob', 30, 60000)], dtype=dtype)

# Access by field name (Fast, vectorized)
print(data['salary'].mean())
```

## Interfacing with C-API

### Using ctypes pointers

```python
import ctypes

# Get raw pointer to data
ptr = arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

# This pointer can be passed to a C/C++ library 
# for direct manipulation of the NumPy buffer.
```

## Performance Optimization

### Vectorized Math with out=

```python
# ❌ SLOW: Creates 3 temporary arrays
# res = (a * b) + c

# ✅ FAST: Reuse memory
np.multiply(a, b, out=a) # a now holds a*b
np.add(a, c, out=a)      # a now holds (a*b)+c
```

### Memory Mapping for Huge Data

```python
# Create an array that stays on disk, reading only what's needed
huge_data = np.memmap('data.bin', dtype='float32', mode='w+', shape=(10000, 10000))
```

## Common Pitfalls

### Broadcast Copying

If you broadcast a small array across a large one, NumPy doesn't copy the small one; it just sets the stride to 0.

```python
# strides of a (10, 1) array broadcasted to (10, 100):
# (8, 0) -> It keeps reading the same memory for the second axis!
```

### The Byte-Order (Endianness)

Scientific data from old instruments might be Big-Endian.

```python
# Convert in-place without copying
raw_data = np.frombuffer(buffer, dtype='>f4').view('<f4')
```

NumPy Low-Level is about removing abstractions. By mastering strides and the array interface, you turn Python into a thin wrapper over raw memory, enabling "impossible" data manipulations at hardware speeds.
