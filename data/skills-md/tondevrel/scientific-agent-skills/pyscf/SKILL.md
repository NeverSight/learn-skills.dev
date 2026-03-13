---
name: pyscf
description: Comprehensive guide for PySCF - Python-based Simulations of Chemistry Framework. Use for ab initio quantum chemistry calculations including Hartree-Fock, DFT, MP2, CCSD, geometry optimization, excited states, and molecular properties. Industry-standard library for electronic structure calculations.
version: 2.5.0
license: Apache-2.0
---

# PySCF - Quantum Chemistry Framework

Python library for ab initio electronic structure calculations and quantum chemistry.

## When to Use

- Running Hartree-Fock (HF) and Density Functional Theory (DFT) calculations
- Calculating molecular energies and gradients
- Optimizing molecular geometries
- Computing post-HF methods (MP2, CCSD, CI, coupled-cluster)
- Analyzing molecular orbitals and electron density
- Calculating excited states (TD-DFT, CI, EOM-CCSD)
- Computing molecular properties (dipole, charges, NMR, IR)
- Performing periodic calculations (solids, surfaces)
- Benchmarking quantum chemistry methods
- Integrating quantum calculations with ML/AI workflows

## Reference Documentation

**Official docs**: https://pyscf.org/  
**Search patterns**: `gto.M`, `scf.RHF`, `dft.RKS`, `mp.MP2`, `optimize`, `tddft.TDDFT`

## Core Principles

### Use PySCF For

| Task | Module | Example |
|------|--------|---------|
| Build molecule | `gto` | `gto.M(atom='H 0 0 0; H 0 0 1')` |
| Hartree-Fock | `scf` | `scf.RHF(mol).run()` |
| DFT calculation | `dft` | `dft.RKS(mol, xc='B3LYP')` |
| MP2 correlation | `mp` | `mp.MP2(mf).run()` |
| Coupled-cluster | `cc` | `cc.CCSD(mf).run()` |
| Geometry optimization | `geomopt` | `optimize(mf)` |
| Excited states | `tddft` | `tddft.TDDFT(mf).run()` |
| Periodic systems | `pbc` | `pbc.gto.Cell()` |

### Do NOT Use For

- Molecular dynamics simulations (use GROMACS, OpenMM, ASE)
- Very large systems (>1000 atoms) - use semi-empirical or force fields
- Interactive visualization (use PyMOL, VMD)
- High-throughput virtual screening (too slow)
- Real-time quantum simulations

## Quick Reference

### Installation

```bash
# pip (recommended)
pip install pyscf

# With extensions
pip install pyscf[geomopt,dftd3,dmrgscf]

# From conda
conda install -c pyscf pyscf

# Development version
pip install git+https://github.com/pyscf/pyscf
```

### Standard Imports

```python
# Core modules
from pyscf import gto, scf, dft
from pyscf import mp, cc, ci
from pyscf import grad, geomopt
from pyscf import tddft, tdscf
from pyscf import lo, ao2mo

# Tools
from pyscf.tools import molden, cubegen
import numpy as np
```

### Basic Pattern - Single Point Energy

```python
from pyscf import gto, scf

# 1. Build molecule
mol = gto.M(
    atom='O 0 0 0; H 0 1 0; H 0 0 1',
    basis='6-31g',
    charge=0,
    spin=0  # 2S, 0 = singlet
)

# 2. Run SCF
mf = scf.RHF(mol)
energy = mf.kernel()

# 3. Check convergence
if not mf.converged:
    raise RuntimeError("SCF did not converge")

print(f"E(HF) = {energy:.8f} Hartree")
```

### Basic Pattern - DFT Calculation

```python
from pyscf import gto, dft

mol = gto.M(atom='C 0 0 0; O 0 0 1.2', basis='def2-tzvp')

# DFT with B3LYP
mf = dft.RKS(mol)
mf.xc = 'B3LYP'
energy = mf.kernel()

print(f"E(B3LYP) = {energy:.8f} Hartree")
```

### Basic Pattern - Geometry Optimization

```python
from pyscf import gto, scf
from pyscf.geomopt.geometric_solver import optimize

mol = gto.M(atom='H 0 0 0; H 0 0 1.5', basis='6-31g')
mf = scf.RHF(mol)

# Optimize geometry
mol_eq = optimize(mf)

print(f"Optimized geometry:\n{mol_eq.atom}")
```

## Critical Rules

### ✅ DO

- **Check convergence** - Always verify `mf.converged == True`
- **Start with small basis** - Test with STO-3G or 3-21G first
- **Specify charge and spin** - Be explicit about electronic state
- **Save results** - Use `chkfile` for restart capability
- **Use symmetry** - Enable when applicable for speed
- **Provide good initial guess** - Use `init_guess='minao'` or previous results
- **Monitor memory** - Set `max_memory` appropriately
- **Verify units** - PySCF uses Bohr and Hartree internally
- **Use density fitting** - Enable for large systems
- **Check multiplicity** - Ensure spin matches expected state

