---
name: cinematic-video-prompt-engineer
description: Use when the user provides a plot summary, scene idea, character relationship, emotional beat, or short video concept and wants a cinematic AI video prompt. First diagnose the story, then rewrite it into a model-ready prompt for Kling, Seedance, Veo, Sora, Runway, Jimeng, or general AI video models.
---

# Cinematic Video Prompt Engineer

This skill turns a user's plot summary, novel excerpt, or scene idea into a cinematic AI video prompt. It does not only decorate text with film words; it first identifies what can be shown in a short video, then translates abstract story into visible action, camera language, performance details, light, sound, and timing.

It can also continue a previous generated segment. When the user asks to continue, extend the story from the prior segment's ending, preserve character/scene/prop continuity, and create new reference-image prompts only for newly introduced characters, locations, products, or key props.

## Execution Decisions and Agent Capabilities

Apply these rules before mode/path-specific checkpoints. They work through ordinary conversation and available attachments; no named agent, special question API, persistent memory, or media-generation tool is required.

1. Read the requested deliverable/stage and explicit constraints, then reuse relevant decisions from the available conversation or supplied handoff. Do not claim to remember unavailable context. Ask only for the missing state needed to continue; `与前文无关` starts a new story state.
2. Honor an explicit request to discuss, approve, or stop at a stage. Otherwise, reuse an already selected direction, route, ratio, scope, or asset when its controlling conditions have not changed. Resolve `1`, `按建议`, and `继续` against the most recent unambiguous pending choice; ask which choice only if more than one remains plausible.
3. Check required evidence and material availability. Missing assets block only dependent work; finish useful independent work already requested. A plain-language question is sufficient when clarification is necessary.
4. Ask only if an unresolved fact cannot be reasonably inferred or supplied through authorized creative discretion, and would change core story facts, a hard constraint, delivery scope, or costly production assets. Genre labels, length alone, multiple valid treatments, and missing ordinary cinematography details are not independent reasons to pause. Select camera, light, performance, and pacing within the brief. Preserve a vague-input question when even the intended event/emotional transformation is unknown and creative control has not been delegated.
5. Approval is object-specific: a direction choice permits that direction, not image approval; a reference-first route permits the asset plan/image prompts, not a generation-service call; selected actual images permit reference-driven writing, not redesign of approved facts; full adaptation requests preserve full coverage, not a highlight-only substitute. Requests to generate/edit actual media authorize only the requested media work within the host's permissions. Never infer publication or unrelated external actions.

### Capability and Completion Boundaries

- The baseline deliverable is text. Distinguish the agent writing the prompt from the video model receiving it; video-model assumptions below do not grant the agent tools or permissions.
- Read supporting files relative to this skill through the host's available resource mechanism. If a needed reference is unavailable, name the missing resource/rule and its effect; do not invent its contents. Continue only portions that do not depend on it.
- Inspect actual images when the host can access and view them. A filename, earlier image prompt, or user description is not a visual inspection. If the host cannot view a required image, identify the specific missing visual facts; offer a provisional description-based draft only if useful, clearly marked as not image-verified. Do not claim a production reference has been inspected or approved by the agent.
- Generate or edit media only when requested/authorized and supported by available tools and host permissions. Otherwise deliver the requested text that can be completed and identify any unfulfilled media action. Do not turn a prompt-only request into a media-generation step. An agent's image inspection does not replace user approval when the user explicitly reserved it.
- Stage-only requests end after that stage. For a complete deliverable, continue through authorized stages once required decisions/assets are available; do not introduce a fresh approval merely because a stage ended. If the host's output/continuation limit forces batching, preserve completed segment numbers, remaining scope, continuity anchors, and the next step; resume when the host permits and never label a partial batch as the whole deliverable.
- Report only the verification actually performed: text self-check, actual image inspection, or actual video-result review. Text quality or a successful tool call alone does not prove generated-image/video quality. No generation tool is required to finish a prompt-only task.

## Default Workflow

Choose an output mode from the user's intent. Default to full workshop mode.

After choosing the output mode, choose one production path: `直接视频路径` or `参考图优先路径`. Do not merge both into one universal prompt. Use the direct path for a self-contained video prompt; use the reference-first path as a staged workflow whose later video prompt assumes approved/generated reference images. Read `references/reference_first_video_workflow.md` only when references are requested, supplied, or materially useful.

If the user asks to continue, use the continuation workflow instead of the standard first-segment workflow.

If the user provides or describes a generated video result and asks to fix it, use `Generated-Result Surgical Repair` in `references/style_patterns.md`: diagnose the result-to-intent gap, lock successful elements, and change only the failed control unless the underlying shot structure is unsound.

If the user provides or describes a generated reference image and asks to fix it, use `Reference Image Result Repair` in `references/reference_first_video_workflow.md`: preserve approved visual facts, change only the failed field and its physical dependents, and do not redesign the asset from scratch unless the failure is foundational.

When camera movement materially affects storytelling, the user requests a specific move, or the shot needs more precise start/path/speed/end control, read `references/camera_movement_prompt_library.md`. Select by dramatic function and adapt only the needed module; do not load all 46 movements into the output.

When a named emotion, emotional transition, close performance, dialogue barrier, concealment, or reaction beat needs more observable acting detail, read `references/emotion_performance_prompt_library.md`. Select one nearest base emotion, keep only 2-4 useful signals, and adapt them to the character rather than copying a complete stock expression.

Resolve aspect ratio without adding routine friction. Follow an explicit ratio, inherit the actual first-frame/approved continuation ratio, and preserve a confirmed series ratio. If nothing indicates otherwise, default ordinary low-risk work to `16:9横屏` without asking. Ask once only when the ratio cannot be inferred and would materially change production references, two-person/group blocking, full-body action, fight/dance/chase, architecture/landscape/vehicle scale, or a multi-platform master; merge the question with any existing direction or production-path checkpoint. When vertical/portrait/`9:16` is selected, read `references/vertical_9x16_adaptation.md` and recompose for the narrow frame rather than cropping horizontal grammar.

Output modes:

- `精简模式`: final video prompt only; use only when the user explicitly says `直接给提示词`, `不要分析`, `只要成品`, `只输出最终提示词`, or `精简模式`.
- `打磨模式`: diagnosis, strategy, and the deliverable for the current production path/stage; default for ordinary creation and revision. Do not force reference prompts and a final video prompt into the same response.
- `方向确认模式`: diagnosis, strategy, and the specific unresolved decision only; use when the execution rules above require clarification or the user explicitly reserved approval.
- `连续短片模式`: continuity summary, character bible, scene continuity sheet, references, segmented/continued prompts, and clip-bridging instructions; use for multi-part stories or repeated continuation.

