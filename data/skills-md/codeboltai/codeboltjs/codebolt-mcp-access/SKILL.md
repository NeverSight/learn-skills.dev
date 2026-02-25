---
name: codebolt-mcp-access
description: Core skill for Codebolt agents to interact with the Codebolt MCP (Model Context Protocol) API. Use when agents need to execute tools for file operations, git, browser automation, terminal, memory, orchestration, planning, testing, collaboration, or any Codebolt platform functionality. Triggers on requests involving codebolt.tools.executeTool(), file system operations, git commands, browser control, agent orchestration, task management, or any MCP namespace operations.
---

# Codebolt MCP Access

Execute Codebolt platform tools via the MCP interface.

## Quick Start

```javascript
const result = await codebolt.tools.executeTool(
  "codebolt.<namespace>",
  "<tool_name>",
  { param1: "value1", param2: "value2" }
);
```

## Tool Categories

### Core Tools
| Namespace | Use Case |
|-----------|----------|
| `codebolt.fs` | Read, write, edit files |
| `codebolt.git` | Version control operations |
| `codebolt.browser` | Web automation |
| `codebolt.terminal` | Command execution |
| `codebolt.search` | Code/file search (glob, grep, semantic) |

### Data & State
| Namespace | Use Case |
|-----------|----------|
| `codebolt.memory` | Persistent data storage (JSON, markdown, episodic) |
| `codebolt.state` | Agent and project state management |
| `codebolt.rag` | RAG indexes and document retrieval |
| `codebolt.vector` | Vector database operations |
| `codebolt.knowledge` | Knowledge graph management |

### Agent & Orchestration
| Namespace | Use Case |
|-----------|----------|
| `codebolt.orchestration` | Tasks, agents, threads |
| `codebolt.agent` | Agent lifecycle management |
| `codebolt.task` | Task CRUD operations |
| `codebolt.job` | Work items with dependencies |
| `codebolt.capability` | Skills and powers |

### Project Management
| Namespace | Use Case |
|-----------|----------|
| `codebolt.planning` | Roadmaps and action plans |
| `codebolt.actionPlan` | Action plan management |
| `codebolt.actionBlock` | ActionBlock management |
| `codebolt.roadmap` | Roadmap management |
| `codebolt.requirementPlan` | Requirements planning |
| `codebolt.autoTesting` | Automated testing |
| `codebolt.codemap` | Code structure visualization |
| `codebolt.calendar` | Events and scheduling |
| `codebolt.todo` | Todo list management |
| `codebolt.review` | Code review workflow |
| `codebolt.reviewMergeRequest` | Review merge requests |
| `codebolt.testing` | Test suite management |

### Communication & Collaboration
| Namespace | Use Case |
|-----------|----------|
| `codebolt.chat` | Chat and notifications |
| `codebolt.message` | Message handling |
| `codebolt.notification` | Event notifications |
| `codebolt.collaboration` | Feedback and deliberation |
| `codebolt.swarm` | Swarm/team/role management |
| `codebolt.agentDeliberation` | Multi-agent deliberation |
| `codebolt.agentPortfolio` | Agent portfolio/reputation |
| `codebolt.groupFeedback` | Group feedback sessions |
| `codebolt.mail` | Agent mail/messaging |
| `codebolt.config` | MCP server configuration |

### Memory & Knowledge
| Namespace | Use Case |
|-----------|----------|
| `codebolt.memory` | Persistent data storage |
| `codebolt.episodicMemory` | Episode-based memory |
| `codebolt.persistentMemory` | Long-term memory pipelines |
| `codebolt.dbmemory` | Database memory |
| `codebolt.eventLog` | Event logging |
| `codebolt.state` | Agent and project state |
| `codebolt.rag` | RAG indexes |
| `codebolt.vector` | Vector database |
| `codebolt.knowledge` | Knowledge graph |

### Project & Code
| Namespace | Use Case |
|-----------|----------|
| `codebolt.project` | Project info and settings |
| `codebolt.projectStructure` | Project structure management |
| `codebolt.crawler` | Web crawler |
| `codebolt.codebase` | Semantic code search |
| `codebolt.fileIntent` | File intent management |

