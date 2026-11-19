---
name: research
last_reviewed: 2026-09-06
group: Research
description: >-
  Investigate properly: frame questions, build source ladders, triangulate, and report findings.
  Use when investigating complex questions with primary sources.
---

# research

## Core Philosophy
Research is not browsing search engines, skimming blog posts, and summarizing the first three links. Anyone can query an LLM or Google and produce a surface-level synthesis of conventional wisdom. Rigorous, high-trust research is an **investigative discipline**: it frames sharp, refutable hypotheses, climbs the "Source Ladder" to primary provenance, triangulates claims across independent conflicting vectors, audits funding and bias, and delivers structured intelligence with auditable citations.

---

## 4-Step Investigative Research Framework

### Step 1: Question Framing & Scope Bounding
1. **Refining the Research Perimeter**:
   - Broad questions produce generic fluff. Narrow inquiries produce high-signal intelligence:
     - *Fluffy*: "How does WebAssembly perform?"
     - *Incisive*: "What is the memory and cold-start latency overhead of Wasmtime versus Node.js v20 when executing identical JSON-parsing microservices under 1,000 QPS on AWS Lambda?"
2. **Defining the Falsification Criteria**:
   - State what empirical evidence would refute your initial operating hypothesis.

### Step 2: The Source Ladder Architecture
1. **Climbing the Provenance Ladder**:
   - **Tier 1 (Primary Provenance - Highest Trust)**: Source code, benchmark raw telemetry, official RFC specifications, SEC 10-K filings, court transcripts, peer-reviewed clinical trial datasets.
   - **Tier 2 (Authoritative Secondary)**: Official technical documentation from system authors, seminal textbooks, peer-reviewed review articles.
   - **Tier 3 (Practitioner Analysis)**: Production post-mortems, engineering blogs from scaled tech companies (e.g. Netflix, Cloudflare).
   - **Tier 4 (Unverified / Opinion - Zero Trust without Verification)**: Marketing whitepapers, Medium posts, corporate PR releases, Reddit comments.
2. **The Golden Rule**: Never cite a Tier 4 claim without tracing it back to its Tier 1 origin.

### Step 3: Triangulation & Cross-Vector Verification
1. **The 3-Vector Rule**:
   - A non-obvious empirical claim cannot be accepted as fact until verified across **three independent, non-affiliated sources**:
     - Vector 1: Empirical benchmark or source code audit.
     - Vector 2: Third-party independent academic replication or audit.
     - Vector 3: Production post-mortem documenting real-world failure/success.
2. **Reconciling Conflicting Findings**:
   - When Source A says X and Source B says Not-X, identify the hidden variable: Did they test different hardware? Different compiler flags? Different network conditions?

### Step 4: Structuring the Research Dossier
1. **Standardized Dossier Structure**:
   - Executive Summary (BLUF: Bottom Line Up Front).
   - Core Hypotheses & Findings Matrix.
   - Deep Evidence & Methodology Dissection.
   - Contradictions & Caveats.
   - Primary Source Provenance References.

---

## Deliverable Format: High-Trust Research Dossier

```markdown
# Research Dossier: Edge Compute Cold Starts — Wasmtime vs V8 Isolates

### 1. Executive Summary (BLUF)
Wasmtime delivers a 12x faster cold-start initialization compared to V8 isolates (0.45ms vs 5.6ms), but suffers a 1.8x throughput penalty on heavy numerical compute tasks due to the lack of dynamic JIT profiling and tier-2 optimization.

### 2. Empirical Triangulation Matrix

| Vector | Source / Provenance | Methodology / Scope | Verified Finding |
|---|---|---|---|
| **Vector 1: Primary Telemetry** | Bytecode Alliance Wasmtime Benchmarks (v18.0) | Memory footprint per instance | Baseline idle footprint is 180KB RAM vs 18MB for Node.js V8. |
| **Vector 2: Academic Study** | ACM SIGPLAN 2024 (Müller et al.) | 100k synthetic microservice requests | Cold start latency: 0.42ms (p50), 0.98ms (p99) on Linux x86_64. |
| **Vector 3: Production Audit** | Fastly Lucet/Wasm Architecture Report | Global edge POP telemetry | 99.8% of tenant requests execute in existing pre-warmed memory instances. |

### 3. Critical Contradictions & Edge Cases
- *Discrepancy*: Several commercial serverless benchmarks claimed Wasm cold starts were 50ms.
- *Root Cause Analysis*: Tracing the setup revealed those benchmarks included container cold start times (Docker daemon initialization), not raw WebAssembly runtime compilation.

### 4. Primary Source Citations
1. Bytecode Alliance. (2024). *Wasmtime Performance Suite*. GitHub: https://github.com/bytecodealliance/wasmtime
2. Müller, K., et al. (2024). "Sandboxing at the Edge." *ACM SIGPLAN*, 42(3), 112–126.
```

---

## Worked Example: Investigating an Enterprise Vendor's "Zero Overhead" Database Claim

- **Context**: A vendor claimed their distributed database layer introduced "zero performance overhead" over raw NVMe disk operations.
- **Investigation**:
  1. Cloned the vendor's open-source benchmark repository and reviewed the configuration.
  2. Discovered the benchmark had disabled write-ahead logging (`fsync=off`) and kept the entire test database within the 64GB OS page cache.
  3. Reran the benchmark with persistent disk flushing (`O_DIRECT` / `fsync=on`) with working set sizes exceeding RAM.
- **Outcome**: Uncovered a 42% write latency regression under durable transaction conditions, saving the enterprise from a flawed multi-million-dollar infrastructure migration.

---

## Verification Checklist

- [ ] Specific, falsifiable research question formulated before gathering data.
- [ ] Source Ladder climbed to primary source code, raw data, or official specs.
- [ ] Key claims triangulated across at least 3 independent, non-affiliated vectors.
- [ ] Benchmark conditions audited for hidden configuration biases (e.g. caching, compute parity).
- [ ] Conflicting data and outlier results acknowledged and reconciled.

---

## Anti-Patterns

- **Single-Source Paraphrasing**: Relying entirely on a single corporate whitepaper or sponsored blog post to make architectural decisions.
- **Citing Secondary Aggregators**: Citing a news article that cites a blog post that misquotes a scientific paper. Always read the original paper.
- **Confirmation Bias Hunting**: Searching only for queries that confirm your favorite technical bias (e.g. searching only *"Why Rust is faster than Go"*).
