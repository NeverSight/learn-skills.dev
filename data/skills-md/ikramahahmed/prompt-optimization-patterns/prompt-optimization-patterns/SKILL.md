---
name: prompt-optimization-patterns
description: Analyze and optimize prompts using proven patterns and best practices. Provides iterative improvements, before/after comparisons, multiple variants, and detailed optimization reports for general tasks, code generation, and creative writing.
version: 1.0.0
author: Skills Community
tags: [prompt-engineering, optimization, best-practices, code-generation, creative-writing, llm, ai-prompts]
---

# Prompt Optimization Patterns

A comprehensive skill for analyzing and optimizing prompts using proven prompt engineering patterns and best practices.

## When to Use This Skill

Trigger this skill when users:
- Ask to "optimize", "improve", or "fix" a prompt
- Say "make this prompt better" or "help me write a better prompt"
- Request "prompt engineering help" or "best practices"
- Want to "create a prompt for [task]" from scratch
- Need help with prompt clarity, structure, or effectiveness

## What This Skill Does

This skill helps users:

1. **Analyze and improve existing prompts** - Identify weaknesses and apply optimization patterns
2. **Generate optimized prompts from scratch** - Build high-quality prompts using templates and best practices
3. **Teach prompt engineering patterns** - Explain the "why" behind each optimization with educational context
4. **Fix common mistakes** - Address vagueness, missing context, poor structure, and conflicting instructions

## Output Format

The skill provides **four complementary output formats** for every optimization:

### 1. Iterative Improvements with Explanations
Show 2-4 progressive versions, explaining what changed and why at each step:
- Version 1: Original prompt
- Version 2: Basic clarity improvements
- Version 3: Structure and format additions
- Version 4: Final optimized version

**Educational approach** - helps users understand prompt engineering principles.

### 2. Before/After Comparison
Side-by-side display showing:
- Original prompt with quality score
- Optimized prompt with improved score
- Bulleted list of specific changes made
- Visual highlighting of improvements

**Quick understanding** - immediately see what changed.

### 3. Multiple Variants (2-3 different approaches)
Generate distinct optimized versions using different strategies:
- Variant A: One optimization focus (e.g., "Maximum Clarity")
- Variant B: Different optimization focus (e.g., "Structured Output")
- Variant C: Alternative approach (e.g., "Context-Rich with Examples")

Each variant is **clearly labeled** with its strategy and best use case.

### 4. Detailed Optimization Report
Comprehensive analysis including:
- Quality metrics table (before/after scores across 6 dimensions)
- Patterns applied with explanations
- Specific improvements made
- Remaining optimization opportunities
- Best practices demonstrated
- Recommended usage for each variant

## The 10 Core Optimization Patterns

### Pattern 1: Clarity and Specificity
**Problem**: Vague or ambiguous instructions → inconsistent results  
**Solution**: Use precise language, define terms, specify constraints

**Example**:
```
❌ "Write about AI"
✅ "Write a 500-word blog post explaining transformer models for software engineers with basic ML knowledge"
```

**Key Techniques**:
- Define the task explicitly
- Specify target audience
- Set length/format constraints
- Include domain context
- Use concrete rather than abstract language

### Pattern 2: Structured Output Formatting
**Problem**: Outputs are hard to parse or don't match expected format  
**Solution**: Explicitly request structure using XML, JSON, markdown, or templates

**Example**:
```
❌ "Analyze this code"
✅ "Analyze this code and structure your response as:
    <analysis>
      <bugs>List of bugs found</bugs>
      <improvements>Suggested improvements</improvements>
      <rating>Code quality rating 1-10</rating>
    </analysis>"
```

**Key Techniques**:
- Request XML/JSON for structured data
- Use markdown headers for reports
- Specify section requirements
- Provide output templates

### Pattern 3: Role and Persona Assignment
**Problem**: Generic responses lack domain expertise or appropriate tone  
**Solution**: Assign a specific role, expertise level, or persona

**Example**:
```
❌ "Explain quantum computing"
✅ "You are a physics professor teaching undergraduates. Explain quantum computing using relatable analogies"
```

**Key Techniques**:
- Define expertise level
- Set appropriate tone
- Specify perspective
- Establish domain knowledge

### Pattern 4: Chain-of-Thought (CoT) Reasoning
**Problem**: Complex tasks produce superficial or incorrect answers  
**Solution**: Request step-by-step reasoning before the final answer

