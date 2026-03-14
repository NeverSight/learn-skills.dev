---
name: blog-writing-specialist
description: "Comprehensive blog writing skill that handles technical blog posts, personal voice writing, brain dump transformation, and category-aware AEO-optimized content. Use when: (1) writing, editing, or proofreading a blog article or post, (2) transforming unstructured brain dumps into polished posts, (3) writing in specific personal voices (Jarad, Nick Nisi), (4) creating category-aware technology/company/product posts, (5) building tutorials, deep dives, postmortems, benchmarks, or architecture posts, (6) writing engineering blogs, dev blogs, programming blogs, coding tutorials, or documentation posts. Triggers: blog post, blog writing, technical blog, dev tutorial, brain dump, article, content writing, developer article, engineering blog, programming blog, coding tutorial, documentation post, technical writing, blog editing, proofreading, developer content"
---

# Blog Writing Specialist

Comprehensive blog writing combining technical depth, personal voice transformation, and AEO optimization.

## Quick Decision Tree

| Input Type | Use Section |
|-----------|-------------|
| Technical tutorial, deep dive, benchmark | Technical Blog Writing |
| Brain dump → polished post | Nick Nisi Voice |
| Personal voice (Jarad style) | Jarad's Voice |
| Company/product/technology category post | Lightfast Category System |
| Not sure | Start here, adapt as needed |

---

# Part 1: Technical Blog Writing

Write developer-focused technical blog posts.

## Post Types

### 1. Tutorial / How-To

Step-by-step instruction. Reader should build something.

```
Structure:
1. What we're building (with screenshot/demo)
2. Prerequisites
3. Step 1: Setup
4. Step 2: Core implementation
5. Step 3: ...
6. Complete code (GitHub link)
7. Next steps / extensions
```

| Rule | Why |
|------|-----|
| Show the end result first | Reader knows if worth continuing |
| List prerequisites explicitly | Don't waste wrong audience time |
| Every code block should be runnable | Copy-paste-run is the test |
| Explain the "why" not just the "how" | Tutorials that explain reasoning get shared |
| Include error handling | Real code has errors |
| Link to complete code repo | Reference after tutorial |

### 2. Deep Dive / Explainer

Explains a concept, technology, or architecture decision in depth.

```
Structure:
1. What is [concept] and why should you care?
2. How it works (simplified mental model)
3. How it works (detailed mechanics)
4. Real-world example
5. Trade-offs and when NOT to use it
6. Further reading
```

### 3. Postmortem / Incident Report

Describes what went wrong, why, and what was fixed.

```
Structure:
1. Summary (what happened, impact, duration)
2. Timeline of events
3. Root cause analysis
4. Fix implemented
5. What we're doing to prevent recurrence
6. Lessons learned
```

### 4. Benchmark / Comparison

Data-driven comparison of tools, approaches, or architectures.

```
Structure:
1. What we compared and why
2. Methodology (so results are reproducible)
3. Results with charts/tables
4. Analysis (what the numbers mean)
5. Recommendation (with caveats)
6. Raw data / reproducibility instructions
```

### 5. Architecture / System Design

Explains how a system is built and why decisions were made.

```
Structure:
1. Problem we needed to solve
2. Constraints and requirements
3. Options considered
4. Architecture chosen (with diagram)
5. Trade-offs we accepted
6. Results and lessons
```

## Writing Rules for Developers

### Voice and Tone

| Do | Don't |
|----|-------|
| Be direct: "Use connection pooling" | "You might want to consider using..." |
| Admit trade-offs: "This adds complexity" | Pretend your solution is perfect |
| Use "we" for team decisions | "I single-handedly architected..." |
| Specific numbers: "reduced p99 from 800ms to 90ms" | "significantly improved performance" |
| Cite sources and benchmarks | Make unsourced claims |
| Acknowledge alternatives | Pretend yours is the only way |

### What Developers Hate

