---
name: create-topic-note
description: "Create a Commentary topic note grouping related notes under a common theme, with automatic backlinking to source notes. Triggers: 'group these under a topic', 'create topic note for [[A]], [[B]], [[C]]'."
argument-hint: "<topic title> [[[note1]]] [[[note2]]] ..."
metadata:
  author: nweii
  version: "1.0.0"
  internal: true
---

# Create topic note

Create a new topic note that groups related notes under a common theme. Synthesizes provided notes into a lightweight hub.

## Arguments

`$ARGUMENTS` should contain:

- **Topic title** (required) — name for the new topic note
- **Notes to group** — wikilinks or file paths to notes that share a theme

If no notes are provided, prompt for them. If no title is given but notes are provided, suggest a title based on the notes' common theme.

## Process

### 1. Read the provided notes

Read each note's frontmatter (especially `description`) and skim content to understand:

- Common themes and concepts
- Shared vocabulary or framing
- The throughline that connects them

### 2. Expand context (optional)

Use available tools to discover additional relevant notes not explicitly provided:

- Follow wikilinks in the provided notes to find related children or siblings
- Use semantic search to find notes with similar themes
- Check `related` properties for existing connections worth including
- Search for shared tags or vocabulary

If you find notes that clearly belong under this topic, propose adding them to the group. Ask the user before including notes they didn't explicitly provide.

### 3. Create the topic note

Create a new file in `03-Records/Topics/` with this structure:

```yaml
---
aliases:
  - {alternative names if useful}
categories: ["[[Commentary]]"]
icon:
description: "{1-2 sentence summary synthesized from the grouped notes}"
related: []
tags: [{relevant topical tags, drawn from the grouped notes}]
---

{Optional 1-2 sentences of context if needed, otherwise leave blank}

![[Related.base]]
```

#### Description guidelines

- Synthesize a shorthand summary that captures what connects the grouped notes
- Use terse telegraphic style: semicolons, commas, dashes over conjunctive adverbs
- Stay under 200 characters when possible
- Focus on the conceptual throughline, not an exhaustive list

#### Tag selection

- Pull relevant tags from the grouped notes
- Add `topics` tag if not present
- Keep to 5-10 tags max

### 4. Update source notes

For each note provided, add the new topic note to its `related` property:

```yaml
related:
  - "[[New Topic Note Title]]"
  - ... existing related items
```

If `related` doesn't exist, create it. Place new items at the beginning of the list.

## Output

1. The new topic note file
2. Confirmation of which notes were updated with the `related` backlink

## Example

**Input**: "Group these under a topic about attention economy critique: [[Platforms engineer compulsive consumption]], [[Optimizing for attention undermines quality experience]], [[Social media commoditizes intrinsic needs]]"

**Creates**: `03-Records/Topics/Attention economy critique.md` with description synthesized from those notes

**Updates**: Each input note gets `"[[Attention economy critique]]"` added to its `related` property
