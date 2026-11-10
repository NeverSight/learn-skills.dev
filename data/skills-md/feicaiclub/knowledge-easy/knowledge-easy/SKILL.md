---
name: knowledge-easy
description: Create and revise Chinese-language knowledge videos, covering research and scripts, visual design, original illustration, footage selection, editing, narration, sound, and review. Can also handle any one of these stages on its own.
---

[Purpose]
    Make visuals, language, and sound work together to explain an idea. Set the quality floor through convincing forms, clear hierarchy, material treatment, purposeful motion, readability, and sound. Let the subject determine the story, visual approach, and editing. Reuse drawing, layout, and animation capabilities while designing the content anew for each project.

[Scope]
    Read the user's request, current files, and previously approved decisions before choosing the scope:
    Writing or revising a script:
        Deliver in this turn: the script and any necessary fact-checking. Do not add visual directions to a requested narration-only script.
        What this establishes: script completion does not establish that the video works.
    Editing or reviewing the Skill:
        Deliver in this turn: local instructions, configuration, and any source changes needed, with consistent file references.
        What this establishes: mark production and visual checks that have not been run as pending.
    Producing or revising a video:
        Deliver in this turn: complete the affected production steps and review the actual visuals and full audio.
        What this establishes: record technical checks, self-review, and user approval separately.
    This file contains the complete production instructions. Do not create a separate AGENTS.md or a second set of directing rules. Reference files provide interfaces, parameters, and sources; the visual handbook is for the user and is not an execution dependency for the Agent. Video production currently supports Chinese only. Keep dependencies, models, caches, projects, and outputs outside the Skill directory.
    Editing the Skill alone does not trigger generation, sample videos, rendering, installation, or publishing. When the user will run it themselves, deliver the source and identify what remains unverified. Read [Commands and Project Files](references/workflow.md) and [Runtime Setup](references/runtime.md) only when production requires commands. Proceed independently within the authorization already given; do not repeatedly request approval for ordinary design decisions.

[Creative Direction]
    Understand the script's central question, turns in the argument, and final takeaway before choosing visuals. When shortening an approved script, preserve its strong opening, main points, concrete examples, and logical connections. Verify facts, concepts, quotations, data, and identities; distinguish evidence, inference, and visual metaphor.
    Before reading example stories or shot code, record the following decisions in the project's existing notes, or in research/design.md if none exist. For a small revision, update only what it affects.
    Change in understanding:
        What does the viewer believe at the start, and what do they understand by the end? Where do they need to see evidence, a comparison, or a mechanism?
    Presentation approach:
        Why does this subject call for live action, illustration, diagrams, investigation, a continuous scene, or mixed media? When several structures are plausible, compare them and explain the choice; do not require a fixed number of options.
    This film's visual language:
        Define the subjects' forms, spatial relationships, lighting and color logic, typographic roles, materials, framing, and motion. Record which qualities need to remain consistent within the project and which can vary.
    Reference qualities:
        Choose images or work suited to the subject. When the user requests a close reconstruction of a particular reference, compare silhouette, proportions, placement, color, lighting, and motion point by point. Credit copied studies rather than claiming them as original. Maintain the implementation code in this project.
    Shot intent:
        For each shot with a distinct purpose, record “corresponding line → subject and shot size → visible action or information change → implementation source → reading or action completion condition.” Estimate timing first, then align it to the finished narration.
    “Pressure” might appear as a growing load, shrinking space, or obstructed movement. “These are different” might be explained through a visible difference at a common scale. Do not turn every sentence into a title card or force every subject into the same character journey. The content determines the opening, subjects, composition, action, and ending. Once the approach is established, use example source files to learn how to implement it.

[Footage and Lighting]
    First decide what each piece of media must contribute: factual evidence, human behavior, a setting, a mechanism, or emotion. Review user-provided material for its intended use, preserving valuable expressions, gestures, and context.
    Search terms should describe the subject, action, shot size, and light together. “Backlit by a window, a hesitant face in profile, close-up” is more useful than “emotion.” Review usable ranges, changes in action, and potential edit points. A thumbnail, tag, or convenient download is not a reason to choose a shot. See [Media Sources and Records](references/assets.md) for candidate notes and source fields.
    Check whether lighting separates the subject from the background, preserves detail in highlights and shadows, creates depth, and supports the intended mood. For graphic sequences, blurred moving backgrounds establish atmosphere while foreground evidence and people remain sharp. If the footage is visually weak, keep looking; extra blur or grain cannot supply the missing quality. Where relevant, check shot size, eyelines, direction, and brightness across cuts. Deliberate visual contrast is allowed.
    Film and TV clips, live-action footage, archival material, original work, and generated media may be combined. Real evidence must remain traceable; illustrations and reconstructions must not masquerade as records. Do not impose a fixed ratio of media types. When a project requires unique shots, check identity within the original work: cropping, retiming, renaming, or taking another range from the same shot does not make it a new shot. See [Licenses and Sources](references/sources.md).

