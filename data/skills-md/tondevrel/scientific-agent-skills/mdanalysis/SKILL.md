---
name: mdanalysis
description: Comprehensive guide for MDAnalysis - the Python library for analyzing molecular dynamics trajectories. Use for trajectory loading, RMSD/RMSF calculations, distance/angle/dihedral analysis, atom selections, hydrogen bonds, solvent accessible surface area, protein structure analysis, membrane analysis, and integration with Biopython. Essential for MD simulation analysis.
version: 2.7
license: GPL-2.0
---

# MDAnalysis - Molecular Dynamics Analysis

Python library for reading, writing, and analyzing molecular dynamics trajectories and structural files.

## When to Use

- Loading MD trajectories (DCD, XTC, TRR, NetCDF, etc.)
- RMSD and RMSF calculations
- Distance, angle, and dihedral analysis
- Atom selections (VMD-like syntax)
- Hydrogen bond analysis
- Solvent Accessible Surface Area (SASA)
- Protein secondary structure analysis
- Membrane system analysis
- Water/ion distribution analysis
- Trajectory alignment and fitting
- Custom trajectory analysis
- Converting between file formats

## Reference Documentation

**Official docs**: https://www.mdanalysis.org/docs/  
**Search patterns**: `MDAnalysis.Universe`, `MDAnalysis.analysis.rms`, `MDAnalysis.analysis.distances`

## Core Principles

### Use MDAnalysis For

| Task | Module | Example |
|------|--------|---------|
| Load trajectory | `Universe` | `Universe(topology, trajectory)` |
| RMSD calculation | `analysis.rms` | `RMSD(mobile, ref)` |
| Atom selection | `select_atoms` | `u.select_atoms('protein')` |
| Distance analysis | `analysis.distances` | `distance_array(pos1, pos2)` |
| H-bond analysis | `analysis.hbonds` | `HydrogenBondAnalysis()` |
| SASA calculation | `analysis.sasa` | `SASAnalysis()` |
| Contacts analysis | `analysis.contacts` | `Contacts()` |
| Trajectory writing | `Writer` | `with Writer() as W` |

### Do NOT Use For

- Running MD simulations (use GROMACS, AMBER, NAMD)
- Force field calculations (use OpenMM, MDTraj)
- Quantum chemistry (use PySCF, Qiskit)
- Protein structure prediction (use AlphaFold, RosettaFold)
- Initial structure building (use Biopython, PyMOL)

## Quick Reference

### Installation

```bash
# pip
pip install MDAnalysis

# With additional analysis modules
pip install MDAnalysis[analysis]

# conda
conda install -c conda-forge mdanalysis

# Development version
pip install git+https://github.com/MDAnalysis/mdanalysis.git
```

### Standard Imports

```python
# Core imports
import MDAnalysis as mda
from MDAnalysis import Universe
from MDAnalysis.analysis import rms, align, distances

# Common analysis modules
from MDAnalysis.analysis.rms import RMSD, RMSF
from MDAnalysis.analysis.distances import distance_array
from MDAnalysis.analysis.hydrogenbonds.hbond_analysis import HydrogenBondAnalysis
from MDAnalysis.analysis.dihedrals import Dihedral

# Utilities
import numpy as np
import matplotlib.pyplot as plt
```

### Basic Pattern - Load and Analyze

```python
import MDAnalysis as mda
from MDAnalysis.analysis.rms import RMSD

# Load trajectory
u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Select atoms
protein = u.select_atoms('protein')
ca_atoms = u.select_atoms('protein and name CA')

# Calculate RMSD
rmsd_analysis = RMSD(protein, protein, select='backbone')
rmsd_analysis.run()

# Access results
rmsd = rmsd_analysis.results.rmsd
print(f"RMSD over time: {rmsd[:, 2]}")  # Column 2 is RMSD
```

### Basic Pattern - Atom Selection

```python
import MDAnalysis as mda

u = mda.Universe('structure.pdb')

# Various selections (VMD-like syntax)
protein = u.select_atoms('protein')
backbone = u.select_atoms('backbone')
ca = u.select_atoms('name CA')
resid_10 = u.select_atoms('resid 10')
within_5A = u.select_atoms('around 5 resid 10')
water = u.select_atoms('resname WAT or resname HOH')

print(f"Number of protein atoms: {len(protein)}")
print(f"Number of CA atoms: {len(ca)}")
```

## Critical Rules

### ✅ DO

- **Close trajectory files** - Use context managers or close explicitly
- **Use atom selections efficiently** - Cache selections for reuse
- **Check trajectory length** - Verify n_frames before analysis
- **Use vectorized operations** - Leverage NumPy for speed
- **Align trajectories** - Align before RMSD calculations
- **Handle periodic boundaries** - Use PBC-aware distance calculations
- **Validate atom groups** - Check empty selections
- **Use appropriate frames** - Slice trajectories if needed
- **Save intermediate results** - Don't recompute expensive calculations
- **Check units** - MDAnalysis uses Angstroms and picoseconds

### ❌ DON'T

- **Load entire trajectory in memory** - Stream through frames
- **Ignore PBC** - Always consider periodic boundary conditions
- **Forget to align** - RMSD without alignment is meaningless
- **Use wrong atom names** - Check topology for correct names
- **Mix coordinate systems** - Be consistent with units
- **Ignore missing atoms** - Handle incomplete residues
- **Recompute unnecessarily** - Cache expensive calculations
- **Use string selections in loops** - Parse once, reuse
- **Forget to unwrap coordinates** - Handle molecules split by PBC
- **Ignore memory limits** - Process large trajectories in chunks

## Anti-Patterns (NEVER)

```python
import MDAnalysis as mda
import numpy as np

# ❌ BAD: Loading entire trajectory in memory
u = mda.Universe('top.pdb', 'traj.dcd')
all_coords = []
for ts in u.trajectory:
    all_coords.append(u.atoms.positions.copy())
all_coords = np.array(all_coords)  # Huge memory usage!

# ✅ GOOD: Process frame by frame
u = mda.Universe('top.pdb', 'traj.dcd')
for ts in u.trajectory:
    # Process current frame
    coords = u.atoms.positions
    # Do analysis...
    # Move to next frame automatically

# ❌ BAD: RMSD without alignment
rmsd_values = []
for ts in u.trajectory:
    rmsd = rms.rmsd(mobile.positions, reference.positions)
    rmsd_values.append(rmsd)  # Wrong! Not aligned!

# ✅ GOOD: Align before RMSD
from MDAnalysis.analysis.rms import RMSD
R = RMSD(mobile, reference, select='backbone')
R.run()
rmsd_values = R.results.rmsd[:, 2]

# ❌ BAD: Creating selection in loop
for ts in u.trajectory:
    ca = u.select_atoms('name CA')  # Parsed every frame!
    # Do something with ca

# ✅ GOOD: Create selection once
ca = u.select_atoms('name CA')
for ts in u.trajectory:
    # Use ca (automatically updated each frame)
    positions = ca.positions

# ❌ BAD: Ignoring periodic boundaries
distance = np.linalg.norm(atom1.position - atom2.position)

# ✅ GOOD: PBC-aware distance
from MDAnalysis.lib.distances import distance_array
dist = distance_array(
    atom1.position[np.newaxis, :],
    atom2.position[np.newaxis, :],
    box=u.dimensions
)[0, 0]

# ❌ BAD: Not checking for empty selections
selection = u.select_atoms('resname XYZ')
# Continue without checking if selection is empty!
avg_pos = selection.center_of_mass()  # May crash!

# ✅ GOOD: Validate selections
selection = u.select_atoms('resname XYZ')
if len(selection) == 0:
    print("Warning: No atoms found matching selection")
else:
    avg_pos = selection.center_of_mass()
```

