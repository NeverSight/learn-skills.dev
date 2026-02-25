---
name: diverse-content-gen
description: "Agent workflow for generating highly diverse creative content using Verbalized Sampling (VS) technique. Use when user requests multiple variations, brainstorming, creative ideas, or when standard prompting produces repetitive outputs. Increases diversity by 1.6-2.1× while maintaining quality. Works for: blog posts, social media captions, stories, campaign ideas, product descriptions, taglines, and open-ended creative tasks."
---

# Diverse Content Generation using Verbalized Sampling

## Overview

This skill teaches agents how to use **Verbalized Sampling (VS)** - a research-backed prompting technique that dramatically increases output diversity (1.6-2.1× improvement) without sacrificing quality.

**The Problem:** Standard aligned LLMs suffer from "mode collapse" - they generate overly similar, safe, predictable outputs because of typicality bias in training data.

**The Solution:** Instead of asking for single instances ("write a blog post"), VS prompts the model to verbalize a probability distribution over multiple responses ("generate 5 blog post ideas with their probabilities").

**Core Principle:** Different prompt types collapse to different modes. Distribution-level prompts recover the diverse base model distribution, while instance-level prompts collapse to the most typical output.

---

## Workflow Decision Tree

**Detect user intent, route to appropriate reference:**

| User Request Pattern | Route To | Description |
|---------------------|----------|-------------|
| "Generate diverse [content]" | `references/vs-core-technique.md` | Learn VS basics, prompt templates, execution |
| "Write 5 blog posts / captions / ideas" | `references/task-workflows.md` | Task-specific workflows pre-configured |
| "Need higher quality" or "too wild" | `references/advanced-techniques.md` | VS-CoT, VS-Multi, parameter tuning |
| "Save to file" or "batch process 50 items" | `references/tool-integration.md` | VS + File tools, batch workflows |
| "VS outputs too similar" or errors | `references/troubleshooting.md` | Common pitfalls and solutions |
| "Which model works best?" | `references/research-findings.md` | Benchmarks, model compatibility |

**Default workflow:** Load `vs-core-technique.md` first, then load additional references as needed.

---

## When to Use This Skill

### Trigger Scenarios

**Use VS when user requests:**
- "Give me **multiple variations/options/ideas**"
- "I need **diverse** [content type]"
- "**Brainstorm** several approaches to..."
- "Generate **different angles** for..."
- "Avoid repetitive/similar outputs"

**Use VS for these content types:**
- Creative writing (blog posts, stories, poems, scripts)
- Marketing (campaign ideas, taglines, ad copy, social captions)
- Product content (descriptions, feature bullets, value props)
- Ideation (brainstorming, exploration, strategy options)
- Open-ended QA (tasks with multiple valid answers)

**DON'T use VS for:**
- Single-answer factual questions
- Tasks requiring deterministic output
- When user explicitly wants "the best" single answer
- Real-time low-latency applications

---

## Quick Start (30-Second Version)

**For agents who need VS immediately:**

### 1. Detect Need
User wants multiple variations → Use VS

### 2. Basic VS Prompt Template
```
Generate {k} responses to: {user_request}

Return JSON format with key "responses" (list of dicts).
Each dict must include:
• text: the response string only
• probability: estimated probability (0.0-1.0)

Give ONLY the JSON object, no extra text.
```

### 3. Standard Parameters
- **k = 5** (candidates per call)
- **temperature = 0.8**
- **threshold = 0.10** (optional, for more diversity)

### 4. Process Output
```python
import json
data = json.loads(llm_output)
candidates = data["responses"]
# Present to user ranked by probability
```

**For detailed instructions:** Load `references/vs-core-technique.md`

---

## Progressive Learning Path

**Recommended loading sequence:**

### Level 1: Basics (Required)
1. Start here: `references/vs-core-technique.md`
   - VS theory and why it works
   - Copy-paste ready prompt templates
   - Step-by-step execution workflow
   - Output parsing and presentation

### Level 2: Task-Specific (Choose based on use case)
2. Load: `references/task-workflows.md`
   - Blog post ideas workflow
   - Social media captions workflow
   - Campaign/strategy ideas workflow
   - Story/narrative generation workflow

### Level 3: Advanced (On-demand)
3. When needed:
   - **Higher quality needed:** `references/advanced-techniques.md` (VS-CoT, VS-Multi)
   - **File operations:** `references/tool-integration.md` (Write, batch processing)
   - **Issues/errors:** `references/troubleshooting.md` (Pitfalls & fixes)
   - **Model selection:** `references/research-findings.md` (Benchmarks)

---

## Quick Reference Card

**Copy this for quick lookup:**

| Parameter | Default Value | When to Adjust |
|-----------|--------------|----------------|
| k (candidates) | 5 | Use 3 for quick, 10 for exploration |
| Temperature | 0.7-1.0 | Combine with VS for extra diversity |
| Probability threshold | 0.10 (optional) | Lower (0.01) for more creative outputs |

**Troubleshooting shortcuts:**
- Outputs too similar? → Lower threshold OR increase k OR load `advanced-techniques.md`
- Quality too low? → VS-Multi workflow (see `advanced-techniques.md`)
- JSON parsing errors? → Emphasize "ONLY JSON" OR use regex extraction
- Not sure which model? → Load `research-findings.md`

**Quality checklist before presenting:**
- [ ] Diversity achieved (different angles/styles)
- [ ] Quality maintained (baseline standards)
- [ ] User intent matched
- [ ] Clean formatting (no JSON artifacts)

---

## Resources

This skill uses progressive disclosure for optimal token efficiency:

### references/
Documentation loaded on-demand based on agent needs:

- **vs-core-technique.md** - Core VS concepts, prompt templates, execution steps
- **task-workflows.md** - Pre-configured workflows for common content types
- **advanced-techniques.md** - VS-CoT, VS-Multi, parameter tuning, refinement
- **tool-integration.md** - Combining VS with file tools, batch processing
- **troubleshooting.md** - Common pitfalls and solutions
- **research-findings.md** - Performance benchmarks, model compatibility data

**Pattern:** Agent loads SKILL.md first (routing), then loads specific references as needed during execution.

---

## Examples in Context

### Example 1: Simple Brainstorming
**User:** "Give me 5 tagline ideas for a coffee shop"

**Agent workflow:**
1. Detect: "5 ideas" → VS needed
2. Load: `vs-core-technique.md` (if not already loaded)
3. Execute: VS prompt with k=5
4. Parse & present: 5 diverse taglines

### Example 2: Production Content
**User:** "Write 10 blog post ideas about AI, I need them saved to a file"

**Agent workflow:**
1. Detect: "10 ideas" + "saved to file" → VS + file tools
2. Load: `vs-core-technique.md` + `tool-integration.md`
3. Execute: VS with k=5, make 2 calls
4. Process: Format as markdown
5. Write: Use Write tool to save file

### Example 3: Quality Refinement
**User:** "These are good but need more polish for production use"

**Agent workflow:**
1. Detect: Quality improvement needed
2. Load: `advanced-techniques.md`
3. Execute: VS-Multi workflow (initial VS → user selects → refine)
4. Deliver: Polished output

---

**Ready to start?** Load `references/vs-core-technique.md` to begin using VS.
