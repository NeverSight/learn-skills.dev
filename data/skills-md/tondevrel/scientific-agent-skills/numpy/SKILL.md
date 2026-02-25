---
name: numpy
description: Comprehensive guide for NumPy - the fundamental package for scientific computing in Python. Use for array operations, linear algebra, random number generation, Fourier transforms, mathematical functions, and high-performance numerical computing. Foundation for SciPy, pandas, scikit-learn, and all scientific Python.
version: 1.26
license: BSD-3-Clause
---

# NumPy - Numerical Python

The fundamental package for numerical computing in Python, providing multi-dimensional arrays and fast operations.

## When to Use

- Working with multi-dimensional arrays and matrices
- Performing element-wise operations on arrays
- Linear algebra computations (matrix multiplication, eigenvalues, SVD)
- Random number generation and statistical distributions
- Fourier transforms and signal processing basics
- Mathematical operations (trigonometric, exponential, logarithmic)
- Broadcasting operations across different array shapes
- Vectorizing Python loops for performance
- Reading and writing numerical data to files
- Building numerical algorithms and simulations
- Serving as foundation for pandas, scikit-learn, SciPy

## Reference Documentation

**Official docs**: https://numpy.org/doc/  
**Search patterns**: `np.array`, `np.zeros`, `np.dot`, `np.linalg`, `np.random`, `np.broadcast`

## Core Principles

### Use NumPy For

| Task | Function | Example |
|------|----------|---------|
| Create arrays | `array`, `zeros`, `ones` | `np.array([1, 2, 3])` |
| Mathematical ops | `+`, `*`, `sin`, `exp` | `np.sin(arr)` |
| Linear algebra | `dot`, `linalg.inv` | `np.dot(A, B)` |
| Statistics | `mean`, `std`, `percentile` | `np.mean(arr)` |
| Random numbers | `random.rand`, `random.normal` | `np.random.rand(10)` |
| Indexing | `[]`, boolean, fancy | `arr[arr > 0]` |
| Broadcasting | Automatic | `arr + scalar` |
| Reshaping | `reshape`, `flatten` | `arr.reshape(2, 3)` |

### Do NOT Use For

- String manipulation (use built-in str or pandas)
- Complex data structures (use pandas DataFrame)
- Symbolic mathematics (use SymPy)
- Deep learning (use PyTorch, TensorFlow)
- Sparse matrices (use scipy.sparse)

## Quick Reference

### Installation

```bash
# pip
pip install numpy

# conda
conda install numpy

# Specific version
pip install numpy==1.26.0
```

### Standard Imports

```python
import numpy as np

# Common submodules
from numpy import linalg as la
from numpy import random as rand
from numpy import fft

# Never import *
# from numpy import *  # DON'T DO THIS!
```

### Basic Pattern - Array Creation

```python
import numpy as np

# From list
arr = np.array([1, 2, 3, 4, 5])

# Zeros and ones
zeros = np.zeros((3, 4))
ones = np.ones((2, 3))

# Range
range_arr = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]

# Linspace
linspace_arr = np.linspace(0, 1, 5)  # [0, 0.25, 0.5, 0.75, 1]

print(f"Array: {arr}")
print(f"Shape: {arr.shape}")
print(f"Dtype: {arr.dtype}")
```

### Basic Pattern - Array Operations

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Element-wise operations
c = a + b      # [5, 7, 9]
d = a * b      # [4, 10, 18]
e = a ** 2     # [1, 4, 9]

# Mathematical functions
f = np.sin(a)
g = np.exp(a)

print(f"Sum: {c}")
print(f"Product: {d}")
```

### Basic Pattern - Linear Algebra

```python
import numpy as np

# Matrix multiplication
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Dot product
C = np.dot(A, B)  # or A @ B

# Matrix inverse
A_inv = np.linalg.inv(A)

# Eigenvalues
eigenvalues, eigenvectors = np.linalg.eig(A)

