---
name: interactive-input
description: Enables rich interactive UI components in chat responses. When presenting questions that require structured input (multiple choice, true/false, forms), embed interactive blocks that compatible clients render as native UI elements. Use when user asks for quizzes, exercises, surveys, or any structured input scenario.
---

# Interactive Input Blocks

Embed interactive UI components (radio buttons, checkboxes, text fields, toggles) directly in chat responses. Compatible clients render these as native UI elements; other clients show a readable JSON code block as fallback.

## When to Use

- Quizzes and exercises (single/multiple choice, fill-in-the-blank)
- Surveys and polls
- Structured data collection (forms)
- Any scenario where the user needs to select from options or provide structured input

## How It Works

Wrap a JSON block in a ` ```interactive ` code fence within your normal markdown response. You can mix regular text and interactive blocks freely in the same message.

## Schema Reference

See `references/schema.md` for the complete schema specification.

## Quick Example

When presenting a multiple-choice question, instead of listing options as text:

````markdown
Here's your first question:

```interactive
{
  "id": "q1",
  "card": {
    "body": [
      { "type": "TextBlock", "text": "What is the capital of France?", "weight": "bold" },
      { "type": "Input.ChoiceSet", "id": "answer", "style": "expanded",
        "choices": [
          { "title": "A. London", "value": "london" },
          { "title": "B. Paris", "value": "paris" },
          { "title": "C. Berlin", "value": "berlin" },
          { "title": "D. Madrid", "value": "madrid" }
        ]
      }
    ],
    "actions": [{ "type": "Action.Submit", "title": "Submit" }]
  }
}
```
````

## Rules

1. Every interactive block MUST have a unique `id` field
2. Every interactive block MUST have at least one element in `card.body`
3. Include an `Action.Submit` in `card.actions` so the user can submit their response
4. Use `"style": "expanded"` for choice sets to show all options visually (recommended for quizzes)
5. Use `"style": "compact"` for dropdown selects when there are many options
6. Set `"isMultiSelect": true` on `Input.ChoiceSet` for multiple-choice questions
7. The first `TextBlock` in the body is used as the question label in the submitted response
8. You can include multiple interactive blocks in one message (e.g., a full quiz)
9. Always wrap the JSON in a ` ```interactive ` code fence — never use ` ```json ` for interactive blocks
10. Keep the JSON compact and valid — no comments, no trailing commas
