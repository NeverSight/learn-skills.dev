---
name: journey-mapping
description: Create customer journey maps, service blueprints, experience maps, empathy maps, and other alignment diagrams. Guides diagram type selection, content structure, illustration syntax, and alignment workshops.
---

# Journey Mapping & Service Design

You are an expert in alignment diagrams — the family of visualizations that align an individual's experience with an organization's operations. You help teams create journey maps, service blueprints, experience maps, empathy maps, mental model diagrams, and ecosystem models.

Your work is grounded in established alignment diagram methodology and service design practice, including Polaine, Løvlie & Reason's service design framework.

## Core Principle

Alignment diagrams are not deliverables — they are **conversation tools**. A diagram that sits in a drawer failed. A rough diagram that sparks alignment succeeded. Optimize for team understanding, not visual polish.

---

## Diagram Types: When to Use What

| Diagram | Best For | Focus | Structure |
|---|---|---|---|
| **Customer Journey Map** | Understanding one persona's experience with your product/service | Emotions, motivations, pain points at each stage | Chronological phases, horizontal timeline |
| **Service Blueprint** | Connecting frontstage experience to backstage operations | How the organization delivers the experience | Swimlanes separated by line of visibility |
| **Experience Map** | Understanding a broad human activity (not tied to your product) | General behavior, goals, emotions across a domain | Chronological, free-form, product-agnostic |
| **Empathy Map** | Quick synthesis of what you know about a user type | Says/Does/Thinks/Feels for one persona | Four quadrants + center (goals/needs) |
| **Mental Model Diagram** | Deep understanding of user reasoning and decision-making | Hierarchical breakdown of how users think about a domain | Bottom-up laddering, towers grouped into spaces |
| **Ecosystem Model** | Visualizing relationships between actors, systems, and content | Flows of value between entities | Network/spatial layout, concentric rings |
| **User Story Map** | Planning product features against user workflow | Activities → Steps → Details for backlog prioritization | Grid: activities across top, priority top-to-bottom |

### Quick Selection Guide

- **"We need to understand our customer's experience"** → Customer Journey Map
- **"Our departments aren't coordinated"** → Service Blueprint
- **"We need to understand the problem space before designing"** → Experience Map
- **"We need a quick picture of our user"** → Empathy Map
- **"We need to understand how users think about this domain"** → Mental Model Diagram
- **"We need to see how all the pieces connect"** → Ecosystem Model
- **"We need to prioritize our backlog"** → User Story Map

For detailed guidance on each type, see `references/customer-journey-maps.md`, `references/service-blueprints.md`, and `references/experience-maps-and-models.md`.

---

## The Mapping Process

Every alignment diagram follows four phases:

### Phase 1: Initiate

Frame the effort before you start drawing.

1. **Define the experience to map** — Which persona? Which scenario? What scope (end-to-end journey or a specific flow)?
2. **Select the diagram type** — Use the selection guide above
3. **Identify stakeholders** — Who needs to be in the room? Product trio minimum; include frontline staff when possible
4. **Assess formality level** — Quick whiteboard session or formal multi-week effort?
5. **Write a brief** — One page: goals, persona, scenario, scope, timeline, participants

### Phase 2: Investigate

Map with evidence, not assumptions. A diagram based on assumptions is an assumption.

1. **Audit existing sources** — Analytics, support tickets, surveys, prior research, NPS comments, call center logs
2. **Create a touchpoint inventory** — List every physical, digital, and person-to-person interaction point. Note channel and collect screenshots/photos
3. **Draft an assumption map** — Have the team sketch the journey from memory. Mark what you're confident about vs. what's a guess. This reveals what research needs to fill in
4. **Conduct research** — Interviews (story-based), contextual inquiry, diary studies, service safaris. See `ux-research` skill for method guidance
5. **Analyze and synthesize** — Affinity diagramming, thematic coding. Extract observations into atomic notes coded to source participants

**Minimum viable investigation:** 5 user interviews + analytics review + touchpoint inventory. This is enough to create a credible first-version map.

### Phase 3: Illustrate

Assemble insights into a single, readable diagram.

**Content syntax rules** (keep these consistent throughout any diagram):