print(f"Matrix product:\n{C}")
print(f"Eigenvalues: {eigenvalues}")
```

## Critical Rules

### ✅ DO

- **Use vectorization** - Avoid Python loops, use array operations
- **Specify dtype explicitly** - For memory efficiency and precision control
- **Use views when possible** - Avoid unnecessary copies
- **Broadcast properly** - Understand broadcasting rules
- **Check array shapes** - Use `.shape` frequently
- **Use axis parameter** - For operations along specific dimensions
- **Pre-allocate arrays** - Don't grow arrays in loops
- **Use appropriate dtypes** - int32, float64, complex128, etc.
- **Copy when needed** - Use `.copy()` for independent arrays
- **Use built-in functions** - They're optimized in C

### ❌ DON'T

- **Loop over arrays** - Use vectorization instead
- **Grow arrays dynamically** - Pre-allocate instead
- **Use Python lists for math** - Convert to arrays first
- **Ignore memory layout** - C-contiguous vs Fortran-contiguous matters
- **Mix dtypes carelessly** - Know implicit type promotion rules
- **Modify arrays during iteration** - Can cause undefined behavior
- **Use == for array comparison** - Use `np.array_equal()` or `np.allclose()`
- **Assume views vs copies** - Check with `.base` attribute
- **Ignore NaN handling** - Use `np.nanmean()`, `np.nanstd()`, etc.
- **Use outdated APIs** - Check for deprecated functions

## Anti-Patterns (NEVER)

```python
import numpy as np

# ❌ BAD: Python loops
result = []
for i in range(len(arr)):
    result.append(arr[i] * 2)
result = np.array(result)

# ✅ GOOD: Vectorization
result = arr * 2

# ❌ BAD: Growing arrays
result = np.array([])
for i in range(1000):
    result = np.append(result, i)  # Very slow!

# ✅ GOOD: Pre-allocate
result = np.zeros(1000)
for i in range(1000):
    result[i] = i

# Even better: Use arange
result = np.arange(1000)

# ❌ BAD: Comparing arrays with ==
if arr1 == arr2:  # This is ambiguous!
    print("Equal")

# ✅ GOOD: Use appropriate comparison
if np.array_equal(arr1, arr2):
    print("Equal")

# Or for floating point
if np.allclose(arr1, arr2, rtol=1e-5):
    print("Close enough")

# ❌ BAD: Ignoring dtypes
arr = np.array([1, 2, 3])
arr[0] = 1.5  # Silently truncates to 1!

# ✅ GOOD: Explicit dtype
arr = np.array([1, 2, 3], dtype=float)
arr[0] = 1.5  # Now works correctly

# ❌ BAD: Unintentional modification
a = np.array([1, 2, 3])
b = a  # b is just a reference!
b[0] = 999  # Also modifies a!

# ✅ GOOD: Explicit copy
a = np.array([1, 2, 3])
b = a.copy()  # b is independent
b[0] = 999  # a is unchanged
```

## Array Creation

### Basic Array Creation

```python
import numpy as np

# From Python list
arr1 = np.array([1, 2, 3, 4, 5])

# From nested list (2D)
arr2 = np.array([[1, 2, 3], [4, 5, 6]])

# Specify dtype
arr3 = np.array([1, 2, 3], dtype=np.float64)
arr4 = np.array([1, 2, 3], dtype=np.int32)

# From tuple
arr5 = np.array((1, 2, 3))

# Complex numbers
arr6 = np.array([1+2j, 3+4j])

print(f"1D array: {arr1}")
print(f"2D array:\n{arr2}")
print(f"Float array: {arr3}")
```

### Special Array Creation

```python
import numpy as np

# Zeros
zeros = np.zeros((3, 4))  # 3x4 array of zeros

# Ones
ones = np.ones((2, 3, 4))  # 2x3x4 array of ones

# Empty (uninitialized)
empty = np.empty((2, 2))  # Faster but values are garbage

# Full (constant value)
full = np.full((3, 3), 7)  # 3x3 array filled with 7

# Identity matrix
identity = np.eye(4)  # 4x4 identity matrix

# Diagonal matrix
diag = np.diag([1, 2, 3, 4])

print(f"Zeros shape: {zeros.shape}")
print(f"Identity:\n{identity}")
```

### Range-Based Creation

```python
import numpy as np

# Arange (like Python range)
a = np.arange(10)           # [0, 1, 2, ..., 9]
b = np.arange(2, 10)        # [2, 3, 4, ..., 9]
c = np.arange(0, 10, 2)     # [0, 2, 4, 6, 8]
d = np.arange(0, 1, 0.1)    # [0, 0.1, 0.2, ..., 0.9]

