---
name: llm-advisor
description: Consult other LLMs (GPT-5.2, GPT-5, Gemini 3) for second opinions on complex bugs, hard problems, planning, and architecture decisions. Use proactively when stuck for >15 minutes or facing complex debugging. Use when user says "ask Gemini/GPT/Claude about X" or "get a second opinion".
---

# LLM Advisor

Use Simon Willison's `llm` CLI to consult other LLMs for second opinions, alternative perspectives, and expert advice on complex problems.

## When to Use This Skill

### Proactive Use (autonomous)

Use this skill proactively without being asked when:

- **Stuck >15 minutes** on a bug or problem
- **Complex debugging** with unclear root cause
- **Architecture decisions** with significant trade-offs
- **Planning complex features** that need validation
- **Unfamiliar codebase/language** where you need guidance
- **Security-sensitive code** (auth, crypto, input validation)

### On-Demand Use (user requests)

Use when the user says:
- "Ask Gemini/GPT/Claude about X"
- "Get a second opinion on this"
- "What would GPT think about this approach?"
- "Check with another model"

## Prerequisites

### Installation

```bash
# Install llm CLI
brew install llm
# or
pip install llm

# Set up OpenAI API key
llm keys set openai

# Install Gemini plugin (optional)
llm install llm-gemini
llm keys set gemini
```

### Verify Setup

```bash
# Check available models
llm models

# Test a simple prompt
llm "Hello, what model are you?"
```

## Model Selection

Use `reasoning_effort` to control speed vs quality trade-off. Prefer GPT-5.2 for best quality, GPT-5 for cost efficiency.

### OpenAI Models

| Use Case | Model | Command |
|----------|-------|---------|
| Fast/simple | gpt-5 | `llm -m gpt-5 -o reasoning_effort=low "question"` |
| Default | gpt-5 | `llm -m gpt-5 "question"` |
| Complex | gpt-5 | `llm -m gpt-5 -o reasoning_effort=high "question"` |
| Premium fast | gpt-5.2 | `llm -m gpt-5.2 -o reasoning_effort=low "question"` |
| Premium default | gpt-5.2 | `llm -m gpt-5.2 "question"` |
| Premium max | gpt-5.2 | `llm -m gpt-5.2 -o reasoning_effort=high "question"` |

### Google Gemini Models

| Use Case | Model | Command |
|----------|-------|---------|
| Fast general | gemini-3-flash | `llm -m gemini-3-flash "question"` |
| Fast + thinking | gemini-3-flash | `llm -m gemini-3-flash -o thinking=true "question"` |
| Advanced | gemini-3-pro | `llm -m gemini-3-pro "question"` |
| Long context (1M) | gemini-2.5-pro | `llm -m gemini-2.5-pro "question"` |
| Deep reasoning | gemini-2.5-pro | `llm -m gemini-2.5-pro -o thinking=32000 "question"` |

### Model Selection Guidelines

1. **Quick questions**: Use `gpt-5 -o reasoning_effort=low` or `gemini-3-flash`
2. **General advice**: Use `gpt-5` or `gpt-5.2` (default reasoning)
3. **Complex debugging**: Use `gpt-5.2 -o reasoning_effort=high` or `gemini-2.5-pro -o thinking=32000`
4. **Code review**: Use `gpt-5.2` for thorough analysis
5. **Architecture**: Use `gpt-5.2 -o reasoning_effort=high` for deep reasoning

## Command Reference

### Basic Prompts

```bash
# Simple question
llm "What's the best way to handle rate limiting in a REST API?"

# With specific model
llm -m gpt-5.2 "Explain this error: <error message>"

# With system prompt
llm -s "You are a senior software architect" "Review this design: <design>"
```

### Piped Input

```bash
# Analyze code from file
cat src/auth.ts | llm -m gpt-5.2 "Review this authentication code for security issues"

# Analyze git diff
git diff | llm -m gpt-5.2 "Review these changes for bugs"

# Analyze error logs
cat error.log | llm -m gpt-5 "What's causing these errors?"
```

