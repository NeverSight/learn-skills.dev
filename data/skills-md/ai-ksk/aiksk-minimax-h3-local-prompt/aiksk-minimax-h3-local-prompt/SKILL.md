---
name: aiksk-minimax-h3-local-prompt
version: "1.7.2-2026.08.30"
description: "AIKSK MiniMax H3 full-domain prompt compiler with AIMixer Director production rules. Covers Base T2VA/I2VA/FL2VA/L2VA and Full-reference Ref2VA, Director r2v/v2v/rv2v material mapping, Subject/Picture semantics, causal multi-shot transitions, identity/product/audio locks, camera/timing/dialogue, prompt repair, and reusable creative production recipes. MiniMax official grammar is always the hard source of truth; AIKSK rules are production heuristics layered on top."
compatibility: "Claude/Codex/agent harnesses that can read SKILL.md and local references; local ComfyUI/RunningHub/AIMixer Director workflows when their actual material mapping is known."
---

# AIKSK MiniMax H3 全域提示词规范 v1.7 — Director Production

## 0. Governing principle

This skill compiles creator intent into H3-ready production prompts.

Always obey this precedence:

**Official MiniMax grammar → actual asset truth / Director mapping → user hard constraints → AIKSK production enhancement.**

If any AIKSK heuristic conflicts with the current official H3 guides, the official guide wins.

Never describe an AIKSK heuristic as an official MiniMax requirement.

---

# Layer 0 — Mandatory mode routing

## 0.1 Base family

Use `references/official/base-en.txt` for:

- `T2VA` — text only
- `I2VA` — first frame + text
- `FL2VA` — first + last frame + text
- `L2VA` — last frame + text

Director mapping:

- `t2v` → T2VA
- `i2v` → I2VA
- `fl2v` with no images → T2VA
- `fl2v` with first only → I2VA
- `fl2v` with last only → L2VA
- `fl2v` with both → FL2VA

### Base hard structure

T2VA begins directly with:

1. `integrated_multimodal_description:`
2. `overall_soundscape:`
3. `non_diegetic_music:`

I2VA first line must be:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
```

FL2VA first line must follow the official form:

```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video.
```

L2VA first line must follow the official form:

```text
How the reference pictures align with the target video — <Picture 1> (from [Shot N]) aligns with the S.SS-second mark of the target video.
```

Do not rename the three core fields.

## 0.2 Full-reference family

Use `references/official/ref-en.txt` for:

- Ref2VA
- Director `r2v`
- Director `v2v`
- Director `rv2v`

### Ref2VA hard section order

1. `subject_definitions:`
2. `summary:`
3. `retention_analysis:`
4. `detailed_description:`
5. `overall_soundscape:`
6. `non_diegetic_music:`

Do not reorder or rename these sections.
Do not introduce new reference labels after `subject_definitions`.

---

# Layer 1 — The Director mental model

Read `references/director/AIMIXER_DIRECTOR_RULES.md` whenever AIMixer Director is involved.

## 1.1 File label vs semantic identity

Director material slots directly map to:

- `<Picture N>` — uploaded image
- `<Video N>` — uploaded/source video
- `<Audio N>` — uploaded/extracted audio signal

Prefer the Director `@` picker to obtain actual indices.

`<Subject N>` is not an upload slot. It is a reusable semantic identity defined by the prompt.

Use the plain-language rule:

**Picture = which file/frame. Subject = who/what this reusable thing is.**

## 1.2 When to create a Subject

Create `<Subject N>` only for visible content that must be tracked/reused:

- person/character;
- animal/creature;
- product/prop;
- reusable environment;
- style/action/pose only when it must be tracked as a reusable content unit.

The same subject may be established by multiple references:

```text
<Subject 1> is the same woman whose identity and appearance are established by <Picture 1>, <Picture 2>, and <Picture 3>.
```

Do not create a different Subject for the same recurring character merely because a different Picture shows it.

## 1.3 When a Picture remains a standalone tracked label

Keep `<Picture N>` as an independently defined item when the image itself is:

- a first frame;
- last frame;
- keyframe;
- edited keyframe;
- composition anchor;
- storyboard/shot-planning anchor.

If an image only supplies character/costume/prop/style identity, cite the image inside the appropriate Subject definition instead of forcing a redundant standalone Picture line.

---

# Layer 2 — Creator-intent compiler

For every non-trivial task, reason in this order.

## STEP 1 — Immutable constraints

Extract:

- who/what must remain the same;
- exact wardrobe/appearance/product geometry;
- beginning and ending state;
- required scene(s);
- duration;
- requested action;
- exact dialogue/lyrics/visible text;
- audio role;
- forbidden changes.

## STEP 2 — Asset map

For every input, classify its actual role:

- identity reference;
- first/last/keyframe;
- composition/storyboard anchor;
- environment/style reference;
- motion/camera reference;
- source video for edit;
- source video for continuation;
- voice/music/audio reference;
- audio signal reuse.

Never infer role only from file type.

## STEP 3 — Subject graph

Group multiple assets that depict the same reusable content into one Subject where appropriate.

Example:

```text
Picture 1 + Picture 2 + Picture 3
        ↓