# Linspace (linearly spaced)
e = np.linspace(0, 1, 5)    # [0, 0.25, 0.5, 0.75, 1]
f = np.linspace(0, 10, 100) # 100 points from 0 to 10

# Logspace (logarithmically spaced)
g = np.logspace(0, 2, 5)    # [1, 10^0.5, 10, 10^1.5, 100]

# Geomspace (geometrically spaced)
h = np.geomspace(1, 1000, 4) # [1, 10, 100, 1000]

print(f"Arange: {a}")
print(f"Linspace: {e}")
```

### Array Copies and Views

```python
import numpy as np

original = np.array([1, 2, 3, 4, 5])

# View (shares memory)
view = original[:]
view[0] = 999  # Modifies original!

# Copy (independent)
copy = original.copy()
copy[0] = 777  # Doesn't affect original

# Check if array is a view
print(f"Is view? {view.base is original}")
print(f"Is copy? {copy.base is None}")

# Some operations create views, some create copies
slice_view = original[1:3]  # View
boolean_copy = original[original > 2]  # Copy!
```

## Array Indexing and Slicing

### Basic Indexing

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# Single element
print(arr[0])   # 10
print(arr[-1])  # 50 (last element)

# Slicing
print(arr[1:4])    # [20, 30, 40]
print(arr[:3])     # [10, 20, 30]
print(arr[2:])     # [30, 40, 50]
print(arr[::2])    # [10, 30, 50] (every 2nd element)

# Negative indices
print(arr[-3:-1])  # [30, 40]

# Reverse
print(arr[::-1])   # [50, 40, 30, 20, 10]
```

### Multi-Dimensional Indexing

```python
import numpy as np

arr = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]])

# Single element
print(arr[0, 0])   # 1
print(arr[1, 2])   # 6
print(arr[-1, -1]) # 9

# Row slicing
print(arr[0])      # [1, 2, 3] (first row)
print(arr[1, :])   # [4, 5, 6] (second row)

# Column slicing
print(arr[:, 0])   # [1, 4, 7] (first column)
print(arr[:, 1])   # [2, 5, 8] (second column)

# Sub-array
print(arr[0:2, 1:3])  # [[2, 3], [5, 6]]

# Every other element
print(arr[::2, ::2])  # [[1, 3], [7, 9]]
```

### Boolean Indexing

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Boolean condition
mask = arr > 5
print(mask)  # [False, False, False, False, False, True, True, True, True, True]

# Boolean indexing
filtered = arr[arr > 5]
print(filtered)  # [6, 7, 8, 9, 10]

# Multiple conditions (use & and |, not 'and' and 'or')
result = arr[(arr > 3) & (arr < 8)]
print(result)  # [4, 5, 6, 7]

# Or condition
result = arr[(arr < 3) | (arr > 8)]
print(result)  # [1, 2, 9, 10]

# Negation
result = arr[~(arr > 5)]
print(result)  # [1, 2, 3, 4, 5]
```

### Fancy Indexing

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# Index with array of integers
indices = np.array([0, 2, 4])
result = arr[indices]
print(result)  # [10, 30, 50]

# 2D fancy indexing
arr2d = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

rows = np.array([0, 2])
cols = np.array([1, 2])
result = arr2d[rows, cols]  # Elements at (0,1) and (2,2)
print(result)  # [2, 9]

# Combining boolean and fancy indexing
mask = arr > 25
indices_of_large = np.where(mask)[0]
print(indices_of_large)  # [2, 3, 4]
```

## Array Operations

### Element-wise Operations

```python
import numpy as np

a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])

# Arithmetic operations
print(a + b)    # [6, 8, 10, 12]
print(a - b)    # [-4, -4, -4, -4]
print(a * b)    # [5, 12, 21, 32]
print(a / b)    # [0.2, 0.333..., 0.428..., 0.5]
print(a ** 2)   # [1, 4, 9, 16]
print(a // b)   # [0, 0, 0, 0] (floor division)
print(a % b)    # [1, 2, 3, 4] (modulo)

# With scalars
print(a + 10)   # [11, 12, 13, 14]
print(a * 2)    # [2, 4, 6, 8]
```

### Mathematical Functions

