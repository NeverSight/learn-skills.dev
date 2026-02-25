---
name: slurm
description: Submit, manage, and monitor GPU workloads on SRP's Slurm clusters with Apptainer containers
---

# Slurm Cluster Management

Help developers submit, manage, and troubleshoot GPU-accelerated workloads on SRP's Slurm clusters. Supports training, inference, and data processing jobs using Apptainer containers.

## When to Use This Skill

Use this skill when:
- Submitting GPU training or inference jobs to Slurm clusters
- Managing running or queued jobs
- Monitoring cluster resources and job status
- Debugging job failures or performance issues
- Writing Slurm job scripts with Apptainer containers
- Checking GPU availability and utilization

## SRP Slurm Clusters

### Oracle OKE Cluster (H100 GPUs)

**SSH Access:**
```bash
ssh -p 2222 <your-ldap-username>@129.80.180.16

# Example:
ssh -p 2222 zhuguangbin@129.80.180.16
```

**GPU Type:** H100
**Partition:** `h100` (must specify in job scripts)
**Use Cases:** Large model training, high-performance inference

### DO DOKS Cluster (H200 GPUs)

**SSH Access:**
```bash
ssh -p 2222 <your-ldap-username>@129.212.240.50

# Example:
ssh -p 2222 zhuguangbin@129.212.240.50
```

**GPU Type:** H200
**Partition:** Specify in job scripts
**Use Cases:** Latest GPU workloads, large-scale training

### Data Access

Both clusters use **JuiceFS** for unified data access:
- Path: `/data0/` or `/data/srp/`
- Same permissions and directory structure as development machines
- Shared across all cluster nodes and with A10 dev machines

### Monitoring

**Oracle OKE Cluster Dashboards:**
- Cluster Overview: https://grafana.g.yesy.site/d/edrg5th9t1edcb/slinky-slurm
- Workload Monitoring: https://grafana.g.yesy.site/d/f2c83374-71e2-42c6-92a1-10505b584cf2/workload
- Job-Level Stats: https://grafana.g.yesy.site/d/HRLkiLS7k/slurmjobstats

**DO DOKS Cluster Dashboards:**
- Cluster Overview: https://grafana.g2.yesy.site/d/edrg5th9t1edcb/slinky-slurm
- Workload Monitoring: https://grafana.g2.yesy.site/d/workload/workload
- Job-Level Stats: https://grafana.g2.yesy.site/d/slurm/slurm

**Metrics Available:**
- Cluster resource utilization
- GPU availability and usage
- Job queue status
- Per-job resource consumption
- Historical workload patterns

## Essential Slurm Commands

### Job Submission

```bash
# Submit batch job script
sbatch job_script.sh

# Submit with ssubmit wrapper (recommended)
ssubmit -j job_name -p h100 -g 1 -c 10 -m 32G -t 2:00:00 -cmd "python train.py"

# Interactive job allocation
salloc --partition=h100 --gres=gpu:1 --time=01:00:00

# Run command directly
srun --partition=h100 --gres=gpu:1 python test.py
```

### Job Management

```bash
# View your jobs
squeue -u $USER

# View all jobs
squeue

# View specific job details
scontrol show job <job_id>

# Cancel job
scancel <job_id>

# Cancel all your jobs
scancel -u $USER

# Cancel jobs by name
scancel --name=job_name
```

### Cluster Information

```bash
# View partitions and nodes
sinfo

# View detailed node info
sinfo -N -l

# Check GPU availability
sinfo -o "%20N %10c %10m %25f %10G"

# View specific partition
sinfo -p h100
```

### Job History

```bash
# View completed jobs
sacct

# View specific job details
sacct -j <job_id> --format=JobID,JobName,Partition,AllocCPUS,State,ExitCode

# View jobs from last week
sacct --starttime=now-7days --format=JobID,JobName,Elapsed,State,ExitCode
```

## Job Script Structure

### Modern Slurm Script (Simplified)

The new Slinky Slurm clusters use **prolog/epilog** for notifications, so scripts are much simpler:

