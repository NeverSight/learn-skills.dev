---
name: karpathy-education-first
description: 'Apply the education-first mindset — make everything you build teachable, create nano-project explanations, write for beginners. Use this skill when the user wants to explain a project to beginners, create a tutorial from code, write documentation that teaches (not just documents), make a concept accessible, or says "make this teachable", "explain like im a beginner", "nano project version", "teaching version", "explain from scratch", "blog post about this". Based on Karpathy 243-line GPT and Eureka Labs posts.'
disable-model-invocation: false
user-invocable: true
related_skills:
  - karpathy-output-evolution
  - karpathy-practice-environments
  - karpathy-llm-wiki
  - karpathy-autoresearch
---

# Skill 12: Education-First Mindset（教育至上）

> Source: https://x.com/karpathy/status/2021694437152157847 | https://x.com/karpathy/status/2056753169888334312
> 243-line pure Python GPT | "education热情不变" even at Anthropic

## Core Principle

**If you can't teach it, you don't own it. Make everything a nano-project.**

Karpathy's signature move: take a complex system and reimplement it from scratch in minimal, readable code with maximal explanation. Not for production. For understanding.

The 243-line GPT wasn't the fastest implementation. It was the most comprehensible implementation. That's the goal.

## The Teaching Version Prompt

After completing any project, generate its teaching version:

```
I just built [PROJECT/CONCEPT]. Now create a teaching version of it.

[PASTE CODE OR DESCRIBE PROJECT]

Teaching version requirements:
1. Target audience: curious beginner who knows [PREREQUISITE LEVEL]
2. Start with: "Here's what we're building and why it matters" (2 paragraphs)
3. Walk through the code line-by-line in the most important sections
4. For every non-obvious decision: add a comment explaining WHY, not just WHAT
5. Add a "Try this yourself" section at the end with 3 small exercises
6. Maximum complexity rule: if a beginner would say "wait, what?" — add an explanation

Output: the teaching version as a complete annotated script or tutorial.
```

## The Nano-Project Pattern

Karpathy's approach to making anything understandable:

```
Create a nano-project that demonstrates [COMPLEX CONCEPT].

Rules:
- Under 200 lines of code (pure Python / stdlib preferred)
- Zero external dependencies
- Every line earns its place
- Annotated: inline comments explain the key insight of each section
- Complete: runs from scratch, shows meaningful output
- Pedagogical: the code's structure mirrors the concept's structure

The concept to demonstrate: [CONCEPT]
What should the reader understand after running this? [LEARNING GOAL]

Also provide:
- 3-sentence explanation at the top of the file
- What to try next (3 suggestions for extending it)
```

## The "Explain Like Karpathy" Prompt

For explaining any technical concept:

```
Explain [CONCEPT] the way Karpathy would explain it — clear, direct, minimal jargon, example-first.

Format:
1. The one-sentence intuition (what it IS, not what it does)
2. The simplest possible concrete example (with actual numbers or code)
3. Why it matters (1-2 sentences, no hype)
4. The common misconception most people have about it
5. If you want to go deeper: [3 resources, ordered by accessibility]

Audience: [DESCRIBE YOUR READER]
```

## Documentation That Teaches

Transform technical documentation from reference to tutorial:

```
Rewrite this documentation to be educational, not just informational.

Current docs:
[PASTE DOCUMENTATION]

Rewrite rules:
1. Lead with a concrete example, not with definitions
2. Explain each parameter with: what it does + why you'd change it + what the default is and why
3. Add a "Common patterns" section showing 3 real use cases
4. Add a "Common mistakes" section showing 3 errors people make and how to fix them
5. Keep all technical accuracy; only improve pedagogical structure
6. Add: "After reading this, you should be able to [LEARNING GOAL]" at the top
```

## The Blog Post Generator

For turning any project into a shareable piece of teaching content:

```
Write a technical blog post about [PROJECT/INSIGHT].

Style: Karpathy-style — direct, precise, example-driven, opinionated.

Structure:
1. Hook: why does this matter RIGHT NOW? (1-2 punchy sentences)
2. The core insight: one thing that changes how you think about [topic]
3. Show, don't tell: working code example that demonstrates the insight
4. What I tried that didn't work (builds credibility + saves readers time)
5. What I learned: 3-5 concrete takeaways, actionable
6. What's next: 2-3 things worth exploring

Tone:
- First person, direct
- Specific (exact line counts, benchmark numbers, actual errors)
- Skeptical of hype, enthusiastic about substance
- Never say "in conclusion" or "in summary" — just end when you're done

Audience: [WHO WILL READ THIS]
Length: [~1000 words for blog / ~500 for Twitter thread / ~300 for Gist]
```

## Making Complex Research Accessible

For distilling papers or research into teachable content:

```
Distill this [paper/research/concept] into a teachable explainer.

Source: [PASTE ABSTRACT OR KEY SECTIONS]

Output:
1. ELI5 version: explain to a smart non-expert in 3 sentences
2. Key insight: what's the one thing this paper figured out?
3. The method in plain language: how did they do it? (no equations, just logic)
4. Why it matters: what does this enable that wasn't possible before?
5. The catch: what are the limitations or assumptions?
6. Nano-project idea: how could someone understand this by building a tiny version?
```

## Teaching Code Review Checklist

When reviewing code with education-first lens:

```markdown
Is this code teachable?
- [ ] Can a motivated beginner understand what it does in 5 minutes?
- [ ] Does each function have a comment explaining WHY, not just what?
- [ ] Are variable names descriptive enough to read like documentation?
- [ ] Is there a README that explains how to run it from scratch?
- [ ] Does it have at least one worked example in the comments?
- [ ] Are the non-obvious parts explained?

If any box is unchecked: the code isn't done yet.
```

## Workflow

**属于工作流：研究到发布（终点）+ 工作流：月度体检（终点）**

| 位置 | 上游 | 下游 |
|------|------|------|
| B的第4步 | karpathy-output-evolution（包装完成后） | 发布/分享 |
| D的第4步 | karpathy-practice-environments（练习后） | 教程输出 |

研究到发布链路：autoresearch → llm-wiki → output-evolution → education-first
月度体检链路：meta-reflection → understanding-first → practice-environments → education-first

## Prompt Contract

```text
Convert <PROJECT_OR_CONCEPT> into a teaching version for beginners. Produce: 1) Core concept in one sentence, 2) Minimal runnable example (< 300 lines, no hidden deps), 3) Step-by-step walkthrough (explain WHY not just WHAT), 4) 3-5 progressive exercises (easy→hard), 5) Common misconceptions and how to check if you fell into them.
```

## Verification Checklist

- [ ] 核心概念用一句话能说清
- [ ] 最小可运行示例确实能跑（< 300 行，无隐藏依赖）
- [ ] walkthrough 解释了 WHY，不只是 WHAT
- [ ] 练习题有递进难度
- [ ] 常见误区有自检方法
- [ ] 零基础读者能在 5 分钟内理解第一步
