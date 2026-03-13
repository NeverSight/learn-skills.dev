---
name: template-skill
description: A starter template for creating new Claude Skills with best practices and example structure
---

# Template Skill

This is a starter template for building your own Claude Skills. Use this as a foundation for creating custom tools that extend Claude's capabilities.

## Purpose

This skill demonstrates the proper structure and format for Claude Skills, including:
- YAML frontmatter with required metadata
- Clear instructions and guidelines
- Example usage patterns
- Helper scripts and resources
- Best practices for skill development

## When to Use

Use this skill as a reference when:
- Creating a new custom skill for your workflow
- Learning about skill structure and organization
- Understanding how to bundle resources and documentation
- Building skills for team collaboration

## Key Features

1. **Well-Organized Structure** - Follows the recommended directory layout with clear separation of concerns
2. **Progressive Disclosure** - Bundles helper scripts and documentation that Claude loads as needed
3. **Example Usage** - Provides concrete examples of how the skill should be invoked
4. **Flexible and Extensible** - Easily customize for your specific use case

## Directory Structure

```
template-skill/
├── SKILL.md                 # Main skill definition (this file)
├── scripts/
│   ├── helper.py           # Python helper script
│   └── utilities.sh         # Bash utilities
├── references/
│   └── best-practices.md    # Supporting documentation
└── assets/
    ├── templates/          # Template files
    └── examples/           # Example data
```

## Instructions

When you activate this skill, Claude will:

1. **Follow the guidelines** outlined below
2. **Use helper scripts** from the `scripts/` directory when appropriate
3. **Reference documentation** from the `references/` directory for detailed information
4. **Apply templates** from the `assets/` directory to structure outputs
5. **Provide clear examples** based on the patterns demonstrated here

## Guidelines

- Keep your SKILL.md file concise (under 5,000 words) to avoid overwhelming Claude's context window
- Use progressive disclosure - provide basic instructions in SKILL.md and detailed docs in separate files
- Include concrete examples and expected outputs to clarify your intent
- Organize helper files logically in subdirectories (scripts/, references/, assets/)
- Document any dependencies or prerequisites clearly
- Make skills modular and composable with other skills

## Examples

### Example 1: Basic Invocation
When you want to use this skill, simply activate it and describe your task:
```
Activate the template-skill and help me create a new custom skill for handling batch data processing.
```

### Example 2: With Specific Parameters
```
Use the template-skill to generate a skill that integrates with our internal API and follows our team's coding standards.
```

### Example 3: Extending the Template
```
Based on the template-skill structure, help me create a skill that automates our documentation workflow.
```

## Helper Resources

This skill includes the following helper files:

- **scripts/helper.py** - Python utilities for common tasks
- **scripts/utilities.sh** - Bash functions for file and text processing
- **references/best-practices.md** - Detailed guidelines for skill development
- **assets/templates/** - Ready-to-use templates for common skill patterns
- **assets/examples/** - Real-world examples of well-structured skills

## Tips for Creating Your Own Skill

1. **Start with a clear purpose** - Define what problem your skill solves
2. **Keep instructions concise** - Users should understand your skill in seconds
3. **Provide examples** - Show concrete use cases and expected outputs
4. **Organize resources** - Use subdirectories (scripts/, references/, assets/) to stay organized
5. **Test thoroughly** - Verify that Claude correctly interprets your skill instructions
6. **Document dependencies** - Clearly list any prerequisites or external tools required
7. **Iterate based on feedback** - Refine your skill based on how Claude uses it

## Related Resources

- Claude Code Documentation: https://docs.claude.com/claude-code/skills
- Skill Authoring Best Practices: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
- Anthropic Skills Repository: https://github.com/anthropics/skills

## Support

For questions about creating skills or issues with this template:
1. Review the guidelines and examples above
2. Check the supporting documentation in `references/best-practices.md`
3. Examine the helper scripts in the `scripts/` directory
4. Consult the Anthropic skills repository for additional examples
