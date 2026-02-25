---
name: prompt-engineering
description: 'Prompt engineering and agentic orchestration patterns. Use when crafting prompts for reasoning models, implementing chain-of-thought or Tree-of-Thoughts, designing ReAct loops, building few-shot examples, optimizing prompt performance, structuring system prompts, using extended thinking, or designing tool use workflows. Use for prompt templates, multi-step agent workflows, structured thinking protocols, and multimodal prompting.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering
user-invocable: false
---

# Prompt Engineering

Advanced prompt design for LLMs and autonomous agents. Covers reasoning patterns, template systems, optimization workflows, agentic orchestration, extended thinking, and tool use prompting.

**When to use**: Designing prompts that require structured reasoning, building agent loops, optimizing LLM output quality, creating reusable prompt templates, configuring extended thinking for complex tasks, or designing multimodal prompts with images and text.

**When NOT to use**: Simple factual queries, direct lookups, or creative writing that benefits from open-ended generation.

## Key Principles

1. **Explicit over implicit** -- Modern models (Claude 4.x, GPT-4.1) follow instructions literally. Be specific about desired output, format, and behavior rather than relying on the model to infer intent.
2. **Objective over instruction** -- For reasoning models (OpenAI o-series, Claude with extended thinking), state the goal rather than prescribing step-by-step methods. These models plan natively.
3. **Structure signals intent** -- Use XML tags, clear delimiters, and consistent formatting to communicate prompt structure. Models trained on structured prompts parse them more reliably than plain text.
4. **One good example beats many rules** -- Few-shot examples with consistent formatting anchor model behavior more effectively than verbose instructions.
5. **Feedback loops are built-in** -- Design prompts that ask the model to verify, critique, or score its own output before finalizing.
6. **Token economy matters** -- Every extra token adds latency and cost. Compress context, remove filler, and front-load critical information.

## Model-Specific Considerations

**Claude 4.x models** follow instructions with high precision. They take prompts literally and do exactly what is asked -- no more, no less. Use XML tags to structure prompt sections (`<rules>`, `<context>`, `<output_format>`). Frame instructions positively (describe what to do, not what to avoid). Provide context or motivation behind instructions so Claude can generalize. Extended thinking and interleaved thinking provide native reasoning capabilities.

**OpenAI o-series models** (o3, o4-mini) use internal reasoning tokens before responding. Use developer messages instead of system messages. Write detailed function descriptions as interface contracts. Do not add explicit reasoning prompts -- these models reason natively and additional planning prompts can hurt performance. Pass back persisted reasoning items for multi-turn conversations.

**GPT-4.1 and standard models** benefit from explicit step-by-step instructions, few-shot examples, and structured output schemas. These models do not have native reasoning loops, so CoT prompting and structured thinking protocols add measurable value.

**Multimodal models** (GPT-4o, Claude with vision, Gemini) accept images alongside text. Provide context about what each image represents, use clear action verbs, and crop images to relevant regions. Label multiple images explicitly and specify their relationship.

## Quick Reference

| Pattern              | API / Technique                           | Key Point                                      |
| -------------------- | ----------------------------------------- | ---------------------------------------------- |
| Zero-shot CoT        | `"Let's think step by step"` trigger      | Elicits reasoning without examples             |
| Few-shot CoT         | Explicit reasoning chain examples         | One good example beats many rules              |
| Self-consistency     | Multiple paths + majority vote            | Higher accuracy on complex tasks               |
| Tree-of-Thoughts     | Generate 3+ strategies, eliminate weakest | Parallel exploration with pruning; high cost   |
| ReAct loop           | Thought-Action-Observation cycle          | Agent reasons and acts in unison               |
| System prompt        | Role + Expertise + Guidelines + Format    | Foundation for all LLM behavior                |
| Prompt template      | Modular composition with variable slots   | Reusable, validated, cacheable                 |
| A/B testing          | Statistical comparison of prompt variants | Isolate variables, measure significance        |
| Extended thinking    | Budget-controlled deep reasoning (Claude) | Let model think before responding              |
| Interleaved thinking | Think between tool calls (Claude 4)       | Reason after each tool result                  |
| Think tool           | No-op tool for structured reasoning space | Gives agents a place to reason mid-turn        |
| Reasoning models     | Objective-based prompting for o3/o4-mini  | Let the model plan its own reasoning           |
| Structured thinking  | Understanding-Analysis-Execution protocol | Forces verification before acting              |
| XML structuring      | Tags to delimit prompt sections           | Models parse structured prompts reliably       |
| Multimodal prompting | Text + image context for vision models    | Provide spatial context and clear action verbs |
| Confidence scoring   | Model self-reports certainty per claim    | Quantifies reliability of output               |
| Token optimization   | Compress context, remove filler words     | Reduce latency and cost                        |