```python
import numpy as np

x = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])

# Trigonometric
sin_x = np.sin(x)
cos_x = np.cos(x)
tan_x = np.tan(x)

# Inverse trig
arcsin_x = np.arcsin([0, 0.5, 1])

# Exponential and logarithm
arr = np.array([1, 2, 3, 4])
exp_arr = np.exp(arr)
log_arr = np.log(arr)
log10_arr = np.log10(arr)

# Rounding
floats = np.array([1.2, 2.7, 3.5, 4.9])
print(np.round(floats))   # [1, 3, 4, 5]
print(np.floor(floats))   # [1, 2, 3, 4]
print(np.ceil(floats))    # [2, 3, 4, 5]

# Absolute value
print(np.abs([-1, -2, 3, -4]))  # [1, 2, 3, 4]
```

### Aggregation Functions

```python
import numpy as np

arr = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]])

# Sum
print(np.sum(arr))         # 45 (all elements)
print(np.sum(arr, axis=0)) # [12, 15, 18] (column sums)
print(np.sum(arr, axis=1)) # [6, 15, 24] (row sums)

# Mean
print(np.mean(arr))        # 5.0

# Standard deviation
print(np.std(arr))         # ~2.58

# Min and max
print(np.min(arr))         # 1
print(np.max(arr))         # 9
print(np.argmin(arr))      # 0 (index of min)
print(np.argmax(arr))      # 8 (index of max)

# Median and percentiles
print(np.median(arr))      # 5.0
print(np.percentile(arr, 25))  # 3.0 (25th percentile)
```

## Broadcasting

### Broadcasting Rules

```python
import numpy as np

# Scalar and array
arr = np.array([1, 2, 3, 4])
result = arr + 10  # Broadcast scalar to array shape
print(result)  # [11, 12, 13, 14]

# 1D and 2D
arr1d = np.array([1, 2, 3])
arr2d = np.array([[10], [20], [30]])

result = arr1d + arr2d
print(result)
# [[11, 12, 13],
#  [21, 22, 23],
#  [31, 32, 33]]

# Broadcasting example: standardization
data = np.random.randn(100, 3)  # 100 samples, 3 features
mean = np.mean(data, axis=0)    # Mean of each column
std = np.std(data, axis=0)      # Std of each column
standardized = (data - mean) / std  # Broadcasting!
```

### Explicit Broadcasting

```python
import numpy as np

# Using broadcast_to
arr = np.array([1, 2, 3])
broadcasted = np.broadcast_to(arr, (4, 3))
print(broadcasted)
# [[1, 2, 3],
#  [1, 2, 3],
#  [1, 2, 3],
#  [1, 2, 3]]

# Using newaxis
arr1d = np.array([1, 2, 3])
col_vector = arr1d[:, np.newaxis]  # Shape (3, 1)
row_vector = arr1d[np.newaxis, :]  # Shape (1, 3)

# Outer product using broadcasting
outer = col_vector * row_vector
print(outer)
# [[1, 2, 3],
#  [2, 4, 6],
#  [3, 6, 9]]
```

## Linear Algebra

### Matrix Operations

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Matrix multiplication
C = np.dot(A, B)  # Traditional
C = A @ B         # Modern syntax (Python 3.5+)

# Element-wise multiplication
D = A * B  # Not matrix multiplication!

# Matrix transpose
A_T = A.T

# Trace (sum of diagonal)
trace = np.trace(A)

# Matrix power
A_squared = np.linalg.matrix_power(A, 2)

print(f"Matrix product:\n{C}")
print(f"Transpose:\n{A_T}")
print(f"Trace: {trace}")
```

### Solving Linear Systems

```python
import numpy as np

# Solve Ax = b
A = np.array([[3, 1], [1, 2]])
b = np.array([9, 8])

# Solve for x
x = np.linalg.solve(A, b)
print(f"Solution: {x}")  # [2, 3]

# Verify solution
print(f"Verification: {np.allclose(A @ x, b)}")  # True

# Matrix inverse
A_inv = np.linalg.inv(A)
print(f"Inverse:\n{A_inv}")

# Determinant
det = np.linalg.det(A)
print(f"Determinant: {det}")
```

### Eigenvalues and Eigenvectors

```python
import numpy as np

# Square matrix
A = np.array([[1, 2], [2, 1]])

# Eigenvalue decomposition
eigenvalues, eigenvectors = np.linalg.eig(A)

print(f"Eigenvalues: {eigenvalues}")
print(f"Eigenvectors:\n{eigenvectors}")