<Subject 1> = same heroine
<Subject 2> = same crowned boar
```

## STEP 4 — Story beats

Translate the request into observable beats, not plot-summary verbs.

Bad:

`She is chased and later rides the boar.`

Better:

`she runs → looks back → reaches toward the chain → closes her grip → steps into the boar's momentum → swings onto its back`

## STEP 5 — Causal bridges

For multi-shot stories, the end of each shot must create the next shot's opening state.

Use at least one continuity carrier:

- body movement;
- gaze;
- prop contact;
- momentum/direction;
- sound cue;
- camera direction;
- visible state change.

Example:

`pet → snort/lean forward → cut → chase already moving`

`run → reach for chain → cut → grip completes → mount`

This is the default AIKSK Director heuristic.

## STEP 6 — Timing

Allocate duration by information load, not by equal division.

- `[Shot 1]` has no timestamp.
- `[Shot 2+]` use strictly increasing cut times.
- Timestamps must fit the effective workflow duration.
- If ComfyUI/Director snaps the requested duration to a valid H3 frame grid, use the effective duration for final alignment rather than blindly writing the user's nominal value.

## STEP 7 — Camera/audio layer

For each shot specify only useful information:

- composition;
- subject position;
- action/state change;
- one dominant camera behavior;
- diegetic sound;
- dialogue if any;
- active reference relation;
- transition carrier.

## STEP 8 — Compile into official grammar

Only now write the final Base or Ref2VA structure.

---

# Layer 3 — Ref2VA official semantics

## 3.1 Reference label roles

- `<Subject N>` — reusable visible content abstracted from one or more assets.
- `<Picture N>` — concrete image/frame/planning anchor.
- `<Video N>` — source edit/continuation/whole-video temporal structure.
- `<Audio N>` — copied or referenced audio signal.

Once defined, each label keeps the same meaning everywhere.

## 3.2 summary task types

Use only official task types justified by actual roles:

- `keyframe completion`
- `reference generation`
- `video editing`
- `video continuation`
- `audio reuse`
- `audio reference`

Combine with ` + ` when needed.

Do not call a motion-reference video `video editing` unless the target directly edits that video.

For actual video editing, begin after the task prefix with:

```text
The target video is an edited version of <Video 1>.
```

## 3.3 retention_analysis markers

Visible references:

- `fully_preserved`
- `partially_preserved`
- `attribute_transfer`
- `weak_reference`

Audio references:

- `fully_copy`
- `partially_copy`
- `reference`
- `weak_reference`

Use markers according to the role defined in `subject_definitions`, not according to whether the target story adds new content.

## 3.4 Full-reference detailed_description

- structural prose is English;
- preserve original language only for dialogue, lyrics, and visible text;
- establish overall style in one or two English sentences **before `[Shot 1]`**;
- then describe shots in playback order;
- cite reference labels where their roles become active;
- generation tasks normally target approximately **350–500 English words**;
- dialogue-dense tasks prioritize fitting the complete spoken timeline over word-count targets.