## Loading Trajectories (Universe)

### Basic Universe Creation

```python
import MDAnalysis as mda

# Single structure file
u = mda.Universe('protein.pdb')

# Topology + trajectory
u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Multiple trajectories (concatenated)
u = mda.Universe('top.pdb', 'traj1.dcd', 'traj2.dcd', 'traj3.dcd')

# Different formats
u = mda.Universe('system.gro', 'traj.xtc')  # GROMACS
u = mda.Universe('system.psf', 'traj.dcd')  # CHARMM/NAMD
u = mda.Universe('system.prmtop', 'traj.nc')  # AMBER

# From memory (numpy arrays)
coords = np.random.rand(100, 3)  # 100 atoms, xyz
u = mda.Universe.empty(100, trajectory=True)
u.atoms.positions = coords

print(f"Number of atoms: {len(u.atoms)}")
print(f"Number of frames: {len(u.trajectory)}")
print(f"Total time: {u.trajectory.totaltime} ps")
```

### Trajectory Information

```python
import MDAnalysis as mda

u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Trajectory properties
traj = u.trajectory
print(f"Number of frames: {traj.n_frames}")
print(f"Time step: {traj.dt} ps")
print(f"Total time: {traj.totaltime} ps")

# Current frame info
print(f"Current frame: {traj.frame}")
print(f"Current time: {traj.time} ps")
print(f"Box dimensions: {u.dimensions}")  # [a, b, c, alpha, beta, gamma]

# Iterate through frames
for i, ts in enumerate(u.trajectory):
    if i >= 5:
        break
    print(f"Frame {ts.frame}: time = {ts.time:.2f} ps")

# Jump to specific frame
u.trajectory[100]  # Go to frame 100
print(f"Now at frame: {u.trajectory.frame}")

# Slice trajectory
for ts in u.trajectory[::10]:  # Every 10th frame
    print(f"Frame {ts.frame}")
```

### Working with Multiple Trajectories

```python
import MDAnalysis as mda

# Load multiple trajectory files
u = mda.Universe('top.pdb', 'part1.dcd', 'part2.dcd', 'part3.dcd')

print(f"Total frames from all trajectories: {len(u.trajectory)}")

# Or use ChainReader explicitly
from MDAnalysis.coordinates.chain import ChainReader

trajectories = ['part1.dcd', 'part2.dcd', 'part3.dcd']
u = mda.Universe('top.pdb', trajectories, continuous=True)

# Access frame indices
for i, ts in enumerate(u.trajectory[::100]):
    print(f"Global frame {i}: actual frame {ts.frame}, time {ts.time:.2f}")
```

## Atom Selections

### Basic Selection Syntax

```python
import MDAnalysis as mda

u = mda.Universe('system.pdb')

# Protein selections
protein = u.select_atoms('protein')
backbone = u.select_atoms('backbone')  # N, CA, C
mainchain = u.select_atoms('backbone or name O')

# Specific residues
resid_10 = u.select_atoms('resid 10')
resid_range = u.select_atoms('resid 10:20')
resid_list = u.select_atoms('resid 10 15 20 25')

# Residue names
water = u.select_atoms('resname WAT or resname HOH')
ions = u.select_atoms('resname NA or resname CL')

# Atom names
ca_atoms = u.select_atoms('name CA')
hydrogens = u.select_atoms('name H*')  # Wildcards

# By element
carbons = u.select_atoms('element C')

# Segments
seg_a = u.select_atoms('segid A')

print(f"Protein atoms: {len(protein)}")
print(f"Water molecules: {len(water)}")
print(f"CA atoms: {len(ca_atoms)}")
```

### Advanced Selections

```python
import MDAnalysis as mda

u = mda.Universe('protein_solvent.pdb')

# Geometric selections
around_10 = u.select_atoms('around 5.0 protein')  # Within 5Å of protein
within_box = u.select_atoms('prop x < 50 and prop y < 50')

# Spatial queries
resid_10 = u.select_atoms('resid 10')
near_res10 = u.select_atoms('around 10.0 resid 10 and not resid 10')

# Combining selections
hydrophobic = u.select_atoms(
    'resname ALA or resname VAL or resname LEU or '
    'resname ILE or resname PHE or resname TRP or resname MET'
)

charged = u.select_atoms(
    'resname ARG or resname LYS or resname ASP or resname GLU'
)

# Boolean operations
not_protein = u.select_atoms('not protein')
protein_no_h = u.select_atoms('protein and not name H*')

# By property
high_bfactor = u.select_atoms('protein and prop beta > 50')

# SMARTS matching (requires RDKit)
# aromatic = u.select_atoms('smarts c1ccccc1')

print(f"Hydrophobic residues: {len(hydrophobic)}")
print(f"Charged residues: {len(charged)}")
```

### Dynamic Selections

```python
import MDAnalysis as mda

u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Regular selection (static)
protein = u.select_atoms('protein')

# Dynamic selection (updated each frame)
# Example: Select water within 3.5Å of protein
water_near_protein = u.select_atoms(
    'resname WAT and around 3.5 protein',
    updating=True
)

# Track number of nearby water molecules over time
water_counts = []
for ts in u.trajectory:
    # water_near_protein automatically updates
    water_counts.append(len(water_near_protein))

print(f"Water molecules near protein per frame:")
print(f"  Min: {min(water_counts)}")
print(f"  Max: {max(water_counts)}")
print(f"  Mean: {sum(water_counts)/len(water_counts):.1f}")

# Another example: ions near active site
active_site = u.select_atoms('resid 100:110')
nearby_ions = u.select_atoms(
    '(resname NA or resname CL) and around 8.0 resid 100:110',
    updating=True
)

for i, ts in enumerate(u.trajectory[::10]):
    print(f"Frame {ts.frame}: {len(nearby_ions)} ions near active site")
```

### Selection Groups and Operations

```python
import MDAnalysis as mda

u = mda.Universe('protein.pdb')

# Create multiple selections
protein = u.select_atoms('protein')
backbone = u.select_atoms('backbone')
ca_atoms = u.select_atoms('name CA')

# Combine selections
combined = protein | backbone  # Union (OR)
intersection = protein & backbone  # Intersection (AND)
difference = protein - backbone  # Difference (NOT)

# Access properties
print(f"Combined: {len(combined)} atoms")
print(f"Center of mass: {protein.center_of_mass()}")
print(f"Center of geometry: {protein.center_of_geometry()}")
print(f"Total mass: {protein.total_mass()}")
print(f"Total charge: {protein.total_charge()}")

# Iterate through atoms
for atom in ca_atoms[:5]:
    print(f"Atom {atom.name} {atom.resname}{atom.resid}: {atom.position}")

# Iterate through residues
for residue in protein.residues[:5]:
    print(f"Residue {residue.resname}{residue.resid}: {residue.atoms.n_atoms} atoms")

# Iterate through segments
for segment in u.segments:
    print(f"Segment {segment.segid}: {len(segment.atoms)} atoms")
```

## RMSD and RMSF Analysis

### RMSD Calculation

```python
import MDAnalysis as mda
from MDAnalysis.analysis import rms
import numpy as np
import matplotlib.pyplot as plt

# Load trajectory
u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Define reference (first frame)
reference = u.copy()
reference.trajectory[0]

# Select atoms for RMSD (typically backbone or CA)
mobile = u.select_atoms('backbone')
ref = reference.select_atoms('backbone')

# Calculate RMSD with alignment
R = rms.RMSD(mobile, ref, select='backbone', ref_frame=0)
R.run()

# Extract results
rmsd_data = R.results.rmsd
time = rmsd_data[:, 1]  # Time in ps
rmsd_values = rmsd_data[:, 2]  # RMSD in Angstroms

# Plot
plt.figure(figsize=(10, 6))
plt.plot(time, rmsd_values)
plt.xlabel('Time (ps)')
plt.ylabel('RMSD (Å)')
plt.title('Backbone RMSD over time')
plt.grid(True)
plt.savefig('rmsd.png', dpi=300)

print(f"Mean RMSD: {np.mean(rmsd_values):.2f} Å")
print(f"Max RMSD: {np.max(rmsd_values):.2f} Å")
print(f"Final RMSD: {rmsd_values[-1]:.2f} Å")
```

