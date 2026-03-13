---
name: chain-of-thought
description: Inject structured reasoning blocks into prompts to encourage step-by-step thinking. Use when tasks require complex problem-solving, multi-step reasoning, planning, analysis, or when you need the model to show its work and reflect on decisions before providing answers.
---

# Chain of Thought Reasoning

## Purpose

This skill enables structured, transparent reasoning by injecting chain of thought (CoT) blocks into prompts. It encourages the model to think step-by-step, explicitly show reasoning processes, and separate thinking from final outputs.

Chain of thought reasoning improves:
- **Problem-solving accuracy** - Breaking down complex problems into manageable steps
- **Transparency** - Making reasoning visible and auditable
- **Self-correction** - Allowing the model to catch and fix errors during reasoning
- **Planning** - Enabling reflection and iterative plan refinement
- **Debugging** - Understanding how conclusions were reached

## When to Use

Activate this skill for tasks that benefit from explicit reasoning:

- **Complex problem-solving** - Multi-step mathematical, logical, or analytical problems
- **Code analysis** - Understanding unfamiliar codebases, debugging, or architecture decisions
- **Planning and design** - Breaking down features, designing systems, or creating implementation plans
- **Research tasks** - Synthesizing information from multiple sources
- **Decision-making** - Evaluating trade-offs between multiple approaches
- **Error diagnosis** - Investigating bugs or unexpected behavior
- **Refactoring** - Reasoning about code improvements and their implications
- **Any task where "showing your work" leads to better outcomes**

## How It Works

Chain of thought uses XML tags to demarcate reasoning and output sections:

### Primary Structure

```xml
<thinking>
Step 1: [Analyze the problem]
- What are we trying to accomplish?
- What information do we have?
- What's missing?

Step 2: [Break down the approach]
- What are the main steps?
- What are potential challenges?

Step 3: [Evaluate options]
- Option A: pros and cons
- Option B: pros and cons
- Decision: [chosen approach and why]

Step 4: [Verify reasoning]
- Does this make sense?
- Are there edge cases?
- What could go wrong?
</thinking>

<answer>
[Clear, concise final output based on the reasoning above]
</answer>
```

### Advanced Structure for Multi-Agent Systems

Inspired by the Manus AI multi-agent system, use nested thinking for complex workflows:

```xml
<thinking>
## Initial Analysis
[First pass understanding]

## Plan Formation
Current plan:
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Reflection
Is this plan optimal?
- Consideration 1: [reflection]
- Consideration 2: [reflection]

## Plan Update
Revised plan:
1. [Updated step 1]
2. [Updated step 2]
3. [New step 3]

Rationale for changes: [explanation]

## Execution Strategy
How to implement step 1:
- [Details]
- [Considerations]
</thinking>

<answer>
[Final output incorporating refined thinking]
</answer>
```

## Prompt Injection Patterns

### Pattern 1: Problem-Solving Template

```
<thinking>
1. Problem understanding:
   - Given: [what we know]
   - Goal: [what we need to find/do]
   - Constraints: [limitations]

2. Approach:
   - Strategy: [chosen method]
   - Why: [rationale]

3. Step-by-step execution:
   - [Step 1 with reasoning]
   - [Step 2 with reasoning]
   - [Step 3 with reasoning]

4. Verification:
   - Does the solution meet requirements?
   - Are there edge cases?
</thinking>

<answer>
[Solution]
</answer>
```

### Pattern 2: Code Analysis Template

```
<thinking>
1. Code structure overview:
   - Main components: [list]
   - Data flow: [description]

2. Key observations:
   - Pattern 1: [what and why]
   - Pattern 2: [what and why]

3. Analysis:
   - [Detailed reasoning about the code]

4. Conclusion:
   - [Synthesis of findings]
</thinking>

<answer>
[Clear explanation or recommendation]
</answer>
```

### Pattern 3: Planning Template

```
<thinking>
1. Requirements analysis:
   - Must have: [core requirements]
   - Nice to have: [optional features]

2. Initial plan:
   [List of steps]

3. Risk assessment:
   - Risk 1: [description and mitigation]
   - Risk 2: [description and mitigation]

4. Plan refinement:
   [Updated plan based on risks]

5. Validation:
   - Does this plan address all requirements?
   - Is it feasible?
   - What assumptions are we making?
</thinking>

<answer>
[Final plan with clear action items]
</answer>
```

## Guidelines

### 1. Structure Your Thinking

- **Start with understanding** - State what you know and what you need to find out
- **Break down complex tasks** - Divide into smaller, manageable pieces
- **Show your work** - Write out intermediate steps, not just conclusions
- **Be explicit** - State assumptions, trade-offs, and reasoning clearly

### 2. Use Reflection

- **Question your approach** - "Is this the best way?"
- **Check your logic** - "Does this reasoning hold up?"
- **Consider alternatives** - "What other approaches exist?"
- **Update your plan** - Don't be afraid to revise based on new insights

### 3. Separate Thinking from Output

- **Thinking block** - For exploration, reasoning, and working through problems
- **Answer block** - For the polished, final response
- **Keep thinking raw** - Don't over-polish; show genuine reasoning
- **Keep answers concise** - User sees the answer; thinking is internal

### 4. When to Use Each Block

**Use `<thinking>` for:**
- Analyzing requirements
- Breaking down problems
- Evaluating options
- Working through logic
- Planning implementation
- Reflecting on decisions
- Catching errors
- Exploring trade-offs

**Use `<answer>` for:**
- Final recommendations
- Implemented solutions
- Clear explanations
- Action items
- Conclusions

### 5. Best Practices

