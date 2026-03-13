---
name: summarization
description: Condenses long documents, conversation logs, or transcripts into concise summaries. Supports retrieval from memory/files, multiple output formats (bullet points, paragraphs, executive summary), and customizable detail levels. Use when the user needs to quickly understand large amounts of text content.
---

# Document & Conversation Summarization Skill

This skill provides comprehensive summarization capabilities for long documents, conversation logs, transcripts, and other text content. It combines intelligent retrieval with advanced summarization techniques to produce clear, actionable summaries.

## When to Use This Skill

Use this skill when:
- User requests a summary of a long document or file
- User wants to condense conversation logs or chat transcripts
- User needs to extract key points from meeting notes or recordings
- User asks to "summarize", "condense", "give me the highlights", or "what's the TLDR"
- Content is too long to read in full and needs to be distilled
- User wants to understand the main themes or topics in a large body of text

## Skill Capabilities

1. **Multi-source Retrieval**: Reads from files, directories, conversation history, or pasted text
2. **Format Flexibility**: Outputs in bullets, paragraphs, executive summary, or custom formats
3. **Detail Control**: Supports brief, standard, and detailed summary levels
4. **Smart Extraction**: Identifies key themes, action items, decisions, and critical information
5. **Context Awareness**: Understands code, technical docs, conversations, and general content

## Summarization Workflow

Follow this systematic workflow when the user requests a summary:

### Step 1: Identify the Source
Determine what needs to be summarized:
- **File/Document**: Use Read tool to load the content
- **Multiple Files**: Use Glob to find files, then Read each
- **Directory**: Use Glob with pattern matching, then batch read
- **Conversation History**: Reference the current conversation transcript
- **Pasted Content**: Work with text provided directly by the user
- **Web Content**: Use WebFetch if a URL is provided

**Actions**:
- Ask clarifying questions if the source is ambiguous
- Confirm the scope (single file vs. multiple files vs. entire directory)

### Step 2: Analyze Content Type
Identify what type of content you're summarizing:
- **Technical Documentation**: Focus on concepts, APIs, usage patterns
- **Code Files**: Explain purpose, key functions, architecture
- **Conversation Logs**: Extract topics, decisions, action items
- **Meeting Transcripts**: Identify attendees, agenda items, outcomes
- **Research Papers**: Highlight methodology, findings, conclusions
- **General Text**: Main themes, arguments, key points

**Actions**:
- Scan the content structure
- Note the length and complexity
- Identify special elements (code blocks, data tables, timestamps, etc.)

### Step 3: Determine Output Format
Ask the user or infer their preferred format:

**Available Formats**:

1. **Bullet Points** (Default for most use cases)
   ```markdown
   ## Summary
   - Key point 1
   - Key point 2
   - Key point 3

   ## Details
   - Supporting detail A
   - Supporting detail B
   ```

2. **Paragraph Format** (For narrative summaries)
   ```markdown
   ## Summary
   This document discusses... The main themes include...

   ## Key Insights
   The analysis reveals that...
   ```

3. **Executive Summary** (For business/formal contexts)
   ```markdown
   ## Executive Summary
   **Purpose**: [What is this about]
   **Key Findings**: [Main discoveries/points]
   **Recommendations**: [Action items if applicable]
   **Conclusion**: [Final takeaway]
   ```

4. **Hierarchical** (For complex multi-topic content)
   ```markdown
   ## Summary

   ### Topic 1: [Name]
   - Point A
   - Point B

   ### Topic 2: [Name]
   - Point C
   - Point D
   ```

5. **Custom Format** (User-specified structure)
   - Follow user's specific requirements

**Actions**:
- If user doesn't specify, use bullet points for short content, executive summary for long content
- Match the format to the content type (e.g., hierarchical for multi-section docs)

### Step 4: Set Detail Level
Determine how detailed the summary should be:

**Detail Levels**:

1. **Brief** (TLDR - 2-5 sentences or bullets)
   - Only the absolute essentials
   - One-line overview + top 3-5 points
   - Best for: Quick scans, very long content

2. **Standard** (Default - 1-2 paragraphs or 5-10 bullets)
   - Main themes and key points
   - Enough detail to understand the content
   - Best for: Most use cases

3. **Detailed** (Comprehensive - Multiple sections)
   - All major topics covered
   - Supporting details included
   - Maintains nuance and context
   - Best for: Complex technical docs, important decisions

4. **Custom** (User-defined)
   - Specific word/line/bullet count
   - Focus on particular sections
   - Special requirements

**Actions**:
- Default to "Standard" unless specified
- For content over 10,000 lines, suggest "Brief" first
- Offer to expand if user wants more detail

### Step 5: Extract and Organize Information
Process the content systematically:

**Extraction Strategy**:

1. **Read/Scan**: Load all content into context
2. **Identify Structure**: Note headings, sections, timestamps, speakers
3. **Extract Key Elements**:
   - Main topics/themes
   - Important decisions or conclusions
   - Action items or next steps
   - Critical data points or statistics
   - Names, dates, and key events
   - Questions or open issues

4. **Categorize**: Group related information together
5. **Prioritize**: Rank by importance and relevance

**Special Handling**:

- **Code**: Explain what it does, not line-by-line details
- **Conversations**: Track who said what, decisions made, action items
- **Technical Docs**: Focus on "what" and "how to use", less on implementation
- **Data**: Highlight trends, outliers, key statistics

### Step 6: Generate the Summary
Craft the summary following these principles:

**Quality Guidelines**:

1. **Clarity**: Use simple, direct language
2. **Accuracy**: Don't add information not in the source
3. **Completeness**: Cover all major points
4. **Conciseness**: Remove redundancy and filler
5. **Actionability**: Highlight decisions and next steps
6. **Context**: Maintain enough background for understanding