---

# Layer 4 — Base prompt rules

## 4.1 Style placement

In Base modes, establish style and initial composition at the beginning of `[Shot 1]`.

## 4.2 Shots/cuts

- `[Shot 1]` has no timestamp.
- Later shots begin with a strictly increasing time such as `At 00:03.500, ...`.
- A cut should reveal genuinely new subject/space/state/viewpoint/time information.
- If only framing shifts slightly, prefer camera motion.

## 4.3 FL2VA path logic

Do not merely describe first and last images as static states.

Compile:

`first-frame state → observable intermediate changes → narrowing difference → final-frame landing`

FL2VA usually benefits from a continuous path and should not add unnecessary cuts.

---

# Layer 5 — Camera and action grammar

## 5.1 Camera

Use natural motion expressions rather than tag piles.

Choose one dominant move per short beat when possible:

- Static Shot
- Push In / Pull Out
- Zoom In / Zoom Out
- Pan Left / Pan Right
- Truck Left / Truck Right
- Tilt Up / Tilt Down
- Pedestal Up / Down
- Arc Shot
- Tracking Shot
- Shake Slightly / Strongly
- POV
- Roll Clockwise / Counterclockwise

Add amplitude/speed only when meaningful.

## 5.2 Action

Use:

`initial state → trigger → physical action → intermediate state → final state`

For contact/action choreography, name direction, contact, reaction, and endpoint.

---

# Layer 6 — Dialogue, text, and audio

## 6.1 Speakers

- actual vocal sources use stable `(S1)`, `(S2)` IDs;
- same speaker keeps the same ID across shots;
- non-vocal characters get no speaker ID;
- multiple numbered speakers speaking together may use `(S1,S2)`.

## 6.2 Dialogue

Use:

```text
The woman (S1) says: <d>[Chinese] 原台词。</d>
```

Inside `<d>` keep only the language tag and the actual spoken content. Preserve the user's words unless rewrite is requested.

For off-screen voiceover use the official phrase `says in an off-screen voiceover` and keep the corresponding on-screen lips closed when applicable.

## 6.3 Visible text

Visible signs/labels/subtitles use English double quotation marks while preserving original text exactly.

## 6.4 Sound layers

Keep separate:

1. dialogue/singing;
2. diegetic ambience;
3. physical sound effects;
4. non-diegetic music.

`overall_soundscape` summarizes ambience, action sounds, and non-verbal human/creature sounds; do not repeat dialogue.

`non_diegetic_music` is score audible to the audience but not the characters. Use `N/A` when absent.

---

# Layer 7 — Director common prompt policy

AIMixer common prompt is concatenated with each material-group prompt.

## 7.1 Safe default

For general creators and Codex automation:

**common prompt OFF/empty + complete official prompt per group.**

This is the default because it is easiest to audit and least likely to break section ordering.

## 7.2 Advanced shared-definition mode

If common prompt is necessary, it may begin `subject_definitions:` and contain shared Subject definitions.

The group prompt must continue that same section with any group-only definitions, then proceed to `summary:`. Do not write a second `subject_definitions:` header.

---

# Layer 8 — Runtime facts

Current official H3 boundaries validated 2026-08-29:

- output duration: 4–15 seconds;
- output frame rate: 24 FPS;
- output audio: stereo 32 kHz;
- base generation shorter side defaults to 768 px; 2K is associated with H3-Regenerate-2K;
- Ref2VA Images ≤ 9;
- Ref2VA Videos ≤ 3, each 2–15 seconds, total video duration ≤ 15 seconds;
- Ref2VA Audio ≤ 3, each 2–15 seconds, total audio duration ≤ 15 seconds;
- total mixed files ≤ 12;
- official H3-Context-IR is hosted preprocessing/orchestration and is not identical to this local prompt skill.

Do not invent a universal 10-second limit.

---

# Layer 9 — Production locks

Use only locks that matter:

- identity/face/hair/body silhouette;
- wardrobe/accessory;
- product geometry/material/logo/text;
- environment/composition;
- motion direction/camera axis;
- lighting;
- voice timbre;
- exact dialogue;
- source audio reuse.

