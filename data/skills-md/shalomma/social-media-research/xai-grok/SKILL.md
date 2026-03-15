---
name: xai-grok
description: Use xAI's Grok model with agentic tool calling for X (Twitter) search, web search, code execution, and real-time data access. Invoke when user needs Twitter/X insights, current events, alternative perspectives, or complex multi-step research.
---

# xAI Grok Integration with Agentic Tool Calling

This skill enables Claude to delegate queries to xAI's Grok model with powerful agentic capabilities including real-time X (Twitter) search, web browsing, and code execution.

## When to Use This Skill

Use this skill when:
- User explicitly asks to use Grok or xAI
- User needs **real-time X (Twitter) search** - finding tweets, users, trends
- User requests "another opinion" or "alternative perspective"
- Query requires very recent information or current events
- User wants social media analysis or Twitter/X insights
- Task benefits from Grok's unique training and perspective
- Complex research requiring multiple tools (web search + code + Twitter)

## Core Capabilities

### 1. X (Twitter) Search
- **Semantic and keyword search** across X posts, users, and threads
- **User search** by name or handle
- **Thread fetching** for full conversation context
- **Real-time data** from the X platform

### 2. Web Search
- Real-time search across the internet
- Browse web pages and extract content

### 3. Code Execution
- Write and execute Python code
- Data analysis and complex computations
- Generate visualizations and process data

### 4. Agentic Orchestration
- **Server-side tool calling** - Grok autonomously decides which tools to use
- **Multi-step reasoning** - Combines multiple tools to answer complex queries
- **Streaming mode** - Real-time progress and observability (always used per xAI recommendation)
- **Citations** - Full traceability of information sources

## Usage

The skill uses a modern Typer-based CLI at `.claude/skills/xai-grok/src/grok.py`:

### Basic Usage (X Search + Web Search enabled by default)

```bash
python3 grok.py "Find recent tweets from Israeli tech nano-influencers"
```

### With All Tools Including Code Execution

```bash
python3 grok.py "Analyze tech trends with charts" --enable-code-execution
```

### Get Help

```bash
python grok.py --help
```

### Twitter/X Search Examples

```bash
# Find specific users
python3 grok.py "Who are the top Israeli tech influencers on X?"

# Search for recent tweets
python3 grok.py "Latest tweets about Israeli startups"

# Analyze trends
python3 grok.py "What are Israeli tech companies tweeting about today?"

# Use fast model with custom temperature (short options)
python3 grok.py "Recent AI tweets" -m grok-4-fast-reasoning -t 0.5
```

### Disable Specific Tools

```bash
# Only X search, no web search
python3 grok.py "Find tweets" --disable-web-search

# Only web search, no X search
python3 grok.py "Latest news" --disable-x-search

# No tools (basic chat)
python3 grok.py "Explain AI" --disable-all-tools
```

### Available Options

```bash
--model, -m              # Model selection (default: grok-4)
--temperature, -t        # Temperature for response generation (default: 0.3)
--disable-x-search       # Disable X (Twitter) search (enabled by default)
--disable-web-search     # Disable web search (enabled by default)
--enable-code-execution  # Enable Python code execution (opt-in)
--disable-all-tools      # Disable all tools (basic chat mode)
--show-citations         # Show source URLs (default: enabled)
--no-show-citations      # Hide source URLs
--show-usage             # Show token usage statistics
--show-tool-calls        # Show real-time tool calls
--install-completion     # Install shell completion for the current shell
--show-completion        # Show completion script for customization
```

### Available Grok 4 Models

- `grok-4` - Highest quality model, 256k context [DEFAULT]
- `grok-4-fast-reasoning` - Cost-efficient with reasoning, 2M context
- `grok-4-fast-non-reasoning` - Cost-efficient without reasoning, 2M context

## Requirements

- XAI_API_KEY environment variable in project's .env file

## How It Works

When you invoke this skill with tools enabled, Grok uses **agentic tool calling**:

1. **Analyzes your query** to understand what information is needed
2. **Autonomously selects tools** - decides whether to search X, browse web, execute code, or combine multiple approaches
3. **Executes tools server-side** - no need for you to handle tool responses
4. **Iterates and refines** - uses tool results to make better decisions
5. **Returns comprehensive answer** with citations and sources

This means a single query like "What are Israeli tech companies tweeting about and how does it compare to global trends?" can automatically:
- Search X for Israeli tech company tweets
- Search the web for global tech trends
- Execute Python code to analyze patterns
- Synthesize everything into a comprehensive answer

## Output

The script provides:
- **Streaming responses** with real-time progress
- **Citations** - URLs of all sources Grok used
- **Tool call visibility** - See which tools Grok invoked (optional)
- **Token usage** - Detailed cost tracking (optional)
- **Professional CLI** - Rich formatted help text with boxed sections
- **Shell completion** - Tab completion support for all commands and options

## Notes

- **Typer-powered CLI** provides a modern, user-friendly interface with rich formatting
- Grok responses are clearly indicated in output
- X search provides **real-time data** from the Twitter/X platform
- Citations show full traceability of information sources
- This is a supplementary tool; Claude remains the primary assistant
- API usage incurs costs on the user's xAI account
- **Streaming mode is always used** for agentic workflows (per xAI strong recommendation)
- Image/video understanding is **not supported** in this implementation
