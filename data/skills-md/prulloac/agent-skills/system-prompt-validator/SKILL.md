---
name: system-prompt-validator
description: Validate agent system prompts (such as agents.md) for being objective-driven, clear, readable, free of duplicated intentions, without missing or broken links, and ensuring required sections like general agentic guidelines, code review, and code generation are present. Use when validating or reviewing agent prompt files.
---

# System Prompt Validator

## Overview

This skill provides guidelines and checklists for manually validating agent system prompts to ensure they meet quality standards for clarity, completeness, and correctness.

## Validation Criteria

Agent prompts must be:

- **Objective-driven**: Clearly state the agent's purpose and goals
- **Clear and Readable**: Use straightforward language and proper structure
- **No Duplicated Intentions**: Avoid redundant statements of the same requirements
- **Valid Links**: All referenced files exist and links are not broken
- **Required Sections**: Must include content covering general agentic guidelines, code review, and code generation (sections may be named or integrated differently)
- **General Agentic Guidelines**: Must at least cover handling uncertainty, avoiding training biases by prioritizing skills/tools over improvisation, using in-memory todo lists for tasks requiring more than 2 steps, and respecting agent-to-human output formats when present and explicit (ensuring they are not omitted by agents or subagents)

## Usage

To validate an agent prompt file:

1. Review the prompt against each criterion in the checklist
2. Check for required sections by scanning headings
3. Verify links by confirming referenced files exist
4. Identify any duplicated content or unclear language
5. Fix identified issues

## Validation Checklist

- [ ] **Objective-driven**: Does the prompt clearly state purpose and goals?
- [ ] **Clear and Readable**: Is language straightforward? Sentences under 25 words average?
- [ ] **No Duplications**: Any repeated requirements or statements?
- [ ] **Valid Links**: All file references exist and correct?
- [ ] **Required Sections**: Includes content covering general agentic guidelines, code review, and code generation (sections may be integrated or named differently)?
- [ ] **General Guidelines Coverage**: Handles uncertainty, avoids training biases, uses todo lists for multi-step tasks, respects explicit output formats?

## Resources

### references/
- `validation_guide.md`: Detailed guide on validation criteria and examples - see [validation_guide.md](references/validation_guide.md)
- `examples/good_prompt.md`: Example of a well-structured agent prompt - see [good_prompt.md](examples/good_prompt.md)
- `examples/good_prompt2.md`: Additional example from Andrej Karpathy's CLAUDE.md - see [good_prompt2.md](examples/good_prompt2.md)
- `examples/bad_prompt.md`: Example of a prompt with issues - see [bad_prompt.md](examples/bad_prompt.md)
