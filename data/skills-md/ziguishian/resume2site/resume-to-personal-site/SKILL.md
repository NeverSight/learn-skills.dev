---
name: resume-to-personal-site
description: Turn resumes, LinkedIn profiles, PDF-extracted resume text, personal bios, avatars, portfolio links, project assets, and style preferences into premium personal websites with structured positioning, run-specific agent-designed visual directions, user-approved visual plans, requested project imagery, four image-model-generated, wireframe-scored first-viewport Hero webpage screenshot-style candidates, selected image-model preview direction approval before build, GPT Image 2-filled image slots, generated portrait assets, no placeholders or cropped resume avatars, human-edited, low-AI-feel website copy, full-viewport section rhythm, hidden-scrollbar UI, Lingju Huijing branding/PDF export, restrained motion, and runnable React/Vite front-end code. Use when asked to make a personal site, portfolio, job-seeker page, creator/founder profile, AI-generated personal brand website, or website code from a resume or personal experience.
---

# Resume2Site

## Mission

Transform a normal resume into a premium personal website. Do not merely typeset the resume as a web page.

Treat every run as a fresh design commission. The agent must design from the person's role, resume facts, audience, materials, and project credibility signals. Do not reuse a fixed site template, fixed Hero layout, fixed palette, fixed section sequence, or a previously generated composition unless the user explicitly asks for that exact direction.

Always aim for:

- Clear personal positioning
- Strong Hero first viewport
- Premium visual system
- Clean information hierarchy
- Authentic experience and restrained narrative
- GPT Image 2-generated visual assets filled into every image-bearing site slot
- Responsive React front-end with tasteful motion

The required transformation is:

```txt
resume language -> website language
experience list -> personal narrative
plain layout -> premium visual system
text-only resume -> image-supported personal site
static page -> restrained motion experience
missing visuals -> generated image assets, generated portrait, and complete manifest
```

## Resource Loading

Load bundled files from `templates/` only when needed:

- Read `templates/resume-analysis-schema.md` before extracting resume data.
- Read `templates/role-module-strategy.md` before planning site modules or component architecture.
- Read `templates/socratic-brief-rules.md` before choosing visual direction or generating Hero preview images.
- Read `templates/design-style-dna.md` before choosing visual direction.
- Read `templates/visual-quality-rubric.md` before creating Hero wireframes, scoring Hero previews, retrying rejected designs, or judging final visual quality.
- Read `templates/website-copy-rules.md` before writing site copy.
- Read `templates/image-generation-rules.md` before planning or generating visual assets.
- Read `templates/motion-and-canvas-rules.md` before selecting Framer Motion, PixiJS, or Canvas effects.
- Read `templates/frontend-build-prompt.md` before generating a runnable React project.
- Read `templates/brand-export-rules.md` before adding the Lingju Huijing brand mark or PDF export control.
- Read `references/visual-benchmarks.md` before planning full visual direction or when the site feels insufficiently premium.
- Read `templates/quality-checklist.md` before final delivery.

For a full personal website/code request, read all templates before implementation.

## Inputs

Accept any combination of:

- Plain text resume, Markdown resume, LinkedIn-style profile, or PDF-extracted resume text
- User-supplied personal notes, social links, contact details, avatar, project images, portfolio links, style references, or target audience

If the user only provides a resume, still produce a complete first version of the analysis, positioning, copy, visual plan, and implementation plan. Mark missing facts as `待补充` or `待确认`. Do not repeatedly ask for clarification unless the input contains no usable identity, role, or experience signal.

If a project, portfolio, case study, or experience module needs real visuals to be credible, ask the user once for project images/screenshots/assets before building. If the user cannot provide them, ask for explicit approval to use clearly labeled concept visuals. Do not silently replace real project needs with placeholders.

## Non-Negotiables