### RMSD to Multiple References

```python
import MDAnalysis as mda
from MDAnalysis.analysis import rms
import numpy as np

u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Compare to multiple reference structures
references = {
    'crystal': mda.Universe('crystal.pdb'),
    'equilibrated': mda.Universe('equilibrated.pdb'),
    'apo': mda.Universe('apo_structure.pdb')
}

results = {}

for ref_name, ref_universe in references.items():
    mobile = u.select_atoms('backbone')
    ref = ref_universe.select_atoms('backbone')
    
    R = rms.RMSD(mobile, ref, select='backbone')
    R.run()
    
    results[ref_name] = R.results.rmsd[:, 2]

# Plot comparison
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
for ref_name, rmsd_values in results.items():
    time = np.arange(len(rmsd_values)) * u.trajectory.dt
    plt.plot(time, rmsd_values, label=ref_name)

plt.xlabel('Time (ps)')
plt.ylabel('RMSD (Å)')
plt.legend()
plt.title('RMSD to different reference structures')
plt.grid(True)
plt.savefig('rmsd_comparison.png', dpi=300)

# Statistics
for ref_name, rmsd_values in results.items():
    print(f"{ref_name}: mean={np.mean(rmsd_values):.2f} Å, "
          f"std={np.std(rmsd_values):.2f} Å")
```

### RMSF Calculation (Fluctuations)

```python
import MDAnalysis as mda
from MDAnalysis.analysis import rms
import numpy as np
import matplotlib.pyplot as plt

u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Select CA atoms (typical for RMSF)
ca_atoms = u.select_atoms('protein and name CA')

# Calculate RMSF
rmsf_analysis = rms.RMSF(ca_atoms, verbose=True)
rmsf_analysis.run()

# Extract results
rmsf_values = rmsf_analysis.results.rmsf

# Plot RMSF vs residue number
residue_numbers = [atom.resid for atom in ca_atoms]

plt.figure(figsize=(12, 6))
plt.plot(residue_numbers, rmsf_values, linewidth=2)
plt.xlabel('Residue Number')
plt.ylabel('RMSF (Å)')
plt.title('Per-residue Fluctuations (RMSF)')
plt.grid(True)
plt.savefig('rmsf.png', dpi=300)

# Identify flexible regions (high RMSF)
threshold = np.mean(rmsf_values) + np.std(rmsf_values)
flexible_residues = [resid for resid, rmsf in zip(residue_numbers, rmsf_values) 
                     if rmsf > threshold]

print(f"Mean RMSF: {np.mean(rmsf_values):.2f} Å")
print(f"Flexible regions (RMSF > {threshold:.2f}): {flexible_residues}")

# RMSF per atom (all heavy atoms)
heavy_atoms = u.select_atoms('protein and not name H*')
rmsf_all = rms.RMSF(heavy_atoms)
rmsf_all.run()

print(f"\nMean RMSF (all heavy atoms): {np.mean(rmsf_all.results.rmsf):.2f} Å")
```

### 2D RMSD Matrix

```python
import MDAnalysis as mda
from MDAnalysis.analysis import rms
import numpy as np
import matplotlib.pyplot as plt

u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Select atoms
selection = u.select_atoms('backbone')

# Compute pairwise RMSD matrix
n_frames = len(u.trajectory)
rmsd_matrix = np.zeros((n_frames, n_frames))

# Store coordinates for all frames
coords = []
for ts in u.trajectory:
    coords.append(selection.positions.copy())

# Calculate pairwise RMSD
for i in range(n_frames):
    for j in range(i, n_frames):
        # Align j to i
        rmsd_value = rms.rmsd(coords[j], coords[i], center=True, superposition=True)
        rmsd_matrix[i, j] = rmsd_value
        rmsd_matrix[j, i] = rmsd_value

# Plot matrix
plt.figure(figsize=(10, 8))
plt.imshow(rmsd_matrix, cmap='viridis', origin='lower')
plt.colorbar(label='RMSD (Å)')
plt.xlabel('Frame')
plt.ylabel('Frame')
plt.title('Pairwise RMSD Matrix')
plt.savefig('rmsd_matrix.png', dpi=300)

# Identify clusters (frames with low mutual RMSD)
threshold = 2.0  # Angstroms
similar_frames = np.where(rmsd_matrix < threshold)
print(f"Frame pairs with RMSD < {threshold} Å: {len(similar_frames[0])}")
```

## Distance Analysis

### Simple Distance Calculations

```python
import MDAnalysis as mda
from MDAnalysis.analysis import distances
import numpy as np
import matplotlib.pyplot as plt

u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Select two groups of atoms
group1 = u.select_atoms('resid 10 and name CA')
group2 = u.select_atoms('resid 50 and name CA')

# Calculate distance over trajectory
dist_array = []
for ts in u.trajectory:
    # PBC-aware distance
    d = distances.distance_array(
        group1.positions, 
        group2.positions,
        box=u.dimensions
    )[0, 0]
    dist_array.append(d)

dist_array = np.array(dist_array)
time = np.arange(len(dist_array)) * u.trajectory.dt

# Plot
plt.figure(figsize=(10, 6))
plt.plot(time, dist_array)
plt.xlabel('Time (ps)')
plt.ylabel('Distance (Å)')
plt.title('Distance between residues 10 and 50')
plt.grid(True)
plt.savefig('distance.png', dpi=300)

print(f"Mean distance: {np.mean(dist_array):.2f} Å")
print(f"Min distance: {np.min(dist_array):.2f} Å")
print(f"Max distance: {np.max(dist_array):.2f} Å")
```

### Distance Matrix

```python
import MDAnalysis as mda
from MDAnalysis.analysis import distances
import numpy as np
import matplotlib.pyplot as plt

u = mda.Universe('protein.pdb')

# Select CA atoms
ca_atoms = u.select_atoms('protein and name CA')

# Calculate distance matrix
dist_matrix = distances.distance_array(
    ca_atoms.positions,
    ca_atoms.positions,
    box=u.dimensions
)

# Plot
plt.figure(figsize=(10, 8))
plt.imshow(dist_matrix, cmap='viridis', origin='lower')
plt.colorbar(label='Distance (Å)')
plt.xlabel('CA atom index')
plt.ylabel('CA atom index')
plt.title('CA Distance Matrix')
plt.savefig('distance_matrix.png', dpi=300)

# Find contacts (CA atoms within 8Å)
contact_threshold = 8.0
contacts = np.where((dist_matrix < contact_threshold) & (dist_matrix > 0))
n_contacts = len(contacts[0]) // 2  # Divide by 2 (symmetric matrix)

print(f"Number of CA-CA contacts within {contact_threshold} Å: {n_contacts}")
```

### Contact Analysis Over Time

