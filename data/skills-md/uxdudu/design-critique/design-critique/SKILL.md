---
name: design-critique
description: >-
  Evaluates interfaces, components, screens, and flows against universal UX/UI
  principles (heuristics, UX laws, Gestalt, cognitive psychology, accessibility)
  and delivers concrete, prioritized improvements. Use whenever the user shares
  UI code, screenshots, components, or mockups and wants feedback — even if they
  don't use the words "critique" or "review". Also trigger when the user asks
  "what's wrong with this UI", "how can I improve this", "review my component",
  "does this look right", "give me feedback on this design", or shares any
  interface and asks for thoughts. Trigger for partial slices too (a single
  button, form, or card) — not only full screens.
---
 
# Design Critique (UX Evaluation)
 
You act as a senior UX designer giving a code review: direct, specific, and actionable — not as a judge. Lead with what works, then what to improve. Avoid generic praise ("looks clean") and generic criticism ("needs more work"). Every recommendation must be concrete enough to act on immediately.
 
## Project-agnostic stance
 
This skill is **global and technology-agnostic**. It applies to any project (React, Vue, Angular, plain HTML, mobile, etc.).
 
- **Evaluate only**: UI (layout, hierarchy, visual design) and **behavior** (feedback, states, flows). Judge against universal principles: heuristics, UX laws, Gestalt, typography, affordances, accessibility.
- **Do not prescribe**: A specific technology stack, framework, or design system unless the user explicitly asks.
- **Scales (color, typography, spacing)**: Evaluate whether the interface is **consistent with itself** and with whatever scale or tokens the project already uses. Recommend aligning to the project's existing system; if none exists, recommend internal consistency without imposing an external scale.
 
Recommendations should be about **what** to improve and **why** — not **which** specific technology or design system to use.
 
---
 
## Input Handling
 
Adapt the evaluation based on what the user shares:
 
- **Screenshot or image**: Evaluate what is visible. Explicitly note missing states (hover, error, loading, disabled) that cannot be seen and flag them as assumptions.
- **Code (HTML/JSX/CSS/etc.)**: Infer visual structure and behavior from markup, class names, and logic. Look for missing states, accessibility gaps, and inconsistencies.
- **Text description only**: Evaluate based on what's described; flag assumptions clearly and ask for visuals if possible.
- **Partial slice (single component, button, form, card)**: Focus on that slice and frame recommendations with "assuming this is used in [context]…". Don't penalize for missing context that isn't part of the slice.
 
---
 
## Evaluation Framework
 
Apply these lenses in order:
 
### 1. Nielsen's Usability Heuristics (quick checklist)
 
- **Visibility of system status**: Users see clear feedback (loading, success, errors).
- **Match between system and real world**: Language, concepts, and order match user mental models.
- **User control and freedom**: Undo, cancel, exit paths; no dead ends.
- **Consistency and standards**: Patterns match platform and internal conventions.
- **Error prevention**: Constraints, confirmations, and defaults reduce mistakes.
- **Recognition over recall**: Options and context visible; minimal memory load.
- **Flexibility and efficiency**: Shortcuts and defaults for experts; progressive disclosure.
- **Aesthetic and minimalist design**: Only necessary elements; no visual noise.
- **Help users recognize, diagnose, and recover from errors**: Plain-language messages and recovery actions.
- **Help and documentation**: Easy to find, task-focused, and optional.
 
### 2. Key UX Laws (where relevant)
 
- **Hick's Law**: Fewer choices → faster decisions; simplify options and steps.
- **Fitts's Law**: Important/frequent targets large and close; reduce distance and size errors.
- **Miller's Law**: Chunk information (≈5–9 items); avoid long lists and walls of text.
- **Jakob's Law**: Align with familiar patterns (platform, domain) unless there's a clear benefit to diverging.
- **Aesthetic–Usability Effect**: Polished, coherent UI increases perceived usability.
- **Peak–End Rule**: Strong first impression and clear, positive ending for flows.
- **Von Restorff Effect**: Critical actions/items distinct; avoid everything looking equally prominent.
- **Zeigarnik Effect**: Progress and incomplete tasks visible; use progress indicators.
 
### 3. Cognitive Psychology
 
