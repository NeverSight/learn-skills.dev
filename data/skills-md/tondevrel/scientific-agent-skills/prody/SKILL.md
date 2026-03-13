---
name: prody
description: Protein Dynamics, Evolution, and Structure analysis. Specialized in Normal Mode Analysis (NMA) using Anisotropic (ANM) and Gaussian Network Models (GNM). Features tools for structural ensemble analysis, PCA, and co-evolutionary analysis (Evol). Use for protein flexibility prediction, collective motions, structural ensemble comparison, hinge region identification, binding site analysis, MD trajectory filtering, and evolutionary analysis.
version: 2.4
license: BSD-3-Clause
---

# ProDy - Protein Dynamics & Structural Biology

ProDy is designed to model the collective motions of proteins. It treats proteins as elastic networks, allowing researchers to predict functional movements and structural flexibility from a single PDB file or an ensemble of structures.

## When to Use

- Predicting protein flexibility and collective motions (ANM/GNM).
- Performing Principal Component Analysis (PCA) on structural ensembles or MD trajectories.
- Analyzing structural conservation and co-evolution (Evol).
- Comparing multiple protein structures (Ensemble analysis).
- Identifying hinge regions and rigid domains in proteins.
- Docking preparation and binding site analysis (druggability).
- Filtering MD trajectories based on collective modes.

## Reference Documentation

**Official docs**: http://prody.csb.pitt.edu/  
**Manual**: http://prody.csb.pitt.edu/manual/  
**Search patterns**: `prody.parsePDB`, `prody.ANM`, `prody.GNM`, `prody.select`, `prody.Ensemble`

## Core Principles

### Atom Selection Algebra

ProDy features a powerful selection language similar to VMD or PyMOL. You can select atoms by chain, residue, property, or proximity (e.g., `'protein and resname TRP and within 5 of resname HEM'`).

### Elastic Network Models (ENM)

- **GNM (Gaussian Network Model)**: Predicts magnitude of fluctuations (B-factors).
- **ANM (Anisotropic Network Model)**: Predicts direction and magnitude of motion.

### Ensembles

A collection of structures (e.g., multiple NMR models or MD frames) stored in a way that allows for rapid statistical analysis and PCA.

## Quick Reference

### Installation

```bash
pip install prody
```

### Standard Imports

```python
import numpy as np
from prody import *
# Optional: for plotting
# confProDy(auto_show=False)
```

### Basic Pattern - Normal Mode Analysis

```python
from prody import *

# 1. Parse structure
atoms = parsePDB('1p38')
calphas = atoms.select('protein and calpha')

# 2. Build and solve ANM
anm = ANM('p38_anm')
anm.buildHessian(calphas)
anm.calcModes(n_modes=20)

# 3. Analyze results
for mode in anm[:3]:
    print(f"Mode {mode.getIndex()}: Variance = {mode.getVariance():.2f}")

# 4. Save for visualization (NMD format for VMD/PyMOL)
writeNMD('p38_modes.nmd', anm, calphas)
```

## Critical Rules

### ✅ DO

- **Select C-alphas for NMA** - For large systems, ENMs (ANM/GNM) are most effective and computationally efficient when applied only to C-alpha atoms.
- **Always Align Ensembles** - Before performing PCA on a structural ensemble, ensure all frames are aligned to a reference structure using `ensemble.iterpose()`.
- **Use select() early** - Filter your PDB object to only necessary chains/atoms to save memory during Hessian matrix calculations.
- **Check Eigensolver Convergence** - Ensure the calculated modes represent the majority of the variance.
- **Preserve Atom Orders** - When comparing structures, ensure atom selections result in matching indices using `matchAlign()`.

### ❌ DON'T

- **Run NMA on raw PDBs** - PDBs often have missing loops or multiple occupancies. Clean or select specific chains before analysis.
- **Ignore the "Zero Modes"** - The first 6 modes of an ANM are rigid-body translations/rotations and have zero frequency. Real biological motion starts at mode index 6.
- **Calculate Hessian for All-Atom large proteins** - All-atom ENM creates a 3N×3N matrix; for a 1000-residue protein, this is a 30,000×30,000 matrix, which is memory-intensive.

## Anti-Patterns (NEVER)

```python
from prody import *

# ❌ BAD: Iterating over atoms to find distance
# for a1 in atoms:
#     for a2 in atoms: ... # O(N^2) Python loop

# ✅ GOOD: Use selection algebra
nearby = atoms.select('within 5 of resname LIG')

# ❌ BAD: PCA on unaligned frames
# pca = PCA('test'); pca.buildCovariance(coord_array) # Wrong!

# ✅ GOOD: Create Ensemble and interpose
ens = Ensemble(atoms)
ens.addCoordset(trajectory)
ens.iterpose() # Crucial step
pca = PCA('test')
pca.buildCovariance(ens)

# ❌ BAD: Using NMA modes 0-5 for biology
# slow_mode = anm[0] # This is just a translation/rotation
```

## Atom Selection & Manipulation

### Powerful Queries

```python
atoms = parsePDB('3hhr')

# Chain and residue range
heavy_chain = atoms.select('chain H and resnum 1 to 120')

# Chemical properties
backbone = atoms.select('backbone')
hydrophobic = atoms.select('resname ALA VAL ILE LEU MET PHE TYR TRP')

# Proximity (Binding site)
site = atoms.select('protein and within 10 of resname ATP')

# Geometric center
center = calcCenter(site)
```

## Elastic Network Models (ENM)

### GNM (Fluctuations)