[Visual Design]
    The default video graphics retain the cinematic compositions established in the first version: moving film or live-action footage, softened with blur and tonal adjustments, supports sharp images, relationship diagrams, paper cards, and lit Song-style typography. Draw illustrations against the selected editorial illustration references. For a new subject, change the objects, footage, composition, and content while preserving the approved visual language. Develop a different style deliberately when the user selects one.
    Design representative shots in this order, then extend the approach to related shots:
    Form and space:
        Start with silhouette, balance, scale, overlap, and room for action. Hands should touch the objects they hold; feet should meet their supports; shadows should match the light. Do not use the same stock figure and pose for every situation.
    Hierarchy and reading:
        Separate the subject, explanation, evidence, and captions. The order of headline and evidence should follow the argument. Route connectors around text and place labels near what they identify. Crop images without losing expressions, action endpoints, or important evidence.
    Color and materials:
        Establish value structure first, then assign accent and supporting colors. Shadows describe space, lines describe structure, and texture describes material. The image should still be organized when decorative effects are removed.
    Key states and motion:
        Define the state before an action, the transition, and the result. Make those states readable before connecting them. The composition must accommodate the final positions of subjects and text.
    For explanatory graphics, start around 54–76 px for headings, 32–40 px for explanatory text, and 26–30 px for supporting information. For short cinematic titles, retain the scale, proportions, and spacing of the selected reference rather than shrinking all display type to body-text sizes. Use natural spacing and intact phrases in Chinese; handle punctuation, line breaks, and isolated final characters. If text does not fit, change the composition or wording. Captions and text within the graphic serve different roles; do not make room merely by shrinking the type. Captions default to one line, divided by phrase and aligned to the actual speech. See [Chinese Production](references/language.md) for fields and current length limits.
    During production, inspect representative frames and key actions using the source that will actually appear in the film. If form, type hierarchy, lighting, or motion still has obvious problems, fix the cause before extending it across the film. A separately drawn attractive preview cannot validate a different implementation. When only editing source, leave this check pending.

[Using Components]
    Identify the relationship the current passage needs to explain before choosing a component. Read the matching input example in [Component Inputs and Integration](references/packaging.md) and its actual renderer; do not guess parameters from the name.
    Subjects, questions, and chapter structure:
        Reusable base components: hero, chapter
    Comparisons at a common scale and quantities:
        Reusable base components: compare, quantity
    Evidence, details, and context:
        Reusable base components: evidence, context
    Relationships and feedback:
        Reusable base components: relation, feedback
    Change over time:
        Reusable base component: timeline
    Locations, routes, and changes between periods:
        Reusable base components: map-focus, map-route, map-period
    These are starting points for selection, not a checklist every film must complete. A live-action shot can stand on its own. Complex explanations may combine layouts, SVG, footage, and text, or use a project-specific renderer.
    Integration sequence:
        Declare component or components in the project's film.json → scripts/composition.py resolves the layers → editorial.py in the project's kit snapshot calls the base layout, extension, or artwork renderer. Supply this film's content through data and arrange timing through cues and local start/duration. A layer's frame only scales and positions it proportionally; it does not reflow the layout. After scaling, reassess type size, line weight, and room for action at the final output size.
    Reusing an existing design:
        Call the complete source, preserving effective paths, letterforms, proportions, overlaps, and motion relationships, then make deliberate changes. Choosing an existing design does not justify replacing it with a few crude shapes and calling that reuse.
    Original illustration:
        Copy the selected SVG source into the project and adapt it, or load project-owned drawing code through artwork. Match SVG layer names to motion targets. JavaScript draws from local time t; see the [Drawing Interface](references/illustration.md).
    New compositions or components:
        Register the source, design rationale, and reference in film.extensions, then call it through the shared interface. New work can exceed the existing designs. Judge explanatory value, form, materials, and motion without requiring visual sameness. Do not bypass registration by replacing shared rendering functions in memory.
    After build, inspect research/component-usage.json. Each instance should identify the actual library snapshot, drawing_source, or extension source and include real reading_order and design_reference values. This record proves where an implementation came from, not whether it looks good. A component ID in design_reference only identifies a comparison target; a project reference image needs an explanation of the qualities being compared. Compare custom work to that reference in actual frames and motion. Component counts, class names, or matching colors cannot replace this assessment.
    Existing projects retain their kit snapshots. Upgrade deliberately only when a new capability is needed. Do not let the current change silently alter an older film.

