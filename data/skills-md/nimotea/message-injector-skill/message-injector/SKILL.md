---
name: message-injector
description: Inject information from a source text into a target template with placeholders. This skill MUST ONLY be triggered when the user explicitly uses the keyword "--提取".
---

# Message Injector

This skill extracts information from a provided source text and injects it into a target template string that contains placeholders.

## Trigger Keyword
**CRITICAL**: This skill should ONLY be used when the user message contains the exact keyword `--提取`. If this keyword is missing, do NOT use this skill.

## When to use this skill
- When the user provides a source text and a template, AND includes the `--提取` keyword.
- When the user explicitly asks to "extract" information into a template using the `--提取` command.

## Instructions
1.  **Analyze the Source Text**: Identify key entities and information in the source text that correspond to the placeholders in the template.
2.  **Identify Placeholders**: Locate all placeholders in the template string.
3.  **Extract and Map**: Map the information from the source text to the corresponding placeholders.
4.  **Inject**: Replace the placeholders in the template with the extracted values.
5.  **Output Format**: 
    - **PLAIN TEXT**: Return only the final string with the injected values.
    - **NO FILE WRITING**: Do NOT write the result to any file. Only return the text in the chat response.

## Examples

### Example 1
**Input**:
--提取 Source: "The meeting is at 2 PM on Friday in Room 101."
Template: "Reminder: Meeting at {time} on {day} in {location}."

**Output**:
Reminder: Meeting at 2 PM on Friday in Room 101.

### Example 2
**Input**:
--提取 Source: "User john_doe signed up with email john@example.com."
Template: "Welcome, {{username}}! We sent a verification link to {{email}}."

**Output**:
Welcome, john_doe! We sent a verification link to john@example.com.