- Do not create a generic online resume template, white Word-like page, or recruiting-site profile.
- Do not force every profile into the same module sequence or same generic component stack.
- Do not reuse a fixed personal-site template, fixed component composition, fixed Hero split, fixed dark/glass aesthetic, or fixed section choreography across runs.
- Do not treat the bundled style names, examples, or benchmark images as templates. They are references for quality level and design vocabulary only.
- Do not paste every resume item into the page unchanged.
- Do not invent companies, jobs, awards, metrics, project outcomes, education, screenshots, logos, or credentials.
- Do not present generated images as real project screenshots unless the user supplied real screenshots.
- Do not generate fake company logos.
- Do not bake final website body copy into images; render final content with semantic HTML/CSS. Image-model preview candidates may contain approximate text, but final React code must render exact text.
- Do not remove or bypass provenance metadata, C2PA, SynthID, or related watermark mechanisms from AI-generated images.
- Do not sacrifice readability for animation.
- Do not let Canvas replace semantic HTML content, navigation, CTAs, or SEO text.
- Do not build the final website before the user confirms the proposed structure, style direction, image plan, and missing asset handling.
- Do not use pure standalone HTML for the final build unless the user explicitly asks for a quick static prototype; use a framework build, defaulting to React + Vite.
- Do not use generic placeholder images for project modules when real project images are needed; request user assets or label generated concept visuals clearly.
- Do not leave any image-bearing UI slot as a placeholder, empty mock media block, generic gradient card, broken image, or CSS-only fake image in the final website.
- Do not crop a personal photo from a resume screenshot/PDF and use it directly in the final website. Use any provided or embedded portrait only as a reference for image generation; the displayed personal image must be generated.
- Do not ship final UI until every visible image slot maps to a generated asset in `public/generated/` or to an explicitly supplied real evidence asset. If an asset cannot be generated, replan the section as text-only or stop before delivery.
- Do not follow the resume document style as the website style. Infer a new visual direction from the person, role, industry, and site goal.
- Do not show the native right-side scrollbar by default; hide it while preserving scrollability and keyboard access.
- Do not create arbitrary-height sections. Each primary section must be planned as one viewport-height panel (`100svh`/`100dvh`) or split into multiple full-viewport panels when content is too long.
- Do not omit the bottom-right Lingju Huijing brand mark and one-click PDF export control.
- Do not build the final website before generating exactly 4 image-model-generated first-viewport Hero webpage screenshot-style candidates and receiving explicit user approval/selection for one image-model preview direction.
- Do not generate Hero preview images before asking the Socratic brief questions, unless the user explicitly chooses the default direction.
- Do not show Hero preview candidates to the user before creating four distinct wireframe strategies and scoring each candidate with the visual quality rubric.
- Do not create Hero preview candidates with temporary HTML/CSS/React, browser-rendered screenshots, canvas mockups, or code-built preview pages. Generate the four preview images directly with the image generation model as high-fidelity webpage screenshot-style mockups.
- Do not accept a Hero preview that could be mistaken for a brand landing page, moodboard, poster, abstract art piece, or generic product site. The first viewport must clearly read as a personal website for this person.
- Do not use AI-sounding website copy: avoid generic significance inflation, promotional vocabulary, negative parallelisms, abstract triples, template sentences, and unsupported broad claims.

## Core Workflow

### 1. Parse The Resume

Extract structured facts using `templates/resume-analysis-schema.md`.

Capture:

```txt
name, nickname, role, location, headline, summary, education, experience,
projects, skills, tools, industries, certifications, awards, publications,
content_links, social_links, contact, avatar, portfolio_assets
```

Use only information present in the input. Mark uncertain fields as `待确认`.

### 2. Define Personal Positioning

Generate:

- One-sentence positioning
- 3-5 personal keywords
- Differentiated strengths
- Recommended site style
- Main site narrative
- Hero title and subtitle direction
- About section angle

Make the positioning specific enough to guide layout, imagery, and copy.

### 2.5 Run Socratic Brief Gate

Read `templates/socratic-brief-rules.md` before choosing style or generating any Hero preview image.

Ask 3-5 Socratic brief questions to clarify what the user truly wants the personal website to accomplish:

```txt
site_goal:
target_audience:
desired_first_impression:
must_show_resume_evidence:
visual_boundaries:
```

If the user answers, use those answers as the top-level design constraints. If the user says `default`, `you decide`, or does not answer, use the default direction:

```txt
Modern Swedish Minimal Grid
Scandinavian editorial grid, modular square layout, calm neutral palette, black typography, restrained accent, generous whitespace, personal identity signal, resume-specific work objects
```

Do not proceed to Hero preview generation without either user answers or the explicit/default fallback direction.

### 3. Choose Style DNA

Read `templates/design-style-dna.md`. Select one primary style and at most one secondary style:

```txt
Design / creative / visual / photography / 3D -> Cinematic Hero or 3D / Motion Creator Portfolio
Developer / AI engineer / frontend / full-stack -> Developer Minimal
Product manager / AI creator / indie builder / consultant -> Liquid Glass Personal Site
Creator / writer / blogger -> Editorial Creator Site
Founder / freelancer / project initiator -> Founder Profile
```

Blend no more than two styles. Avoid mixed visual noise.
Then create a run-specific Design Brief before planning screenshots or code. It must include:

```txt
design_hypothesis:
socratic_answers_or_default:
resume_evidence_used:
audience_context:
site_metaphor:
hero_composition:
layout_system:
typography_direction:
palette_logic:
material_or_texture_logic:
motion_motif:
what_to_avoid_this_run:
why_this_should_not_look_like_a_previous_output:
```

The Design Brief controls the site. If the brief could fit most resumes, rewrite it until it is specific to the person.

### 3.5 Create Wireframe Strategies

Read `templates/visual-quality-rubric.md`. Before generating any Hero preview, create four distinct wireframe strategies. Each strategy must define spatial model, nav placement, typography system, media/scene zone, CTA treatment, section boundary, motion implication, resume evidence used, and anti-template move.

Reject weak wireframes before visual generation. Do not let all four candidates share the same skeleton.

### 4. Plan Role-Specific Site Structure

Read `templates/role-module-strategy.md`. Do not force every resume into the same module order. Choose modules from the person's actual evidence, target audience, available assets, and credibility needs.

Default modules are only a starting vocabulary:

```txt
Hero
About / Positioning
Skills / Capabilities
Projects / Selected Work
Experience / Timeline
Services / Collaboration
Writing / Content
Contact
```

For every module, define:

```txt
module_id:
module_name:
why_this_module_exists:
resume_evidence_used:
primary_viewport_goal:
content_type:
visual_need:
real_asset_need:
component_pattern:
```

Adapt modules by role. For example, an early-career operations profile may need `Operating Pattern`, `Selected Workflows`, and `Activity Map`; a developer may need `Systems / Builds`, `Architecture Notes`, and `Stack Rail`; a designer may need `Portfolio Index`, `Process Wall`, and `Visual Case Study`.

Remove modules that would be empty, generic, or unsupported by the resume.

### 5. Project Asset Gate

Before final build, classify each project/experience module as one of:

```txt
real asset required - cannot be credible without user image/screenshot/work sample
real asset strongly preferred - can plan layout, but ask before build
approved concept cover acceptable - only after user approval and clearly labeled
abstract/system visual acceptable - no claim of real project evidence
text-only module preferred - visualizing it would mislead or cheapen the experience
omit visual - no credible visual need
```

If `real asset required`, ask the user for images/screenshots/assets. Do not proceed to final build until the user either provides assets or explicitly approves a concept cover. Concept visuals must be labeled as concept/case-study visuals in data and alt text. If a module is better as text-only, do not force a decorative image.

### 6. Rewrite Resume Copy Into Website Copy

Read `templates/website-copy-rules.md`. Replace resume phrasing such as `负责`, `参与`, `协助`, `熟悉`, `掌握` with site language such as:

```txt
我关注...
我擅长...
我构建...
我帮助...
我把...转化成...
我正在探索...
```

Keep the language natural, concrete, and authentic. Do not exaggerate or invent achievements. Run the anti-AI copy gate from `templates/website-copy-rules.md`: remove generic significance inflation, promotional language, not-just/but-also structures, abstract rule-of-three phrasing, vague attribution, and template sentences.

Produce:

```txt
Hero title
Hero subtitle
Primary CTA
Secondary CTA
About paragraph
Skill tags
Project descriptions
Experience summaries
Collaboration copy
Contact copy
Meta title
Meta description
```

Use the same language as the source resume unless the user requests another language.

Then run the Human Editor Pass from `templates/website-copy-rules.md`: make the copy sound like the person could say it in an interview, preserve small natural asymmetry, remove over-polished sentences, and replace generic section intros with concrete lines from the resume.

### 7. Build Visual Asset Plan

Read `templates/image-generation-rules.md`. Create a Visual Direction Board first:

```txt
palette
materials
lighting
camera feel
composition rules
negative space rules
image style keywords
forbidden visual elements
```