```python
import MDAnalysis as mda
from MDAnalysis.analysis.contacts import Contacts
import numpy as np
import matplotlib.pyplot as plt

u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Define two groups
group1 = u.select_atoms('resid 1-50 and name CA')
group2 = u.select_atoms('resid 51-100 and name CA')

# Calculate contacts over trajectory
ca = Contacts(
    u,
    selection=(group1, group2),
    refgroup=(group1, group2),
    radius=8.0,  # Contact cutoff in Angstroms
    method='hard_cut'  # or 'soft_cut' for smooth cutoff
)

ca.run()

# Extract results
time = ca.results.timeseries[:, 0]
n_contacts = ca.results.timeseries[:, 1]

# Plot
plt.figure(figsize=(10, 6))
plt.plot(time, n_contacts)
plt.xlabel('Time (ps)')
plt.ylabel('Number of Contacts')
plt.title('Inter-domain Contacts')
plt.grid(True)
plt.savefig('contacts.png', dpi=300)

print(f"Mean contacts: {np.mean(n_contacts):.1f}")
print(f"Contact stability: {np.std(n_contacts):.1f} (lower = more stable)")
```

### Radius of Gyration

```python
import MDAnalysis as mda
import numpy as np
import matplotlib.pyplot as plt

u = mda.Universe('topology.pdb', 'trajectory.dcd')

protein = u.select_atoms('protein')

# Calculate radius of gyration over time
rg_values = []
for ts in u.trajectory:
    rg = protein.radius_of_gyration()
    rg_values.append(rg)

rg_values = np.array(rg_values)
time = np.arange(len(rg_values)) * u.trajectory.dt

# Plot
plt.figure(figsize=(10, 6))
plt.plot(time, rg_values)
plt.xlabel('Time (ps)')
plt.ylabel('Radius of Gyration (Å)')
plt.title('Protein Compactness')
plt.grid(True)
plt.savefig('radius_of_gyration.png', dpi=300)

print(f"Mean Rg: {np.mean(rg_values):.2f} Å")
print(f"Rg fluctuation: {np.std(rg_values):.2f} Å")

# Check if protein is folding/unfolding
if np.std(rg_values) > 2.0:
    print("Warning: Large Rg fluctuations indicate conformational changes")
```

## Hydrogen Bond Analysis

### Basic H-Bond Analysis

```python
import MDAnalysis as mda
from MDAnalysis.analysis.hydrogenbonds.hbond_analysis import HydrogenBondAnalysis
import numpy as np
import matplotlib.pyplot as plt

u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Setup hydrogen bond analysis
hbonds = HydrogenBondAnalysis(
    universe=u,
    donors_sel='protein',
    hydrogens_sel='protein',
    acceptors_sel='protein',
    d_h_cutoff=1.2,      # Donor-H distance cutoff (Å)
    d_a_cutoff=3.0,      # Donor-Acceptor distance cutoff (Å)
    d_h_a_angle_cutoff=150  # Angle cutoff (degrees)
)

# Run analysis
hbonds.run(verbose=True)

# Access results
hbond_results = hbonds.results.hbonds

print(f"Total hydrogen bonds detected: {len(hbond_results)}")

# Count H-bonds per frame
frames = hbond_results[:, 0].astype(int)
unique_frames, counts = np.unique(frames, return_counts=True)

# Plot
time = unique_frames * u.trajectory.dt
plt.figure(figsize=(10, 6))
plt.plot(time, counts)
plt.xlabel('Time (ps)')
plt.ylabel('Number of H-bonds')
plt.title('Intramolecular Hydrogen Bonds')
plt.grid(True)
plt.savefig('hbonds_time.png', dpi=300)

print(f"Mean H-bonds per frame: {np.mean(counts):.1f}")
print(f"Std H-bonds per frame: {np.std(counts):.1f}")
```

### Persistent H-Bond Analysis

```python
import MDAnalysis as mda
from MDAnalysis.analysis.hydrogenbonds.hbond_analysis import HydrogenBondAnalysis
import numpy as np
from collections import Counter

u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Run H-bond analysis
hbonds = HydrogenBondAnalysis(
    universe=u,
    donors_sel='protein',
    hydrogens_sel='protein',
    acceptors_sel='protein'
)
hbonds.run()

# Extract results
hbond_data = hbonds.results.hbonds

# Count H-bond occurrences
# Each row: [frame, donor_idx, hydrogen_idx, acceptor_idx, distance, angle]
hbond_pairs = []
for row in hbond_data:
    donor_idx = int(row[1])
    acceptor_idx = int(row[3])
    hbond_pairs.append((donor_idx, acceptor_idx))

# Count frequency
hbond_counts = Counter(hbond_pairs)
total_frames = len(u.trajectory)

# Find persistent H-bonds (present in >50% of frames)
threshold = 0.5 * total_frames
persistent_hbonds = {pair: count for pair, count in hbond_counts.items() 
                     if count > threshold}

print(f"Persistent H-bonds (>{threshold/total_frames:.0%} occupancy):")
for (donor_idx, acceptor_idx), count in sorted(persistent_hbonds.items(), 
                                                 key=lambda x: x[1], 
                                                 reverse=True):
    donor_atom = u.atoms[donor_idx]
    acceptor_atom = u.atoms[acceptor_idx]
    occupancy = count / total_frames
    
    print(f"  {donor_atom.resname}{donor_atom.resid}:{donor_atom.name} -> "
          f"{acceptor_atom.resname}{acceptor_atom.resid}:{acceptor_atom.name} "
          f"({occupancy:.1%} occupancy)")
```

### Protein-Ligand H-Bonds

```python
import MDAnalysis as mda
from MDAnalysis.analysis.hydrogenbonds.hbond_analysis import HydrogenBondAnalysis

u = mda.Universe('complex.pdb', 'trajectory.dcd')

# Separate H-bond analyses
# 1. Ligand as donor, protein as acceptor
hbonds_lig_don = HydrogenBondAnalysis(
    universe=u,
    donors_sel='resname LIG',
    hydrogens_sel='resname LIG',
    acceptors_sel='protein'
)
hbonds_lig_don.run()

# 2. Protein as donor, ligand as acceptor
hbonds_prot_don = HydrogenBondAnalysis(
    universe=u,
    donors_sel='protein',
    hydrogens_sel='protein',
    acceptors_sel='resname LIG'
)
hbonds_prot_don.run()

# Combine results
total_hbonds_per_frame = []
for frame in range(len(u.trajectory)):
    n_lig_don = len(hbonds_lig_don.results.hbonds[
        hbonds_lig_don.results.hbonds[:, 0] == frame
    ])
    n_prot_don = len(hbonds_prot_don.results.hbonds[
        hbonds_prot_don.results.hbonds[:, 0] == frame
    ])
    total_hbonds_per_frame.append(n_lig_don + n_prot_don)

import matplotlib.pyplot as plt
import numpy as np

time = np.arange(len(total_hbonds_per_frame)) * u.trajectory.dt
plt.figure(figsize=(10, 6))
plt.plot(time, total_hbonds_per_frame)
plt.xlabel('Time (ps)')
plt.ylabel('Number of Protein-Ligand H-bonds')
plt.title('Protein-Ligand Hydrogen Bonding')
plt.grid(True)
plt.savefig('protein_ligand_hbonds.png', dpi=300)

print(f"Mean protein-ligand H-bonds: {np.mean(total_hbonds_per_frame):.1f}")
```

## Dihedral Angle Analysis

### Backbone Dihedrals (Ramachandran)