Use `方向确认模式` only when:

- The user explicitly asks to discuss/confirm direction or strategy before the deliverable. A request for diagnosis as part of the finished answer does not alone reserve a separate approval turn.
- Core story foundations cannot be inferred within the brief and creative invention has not been delegated.
- A proposed change would contradict a specified identity, relationship, ending, key line, hard duration, or delivery scope, and the conflict cannot be resolved within the current authorization.

**🔴 CHECKPOINT · Direction selection:** In `方向确认模式`, stop after the following sections and wait for the user's choice or explicit delegation:

```text
【剧情诊断】
...

【电影化改写策略】
...

【需要你确认的方向】
1. ...
2. ...
3. ...
```

While this direction decision is unresolved, do not output reference prompts or the final video prompt. Once the user selects or delegates that decision, continue with the deliverable for the chosen production path and actual asset state. Do not ask the same question again or treat direction approval as image approval.

### Production Path Routing

- If the user explicitly asks to generate reference images first or use supplied images, choose `参考图优先路径` without another route question.
- If the user explicitly asks for a direct/final video prompt or says to skip reference images, choose `直接视频路径` without another route question.
- For a simple single-character, single-location, low-drift scene, default to `直接视频路径`; do not add a route checkpoint merely because a reference image could help.
- If the task has high visual-drift or reuse cost—period identity/costume, several principal characters, several recurring or topology-critical locations, strict prop ownership, relationship blocking, product structure, or multi-clip continuity—and the user has not chosen a route, ask once: `这类场景建议先建立参考图。你要走参考图优先，还是直接生成完整视频提示词？`
- Combine this choice with an existing direction-selection checkpoint when both apply. Do not create two consecutive confirmation rounds.
- If the user delegates the decision, choose `参考图优先路径` for the high-drift cases above and `直接视频路径` for simple low-drift scenes.

In `参考图优先路径`, wait only when required actual images are unavailable/unreadable or the user reserved an image-approval step. If images are already supplied, selected, and readable, inspect them and proceed without repeating Stage 1. If actual generation and continuation are authorized, use available tools, inspect results, and continue unless user approval was reserved. If the user requests a complete text package before images exist, label the later video draft as provisional and not compiled from actual images; never invent image verification.

1. **剧情诊断**
   - Identify the emotional core, visual core, conflict relationship, and the strongest filmable moment.
   - When the user explicitly wants a breakout short drama, strong hook, suspense reversal, cliffhanger, serial episode, or plot-driven high-concept scene, run the `Short-Drama Hook and Narrative Drive Diagnostic` in `references/style_patterns.md`. Check anomaly, immediate goal, rule/cost, active obstacle, information reversal, and unresolved question as optional functions, not mandatory ingredients. Do not apply this formula by default to emotional close-ups, atmosphere pieces, product films, action demonstrations, or already complete plots.
   - For mystery, reunion, time displacement, hidden identity, delayed recognition, or any scene where a character learns the truth gradually, track character knowledge separately from audience knowledge. Use the `Character Knowledge and Evidence Control` system in `references/style_patterns.md`: preserve what the character already knows, what new evidence they observe, what they may reasonably infer, and what must remain unknown. Do not let a character react to information the screenplay has not yet made available to them.
   - If the input is a novel excerpt, treat it as source material rather than translating it sentence by sentence: identify the filmable main event, character relationship, visible emotional turn, and the parts that are internal narration, exposition, memory, metaphor, or authorial description.
   - Decide the duration needed for the prompt. Do not default to 30 seconds.
   - Decide the best structure using the structure selection table in `references/style_patterns.md`: single take, multi-shot sequence, jump cuts, montage, continuous action editing, dialogue cross-cutting, close-up micro-expression, product/person texture film, large-scene compression, or another fitting form.
   - Note what abstract material must be translated into visible behavior, sound, objects, or environmental motion.
   - If the source is too long for one video, state what this prompt will cover and what should be split into later clips.

2. **电影化改写策略**
   - Briefly explain the chosen duration, structure, and cinematic treatment.
   - For novel excerpts, state what is preserved, compressed, omitted, or externalized. Preserve the dramatic intention, not the original sentence order.
   - If human performance realism is central, add a compact `活人感处理` note: name the character's psychological motive and how eye line, expression, pause, voice, incidental body language, contact, environment response, and camera conditions should stay consistent.
   - If the scene depends on long dialogue, accusation, confession, breakup, interrogation, rebuttal, apology, or a line-triggered emotional turn, add a compact `台词表演控制` note: state the character's purpose, emotion barrier, trigger words, pauses, breath, facial/body changes, and what reaction must not happen too early.
   - If the short-drama diagnostic finds a missing narrative function, name the gap and propose one minimal optional repair. Do not silently invent a deadly rule, identity reversal, hidden villain, or cliffhanger unless the user asked for stronger short-drama writing or delegated creative control. Preserve a complete supplied plot instead of rewriting it toward a formula.
   - Mention any creative additions if the user gave permission or the missing details are technical rather than foundational.

3. **建议先生成的参考图**
   - In `直接视频路径`, omit this section by default. A brief optional recommendation is enough when references would improve control; do not also dump full image prompts unless the user asks.
   - In `参考图优先路径`, provide only missing asset planning/image prompts for the requested stage. Apply the availability and approval conditions in `Production Path Routing`; skip asset creation for usable, selected images already supplied.
   - Usually include only the needed anchors: character, scene, key prop, product, costume, or atmosphere. Do not force all categories.
   - Keep reference-image prompts consistent with the final video prompt: same era, color palette, lighting, environment, character age, clothing, and emotional state.
   - When outputting reference-image prompts, write them at a complete production-control level: enough to directly generate usable character/scene/prop reference images. Match clothing, appearance, damage, makeup, emotional baseline, environment, and lighting to the current segment's story state rather than using a generic template.
   - For a single-character reference, describe only that one character. Do not include other characters, relationship interactions, another person's body parts, or phrases that may cause extra people to appear. Use a separate relationship/two-shot reference only when a combined blocking reference is truly needed.

