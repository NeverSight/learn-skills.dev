---
name: agentscope-skill
description: This guide covers the design philosophy, core concepts, and practical usage of the AgentScope framework. Use this skill whenever the user wants to do anything with the AgentScope (Python) library. This includes building agent applications using AgentScope, answering questions about AgentScope, looking for guidance on how to use AgentScope, searching for examples or specific information (functions/classes/modules).
version: 0.1.0
---

## Understanding AgentScope
### What is AgentScope?
AgentScope is a production-ready, enterprise-grade open-source framework for building multi-agent applications with large language models. Its functionalities cover:

- **Development**: ReAct agent, context compression, short/long-term memory, tool use, human-in-the-loop, multi-agent orchestration, agent hooks, structured output, planning, integration with MCP, agent skill, LLMs API, voice interaction (TTS/Realtime), RAG
- **Evaluation**: Evaluate multistep agentic applications with statistical analysis
- **Training**: Agentic reinforcement learning
- **Deployment**: Session/state management, sandbox, local/serverless/Kubernetes deployment

### Installation
```bash
pip install agentscope
# or
uv pip install agentscope
```

### Core Concepts
- **Message**: The core abstraction for information exchange between agents. Supports heterogeneous content blocks (text, images, tool calls, tool results).
```python
from agentscope.message import Msg, TextBlock, ImageBlock, URLSource

msg = Msg(
    name="user",
    content=[TextBlock("Hello world"), ImageBlock(type="image", source=URLSource(type="url", url="..."))],
    role="user"
)
```
- **Agent**: LLM-empowered agent that can reason, use tools, and generate responses through iterative thinking and action loops.
- **Toolkit**: Register and manage tools (Python functions, MCP, agent skills) that agents can call.
- **Memory**: Store `Msg` objects as conversation history/context with a marking mechanism for advanced memory management (compression, retrieval).
- **ChatModel**: Unified interface across different providers (OpenAI, Anthropic, DashScope, Ollama, etc.) with support for tool use and streaming.
- **Formatter**: Convert `Msg` objects to LLM API-specific formats. Must be used with the corresponding ChatModel. Supports multi-agent conversations with different agent identifiers.

### Basic Usage Examples
#### Example 1: Simple Chatbot
```python
from agentscope.agent import ReActAgent, UserAgent
from agentscope.model import DashScopeChatModel
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit, execute_python_code, execute_shell_command
import os, asyncio

async def main():
    # Initialize toolkit with tools
    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(execute_shell_command)

    # Create ReActAgent with model, memory, formatter, and toolkit
    agent = ReActAgent(
        name="Friday",
        sys_prompt="You're a helpful assistant named Friday.",
        model=DashScopeChatModel(
            model_name="qwen-max",
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            stream=True,
        ),
        memory=InMemoryMemory(),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
    )

    # Create user agent for terminal input
    user = UserAgent(name="user")

    # Conversation loop
    msg = None
    while True:
        msg = await agent(msg)  # Agent processes and replies
        msg = await user(msg)   # User inputs next message
        if msg.get_text_content() == "exit":
            break

asyncio.run(main())
```

#### Example 2: Multi-Agent Conversation
AgentScope adopts explicit message passing for multi-agent conversations (PyTorch-like dynamic graph), allowing flexible information flow control.

```python
alice, bob, carol, david = ReActAgent(...), ReActAgent(...), ReActAgent(...), ReActAgent(...)

msg_alice = await alice()
msg_bob = await bob(msg_alice)  # Bob receives Alice's message and generate a reply. Alice doesn't receive Bob's message unless explicitly passed back.
msg_carol = await carol(msg_alice)  # Similarly, the agent cannot receive messages from other agents unless explicitly passed.

# Broadcasting with MsgHub, a syntactic sugar for message broadcasting within a group of agents
from agentscope.pipeline import MsgHub

async with MsgHub(
    participants=[alice, bob, carol],
    announcement=Msg("Host", "Let's discuss", "user")
) as hub:
    await alice()  # Bob and Carol receive this
    await bob()    # Alice and Carol receive this

    # Manual broadcast
    await hub.broadcast(Msg("Host", "New topic", "user"))

    # Dynamic participant management
    hub.add(david)
    hub.delete(bob)
```

