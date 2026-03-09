---
name: ascii
description: "Creates ASCII diagrams for flows, architectures, sequence diagrams, state machines, and tree hierarchies. Offers to save the result to a file."
---

# ASCII Diagram Generator

Create ASCII diagrams for flows, architectures, and processes.

Arguments: $ARGUMENTS

## Instructions

Generate an ASCII diagram based on the user's description provided in `$ARGUMENTS`.

**If no arguments provided**, ask the user what they want diagrammed.

### Phase 1: Analyze the Request

1. Parse the `$ARGUMENTS` to understand what flow/diagram is needed
2. Identify the type of diagram:
   - **Flow diagram**: Sequential steps with arrows
   - **Architecture diagram**: Boxes representing components
   - **Sequence diagram**: Interactions between entities
   - **Tree/hierarchy**: Parent-child relationships
   - **State machine**: States and transitions

### Phase 2: Create the Diagram

Generate a clean ASCII diagram using these conventions:

**Boxes**:
```
┌─────────────┐
│   Label     │
└─────────────┘
```

**Arrows**:
- Horizontal: `───>` or `<───`
- Vertical: `│` with `▼` or `▲`
- Bidirectional: `<──>`

**Flow connections**:
```
┌───────┐     ┌───────┐
│ Step1 │────>│ Step2 │
└───────┘     └───────┘
```

**Decision points**:
```
    ┌───────┐
    │ Check │
    └───┬───┘
        │
   ┌────┴────┐
   ▼         ▼
┌─────┐   ┌─────┐
│ Yes │   │ No  │
└─────┘   └─────┘
```

**Guidelines**:
- Keep boxes aligned and evenly spaced
- Use consistent widths where possible
- Add labels to arrows when needed: `──(label)──>`
- Use comments/notes outside the diagram for context
- Keep it readable — don't overcrowd

### Phase 3: Present the Diagram

Display the completed ASCII diagram in a code block:

```
[Your ASCII diagram here]
```

### Phase 4: Ask About Saving

After showing the diagram, ask the user what they'd like to do:

```
What would you like to do with this diagram?

1. Save to a new markdown file
2. Add to an existing file
3. Don't save (just viewing)
```

Use the AskUserQuestion tool with these options:
- **Save to new file**: Ask for filename, create `[filename].md` with the diagram in a code block
- **Add to existing file**: Ask which file, then append the diagram to that file
- **Don't save**: Acknowledge and end

### Saving Behavior

**New file format**:
```markdown
# [Title based on diagram content]

[ASCII diagram in code block]

---
*Generated with /ascii*
```

**Appending to existing file**:
- Add a newline separator
- Insert the diagram in a code block
- Don't modify existing content

## Examples

**Input**: `/ascii user login flow`

**Output**:
```
┌──────────┐     ┌────────────┐     ┌──────────────┐
│  User    │────>│ Login Form │────>│ Validate     │
└──────────┘     └────────────┘     └──────┬───────┘
                                           │
                                    ┌──────┴──────┐
                                    ▼             ▼
                              ┌─────────┐   ┌─────────┐
                              │ Success │   │ Error   │
                              └────┬────┘   └────┬────┘
                                   │             │
                                   ▼             ▼
                              ┌─────────┐   ┌─────────┐
                              │Dashboard│   │ Retry   │
                              └─────────┘   └─────────┘
```

**Input**: `/ascii api request lifecycle`

**Output**:
```
┌────────┐    ┌────────────┐    ┌────────────┐    ┌──────────┐
│ Client │───>│ Middleware │───>│ Controller │───>│ Service  │
└────────┘    └────────────┘    └────────────┘    └────┬─────┘
     ▲                                                 │
     │                                                 ▼
     │                                           ┌──────────┐
     │                                           │ Database │
     │                                           └────┬─────┘
     │                                                │
     └────────────────────────────────────────────────┘
                        Response
```