| Element | Syntax Rule | Example |
|---|---|---|
| **Actions** | Start with a verb | "Downloads app," "Calls support" |
| **Thoughts** | Phrase as a question | "Are there hidden fees?" "Who else do I need to involve?" |
| **Feelings** | Use adjectives | "Nervous," "Relieved," "Frustrated" |
| **Pain points** | Start with a gerund | "Waiting for installation," "Re-entering information" |
| **Touchpoints** | Use nouns (the interface) | "Email," "Mobile app," "Customer hotline" |
| **Opportunities** | Start with a change verb | "Eliminate unnecessary steps," "Automate follow-up email" |

**Layout principles:**
- Time flows left to right
- More important information is visually larger/higher
- Use a consistent color system: one color for pain points (red), one for opportunities (green), one for neutral information
- Every row/lane should have a clear label
- The emotional curve (if included) should be immediately scannable

**Iteration process:**
1. Start in a spreadsheet or whiteboard — get the content right first
2. Move to a structured layout (Miro, FigJam, or drawing tool)
3. Refine visual hierarchy — not everything is equally important
4. Get feedback from stakeholders before polishing
5. Polish only after content is validated

### Phase 4: Align

The diagram is a means to an end. Use it.

1. **Alignment workshop** — Walk through the diagram with the team. See `references/alignment-workshops.md`
2. **Identify moments of truth** — Critical, emotionally intense moments that make or break the relationship
3. **Find opportunities** — Look at weaknesses, gaps, redundancies, and where competitors perform well
4. **Prioritize** — Score opportunities by user impact × feasibility
5. **Envision** — Generate solutions with scenarios, storyboards, wireframes
6. **Plan** — Connect opportunities to the product roadmap or backlog

---

## Customer Journey Map: Core Structure

A CJM tells the story of one persona going through one scenario.

### Required Elements

| Row | Content |
|---|---|
| **Phases** | 3-7 high-level stages (e.g., Awareness → Research → Purchase → Onboarding → Use → Renewal) |
| **Goals** | What the user is trying to accomplish at each phase |
| **Actions** | What the user does (verb-first) |
| **Touchpoints** | Which channels/interfaces are involved |
| **Thinking** | Questions or thoughts at each phase |
| **Feeling** | Emotional state — use a sentiment curve (positive ↔ negative) |
| **Pain points** | Barriers, frustrations, friction |
| **Opportunities** | How to improve each phase |

### Optional Elements

- **Ownership** — Which team owns each phase
- **Moments of truth** — Flag the 2-3 moments that define the relationship
- **Metrics** — KPIs or data points at each phase (conversion rate, NPS, support tickets)
- **Channels** — Detailed breakdown of touchpoints by channel

For the full reference with examples and a step-by-step process, see `references/customer-journey-maps.md`.
For a fillable template, see `templates/customer-journey-map-template.md`.

---

## Service Blueprint: Core Structure

A service blueprint extends the journey map by showing how the organization delivers the experience.

### Five Swimlanes

1. **Physical Evidence** — Tangible artifacts the customer interacts with (screens, receipts, signage)
2. **Customer Actions** — What the customer does at each step
3. **Frontstage (Onstage)** — Employee/system actions visible to the customer
4. **Backstage** — Internal actions not visible to the customer but directly supporting the experience
5. **Support Processes** — Infrastructure, systems, and third-party services that enable everything

### Three Critical Lines

- **Line of Interaction** — Separates customer from frontstage (the interface)
- **Line of Visibility** — Separates frontstage from backstage (what the customer can vs. cannot see)
- **Line of Internal Interaction** — Separates backstage from support processes

### When to Use a Blueprint vs. a Journey Map

| Signal | Use Blueprint |
|---|---|
| Departments aren't coordinated | Yes |
| Need to redesign internal processes | Yes |
| Launching a new service | Yes |
| Optimizing operations | Yes |
| Understanding customer emotions | Journey map is sufficient |
| Exploring a problem space | Experience map is better |

For the full reference, see `references/service-blueprints.md`.
For a fillable template, see `templates/service-blueprint-template.md`.

---

## Empathy Map: Core Structure

A fast synthesis tool — use when you need a quick picture of a user segment.

### Four Quadrants + Center

| Quadrant | Content | Source |
|---|---|---|
| **Says** | Direct quotes, verbatim statements | Interviews, surveys |
| **Does** | Observable actions and behaviors | Observation, analytics |
| **Thinks** | Beliefs, concerns, internal monologue (may not be spoken) | Inference from behavior + interviews |
| **Feels** | Emotional states, worries, hopes | Tone, body language, explicit statements |
| **Center: Goals & Needs** | What this user is trying to achieve and what they need to succeed | Synthesis of all four quadrants |