#### Example 3: Master-Worker Pattern
Wrap worker agents as tools for the master agent.

```python
from agentscope.tool import ToolResponse, Toolkit

async def create_worker(task: str) -> ToolResponse:
    """Create a worker agent for the given task.

    Args:
        task (`str`): The given task, which should be specific and concise.
    """
    task_msg = Msg(name="master", content=task, role="user") # Use the input task or wrap it into a more complex prompt
    worker = ReActAgent(...)
    res = await worker(task_msg)
    return ToolResponse(content=res.content) # Return the worker's response as the tool response

toolkit = Toolkit()
toolkit.register_tool_function(create_worker)
```

## Working with AgentScope
This section provides guidance on how to effectively answer questions about AgentScope or coding with the framework.

### Step 1: Clone the Repository First

**CRITICAL**: Before doing anything else, clone or update the AgentScope repository. The repository contains essential examples and references.

```bash
# Clone into this skill directory so that you can refer to it across different sessions
cd /path/to/this/skill/directory
git clone -b main https://github.com/agentscope-ai/agentscope.git

# Or update if already cloned
cd /path/to/this/skill/directory/agentscope
git pull
```

**Why this matters**: The repository contains working examples, complete API documentation in source code, and implementation patterns that are more reliable than guessing.

### Step 2: Understand the Repository Structure
The cloned repository is organized as follows. Note this may be outdated as the project evolves, you should always check the actual structure after cloning.
```
agentscope/
├── src/agentscope/          # Main library source code
│   ├── agent/               # Agent implementations (ReActAgent, etc.)
│   ├── model/               # LLM API wrappers (OpenAI, Anthropic, DashScope, etc.)
│   ├── formatter/           # Message formatters for different models
│   ├── memory/              # Memory implementations
│   ├── tool/                # Tool management and built-in tools
│   ├── message/             # Msg class and content blocks
│   ├── pipeline/            # Multi-agent orchestration (MsgHub, etc.)
│   ├── session/             # Session/state management
│   ├── mcp/                 # MCP integration
│   ├── rag/                 # RAG functionality
│   ├── realtime/            # Realtime voice interaction
│   ├── tts/                 # Text-to-speech
│   ├── evaluate/            # Evaluation tools
│   └── ...                  # Other modules
│
├── examples/                # Working examples organized by category
│   ├── agent/               # Different agent types
│   │   └── ...
│   ├── workflows/           # Multi-agent workflows
│   │   └── ...
│   ├── functionality/       # Specific features
│   │   └── ...
│   ├── deployment/          # Deployment patterns
│   ├── integration/         # Third-party integrations
│   ├── evaluation/          # Evaluation examples
│   └── game/                # Game examples (e.g., werewolves)
│
├── docs/                    # Documentation
│   ├── tutorial/            # Tutorial markdown files
│   ├── changelog.md         # Version history
│   └── roadmap.md           # Development roadmap
│
└── tests/                   # Test files
```

### Step 3: Browse Examples by Category

When looking for similar implementations, **browse the examples directory by category** rather than searching by keywords alone:
1. **Start with the category** that matches your use case:
   - Building a specific agent type? → `examples/agent/`
   - Multi-agent system? → `examples/workflows/`
   - Need a specific feature (MCP, RAG, session)? → `examples/functionality/`
   - Deployment patterns? → `examples/deployment/`
2. **List the subdirectories** to see what's available:
   - Use file listing tools to explore directory structure
   - Read directory names to understand what each example covers
3. **Read example files** to understand implementation patterns:
   - Most examples contain a main script and supporting files
   - Look for README files in subdirectories for explanations
4. **Combine with text search** when needed:
   - After identifying relevant directories, search within them for specific patterns
   - Search for class names, method calls, or specific functionality