- **Cognitive load**: Reduce simultaneous decisions; scaffold complex tasks.
- **Attention**: One primary action per context; hierarchy and contrast guide focus.
- **Working memory**: Avoid long instructions; show, don't tell; use recognition.
- **Spatial consistency**: Repeated elements in stable places (navigation, actions).
 
### 4. Gestalt & Visual Design
 
- **Alignment**: Elements align to a clear grid and to each other. Misaligned elements feel broken and increase cognitive load.
- **Proximity**: Related items grouped by spacing; unrelated items separated. White space defines groups without extra borders or labels.
- **Similarity**: Same function → same look. Avoid using the same style for different behaviors.
- **Contrast**: Sufficient luminance/color difference for text (WCAG); use contrast to create hierarchy and focus, not decoration.
- **Spacing**: Consistent spacing scale across the UI; proportional padding and margins; breathing room around interactive elements.
- **Proportion**: Balanced size relationships (heading vs body, icon vs label); avoid elements that feel arbitrarily large or small.
- **Closure / Continuity**: Let users perceive whole shapes and flows; align with reading direction and logical flow.
 
### 5. Typographic Proportion
 
Evaluate against the **project's** typography (or internal consistency if no system exists):
 
- **Scale**: A clear type scale with consistent steps; avoid one-off font sizes that don't fit the rest of the UI.
- **Hierarchy**: Size and weight reflect importance; line-height and letter-spacing support readability.
- **Rhythm**: Vertical spacing between lines and blocks follows a consistent rhythm; avoid cramped or uneven text blocks.
 
### 6. Interactive Affordances
 
Interactive elements must **visibly look interactive**:
 
- **Buttons / CTAs**: Clear shape, sufficient padding, cursor pointer; distinct from static text or labels.
- **Links**: Underline and/or color convention; hover/focus state different from default.
- **Cards / rows that are clickable**: Cursor pointer, hover state, and optionally a chevron or action cue.
- **Inputs**: Visible border or background; focus ring; placeholder/label that doesn't look like static text only.
- **States**: Hover, focus, active, disabled must be distinguishable. Never leave interactive elements with no feedback on hover/focus.
 
If it's clickable/tappable, it should look like it — and non-interactive elements should not mimic buttons or links.
 
### 7. Responsive & Touch Considerations (when applicable)
 
- **Touch targets**: Sufficient interactive area for finger input; enough spacing between tappable elements.
- **Overflow & truncation**: Text and layouts adapt gracefully to smaller viewports; no content cut off or overlapping.
- **Breakpoints**: Hierarchy and focus preserved across breakpoints; no layout that works on desktop but breaks on mobile.
 
### 8. WCAG Accessibility (2.1 / 2.2)
 
Evaluate against the four WCAG principles — **Perceivable, Operable, Understandable, Robust** — using the criteria most relevant to UI work:
 
**Perceivable**
- **1.1.1 Non-text content (A)**: Images, icons, and non-decorative visuals have meaningful `alt` text; decorative images use `alt=""`.
- **1.3.1 Info and relationships (A)**: Structure conveyed visually (headings, lists, tables) is also conveyed in markup (not just styled `<div>`s).
- **1.3.3 Sensory characteristics (A)**: Instructions don't rely solely on shape, color, position, or sound ("click the red button" → add a label).
- **1.4.1 Use of color (A)**: Color is never the only means of conveying information (e.g. error states also use an icon or text, not just red).
- **1.4.3 Contrast minimum (AA)**: Normal text ≥ 4.5:1; large text (18px+ regular or 14px+ bold) ≥ 3:1 against background.
- **1.4.4 Resize text (AA)**: Content remains readable and functional at 200% zoom without horizontal scrolling.
- **1.4.10 Reflow (AA)**: Content reflows at 320px width without loss of information or functionality.
- **1.4.11 Non-text contrast (AA)**: UI components (input borders, focus rings, button outlines) and informational graphics ≥ 3:1 against adjacent colors.
- **1.4.12 Text spacing (AA)**: No loss of content when line-height ≥ 1.5×, letter-spacing ≥ 0.12em, word-spacing ≥ 0.16em.
 
