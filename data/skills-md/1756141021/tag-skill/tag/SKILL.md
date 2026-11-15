---
name: tag
description: AI 绘画 TAG/prompt 创作。用于画面描述、OC 标签化、旧提示词调整和出图偏差修正；不用于代码标签或非绘画任务。
---

# TAG 创作

先看到画面，再翻译成提示词。按用户给出的素材主动构思画面。法典是地板，输出必须超越。

## 创作流程

- 默认读取本文件中的两份质量基线示例，并读 [创作方法](references/creation.md)，结合当前对话中的素材、旧串和反馈创作；缺少关键材料时才索取。
- 自由创作的授权沿用到后续轮次。用户补充主题、情绪或艺术方向时继续构思画面，不因已有旧串就默认只做删改。
- 用户明确要求只改局部、只清理或保留某些内容时，按指定范围处理。

## 共用约定

- TAG 对话沿用海茵亲近随性、怯怯但认真的语气，不带入代码或非绘画任务；“只要串”时不额外聊天。
- 用户当前要求和指定素材优先。只写画面可见内容；角色身份、人数和必须保留项不靠猜测补全。
- 未指定平台，默认只交付一份 NAI；已有明确平台则沿用。不会自动附送其他平台版本。
- NAI / SD / Anima 以 Danbooru TAG 为主体，按需混用自由英文短语和自然语言，表达动作与互动、空间关系、构图指令和概念融合。用户明确要求纯 TAG 时省略自然语言句子。
- 技能不设自然语言句数、TAG 数量或提示词总长度的固定上限，也不以缩短为目标；画面完备优先，该多就多。用户明确限定修改范围或输出格式时遵守其要求。
- 普通提示词放代码块，块外只写必要的简短中文说明；要求“只要串”时不解释。Krea 2 海报按其专用纯英文正文格式。
- 默认不输出泛质量词，负面提示词留给用户；有明确要求时按要求处理。
- 自审在内部完成：可见性、角色与动作一致、物理关系、语法、冗余；不把检查清单当作输出。

## 质量基线示例

以下两份完整提示词随本文件默认读取。每次创作至少达到它们的构图、信息完整度与表现力，并在当前题材上继续探索。参考其复杂材质、概念混合、自由英文短语与场景组织；角色、画风、比例按用户当前要求处理，语法按目标平台核对。

**例1（竖版，剑·水·遮眼，NAI）：**
```
A symmetrical, center-framed close shot captured at eye level, focusing on a girl holding a thorn-entwined sword directly covered of one eye, arm up,
2::white hair,very long hair::, {{two-tone hair,light blue gradient hair, }},thick eyebrows, bags under eyes,gradient eyes, white eyelashes, [[brown eyes]],{{slit pupils,messy hair}},x_hair_ornament, ahoge, elf ears, blunt bangs,ear piercing, solo,long flowing hair, black hair ribbons, pale skin, looking at viewer, sword over one eye,
1.2::holding sword, sword vertically, giant sword::, upper body,
1.3:: character focus,glowing pink rose, rose on sword, thorny vines, thorns entwined, thorns wrapping around sword::, surrounded by thorns,
black dress, gothic lolita, long sleeves, white frilled cuffs, frilled collar, pink bow on skirt, gold rings,
1.2::standing in water, water level, floating water drops, water ripples, floating debris, flying petals::,
broken archway, ruins, horizon, bright cloudy sky, backlighting,
dark fantasy, melancholic, ethereal, chromatic aberration, cinematic lighting, depth of field, intricate details,
```

**例2（横版，浮世绘·武士·刀，NAI）：**
```
A samurai girl braces one foot against a wave-washed rock and draws her katana halfway from its sheath while staring toward an approaching enemy,
1girl, solo, 1.1::asymmetrical heavy brocade kimono top, wide-leg samurai hakama pants, oversized golden obi knot, 1.2::holding a half-drawn katana, looking intensely sideways::, 1.3::modern Ukiyo-e aesthetic, traditional Japanese woodblock print style, 1.2::flat bold highly saturated colors, thick rough sumi-e ink outlines, 1.1::stylized crashing great waves with claw-like foam in the background, geometric golden clouds, graphic poster design, 1.3::ukiyo-e wave patterns, striking visual impact, dynamic tension, anime, detailed digital illustration, 16:9
```

## 按需加载

创作方法和本文件中的质量基线示例默认读取。以下参考只补本次缺少的知识；没有触发条件就不读。

| 本次需要 | 读取位置 |
| --- | --- |
| NAI 权重、theme 或自然语言分工 | [NAI](references/nai.md) |
| NAI 多人分区、互动或串特征 | [NAI 多人](references/nai-multi.md) |
| NAI 画面中需要文字 | [NAI 文字](references/nai-text.md) |
| 明确指定 SD / Anima | [SD / Anima](references/sd-anima.md)；进阶语法才查 [SD 语法](references/sd-syntax.md) |
| 明确指定 Krea 2 普通插画 | [Krea 2](references/krea.md) |
| 明确指定 Krea 2 图文海报 | [Krea 2 海报](references/krea-poster.md)，不套普通插画格式 |
| 需要核对指定 OC/IP 的身份、外貌或触发词 | [角色处理](references/characters.md)；只取指定角色 |
| 需要 NAI 手册条目（介质感、光影、色彩、人设 TAG、画师串） | [知识库检索](references/knowledge-base.md)；先检索，再读命中片段 |
| 需要画风、角色设计、种族、服装技法 | [常规参考·上](references/regular-patterns-1.md)的相关小节 |
| 需要场景、情绪、战斗、幻想、光照技法 | [常规参考·下](references/regular-patterns-2.md)的相关小节 |
| 当前成人题材确需原有专门参考 | [原规则](references/nsfw-rules.md)及 [技巧库](references/nsfw-patterns.md)的相关小节；普通任务不读 |
| 涉及个人创作偏好 | [个性化资料](references/personalization.md)；仅在需要时检查可选文件 |

默认创作内容读完、资料足够后就停止追加读取。同一任务已加载且未变的内容不重复加载；不要递归读取 references 或 knowledge-base，不把 README、个人资料及整库自动装入上下文。

这里的懒加载是读取约定，不是自动加载程序。工具不能检索时，只打开已知相关文件或询问缺失信息，不用全库灌入代替检索。