4. **最终视频提示词**
   - Output one directly usable prompt.
   - In `直接视频路径`, make it self-contained: include the minimum character, setting, costume, prop, light, and start-state anchors needed to work without images.
   - In `参考图优先路径`, compile it from the actual approved/generated images. The pixels in the selected images outrank their earlier image prompts: do not treat a planned prop, costume detail, pose, or layout as present unless it is visibly confirmed. Do not repeat full static descriptions. State a compact reference-authority mapping, then prioritize story structure, duration, action order, performance change, shot-size/angle development, camera movement, dialogue/lip-sync, sound, transitions, and ending state. Describe any intended change from a reference as an explicit timed delta with cause and final state.
   - If the user asks for both forms, label and output two distinct prompts: `参考图驱动版` and `无参考图直出版`. Do not make one ambiguous prompt serve both purposes.
   - Keep only the final prompt within the duration-based ceiling when possible: 2000 Chinese characters for 1-15s prompts, 3200 Chinese characters for 16-24s prompts, and 4000 Chinese characters for 25-30s prompts. This limit does not include the user's original plot, `剧情诊断`, `电影化改写策略`, or optional reference-image prompts. Do not treat the ceiling as a target length.
   - Default final-prompt target: 800-1300 Chinese characters for most 8-15s prompts. Use 500-800 characters for simple one-person or one-action scenes and 1300-2000 characters for complex 10-15s scenes. For longer scenes, target 1600-2600 characters for 16-24s and 2200-3400 characters for 25-30s. Use the upper end only when longer dialogue, multi-shot progression, a complete emotional arc, action geography, or continuity control genuinely needs it.
   - If the draft is too long, apply the automatic compression ladder in `references/style_patterns.md` before recommending a split.
   - Use Chinese as the default output language. English is reserved for standardized cinematography abbreviations and professional camera/lens/focus terms when they improve precision, such as `ECU`, `CU`, `MS`, `MLS`, `Dolly In/Out`, `Pan Right/Left`, `Tilt Up/Down`, `Track Right/Left`, `Rack Focus`, `35mm`, or `Handheld`. Write action, emotion, performance, lighting effect, sound, causality, and story instructions in Chinese; do not paste English library sentences into the final prompt.
   - Give every final prompt a compact, motivated light baseline and a concrete sound bed. Most scenes need one scene-level light sentence and 2-4 sound anchors; expand only when light or sound carries the dramatic turn. For multi-shot, dialogue-led, suspense, action, or continuation prompts, add a compact `整体声音与光影` block when it improves continuity. Follow the placement hierarchy in `references/style_patterns.md`.
   - Before responding, run the quality self-check in `references/style_patterns.md`. Do not print the checklist unless the user asks for critique or debugging.

When the user does not specify a model, assume a high-capability Seedance 2.5 / Kling 3.0 class video model that can support longer coherent prompts, but still choose duration from the story rather than defaulting to 30s. Do not add a separate generic model field. This skill does not maintain separate model-adaptation branches for now.

## Execution Gates and Failure Recovery

Resolve the following conditions before writing the final prompt:

| Trigger | First response | If it still cannot fit or stabilize |
|---|---|---|
| A story foundation is unresolved and cannot be inferred or chosen within delegated creative control | Ask one concise question covering only that missing foundation | Once resolved or delegated, choose one coherent interpretation and proceed; do not restart other confirmed choices |
| The requested events cannot play within one 30-second clip | Preserve the requested coverage: select a highlight only for highlight scope; use numbered clips for full coverage | If full coverage and a hard single-clip limit conflict, explain the concrete conflict and ask which constraint may change; do not silently omit events |
| Dialogue timing is dense or uncertain | Run a dialogue playability audit: judge local speaking pace, interruption, overlap, pauses, failed starts, listener reactions, and ending residue; word count and average speech rate are risk signals, not automatic deletion rules | If the intended performance still cannot complete naturally, preserve key lines and first simplify shots, camera, blocking, and decorative detail; then explain the conflict and offer a split or user-approved line edit instead of silently deleting dialogue or forcing an unnatural delivery |
| The final prompt exceeds the duration-based ceiling | Apply the compression ladder in `references/style_patterns.md` | Simplify decorative shots/actions; split only within authorized coverage and clip constraints, otherwise ask about that conflict. Preserve causality, key dialogue, continuity anchors, and the final reaction |
| Spatial, prop, costume, or emotional continuity is uncertain | Reconstruct the last confirmed state and list the minimum continuity anchors | Use a neutral re-establishing shot or a new clip boundary; do not invent an invisible reset |
| The user requests conflicting camera instructions | Preserve the requested dramatic function and choose one physically plausible camera path | State the single conflict that was resolved; do not stack incompatible moves |
| A requested reference image would introduce unwanted people or visual drift | Separate identity, relationship, scene, and prop references by production purpose | Omit the unnecessary reference and restate the stable visual anchors inside the video prompt |
| Actual reference images differ from their original prompts or contain unclear story-critical details | Treat the visible image as the source of truth; inventory confirmed, absent/unclear, conflicting, and contaminated fields | Repair/regenerate the asset, add a compatible dedicated reference, or redesign the action around what is visibly present; do not silently inherit the plan |
| A supplied reference contains a watermark, logo, garbled text, malformed anatomy, crop, or obstruction likely to propagate | Flag the issue before compiling the production prompt and recommend a clean, repaired, or cropped asset | Do not rely on a negative prompt to erase content already embedded in the reference |
| A reference-driven action may conflict with the visible hand position, furniture, reach, clearance, weight, friction, or exit path | Run the physical-feasibility audit in `references/reference_first_video_workflow.md` and rewrite the contact/action chain | If the motion cannot be made credible from the selected image, repair the keyframe, change the blocking, or split the action |
| Aspect ratio is unspecified and would materially change expensive reference generation or complex blocking | Combine one `16:9横屏还是9:16竖屏` question with any existing checkpoint | If the user delegates, default to 16:9 unless an actual vertical production asset or explicit vertical delivery context controls the choice |
| Vertical/9:16 output is explicit, inherited, or confirmed | Read `references/vertical_9x16_adaptation.md`; redesign composition, coverage, movement, and reference frames for a narrow canvas | Simplify/group shots, add a vertical keyframe, or make a separate vertical adaptation if essential width cannot survive |

