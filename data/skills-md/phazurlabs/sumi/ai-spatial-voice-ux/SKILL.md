---
name: ai-spatial-voice-ux
description: "AI-native interface patterns, conversational and voice UX, spatial computing (AR/VR/MR), and multimodal interaction. Use when designing a chatbot or assistant, a voice-first flow, headset or mixed-reality UI, or when combining speech, gaze, and gesture input."
---

# AI, Spatial & Voice UX — Next-Generation Interface Design

## AI-Native Interface Design

### The AI UX Paradigm Shift

AI interfaces fundamentally differ from traditional deterministic UIs. Traditional interfaces execute exactly what users request; AI interfaces interpret, generate, and sometimes surprise. This creates new UX challenges around trust, control, transparency, and error recovery that require fresh design patterns.

### Core AI Interface Principles

1. **Predictability in unpredictability** — AI output varies, but the interface behavior around it must be consistent
2. **Graceful degradation** — when AI fails or produces poor results, the experience must remain usable
3. **Progressive trust** — earn user trust incrementally; do not assume it
4. **Human in the loop** — always provide mechanisms for human oversight, correction, and override
5. **Transparency over magic** — explain what the AI is doing without exposing technical complexity

### AI Chat and Conversational Interface Patterns

**Message Design:**
- Differentiate human and AI messages through visual treatment (alignment, color, avatar)
- AI messages should stream/type progressively — it communicates processing and allows early reading
- Show "thinking" or "processing" indicators during AI computation
- Support rich content in AI responses: formatted text, code blocks, tables, images, interactive elements

**Input Patterns:**
- Multi-line text input with Shift+Enter for newlines, Enter to send
- Suggested prompts and conversation starters for discoverability
- File and image attachment for multimodal input
- Voice input as an alternative to typing
- Conversation history with search and reference capability

**Context and Memory:**
- Show what context the AI has access to (conversation history, documents, tools)
- Allow users to explicitly provide or revoke context
- Indicate when AI is using information from previous conversations
- Support conversation branching for exploring alternative responses

### AI Output Design

**Generated Content:**
- Always indicate AI-generated content clearly (label, subtle marker, or consistent styling)
- Provide copy, edit, regenerate, and rate actions for all generated content
- Show confidence indicators where appropriate (not raw probabilities, but contextual cues)
- Allow comparison between multiple generated options (A/B generation)

**AI Actions and Tool Use:**
- Show what actions the AI is taking in real time (searching, calculating, calling APIs)
- Require confirmation before AI executes consequential actions (sending email, modifying data)
- Provide an activity log or audit trail of AI actions
- Support undo for AI-initiated changes

**Error and Limitation Handling:**
- AI must acknowledge limitations honestly: "I don't have enough information to answer that"
- Suggest alternative approaches when the AI cannot fulfill a request
- Never fabricate information — when uncertain, communicate uncertainty
- Provide fallback to human support when AI reaches its limits

### AI-Specific UX Patterns

**Prompt Engineering UX:**
- Templates and examples that teach effective prompting through use
- Prompt history and favorites for reuse
- Structured input modes (forms, guided wizards) alongside free-text
- Context window indicators to prevent users from exceeding limits

**AI Settings and Control:**
- Tone/style preferences (formal, casual, concise, detailed)
- Output format preferences (bullet points, paragraphs, tables)
- Domain/role context setting (act as expert in X)
- Safety and content filter controls with clear explanations

## Spatial Computing UX (AR/VR/MR)

### Spatial Design Principles

1. **Respect physical space** — digital elements must coexist naturally with the physical environment
2. **Spatial hierarchy** — distance from user communicates importance (near = primary, far = peripheral)
3. **Comfort first** — never cause disorientation, nausea, or visual strain
4. **Body-aware interaction** — design for natural human posture, reach, and movement
5. **Environment-adaptive** — interfaces must respond to lighting, surfaces, and obstacles

### AR Interface Patterns

**Spatial Anchoring:**
- Anchor UI elements to real-world surfaces (tables, walls) when contextually appropriate
- Keep frequently-accessed controls anchored to the user's field of view (head-locked)
- Use world-locked placement for persistent information (room labels, equipment status)
- Ensure anchored content does not obstruct critical real-world visual information

**Visual Design for AR:**
- Use semi-transparent panels with blur backgrounds — maintain awareness of real environment
- High contrast text and icons — AR competes with unpredictable real-world lighting
- Avoid pure white backgrounds — they wash out in bright environments
- Dark UI with light text works better in varied lighting conditions
- Minimum text size: 1.5-2x standard screen sizes due to rendering at distance

**AR Interaction:**
- Gaze + pinch (Apple Vision Pro pattern) for selection
- Hand tracking for direct manipulation
- Voice commands for hands-free operations
- Spatial audio cues for off-screen elements
- Ray casting for distant object selection

### VR Interface Patterns

**Comfort and Safety:**
- Maintain stable horizon line — never tilt the world
- Provide a fixed reference frame (virtual floor, cockpit, room) to prevent motion sickness
- Field of view tunneling during movement reduces motion sickness
- Maximum movement speed should be comfortable; offer teleportation as alternative
- Rest-state UI: elements at 1-2 meter distance, slightly below eye level (ergonomic neutral)

**VR Layout:**
- Primary content: centered, 1-2m from user, slight downward angle
- Secondary panels: curved arrangement at 120-160 degree arc around user
- Avoid placing content behind the user — require explicit turning
- Maximum comfortable horizontal eye sweep: plus/minus 30 degrees from center
- Maximum comfortable vertical eye range: +20 degrees to -40 degrees from eye level