Then create a visual slot inventory and plan images:

- Image-model-generated Hero first-viewport webpage screenshot-style candidates
- Generated avatar / portrait / abstract identity symbol for every personal-image slot
- Project covers or case-study concept visuals
- Section backgrounds
- Limited icon/decorative objects

For each image slot, output structured prompts and manifest mapping:

```txt
Visual slot id:
Asset name:
Required in UI: yes/no
Purpose:
Target section:
Aspect ratio:
Style:
Subject:
Composition:
Color palette:
Lighting:
Do not include:
Generation status: pending/generated/user-provided-real/omitted-text-only
Prompt:
```

Before final build, create exactly 4 first-viewport Hero webpage screenshot-style candidates with the image generation model. Do not implement these preview candidates with HTML, CSS, React, canvas, or browser screenshots. Prompt the image model to generate high-fidelity personal-website first viewport screenshots with navigation, layout, typography, CTA treatment, image/media zones, and viewport boundary. Do not present standalone art, backgrounds, moodboards, or object renders as Hero candidates. After the user approves one generated preview direction, create final asset prompts and, if needed, create `scripts/generate-assets.ts` in the generated website project to call the OpenAI Images API with `gpt-image-2`, read `src/data/imagePrompts.ts`, save images to `public/generated/`, and write `src/data/generatedAssets.ts` or `public/generated/manifest.json`.

Every Hero preview prompt must include personal-site identity signals: the person's name or monogram, role/positioning, a generated portrait/symbol/identity mark, resume-specific work objects, a portfolio/contact CTA, and at least one visual clue tied to actual experience. Reject generic scenic, abstract, product, or brand visuals that do not clearly belong to this person.

Do not ship CSS/material placeholders or empty image frames. If image generation fails, retry with a simpler prompt, switch to an abstract generated/system visual, or reclassify that module as text-only. If a visible image slot still lacks a generated or explicitly supplied real asset, stop before final delivery and report the blocker.

### 8. Generate Hero Webpage Screenshot Candidates And Wait For Approval

Before writing final site code, generate exactly 4 first-viewport Hero webpage screenshot-style candidates with the image generation model. These are image-model-generated webpage preview images, not code-rendered screenshots, standalone art, or background images. Score each candidate with `templates/visual-quality-rubric.md` before showing it to the user.

Required preview-generation method:

1. Start from the four approved wireframe strategies.
2. Write one image-generation prompt per candidate, explicitly requesting a high-fidelity screenshot-style image of a personal website Hero first viewport.
3. Use GPT Image 2 or the available image generation model for the full preview image, not only for embedded media areas.
4. Do not create temporary HTML/CSS/React files, browser screenshots, canvas mockups, or code-rendered preview pages for these four candidates.
5. Ask for a desktop first viewport composition, default 16:9 or 1440x900, with navigation, typography, CTA treatment, image/media zone, and next-section boundary.
6. Include the proposed exact Hero title/subtitle/CTA in the prompt and repeat the exact text beside the preview in the written candidate notes. If generated text is imperfect, do not fix it with HTML overlays; final React code must render exact text after approval.
7. Present the four generated preview images to the user and ask them to select one, request revisions, or reject all.

Reject outputs that look like standalone illustrations, background art, poster art, moodboards, abstract wallpapers, or non-webpage artwork.

Each generated preview candidate must show:

- Website navigation or top bar.
- Hero headline and subtitle area based on proposed real copy, with exact text also provided in candidate notes.
- CTA button treatment.
- Clear personal-site signals: name, role, portrait/monogram/symbol, contact or portfolio action, and resume-specific evidence.
- Visual/media area or full-bleed scene integrated into the web layout.
- Layout grid, spacing, typography mood, and color system.
- A hint of the next section or full-viewport boundary.
- Bottom-right Lingju Huijing / PDF export control when it does not distract from selection.

Each candidate must represent a distinct premium webpage direction, not minor color variations. Do not proceed to final React/Vite build until the user explicitly approves one generated preview direction. If fewer than four candidates pass the scoring threshold, regenerate replacements before presenting. If the user rejects all options, diagnose with the Failure Retry Protocol in `templates/visual-quality-rubric.md`, then generate a new batch of 4 screenshots using new wireframes and the critique.