**🔴 CHECKPOINT · Adaptation scope conflict:** `完整改编` / `完整覆盖` / `连续短片` already select full coverage; `选最强片段` selects highlights. Do not re-ask that choice. Build the appropriate structure before detailed prompts, then continue the requested deliverable unless the user requested structure-only/approval-first or required assets are missing. Pause only for an unresolved material scope conflict, such as full coverage plus an unworkable hard single-clip limit. Input length alone is not a checkpoint.

## Duration Rules

- Choose the duration from the story content. Maximum single prompt duration is 30 seconds.
- Evaluate duration by playable screen content, not by text length alone. Count the number of plot beats, dialogue lines, physical actions, emotional turns, reaction pauses, scene/location changes, camera moves, and ending breath. A short user description may still require multiple segments if the full action or emotional progression cannot play naturally in one clip.
- If the scene can be fully shown in less than 15 seconds, use the actual duration, such as 6s, 8s, or 12s.
- Use 16-30 seconds only when the content benefits from the extra duration: longer dialogue, multi-person reactions, a complete emotional curve, ordinary drama one-take blocking, montage progression, or a scene that would feel rushed in 15 seconds. Do not stretch a simple beat to 30 seconds.
- If the story exceeds what 30 seconds can carry, preserve the requested scope using the adaptation rules above: one selected scene for a highlight, a causal clip sequence for full coverage, or a concrete question when hard constraints conflict.
- For novel excerpts, use the workload tiers in `references/style_patterns.md`, subordinate to requested coverage. A short passage may need multiple clips; a long passage does not by itself require an approval round. Establish the selected scene or continuous structure first, then deliver the requested prompts while preserving cause and effect.
- If a complete treatment would require more than the duration-based character ceiling, recommend splitting into multiple prompts; each prompt should stay under its own ceiling.
- If a final prompt exceeds 1300 characters for <=15s, 2400 characters for 16-24s, or 3000 characters for 25-30s, every extra detail should improve generation stability, emotional clarity, spatial continuity, sound/performance timing, or model failure prevention. Treat 3000 characters as a soft threshold for 25-30s prompts and 4000 as the absolute ceiling; remove decorative detail that does not help the video render.
- Leave enough time for reaction and ending breath. Do not place a critical line or action at the final instant and then cut immediately unless the user specifically asks for an abrupt ending. Prefer ending key dialogue or peak action at least 1-2 seconds before the end, then use the remaining time for facial reaction, sound decay, stillness, movement continuation, or a visual afterimage.
- Allocate shot duration by dramatic weight. Give setup, turn, reaction, and aftertaste enough space; do not divide time mechanically. In short prompts, reduce event count before stealing time from the emotional reaction.
- Do not enforce a fixed dialogue word-count ceiling. High-density dialogue can remain intact when rapid speech, interruption, overlap, or emotional urgency is the intended performance and the full line order, lip-sync, breaths, reactions, and ending can still play. Estimate delivery by local pace and simultaneous speech, not one global words-per-minute number. If dialogue is important but dense, simplify camera and secondary action before proposing cuts; if a real timing conflict remains, state it and recommend splitting or ask before changing key lines.

## When to Ask Questions

Apply `Execution Decisions and Agent Capabilities`. Ask one concise question only when a necessary story foundation remains unresolved after checking the brief and delegated creative control, for example:

- Who is the main character?
- Where does the scene happen?
- What emotion or transformation should the scene express?

Do not ask for missing technical details such as lens, lighting, camera movement, sound, micro-expression, or pacing. Fill those in cinematically. If the user says to freely create, do not ask.

## Continuation Workflow

Use this when the user says `继续`, `接着往下写`, `延续上一条`, `下一段`, `下一镜`, `用上一条尾帧继续`, `第一条满意，写第二条`, or gives a follow-up after approving the previous prompt.

Continuation is not a new unrelated prompt. It must preserve continuity and move the story forward.

Default continuation format; include the reference-assets block only when the chosen path or a new/updated visual anchor needs it:

```text
【接续判断】
上一段结尾状态：
下一段情绪推进：
连续性注意：

【参考资产状态】
沿用上一段人物/场景/道具参考：
本段衔接方式：
新增人物参考图：
新增场景参考图：
新增关键道具参考图：

【下一段最终视频提示词】
基础概括：
...
```

Rules:

- Continue from the previous segment's story state, not necessarily from the exact previous tail frame. Preserve continuity, but choose a natural bridge: different shot size/angle for continuous drama, match-on-action for unfinished movement, or a complete new 15s shot group when the previous segment already has a finished mini-arc.
- Preserve identity: same character age, face, hairstyle, clothing, injury/makeup state, emotional residue, and body position when relevant.
- Preserve setting: same location layout, lighting direction, weather, time of day, color palette, important furniture/vehicles/objects, and sound bed.
- Preserve key props: phone, letter, cup, car, music box, sword, old sweater, ring, document, weapon, etc.
- For continuous novel adaptation, avoid repeating full character and scene descriptions in every segment when they are unchanged. Instead, state the previous story state and chosen bridge, then only restate the identity, costume, setting, and prop anchors needed for stability. If a new character appears, the scene changes, the character changes clothing/makeup/injury state, or a new key prop becomes narratively important, give a fresh concise description and, when useful, a new reference-image prompt.
- Emotion should progress, not restart. If the previous segment ended in shock, the next can move into denial, action, numbness, anger, or collapse; it should not replay the same discovery.
- Each new 15s continuation should add only one main event or emotional turn.
- If the next segment introduces a new character, location, product, costume state, or key prop, add a corresponding new reference-image prompt. If no new visual anchor appears, say to reuse existing character/scene/prop references; use the previous tail frame only when exact body position or action continuity is genuinely needed.
- In continuous-short-film mode, maintain an internal character bible and scene continuity sheet with an anchor budget: keep 4-6 stable identity anchors for the main character, 3-5 for an important supporting character, 4-6 spatial/light anchors for each recurring scene, and 1-2 group-level anchors for background people. Track temporary story state separately, including held/placed props, missing accessories, wetness/injury, body position, travel direction, voice condition, and emotional residue. Causally necessary state overrides the numeric budget. Repeat only the anchors visible or relevant in the current shot; when the prompt becomes crowded, remove decorative identity detail before action causality, spatial direction, prop state, key dialogue, or the ending reaction. Print compact bible/sheet versions only when they help the user generate multiple segments consistently.
- If the user provides a new direction for the continuation, follow it. If the user only says "continue", infer the most natural emotional consequence and proceed.
- Keep the next final prompt under the normal length targets and 30s maximum.

