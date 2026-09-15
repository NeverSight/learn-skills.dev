---
name: architecture-diagram-gpt-imagegen
description: Generate a copy-paste-ready GPT prompt that produces a polished architecture or workflow diagram image, and optionally render the image directly via Codex CLI image generation. Trigger when the user wants to create, make, generate, draw, or visualize a diagram, architecture image, system workflow picture, or flowchart, or pastes a Mermaid diagram asking for a polished image.
---

# Architecture Diagram GPT Image Generator

Produce a GPT prompt that, when pasted into a chat model, generates a polished architecture or workflow diagram image. Write the prompt to a file. Keep chat output to the file path only.

## Output Discipline

When this skill fires:

1. Write the full prompt to `~/diagram-prompts/<slug>.md`. Create the directory if missing. `<slug>` is short kebab-case inferred from the topic.
2. The file content must be the prompt and nothing else.
3. The chat reply must be exactly:

```text
Prompt -> /home/arthur/diagram-prompts/<slug>.md
Open the file, copy all, paste into GPT.
```

4. Do not echo the prompt body back into chat after writing it.

## Minimum Input

The user may give:

- A Mermaid diagram
- A rough voice-note style description
- A list of services and connections
- A request to diagram the current project

If critical flow direction or system intent is genuinely ambiguous, ask one short clarifying question. Otherwise fill gaps from the defaults below.

## Mandatory Defaults

Always apply these unless the user explicitly overrides them:

1. Orientation defaults to horizontal left-to-right.
2. Image aspect ratio defaults to 16:9 horizontal landscape.
3. The prompt must be self-contained and usable in a fresh chat session.
4. Mermaid source inside the prompt should default to `flowchart LR`.

## Prompt Template

Write the prompt file using this structure, adapting the content to the specific diagram:

```text
Create a polished enterprise architecture diagram image. Render the image in 16:9 horizontal landscape aspect ratio. Do NOT output Mermaid code. Do NOT explain the diagram. Your task is to GENERATE AN IMAGE based on the specification below.

## Layout & system boundary

- Image canvas: 16:9 horizontal landscape
- Horizontal left-to-right layout
- [system-boundary containers and spatial arrangement]

## Visual style

- Clean, modern, enterprise-grade architecture diagram
- Rounded containers, soft shadows, generous spacing
- Crisp directional arrows; label branches on every decision diamond
- Minimal text inside nodes — use icons or emojis for meaning
- Prioritize clarity over technical detail

## Logos & icon mapping

Use recognizable logos for:
- [services that appear in the diagram]

Use visual metaphors:
- [emojis used in the diagram]

## Flow structure

[numbered left-to-right stages, grouping nodes and decisions]

## Color guidance

- System container: [platform tint]
- Entry points or triggers: warm red or amber
- Inputs or read tools: green
- AI or prompt nodes: purple or blue
- Decisions or retry loops: neutral blue-gray
- Output channels: green
- Per-service nodes use brand colors

## Semantic constraints

- [topology, ordering, and decision rules]

## Source structure (for reference only, do not output)

```mermaid
[mermaid source from the user or inferred from the description]
```
```

## Default Logo Library

Map products and systems to recognizable logos when relevant:

- Jira
- Bitbucket
- Slack
- Databricks
- AWS
- Kubernetes
- Datadog
- Confluence
- OpenAI
- Claude
- GitHub
- Google Sheets
- Java or backend services

If a service is not covered, use a plain rounded box with a fitting emoji.

## Default Visual Metaphors

Use emojis only when a concept has no natural product logo. Useful defaults include:

- `📄` prompt or document
- `🏷️` classification or label
- `💬` rationale or comment
- `⚙️` decision logic or processing
- `🛠️` fix or modification
- `🔒` validation
- `📣` routing
- `🚨` alert or failure
- `✅` success
- `❌` failure
- `⏰` schedule
- `🔁` retry loop
- `🔍` search or lookup
- `📊` metrics
- `🧠` AI or agent
- `🗄️` storage
- `📥` input
- `📤` output

## Parsing The User's Input

1. Identify services and products, then map them to logos.
2. Identify flow direction. Default to horizontal LR except genuine hierarchy-heavy exceptions.
3. Identify containers or subgraphs.
4. Identify decision diamonds and label both branches.
5. Identify retry loops and label them clearly.
6. Apply colors by role.
7. Build a Mermaid source block so the generator has a spatial spine.

## File Writing

Create `~/diagram-prompts` if it does not exist, then write the full prompt to `~/diagram-prompts/<slug>.md`. Do not add timestamps unless the user explicitly asks.

## Final Chat Reply

After the file is written, the chat reply must be exactly:

```text
Prompt -> /home/arthur/diagram-prompts/<slug>.md
Open the file, copy all, paste into GPT — or reply "imagegen" to render it directly via Codex CLI.
```

## Optional Codex Image Generation

If the user explicitly replies with `imagegen`, `yes generate`, `render it`, or another clear affirmative, run the local helper that turns the prompt into an image and return only the image path plus a one-line open command.
