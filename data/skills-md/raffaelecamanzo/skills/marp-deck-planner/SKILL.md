---
name: marp-deck-planner
description: Plan a MARP presentation from a high-level deck definition (sections, key messages, constraints). Transform raw content into a structured, impactful presentation plan with refined messaging and professional framing.
---

# Marp Deck Planner

## Purpose

Generate a **presentation plan**, not a finished deck.

The output must describe:
- slide sequence
- slide intent
- content structure (with **refined, presentation-ready language**)
- suggested visuals (described, not generated)

The planner must **not** generate diagrams, Mermaid code, or images.

**Critical difference from a simple outline:** This is a *transformation* task. Raw definition content must be refined into compelling presentation language that maintains fidelity to the original intent while improving clarity, impact, and professionalism.

---

## Content transformation principles

### What to preserve
- **Core message and intent** - never change what the definition is trying to communicate
- **Key facts, data, and claims** - maintain accuracy
- **Logical flow and relationships** between concepts
- **Constraints** specified in the definition (tone, audience, scope)

### What to transform
- **Wording and phrasing** - convert casual/raw language into presentation-ready copy
- **Structure and emphasis** - reorganize for maximum impact
- **Framing** - find the most compelling angle for each message
- **Specificity** - make vague statements concrete; make verbose statements concise

### Quality standards for presentation language

**DO:**
- Use active voice and strong verbs
- Lead with the insight, then support it
- Make titles declarative and specific (not generic labels)
- Use parallel structure within slide content
- Employ concrete, vivid language over abstractions
- Frame messages from the audience's perspective

**DON'T:**
- Copy-paste wording from the definition verbatim
- Use filler words ("basically", "essentially", "in order to")
- Create titles that are just topic labels ("Overview", "Background")
- Stack multiple complex ideas on one slide
- Use jargon without defining it first

---

## Output format

Produce a single Markdown file with this structure:

- Deck title:  
  `# <Deck Title> – Presentation plan`

- Slide separator:  
  A line containing only: ---

- **Standard slides** must contain:
  - `## Title`
  - `## Structure`
  - `## Content`
  - *(optional)* `## Image`

- **Section divider slides** must contain:
  - `## Section`
  - The section name on the next line  
    *(no other fields)*

- The file must be saved as:  
  `planning/deck-plan.md`

### Formatting rules

- Use bullet points, short phrases, and tables
- Include a full prose paragraph only when the message is important enough to warrant an entire slide
- No slide numbering
- Keep titles short, specific, and high-signal
- Prefer parallel phrasing across slides in the same section

---

## Workflow

### 1. Parse and internalize the definition

From `definition/deck-definition.md`, extract:
- Deck title (if present)
- Ordered section names
- Key messages for each section
- Explicit constraints (tone, audience, slide limits, mandatory topics)

**Important:** Understand the *intent* behind each message, not just the literal words.

---

### 2. Plan the slide sequence

- Optionally add **1–3 introductory slides** before the first section when context is required
- For each section:
  - Add **one section divider slide**
  - Add **2–5 standard slides** to cover the section's key messages
- Add a closing / next-steps slide **only if** the definition implies a call to action

---

### 3. Map and refine key messages

**For each key message:**

1. **Identify the core insight** - what's the one thing this message needs to communicate?
2. **Find the compelling angle** - why does this matter to the audience?
3. **Craft a declarative title** that captures the insight (not just labels the topic)
4. **Structure supporting points** to build toward the title's claim

**Example transformation:**

*Definition says:*  
"We need to talk about how our current system has problems with scalability and this causes issues when we try to grow"

*Presentation plan says:*

Title: "Current architecture cannot scale beyond 50K users"

Content:
- Three infrastructure bottlenecks limit growth
- Database queries degrade 40% per 10K user increase  
- Resolution requires fundamental re-architecture, not patches

---

### 4. Define slide content (planning level)

For each **standard slide**:

#### `## Title`
Create a **specific, declarative title** that:
- States the slide's core message (not just the topic)
- Uses concrete language
- Could stand alone as a key takeaway

