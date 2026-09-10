---
name: remote-compute-ssh
description: Run Feynman research jobs on SSH, Slurm, or lab hosts. Use when a task needs remote host setup, job submission, log harvest, artifact sync, or GPU/cluster execution outside Modal.
---

# Remote Compute: SSH

Use this skill for lab machines, SSH hosts, and Slurm-style research jobs.

Workflow:

1. Record host alias, scheduler, working directory, environment module/conda/container needs, data paths, and artifact return path.
2. Verify access and a tiny smoke command before the main job.
3. Submit with a bounded script that logs package versions, hardware, command, and seed.
4. Harvest stdout/stderr, job id, exit status, produced artifacts, and checksums into the Feynman workspace.
5. Mark failed or partial jobs honestly; do not fabricate remote artifacts from local expectations.

Keep remote credentials and private paths out of user-facing summaries unless they are needed for reproducibility.