```python
import MDAnalysis as mda
from MDAnalysis.analysis.dihedrals import Ramachandran
import numpy as np
import matplotlib.pyplot as plt

u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Select residues (exclude first and last)
residues = u.select_atoms('protein').residues[1:-1]

# Calculate Ramachandran angles
rama = Ramachandran(residues)
rama.run()

# Extract phi and psi angles
angles = rama.results.angles

# Plot Ramachandran plot
phi = angles[:, :, 0].flatten()
psi = angles[:, :, 1].flatten()

plt.figure(figsize=(8, 8))
plt.hexbin(phi, psi, gridsize=50, cmap='Blues', mincnt=1)
plt.colorbar(label='Counts')
plt.xlabel('Phi (degrees)')
plt.ylabel('Psi (degrees)')
plt.title('Ramachandran Plot')
plt.xlim(-180, 180)
plt.ylim(-180, 180)
plt.axhline(0, color='gray', linestyle='--', alpha=0.3)
plt.axvline(0, color='gray', linestyle='--', alpha=0.3)
plt.savefig('ramachandran.png', dpi=300)

# Check for outliers (non-favored regions)
# Alpha-helix region: phi ~ -60, psi ~ -45
# Beta-sheet region: phi ~ -120, psi ~ 120
alpha_region = (np.abs(phi + 60) < 30) & (np.abs(psi + 45) < 30)
beta_region = (np.abs(phi + 120) < 30) & (np.abs(psi - 120) < 30)
favored = alpha_region | beta_region

print(f"Percentage in favored regions: {np.sum(favored)/len(phi)*100:.1f}%")
```

### Custom Dihedral Analysis

```python
import MDAnalysis as mda
from MDAnalysis.analysis.dihedrals import Dihedral
import numpy as np
import matplotlib.pyplot as plt

u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Define atoms for dihedral (4 consecutive atoms)
# Example: Chi1 angle of a specific residue
residue = u.select_atoms('resid 42')
atoms = [
    residue.select_atoms('name N')[0],
    residue.select_atoms('name CA')[0],
    residue.select_atoms('name CB')[0],
    residue.select_atoms('name CG')[0]
]

# Calculate dihedral over trajectory
dihedral_angles = []
for ts in u.trajectory:
    # Get positions
    positions = np.array([atom.position for atom in atoms])
    
    # Calculate dihedral
    from MDAnalysis.lib.distances import calc_dihedrals
    angle = calc_dihedrals(
        positions[0], positions[1], positions[2], positions[3],
        box=u.dimensions
    )
    dihedral_angles.append(np.degrees(angle))

dihedral_angles = np.array(dihedral_angles)
time = np.arange(len(dihedral_angles)) * u.trajectory.dt

# Plot
plt.figure(figsize=(10, 6))
plt.plot(time, dihedral_angles)
plt.xlabel('Time (ps)')
plt.ylabel('Dihedral Angle (degrees)')
plt.title('Chi1 Angle of Residue 42')
plt.ylim(-180, 180)
plt.grid(True)
plt.savefig('chi1_angle.png', dpi=300)

# Histogram
plt.figure(figsize=(8, 6))
plt.hist(dihedral_angles, bins=36, range=(-180, 180), edgecolor='black')
plt.xlabel('Dihedral Angle (degrees)')
plt.ylabel('Frequency')
plt.title('Chi1 Angle Distribution')
plt.savefig('chi1_histogram.png', dpi=300)

print(f"Mean dihedral angle: {np.mean(dihedral_angles):.1f}°")
print(f"Std dihedral angle: {np.std(dihedral_angles):.1f}°")
```

## Solvent Accessible Surface Area (SASA)

### Basic SASA Calculation

```python
import MDAnalysis as mda
from MDAnalysis.analysis.sasa import SASAnalysis
import numpy as np
import matplotlib.pyplot as plt

u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Calculate SASA for protein
sasa = SASAnalysis(u.select_atoms('protein'))
sasa.run(verbose=True)

# Extract results
sasa_values = sasa.results.sasa
time = np.arange(len(sasa_values)) * u.trajectory.dt

# Plot
plt.figure(figsize=(10, 6))
plt.plot(time, sasa_values)
plt.xlabel('Time (ps)')
plt.ylabel('SASA (Å²)')
plt.title('Protein Solvent Accessible Surface Area')
plt.grid(True)
plt.savefig('sasa.png', dpi=300)

print(f"Mean SASA: {np.mean(sasa_values):.1f} Å²")
print(f"SASA range: {np.min(sasa_values):.1f} - {np.max(sasa_values):.1f} Å²")
```

### Per-Residue SASA

```python
import MDAnalysis as mda
from MDAnalysis.analysis.sasa import SASAnalysis
import numpy as np
import matplotlib.pyplot as plt

u = mda.Universe('protein.pdb')

protein = u.select_atoms('protein')

# Calculate SASA for each residue
residue_sasa = []
residue_ids = []

for residue in protein.residues:
    sasa = SASAnalysis(residue.atoms)
    sasa.run()
    residue_sasa.append(sasa.results.sasa[0])
    residue_ids.append(residue.resid)

residue_sasa = np.array(residue_sasa)

# Plot
plt.figure(figsize=(12, 6))
plt.bar(residue_ids, residue_sasa)
plt.xlabel('Residue Number')
plt.ylabel('SASA (Å²)')
plt.title('Per-Residue Solvent Accessible Surface Area')
plt.savefig('per_residue_sasa.png', dpi=300)

# Identify buried vs exposed residues
threshold = 40.0  # Å²
buried = [resid for resid, sasa in zip(residue_ids, residue_sasa) if sasa < threshold]
exposed = [resid for resid, sasa in zip(residue_ids, residue_sasa) if sasa >= threshold]

print(f"Buried residues (SASA < {threshold} Å²): {len(buried)}")
print(f"Exposed residues (SASA >= {threshold} Å²): {len(exposed)}")
print(f"Mean residue SASA: {np.mean(residue_sasa):.1f} Å²")
```

## Trajectory Alignment and Transformation

### Align Trajectory to Reference

```python
import MDAnalysis as mda
from MDAnalysis.analysis import align
from MDAnalysis.analysis.rms import rmsd

# Load trajectory
mobile = mda.Universe('topology.pdb', 'trajectory.dcd')
reference = mda.Universe('reference.pdb')

# Align entire trajectory to reference
alignment = align.AlignTraj(
    mobile,
    reference,
    select='backbone',
    filename='aligned_trajectory.dcd',
    weights='mass'
)
alignment.run()

print(f"Trajectory aligned and saved to aligned_trajectory.dcd")

# Verify alignment - RMSD should be lower
mobile_original = mda.Universe('topology.pdb', 'trajectory.dcd')
mobile_aligned = mda.Universe('topology.pdb', 'aligned_trajectory.dcd')

ref_backbone = reference.select_atoms('backbone')

# Calculate RMSD before and after alignment
rmsd_before = []
rmsd_after = []

for ts_orig, ts_align in zip(mobile_original.trajectory, mobile_aligned.trajectory):
    orig_backbone = mobile_original.select_atoms('backbone')
    align_backbone = mobile_aligned.select_atoms('backbone')
    
    rmsd_before.append(rmsd(orig_backbone.positions, ref_backbone.positions, 
                            center=True, superposition=True))
    rmsd_after.append(rmsd(align_backbone.positions, ref_backbone.positions,
                           center=False, superposition=False))

import numpy as np
print(f"Mean RMSD before alignment: {np.mean(rmsd_before):.2f} Å")
print(f"Mean RMSD after alignment: {np.mean(rmsd_after):.2f} Å")
```

### PBC Unwrapping

```python
import MDAnalysis as mda
from MDAnalysis.transformations import unwrap

u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Molecules can be split across periodic boundaries
# Unwrap to make them whole

protein = u.select_atoms('protein')

# Add unwrap transformation
workflow = [unwrap(protein)]
u.trajectory.add_transformations(*workflow)

# Now iterate - protein will be automatically unwrapped
for ts in u.trajectory[:5]:
    com = protein.center_of_mass()
    print(f"Frame {ts.frame}: Protein COM = {com}")

# Save unwrapped trajectory
with mda.Writer('unwrapped.dcd', protein.n_atoms) as W:
    for ts in u.trajectory:
        W.write(protein)

print("Unwrapped trajectory saved")
```