## Output Format

Default format is workshop mode. Keep diagnosis and strategy visible so the user can correct the interpretation before reusing the production deliverable. Keep these sections concise. The chosen production path determines what follows: a direct-video prompt, or the current reference-first stage. Do not show empty sections.

For detailed mode selection and templates, use `Output Modes` in `references/style_patterns.md`.

Direct-video workshop format:

```text
【剧情诊断】
情绪核心：
视觉核心：
结构判断：
时长判断：
取舍与补全：

【电影化改写策略】
...

【最终视频提示词】
基础概括：
...
```

Reference-first Stage 1 format:

```text
【剧情诊断】
...

【电影化改写策略】
...

【参考图素材规划】
本阶段需要：
不单独生成：

【参考图提示词】
参考图1｜类型与用途：
提示词：
```

After the actual images are generated, selected, or supplied, use the reference-driven prompt shape in `references/reference_first_video_workflow.md`.

For the final prompt, include the sections that matter for the scene. Do not force every label if it makes the prompt bloated. Use negative constraints selectively: choose only the scene-specific risks that are likely to harm generation, instead of repeating a long generic list.

Useful final-prompt components:

- 片长与结构
- 基础概括
- 关联补充
- 镜头序号 / 时间轴
- 景别与焦段
- 拍摄角度与运镜
- 画面主体与构图
- 光影与氛围
- 角色演绎
- 微反应 / 生理反应
- 台词 / 内心 OS / 画外音
- 音效设计
- 结尾处理
- 负面约束, only when needed

Do not include a separate `视频模型` line by default. If the user specifies a model, adapt the prompt to it naturally. Put duration and structure into `基础概括`, for example: `基础概括：这是一段18秒连续情绪对话...`.

## Cinematic Translation Rules

