---
name: Celebrity Quotes
description: Generate 5 inspirational quotes from a given celebrity with context and images.
user-invocable: true
auto-invoke: false
version: "1.0.1"
capabilities: ["generate_image"]
---

# Celebrity Quotes

Given a celebrity name, generate 5 inspirational quotes attributed to them. For each quote, provide the following in both English and Chinese:

1. The quote itself (Original English and Chinese translation).
2. A brief context or interpretation of why it is inspirational (In both English and Chinese).
3. An image generated for the quote using the `generate_image` tool.

## Input

- `<celebrity_name>`: The name of the celebrity to generate quotes for.

## Instructions

1. Search for or recall 5 famous and inspirational quotes by the specified `<celebrity_name>`.
2. Format the output as a list of 5 items.
3. For each item:
   - Provide the quote and a sentence context, rendered in both English and Chinese.
   - Use the `generate_image` tool to create a visually stunning image that reflects the theme of the quote. Use the quote and the celebrity's persona to craft the prompt.