**Example**:
```
❌ "What's 15% of 240?"
✅ "Calculate 15% of 240. Show your work step-by-step before giving the final answer"
```

**Key Techniques**:
- Request "think step-by-step"
- Ask for reasoning before conclusions
- Break complex tasks into subtasks
- Use "Let's approach this systematically"

### Pattern 5: Few-Shot Learning with Examples
**Problem**: The model doesn't understand desired output style or format  
**Solution**: Provide 2-3 high-quality input→output example pairs

**Example**:
```
❌ "Convert these sentences to bullet points"
✅ "Convert sentences to bullet points. Examples:
    
    Input: 'The sky is blue. Birds fly high.'
    Output: • Sky is blue
            • Birds fly high
    
    Now convert: [user's text]"
```

**Key Techniques**:
- Show 2-5 diverse examples
- Include edge cases
- Match exact desired format
- Label examples clearly

### Pattern 6: Context and Background Information
**Problem**: Outputs miss important nuances or make wrong assumptions  
**Solution**: Provide relevant context, constraints, and background

**Example**:
```
❌ "Write a product description"
✅ "Write a product description for a B2B SaaS analytics platform. 
    Target: CTOs at mid-size companies
    Key differentiator: real-time data processing
    Tone: professional but approachable
    Length: 150 words"
```

**Key Techniques**:
- Define the audience
- Explain constraints
- Provide domain knowledge
- Set tone and style guides

### Pattern 7: Constraint-Based Prompting
**Problem**: Outputs violate requirements or best practices  
**Solution**: Explicitly state what to avoid and requirements to follow

**Example**:
```
❌ "Write Python code"
✅ "Write Python code following these constraints:
    - Use type hints for all functions
    - Maximum line length: 88 characters
    - Include docstrings for all public methods
    - Do not use global variables
    - Prefer list comprehensions over loops where readable"
```

**Key Techniques**:
- List "must have" requirements
- List "must not have" restrictions
- Specify style preferences
- Define quality criteria

### Pattern 8: Iterative Refinement
**Problem**: First attempt doesn't meet all needs  
**Solution**: Build prompts that encourage self-critique and revision

**Example**:
```
❌ "Write an essay"
✅ "Write an essay about climate change. After writing, critique your own work for: 
    (1) argument strength
    (2) evidence quality
    (3) clarity
    Then revise based on your critique"
```

**Key Techniques**:
- Request self-evaluation
- Ask for multiple drafts
- Encourage revision
- Set quality checkpoints

### Pattern 9: Template and Variable Substitution
**Problem**: Need similar content with different inputs  
**Solution**: Create reusable prompt templates with variable slots

**Example**:
```
❌ Multiple separate prompts for each product
✅ "Generate a product review for {PRODUCT_NAME}. 
    Focus on {KEY_FEATURES}. 
    Target audience: {AUDIENCE}. 
    Tone: {TONE}. 
    Include sections: Overview, Pros, Cons, Verdict"
```

**Key Techniques**:
- Use {VARIABLE} notation
- Document each variable
- Provide default values
- Create modular components

### Pattern 10: Multi-Step Decomposition
**Problem**: Complex tasks overwhelm or produce shallow results  
**Solution**: Break tasks into explicit sequential steps

**Example**:
```
❌ "Analyze this business strategy"
✅ "Analyze this business strategy in three steps:
    Step 1: Summarize the key strategic points
    Step 2: Identify strengths and weaknesses using SWOT
    Step 3: Provide specific recommendations with rationale"
```

**Key Techniques**:
- Number steps explicitly
- Make each step concrete
- Build later steps on earlier ones
- Set clear deliverables per step

## Common Prompt Mistakes to Avoid

### 1. Ambiguity and Vagueness
❌ "Tell me about it"  
❌ "Make it better"  
❌ "Write something creative"

### 2. Assuming Context
❌ Not specifying what "it" refers to  
❌ Omitting audience or use case  
❌ Skipping necessary background

### 3. No Output Format
❌ Leaving structure to chance  
❌ Not specifying length constraints  
❌ Unclear about desired format

### 4. Conflicting Instructions
❌ "Be brief but comprehensive"  
❌ "Creative but follow exact template"  
❌ "Casual but professional"

### 5. Missing Examples
❌ No reference for complex formats  
❌ Unclear quality expectations  
❌ Abstract requirements only

### 6. Overloading Single Prompt
❌ Too many unrelated tasks  
❌ Conflicting objectives  
❌ No prioritization

