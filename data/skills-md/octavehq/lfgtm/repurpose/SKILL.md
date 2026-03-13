---
name: repurpose
description: Repurpose existing content (text, file, URL) for a different audience, persona, or context using your Octave library. Use when user says "repurpose this", "adapt for [persona]", "convert this blog to email", "rewrite for a different audience", or provides existing content to transform.
---

# /octave:repurpose - Content Repurposing

Transform existing content for a different audience, persona, channel, or context—grounded in your Octave library.

## Usage

```
/octave:repurpose <source>
```

Where `<source>` can be:
- **Text**: Direct text content (in quotes or pasted)
- **File**: Path to a local file
- **URL**: Web page or document URL

## Examples

```
/octave:repurpose "Our platform reduces deployment time by 80%..."
/octave:repurpose ./content/enterprise-whitepaper.md
/octave:repurpose https://blog.company.com/our-product-launch
/octave:repurpose --from "CTO audience" --to "CFO audience"
```

## Instructions

When the user runs `/octave:repurpose`:

### Step 1: Capture the Source Content

**Identify the source type and extract content:**

If text provided directly:
```
Got it! I've captured your content:
---
[Preview first 200 chars]...
---
[X words total]
```

If file path provided:
- Read the file using Read tool
- Confirm the content was loaded

If URL provided:
- Fetch the content using WebFetch
- Extract the main content

If no source provided, ask:
```
What content would you like to repurpose?

1. Paste text directly
2. Provide a file path
3. Provide a URL
4. Upload a document

(Paste your content or provide a path/URL):
```

### Step 2: Understand the Repurposing Goal

Ask clarifying questions to understand the transformation:

```
Great! Now let's define how to repurpose this content.

WHO is this for?
(Select a persona, segment, or describe the audience)

1. [List personas from library via list_all_entities]
2. [List segments from library]
3. Describe a custom audience

Your choice:
```

After persona/audience selection:

```
WHAT transformation do you need?

1. Adjust tone/voice for [selected persona]
2. Change format (e.g., blog → email, whitepaper → one-pager)
3. Shift focus/angle (e.g., technical → business value)
4. Adapt for different channel (LinkedIn, email, presentation)
5. Condense/expand length
6. Multiple transformations

Your choice:
```

Optional follow-up:

```
Any specific instructions or changes?

Examples:
- "Focus more on ROI and cost savings"
- "Make it more conversational"
- "Remove technical jargon"
- "Add a stronger CTA"
- "Keep the same structure but change examples"

(Enter instructions or press Enter to skip):
```

### Step 3: Gather Library Context

Based on the repurposing goal, fetch relevant context:

**For Persona-Based Repurposing:**
```
# Get persona details
get_entity({ oId: "<selected_persona_oId>" })

# Get relevant playbook for messaging guidance
search_knowledge_base({
  query: "<persona name> messaging value proposition",
  entityTypes: ["playbook"]
})

# Get brand voice if adjusting tone
list_brand_voices()

# Get writing style if specified
list_writing_styles()
```

**For Segment-Based Repurposing:**
```
# Get segment details
get_entity({ oId: "<selected_segment_oId>" })

# Find personas in this segment
search_knowledge_base({
  query: "<segment name> persona buyer",
  entityTypes: ["persona"]
})

# Get relevant playbooks
search_knowledge_base({
  query: "<segment name>",
  entityTypes: ["playbook"]
})
```

**For Format/Channel Changes:**
```
# Get brand voice guidelines
list_brand_voices()

# Get writing style for target format
search_knowledge_base({
  query: "<target format> writing style",
  entityTypes: ["writing_style"]
})
```

### Step 4: Confirm Transformation Plan

Present the transformation plan before executing:

```
REPURPOSING PLAN
================

Source Content:
- Type: [Blog post / Email / Document / etc.]
- Length: [X words]
- Original audience: [Inferred or stated]

Target:
- Audience: [Selected persona/segment]
- Format: [Same / Changed to X]
- Tone: [Based on brand voice / persona]

Key Changes:
1. [Change 1 - e.g., "Shift from technical features to business outcomes"]
2. [Change 2 - e.g., "Add CFO-relevant proof points"]
3. [Change 3 - e.g., "Shorten to 300 words for email"]

Context I'll Use:
- Persona: [Name] - [Key pain points to address]
- Playbook: [Name] - [Key messaging angle]
- Brand Voice: [Name] - [Tone characteristics]

Proceed with repurposing? (yes / adjust plan):
```

### Step 5: Generate Repurposed Content

Use the `generate_content` MCP tool with gathered context:

```
generate_content({
  instructions: `
    Repurpose the following content for [persona/audience].

    ORIGINAL CONTENT:
    ${originalContent}

    TARGET PERSONA: [Persona details from library]
    - Pain points: [List]
    - Priorities: [List]
    - Communication preferences: [Details]

    TARGET FORMAT: [Format]

    TONE/VOICE: [Brand voice guidelines]

    SPECIFIC INSTRUCTIONS:
    ${userInstructions}

    KEY CHANGES TO MAKE:
    1. [Change 1]
    2. [Change 2]
    3. [Change 3]

    Maintain the core message while adapting language, examples, and emphasis
    to resonate with the target audience.
  `,
  customContext: "[Relevant playbook messaging, proof points, etc.]"
})
```

### Step 6: Present Results

```
REPURPOSED CONTENT
==================

[Generated content]

---

CHANGES MADE
------------
✓ [Change 1 description]
✓ [Change 2 description]
✓ [Change 3 description]

CONTEXT APPLIED
---------------
- Persona pain points addressed: [List]
- Messaging angle: [From playbook]
- Tone: [From brand voice]

---

What would you like to do?

1. Refine further (provide feedback)
2. Try a different angle
3. Repurpose for another audience
4. Save to library as a template
5. Done - copy to clipboard
```

### Step 7: Iterate if Needed

If the user wants refinement:

```
What would you like me to adjust?

1. Make it more [formal/casual/urgent/etc.]
2. Focus more on [specific topic]
3. Add [specific element]
4. Remove [specific element]
5. Change the CTA
6. Other (describe)

Your feedback:
```

Then regenerate with updated instructions.

## Common Repurposing Scenarios

### Blog → Email Sequence
```
Source: Long-form blog post (1500 words)
Target: 3-email nurture sequence

Transformation:
1. Extract key insights for email hooks
2. Break into digestible pieces
3. Add persona-specific CTAs
4. Adjust tone for 1:1 communication
```

### Technical Doc → Executive Summary
```
Source: Technical whitepaper
Target: C-suite one-pager

Transformation:
1. Remove technical jargon
2. Lead with business outcomes
3. Add ROI/metrics focus
4. Condense to 1 page
5. Include executive-relevant proof points
```

### Internal → External
```
Source: Internal product brief
Target: Customer-facing content

Transformation:
1. Remove internal references
2. Reframe features as benefits
3. Add social proof
4. Apply brand voice
5. Include appropriate CTAs
```

### One Persona → Another
```
Source: Content for technical evaluators
Target: Content for economic buyers

Transformation:
1. Shift from features to outcomes
2. Add financial impact language
3. Include ROI proof points
4. Adjust complexity level
5. Change CTAs (demo → business case)
```

## MCP Tools Used

### Read Operations
- `list_all_entities` - Get available personas and segments
- `list_brand_voices` - Get available brand voice configurations
- `list_writing_styles` - Get available writing style configurations
- `get_entity` - Get full details for persona and segment entities by oId
- `get_playbook` - Get messaging guidance and value props
- `search_knowledge_base` - Find relevant proof points, messaging, examples

### Write Operations
- `generate_content` - Generate the repurposed content with context

### External Content
- WebFetch tool - Fetch content from URLs

## Input Handling

### Text Input
Accept text directly in the command or pasted in follow-up:
```
/octave:repurpose "Your content here..."
```

### File Input
Accept local file paths:
```
/octave:repurpose ./path/to/content.md
/octave:repurpose /absolute/path/to/document.txt
```

Supported file types: .md, .txt, .doc, .docx, .pdf, .html

### URL Input
Accept web URLs:
```
/octave:repurpose https://example.com/blog-post
```

Use WebFetch to extract content, then proceed with repurposing.

## Error Handling

**No Source Content:**
> I need content to repurpose. Please provide:
> - Text (paste directly)
> - File path (e.g., ./content/blog.md)
> - URL (e.g., https://blog.example.com/post)

**File Not Found:**
> I couldn't find the file at [path].
> Please check the path and try again, or paste the content directly.

**URL Fetch Failed:**
> I couldn't fetch content from [URL].
>
> This might be because:
> - The page requires authentication
> - The URL is incorrect
> - The site blocks automated access
>
> Try: Paste the content directly, or provide a different URL.

**No Personas/Context in Library:**
> Your library doesn't have personas defined yet.
>
> I can still repurpose content, but it will be more generic.
>
> Options:
> 1. Describe your target audience manually
> 2. Create a persona first (/octave:library create persona)
> 3. Proceed without persona context

**Content Too Long:**
> The source content is quite long ([X words]).
>
> Options:
> 1. Repurpose the full content (may take longer)
> 2. Select a section to repurpose
> 3. Let me summarize first, then repurpose the summary

## Related Skills

- `/octave:generate` - Generate new content from scratch
- `/octave:library` - Manage personas, playbooks, and other context
- `/octave:brainstorm` - Brainstorm content ideas
- `/octave:pmm` - Create marketing collateral
- `/octave:campaign` - Multi-channel campaign content
