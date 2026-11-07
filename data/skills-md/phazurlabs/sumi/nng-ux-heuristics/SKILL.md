---
name: nng-ux-heuristics
description: "Jakob Nielsen's 10 usability heuristics with modern interpretation, evaluation protocol, and 0-4 severity rating scale. Use when running a heuristic evaluation or usability review, rating the severity of a finding, or grounding UX feedback in established principles."
---

# NNG UX Heuristics — Modern Evaluation Framework

## Foundation

Jakob Nielsen's 10 usability heuristics remain the most validated and widely-used framework for evaluating interface quality. Originally published in 1994 and continuously refined by Nielsen Norman Group, these heuristics apply universally across platforms, devices, and interaction paradigms — from traditional GUIs to AI-native and spatial interfaces.

### The Core Philosophy (Don Norman + Jakob Nielsen)

Usability is not optional decoration — it is the fundamental determinant of whether a product succeeds. Every interface element must earn its place by serving user goals. The system exists to serve the user, never the reverse.

## The 10 Heuristics — Modern Interpretation

### H1: Visibility of System Status

The system must always keep users informed about what is going on through appropriate feedback within reasonable time.

**Modern application:**
- Show loading states with progress indicators, not spinners alone — communicate *what* is happening
- AI systems must indicate when they are processing, uncertain, or complete
- Real-time collaboration needs presence indicators and change attribution
- Background processes require persistent but non-intrusive status communication
- Skeleton screens communicate structure before content arrives

**Severity when violated:** High — users who cannot determine system state abandon tasks at 3x the normal rate.

### H2: Match Between System and Real World

The system must speak the users' language, with words, phrases, and concepts familiar to the user rather than system-oriented terms. Follow real-world conventions, making information appear in a natural and logical order.

**Modern application:**
- Use domain-specific language appropriate to the audience — medical apps use clinical terms for clinicians, plain language for patients
- AI confidence should be expressed in human-understandable terms, not raw probabilities
- Icon metaphors must evolve — the floppy disk "save" icon persists but new domains need fresh metaphors
- Voice interfaces must match conversational expectations and cultural norms
- Spatial interfaces must respect physical-world affordances (gravity, proximity, occlusion)

**Severity when violated:** Medium-High — vocabulary mismatch causes 40%+ error rates in form completion.

### H3: User Control and Freedom

Users often perform actions by mistake. The system must provide a clearly marked "emergency exit" to leave an unwanted state without going through an extended process. Support undo and redo.

**Modern application:**
- Every destructive action requires confirmation with clear consequences stated
- Multi-level undo (not just single-step) is the baseline expectation
- AI-generated content must be editable, rejectable, and regenerable
- Autosave with version history replaces manual save paradigms
- Gesture-based interfaces need clear gesture cancellation paths

**Severity when violated:** Critical — lack of undo is the #1 source of user anxiety and data loss complaints.

### H4: Consistency and Standards

Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform conventions.

**Modern application:**
- Follow platform-specific patterns: iOS Human Interface Guidelines, Material Design 3, Fluent Design
- Internal consistency across product suite matters as much as platform consistency
- Design tokens enforce consistency programmatically — do not rely on manual enforcement
- AI behavior consistency: same prompt patterns should produce predictably similar interaction styles
- Cross-device consistency: the experience must feel unified across mobile, desktop, and wearable

**Severity when violated:** Medium — inconsistency increases learning time by 25-50% and erodes trust.

### H5: Error Prevention

Even better than good error messages is a careful design which prevents a problem from occurring in the first place. Either eliminate error-prone conditions or check for them and present users with a confirmation option before they commit to the action.

**Modern application:**
- Inline validation as users type, not on submission
- Smart defaults reduce decision fatigue and error opportunity
- Constrained inputs (date pickers, dropdowns) prevent format errors
- AI should flag potential issues before users commit (smart warnings)
- Dangerous zones in interfaces should have increased friction (confirmation dialogs, delay timers)

**Severity when violated:** High — prevention is 10x cheaper than recovery.

### H6: Recognition Rather Than Recall

Minimize the user's memory load by making elements, actions, and options visible. The user should not have to remember information from one part of the interface to another. Information required to use the design should be visible or easily retrievable.

**Modern application:**
- Recent items, favorites, and contextual suggestions reduce memory burden
- Command palettes (Cmd+K pattern) combine recognition with speed
- AI-powered suggestions surface relevant actions based on context
- Breadcrumbs, progress indicators, and contextual help maintain orientation
- Auto-complete and type-ahead search leverage recognition over recall

**Severity when violated:** Medium — excessive recall demands cause 60% task abandonment in complex workflows.

### H7: Flexibility and Efficiency of Use

Accelerators — unseen by the novice user — may speed up the interaction for the expert user such that the system can cater to both inexperienced and experienced users. Allow users to tailor frequent actions.

**Modern application:**
- Keyboard shortcuts with discoverable overlay (hold modifier key to reveal)
- Customizable toolbars and workflows for power users
- Progressive disclosure: simple by default, powerful on demand
- AI adapts to user skill level over time — suggesting shortcuts to frequent users
- Batch operations and bulk editing for data-heavy workflows

**Severity when violated:** Low-Medium for basic use, High for professional/enterprise tools.

### H8: Aesthetic and Minimalist Design

Dialogues should not contain information which is irrelevant or rarely needed. Every extra unit of information in a dialogue competes with the relevant units of information and diminishes their relative visibility.