Bad: "Market Overview"  
Good: "Enterprise SaaS market growing 23% annually"

#### `## Structure`  
Describe layout intent using presenter's perspective:

- "Two columns: problem left, solution right"
- "Vertical flow building to conclusion"
- "Three-part framework with equal emphasis"

#### `## Content`  
Provide **refined bullet points** describing what goes on the slide.

**This is where transformation happens:**
- Rewrite definition content in presentation voice
- Use specific, active language
- Structure points for progressive disclosure
- Lead with the "so what"

**Example:**

*From definition:*  
"Users don't really understand how to use the feature and there's confusion about when to apply it"

*In Content section:*
- 67% of users unaware the feature exists
- Those who discover it misapply it in 40% of cases
- Root cause: hidden in settings, no contextual triggers
- Proposed: in-line prompts at relevant workflow moments

---

### 5. Describe visuals (no generation)

Add a `## Image` section **only when a visual clearly reinforces understanding**

The `## Image` section must contain:
- A **natural-language description** of the visual
- The **purpose** of the visual (what it clarifies or reinforces)

Examples:
- "Simple flow diagram: User action → System response → Feedback loop. Purpose: Show the circular nature of the interaction, not linear."
- "Side-by-side comparison: Current state (fragmented tools) vs. Future state (unified platform). Purpose: Visual contrast makes the value proposition immediate."
- "Stacked bar chart showing cost breakdown across three scenarios. Purpose: Make financial impact concrete and comparable."

Rules:
- Do **not** generate Mermaid code
- Do **not** reference files, assets, or tasks
- Do **not** assume the visual will actually be created

If a slide works better with text alone, omit `## Image`.

---

## Slide patterns (recommended)

Use these as defaults unless the definition suggests otherwise:

### **Opening framing slide**  
- Lead with the high-stakes context or question
- 2–4 brief statements that establish why this matters
- Title: Problem statement or opportunity framed

### **Insight slide**  
- One core principle or finding
- 3–5 supporting points building the case
- Title: The insight itself, stated declaratively

### **Comparison slide**  
- Two-column parallel structure
- Mirrored bullet points for easy scanning
- Title: What's being compared and the conclusion

### **Process/journey slide**  
- Sequential steps or phases
- Each with brief outcome or milestone
- Title: The transformation or path being described

### **Framework/model slide**  
- 2×2 matrix, Venn diagram, or categorization
- Each segment defined and labeled
- Title: The organizing principle

### **Evidence slide**  
- Data points or examples supporting a claim
- Visual emphasis on the key number or pattern
- Title: The claim being supported

---

## Quality checks (mandatory)

Before finalizing, ensure:

✓ Every section in the definition has a section divider slide  
✓ All key messages are represented (though reworded and refined)  
✓ No slide contains long-form prose (unless intentionally emphasized)  
✓ Slide titles are specific and declarative, not generic labels  
✓ Content bullets are in presentation voice, not copied from definition  
✓ Slide intent is unambiguous and builds a narrative arc  
✓ Visuals are described with clear purpose, not implemented  
✓ The plan reads like a professional presentation structure, not an outline

---

## Example transformation

### From definition:
"Talk about the reasons why we should consider moving to cloud infrastructure and what benefits that might bring"

### In presentation plan:

**Title:** Cloud migration reduces costs 35% while improving reliability

**Structure:**  
Two-part reveal: Cost impact first, then operational benefits

**Content:**
- Current on-premise infrastructure costs $2M annually
- Cloud-native approach projects at $1.3M (35% reduction)
- Built-in redundancy eliminates single points of failure
- Auto-scaling handles traffic spikes without over-provisioning
- Team shifts from maintenance to feature development

**Image:**  
Cost comparison graphic: Stacked bars showing on-premise vs. cloud total cost of ownership over 3 years. Purpose: Make the financial case visual and undeniable.

---

## Final note

The output must remain a **planning artifact** that can be directly executed by a deck builder, but the language and framing should already be presentation-ready. Think of this as the work a professional presentation consultant would do: understanding the raw content and transforming it into a compelling narrative structure.