### ❌ DON'T

- **Skip convergence check** - Never use results from unconverged calculation
- **Use huge basis sets initially** - Start small, expand gradually
- **Ignore charge/spin** - Defaults may not match your system
- **Run without `chkfile`** - You'll lose data if crash occurs
- **Disable symmetry unnecessarily** - It speeds up calculations
- **Mix coordinate systems** - Be consistent with Angstrom vs Bohr
- **Use wrong multiplicity** - 2S+1, not 2S
- **Forget about memory** - Large calculations can OOM
- **Trust unconverged results** - They're meaningless
- **Compare methods without same basis** - Use consistent basis sets

## Anti-Patterns (NEVER)

```python
# ❌ BAD: Not checking convergence
mf = scf.RHF(mol)
energy = mf.kernel()
# Use energy without checking convergence!

# ✅ GOOD: Always check convergence
mf = scf.RHF(mol)
energy = mf.kernel()
if not mf.converged:
    raise RuntimeError("SCF not converged, results unreliable")

# ❌ BAD: Using huge basis immediately
mol = gto.M(atom='protein.xyz', basis='def2-qzvppd')
# This will take forever or crash!

# ✅ GOOD: Start small, expand if needed
mol = gto.M(atom='protein.xyz', basis='sto-3g')
# Test first, then use def2-svp, def2-tzvp, etc.

# ❌ BAD: Ignoring electronic state
mol = gto.M(atom='O 0 0 0; O 0 0 1.2')
mf = scf.RHF(mol)  # What charge? What spin?

# ✅ GOOD: Explicit state specification
mol = gto.M(
    atom='O 0 0 0; O 0 0 1.2',
    charge=0,
    spin=2  # Triplet O2
)
mf = scf.ROHF(mol)  # Restricted open-shell for triplet

# ❌ BAD: No checkpoint file
mf = scf.RHF(mol)
mf.kernel()  # If crash, lose everything!

# ✅ GOOD: Use checkpoint files
mf = scf.RHF(mol)
mf.chkfile = 'calculation.chk'
mf.kernel()
# Can restart if needed

# ❌ BAD: Wrong multiplicity
mol = gto.M(atom='O 0 0 0; O 0 0 1.2', spin=2)  # Wrong!
# spin should be 2S, not multiplicity!

# ✅ GOOD: Correct spin specification
mol = gto.M(
    atom='O 0 0 0; O 0 0 1.2',
    spin=2  # 2S = 2 for triplet (multiplicity = 2S+1 = 3)
)
```

## Molecule Building

### Basic Molecule Definition

```python
from pyscf import gto

# Cartesian coordinates (Angstrom by default)
mol = gto.M(
    atom='''
        O  0.0  0.0  0.0
        H  0.0  1.0  0.0
        H  0.0  0.0  1.0
    ''',
    basis='6-31g',
    charge=0,
    spin=0
)

# Compact format
mol = gto.M(
    atom='O 0 0 0; H 0 1 0; H 0 0 1',
    basis='6-31g'
)

# Using tuple format
mol = gto.M(
    atom=[
        ('O', (0.0, 0.0, 0.0)),
        ('H', (0.0, 1.0, 0.0)),
        ('H', (0.0, 0.0, 1.0))
    ],
    basis='6-31g'
)
```

### Loading from Files

```python
from pyscf import gto

# From XYZ file
mol = gto.M(atom='molecule.xyz', basis='6-31g')

# From PDB file
mol = gto.M(atom='protein.pdb', basis='sto-3g')

# From Z-matrix
mol = gto.M(
    atom='''
    H
    H  1  0.74
    ''',
    basis='6-31g'
)
```

### Molecular Properties and Info

```python
from pyscf import gto

mol = gto.M(atom='H2O', basis='6-31g')

# Basic properties
print(f"Number of atoms: {mol.natm}")
print(f"Number of electrons: {mol.nelectron}")
print(f"Number of basis functions: {mol.nao_nr()}")
print(f"Charge: {mol.charge}")
print(f"Spin (2S): {mol.spin}")
print(f"Nuclear repulsion: {mol.energy_nuc():.8f}")

# Atom information
for i in range(mol.natm):
    atom_symbol = mol.atom_symbol(i)
    atom_charge = mol.atom_charge(i)
    coord = mol.atom_coord(i)
    print(f"Atom {i}: {atom_symbol} (Z={atom_charge}) at {coord}")
```

### Basis Set Specification

