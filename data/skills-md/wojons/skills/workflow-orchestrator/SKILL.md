---
name: workflow-orchestrator
description: Build and orchestrate AI-driven development workflows (Ralph loops) that iterate until success using configurable patterns and multi-agent coordination
license: MIT
compatibility: opencode
metadata:
  audience: developers, AI agents, team leads
  category: workflow
---

# Workflow Orchestrator

Design, configure, and execute AI-driven development workflows (Ralph loops) that iterate until tasks complete successfully using configurable patterns, multi-agent coordination, and intelligent stop conditions.

## When to use me

Use this skill when:
- Building complex features requiring multiple AI agent passes
- Implementing automated development workflows with verification steps
- Coordinating parallel AI agents for different aspects of a task
- Creating self-correcting loops that iterate until success criteria met
- Designing workflow patterns for team consistency
- Need to orchestrate multiple AI agents in sequence or parallel
- Want to implement "Ralph loops" (AI workflows that feed failures back into input)

## What I do

### 1. Workflow Pattern Selection
- **Analyze task requirements** to recommend optimal workflow patterns
- **Match complexity levels** with appropriate workflow types
- **Compare trade-offs** between speed, cost, control, and quality
- **Select from proven patterns** (simple, verified, planned, parallel, custom)

### 2. Configuration Generation
- **Generate YAML configurations** for workflow execution
- **Define agent roles and responsibilities** (builder, verifier, planner, merger)
- **Set success criteria and stop conditions** for automated completion
- **Configure iteration limits and escape hatches** for safety
- **Specify tool permissions and model selections** per agent

### 3. Multi-Agent Coordination
- **Sequence agents** for linear workflows (build → verify → plan)
- **Parallelize agents** for concurrent execution
- **Merge results** from multiple agent perspectives
- **Handle failures and retries** with intelligent routing
- **Implement steering patterns** (linear, conditional, parallel, unblocking)

### 4. Ralph Loop Implementation
- **Create feedback loops** where failures inform subsequent attempts
- **Implement stop hooks** to detect completion promises (`<promise>...</promise>`)
- **Build contextual pressure cookers** that iterate toward success
- **Manage iteration limits** to prevent infinite loops
- **Track progress and telemetry** across workflow executions

### 5. Integration & Tooling
- **OpenCode server integration** for HTTP-based workflows
- **SSE event streaming** for real-time monitoring
- **TUI/UI dashboards** for workflow visualization
- **Git hook integration** for automated quality gates
- **Cost tracking and budgeting** across agent executions

## Workflow Patterns

### Pattern 1: Builder Only (Simple)
```
Single Agent → Build → [Success?] → Done
                     ↓ No
                     Retry (max iterations)
```

**Best for**: Simple tasks, bug fixes, small features  
**Agents**: 1 (builder)  
**Control**: Low, Cost: Low, Speed: High

### Pattern 2: Build + Verify
```
Builder → [Success?] → Verifier → [Pass?] → Done
           ↓ No                 ↓ No
           Retry                Feedback → Builder
```

**Best for**: Quality-critical work, production code  
**Agents**: 2 (builder, verifier)  
**Control**: Medium, Cost: Medium, Speed: Medium

### Pattern 3: Build + Verify + Plan
```
Planner → Builder → Verifier → [Pass?] → Done
                            ↓ No
                            Feedback → Planner
```

**Best for**: Complex features, architectural changes  
**Agents**: 3+ (planner, builder, verifier)  
**Control**: High, Cost: High, Speed: Low

### Pattern 4: Multi-Agent Pipeline
```
[Agent A] → [Merge]
[Agent B] → [Results] → Done
[Agent C] → 
```

**Best for**: Multiple perspectives, comprehensive solutions  
**Agents**: 3+ parallel agents  
**Control**: High, Cost: High, Speed: Medium

### Pattern 5: Custom Workflow
User-defined sequence of agents with custom routing logic.

## Configuration Examples

### Simple Builder Loop (builder-only.yaml):
```yaml
workflow:
  version: "1.0"
  settings:
    max_iterations: 20
    stop_on_success: true
    
  loop:
    agent: builder
    task: "Build the requested feature"
    stop_condition: "<promise>BUILD_COMPLETE</promise>"
    tools:
      read: true
      write: true
      edit: true
      bash: true
```

### Build + Verify Loop:
```yaml
workflow:
  version: "1.0"
  
  agents:
    builder:
      role: "Build the feature"
      stop_condition: "<promise>BUILT</promise>"
    
    verifier:
      role: "Verify quality and correctness"
      stop_condition: "<promise>VERIFIED</promise>"
  
  sequence:
    - agent: builder
    - agent: verifier
      condition: "builder.stop_condition met"
    
  feedback:
    verifier_failed: "builder"
```

### Multi-Agent Parallel Workflow:
```yaml
workflow:
  version: "1.0"
  
  agents:
    frontend_specialist:
      role: "Implement UI components"
    
    backend_specialist:
      role: "Implement API and business logic"
    
    qa_specialist:
      role: "Test implementation"
  
  parallel:
    - frontend_specialist
    - backend_specialist
  
  sequence:
    - parallel: [frontend_specialist, backend_specialist]
    - agent: qa_specialist
  
  merger:
    agent: lead_developer
    task: "Merge parallel work into cohesive solution"
```

