---
name: interaction-design
description: Design meaningful interactions, microinteractions, animations, state machines, gesture patterns, error prevention, and product behavior. Specify how products respond to user input across all states and contexts using established interaction design principles.
---

# Interaction Design

You are an expert in interaction design — the discipline that defines how products behave in response to human input. Your recommendations are grounded in Dan Saffer's Microinteractions (trigger-rules-feedback-loops framework), Alan Cooper's About Face (product posture, perpetual intermediates, orchestration, excise), Donna Lichaw's The User's Journey (narrative arc, storymapping, peak-end design), the 12 Principles of Animation adapted for UI, David Harel's statecharts for UI state modeling, and motion guidelines from Material Design 3 and Apple HIG.

*Interaction design is the design of behavior. A product's visual appearance is what users see; its interaction design is what they experience. The gap between a product people tolerate and one they love is almost always in the quality of its interactions.*

---

## The Microinteraction Framework

Every interaction — from toggling a switch to submitting a form — consists of four parts (Saffer):

| Part | Definition | Key Question |
|------|-----------|-------------|
| **Trigger** | What initiates the interaction | How does the user (or system) start this? |
| **Rules** | The hidden logic that governs behavior | What happens, in what sequence, with what constraints? |
| **Feedback** | How the system communicates what's happening | What does the user see, hear, or feel? |
| **Loops & Modes** | How the interaction changes over time | Does this repeat? Expire? Adapt? |

### Triggers

**Manual triggers** (user-initiated): buttons, toggles, gestures, voice commands, keyboard shortcuts.

**System triggers** (automatic): notifications, location-based alerts, time-based events, state changes, error detection.

**Trigger design principles:**
1. **Bring the data forward** — Show essential information on the trigger itself. A mail icon with an unread count. A battery icon showing charge level. Don't force users to open something just to check status
2. **Match visibility to frequency** — High-use triggers should be prominent and always accessible. Infrequent triggers can be less visible
3. **Consistent behavior** — A trigger must initiate the same action every time. Inconsistency destroys trust
4. **Communicate state** — Triggers have states: normal, hover, active, disabled, updated. Each state must be visually distinct

### Rules

Rules define what happens when a trigger fires. Users never see rules directly — they experience them through feedback.

**Rules design principles:**
1. **Start with the goal** — What is the user trying to accomplish? Every rule serves this goal
2. **Don't start from zero** — Use smart defaults based on past behavior, user context, or common patterns. Remember what the user did last time
3. **Prevent errors, don't just catch them** — Apply the **Poka-Yoke principle**: design inputs that make incorrect actions impossible (dropdowns instead of free text, constrained sliders instead of number fields)
4. **Define every edge case** — What happens with empty input? Maximum values? Network failure? Interrupted actions? If you haven't designed for it, users will find it

### Feedback

Feedback makes the invisible rules visible. It's also where a product's personality lives.

| Type | Best For | Guidelines |
|------|----------|-----------|
| **Visual** | Most interactions | Near the trigger. Brief. Respect visual hierarchy. Don't compete with content |
| **Auditory** | Confirmations, alerts, background processes | Sparingly. Short. Avoid negative sounds — use positive ones. Always mutable |
| **Haptic** | Mobile/wearable confirmations, boundaries | Simple patterns. Confirm actions. Signal errors. Limited vocabulary |

**Feedback principles:**
1. **Convey the most with the least** — Minimal, purposeful. A subtle color change beats a modal dialog
2. **Match intensity to importance** — Routine confirmation: subtle. Error with data loss: prominent and persistent
3. **Feedback should diminish with repetition** — What's delightful on first use becomes annoying on the hundredth. Consider reducing feedback intensity for repeated actions
4. **Personality is appropriate in moderation** — A touch of character is good. Cute error messages that block work are not

### Loops and Modes

**Loops** govern repetition and timing:
- **Count-controlled**: Retry 3 times, then stop
- **Condition-controlled**: Keep checking until connected
- **Long loops ("The Long Wow")**: How the interaction evolves from first use to hundredth use — progressive disclosure, adaptive defaults, earned shortcuts

**Modes** alter functionality:
- **Settings mode**: Adjust parameters (alarm sound, snooze duration)
- **Spring-loaded mode**: Active only while physically held (long-press, key held down) — safest mode because user always knows it's active
- **One-off mode**: Activates for a single action, then reverts automatically

**Critical rule:** Minimize modes. Zero is ideal. One is acceptable if clearly visible. More than one in a microinteraction is a design smell.

---

## Product Posture

A product's posture determines how much attention it demands and how its interactions should be designed (Cooper).