# Verify: A * v = λ * v
for i in range(len(eigenvalues)):
    lam = eigenvalues[i]
    v = eigenvectors[:, i]
    
    left = A @ v
    right = lam * v
    
    print(f"Eigenvalue {i}: {np.allclose(left, right)}")
```

### Singular Value Decomposition (SVD)

```python
import numpy as np

# Any matrix
A = np.array([[1, 2, 3],
              [4, 5, 6]])

# SVD: A = U @ S @ Vt
U, s, Vt = np.linalg.svd(A)

# Reconstruct original matrix
S = np.zeros((2, 3))
S[:2, :2] = np.diag(s)
A_reconstructed = U @ S @ Vt

print(f"Original:\n{A}")
print(f"Reconstructed:\n{A_reconstructed}")
print(f"Close? {np.allclose(A, A_reconstructed)}")

# Singular values
print(f"Singular values: {s}")
```

### Matrix Norms

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])

# Frobenius norm (default)
norm_fro = np.linalg.norm(A)

# 1-norm (max column sum)
norm_1 = np.linalg.norm(A, ord=1)

# Infinity norm (max row sum)
norm_inf = np.linalg.norm(A, ord=np.inf)

# 2-norm (spectral norm)
norm_2 = np.linalg.norm(A, ord=2)

print(f"Frobenius: {norm_fro:.4f}")
print(f"1-norm: {norm_1:.4f}")
print(f"2-norm: {norm_2:.4f}")
print(f"inf-norm: {norm_inf:.4f}")
```

## Random Number Generation

### Basic Random Generation

```python
import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# Random floats [0, 1)
rand_uniform = np.random.rand(5)  # 1D array of 5 elements
rand_2d = np.random.rand(3, 4)    # 3x4 array

# Random integers
rand_int = np.random.randint(0, 10, size=5)  # [0, 10)
rand_int_2d = np.random.randint(0, 100, size=(3, 3))

# Random normal distribution
rand_normal = np.random.randn(1000)  # Mean=0, std=1
rand_normal_custom = np.random.normal(loc=5, scale=2, size=1000)

# Random choice
choices = np.random.choice(['a', 'b', 'c'], size=10)
weighted_choices = np.random.choice([1, 2, 3], size=100, p=[0.1, 0.3, 0.6])
```

### Statistical Distributions

```python
import numpy as np

# Uniform distribution [low, high)
uniform = np.random.uniform(low=0, high=10, size=1000)

# Normal (Gaussian) distribution
normal = np.random.normal(loc=0, scale=1, size=1000)

# Exponential distribution
exponential = np.random.exponential(scale=2, size=1000)

# Binomial distribution
binomial = np.random.binomial(n=10, p=0.5, size=1000)

# Poisson distribution
poisson = np.random.poisson(lam=3, size=1000)

# Beta distribution
beta = np.random.beta(a=2, b=5, size=1000)

# Chi-squared distribution
chisq = np.random.chisquare(df=2, size=1000)
```

### Modern Random Generator (numpy.random.Generator)

```python
import numpy as np

# Create generator
rng = np.random.default_rng(seed=42)

# Generate random numbers
rand = rng.random(size=10)
ints = rng.integers(low=0, high=100, size=10)
normal = rng.normal(loc=0, scale=1, size=10)

# Shuffle array in-place
arr = np.arange(10)
rng.shuffle(arr)

# Sample without replacement
sample = rng.choice(100, size=10, replace=False)

print(f"Random: {rand}")
print(f"Shuffled: {arr}")
```

## Reshaping and Manipulation

### Reshaping Arrays

```python
import numpy as np

# Original array
arr = np.arange(12)  # [0, 1, 2, ..., 11]

# Reshape
arr_2d = arr.reshape(3, 4)
arr_3d = arr.reshape(2, 2, 3)

# Automatic dimension calculation with -1
arr_auto = arr.reshape(3, -1)  # Automatically calculates 4

# Flatten to 1D
flat = arr_2d.flatten()  # Returns copy
flat = arr_2d.ravel()    # Returns view if possible

# Transpose
arr_t = arr_2d.T

print(f"Original shape: {arr.shape}")
print(f"2D shape: {arr_2d.shape}")
print(f"3D shape: {arr_3d.shape}")
```

### Stacking and Splitting

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
c = np.array([7, 8, 9])