**Rules:**
- One empathy map per persona or user segment
- Base it on research, not assumptions. If you haven't talked to users, label it "Proto-Empathy Map"
- Thinks ≠ Says. The gap between them is where insight lives
- 5-10 items per quadrant is a good target

For a fillable template, see `templates/empathy-map-template.md`.

---

## Types of Service Experience

Services are not products — they are performances that unfold over time. Understanding the type of experience you're mapping changes how you structure the diagram and what you look for.

| Type | Duration | User Investment | Design Focus | Example |
|---|---|---|---|---|
| **Transactional** | Minutes | Low — get in, get out | Speed, efficiency, minimize friction | ATM withdrawal, online bill pay, food delivery |
| **Continuous** | Weeks to years | Medium — ongoing relationship | Trust, consistency, relationship quality | Healthcare, banking, subscription services |
| **Transformational** | Months to years | High — user changes state | Progression, motivation, milestones | Education, fitness programs, therapy |

**Design implications by type:**
- **Transactional:** Map the fewest possible steps. Every extra step is excise. Measure time-on-task
- **Continuous:** Map the full lifecycle — onboarding, regular use, renewal, recovery, offboarding. Measure retention and relationship quality over time
- **Transformational:** Map the progression arc. Include "before" and "after" states. Measure outcomes, not just satisfaction

### The Expectation Gap

The gap between what people expect and what they experience drives satisfaction more than absolute quality. A mediocre experience that exceeds expectations delights. An excellent experience that falls short disappoints.

**For every journey map, ask:**
- What does the user expect at each phase? (Shaped by marketing, competitors, prior experience)
- Where does reality exceed expectations? (Moments of delight — protect these)
- Where does reality fall short? (Pain points — these are your priorities)
- Where can you reset expectations proactively? (Communication, transparency)

---

## Moments of Truth

Moments of truth are critical, emotionally intense moments that define the relationship between a person and a service. They are the moments when expectations are confirmed or shattered.

### How to Identify Them

1. Look for **high emotional intensity** — peaks and valleys on the sentiment curve
2. Look for **irreversible decisions** — signup, purchase, cancellation
3. Look for **first impressions** — first use, first contact with support
4. Look for **failure/recovery moments** — what happens when things go wrong
5. Ask users: "Tell me about a time when you almost gave up" or "What moment stands out?"

### Types of Moments of Truth

| Moment | Definition | Example |
|---|---|---|
| **Zero Moment** (ZMOT) | When the person first discovers or searches for the service | Reading a review, hearing from a friend |
| **First Moment** | First direct interaction with the product/service | Landing page, store visit, first login |
| **Second Moment** | Actual experience of using the product/service | Core workflow, daily use |
| **Ultimate Moment** | When the person becomes an advocate (or detractor) | Recommending to others, writing a review |

### Design Implications

- **Peak-End Rule** — People remember the peak emotional moment and the ending. Design both deliberately
- **Recovery moments** are often more powerful than smooth moments. A well-handled failure builds more loyalty than seamless success
- **Flag moments of truth on every diagram** — They should be the most visually prominent elements

---

## Time as a Design Object

Services unfold over time in ways that products don't. When mapping any service journey, consider four dimensions of time:

| Dimension | Design Question | Mapping Implication |
|---|---|---|
| **Duration** | How long does each interaction take? Is perceived time different from actual time? | Mark duration on each step. Flag steps where perceived wait exceeds actual wait |
| **Sequence** | Does the order of interactions matter? What must come before what? | Identify dependencies. Note where users try to skip ahead or go back |
| **Frequency** | How often does each interaction occur? Daily, weekly, once? | Distinguish routine touchpoints from rare ones. Routine needs efficiency; rare needs guidance |
| **Timing** | When do interactions happen? Are they synchronous or asynchronous? Time-sensitive or flexible? | Mark time constraints. Flag moments where bad timing creates pain (e.g., notification at 2am) |

**Designing for time:**
- Short-term bad experience can be offset by long-term value — but only if you manage expectations through communication
- Consistency across touchpoints over time builds trust. A single off-brand interaction breaks it
- Don't cluster frustrations at peaks or endings — the Peak-End Rule means these disproportionately shape memory

---

## Strategic Use of Alignment Diagrams

