---
name: openbabel
description: A chemical toolbox designed to speak the many languages of chemical data. Supports over 110 formats and provides tools for conversion, 3D structure generation, molecular searching (SMARTS), and force field calculations. Use for chemical file format conversion (SDF, PDB, SMILES, CIF, Gaussian), 3D coordinate generation from 2D structures, substructure searching with SMARTS patterns, molecular docking preparation, force field minimizations (UFF, GAFF, MMFF94), molecular fingerprints and Tanimoto coefficients, and batch processing of chemical databases.
version: 3.1
license: GPL-2.0
---

# Open Babel - The Universal Chemical Translator

Open Babel (and its Python wrapper pybel) is the essential tool for chemical data interoperability. It allows researchers to seamlessly move data between formats like SMILES, PDB, SDF, CIF, and Gaussian input/output.

## When to Use

- Converting chemical files between different formats (e.g., SDF to PDB).
- Generating 3D coordinates from 2D structures or SMILES.
- Searching for substructures using SMARTS patterns.
- Performing fast molecular docking preparation (e.g., adding hydrogens, calculating charges).
- Running basic force field minimizations (UFF, GAFF, MMFF94).
- Calculating molecular fingerprints and Tanimoto coefficients.
- Batch processing large chemical databases (millions of molecules).

## Reference Documentation

**Official docs**: https://openbabel.org/docs/dev/  
**Python API (Pybel)**: https://openbabel.org/docs/dev/UseTheLibrary/Python_Pybel.html  
**Search patterns**: `openbabel.OBMol`, `pybel.readfile`, `pybel.readstring`, `mol.make3D`

## Core Principles

### OB vs. Pybel

- **OpenBabel (SWIG)**: Низкоуровневый интерфейс, прямой доступ к C++ классам (OBMol, OBAtom). Сложный, но максимально мощный.
- **Pybel**: Высокоуровневая «обертка», более Pythonic-стиль. Рекомендуется для 90% задач.

### The Conversion Engine

Open Babel работает как конвейер: Input Format -> Internal OBMol -> Output Format. Вы можете добавлять фильтры и трансформации (удаление солей, добавление водородов) прямо в процессе конвертации.

## Quick Reference

### Installation

```bash
# Recommended via conda/mamba
conda install -c conda-forge openbabel
```

### Standard Imports

```python
from openbabel import openbabel as ob
from openbabel import pybel
```

### Basic Pattern - Format Conversion

```python
from openbabel import pybel

# 1. Read molecule (from string or file)
mol = pybel.readstring("smi", "CC(=O)Oc1ccccc1C(=O)O") # Aspirin

# 2. Add metadata
mol.title = "Aspirin_001"

# 3. Write to a different format
output_pdb = mol.write("pdb")
# Or write to file
# mol.write("sdf", "aspirin.sdf", overwrite=True)
```

## Critical Rules

### ✅ DO

- **Use Pybel for simplicity** - It handles memory management and provides easy access to molecular properties.
- **Add Hydrogens for 3D** - Always call `mol.OBMol.AddHydrogens()` or `mol.addh()` before generating 3D coordinates.
- **Use SMARTS for Substructures** - It is the most robust way to find functional groups.
- **Batch Processing** - Use `pybel.readfile` instead of reading molecules into a list to save memory.
- **Check for Valid Geometries** - After 3D generation, check if the energy is reasonable.
- **Close File Iterators** - Use `list(pybel.readfile(...))` or properly iterate to ensure file handles are managed.

### ❌ DON'T

- **Mix RDKit and Open Babel objects** - They are incompatible. Convert to SMILES/SDF to pass data between them.
- **Ignore Errors** - Open Babel is quiet; check if the resulting molecule is not None.
- **Forget Stereochemistry** - SMILES without `@` or `/` will lose stereocenter information during conversion.
- **Use for Complex Descriptors** - For advanced QSAR, RDKit is generally preferred; Open Babel is best for conversion and 3D work.

## Anti-Patterns (NEVER)

```python
from openbabel import pybel

# ❌ BAD: Loading millions of molecules into a list
# mols = list(pybel.readfile("sdf", "huge_database.sdf")) # Crashes RAM

# ✅ GOOD: Iterator-based processing
for mol in pybel.readfile("sdf", "huge_database.sdf"):
    # process one by one
    pass

# ❌ BAD: Generating 3D without hydrogens
mol = pybel.readstring("smi", "C1CCCCC1")
mol.make3D() # ❌ Resulting structure will be distorted/incorrect

# ✅ GOOD: Add H first
mol = pybel.readstring("smi", "C1CCCCC1")
mol.addh()
mol.make3D()
mol.optimize("mmff94")

# ❌ BAD: Manual string manipulation to change format
# pdb_str = sdf_str.replace(...) # ❌ Never works reliably
```

## Working with Molecules (pybel)

### Properties and Atoms

```python
mol = pybel.readstring("smi", "c1ccccc1O") # Phenol

print(f"Formula: {mol.formula}")
print(f"Weight: {mol.molwt:.2f}")

# Iterate over atoms
for atom in mol.atoms:
    print(f"Atom: {atom.type}, Coords: {atom.coords}")

# Get data as a dictionary
data = mol.data # Access SDF tags/metadata
```

### Substructure Searching (SMARTS)

```python
# Search for carboxylic acid group
smarts = pybel.Smarts("C(=O)[OH]")
mol = pybel.readstring("smi", "CC(=O)O") # Acetic acid

if smarts.findall(mol):
    print("Molecule contains a carboxylic acid!")
```