```python
from pyscf import gto

# Single basis for all atoms
mol = gto.M(atom='H2O', basis='6-31g')

# Different basis for different atoms
mol = gto.M(
    atom='H2O',
    basis={
        'O': '6-311g**',
        'H': '6-31g'
    }
)

# Custom basis sets
mol = gto.M(
    atom='H 0 0 0; H 0 0 1',
    basis={
        'H': gto.basis.parse('''
            H    S
                 13.0107010              0.19682158E-01
                  1.9622572              0.13796524
                  0.44453796             0.47831935
            H    S
                  0.12194962             1.0000000
        ''')
    }
)
```

### Molecular Symmetry

```python
from pyscf import gto

# Auto-detect symmetry
mol = gto.M(atom='H2O', basis='6-31g', symmetry=True)
print(f"Point group: {mol.groupname}")
print(f"Irreps: {mol.irrep_name}")

# Specify symmetry
mol = gto.M(atom='H2O', basis='6-31g', symmetry='C2v')

# Disable symmetry
mol = gto.M(atom='H2O', basis='6-31g', symmetry=False)
```

## Hartree-Fock Methods

### Restricted Hartree-Fock (RHF)

```python
from pyscf import gto, scf

# Closed-shell molecule
mol = gto.M(atom='H2O', basis='6-31g')
mf = scf.RHF(mol)

# Run calculation
energy = mf.kernel()

if mf.converged:
    print(f"E(RHF) = {energy:.8f} Hartree")
    print(f"Orbital energies: {mf.mo_energy}")
else:
    print("SCF not converged")
```

### Unrestricted Hartree-Fock (UHF)

```python
from pyscf import gto, scf

# Open-shell molecule (triplet O2)
mol = gto.M(
    atom='O 0 0 0; O 0 0 1.2',
    basis='6-31g',
    spin=2  # Triplet
)

mf = scf.UHF(mol)
energy = mf.kernel()

# Analyze spin
print(f"<S^2> = {mf.spin_square()[0]:.4f}")  # Should be ~2.0 for triplet
```

### Restricted Open-Shell HF (ROHF)

```python
from pyscf import gto, scf

# Open-shell with restricted spatial orbitals
mol = gto.M(
    atom='O 0 0 0; O 0 0 1.2',
    basis='6-31g',
    spin=2
)

mf = scf.ROHF(mol)
energy = mf.kernel()

print(f"E(ROHF) = {energy:.8f} Hartree")
```

### SCF Convergence Control

```python
from pyscf import gto, scf

mol = gto.M(atom='H2O', basis='6-31g')
mf = scf.RHF(mol)

# Convergence parameters
mf.conv_tol = 1e-8  # Energy convergence threshold
mf.conv_tol_grad = 1e-5  # Gradient convergence
mf.max_cycle = 100  # Maximum iterations
mf.diis_space = 12  # DIIS history size

# Initial guess
mf.init_guess = 'minao'  # Options: 'minao', 'atom', '1e', 'huckel'

# Level shift (helps difficult cases)
mf.level_shift = 0.5

energy = mf.kernel()
```

### Convergence Strategies for Difficult Cases

```python
from pyscf import gto, scf

mol = gto.M(atom='difficult_molecule.xyz', basis='6-31g')

# Strategy 1: Smaller basis first
mol_small = gto.M(atom='difficult_molecule.xyz', basis='sto-3g')
mf_small = scf.RHF(mol_small)
mf_small.kernel()

# Use small basis result as initial guess
mol_large = gto.M(atom='difficult_molecule.xyz', basis='6-31g')
mf = scf.RHF(mol_large)
mf.init_guess = mf_small.make_rdm1()  # Use small basis density

# Strategy 2: Use level shift
mf.level_shift = 0.3
mf.kernel()

# Strategy 3: Try different initial guess
if not mf.converged:
    mf.init_guess = 'atom'
    mf.kernel()
```

## Density Functional Theory

### Basic DFT Calculation

```python
from pyscf import gto, dft

mol = gto.M(atom='H2O', basis='def2-tzvp')

# Setup DFT
mf = dft.RKS(mol)
mf.xc = 'B3LYP'  # Hybrid functional

energy = mf.kernel()
print(f"E(B3LYP) = {energy:.8f} Hartree")
```

### Common Functionals

```python
from pyscf import gto, dft

mol = gto.M(atom='CH4', basis='6-31g')

# LDA
mf = dft.RKS(mol)
mf.xc = 'LDA,VWN'
e_lda = mf.kernel()

# GGA
mf.xc = 'PBE'
e_pbe = mf.kernel()

# Hybrid GGA
mf.xc = 'B3LYP'
e_b3lyp = mf.kernel()

# Meta-GGA
mf.xc = 'M06'
e_m06 = mf.kernel()

# Range-separated
mf.xc = 'wB97X-D'
e_wb97xd = mf.kernel()

print(f"LDA:    {e_lda:.6f}")
print(f"PBE:    {e_pbe:.6f}")
print(f"B3LYP:  {e_b3lyp:.6f}")
print(f"M06:    {e_m06:.6f}")
print(f"wB97X-D: {e_wb97xd:.6f}")
```

