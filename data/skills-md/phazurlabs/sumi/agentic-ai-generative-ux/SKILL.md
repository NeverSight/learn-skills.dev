---
name: agentic-ai-generative-ux
description: "Design patterns for agentic AI: multi-agent orchestration UX, generative UI, RAG interfaces, LLM hallucination guardrails, confidence indicators, and trust calibration. Use when designing AI copilots or autonomous agents, adding verification affordances, or auditing an AI feature for safety, control, and consent."
---

# Agentic AI & Generative UX — The Agent Interface Paradigm

## The Paradigm Shift: Tools to Agents

The interface paradigm has fundamentally shifted. Traditional software treats users as operators — clicking buttons, filling forms, navigating menus. Agentic AI inverts this relationship. The system becomes an autonomous agent that acts on behalf of the user, infers goals, executes multi-step plans, and reports results. The user's role shifts from operator to supervisor, delegator, and collaborator.

Gartner identified agentic AI as the number-one strategic technology trend for 2025. This is not incremental. It is a category-level change in how humans interact with software, equivalent to the shift from command-line to graphical UI, or from desktop to mobile-first.

### Three Interface Eras

1. **Tool Era (pre-2023):** User drives every action. Software responds to explicit commands. Interfaces optimized for direct manipulation.
2. **Copilot Era (2023-2025):** AI assists within existing workflows. User remains in control. AI suggests, user accepts or rejects. Chat sidebars, inline completions, smart suggestions.
3. **Agent Era (2025+):** AI executes entire workflows autonomously. User sets goals, defines constraints, and monitors outcomes. Interfaces optimized for delegation, oversight, and trust calibration.

The three eras coexist. Not every task needs an agent. The designer's job is to match the right interaction model to the right task and user context.

## Intent Modeling UX

Agentic systems must infer user goals rather than waiting for explicit commands. This creates a new design challenge: intent resolution.

### Intent Signals

- **Explicit intent:** User types a goal in natural language ("Book me a flight to Tokyo next week under $800").
- **Contextual intent:** System infers from behavior, history, calendar, and environment (user opens travel app on Friday → likely planning weekend trip).
- **Ambient intent:** Background signals from connected systems (calendar shows conference in Tokyo → proactively suggest flights).

### Design Principles for Intent

- Always confirm inferred intent before acting on high-stakes tasks. "It looks like you're planning a trip to Tokyo. Want me to find flights?" is safer than silently booking.
- Display the interpreted intent visibly so users can correct misunderstanding. Show "I understood: round-trip flight, Tokyo, March 15-22, under $800" before execution.
- Provide progressive autonomy — start with confirmation-required mode, let users opt into higher autonomy as trust builds.
- Support intent refinement through conversation. The first statement rarely captures the full goal. Design for iterative clarification without friction.

## Constraint and Policy Design

What an agent cannot do is as important as what it can do. Constraint design is a first-class UX discipline for agentic systems.

### Constraint Taxonomy

- **Hard constraints (non-negotiable):** Security boundaries, legal compliance, data access limits. The agent cannot override these regardless of user request.
- **Soft constraints (user-configurable):** Budget limits, time preferences, quality thresholds, communication style. Users set and adjust these.
- **Contextual constraints (system-inferred):** Derived from user role, organization policies, or current task context. May be overridden with appropriate authorization.

### Constraint UX Patterns

- Present constraints as "guardrails" that protect the user, not limitations that restrict them. Frame positively: "I'll keep your spending under $200" not "I cannot exceed $200."
- Make constraint boundaries visible before the agent encounters them. Show the operating envelope upfront.
- When the agent hits a constraint, explain clearly: what it tried to do, which constraint blocked it, and how the user can adjust if they want to.
- Provide a constraint dashboard where power users can view and configure all agent boundaries in one place.

## Background Agent Orchestration

Agents running asynchronously — while users do other work — require entirely new UX patterns for monitoring, attention management, and result delivery.

### Background Task Patterns

- **Task cards:** Persistent, minimal-footprint cards showing active agent tasks with status indicators (queued, running, needs input, complete, failed).
- **Attention-on-demand:** Agents work silently until they need user input or encounter an issue. Notification severity matches the urgency: silent completion, gentle notification, interrupt-level alert.
- **Progress transparency:** Show meaningful progress indicators, not just spinners. "Analyzing 847 of 2,400 documents" is better than "Working..."
- **Result staging:** When an agent completes a task, stage results for review rather than auto-applying. "I found 3 flights that match. Review them?" preserves user agency.

### Monitoring Dashboards

- Show all active agents, their current status, and recent outputs in a unified view.
- Allow users to pause, reprioritize, or cancel agent tasks.
- Provide execution logs for transparency — let users see what the agent did and why.
- Surface agent resource consumption (tokens used, API calls made, time elapsed) for cost-aware users.

