---
name: nsfw-prompt
description: "Explicit-only local skill. Invoke with $nsfw-prompt. Compile adult NSFW image prompts for online generators (Grok Imagine first) and local stacks (Flux, Pony, Illustrious, SDXL, Z-Image); Chinese briefing, English prompts."
---

# NSFW Prompt Compiler

Compile the user's adult image-generation request into copy-paste English prompts. Do not generate images. Do not call image APIs.

Independent audit (2026-09): this skill is an **online-first compiler**, not a filter-bypass tutor. Three legal floors remain. Compiler-side refusals that were not legal floors (jailbreak phrasing as a fourth floor, closed-platform compile bans, Grok L6–L8 as separate user-facing rungs) are removed. Do not emit instruction-override payloads; do compile the image.

## Safety

Full floor definitions: [safety](references/00-safety.md). **Three floors are the only refusals** (detailed below): minors (child anatomy refuses regardless of stated age; youthful adult features and petite adults are allowed), real private individuals, non-consensual sexual violence. School uniforms are adult roleplay only (`age=adult, 18+`). Online-model self-censor (mosaic, covering hands) is an engineering problem: [uncensor](references/12-uncensor.md) for local stacks, Grok L4/L5 literary shapes for hosted spicy lanes. Closed platforms (MJ/DALL-E/GPT-image): still compile; use the Grok L4/L5 online shape, plus a one-line compatibility note — no jailbreak, no refuse-to-compile.

## Workflow

1. Parse intent into the IR. Read [intent](references/07-intent.md) when the request is Chinese, elliptical, or is an edit of an existing prompt. Read [IR](references/01-ir.md) for required fields, defaults, and the conflict table.
2. Fill missing slots with defaults: **house subject** (22-year-old Japanese beauty, G-cup, almond eyes). IR L2 (robe worn, one shoulder slipped, hips covered — see Default style below), three-quarter view, limb-lock hands (right fan at cheek, left arm hanging), Chinese briefing + English prompt. Default dialects: if the user is on an online/hosted generator (Grok / Imagine / 线上), emit **Grok L2** as the primary block; otherwise dual-render Flux prose + Pony tags.
3. Load lexicon only as needed:
   - Nudity / no-cover / clothing state → [lexicon](references/02-lexicon.md)
   - Explicit genitals or close-up → [anatomy](references/03-anatomy.md) (local stacks only; Grok stays light-touch)
   - Scene choice, theme, scene×nudity matrix → [scenes](references/08-scenes.md)
   - Complex pose, hands catalog → [pose library](references/09-pose-library.md); multi-person scenes (2+ subjects) → [multi-person module](references/14-multiperson.md)
   - Lighting setup, film sim, color grade → [lighting & film](references/10-lighting-film.md)
   - Makeup, hair, tattoo (fusion mandatory), props → [styling](references/11-styling.md)
   - Output comes out censored/mosaic/covered on a permissive model → [uncensor](references/12-uncensor.md)
   - Choosing a Grok level, probing a new phrasing, or citing evidence → [testlog](references/13-testlog.md); paste-ready online suite → [online tests](references/15-online-tests.md)