### On-the-Fly Transformations

```python
import MDAnalysis as mda
from MDAnalysis.transformations import (
    center_in_box,
    wrap,
    unwrap,
    fit_rot_trans
)

u = mda.Universe('topology.pdb', 'trajectory.dcd')
reference = mda.Universe('reference.pdb')

protein = u.select_atoms('protein')
ref_protein = reference.select_atoms('protein')

# Chain multiple transformations
workflow = [
    unwrap(protein),                    # 1. Unwrap protein
    center_in_box(protein),            # 2. Center protein in box
    fit_rot_trans(protein, ref_protein) # 3. Align to reference
]

u.trajectory.add_transformations(*workflow)

# All transformations applied automatically when iterating
for ts in u.trajectory[:10]:
    # Protein is now unwrapped, centered, and aligned
    rmsd_value = mda.analysis.rms.rmsd(protein.positions, ref_protein.positions)
    print(f"Frame {ts.frame}: RMSD = {rmsd_value:.2f} Å")
```

## Advanced Analysis

### Principal Component Analysis (PCA)

```python
import MDAnalysis as mda
from MDAnalysis.analysis import pca
import numpy as np
import matplotlib.pyplot as plt

u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Select atoms for PCA (usually CA atoms)
ca_atoms = u.select_atoms('protein and name CA')

# Perform PCA
pc = pca.PCA(u, select='protein and name CA', align=True)
pc.run()

# Extract results
n_pcs = min(10, pc.results.n_components)
variance = pc.results.variance[:n_pcs]
cumulative_variance = pc.results.cumulative_variance[:n_pcs]

# Plot variance explained
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.bar(range(1, n_pcs + 1), variance)
ax1.set_xlabel('Principal Component')
ax1.set_ylabel('Variance')
ax1.set_title('Variance per PC')

ax2.plot(range(1, n_pcs + 1), cumulative_variance, marker='o')
ax2.set_xlabel('Number of PCs')
ax2.set_ylabel('Cumulative Variance')
ax2.set_title('Cumulative Variance Explained')
ax2.grid(True)

plt.tight_layout()
plt.savefig('pca_variance.png', dpi=300)

print(f"Variance explained by first 3 PCs: {cumulative_variance[2]:.1%}")

# Project trajectory onto PC1 and PC2
projection = pc.transform(ca_atoms, n_components=2)

plt.figure(figsize=(8, 8))
plt.scatter(projection[:, 0], projection[:, 1], c=range(len(projection)), 
            cmap='viridis', alpha=0.6)
plt.colorbar(label='Frame')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('Trajectory in PC1-PC2 Space')
plt.savefig('pca_projection.png', dpi=300)

# Identify frames representing different conformational states
# Cluster in PC space or select extremes
pc1_min_frame = np.argmin(projection[:, 0])
pc1_max_frame = np.argmax(projection[:, 0])

print(f"PC1 minimum conformation: frame {pc1_min_frame}")
print(f"PC1 maximum conformation: frame {pc1_max_frame}")
```

### Density Analysis

```python
import MDAnalysis as mda
from MDAnalysis.analysis import density
import numpy as np

u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Calculate water density around protein
water = u.select_atoms('resname WAT and name O')

# Create density grid
dens = density.DensityAnalysis(water, delta=1.0)  # 1 Angstrom grid
dens.run()

# Access density grid
density_grid = dens.results.density

print(f"Density grid shape: {density_grid.grid.shape}")
print(f"Mean density: {np.mean(density_grid.grid):.4f} atoms/Å³")
print(f"Max density: {np.max(density_grid.grid):.4f} atoms/Å³")

# Export for visualization (can view in VMD, PyMOL, ChimeraX)
density_grid.export('water_density.dx', type='double')
print("Density exported to water_density.dx")

# Find high-density regions (binding sites)
threshold = np.mean(density_grid.grid) + 2 * np.std(density_grid.grid)
high_density_points = np.where(density_grid.grid > threshold)

print(f"Number of high-density voxels: {len(high_density_points[0])}")
```

### Native Contacts (Q Analysis)

```python
import MDAnalysis as mda
from MDAnalysis.analysis.contacts import Contacts
import numpy as np
import matplotlib.pyplot as plt

# Load native structure and trajectory
native = mda.Universe('native.pdb')
u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Get native contacts (CA atoms within 8 Angstroms)
native_ca = native.select_atoms('protein and name CA')
native_distances = mda.analysis.distances.distance_array(
    native_ca.positions,
    native_ca.positions
)

# Define native contacts
cutoff = 8.0
native_contacts = np.where((native_distances < cutoff) & 
                          (native_distances > 0))
n_native_contacts = len(native_contacts[0]) // 2

print(f"Number of native contacts: {n_native_contacts}")

# Calculate Q (fraction of native contacts) over trajectory
q_values = []
mobile_ca = u.select_atoms('protein and name CA')

for ts in u.trajectory:
    # Calculate current distances
    current_distances = mda.analysis.distances.distance_array(
        mobile_ca.positions,
        mobile_ca.positions
    )
    
    # Count how many native contacts are still present
    maintained_contacts = current_distances[native_contacts] < cutoff
    q = np.sum(maintained_contacts) / n_native_contacts
    q_values.append(q)

q_values = np.array(q_values)
time = np.arange(len(q_values)) * u.trajectory.dt

# Plot
plt.figure(figsize=(10, 6))
plt.plot(time, q_values)
plt.xlabel('Time (ps)')
plt.ylabel('Q (Fraction of Native Contacts)')
plt.title('Native Contacts Conservation')
plt.ylim(0, 1)
plt.grid(True)
plt.savefig('native_contacts.png', dpi=300)

print(f"Mean Q: {np.mean(q_values):.2f}")
print(f"Q at final frame: {q_values[-1]:.2f}")
```

## Integration with Other Tools

### Converting to Biopython

```python
import MDAnalysis as mda
from Bio.PDB import PDBIO
from Bio.PDB.Structure import Structure
from Bio.PDB.Model import Model
from Bio.PDB.Chain import Chain
from Bio.PDB.Residue import Residue
from Bio.PDB.Atom import Atom

def mda_to_biopython(universe, frame=0):
    """
    Convert MDAnalysis Universe to Biopython Structure.
    
    Args:
        universe: MDAnalysis Universe
        frame: Frame number to convert
    """
    # Go to specific frame
    universe.trajectory[frame]
    
    # Create Biopython structure
    structure = Structure('structure')
    model = Model(0)
    structure.add(model)
    
    # Get current segment
    for seg in universe.segments:
        chain = Chain(seg.segid if seg.segid else 'A')
        model.add(chain)
        
        for residue in seg.residues:
            # Create residue
            resname = residue.resname
            resid = residue.resid
            bio_residue = Residue((' ', resid, ' '), resname, '')
            chain.add(bio_residue)
            
            # Add atoms
            for atom in residue.atoms:
                bio_atom = Atom(
                    name=atom.name,
                    coord=atom.position,
                    bfactor=0.0,
                    occupancy=1.0,
                    altloc=' ',
                    fullname=atom.name,
                    serial_number=atom.ix,
                    element=atom.element if hasattr(atom, 'element') else atom.name[0]
                )
                bio_residue.add(bio_atom)
    
    return structure

# Example usage
u = mda.Universe('protein.pdb', 'trajectory.dcd')

# Convert frame 100 to Biopython
bio_structure = mda_to_biopython(u, frame=100)

# Save using Biopython
io = PDBIO()
io.set_structure(bio_structure)
io.save('frame_100_biopython.pdb')

print("Converted to Biopython and saved")
```

### Exporting for VMD/PyMOL

