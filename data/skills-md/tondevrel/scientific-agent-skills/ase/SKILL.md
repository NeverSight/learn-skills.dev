---
name: ase
description: Atomic Simulation Environment - a set of tools for setting up, manipulating, running, visualizing, and analyzing atomistic simulations. Acts as a universal interface between Python and numerous quantum chemical and molecular dynamics codes. Use for building atomic structures, geometry optimization, molecular dynamics simulations, transition state searches (NEB), file format conversion (CIF, XYZ, POSCAR, PDB), electronic property calculations (DOS, band structures), and automating simulation workflows with DFT/MD codes like VASP, GPAW, Quantum ESPRESSO, LAMMPS.
version: 3.23
license: LGPL-2.1
---

# ASE - Atomic Simulation Environment

ASE is built around the Atoms object, which represents a collection of atoms with positions, atomic numbers, and a unit cell. It provides a common interface for interacting with various "Calculators" (external codes that compute energies and forces).

## When to Use

- Building complex atomic structures: molecules, crystals, surfaces, and nanoparticles.
- Running geometry optimizations (finding the minimum energy structure).
- Performing Molecular Dynamics (MD) simulations in various ensembles.
- Calculating Potential Energy Surfaces (PES) and transition states (NEB method).
- Converting between atomic file formats (CIF, XYZ, POSCAR, PDB, etc.).
- Calculating electronic properties like Density of States (DOS) and Band Structures.
- Automating simulation workflows involving multiple software packages.

## Reference Documentation

**Official docs**: https://wiki.fysik.dtu.dk/ase/  
**List of Calculators**: https://wiki.fysik.dtu.dk/ase/ase/calculators/calculators.html  
**Search patterns**: `ase.Atoms`, `ase.build`, `ase.optimize`, `ase.io.read`, `ase.calculators`

## Core Principles

### The Atoms Object

The heart of ASE. It stores:
- **positions**: Cartesian coordinates in Angstroms (Nx3 array).
- **symbols**: Chemical elements (e.g., 'H', 'Fe').
- **cell**: Unit cell vectors (3x3 matrix or 3/6 lengths/angles).
- **pbc**: Periodic Boundary Conditions (boolean for each axis).

### Calculators

ASE does not calculate energy itself. You attach a Calculator (e.g., GPAW, VASP, EMT, Lennard-Jones) to the Atoms object. When you call `atoms.get_potential_energy()`, ASE asks the calculator to perform the computation.

### Units

**Crucial Rule**: ASE uses eV (electron-volts) for energy and Angstroms for distance. Time is in ASE units (often converted to fs).

## Quick Reference

### Installation

```bash
pip install ase
```

### Standard Imports

```python
from ase import Atoms
from ase.build import molecule, bulk, surface
from ase.io import read, write
from ase.optimize import BFGS
from ase.visualize import view
```

### Basic Pattern - Creating and Optimizing a Molecule

```python
from ase.build import molecule
from ase.optimize import BFGS
from ase.calculators.emt import EMT # Simple effective medium theory calculator

# 1. Build structure
atoms = molecule('H2O')

# 2. Attach a calculator
atoms.calc = EMT()

# 3. Optimize geometry
opt = BFGS(atoms, trajectory='opt.traj')
opt.run(fmax=0.05) # Converge until forces are < 0.05 eV/Ang

print(f"Final Energy: {atoms.get_potential_energy():.3f} eV")
```

## Critical Rules

### ✅ DO

- **Specify Periodic Boundary Conditions** - Set `pbc=[True, True, True]` for crystals and `False` for isolated molecules.
- **Use Vectorized NumPy access** - Manipulate `atoms.positions` or `atoms.get_positions()` directly with NumPy.
- **Check convergence** - Always verify that your optimizer reached the desired `fmax`.
- **Set the unit cell correctly** - For periodic systems, the cell must be large enough to prevent self-interaction.
- **Use ase.build** - Leverage built-in functions for complex tasks like creating slabs (`surface`) or nanotubes.
- **Monitor trajectories** - Use `.traj` files to inspect the optimization or MD progress in ASE-GUI.

### ❌ DON'T

- **Manually loop over atoms** - Avoid Python loops for moving atoms; use `atoms.positions += displacement`.
- **Forget ASE units** - Don't mix kcal/mol or Hartrees without explicit conversion (`from ase.units import Hartree, kcal, mol`).
- **Assume vacuum is infinite** - For non-periodic directions in a slab, ensure enough vacuum padding (e.g., 10-15 Å).
- **Hardcode atomic numbers** - Use chemical symbols ('Au') instead of 79 for readability.

## Anti-Patterns (NEVER)

```python
# ❌ BAD: Moving atoms in a Python loop
for atom in atoms:
    atom.position += [0.1, 0, 0]

# ✅ GOOD: Vectorized movement
atoms.positions += [0.1, 0, 0]

# ❌ BAD: Not defining a cell for a "bulk" system
iron = Atoms('Fe', positions=[[0, 0, 0]]) # No cell = not a crystal!

# ✅ GOOD: Use the bulk constructor
from ase.build import bulk
iron = bulk('Fe', 'bcc', a=2.87)

# ❌ BAD: Ignoring forces after optimization
energy = atoms.get_potential_energy() # Optimization might have failed!

# ✅ GOOD: Check forces
forces = atoms.get_forces()
max_force = (forces**2).sum(axis=1).max()**0.5
if max_force > 0.05:
    print("Warning: Structure not converged!")
```

