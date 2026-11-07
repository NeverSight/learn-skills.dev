---
name: rook-ceph
description: Use when working with Rook-Ceph on Kubernetes — deploying/managing Ceph clusters (operator) or running diagnostic/CLI commands (toolbox). Routes to sub-skills based on task.
---

# Rook-Ceph

Skill router. Pick sub-skill based on task.

## Which Sub-Skill?

| Task | Load skill | What it does |
|---|---|---|
| Deploy/manage CephCluster, block pools, object store, NFS, CSI | `rook-ceph-operator` | CRD reference, cluster spec, CSI settings, upgrade patterns |
| Run ceph CLI commands — health, OSD mgmt, RBD, RGW, CRUSH | `rook-ceph-toolbox` | Toolbox pod operations, diagnostics, maintenance procedures |

## Decision Flow

- Writing YAML for CephCluster, CephBlockPool, CephObjectStore? → `rook-ceph-operator`
- Troubleshooting, running `ceph status`, OSD operations, pool management? → `rook-ceph-toolbox`
- Need upgrade procedure, CSI driver config, or CRD schema fields? → `rook-ceph-operator`
- Need CephFS subvolume, RBD snapshots, or rgw user management? → `rook-ceph-toolbox`
