---
name: parallel-workflow
description: Use when executing multiple tasks with dependencies - automatically determines optimal parallel execution order while respecting task dependencies through DAG scheduling
location: managed
allowed-tools:
  - Read
  - Write
  - Task
  - Bash(ls *)
---

# Parallel Workflow: DAG-Based Task Orchestration

Execute complex multi-step workflows with dependencies, maximizing parallelism while respecting execution order.

## Execution Instructions

When invoked, you will:

1. **Parse task definitions** with dependency declarations
2. **Build DAG** (Directed Acyclic Graph) and validate
3. **Compute execution waves** via topological sort
4. **Execute waves in parallel** - tasks at same level run concurrently
5. **Handle failures** - skip dependent tasks if parent fails
6. **Report progress** - show execution status and results

---

## Step 1: Parse Task Definitions

Task definitions follow this structure:

```yaml
tasks:
  - id: task-1
    description: "Description of what this task does"
    agent: "agent-name"  # Optional: specific agent type
    prompt: "Task-specific instructions"
    depends_on: []  # List of task IDs this depends on

  - id: task-2
    description: "Another task"
    prompt: "Instructions"
    depends_on: [task-1]  # This task runs after task-1

  - id: task-3
    description: "Independent task"
    prompt: "Instructions"
    depends_on: []  # Runs in parallel with task-1
```

**Field definitions:**
- `id` (required): Unique task identifier
- `description` (required): What this task does
- `prompt` (required): Instructions for the agent
- `depends_on` (required): Array of task IDs (empty array if no dependencies)
- `agent` (optional): Specific agent type to use (defaults to general-purpose)
- `capability` (optional): "highest", "high", "standard" (defaults to "high")

---

## Step 2: Build and Validate DAG

### Build Dependency Graph

For each task, create node and edges:

```python
# Pseudocode
graph = {}
for task in tasks:
    graph[task.id] = {
        'task': task,
        'dependencies': task.depends_on,
        'dependents': []  # Will be computed
    }

# Compute reverse edges (dependents)
for task_id, node in graph.items():
    for dep_id in node['dependencies']:
        graph[dep_id]['dependents'].append(task_id)
```

### Validate DAG

**1. Check all dependencies exist:**
```python
for task_id, node in graph.items():
    for dep_id in node['dependencies']:
        if dep_id not in graph:
            ERROR: "Task {task_id} depends on non-existent task {dep_id}"
```

**2. Detect cycles:**
```python
def has_cycle(graph):
    visited = set()
    rec_stack = set()

    def visit(node_id):
        visited.add(node_id)
        rec_stack.add(node_id)

        for dep_id in graph[node_id]['dependencies']:
            if dep_id not in visited:
                if visit(dep_id):
                    return True
            elif dep_id in rec_stack:
                return True  # Cycle detected!

        rec_stack.remove(node_id)
        return False

    for node_id in graph:
        if node_id not in visited:
            if visit(node_id):
                return True
    return False
```

**If cycle detected:**
```
ERROR: Circular dependency detected!

Example cycle: task-3 → task-5 → task-7 → task-3

This creates an infinite loop. Please restructure dependencies.
```

---

## Step 3: Compute Execution Waves (Topological Sort)

Use Kahn's algorithm to compute execution order:

```python
def compute_waves(graph):
    # Count incoming edges (dependencies)
    in_degree = {task_id: len(node['dependencies'])
                 for task_id, node in graph.items()}

    # Start with tasks that have no dependencies
    queue = [task_id for task_id, degree in in_degree.items()
             if degree == 0]

    waves = []

    while queue:
        # All tasks in queue can run in parallel (same wave)
        current_wave = queue[:]
        waves.append(current_wave)
        queue = []

        # Process each task in current wave
        for task_id in current_wave:
            # Reduce in-degree for dependent tasks
            for dependent_id in graph[task_id]['dependents']:
                in_degree[dependent_id] -= 1

                # If all dependencies satisfied, add to next wave
                if in_degree[dependent_id] == 0:
                    queue.append(dependent_id)

    return waves
```