## Building Structures (ase.build)

### Molecules, Crystals, and Surfaces

```python
from ase.build import molecule, bulk, surface, add_adsorbate

# Molecule from database
h2o = molecule('H2O')

# Bulk crystal (Copper fcc)
cu = bulk('Cu', 'fcc', a=3.6)

# Surface slab (Al 111 surface, 3 layers)
slab = surface('Al', (1, 1, 1), layers=3)
slab.center(vacuum=10, axis=2) # Add 10A vacuum on Z axis

# Adding an adsorbate (CO on a surface)
co = molecule('CO')
add_adsorbate(slab, co, height=2.0, position='ontop')
```

## Optimization and Dynamics (ase.optimize, ase.md)

### Geometry Minimization

```python
from ase.optimize import QuasiNewton

# BFGS, LBFGS, GPMin, QuasiNewton are common choices
opt = QuasiNewton(atoms, trajectory='relax.traj', logfile='relax.log')
opt.run(fmax=0.01)
```

### Molecular Dynamics

```python
from ase.md.langevin import Langevin
from ase import units

# MD at 300K with Langevin thermostat
dyn = Langevin(atoms, 
               timestep=1.0 * units.fs, 
               temperature_K=300, 
               friction=0.01)

# Run for 1000 steps
dyn.run(1000)
```

## File I/O (ase.io)

### Reading and Writing

```python
from ase.io import read, write

# Read from XYZ or CIF
atoms = read('structure.cif')

# Read multiple frames from a trajectory
frames = read('simulation.traj', index=':') # All frames
last_5 = read('simulation.traj', index='-5:') # Last 5 frames

# Write to different formats
write('output.poscar', atoms, format='vasp')
write('movie.gif', frames, rotation='10x,10y,10z') # Create animated gif
```

## Advanced: Transition States (NEB)

### Nudged Elastic Band

```python
from ase.mep import NEB
from ase.optimize import BFGS

# Initial and Final states (must have same atoms/order)
initial = read('initial.traj')
final = read('final.traj')

# Create 5 images between initial and final
images = [initial]
for i in range(5):
    images.append(initial.copy())
images.append(final)

# Interpolate positions
neb = NEB(images)
neb.interpolate()

# Run optimization on all images
opt = BFGS(neb, trajectory='neb.traj')
opt.run(fmax=0.05)
```

## Practical Workflows

### 1. Lattice Parameter Scan (Equation of State)

```python
import numpy as np
from ase.build import bulk
from ase.calculators.emt import EMT

def find_opt_lattice():
    volumes = []
    energies = []
    for a in np.linspace(3.5, 3.7, 5):
        atoms = bulk('Cu', 'fcc', a=a)
        atoms.calc = EMT()
        volumes.append(atoms.get_volume())
        energies.append(atoms.get_potential_energy())
    
    # You can then fit these to Birch-Murnaghan EOS
    return volumes, energies
```

### 2. Vibrational Analysis (Thermodynamics)

```python
from ase.vibrations import Vibrations

# Calculate vibrations (requires a calculator)
vib = Vibrations(atoms)
vib.run()
vib.summary()

# Get Helmholtz free energy at 300K
from ase.thermochemistry import IdealGasThermo
thermo = IdealGasThermo(vib_energies=vib.get_frequencies(), 
                        geometry='nonlinear', 
                        potentialenergy=atoms.get_potential_energy())
F = thermo.get_helmholtz_free_energy(temperature=300)
```

### 3. Integration with PySCF (Quantum Chemistry)

```python
from ase.calculators.pyscf_calc import PySCF
from ase.build import molecule

atoms = molecule('H2')
# Define PySCF calculator
atoms.calc = PySCF(mol_options={'basis': '6-31g', 'spin': 0},
                   method='RKS.xc = "b3lyp"')

energy = atoms.get_potential_energy()
```

## Performance Optimization

### Using Symmetry

If building large crystals, using the spglib integration within ASE can help identify symmetry, though ASE's core structures don't automatically enforce it during optimization unless specific constraints are added.

### Constraints

Fixing atoms (e.g., bottom layers of a slab) speeds up relaxation significantly.

```python
from ase.constraints import FixAtoms

# Fix all atoms with Z-coordinate < 5.0
c = FixAtoms(mask=[atom.position[2] < 5.0 for atom in atoms])
atoms.set_constraint(c)
```

## Common Pitfalls and Solutions

### The "Missing Calculator" Error

```python
# ❌ Problem: atoms.get_potential_energy() fails
# ✅ Solution: Ensure .calc is set and external code is in PATH
import os
os.environ['VASP_COMMAND'] = 'mpirun vasp_std' # Example for VASP
```

### Cell Vector Sign Convention

ASE typically uses a right-handed coordinate system. Be careful when importing from old codes that might use different conventions.

### Purity of the Atoms Object

If you delete atoms from the list, the indices change.

```python
# ❌ Problem: Deleting atoms in a loop by index
# ✅ Solution: Use a mask or the .pop() method carefully
del atoms[[0, 5, 10]] # Bulk delete by index list
```

ASE is the standard "glue" of the atomistic simulation world. It allows you to switch from a simple empirical potential to an expensive DFT calculation by changing just one line of code (`atoms.calc`), making it indispensable for high-throughput computational materials science.