State what may change separately from what may not change.

---

# Layer 10 — Failure repair

## Identity drift

- consolidate the same character under one `<Subject N>`;
- cite all relevant identity source Pictures inside that Subject definition;
- remove unnecessary style transformations;
- repeat the Subject label at important appearances without redefining it.

## Three-image slideshow feeling

Cause: references were treated as three disconnected scenes.

Repair:

- create recurring Subjects;
- assign each Picture a story/planning role;
- add causal bridges across cuts;
- continue motion/contact/sound across transitions.

## Action too weak

Replace abstract intention with physical transitions and endpoints.

## Camera chaos

Use one dominant move per shot; eliminate ornamental camera stacking.

## Dialogue rush/cutoff

Reduce visual complexity during speech; place cuts at natural pauses; preserve exact text unless permission to rewrite is given.

## Product deformation

Promote geometry/material/logo/text to hard continuity constraints and reduce transformations touching the product.

---

# Layer 11 — Output profiles

These are AIKSK profiles, not MiniMax modes.

- `official_full` — default final production; exact grammar + rich detail.
- `official_compact` — exact grammar + less redundancy.
- `director` — stronger blocking, causal transitions, camera and sound.
- `identity_lock` — stronger identity/wardrobe/product continuity.
- `edit_lock` — Ref2VA source edit with minimal unintended changes.
- `motion_reference` — transfer body/camera/rhythm without accidental identity/environment copying.
- `audio_control` — voice/music/sound relationship priority.
- `creative_max` — creative enrichment within user constraints.

---

# Layer 12 — Workflow awareness

When actual ComfyUI/RunningHub/Director mapping exists, inspect it before assigning label numbers.

When no mapping exists, require or establish a manifest:

```text
Picture 1 = ...
Picture 2 = ...
Video 1 = ...
Audio 1 = ...
```

For Director use `@` picker mappings when available.

Never infer custom-node reordering from filenames alone.

---

# Layer 13 — Final QA checklist

Before returning a prompt, verify:

1. correct Base vs Ref2VA family;
2. exact official section/field names;
3. actual asset numbering is respected;
4. Subject and Picture semantics are not confused;
5. same recurring identity keeps one Subject ID;
6. no new labels after `subject_definitions`;
7. summary task type is official and role-correct;
8. retention markers are official and role-correct;
9. `[Shot 1]` has no cut timestamp;
10. later timestamps strictly increase and fit effective duration;
11. multi-shot narrative has causal bridges;
12. camera is not overloaded;
13. dialogue uses stable `(Sx)` and `<d>[Language]`;
14. soundscape does not duplicate dialogue;
15. audience-only score is separated from diegetic sound;
16. Ref2VA generation detail is sufficiently explicit, normally around 350–500 English words;
17. every claim respects the Layer 15 evidence tiers — no AIKSK heuristic and
    no Director behavior is labeled as MiniMax official.

---

# Layer 14 — Response modes

Match the delivery shape to what was actually asked.

## User asks only for a prompt

Return only the final copyable prompt in the correct official structure. No commentary, no analysis scaffolding.

## User asks for workflow / production output

Return:

```text
Family:
Director task:
Profile:
Duration:
Asset map:
Reference map:
Locks:
Final prompt:
Validation / risks:
```

## User asks for multiple variants

Default variants:

1. `official_full`
2. `official_compact`
3. one task-specific profile (`director`, `identity_lock`, `edit_lock`, `motion_reference`, or `audio_control`)

Do not generate meaningless stylistic variants that differ only by adjectives.

---

# Layer 15 — Evidence boundaries

Every claim in a reply must be traceable to one of these tiers. When tiers
disagree, the earlier tier wins. Never promote a lower tier to a higher one.

## 15.1 MiniMax official — grammar and runtime

May be stated as official when the bundled guides support them:

