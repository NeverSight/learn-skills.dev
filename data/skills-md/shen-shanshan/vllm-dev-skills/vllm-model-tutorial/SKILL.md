---
name: vllm-model-tutorial
description: >
  Generate comprehensive Chinese technical tutorial documents for specific vLLM models (e.g., Qwen3-VL, DeepSeek-V3, Llama 4, InternVL3, etc.).
  Produces deep-dive model walkthrough documents with Mermaid architecture diagrams, comparison tables,
  input preprocessing flows, forward pass analysis, ViT computation (for VLMs), vLLM code implementation
  analysis, and technical principle explanations (MoE, MLA, Gated Attention, ViT, DiT, etc.).
  Output is saved as Markdown to the skill's outputs/ directory.
  TRIGGER when: user asks to learn about a specific vLLM model (e.g., "我想了解 vllm 中的 Qwen3-VL",
  "帮我生成 Qwen3-VL 的模型教程", "generate a model tutorial for InternVL3 in vllm",
  "vllm 中的 DeepSeek-V3 是怎么实现的", "写一个 Llama 4 的vllm教程").
  DO NOT TRIGGER when: user asks about non-vLLM models, general LLM questions without requesting a tutorial,
  or asks about vLLM features/modules rather than specific models.
---

# vLLM Model Tutorial Generator

Generate a comprehensive model technical tutorial document for a given model supported by vLLM.

## Workflow

### Step 1: Identify the Model

Extract the model name from the user's request. Normalize common aliases:

- "Qwen3-VL" / "Qwen3VL" → Qwen3-VL
- "Qwen2.5-VL" → Qwen2.5-VL
- "DeepSeek-V3" / "DSv3" → DeepSeek-V3
- "InternVL3" / "InternVL 3" → InternVL3
- "Llama 4" → Llama 4
- "GPT-OSS" → GPT-OSS

If the model name is ambiguous, ask the user to clarify.

### Step 2: Research the Model

Gather information from multiple sources. This is the most critical step — thorough research determines document quality.

**2a. Find Technical Reports and Papers**

Search for the model's official technical report, paper, or blog post:
- Use WebSearch: `"{model_name} technical report arxiv"` or `"{model_name} paper"`
- Use WebFetch to read the paper/report and extract architecture details, innovations, benchmarks
- For model series: also find reports for predecessor models to build the evolution timeline

**2b. Gather Model Family Information**

Build the model family comparison context:
- Search for the full model series evolution (e.g., Qwen-VL → Qwen2-VL → Qwen2.5-VL → Qwen3-VL)
- For each variant: collect parameter counts, release dates, key innovations, performance benchmarks
- Find HuggingFace and ModelScope links for each variant (search `huggingface.co/{model_id}`)
- Collect technical report / paper links for each variant

**2c. Analyze Model Architecture**

Extract detailed architecture information from papers, docs, and the LLM Architecture Gallery:
- Overall architecture design (encoder-decoder, decoder-only, cross-attention)
- Key components: attention mechanism (MHA/GQA/MQA/MLA), FFN type (dense/MoE), normalization, activation
- For VLMs: ViT architecture, visual token projection, multimodal fusion strategy
- Context length, vocabulary size, hidden dimensions, layer counts
- Special tokens, chat template, generation config
- Reference: `https://sebastianraschka.com/llm-architecture-gallery/` for comparative context

**2d. Explore vLLM Source Code**

Find the model's implementation in vllm-project/vllm:
- Use `gh` CLI to find model files: `gh search code "repo:vllm-project/vllm {model_keyword}" --path vllm/model_executor/models`
- For VLMs, also search multimodal processing: `gh search code "repo:vllm-project/vllm {model_keyword}" --path vllm/multimodal`
- Read key implementation files to understand:
  - Model registration and configuration
  - Core class hierarchy (which vLLM base classes are extended)
  - Input processing pipeline (text + multimodal)
  - Forward pass implementation details
  - vLLM-specific optimizations applied
- See [references/model-research-guide.md](references/model-research-guide.md) for detailed code analysis methodology

**2e. Cross-Reference Documentation**

- Check vLLM docs: `https://docs.vllm.ai/en/latest/models/supported_models/`
- Search for known issues: `gh search issues "repo:vllm-project/vllm {model_keyword}" --label bug`

### Step 3: Generate the Tutorial Document

Read [references/style-guide.md](references/style-guide.md) for complete document structure and formatting conventions.

Key requirements:
- Write in **Chinese (简体中文)**, keeping English for technical terms
- Follow the multi-part structure defined in the style guide
- Include rich visual elements (see style guide for Mermaid diagram patterns)
- Include technical principle deep-dives for relevant mechanisms (MoE, MLA, GQA, ViT, etc.)
- Include document header with version info and date
- Include a "文档概述" section with target audience and reading guide

### Step 4: Save Output

Save the generated markdown file to `outputs/` directory relative to this skill's location:
- File path: `outputs/{model_name_snake_case}.md` (e.g., `outputs/qwen3_vl.md`, `outputs/deepseek_v3.md`)
- Create the `outputs/` directory if it doesn't exist
- Use snake_case for file names (lowercase, underscores)

The skill directory is the same directory as this SKILL.md file.

## Model Identification Heuristics

When the user's request is ambiguous, use these heuristics to determine what to include:

- If the model name contains "VL" or "Vision" → it's a VLM, include Part 5 (ViT computation)
- If the model is known MoE (DeepSeek-V3, Mixtral, Qwen3-MoE) → emphasize MoE in Part 2
- If the model has MLA (DeepSeek-V3 series) → include MLA deep-dive in Part 2
- If the model is dense + GQA (Llama 4, Qwen3 dense) → emphasize GQA analysis
- If the model generates images/video → check for DiT architecture and include if relevant

## Quality Checklist

Before saving the document, verify:
- [ ] Document has 4+ Mermaid diagrams (architecture, flow, sequence, class)
- [ ] Document has 3+ comparison/reference tables
- [ ] Document includes actual code snippets from vLLM source with file path annotations
- [ ] Document follows Chinese writing convention with English technical terms
- [ ] All sections have substantive content (no placeholder text)
- [ ] Document header includes version and date metadata
- [ ] Model series comparison table includes: model name, params, release date, key innovations, paper link, HF/ModelScope link
- [ ] Technical principle deep-dives present for relevant mechanisms
- [ ] Code location index table in appendix maps components to file paths
- [ ] For VLM models: Part 5 (ViT) is present and complete; For non-VLM: Part 5 is omitted

## References

- [references/style-guide.md](references/style-guide.md) — Document structure, formatting conventions, and output patterns
- [references/model-research-guide.md](references/model-research-guide.md) — Detailed research methodology for code analysis
- External: [LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/) — Comparative model architecture reference
