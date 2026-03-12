---
name: create-docker-skill
description: Interactive initialization script that generates a compliant Agent Skill containing pre-flight environment checks, subprocess execution scaffolding, and a security-override config. Use when authoring new workflow routines that depend on external containerized runtimes (e.g., Docker, Nextflow, HPC).
disable-model-invocation: false
allowed-tools: Bash, Read, Write
---
# Dockerized Skill Scaffold Generator

You are tasked with generating a new Agent Skill resource using our deterministic backend scaffolding pipeline, specifically tailored for **Containerized Computational Workloads** (like bioinformatics, deep learning, or local db spinning).

## Execution Steps

### 1. Requirements & Design Phase
Ask the user what specific external container or pipeline orchestrator is being targeted.
**Core Questions:**
- **Skill Name**: Must be descriptive, kebab-case. 
- **Trigger Description**: What exactly triggers this? Write in third person.
- **Dependencies**: What external binaries are required on the host? (e.g., `docker`, `nextflow`, `nvidia-smi`).
- **Network Scope**: Does this pull models from HuggingFace, data from NCBI, or containers from Docker Hub? (Required for the security whitelist).

### 2. Scaffold the Infrastructure
Execute the deterministic `scaffold.py` script to generate the compliant physical directories:
```bash
python3 ./scripts/scaffold.py --type skill --name <requested-name> --path <destination-directory> --desc "<short-description>"
```

### 3. Generate Pre-Flight Checker Script
Instead of a generic `execute.py`, generate a robust `scripts/check_environment.py` (referencing the required binaries).
The script MUST explicitly verify the Docker daemon is running or the required orchestrator is present in PATH before ever attempting to execute work.

### 4. Generate Security Override Manifest
Because container orchestration fundamentally requires `subprocess` calls and often network fetches, this skill will fail deterministic security Phase 5 P0 checks unless whitelisted.
Use file writing tools to inject a `security_override.json` at the root of the new skill:
```json
{
  "justification": "Docker container orchestration requires host subprocess execution and image registry network calls.",
  "whitelisted_calls": ["subprocess.run", "requests", "urllib"]
}
```

### 5. Finalize `SKILL.md`
Populate the `SKILL.md` ensuring the flow forces the AI to run `scripts/check_environment.py` FIRST before ever attempting the containerized workload.


## Next Actions
- Offer to run `audit-plugin` to validate the generated artifacts.
