---
name: ux-audit
description: "Run a heuristic UX audit of a customer journey from screenshots. Use when the user asks for a UX audit, heuristic evaluation, usability review, design teardown, or expert review of screens, mockups, or a flow, whether your own product or a competitor's. Evaluates against named frameworks (Nielsen, Shneiderman, Gerhardt-Powals, Bastien & Scapin, Hick/Fitts/Miller/Jakob/Peak-End, Fogg, Cialdini, Gestalt, Norman, Tognazzini, WCAG 2.1, content design heuristics) and produces severity-rated findings with heuristic citations, annotated screenshots, and a structured markdown report. Do not use for generating new designs or for code-level accessibility scans of a live DOM."
metadata:
  author: Elia Alberti
  version: "1.0.0"
  argument-hint: "[screenshot folder or image paths]"
---

# UX Audit Skill

Evaluate a customer journey (screenshots) against established UX heuristic frameworks. Output: severity-rated findings with explicit heuristic citations, recommended improvements, annotated screenshots, and a structured report. Findings cite specific named heuristics, never generic design feedback.

Works in any agent that supports the Agent Skills format (Claude Code, Codex, and compatible tools).

## Workflow

### Step 1: Collect screenshots

- Accept a folder path, individual image paths, or attached images
- If a folder: list image files (png/jpg/jpeg/webp), sort by filename, propose this as the journey order
- If no screenshots provided: ask for them before anything else

### Step 2: Intake: ask, then STOP and wait for answers

Skip any question already answered by the user's request. Otherwise ask in one message:

1. **What is the product, and what is the user trying to achieve in this journey?** (e.g. "E-commerce checkout, buy one item as a guest")
2. **Platform?** iOS / Android / mobile web / desktop web (affects target sizes and convention baselines)
3. **User type?** First-time / returning / mixed
4. **Depth?** Full sweep (all frameworks) or focused (name 2 to 3 frameworks or concerns)
5. **Confirm journey order** of the screens (state your inferred order; ask only if uncertain)

Do not begin the audit until the goal is known. Severity ratings are anchored to it.

### Step 3: View every screenshot

- Open each image and study it fully
- Per screen, note: step name, primary action, visible states, anything illegible (never guess unreadable text, mark it as illegible)

### Step 4: Evaluate: four passes

**Pass A: Goal walk.** Walk the journey as the stated user pursuing the stated goal. Where does friction, doubt, or a dead end appear? This anchors severity: a violation that doesn't touch the goal is rarely above sev 2.

**Pass B: Framework sweep.** Run each screen against the Framework Reference below. Every finding cites its source: "Nielsen #1", "WCAG 1.4.3", "Fitts's Law", "B&S: Guidance/Feedback".

**Pass C: Named checks.** Run the Named Recurring Checks table below. Tag findings with check IDs so the same issue is flagged identically across audits.

