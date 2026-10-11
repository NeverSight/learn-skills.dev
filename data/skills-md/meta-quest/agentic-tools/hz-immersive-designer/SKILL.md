---
name: hz-immersive-designer
license: Apache-2.0
description: "Guides design of comfortable, intuitive VR/MR experiences for Meta VR and Horizon OS — comfort guidelines, interaction patterns, spatial layout, accessibility. Use during UX design review or when evaluating comfort and accessibility. Build paths: Meta Spatial SDK, Unity, Unreal, native OpenXR, and WebXR; for 2D panel apps use hz-panel-designer if available. Use hz-quest-verify-first if the build path is unclear."
---

# Immersive Designer

A knowledge skill for designing comfortable, intuitive, and accessible VR and MR experiences on Meta VR. This skill provides design principles, best practices, and review checklists for spatial computing UX.

## When to Use

- Designing new VR or MR experiences for Meta VR
- Reviewing UX decisions in existing Meta VR applications
- Evaluating comfort and usability of spatial interfaces
- Planning interaction models for immersive content
- Ensuring accessibility compliance in XR applications
- Advising on spatial layout, depth placement, and UI positioning
- Troubleshooting user comfort complaints such as motion sickness or eye strain

## Core Design Principles

1. **Comfort First** — User comfort is non-negotiable. Motion sickness, eye strain, and fatigue will cause users to abandon an app regardless of content quality. When in doubt, choose the more conservative option.

2. **Presence** — Maintain the feeling of "being there" through consistent spatial cues, coherent lighting, plausible physics, and stable world anchoring. In MR, blend virtual content seamlessly with physical surroundings.

3. **Intuitive Interaction** — Leverage gestures and spatial relationships that map to real-world expectations. Introduce novel patterns gradually with clear affordances. Never assume prior VR experience.

4. **Accessibility** — Design for the widest range of abilities from the start. Every core function should have alternative interaction paths, and comfort options should be adjustable.

## Key Design Areas

### Comfort

Managing user comfort across all aspects of the experience. This encompasses motion sickness prevention, field of view management, locomotion design, refresh rate considerations, session length awareness, and vestibular mismatch avoidance.

See [Comfort Guidelines](references/comfort-guidelines.md) for detailed guidance.

### Interaction

Designing how users engage with the virtual world and its elements. This covers direct manipulation, ray casting, gaze-based interaction, voice input, gesture recognition, controller mapping, haptic feedback, and multi-modal input support.

See [Interaction Patterns](references/interaction-patterns.md) for detailed guidance.

### Spatial Layout

Structuring the three-dimensional space for optimal usability and visual comfort. This includes depth zone management, UI placement and readability, scale and proportion, spatial audio positioning, and environmental design fundamentals.

See [Spatial Layout](references/spatial-layout.md) for detailed guidance.

### Accessibility

Ensuring the experience is usable by people with diverse abilities. This spans physical accessibility (one-handed use, seated play), visual accessibility (contrast, colorblind support), audio accessibility (captions, visual indicators), cognitive accessibility (clear instructions, adjustable pacing), and motion sensitivity accommodations.

See [Accessibility](references/accessibility.md) for detailed guidance.

## Quick Design Review Checklist

Use this checklist when reviewing any VR or MR experience design. Each item includes specific pass/fail measurements where applicable. Guidelines evolve — when an item feels stale, confirm it against current docs with `metavr docs search "<topic>"` before citing it.

### Comfort

- Does the locomotion system follow comfort guidelines (snap turning default, teleportation option, vignette during movement)?
- Is the camera ever moved without direct user input? Any camera movement not initiated by the user's physical head motion is a comfort violation.
- Is the horizon line stable during all interactions?
- Does the application target at least 72 Hz refresh rate? 90 Hz is recommended for Quest 3, and 120 Hz for fast-paced content.
- Are there session length reminders or natural break points every 20-30 minutes?
- Is there a risk of vestibular mismatch in any scenario?
- **Locomotion speed**: Smooth locomotion speed should not exceed 1.4 m/s (walking pace) without vignette. Speeds above 3 m/s require aggressive FOV restriction.
- **Rotation**: Snap turn increments should be 30-45 degrees. Smooth turn speed should default to 60-90 degrees/second with user-adjustable range.

### Viewing and Readability

- Are primary UI elements placed between **1.0 m and 2.0 m** from the user? This is the comfort zone where accommodation-vergence conflict is minimal.
- **Minimum text size**: Text must subtend at least **1.0 degree of visual arc** at its intended viewing distance. At 1.0 m, this is approximately **17.5 mm** (roughly 50px at Quest 3 resolution). At 2.0 m, double the physical size.
- Is critical content placed within **30 degrees** of center gaze? Content beyond 30 degrees requires head movement. Content beyond 55 degrees is outside comfortable neck rotation.
- Are there any content elements closer than **0.5 m** to the user? Objects closer than 0.5 m cause vergence-accommodation conflict and eye strain. Never place interactive content closer than 0.5 m.
- Do wide UI surfaces (wider than **0.6 m** at their viewing distance) use curved panels to maintain consistent focal distance across the panel?
- **Maximum panel width**: Individual panels should not exceed **50 degrees** of visual arc. For a panel at 1.5 m, this is approximately **1.4 m** wide.