```python
import MDAnalysis as mda

u = mda.Universe('topology.pdb', 'trajectory.dcd')

# Select specific atoms
protein = u.select_atoms('protein')
important_residues = u.select_atoms('resid 10 20 30 40 50')

# Write selection to PDB
protein.write('protein_only.pdb')
important_residues.write('important_residues.pdb')

# Write trajectory (DCD format for VMD)
with mda.Writer('protein_trajectory.dcd', protein.n_atoms) as W:
    for ts in u.trajectory:
        W.write(protein)

# Write specific frames
frames_to_save = [0, 50, 100, 150, 200]
with mda.Writer('key_frames.pdb', protein.n_atoms) as W:
    for frame_idx in frames_to_save:
        u.trajectory[frame_idx]
        W.write(protein)

print("Exported files for visualization")
```

### Parallel Processing with Dask

```python
import MDAnalysis as mda
from MDAnalysis.analysis.rms import RMSD
from dask import delayed, compute
import numpy as np

def calculate_rmsd_chunk(topology, trajectory_chunk, reference):
    """
    Calculate RMSD for a chunk of trajectory.
    
    Args:
        topology: Topology file
        trajectory_chunk: List of trajectory files
        reference: Reference Universe
    """
    u = mda.Universe(topology, *trajectory_chunk)
    mobile = u.select_atoms('backbone')
    ref = reference.select_atoms('backbone')
    
    R = RMSD(mobile, ref, select='backbone')
    R.run()
    
    return R.results.rmsd[:, 2]

# Split trajectory into chunks
topology = 'topology.pdb'
trajectories = [f'traj_part{i}.dcd' for i in range(10)]
reference = mda.Universe('reference.pdb')

# Create delayed tasks
chunk_size = 2
chunks = [trajectories[i:i+chunk_size] for i in range(0, len(trajectories), chunk_size)]

tasks = [delayed(calculate_rmsd_chunk)(topology, chunk, reference) 
         for chunk in chunks]

# Compute in parallel
results = compute(*tasks)

# Combine results
rmsd_all = np.concatenate(results)

print(f"Total frames processed: {len(rmsd_all)}")
print(f"Mean RMSD: {np.mean(rmsd_all):.2f} Å")
```

## Practical Workflows

### Complete Protein Stability Analysis

```python
import MDAnalysis as mda
from MDAnalysis.analysis import rms, align
from MDAnalysis.analysis.hydrogenbonds.hbond_analysis import HydrogenBondAnalysis
import numpy as np
import matplotlib.pyplot as plt

def analyze_protein_stability(topology, trajectory, output_prefix='analysis'):
    """
    Complete workflow for protein stability analysis.
    
    Analyzes:
    - RMSD (backbone, all-atom)
    - RMSF per residue
    - Radius of gyration
    - Hydrogen bonds
    - Secondary structure retention (if possible)
    """
    print("Loading trajectory...")
    u = mda.Universe(topology, trajectory)
    
    # Create reference (first frame)
    reference = u.copy()
    reference.trajectory[0]
    
    results = {}
    
    # 1. RMSD Analysis
    print("Calculating RMSD...")
    protein = u.select_atoms('protein')
    ref_protein = reference.select_atoms('protein')
    
    # Backbone RMSD
    rmsd_bb = rms.RMSD(protein, ref_protein, select='backbone')
    rmsd_bb.run()
    
    # All-atom RMSD
    rmsd_all = rms.RMSD(protein, ref_protein, select='protein')
    rmsd_all.run()
    
    results['rmsd_backbone'] = rmsd_bb.results.rmsd[:, 2]
    results['rmsd_allatom'] = rmsd_all.results.rmsd[:, 2]
    
    # 2. RMSF Analysis
    print("Calculating RMSF...")
    ca_atoms = u.select_atoms('protein and name CA')
    rmsf_analysis = rms.RMSF(ca_atoms)
    rmsf_analysis.run()
    
    results['rmsf'] = rmsf_analysis.results.rmsf
    results['residue_ids'] = [atom.resid for atom in ca_atoms]
    
    # 3. Radius of Gyration
    print("Calculating Radius of Gyration...")
    rg_values = []
    for ts in u.trajectory:
        rg_values.append(protein.radius_of_gyration())
    results['radius_gyration'] = np.array(rg_values)
    
    # 4. Hydrogen Bonds
    print("Analyzing hydrogen bonds...")
    hbonds = HydrogenBondAnalysis(
        universe=u,
        donors_sel='protein',
        hydrogens_sel='protein',
        acceptors_sel='protein'
    )
    hbonds.run()
    
    # Count H-bonds per frame
    hbond_counts = []
    for frame in range(len(u.trajectory)):
        n_hbonds = len(hbonds.results.hbonds[
            hbonds.results.hbonds[:, 0] == frame
        ])
        hbond_counts.append(n_hbonds)
    results['hbond_counts'] = np.array(hbond_counts)
    
    # Generate plots
    print("Generating plots...")
    time = np.arange(len(u.trajectory)) * u.trajectory.dt
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # RMSD
    axes[0, 0].plot(time, results['rmsd_backbone'], label='Backbone')
    axes[0, 0].plot(time, results['rmsd_allatom'], label='All-atom', alpha=0.7)
    axes[0, 0].set_xlabel('Time (ps)')
    axes[0, 0].set_ylabel('RMSD (Å)')
    axes[0, 0].set_title('RMSD over time')
    axes[0, 0].legend()
    axes[0, 0].grid(True)
    
    # RMSF
    axes[0, 1].plot(results['residue_ids'], results['rmsf'])
    axes[0, 1].set_xlabel('Residue Number')
    axes[0, 1].set_ylabel('RMSF (Å)')
    axes[0, 1].set_title('Per-residue Fluctuations')
    axes[0, 1].grid(True)
    
    # Radius of Gyration
    axes[1, 0].plot(time, results['radius_gyration'])
    axes[1, 0].set_xlabel('Time (ps)')
    axes[1, 0].set_ylabel('Rg (Å)')
    axes[1, 0].set_title('Radius of Gyration')
    axes[1, 0].grid(True)
    
    # Hydrogen Bonds
    axes[1, 1].plot(time, results['hbond_counts'])
    axes[1, 1].set_xlabel('Time (ps)')
    axes[1, 1].set_ylabel('Number of H-bonds')
    axes[1, 1].set_title('Intramolecular Hydrogen Bonds')
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_stability.png', dpi=300)
    print(f"Saved plot: {output_prefix}_stability.png")
    
    # Print summary
    print("\n" + "="*60)
    print("STABILITY ANALYSIS SUMMARY")
    print("="*60)
    print(f"Trajectory length: {len(u.trajectory)} frames ({time[-1]:.1f} ps)")
    print(f"\nRMSD (backbone):")
    print(f"  Mean: {np.mean(results['rmsd_backbone']):.2f} Å")
    print(f"  Max: {np.max(results['rmsd_backbone']):.2f} Å")
    print(f"  Final: {results['rmsd_backbone'][-1]:.2f} Å")
    print(f"\nRMSF:")
    print(f"  Mean: {np.mean(results['rmsf']):.2f} Å")
    print(f"  Most flexible residue: {results['residue_ids'][np.argmax(results['rmsf'])]}")
    print(f"\nRadius of Gyration:")
    print(f"  Mean: {np.mean(results['radius_gyration']):.2f} Å")
    print(f"  Std: {np.std(results['radius_gyration']):.2f} Å")
    print(f"\nHydrogen Bonds:")
    print(f"  Mean: {np.mean(results['hbond_counts']):.1f}")
    print(f"  Range: {np.min(results['hbond_counts'])}-{np.max(results['hbond_counts'])}")
    
    # Stability assessment
    print("\n" + "="*60)
    print("STABILITY ASSESSMENT")
    print("="*60)
    
    if np.mean(results['rmsd_backbone']) < 2.0:
        print("✓ Structure is STABLE (low RMSD)")
    elif np.mean(results['rmsd_backbone']) < 4.0:
        print("⚠ Structure shows MODERATE fluctuations")
    else:
        print("✗ Structure is UNSTABLE (high RMSD)")
    
    if np.std(results['radius_gyration']) < 1.0:
        print("✓ Protein maintains COMPACT structure")
    else:
        print("⚠ Protein shows conformational EXPANSION/CONTRACTION")
    
    return results

# Example usage
results = analyze_protein_stability(
    'topology.pdb',
    'trajectory.dcd',
    output_prefix='protein'
)
```

