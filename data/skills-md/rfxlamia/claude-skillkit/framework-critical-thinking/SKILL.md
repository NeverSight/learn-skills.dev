---
name: framework-critical-thinking
description: Architectural framework for building AI agents with critical thinking capabilities - structured reasoning selection (CoT/ToT/GoT), metacognitive monitoring, self-verification, and cognitive bias detection. Use when building or enhancing AI agents that require reliable, self-correcting, and transparent reasoning.
---

# Framework Critical Thinking Framework (FCT)

## Overview

Critical Thinking Framework (FCT) provides architectural components for building AI agents with metacognition and self-correction capabilities. This framework integrates state-of-the-art techniques such as Chain-of-Thought, Tree-of-Thoughts, and self-verification to produce more reliable and transparent reasoning.

**When to use this skill:**
- Building AI agents for complex tasks requiring multi-step reasoning
- Implementing self-correction and error detection in agent workflows
- Selecting the appropriate reasoning method (CoT vs ToT vs GoT) based on task characteristics
- Adding metacognitive monitoring to improve reliability
- Reducing hallucination and reasoning errors in AI outputs

**Triggers:** Use this skill when the user requests help with:
- "build an agent that can self-correct"
- "implement better reasoning"
- "reduce hallucination in AI system"
- "choose between CoT, ToT, or other reasoning methods"
- "add error detection to agent workflow"

## Core Capabilities

### 1. Reasoning Router
**File:** `references/reasoning_router.md`

Detects problem complexity and routes to the optimal reasoning method (CoT/ToT/GoT/Self-Consistency).

**Use cases:**
- Straightforward task with single solution path → CoT
- Complex task with multiple viable paths → ToT (BFS/DFS)
- Task with interconnected reasoning → GoT
- Critical task requiring verification → Self-Consistency

### 2. Metacognitive Monitor
**File:** `references/metacognitive_monitor.md`

Self-assessment and error detection in the reasoning process. Implements the Producer-Critic pattern for continuous quality control.

**Key features:**
- Confidence scoring per reasoning step
- Anomaly detection in thought patterns
- Reflection trigger conditions
- Human handoff protocols

### 3. Self-Verification
**File:** `references/self_verification.md`

Implementation of Chain-of-Verification (CoVe) and other self-verification techniques to validate outputs before delivery.

**Methods covered:**
- Chain-of-Verification (CoVe)
- Self-Refine loops
- Backward verification
- Cross-verification with external sources

### 4. Bias Detector
**File:** `references/bias_detector.md`

Detection of cognitive bias in the reasoning process and mitigation strategies.

**Bias types covered:**
- Confirmation bias
- Anchoring bias
- Availability heuristic
- Framing effects
- Recency bias

### 5. Producer-Critic Orchestrator
**File:** `references/producer_critic_orchestrator.md`

Pattern for orchestrating Generate-Critique-Refine cycles in agent workflows.

**Architecture:**
- Master Agent (orchestrator)
- Producer Agent (generation)
- Critic Agent (evaluation)
- Refinement loops with budget constraints

### 6. Memory Curator
**File:** `references/memory_curator.md`

Management of episodic memory with quality weighting to prevent memory pollution from bad episodes.

**Features:**
- Quality-weighted memory storage
- Experience replay for learning
- Memory consolidation strategies
- Selective retention policies

### 7. Reasoning Validator
**File:** `references/reasoning_validator.md`

Logical consistency checker and structural validation for reasoning chains.

**Validation types:**
- Logical consistency checks
- Structural completeness
- Assumption validation
- Contradiction detection

### 8. Reflection Trigger
**File:** `references/reflection_trigger.md`

Rule-based triggers to activate self-correction loops based on specific conditions.

**Trigger conditions:**
- Confidence threshold violations
- Repeated action patterns
- Latency spikes
- Complexity indicators

## Workflow Decision Tree

