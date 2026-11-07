---
name: cognitive-psychology-ux
description: "Laws of UX (Fitts, Hick, Miller, Jakob, Peak-End, Doherty), Gestalt principles, cognitive biases, mental models, attention, and memory constraints. Use when auditing cognitive load, sizing tap targets, reducing choice overload, fixing decision fatigue, or grounding a design decision in research."
---

# Cognitive Psychology for UX Design

## Why Cognitive Psychology Is the Foundation of Great UX

Every pixel on a screen is ultimately processed by a human brain. The visual cortex parses layout. Working memory juggles options. The prefrontal cortex weighs decisions. The amygdala registers frustration or delight. No amount of visual polish can rescue an interface that violates how human cognition actually works.

Cognitive psychology is not a nice-to-have theoretical overlay on design practice. It is the bedrock discipline that explains why some interfaces feel effortless while others — despite beautiful aesthetics — leave users confused, exhausted, or angry. When a checkout flow loses 68% of users at the payment step, the answer is almost never "the button color was wrong." The answer is cognitive: too many form fields overloaded working memory, unclear labels forced recall instead of recognition, or choice paralysis froze decision-making entirely.

Designers who internalize cognitive principles stop guessing and start predicting. They can look at a wireframe and identify the exact moment where cognitive load will spike, where attention will drift, where a bias will nudge behavior in an unintended direction. This skill transforms design from an opinion-driven craft into an evidence-based discipline.

This module provides the scientific foundations — the laws, biases, and mental mechanisms — that underpin every other skill in this plugin. Whether you are evaluating heuristics, building design systems, crafting motion, or auditing accessibility, cognitive psychology is the common language that connects them all.

## Core Laws of UX: A Working Overview

The following laws represent decades of experimental psychology distilled into principles directly applicable to interface design. Each law is covered in depth in the **Laws of UX Encyclopedia** reference file; what follows here is a working summary designed for rapid application.

**Hick's Law** states that the time to make a decision increases logarithmically with the number of choices. In practical terms: every option you add to a menu, every extra button on a toolbar, every additional plan on a pricing page increases decision time and the probability of abandonment. The design response is progressive disclosure — reveal complexity only when the user needs it.

**Fitts's Law** quantifies the time required to move to a target as a function of the target's distance and size. Larger, closer targets are faster to acquire. This is why primary actions should be large and positioned near the user's current focus, and why mobile tap targets must be at least 44x44 points.

**Miller's Law** establishes that working memory can hold roughly 7 plus or minus 2 chunks of information. This is not a design rule to "always group things in sevens" — it is a warning that interfaces presenting more than a handful of ungrouped items will overwhelm short-term retention. The design response is chunking: group related items visually and semantically.

**Jakob's Law** observes that users spend most of their time on other sites and apps. They arrive at your product with expectations formed elsewhere. Deviating from established conventions imposes a learning cost. Innovation should be reserved for your core value proposition, not for reinventing the hamburger menu.

**Gestalt Principles** — proximity, similarity, closure, continuity, common region, figure-ground, uniform connectedness, and Pragnanz (simplicity) — describe how the visual system automatically organizes elements into coherent groups. These principles are the grammar of visual layout. They determine what users perceive as related, separated, primary, or secondary without reading a single word.

**The Peak-End Rule** (Kahneman) demonstrates that people judge an experience not by its average quality but by its most intense moment (the peak) and its final moment (the end). A painful 20-minute process with a satisfying confirmation screen will be remembered more fondly than a smooth 5-minute process with an abrupt ending. Design your peaks and endings deliberately.

**The Doherty Threshold** establishes that system response times under 400 milliseconds keep users in a productive flow state. Above that threshold, attention fragments and task-switching begins. This is the quantitative argument for performance optimization as a UX concern, not merely an engineering concern.

For the complete treatment of 25+ laws with formulas, code examples, and anti-patterns, see `references/laws-of-ux-encyclopedia.md`.

## Mental Models: The User-System Gap

A mental model is a user's internal representation of how a system works. Users do not read documentation or inspect source code; they build a mental model from the interface's affordances, labels, feedback, and their prior experience with similar systems.

The **system model** is how the system actually works — its data structures, state machines, and business logic. The **user model** is what the user believes is happening. The **design model** (or represented model) is what the interface communicates.

