---
name: chinese-calligraphic-font-generation
description: Generate Chinese text in flowing handwritten calligraphy style with reference images, white background, and natural stroke continuity. Use this skill whenever the user asks for atmospheric/vibe-y Chinese handwritten typography (氛围感手写字体), flowing script text (飘逸手写体), or brush-pen style Chinese phrases for social media covers, quote cards, or design mockups — especially when they reference "手写体", "书法感", or want text that looks written in one continuous stroke.
---

# Chinese Calligraphic Font Generation

## Core Methodology

### Multi-Reference Style Synthesis Framework

When designing custom typography from reference images, apply **Reference Ensemble Logic** — treat each reference image as encoding different dimensional attributes of the target style:

**Dimension 1 (Stroke Gesture)**: Character-level line quality — fluidity, pressure variation, speed signature
- Flowing handwritten (飘逸手写体): light entry, accelerating mid-stroke, tapering exit
- Message board casual (留言板): consistent pressure, minimal variation, relaxed tempo
- **Rounded terminals**: every stroke start and end point must be soft and rounded — never a sharp, pointed, or "whip-crack" tip. This applies at both the character level and the phrase-level entry/exit strokes.

**Dimension 2 (Structural Rhythm)**: Spatial distribution patterns across characters in a phrase
- Vertical alignment tolerance (baseline drift within ±5-10% of character height)
- Horizontal spacing consistency (inter-character gaps vs intra-character density)
- Size variation logic (emphasis through scale vs uniform rhythm)

**Dimension 3 (Material Impression)**: Simulated writing instrument and surface interaction
- Brush texture (ink diffusion, bristle marks, pressure pooling)
- Pen texture (smooth flow, edge clarity, uniform width)
- Digital simulation markers (anti-aliasing quality, vector precision)

**Dimension 4 (Compositional Balance)**: Phrase-level layout principles
- Center-weighted (symmetrical character distribution)
- Asymmetric flow (progressive size/weight shift left-to-right)
- Vertical stacking vs horizontal expansion

**Synthesis Strategy**: Extract dominant attributes from each reference image and blend into a unified style profile. When references conflict (e.g., one shows tight spacing, another loose), prioritize the attribute appearing in majority of references.

### Primary vs. Secondary Reference Weighting

This skill bundles six proven reference images in `assets/`:

- `assets/reference-01-primary.png` and `assets/reference-02-primary.png` — **anchor references**. These two have tested as the most reliable at reproducing the target style and should be treated as the dominant style signal whenever attributes conflict across references.
- `assets/reference-03.png` through `assets/reference-06.png` — **supporting references**. Use these to reinforce the consensus and widen the sample so the model doesn't overfit to only two images, but if any of them pulls in a different direction than the two primary images, defer to the primary pair.

**Always attach all six images** to the generation request (see Reference Attachment below) — even though 01 and 02 carry more weight, the full set is what keeps the style profile stable across repeated generations. Dropping to fewer than three images risks the model overfitting to idiosyncrasies of whichever one or two remain.

### One-Pass Continuity Principle

Chinese calligraphy derives authenticity from **连笔 (lián bǐ)** — the natural flow when a human hand writes multiple characters without lifting the pen. This is NOT merely connecting strokes visually, but encoding the biomechanical rhythm of continuous writing:

- **Momentum Transfer**: Each character's exit stroke velocity influences the next character's entry angle
- **Energy Conservation**: A natural writer decelerates before directional changes, accelerates on straight paths
- **Micro-Variations**: Subtle rotation drift (±2-5°) and baseline shift maintain organic feel vs mechanical repetition
- **Soft Terminals**: Deceleration into rounded entry/exit points, not an abrupt release that leaves a sharp tail

Implementation: Generate the entire phrase as a single compositional unit, NOT character-by-character assembly. The latter produces dead joints where strokes meet.

### Background Isolation Protocol

**Pure White Requirement**: Background must be #FFFFFF (RGB 255,255,255) with NO:
- Texture overlays (paper grain, canvas weave)
- Shadow casting from strokes
- Gradient transitions (should be flat white)
- Edge halos or anti-aliasing artifacts bleeding into background

Test: Sample 10 random background pixels — all must return exactly (255,255,255). Acceptable tolerance: 0 values deviation.

## Workflow

### 1. Preparation Stage