### Utilities
| Namespace | Use Case |
|-----------|----------|
| `codebolt.code_utils` | AST and pattern matching |
| `codebolt.tokenizer` | Text tokenization |
| `codebolt.debug` | Debugging utilities |
| `codebolt.kvStore` | Key-value storage |
| `codebolt.outputParsers` | Output parsing |
| `codebolt.sideExecution` | Isolated code execution |
| `codebolt.userMessageManager` | User message context |
| `codebolt.userMessageUtilities` | Message utilities |
| `codebolt.history` | Chat history summarization |
| `codebolt.event` | Background agent events |
| `codebolt.hook` | Event-driven hooks |
| `codebolt.orchestrator` | Orchestrator lifecycle |
| `codebolt.contextRuleEngine` | Conditional memory rules |
| `codebolt.llm` | LLM inference |
| `codebolt.admin` | Admin operations |
| `codebolt.mcp` | MCP server management |

## Reference Files

Load the reference file for detailed parameter tables:

### Core
| Reference | Namespace |
|-----------|-----------|
| [fs.md](references/fs.md) | `codebolt.fs` |
| [git.md](references/git.md) | `codebolt.git` |
| [browser.md](references/browser.md) | `codebolt.browser` |
| [terminal.md](references/terminal.md) | `codebolt.terminal` |
| [search.md](references/search.md) | `codebolt.search` |

### Data & State
| Reference | Namespace |
|-----------|-----------|
| [memory.md](references/memory.md) | `codebolt.memory` |
| [state.md](references/state.md) | `codebolt.state` |
| [rag.md](references/rag.md) | `codebolt.rag` |
| [knowledge.md](references/knowledge.md) | `codebolt.knowledge` |
| [context.md](references/context.md) | `codebolt.context` |
| [codebase.md](references/codebase.md) | `codebolt.codebase` |

### Agent & Orchestration
| Reference | Namespace |
|-----------|-----------|
| [orchestration.md](references/orchestration.md) | `codebolt.orchestration` |
| [agent.md](references/agent.md) | `codebolt.agent` |
| [job.md](references/job.md) | `codebolt.job` |
| [capability.md](references/capability.md) | `codebolt.capability` |
| [admin.md](references/admin.md) | `codebolt.admin` |
| [llm.md](references/llm.md) | `codebolt.llm` |

### Project Management
| Reference | Namespace |
|-----------|-----------|
| [planning.md](references/planning.md) | `codebolt.planning` |
| [calendar.md](references/calendar.md) | `codebolt.calendar` |
| [todo.md](references/todo.md) | `codebolt.todo` |
| [review.md](references/review.md) | `codebolt.review` |
| [testing.md](references/testing.md) | `codebolt.testing` |
| [project.md](references/project.md) | `codebolt.project` |

### Communication
| Reference | Namespace |
|-----------|-----------|
| [chat.md](references/chat.md) | `codebolt.chat` |
| [collaboration.md](references/collaboration.md) | `codebolt.collaboration` |
| [mcp_servers.md](references/mcp_servers.md) | `codebolt.mcp` |

### Multi-Agent & Collaboration
| Reference | Namespace |
|-----------|-----------|
| [swarm.md](references/swarm.md) | `codebolt.swarm` |
| [agentDeliberation.md](references/agentDeliberation.md) | `codebolt.agentDeliberation` |
| [agentPortfolio.md](references/agentPortfolio.md) | `codebolt.agentPortfolio` |
| [groupFeedback.md](references/groupFeedback.md) | `codebolt.groupFeedback` |
| [mail.md](references/mail.md) | `codebolt.mail` |
| [collaboration.md](references/collaboration.md) | `codebolt.collaboration` |

