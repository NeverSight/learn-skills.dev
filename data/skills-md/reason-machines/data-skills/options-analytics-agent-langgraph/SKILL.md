---
name: options-analytics-agent-langgraph
description: Build AI agents for real-time financial options analysis with LangGraph, ChromaDB RAG, and Polygon.io data
triggers:
  - analyze stock options using LangGraph agent
  - build financial options analysis agent
  - create options trading analysis with RAG
  - integrate Polygon.io options data with AI
  - implement options analytics with persistent memory
  - set up ChromaDB for financial data caching
  - build multi-agent workflow for options trading
  - create intelligent options data processing system
---

# Options Analytics Agent with LangGraph

> Skill by [ara.so](https://ara.so) — Data Skills collection.

A sophisticated LangGraph-based agent that automates financial options analysis with real-time data from Polygon.io, smart caching via ChromaDB, persistent memory, and professional-grade analysis. Built for creating intelligent trading assistants with RAG capabilities and microservice architecture.

## What It Does

This project provides a complete AI agent system for:
- **Real-time options data retrieval** from Polygon.io with intelligent caching
- **RAG-powered knowledge base** using ChromaDB for semantic search
- **Persistent conversation memory** across sessions via SQLite
- **Professional options analysis** with Greeks, sentiment, and anomaly detection
- **Multi-format exports** (CSV, charts, reports)
- **LangGraph orchestration** for multi-agent workflows
- **FastAPI microservice** deployment

## Installation

### Prerequisites

```bash
# Python 3.10+
python --version

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

**Key dependencies:**
```
langchain>=0.3.0
langgraph>=0.2.45
langchain-openai>=0.2.6
langchain-chroma>=0.1.4
chromadb>=0.5.20
fastapi>=0.115.5
uvicorn>=0.32.1
pandas>=2.2.3
matplotlib>=3.9.2
tavily-python>=0.5.0
```

### Environment Configuration

Create `.env` file in project root:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key
POLYGON_API_KEY=your_polygon_io_api_key

# Optional
TAVILY_API_KEY=your_tavily_api_key  # For web search
LANGCHAIN_API_KEY=your_langchain_api_key  # For tracing
LANGCHAIN_TRACING_V2=true
```

### Verify Installation

```python
# Test import
from agent_main import create_agent_workflow
from config.settings import validate_api_keys

# Validate API keys
validate_api_keys()
print("✓ Installation successful")
```

## Project Structure

```
project/
├── agent_main.py              # Main agent entry point
├── config/settings.py         # Configuration management
├── tools/
│   ├── search/               # Options search tools
│   ├── export/               # Data export tools
│   └── analysis/             # Analysis tools
├── rag/                      # RAG knowledge base
├── monitoring/               # Performance tracking
└── microservice/             # FastAPI deployment
```

## Core Usage

### Basic Agent Interaction

```python
from agent_main import create_agent_workflow
from langchain_core.messages import HumanMessage

# Create agent
workflow = create_agent_workflow()
app = workflow.compile()

# Simple query
config = {"configurable": {"thread_id": "session_1"}}
query = "Search for AAPL options expiring this week"

result = app.invoke(
    {"messages": [HumanMessage(content=query)]},
    config=config
)

print(result["messages"][-1].content)
```

### Interactive Chat Loop

```python
from agent_main import create_agent_workflow
from langchain_core.messages import HumanMessage

def chat():
    workflow = create_agent_workflow()
    app = workflow.compile()
    session_id = "user_session_1"
    
    print("Options Analytics Agent (type 'exit' to quit)")
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            break
            
        config = {"configurable": {"thread_id": session_id}}
        result = app.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config
        )
        
        response = result["messages"][-1].content
        print(f"\nAgent: {response}")

if __name__ == "__main__":
    chat()
```

## Key Tools & Commands

### 1. Options Search Tool

Search for options data with automatic caching:

```python
from tools.search.options_search import OptionsSearchTool

tool = OptionsSearchTool()

# Search with automatic caching
result = tool._run(
    ticker="NVDA",
    expiration_date="2024-12-20",
    option_type="call",
    force_refresh=False  # Use cache if available
)

# Force fresh API call
result = tool._run(
    ticker="NVDA",
    expiration_date="2024-12-20",
    option_type="call",
    force_refresh=True
)
```

### 2. Batch Search Tool

Search multiple tickers efficiently:

```python
from tools.search.batch_search import BatchOptionsSearchTool

tool = BatchOptionsSearchTool()

result = tool._run(
    tickers=["AAPL", "MSFT", "GOOGL"],
    expiration_date="2024-12-31",
    option_type="call"
)
```

### 3. RAG Knowledge Base

Query cached options data semantically:

```python
from rag.rag_tools import RAGQueryTool

rag_tool = RAGQueryTool()

# Semantic search
results = rag_tool._run(
    query="high volume AAPL calls near the money",
    top_k=5
)

# Date-based retrieval
from rag.rag_collection_tools import DateRangeCollectionTool

date_tool = DateRangeCollectionTool()
data = date_tool._run(
    ticker="AAPL",
    start_date="2024-12-01",
    end_date="2024-12-31"
)
```

### 4. Options Analysis

Professional-grade analysis:

```python
from tools.analysis.analysis_tools import AnalyzeOptionsTool

analysis_tool = AnalyzeOptionsTool()

result = analysis_tool._run(
    ticker="TSLA",
    expiration_date="2024-12-20",
    analysis_type="sentiment"  # or "greeks", "anomaly"
)

print(result)
```

### 5. Data Export

Export to CSV or charts:

```python
from tools.export.csv_export import CSVExportTool
from tools.export.visualization import ChartVisualizationTool

# CSV export
csv_tool = CSVExportTool()
csv_tool._run(
    ticker="AAPL",
    expiration_date="2024-12-20",
    option_type="call",
    output_filename="aapl_calls.csv"
)

# Chart generation
chart_tool = ChartVisualizationTool()
chart_tool._run(
    ticker="AAPL",
    expiration_date="2024-12-20",
    chart_type="volume_oi"
)
```

## Configuration

### Settings Management

```python
# config/settings.py
from config.settings import (
    OPENAI_API_KEY,
    POLYGON_API_KEY,
    MODEL_NAME,
    CHROMA_PERSIST_DIR,
    validate_api_keys
)

# Validate all keys
validate_api_keys()

# Access configuration
print(f"Model: {MODEL_NAME}")
print(f"ChromaDB: {CHROMA_PERSIST_DIR}")
```

### Custom Agent Configuration

```python
from agent_main import create_agent_workflow
from langgraph.checkpoint.memory import MemorySaver

# Create with custom checkpointer
memory = MemorySaver()
workflow = create_agent_workflow()
app = workflow.compile(checkpointer=memory)

# Or use SQLite checkpointer
from langgraph.checkpoint.sqlite import SqliteSaver

with SqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
    app = workflow.compile(checkpointer=checkpointer)
```

## Advanced Patterns

### Custom Tool Integration

```python
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

@tool
def custom_options_analyzer(ticker: str, metric: str) -> str:
    """Analyze specific option metric.
    
    Args:
        ticker: Stock symbol
        metric: Metric to analyze (volatility, skew, etc.)
    """
    # Your custom logic
    return f"Analysis for {ticker}: {metric}"

# Add to agent
from config.settings import get_llm

llm = get_llm()
tools = [custom_options_analyzer]
agent = create_react_agent(llm, tools)
```

### RAG Knowledge Base Setup

```python
from rag.rag_knowledge_base import RAGKnowledgeBase

# Initialize
kb = RAGKnowledgeBase(
    persist_directory="./data/chroma_db",
    collection_name="options_data"
)

# Add documents
kb.add_documents([
    {
        "ticker": "AAPL",
        "expiration": "2024-12-20",
        "strike": 180.0,
        "type": "call",
        "volume": 5000,
        "open_interest": 10000
    }
])

# Query
results = kb.query(
    query_text="high volume Apple calls",
    n_results=5
)
```

### Persistent Memory Across Sessions

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Create persistent checkpointer
checkpointer = SqliteSaver.from_conn_string("./data/conversation_memory.db")

workflow = create_agent_workflow()
app = workflow.compile(checkpointer=checkpointer)

# Session 1
config1 = {"configurable": {"thread_id": "user_123"}}
app.invoke({"messages": [HumanMessage("Search AAPL options")]}, config1)

# Session 2 (remembers previous context)
app.invoke({"messages": [HumanMessage("Show me the calls")]}, config1)
```

### Streaming Responses

```python
from langchain_core.messages import HumanMessage

workflow = create_agent_workflow()
app = workflow.compile()

config = {"configurable": {"thread_id": "session_1"}}
query = HumanMessage(content="Analyze TSLA options")

# Stream tokens
for chunk in app.stream({"messages": [query]}, config):
    if "messages" in chunk:
        print(chunk["messages"][-1].content, end="", flush=True)
```

## Microservice Deployment

### FastAPI Server

```python
# microservice/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent_main import create_agent_workflow
from langchain_core.messages import HumanMessage

app = FastAPI(title="Options Analytics API")
workflow = create_agent_workflow()
agent_app = workflow.compile()

class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"

@app.post("/query")
async def query_agent(request: QueryRequest):
    try:
        config = {"configurable": {"thread_id": request.session_id}}
        result = agent_app.invoke(
            {"messages": [HumanMessage(content=request.query)]},
            config=config
        )
        return {
            "response": result["messages"][-1].content,
            "session_id": request.session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run: uvicorn microservice.app:app --reload
```

### Docker Deployment

```dockerfile
# microservice/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "microservice.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  options-agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - POLYGON_API_KEY=${POLYGON_API_KEY}
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
```

**Start service:**
```bash
docker-compose up -d
```

## Common Workflows

### Complete Options Analysis Pipeline

```python
from agent_main import create_agent_workflow
from langchain_core.messages import HumanMessage

def analyze_options_workflow(ticker: str, expiration: str):
    workflow = create_agent_workflow()
    app = workflow.compile()
    
    config = {"configurable": {"thread_id": f"analysis_{ticker}"}}
    
    # Step 1: Search options
    query1 = f"Search {ticker} options expiring {expiration}"
    result1 = app.invoke({"messages": [HumanMessage(query1)]}, config)
    
    # Step 2: Analyze sentiment
    query2 = f"Analyze sentiment for {ticker} options"
    result2 = app.invoke({"messages": [HumanMessage(query2)]}, config)
    
    # Step 3: Export to CSV
    query3 = f"Export {ticker} options to CSV"
    result3 = app.invoke({"messages": [HumanMessage(query3)]}, config)
    
    return {
        "search": result1["messages"][-1].content,
        "analysis": result2["messages"][-1].content,
        "export": result3["messages"][-1].content
    }

# Run pipeline
results = analyze_options_workflow("NVDA", "2024-12-31")
```

### Batch Processing Multiple Tickers

```python
from tools.search.batch_search import BatchOptionsSearchTool
from tools.analysis.analysis_tools import AnalyzeOptionsTool

def batch_analysis(tickers: list, expiration: str):
    search_tool = BatchOptionsSearchTool()
    analysis_tool = AnalyzeOptionsTool()
    
    results = {}
    
    # Batch search
    search_result = search_tool._run(
        tickers=tickers,
        expiration_date=expiration,
        option_type="call"
    )
    
    # Individual analysis
    for ticker in tickers:
        analysis = analysis_tool._run(
            ticker=ticker,
            expiration_date=expiration,
            analysis_type="sentiment"
        )
        results[ticker] = analysis
    
    return results

# Process watchlist
watchlist = ["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"]
results = batch_analysis(watchlist, "2024-12-31")
```

### Real-time Monitoring with Callbacks

```python
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.messages import HumanMessage

class OptionsMonitorCallback(BaseCallbackHandler):
    def on_tool_start(self, serialized, input_str, **kwargs):
        print(f"🔧 Tool: {serialized['name']}")
    
    def on_tool_end(self, output, **kwargs):
        print(f"✅ Result: {output[:100]}...")

# Use callback
workflow = create_agent_workflow()
app = workflow.compile()

config = {
    "configurable": {"thread_id": "monitor_session"},
    "callbacks": [OptionsMonitorCallback()]
}

result = app.invoke(
    {"messages": [HumanMessage("Search AAPL options")]},
    config=config
)
```

## Troubleshooting

### API Key Issues

```python
# Validate API keys
from config.settings import validate_api_keys

try:
    validate_api_keys()
    print("✓ All API keys valid")
except ValueError as e:
    print(f"✗ Missing: {e}")
    # Set missing keys in .env file
```

### ChromaDB Connection Errors

```python
# Reset ChromaDB
import shutil
import os

chroma_path = "./data/chroma_db"
if os.path.exists(chroma_path):
    shutil.rmtree(chroma_path)
    print("ChromaDB reset")

# Reinitialize
from rag.rag_knowledge_base import RAGKnowledgeBase
kb = RAGKnowledgeBase()
```

### Clear Conversation Memory

```python
# Clear SQLite memory
import os

memory_file = "./data/conversation_memory.db"
if os.path.exists(memory_file):
    os.remove(memory_file)
    print("Conversation memory cleared")
```

### Polygon.io Rate Limits

```python
# Use caching to reduce API calls
from tools.search.options_search import OptionsSearchTool

tool = OptionsSearchTool()

# Always try cache first
result = tool._run(
    ticker="AAPL",
    expiration_date="2024-12-20",
    option_type="call",
    force_refresh=False  # Use cached data
)

# Only force refresh when absolutely necessary
```

### Debug Agent State

```python
# Inspect agent state
from agent_main import create_agent_workflow

workflow = create_agent_workflow()
app = workflow.compile()

config = {"configurable": {"thread_id": "debug_session"}}
result = app.invoke(
    {"messages": [HumanMessage("Search AAPL options")]},
    config=config
)

# Print full state
print("Messages:", result["messages"])
print("Tools called:", [m.additional_kwargs for m in result["messages"]])
```

### Enable Tracing

```python
# Set in .env
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=your_key

# Or in code
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your_key"

# View traces at https://smith.langchain.com
```

## Performance Optimization

### Batch Embeddings

```python
from rag.rag_knowledge_base import RAGKnowledgeBase

kb = RAGKnowledgeBase()

# Batch add for efficiency
documents = [
    {"ticker": "AAPL", "data": "..."},
    {"ticker": "MSFT", "data": "..."},
    # ... more documents
]

kb.add_documents(documents)  # Processes in batches
```

### Parallel Tool Execution

```python
from concurrent.futures import ThreadPoolExecutor
from tools.search.options_search import OptionsSearchTool

def search_ticker(ticker, date):
    tool = OptionsSearchTool()
    return tool._run(ticker=ticker, expiration_date=date, option_type="call")

tickers = ["AAPL", "MSFT", "GOOGL", "NVDA"]
date = "2024-12-31"

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(lambda t: search_ticker(t, date), tickers))
```

## Testing

### Unit Test Example

```python
import unittest
from tools.search.options_search import OptionsSearchTool

class TestOptionsSearch(unittest.TestCase):
    def setUp(self):
        self.tool = OptionsSearchTool()
    
    def test_search_call_options(self):
        result = self.tool._run(
            ticker="AAPL",
            expiration_date="2024-12-20",
            option_type="call"
        )
        self.assertIn("AAPL", result)
        self.assertIn("call", result.lower())

if __name__ == "__main__":
    unittest.main()
```

This skill provides comprehensive coverage of the Options Analytics Agent project, enabling AI coding agents to effectively assist developers in building sophisticated financial analysis systems with LangGraph, RAG, and persistent memory.
