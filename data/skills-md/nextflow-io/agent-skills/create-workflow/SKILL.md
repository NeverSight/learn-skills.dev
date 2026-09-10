---
name: create-workflow
description: |
  INVOKE THIS SKILL IMMEDIATELY when user asks to: write/create/build a Nextflow pipeline or workflow,
  create any bioinformatics pipeline (RNA-seq, DNA-seq, variant calling, ChIP-seq, etc.),
  or compose/chain Nextflow modules from the Nextflow Registry. This skill handles all Nextflow workflow creation tasks.
allowed-tools: Bash, Read, Edit, Write, Glob, Grep, Skill
---

# Nextflow Workflow Writer

Create complete Nextflow workflows by composing validated modules from the [Nextflow Registry](https://registry.nextflow.io).

Modules are published under namespaces (e.g. `nf-core/fastqc`), and these skills compose modules from any of them.

**Requires Nextflow 26.04 or later** (for the `nextflow module` commands used during validation).

**NEVER write a wrapper workflow just to run/test a single module.**

❌ **WRONG** - Writing a workflow to run one module:
```groovy
// DO NOT DO THIS - not even when a module run fails!
include { FASTQC } from 'nf-core/fastqc'
workflow { FASTQC(Channel.fromPath('data/*.fq.gz')) }
```

✅ **CORRECT** - Use the `run-module` skill:
```
Skill(skill="run-module")
```

**The `run-module` skill:**
- Uses `nextflow module search/view` to discover and get proper inputs/parameters
- Runs modules directly via `nextflow module run <namespace>/<module>`
- No wrapper workflow needed

**⚠️ When a module run fails due to missing args:**
- DO NOT write a wrapper workflow as a "fix"
- Instead: run `nextflow module view <module>` to get correct parameters
- Fix the command-line arguments and re-run directly

**Only write a workflow in Step 4** when composing multiple validated modules together.

## 4-Step Workflow Creation Process

**ALWAYS follow this structured process when creating a new workflow:**

### Step 1: Identify Modules and Propose Plan

1. Use `nextflow module search <term>` to find Registry modules for each processing step
2. Use `nextflow module view <name>` to understand inputs/outputs of each module
3. **Present a plan to the user** with:
   - List of identified modules
   - Processing sequence (which module runs first, second, etc.)
   - Data flow between modules (outputs → inputs)

**STOP and wait for user approval before proceeding.**

### Step 2: User Agreement

- Wait for user to review and approve the proposed plan
- Address any questions or modifications requested
- Only proceed when user explicitly agrees

### Step 3: Validate Modules ONE BY ONE (MANDATORY)

**NEVER skip this step.** After user agreement:

1. Determine appropriate **test data** for validation
2. For EACH module in the plan, sequentially:
   - **Install and run with test data**: Invoke `Skill(skill="run-module")`
   - **Verify outputs** - confirm expected data is produced
   - Only proceed to next module after current one succeeds
3. Log ALL module run commands and their outputs to a debug file with the `.modules-validation-` prefix
4. If a command fails, stop and show the user the command used and the output generated before trying something else

> **Note**: The `run-module` skill uses `nextflow module` commands for discovery, configuration, and execution — modules are installed on-the-fly.

**DO NOT proceed to Step 4 until ALL modules have been individually validated.**

### Step 4: Compose Final Workflow

Only after ALL modules run successfully:

1. Configure `nextflow.config` with Wave + Conda:
   ```groovy
   wave.enabled = true
   wave.strategy = 'conda,container'
   docker.enabled = true
   ```

2. Write the workflow script compositing all validated steps using **Nextflow managed modules** (no `./` prefix — Nextflow automatically downloads and installs them from the Nextflow Registry):
   ```groovy
   include { MODULE_A } from 'nf-core/module_a'
   include { MODULE_B } from 'nf-core/module_b'

   workflow {
       MODULE_A(input_ch)
       MODULE_B(MODULE_A.out.results)
   }
   ```

3. **Run the complete workflow using the same test data** to validate end-to-end

## Critical Guidelines

### Command Execution
- Use `-resume` flag to leverage cached results when appropriate
- Use absolute paths, never relative paths

### File Handling
- When specifying multiple files, separate with comma and wrap in double quotes: `--input "file1.fq,file2.fq"`
- ALWAYS expand wildcards/globs to comma-separated file lists before running
- Reference task IDs from stdout to locate output files in work directories

### Module Include Syntax
- `include { MOD } from 'nf-core/module'` — **Nextflow managed module** (default). Nextflow automatically downloads and installs it from the Nextflow Registry. Always prefer this form. (`nf-core` here is the namespace; substitute the actual namespace of the module you are using.)
- `include { MOD } from './modules/nf-core/module/main.nf'` — **Local file path**, resolved against the working directory. Only use when referencing locally modified modules.

### Module Selection
- Prefer single-tool modules over sub-workflows
- Do not write wrapper workflows to test single modules - use `Skill(skill="run-module")` instead
- Use `nextflow module search` to find modules, then `nextflow module view` for details

### Debugging Protocol
1. Check the task work directory using the task ID from stdout
2. Examine `.command.log`, `.command.err`, and `.command.out` files
3. Verify input files exist and are accessible
4. Check resource requirements (memory, CPUs) match available resources

## Skill Delegation (IMPORTANT)

**Delegate module-specific tasks to specialized skills using the `Skill` tool:**

| Task | Invoke Skill |
|------|--------------|
| Install/run/test a module | `Skill(skill="run-module")` |

### When to Delegate

- **Step 3 (Validate Modules)**: Use `run-module` skill for each module validation

### Example: Step 3 Validation

For each module in your plan:
```
1. Invoke: Skill(skill="run-module") → install, run with test data, and verify outputs
2. Only proceed to next module after success
```

These skills contain detailed instructions for their specific tasks and ensure consistent execution patterns.

## Quick Reference

```
Step 1: Identify modules → Propose plan to user
Step 2: Wait for user agreement
Step 3: Validate ALL modules ONE BY ONE with test data
Step 4: Compose final workflow (only after Step 3 succeeds)
```
