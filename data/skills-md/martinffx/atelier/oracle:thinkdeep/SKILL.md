---
name: oracle:thinkdeep
description: Extended reasoning analysis using sequential thinking. Use for deep exploration, comprehensive analysis, complex decisions, or when you need fresh perspectives on difficult problems.
user-invocable: false
---

# ThinkDeep: Extended Reasoning Analysis

## Step 1: Parse Request Parameters

<strategist>
@agent-oracle

Analyze the thinkdeep request: $ARGUMENTS

**Parameter Extraction:**
- **Main prompt**: [extract core thinking request]
- **Focus areas**: [extract "architecture, performance, security" etc]
- **File references**: [extract "reference to file.py" patterns]
- **Problem context**: [extract additional context provided]

**Parsed Configuration:**
- Prompt: [core request]
- Focus areas: [identified areas]
- File references: [any files mentioned]
- Problem context: [additional context]
</strategist>

## Step 2: Deep Sequential Analysis

<strategist>
@agent-oracle

Use sequential thinking (mcp__sequential-thinking__sequentialthinking) for extended reasoning:

### Thought 1: Context Understanding
Analyze the current session context to understand:
- What has been discussed so far
- Previous decisions and analyses made
- User's specific constraints and goals
- Existing solutions or approaches tried

### Thought 2: Problem Decomposition
Break down the core issue into:
- Primary problem statement
- Key sub-problems or components
- Underlying assumptions and constraints
- Success criteria and desired outcomes

### Thought 3: Assumption Challenge
Question the underlying assumptions:
- What assumptions are we making?
- Are these assumptions valid in this context?
- What if the opposite were true?
- Alternative perspectives to consider

### Thought 4: Alternative Approaches Exploration
Explore different solution paths:
- Conventional approaches and their pros/cons
- Unconventional or innovative solutions
- Trade-offs between different options
- Hybrid or combined approaches

### Thought 5: Context Integration
Incorporate relevant context:
- File references and code patterns
- Previous session insights
- User's specific technical stack
- Business or project constraints

### Thought 6: Edge Case Analysis
Identify potential issues:
- What could go wrong with each approach?
- Edge cases and failure modes
- Scalability and performance concerns
- Security and maintenance implications

### Thought 7: Risk Assessment
Evaluate risks for each option:
- Implementation complexity
- Technical debt potential
- Team skill requirements
- Timeline and resource impacts

### Thought 8: Solution Synthesis
Combine insights into recommendations:
- Primary recommended approach
- Backup or alternative options
- Implementation considerations
- Next steps and validation points

Continue sequential thinking until satisfaction, using:
- `isRevision: true` to refine previous thoughts
- `branchFromThought` to explore alternative reasoning paths
- `needsMoreThoughts: true` to extend analysis if needed
</strategist>

## Step 3: Critical Evaluation & Synthesis

**Self-Critique Questions:**
- Does the analysis address the user's specific context?
- Are the recommendations practical and implementable?
- Have we considered the most important constraints?
- Are there any blind spots or missing perspectives?

**Contextual Validation:**
- Fit with user's technical stack and preferences
- Alignment with previous decisions in session
- Practicality given team skills and resources
- Integration with existing systems or patterns

**Final Synthesis:**
- **Primary Recommendation**: [best approach with rationale]
- **Alternative Options**: [backup plans with trade-offs]
- **Implementation Guidance**: [key considerations and next steps]
- **Risk Mitigation**: [how to address identified concerns]

---

## Usage Examples

**Basic deep analysis:**
```
/atelier-thinkdeep "Analyze my authentication architecture"
```

**With file references:**
```
/atelier-thinkdeep "Evaluate my database schema with reference to models/user.py"
```

**With focus areas:**
```
/atelier-thinkdeep "Assess my microservices design focusing on performance and security"
```

**Complex architectural decisions:**
```
/atelier-thinkdeep "Should I use GraphQL or REST for my API considering team skills and scalability needs"
```

## When to Use ThinkDeep

- **Architecture decisions**: When choosing between major design approaches
- **Complex problem solving**: Multi-faceted issues requiring deep analysis
- **Assumption validation**: Challenging conventional wisdom or previous decisions
- **Alternative exploration**: When stuck and need fresh perspectives
- **Risk assessment**: Before major implementation decisions

## ThinkDeep vs Challenge

**Use /atelier-thinkdeep**: Deep exploration, comprehensive analysis, alternative discovery, complex decisions
**Use /atelier-challenge**: Question assumptions, test validity, assess risks, prevent automatic agreement

**Key distinction**: ThinkDeep = deep exploration, Challenge = critical evaluation

## Expected Outcomes

After using this command:
- Comprehensive understanding of the problem space
- Multiple approaches evaluated with trade-offs
- Clear recommendation with solid reasoning
- Risk assessment and mitigation strategies
- Actionable next steps for implementation
