---
name: jira-expressions
description: Write and fix Jira expressions for ScriptRunner for Jira Cloud workflow conditions and validators, with the full language reference and worked examples. Use for any Jira expression, as they are not JavaScript and anything missing from the reference fails when it runs.
metadata:
    author: sms-core
    version: '1.0'
---

# Jira Expressions Skill

Use this skill whenever you need to write, review, or convert a Jira
expression. On ScriptRunner for Jira Cloud, workflow conditions and validators
must be implemented as Jira expressions (post functions remain Groovy-based).

## Activation Signals

- The task involves a Jira Cloud workflow condition or validator.
- The user asks for a Jira expression, or to convert Data Center Groovy
  workflow logic to Cloud.
- You are reviewing or debugging an expression that fails to evaluate.

## Workflow

1. If a `jira-expression-generator` subagent is available in your
   environment, delegate expression generation to it instead of using this
   skill's references directly - it embeds the same reference material.
2. Otherwise, read `references/reference.md` in full before writing any
   expression. Jira Expressions is **not** JavaScript: only the syntax,
   methods, and properties documented there exist, and anything else fails at
   runtime.
3. Read `references/examples.md` for worked condition and validator
   patterns before inventing your own.
4. Validate the result against the reference: a workflow condition or
   validator must evaluate to a boolean, and expensive-operation limits apply.

## Notes

- Output raw expression text only - no markdown fences and no language hint
  lines such as `jira-expression`.
- Apply null checks liberally (`?.`, `?? `, explicit `!= null`); hidden
  fields and missing custom fields return `null`.
- When converting from Data Center Groovy, preserve Groovy truthiness, null
  ordering, and string literals exactly as the reference's translation rules
  describe.
- If the request cannot be achieved with the Jira Expressions DSL, say so and
  explain the limitation instead of inventing undocumented syntax.