# Vertical stacking (vstack)
vstacked = np.vstack([a, b, c])
print(vstacked)
# [[1, 2, 3],
#  [4, 5, 6],
#  [7, 8, 9]]

# Horizontal stacking (hstack)
hstacked = np.hstack([a, b, c])
print(hstacked)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Column stack
col_stacked = np.column_stack([a, b, c])

# Concatenate (more general)
arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])
concat_axis0 = np.concatenate([arr1, arr2], axis=0)
concat_axis1 = np.concatenate([arr1, arr2], axis=1)

# Splitting
arr = np.arange(12)
split = np.split(arr, 3)  # Split into 3 equal parts
print(split)  # [array([0, 1, 2, 3]), array([4, 5, 6, 7]), array([8, 9, 10, 11])]
```

## File I/O

### Text Files

```python
import numpy as np

# Save to text file
data = np.array([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]])

np.savetxt('data.txt', data)
np.savetxt('data.csv', data, delimiter=',')
np.savetxt('data_formatted.txt', data, fmt='%.2f')

# Load from text file
loaded = np.loadtxt('data.txt')
loaded_csv = np.loadtxt('data.csv', delimiter=',')

# Skip header rows
loaded_skip = np.loadtxt('data.txt', skiprows=1)

# Load specific columns
loaded_cols = np.loadtxt('data.csv', delimiter=',', usecols=(0, 2))
```

### Binary Files (.npy, .npz)

```python
import numpy as np

# Save single array
arr = np.random.rand(100, 100)
np.save('array.npy', arr)

# Load single array
loaded = np.load('array.npy')

# Save multiple arrays (compressed)
arr1 = np.random.rand(10, 10)
arr2 = np.random.rand(20, 20)
np.savez('arrays.npz', first=arr1, second=arr2)

# Load multiple arrays
loaded = np.load('arrays.npz')
loaded_arr1 = loaded['first']
loaded_arr2 = loaded['second']

# Compressed save
np.savez_compressed('arrays_compressed.npz', arr1=arr1, arr2=arr2)
```

## Advanced Techniques

### Universal Functions (ufuncs)

```python
import numpy as np

# Ufuncs operate element-wise
arr = np.array([1, 2, 3, 4, 5])

# Built-in ufuncs
result = np.sqrt(arr)
result = np.exp(arr)
result = np.log(arr)

# Custom ufunc
def my_func(x):
    return x**2 + 2*x + 1

vectorized = np.vectorize(my_func)
result = vectorized(arr)

# More efficient: define true ufunc
@np.vectorize
def better_func(x):
    return x**2 + 2*x + 1
```

### Structured Arrays

```python
import numpy as np

# Define dtype
dt = np.dtype([('name', 'U20'), ('age', 'i4'), ('weight', 'f8')])

# Create structured array
data = np.array([
    ('Alice', 25, 55.5),
    ('Bob', 30, 70.2),
    ('Charlie', 35, 82.1)
], dtype=dt)

# Access by field name
names = data['name']
ages = data['age']

# Sort by field
sorted_data = np.sort(data, order='age')

print(f"Names: {names}")
print(f"Sorted by age:\n{sorted_data}")
```

### Memory Layout and Performance

```python
import numpy as np

# C-contiguous (row-major, default)
arr_c = np.array([[1, 2, 3], [4, 5, 6]], order='C')

# Fortran-contiguous (column-major)
arr_f = np.array([[1, 2, 3], [4, 5, 6]], order='F')

# Check memory layout
print(f"C-contiguous? {arr_c.flags['C_CONTIGUOUS']}")
print(f"F-contiguous? {arr_c.flags['F_CONTIGUOUS']}")

# Make contiguous
arr_made_c = np.ascontiguousarray(arr_f)
arr_made_f = np.asfortranarray(arr_c)

# Memory usage
print(f"Memory (bytes): {arr_c.nbytes}")
print(f"Item size: {arr_c.itemsize}")
```

### Advanced Indexing with ix_

```python
import numpy as np

arr = np.arange(20).reshape(4, 5)

# Select specific rows and columns
rows = np.array([0, 2])
cols = np.array([1, 3, 4])

# ix_ creates open mesh
result = arr[np.ix_(rows, cols)]
print(result)
# [[1, 3, 4],
#  [11, 13, 14]]