**Modern application (Dieter Rams: "Less, but better"):**
- Content-to-chrome ratio should favor content — minimize interface overhead
- Progressive disclosure over cluttered screens
- White space is a design element, not wasted space
- Information density must match user expertise — dashboards for analysts, simplified views for casual users
- AI interfaces should show results first, process second

**Severity when violated:** Medium — cluttered interfaces reduce task completion by 20% and user satisfaction by 40%.

### H9: Help Users Recognize, Diagnose, and Recover from Errors

Error messages should be expressed in plain language (no codes), precisely indicate the problem, and constructively suggest a solution.

**Modern application:**
- Error messages must state: what happened, why it happened, and exactly how to fix it
- Inline errors positioned near the source, not in distant toast notifications
- AI failures should explain limitations honestly and suggest alternatives
- Network errors should offer retry with offline capability where possible
- Form validation errors must persist until resolved and disappear immediately once fixed

**Severity when violated:** High — poor error recovery doubles support ticket volume.

### H10: Help and Documentation

Even though it is better if the system can be used without documentation, it may be necessary to provide help and documentation. Any such information should be easy to search, focused on the user's task, list concrete steps, and not be too large.

**Modern application:**
- Contextual help tooltips and inline guidance over separate documentation portals
- Onboarding flows that teach by doing, not by reading
- AI-powered help that answers natural language questions about the interface
- Empty states as teaching moments — guide first-time users to valuable actions
- Searchable, task-oriented help organized by user goals, not feature names

**Severity when violated:** Low for simple apps, High for complex professional tools.

## Heuristic Evaluation Methodology

### Preparation Phase
1. Define the scope: which flows, screens, or components to evaluate
2. Select 3-5 evaluators with diverse expertise (NNG recommends 3-5 for optimal cost-benefit)
3. Prepare user personas and key task scenarios
4. Set severity rating scale (0-4, defined below)

### Evaluation Phase
1. Each evaluator independently reviews the interface against all 10 heuristics
2. Walk through each task scenario noting violations
3. Rate each violation by severity (see scale)
4. Capture screenshots or recordings of each issue
5. Note which heuristic(s) each violation maps to

### Severity Rating Scale
- **0 — Not a usability problem:** Cosmetic only, no user impact
- **1 — Cosmetic problem:** Fix when convenient, low priority
- **2 — Minor usability problem:** Causes slight delays, fix with moderate priority
- **3 — Major usability problem:** Causes significant difficulty, fix with high priority
- **4 — Usability catastrophe:** Prevents task completion, must fix before release

### Reporting Phase
1. Consolidate findings across evaluators
2. Deduplicate and merge related issues
3. Prioritize by severity × frequency × user impact
4. Generate actionable recommendations with specific implementation guidance
5. Track remediation through design and development

## Routing

For **running an evaluation end to end** — the step-by-step protocol, how to
write a finding, the 0-4 severity scale with calibration examples, the
severity x frequency x impact prioritization matrix, reporting formats per
audience, and the common pitfalls: read `references/heuristic-evaluation-guide.md`.

For **what a heuristic means on a modern interface** — all ten reinterpreted for
today's patterns, where heuristics conflict with each other, industry-specific
applications, cultural considerations, and case studies of famous violations:
read `references/modern-heuristic-applications.md`.

## Cross-Referencing

- For visual design evaluation criteria, reference `ui-visual-design-system`
- For accessibility-specific evaluation, reference `accessibility-inclusive-design`
- For mobile-specific heuristic application, reference `mobile-ux-design`
- For AI interface evaluation, reference `ai-spatial-voice-ux`

## v3.0 Cross-References

The v3.0 upgrade introduces skills that deepen and extend heuristic evaluation into scientific foundations, structured critique, and production implementation.

### Cognitive Psychology Foundations — `cognitive-psychology-ux`

Each heuristic maps to underlying cognitive science. The `cognitive-psychology-ux` skill provides the scientific research behind why these heuristics work:

- **H6 Recognition Rather Than Recall** connects directly to the distinction between recognition memory and recall memory. The cognitive psychology skill covers working memory capacity (Miller's 7 plus/minus 2, Cowan's refined 4 plus/minus 1), encoding specificity, and context-dependent retrieval — explaining *why* recognition is cognitively cheaper than recall.
- **H8 Aesthetic and Minimalist Design** maps to cognitive load theory (Sweller). The skill details intrinsic, extraneous, and germane cognitive load, providing the scientific basis for why every extraneous element degrades performance.
- **H5 Error Prevention** relates to mental model theory (Johnson-Laird). The skill covers how users form mental models, the gulf of execution and evaluation (Norman), and how design can align system behavior with user expectations to prevent errors at the cognitive level.

### Structured Design Reviews — `design-critique-case-studies`

The `design-critique-case-studies` skill provides structured frameworks for applying heuristic evaluations in team settings — including critique session facilitation, severity calibration across evaluators, and case study examples of heuristic violations in real-world products with documented remediation outcomes.

### Production Implementation — `component-patterns-code`

The `component-patterns-code` skill contains production-ready React and SwiftUI component patterns that demonstrate heuristic compliance in code — including loading state patterns (H1), undo/redo implementations (H3), inline validation (H5), and command palette implementations (H6, H7). Use these as reference implementations when translating heuristic evaluation findings into development tickets.

## Key Sources

- Nielsen, J. (1994). "10 Usability Heuristics for User Interface Design" — updated 2024
- Norman, D. (2013). "The Design of Everyday Things" — revised edition
- NNG Group research articles and studies (2020-2025)
- Rams, D. "Ten Principles for Good Design"