### 7. No Success Criteria
❌ Unclear what "good" looks like  
❌ No measurable outcomes  
❌ Missing quality indicators

## Optimization Workflow

When a user provides a prompt to optimize, follow this systematic approach:

### Step 1: Analysis (Assessment Phase)
1. Identify the core task/goal
2. Assess current prompt quality using 6-dimension scoring:
   - Clarity (1-10)
   - Specificity (1-10)
   - Structure (1-10)
   - Context (1-10)
   - Examples (1-10, if applicable)
   - Completeness (1-10)
3. Detect which patterns would be most beneficial
4. Spot common mistakes present
5. Note missing critical elements

### Step 2: Pattern Application (Optimization Phase)

**For General Tasks**, prioritize:
- Clarity and Specificity (always)
- Context and Background
- Structured Output
- Constraint-Based Prompting

**For Code Generation**, prioritize:
- Constraint-Based Prompting (style, requirements)
- Few-Shot Examples (usage patterns)
- Structured Output (comments, tests, docs)
- Chain-of-Thought (for algorithms)

**For Creative Writing**, prioritize:
- Role and Persona
- Context and Background
- Few-Shot Examples (style references)
- Iterative Refinement

### Step 3: Generate All Four Output Formats

**A. Iterative Improvements**
- Show 2-4 progressive refinements
- Explain each change with educational rationale
- Build from basic to fully optimized

**B. Before/After Comparison**
- Display original with score
- Display optimized with improved score
- List specific changes with checkmarks
- Highlight key improvements

**C. Multiple Variants**
Generate 2-3 versions with different strategies:
- Variant 1: One optimization focus (label clearly)
- Variant 2: Different optimization focus (label clearly)
- Variant 3: Alternative approach (label clearly)
- Specify "best for" use case for each

**D. Detailed Report**
Include:
- Quality metrics table (before/after across all dimensions)
- Patterns applied with explanations
- Specific improvements breakdown
- Remaining opportunities for edge cases
- Best practices demonstrated
- Recommended usage guidance

## Quality Scoring Rubric

Rate prompts on 1-10 scale across these dimensions:

| Dimension | What It Measures |
|-----------|------------------|
| **Clarity** | How clear and unambiguous are the instructions? |
| **Specificity** | How precise are the requirements and constraints? |
| **Structure** | How well-organized and formatted is the prompt? |
| **Context** | How much relevant background information is provided? |
| **Examples** | Quality and relevance of examples (if needed for task) |
| **Completeness** | Are all necessary elements present? |

**Overall Score** = Average of applicable dimensions

**Interpretation**:
- 1-3: Poor - Major issues, needs significant work
- 4-6: Fair - Basic structure but missing key elements
- 7-8: Good - Well-formed with minor improvements possible
- 9-10: Excellent - Professional-quality prompt

## Task-Specific Templates

### Code Generation Template
```
Write [LANGUAGE] code to [TASK].

Requirements:
- Input: [TYPE and DESCRIPTION]
- Output: [TYPE and DESCRIPTION]
- Style: [STYLE_GUIDE like PEP 8, ESLint]
- Include: [error handling/logging/tests/documentation]
- Constraints: [performance/dependencies/compatibility]

Example usage:
[SHOW CONCRETE EXAMPLE]
```

### Creative Writing Template
```
Write a [FORMAT] in the [GENRE] genre.

Details:
- Audience: [WHO]
- Tone: [TONE/VOICE]
- Length: [WORD COUNT or DURATION]
- Setting: [WHERE/WHEN]
- Characters: [WHO]
- Theme: [WHAT IT'S ABOUT]
- Style: [REFERENCES or DESCRIPTION]

[Optional: Provide example passage showing desired style]
```

### General Task Template
```
[CLEAR TASK STATEMENT]

Context: [BACKGROUND INFO]
Audience: [WHO WILL USE THIS]
Format: [HOW TO STRUCTURE OUTPUT]
Length: [SPECIFIC CONSTRAINT]
Tone: [STYLE GUIDANCE]

Requirements:
- [MUST HAVE #1]
- [MUST HAVE #2]

Constraints:
- [MUST NOT #1]
- [MUST NOT #2]

[Optional: Examples if format is non-standard]
```

## Response Format Structure

When optimizing a prompt, structure your response exactly as:

```markdown
# Prompt Optimization Analysis

## Original Prompt Assessment
[Brief analysis of current prompt - 2-3 sentences]
Quality Score: X/10
Issues Detected: [Bulleted list of 3-5 issues]

## Optimization Strategy
Patterns Applied: [List 2-4 patterns being used]
Focus Areas: [What you're prioritizing]

---

## 1. ITERATIVE IMPROVEMENTS

### Version 1: Original
[Original prompt exactly as provided]

### Version 2: [Name of improvement focus]
[Improved prompt]
**Changes Made**: [1-2 sentence explanation]

### Version 3: [Name of improvement focus]
[Further improved prompt]
**Changes Made**: [1-2 sentence explanation]

### Version 4: Final Optimized
[Fully optimized prompt]
**Changes Made**: [1-2 sentence explanation]

---

## 2. BEFORE/AFTER COMPARISON

### BEFORE (Score: X/10)
```
[Original prompt exactly as provided]
```

### AFTER (Score: Y/10)
```
[Final optimized prompt]
```

### Key Changes:
- ✅ Added: [What was added]
- ✅ Clarified: [What was clarified]
- ✅ Structured: [How it was structured]
- ✅ Improved: [Other improvements]

---

## 3. MULTIPLE VARIANTS

### Variant A: [Strategy Name]
**Strategy**: [1 sentence explaining the approach]
```
[Variant A full text]
```
**Best for**: [When to use this variant]

### Variant B: [Strategy Name]
**Strategy**: [1 sentence explaining the approach]
```
[Variant B full text]
```
**Best for**: [When to use this variant]

### Variant C: [Strategy Name]
**Strategy**: [1 sentence explaining the approach]
```
[Variant C full text]
```
**Best for**: [When to use this variant]

---

## 4. DETAILED OPTIMIZATION REPORT

### Quality Metrics
| Dimension | Before | After | Change |
|-----------|--------|-------|--------|
| Clarity | X/10 | Y/10 | +Z |
| Specificity | X/10 | Y/10 | +Z |
| Structure | X/10 | Y/10 | +Z |
| Context | X/10 | Y/10 | +Z |
| Examples | X/10 | Y/10 | +Z |
| Completeness | X/10 | Y/10 | +Z |
| **Overall** | **X/10** | **Y/10** | **+Z** |

### Patterns Applied
1. **[Pattern Name]**: [How it improved the prompt - 1 sentence]
2. **[Pattern Name]**: [How it improved the prompt - 1 sentence]
[Continue for all patterns used]

### Specific Improvements
- **Clarity**: [What was clarified]
- **Structure**: [How it was organized]
- **Context**: [What background was added]
- **Examples**: [What examples were provided]
- **Constraints**: [What requirements were specified]

### Remaining Opportunities
[Optional improvements for specific edge cases - 2-3 bullets]

### Best Practices Demonstrated
- ✓ [Practice 1]
- ✓ [Practice 2]
- ✓ [Practice 3]

### Recommended Usage
[1-2 sentences on when to use each variant and additional tips]
```

## Edge Cases and Special Handling

### When User Wants Prompt from Scratch
1. Ask clarifying questions or make reasonable assumptions
2. Identify task category (general/code/creative)
3. Apply appropriate template as foundation
4. Layer relevant patterns based on complexity
5. Provide all four output formats

### When User Has Multiple Prompts
1. Optimize each separately
2. Identify common patterns across them
3. Suggest a meta-template if appropriate
4. Show consistency improvements

### When User's Prompt is Already High Quality
1. Acknowledge what's working well explicitly
2. Suggest only minor refinements
3. Focus on edge case handling or advanced patterns
4. Provide variants for different contexts
5. Don't over-engineer

### When Conflicting Requirements Exist
1. Flag the conflict explicitly in analysis
2. Suggest resolution strategies
3. Provide variants with different trade-offs
4. Let user choose based on priorities
5. Explain why conflicts hurt effectiveness

## Implementation Guidelines

### Pattern Selection Priority
**Always apply:**
- Clarity and Specificity (foundation for all prompts)
- Structured Output (unless free-form is explicitly required)

**Apply for complex tasks:**
- Chain-of-Thought Reasoning
- Multi-Step Decomposition

**Apply when format unclear:**
- Few-Shot Learning with Examples
- Template and Variable Substitution

**Apply for specialized needs:**
- Role and Persona Assignment
- Context and Background Information

**Apply for quality control:**
- Constraint-Based Prompting
- Iterative Refinement