[Illustration]
    The default illustration direction follows the selected Notion-style editorial references: distinctive silhouettes, natural gestures and poses, black-and-white linework with primary-color shapes, and carefully composed negative space. Establish form, composition, and performance against the reference first, then choose from the reusable drawing methods below. Linework, overprinting, and wash tools do not by themselves establish reference-level quality.
    [Structural Linework](references/styles/etch.md):
        Required qualities: clear hierarchy among contours, structural lines, and hatching; strokes follow form and overlap, with open highlights.
        Open to redesign: people, objects, cutaways, mechanisms, selective color, and viewpoint.
    [Flat Color and Overprinting](references/styles/print.md):
        Required qualities: readable color silhouettes, negative space, and shadows; meaningful layering at overlaps, with clean reading areas.
        Open to redesign: palette, scale, space, light source, overlaps, and action.
    [Natural Wash](references/styles/wash.md):
        Required qualities: stroke width and direction respond to structure; transparent washes build depth, with controlled variation at pigment edges.
        Open to redesign: organic forms, flow, terrain, abstract processes, and framing.
    For a person, draw the line of action, shoulder and hip angles, support, and hand relationships before facial features and clothing folds. For an object, establish thickness, openings, support, and contact before its surface. For organic forms, establish branching, flow, and density before leaves or water marks. Important contours must remain readable at the final size; close-ups must not expose careless seams.
    Drawing tools provide construction techniques, not automatic direction or artistic judgment. hatch does not understand surfaces, person does not invent a new character, and foliage does not establish branch connections. When the image requires more complex volume, poses, or materials, develop them in project code or choose a more suitable drawing implementation. Existing helper functions are not a ceiling on creativity.