- the Base and Full-reference prompt-mode structures;
- Base three core fields, and their order;
- Ref2VA six-section order;
- the four reference label types and their semantics;
- official `summary` task types;
- official visual and audio retention markers;
- speaker IDs and `<d>[Language] ...</d>` dialogue formatting;
- shot/cut notation and timestamp rules;
- camera-motion guidance;
- that an identity/costume/style-only image belongs inside a Subject, and that
  a standalone Picture is for frame, composition-anchor or storyboard roles;
- H3 runtime specs: 4–15s output, 24 FPS, stereo 32 kHz, and the Ref2VA input
  limits recorded in the source register.

## 15.2 ComfyUI official — node behavior

- native H3 node families and the workflows they support;
- frame-grid behavior, which is why prompt timestamps follow the effective
  workflow duration rather than the requested duration.

## 15.3 AIMixer Director official — mapping only

Official **to the Director project**, not to MiniMax:

- the six Director tasks;
- `t2v`/`i2v`/`fl2v` → `fl2va`, `r2v`/`v2v`/`rv2v` → `ref2va`;
- R2V material tags and the `@` picker;
- common-prompt concatenation onto each group prompt;
- automatic `<Video 1>` binding of the v2v/rv2v source segment.

State these as Director behavior, never as MiniMax grammar. They describe one
custom node set and can change with its version, so defer to the actual
installed workflow whenever it is visible.

## 15.4 AIKSK production heuristics

Usable, but must be labeled internally as heuristics:

- causal bridges across cuts;
- output profiles;
- the lock hierarchy;
- the operational Subject-vs-Picture decision procedure built on top of 15.1;
- multi-reference conflict priority;
- story/use-case routers and playbooks;
- failure-repair recipes;
- dialogue-density splitting;
- response-mode shaping in Layer 14.

## 15.5 Never claim

- that this skill reproduces official H3-Context-IR exactly;
- that local prompt rewriting equals H3-Regenerate-2K;
- that an AIKSK heuristic or a Director behavior is a MiniMax official
  requirement;
- that a community LoRA or third-party custom node is an official MiniMax
  feature;
- that unseen source media contains any specific detail.

---

# Layer 16 — Supporting files

- Official syntax: `references/official/base-en.txt`, `references/official/ref-en.txt`
- Director rules: `references/director/AIMIXER_DIRECTOR_RULES.md`
- Plain-language logic: `references/director/DIRECTOR_PROMPT_LOGIC_ZH.md`
- Use-case router: `references/playbooks/use-case-catalog.md`
- Camera/action recipes: `references/playbooks/camera-action-recipes.md`
- Dialogue/audio recipes: `references/playbooks/dialogue-audio-recipes.md`
- Ref2VA recipes: `references/playbooks/ref2va-reference-recipes.md`
- Failure repair: `references/playbooks/failure-repair-matrix.md`
- Director R2V template: `templates/director_r2v_master.txt`
- 10-second three-image example: `examples/director_r2v_10s_three_image_story.txt`
- Source validation: `references/CROSS_VALIDATION.md`, `references/SOURCE_REGISTER.md`

---

# Layer 17 — Trigger phrases

Use this skill when the request mentions or implies:

- MiniMax H3 prompt / 提示词 / Prompt;
- T2VA / I2VA / FL2VA / L2VA / Ref2VA;
- Director / 导演台 / AIMixer / ComfyUI_MiniMaxH3_Director;
- `t2v` / `i2v` / `fl2v` / `r2v` / `v2v` / `rv2v` / 分组 / 公共提示词;
- 文生视频 / 图生视频 / 首尾帧 / 尾帧 / 参考生视频;
- 参考图 / 参考视频 / 参考音频 / 声音参考 / 素材编号 / Subject 定义;
- 视频编辑 / 续写 / 人物一致性 / 动作参考;
- 镜头设计 / 运镜 / 分镜 / 转场 / 因果衔接 / 音效 / 对白 / 歌词 / MV;
- 产品广告 / 品牌片 / 3D 动画 / 游戏开场 / 纸艺 / 拼贴;
- AI 短剧 / 数字人 / 双人对话 / 打斗 / 变身 / 舞蹈;
- H3 Prompt 修复 / 重写 / 压缩 / 扩写 / 诊断 / 幻灯片感。
