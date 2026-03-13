---
name: qiskit-hardware
description: Advanced sub-skill for Qiskit focused on executing circuits on physical quantum processing units (QPUs). Covers IBM Quantum Runtime, error mitigation techniques (TREX, ZNE), hardware-aware transpilation, and low-level pulse control (OpenPulse).
version: 1.0
license: Apache-2.0
---

# Qiskit - Real Hardware & Pulse Control

Moving from simulators to real hardware requires a shift in mindset. You are no longer working with perfect "ideal" qubits, but with superconducting circuits that suffer from decoherence, readout errors, and crosstalk. This guide covers how to get the most science out of noisy intermediate-scale quantum (NISQ) devices.

## When to Use

- Executing quantum algorithms on real IBM Quantum backends.
- Characterizing hardware noise (T1, T2 relaxation times).
- Implementing Error Mitigation to improve result accuracy.
- Using Qiskit Pulse to define custom microwave pulses (OpenPulse).
- Optimizing circuits for specific hardware topologies (coupling maps).
- Benchmarking quantum advantage in real-world conditions.

## Reference Documentation

- **IBM Quantum Learning**: https://learning.quantum.ibm.com/
- **Qiskit Runtime Docs**: https://docs.quantum.ibm.com/run
- **Qiskit Pulse Guide**: https://docs.quantum.ibm.com/build/pulse
- **Search patterns**: `QiskitRuntimeService`, `Sampler`, `Estimator`, `transpile`, `InstructionScheduleMap`

## Core Principles

### 1. Qiskit Runtime (Primitives)

The modern way to interact with hardware. Instead of sending raw circuits, you use Primitives:

- **Sampler**: Returns quasi-probabilities (bitstrings).
- **Estimator**: Returns expectation values of observables (e.g., energy).

### 2. Transpilation (Hardware Mapping)

Physical backends only support a small set of "Basis Gates" (e.g., `rz`, `x`, `sx`, `ecr`). The Transpiler rewrites your abstract math into these specific instructions and maps virtual qubits to physical ones based on error rates.

### 3. Error Mitigation

Unlike Error Correction (which requires thousands of qubits), Mitigation uses statistical tricks (like TREX or ZNE) to "clean" the results after execution.

## Quick Reference: Connecting to Hardware

### Installation

```bash
pip install qiskit-ibm-runtime
```

### Setup and Job Execution

```python
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# 1. Initialize service (requires API key from quantum.ibm.com)
# service = QiskitRuntimeService(channel="ibm_quantum", token="YOUR_TOKEN")
service = QiskitRuntimeService() # Uses saved credentials

# 2. Select backend
backend = service.least_busy(operational=True, simulator=False)

# 3. Run job using Primitives
sampler = Sampler(backend=backend)
job = sampler.run([my_circuit])
result = job.result()
```

## Critical Rules

### ✅ DO

- **Check Calibration Data** - Backends change daily. Always check `backend.properties()` for the latest error rates before choosing qubits.
- **Use "Sessions"** - Wrap multiple related jobs in a `RuntimeSession` to minimize queue wait times.
- **Set optimization_level** - Use level 3 for hardware to enable advanced routing and gate fusion.
- **Apply Readout Mitigation** - Readout (measuring 0 as 1) is the largest error source. Use `resilience_level=1` in Primitives.
- **Use Dynamical Decoupling (DD)** - Add pulses to "idling" qubits to prevent them from losing their state while waiting for other gates.

### ❌ DON'T

- **Don't use execute()** - The old `qiskit.execute` is deprecated for hardware. Use `Sampler` and `Estimator`.
- **Don't run deep circuits** - NISQ devices have limited coherence. If your circuit depth > 50-100, the result will likely be pure noise.
- **Don't ignore the Coupling Map** - If you force a CNOT between two qubits that aren't physically connected, the transpiler will add many "SWAP" gates, increasing error.
- **Don't use qasm_simulator for hardware prep** - Use `FakeBackend` objects (e.g., `FakeManilaV2`) which mimic real hardware noise for local debugging.