## Examples

```bash
# Analyze project and suggest workflow pattern
npm run workflow:analyze -- --task "Add user authentication"

# Generate workflow configuration
npm run workflow:generate -- --pattern build-verify --output auth-workflow.yaml

# Execute workflow
npm run workflow:execute -- --config auth-workflow.yaml --max-iterations 20

# Monitor running workflow
npm run workflow:monitor -- --workflow-id auth-123

# List available patterns
npm run workflow:patterns -- --list

# Create custom workflow from template
npm run workflow:custom -- --agents "planner,builder,verifier" --sequence "sequential"
```

## Output format

### Workflow Analysis Report:
```
Workflow Orchestrator Analysis
──────────────────────────────
Task: Add user authentication to React/Node.js app
Date: 2026-02-26

Recommended Pattern: Build + Verify + Plan
Rationale: Authentication requires security review, testing, and planning

Pattern Comparison:
┌─────────────────┬─────────┬─────────┬─────────┬──────────┐
│ Pattern         │ Control │ Cost   │ Speed   │ Quality  │
├─────────────────┼─────────┼─────────┼─────────┼──────────┤
│ Builder Only    │ Low     │ $      │ Fast    │ Medium   │
│ Build + Verify  │ Medium  │ $$     │ Medium  │ High     │
│ Build+Verify+Plan│ High    │ $$$    │ Slow    │ Highest  │
│ Multi-Agent     │ Highest │ $$$$   │ Medium  │ Highest  │
└─────────────────┴─────────┴─────────┴─────────┴──────────┘

Agents Required:
1. Planner (architect authentication flow)
2. Builder (implement components and API)
3. Verifier (security and testing specialist)

Estimated:
- Iterations: 3-5
- Cost: $15-25
- Time: 45-60 minutes
- Success Probability: 85%

Configuration Generated: auth-workflow.yaml
```

### Workflow Configuration:
```yaml
workflow:
  name: "user-authentication"
  version: "1.1"
  created: "2026-02-26T18:00:00Z"
  
  settings:
    max_iterations: 20
    stop_on_success: true
    escape_hatch: true
    cost_limit: 50.00
    time_limit_minutes: 120
    
  agents:
    planner:
      model: "anthropic/claude-sonnet-4-20250514"
      temperature: 0.3
      role: "Plan authentication architecture"
      tools: ["read", "write", "question"]
      stop_condition: "<promise>PLAN_COMPLETE</promise>"
      
    builder:
      model: "anthropic/claude-sonnet-4-20250514"
      temperature: 0.7
      role: "Implement authentication components"
      tools: ["read", "write", "edit", "bash", "webfetch"]
      stop_condition: "<promise>BUILD_COMPLETE</promise>"
      
    verifier:
      model: "anthropic/claude-sonnet-4-20250514"
      temperature: 0.2
      role: "Verify security and functionality"
      tools: ["read", "bash", "question"]
      stop_condition: "<promise>VERIFIED</promise>"
  
  sequence:
    - agent: planner
    - agent: builder
      condition: "planner.stop_condition met"
    - agent: verifier
      condition: "builder.stop_condition met"
  
  feedback:
    verifier_failed:
      target: planner
      message: "Verification failed, replan needed"
      
    builder_stuck:
      target: planner
      message: "Builder stuck, needs guidance"
  
  success_criteria:
    - "All tests pass"
    - "Security review passed"
    - "API endpoints documented"
    - "User stories implemented"
  
  telemetry:
    track_costs: true
    track_iterations: true
    track_duration: true
    dashboard_url: "http://localhost:3000/dashboard"
```

### Workflow Execution Log:
```
Workflow Execution: user-authentication
─────────────────────────────────────
Status: Running
Start Time: 2026-02-26T18:00:00Z
Current Iteration: 3/20
Cost: $8.75
Duration: 25m 30s

Agent Timeline:
00:00:00 - Planner started
00:05:15 - Planner completed: <promise>PLAN_COMPLETE</promise>
00:05:30 - Builder started
00:15:45 - Builder: Created 12 files, 457 lines
00:20:30 - Builder completed: <promise>BUILD_COMPLETE</promise>
00:20:45 - Verifier started
00:25:30 - Verifier: Running security checks

Current Agent: Verifier
Progress: 75%
Estimated Completion: 00:35:00

Success Criteria Status:
✅ Tests passing: 42/42 tests
🔍 Security review: In progress
📚 Documentation: 80% complete
👤 User stories: 3/4 implemented

Next: Verifier completion → Workflow success
```

## Notes

- **Ralph loops work best with clear success criteria** - vague goals lead to infinite loops
- **Start simple** - use Builder Only pattern for small tasks before scaling up
- **Monitor costs** - parallel agents and multiple iterations increase expense
- **Implement escape hatches** - always have manual stop conditions
- **Use stop promises** (`<promise>...</promise>`) for reliable completion detection
- **Consider feedback mechanisms** - failed verification should inform subsequent attempts
- **Balance control vs. autonomy** - more agents = more control but higher cost/complexity
- **Test workflows** with simple tasks before applying to critical work
- **Document patterns** for team consistency and knowledge sharing
- **Review telemetry** to optimize workflow configurations over time