```
User Request: Build/improve AI agent with critical thinking

├─ Step 1: Analyze Task Complexity
│  ├─ Simple, single-path → Use CoT (Chain-of-Thought)
│  ├─ Complex, multi-path → Use ToT (Tree-of-Thoughts)
│  ├─ Interconnected → Use GoT (Graph-of-Thoughts)
│  └─ Critical, needs verification → Use Self-Consistency
│
├─ Step 2: Implement Metacognitive Layer
│  ├─ Add confidence scoring
│  ├─ Set up reflection triggers
│  └─ Configure human handoff thresholds
│
├─ Step 3: Add Self-Verification
│  ├─ Implement CoVe for factual claims
│  ├─ Add backward verification for math/logic
│  └─ Setup cross-verification if external sources available
│
├─ Step 4: Integrate Bias Detection
│  ├─ Check for confirmation bias
│  ├─ Validate assumption diversity
│  └─ Apply mitigation strategies
│
└─ Step 5: Setup Memory & Learning
   ├─ Configure episodic memory
   ├─ Setup quality weighting
   └─ Implement experience replay
```

## Quick Reference: Reasoning Method Selection

| Task Characteristic | Recommended Method | Cost | Accuracy |
|---------------------|-------------------|------|----------|
| Simple, linear | CoT | Low | Good |
| Complex planning | ToT-BFS | High | Very Good |
| Deep reasoning | ToT-DFS | High | Very Good |
| Interconnected | GoT | Very High | Excellent |
| Critical decisions | Self-Consistency | Very High | Excellent |
| Factual claims | CoVe | Medium | Good |

## Implementation Example

```python
# Pseudo-code for agent with ACT-F

class CriticalThinkingAgent:
    def __init__(self):
        self.reasoning_router = ReasoningRouter()
        self.metacognitive_monitor = MetacognitiveMonitor()
        self.self_verifier = SelfVerification()
        self.bias_detector = BiasDetector()

    async def solve(self, problem):
        # Step 1: Route to appropriate method
        method = self.reasoning_router.select(problem)

        # Step 2: Generate with monitoring
        thoughts = []
        for step in method.generate(problem):
            confidence = self.metacognitive_monitor.assess(step)
            if confidence < THRESHOLD:
                step = self.reflect_and_improve(step)
            thoughts.append(step)

        # Step 3: Self-verification
        verified = self.self_verifier.verify(thoughts)

        # Step 4: Bias check
        if self.bias_detector.detect(verified):
            verified = self.bias_detector.mitigate(verified)

        return verified
```

## Resources

### references/
Complete documentation for each ACT-F component:

- `reasoning_router.md` - Reasoning method selection (P0)
- `metacognitive_monitor.md` - Self-assessment and monitoring (P0)
- `self_verification.md` - Output verification techniques (P0)
- `bias_detector.md` - Bias detection and mitigation (P0)
- `producer_critic_orchestrator.md` - Generate-critique-refine pattern (P1)
- `memory_curator.md` - Memory management (P1)
- `reasoning_validator.md` - Logical validation (P1)
- `reflection_trigger.md` - Trigger conditions (P1)
- `uncertainty_quantifier.md` - Confidence calibration (P2)
- `fallback_handler.md` - Graceful degradation (P2)

### scripts/
Utilities and templates for implementation (optional).

---

**Sources:**
- [Tree of Thoughts: Branching Reasoning for LLMs](https://www.emergentmind.com/topics/tree-of-thoughts-tot)
- [AI Agents: Metacognition for Self-Aware Intelligence - Microsoft](https://techcommunity.microsoft.com/blog/educatordeveloperblog/ai-agents-metacognition-for-self-aware-intelligence---part-9/4402253)
- [Self-Verification-Based LLMs](https://www.emergentmind.com/topics/self-verification-based-llms)
- [Cognitive Architecture in AI](https://sema4.ai/learning-center/cognitive-architecture-ai/)