**VR Text and Readability:**
- Minimum angular text size: 1.5 degrees of visual angle (roughly 3x screen sizes)
- Use bold, high-contrast fonts — thin strokes render poorly in VR headsets
- Limit text to short labels and essential information — spatial UIs favor visual communication
- Panel curvature: match content panels to a curved surface at consistent distance

## Voice Interface Design

### Voice UX Principles

1. **Be conversational** — match natural speech patterns, not command-line syntax
2. **Keep it brief** — voice responses must be shorter than visual text equivalents
3. **Confirm ambiguity** — repeat back unclear inputs for confirmation
4. **Provide escape hatches** — "cancel", "go back", "start over" must always work
5. **Progressive disclosure via voice** — offer summaries with option to hear details

### Voice Interaction Patterns

**Invocation and Wake:**
- Clear wake word or button activation
- Visual + audio indicator that the system is listening
- Timeout with gentle prompt: "Are you still there?"

**Dialogue Design:**
- Present maximum 3 options in voice menus — more causes memory overload
- Use confirming responses: "Okay, setting a timer for 10 minutes"
- Offer correction mechanisms: "Did you mean...?"
- Support barge-in (interrupting the system while it is speaking)

**Error Recovery:**
- "I didn't catch that. Could you say it again?" (friendly, specific)
- Escalation path: after 2-3 failures, offer alternative input method or human help
- Never respond with silence — even "I'm not sure how to help with that" is better than nothing

**Multimodal Voice + Screen:**
- Voice for input, screen for output works best for complex information
- Show visual confirmation of voice commands
- Allow switching between voice and touch seamlessly
- Voice should complement touch, not replace it entirely

## Multimodal Interaction Design

### The Multimodal Stack (2025-2030)
- **Touch + Voice:** Common on phones and smart displays
- **Gaze + Hand + Voice:** Spatial computing (Vision Pro, Quest)
- **Keyboard + Mouse + AI:** Desktop productivity
- **Gesture + Voice + Touch:** Automotive and kiosk interfaces
- **Brain-Computer Interface (emerging):** Assistive tech, early consumer exploration

### Multimodal Design Rules
- Each modality should be self-sufficient for critical tasks — never require a specific modality
- Complement modalities: voice for command, visual for confirmation, haptic for feedback
- Resolve conflicts between simultaneous inputs gracefully (voice says "blue" while touching "red")
- Adapt interface emphasis based on active modality (larger touch targets when touch is primary)

## Design Patterns for Emerging Tech

### Ambient Computing
- Interfaces that appear when needed and disappear when not
- Context-aware: adapt based on time, location, activity, and user state
- Proactive suggestions without being intrusive — the design challenge of the decade
- Respect boundaries: ambient does not mean always-on surveillance

### Generative UI
- Interfaces that adapt layout and content based on AI understanding of user intent
- Dynamic form generation based on the user's specific task
- Personalized dashboards that surface relevant information automatically
- Challenge: maintain consistency and learnability while personalizing

## Routing

For **spatial, voice and multimodal depth** — Apple Vision Pro and Meta Quest
patterns, spatial layout principles, the voice interface deep dive, multimodal
interaction design, and the emerging paradigms through 2030: read
`references/spatial-voice-multimodal.md`.

For **the AI interface archetypes** shared with `agentic-ai-generative-ux`: read
`references/ai-native-interface-patterns.md`.

## Cross-Referencing

- For interaction and motion patterns, reference `interaction-motion-design`
- For accessibility in emerging platforms, reference `accessibility-inclusive-design`
- For ethical AI design, reference `ux-ethics-content-strategy`
- For design system adaptation to spatial platforms, reference `design-systems-architecture`

## v3.0 Cross-References

The v3.0 upgrade adds new skills and references that deepen and extend AI, voice, and spatial interaction coverage.

**Conversational AI Dialogue Patterns**
See `agentic-ai-generative-ux/references/conversational-ai-dialogue-patterns.md` for comprehensive conversational AI interaction design patterns including dialogue state management, streaming UX for LLM responses (token-by-token rendering, progressive disclosure of long outputs), AI persona design principles (tone calibration, personality consistency, brand voice alignment), and memory transparency patterns (showing users what context the AI retains, selective memory controls, conversation history management). This reference extends the dialogue design section above with production-level patterns specific to LLM-powered conversational interfaces.

**Ambient & Calm Computing**
See the `ambient-calm-zero-ui` skill for dedicated coverage of ambient computing, calm technology principles (Weiser & Brown), screenless interaction paradigms, and zero-UI design patterns. This skill complements the "Ambient Computing" section above with structured frameworks for proactive, non-intrusive interfaces — including notification philosophy for ambient systems, peripheral attention design, and context-aware information surfacing without screen dependency.

**Cognitive Psychology for Voice and Spatial Interfaces**
See the `cognitive-psychology-ux` skill for foundational cognitive science that directly impacts voice and spatial interface design — particularly Miller's Law constraints on voice menu options (the 3-option maximum for voice menus derives from working memory limits), attention models relevant to spatial UI placement (Treisman's feature integration theory for AR overlay design), cognitive load theory for multimodal input (split-attention effect when combining voice, gaze, and gesture), and Hick's Law implications for voice command discoverability.

## Key Sources

- Apple Vision Pro Human Interface Guidelines (2024)
- Meta Quest Design Guidelines
- Google Conversational Design Guidelines
- NNG Group AI UX research articles (2023-2025)
- Nielsen, J. "AI as UX" research series