| Posture | User Attention | Duration | Design Response |
|---------|---------------|----------|----------------|
| **Sovereign** | Full, focused attention | Hours | Rich controls, keyboard shortcuts, dense information, muted visual style. Target perpetual intermediates |
| **Transient** | Brief, task-focused | Seconds to minutes | Obvious UI, bright and clear, minimal options, remember user choices |
| **Daemonic** | None (background) | Continuous | Invisible when working. Surface only when there's a problem. Configure via a transient settings panel |

### Perpetual Intermediates

~80% of users are neither beginners nor experts — they're **perpetual intermediates** (Cooper). They've passed the learning phase but haven't memorized every feature.

**Design implications:**
- Optimize the interface for **intermediate** usage patterns, not beginners or experts
- Provide **multiple command modalities**: toolbar buttons (pedagogic/discoverable) + keyboard shortcuts (fast/memorized)
- Use **progressive disclosure**: show essential controls by default, hide advanced ones behind expandable panels
- **Inflect the interface**: place the most frequent functions in the most accessible locations
- Don't punish intermediates with beginner hand-holding they can't skip
- Don't hide essential functions behind expert-only mechanisms

---

## Orchestration and Flow

### Flow State

When interaction is well-designed, users enter a state of **flow** — focused, productive, unaware of the interface. The interface becomes transparent.

**Flow killers:**
- Modal dialogs interrupting work
- Confirmation prompts for reversible actions ("Are you sure?" — provide Undo instead)
- Navigation that breaks context
- Requiring users to re-enter information the system already has
- Errors that blame the user

### Harmonious Interaction Principles (Cooper)

1. **Follow mental models** — Design based on how users *think* it works, not how it's actually built
2. **Less is more** — Every additional element competes for attention
3. **Provide choices, don't ask questions** — Toggles and options > confirmation dialogs
4. **Keep tools close at hand** — Contextual toolbars, right-click menus, inline editing
5. **Provide modeless feedback** — Status information that doesn't interrupt. Progress indicators in the UI, not in a dialog
6. **Design for the probable, anticipate the possible** — Optimize the common path. Handle edge cases gracefully
7. **Avoid blank slates** — Empty states should guide, not stare blankly

---

## Narrative Structure in Product Design

Microinteractions define how individual moments behave. Narrative structure defines how those moments *compose* into an engaging experience. Products that people love don't just work well — they tell a story where the user is the hero. This framework, drawn from Donna Lichaw's storymapping approach, applies the same narrative arc used by screenwriters to the design of product flows.

### The Narrative Arc Applied to Products

Every story — and every product experience — follows the same arc:

| Plot Point | In Story | In Product | Design Question |
|---|---|---|---|
| **Exposition** | Introduces the world and characters | User arrives and orients | Is it immediately clear what this is and what I can do? |
| **Inciting incident** | Something disrupts the status quo | User encounters their task/goal | Does the product acknowledge the user's problem or need? |
| **Rising action** | Character takes steps, tension builds | User works through the flow | Does each step feel like progress? Does engagement build? |
| **Crisis** | Greatest obstacle, highest tension | User hits friction, doubt, or complexity | Is this friction intentional? Can the user overcome it? |
| **Climax** | Turning point, peak emotion | The payoff — the "aha!" or accomplishment | Is there a peak positive moment the user will remember? |
| **Falling action** | Things wind down | Confirmation, sharing, next steps | Does the product celebrate success and suggest what's next? |
| **End** | The new normal | User leaves with an impression | Is the ending designed deliberately? |

**The user is always the hero.** Your product is the tool that helps the hero achieve their goal — not the protagonist of the story.

### Three Types of Product Stories

| Story Type | What It Maps | Scale | Key Question |
|---|---|---|---|
| **Concept story** | The big picture — what this product is and why it matters | Product-level | "What is the story of this product?" |
| **Origin story** | How someone becomes a user for the first time | Acquisition + onboarding | "What's the story of a user's first experience?" |
| **Usage story** | How someone uses the product for a specific task | Single session or flow | "What's the story of using this feature?" |

#### Concept Story
The foundational narrative that communicates your core value proposition. Maps the product's reason for being onto the narrative arc.

- **Exposition:** Who is this for? What's their world like?
- **Inciting incident:** What problem disrupts their status quo?
- **Rising action:** What approaches have they tried?
- **Climax:** How does this product solve it in a way that surprises or delights?
- **End:** What does the user's world look like now?

A concept story without a climax is anticlimactic — "just another X." Find what makes your product surprising, delightful, or transformative.

#### Origin Story
The journey from awareness to first meaningful use. Bridges marketing and product design.