```python
gnm = GNM('1p38_gnm')
gnm.buildKirchhoff(calphas, cutoff=10.0)
gnm.calcModes()

# Cross-correlations (How atoms move together)
cross_corr = calcCrossCorr(gnm)

# Square fluctuations (Theoretical B-factors)
sq_flucts = calcSqFlucts(gnm)
```

### ANM (Directions of motion)

```python
anm = ANM('1p38_anm')
anm.buildHessian(calphas, cutoff=15.0)
anm.calcModes()

# Getting the hinge regions (where motion changes direction)
hinges = findHinges(anm[0]) # From the slowest mode
```

## Ensemble Analysis and PCA

### Structural Comparison

```python
# Parse multiple structures
pdb_ids = ['1p38', '1zz2', '1ywr']
structures = [parsePDB(pid) for pid in pdb_ids]

# Align and match
ensemble = Ensemble('p38_set')
for s in structures:
    # Match calphas of s to the reference first structure
    mappings = matchAlign(s, structures[0])
    ensemble.addCoordset(mappings[0][0]) # Add matched coords

# PCA
pca = PCA('p38_pca')
pca.buildCovariance(ensemble)
pca.calcModes()

# Project structures onto PCs
projection = ensemble.getProjection(pca[:2])
```

## Evolutionary Analysis (Evol)

### Sequence Conservation and Co-evolution

```python
# Load Multiple Sequence Alignment (MSA)
msa = parseMSA('p38_alignment.fasta')

# Calculate conservation (Shannon Entropy)
entropy = calcShannonEntropy(msa)

# Mutual Information (Co-evolution)
mi = calcMutualInformation(msa)

# Direct Coupling Analysis (DCA) - requires external tools or specific plugins
# dca = calcDirectCovariance(msa)
```

## Practical Workflows

### 1. Identifying Functional "Hinges"

```python
def get_protein_hinges(pdb_id):
    atoms = parsePDB(pdb_id)
    calphas = atoms.select('protein and calpha')
    
    anm = ANM(pdb_id)
    anm.buildHessian(calphas)
    anm.calcModes()
    
    # Hinge residues for the first two functional modes
    hinges_m1 = findHinges(anm[0])
    hinges_m2 = findHinges(anm[1])
    
    return list(set(hinges_m1) | set(hinges_m2))
```

### 2. Comparing MD Trajectory to ANM Modes

```python
def compare_md_to_anm(md_traj, p_pdb):
    # 1. ANM from static structure
    atoms = parsePDB(p_pdb)
    anm = ANM('static')
    anm.buildHessian(atoms.select('calpha'))
    anm.calcModes()
    
    # 2. PCA from MD
    ens = Ensemble('md')
    ens.setCoords(atoms)
    ens.addCoordset(md_traj)
    ens.iterpose()
    pca = PCA('md_pca')
    pca.buildCovariance(ens)
    pca.calcModes()
    
    # 3. Overlap (Inner product of modes)
    overlap = calcOverlap(anm[0], pca[0])
    return overlap
```

### 3. Druggability Analysis (TRAWLER/ProDy Integration)

```python
# Note: Full druggability analysis usually involves 'hotspot' calculations
def binding_site_flexibility(atoms, lig_resname):
    site = atoms.select(f'protein and within 8 of resname {lig_resname}')
    # Calculate GNM just for the site context
    gnm = GNM('site')
    gnm.buildKirchhoff(atoms.select('calpha'))
    gnm.calcModes()
    
    # High fluctuations = likely flexible binding site
    flucts = calcSqFlucts(gnm)
    return flucts[site.getIndices()]
```

## Performance Optimization

### Memory Management with Large Hessians

For very large complexes (Ribosomes, Capsids), use sparse matrices or the Hierarchical Network Model (HNM) if available.

### Parallel MSA Parsing

When dealing with massive alignments (100k+ sequences), use `parseMSA` with specific memory-efficient flags.

## Common Pitfalls and Solutions

### Atom Mapping Mismatch

When comparing two PDBs of the same protein, one might have missing residues.

```python
# ❌ Problem: ensemble.addCoordset(pdb2) fails due to different atom counts
# ✅ Solution: Use matchAlign
matches = matchAlign(pdb2, pdb1)
if matches:
    ensemble.addCoordset(matches[0][0])
```

### Non-Standard Residues

ProDy might not recognize unusual ligands as 'hetero' or 'protein'.

```python
# ✅ Solution: Use specific residue names or 'all'
ligand = atoms.select('resname MYL')
```

### Hessian Singularities

If your protein has disconnected parts, the Hessian will have more than 6 zero eigenvalues.

```python
# ✅ Solution: Check connectivity
if not atoms.select('protein').connected:
    print("Warning: Disconnected components found!")
```

## Best Practices

1. Always select C-alpha atoms for NMA on large proteins to reduce computational cost.
2. Align all structures in an ensemble before performing PCA using `iterpose()`.
3. Filter PDB structures early using selection algebra to reduce memory usage.
4. Remember that ANM modes 0-5 are rigid-body motions; biological motion starts at mode 6.
5. Use `matchAlign()` when comparing structures with different atom counts or missing residues.
6. Check for disconnected components before building Hessian matrices.
7. Use appropriate cutoff distances (typically 10-15 Å for C-alpha networks).
8. Validate eigensolver convergence to ensure meaningful results.
9. Save modes in NMD format for visualization in VMD or PyMOL.
10. Consider using sparse matrix representations for very large systems.

ProDy is the essential toolkit for the "Dynamic" in Structural Biology. By treating proteins as physical networks, it provides a bridge between static snapshots and the vibrating reality of life at the molecular scale.