# Equivalent to
# result = arr[[0, 2]][:, [1, 3, 4]]
```

## Practical Workflows

### Statistical Analysis

```python
import numpy as np

# Generate sample data
np.random.seed(42)
data = np.random.normal(loc=100, scale=15, size=1000)

# Descriptive statistics
mean = np.mean(data)
median = np.median(data)
std = np.std(data)
var = np.var(data)

# Percentiles
q25, q50, q75 = np.percentile(data, [25, 50, 75])

# Histogram
counts, bins = np.histogram(data, bins=20)

# Correlation coefficient
data2 = data + np.random.normal(0, 5, size=1000)
corr = np.corrcoef(data, data2)[0, 1]

print(f"Mean: {mean:.2f}")
print(f"Median: {median:.2f}")
print(f"Std: {std:.2f}")
print(f"IQR: [{q25:.2f}, {q75:.2f}]")
print(f"Correlation: {corr:.3f}")
```

### Monte Carlo Simulation

```python
import numpy as np

def estimate_pi(n_samples=1000000):
    """Estimate π using Monte Carlo method."""
    # Random points in [0, 1] x [0, 1]
    x = np.random.rand(n_samples)
    y = np.random.rand(n_samples)
    
    # Check if inside quarter circle
    inside = (x**2 + y**2) <= 1
    
    # Estimate π
    pi_estimate = 4 * np.sum(inside) / n_samples
    
    return pi_estimate

# Estimate π
pi_est = estimate_pi(10000000)
print(f"π estimate: {pi_est:.6f}")
print(f"Error: {abs(pi_est - np.pi):.6f}")
```

### Polynomial Fitting

```python
import numpy as np

# Generate noisy data
x = np.linspace(0, 10, 50)
y_true = 2*x**2 + 3*x + 1
y_noisy = y_true + np.random.normal(0, 10, size=50)

# Fit polynomial (degree 2)
coeffs = np.polyfit(x, y_noisy, deg=2)
print(f"Coefficients: {coeffs}")  # Should be close to [2, 3, 1]

# Predict
y_pred = np.polyval(coeffs, x)

# Evaluate fit quality
residuals = y_noisy - y_pred
rmse = np.sqrt(np.mean(residuals**2))
print(f"RMSE: {rmse:.2f}")

# Create polynomial object
poly = np.poly1d(coeffs)
print(f"Polynomial: {poly}")
```

### Image Processing Basics

```python
import numpy as np

# Create synthetic image (grayscale)
image = np.random.rand(100, 100)

# Apply transformations
# Rotate 90 degrees
rotated = np.rot90(image)

# Flip vertically
flipped_v = np.flipud(image)

# Flip horizontally
flipped_h = np.fliplr(image)

# Transpose
transposed = image.T

