---
name: karpathy-llm-simulator
description: 'Use LLM as a simulator of expert debates and opposing viewpoints instead of getting a single sycophantic answer. Use this skill when the user needs to make an important decision, wants to stress-test an idea, needs devil''s advocate analysis, wants to avoid confirmation bias, or says "argue against this", "what are the counterarguments", "simulate experts", "debate this", "challenge my thinking". Based on Karpathy 31k-like post.'
disable-model-invocation: false
user-invocable: true
related_skills:
  - karpathy-understanding-first
  - karpathy-system-prompt-learning
  - karpathy-meta-reflection
---

# Skill 3: LLM as Simulator（LLM模拟器思维）

> Source: https://x.com/karpathy/status/2037921699824607591 | https://x.com/karpathy/status/2049907410303865030
> "Drafted a blog post → LLM argue the opposite" — 31k likes

## Core Principle

**Don't ask what the LLM thinks. Ask it to simulate what a diverse group of experts would argue.**

LLMs are trained to please. A direct question gets a sycophantic answer. A simulation request gets a distribution of real perspectives — including the uncomfortable ones.

Karpathy's method: write a draft → ask LLM to argue the strongest possible opposite position → synthesize a better view.

## The 4 Simulator Modes

### Mode 1: Expert Debate Panel
Best for: technical decisions, architecture choices, research directions

```
Simulate a structured debate between these 3 expert personas on [TOPIC/DECISION]:

Expert A: [most optimistic / pro position]
Expert B: [most skeptical / con position]  
Expert C: [pragmatic outsider / unexpected angle]

For each expert:
- State their core argument in 3 sentences
- Cite 2 specific examples or data points they'd use
- Identify what they'd say is the FATAL FLAW in the opposing view

After the debate, synthesize: what's the strongest hybrid position that survives all three critiques?

Topic: [YOUR_TOPIC]
My current position: [YOUR_DRAFT_VIEW]
```

### Mode 2: Steel Man the Opposite
Best for: before publishing, before committing to a decision

```
I'm about to [ACTION / PUBLISH / DECIDE]:

[YOUR PLAN OR DRAFT]

Steel man the strongest possible argument AGAINST this. Be merciless.
Don't hedge. Don't say "while this has merit...". 
Argue as if you genuinely believe the opposite and need to convince a skeptical expert.

Then: what would it take to make my original position survive this attack?
```

### Mode 3: Pre-Mortem Simulation
Best for: project planning, product launches, major decisions

```
Imagine it's [DATE 6 MONTHS FROM NOW] and [YOUR PROJECT/PLAN] has failed completely.

Simulate 3 different failure modes — each from a different root cause:
1. Technical failure: what went wrong in the implementation?
2. Strategic failure: what assumption proved wrong?
3. Execution failure: what human/process error occurred?

For each: describe the specific sequence of events that led to failure.

Then: what early warning signals would have been visible by [DATE 1 MONTH FROM NOW]?
```

### Mode 4: Socratic Drill
Best for: testing your own understanding of a concept

```
I believe I understand [CONCEPT]. 

Ask me 5 increasingly hard Socratic questions to test my understanding.
After each answer I give, probe a potential gap or inconsistency.
At the end, grade my understanding on a scale of 1-10 and identify my biggest blind spot.

Start with question 1.
```

## Anti-Sycophancy Patterns

Always add one of these to prevent the LLM from capitulating to your framing:

- `"Do not soften your critique because you think I want to hear it."`
- `"If my position is clearly wrong, say so directly."`
- `"Ignore that I wrote the original draft — evaluate it as an anonymous submission."`
- `"Your job is to find the fatal flaw, not to validate."`

## Decision Framework

```
Before any major decision:
1. Write down your current position (1-2 paragraphs)
2. Run Mode 2 (Steel Man the Opposite)
3. Update your position based on the strongest critique
4. Run Mode 1 (Expert Debate) to get broader perspective
5. Make the decision — now you've genuinely stress-tested it

Total time: 15-20 minutes. Quality of decision: dramatically better.
```

## When NOT to Use This

- For factual lookups (just ask directly)
- For code generation (use agentic engineering instead)
- When you've already decided and need to execute (move forward, don't ruminate)

## Workflow

**属于工作流：反偏见决策（任何重要判断）**

| 位置 | 上游 | 下游 |
|------|------|------|
| 入口 | 用户面临重要决策时直接触发 | `karpathy-understanding-first`（验证自己是否真正理解） |

完整链路：`llm-simulator → understanding-first → system-prompt-learning`

也在月度体检工作流中用于 stress-test 月度结论。

## Prompt Contract

```text
Simulate a structured debate between 3-5 expert personas with conflicting incentives on <DECISION/TOPIC>. Each persona must: state their core argument, cite specific evidence, identify the fatal flaw in opposing views. After the debate, synthesize the strongest hybrid position that survives all critiques. End with: key assumptions I must verify myself.
```

## Verification Checklist

- [ ] 至少有 3 个角色，且利益/立场互相冲突
- [ ] 每个角色都给出了具体论据（不是泛泛而谈）
- [ ] 每个角色都指出了对方的致命缺陷
- [ ] 综合结论经受住了所有角色的攻击
- [ ] 列出了「我必须亲自验证」的假设清单
- [ ] 没有出现讨好用户原始立场的倾向
