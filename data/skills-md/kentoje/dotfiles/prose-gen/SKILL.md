---
name: prose-gen
description: >
  Generate valid OpenProse workflow code from plain English descriptions.
  Use when the user wants to create multi-agent workflows, orchestrate
  sessions, or automate tasks using the OpenProse language.
user-invocable: true
---

Generate valid OpenProse code from the user's plain English description.

## Your Task

1. Understand what the user wants to accomplish
2. Generate valid OpenProse code following the syntax below
3. Output the code in a fenced code block with `prose` language tag
4. Suggest a filename (e.g., `workflow.prose`)
5. Explain how to run it: `prose run <filename>`

## OpenProse Syntax Reference

### Comments

```prose
# This is a comment
session "Hello"  # Inline comment
```

### Strings

```prose
"Single line string"
"""
Multi-line string
preserves whitespace
"""
"Hello {name}"  # Interpolation with {varname}
```

### Agent Definitions

```prose
agent name:
  model: sonnet          # sonnet, opus, or haiku
  prompt: "System prompt"
  persist: true          # true, project, or path string
  skills: ["skill1"]
  permissions:
    read: ["*.md"]
    write: ["output/"]
    bash: deny           # allow, deny, or prompt
    network: allow
```

### Session Statements

```prose
# Simple session
session "Do something"

# Session with agent
session: agentName
  prompt: "Override prompt"
  model: opus
  context: previousResult
  retry: 3
  backoff: exponential
```

### Variables

```prose
let result = session "Get data"        # Mutable
const config = session "Get config"    # Immutable
result = session "Update"              # Reassign let only

# Context passing
session "Use previous"
  context: result                      # Single
  context: [a, b, c]                   # Multiple
  context: { a, b, c }                 # Object shorthand
```

### Composition Blocks

```prose
# Sequential block
do:
  session "First"
  session "Second"

# Named block (reusable)
block review-pipeline:
  session "Review"
  session "Fix"

do review-pipeline  # Invoke

# Block with parameters
block process(item, mode):
  session "Process {item} in {mode} mode"

do process("data.csv", "strict")

# Inline sequence
session "A" -> session "B" -> session "C"
```

### Parallel Blocks

```prose
parallel:
  a = session "Task A"
  b = session "Task B"

session "Combine"
  context: { a, b }

# Join strategies
parallel ("first"):      # Race - first wins
parallel ("any"):        # First success
parallel ("any", count: 2):  # Wait for 2

# Failure policies
parallel (on-fail: "continue"):   # Let all complete
parallel (on-fail: "ignore"):     # Ignore failures
```

### Fixed Loops

```prose
# Repeat N times
repeat 3:
  session "Generate idea"

repeat 5 as i:
  session "Process item {i}"

# For-each
for item in items:
  session "Process"
    context: item

for item, i in items:
  session "Process {i}"
    context: item

# Parallel for-each (fan-out)
parallel for topic in ["AI", "ML", "DL"]:
  session "Research"
    context: topic
```

### Unbounded Loops

Use `**...**` discretion markers for AI-evaluated conditions:

```prose
loop (max: 50):
  session "Process next"

loop until **the task is complete** (max: 10):
  session "Continue working"

loop while **there are items to process** (max: 20) as i:
  session "Process item {i}"
```

### Pipeline Operations

```prose
let items = ["a", "b", "c"]

# Map
let results = items | map:
  session "Transform"
    context: item

# Filter
let filtered = items | filter:
  session "Keep this? yes/no"
    context: item

# Reduce
let combined = items | reduce(acc, item):
  session "Combine"
    context: [acc, item]

# Parallel map
let fast = items | pmap:
  session "Process in parallel"
    context: item

# Chaining
let final = items
  | filter:
      session "Keep?"
        context: item
  | map:
      session "Transform"
        context: item
```

### Error Handling

```prose
try:
  session "Risky operation"
catch as err:
  session "Handle error"
    context: err
finally:
  session "Always cleanup"

# Throw
throw "Something went wrong"
throw  # Re-raise in catch block

# Retry
session "Flaky API"
  retry: 3
  backoff: exponential  # none, linear, exponential
```

### Choice Blocks

```prose
choice **which approach is best**:
  option "Quick fix":
    session "Apply quick fix"
  option "Full refactor":
    session "Do full refactor"
```

### Conditionals

```prose
if **code has security issues**:
  session "Fix security"
elif **code has performance issues**:
  session "Optimize"
else:
  session "Proceed"
```

### Program Composition

```prose
# Import programs
use "@handle/slug"
use "@handle/slug" as alias

# Inputs and outputs
input topic: "The subject to research"

let result = session "Research {topic}"
output findings = session "Synthesize"
  context: result

# Call imported program
let data = research(topic: "quantum computing")
session "Use findings"
  context: data.findings
```

### Persistent Agents

```prose
agent captain:
  model: opus
  persist: true           # Dies with execution
  persist: project        # Survives across runs
  persist: ".prose/custom/"  # Custom path

# First call creates memory
session: captain
  prompt: "Review plan"

# Resume continues with memory
resume: captain
  prompt: "Continue review"
```

## Example Patterns

### Research Pipeline

```prose
agent researcher:
  model: sonnet
  prompt: "You research topics thoroughly"

agent writer:
  model: opus
  prompt: "You write clear documentation"

let research = session: researcher
  prompt: "Research quantum computing"

session: writer
  prompt: "Write summary"
  context: research
```

### Parallel Review

```prose
parallel:
  security = session "Security review"
  perf = session "Performance review"
  style = session "Style review"

session "Synthesize reviews"
  context: { security, perf, style }
```

### Iterative Improvement

```prose
let draft = session "Write initial draft"

loop until **draft is polished** (max: 5):
  draft = session "Improve draft"
    context: draft

session "Finalize"
  context: draft
```

## Output Format

Always output:

1. The `.prose` code in a fenced code block
2. Suggested filename
3. How to run: `prose run <filename>`

Ask clarifying questions if the request is ambiguous.