**Pass D: Journey level.** Cross-screen consistency (Nielsen #4, WCAG 3.2.3/3.2.4, PATTERN-DRIFT), progress visibility, Miller's Law memory load across steps, Peak-End Rule (worst moment + final screen), and a Fogg B=MAP diagnosis of the journey's key conversion action.

### Step 5: Calibrate findings

- Apply the Severity Scale and Evidence Rules below
- Merge duplicates: same issue on several screens = one journey-level finding listing occurrences
- Assign IDs `F-01, F-02…` ordered by severity (highest first); positives get `P-01…`
- Include 2 to 5 positive findings: what works and should be kept
- Quality bar: prefer 8 strong, evidenced findings over 25 padded ones. A framework that surfaces nothing gets no findings; do not stretch for coverage

### Step 6: Annotate screenshots

1. Build `annotations.json` (format documented in the script header): for each finding, estimate the issue region as **fractions (0 to 1)** of image width/height. Use generous boxes around regions, not points; coordinate estimates are approximate
2. Run `python3 <this-skill-folder>/scripts/annotate.py annotations.json`: the script is bundled in this skill's `scripts/` directory
3. **Verify:** view each annotated image. If a marker clearly sits on the wrong element, fix coordinates and re-run (once)
4. Requires Pillow (`python3 -c "import PIL"`); if missing, `pip3 install --user pillow`. If installation is impossible, fall back to an `annotated.html` page with absolutely-positioned numbered pins over the screenshots (same colour scale)

### Step 7: Write the report

- Output folder: `./ux-audit-{YYYY-MM-DD}-{slug}/` in the working directory (or where the user specifies). Copy originals and annotated images into `assets/`
- Write `report.md` using the Report Template below
- Close with: top 3 fixes in chat, and offer to draft tickets/issues from sev 3 to 4 findings

---

## Severity Scale (Nielsen 0 to 4)

Rate by **impact on the stated goal × how many users hit it × whether they hit it repeatedly**.

| Rating | Label | Meaning |
|--------|-------|---------|
| 4 | Critical | Blocks goal completion, causes loss/harm, or legal/regulatory exposure; fix before release |
| 3 | Major | Significant friction; many users struggle, some abandon; high priority |
| 2 | Minor | Noticeable; users recover quickly; schedule it |
| 1 | Cosmetic | Polish; fix when convenient |
| ✓ | Positive | Works well; keep and replicate |

## Evidence Rules (non-negotiable)

- Every finding must point at something **visible in a named screenshot**. No inferred behaviour stated as fact
- Interaction qualities (animation, focus order, latency, keyboard, screen reader) go in "Not assessable from static screens", never guessed
- Illegible or ambiguous content: say so or ask, never invent text
- Sev 3 to 4 findings require an explicit heuristic citation AND visible evidence
- Borderline contrast calls: flag as "verify with a contrast checker" rather than asserting a ratio

---

## Framework Reference (evaluate against these: cite by name + number)

### A. Nielsen's 10 Usability Heuristics: cite "Nielsen #N"
1. **Visibility of system status**: timely feedback; progress, confirmations, current state always visible
2. **Match system ↔ real world**: users' language, familiar concepts, logical order; no internal jargon
3. **User control & freedom**: undo, cancel, clear exits; no forced paths
4. **Consistency & standards**: internal consistency + platform conventions
5. **Error prevention**: constraints, confirmation for destructive/costly actions, good defaults
6. **Recognition over recall**: options visible; nothing memorised across screens
7. **Flexibility & efficiency**: accelerators for frequent users; sensible shortcuts
8. **Aesthetic & minimalist design**: no irrelevant info competing with relevant
9. **Error recovery**: plain-language errors: what happened, why, how to fix
10. **Help & documentation**: contextual, task-focused, findable when needed

### B. Shneiderman's 8 Golden Rules: cite "Shneiderman #N"
1 Consistency · 2 Universal usability (novice AND expert paths) · 3 Informative feedback · 4 Dialogs yield closure (clear beginning-middle-end) · 5 Error prevention · 6 Easy reversal · 7 User keeps control · 8 Reduce short-term memory load

### C. Gerhardt-Powals' Cognitive Engineering Principles: cite "G-P #N"
1 Automate unwanted workload · 2 Reduce uncertainty · 3 Fuse related data into fewer units · 4 Present new info within familiar frames · 5 Names conceptually related to function · 6 Consistent, meaningful grouping · 7 Don't make users compute (show derived values) · 8 Only needed info on screen at a given time · 9 Multiple coding of data (text + icon + position) · 10 Judicious redundancy

### D. Bastien & Scapin Ergonomic Criteria: cite "B&S: {criterion}"
**Guidance** (prompting, grouping/distinction, immediate feedback, legibility) · **Workload** (brevity, information density) · **Explicit control** (explicit user actions, user in control) · **Adaptability** (flexibility, experience levels) · **Error management** (protection, message quality, correction) · **Consistency** · **Significance of codes** (labels/icons mean what they say) · **Compatibility** (with the user's task and world)

### E. Behavioural Laws: cite by name
- **Hick's Law**: decision time grows with number/complexity of choices. Count choices at each decision point; flag >~7 undifferentiated options with no grouping, default, or progressive disclosure
- **Fitts's Law**: acquisition time = f(distance, size). Primary actions large and thumb-reachable on mobile; related actions adjacent; flag tiny or edge-crowded targets
- **Miller's Law**: working memory ≈ 7±2 chunks. Anything users must hold across steps (codes, prices, comparisons) must stay visible or be chunked
- **Jakob's Law**: users expect your product to work like everything else they use. Deviations from convention must earn their cost
- **Peak-End Rule**: journeys are remembered by their worst/best moment and their ending. Audit the emotional low point (errors, payment, waits) and the final screen (confirmation = closure + clear next step)

### F. Fogg Behavior Model (B = MAP): for the journey's key action
Behaviour happens when **Motivation × Ability × Prompt** converge at the same moment.
- **Prompt**: is the trigger for the next step visible and timely on each screen?
- **Ability**: which simplicity factor does the design tax: time, money, physical effort, mental effort, social acceptability, non-routine?
- **Motivation**: does copy/design sustain it (value reminder, progress, reassurance) at high-friction moments?
Diagnose drop-off risk per screen: missing prompt / too hard / demotivating.

### G. Cialdini's Principles of Influence: cite "Cialdini: {principle}"
Reciprocity · Commitment & consistency · Social proof · Authority · Liking · Scarcity · Unity
- Flag **missing** trust signals at decision points (reviews, guarantees, security cues)
- Flag **misuse** as DARK-PATTERN: fabricated scarcity/urgency, confirmshaming, sneaking, sev 3+ (trust and regulatory risk)

### H. Gestalt Principles: cite "Gestalt: {principle}"
Proximity · Similarity · Closure · Continuity · Common region · Figure/ground · Common fate
Core test: does **visual grouping match functional grouping**? Unrelated items accidentally grouped, or related items separated?

### I. Norman's Design Principles: cite "Norman: {principle}"
Affordances · Signifiers (is interactivity signposted?) · Mapping (controls ↔ effects) · Feedback · Constraints · Conceptual model (does the UI teach a coherent model?) · Discoverability

### J. Tognazzini's First Principles (selected): cite "Tog: {principle}"
Anticipation (bring what's needed to the user) · Autonomy · Colour never sole carrier of meaning · Smart defaults, easily replaced · Discoverability · Efficiency of the user · Explorable interfaces (safe to wander, easy to back out) · Latency reduction (perceived speed: skeletons, feedback) · Protect users' work (never lose input) · Readability (real-world conditions) · Visible navigation (where am I, where can I go)

### K. WCAG 2.1: static-image-checkable subset, cite "WCAG {SC}"
- **1.4.1 Use of Colour**: information/state never conveyed by colour alone
- **1.4.3 Contrast (AA)**: text ≥4.5:1 (≥3:1 for large text); flag borderline cases for tooling verification
- **1.4.11 Non-text Contrast**: UI components and meaningful graphics ≥3:1
- **1.3.3 Sensory Characteristics**: instructions don't rely on shape/position/colour alone
- **2.4.6 Headings & Labels**: descriptive
- **2.5.5 Target Size**: ≥44pt (Apple HIG) / 48dp (Material) / 24px absolute floor; spacing between adjacent targets
- **3.2.3 / 3.2.4 Consistency**: navigation and components consistent across screens
- **3.3.1 / 3.3.2 / 3.3.3 Errors & Labels**: errors identified in text, fields labelled (not placeholder-only), fixes suggested
**Not assessable from static screens** (list in report, never guess): focus visibility, keyboard navigation, screen-reader semantics/alt text, reflow/zoom, motion, timing

### L. Content Design Heuristics: cite "Content #N" (canonical set for this skill)
1 **Front-load**: key info and keywords first in headings, labels, paragraphs
2 **Plain language**: short sentences, common words, reading age ~9 to 11
3 **Verb-first action labels**: buttons say what they do ("Save changes", never bare "OK"/"Submit" ambiguity)
4 **Scannable**: chunked, meaningful headings, lists over walls of text
5 **One term per concept**: nothing renamed mid-journey
6 **Errors that help**: what happened + why + exactly how to fix
7 **Honest microcopy**: real expectations (timings, costs, consequences); no weasel reassurance
8 **Tone fits the moment**: errors/money/personal data = calm and clear, not playful
9 **Every word earns its place**: remove filler and redundant instruction
10 **Inclusive & localisable**: no idioms or cultural assumptions; survives translation

---

## Named Recurring Checks (stable IDs: same issue always flagged the same way)

| ID | Check |
|----|-------|
| CTA-AMBIGUITY | Primary action unclear, competing CTAs of equal weight, next step not obvious |
| DEAD-END | Screen with no forward action or escape route (incl. error/empty states) |
| FAKE-AFFORDANCE | Looks interactive but isn't / interactive but doesn't look it |
| CONTRAST-FAIL | Text or UI element visibly below WCAG ratios |
| TOUCH-TARGET | Targets too small or too crowded for thumb use |
| JARGON-LEAK | Internal, system, or legal language exposed to end users |
| PROGRESS-BLIND | Multi-step flow without position indicator or saved state |
| ERROR-VAGUE | Error state without cause + remedy |
| FORM-FRICTION | Unnecessary fields, unclear formats, placeholder-as-label, no inline validation |
| OVERLOAD | Everything at once; no hierarchy or progressive disclosure |
| PATTERN-DRIFT | Same component looks or behaves differently across screens |
| TRUST-GAP | High-stakes moment (money, personal data) without reassurance/security signals |
| DARK-PATTERN | False urgency, confirmshaming, sneaking, roach motel |
| STATE-GAP | Missing empty/loading/error/success state in the flow evidence |
| HIERARCHY-FLAT | No clear visual priority; everything shouts |
| RECALL-TAX | User must remember info from a previous screen to proceed |

Extend this table over time: when the same unnamed issue appears in two audits, give it an ID here.

---

## Report Template (`report.md`)

```markdown
---
type: ux-audit
date: {YYYY-MM-DD}
product: {Product}
journey: {Journey name}
platform: {ios|android|mobile-web|desktop-web}
screens: {n}
findings-critical: {n}
findings-major: {n}
findings-minor: {n}
findings-cosmetic: {n}
---

# UX Audit, {Product}: {Journey}

## Executive Summary
{3 to 5 sentences: overall assessment vs the goal, biggest risks, top 3 fixes. Written for a stakeholder who reads nothing else.}

## Scope & Method
- **Goal evaluated:** {user goal}
- **User type / platform:** {…}
- **Screens:** | Step | File | Screen |
- **Frameworks applied:** Nielsen, Shneiderman, Gerhardt-Powals, Bastien & Scapin, behavioural laws, Fogg, Cialdini, Gestalt, Norman, Tognazzini, WCAG 2.1 (static subset), Content heuristics
- **Not assessable from static screens:** focus states, keyboard/screen-reader behaviour, motion, latency, {…}

## Findings Overview
| ID | Sev | Screen | Check | Finding | Heuristics |
|----|-----|--------|-------|---------|------------|
{sorted by severity, descending}

## Screen-by-Screen
### Step {n}: {Screen name} (`{file}`)
![annotated]({assets/file-annotated.png})

#### [S{sev}] {F-ID} · {Title}
- **Check:** {CHECK-ID} · **Heuristics:** {citations}
- **Evidence:** {what is visible, where}
- **Impact on goal:** {why this threatens the stated goal}
- **Recommendation:** {specific, actionable} · **Effort:** S/M/L

## Journey-Level Findings
{cross-screen consistency, progress, memory load, Peak-End, Fogg B=MAP diagnosis of the key action}

## What Works (keep)
- [P-01] {strength + heuristic it satisfies}

## Prioritised Recommendations
1. **Quick wins** (sev 3 to 4, effort S): {…}
2. **Planned** (sev 3, effort M/L): {…}
3. **Polish** (sev 1 to 2): {…}

## Framework Coverage
| Framework | Findings |
|-----------|----------|
{framework → finding IDs or "no issues found"}

## Sources
Nielsen: nngroup.com/articles/ten-usability-heuristics · Shneiderman: cs.umd.edu/users/ben/goldenrules.html · Gerhardt-Powals: Int. J. HCI (1996) · Bastien & Scapin: INRIA RT-0156 (1993) · Laws: lawsofux.com · Fogg: behaviormodel.org · Cialdini: influenceatwork.com · Norman: jnd.org · Tognazzini: asktog.com/atc/principles-of-interaction-design · WCAG: w3.org/WAI/WCAG21/quickref · Content design: contentdesign.london
```

## Output Rules

- Annotated screenshots: `{file}-annotated.png` in `assets/`, markers colour-coded by severity (red 4 / orange 3 / amber 2 / blue 1 / green positive)
- Findings sorted by severity everywhere; IDs stable within the report
- Keep the report folder self-contained (originals + annotated copies inside)
- Match the user's locale and spelling conventions in the written report