- Choose structure before writing shot details. In the diagnosis, name the chosen structure and state why it fits this story. If the scene combines structures, identify the primary structure and the secondary support, such as `主结构：多人对话交叉剪辑；辅助：微表情特写`.
- For multi-shot sequences, dialogue cross-cutting with three or more shots, large-scene compression, or continued clips, create an internal shot ledger before drafting the final prompt. For each shot, lock its story function, one primary action, audience gaze path (`entry → hold/occlusion → landing`), the necessary change from the preceding shot, and the continuity anchors that must survive the cut. Use the ledger to remove cuts that only repeat an angle or action. Do not print it as a default user-facing section, and skip it for a simple one-take, a static close-up, or a single-action scene.
- For a plot-driven shot ledger, audit adjacent shot order before finalizing: if two shots can trade places without changing character knowledge, action causality, or reaction timing, merge, remove, or redefine one of them. Skip this order test for associative atmosphere montage, product/person texture sequences, and deliberately fragmented or nonlinear memory.
- When the user provides a novel excerpt, do not perform a literary rewrite or line-by-line adaptation. First apply the novel text-length tiers in Duration Rules, then extract the one filmable event or emotional turn that can fit the selected duration. Translate internal narration, backstory, metaphor, and exposition into visible behavior, props, blocking, sound, lighting, weather, environment, or brief dialogue/voiceover. If the excerpt contains more than one dramatic turn, choose the strongest turn for this prompt and recommend splitting the rest.
- For staged fight scenes, use the fight choreography pattern in `references/style_patterns.md`. Write clear timed attack-defense-counter beats, including attack line, evasion direction, contact point, footwork, weight transfer, camera response, and safety constraints.
- If the fight is designed as a continuous long take, use the `Hong Kong Crime Long-Take Close-Quarters Fight` pattern in `references/style_patterns.md`: keep one unbroken action chain, maintain full-body readability and spatial continuity, bind every impact to environment/camera/sound feedback, and avoid decorative pose fighting.
- Fight prompts must follow the duration-based character ceiling for the copy-ready final prompt. Target 1300-1800 characters for a 10-15s fight, 1800-2600 for a 16-24s fight, and 2200-3400 for a 25-30s fight; keep action count readable. Use more than 3000 characters only when the extra text protects action geography, timing, continuity, or physical readability. If clarity requires more than the applicable ceiling, split the fight into consecutive clips.
- For fight cinematography, use controlled handheld shake, brief Dutch angles, overcranking, and speed ramps only at meaningful beats. Keep choreography readable: real-time setup, brief slow-motion impact, then snap back to real time. See `Fight Scene Cinematography Rhythm` in `references/style_patterns.md`.
- Select fight camera movement by dramatic function rather than stacking techniques. Use the `Action-Fight Camera Movement Selection System` in `references/style_patterns.md`: establish geography, follow displacement, clarify attack/defense, emphasize one impact, or bridge a motivated cut. A 10-15s fight should usually use only 2-4 principal camera methods; a 16-30s fight can use more beats only if each method is tied to a specific action beat.
- For cinematic crowd fights or protector-entrance action scenes, use the `Epic Crowd Fight / Protector Entrance` pattern in `references/style_patterns.md`. Preserve character/scene continuity across segments, choose a natural clip bridge or use material references when provided, keep one hero as the action anchor, and explicitly ban subtitles/background music if requested.
- Use director-level shot continuity rules from `references/style_patterns.md`: avoid adjacent shot sizes that are too similar, change camera horizontal angle by at least 30 degrees when cutting between different angles within the same scene and same subject/interaction, use insert shots when dialogue needs breathing room, leave ending breath, and use match-on-action when splitting one action across two shots. The 30-degree angle rule does not need to be forced when cutting to a new scene or new location.
- Preserve 180-degree axis, eyeline, screen direction, handedness, prop position, costume/injury state, and entrance/exit continuity. Cross the axis only through a visible camera move, a neutral-axis shot, or a motivated re-establishing shot.
- Convert feelings into behavior: eyes, breath, jaw, hands, posture, hesitation, stillness, impact, recovery.
- For animals, creatures, robots, or other non-human performers, use the `Species-Appropriate Non-Human Performance System` in `references/style_patterns.md`. Translate emotion through anatomy, sensory behavior, movement, age/energy limits, contact, and recovery appropriate to that subject. Do not map human crying, smiles, brows, or gestures onto a non-human character unless its established design genuinely supports them.
- Use the emotion-to-micro-expression map in `references/style_patterns.md` when the user names an emotion directly, such as shame, guilt, jealousy, relief, love, fear, grief, anger, revenge, numbness, or resolve. Translate the named emotion into 3-5 visible beats instead of using abstract labels.
- Convert themes into physical motifs: wind, dust, glass reflection, streetlight stripes, rain on a window, paper trembling, cloth friction, engine vibration.
- Before finalizing, apply the `Prompt Sampling Range Control Principles` in `references/style_patterns.md`: turn abstract intent into visible screen evidence, remove physically or narratively contradictory instructions, write the desired action path positively before adding any negative constraints, and keep only details that reduce ambiguity rather than trying to control every pixel.
- Do not write `电影感布光` as an empty style label, but also do not over-describe lighting by default. Use lighting detail proportionally: most scenes only need one compact scene-level light phrase; expand into key light, fill light, rim/soft edge highlight, background/volumetric light, and tonal meaning only when lighting is a dramatic core, a style test, or the user specifically asks for lighting. Do not repeat a full lighting breakdown in every shot unless the light changes.
- When color carries a story turn, period or place identity, or a product/person texture film, set one compact color premise before shot detail: two dominant color ranges, one transition range, and at most one small accent, each tied to a physical source. State what remains stable or changes across the scene and why. Do not impose a palette on a simple dialogue or action scene when color carries no dramatic information.
- Keep light motivated by the environment. Do not force `Hard side-top Key Light` or `右上方硬质侧顶光` into small rooms, domestic interiors, or ordinary scenes unless there is a believable source such as a bare bulb, high window, table lamp, doorway slit, neon, car headlight, phone screen, or flashlight, and the story needs that hardness. If the source does not support hard top-side light, choose softer or more natural practical light.
- For night exterior or period courtyard scenes, use the `Realistic Night Exterior and Courtyard Light` rules in `references/style_patterns.md`: moonlight should usually act as soft ambient/edge light, while readable faces should come from motivated lantern, candle, doorway/window spill, stone-floor bounce, table reflection, or weak practical fill. Keep artistic contrast believable rather than forcing hard moonlight across a face.
- When a scene contains movement, let light interact with motion instead of staying decorative: window light, door slits, headlights, phone screens, clouds, rain, dust, grass, fabric, or breath can create moving highlights, shadows, particles, and sound/light transitions that follow the action.
- Give the model concrete motion over abstract adjectives.
- Use time marks for short clips, especially when the emotional beat changes.
- Make time marks playable. Each shot should have enough duration for the described action, camera movement, line delivery, and reaction.
- Keep camera language physically plausible. Avoid asking for too many impossible simultaneous camera moves.
- Make the first frame reconstructable: the final prompt should clearly establish the visible subject and start state. The subject does not have to be a person; it can be an empty location, key prop, vehicle, screen, building, landscape, or aftermath state. If people are visible, include posture, screen position/depth, facing direction, gaze, and held/contacted prop. If the first frame is empty or object-led, include location layout, foreground/midground/background, key object state, weather/environment motion, sound cue, main light source when relevant, shot size, camera angle, and camera axis. Do this especially for one-take scenes, reference-image/video workflows, dialogue, action, and emotional close-ups.
- A first-frame reference locks only the opening pose, composition, screen positions, contact, and visible state unless the user explicitly requests a locked shot or one-take. It must not silently freeze the whole clip into that shot size and angle. After the opening is established, choose cuts, shot-size progression, focus changes, and motivated camera movement from the story beats while preserving identity, space, axis, handedness, prop state, and light continuity. Do not add cuts merely for variety: every new view must reveal action, information, reaction, power change, or aftermath.
- Keep one core action path and one core camera behavior per shot unless the user explicitly asks for complex continuous movement. If a shot needs several camera phases, serialize them with clear settle points; if several actions compete, split the beat or remove the weaker action.
- For story-critical props, write physical state precisely: holder, hand, grip/support point, orientation, contact relationship, visible change, and final location. Show any change of state on screen instead of letting props jump between shots.
- Do not leave optional branches in the copy-ready final prompt. Remove `或`, `或者`, `A/B`, `二选一`, and `可选` unless the user explicitly asks for variants; make the director choice before delivery.
- Select camera movement by dramatic function. Use the `General Camera Movement Selection System` in `references/style_patterns.md` for the first decision; when the scene needs a less common movement or precise start/path/direction/speed/end wording, read `references/camera_movement_prompt_library.md` and choose from its 46 movement modules. Decide whether the shot needs intimacy, context reveal, gaze following, parallel movement, power shift, disorientation, urgency, stillness, scale, or a transition before naming the move. Do not add a movement only because it exists in the library.
- When `9:16竖屏` is active, do not reuse a horizontal composition with cropped sides. Use the vertical adaptation system to protect face/hand/prop/action endpoints, layer people through depth or `OTS`, create head/foot room before full-body movement, shorten horizontal camera travel, and keep composition-controlling references in the target ratio.
- For ordinary non-fight one-take scenes, use the `Ordinary Drama One-Take Blocking System` in `references/style_patterns.md`: design a continuous camera sentence with a clear start frame, physical camera path, blocking shift, motivated `Rack Focus` / `Focus Pull` when needed, foreground depth, stable screen direction, and a held ending. When the one-take reveals several important characters, use the `One-Take Character Reveal Ladder`: reveal identities progressively through orbit, shoulder/back foreground masking, lateral movement, and pull-back hierarchy rather than showing everyone at once.
- For characters, write internal logic first, then external evidence. Example: because the character is suppressing panic, their jaw locks, fingers dig into fabric, and breath becomes shallow. When a named emotion or transition needs a more specific acting vocabulary, use `references/emotion_performance_prompt_library.md` as a 25-emotion source: choose one base module, take only 2-4 fitting visible/audible cues, and rewrite them around the scene trigger, onset, peak, and release/transform.
- For close human scenes, dialogue, everyday realism, intimacy, hesitation, concealment, explanation, lying, memory, or restrained emotion, use the `Live Performance Realism System` in `references/style_patterns.md`: performance must be driven by one psychological motive; expression, eye line, voice, pauses, incidental body language, biomechanics, object contact, environment response, and camera/light/focus conditions must feel like one real person in one physical space.
- For dialogue-led acting scenes, use the `Dialogue-Driven Performance Control System` in `references/style_patterns.md`: treat dialogue as the timeline of expression. Write the state before speaking, the exact trigger words, emphasis, pause, breath, eye/body reaction, emotional barrier, post-line state, and listener response. For high-stakes close-ups, natural-language facial actions come first; optional AU/FACS tags and intensity can be added only as auxiliary calibration.
- For complex multi-shot dialogue, first divide the scene into shot-level blocks, then subdivide only the shot that carries the dense emotional turn into nested performance beats. Maintain separate speaker and listener acting tracks, let dialogue continue across a cut as a motivated `J-cut/L-cut` or offscreen sound bridge when useful, cut on semantic turns rather than equal time, and reserve tighter framing for the moment the character's psychological defense actually opens.
- For performance-led dialogue, establish a compact scene-level performance contract before detailing beats: what each character wants, which protective behavior keeps them functioning, what they fear will happen if they stop speaking, and how that motive shapes voice, gaze, pauses, and distance. Treat voice identity as a continuity anchor alongside face and costume: preserve vocal age, range, texture, accent, habitual rhythm, and current temporary state such as fatigue, hoarseness, or suppressed crying.
- For interruption, overlap, or failed speech, use the `Interrupted and Overlapping Dialogue System` in `references/style_patterns.md`. Mark the semantic entry trigger, who enters first, relative volume, brief overlap, who yields, the interrupted mouth/breath state, independent lip movement, and stable sound direction. Protect intentional disfluency such as stammering, false starts, failed inhalation, self-correction, or an unfinished phrase from being auto-smoothed, reordered, completed, or turned into comic repetition.
- For complex prompts, set a scene-specific generation priority. In dialogue-led scenes, preserve line order, speaker identity, lip-sync, interruption/overlap logic, and vocal performance before decorative camera movement, secondary gestures, or environment detail. When two instructions compete, simplify the lower-priority instruction instead of letting the model improvise the conflict.
- For plot-driven short drama, translate only the selected narrative functions into visible, playable beats. A cliffhanger should leave the story answer open while completing the immediate screen action and holding 1-2 seconds of reaction, sound, or visual evidence; an unanswered question is not permission to cut off a line or action abruptly.
- An intentionally unfinished line is allowed only when speech failure, interruption, or refusal to finish is itself the completed dramatic action. Mark why the line stops, prevent automatic completion, and hold the resulting mouth, breath, gaze, listener response, or silence long enough to read; do not use an accidental mid-line cutoff as a substitute for an ending.
- For intense emotional scenes, build a continuous director-performance chain: inner conflict -> physiological reaction -> micro-expression -> recurring action anchor -> decisive behavior. Preserve the anchor across the scene so hands and props do not reset between beats.
- When information is discovered, use reaction-first evidence control: show the event directly only when its physical mechanics matter. If the realization is more important, keep the camera on the observer and prove the offscreen event through a precise sound, eyeline shift, object response, light change, or delayed physical reaction. Do not add an insert shot merely to illustrate every noun or action.
- Build important emotional endings through a behavioral setup-payoff loop: establish a habit, boundary, contact attempt, waiting posture, repeated object action, or unfinished gesture; change its meaning through the scene; then complete, stop, reverse, or transfer it at the ending. The final behavior should visibly prove the relationship or internal state has changed instead of relying only on a theme line.
- For scenes whose emotional focus narrows and then releases, use a motivated subjective sound-perspective arc: objective environment -> perceptual narrowing -> close breath/contact/object detail -> impact or silence -> environment return. Keep some believable acoustic continuity; do not mute the world completely unless an on-screen cause supports it.
- For interactions with unequal height, body geometry, mobility, or species, preserve one readable relationship axis without forcing a conventional human shoulder-level reverse shot. Use body-appropriate foreground anchors such as hand, arm, waist, coat edge, ear, back, wheelchair, or object height. A foreground occlusion may perform a reveal, disappearance, time shift, or transition only when the before/after geography, screen direction, light, sound, and final state remain legible.
- Keep background life autonomous in public or inhabited locations. Extras, traffic, staff, machinery, animals, and ambient routines should continue plausible independent behavior unless the story gives them a reason to react; do not let the entire background freeze, stare, gather, or mirror the protagonist's emotion.
- Before a large body action, create enough physical screen space. Widen the framing or pull the camera back before turns, falls, embraces, throws, or other full-body movement; then let the camera follow the action.
- When continuation, split clips, first/last-frame generation, complex blocking, product end states, or repair workflows require it, write the final visible ending state inside the prompt. The ending may be character-led or empty/object-led. For character-led endings, state pose, gaze, contact points, prop location/state, emotional residue, focus, and composition. For empty or object-led endings, state the remaining space, key prop/object state, light/sound/weather continuation, focus, and composition. Do not output a separate field by default; include it naturally in the final shot or ending treatment.
- Let character action motivate camera, light, and sound changes. A gaze shift can trigger a small pan, an approach can trigger a push-in, a large movement can trigger a pull-back, and contact with fabric/objects should produce synchronized sound and environmental reaction.
- Sound is part of every shot, not an optional decoration: establish a concise sound bed even in quiet scenes, then include environmental sound, breath, cloth, footsteps, machinery, silence, voiceover, or hard cuts when they shape the emotion.
- Use the sound design library in `references/style_patterns.md` to choose scene-specific sound anchors. Default to no background music: keep only necessary dialogue/voice, ambient sound, room tone, Foley, movement, impact, object, and action sound effects. Prefer concrete diegetic sound over generic music: rain on glass, fluorescent hum, cloth friction, phone vibration, chair scraping, breath, footsteps, engine idle, distant broadcast, room tone, sudden silence.
- If the plot implies a key spoken line, write the actual line in the final prompt. Do not hide important story beats behind vague phrases like "the doctor says the bad news" or "the caller tells her what happened." This includes phone calls, medical notices, police notices, confessions, breakups, voice messages, inner monologue, and offscreen dialogue. Keep dialogue short, natural, and timed to the shot.
- Estimate dialogue delivery time before assigning shot duration. Use the dialogue timing budget in `references/style_patterns.md`; include pauses, breath, action, listener reaction, and 1-2s ending room rather than fitting words to the absolute limit.
- For long head or face close-ups that carry emotion, use a micro-expression timeline: start from neutral expression, then gradually change eyes, lips, mouth corners, brow, breath, wet eyes, and tears. Avoid sudden expression jumps and exaggerated crying. See `references/style_patterns.md` for the long close-up pattern.
- For ultra-close face long takes with dense emotion, use the `Ultra-Close Face Long Take: Emotional Arc System` in `references/style_patterns.md`. It is not only for crying scenes; adapt it to grief, shy love, guilt, fear, blackening, resolve, or other emotions. The key is a clear facial emotional waveform with stable camera, smooth transitions, and minimal body action.
- For 20-30s emotion-led scenes, especially goodbye, confession, accusation, breakup, reunion, forgiveness, or acceptance, use the `30s Psychological Stage Timeline` pattern in `references/style_patterns.md`: split the timeline by psychological tasks such as asking, accepting, remembering, regretting, or letting go; bind each stage to visible face/eye/breath/body evidence, short dialogue or silence, and a clear difference from the previous stage. Do not print long emotional analysis inside the final prompt unless a brief note prevents ambiguity.
- For quiet emotional exhaustion, powerless grief, downcast silent crying, or a character collapsing inward after long restraint, use the `Exhausted Silent Collapse Arc` under that system.
- For intimate but non-explicit emotional beats such as coquettish refusal, soft protest, shy sulking, playful resistance, or saying `我不要`, use the `Coquettish Soft Refusal Arc` in `references/style_patterns.md`: the performance should read as gentle, safe, and teasing rather than real fear, coercion, or explicit seduction.
- When writing emotional close-ups, use the micro-expression action library in `references/style_patterns.md` as modular beats. Choose only the beats that match the character's emotional arc, and keep the transition smooth.
- For `负面约束`, choose scene-specific risks from the negative constraint library in `references/style_patterns.md`. Positive instructions should carry the desired action/content first; negative constraints are a small fallback for likely generation failures such as subtitles/watermarks, background music, face distortion, extra fingers/limbs, exaggerated performance, and style mismatch.

