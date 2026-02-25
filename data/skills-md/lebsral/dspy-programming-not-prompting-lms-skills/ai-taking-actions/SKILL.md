---
name: ai-taking-actions
description: Build AI that takes actions, calls APIs, and does things autonomously. Use when you need AI to call APIs, use tools, perform calculations, search the web and act on results, interact with databases, or do multi-step tasks. Powered by DSPy agents (ReAct, CodeAct).
---

# Build AI That Takes Actions

Guide the user through building AI that reasons and takes actions — calling APIs, using tools, and completing multi-step tasks. Uses DSPy's ReAct and CodeAct agent modules.

## Step 1: Understand the use case

Ask the user:
1. **What should the AI do?** (answer questions, call APIs, perform calculations, search, etc.)
2. **What tools does it need?** (calculator, search, database, APIs, file system, etc.)
3. **How many steps might it take?** (simple tool call vs. multi-step reasoning)

## Step 2: Define tools

Tools are Python functions with type hints and docstrings. DSPy uses these to tell the AI what's available:

```python
def search(query: str) -> str:
    """Search the web for information."""
    # Your search implementation
    return "search results..."

def calculate(expression: str) -> float:
    """Evaluate a mathematical expression."""
    return dspy.PythonInterpreter({}).execute(expression)

def lookup_database(table: str, query: str) -> str:
    """Query the database for records matching the query."""
    # Your database logic
    return "query results..."
```

**Tool requirements:**
- Type hints on all parameters and return type
- Docstring explaining what the tool does
- Return a string (or something that converts to string)

## Step 3: Build the AI

### ReAct (Reasoning + Acting) — start here

The standard choice. Alternates between thinking and acting:

```python
import dspy

agent = dspy.ReAct(
    "question -> answer",
    tools=[search, calculate],
    max_iters=5,  # max steps before stopping
)

result = agent(question="What is the population of France divided by 3?")
print(result.answer)
```

### CodeAct — for code-heavy tasks

For tasks where writing and executing code is more natural:

```python
agent = dspy.CodeAct(
    "question -> answer",
    tools=[search, calculate],
    max_iters=5,
)

result = agent(question="Calculate the compound interest on $1000 at 5% for 10 years")
print(result.answer)
```

### Custom AI with state

```python
class ResearchBot(dspy.Module):
    def __init__(self):
        self.agent = dspy.ReAct(
            "question, context -> answer",
            tools=[search, lookup_database],
            max_iters=8,
        )

    def forward(self, question):
        # Add initial context or pre-processing
        context = "Use search for general questions, database for specific records."
        return self.agent(question=question, context=context)
```

## Step 4: Test the quality

```python
def action_metric(example, prediction, trace=None):
    # Check if the final answer is correct
    return prediction.answer.strip().lower() == example.answer.strip().lower()

# For open-ended tasks, use an AI judge
class JudgeResult(dspy.Signature):
    """Judge if the AI's answer correctly addresses the question."""
    question: str = dspy.InputField()
    expected: str = dspy.InputField()
    actual: str = dspy.InputField()
    is_correct: bool = dspy.OutputField()

def judge_metric(example, prediction, trace=None):
    judge = dspy.Predict(JudgeResult)
    result = judge(
        question=example.question,
        expected=example.answer,
        actual=prediction.answer,
    )
    return result.is_correct
```

## Step 5: Improve accuracy

```python
# Optimize the AI's reasoning prompts
optimizer = dspy.BootstrapFewShot(metric=action_metric, max_bootstrapped_demos=4)
optimized = optimizer.compile(agent, trainset=trainset)
```

For action-taking AI, `MIPROv2` often works better since it can optimize the reasoning instructions:

```python
optimizer = dspy.MIPROv2(metric=action_metric, auto="medium")
optimized = optimizer.compile(agent, trainset=trainset)
```

## Using LangChain tools

LangChain has 100+ pre-built tools (search engines, Wikipedia, SQL databases, web scrapers, etc.). Convert any of them to DSPy tools with one line:

```python
import dspy
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Convert LangChain tools to DSPy tools
search = dspy.Tool.from_langchain(DuckDuckGoSearchRun())
wikipedia = dspy.Tool.from_langchain(WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()))

# Use in any DSPy agent
agent = dspy.ReAct(
    "question -> answer",
    tools=[search, wikipedia],
    max_iters=5,
)
```

**When to use LangChain tools vs writing your own:**

| Use LangChain tools when... | Write your own when... |
|------------------------------|------------------------|
| There's an existing tool for it (search, Wikipedia, SQL) | You need custom business logic |
| You want quick prototyping | You need tight error handling |
| The tool wraps a standard API | You're wrapping an internal API |

Install the tools you need:

```bash
pip install langchain-community  # DuckDuckGo, Wikipedia, requests, etc.
```

For the full LangChain/LangGraph API reference, see [`docs/langchain-langgraph-reference.md`](../../docs/langchain-langgraph-reference.md).

## Key patterns

- **Start with ReAct** — it's the most general-purpose action module
- **Keep tools simple** — each tool should do one thing well
- **Set `max_iters`** to prevent infinite loops (default is usually fine)
- **Use descriptive docstrings** — the AI uses them to decide when to call each tool
- **Test without optimization first** — action AI often works well zero-shot
- **Add assertions** for safety — use `dspy.Assert` to prevent dangerous tool calls

## Additional resources

- For worked examples (calculator, search, APIs), see [examples.md](examples.md)
- Need multiple agents working together (not just one)? Use `/ai-coordinating-agents`
- Next: `/ai-improving-accuracy` to measure and improve your AI