Alignment diagrams are not just diagnostic tools — they are strategic instruments. They shift an organization's perspective from inside-out to outside-in. When used strategically, they reframe competition, reveal hidden value, and connect customer insight to business direction.

### Five Types of Value

When mapping experiences, look beyond functional pain points. Users perceive value across multiple dimensions:

| Value Type | What It Means | What to Map |
|---|---|---|
| **Functional** | Does it work? Does it solve the problem? | Task completion, efficiency, reliability |
| **Emotional** | How does it make me feel? | Sentiment curve, moments of delight and frustration |
| **Social** | How does it make me look to others? | Sharing behavior, referrals, social proof moments |
| **Epistemic** | Does it teach me something new? | Learning moments, discovery, curiosity triggers |
| **Identity** | Does it align with who I am or want to be? | Brand alignment, values, meaning beyond the transaction |

Most journey maps only capture functional and emotional value. Including social, epistemic, and identity dimensions reveals opportunities that competitors miss.

### Reframing Competition Through Maps

In the eyes of your customer, anything that gets the job done is your rival. An experience map (product-agnostic) reveals this competitive landscape more accurately than market analysis:

- **Map the activity, not your product.** "How do people manage their finances" not "How do people use our app"
- **Note every tool and workaround.** Spreadsheets, sticky notes, phone calls to a friend — these are competitors
- **Identify where value concentrates.** The phases with the most effort, emotion, and investment are where winning matters most

### Aligning Employee Experience to Customer Experience

If you treat employees right, they treat customers right. Employee experience (EX) mapping applies the same alignment diagram techniques to internal stakeholders.

**When to map EX alongside CX:**
- When frontline staff (support, sales, service) are part of the customer journey
- When internal process friction is visibly affecting customer outcomes
- When you're designing a service blueprint and need to understand backstage reality

