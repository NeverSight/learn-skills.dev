---
name: x-tech-articlewriter
description: Specialized skill for crafting high-engagement, long-form tech articles and threads for X (Twitter). Use when the user wants to write technical tutorials, industry news analysis, product deep-dives, or software update announcements that are optimized for X's algorithm, mobile readability, and viral potential.
---

# X-Tech-ArticleWriter

## Overview
This skill transforms technical content into "Perfect Tech X Articles" using a proven engagement-optimized structure. It handles everything from hook generation to body formatting and CTA strategy.

## Workflow

### 1. Analysis & Strategy
- Analyze the source material (links, docs, or ideas).
- **Research & Fact-Check**: If the article mentions AI models or specific software, ensure you use the latest released versions and factual technical data.
- Determine the article type:
  - **Tutorial/Setup**: Step-by-step guidance.
  - **Product Deep-Dive**: Feature-benefit analysis.
  - **Industry News**: Contextual analysis of events.
  - **Dev Updates/Patch Notes**: technical change lists.

### 2. Drafting the Components
Follow the patterns in [article_format.md](references/article_format.md):
- **Title**: Create 3 **click-worthy** options (Numerical, Benefit-driven, Curiosity Gap). Focus on searchability and thumb-stopping power.
- **The Hook**: Draft the first 200 characters to ensure the "Show More" interaction is triggered.
- **Body**: Organize into sections with **bold headers** and **bullet points**.
- **Visuals**: Use the `generate_image` tool to create a relevant 5:2 aspect ratio header image for every article.
- **CTA**: Craft a context-specific call to interaction.

### 3. Formatting Standards
- **Paragraphs**: Max 3-4 lines for mobile readability.
- **Emphasis**: Bold key terms, use italics for nuance.
- **Punctuation**: **DO NOT USE EM-DASHES (`—`)**. Use colons, commas, or start new sentences instead.
- **Code**: Use blocks for technical snippets.
- **Links**: Use descriptive link text.

## Resources
- **references/article_format.md**: Detailed breakdown of successful engagement patterns.

## Example Request
"I want to write an article about setting up a private AI server on Mac using Clawbot."
-> *Response will follow the 6-step tutorial structure with a benefit-driven title and a high-stakes hook.*