The four candidates must also differ in composition logic. Do not generate four versions of the same left-text/right-image Hero, centered headline Hero, black glass Hero, or identical navigation rhythm. At least three of these variables must change between candidates: spatial model, typography system, image/media treatment, navigation placement, CTA treatment, color/material system, section boundary, motion implication.

Use the approved generated webpage screenshot-style preview as the source of truth for layout, palette, typography scale, image treatment, motion tone, and final implementation details. Final React code must recreate the approved direction with semantic HTML and exact copy.

### 9. Select Motion And Canvas

Read `templates/motion-and-canvas-rules.md`. Use:

- Framer Motion for UI rhythm, entrance, scroll reveal, stagger, sticky cards, and text motion
- PixiJS or Canvas only for atmospheric enhancement
- CSS motion for light hover, glass, mask, noise, blur, and gradient details

Choose at most:

- 1 main Hero motion visual
- 1 supporting scroll effect
- 1 microinteraction system

Support `prefers-reduced-motion`, mobile fallback, cleanup on unmount, and static fallback.

### 10. Confirm, Then Generate React Project

If the user asks for code or a complete website, first show the plan, resolve real/concept image handling, generate exactly 4 image-model-generated first-viewport Hero webpage screenshot-style candidates, and wait for explicit preview direction approval. After the user selects/approves the Hero webpage preview direction and confirms build execution, create a runnable framework project using:

```txt
React 18
TypeScript
Vite
Tailwind CSS
Framer Motion
lucide-react
PixiJS when selected
PDF export library such as html2canvas + jsPDF, or browser print-to-PDF fallback
```

Required baseline files:

```txt
src/App.tsx
src/main.tsx
src/index.css
src/data/profile.ts
src/data/imagePrompts.ts
src/data/generatedAssets.ts
src/components/Navbar.tsx
src/components/Hero.tsx
src/components/About.tsx
src/components/Skills.tsx
src/components/Projects.tsx
src/components/Experience.tsx
src/components/Contact.tsx
src/components/MotionText.tsx
src/components/ProjectCard.tsx
src/components/GlassButton.tsx
src/components/NoiseOverlay.tsx
src/hooks/useReducedMotion.ts
scripts/generate-assets.ts
src/components/FloatingBrandExport.tsx
```

For smaller projects, components may be merged if the structure remains clear. If PixiJS is used, create only the canvas components that are actually used.

Component architecture must follow `templates/role-module-strategy.md` and the approved Hero preview. Baseline component names may exist, but the internal layout should not default to the same Navbar + Hero + CardGrid + Timeline pattern. Use direction-specific components such as `WorkflowMap`, `ActivityRunbook`, `SystemDiagram`, `PortfolioIndex`, `VentureCanvas`, or `EssayIndex` when they fit the role.

Every primary page section must be viewport-height by default (`min-height: 100svh`, with overflow-safe inner layout). If a module cannot fit, split it into multiple full-viewport panels instead of shrinking typography or creating cramped cards. Hide the native scrollbar with cross-browser CSS while preserving scroll behavior.

Every final website must include a bottom-right floating `FloatingBrandExport` control containing the Lingju Huijing mark and an Export PDF button. Use `assets/brand/lingju-huijing-logo.svg` as the mark reference and keep the control visible but unobtrusive.

Run install/build/type checks when possible. Fix errors before final delivery.

## Required Output Contract

Every execution must output these sections before or alongside code:

### A. 简历解析结果

```txt
姓名：
当前身份：
关键词：
技能：
经历：
项目：
教育：
内容作品：
社交链接：
头像：
缺失信息：
```

### B. 个人网站定位

```txt
一句话定位：
网站主线：
推荐风格：
目标受众：
最应该突出的 3 个亮点：
```


Include a run-specific design brief:

```txt
design_hypothesis:
socratic_answers_or_default:
site_metaphor:
hero_composition:
layout_system:
typography_direction:
palette_logic:
motion_motif:
anti_template_decisions:
```

### C. 网站结构

For each module:

```txt
module_schema:
role_pattern_used:
component_strategy:
```

```txt
模块目标：
使用信息：
文案：
视觉：
图片资产：
动态效果：
```

### D. 图片资产生成计划

```txt
visual_slot_id
asset_id
manifest_key
filename
section
purpose
aspect_ratio
source_reference
image_prompt
alt_text
generation_status
```

