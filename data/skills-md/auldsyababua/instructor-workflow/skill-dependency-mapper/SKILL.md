---
name: skill-dependency-mapper
description: Analyzes skill ecosystem to visualize dependencies, identify workflow bottlenecks, and recommend optimal skill stacks. Use when asked about skill combinations, workflow optimization, bottleneck identification, or which skills work together. Triggers include phrases like "which skills work together", "skill dependencies", "workflow bottlenecks", "optimal skill stack", or "recommend skills for".
---

# Skill Dependency Mapper

Analyzes the skill ecosystem to understand relationships, identify inefficiencies, and optimize workflows.

## When to Use This Skill

Use this skill when users ask about:
- Which skills commonly work together
- Skill combinations that create bottlenecks
- Optimal skill "stacks" for specific tasks
- Workflow optimization across skills
- Understanding skill dependencies
- Token budget concerns with multiple skills

## Core Workflow

### 1. Scan and Analyze Skills

Run the analyzer script to extract metadata from all available skills:

```bash
cd /home/claude/skill-dependency-mapper
python scripts/analyze_skills.py > /tmp/skill_analysis.txt
```

The script extracts:
- Tool dependencies (bash_tool, web_search, etc.)
- File format associations (docx, pdf, xlsx, etc.)
- Domain overlap (document, research, coding, etc.)
- Complexity metrics (size, tool count, bundled resources)

### 2. Detect Bottlenecks

For bottleneck analysis, first capture skill data as JSON:

```python
import json
from scripts.analyze_skills import SkillAnalyzer

analyzer = SkillAnalyzer()
analyzer.scan_skills()

# Save for bottleneck detection
with open('/tmp/skill_data.json', 'w') as f:
    json.dump(analyzer.skills, f, default=list)
```

Then run bottleneck detection:

```bash
python scripts/detect_bottlenecks.py /tmp/skill_data.json > /tmp/bottlenecks.txt
```

### 3. Generate Dependency Map

Create a text-based dependency visualization:

```python
from scripts.analyze_skills import SkillAnalyzer

analyzer = SkillAnalyzer()
analyzer.scan_skills()

# Generate dependency mapping
dependencies = analyzer.find_dependencies()

# Format as markdown
output = ["# Skill Dependency Map\n"]
for skill, related in sorted(dependencies.items()):
    if related:
        output.append(f"## {skill}\n")
        output.append("Works well with:\n")
        for related_skill in sorted(related)[:8]:
            # Show why they're related
            skill_a = analyzer.skills[skill]
            skill_b = analyzer.skills[related_skill]
            
            shared = []
            if skill_a['tools'] & skill_b['tools']:
                shared.append(f"tools: {', '.join(skill_a['tools'] & skill_b['tools'])}")
            if skill_a['formats'] & skill_b['formats']:
                shared.append(f"formats: {', '.join(skill_a['formats'] & skill_b['formats'])}")
            if skill_a['domains'] & skill_b['domains']:
                shared.append(f"domains: {', '.join(skill_a['domains'] & skill_b['domains'])}")
            
            reason = " | ".join(shared) if shared else "complementary"
            output.append(f"- **{related_skill}** ({reason})\n")
        output.append("\n")

print('\n'.join(output))
```

### 4. Recommend Skill Stacks

For task-specific recommendations:

```python
from scripts.analyze_skills import SkillAnalyzer

analyzer = SkillAnalyzer()
analyzer.scan_skills()

# Get recommended stacks
stacks = analyzer.recommend_stacks()

# Format output
output = ["# Recommended Skill Stacks\n"]
for stack in stacks:
    output.append(f"## {stack['name']}\n")
    output.append(f"**Use case**: {stack['use_case']}\n\n")
    output.append("**Skills**:\n")
    for skill in sorted(stack['skills']):
        skill_data = analyzer.skills[skill]
        output.append(f"- **{skill}** - {skill_data['description'][:80]}...\n")
    output.append("\n")

print('\n'.join(output))
```

### 5. Custom Analysis

For specific queries, filter and analyze programmatically:

```python
from scripts.analyze_skills import SkillAnalyzer

analyzer = SkillAnalyzer()
analyzer.scan_skills()

# Example: Find all skills that use web_search
web_skills = [
    name for name, data in analyzer.skills.items()
    if 'web_search' in data['tools']
]

# Example: Find skills by domain
financial_skills = [
    name for name, data in analyzer.skills.items()
    if 'financial' in data['domains']
]

# Example: Find lightweight skills
lightweight = [
    name for name, data in analyzer.skills.items()
    if data['complexity_score'] < 5 and data['size'] < 2000
]
```

## Output Format

Generate concise markdown reports with:

1. **Executive summary** - Key findings in 2-3 sentences
2. **Dependency maps** - Skills grouped by relationship strength
3. **Bottleneck analysis** - Identified issues with impact assessment
4. **Recommendations** - Actionable optimization suggestions
5. **Skill stacks** - Pre-configured combinations for common workflows

Keep output token-efficient:
- Use bullet points for lists
- Bold key skill names
- Include only actionable insights
- Omit verbose explanations

## Interpreting Results

### Dependency Strength

- **Strong**: Share 3+ characteristics (tools, formats, domains)
- **Medium**: Share 2 characteristics
- **Weak**: Share 1 characteristic

### Bottleneck Severity

- **High**: >10k combined token size or >5 tool calls
- **Medium**: 5-10k tokens or 3-5 tool calls
- **Low**: <5k tokens or <3 tool calls

### Stack Optimization

Optimal stacks minimize:
- Total token budget (<15k characters)
- Tool call diversity (<4 different tools)
- Format conversion steps (<2 conversions)

## Advanced Usage

### Consulting Known Patterns

For established patterns and anti-patterns, reference:

```bash
view /home/claude/skill-dependency-mapper/references/known_patterns.md
```

Use this when:
- User asks about best practices
- Workflow seems suboptimal
- Need to explain why certain combinations work well

### Custom Bottleneck Detection

Modify detection thresholds in `detect_bottlenecks.py`:

```python
detector.detect_high_tool_usage(threshold=4)  # Adjust tool count threshold
detector.detect_large_references(size_threshold=8000)  # Adjust size threshold
detector.detect_token_budget_risks(combined_threshold=12000)  # Adjust combined size
```

### Filtering by Skill Type

Analyze only specific skill types:

```python
analyzer = SkillAnalyzer()
analyzer.scan_skills()

# User skills only
user_skills = {
    name: data for name, data in analyzer.skills.items()
    if data['type'] == 'user'
}

# Public skills only
public_skills = {
    name: data for name, data in analyzer.skills.items()
    if data['type'] == 'public'
}
```

## Common Use Cases

### "Which skills work together for data analysis?"

1. Run analyzer to find spreadsheet/data skills
2. Filter by shared domains and tools
3. Generate dependency map for data domain
4. Recommend optimized stack

### "What's causing slowdowns in my document workflow?"

1. Run bottleneck detection
2. Focus on document-related skills
3. Identify high tool usage or token budget issues
4. Suggest sequential processing or skill consolidation

### "Recommend skills for financial reporting"

1. Filter skills by 'financial' domain
2. Find complementary skills (spreadsheet, presentation)
3. Assess token budget feasibility
4. Output recommended stack with rationale

### "Show me skill dependencies visually"

1. Generate full dependency map
2. Group by relationship strength
3. Highlight clusters of related skills
4. Format as hierarchical markdown sections

## Limitations

- Dependency detection is heuristic-based (not ground truth)
- Cannot analyze skills not in /mnt/skills
- Token estimates are approximate (actual may vary)
- Bottleneck severity depends on specific usage patterns
- No access to actual conversation usage data

## Tips for Effective Analysis

1. **Be specific**: Filter by domain/format for targeted results
2. **Consider context**: Bottlenecks depend on user's workflow
3. **Iterate**: Run analysis, optimize, re-analyze
4. **Validate**: Test recommended stacks with real tasks
5. **Stay current**: Re-run after skill updates or additions