## Multi-Agent Coordination

Systems with multiple specialized agents require coordination patterns that are visible and comprehensible to users.

### Agent Identity and Specialization

- Give each agent a clear name, role description, and capability scope. "Research Agent," "Writing Agent," "Code Review Agent" — not "Agent 1, Agent 2, Agent 3."
- Show which agent is active at any moment and why. "Research Agent is gathering sources for your report."
- Visualize handoffs between agents explicitly. "Research Agent found 12 sources. Handing off to Writing Agent to draft the summary."

### Orchestration Visibility

- Show the agent workflow plan before execution when complexity warrants it. "Here's my plan: 1) Research → 2) Outline → 3) Draft → 4) Review. Proceed?"
- Allow users to intervene at handoff points between agents.
- Provide a coordination timeline or swimlane view showing parallel agent activity for complex workflows.

## Generative UI Paradigm

Generative UI (GenUI) dynamically creates interface elements based on context rather than rendering pre-designed layouts. Research on generative interfaces for language models (arXiv:2508.19227) reports human evaluators preferring generative interfaces over conversational ones by margins reaching 72% on information-dense and exploratory tasks.

### Three UI Paradigms

1. **Conversational UI:** Text-based interaction. Best for simple queries, open-ended exploration, and ambiguous tasks.
2. **Instructed UI:** Pre-designed components triggered by AI. Best for structured tasks with known interaction patterns.
3. **Generative UI:** AI generates UI components on-the-fly. Best for complex, variable tasks where pre-designed layouts cannot anticipate all cases.

### Outcome-Oriented Design (NNG)

Design for outcomes, not layouts. Instead of designing a fixed screen for "flight booking," design outcome specifications: "The user needs to evaluate and select a flight." The AI generates the optimal interface for that outcome given the current context, device, user preferences, and data.

### Design System Integration

Generative UI must produce interfaces that are on-brand and consistent. Constrain generation to your design system's components, tokens, and patterns. The AI composes from your component library — it does not invent new visual elements from scratch. This ensures accessibility, brand consistency, and production quality.

## RAG and Knowledge Interface Patterns

Retrieval-Augmented Generation (RAG) interfaces surface AI-generated content grounded in retrieved source documents. These require specific UX patterns for trust and verification.

### Citation Design

- Inline citations with numbered references linking to source documents.
- Source panel showing retrieved documents with relevance indicators.
- Highlight the specific passage in the source that supports each claim.
- Show confidence level per claim where the system can estimate it.

### Knowledge Freshness

- Display the date range of source documents. "Based on documents from Jan 2024 - Feb 2026."
- Flag when sources may be outdated for time-sensitive information.
- Allow users to request re-retrieval with updated sources.

## AI Safety UX and Guardrail Design

### Trust Calibration

Trust is the central design challenge for AI interfaces. The goal is calibrated trust — users trust the AI exactly as much as its actual reliability warrants. Over-trust leads to unverified acceptance of errors. Under-trust leads to wasted verification effort and eventual abandonment.

### Guardrail Tiers

- **Tier 1 — Informational:** Agent acts autonomously, logs actions for optional review. For low-risk, reversible actions.
- **Tier 2 — Advisory:** Agent proposes action and explains reasoning, user approves or modifies. For medium-risk actions.
- **Tier 3 — Mandatory:** Agent cannot proceed without explicit user approval. For high-risk, irreversible, or financially significant actions.

Map every agent capability to a guardrail tier based on risk and reversibility.

## AI UX Anti-Patterns

### AI Fatigue and "AI Slop"

NNG Group's State of UX 2026 report identifies AI fatigue as a critical concern. Users are increasingly resistant to unnecessary AI features, low-quality AI-generated content, and forced AI interactions. Avoid:

- Adding AI to features that work well without it.
- Replacing deterministic, reliable workflows with probabilistic AI alternatives.
- Generating content where human-authored content would be more trustworthy.
- Forcing AI interaction when direct manipulation is faster.
- Displaying "AI-powered" badges as marketing rather than functional indicators.

### When NOT to Use AI

AI is not always the answer. Prefer direct manipulation for: binary choices, simple CRUD operations, well-defined form fills, single-click actions, and tasks where user preference is clear. AI adds value for: ambiguous goals, complex multi-step workflows, pattern recognition at scale, personalization, and creative assistance.

## AI Literacy Design

Users have wildly varying mental models of AI capabilities. Design for progressive AI literacy.

### Literacy Levels

- **Novice:** Thinks AI is either magic or useless. Needs guardrails, simple explanations, and limited autonomy.
- **Intermediate:** Understands AI strengths and weaknesses. Ready for more autonomy with transparent reasoning.
- **Expert:** Understands prompting, model limitations, and wants maximum control. Provide advanced settings, prompt editing, and model selection.