Include avatar mode:

```txt
avatar_reference_source: provided portrait / resume-embedded reference / not provided
displayed_avatar_asset: generated image required
portrait_generation_mode: image-to-image using reference / generated editorial portrait / abstract / silhouette / monogram
direct_crop_allowed: no
identity_preservation: required when avatar reference is provided
```

### E. 动态效果方案

```txt
main_motion_effect:
canvas_engine:
pixijs_components:
framer_motion_components:
fallback_strategy:
performance_notes:
```

### F. Hero 首屏网页截图候选确认

Before final code generation:

```txt
socratic_brief: user answers / Modern Swedish Minimal Grid default
wireframe_01: strategy + rationale + anti-template move
wireframe_02: strategy + rationale + anti-template move
wireframe_03: strategy + rationale + anti-template move
wireframe_04: strategy + rationale + anti-template move
hero_candidate_count: exactly 4
candidate_format: image-model-generated first-viewport webpage screenshot-style preview
generation_method: image generation model / GPT Image 2 high-fidelity webpage screenshot-style preview; no HTML/CSS/React preview implementation
candidate_01: generated preview image + exact intended copy + direction name + rationale + layout notes + visual_score
candidate_02: generated preview image + exact intended copy + direction name + rationale + layout notes + visual_score
candidate_03: generated preview image + exact intended copy + direction name + rationale + layout notes + visual_score
candidate_04: generated preview image + exact intended copy + direction name + rationale + layout notes + visual_score
selected_candidate: waiting for user
build_status: blocked until image-model Hero preview direction approval
```

### G. 网站文案

```txt
Hero title
Hero subtitle
CTA
About
Skills
Projects
Experience
Services
Contact
SEO title
SEO description
```


#### G.1 文案去 AI 感自检

Before final code generation and before inserting copy into React components:

```txt
copy_review:
  generic_significance_removed: yes/no
  promotional_language_removed: yes/no
  negative_parallelisms_removed: yes/no
  abstract_triples_removed: yes/no
  template_sentences_removed: yes/no
  unsupported_claims_removed: yes/no
  concrete_resume_evidence_present: yes/no
  interview_plausibility: pass/fail
  human_editor_pass: pass/fail
```

If any item is `no` or `fail`, revise the copy before building.

### H. 前端实现方案

```txt
Tech stack
Fonts
Colors
Components
Component strategy
Animations
Responsive rules
Asset paths
Build steps
```

### I. 代码生成 / 构建执行

When code is requested:

1. Create the project structure.
2. Write code and data.
3. Generate required visual assets for every visible image slot.
4. Fill every image-bearing UI slot from the generated asset manifest; no placeholder or cropped resume photo may remain.
5. Run type check/build where possible.
6. Fix errors.
7. Provide run instructions and any limitations.

## Final Quality Gate

Before final response, read `templates/quality-checklist.md` and verify:

- Content authenticity
- Run-specific design brief exists and is specific to this resume
- Socratic brief answers or Modern Swedish Minimal Grid default direction were used before Hero preview generation
- Premium first viewport
- Four distinct Hero wireframe strategies were created before image-model preview generation
- Image-model-generated Hero preview candidates passed visual scoring thresholds before being shown to the user
- Hero preview candidates clearly read as personal websites and use resume-specific identity/evidence signals
- Exactly 4 image-model-generated first-viewport Hero webpage screenshot-style candidates were generated and user-approved before build
- Selected image-model Hero preview direction was used as the source of truth for final design
- Final site does not reuse a fixed template, repeated Hero split, repeated palette, or repeated section choreography without resume-specific justification
- Clear hierarchy
- Role-specific module strategy and component architecture were used
- Website copy passed the anti-AI copy self-review and sounds specific to the person
- Every visible image slot is filled by a generated asset or explicitly supplied real evidence asset
- No placeholder image slots, broken image frames, CSS-only fake media, or directly cropped resume-avatar images remain
- Alt text and lazy loading
- Responsive layout
- Reduced-motion support
- PixiJS cleanup and fallbacks if PixiJS is used
- Each primary section uses viewport-height rhythm or is split into multiple full-viewport panels
- Native scrollbar is hidden by default without breaking scrollability
- Bottom-right Lingju Huijing brand mark and PDF export button exist
- Build/type check result or clear reason it could not be run