**Example workflow**:
```
User asks: "Build a FastAPI app with AgentScope"
→ Browse: List files in examples/deployment/
→ Check: Are there any web service examples?
→ Search: Look for "fastapi", "flask", "api", "server" in examples/
→ Read: Found examples and adapt to user's needs
```

## Step 4: Verify Functionality Exists
Before implementing custom solutions, verify if AgentScope already provides the functionality:

1. **List required functionalities** (e.g., session management, MCP integration, RAG)
2. **Check if provided**:
   - Browse `examples` for examples
   - Search tutorial documentation in `docs/tutorial/`
   - Use the provided scripts (see Part 3) to explore API structure
   - Read source code in `src/agentscope/` for implementation details
3. **If not provided**: Check how to customize by reading base classes and inheritance patterns in source code

### Step 5: Make a Plan
Always create a plan before coding:
1. Identify what AgentScope components you'll use
2. Determine what needs custom implementation
3. Outline the architecture and data flow
4. Consider edge cases and error handling

### Step 6: Code with API Reference
When writing code:
1. **Check docstrings and arguments** before using any class/method
   - Read source code files to see signatures and documentation, or
   - Use the provided scripts to view module/class structures
   - **NEVER** make up classes, methods, or arguments
2. **Check parent classes** - A class's functionality includes inherited methods
3. **Manage lifecycle** - Clean up resources when needed (close connections, release memory)

### Common Pitfalls to Avoid
- ❌ Guessing API signatures without checking documentation
- ❌ Implementing features that already exist in AgentScope
- ❌ Mixing incompatible Model and Formatter (e.g., OpenAI model with DashScope formatter)
- ❌ Forgetting to await async agent calls
- ❌ Not checking parent class methods when searching for functionality
- ❌ Searching by keywords only without browsing the organized examples directory structure

## Resources
This section lists all available resources for working with AgentScope.
### Official Documentation
- **[Tutorial](https://agentscope.ai/docs/)**: Comprehensive step-by-step guide covering most functionalities in detail. This is the primary resource for learning AgentScope.

### GitHub Resources
- **[Main Repository](https://github.com/agentscope-ai/agentscope)**: Source code, examples, and documentation
- **[Project Board](https://github.com/orgs/agentscope-ai/projects/2)**: Official development roadmap and task tracking
- **[Design Discussions](https://github.com/agentscope-ai/agentscope/discussions/categories/agentscope-design-book)**: In-depth explanations about specific modules/functions/components

### Repository Structure
When the repository is cloned locally, the following structure is available for reference:
- **`src/agentscope/`**: Main library source code
  - Read this for API implementation details
  - Check docstrings for parameter descriptions
  - Understand inheritance hierarchies
- **`examples/`**: Working examples demonstrating features
  - Start here when building similar applications
  - Examples cover: basic agents, multi-agent systems, tool usage, deployment patterns
- **`docs/tutorial/`**: Tutorial documentation source files
  - Markdown files explaining concepts and usage
  - More detailed than README files

### Scripts
Located in `scripts/` directory of this skill.

- `view_pypi_latest_version.sh`: View the latest version of AgentScope on PyPI.
```bash
cd /path/to/this/skill/directory/scripts/
bash view_pypi_latest_version.sh
```
- `view_module_signature.py`: Explore the structure of AgentScope modules, classes, and methods.
**Search strategy**: Use deep-first search - start broad, then narrow down:
1. `agentscope` → see all submodules
2. `agentscope.agent` → see agent-related classes
3. `agentscope.agent.ReActAgent` → see specific class methods

```bash
cd /path/to/this/skill/directory/scripts/
# View top-level module
python view_module_signature.py --module agentscope
# View specific submodule
python view_module_signature.py --module agentscope.agent
# View specific class
python view_module_signature.py --module agentscope.agent.ReActAgent
```

## Reference
Located in `references/` directory of this skill.

- **`multi_agent_orchestration.md`**: Multi-agent orchestration concepts and implementation
- **`deployment_guide.md`**: Deployment patterns and best practices