## Hardware-Aware Transpilation

### Mapping to physical qubits

```python
from qiskit import transpile

# Basis gates for a specific backend
basis_gates = backend.operation_names
coupling_map = backend.coupling_map

# Optimized transpilation
optimized_circ = transpile(my_circuit, 
                           backend=backend,
                           optimization_level=3,
                           initial_layout=[0, 2, 4]) # Manual qubit selection
```

## Advanced Error Mitigation

### Resilience Levels in Estimator

```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator, EstimatorOptions

options = EstimatorOptions()
# resilience_level 0: No mitigation
# resilience_level 1: Readout mitigation (TREX)
# resilience_level 2: ZNE (Zero Noise Extrapolation) - expensive but accurate
options.resilience_level = 1 

estimator = Estimator(backend=backend, options=options)
```

## Low-Level: Qiskit Pulse (OpenPulse)

### Defining custom microwave signals

```python
from qiskit import pulse
from qiskit.circuit import Parameter

# Define a Gaussian pulse
amp = Parameter('amp')
with pulse.build(backend=backend, name='custom_pulse') as schedule:
    pulse.play(pulse.Gaussian(duration=160, amp=amp, sigma=40), pulse.drive_channel(0))

# Attach pulse to a gate
my_circuit.add_calibration('my_gate', [0], schedule, params=[amp])
```

## Practical Workflows

### 1. Finding the "Best" Qubits on a Device

```python
def get_best_qubits(backend, n_qubits):
    """Finds a linear chain of qubits with lowest error rates."""
    props = backend.properties()
    # Logic to parse gate_error and readout_error from props
    # and find a connected subgraph with minimal noise.
    pass
```

### 2. VQE on Hardware with Runtime

```python
from qiskit_ibm_runtime import Session, EstimatorV2 as Estimator

def run_hardware_vqe(ansatz, hamiltonian, backend):
    with Session(backend=backend) as session:
        estimator = Estimator(session=session)
        # Standard optimization loop (using SciPy)
        # Each 'step' runs a job within the same session
        pass
```

### 3. Measuring T1 Time (Relaxation)

```python
def t1_experiment(qubit, delay_times):
    circuits = []
    for t in delay_times:
        c = QuantumCircuit(qubit + 1)
        c.x(qubit) # Flip to |1>
        c.delay(t, qubit, unit='us') # Wait
        c.measure_all()
        circuits.append(c)
    # Execute on hardware and fit decay curve
```

## Performance Optimization

### 1. Job Batching

Submit multiple circuits in a single `run()` call to bypass repeated initialization overhead.

### 2. Transpiler Pass Manager

Create custom stages for transpilation to control exactly how your circuit is modified.

```python
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Unroller, BasicSwap
# custom_pm = PassManager([Unroller(['u3', 'cx']), BasicSwap(coupling_map)])
```

## Common Pitfalls and Solutions

### Queue Wait Times

Real hardware has high demand.

```python
# ✅ Solution: 
# 1. Use the 'least_busy' helper.
# 2. Check your IBM Quantum dashboard for reservation windows.
# 3. Use Runtime Sessions to group your jobs.
```

### "Depolarizing" Result

Your histogram looks like a flat line (random noise).

```python
# ✅ Solution:
# 1. Reduce circuit depth.
# 2. Use 'optimization_level=3'.
# 3. Apply Error Mitigation (resilience_level=1+).
# 4. Check if the backend is currently undergoing maintenance/calibration.
```

### Frequency Collisions

Two neighboring qubits have similar frequencies, leading to "Crosstalk".

```python
# ✅ Solution:
# Select qubits that are physically separated or have 
# significantly different frequencies in backend.properties().
```

Qiskit Hardware is where quantum theory meets the harsh reality of physics. Mastering these tools allows you to push the boundaries of what is possible on today's noisy devices, paving the way for the fault-tolerant era.