### Unrestricted DFT

```python
from pyscf import gto, dft

# Radical species
mol = gto.M(
    atom='C 0 0 0; H 0 0 1; H 0 1 0; H 1 0 0',  # CH3 radical
    basis='6-31g*',
    spin=1  # Doublet
)

mf = dft.UKS(mol)
mf.xc = 'B3LYP'
energy = mf.kernel()

print(f"<S^2> = {mf.spin_square()[0]:.4f}")  # Should be ~0.75 for doublet
```

### Grid and Integration

```python
from pyscf import gto, dft

mol = gto.M(atom='H2O', basis='6-31g')
mf = dft.RKS(mol)
mf.xc = 'B3LYP'

# Set grid quality
mf.grids.level = 3  # 0=coarse, 3=fine, 5=very fine
mf.grids.prune = True  # Prune grid points

# Custom grid
from pyscf.dft import gen_grid
mf.grids = gen_grid.Grids(mol)
mf.grids.atom_grid = {"H": (50, 194), "O": (75, 302)}  # (radial, angular)
mf.grids.build()

energy = mf.kernel()
```

### Dispersion Corrections

```python
from pyscf import gto, dft

mol = gto.M(atom='benzene.xyz', basis='def2-tzvp')
mf = dft.RKS(mol)

# DFT-D3 dispersion
mf.xc = 'B3LYP'
mf._numint.libxc = dft.xcfun  # Use XCFun for better D3

# Or use PySCF's D3 interface
from pyscf import dftd3
mf = dftd3.dftd3(mf)

energy = mf.kernel()
```

## Post-Hartree-Fock Methods

### MP2 - Second-Order Møller-Plesset

```python
from pyscf import gto, scf, mp

mol = gto.M(atom='H2O', basis='cc-pvdz')

# First run HF
mf = scf.RHF(mol)
mf.kernel()

# MP2 calculation
mp2 = mp.MP2(mf)
e_corr, t2 = mp2.kernel()

print(f"E(HF)  = {mf.e_tot:.8f}")
print(f"E(MP2) = {mp2.e_tot:.8f}")
print(f"E_corr = {e_corr:.8f}")
```

### CCSD - Coupled Cluster Singles and Doubles

```python
from pyscf import gto, scf, cc

mol = gto.M(atom='H2O', basis='cc-pvdz')

# HF reference
mf = scf.RHF(mol)
mf.kernel()

# CCSD
ccsd = cc.CCSD(mf)
e_corr, t1, t2 = ccsd.kernel()

print(f"E(HF)   = {mf.e_tot:.8f}")
print(f"E(CCSD) = {ccsd.e_tot:.8f}")
print(f"E_corr  = {e_corr:.8f}")
```

### CCSD(T) - with Perturbative Triples

```python
from pyscf import gto, scf, cc

mol = gto.M(atom='N2', basis='cc-pvdz')
mf = scf.RHF(mol)
mf.kernel()

# CCSD(T)
ccsd = cc.CCSD(mf)
ccsd.kernel()

# Perturbative triples correction
et = ccsd.ccsd_t()

print(f"E(HF)     = {mf.e_tot:.8f}")
print(f"E(CCSD)   = {ccsd.e_tot:.8f}")
print(f"E(T)      = {et:.8f}")
print(f"E(CCSD(T))= {ccsd.e_tot + et:.8f}")
```

### Configuration Interaction (CI)

```python
from pyscf import gto, scf, ci

mol = gto.M(atom='LiH', basis='6-31g')
mf = scf.RHF(mol)
mf.kernel()

# CISD
cisd = ci.CISD(mf)
e_cisd = cisd.kernel()[0]

# Full CI (only for small systems!)
fci = ci.FCI(mf)
e_fci = fci.kernel()[0]

print(f"E(HF)   = {mf.e_tot:.8f}")
print(f"E(CISD) = {e_cisd:.8f}")
print(f"E(FCI)  = {e_fci:.8f}")
```

### CASSCF - Complete Active Space

```python
from pyscf import gto, scf, mcscf

mol = gto.M(atom='O 0 0 0; O 0 0 1.2', basis='6-31g', spin=2)
mf = scf.ROHF(mol)
mf.kernel()

# CASSCF(6,6) - 6 electrons in 6 orbitals
mc = mcscf.CASSCF(mf, 6, 6)
mc.kernel()

print(f"E(CASSCF) = {mc.e_tot:.8f}")

# Analyze active space
from pyscf import tools
tools.molden.from_mo(mol, 'cas_orbitals.molden', mc.mo_coeff)
```

