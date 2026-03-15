---
name: session-log
description: Document conversation accomplishments in Obsidian vault with frontmatter, code changes, learning notes, and next steps.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Glob
---

# Session Logger

Document our conversation accomplishments in your Obsidian vault with detailed session notes.

## Usage
Create comprehensive session documentation in `~/Documents/main-vault/Sessions/` with accomplishments, learnings, and next steps.

## Details
This skill will:
1. Analyze the entire conversation history
2. Extract key accomplishments and decisions
3. Document code changes and configurations
4. Capture learning points and insights
5. List commands and tools used
6. Create actionable next steps
7. Add relevant tags for Obsidian organization
8. Include links to created/modified files

## Note Structure
- **Date & Title**: Timestamp and descriptive title
- **Summary**: High-level overview of session
- **Accomplishments**: Bullet points of completed tasks
- **Code & Commands**: Key snippets and commands used
- **Learning Notes**: Concepts explored and understood
- **Files Modified**: List of changed files with descriptions
- **Next Steps**: Actionable items for future sessions
- **Resources**: Links to documentation and references

## Obsidian Integration
- Uses proper markdown formatting
- Adds frontmatter with metadata
- Creates backlinks to related notes
- Includes tags for easy searching

## Example
`/session-log` - Create session note for current conversation
`/session-log detailed` - Include full code snippets
`/session-log project:astro` - Tag with specific project