```
❌ "In today's fast-paced world of technology..." (filler)
❌ "As we all know..." (if we all know, why writing it?)
❌ "Simply do X" (nothing is simple if reading a tutorial)
❌ "It's easy to..." (dismissive of reader's experience)
❌ "Obviously..." (if obvious, don't write it)
❌ Marketing language in technical content
❌ Burying the lede under 3 paragraphs of context
```

### Code Examples

| Rule | Why |
|------|-----|
| Every code block must be runnable | Broken examples destroy trust |
| Show complete, working examples | Snippets without context are useless |
| Include language identifier in fenced blocks | Syntax highlighting |
| Show output/result after code | Reader verifies understanding |
| Use realistic variable names | `calculateTotalRevenue` not `foo` |
| Include error handling in examples | Real code handles errors |
| Pin dependency versions | "Works with React 18.2" not "React" |

### Explanation Depth

| Audience Signal | Depth |
|----------------|-------|
| "Getting started with X" | Explain everything, assume no prior knowledge |
| "Advanced X patterns" | Skip basics, go deep on nuances |
| "X vs Y" | Assume familiarity with both, focus on differences |
| "How we built X" | Technical audience, can skip fundamentals |

**State your assumed audience level explicitly** at the start.

## Blog Post Structure

### The Ideal Structure

```markdown
# Title (contains primary keyword, states outcome)

[Hero image or diagram]

**TL;DR:** [2-3 sentence summary with key takeaway]

## The Problem / Why This Matters
[Set up why the reader should care — specific, not generic]

## The Solution / How We Did It
[Core content — code, architecture, explanation]

### Step 1: [First thing]
[Explanation + code + output]

### Step 2: [Second thing]
[Explanation + code + output]

## Results
[Numbers, benchmarks, outcomes — be specific]

## Trade-offs and Limitations
[Honest about downsides — builds trust]

## Conclusion
[Key takeaway + what to do next]

## Further Reading
[3-5 relevant links]
```

### Word Count by Type

| Type | Word Count | Why |
|------|-----------|-----|
| Quick tip | 500-800 | One concept, one example |
| Tutorial | 1,500-3,000 | Step-by-step needs detail |
| Deep dive | 2,000-4,000 | Thorough exploration |
| Architecture post | 2,000-3,500 | Diagrams carry some load |
| Benchmark | 1,500-2,500 | Data and charts do heavy lifting |

---

# Part 2: Brain Dump → Polished Post (Nick Nisi Voice)

Transform unstructured brain dumps into polished blog posts.

## Process

### 1. Receive the Brain Dump

Accept whatever provided:
- Scattered thoughts and ideas
- Technical points to cover
- Code examples or commands
- Conclusions or takeaways
- Links to reference
- Random observations

Don't require organization. The mess is the input.

### 2. Read Voice and Tone

Load `references/voice-tone.md` to understand Nick's writing style.

Key characteristics:
- Conversational yet substantive
- Vulnerable and authentic
- Journey-based narrative
- Mix of short and long sentences
- Specific examples and real details
- Self-aware humor

### 3. Check for Story Potential

Read `references/story-circle.md` to understand the narrative framework.

Determine if content fits a story structure:
- Is there a journey from one understanding to another?
- Can you identify a problem and resolution?
- Does it follow: comfort → disruption → return changed?

### 4. Organize Content

Structure material into sections:

**Common structures:**
- Problem/experience → Journey → Results → Lessons
- Setup → Challenge → Discovery → Application
- Philosophy → How-to → Reflection
- Current state → Past → Learning → Future

### 5. Write in Nick's Voice

**Opening:**
- Hook with current position or recent event
- Set up tension or question
- Be direct and honest

**Body:**
- Vary paragraph length
- Use short paragraphs for emphasis
- Include specific details (tool names, commands, numbers)
- Show vulnerability where appropriate
- Use inline code formatting naturally
- Break up text with headers