[Editing and Motion]
    Establish the timing of complete narration or key actions before setting the edit. Estimated shot durations cannot override actual pauses and phrase endings. Shape passages through progression, holds, changes in information density, and shot size rather than assigning equal time to every sentence.
    Give each movement a cause, a purpose, and an outcome. Direct attention to the subject first, introduce the relevant objects before connecting them, and let viewers read evidence before presenting the conclusion. Make causal changes visible. Characters need anticipation, action, and follow-through; held objects move with the hand, and overlaps change with the pose. Redesign continuous drifting, identical slide-ins, or repeated zooms that add no explanatory value.
    Count reading time from the moment the essential information becomes legible. Allow time to see and understand it. In fast passages, reduce simultaneous information. Reveal complex relationships in stages or hold the frame instead of cutting away merely to create speed. Transitions may come from shapes, spatial action, turns in the argument, or sound, and a direct cut is often appropriate. Do not impose quotas for camera moves or transitions.
    When visuals, sound effects, or music need the same cue, use a shared event ID in film.beats. Drawing code reads local data.beats; audio reads event/offset. See [Timing Interface](references/direction.md#one-event-clock) for conversions between absolute and local time. Meaning leads in narration-driven passages; musical phrases can lead when the music is intentionally driving the sequence. Do not lock the entire film to a beat grid.

[Narration and Sound]
    Use the approved “Steady Male Voice — Tight Phrasing and Clear Emphasis” by default. See [Narration](references/voice.md) and the [Voice Profile](assets/voice/profile.json) for the actual model, Ryan preset, reference sample, and invocation. Preserve the approved voice identity while rewriting each segment's direction for its script. Move lightly through secondary words, emphasize key words briefly and decisively, and leave space at turns in the argument. Avoid uniform speed and emphasis throughout. If a new reading sounds flat or drawn out, revise the model's native delivery instructions and regenerate it. Do not automatically retime, lower the pitch, or reshape its resonance.
    Assign sound by the shot's needs: narration carries the argument, ambience establishes the space, Foley describes contact and material, and music develops emotion and structure. The next shot's sound can enter before the cut, or the previous shot's sound can continue across it. Preserve purposeful silence. Do not attach the same whoosh to every text entrance or keep the soundtrack full merely to avoid quiet.
    Listen through the complete mix. Check consonant clarity, emphasis, phrase endings, joins, background masking, and effects that arrive too early or late. Use ASR to locate missing or repeated words; it cannot certify emphasis, pronunciation, emotion, or a natural human delivery. Regenerate complete thought groups with context and intact beginning and ending syllables. Approval of a voice reference does not automatically approve each new passage.

[Quality Review]
    These checks apply to actual video production. Editing the Skill alone must not trigger them or mark them as passed.
    Representative design review:
        Before extending the approach across the film, use the actual source to inspect frames and actions that expose the project's main challenges. Compare specific qualities against the selected references. Fix structural issues in the shared source or affected shots before copying the problem further.
    Export review:
        Before delivery, record the following three areas separately:
    Technical integrity and provenance:
        Inspect: full decoding, duration, and audio tracks; source, component usage, and export version alignment; missing assets, truncation, and out-of-bounds content.
        If something fails: fix it and rebuild the affected output. Previous records cannot be reused for changed results.
    Individual shot design:
        Inspect: subjects, letterforms, lighting, materials, and explanatory value at final size. Watch each action from beginning to end, and zoom in to check contact, overlap, connectors, and transitions.
        If something fails: revise the forms, composition, information order, or motion rather than hiding the issue under more decoration.
    The full viewing experience:
        Inspect: watch the entire film with sound at normal speed. Assess the progression of the argument, repeated shots, changes in pace, reading time, narration, and mix.
        If something fails: fix the structure and audiovisual relationships. A single-shot screenshot cannot establish that the sequence works.
    Turn abstract judgments into checkable observations. For example: “The relationship line appears before the node on the right, so the viewer cannot identify what it connects.” Record the location and resolution. Apply the same quality dimensions to custom and existing components. New styles may use different materials, but the review must identify observable qualities of form, space, contrast, and completed motion. “Premium,” “textured,” or “uses components” is not sufficient evidence.
    The built-in tools work as follows; see [Production Commands](references/workflow.md):
        build generates scenes, component-usage.json, and a build provenance record. Check that actual usage matches the design intent.
        render exports a new version, runs technical checks, binds the export to its source, and prepares review evidence. review-visuals can prepare evidence again for the same export.
        Inspect the actual frames, motion clips, and full film referenced by review/visual-review.json. Record what you watched, concrete observations, and conclusions. If default frame sampling misses complex action, inspect additional key states. A contact sheet alone does not count as watching motion.
        accept-visuals checks record completeness and correspondence among evidence and versions. It does not automatically judge aesthetics or establish user approval. Unseen, unheard, or unresolved items remain pending or fail.
    Report technical results, self-review, user approval, and unperformed checks separately. After changes, repeat the affected checks. If editing, mixing, or passage structure changes, review the complete affected passages and their joins again. If the source has not been exercised, report only that the source changes are complete; leave the resulting quality unverified.

[Adapting to New Subjects, Feedback, and Delivery]
    When applying the same capabilities to a new subject, reconsider objects, composition, materials, information order, and motion relationships. Changing colors and text alone does not demonstrate adaptability. If the user asks to verify reuse, choose genuinely different subjects and explanatory challenges, then compare whether the original quality holds up. Do not expand the assignment automatically just to demonstrate adaptability.
    Use the established [Lazy Studio](references/studio.md) review flow: M → comment → Enter. Back in the original conversation, read the text and screenshots for the specific version. Preserve feedback and use a new filename for each output. Ordinary revisions should retain other approved work.
    Deliver the files and results needed for the current request, their locations, checks performed, and pending items. Preserve the FEICAI startup mark, the selected voice reference, and user-specified brand assets. Install, package, or publish only when requested. Keep the Skill directory limited to instructions, necessary assets, and source code, without test films or runtime dependencies.

[Initialization]
    When actually using this Skill, display the FEICAI mark below verbatim in the conversation, once per conversation. It is the user's personal brand, “Feicai.” Preserve its letterforms and do not remove it as an external watermark; retain it when editing files as well. It is a conversation startup mark. Follow the user's existing arrangements for branding within the film, without automatically adding a branded intro or outro.
    ```text
    ███████╗███████╗██╗ ██████╗ █████╗ ██╗
    ██╔════╝██╔════╝██║██╔════╝██╔══██╗██║
    █████╗  █████╗  ██║██║     ███████║██║
    ██╔══╝  ██╔══╝  ██║██║     ██╔══██║██║
    ██║     ███████╗██║╚██████╗██║  ██║██║
    ╚═╝     ╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝
    ```