## Geometry Optimization

### Basic Optimization

```python
from pyscf import gto, scf
from pyscf.geomopt.geometric_solver import optimize

# Start with non-equilibrium geometry
mol = gto.M(
    atom='H 0 0 0; H 0 0 1.5',  # Too far apart
    basis='6-31g'
)

mf = scf.RHF(mol)

# Optimize
mol_eq = optimize(mf)

print("Optimized geometry:")
print(mol_eq.atom)
print(f"Final energy: {mf.e_tot:.8f}")
```

### Optimization with Constraints

```python
from pyscf import gto, scf
from pyscf.geomopt.geometric_solver import optimize

mol = gto.M(atom='H2O2', basis='6-31g')
mf = scf.RHF(mol)

# Constrained optimization (fix O-O distance)
def callback(mol):
    """Keep O-O distance fixed."""
    coords = mol.atom_coords()
    distance = np.linalg.norm(coords[0] - coords[1])
    return distance - 1.5  # Target distance

mol_eq = optimize(mf, constraints=callback)
```

### Transition State Optimization

```python
from pyscf import gto, scf
from pyscf.geomopt.berny_solver import optimize

mol = gto.M(atom='transition_state_guess.xyz', basis='6-31g')
mf = scf.RHF(mol)

# TS optimization (maximize along one mode)
mol_ts = optimize(mf, transition_state=True)

print(f"TS energy: {mf.e_tot:.8f}")
```

### Reaction Path Following

```python
from pyscf import gto, scf
from pyscf.geomopt.geometric_solver import optimize

# Optimize reactant
mol_reactant = gto.M(atom='reactant.xyz', basis='6-31g')
mf_reactant = scf.RHF(mol_reactant)
mol_reactant_opt = optimize(mf_reactant)

# Optimize product
mol_product = gto.M(atom='product.xyz', basis='6-31g')
mf_product = scf.RHF(mol_product)
mol_product_opt = optimize(mf_product)

# NEB or IRC for path
# (requires additional libraries)
```

## Molecular Properties

### Dipole Moment

```python
from pyscf import gto, scf

mol = gto.M(atom='H2O', basis='6-31g')
mf = scf.RHF(mol)
mf.kernel()

# Dipole moment
dip = mf.dip_moment(unit='Debye')
print(f"Dipole: {dip} Debye")
print(f"|μ| = {np.linalg.norm(dip):.4f} Debye")
```

### Mulliken Population Analysis

```python
from pyscf import gto, scf
from pyscf.tools import dump_mat

mol = gto.M(atom='H2O', basis='6-31g')
mf = scf.RHF(mol)
mf.kernel()

# Mulliken charges
mulliken = mf.mulliken_pop()
print("\nMulliken charges:")
for i, charge in enumerate(mulliken[1]):
    print(f"Atom {mol.atom_symbol(i)}: {charge:.4f}")
```

### Löwdin Population Analysis

```python
from pyscf import gto, scf
from pyscf import lo

mol = gto.M(atom='H2O', basis='6-31g')
mf = scf.RHF(mol)
mf.kernel()

# Löwdin analysis
lowdin_charges = lo.orth.lowdin(mol, mf.make_rdm1())
print("Löwdin charges:", lowdin_charges)
```

### Natural Bond Orbitals (NBO)

```python
from pyscf import gto, scf
from pyscf import nao

mol = gto.M(atom='CH3OH', basis='6-31g*')
mf = scf.RHF(mol)
mf.kernel()

# NBO analysis (requires pyscf-nao)
# nao.analyze(mf)
```

### Molecular Orbitals Analysis

```python
from pyscf import gto, scf

mol = gto.M(atom='H2O', basis='6-31g')
mf = scf.RHF(mol)
mf.kernel()

# Orbital energies
print("Orbital energies (eV):")
for i, e in enumerate(mf.mo_energy * 27.2114):  # Convert to eV
    occ = "occ" if i < mol.nelectron//2 else "vir"
    print(f"  MO {i}: {e:8.4f} eV ({occ})")

# HOMO-LUMO gap
homo_idx = mol.nelectron // 2 - 1
lumo_idx = homo_idx + 1
gap = (mf.mo_energy[lumo_idx] - mf.mo_energy[homo_idx]) * 27.2114
print(f"\nHOMO-LUMO gap: {gap:.4f} eV")
```

### Electron Density Analysis