## Common Mistakes

| Mistake                                                | Correct Pattern                                                     |
| ------------------------------------------------------ | ------------------------------------------------------------------- |
| Overloading a single prompt with too many instructions | Use hierarchical rules with clear priority ordering                 |
| Forcing rigid step-by-step on reasoning models         | Use objective-based prompts; reasoning models plan natively         |
| Setting max output tokens too low for reasoning models | Allocate sufficient tokens for internal chain-of-thought            |
| Using static examples for complex tasks                | Select examples dynamically via semantic similarity                 |
| Inconsistent formatting across few-shot examples       | All examples must follow identical input-output structure           |
| Manually parsing unstructured LLM output               | Use JSON mode or structured output schemas                          |
| Ignoring token budget allocation                       | Reserve tokens for system prompt, examples, input, and response     |
| Skipping baseline measurement before optimizing        | Establish metrics first, then change one variable at a time         |
| Using CoT prompts on reasoning models                  | Redundant; these models reason natively without explicit triggers   |
| Telling models what NOT to do instead of what to do    | Frame instructions positively: describe the desired behavior        |
| Passing thinking blocks back as user text (Claude)     | Pass thinking blocks unmodified in assistant message only           |
| Over-prompting reasoning models to "plan more"         | Additional planning prompts can degrade reasoning model performance |

## Prompt Engineering Workflow

1. **Define the objective** -- State what the prompt should achieve and how success is measured
2. **Choose the right pattern** -- Match the task to CoT, ReAct, ToT, or simple prompting based on complexity
3. **Select the model tier** -- Route to lightweight, standard, or reasoning models based on task difficulty
4. **Write the baseline prompt** -- Start simple; use system prompt structure with XML tags for complex cases
5. **Add examples** -- Include 1-3 few-shot examples with consistent formatting if the task requires them
6. **Test and measure** -- Establish baseline metrics (accuracy, latency, token usage) on representative inputs
7. **Analyze failures** -- Categorize errors (format, factual, logical, incomplete) and address the most impactful
8. **Iterate one variable** -- Change one element at a time to isolate what improves performance
9. **Version and deploy** -- Track prompt versions alongside performance data for rollback capability

## Delegation

- **Explore prompt variants and compare model responses**: Use `Explore` agent to test prompt strategies across different inputs
- **Build multi-step agentic workflows with tool use**: Use `Task` agent to implement and validate ReAct loops and autonomous chains
- **Design hierarchical prompt architecture for complex systems**: Use `Plan` agent to structure prompt systems with verification loops

> If the `expert-instruction` skill is available, delegate system prompt design and agent persona crafting to it.

## References

- [Chain-of-Thought](references/chain-of-thought.md) -- Step-by-step reasoning, self-consistency, least-to-most decomposition
- [Few-Shot Learning](references/few-shot-learning.md) -- Example selection strategies, token-aware truncation, edge cases
- [Prompt Templates](references/prompt-templates.md) -- Template architecture, modular composition, validation, caching
- [Prompt Optimization](references/prompt-optimization.md) -- A/B testing, failure analysis, metrics, version control
- [System Prompts](references/system-prompts.md) -- Role definition, constraint specification, dynamic adaptation
- [Reasoning Model Optimization](references/reasoning-model-optimization.md) -- Objective-based prompting for o3/o4-mini, extended thinking configuration
- [Tree-of-Thoughts](references/tree-of-thoughts.md) -- Parallel branch exploration, evaluation, synthesis
- [ReAct Patterns](references/react-patterns.md) -- Thought-Action-Observation loop, tool discovery, error recovery
- [Structured Thinking](references/structured-thinking.md) -- Adversarial critic protocol, confidence scoring, metadata tagging
- [Extended Thinking and Tool Use](references/extended-thinking.md) -- Budget configuration, interleaved thinking, think tool pattern
- [Multimodal Prompting](references/multimodal-prompting.md) -- Vision model techniques, image context, cross-modal alignment
