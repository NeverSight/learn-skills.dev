---
name: surfsense
description: Air-gapped, privacy-focused AI research assistant and NotebookLM alternative (MODSetter/SurfSense). Use when the agent needs to index, research, transform, and synthesize local documentation, codebase notes, whitepapers, or research data without leaking privacy to external cloud servers.
---

# SurfSense (Privacy-Focused Research & Document Intelligence)

Based on [MODSetter/SurfSense](https://github.com/MODSetter/SurfSense): an air-gapped, privacy-first, open-source NotebookLM alternative. It enables AI agents to research, transform, query, and edit extensive document collections, source notes, and technical literature completely offline or with private LLMs.

---

## 🎯 When to Use
- **Deep Document Research:** Synthesizing architectural patterns, API documentation, and reverse-engineering research notes across large repositories.
- **Air-Gapped / Private Analysis:** Querying sensitive proprietary specifications, leaked source archives, or internal security reports without external cloud exposure.
- **Multi-Source Knowledge Synthesis:** Blending Markdown notes, PDFs, web bookmarks, and transcripts into unified, cited technical summaries.

---

## 🚀 Setup & Execution

### 1. Local / Self-Hosted Setup
SurfSense can run entirely locally with Docker or Python:

```bash
# Clone the SurfSense repository
git clone https://github.com/MODSetter/SurfSense.git
cd SurfSense

# Quickstart via Docker Compose
docker compose up -d
```

### 2. Pairing with Local LLMs (Ollama / LM Studio)
Configure SurfSense to point to local Ollama endpoints for 100% offline document intelligence:
- Base URL: `http://localhost:11434/v1`
- Embedding Model: `nomic-embed-text` or `bge-m3`
- Reasoning Model: `llama3.3`, `qwen2.5-coder`, or `deepseek-r1`

---

## ⚡ Integration with REA & Security Workflows
1. **Disassembly & Decompiler Notes RAG:** When reverse-engineering large binaries with REA, index Ghidra/Hopper decompiled dumps into SurfSense to perform semantic search across millions of lines of recovered pseudocode.
2. **Vulnerability Case Knowledge Base:** Keep a private local repository of past audit reports, CVE advisories, and security notes that can be queried during website security assessments.
3. **Zero Data Leakage:** Ensure proprietary client code or unpublished app data is never indexed in third-party hosted vector stores.
