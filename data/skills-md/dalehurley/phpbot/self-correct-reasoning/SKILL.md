---
name: self-correct-reasoning
description: "Analyze and correct previous responses when questioned or when contradictions are detected. Use this skill when the user challenges your reasoning, points out inconsistencies, or asks 'what makes you think that?' to help you review your logic, identify errors in your previous statements, and provide accurate corrections. Useful for maintaining consistency, admitting mistakes, and rebuilding trust through transparent self-evaluation."
tags: [reasoning, error-correction, self-evaluation, conversation-management, quality-assurance, auto-generated]
version: 0.1.0
---

# Skill: self-correct-reasoning

## When to Use
Use this skill when:
- The user questions your reasoning with phrases like 'what makes you think that?', 'why do you say that?', or 'how did you get that?'
- You detect contradictions between your current statement and previously retrieved data
- You realize you made an unsupported claim or logical error
- The user challenges the accuracy or consistency of your response
- You need to review and correct a previous answer

## Input Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `user_challenge` | Yes | The user's question or statement challenging your previous response | what makes you think that? |
| `previous_response` | Yes | Your earlier statement or claim that is being questioned | no raincoat needed |
| `relevant_context` | No | Previously retrieved data, facts, or information relevant to the claim | Sydney weather forecast showing light drizzle and patchy rain |

## Procedure
1. Identify the specific claim or response being questioned
2. Review the conversation history and any data you previously retrieved or stated
3. Check for contradictions between your claim and the actual data or facts presented
4. Identify the logical error, unsupported assumption, or inconsistency
5. Acknowledge the error explicitly and explain what went wrong
6. Provide the correct answer based on the actual data or sound reasoning
7. Apologize if appropriate and thank the user for catching the mistake

## Example

Example requests that trigger this skill:

```
what makes you think that?
```