### Options

```bash
# Control reasoning effort (OpenAI)
llm -m gpt-5.2 -o reasoning_effort=high "Complex question"
llm -m gpt-5.2 -o reasoning_effort=low "Simple question"

# Enable thinking mode (Gemini)
llm -m gemini-2.5-pro -o thinking=32000 "Complex reasoning task"

# Extract code blocks from response
llm -x "Write a function to parse JSON safely"
```

### Conversations

```bash
# Continue previous conversation
llm -c "What about error handling?"

# Start new conversation with context
llm -m gpt-5.2 "I'm debugging a memory leak in a Node.js app..."
llm -c "Here's the heap snapshot: <data>"
```

## Workflow Examples

### Hard Bug Debugging

When stuck on a difficult bug:

```bash
# Describe the problem with context
llm -m gpt-5.2 -o reasoning_effort=high "I'm debugging this issue:

Error: Connection refused on port 5432
Environment: Docker container, Node.js 20
Stack trace: <paste stack trace>

What I've tried:
1. Verified PostgreSQL is running
2. Checked network settings
3. Tested connection from host

What else should I check?"
```

### Architecture Decision

When evaluating design choices:

```bash
llm -m gpt-5.2 -o reasoning_effort=high "I need to decide between these approaches:

Option A: Event-driven with Redis pub/sub
Option B: Direct API calls with circuit breaker

Context:
- Microservices architecture
- ~1000 requests/second
- Eventual consistency is acceptable

What are the trade-offs? Which would you recommend?"
```

### Code Review

Get a second opinion on code changes:

```bash
git diff HEAD~1 | llm -m gpt-5.2 "Review this code change for:
- Bugs or logic errors
- Security vulnerabilities
- Performance issues
- Missing edge cases

Be specific about line numbers and issues."
```

### Plan Validation

Before implementing a complex feature:

```bash
llm -m gpt-5.2 -o reasoning_effort=high "Review this implementation plan:

Feature: User authentication with OAuth2
Steps:
1. Add OAuth2 middleware
2. Create /auth/callback endpoint
3. Store tokens in Redis
4. Add refresh token rotation

What am I missing? What could go wrong?"
```

### Alternative Approaches

When you want fresh ideas:

```bash
llm -m gpt-5.2 "Here's my current approach to <problem>:
<describe approach>

What are alternative ways to solve this? What am I missing?"
```

## Best Practices

### Providing Context

1. **Include relevant code** - Pipe files or paste snippets
2. **Describe the environment** - Framework, language version, dependencies
3. **Explain what you've tried** - Helps avoid repeated suggestions
4. **State your constraints** - Performance requirements, compatibility needs

### Formatting Prompts

```bash
# Good: Structured with clear sections
llm -m gpt-5.2 "Problem: <description>

Context:
- Language: TypeScript
- Framework: Express
- Environment: Docker

Error: <error message>

Question: What's causing this and how do I fix it?"

# Bad: Vague without context
llm "Why doesn't this work?"
```

### Interpreting Results

1. **Verify suggestions** - Always test recommendations against your codebase
2. **Consider multiple perspectives** - Run the same question through different models
3. **Cross-reference** - Check suggestions against documentation
4. **Adapt to your context** - Generic advice may need adjustment

### When NOT to Use

- Simple, obvious changes (typos, formatting)
- Well-documented operations with clear solutions
- When you need to move fast on low-risk changes
- Repetitive tasks where the pattern is established

## Troubleshooting

### Model Not Found

```bash
# List available models
llm models

# Install missing plugin
llm install llm-gemini
```

### API Key Issues

```bash
# Re-set API key
llm keys set openai
llm keys set gemini

# Verify key is set
llm keys
```

### Rate Limiting

If you hit rate limits:
1. Use `reasoning_effort=low` for less token usage
2. Switch to a different model temporarily
3. Wait and retry

### Long Responses Truncated

For complex questions that need detailed answers:
```bash
# Use a model with longer output
llm -m gpt-5.2 -o max_tokens=4096 "detailed question"
```