Great design minimizes the gap between the user model and the system model by making the design model transparent and intuitive. When a user drags a file to the trash, the mental model is "I am throwing this away." If the system actually moves the file to a hidden `.Trash` directory and only deletes it on empty, the design model must communicate this (through the "Empty Trash" action and the recoverable state) or users will be confused when "deleted" files reappear.

**Practical techniques for aligning mental models:**
- Use familiar metaphors grounded in real-world experience (folders, shopping carts, bookmarks)
- Provide immediate, visible feedback that confirms the user's expectation of what just happened
- Use progressive disclosure to match the user's evolving understanding — do not front-load the full system model
- Run first-click tests and think-aloud protocols to surface model mismatches early
- Design error messages that correct the mental model, not just describe the system state

See `nng-ux-heuristics` (Heuristic 2: Match Between System and the Real World) for the heuristic framework that operationalizes mental model alignment.

## Cognitive Load Theory Applied to UI Design

John Sweller's Cognitive Load Theory identifies three types of cognitive load, each with distinct design implications:

**Intrinsic load** is the inherent difficulty of the task itself. Filing a tax return is intrinsically complex; toggling a light switch is intrinsically simple. Designers cannot eliminate intrinsic load, but they can manage it through task decomposition — breaking a complex task into a sequence of simpler steps (wizard patterns, progressive forms).

**Extraneous load** is unnecessary load imposed by poor design. Confusing navigation, inconsistent terminology, hidden controls, gratuitous animation, and unclear hierarchy all add extraneous load. This is the load designers should ruthlessly eliminate. Every unit of extraneous load steals cognitive capacity from the actual task.

**Germane load** is the productive load involved in learning and schema formation. Well-designed onboarding, meaningful patterns, and consistent conventions help users build reusable mental schemas. Germane load is desirable — it represents the user's investment in becoming proficient.

**The design equation:** Minimize extraneous load. Manage intrinsic load through decomposition. Maximize germane load through consistency and meaningful patterns. The total cognitive load at any moment must stay within working memory capacity, or the user will experience confusion, errors, and frustration.

**Measurable indicators of cognitive overload:**
- Task abandonment at specific steps (analytics)
- Increased time-on-task without increased accuracy (usability testing)
- User verbalization of confusion in think-aloud protocols
- Pupil dilation and galvanic skin response (neuroUX research labs)
- Increased error rates at points of high visual density

See `references/neurodesign-engagement-science.md` for Sweller's specific effects (split-attention, redundancy, modality) and measurement techniques.

## Attention: Selective, Divided, and Sustained

Attention is a finite cognitive resource, not an infinite channel. Three modes of attention are directly relevant to interface design:

**Selective attention** is the ability to focus on one stimulus while filtering out others. Users engaged in a task will literally not see elements outside their focus area — a phenomenon called inattentional blindness (Simons & Chabris, 1999). This is why banner blindness exists: users learn to selectively ignore regions associated with advertising. Design implication: critical information must be placed within the user's task-focused visual flow, not relegated to "announcement" areas the brain has learned to filter.

**Divided attention** is the attempt to process multiple information streams simultaneously. Humans are poor at this. Every additional demand — a notification badge, a chatbot popup, an autoplaying video — steals capacity from the primary task. Gloria Mark's research at UC Irvine demonstrates that a single interruption costs an average of 23 minutes and 15 seconds to fully recover from. Design implication: protect the user's primary task flow. Defer non-critical notifications. Never autoplay competing content during task execution.

**Sustained attention** is the ability to maintain focus over extended periods. It degrades predictably: after 10-15 minutes, vigilance drops measurably (the vigilance decrement). Long forms, lengthy onboarding sequences, and extended reading without visual breaks all suffer from this. Design implication: chunk long tasks with progress indicators, celebrate micro-completions, and vary visual rhythm to counteract the decrement.

See `interaction-motion-design` for techniques that direct attention through motion, and `accessibility-inclusive-design` for cognitive accessibility considerations related to attention disorders.

## Memory: Working Memory, Recognition, and Chunking

**Working memory** is the mental workspace where active processing occurs. Cowan's revised estimate places its capacity at roughly 4 chunks (plus or minus 1) for novel information — lower than Miller's original 7 plus or minus 2, which applied to well-practiced domains. This is the fundamental constraint behind every "keep it simple" design recommendation.

**Recognition versus recall** is one of the most actionable distinctions in cognitive psychology. Recognition (identifying something from visible options) is dramatically easier than recall (retrieving something from memory with no cues). Dropdown menus leverage recognition. Blank text fields demand recall. Autocomplete transforms a recall task into a recognition task — this is why it is one of the highest-impact UI patterns ever developed.