**Structure Template** (Standard Format):

```markdown
## Summary of [Document/Conversation Name]

**Source**: [File path or description]
**Length**: [Original size] → [Summary size]
**Type**: [Document type]

### Overview
[2-3 sentence high-level summary]

### Key Points
- [Most important point]
- [Second most important point]
- [Additional key points...]

### [Additional Sections as Needed]
- Action Items (if applicable)
- Decisions Made (for meetings/conversations)
- Technical Details (for code/docs)
- Recommendations (for analysis)
- Open Questions (if any)

### Conclusion
[Final takeaway or next steps]
```

### Step 7: Present and Iterate
Deliver the summary to the user:

**Presentation**:
- Use clear markdown formatting
- Add source references if summarizing multiple files
- Include line numbers or timestamps for important points (e.g., "Decision made at line 234")
- Provide context for technical terms

**Follow-up Options**:
- "Would you like me to expand on any particular section?"
- "I can provide a more detailed summary if needed"
- "Should I focus on a specific aspect of this content?"
- "Would you like summaries of the individual sections?"

**Actions**:
- Present the complete summary
- Offer to adjust detail level or format
- Be ready to drill down into specific sections

## Example Workflows

### Example 1: Summarizing a Single Document

```
User: "Summarize the README.md file"

Assistant Actions:
1. Read /path/to/README.md
2. Identify it's technical documentation
3. Use bullet point format (good for docs)
4. Extract: purpose, installation, usage, features
5. Generate standard-level summary
6. Present with clear sections
```

### Example 2: Summarizing a Conversation Log

```
User: "Can you summarize our last conversation about the API design?"

Assistant Actions:
1. Reference conversation history
2. Identify it's a technical discussion
3. Use executive summary format
4. Extract: decisions, alternatives discussed, action items
5. Generate detailed summary
6. Include timestamps or message references
```

### Example 3: Summarizing Multiple Files

```
User: "Summarize all Python files in the src/ directory"

Assistant Actions:
1. Glob: "src/**/*.py"
2. Read each file
3. Identify they're code files
4. Use hierarchical format (one section per file)
5. For each file: purpose, key functions, dependencies
6. Generate standard-level summary
7. Present with file paths for navigation
```

### Example 4: Custom Format Request

```
User: "Give me a 3-bullet TLDR of the meeting transcript"

Assistant Actions:
1. Read the transcript file
2. Identify format: brief (TLDR)
3. Extract only the 3 most critical points
4. Present as simple bullet list
5. Offer to expand if needed
```

## Advanced Features

### Multi-file Summarization
When summarizing multiple files:
1. Process each file individually
2. Identify common themes across files
3. Create a high-level overview
4. Provide per-file details in sub-sections
5. Cross-reference related content

### Conversation Log Analysis
For chat/meeting transcripts:
1. Identify speakers/participants
2. Track topic transitions
3. Extract decisions with who decided
4. List action items with owners
5. Note unresolved questions
6. Include timestamps for key moments

### Code Summarization
For source code:
1. Explain the file's purpose
2. List main functions/classes and what they do
3. Note dependencies and imports
4. Highlight complex or critical sections
5. Identify potential issues or TODOs
6. Explain the architecture pattern

### Incremental Summarization
For very large content (>50,000 lines):
1. Split into logical chunks
2. Summarize each chunk
3. Synthesize chunk summaries into final summary
4. Maintain coherence across chunks

## Best Practices

1. **Always Read First**: Don't summarize without reading the actual content
2. **Preserve Accuracy**: Don't invent details not in the source
3. **Maintain Context**: Include enough background for the summary to make sense
4. **Be Objective**: Don't add opinions unless the source includes them
5. **Highlight Actionable Items**: Decisions, next steps, and action items are critical
6. **Use Source References**: Link back to specific locations when possible
7. **Match User's Needs**: Brief for quick overview, detailed for deep understanding
8. **Offer Options**: Let users request more or less detail
9. **Format for Readability**: Use markdown, headings, and lists effectively
10. **Note Limitations**: If content is truncated or incomplete, mention it

## Common User Requests and Responses

| User Says | Your Action |
|-----------|-------------|
| "Summarize this file" | Read → Standard bullet summary |
| "Give me the TLDR" | Brief summary (2-5 points) |
| "What's this document about?" | Overview paragraph + key points |
| "Summarize our conversation" | Review history → Extract main topics and decisions |
| "Condense this into bullets" | Bullet point format, standard detail |
| "I need an executive summary" | Executive summary format, detailed level |
| "Just the highlights" | Brief format, top 3-5 points only |
| "Detailed summary please" | Detailed level with all major points |
| "Summarize all files in X" | Multi-file hierarchical summary |

## Error Handling

- **File not found**: Ask user to confirm the path or provide the content
- **Very large files**: Warn about processing time, offer to summarize in chunks
- **Binary/non-text files**: Explain you can only summarize text content
- **Ambiguous request**: Ask clarifying questions about source and format
- **Empty or minimal content**: Note the content is too brief to summarize meaningfully

## Output Quality Checklist

Before presenting your summary, verify:
- [ ] Covers all major topics from the source
- [ ] Accurate (no invented information)
- [ ] Appropriate length for the detail level
- [ ] Clear and easy to understand
- [ ] Properly formatted in markdown
- [ ] Includes source reference
- [ ] Actionable items highlighted (if any)
- [ ] Offers next steps or expansion options

---

## Quick Reference

**Default Behavior**:
- Format: Bullet points
- Detail: Standard (5-10 main points)
- Structure: Overview + Key Points + Conclusion

**Remember**: The goal is to save the user time while preserving the essential information and context they need to understand the content.