### Progressive Enhancement Approach
Build prompts in layers:
1. **Base**: Clear task + output format
2. **Add**: Context and constraints
3. **Add**: Examples (if needed)
4. **Add**: Role/persona (if beneficial)
5. **Add**: Chain-of-thought (if complex)

### Anti-Patterns to Avoid
❌ Over-engineering simple prompts - Don't add unnecessary complexity  
❌ Pattern stacking without purpose - Each pattern should serve a clear need  
❌ Ignoring user's actual goal - Optimize for the real task, not theory  
❌ Removing user's voice - Preserve intent and style preferences  
❌ Making prompts too rigid - Allow flexibility where appropriate

## Examples

### Example 1: Vague Prompt Optimization

**User Input**: 
"Optimize this: 'Write about AI'"

**Skill Output** (abbreviated):

```
# Prompt Optimization Analysis

## Original Prompt Assessment
Extremely vague - no scope, audience, format, or purpose defined.
Quality Score: 2/10
Issues: No topic specificity, missing audience, no format/length, no context

## Optimization Strategy
Patterns Applied: Clarity & Specificity, Structured Output, Context & Background
Focus Areas: Adding specificity, defining audience, setting constraints

---

## 2. BEFORE/AFTER COMPARISON

### BEFORE (Score: 2/10)
```
Write about AI
```

### AFTER (Score: 9/10)
```
Write a 500-word article explaining how AI is transforming the job market.

Target Audience: Business professionals without technical backgrounds
Tone: Professional but accessible - avoid jargon

Structure:
- Introduction: AI adoption overview (100 words)
- Impact 1: Jobs being automated (150 words)
- Impact 2: New jobs being created (150 words)
- Impact 3: Skills to develop (100 words)
- Conclusion: Balanced future perspective (50 words)

Requirements:
- Use examples from at least 2 industries
- Cite recent statistics where possible
- Maintain balanced, non-alarmist perspective
- Make it engaging and understandable
```

### Key Changes:
- ✅ Added: Specific topic (AI's job market impact vs generic "AI")
- ✅ Added: Target audience specification
- ✅ Added: Length constraint (500 words)
- ✅ Structured: Five-part structure with word allocations
- ✅ Added: Content requirements and quality criteria
```

### Example 2: Code Generation Optimization

**User Input**:
"I need a better prompt for: 'Write Python code for sorting'"

**Skill Output** (abbreviated):

```
### AFTER (Score: 9/10)
```
Write a Python function to sort a list of integers in ascending order.

Function Signature:
def sort_integers(numbers: List[int]) -> List[int]:

Input: List[int] - Integers (may have duplicates, negatives, or be empty)
Output: List[int] - New sorted list in ascending order

Requirements:
- Use type hints for all parameters and return values
- Include comprehensive docstring (description, Args, Returns, Examples)
- Use Python's built-in sorted() for efficiency
- Handle edge cases: empty list, single element, duplicates
- Do not modify original list
- Follow PEP 8 style (max 88 chars per line)

Example Usage:
```python
>>> sort_integers([3, 1, 4, 1, 5, 9, 2, 6])
[1, 1, 2, 3, 4, 5, 6, 9]
>>> sort_integers([])
[]
```

Tests: Include at least 3 test cases (normal, empty, negatives)
```

### Key Changes:
- ✅ Added: Function signature with type hints
- ✅ Added: Input/output specifications with edge cases
- ✅ Added: Code quality requirements (PEP 8, docstrings)
- ✅ Added: Example usage demonstrating behavior
- ✅ Added: Testing requirements
```

## Best Practices Summary

✅ **DO:**
- Apply patterns systematically based on task needs
- Provide educational explanations for each change
- Generate multiple variants when beneficial
- Acknowledge existing strengths in prompts
- Focus on user's actual goal and context
- Use all four output formats consistently

❌ **DON'T:**
- Over-engineer simple, straightforward prompts
- Stack patterns without clear purpose
- Ignore or override user's original intent
- Remove user's unique voice or style
- Make prompts unnecessarily rigid or complex
- Skip any of the four required output formats

## Conclusion

The key to effective prompt optimization is **understanding the task, applying relevant patterns systematically, and maintaining clarity**. Focus on making prompts specific, well-structured, and complete while avoiding unnecessary complexity.

**Remember**: The best prompt is one that consistently achieves the user's goal. Optimize for real-world outcomes, not theoretical perfection.

Always provide all four output formats to give users maximum flexibility and understanding.
