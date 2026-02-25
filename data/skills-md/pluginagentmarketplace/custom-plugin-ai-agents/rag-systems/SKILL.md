---
name: rag-systems
description: Build RAG systems - embeddings, vector stores, chunking, and retrieval optimization
sasmp_version: "1.3.0"
bonded_agent: 03-rag-systems
bond_type: PRIMARY_BOND
version: "2.0.0"
---

# RAG Systems

Build Retrieval-Augmented Generation systems for grounded responses.

## When to Use This Skill

Invoke this skill when:
- Building Q&A over custom documents
- Implementing semantic search
- Setting up vector databases
- Optimizing retrieval quality

## Parameter Schema

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `task` | string | Yes | RAG goal | - |
| `vector_db` | enum | No | `pinecone`, `weaviate`, `chroma`, `pgvector` | `chroma` |
| `embedding_model` | string | No | Embedding model | `text-embedding-3-small` |
| `chunk_size` | int | No | Chunk size in chars | `1000` |

## Quick Start

```python
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Split documents
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)

# 2. Create vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(chunks, embeddings)

# 3. Retrieve
docs = vectorstore.similarity_search("query", k=5)
```

## Chunking Strategy

| Content Type | Size | Overlap | Rationale |
|--------------|------|---------|-----------|
| Technical docs | 500-800 | 100 | Preserve code |
| Legal docs | 1000-1500 | 200 | Keep clauses |
| Q&A/FAQ | 200-400 | 50 | Atomic answers |

## Embedding Costs

| Model | Cost/1M tokens |
|-------|---------------|
| text-embedding-3-small | $0.02 |
| text-embedding-3-large | $0.13 |
| Cohere embed-v3 | $0.10 |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Irrelevant results | Improve chunking, add reranking |
| Missing context | Increase k, use parent retriever |
| Hallucinations | Add "only use context" prompt |
| Slow retrieval | Add caching, reduce k |

## Best Practices

- Always include source attribution
- Use hybrid search (dense + BM25)
- Implement reranking for quality
- Evaluate with RAGAS metrics

## Related Skills

- `llm-integration` - LLM for generation
- `agent-memory` - Memory retrieval
- `ai-agent-basics` - Agentic RAG

## References

- [LangChain RAG](https://python.langchain.com/docs/tutorials/rag/)
- [Pinecone Guide](https://www.pinecone.io/learn/)