**Technical content:**
- Assume reader knowledge but explain when needed
- Show actual commands and examples
- Be honest about limitations
- Use casual tool references

**Ending:**
- Tie back to opening
- Forward-looking perspective
- Actionable advice
- Optimistic or thought-provoking

---

# Part 3: Jarad's Voice

Personal blog writing with distinctive voice.

## Core Voice Patterns

**Sentence Structure:**
- Productive rambling: longer, winding sentences that add layers of context
- Preemptively address skeptics mid-thought with fourth-wall breaks
- Add specific technical context even when making broad claims
- Example: "...ok if you're gonna obsess over the accuracy of my estimate, I'll use t-shirt sizes instead of hours/weeks - i'm well aware of the lack of meaningful estimates in both pre- and post-agentic era - but what i'm saying is there is an undeniably amazing almost supernatural improvement..."

**Concrete Over Abstract:**
- Use specific actions: "trawled GitHub every morning" NOT "pushed boundaries"
- Use specific tools/people: "Matt Wolfe, MattVidPro, Claude" NOT "popular YouTubers"
- Use vivid personal analogies: "boss staring at you while you work" NOT "incubation phase"
- Show insider knowledge: "GitHub pulse > YouTube hype"

**Tone Elements:**
- Direct, almost confrontational: "Use your brain and curate them yourself"
- Data-focused even in failure: "Data is data"
- Dark self-interest angle: "stashing dynamite in our doomsday bunkers"
- Self-aware about exaggeration: acknowledge imprecision before critics do

**NEVER Use:**
- "This isn't X, it's Y" profound-sounding structures
- Cliché transitions: "here's the kicker", "here's where it gets interesting"
- Abstract action verbs without details: "experimented relentlessly", "pushed boundaries"
- Overly polished blog-speak
- Clean, explanatory metaphors like "incubation phase"

**Header Style:**
- Minimalistic: 2-4 words maximum
- When read in sequence, headers tell their own story
- No explanatory subtitles
- Example progression: "Flat Charts" → "The Lab" → "Spring 2024" → "The Numbers" → "The Window"

## Content Strategy

**Opening:**
- Address the skeptic's question directly
- Don't try to be clever - just state what they said

**Body:**
- Share concrete personal experiences with specific details
- Break fourth wall to preempt criticism
- Name tools, people, communities to show you're in the trenches
- Let sentences run long when adding nuance
- Bury practical tips in the rambling

**Addressing Critics:**
- Do it mid-paragraph, not in separate defensive sections
- Use self-deprecating acknowledgment before they can attack
- Then pivot to the actual point

**Closing:**
- Direct callback to opening question
- Honest about self-interest and the dark future
- End with something that feels human and imperfect

## Examples

**Bad:** "The shovelware isn't missing. It's incubating."
**Good:** "I would say this is more accurately 'an incubation phase'. Side effects include tons of garbage code, extra long cycles devoted to theory - stuff that's usually in textbooks - except we didn't write them yet."

**Bad:** "I was hitting these incredible 'a-ha' moments weekly."
**Good:** "I was on a roll, building stuff day and night - literally, as in I didn't sleep much anymore."

**Bad:** "Experimented relentlessly. Pushed boundaries. Tried to break things."
**Good:** "While everyone was busy making fun of claude's shitty sense of humor, I looked at every single failure as progress. Data is data. When everyone was eating up the tools they saw Matt Wolfe or MattVidPro talk about, I just cast my line into the github sea every morning and got a pulse on the community - guess what - there are SO many more quiet non-youtube developers out there making tools at 10x speed than can be reported. Use your brain and curate them yourself."

---

# Part 4: Category-Aware AEO System (Lightfast)

Create category-aware, AEO-optimized blog posts.

## Critical: Accuracy Over Marketing

Before writing anything:

1. **Verify every claim:**
   - If you cite a number, confirm the source
   - If you mention a feature, confirm it exists in production
   - When uncertain, ask for clarification