**Output example:**
```yaml
execution_plan:
  wave_1: [task-1, task-2, task-3]  # Run in parallel
  wave_2: [task-4, task-5]          # After wave 1 completes
  wave_3: [task-6]                  # After wave 2 completes
  wave_4: [task-7]                  # After wave 3 completes

estimated_time: "sum of longest path in DAG"
parallelization_factor: "3.2x" # tasks_total / waves_count
```

---

## Step 4: Execute Waves in Parallel

For each wave, spawn tasks in parallel:

```yaml
for each wave in execution_plan:
  # Spawn all tasks in wave concurrently
  results = []

  for task_id in wave:
    task = graph[task_id]['task']

    # Use Task tool to spawn agent
    agent_type = task.agent or "general-purpose"
    capability = task.capability or "high"

    spawn_agent(
      subagent_type: agent_type,
      description: task.description,
      prompt: task.prompt,
      capability: capability
    )

  # Wait for all tasks in wave to complete
  wait_for_completion(wave)

  # Check for failures
  failed_tasks = [t for t in wave if task_failed(t)]

  if failed_tasks:
    handle_failures(failed_tasks, graph)
```

### Parallel Execution Pattern

```
Wave 1:  [Task A] [Task B] [Task C]  ← All run concurrently
            ↓        ↓        ↓
         Wait for all to complete
            ↓
Wave 2:    [Task D] [Task E]          ← Both run concurrently
              ↓        ↓
         Wait for all to complete
            ↓
Wave 3:      [Task F]                 ← Runs alone
```

---

## Step 5: Handle Failures

When a task fails, decide what to do with dependent tasks:

### Strategy 1: Skip Dependent Tasks (Default)

```yaml
if task fails:
  mark_failed(task_id)

  # Skip all tasks that depend on this one
  for dependent_id in compute_all_dependents(task_id):
    mark_skipped(dependent_id, reason: "dependency {task_id} failed")
```

### Strategy 2: Continue with Partial Results (Optional)

```yaml
if task fails:
  mark_failed(task_id)

  # Still execute dependent tasks, but with warning
  for dependent_id in dependents:
    add_warning(dependent_id, "Upstream task {task_id} failed")
    # Let task decide how to handle missing input
```

### Failure Report

```markdown
## Execution Summary

**Status:** PARTIAL_FAILURE

**Completed:** 7/10 tasks
**Failed:** 1/10 tasks
**Skipped:** 2/10 tasks (due to dependency failures)

### Failed Tasks

❌ **task-3** (Wave 2)
- Error: "API endpoint not responding"
- Impact: Skipped task-7, task-9 (depend on task-3)

### Skipped Tasks

⏭️ **task-7** - Skipped because task-3 failed
⏭️ **task-9** - Skipped because task-3 failed
```

---

## Step 6: Report Progress and Results

### During Execution

Show progress in real-time:

```
Executing Wave 1/4 (3 tasks)...
  ✓ task-1 completed (2.3s)
  ✓ task-2 completed (1.8s)
  ✓ task-3 completed (3.1s)

Executing Wave 2/4 (2 tasks)...
  ✓ task-4 completed (1.2s)
  ✗ task-5 failed (error: timeout)

Skipping Wave 3 (1 task) - dependencies failed
  ⏭️ task-6 skipped (depends on task-5)

Executing Wave 4/4 (1 task)...
  ✓ task-7 completed (0.8s)

Total execution time: 8.2s
Parallelization achieved: 3.5x speedup
```

### Final Report

Generate comprehensive execution report:

```markdown
# Parallel Workflow Execution Report

**Status:** SUCCESS | PARTIAL_FAILURE | FAILED
**Total Tasks:** 10
**Completed:** 8
**Failed:** 1
**Skipped:** 1
**Execution Time:** 8.2 seconds
**Parallelization Factor:** 3.5x

## Execution Timeline

### Wave 1 (0.0s - 3.1s)
- ✓ task-1: "Analyze structure" (2.3s)
- ✓ task-2: "Identify technologies" (1.8s)
- ✓ task-3: "Map dependencies" (3.1s)

### Wave 2 (3.1s - 5.5s)
- ✓ task-4: "Analyze architecture" (1.2s)
- ✗ task-5: "Trace workflows" (FAILED: timeout after 2.4s)

### Wave 3 (skipped)
- ⏭️ task-6: "Synthesize findings" (depends on task-5)

### Wave 4 (5.5s - 8.2s)
- ✓ task-7: "Generate report" (2.7s)

## Task Results

### Completed Tasks (8)

**task-1:** Analyze structure
- Agent: Structure Explorer
- Duration: 2.3s
- Output: Found 45 files across 12 directories...

**task-2:** Identify technologies
- Agent: Technology Explorer
- Duration: 1.8s
- Output: Detected Python 3.11, FastAPI, PostgreSQL...

[... rest of completed tasks ...]

### Failed Tasks (1)

**task-5:** Trace workflows
- Agent: Workflow Explorer
- Duration: 2.4s (timeout)
- Error: "Request timeout after 2.4s"
- Impact: Caused task-6 to be skipped

### Skipped Tasks (1)

**task-6:** Synthesize findings
- Reason: Upstream dependency task-5 failed
- Would have depended on: task-5

## Performance Analysis

**Critical Path:** task-1 → task-4 → task-7 (6.2s)
**Total Work:** 28.5s (sum of all task durations)
**Actual Time:** 8.2s
**Speedup:** 3.5x
**Parallelization Efficiency:** 87%

## Recommendations

1. Investigate task-5 timeout - may need longer timeout or optimization
2. Consider splitting task-3 (longest in Wave 1) into subtasks
3. Wave 4 could potentially merge with Wave 3 if dependencies allow
```

---

## Advanced Features

### Conditional Dependencies

```yaml
tasks:
  - id: security-scan
    prompt: "Run security scan"
    depends_on: []

  - id: deploy-staging
    prompt: "Deploy to staging"
    depends_on: [security-scan]
    condition: "security-scan.verdict == 'PASS'"  # Only if scan passes
```

### Retry Logic

```yaml
tasks:
  - id: flaky-api-call
    prompt: "Call external API"
    depends_on: []
    retry:
      max_attempts: 3
      backoff: "exponential"  # 1s, 2s, 4s
```

### Timeout Control

```yaml
tasks:
  - id: long-running-task
    prompt: "Process large dataset"
    depends_on: []
    timeout: 600000  # 10 minutes in milliseconds
```

---

## Example Usage Scenarios

### Scenario 1: Codebase Exploration with Dependencies

```yaml
tasks:
  # Wave 1: Independent base analysis
  - id: structure
    description: "Analyze directory structure"
    prompt: "Map out directory structure and file organization"
    depends_on: []

  # Wave 2: Depends on structure
  - id: tech-stack
    description: "Identify technologies"
    prompt: "Identify technologies, frameworks, and languages used"
    depends_on: [structure]

  - id: dependencies
    description: "Map dependencies"
    prompt: "Analyze package dependencies and imports"
    depends_on: [structure]

  # Wave 3: Depends on both structure and tech
  - id: architecture
    description: "Analyze architecture patterns"
    prompt: "Identify architectural patterns and design decisions"
    depends_on: [structure, tech-stack]

  - id: workflows
    description: "Trace workflows"
    prompt: "Trace request flows and data processing pipelines"
    depends_on: [structure, dependencies]

  # Wave 4: Final synthesis
  - id: synthesis
    description: "Synthesize findings"
    prompt: "Combine all findings into comprehensive report"
    depends_on: [architecture, workflows]
```

**Execution plan:**
```
Wave 1: [structure]                          (1 task)
Wave 2: [tech-stack, dependencies]           (2 tasks in parallel)
Wave 3: [architecture, workflows]            (2 tasks in parallel)
Wave 4: [synthesis]                          (1 task)
```

### Scenario 2: Multi-Stage Verification