This distinction is so important that Nielsen and Norman formalized it as Heuristic 6: Recognition Rather Than Recall. See `nng-ux-heuristics` for the full treatment.

**Chunking** is the strategy of grouping individual items into meaningful clusters to fit within working memory limits. Phone numbers are chunked as 3-3-4 (in the US). Credit card numbers are chunked as 4-4-4-4. A well-designed dashboard chunks metrics into labeled groups (Revenue, Users, Performance) rather than presenting 20 ungrouped numbers.

**Serial position effects** shape what users remember from lists and sequences. The primacy effect (better recall of first items) and recency effect (better recall of last items) mean that the most important navigation items should be placed first and last. Items in the middle of a long list receive the least attention and worst recall. See `references/cognitive-biases-design-patterns.md` for the full treatment.

## Decision-Making: Satisficing, Maximizing, and Choice Architecture

Herbert Simon's concept of **satisficing** describes how humans actually make decisions: not by evaluating every possible option to find the optimal one (maximizing), but by scanning options until they find one that is "good enough." Users do not read every menu item; they click the first one that seems plausible. They do not compare all 15 pricing plans; they look for the one labeled "Most Popular."

**Choice overload** (Iyengar & Lepper, 2000) demonstrates that increasing options can decrease satisfaction and increase decision paralysis. The famous jam study showed that 24 varieties led to 3% purchase rate while 6 varieties led to 30%. In UX terms: fewer, well-curated options outperform exhaustive catalogs unless the user has explicitly entered an exploration mode.

**Choice architecture** (Thaler & Sunstein) is the deliberate structuring of how choices are presented. Smart defaults, recommended options, progressive filtering, and comparison tools are all choice architecture techniques. The ethical imperative is that choice architecture should serve the user's interests, not exploit their biases. A pre-checked "subscribe to marketing emails" checkbox exploits default bias. A pre-selected "standard shipping" option genuinely serves the most common user need.

**Decision fatigue** is the empirically demonstrated degradation of decision quality after extended sequences of choices. Judges grant parole at higher rates after meals. Users accept worse defaults later in a long configuration flow. Design implication: place the most consequential decisions early in a flow, and reduce trivial decisions through intelligent defaults.

See `ux-ethics-content-strategy` for the ethical framework around choice architecture and `references/cognitive-biases-design-patterns.md` for the complete catalog of decision biases.

## Cross-References to Other Skills

Cognitive psychology is the connective tissue of this plugin. Every other skill draws from or applies these foundations:

- **nng-ux-heuristics**: Nielsen's 10 heuristics are applied cognitive psychology. H6 (Recognition over Recall), H8 (Aesthetic and Minimalist Design reducing extraneous load), and H5 (Error Prevention through mental model alignment) all map directly to concepts in this module.
- **accessibility-inclusive-design**: Cognitive accessibility — designing for ADHD, dyslexia, autism spectrum, and age-related cognitive decline — requires deep understanding of attention, memory, and processing speed variability.
- **interaction-motion-design**: Motion is an attention-direction tool. Easing curves map to expectation (mental models of physics). Animation duration thresholds relate to the Doherty Threshold and perceptual timing.
- **design-systems-architecture**: Consistent design tokens and component APIs create the predictability that supports schema formation (germane load) and reduces learning cost (Jakob's Law).
- **ux-ethics-content-strategy**: Dark patterns are cognitive bias exploits. Understanding the bias is the prerequisite for recognizing and refusing to implement its exploitation.
- **ai-spatial-voice-ux**: Conversational and spatial interfaces introduce novel cognitive challenges — working memory demands of voice, spatial navigation mental models, and attention management in 3D environments.

## How to Use This Skill

When Claude Code activates this skill in response to a cognitive psychology trigger, it will draw from:

1. **This overview** for conceptual framing and cross-skill connections
2. **laws-of-ux-encyclopedia.md** for specific law definitions, formulas, code examples, and anti-patterns
3. **cognitive-biases-design-patterns.md** for the complete bias catalog with ethical and dark pattern annotations
4. **neurodesign-engagement-science.md** for visual scanning, attention economics, flow state design, and neuroscience-backed engagement techniques

Use these resources to audit existing designs, generate evidence-based recommendations, write design rationale documentation, and build interfaces that work with human cognition rather than against it.