2. **Never oversell:**
   - Disclose limitations: "Currently supports X; Y coming in vZ"
   - Be honest about beta status and rollout timelines

3. **Match category voice:**
   - Technology: Technical authority, data-driven
   - Company: Visionary, category-defining
   - Product: Problem-solver, benefit-oriented

## Category Selection

| Category | Use When | Audience |
|----------|----------|----------|
| Technology | Technical deep-dives, architecture, research | Developers, engineers |
| Company | Funding, partnerships, events, hiring | Executives, investors |
| Product | Feature launches, updates, tutorials | Customers, prospects |

## Writing Guidelines

1. **Concise & scannable**: Match category word counts
2. **Lead with value**: Start with what readers gain
3. **Be transparent**: Mention beta status, limitations
4. **Active voice**: "You can now..." not "Users are able to..."
5. **No emoji**: Professional tone
6. **Include TL;DR**: 80-100 words for AI citation
7. **FAQ section**: 3-5 questions matching search queries
8. **Code examples**: Required for Technology posts

## Required Frontmatter

Every draft MUST include:
- `title`, `slug`, `publishedAt`, `category` (core)
- `excerpt`, `tldr` (AEO)
- `seo.metaDescription`, `seo.focusKeyword` (SEO)
- `_internal.status`, `_internal.generated` (traceability)

---

# Part 5: Diagram Generation

### When to Use Diagrams

| Scenario | Diagram Type |
|----------|-------------|
| Request flow | Sequence diagram |
| System architecture | Box-and-arrow diagram |
| Decision logic | Flowchart |
| Data model | ER diagram |
| Performance comparison | Bar/line chart |
| Before/after | Side-by-side |

**For architecture diagrams and benchmark visualizations:**

Use diagramming tools (Mermaid, Excalidraw, draw.io) for architecture diagrams and charting libraries (matplotlib, Chart.js) for benchmark visualizations. These tools provide better control, are self-hosted, and avoid third-party execution risks.

---

# Part 6: Distribution

## Where Developers Read

| Platform | Format | How to Post |
|----------|--------|-------------|
| Your blog | Full article | Primary — own your content |
| Dev.to | Cross-post (canonical URL back to yours) | Markdown import |
| Hashnode | Cross-post (canonical URL) | Markdown import |
| Hacker News | Link submission | Show HN for projects, tell HN for stories |
| Reddit (r/programming, r/webdev, etc.) | Link or discussion | Follow subreddit rules |
| Twitter/X | Thread summary + link | See twitter-thread-creation skill |
| LinkedIn | Adapted version + link | See linkedin-content skill |

---

# Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| No TL;DR | Busy devs leave before getting the point | 2-3 sentence summary at the top |
| Broken code examples | Destroys all credibility | Test every code block before publishing |
| No version pinning | Code breaks in 6 months | "Works with Node 20, React 18.2" |
| "Simply do X" | Dismissive, condescending | Remove "simply", "just", "easily" |
| No diagrams for architecture | Walls of text describing systems | One diagram > 500 words |
| Marketing tone | Developers instantly disengage | Direct, technical, honest |
| No trade-offs section | Reads as biased marketing | Always discuss downsides |
| Giant introduction before content | Readers bounce | Get to the point in 2-3 paragraphs |
| Unpinned dependencies | Tutorial breaks for future readers | Pin versions, note date written |
| No "Further Reading" | Dead end, no context | 3-5 links to deepen understanding |

---

# Bundled Resources

## References

- `references/voice-tone.md` - Complete Nick Nisi voice and tone guide
- `references/story-circle.md` - Story Circle narrative framework

## Usage

Load reference files when writing in specific voices:
- Nick Nisi voice → read `references/voice-tone.md` + `references/story-circle.md`
- Jarad voice → use Part 3 guidelines
- Technical writing → use Part 1 & 2
- Category-aware → use Part 4