**Input Checklist**:
- Target text string (Chinese characters, 2-10 characters optimal for calligraphic balance)
- Reference style images: use the six bundled in `assets/` (see Primary vs. Secondary Reference Weighting above) unless the user supplies their own
- Background specification (default: pure white #FFFFFF)

**Reference Analysis**:
For each reference image, extract:
1. **Stroke weight range** (thinnest to thickest in pixels if measurable)
2. **Dominant gesture** (flowing/rigid, fast/slow, light/heavy pressure)
3. **Spacing rhythm** (tight/loose, uniform/varied)
4. **Stylistic markers** (brush texture? pen precision? digital smoothness?)
5. **Terminal quality** (confirm rounded, non-sharp entry/exit points — this is a hard constraint, not just a style preference)

Create a style profile summary encoding the CONSENSUS attributes across all references, weighted toward the two primary images.

**Key Decision**: Determine if references represent a single unified style (ensemble synthesis) or multiple distinct options (user chooses one). Default assumption: unified synthesis unless references show irreconcilable conflicts.

### 2. Initial Generation Stage

**Prompt Structure**:
```
[Target text] + [Style synthesis description] + [Technical constraints]
```

Example breakdown:
- **Text**: "自然流畅,一气呵成" (8 characters)
- **Style synthesis**: "飘逸手写体风格 (flowing handwritten), 笔画连贯自然 (continuous natural strokes), 起笔落笔圆润无尖锐笔锋 (rounded stroke starts and ends, no sharp tips), 参考书法家随性书写的节奏 (reference calligrapher's spontaneous rhythm)"
- **Technical constraints**: "纯白色背景 (#FFFFFF), 无阴影, 无纹理, 单笔完成效果 (single-pass writing effect)"

**Reference Attachment**: Include ALL six images from `assets/` in the generation request, even when synthesizing into a unified style — the model needs the full context to keep results consistent across generations. If the user provides their own references instead, apply the same primary/secondary weighting logic to whichever ones they say worked best.

**Composition Calibration**:
- Horizontal text: Aim for 3:1 to 5:1 width-to-height aspect ratio
- Vertical text: Invert to 1:3 to 1:5 ratio
- Character count affects ideal canvas — 4 characters = more spacious, 10 characters = tighter rhythm

### 3. Iteration Stage

**Stroke Quality Audit**:
- [ ] Pressure variation visible (thick/thin modulation within strokes)
- [ ] Entry/exit points are soft and rounded — zero sharp or needle-like tips anywhere in the phrase
- [ ] Directional momentum logical (follows natural hand movement paths)
- [ ] No mechanical repetition (each instance of same character shows micro-variation)

**Continuity Check**:
- [ ] Inter-character transitions feel like one writing session (no style breaks)
- [ ] Baseline drift stays within organic tolerance (not laser-straight, not chaotically wandering)
- [ ] Spacing rhythm matches reference consensus

**Background Purity Test**:
- [ ] Sample 10 random background pixels → all (255,255,255)
- [ ] No shadow halos around strokes
- [ ] No texture/grain/paper effects
- [ ] Clean edge separation between strokes and background

**When to Regenerate**:
- Background fails purity test → Add explicit "纯白背景,无任何纹理阴影" (pure white background, no texture or shadow) constraint
- Strokes look machine-generated → Emphasize "自然手写感,笔画有轻重变化" (natural handwritten feel, stroke weight variation)
- Characters feel disconnected → Request "一气呵成的连贯书写效果" (continuous one-pass writing effect)
- Any stroke ends in a sharp point or spike → Request "起笔落笔圆润处理,无尖锐笔锋" (rounded stroke starts/ends, no sharp tips) explicitly and regenerate

**When to Accept**:
- Stroke quality matches reference style profile consensus
- Continuity passes organic writing test
- All terminals are rounded, no sharp tips anywhere
- Background passes purity test
- Overall composition balanced (no awkward spacing or size jumps)

## Key Constraints & Standards

### Immutable Rules
1. **Background color**: Must be pure white #FFFFFF, zero tolerance for tints/textures
2. **Stroke continuity**: Generate phrase as unified composition, not character assembly
3. **Reference fidelity**: Output style must reflect consensus of ALL provided reference images, weighted toward the primary pair
4. **Rounded terminals**: No sharp or pointed stroke starts/ends anywhere in the composition

### Stroke Quality Standards
1. **Pressure variation**: Visible thick-to-thin modulation (minimum 1.5:1 ratio within continuous strokes)
2. **Entry/exit tapers**: Strokes must show natural pen lift/press behavior, tapering into a rounded terminal — never a blunt cutoff or a sharp point
3. **Directional logic**: Follow biomechanically plausible writing paths (e.g., Chinese typically writes top-to-bottom, left-to-right per character)

### Compositional Balance
1. **Character sizing**: Acceptable variation range within phrase = 0.8x to 1.2x median size
2. **Baseline drift**: Vertical position variation ≤ 10% of average character height
3. **Inter-character spacing**: Should feel rhythmic, not mechanically uniform (micro-variations create natural feel)

### Reference Synthesis Rules
1. **Attribute conflict resolution**: When references disagree, defer to the two primary references (`reference-01-primary.png`, `reference-02-primary.png`); among the remaining images, majority vote breaks any further ties
2. **Minimum reference count**: 3 images required for robust style profile; 1-2 images risk overfitting to idiosyncrasies — this is why all six bundled images should be attached even though only two are "primary"
3. **Style coherence test**: If references span multiple incompatible styles (e.g., formal kaishu vs wild cursive), request user clarification on priority

### Anti-Patterns to Avoid
1. **Character-by-character assembly**: Produces visible joints where flow breaks
2. **Texture overlays**: Paper grain, canvas weave destroy pure background requirement
3. **Shadow effects**: Even subtle drop shadows violate white background constraint
4. **Mechanical uniformity**: Perfectly consistent stroke weight/spacing looks AI-generated
5. **Floating composition**: Characters should feel grounded on implied baseline (even if baseline itself drifts naturally)
6. **Sharp/pointed terminals**: Whip-like sharp tips at stroke starts or ends break the soft, rounded-pen feel — always round them off

## Example

**Input**:
- Text: "自然流畅,一气呵成"
- References: 6 bundled images in `assets/` showing flowing handwritten Chinese calligraphy styles (飘逸手写体 + 留言板风格), with `reference-01-primary.png` and `reference-02-primary.png` as the anchor style
- Background: Pure white

**Style Profile Synthesis** (from references):
- Stroke gesture: Light, flowing, accelerating mid-stroke, rounded entry/exit
- Structural rhythm: Moderate spacing, slight baseline drift
- Material: Brush-like texture with soft edges
- Balance: Horizontal expansion, center-weighted

**Generation Prompt**:
"生成中文文字'自然流畅,一气呵成',飘逸手写体风格,笔画流畅自然、一气呵成,有明显的轻重变化和笔锋,起笔落笔圆润处理,无尖锐笔锋,纯白色背景 (#FFFFFF),无阴影、无纹理,整体横向排列,字间距自然,仿佛书法家即兴挥毫的效果"

**Expected Output**:
- 8 Chinese characters in unified flowing calligraphic style
- Visible stroke weight variation (thin entries, thick mid-sections, tapered exits) with rounded, non-sharp terminals throughout
- Natural horizontal flow with subtle baseline drift
- Pure white background with zero artifacts
- Composition feels like single continuous writing session

## Advanced Techniques

### Multi-Variant Batch Generation

For projects requiring multiple text strings in consistent style:

1. **Style profile extraction**: On first successful output, document the exact style attributes achieved
2. **Template prompt structure**: Create reusable prompt template embedding those attributes
3. **Micro-variation injection**: For each new text, add small randomization descriptors ("略微奔放" slight boldness, "稍显内敛" slightly restrained) to prevent identical repetition while maintaining style family

### Style Intensity Calibration

When references show a style but user wants MORE or LESS intensity:

- **Amplification**: "夸张版的[style]" (exaggerated [style]), increase variation ranges by 1.5-2x
- **Restraint**: "克制的[style]" (restrained [style]), compress variation ranges by 0.5-0.7x
- **Formalization**: Shift from cursive toward semi-cursive or regular script structure while keeping gestural quality

Example: User loves the flow but finds it too wild → "在飘逸风格基础上增加结构稳定性,保持笔画流畅但字形更规整" (increase structural stability while maintaining stroke fluidity)

### Cross-Language Adaptation

This framework applies to non-Chinese scripts with adjustments:

- **Latin alphabets**: Replace 连笔 (continuous stroke) with cursive joining logic
- **Arabic**: Right-to-left flow, mandatory character connection rules
- **Devanagari**: Horizontal headline (shiro-rekha) must maintain consistent height

Core principle remains: Generate phrase as unified compositional unit reflecting natural handwriting biomechanics.

## Bundled Resources

```
assets/
├── reference-01-primary.png   ("与乐相伴,共赴旋律之旅" — anchor style reference)
├── reference-02-primary.png   ("漫步游荡中,期待与旋律的美好邂逅" — anchor style reference)
├── reference-03.png           ("你的音乐属性是什么呢?")
├── reference-04.png           ("写下此刻的心情,寻找同频共振的你")
├── reference-05.png           ("在这里,遇见懂你音乐的人")
└── reference-06.png           ("留下你的音乐心情,找到志同道合的同好")
```

Attach all six whenever generating; treat 01 and 02 as the tiebreaker when attributes across references disagree.
