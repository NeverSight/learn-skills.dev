---
name: run-module
description: Run Nextflow Registry modules natively using `nextflow module` commands. Use when running, listing, or getting info about Nextflow modules.
allowed-tools: Bash, Read, Glob
---

# Run Nextflow Modules

Run modules from the [Nextflow Registry](https://registry.nextflow.io) natively using `nextflow module` commands. Everything is self-contained — no external tools or MCP needed. Modules are installed on-the-fly when run.

Modules are published under namespaces (e.g. `nf-core/fastqc`), and the `nextflow module` commands work with any of them.

**Requires Nextflow 26.04 or later** (for the `nextflow module` commands).

## ⛔ NEVER WRITE WRAPPER WORKFLOWS

**If a module fails due to missing arguments or incorrect parameters:**

❌ **WRONG** - Writing a wrapper workflow:
```groovy
// NEVER DO THIS - even if the module fails!
include { FASTQC } from 'nf-core/fastqc'
workflow { FASTQC(Channel.fromPath('*.fq.gz')) }
```

✅ **CORRECT** - Use `nextflow module view` to get the correct parameters:
```bash
nextflow module view nf-core/fastqc
```

**When a module run fails:**
1. Run `nextflow module view <module>` to get the command template
2. Fix the arguments based on the template
3. Re-run with `nextflow module run <module> ...`

**NEVER create a wrapper workflow as a "fix" for missing arguments.**

## Step 1: Search for the Module

Use `nextflow module search` with a natural language term — it performs similarity search on module name, description, and features:

```bash
nextflow module search "quality control"
nextflow module search "alignment"
nextflow module search "variant calling"
nextflow module search "BAM statistics"
```

## Step 2: Get Module Info and Run Template

Once you've identified the module, get its detailed info and the command template:

```bash
nextflow module view nf-core/fastqc
```

This returns the module description, inputs, parameters, and the exact run command template. Use this template as the basis for your run command.

## Step 3: Substitute Template Values and Run

Replace placeholder values in the template with the user's concrete values (file paths, parameters), then execute. No explicit install is needed — modules are fetched on-the-fly:

```bash
nextflow module run nf-core/fastqc \
  --input "/path/to/sample.fq.gz" \
  --outdir results
```

### Container Provisioning with Wave + Conda

Modules require containers for their underlying tools. Configure `nextflow.config` to use Wave + Conda so containers are provisioned on-the-fly from each module's conda packages:

```groovy
wave.enabled = true
wave.strategy = 'conda,container'
docker.enabled = true
```

This avoids the need to manually build or pull container images — Wave provisions them from the module's declared conda dependencies.

## Commands Reference

| Command | Description |
|---------|-------------|
| `nextflow module search <term>` | Similarity search by name/description/feature |
| `nextflow module view <name>` | Detailed info about the module and how to run it |
| `nextflow module run <name> [options]` | Run a module (installed on-the-fly) |
| `nextflow module list` | List available modules |

## Examples

### Single-end FASTQ Quality Control
```bash
# 1. Search
nextflow module search "quality control"

# 2. Get the template
nextflow module view nf-core/fastqc

# 3. Run with concrete values
nextflow module run nf-core/fastqc \
  --input "data/sample.fq.gz" \
  --outdir results_fastqc
```

### Paired-end Alignment
```bash
# 1. Search
nextflow module search "bwa alignment"

# 2. Get the template
nextflow module view nf-core/bwa/mem

# 3. Run with concrete values
nextflow module run nf-core/bwa/mem \
  --input "data/reads_1.fq.gz,data/reads_2.fq.gz" \
  --reference "data/genome.fa" \
  --outdir results_bwa
```

## Complete Workflow: Search → Info → Run

1. **Search** for the module:
   ```bash
   nextflow module search "quality control for FASTQ"
   ```

2. **Get info** and run template:
   ```bash
   nextflow module view nf-core/fastqc
   ```

3. **Substitute** template placeholders with actual values from the user's data

4. **Run** the module:
   ```bash
   nextflow module run nf-core/fastqc \
     --input "data/sample.fq.gz" \
     --outdir results
   ```

5. **Process output** — Read the stdout, summarize key results, and suggest the logical next step to the user

## Critical Rules

1. **SEARCH FIRST** — Always use `nextflow module search` to find the right module
2. **GET THE TEMPLATE** — Always run `nextflow module view` before running a module
3. **SUBSTITUTE TEMPLATE VALUES** — Replace all placeholders with concrete values from the user's data
4. **NEVER write wrapper workflows** — If a run fails, use `nextflow module view` to get correct args
5. **NEVER guess parameters** — Always get them from the info template
6. **Expand wildcards first** — Use `ls data/*.fq` then comma-separate results
7. **Quote multi-file inputs** — `--input "file1,file2,file3"`
8. **Use absolute paths** when possible
9. **ALWAYS PROCESS STDOUT OUTPUT** — After a successful run, present a summary and suggest the logical next step

## When Module Run Fails

**DO NOT write a wrapper workflow.** Instead:

1. Run `nextflow module view nf-core/<module>`
2. Compare the template with your command to find discrepancies
3. Fix your `nextflow module run` command with correct arguments
4. Re-run the corrected command

## Step 4: Process Run Output (MANDATORY)

The `nextflow module run` command prints its output to stdout. After a module run, you MUST:

1. **Read the stdout output** from the run command
2. **Present a clear summary** of the results to the user — highlight key metrics, status, and any warnings or errors
3. **Infer the next step** — Based on the output and the module that was run, suggest what the user might want to do next. Examples:
   - After `fastqc`: "Quality scores look good. Would you like to proceed to alignment with `bwa/mem`?"
   - After `bwa/mem`: "Alignment complete. Would you like to sort the BAM with `samtools/sort` or get stats with `samtools/stats`?"
   - After `fastp`: "Trimming done. Would you like to align the trimmed reads?"

Always frame next-step suggestions as questions to the user.

Only list or inspect output files in the work directory if the module or user specifically requires it — do not do this by default.