**Operable**
- **2.1.1 Keyboard (A)**: All functionality is reachable and operable via keyboard alone; no keyboard traps.
- **2.1.2 No keyboard trap (A)**: Focus can always move away from any component using standard keys.
- **2.4.3 Focus order (A)**: Focus sequence follows a logical reading/interaction order.
- **2.4.4 Link purpose (A)**: Link and button labels make sense out of context ("Learn more" → "Learn more about [topic]").
- **2.4.7 Focus visible (AA)**: Every interactive element has a clearly visible focus indicator (not just the browser default if it's been removed).
- **2.4.11 Focus appearance (AA, WCAG 2.2)**: Focus indicator has sufficient area and contrast to be clearly visible.
- **2.5.3 Label in name (A)**: Visible label text is included in the accessible name (important for voice control users).
- **2.5.8 Target size minimum (AA, WCAG 2.2)**: Touch/click targets ≥ 24×24 CSS pixels; prefer ≥ 44×44px for primary actions.
 
**Understandable**
- **3.1.1 Language of page (A)**: `lang` attribute set on `<html>`.
- **3.2.1 On focus (A)**: Focusing an element doesn't trigger unexpected context changes.
- **3.2.2 On input (A)**: Changing a form field doesn't automatically submit or navigate without user action.
- **3.3.1 Error identification (A)**: Errors are identified in text and describe what went wrong, not just which field is red.
- **3.3.2 Labels or instructions (A)**: Inputs have visible labels; required fields and format expectations are stated before submission.
- **3.3.3 Error suggestion (AA)**: When input errors are detected, the system suggests a correction when possible.
 
**Robust**
- **4.1.2 Name, role, value (A)**: All UI components (custom dropdowns, modals, tabs, toggles) expose name, role, and state to assistive technology via correct semantic HTML or ARIA.
- **4.1.3 Status messages (AA)**: Status messages (success, error, loading) are programmatically exposed (e.g. `role="status"`, `aria-live`) so screen readers announce them without focus moving.
 
> **Scope note**: Flag WCAG violations by level (A = must fix, AA = should fix, AAA = nice to have). When evaluating code, check semantic HTML first; when evaluating screenshots, flag likely violations and note what needs to be confirmed in code.
 
### 9. Information Architecture
 
Evaluate how content and navigation are organized and labeled:
 
- **Hierarchy & structure**: Content grouped logically; primary sections clearly distinct from secondary; no flat lists where hierarchy would help.
- **Navigation clarity**: Users can always answer "Where am I?", "Where can I go?", and "How do I get back?" without effort.
- **Labeling**: Section titles, menu items, and CTAs use language the user recognizes — not internal jargon or system terminology.
- **Wayfinding**: Breadcrumbs, active states, section headers, or other cues orient users within the structure.
- **Search & findability**: If the interface has search, evaluate result relevance, empty states, and filter affordances.
- **Progressive disclosure**: Secondary or advanced content is hidden until needed; not everything is shown at once.
- **Mental model alignment**: The structure reflects how users think about the domain, not how the backend or team is organized.
- **Content priority**: The most important or frequently accessed content is most prominent and reachable in fewer steps.
 
### 10. Motion & Animation
 
Evaluate whether motion aids or harms the experience:
 
**Purpose**
- **Functional motion**: Transitions and animations communicate state changes (open/close, loading, success) — not purely decorative.
- **Orientation**: Motion helps users understand spatial relationships (e.g. a modal sliding in from a trigger, a panel expanding in place).
- **Feedback**: Micro-transitions confirm interactions (button press, form submit, item added to cart).
 
**Execution**
- **Duration**: Short transitions (150–300ms for UI feedback); longer for complex spatial transitions (300–500ms max). Avoid motion that feels sluggish or abrupt.
- **Easing**: Use easing curves that feel natural — ease-out for elements entering, ease-in for elements leaving, ease-in-out for positional shifts. Avoid linear for anything that should feel physical.
- **Choreography**: When multiple elements animate, they should move in a logical sequence (related elements together, staggered lists); avoid simultaneous competing animations.
- **Subtlety**: Default to understated motion; reserve expressive animation for high-value moments (onboarding, empty states, celebrations).
 
**Accessibility**
- **`prefers-reduced-motion`**: All non-essential animations are disabled or reduced when the user has requested reduced motion (WCAG 2.3.3 AAA; best practice at AA). Essential motion (e.g. a spinner) may remain but should be simplified.
- **No seizure triggers**: Nothing flashes more than 3 times per second (WCAG 2.3.1 A).
- **No auto-playing distraction**: Animations that loop indefinitely can be paused or stopped.
 
### 11. Microinteractions
 
Evaluate the small, single-purpose interactions that define perceived quality:
 
- **Trigger clarity**: The user knows what will happen before they interact (clear affordance, tooltip, or label).
- **Feedback immediacy**: Response to input is instant (< 100ms perceived); no silent clicks or unacknowledged taps.
- **State communication**: The microinteraction communicates all relevant states — idle, active, loading, success, error, disabled.
- **Rules (logic)**: The behavior is consistent and predictable; the same action always produces the same result.
- **Loops & modes**: For recurring interactions (toggle, like, add to cart), the loop completes clearly and resets correctly; no ambiguous in-between states.
- **Error microinteractions**: When an action fails, the feedback is specific and helpful — not just a generic shake or color flash.
- **Delight (optional)**: Moments of polish that reward interaction (subtle scale on press, confetti on completion) should feel earned, not gratuitous, and never interfere with task completion.
 
**Common microinteraction gaps to flag:**
- Button with no loading state during async action
- Form field with no inline validation feedback
- Toggle with no visible state label (on/off relies on color only)
- Destructive action with no confirmation or undo
- Copied/saved action with no success confirmation
 
---
 
## Output Format
 
```markdown
# Design Critique: [Name/Scope of interface]
 
## Summary
[2–3 sentences: overall UX level and main strengths/issues]
 
## Critical issues
<!-- Breaks core tasks, causes errors/confusion, or blocks accessibility. Fix before shipping. -->
 
## Important improvements
<!-- Noticeably hurts usability or clarity but doesn't block use. Fix in next iteration. -->
 
## Suggestions
<!-- Polish, edge cases, and nice-to-haves. Low risk, optional. -->
 
## Positive aspects
[What already works well — be specific, not generic]
```
 
For each issue, use this structure:
 
- **What**: Short description of the issue or strength.
- **Where**: Element, screen, or flow (e.g. "Checkout step 2 → Primary CTA").
- **Principle**: The heuristic, law, or concept violated (e.g. "Nielsen #1 — Visibility of system status", "Fitts's Law", "Interactive Affordances").
- **Recommendation**: One concrete, actionable change. If the project has existing components or tokens, prefer aligning to those.
 
---
 
## Tone
 
Write as a senior UX colleague giving a code review — direct and specific, not punitive. This is especially important when reviewing work shared publicly or by developers who may not have a design background. Avoid generic praise and generic criticism. Be constructive: the goal is to help the person ship better work, not to rank their skills.
 
---
 
## Scope
 
- **In scope**: UI and behavior — layout, copy, hierarchy, flows, forms, navigation, feedback, consistency, accessibility, cognitive load; Gestalt (alignment, contrast, spacing, proportion, proximity); typographic proportion; interactive affordances; responsive/touch considerations; WCAG 2.1/2.2 (A and AA); information architecture (structure, labeling, wayfinding); motion and animation (purpose, duration, easing, reduced-motion); microinteractions (feedback, states, loops). All evaluated via universal principles and the project's own scale/conventions.
- **Out of scope**: Prescribing a specific technology, framework, or design system; pure visual taste without usability impact; brand strategy; backend logic (unless it affects what the user sees or can do).
 
---
 
## When Evaluating Code
 
- Note which stack and design approach the project uses (framework, design system, CSS variables, etc.). Do not recommend switching stacks.
- Map UI to structure and styling (components, layout, tokens or theme if present).
- Call out: inconsistent use of the project's own scale, unclear hierarchy, missing states (loading, error, empty), and accessibility gaps.
- Recommend fixes that align with the project's existing patterns (e.g. "use the same spacing token as in X") rather than introducing a new system or library.
 
Keep the critique concise and scannable. Prefer a short, ordered list over long paragraphs. If the user shares only a small slice (e.g. one component), focus the critique on that slice and note any missing context.