### Planning & Project Management
| Reference | Namespace |
|-----------|-----------|
| [actionPlan.md](references/actionPlan.md) | `codebolt.actionPlan` |
| [actionBlock.md](references/actionBlock.md) | `codebolt.actionBlock` |
| [roadmap.md](references/roadmap.md) | `codebolt.roadmap` |
| [requirementPlan.md](references/requirementPlan.md) | `codebolt.requirementPlan` |
| [autoTesting.md](references/autoTesting.md) | `codebolt.autotesting` |
| [codemap.md](references/codemap.md) | `codebolt.codemap` |
| [reviewMergeRequest.md](references/reviewMergeRequest.md) | `codebolt.reviewMergeRequest` |

### Memory & Knowledge
| Reference | Namespace |
|-----------|-----------|
| [episodicMemory.md](references/episodicMemory.md) | `codebolt.episodicMemory` |
| [persistentMemory.md](references/persistentMemory.md) | `codebolt.persistentMemory` |
| [dbmemory.md](references/dbmemory.md) | `codebolt.dbmemory` |
| [eventLog.md](references/eventLog.md) | `codebolt.eventLog` |

### Project & Code
| Reference | Namespace |
|-----------|-----------|
| [projectStructure.md](references/projectStructure.md) | `codebolt.projectStructure` |
| [crawler.md](references/crawler.md) | `codebolt.crawler` |
| [hook.md](references/hook.md) | `codebolt.hook` |
| [orchestrator.md](references/orchestrator.md) | `codebolt.orchestrator` |
| [contextRuleEngine.md](references/contextRuleEngine.md) | `codebolt.contextRuleEngine` |

### Utilities
| Reference | Namespace |
|-----------|-----------|
| [kvStore.md](references/kvStore.md) | `codebolt.kvStore` |
| [outputParsers.md](references/outputParsers.md) | `codebolt.outputparsers` |
| [sideExecution.md](references/sideExecution.md) | `codebolt.sideExecution` |
| [userMessageManager.md](references/userMessageManager.md) | `codebolt.userMessageManager` |
| [userMessageUtilities.md](references/userMessageUtilities.md) | `codebolt.userMessageUtilities` |
| [history.md](references/history.md) | `codebolt.history` |
| [codeboltEvent.md](references/codeboltEvent.md) | `codebolt.event` |
| [vector.md](references/vector.md) | `codebolt.vector` |
| [tokenizer.md](references/tokenizer.md) | `codebolt.tokenizer` |
| [code_utils.md](references/code_utils.md) | `codebolt.code_utils` |
| [debug.md](references/debug.md) | `codebolt.debug` |
| [notification.md](references/notification.md) | `codebolt.notification` |
| [message.md](references/message.md) | `codebolt.message` |
| [config.md](references/config.md) | `codebolt.config` |
| [task.md](references/task.md) | `codebolt.task` |
| [problem.md](references/problem.md) | `codebolt.problem` |

## Common Patterns

### Read then Edit
```javascript
// 1. Read file first
const content = await codebolt.tools.executeTool("codebolt.fs", "read_file", {
  absolute_path: "/path/to/file.js"
});

// 2. Edit with old_string/new_string
await codebolt.tools.executeTool("codebolt.fs", "edit", {
  absolute_path: "/path/to/file.js",
  old_string: "original text",
  new_string: "replacement text"
});
```

### Search then Act
```javascript
// 1. Search for files
const files = await codebolt.tools.executeTool("codebolt.search", "glob", {
  pattern: "**/*.ts"
});

// 2. Search content
const matches = await codebolt.tools.executeTool("codebolt.search", "grep", {
  pattern: "function\\s+\\w+",
  path: "./src"
});
```

### Multi-Agent Task
```javascript
// 1. Find suitable agent
const agents = await codebolt.tools.executeTool("codebolt.orchestration", "agent_find", {
  task: "Write unit tests"
});

// 2. Create and assign task
const task = await codebolt.tools.executeTool("codebolt.orchestration", "task_create", {
  title: "Write tests for auth module"
});

// 3. Execute with agent
await codebolt.tools.executeTool("codebolt.orchestration", "task_execute", {
  task_id: task.id,
  agent_id: agents[0].id
});
```