- **Be honest in thinking** - If uncertain, say so
- **Show error correction** - If you notice a mistake, correct it in the thinking block
- **Use markdown** - Format thinking blocks for readability
- **Number your steps** - Makes reasoning easier to follow
- **Summarize in answer** - Don't make users read all thinking to get the point

## Examples

### Example 1: Debugging a Problem

**Prompt:** "This function is returning incorrect results for negative numbers. Can you fix it?"

```xml
<thinking>
1. Understanding the problem:
   - Function works for positive numbers
   - Fails for negative numbers
   - Need to identify why negatives cause issues

2. Code analysis:
   - [Read through the function]
   - Line 15: Uses Math.abs() - converts negative to positive
   - Line 20: Returns result without sign restoration
   - Aha! The absolute value removes the sign, but we never restore it

3. Solution approach:
   - Option A: Track sign separately and reapply
   - Option B: Handle negative numbers differently
   - Choosing A: cleaner and preserves existing logic

4. Implementation plan:
   - Store original sign
   - Apply absolute value for calculation
   - Multiply result by original sign
</thinking>

<answer>
The bug is on lines 15-20. The function uses `Math.abs()` but never restores the original sign. Here's the fix:

```javascript
const sign = num < 0 ? -1 : 1;
const absNum = Math.abs(num);
// ... existing calculation ...
return result * sign;
```
</answer>
```

### Example 2: Choosing Between Architectures

**Prompt:** "Should we use microservices or a monolith for this project?"

```xml
<thinking>
1. Context gathering:
   - Team size: small (3 developers)
   - Project scope: MVP with planned growth
   - Timeline: 3 months to launch
   - Infrastructure: cloud-based

2. Microservices analysis:
   Pros:
   - Scalability per service
   - Independent deployment
   - Technology flexibility

   Cons:
   - Operational complexity (DevOps overhead)
   - Network latency
   - Distributed debugging challenges
   - Over-engineering for small team

3. Monolith analysis:
   Pros:
   - Simpler deployment
   - Easier debugging
   - Faster initial development
   - Single codebase

   Cons:
   - Scaling requires scaling entire app
   - Potential coupling issues
   - May need to break apart later

4. Decision reasoning:
   - Small team → simpler is better
   - MVP timeline → need speed
   - Planned growth → can refactor later
   - Monolith-first approach is lower risk

5. Recommendation:
   Start with modular monolith, design for eventual extraction
</thinking>

<answer>
For your project, I recommend starting with a **modular monolith**:

**Why:**
- Your small team will move faster without microservices overhead
- 3-month MVP timeline needs simplicity
- You can refactor to microservices later if needed

**Key principle:** Design modules with clear boundaries (separate folders, interfaces) so future extraction is easier.

**Action items:**
1. Structure code in domain modules (auth, payments, users)
2. Use dependency injection for loose coupling
3. Plan data models to avoid cross-module dependencies
</answer>
```

### Example 3: Multi-Step Implementation Planning

**Prompt:** "Add user authentication with OAuth to our app"

```xml
<thinking>
## Initial Analysis
Requirements:
- OAuth integration (which providers? assuming Google/GitHub)
- User session management
- Protected routes
- Existing app: appears to be Express.js based

## Plan Formation v1
1. Choose OAuth library
2. Set up OAuth credentials
3. Implement login/logout routes
4. Add session middleware
5. Protect existing routes

## Reflection
Issues with v1:
- Didn't consider token storage
- No user database integration mentioned
- Missing error handling strategy
- Should address CSRF protection

## Plan Formation v2
1. Research codebase for existing auth patterns
2. Choose OAuth library (passport.js likely best for Express)
3. Set up database schema for users
4. Configure OAuth providers (Google, GitHub)
5. Implement authentication routes
6. Add session management with secure tokens
7. Create auth middleware for protected routes
8. Add CSRF protection
9. Implement logout and session cleanup
10. Add error handling for auth failures

## Execution Strategy for Step 1
Need to:
- Check if passport.js already installed
- Look for existing user models
- Identify protected routes
- Check current session handling
</thinking>

<answer>
I'll implement OAuth authentication. Let me start by researching your current codebase to understand existing patterns, then proceed with the implementation plan:

1. Audit current auth patterns
2. Set up passport.js with OAuth strategies
3. Create user database schema
4. Implement login/logout flows
5. Add session management
6. Protect routes with auth middleware
7. Add security measures (CSRF, secure tokens)

Starting with codebase research...
</answer>
```

## Integration with Multi-Agent Systems

In multi-agent architectures like Manus AI, chain of thought enables:

- **Agent reflection** - Agents explicitly reason about their actions before executing
- **Plan updating** - Agents revise strategies based on intermediate results
- **Inter-agent communication** - Thinking blocks provide transparency for coordination
- **Error recovery** - Agents can detect issues during reasoning and adapt

Agents can maintain persistent thinking across multiple turns:

```xml
<thinking>
## Turn 1 Reflection
Previous attempt: [what was tried]
Result: [what happened]
Learning: [what we discovered]

## Updated Strategy
Based on the failure, trying new approach:
[revised plan]
</thinking>

<answer>
[Action based on updated thinking]
</answer>
```

## References

For detailed examples and advanced patterns, see:
- [REFERENCE.md](references/REFERENCE.md) - Extended examples and patterns
- [XML Guide Conventions](references/XML-GUIDE.md) - Proper XML tag usage

## Summary

Chain of thought reasoning makes AI behavior more:
- **Transparent** - You can see how conclusions were reached
- **Reliable** - Step-by-step reduces errors
- **Debuggable** - Easy to spot where reasoning went wrong
- **Adaptive** - Reflection enables plan updates

Use this skill whenever explicit reasoning improves outcomes.