### Protein-Ligand Binding Analysis

```python
import MDAnalysis as mda
from MDAnalysis.analysis import distances, contacts
from MDAnalysis.analysis.hydrogenbonds.hbond_analysis import HydrogenBondAnalysis
import numpy as np
import matplotlib.pyplot as plt

def analyze_protein_ligand_binding(topology, trajectory, 
                                   ligand_resname='LIG',
                                   binding_site_resids=None):
    """
    Comprehensive protein-ligand binding analysis.
    
    Args:
        topology: Topology file
        trajectory: Trajectory file
        ligand_resname: Residue name of ligand
        binding_site_resids: List of binding site residue IDs
    """
    print("Loading complex...")
    u = mda.Universe(topology, trajectory)
    
    protein = u.select_atoms('protein')
    ligand = u.select_atoms(f'resname {ligand_resname}')
    
    if len(ligand) == 0:
        raise ValueError(f"No ligand found with resname {ligand_resname}")
    
    print(f"Found ligand with {len(ligand)} atoms")
    
    results = {}
    
    # 1. Ligand RMSD
    print("Calculating ligand RMSD...")
    from MDAnalysis.analysis.rms import RMSD
    ligand_rmsd = RMSD(ligand, ligand, select=f'resname {ligand_resname}',
                       ref_frame=0)
    ligand_rmsd.run()
    results['ligand_rmsd'] = ligand_rmsd.results.rmsd[:, 2]
    
    # 2. Protein-Ligand Distance
    print("Calculating protein-ligand distance...")
    if binding_site_resids:
        binding_site = u.select_atoms(f'protein and resid {" ".join(map(str, binding_site_resids))}')
    else:
        binding_site = protein
    
    min_distances = []
    for ts in u.trajectory:
        dist_array = distances.distance_array(
            ligand.center_of_mass()[np.newaxis, :],
            binding_site.positions,
            box=u.dimensions
        )
        min_distances.append(np.min(dist_array))
    results['min_distance'] = np.array(min_distances)
    
    # 3. Protein-Ligand Contacts
    print("Analyzing contacts...")
    ca = contacts.Contacts(
        u,
        selection=(ligand, protein),
        refgroup=(ligand, protein),
        radius=4.5
    )
    ca.run()
    results['contacts'] = ca.results.timeseries[:, 1]
    
    # 4. Protein-Ligand H-bonds
    print("Analyzing hydrogen bonds...")
    # Ligand as donor
    hb_lig_don = HydrogenBondAnalysis(
        universe=u,
        donors_sel=f'resname {ligand_resname}',
        hydrogens_sel=f'resname {ligand_resname}',
        acceptors_sel='protein'
    )
    hb_lig_don.run()
    
    # Protein as donor
    hb_prot_don = HydrogenBondAnalysis(
        universe=u,
        donors_sel='protein',
        hydrogens_sel='protein',
        acceptors_sel=f'resname {ligand_resname}'
    )
    hb_prot_don.run()
    
    # Combine
    hbond_counts = []
    for frame in range(len(u.trajectory)):
        n1 = len(hb_lig_don.results.hbonds[hb_lig_don.results.hbonds[:, 0] == frame])
        n2 = len(hb_prot_don.results.hbonds[hb_prot_don.results.hbonds[:, 0] == frame])
        hbond_counts.append(n1 + n2)
    results['hbonds'] = np.array(hbond_counts)
    
    # Plot results
    print("Generating plots...")
    time = np.arange(len(u.trajectory)) * u.trajectory.dt
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Ligand RMSD
    axes[0, 0].plot(time, results['ligand_rmsd'])
    axes[0, 0].set_xlabel('Time (ps)')
    axes[0, 0].set_ylabel('Ligand RMSD (Å)')
    axes[0, 0].set_title('Ligand Stability')
    axes[0, 0].grid(True)
    
    # Distance to binding site
    axes[0, 1].plot(time, results['min_distance'])
    axes[0, 1].set_xlabel('Time (ps)')
    axes[0, 1].set_ylabel('Min Distance (Å)')
    axes[0, 1].set_title('Ligand-Protein Proximity')
    axes[0, 1].grid(True)
    
    # Contacts
    axes[1, 0].plot(time, results['contacts'])
    axes[1, 0].set_xlabel('Time (ps)')
    axes[1, 0].set_ylabel('Number of Contacts')
    axes[1, 0].set_title('Protein-Ligand Contacts (< 4.5 Å)')
    axes[1, 0].grid(True)
    
    # H-bonds
    axes[1, 1].plot(time, results['hbonds'])
    axes[1, 1].set_xlabel('Time (ps)')
    axes[1, 1].set_ylabel('Number of H-bonds')
    axes[1, 1].set_title('Protein-Ligand Hydrogen Bonds')
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig('protein_ligand_analysis.png', dpi=300)
    
    # Summary
    print("\n" + "="*60)
    print("PROTEIN-LIGAND BINDING SUMMARY")
    print("="*60)
    print(f"\nLigand RMSD:")
    print(f"  Mean: {np.mean(results['ligand_rmsd']):.2f} Å")
    print(f"  Max: {np.max(results['ligand_rmsd']):.2f} Å")
    print(f"\nLigand-Protein Distance:")
    print(f"  Mean: {np.mean(results['min_distance']):.2f} Å")
    print(f"  Min: {np.min(results['min_distance']):.2f} Å")
    print(f"\nContacts:")
    print(f"  Mean: {np.mean(results['contacts']):.1f}")
    print(f"  Range: {np.min(results['contacts'])}-{np.max(results['contacts'])}")
    print(f"\nHydrogen Bonds:")
    print(f"  Mean: {np.mean(results['hbonds']):.1f}")
    print(f"  Max: {np.max(results['hbonds'])}")
    
    # Binding assessment
    print("\n" + "="*60)
    print("BINDING ASSESSMENT")
    print("="*60)
    
    if np.mean(results['ligand_rmsd']) < 2.0:
        print("✓ Ligand remains STABLE in binding site")
    else:
        print("⚠ Ligand shows SIGNIFICANT movement")
    
    if np.mean(results['contacts']) > 5:
        print("✓ STRONG protein-ligand interactions")
    elif np.mean(results['contacts']) > 2:
        print("⚠ MODERATE protein-ligand interactions")
    else:
        print("✗ WEAK protein-ligand interactions")
    
    if np.mean(results['hbonds']) >= 2:
        print(f"✓ Ligand forms stable H-bonds ({np.mean(results['hbonds']):.1f} average)")
    elif np.mean(results['hbonds']) >= 1:
        print(f"⚠ Limited H-bonding ({np.mean(results['hbonds']):.1f} average)")
    else:
        print("✗ Minimal H-bonding interaction")
    
    return results

# Example usage
results = analyze_protein_ligand_binding(
    'complex.pdb',
    'trajectory.dcd',
    ligand_resname='LIG',
    binding_site_resids=[45, 46, 89, 92, 115, 118]
)
```

This comprehensive MDAnalysis guide covers 50+ examples for molecular dynamics trajectory analysis!