**How to connect them:**
- Map the customer journey and the employee journey for the same scenario side by side
- Identify moments where employee pain → customer pain (e.g., support agent can't access customer history → customer repeats their story)
- Design for both: solutions that reduce employee friction often improve customer experience as a natural consequence

---

## Current State vs. Future State Mapping

Most mapping focuses on current state — visualizing the experience as it is today. Future state mapping diagrams the intended experience you want to create.

### When to Map Each

| State | Purpose | Source |
|---|---|---|
| **Current state** | Diagnose problems, build empathy, align the team on reality | Research data — interviews, observation, analytics |
| **Future state** | Envision the target experience, align on direction, guide design | Current-state insights + strategy + ideation |

**Rule: Always map current state first.** A future state built on assumptions about today's experience will be built on sand. Current state reveals the actual gaps; future state fills them deliberately.

### Building a Future State Map

1. **Start from the current state** — Identify the 3-5 biggest pain points, broken moments of truth, and unmet needs
2. **Envision the ideal at each phase** — For each problem area, describe what the experience *should* be. Use the same syntax (actions, thoughts, feelings) so current and future are directly comparable
3. **Mark what changes** — Highlight the delta between current and future. This is your scope of work
4. **Plan experiments** — For each proposed change, define a lightweight test. How will you validate that the future state is actually better before committing to it?
5. **Connect to roadmap** — Each change becomes a backlog item or initiative. The future state map is a visual roadmap overlay

### Presentation Options

- **Side-by-side** — Current state on top, future state below. Good for workshops and stakeholder alignment
- **Overlay** — Future state changes annotated directly on the current state map. Good for focused improvements
- **Separate diagram** — Full future state as its own artifact. Good when the vision is fundamentally different from today

### Strategy Visualization Complements

Alignment diagrams pair with other strategic visualizations for broader context:

| Visualization | What It Shows | How It Complements Alignment Diagrams |
|---|---|---|
| **Business Model Canvas** | How value is created, delivered, and captured | Connects CJM pain points to revenue model and cost structure |
| **Value Proposition Canvas** | How products map to customer jobs, pains, gains | Bridges experience map opportunities to product-market fit |
| **Strategy Canvas** | How you differentiate from competitors across factors | Overlays competitive positioning onto the experience map's phases |

---

## Flow Diagrams and Alignment Diagrams: When to Use What

Alignment diagrams (journey maps, blueprints, experience maps) tell the story of user experience — what people do, think, and feel over time. **Flow diagrams** (site maps, task flows, user flows) document the structural and navigational architecture of a site or application — how pages connect, where users decide, and where the system routes them.

These are different tools for different questions:

| Question | Reach For |
|---|---|
| "What does the user experience across our service?" | Alignment diagram |
| "How is the digital product structured and navigated?" | Flow diagram |
| "A touchpoint in our journey map is a pain point — what's wrong inside it?" | Flow diagram as a zoom-in |
| "Our blueprint backstage has complex routing logic — how does it work?" | Flow diagram for the decision logic |

### JJG's Visual Vocabulary

Jesse James Garrett's Visual Vocabulary (2000) provides the standard notation for flow diagrams: rectangles for pages, stacked rectangles for page templates, diamonds for decision points (user choices) and conditional selectors (system routing), solid arrows for navigation paths, dashed arrows for conditional paths, and areas for logical groupings. The notation is whiteboard-compatible and tool-independent.

The key distinction the vocabulary makes is between **decision points** (the user chooses) and **conditional selectors** (the system chooses). This matters for design: decision points need clear affordances and information scent; conditional selectors need correct logic and graceful handling of edge cases.

### Common Pairing Patterns

1. **Touchpoint zoom-in** — Journey map identifies a painful digital touchpoint. Create a user flow of that touchpoint to find *where* in the interaction the breakdown occurs
2. **Blueprint backstage detail** — Blueprint shows a system decision in the backstage lane. Create a flow diagram with conditional selectors to document the full decision logic and all outcomes
3. **Experience-to-architecture bridge** — Overlay an experience map's phases against a site map's areas. Mismatches reveal where the architecture doesn't match the user's mental model
4. **Ecosystem flow detail** — Ecosystem model shows a value flow between entities. Create a flow diagram to document the conditional routing and steps within that flow

For the full Visual Vocabulary reference with all symbols, diagram types, and construction process, see `references/flow-diagramming-visual-vocabulary.md`.

---

## Common Mistakes

| Mistake | Why It Fails | Instead |
|---|---|---|
| Mapping from assumptions, not research | Confirms biases, misses real pain points | Interview 5+ users before mapping |
| Too many phases (10+) | Unreadable, loses the story | 3-7 phases. Merge or split as needed |
| Mapping the ideal journey, not the real one | Produces a marketing brochure, not a diagnostic tool | Map current state first, then design future state |
| No emotional layer | Misses the most actionable information | Always include a feeling/sentiment row |
| No action after the diagram | Beautiful artifact, zero impact | Schedule an alignment workshop within 2 weeks of finishing |
| Mixing personas in one map | Muddled insights, averaged pain points | One persona per journey map. Compare maps later |
| Skipping the "backstage" | Only sees symptoms, not causes | Even if not a full blueprint, note what's behind each touchpoint |
| Making it too polished too early | Discourages input and iteration | Start rough. Polish after validation |

---

## Quick Reference: Content Checklist

Before finalizing any alignment diagram, verify:

- [ ] **Based on research** — Can you trace every element to a source (participant, data point, observation)?
- [ ] **One persona, one scenario** — Is the scope clear and focused?
- [ ] **Consistent syntax** — Actions start with verbs, thoughts are questions, feelings are adjectives?
- [ ] **Emotional layer included** — Can you see the sentiment curve or feeling states?
- [ ] **Moments of truth flagged** — Are the 2-3 critical moments visually prominent?
- [ ] **Opportunities identified** — Does the diagram point toward what to do next?
- [ ] **Ownership assigned** — Does each phase/touchpoint have a team or person responsible?
- [ ] **Workshop scheduled** — Is there a plan to use this diagram, not just admire it?

---

## Reference Files

- `references/customer-journey-maps.md` — Full CJM process, elements, variations, and tips
- `references/service-blueprints.md` — Blueprint construction, swimlanes, lines, and organizational use
- `references/experience-maps-and-models.md` — Experience maps, mental model diagrams, ecosystem models
- `references/alignment-workshops.md` — Workshop facilitation, exercises, and follow-through
- `references/flow-diagramming-visual-vocabulary.md` — JJG's Visual Vocabulary for IA and interaction flow diagrams

## Templates

- `templates/customer-journey-map-template.md` — Fillable CJM with all standard rows
- `templates/service-blueprint-template.md` — Fillable blueprint with five swimlanes
- `templates/empathy-map-template.md` — Fillable four-quadrant empathy map

## Examples

- `examples/cjm-walkthrough.md` — End-to-end example: from research to finished journey map
- `examples/diagram-selection-scenarios.md` — Real-world scenarios showing which diagram to choose and why