```python
from pyscf import gto, scf
from pyscf.tools import cubegen

mol = gto.M(atom='H2O', basis='6-31g')
mf = scf.RHF(mol)
mf.kernel()

# Generate cube file for electron density
cubegen.density(mol, 'h2o_density.cube', mf.make_rdm1())

# Generate cube for specific orbital
cubegen.orbital(mol, 'h2o_homo.cube', mf.mo_coeff[:, homo_idx])
```

## Excited States

### TD-DFT for Excited States

```python
from pyscf import gto, dft, tddft

mol = gto.M(atom='H2O', basis='6-31g')

# Ground state DFT
mf = dft.RKS(mol)
mf.xc = 'B3LYP'
mf.kernel()

# TD-DFT for excited states
td = tddft.TDDFT(mf)
td.nroots = 5  # Number of excited states

excitations = td.kernel()[0]

print("Excitation energies:")
for i, e in enumerate(excitations):
    print(f"State {i+1}: {e * 27.2114:.4f} eV")
```

### TD-DFT with Oscillator Strengths

```python
from pyscf import gto, dft, tddft

mol = gto.M(atom='formaldehyde', basis='6-31g')
mf = dft.RKS(mol)
mf.xc = 'B3LYP'
mf.kernel()

td = tddft.TDDFT(mf)
td.nroots = 10

energies, xy = td.kernel()

# Calculate oscillator strengths
f = td.oscillator_strength()

print("\nExcitation   Energy (eV)   f")
print("-" * 40)
for i in range(len(energies)):
    print(f"  {i+1:2d}       {energies[i]*27.2114:8.4f}    {f[i]:.6f}")
```

### EOM-CCSD for Excited States

```python
from pyscf import gto, scf, cc

mol = gto.M(atom='H2O', basis='cc-pvdz')
mf = scf.RHF(mol)
mf.kernel()

# EOM-CCSD
eom = cc.eom_rccsd.EOMIP(cc.CCSD(mf))
e_ip, v_ip = eom.kernel(nroots=3)

print("Ionization potentials:")
for i, e in enumerate(e_ip):
    print(f"IP {i+1}: {e * 27.2114:.4f} eV")
```

### CASSCF/CASPT2 for Multi-Reference States

```python
from pyscf import gto, scf, mcscf

mol = gto.M(atom='ethylene', basis='6-31g')
mf = scf.RHF(mol)
mf.kernel()

# CASSCF for π → π* states
mc = mcscf.CASSCF(mf, 2, 2)  # 2e in 2 orbitals (π bonding/antibonding)

# State-averaged CASSCF (for excited states)
mc = mc.state_average_([0.5, 0.5])  # Equal weight S0 and S1
mc.kernel()

print("State-averaged energies:")
for i, e in enumerate(mc.e_states):
    print(f"State {i}: {e:.8f}")
```

## Advanced Workflows

### Potential Energy Surface Scan

```python
from pyscf import gto, scf
import numpy as np

def calculate_pes_scan(atom_template, distances, basis='6-31g'):
    """Scan potential energy surface along distance."""
    energies = []
    
    for d in distances:
        # Build molecule with current distance
        atom = atom_template.format(d=d)
        mol = gto.M(atom=atom, basis=basis)
        
        mf = scf.RHF(mol)
        energy = mf.kernel()
        
        if mf.converged:
            energies.append(energy)
        else:
            energies.append(np.nan)
    
    return np.array(energies)

# Example: H2 dissociation curve
distances = np.linspace(0.5, 3.0, 20)
atom_template = 'H 0 0 0; H 0 0 {d}'

energies = calculate_pes_scan(atom_template, distances)

# Find minimum
min_idx = np.nanargmin(energies)
print(f"Equilibrium distance: {distances[min_idx]:.3f} Angstrom")
print(f"Energy at minimum: {energies[min_idx]:.8f} Hartree")
```

### Thermochemistry

```python
from pyscf import gto, scf, hessian
import numpy as np

mol = gto.M(atom='H2O', basis='6-31g')
mf = scf.RHF(mol)
mf.kernel()

# Calculate Hessian (force constants)
h = hessian.RHF(mf)
hess = h.kernel()

# Vibrational frequencies
from pyscf.hessian import thermo
freq_info = thermo.harmonic_analysis(mol, hess)

print("Vibrational frequencies (cm^-1):")
print(freq_info['freq_wavenumber'])

# Thermochemistry at 298.15 K
results = thermo.thermo(mf, freq_info['freq_wavenumber'], 298.15)
print(f"\nZero-point energy: {results['ZPE']:.6f} Hartree")
print(f"Enthalpy: {results['H']:.6f} Hartree")
print(f"Entropy: {results['S']:.6f} Hartree/K")
print(f"Gibbs free energy: {results['G']:.6f} Hartree")
```

### NMR Chemical Shifts

