---
name: ai-app-performance-optimization
description: Shift focus from AI hype (latest models, vector DBs, agentic frameworks) to high-leverage activities that actually improve product quality. Use this when an AI feature is underperforming, when the team is stuck in a "research loop," or when planning the roadmap for a new AI application.
---

To build successful AI applications, move beyond the "ideal crisis" of chasing every new research paper or model update. Real performance gains come from traditional product engineering applied to AI: data quality, workflow optimization, and user-centric evaluation.

## The Optimization Pivot
Differentiate between activities that offer marginal gains (The Hype) and those that drive exponential product quality (The Reality).

### Low-Leverage (Avoid Over-Agonizing)
*   **Constant model switching:** Evaluating every new "smarter" model.
*   **Vector Database wars:** Spending weeks choosing between different database providers.
*   **Framework chasing:** Adopting the newest agentic library before the core logic works.
*   **Latest News:** Staying up-to-date with every AI headline instead of focusing on user feedback.

### High-Leverage (Prioritize These)
*   **Data Preparation:** Rewriting data into Q&A formats or adding metadata.
*   **Workflow Mapping:** Optimizing the end-to-end user journey rather than just the model output.
*   **Prompt Engineering:** Iteratively refining instructions and context.
*   **Reliable Infrastructure:** Building the platform stability needed for production scale.

## Implementation Guide

### 1. Optimize Data for Retrieval (RAG)
If using Retrieval-Augmented Generation (RAG), the biggest lever for quality is not the retrieval algorithm, but how the data is prepared.
*   **Chunking Strategy:** Balance chunk size. If chunks are too long, you lose precision; if too short, you lose context.
*   **Hypothetical Questions:** Generate 5-10 "hypothetical questions" for each chunk of data using an LLM. Store these questions alongside the data. At retrieval time, match the user's query against these questions to find the most relevant chunk.
*   **Contextual Metadata:** Add summary headers to data chunks. For example, if a document section explains "maternity leave," ensure the word "HR Policy" is in the metadata even if it isn't in the specific paragraph.
*   **AI-Native Formatting:** Rewrite documentation specifically for AI consumption. Humans have common sense; AI needs explicit annotations (e.g., explaining that a "Temperature of 1" on a specific graph refers to a relative scale, not degrees Celsius).

### 2. Establish Pragmatic Evals
Do not wait for a "perfect" evaluation suite. Use evals to identify where the product is failing.
*   **Focus on the Core:** Build evals for the most common 20% of use cases that drive 80% of value.
*   **Segment Failures:** Look for specific user segments or topics where the model performs poorly. 
*   **Vibe Check vs. Scale:** For early features, a "vibe check" (manual review) is acceptable. As you scale, implement "tyrannical" evals for catastrophic failure modes (e.g., hallucinating legal advice or leaking sensitive data).
*   **Step-by-Step Evaluation:** For complex tasks (like deep research), evaluate the intermediate steps (e.g., "Are the search queries diverse?") rather than just the final summary.

### 3. Apply System Thinking
AI is better at "disjointed skills" than "system thinking." 
*   **Holistic Debugging:** When a model fails, don't just change the prompt. Check if the error is coming from an external component (e.g., an API tier limit, a missing environment variable, or a bad data source).
*   **Scaffold the Reasoning:** If a task is complex, provide a "scaffold" or a step-by-step checklist for the AI to follow, mimicking how a senior human expert would approach the problem.

## Examples

**Example 1: Customer Support Bot**
*   **Context:** A RAG-based bot is giving generic, unhelpful answers to technical questions.
*   **Input:** Technical documentation in raw PDF format.
*   **Application:** Rewrite the documentation into a "Question and Answer" format using an LLM. Add metadata tags for "Product Version" and "User Persona."
*   **Output:** The bot's retrieval accuracy increases because the query now matches specific Q&A pairs instead of dense technical paragraphs.

**Example 2: Internal Research Tool**
*   **Context:** A tool meant to summarize podcast transcripts is missing key nuances.
*   **Input:** 50 hours of raw transcripts.
*   **Application:** Create an evaluation set of 10 "Gold Standard" summaries. Run a "Test Time Compute" strategy: have the model generate 3 different summaries and use a second "judge" model to select the one that best captures the nuances identified in the gold standard.
*   **Output:** Higher quality summaries that better reflect the "system thinking" required for the task.

## Common Pitfalls
*   **The Fine-Tuning Trap:** Attempting to fine-tune a model to "learn" new facts. Fine-tuning is for changing *behavior* or *format*; RAG is for providing *facts*.
*   **Over-reliance on Junior Code:** Letting AI generate bulk code without senior review. This leads to "local" optimizations that break "global" system architecture.
*   **Measuring the Wrong Thing:** Using "lines of code" or "number of PRs" to measure AI-driven productivity. Focus instead on "Task Completion Rate" or "Conversion."
*   **Solving the Wrong Problem:** Spending months on sub-millisecond latency when the user's primary frustration is the accuracy of the answer.