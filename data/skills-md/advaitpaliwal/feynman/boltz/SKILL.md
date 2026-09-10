---
name: boltz
description: Run or plan Boltz biomolecular structure predictions for proteins, complexes, ligands, or nucleic-acid assemblies. Use when a task asks for Boltz setup, inputs, outputs, confidence interpretation, or reproduction.
---

# Boltz

Use this skill when the active research run needs Boltz-style biomolecular prediction.

Workflow:

1. Normalize inputs into explicit entities: protein chains, nucleic-acid chains, ligands, covalent links, templates, constraints, and seeds.
2. Verify the available execution route from Feynman Settings, notebook runtimes, managed endpoints, Modal, SSH, or local installs before claiming the model can run.
3. Run only from a recorded input manifest. Preserve exact sequences, ligand identifiers, model parameters, seed, hardware, package version, and command.
4. Save structures, confidence outputs, logs, and rendered previews as Feynman artifacts.
5. Interpret the output as a hypothesis: separate high-confidence local folds from weak interfaces, ligand poses, flexible regions, and unsupported biological claims.

Do not treat a single attractive structure as proof. Add verification checks against source literature, known structures, or orthogonal experiments when the result drives a decision.