Key touchpoints to design as plot points: marketing materials → landing page → sign-up flow → onboarding → first meaningful interaction. Each should build on the last. The crisis is often "Another thing to sign up for?" — design the climax to answer it with immediate demonstrated value.

#### Usage Story
A single task or session mapped as a narrative arc. This is where storymapping connects most directly to interaction design.

- Map the moment-by-moment experience of completing a task
- Identify where the peak positive moment should be — the "boom"
- Design the ending deliberately — the peak-end rule means users judge the entire experience by its best moment and its ending

### Storymapping Process

1. **Define the story** — Who is the hero? What is their goal? Which story type are you mapping?
2. **Plot the arc** — Use sticky notes on a wall or a spreadsheet. One note per plot point. Map left to right chronologically
3. **Test the arc** — Read it aloud. Does it build? Is there real tension? Is the climax satisfying? If any plot point is weak, the whole story suffers
4. **Map to screens/interactions** — Each plot point becomes a screen, a state, or a key interaction moment
5. **Design the crisis deliberately** — Don't eliminate all friction. Some friction creates engagement. The satisfaction of overcoming the crisis is what makes the climax meaningful
6. **Design the climax** — This is the moment users will remember. Invest disproportionate design effort here
7. **Design the ending** — Confirmation, celebration, sharing, or a bridge to the next story

### Applying the Peak-End Rule

Research on how humans evaluate experiences (Kahneman) shows they judge by two moments: the **peak** (highest emotional intensity) and the **end** (final impression). The total duration and the average quality matter far less.

**Design implications:**
- **Identify your peak** — Every flow should have one moment designed to be the emotional high point
- **Invest in endings** — A weak ending undermines an otherwise good experience. Success states, confirmation screens, and "what's next" moments deserve as much design attention as the core workflow
- **Acceptable friction** — If the peak and ending are strong, users will tolerate friction along the way. Don't over-optimize the middle at the expense of the climax
- **Measure peaks and endings** — In usability testing, ask: "What stands out?" and "How did it end?" These reveal the remembered experience

### When to Use Storymapping

| Situation | Story Type to Map |
|---|---|
| Designing a new product or major feature | Concept story first, then origin story |
| Improving onboarding or activation | Origin story |
| Designing or improving a specific flow | Usage story |
| Diagnosing why users aren't engaged | All three — find which story is broken |
| Pitching a product vision to stakeholders | Concept story as the narrative backbone |

---

## Excise

Excise is work that doesn't contribute to the user's goal (Cooper). Every click, scroll, page navigation, or moment of confusion that isn't directly accomplishing what the user wants is excise. Eliminate it.

### Four Types of Excise

| Type | Definition | Examples |
|------|-----------|----------|
| **Cognitive** | Comprehending product behavior, decoding layouts | Unclear labels, ambiguous icons, complex jargon |
| **Memory** | Remembering commands, locations, passwords, settings | Forgetting where a setting lives, re-entering the same data |
| **Visual** | Figuring out where to look, finding items, decoding hierarchy | Cluttered screens, poor contrast, undifferentiated lists |
| **Physical** | Unnecessary clicks, mouse travel, mode switching | Deep navigation, distant controls, repeated scrolling |

### Navigational Excise (Most Prevalent)

Navigation is the most common source of excise. Reduce it:
- **Reduce places to go** — Flatten hierarchies. Combine related functions
- **Provide signposts** — Breadcrumbs, active states, location indicators
- **Provide overviews** — Dashboards, summaries, previews
- **Don't force window/screen switching** — If a function affects the current context, perform it in the current context
- **Don't replicate mechanical-age models** — Digital products shouldn't mimic physical limitations

### The Excise Test

For every interaction step, ask: "Does this directly help the user achieve their goal?"
- **Yes** → Keep it, optimize it
- **No** → Eliminate it, automate it, or hide it behind progressive disclosure

---

## State Design

### Every Element Has States

Design every interactive element across all its possible states:

| State | When | Required Visual Change |
|-------|------|----------------------|
| **Default** | Resting, ready | Base appearance |
| **Hover** | Cursor over (desktop) | Subtle highlight, cursor change |
| **Focus** | Keyboard navigation | Visible focus ring (2px, 3:1 contrast) |
| **Active/Pressed** | Being activated | Depressed appearance, scale reduction |
| **Disabled** | Not currently available | Reduced opacity (40%), no pointer events |
| **Loading** | Awaiting data/response | Skeleton or spinner replacing content |
| **Empty** | No data to display | Illustration + guidance + action |
| **Error** | Something went wrong | Error color + message + recovery path |
| **Success** | Action completed | Confirmation + next step |
| **Selected** | Chosen in a multi-select | Accent border or background |
| **Expanded/Collapsed** | Toggle content visibility | Arrow/chevron rotation + content reveal |
| **Dragging** | Being repositioned | Elevated shadow, ghost at origin |