### Interaction Quality

- Are interaction targets at least **48 mm x 48 mm** (approximately 2.8 degrees at 1.0 m) for controller ray interaction and at least **64 mm x 64 mm** for hand tracking poke/pinch?
- Is there clear visual distinction between interactive and non-interactive elements (depth offset, highlight, or material change)?
- Do all interactive elements provide hover, press, and release feedback states?
- Is haptic feedback used to confirm interactions? Recommended pulse: 0.1-0.3 seconds, medium intensity.
- Can destructive actions be undone or cancelled?
- **Grab interaction range**: Objects should be grabbable within **0.3-0.8 m** arm's reach for direct grab. Beyond 0.8 m, use ray-based grab or distance grab.

### Feedback

- Is there adequate visual feedback for every user action?
- Is there adequate audio feedback for important interactions?
- Do spatial audio sources match their visual positions within **15 degrees** of angular accuracy?
- Are loading states and progress clearly communicated?

### Accessibility and Flexibility

- Can the experience be used while seated? Seated-mode users have a reachable volume of approximately **0.6 m** radius from their torso.
- Can all core functions be performed with one hand?
- Are there alternatives for interactions that rely solely on color? Use shape, pattern, or label in addition to color. Minimum contrast ratio for text: **4.5:1** (WCAG AA).
- Are captions or subtitles available for speech and important audio?
- Are there comfort mode options for motion-sensitive users?
- Can text size and contrast be adjusted?

### Mixed Reality Considerations

- Does virtual content blend plausibly with the physical environment?
- Are passthrough and virtual element boundaries clearly defined?
- Does the experience respect the user's physical space boundaries (Guardian/boundary system)?
- Are virtual objects anchored stably to real-world positions? Anchored objects should not drift more than **1-2 cm** during a session.

## Gotchas

These are common design mistakes that cause comfort issues or poor reviews.

- **Text is too small** -- This is the single most common design failure in VR apps. Developers test on desktop monitors where everything is readable, then deploy to a Meta VR headset where the effective resolution per degree is much lower. Always validate text readability on device, not in editor.
- **UI placed at arm's length (0.3-0.5 m)** -- New VR developers instinctively place UI panels within arm's reach, like a tablet. This causes severe eye strain because it falls in the vergence-accommodation conflict zone. Push primary UI panels to 1.0-1.5 m distance.
- **Smooth locomotion with no comfort options** -- Shipping smooth locomotion without a teleportation fallback or vignette will cause motion sickness for 30-40% of users. Always provide snap turn and teleportation as alternatives and make them the default.
- **Ignoring seated users** -- If all interactive elements require standing and reaching above head height, seated users (including wheelchair users) cannot use the app. Design all core interactions within a 0.6 m radius at chest-to-head height.
- **Color-only feedback** -- Approximately 8% of males have some form of color vision deficiency. If interactive elements are distinguished only by color (red = error, green = success), add shape or icon indicators as well.
- **Anchoring UI to the head (head-locked HUD)** -- Head-locked UI panels cause nausea and obscure the 3D scene. Use world-locked or body-locked UI that follows the user with lag and stays at a comfortable distance.
- **Spatial audio with no fallback** -- Some users are deaf or hard of hearing. Every spatial audio cue (directional alerts, proximity sounds) should have a corresponding visual indicator.
- **Infinite render distance without LOD** -- Rendering detailed geometry at all distances tanks frame rate. Use LOD (level of detail) groups and impostor billboards for objects beyond 20 m.

## Reference Documents

- [Comfort Guidelines](references/comfort-guidelines.md) — Motion sickness prevention, FOV management, refresh rates, session design
- [Interaction Patterns](references/interaction-patterns.md) — Input modalities, feedback design, multi-modal support
- [Spatial Layout](references/spatial-layout.md) — Depth zones, UI placement, scale, spatial audio, environment design
- [Accessibility](references/accessibility.md) — Physical, visual, audio, cognitive accessibility and motion sensitivity

## General Guidance for Design Reviews

When reviewing a design or providing UX guidance for an immersive experience, consider the following approach:

1. **Start with comfort.** Identify any potential sources of discomfort before evaluating any other aspect of the design. Comfort issues are show-stoppers.

2. **Evaluate the interaction model.** Determine whether the chosen interaction patterns are appropriate for the content and audience. Ensure they are learnable and provide adequate feedback.

3. **Assess spatial layout.** Check that content is placed at appropriate depths, UI is readable and reachable, and the environment supports orientation and navigation.

4. **Review accessibility.** Verify that the experience can be enjoyed by users with diverse abilities. Identify any interactions or information channels that lack alternatives.

5. **Consider the full session.** Think about the experience over time — onboarding, sustained use, transitions, and session end. Comfort and usability must hold up across the entire duration, not just the first few minutes.

6. **Prioritize recommendations.** Not all issues carry equal weight. A comfort violation that causes nausea is more urgent than a suboptimal button placement. Communicate severity clearly in any review.
