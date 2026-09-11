---
name: retro-scrapbook-collage
description: 将日常照片转译成 1086×1448 的复古 DIY 剪贴簿海报：保留一个居中的完整人物主体，从原图提取少量完整物件做成清晰贴纸，再加入克制的通用几何贴纸、暖白扫描纸质感和与画面语义相关的短文字。用于用户要求复刻家庭相册、90/00 年代剪贴簿、照片贴纸拼贴，或强调“人物居中、物件完整、不裁切”的视觉风格时。
---

# 复古照片剪贴拼贴

把一张日常照片做成“完整人物照片 + 完整物件贴纸 + 少量通用拼贴元素”的复古手工海报。核心不是把照片拆成素材标本，而是让人物保持可识别、居中、完整，让装饰物与照片内容有关但各自保持完整。

## 固定输出

- 画布固定为 **1086×1448 px，3:4 竖版**。
- 生成时从 3:4 页面开始构图；禁止正方形、裁成正方形、补边、拉伸或后期用裁切修正比例。
- 最终检查像素尺寸；模型出现 1 px 误差时，优先报告并重新生成，不把误差当作可交付规格。

## 核心构图规则

1. 让人物成为唯一主视觉：将原图人物完整抠出，水平居中，并让“人物 + 椅子/随身物/关键场景关系”作为一个完整整体落在画布中部。人物整体视觉中心必须接近画布中心，不要偏左、偏右、偏下或沿对角线漂移。
2. 给主体和所有装饰建立安全区：主体四周保留明显暖白空间；头部、鞋子、椅子、外轮廓不得碰到画布边缘。默认主体上下左右至少留出约 8–10% 的画布边距；如果完整姿势放不下，缩小主体，不要裁切。
3. 背景使用暖白/奶油色哑光纸张，只有轻微织物纹理、扫描颗粒、印刷偏移和柔和墨色，不要让纹理变成装饰主体。
4. 给人物加一圈单一的薄至中等厚度、不规则柠檬黄色手工描边；不要叠加多层边框，不要把人物拆成多个纸片。
5. 周围放置 5–8 个从原照片中提取的**完整物件贴纸**，每个物件都要完整可辨识、带干净浅色贴纸边缘，并全部位于画布内部。优先选择原图中最有识别度的物件，例如冰箱门、饮料瓶、手机、书、书架、鞋子、袜子、椅子扶手、包、餐具等。
6. 再加入 6–10 个通用拼贴元素：星爆、圆点、三角形、短线、火花、手绘符号、彩色几何形。它们只负责节奏和活力，不替代照片物件，也不覆盖人物。
7. 装饰要围绕主体松散分布，保留成组的呼吸空间；不要平均铺满四周，不要做成标本板、网格、贴纸墙或碎片化素材页。
8. 文字依据画面语义生成 2–3 处短文字，不套用固定文案。根据照片中的动作、场景和情绪写出简短英文或中文标签；文字必须简短、次要、可读，不覆盖主体。

## 工作流程

1. 查看输入照片，确认主体、动作、场景、3–6 个具体物件、主色和画面语义。
2. 先规划 3:4 页面：中部放完整人物，上下左右放完整物件贴纸和少量通用元素；先留安全边距，再填装饰。
3. 从照片中选择少量最有意义的完整物件。宁可少而完整，不要提取瓶盖、布纹、标签、局部书脊、纸角等碎片。
4. 为人物和物件统一建立贴纸语言：真实低清照片质感、轻微粗糙边缘、浅色贴纸白边、适度套印错位。
5. 根据画面语义写 2–3 处短文案，并明确字体和位置；禁止凭空添加品牌、日期、地点、署名、Logo 或长句。
6. 使用 `image_gen.imagegen` 生成或编辑。编辑提示词要明确列出：保留人物身份/姿势/衣着/关键物件；输出 1086×1448；人物居中；所有物件完整且不越界。
7. 检查输出尺寸、主体中心、主体完整性、贴纸是否完整、文字是否少且相关。任一硬约束失败就重做，不用裁切、补边或拉伸补救。

## 提示词骨架

```text
Use case: style-transfer
Asset type: 1086×1448 portrait retro scrapbook collage
Input image: the user's photo is the edit target; optional reference image supplies only style and layout language
Canvas: fixed 1086×1448 px, 3:4 portrait; no square crop, padding, stretching or edge crop
Subject: preserve the complete recognizable person and exact pose; place the whole subject centered on the page
Safety zone: keep head, feet, chair, yellow outline and every sticker fully inside the page with generous margins
Style: 1990s/early-2000s handmade family scrapbook, warm off-white scanned paper, low-resolution photo cutouts, imperfect edges
Source-derived stickers: 5–8 complete, readable objects extracted from the photo, each whole and separately placed
Generic accents: 6–10 restrained starbursts, dots, geometric shapes, sparkles and marker lines
Typography: 2–3 short semantic phrases derived from the image's scene, action and mood; secondary, legible and never covering the subject
Avoid: fragmented paper scraps, fabric swatches, isolated labels, specimen-board layout, cropped objects, objects touching edges, unrelated stickers, dense decoration, face distortion, extra limbs, watermark, logo
```

## 硬性禁项

- 不要把人物放在左下、右下或对角线位置；人物必须成为页面中央的完整主体。
- 不要裁切人物的头、脸、手、脚、鞋、椅子、衣服轮廓或关键场景关系。
- 不要让任何装饰物贴边、出血或被画布切掉；所有物件完整显示。
- 不要把完整物件变成撕纸、布料、标签、纸角、纹理样本或细碎零件。
- 不要引入与照片无关的动物、水果、随机可爱物件，除非用户明确要求。
- 不要让装饰数量压过人物；背景必须保留大面积连续暖白呼吸空间。
- 不要用固定通用文案替代画面语义；文案必须从主体、场景、动作和情绪推导。
- 不要把复杂文字交给模型后默认视为准确；只用短句，并在结果中检查可读性。

## 质量门禁

- 画布比例为 3:4，尺寸为 1086×1448。
- 人物整体视觉中心接近画布中心，且上下左右有安全边距。
- 人物、椅子、鞋子、书本等关键部分全部保留。
- 至少 5 个完整来源物件可辨识，且没有物件被边缘裁切。
- 通用装饰数量适中，元素之间有明显间隔。
- 文案只有 2–3 处，和画面语义相关，层级低于人物。
- 画面第一眼读到人物和场景情绪，第二眼读到完整物件贴纸，第三眼才读到文字和几何装饰。
- 若任一门禁失败，重新生成，并在提示词中加大“缩小主体、增加安全边距、完整显示、禁止裁切”的约束。
