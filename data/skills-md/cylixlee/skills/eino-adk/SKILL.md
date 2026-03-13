---
name: eino-adk
description: Eino Agent Development Kit development skill. For building AI Agent applications including ChatModelAgent, workflows (Sequential/Parallel/Loop), multi-agent systems (Supervisor/PlanExecute), human-in-the-loop (interruption/approval). Use when users need to create Agents, use Runner for execution, manage tool calls, build multi-agent systems.
---

# Eino ADK Development Guide

## When to Use This Skill

Use this skill when:
- User needs to build AI Agent applications
- User asks how to use Eino ADK
- User needs to implement multi-agent systems, workflows, human-in-the-loop
- User wants to understand core concepts like Agent, Runner, Tool

## Quick Start

### Step 1: Import Required Packages

```go
import (
    "context"
    "errors"
    "fmt"
    "io"

    "github.com/cloudwego/eino/adk"
    "github.com/cloudwego/eino/adk/prebuilt/planexecute"
    "github.com/cloudwego/eino/adk/prebuilt/supervisor"
    "github.com/cloudwego/eino/components/model"
    "github.com/cloudwego/eino/components/tool"
    "github.com/cloudwego/eino/schema"
)
```

### Step 2: Create ChatModelAgent

```go
agent, err := adk.NewChatModelAgent(ctx, &adk.ChatModelAgentConfig{
    Name:        "my_agent",
    Description: "An agent that helps with tasks",
    Instruction: "You are a helpful assistant.",
    Model:       chatModel, // model.ToolCallingChatModel
    ToolsConfig: adk.ToolsConfig{
        Tools: []tool.BaseTool{myTool},
    },
})
```

### Step 3: Create Runner and Execute

```go
runner := adk.NewRunner(ctx, adk.RunnerConfig{
    Agent:           agent,
    EnableStreaming: true,
})

events := runner.Run(ctx, []schema.Message{
    schema.UserMessage("Hello!"),
})

for event, ok := events.Next(); ok; event, ok = events.Next() {
    if event.Output != nil && event.Output.MessageOutput != nil {
        if stream := event.Output.MessageOutput.MessageStream; stream != nil {
            for {
                chunk, err := stream.Recv()
                if errors.Is(err, io.EOF) {
                    break
                }
                if err != nil {
                    // handle error
                    break
                }
                fmt.Print(chunk.Content)
            }
        }
    }
}
```

Note: MessageStream is automatically closed by ADK, no manual cleanup required.

## Core Workflow

### Basic Execution Flow

1. **Create Agent** - Use `NewChatModelAgent` or prebuilt agents
2. **Create Runner** - Use `NewRunner` to wrap the Agent
3. **Execute** - Call `runner.Run()` or `runner.Query()`
4. **Process Events** - Iterate `AsyncIterator[*AgentEvent]` to handle output

### Key Interfaces

| Interface  | Location                                                   | Description           |
| ---------- | ---------------------------------------------------------- | --------------------- |
| Agent      | [references/core-concepts.md](references/core-concepts.md) | Core Agent interface  |
| Runner     | [references/core-concepts.md](references/core-concepts.md) | Execution entry point |
| AgentEvent | [references/core-concepts.md](references/core-concepts.md) | Event stream          |
| Session    | [references/core-concepts.md](references/core-concepts.md) | Session state         |

## Common Patterns

### 1. Basic Agent

See [examples.md](references/examples.md#hello-world)

```go
agent, _ := adk.NewChatModelAgent(ctx, &adk.ChatModelAgentConfig{...})
runner := adk.NewRunner(ctx, adk.RunnerConfig{
    Agent:           agent,
    EnableStreaming: true,
})
events := runner.Query(ctx, "Hello!")

for event, ok := events.Next(); ok; event, ok = events.Next() {
    if event.Output != nil && event.Output.MessageOutput != nil {
        if stream := event.Output.MessageOutput.MessageStream; stream != nil {
            for {
                chunk, err := stream.Recv()
                if errors.Is(err, io.EOF) {
                    break
                }
                if err != nil {
                    // handle error
                    break
                }
                fmt.Print(chunk.Content)
            }
        }
    }
}
```

### 2. Workflow Agent

See [examples.md](references/examples.md#workflow)

```go
// Sequential - executes sub-agents in order
agent := adk.NewSequentialAgent(ctx, &adk.SequentialAgentConfig{
    SubAgents: []adk.Agent{agent1, agent2},
})

// Parallel - executes sub-agents concurrently
agent := adk.NewParallelAgent(ctx, &adk.ParallelAgentConfig{
    SubAgents: []adk.Agent{agent1, agent2},
})

// Loop - iterates until condition met
agent := adk.NewLoopAgent(ctx, &adk.LoopAgentConfig{
    SubAgents:     []adk.Agent{agent1},
    MaxIterations: 5,
})
```

### 3. Multi-Agent Systems

See [examples.md](references/examples.md#multi-agent)

```go
// Supervisor pattern
supervisor := supervisor.New(ctx, &supervisor.Config{
    Supervisor: supervisorAgent,
    SubAgents:  []adk.Agent{agent1, agent2},
})

// Plan-Execute-Replan pattern
entryAgent := planexecute.New(ctx, &planexecute.Config{
    Planner:   planAgent,
    Executor:  execAgent,
    Replanner: replanAgent,
})
```

### 4. Agent as Tool

See [examples.md](references/examples.md#agent-tool)

```go
agentTool := adk.NewAgentTool(ctx, subAgent,
    adk.WithFullChatHistoryAsInput(),
)
```

### 5. Interruption and Resume

See [examples.md](references/examples.md#human-in-the-loop)

```go
// Trigger interruption (in tool's InvokableRun method)
err := adk.StatefulInterrupt(ctx, &ReviewInfo{...}, args)
return "", err

// Resume execution
iter, _ := runner.Resume(ctx, checkpointID)
```

### 6. Session Values

```go
// Store
adk.AddSessionValue(ctx, "key", value)

// Retrieve
value, _ := adk.GetSessionValue(ctx, "key")
```

## Configuration

Key configuration options in [configuration.md](references/configuration.md):
- ChatModelAgentConfig
- RunnerConfig
- ToolsConfig
- AgentMiddleware

## API Reference

Key APIs in [api-reference.md](references/api-reference.md):
- NewChatModelAgent
- NewRunner
- Run/Query/Resume
- NewAgentTool

## Error Handling

Common error handling:

1. **Tool call failure**: Check tool definition and parameters
2. **Model call failure**: Check Model configuration and API Key
3. **Resume failure**: Verify CheckpointStore and ResumeInfo
4. **Concurrency issues**: Ensure Agent instances are not shared

## References

- [Core Concepts](references/core-concepts.md) - Detailed core concepts
- [API Reference](references/api-reference.md) - API documentation
- [Examples](references/examples.md) - Example scenarios
- [Configuration](references/configuration.md) - Configuration options