```bash
#!/bin/bash
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --job-name=my-training-job
#SBATCH --partition=h100
#SBATCH --gres=gpu:H100:1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=10
#SBATCH --mem=32GB
#SBATCH --time=02:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=slurm-notification@srp.one

set -x

#==============================
# Environment Setup
#==============================
export MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
export MASTER_PORT=$(shuf -i 1000-65535 -n 1)

export LOGLEVEL=INFO
export NCCL_DEBUG=INFO
export PYTHONFAULTHANDLER=1

# Set your tokens (replace with actual values)
export HF_TOKEN=your_huggingface_token_here
export WANDB_API_KEY=your_wandb_api_key_here
export WANDB_PROJECT=${SLURM_JOB_NAME}
export WANDB_NAME=${SLURM_JOB_NAME}-$(date +%Y%m%d%H%M%S)

#==============================
# Pre-task initialization
#==============================
echo "Running pre-task initialization..."
# Your setup commands here

#==============================
# Main Job Execution
#==============================
echo "Starting main task..."
srun -v -l --jobid $SLURM_JOBID --job-name=${SLURM_JOB_NAME} \
  --output $SLURM_SUBMIT_DIR/logs/%x_%j_%s_%t_%N.out \
  --error $SLURM_SUBMIT_DIR/logs/%x_%j_%s_%t_%N.err \
  apptainer run --fakeroot --writable-tmpfs --nv \
  /data0/apptainer/pytorch_24.01-py3.sif bash -ex << 'EOF'

# ==== YOUR JOB COMMANDS START ====
echo "Training started at $(date)"

python train.py \
  --model gpt2 \
  --batch-size 32 \
  --epochs 10 \
  --output-dir /data0/models/

nvidia-smi

echo "Training completed at $(date)"
# ==== YOUR JOB COMMANDS END ====
EOF
```

### Key SBATCH Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--job-name` | Job name (shows in squeue) | `my-training` |
| `--partition` | Cluster partition | `h100` |
| `--gres` | GPU resources | `gpu:H100:1` (1 GPU)<br>`gpu:H100:2` (2 GPUs) |
| `--nodes` | Number of nodes | `1` (single node)<br>`2` (distributed) |
| `--cpus-per-task` | CPUs per task | `10` |
| `--mem` | Memory per node | `32GB` |
| `--time` | Max runtime | `02:00:00` (2 hours) |
| `--output` | stdout log file | `logs/%x_%j.out` |
| `--error` | stderr log file | `logs/%x_%j.err` |
| `--mail-type` | Email notification | `ALL`, `FAIL`, `END` |

**Log File Placeholders:**
- `%x` - Job name
- `%j` - Job ID
- `%s` - Step ID
- `%t` - Task ID
- `%N` - Node name

### Multi-Node Distributed Training

```bash
#!/bin/bash
#SBATCH --job-name=distributed-training
#SBATCH --partition=h100
#SBATCH --nodes=2
#SBATCH --gres=gpu:H100:2
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=10
#SBATCH --mem=64GB
#SBATCH --time=04:00:00

set -x

# Distributed training setup
export MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
export MASTER_PORT=12345
export WORLD_SIZE=$((SLURM_NNODES * SLURM_NTASKS_PER_NODE))

srun apptainer run --nv /data0/apptainer/pytorch_24.01-py3.sif \
  python -m torch.distributed.launch \
  --nproc_per_node=$SLURM_NTASKS_PER_NODE \
  --nnodes=$SLURM_NNODES \
  --node_rank=$SLURM_NODEID \
  --master_addr=$MASTER_ADDR \
  --master_port=$MASTER_PORT \
  train_distributed.py
```

## Using Apptainer Containers

### Available Container Images

**Location:** `/data0/apptainer/`

**Common Images:**
- `pytorch_24.01-py3.sif` - PyTorch 24.01 with Python 3
- `ray_2.52.0-py310-gpu.sif` - Ray 2.52.0 with Python 3.10
- Custom images built for specific projects

### Apptainer Command Patterns

```bash
# Run container with GPU support
apptainer run --nv /data0/apptainer/pytorch_24.01-py3.sif python script.py

# Shell into container
apptainer shell --nv /data0/apptainer/pytorch_24.01-py3.sif

# Execute single command
apptainer exec --nv /data0/apptainer/pytorch_24.01-py3.sif nvidia-smi

# With additional flags
apptainer run --fakeroot --writable-tmpfs --nv <image.sif> <command>
```

**Common Flags:**
- `--nv` - Enable NVIDIA GPU support
- `--fakeroot` - Fake root user privileges (for installing packages)
- `--writable-tmpfs` - Create writable temporary filesystem
- `--bind <src>:<dst>` - Mount additional directories

### Interactive Container Session

```bash
# Start interactive job with Apptainer
sapptainer -c 20 -m 200G -g 1 -p h100 -i /data0/apptainer/pytorch_24.01-py3.sif

# Parameters:
# -c: CPUs
# -m: Memory
# -g: GPUs
# -p: Partition
# -i: Container image
```

## Using ssubmit Wrapper

SRP provides `ssubmit` wrapper for simplified job submission:

```bash
# Basic usage
ssubmit -j job_name -p h100 -g 1 -c 10 -m 32G -t 2:00:00 \
  -cmd "python train.py"

# With custom script
ssubmit -j my-job -p h100 -g 2 -s job_script.sh

# Interactive mode
ssubmit -j interactive -p h100 -g 1 -i
```

**Parameters:**
- `-j` - Job name
- `-p` - Partition (h100, compute)
- `-g` - Number of GPUs
- `-c` - Number of CPUs
- `-m` - Memory (e.g., 32G)
- `-t` - Time limit (HH:MM:SS)
- `-cmd` - Command to run
- `-s` - Script file to execute
- `-i` - Interactive mode

**Reference:** https://github.com/SerendipityOneInc/llm-jobs/blob/main/slurm/ssubmit-examples/README.md

## Feishu Notifications

Slurm clusters automatically send **Feishu notifications** for job events via prolog/epilog:

**Notification Types:**
- ✅ Job started
- ✅ Job completed successfully
- ❌ Job failed with error code
- ⏱️ Job timeout
- 🛑 Job cancelled

**Notification Channel:** `slurm-notification@srp.one`

**What's Included:**
- Job ID, name, partition
- Node allocation
- Start and end time
- Exit status
- Resource usage summary
- Log file locations

**No Action Needed:** Notifications are automatic - no need to add notification code to your scripts.

## Best Practices

### Resource Allocation

1. **Request What You Need:**
   - Don't over-request CPUs/memory - it delays scheduling
   - Start with minimal resources, scale up if needed

2. **GPU Utilization:**
   - Use `nvidia-smi` to verify GPU is being used
   - Monitor GPU memory with `nvidia-smi dmon`

3. **Time Limits:**
   - Set realistic time limits (slightly above expected)
   - Jobs exceeding time limit are killed

4. **Partitions:**
   - Always specify partition explicitly
   - Use `h100` for Oracle, appropriate partition for DO

### Job Organization

```bash
# Organize logs by date
#SBATCH --output=logs/%Y%m%d/%x_%j.out
#SBATCH --error=logs/%Y%m%d/%x_%j.err

# Or by job name
#SBATCH --output=logs/%x/%j.out
#SBATCH --error=logs/%x/%j.err
```

### Checkpoint and Resume

```python
# Save checkpoints periodically
import torch
import os

checkpoint_dir = "/data0/checkpoints"
checkpoint_path = os.path.join(checkpoint_dir, f"model_epoch_{epoch}.pt")

torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}, checkpoint_path)

# Resume from checkpoint
if os.path.exists(checkpoint_path):
    checkpoint = torch.load(checkpoint_path)
    model.load_state_dict(checkpoint['model_state_dict'])
    start_epoch = checkpoint['epoch'] + 1
```

### Error Handling

```bash
# Set bash options for safety
set -e  # Exit on error
set -u  # Error on undefined variable
set -x  # Print commands (useful for debugging)
set -o pipefail  # Exit on pipe failure

# Add error traps
trap 'echo "Error on line $LINENO"; exit 1' ERR
```

## Monitoring and Debugging

### Check Job Status

```bash
# Detailed job info
scontrol show job <job_id>

# Watch job queue
watch -n 5 squeue -u $USER

# Check why job is pending
squeue -j <job_id> --start
```

### View Logs

```bash
# Tail logs while job runs
tail -f logs/job_name_12345.out

# View last 100 lines
tail -n 100 logs/job_name_12345.out

# Search for errors
grep -i error logs/job_name_12345.err
```

### GPU Monitoring

```bash
# Inside running job container
nvidia-smi

# Continuous monitoring
nvidia-smi dmon

# Detailed GPU utilization
nvidia-smi --query-gpu=timestamp,name,utilization.gpu,utilization.memory,memory.used,memory.free --format=csv -l 5
```

### Resource Usage

```bash
# Check job efficiency
seff <job_id>

# Detailed accounting
sacct -j <job_id> --format=JobID,JobName,Elapsed,CPUTime,MaxRSS,State
```

## Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| **Job pending forever** | No available resources | Check `sinfo` for available GPUs; adjust resource requests |
| **"Out of memory" error** | Insufficient memory request | Increase `--mem` in job script |
| **GPU not detected** | Missing `--gres` or `--nv` | Add `--gres=gpu:X` to sbatch, `--nv` to apptainer |
| **Container not found** | Wrong image path | Verify path in `/data0/apptainer/` |
| **Permission denied** | File permissions issue | Check file ownership and permissions |
| **Module not found** | Missing Python packages | Install in container or use different image |
| **NCCL timeout** | Network issues in distributed training | Check NCCL env vars, verify nodes can communicate |
| **Killed job (OOM)** | Memory exceeded | Reduce batch size or increase `--mem` |

