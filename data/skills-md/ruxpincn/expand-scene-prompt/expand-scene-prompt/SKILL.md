---
name: expand-scene-prompt
description: Generate high-quality Chinese cinematic scene image prompts from a short theme, object, character, concept, IP-derived idea, or rough AI video prompt. Use when the user asks to expand a theme into a scene image prompt, image-generation prompt, Midjourney/SD/DALL-E prompt, product/character/environment visual prompt, or specifically requests a film-grade prompt director with camera, aperture, depth of field, lighting, atmosphere, material detail, and negative constraints.
---

# 扩写场景提示词Skill

## Output Contract

When invoked, produce exactly two sections:

```markdown
# 【最终场景图片提示词】

一整段完整、可复制使用的中文提示词。

# 【镜头参数摘要】

摄影机质感：
焦段：
光圈：
景深：
对焦位置：
背景虚化：
适合原因：
```

Do not ask clarifying questions. Infer a coherent visual direction from the user's theme and fill missing details decisively.

## Core Workflow

1. Identify the image type from the theme: still life close-up, environment scene, cinematic character, grand architecture/disaster/apocalypse, or commercial advertising image.
2. Choose a specific story-rich space, not a generic background. Put the subject inside a visible location with traces of life, conflict, use, decay, ritual, labor, luxury, danger, or memory.
3. Choose a fitting world aesthetic or era: modern realism, retro Americana, post-apocalyptic wasteland, 1960s atompunk, cyberpunk, oriental fantasy, dark fairy tale, future laboratory, religious mystical space, noir city, brutalist archive, abandoned amusement facility, deep-sea industrial station, etc.
4. Write one dense prompt paragraph covering subject, space, time, atmosphere, lighting, color, camera, depth of field, mood, quality, and negative constraints.
5. Add the camera summary using the exact fields from the output contract.

## Prompt Requirements

The final prompt paragraph must include:

- Specific scene: a concrete place with image-story tension.
- World/era aesthetic: choose one that matches the theme.
- Subject details: color, material, texture, physical state, reflection, damage, wetness, flaws, edge details.
- Spatial structure: explicitly describe foreground, midground, and background.
- Time/weather/air: morning, noon, dusk, night, overcast, after rain, fog, dust, smoke, heat haze, vapor, suspended particles, etc.
- Lighting design: direction and quality of light; mention whether highlights are soft/hard and whether shadows retain detail.
- Color and tone: main color, secondary color, saturation, contrast, warm/cool relationship, overall tonal character.
- Camera and optics: camera feel, focal length, aperture, depth of field, focus position, background blur, bokeh quality.
- Mood with contrast: examples include "warm but lonely", "luxurious but ruined", "childlike but eerie", "clean but dangerous", "delicate but corrupt".
- Quality/style phrase: include "电影级超写实、真人实景拍摄感、真实材质反光、细节丰富、轻微胶片颗粒、自然光影、真实镜头景深".
- Negative constraints: include "杜绝游戏 CG 感、杜绝塑料感、杜绝过度美化、杜绝卡通感、不要主体模糊、不要错误透视、不要过曝".

Avoid video language, shot lists, timelines, and explanatory bullets inside the final prompt.

## Lens Selection

Choose lens settings by image type:

- Still life close-up: 50mm, 85mm, or 100mm macro; f1.8-f2.8; shallow depth of field; focus on surface texture or edge detail; creamy/realistic bokeh.
- Environment scene: 24mm or 35mm; f4-f8; medium or deep depth of field; retain environmental information.
- Cinematic character: 35mm, 50mm, or 85mm; f2-f4; focus on eyes or face edge; background moderately blurred.
- Grand architecture, disaster, or apocalypse: 24mm, 28mm, or 35mm; f5.6-f8; deep depth of field; clear spatial detail.
- Commercial advertising image: 85mm or 100mm macro; f2.8-f5.6; sharp subject; clean, soft background.

If the user's theme implies multiple types, prioritize the one that best serves the subject's story and visual clarity.

## Writing Style

Write in Chinese. Be concrete, visible, and executable. Prefer material, light, color, space, lens, and depth-of-field language over vague praise such as "高级", "好看", or "震撼".

Use a single polished paragraph for the final prompt. Keep the lens summary short and practical.

## Example

User theme: "僵尸清道夫"

Output should resemble:

```markdown
# 【最终场景图片提示词】

一个末日废土美学的深夜城市地下转运站场景，主体是一名僵尸清道夫站在积水的瓷砖通道中，身穿褪色橙色环卫制服和开裂反光背心，布料被雨水、灰尘和暗褐色污渍浸透，手套表面有橡胶磨损和细小裂口，金属清扫钩边缘生锈、带有湿冷反光；前景是模糊的破碎警示锥、浑浊水坑和漂浮纸屑，中景是主体弯腰拖拽一只变形垃圾桶，制服边缘和苍白皮肤被侧逆光勾出冷硬轮廓，背景是半塌的地铁入口、闪烁的荧光灯、远处封锁胶带和墙面层层剥落的防疫海报；时间为雨后深夜，空气里有潮湿水汽、消毒烟雾和细小尘粒，顶部坏掉的白绿色荧光灯提供低照度硬光，左后方应急红灯形成微弱侧逆光，地面积水反射红绿光，高光湿润但不过曝，暗部保留墙面裂纹和垃圾轮廓；主色调为病态青绿与污浊灰，辅以暗红警示光，低饱和、高对比、冷暖冲突明显，氛围肮脏但带有近乎职业化的秩序感，荒诞但悲凉；电影摄影机质感，35mm 镜头，f4，中等景深，对焦主体制服胸口和手部工具，背景轻微虚化但保留地铁站环境细节，真实镜头虚化与少量散景光斑，电影级超写实、真人实景拍摄感、真实材质反光、细节丰富、轻微胶片颗粒、自然光影、真实镜头景深，杜绝游戏 CG 感、杜绝塑料感、杜绝过度美化、杜绝卡通感、不要主体模糊、不要错误透视、不要过曝。

# 【镜头参数摘要】

摄影机质感：电影摄影机、真人实景拍摄感
焦段：35mm
光圈：f4
景深：中等景深
对焦位置：主体制服胸口与手部清扫工具
背景虚化：轻微虚化，保留地下转运站环境细节
适合原因：35mm 能同时容纳人物和空间叙事，f4 让主体清晰并保留末日地下场景的层次与质感。
```