# Normalize to [0, 255]
normalized = ((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8)

print(f"Original shape: {image.shape}")
print(f"Value range: [{image.min():.2f}, {image.max():.2f}]")
```

### Distance Matrices

```python
import numpy as np

# Points in 2D
points = np.random.rand(100, 2)

# Pairwise distances (broadcasting)
diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
distances = np.sqrt(np.sum(diff**2, axis=2))

print(f"Distance matrix shape: {distances.shape}")
print(f"Max distance: {distances.max():.4f}")

# Find nearest neighbors
for i in range(5):
    # Exclude self (distance = 0)
    dists = distances[i].copy()
    dists[i] = np.inf
    nearest = np.argmin(dists)
    print(f"Point {i} nearest to point {nearest}, distance: {distances[i, nearest]:.4f}")
```

### Sliding Window Operations

```python
import numpy as np

def sliding_window_view(arr, window_size):
    """Create sliding window views of array."""
    shape = (arr.shape[0] - window_size + 1, window_size)
    strides = (arr.strides[0], arr.strides[0])
    return np.lib.stride_tricks.as_strided(arr, shape=shape, strides=strides)

# Time series data
data = np.random.rand(100)

# Create sliding windows
windows = sliding_window_view(data, window_size=10)

# Compute statistics for each window
window_means = np.mean(windows, axis=1)
window_stds = np.std(windows, axis=1)

print(f"Number of windows: {len(windows)}")
print(f"First window mean: {window_means[0]:.4f}")
```

## Performance Optimization

### Vectorization Examples

```python
import numpy as np
import time

# Bad: Python loop
def sum_python_loop(arr):
    total = 0
    for x in arr:
        total += x**2
    return total

# Good: Vectorized
def sum_vectorized(arr):
    return np.sum(arr**2)

# Benchmark
arr = np.random.rand(1000000)

start = time.time()
result1 = sum_python_loop(arr)
time_loop = time.time() - start

start = time.time()
result2 = sum_vectorized(arr)
time_vec = time.time() - start

print(f"Loop time: {time_loop:.4f}s")
print(f"Vectorized time: {time_vec:.4f}s")
print(f"Speedup: {time_loop/time_vec:.1f}x")
```

### Memory-Efficient Operations

```python
import numpy as np

# Bad: Creates intermediate arrays
def inefficient(arr):
    temp1 = arr * 2
    temp2 = temp1 + 5
    temp3 = temp2 ** 2
    return temp3

# Good: In-place operations
def efficient(arr):
    result = arr.copy()
    result *= 2
    result += 5
    result **= 2
    return result

# Even better: Single expression (optimized by NumPy)
def most_efficient(arr):
    return (arr * 2 + 5) ** 2
```

### Using numexpr for Complex Expressions

```python
import numpy as np

# For very large arrays and complex expressions,
# numexpr can be faster (requires installation)

# Without numexpr
a = np.random.rand(10000000)
b = np.random.rand(10000000)
result = 2*a + 3*b**2 - np.sqrt(a)

# With numexpr (if installed)
# import numexpr as ne
# result = ne.evaluate('2*a + 3*b**2 - sqrt(a)')
```

## Common Pitfalls and Solutions

### NaN Handling

```python
import numpy as np

arr = np.array([1, 2, np.nan, 4, 5, np.nan])

# Problem: Regular functions return NaN
mean = np.mean(arr)  # Returns nan

# Solution: Use nan-safe functions
mean = np.nanmean(arr)  # Returns 3.0
std = np.nanstd(arr)
sum_val = np.nansum(arr)

# Check for NaN
has_nan = np.isnan(arr).any()
where_nan = np.where(np.isnan(arr))[0]

# Remove NaN
arr_clean = arr[~np.isnan(arr)]

print(f"Mean (nan-safe): {mean}")
print(f"NaN positions: {where_nan}")
```

### Integer Division Pitfall

```python
import numpy as np

# Problem: Integer division with integers
a = np.array([1, 2, 3])
b = np.array([2, 2, 2])
result = a / b  # With Python 3, this is fine

# But be careful with older code or explicit int types
a_int = np.array([1, 2, 3], dtype=np.int32)
b_int = np.array([2, 2, 2], dtype=np.int32)

# In NumPy, / always gives float result
result_float = a_int / b_int  # [0.5, 1, 1.5]

# Use // for integer division
result_int = a_int // b_int  # [0, 1, 1]

print(f"Float division: {result_float}")
print(f"Integer division: {result_int}")
```

### Array Equality

```python
import numpy as np

a = np.array([1.0, 2.0, 3.0])
b = np.array([1.0, 2.0, 3.0])

# Problem: Can't use == directly for array comparison
# if a == b:  # ValueError!

# Solution 1: Element-wise comparison
equal_elements = a == b  # Boolean array

# Solution 2: Check if all elements equal
all_equal = np.all(a == b)

# Solution 3: array_equal
array_equal = np.array_equal(a, b)

# Solution 4: For floating point, use allclose
c = a + 1e-10
close_enough = np.allclose(a, c, rtol=1e-5, atol=1e-8)

print(f"All equal: {all_equal}")
print(f"Arrays equal: {array_equal}")
print(f"Close enough: {close_enough}")
```

### Memory Leaks with Views

```python
import numpy as np

# Problem: Large array kept in memory
large_array = np.random.rand(1000000, 100)
small_view = large_array[0:10]  # Just 10 rows

# large_array is kept in memory because small_view references it!
del large_array  # Doesn't free memory!

# Solution: Make a copy
large_array = np.random.rand(1000000, 100)
small_copy = large_array[0:10].copy()
del large_array  # Now memory is freed

# Check if it's a view
print(f"Is view? {small_view.base is not None}")
print(f"Is copy? {small_copy.base is None}")
```

This comprehensive NumPy guide covers 50+ examples across all major array operations and numerical computing workflows!