```python
from pyscf import gto, scf
from pyscf.prop import nmr

mol = gto.M(atom='CH4', basis='6-31g*')
mf = scf.RHF(mol)
mf.kernel()

# NMR shielding tensors
nmr_calc = nmr.RHF(mf)
shielding = nmr_calc.kernel()

print("NMR shielding tensors:")
for i in range(mol.natm):
    print(f"{mol.atom_symbol(i)}: {shielding[i]} ppm")
```

### IR Spectra Calculation

```python
from pyscf import gto, scf, hessian
from pyscf.hessian import thermo

mol = gto.M(atom='CO2', basis='6-31g')
mf = scf.RHF(mol)
mf.kernel()

# Calculate Hessian
h = hessian.RHF(mf)
hess = h.kernel()

# Get frequencies and intensities
freq_info = thermo.harmonic_analysis(mol, hess)

print("IR Frequencies and Intensities:")
print("Freq (cm^-1)    Intensity")
for freq, intensity in zip(freq_info['freq_wavenumber'], 
                           freq_info['IR_intensity']):
    if freq > 0:  # Skip imaginary frequencies
        print(f"{freq:8.2f}      {intensity:.4f}")
```

### QMMM Calculations

```python
from pyscf import gto, scf, qmmm

# QM region
mol = gto.M(
    atom='C 0 0 0; H 0 1 0; H 1 0 0; H 0 0 1; H -1 0 0',
    basis='6-31g'
)

# MM point charges (environment)
mm_coords = np.array([
    [3.0, 0.0, 0.0],
    [0.0, 3.0, 0.0],
    [0.0, 0.0, 3.0]
])
mm_charges = np.array([-0.5, -0.5, 1.0])

# Add MM charges to QM calculation
mf = scf.RHF(mol)
mf = qmmm.mm_charge(mf, mm_coords, mm_charges)

energy = mf.kernel()
print(f"QM/MM energy: {energy:.8f}")
```

### Solvation Models (PCM)

```python
from pyscf import gto, scf, solvent

mol = gto.M(atom='H2O', basis='6-31g')

# Polarizable Continuum Model
mf = scf.RHF(mol)
mf = solvent.ddCOSMO(mf)  # ddCOSMO solvation
mf.with_solvent.eps = 78.3553  # Water dielectric

energy = mf.kernel()
print(f"Energy in solution: {energy:.8f}")
```

## Periodic Systems

### Basic Periodic Calculation

```python
from pyscf.pbc import gto, scf

# Define unit cell
cell = gto.Cell()
cell.atom = '''
    C 0 0 0
    C 1.68 1.68 1.68
'''
cell.basis = 'gth-dzvp'
cell.pseudo = 'gth-pade'
cell.a = '''
    0.0 3.37 3.37
    3.37 0.0 3.37
    3.37 3.37 0.0
'''
cell.unit = 'angstrom'
cell.build()

# k-points
kpts = cell.make_kpts([2, 2, 2])  # 2x2x2 k-point mesh

# Run calculation
kmf = scf.KRHF(cell, kpts)
energy = kmf.kernel()

print(f"Energy per unit cell: {energy:.8f}")
```

### Band Structure Calculation

```python
from pyscf.pbc import gto, scf, tools
import numpy as np

cell = gto.Cell()
# ... (build cell as above)

# Self-consistent calculation
kmf = scf.KRHF(cell)
kmf.kernel()

# Band structure along high-symmetry path
kpath = tools.pbc.get_kpath(cell, [10, 10, 10])
bands = []

for k in kpath:
    kmf_k = scf.KRHF(cell, k)
    kmf_k.kernel(dm0=kmf.make_rdm1())
    bands.append(kmf_k.mo_energy)

# Plot bands (requires matplotlib)
```

## Performance Optimization

### Density Fitting

```python
from pyscf import gto, scf

mol = gto.M(atom='protein_fragment.xyz', basis='def2-svp')

# Use density fitting for faster calculation
mf = scf.RHF(mol).density_fit()
mf.kernel()

# Can also specify auxiliary basis
mf = scf.RHF(mol).density_fit(auxbasis='def2-svp-jkfit')
mf.kernel()
```

### Parallel Computation

```python
from pyscf import gto, scf, lib

# Set number of threads
lib.num_threads(8)

mol = gto.M(atom='large_molecule.xyz', basis='6-31g')
mf = scf.RHF(mol)

# Enable parallel computation
mf.max_memory = 4000  # MB per thread
energy = mf.kernel()
```

### Memory Management

```python
from pyscf import gto, scf

mol = gto.M(atom='large_system.xyz', basis='6-31g')
mf = scf.RHF(mol)

# Set maximum memory (MB)
mf.max_memory = 8000  # 8 GB

# Use less memory (slower)
mf.direct_scf = True  # Direct SCF, no integrals stored

energy = mf.kernel()
```