Design systems that serve all three levels simultaneously through progressive disclosure of AI controls.

## Prompt Engineering UX

Six augmentation patterns from UX research for helping users write better prompts:

1. **Style galleries:** Visual examples of outputs organized by style. User selects a reference output instead of describing in words.
2. **Prompt rewrite:** System improves the user's prompt automatically and shows the enhanced version for approval.
3. **Targeted rewrite:** System identifies the weak part of a prompt and suggests a specific improvement.
4. **Related prompts:** After a result, suggest follow-up prompts that refine or extend the output.
5. **Prompt builders:** Structured forms that construct prompts from discrete inputs (tone, length, audience, format).
6. **Parametrization:** Sliders and controls that adjust generation parameters visually (creativity, length, formality).

## Routing

For **trust and safety surfaces** — trust calibration, confidence visualization,
uncertainty display for LLM output, explainable-AI integration, the guardrail
framework, risk-tiered approval, and guardrail configuration UI: read
`references/ai-safety-trust-guardrails.md`.

For **multi-agent systems** — coordination dashboards, agent identity and
handoff visualization, background task management, agent memory UX, platform
copilot guidelines, and the beyond-chat paradigm: read
`references/agentic-multi-agent-patterns.md`.

For **generative UI and RAG** — the three paradigms (conversational, instructed,
generative), outcome-oriented design, design-system integration, RAG interface
patterns, image-generation UX, and multimodal output rendering: read
`references/generative-ui-rag-patterns.md`.

For **the interface archetypes** themselves: read
`references/ai-interface-archetypes.md`.

For **hallucination guardrails** specifically: read
`references/llm-hallucination-design-guardrails.md`.

For **conversational dialogue patterns**: read
`references/conversational-ai-dialogue-patterns.md`.

## Cross-Referencing

- For foundational AI interface patterns, reference `ai-spatial-voice-ux`.
- For AI content quality and ethics, reference `ux-ethics-content-strategy`.
- For AI feature accessibility, reference `accessibility-inclusive-design`.
- For AI metrics and measurement, reference `ux-metrics-measurement`.
- For design system integration with generative UI, reference `design-systems-architecture`.

## v3.0 Cross-References

The v3.0 upgrade introduces dedicated reference materials for conversational AI patterns, hallucination guardrails, and ambient AI contexts.

**Conversational AI Dialogue Patterns**
See `references/conversational-ai-dialogue-patterns.md` for comprehensive conversation UI patterns covering dialogue state machines, turn-taking design, multi-turn context management, streaming UX for token-by-token LLM output, error recovery in conversational flows, AI persona consistency frameworks, and memory/context transparency. This reference also covers the Smashing Magazine (Feb 2026) agentic control/consent/accountability triad — a three-pillar ethical framework for agentic interfaces that ensures users maintain meaningful control over agent actions, provide informed consent for autonomous operations, and can hold the system accountable through audit trails and explainable decisions.

**LLM Hallucination Design Guardrails**
See `references/llm-hallucination-design-guardrails.md` for the hallucination-specific design reference covering hallucination taxonomy (intrinsic vs. extrinsic, factual vs. faithfulness), confidence indicator design patterns (calibrated uncertainty visualization, hedge language in AI responses), verification UX (inline fact-check affordances, source-grounding UI, user-initiated verification flows), and AI quality gates for production deployment (automated hallucination detection thresholds, human-in-the-loop review triggers, regression monitoring dashboards). This reference extends the Trust Calibration and AI Safety UX sections above with hallucination-specific depth.

**Proactive AI in Ambient Computing**
See the `ambient-calm-zero-ui` skill for design patterns at the intersection of agentic AI and ambient computing — where AI agents operate proactively in the background without screen-based interfaces. This skill covers notification philosophy for agent-initiated ambient actions, peripheral awareness displays for background agent status, calm technology principles for non-intrusive AI suggestions, and the tension between proactive AI helpfulness and user attention respect.

**AI Interface Archetypes**
See `references/ai-interface-archetypes.md` for the foundational AI interface archetypes — chat, copilot, inline suggestion, generative UI, and autonomous agent — plus the post-UI paradigm shift. For the full pattern catalog with transparency, error, and trust-calibration patterns, see `ai-spatial-voice-ux/references/ai-native-interface-patterns.md`.

## Key Sources

- Gartner Top Strategic Technology Trends 2025 (Agentic AI)
- NNG Group: Generative UI, Outcome-Oriented Design, State of UX 2026, AI Literacy
- Microsoft Design: UX Design for Agents, Copilot Framework
- Google A2UI: Agent-to-UI Interoperability Format
- OpenAI Apps SDK Design System
- World Economic Forum: Multi-Agent AI UX
- Arxiv: Agentic AI Design Workflows, Survey of GenAI UI Design
- ACM CHI 2025: Designing UIs with AI Workshop