## Quick Reference

### Essential Commands

```bash
# Submit job
sbatch job.sh

# Check queue
squeue -u $USER

# Job details
scontrol show job <job_id>

# Cancel job
scancel <job_id>

# View logs
tail -f logs/job_*.out

# Cluster info
sinfo -p h100

# Job history
sacct --starttime=today
```

### Example Workflows

#### 1. Quick GPU Test

```bash
# Submit test job
sbatch << 'EOF'
#!/bin/bash
#SBATCH --job-name=gpu-test
#SBATCH --partition=h100
#SBATCH --gres=gpu:1
#SBATCH --time=00:10:00
#SBATCH --output=test_%j.out

srun apptainer exec --nv /data0/apptainer/pytorch_24.01-py3.sif \
  nvidia-smi
EOF
```

#### 2. Training with Checkpoints

```bash
#!/bin/bash
#SBATCH --job-name=training-with-checkpoint
#SBATCH --partition=h100
#SBATCH --gres=gpu:H100:1
#SBATCH --time=04:00:00
#SBATCH --signal=B:USR1@60

checkpoint_handler() {
    echo "Received signal, saving checkpoint..."
    # Signal Python process to save checkpoint
    pkill -USR1 -f train.py
}

trap checkpoint_handler USR1

srun apptainer run --nv /data0/apptainer/pytorch_24.01-py3.sif \
  python train.py \
  --checkpoint-dir /data0/checkpoints \
  --resume-if-exists
```

#### 3. Batch Processing

```bash
#!/bin/bash
#SBATCH --job-name=batch-inference
#SBATCH --partition=h100
#SBATCH --gres=gpu:H100:1
#SBATCH --array=0-9
#SBATCH --time=01:00:00

# Process 10 shards in parallel
SHARD_ID=$SLURM_ARRAY_TASK_ID

srun apptainer run --nv /data0/apptainer/pytorch_24.01-py3.sif \
  python inference.py \
  --input /data0/input/shard_${SHARD_ID}.json \
  --output /data0/output/shard_${SHARD_ID}.json
```

## Resources

### Official Documentation
- Slurm Commands: https://slurm.schedmd.com/man_index.html
- Slurm Quick Start: https://slurm.schedmd.com/quickstart.html
- Apptainer User Guide: https://apptainer.org/docs/user/latest/

### SRP Resources
- Deployment Guide: https://starquest.feishu.cn/wiki/TZASwm86nivXLTkMV6kcoJF4n2I
- **Oracle OKE Grafana:**
  - Cluster: https://grafana.g.yesy.site/d/edrg5th9t1edcb/slinky-slurm
  - Workload: https://grafana.g.yesy.site/d/f2c83374-71e2-42c6-92a1-10505b584cf2/workload
  - Job Stats: https://grafana.g.yesy.site/d/HRLkiLS7k/slurmjobstats
- **DO DOKS Grafana:**
  - Cluster: https://grafana.g2.yesy.site/d/edrg5th9t1edcb/slinky-slurm
  - Workload: https://grafana.g2.yesy.site/d/workload/workload
  - Job Stats: https://grafana.g2.yesy.site/d/slurm/slurm
- ssubmit Examples: https://github.com/SerendipityOneInc/llm-jobs/blob/main/slurm/ssubmit-examples/README.md

## Implementation Steps

When helping users with Slurm jobs:

1. **Understand Requirements:**
   - What workload type? (training, inference, data processing)
   - GPU requirements (quantity, memory)
   - Expected runtime
   - Data input/output locations

2. **Choose Cluster:**
   - Oracle OKE (H100) for most workloads
   - DO DOKS (H200) for cutting-edge GPU needs

3. **Write Job Script:**
   - Use modern simplified template (no notification code)
   - Specify appropriate resources
   - Use Apptainer container with `--nv` flag
   - Set up proper logging

4. **Submit and Monitor:**
   - Submit with `sbatch` or `ssubmit`
   - Monitor with `squeue` and Grafana
   - Check logs for errors
   - Verify GPU utilization

5. **Debug Issues:**
   - Check Feishu notifications for failure reasons
   - Review log files
   - Use `scontrol` for detailed job info
   - Consult troubleshooting table

6. **Optimize:**
   - Adjust batch sizes based on GPU memory
   - Use job arrays for parallel processing
   - Implement checkpointing for long runs
   - Monitor resource usage with `sacct` and `seff`