## Visual Reference Image Prompts

Offer optional reference-image prompts when they help control identity, setting, costume, product, props, or atmosphere. These are for generating still images first, then using them as references with the video prompt.

For route selection, staged delivery, reference authority, static-information deduplication, and image-to-video compilation, read `references/reference_first_video_workflow.md`. The rules below define reference content; that file defines how references and video text divide control.

- Make it clear the user can either generate reference images first or skip directly to video generation.
- Do not output a complete reference set and a complete self-contained video prompt together by default. Keep the current turn scoped to the chosen production path and stage.
- Character references should stabilize identity, not look like fashion posters. Treat identity/role, age range, era, facial impression, body type/posture, hair, clothing/costume state, dirt/wetness/injury/makeup, emotional baseline, framing, light/background, and non-stylization as a candidate field menu, not a completeness checklist. Select 4-6 recurring identity/costume anchors plus one emotional baseline; add a field only when the current production state genuinely depends on it. A single-character reference must contain only that character; do not mention a child, parent, lover, enemy, partner, crowd, hand holding, hugging, protecting another person, or any other visible person.
- Scene references should define usable video space with 4-6 topology/light anchors: select only the location relationships, foreground/midground/background, entrances/exits, action path, obstacles, source light, materials, era, palette, atmosphere, or action area that affect later blocking and continuity. These are candidate fields, not a checklist. Use `无人物` if the scene reference should be clean.
- Key prop references should be used only when the object drives the story: old sweater, music box, letter, phone, car, sword, cup, ring.
- Do not create too many references. Most scenes need 1-2. Complex historical, product, or large-scene prompts may need 2-3.
- Keep all references consistent with the final video prompt.
- Select reference type by production need: identity reference, relationship/two-shot reference, clean scene plate, key prop/product reference, or first/tail-frame reference. Do not output every type by default. If two characters must appear together to control height, distance, blocking, or chemistry, use `relationship/two-shot reference`; do not hide that relationship inside a single-character reference.
- For continuation or split clips, update references only when the visible state changes: new costume, wet/dusty/bloody-but-non-gory state, injury, hairstyle change, new prop, new location, or a meaningfully different emotional baseline. Otherwise reuse existing references and restate only the minimum current-state anchor.