### Checkpointing and Restart

```python
from pyscf import gto, scf, lib

mol = gto.M(atom='molecule.xyz', basis='6-31g')
mf = scf.RHF(mol)

# Save checkpoint
mf.chkfile = 'calculation.chk'
energy = mf.kernel()

# Restart from checkpoint
mf2 = scf.RHF(mol)
mf2.chkfile = 'calculation.chk'
mf2.init_guess = 'chkfile'
energy2 = mf2.kernel()
```

## Integration with Other Tools

### Export to Molden Format

```python
from pyscf import gto, scf
from pyscf.tools import molden

mol = gto.M(atom='H2O', basis='6-31g')
mf = scf.RHF(mol)
mf.kernel()

# Write Molden file for visualization
with open('molecule.molden', 'w') as f:
    molden.header(mol, f)
    molden.orbital_coeff(mol, f, mf.mo_coeff, ene=mf.mo_energy, occ=mf.mo_occ)
```

### Interface with ASE

```python
from pyscf import gto, scf
from ase import Atoms
from ase.optimize import BFGS

# Create ASE calculator wrapper
class PySCFCalculator:
    def __init__(self, basis='6-31g', method='RHF'):
        self.basis = basis
        self.method = method
    
    def get_potential_energy(self, atoms):
        mol = gto.M(
            atom=[(atoms.get_chemical_symbols()[i], atoms.positions[i]) 
                  for i in range(len(atoms))],
            basis=self.basis,
            unit='angstrom'
        )
        
        if self.method == 'RHF':
            mf = scf.RHF(mol)
        elif self.method == 'B3LYP':
            mf = dft.RKS(mol)
            mf.xc = 'B3LYP'
        
        return mf.kernel()

# Use with ASE
atoms = Atoms('H2O', positions=[[0,0,0], [0,1,0], [0,0,1]])
atoms.calc = PySCFCalculator()

# Optimize with ASE
opt = BFGS(atoms)
opt.run(fmax=0.01)
```

## Common Pitfalls and Solutions

### SCF Convergence Failures

```python
from pyscf import gto, scf

mol = gto.M(atom='difficult.xyz', basis='6-31g')
mf = scf.RHF(mol)

# Problem: SCF not converging
energy = mf.kernel()
if not mf.converged:
    # Solution 1: Use level shift
    mf.level_shift = 0.5
    mf.kernel()
    
    # Solution 2: Increase DIIS space
    if not mf.converged:
        mf.diis_space = 15
        mf.kernel()
    
    # Solution 3: Try different initial guess
    if not mf.converged:
        mf.init_guess = 'atom'
        mf.kernel()
    
    # Solution 4: Use smaller basis first
    if not mf.converged:
        mol_small = gto.M(atom='difficult.xyz', basis='sto-3g')
        mf_small = scf.RHF(mol_small).run()
        mf.init_guess = mf_small.make_rdm1()
        mf.kernel()
```

### Memory Issues

```python
from pyscf import gto, scf

# Problem: Running out of memory
mol = gto.M(atom='huge.xyz', basis='def2-tzvp')
mf = scf.RHF(mol)

# Solution 1: Use density fitting
mf = mf.density_fit()

# Solution 2: Set memory limit
mf.max_memory = 4000  # MB

# Solution 3: Use direct SCF
mf.direct_scf = True

energy = mf.kernel()
```

### Spin Contamination

```python
from pyscf import gto, scf

mol = gto.M(atom='radical.xyz', basis='6-31g', spin=1)

# Problem: UHF has spin contamination
mf = scf.UHF(mol)
mf.kernel()
s2 = mf.spin_square()[0]
print(f"<S^2> = {s2:.4f}  (expected 0.75)")

# Solution: Use ROHF if appropriate
if abs(s2 - 0.75) > 0.1:
    mf = scf.ROHF(mol)
    mf.kernel()
    print(f"Using ROHF instead")
```

### Basis Set Linear Dependency

```python
from pyscf import gto, scf

# Problem: Large basis sets can have linear dependencies
mol = gto.M(atom='molecule.xyz', basis='aug-cc-pvqz')
mf = scf.RHF(mol)

# Solution: Remove linear dependencies
from pyscf import lo
mf.kernel()

if not mf.converged:
    # Check condition number
    s = mf.get_ovlp()
    cond = np.linalg.cond(s)
    if cond > 1e10:
        print("Linear dependency detected")
        # Use canonical orthogonalization
        mf = scf.addons.remove_linear_dep_(mf)
        mf.kernel()
```

This comprehensive PySCF guide covers 50+ examples across all major quantum chemistry workflows!