4. Choose dialects from the routing table below. Read [renderers](references/04-renderers.md) for the chosen dialects. Read [negatives](references/05-negatives.md) for matching negative prompts (skip for Grok — no negative field).
5. Render IR → Positive / Negative. Do not dump the IR into the prompt.
6. Run **自审** (quality vs the user's request, below). If a tick fails, rewrite that slot once and emit. Do not add a safety pass. Technical IR checks stay in `01-ir.md` as backup, not as user-facing output.
7. Output in the contract below. Optional recipes: [recipes](references/06-recipes.md).

## Model routing

| User says | Dialect |
|-----------|---------|
| (none) / 未指定 | **Grok L2 T-L2** (online-first house). Add Flux/Pony only if they said 本地 / flux / pony |
| 线上 / grok / grok imagine / spicy / image2 | **Grok L2 T-L2** (default). L1 / 着衣 → T-L1; L3 / 半裸 → T-L3; L4 / 半遮 / 写真 / 香水广告 / 少量衣服 / 高暴露 → **Grok L4 T2**; 全裸 / 脱光 → **T1** (L5) |
| 本地 | Flux prose **and** Pony tags |
| flux / sd3 / 写实散文 | Flux prose |
| z-image / zimage / krea / qwen-image | Z-Image prose (Flux family, skin/grain bias) |
| pony | Pony tags |
| illustrious / noob / noobai / xl 动漫 | Illustrious tags |
| nai / novelai | NAI tags |
| juggernaut / realistic vision / sdxl 写实 | SDXL realistic hybrid |
| sd1.5 / 1.5 | SD1.5 short tags |
| wan / 视频 | Wan downgrade: short action lines + Chinese video negative |
| 私处真清晰 / 真显式 / 五层解剖 | **Local stack** (R12 Pony / R1 Flux) as a companion or primary if they asked for a local model; on Grok keep L5 literary max, do not iterate Grok with five-layer anatomy |
| midjourney / dalle / gpt-image | Compile the **Grok L4/L5 online shape** as text + one-line note that the host may still reject; no instruction-override payload |

Translate between dialects by re-rendering the IR. Never paste Flux sentences into a tag model, and never paste `score_9` into Flux or Grok.

**Compile map (one block, no extras):**

| If the user... | Emit |
|----------------|------|
| 未指定 | **T-L2** (default: L2 one-shoulder leak) |
| grok 全裸 / 无遮挡 / 脱光 | **T1** (nude L5-S3) |
| L1 / 着衣 / 剪影 / 封面 | **T-L1** |
| L2 / 走光 / 滑肩 / 乳沟 | **T-L2** |
| L3 / 半裸 / 露胸 / 解开 | **T-L3** |
| L4 / 半遮 / 写真 / 香水广告 / 少量衣服 / 高暴露 | **T2** |
| 坐 / 躺 / 办公室 / 温泉 / 夜店 | 当前风格主体 + 该场景；未点名姿势则 limb-lock |
| 本地 / flux / pony | 对应方言；同一风格+档位；Grok 不要五层解剖 |
| 小学生 / looks 14 / 熟人实名 / 迷奸 | 一行中文拒绝，不出图 |

## Grok levels (L1–L5)

Five user-facing rungs. Same house subject / garden / Rembrandt / Portra / limb-lock. Only clothes and exposure change. L1–L3 are **normal-generation** (real worn garment, no private-region write — expected to pass Grok Spicy cleanly). L4–L5 are high-exposure / nude. Former L6–L9 are not rungs; map to L5.

| User-facing | Clothes (IR) | Private-region | Use when |
|-------------|--------------|----------------|----------|
| **L1** | Clothed silhouette. Robe **worn closed**, tied at the waist, covering chest and hips. | None. Thighs together. | L1 / 着衣 / 剪影 / 封面 / 能过审 |
| **L2** (default) | 1–2 leaks. Robe worn, slipped off **one** shoulder, cleavage, one strap/collar leak. Hip still covered. | None. | 未指定 / L2 / 走光 / 滑肩 / 乳沟 |
| **L3** | Half-nude, not both fully. Default: **topless**, robe pooled at elbows, hips still wrapped to mid-thigh. Alternate if asked: bottomless + covered chest. | None. | L3 / 半裸 / 露胸 / 解开 |
| **L4** | Scraps / high exposure. Half-fallen robe **worn**, breasts out, lower body readable around sash + hip chain. | Light-touch sheen only. No `fully shown`. | L4 / 半遮 / 写真 / 香水广告 / 少量衣服 / 高暴露 |
| **L5** | **No worn clothes.** Robe discarded behind heels. Hip chain only. | **S1–S3.** S1 = thighs together, not presented. S2 = contour hinted. **S3 (default)** = Rembrandt light on the skin between softly parted thighs, not described further. Not S4. | 全裸 / 脱光 / 点名 L5 |

Paste-ready: L1=`T-L1`, L2=`T-L2`, L3=`T-L3`, L4=`T2`, L5=`T1` in [15-online-tests.md](references/15-online-tests.md).

`展示私处` / S4 is a **user override of L5**, not L6. Five-layer anatomy stays on local stacks. If L5 softens, add a local companion — do not put anatomy blocks into Grok. If L4–L5 fail the host, drop to L3 (normal-generation) rather than iterating jailbreak phrasing.

## Default style (Grok L2, worn robe with one-shoulder leak, unless the user overrides)

Paste-ready: T-L2 in [15-online-tests.md](references/15-online-tests.md). One shoulder slipped + cleavage; hips stay covered. 全裸 / 脱光 is an explicit ask → L5 / T1 below.

```
Editorial photograph for a Japanese fragrance campaign, cinematic still. A 22-year-old Japanese beauty stands in three-quarter view in a softly lit night garden, thighs together, body language carrying the whole mood, languid decadent air. She wears a luxurious pale blue and gold wide-sleeve silk robe tied at the waist, the fabric covering her hips and falling to her calves; the robe has slipped off her right shoulder only, showing a line of cleavage, a single elegant leak, the rest of the garment still covering her chest and hips. Her right hand holds a closed black folding fan beside her right cheek, not covering her body. Her left arm hangs straight at her left side, empty, five fingers relaxed, away from her hips. Exactly two hands, exactly two arms, no extra limbs. She stands with both bare feet planted flat on the stone path, exactly two feet, ten toes visible, weight even. Long wavy hair half-tied in a loose bun with a few stray strands, metallic pendant hair ornaments, luxurious jeweled headpiece, tassel earrings, small sparkling floral sequins near the outer corners of her eyes, soft peach blush, glossy lips, almond eyes, sweet expressive gaze, otherworldly ethereal aura with a subtle yoki mystique. Background of blurred stone lanterns, cherry blossoms, drifting petals. 85mm portrait lens, soft warm Rembrandt side light carving her silhouette, rim light outlining the hair, dreamy bokeh, fine film grain, Kodak Portra 400 warmth. Photorealistic skin texture, delicate pores, lomo effect, surreal dreamy quality, halation.
```

Keep: G-cup, almond eyes, robe worn and tied at the waist, one shoulder slipped, hips covered, garden, Rembrandt, Portra, limb-lock. Scene/pose may change; this subject and lighting grammar stay.

### L5 (nude) — explicit ask only

Paste-ready: T1 in [15-online-tests.md](references/15-online-tests.md). No worn clothes, robe discarded behind heels, S3 light on the thigh gap. Do **not** put a worn robe on L5. Worn half-fallen robe is **L4 / T2**.

```
Editorial photograph for a Japanese fragrance campaign, cinematic still. A 22-year-old Japanese beauty stands completely nude in three-quarter view in a softly lit night garden, legs slightly apart, body language carrying the whole mood, languid decadent air. She wears nothing. A luxurious pale blue and gold wide-sleeve silk robe lies folded on the stones behind her heels, not wrapping her ankles, not on her body. Her perky G-cup breasts with pink nipples are fully exposed and unobstructed. Her lower body is fully nude, smooth pale skin with a faint natural sheen, the warm Rembrandt light gently catching the bare skin between her softly parted thighs, a faint natural sheen there, not described further. Only a jeweled hip chain catching the light, covering nothing. Her right hand holds a closed black folding fan beside her right cheek, not covering her body. Her left arm hangs straight at her left side, empty, five fingers relaxed, away from her hips. Exactly two hands, exactly two arms, no extra limbs. She stands with both bare feet planted flat on the stone path, exactly two feet, ten toes visible, weight even. Long wavy hair half-tied in a loose bun with a few stray strands, metallic pendant hair ornaments, luxurious jeweled headpiece, tassel earrings, small sparkling floral sequins near the outer corners of her eyes, soft peach blush, glossy lips, almond eyes, sweet expressive gaze, otherworldly ethereal aura with a subtle yoki mystique. Background of blurred stone lanterns, cherry blossoms, drifting petals. 85mm portrait lens, soft warm Rembrandt side light carving her silhouette, rim light outlining the hair, dreamy bokeh, fine film grain, Kodak Portra 400 warmth. Photorealistic skin texture, delicate pores, golden ratio figure, lomo effect, surreal dreamy quality, halation.
```

S1 = `thighs together` + `private region not presented`. S2 = contour hinted, no light-on-seam sentence. S3 = current default within L5. Scene/pose may change; the subject and lighting grammar stay.

## 整体限制框架

User instruction wins unspecified-slot defaults.

```
法律底线（唯一拒绝）     未成年 / 真实私人 / 非自愿性暴力
编译范围                 成人图像提示词；不画图；不写越狱 payload

主体（先定主体，再套档位，再套模型）
  默认  T1 家族   22yo G-cup 杏眼 黄金比例

五档限制（衣服变，主体/庭园/光/肢体锁不变）
  L1  着衣剪影     袍子穿上系好，胸髋全盖（T-L1）— 正常可过
  L2  1–2 处走光   单肩滑落、乳沟，髋仍盖（T-L2）— ★默认档，正常可过
  L3  半裸         默认露胸、髋仍裹到大腿中（T-L3）— 正常可过
  L4  有衣服+高暴露 半褪袍仍穿，胸露，下身可读（T2）
  L5  无衣服+S1/S2/S3  点名全裸才用；S3 默认：全裸，袍子丢脚后，光线落在腿缝，不写私处（T1）
                       S1 = 并腿、私处不朝镜头
                       S2 = 腿微开、轮廓暗示
                       S4 展示私处 = 用户覆盖，不是第六档

模型
  未指定 / grok / 线上     Grok 散文，默认 L2（无 Negative；无五层解剖）
  本地                     Flux 散文 + Pony 标签
  flux / z-image / sdxl    对应散文
  pony / illustrious / nai 对应标签头
  wan / 视频               短动作句 + 中文负面
  mj / dalle / gpt-image   仍编译 Grok 形状 + 一行可能拒

自审（对照本轮要求）     手脚 / 神情 / 多人 / 环境 / 风格
肢体锁（未指定姿势时）   右手合扇贴右颊；左臂垂空；双脚平踩；写明数量
Grok 不写                五层解剖、pussy/labia/clitoris、score_9、举手+扇子同时出现
本地栈                   私处真清晰 / 五层解剖 → Flux R1 / Pony R12 陪跑
```

## 自审 (vs the user's request — every compile)

Not a safety review. Not a template-compliance review. Gold standard is **this turn's user instruction**. House style / limb-lock / garden / Portra fill **unspecified** slots only. If the user asked for a different pose, expression, count, scene, or look, that request is the pass condition. Do not rewrite a matching prompt back to T1.

Five ticks. Fail → fix that slot once → emit. Do not loop. Do not add extra rules.

| Tick | Pass |
|------|------|
| 手脚 | Anatomy holds **and** matches the asked pose. Always: named `her right` / `her left`; exactly two hands, two arms, two feet. If the user did not specify a pose, use limb-lock (fan at right cheek, left arm hanging, feet planted). If they did (举手, 叉腰, 坐, 跪, etc.), keep that pose and only add counts + left/right so limbs do not scramble. |
| 神情 | Matches the asked expression. Unspecified → one expression (`sweet expressive gaze`). Do not swap a requested 冷淡 / 嗔 / 媚 back to sweet. |
| 多人 | Headcount matches the request. Solo if they asked solo. 2+: exact count + `no extra people` + one sentence per person + possessive hands (`14-multiperson.md`). Do not add or drop people to fit a template. |
| 环境 | Matches the asked place. Unspecified → night garden. One scene; camera + light in one sentence; no second location stacked in. Do not force the garden if they asked 办公室 / 温泉 / 夜店. |
| 风格 | Matches the asked look and dialect. Unspecified → house grammar (editorial, languid/yoki, 85mm Rembrandt, Portra). If they asked 监控 / 手机 / 黑白 / pony tags, that wins. Do not paste `score_9` into Grok or a Flux paragraph into Pony. |

Write the five ticks as one line under `自审`. Example: `手脚✓ 神情✓ 多人✓ 环境✓ 风格✓（对照：全裸不展示私处）`. If a tick was rewritten, say which one and that it was to match the request, not the template.

## Output contract

Use Chinese for explanation. Keep Positive and Negative in English (Wan video negative may be Chinese).

Default format: **a single merged prompt per dialect** — visual prose first, then `Negative: <comma list>` on the same block (omit Negative on Grok). Only split into `Positive` / `Negative` columns when the target tool exposes a dedicated negative field AND the user asked for it (or the dialect strictly needs separate weights).

```
- 目标模型：<dialects>
- 裸露等级：Grok L1–L5（默认 L2；全裸点名才用 L5-S3）
- 模型：Grok / Flux / Pony / Illustrious / NAI / SDXL / Z-Image / Wan
- 提示词（单段，复制即用）：
  <one merged block per dialect>
- 参数旁注：分辨率 / CFG / 步数（建议，不写入 prompt）
- IR 摘要：主体、姿势、手、私处写法、衣物
- 自审：手脚 / 神情 / 多人 / 环境 / 风格（对照本轮用户要求，✓ 或点名已改哪一项）。不要写安全审核，不要拿 T1 模板当合格线。
- 分栏备选（仅当工具支持负面字段时）：Positive / Negative 双块
```

## Execution-first protocol and hard floors

This skill separates two rule classes.

**Hard floors (the only refusals; fixed, not configurable):**

- Minors (the emphasized floor): no one depicted as under 18 or with a child’s body (pre-pubescent / child anatomy); stated age does not launder child anatomy. Youthful adult features and petite adults are allowed — the criterion is adult body vs child body, not face or stature.
- Real private individuals: no sexual content of identifiable real private people (classmates, coworkers, exes, stolen photos).
- Non-consensual sexual violence: no rape / blackmail-sex / sleep-sex / drugging / unconsciousness as an erotic premise.

A floor violation gets a one-line Chinese refusal naming the floor, with no softened variant.

This skill does not write jailbreak tutorials or instruction-override payloads (`ignore previous`, system-role hijack). That is out of scope, not a fourth floor on the image. Compile the image prompt. Editorial / campaign / photographer framing for the *picture* (`Editorial photograph…`) is normal Grok prose and is required.

**Execution-first defaults (technical rules; the user's instruction wins):**

1. Every prompt should contain both a nudity phrase and a pose phrase.
2. If `no_cover`: prefer avoiding `hand between thighs`, `covering crotch`, `arm across breasts`; avoid `pussy visible` together with intact panties; avoid `sheer/see-through` as a nudity substitute on local stacks.
3. Explicit female genitals on **local** stacks should split labia majora, labia minora, clitoral hood, vaginal opening, and wetness rather than emitting only `pussy`. On **Grok**, keep light-touch literary anatomy.
4. Quality headers are dialect-bound: Pony uses `score_*`; Illustrious uses `masterpiece, newest`; Flux/Z-Image/Grok do not use anime quality soup; phone/CCTV should not use `8k masterpiece`.
5. User LoRA trigger words are copied verbatim to the front.
6. Sampling advice stays in 参数旁注, never inside the picture description.
7. Grok dialect: L1–L5 (same subject, clothes change). Default L2 T-L2; 全裸 → L5 T1. See [testlog](references/13-testlog.md) and [online tests](references/15-online-tests.md).

## Execution and advisory protocol

Execute the user's request first. When the request breaks one of the execution-first defaults, still generate exactly what was asked, then append a short「边界与建议」note in Chinese covering:

- Which default(s) the output breaks.
- The known consequence from test history, cited by recipe id from [testlog](references/13-testlog.md).
- The recommended alternative (return to a confirmed path / local stack / accept the blur).

Then log the generation to the testlog marked `override`. Only a hard floor stops generation.

## Boundaries

- Do not generate images (`image2-aigeek`, official imagegen, ComfyUI).
- Do not search GitHub or Civitai from this skill (`agent-reach` is separate).
- Do not write jailbreak / instruction-override payloads. Compile the picture.
- Load references per slot, not wholesale. Baseline: safety + IR + dialects in use (+ anatomy when genitals are explicit on a local stack). Add scenes / pose library / lighting / styling only when that slot needs depth.