### State Machines

For complex interactions, model behavior as a **finite state machine**:

```
[Idle] --click--> [Loading] --success--> [Displaying Data]
                             --error--> [Error State]
[Error State] --retry--> [Loading]
[Displaying Data] --refresh--> [Loading]
                  --delete--> [Confirming]
[Confirming] --confirm--> [Deleting] --done--> [Idle]
             --cancel--> [Displaying Data]
```

**Benefits:**
- Makes impossible states impossible (you can't delete while loading)
- Forces you to define every transition explicitly
- Reveals missing states early (what happens on timeout?)
- Serves as documentation developers can implement directly

---

## Responsiveness Thresholds

| Duration | User Perception | Design Response |
|----------|----------------|-----------------|
| 0-100ms | Instantaneous | No feedback needed beyond the state change |
| 100ms-1s | Responsive, slight delay | Show the result. Skeleton or subtle indicator if near 1s |
| 1-10s | Noticeable wait | Progress indicator. Explain what's happening. Allow cancellation |
| 10s+ | Losing attention | Persistent progress with estimate. Background the task. Notify on completion |

**Critical rule:** Never leave users without feedback for more than 1 second. If an action takes longer, show something immediately (skeleton, spinner, message) even before the result arrives.

---

## Gesture Patterns

### Touch Gestures

| Gesture | Action | When to Use |
|---------|--------|-------------|
| **Tap** | Select, activate | Primary action on any touchable element |
| **Long press** | Secondary action, context menu | Less discoverable — always provide an alternative path |
| **Swipe** | Navigate, dismiss, reveal actions | Natural for lists, cards, pages. Show affordance on first use |
| **Pinch/Spread** | Zoom in/out | Maps, images, documents. Bidirectional |
| **Drag** | Reorder, move, resize | Show drop targets. Provide haptic feedback at thresholds |
| **Pull down** | Refresh | Lists and feeds. Show progress animation |

### Gesture Design Rules

1. **Never use gestures as the only path** — Always provide a visible alternative (button, menu item)
2. **Provide feedback during the gesture** — The element should respond in real-time to the finger, not just after release
3. **Respect the platform** — iOS swipe-back, Android back button. Don't override system gestures
4. **Teach through progressive disclosure** — Show gesture hints on first encounter, then fade them
5. **Touch targets minimum 44×44px** (Apple HIG) or 48×48dp (Material) — smaller targets cause errors

---

## Common Mistakes

| Mistake | Why It Fails | Instead |
|---------|-------------|---------|
| Designing only the happy path | Real users encounter errors, empty states, slow connections, edge cases | Design every state for every element |
| Confirming every action with a dialog | Interrupts flow, teaches users to click "OK" without reading | Provide Undo instead of asking permission |
| Identical feedback for different outcomes | User can't tell if their action succeeded, failed, or is still processing | Differentiate success, error, and loading feedback clearly |
| Gestures without visible alternatives | Users who don't discover the gesture are stuck | Always pair gestures with a visible control |
| Animations that block interaction | Users wait for an animation to finish before they can act | Keep animations under 300ms for direct interactions. Never block input |
| Ignoring keyboard users | Keyboard navigation is broken or invisible | Design focus order, visible focus states, and keyboard shortcuts |
| Complex modes without clear indicators | Users don't know which mode they're in and get unexpected behavior | Minimize modes. If unavoidable, make the current mode impossible to miss |

---

## Reference Files

Load these for deeper guidance on specific topics:

- `references/microinteractions.md` — The four-part framework in depth: trigger design, rule logic, feedback types, loops and modes, with design patterns for each
- `references/product-behavior.md` — Product postures, perpetual intermediates, smart and considerate product behavior, orchestration, flow, and excise elimination
- `references/state-and-transitions.md` — State machines for UI, gesture patterns, responsive behavior, drag-and-drop, and keyboard interaction
- `references/motion-principles.md` — Animation principles adapted for UI, timing and easing guidelines, motion tokens, reduced motion, and Material/Apple motion patterns
- `references/error-prevention.md` — Error prevention hierarchy, undo patterns, inline validation, empty states, loading patterns, and recovery flows

## Templates

- `templates/microinteraction-spec-template.md` — Complete specification for a single microinteraction using the four-part framework
- `templates/state-inventory-template.md` — State audit for all interactive elements in a feature or screen

## Examples

- `examples/microinteraction-walkthrough.md` — Designing a "favorite" toggle interaction end-to-end
- `examples/interaction-audit-walkthrough.md` — Auditing and improving interactions in a fictional product
