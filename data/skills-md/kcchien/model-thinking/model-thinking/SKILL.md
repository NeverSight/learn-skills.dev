---
name: model-thinking
description: Mental models toolkit for clearer thinking, better decisions, and problem-solving. Use when users face complex problems, need decision support, want to analyze situations from multiple angles, organize information, understand systems, predict outcomes, or learn about specific mental models. Triggers include phrases like "help me think through", "analyze this problem", "what models apply here", "how should I decide", "evaluate options", or direct model references (e.g., "use second-order thinking", "apply inversion"). 中文觸發：「思維模型」、「幫我分析」、「決策分析」、「多角度思考」、「怎麼判斷」、「幫我想清楚」、「系統思考」、「風險評估」。
---

# Model Thinking

## Response Modes

| Mode | Trigger | Output |
|------|---------|--------|
| **Guided** | Ambiguous problem | Diagnostic questions → model recommendations |
| **Direct** | Clear problem or specific model requested | Structured multi-model analysis |
| **Teaching** | Wants to learn models | Model explanation + example + practice |

## Workflow

1. **Classify**: Decision? System? Strategy? Data? Learning?
2. **Select mode**: Ambiguous → Guided | Clear → Direct | Learning → Teaching
3. **Apply 2-3 models**: Primary insight + complementary views + blind spot check
4. **Deliver**: Key insights → Recommendations → Caveats

## Reference File Selection

| Problem Pattern | Primary | Also Consider |
|-----------------|---------|---------------|
| Choosing between options | [decisions.md](references/decisions.md) | economics.md, psychology.md |
| Understanding complex behavior | [systems.md](references/systems.md) | networks.md |
| Interpreting data, prediction | [statistics.md](references/statistics.md) | algorithms.md, risk.md |
| Competition, negotiation | [strategy.md](references/strategy.md) | psychology.md, economics.md |
| Human behavior, bias | [psychology.md](references/psychology.md) | economics.md |
| Connections, influence, platforms | [networks.md](references/networks.md) | economics.md, systems.md |
| Computational problem-solving | [algorithms.md](references/algorithms.md) | statistics.md |
| Uncertainty, tail events | [risk.md](references/risk.md) | statistics.md, psychology.md |
| Acquiring knowledge, skills | [learning.md](references/learning.md) | psychology.md |
| Markets, incentives | [economics.md](references/economics.md) | psychology.md, strategy.md |
| Cross-domain synthesis, model pairing | [combinations.md](references/combinations.md) | All domain files as needed |

## Guided Mode: Diagnostic Questions

When problem is ambiguous, ask 2-3 from relevant domain:

| Domain | Key Questions |
|--------|---------------|
| Decisions | Reversibility? (能不能反悔？) Time horizon? (影響多久？) Stakes? (賭注多大？) Stakeholders? (誰會受影響？) |
| Systems | Linear/non-linear? (結果跟投入成正比嗎？) Feedback loops? (有沒有自我強化或抑制的循環？) Delays? (行動到看見結果要多久？) Boundary? (問題的邊界畫在哪？) |
| Strategy | Players? (有哪些參與者？) Game type? (零和還是共贏？) Info asymmetries? (誰知道得比較多？) Incentives? (各方動機是什麼？) |
| Data | Sample size? (資料量夠嗎？) Base rate? (一般情況下機率多少？) Selection bias? (取樣有偏差嗎？) Signal vs noise? (訊號還是雜訊？) |
| Risk | Fat tail or thin tail? (極端事件常見嗎？) Reversible? (損害能恢復嗎？) Ruin possible? (有沒有全軍覆沒的可能？) |

## Direct Application Template

When applying models directly:

```markdown
## Analysis: [Problem Summary]

### Model Applied: [Model Name]
**Core Insight**: [One-sentence key takeaway]

**Application**:
[2-4 bullet points applying the model to the specific situation]

### Complementary View: [Second Model]
[Brief application showing different angle]

### Synthesis
- **Recommendation**: [Specific action]
- **Key Risk**: [What could go wrong]
- **Next Step**: [Immediate action to take]
```

## Teaching Mode Template

```markdown
## [Model Name]
**One-liner**: [Memorable summary]

**Core Concept**: [2-3 sentences]

**Example**: [Concrete scenario]

**When to Use**: [Situations]

**Common Mistake**: [Key pitfall to avoid]

**Practice Prompt**: [A question for the user to apply this model to their own situation]
```

## Multi-Model Synthesis Example

**Problem**: Should I accept this job offer?

| Model | Insight |
|-------|---------|
| **Regret Minimization** | At 80, would I regret not trying this path? |
| **Opportunity Cost** | What salary/growth/learning am I giving up? |
| **Reversibility** | One-way door or can I return to current field? |
| **Second-Order** | How does this affect family, health, skills in 5 years? |

**Synthesis**: High regret potential + acceptable opportunity cost + reversible → **Accept**

Use 2-3 models from different domains to triangulate. Agreement = confidence. Disagreement = complexity worth exploring.

## Critical Checks

Before finalizing any analysis:

1. **Inversion**: What would make this analysis wrong?
2. **Base Rate**: What typically happens in similar situations?
3. **Incentives**: Who benefits from each outcome?
4. **Second-Order Effects**: What happens next after the first-order effect?
5. **Falsifiability**: How would we know if we're wrong?

## Quick Reference: 10 Universal Models

> Detailed explanations and application examples for each model are in the reference files listed in the [Reference File Selection](#reference-file-selection) table above.

| Model | One-liner | Apply When |
|-------|-----------|------------|
| Inversion | Avoid stupidity rather than seek brilliance | Any decision |
| Second-Order Thinking | Then what? | Evaluating consequences |
| Opportunity Cost | What are you giving up? | Resource allocation |
| Base Rates | Prior probability matters | Any prediction |
| Feedback Loops | Effects become causes | System analysis |
| Margin of Safety | Build in buffers | Risk management |
| Incentives | Show me incentive, I show you outcome | Analyzing behavior |
| Map vs Territory | The model isn't reality | Any model use |
| Sunk Cost | Past costs are irrelevant | Decision-making |
| Explore/Exploit | Balance new vs known | Resource allocation |

For all models organized by domain, load reference files above. For multi-model combination strategies and cross-domain examples, see [combinations.md](references/combinations.md).