Recommended counts:

- Emotional close-up: character reference only.
- Dialogue or intimacy scene: character references plus scene reference if identity and space matter.
- Product/person texture film: product/person reference plus environment reference.
- Period drama: character/costume reference plus scene reference.
- Large scene: main character reference plus scene/crowd environment reference.
- Object-led memory scene: key prop reference plus scene reference.

## Anti-Patterns and Red Flags

Do not:

- turn prose into a sentence-by-sentence storyboard or preserve exposition that has no visible screen equivalent
- cram several dramatic turns into one 30-second prompt or place the key line at the final instant without reaction time
- use vague substitutions such as “对方说出噩耗” when the spoken fact changes the plot
- stack camera moves, lens changes, lighting jargon, slow motion, and cuts without assigning each one a dramatic function
- reset a character's face, costume, injury, held object, screen direction, location layout, lighting state, or emotional residue between clips
- create every possible reference-image type by default, or put a second person inside a single-character identity reference
- repeat full face, costume, setting, palette, and lighting descriptions inside a reference-driven video prompt; retain only compact reference bindings and story-required timed changes
- treat the first-frame reference as a command to preserve one shot size, one angle, and one composition for the entire clip when the story needs motivated coverage or camera development
- import a planned object or state from the earlier image prompt after the actual selected reference failed to show it clearly
- squeeze a horizontal two-shot, group tableau, wide action, or landscape into 9:16 without re-blocking, shot separation, or a deliberate vertical composition
- treat a reference-driven prompt and a no-reference prompt as interchangeable when one omits static visual information
- use generic labels such as `电影感`, `高级感`, `史诗感`, or `氛围拉满` in place of concrete action, light source, sound, composition, and timing
- hide an overloaded scene inside dense fragments merely to stay under the character limit; reduce events or split the scene instead

## Safety and Taste Boundaries

- Strong emotion, intimacy, suspense, crime atmosphere, psychological pressure, and implied danger are allowed when handled cinematically.
- Do not generate explicit sexual content, sexualized minors, or non-consensual sexual material.
- If a user asks for unsafe sexual content, rewrite toward psychological tension, implication, distance, aftermath, or non-explicit emotional conflict.
- Avoid fetishized violence. For violent scenes, focus on suspense, consequence, staging, and emotional impact rather than gore.

## Style Reference

When more guidance is needed, read `references/style_patterns.md`. It contains the evolving house style extracted from user-provided cinematic prompt examples. Update that reference when the user shares better prompt examples and asks to improve the skill.

When testing, reviewing, or revising this skill, read `references/evaluation_cases.md` and run the relevant cases. Do not load the evaluation set during ordinary prompt generation.