```yaml
tasks:
  # Wave 1: Domain analysis
  - id: security-analysis
    prompt: "Analyze security aspects"
    depends_on: []

  - id: performance-analysis
    prompt: "Analyze performance aspects"
    depends_on: []

  # Wave 2: Integration analysis (needs domain findings)
  - id: integration-check
    prompt: "Check integration impact using domain findings"
    depends_on: [security-analysis, performance-analysis]

  - id: devils-advocate
    prompt: "Challenge assumptions from domain analysis"
    depends_on: [security-analysis, performance-analysis]

  # Wave 3: Final review (needs everything)
  - id: third-party-review
    prompt: "Fresh eyes review of all analysis"
    depends_on: [integration-check, devils-advocate]
```

---

## Error Handling

### Cycle Detection Error

```
❌ ERROR: Circular dependency detected!

Dependency cycle found:
  task-A depends on task-B
  task-B depends on task-C
  task-C depends on task-A  ← Creates cycle!

This creates an infinite loop. Please restructure your dependencies.

Suggestion: Remove one of these dependencies to break the cycle.
```

### Missing Dependency Error

```
❌ ERROR: Invalid dependency reference!

Task "integration-check" depends on "domain-analysis"
But task "domain-analysis" does not exist.

Available tasks: [security-analysis, performance-analysis, integration-check]

Did you mean: "security-analysis"?
```

### Empty Wave Error

```
⚠️ WARNING: No tasks ready to execute!

All remaining tasks have unmet dependencies.
This usually indicates a cycle or missing task.

Remaining tasks: [task-7, task-9]
Waiting for: [task-3] which is blocked by [task-5]
```

---

## Best Practices

### 1. Minimize Critical Path

The critical path is the longest dependency chain. Minimize it:

```yaml
# ❌ Bad: Long critical path
task-1 → task-2 → task-3 → task-4 → task-5  (5 waves)

# ✅ Good: Shorter critical path
Wave 1: [task-1]
Wave 2: [task-2, task-3, task-4]  # Parallel
Wave 3: [task-5]                   (3 waves)
```

### 2. Balance Wave Sizes

Avoid waves with very different task counts:

```yaml
# ⚠️ Suboptimal: Unbalanced waves
Wave 1: [task-1]                    # 1 task
Wave 2: [task-2, task-3, ..., task-10]  # 9 tasks
Wave 3: [task-11]                   # 1 task

# ✅ Better: Balanced waves
Wave 1: [task-1, task-2, task-3]    # 3 tasks
Wave 2: [task-4, task-5, task-6]    # 3 tasks
Wave 3: [task-7, task-8]            # 2 tasks
```

### 3. Declare Only Necessary Dependencies

Don't over-constrain:

```yaml
# ❌ Bad: Unnecessary dependencies
- id: task-C
  depends_on: [task-A, task-B]  # If task-C only needs task-A

# ✅ Good: Minimal dependencies
- id: task-C
  depends_on: [task-A]  # Only declare what's actually needed
```

### 4. Group Related Tasks

Keep related tasks in same wave when possible:

```yaml
# ✅ Good: Related analysis grouped
Wave 1:
  - security-analysis
  - accessibility-analysis
  - performance-analysis

Wave 2:
  - integration-check  # Uses all Wave 1 results
```

---

## Output Format

Save execution report to `.outputs/workflow/`:

```
.outputs/workflow/
├── YYYYMMDD-HHMMSS-workflow-execution.md
└── YYYYMMDD-HHMMSS-workflow-execution.json
```

**No symlinks.** To find the latest artifact:
```bash
ls -t .outputs/workflow/ | head -1
```

JSON format follows schema in `schemas/workflow-execution-schema.json`

---

## Notes

- **Parallelization speedup** is limited by critical path length
- **Wave count** = length of longest dependency chain
- **Max parallelism** = size of largest wave
- **Cycle detection** is O(V + E) using DFS
- **Topological sort** is O(V + E) using Kahn's algorithm
- **Failure handling** can be configured per-workflow