## 3D Structure and Force Fields

### Generation and Optimization

```python
mol = pybel.readstring("smi", "CN1C=NC2=C1C(=O)N(C(=O)N2C)C") # Caffeine

# 1. Prepare for 3D
mol.addh()

# 2. Generate initial 3D (Distance Geometry)
mol.make3D(forcefield='mmff94', steps=50)

# 3. Fine-tune with a local optimizer
# Options: uff, gaff, mmff94, ghemical
mol.optimize(forcefield='mmff94', steps=500)

print(f"3D Energy: {mol.energy:.2f} kJ/mol")
```

## Advanced: Low-Level Open Babel API

### Direct OBMol Manipulation

```python
from openbabel import openbabel as ob

# Access the internal OBMol object from a pybel molecule
obmol = mol.OBMol

# Manual atom addition
new_atom = obmol.NewAtom()
new_atom.SetAtomicNum(6) # Carbon
new_atom.SetVector(1.0, 1.0, 1.0)

# Bond information
for i in range(obmol.NumBonds()):
    bond = obmol.GetBond(i)
    print(f"Bond between {bond.GetBeginAtomIdx()} and {bond.GetEndAtomIdx()}")
```

### Calculation of Descriptors

```python
# Fingerprints
# Standard types: FP2 (path-based), FP3 (SMARTS patterns), FP4 (functional groups)
fps = mol.calcfp("FP2")
print(f"Fingerprint bits: {fps.bits}")

# Similarity
mol2 = pybel.readstring("smi", "c1ccccc1")
fps2 = mol2.calcfp("FP2")
similarity = fps | fps2 # Tanimoto coefficient
```

## Practical Workflows

### 1. High-Throughput Format Converter

```python
def batch_convert(input_file, in_fmt, output_file, out_fmt, add_h=False):
    """Converts large files with optional hydrogen addition."""
    writer = pybel.Outputfile(out_fmt, output_file, overwrite=True)
    
    for mol in pybel.readfile(in_fmt, input_file):
        if add_h:
            mol.addh()
        writer.write(mol)
    
    writer.close()

# batch_convert("library.smi", "smi", "library.sdf", "sdf", add_h=True)
```

### 2. Preparing Ligands for Docking (PDBQT)

```python
def prepare_ligand(smi_str, output_name):
    """Basic prep for AutoDock Vina."""
    mol = pybel.readstring("smi", smi_str)
    mol.addh()
    mol.make3D()
    mol.optimize("gaff")
    
    # Open Babel has a dedicated pdbqt format
    mol.write("pdbqt", f"{output_name}.pdbqt", overwrite=True)
```

### 3. Salt Removal (Chemical Cleaning)

```python
def strip_salts(mol):
    """Removes smaller fragments (salts/solvents) from a molecule."""
    if len(mol.reversesmi.split(".")) > 1:
        # Get the largest fragment by number of atoms
        fragments = mol.OBMol.Separate()
        largest = max(fragments, key=lambda x: x.NumAtoms())
        return pybel.Molecule(largest)
    return mol
```

## Performance Optimization

### Fast Search with FP2

Before doing expensive 3D or SMARTS matching on millions of molecules, use fingerprint screening (Tanimoto) to filter candidates.

### Using OBConversion for Raw Speed

If you only need to convert formats and don't need to manipulate atoms, using the raw OBConversion class is faster than creating pybel.Molecule objects.

```python
obconv = ob.OBConversion()
obconv.SetInAndOutFormats("smi", "sdf")
obconv.ConvertFile("in.smi", "out.sdf")
```

## Common Pitfalls and Solutions

### The "Empty Molecule" from SMILES

```python
# ❌ Problem: pybel.readstring("smi", "invalid_smiles") returns a blank molecule
# ✅ Solution: Always check for atom count
mol = pybel.readstring("smi", some_input)
if len(mol.atoms) == 0:
    print("Error: Invalid molecule data")
```

### Path issues for Force Fields

On some systems, Open Babel cannot find its data files (force field parameters).

```python
# ✅ Solution: Manually set BABEL_DATADIR if needed
import os
# os.environ['BABEL_DATADIR'] = '/path/to/openbabel/data'
```

### 3D Chirality Inversion

Sometimes make3D can invert a stereocenter if the input SMILES isn't specific.

```python
# ✅ Solution: Use 'gen3d' operation instead of simple make3D
# which is more robust for preserving stereochemistry.
obconv = ob.OBConversion()
obconv.AddOption("gen3d", ob.OBConversion.GENOPTIONS)
```

## Best Practices

1. **Always add hydrogens before 3D generation** - Structures without hydrogens will be incorrect.
2. **Use iterators for large files** - Don't load entire databases into memory.
3. **Validate molecules after reading** - Check atom count and basic properties.
4. **Use appropriate force fields** - MMFF94 for organic molecules, UFF for general use, GAFF for drug-like molecules.
5. **Preserve stereochemistry** - Use explicit SMILES notation with `@` and `/` when needed.
6. **Use fingerprints for similarity** - Before expensive operations, filter with Tanimoto coefficients.
7. **Close file writers explicitly** - Use context managers or `.close()` to ensure data is written.
8. **Check energy after optimization** - Unreasonable energies indicate geometry problems.

Open Babel is the "glue" of the chemical world. While it may not have the sophisticated 2D-rendering of RDKit or the high-level math of PySCF, its ability to handle any format and generate 3D starting points makes it a mandatory tool in every computational chemist's belt.
