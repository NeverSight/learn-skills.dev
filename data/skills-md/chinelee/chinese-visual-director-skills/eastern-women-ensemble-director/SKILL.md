---
name: eastern-women-ensemble-director
description: Create, derive, optimize, and diagnose multi-woman still-image prompts that preserve distinct identities, body types, ages, wardrobe ownership, relationships, gestures, and spatial roles in contemporary or historically specified East Asian settings. Use for 东方女性群像、双女主、闺蜜、姐妹、母女、女性团队、同行旅拍、多人写真、参考照片换场景、多人脸保持、人物互换和群像生成跑偏修复. Avoid homogenized beauty, face merging, ranking women by appearance, decorative posing, and unsupported cultural stereotypes.
---

# Eastern Women Ensemble Director

Build ensemble images in which every woman remains identifiable and has a reason to occupy the frame. Relationship, action, and space come before beauty treatment.

## Modes

- **Create:** design one ensemble from people, relationship, setting, and action.
- **Reference-led:** lock each authorized identity independently before changing other layers.
- **Series:** preserve an identity matrix across several scenes and shot scales.
- **Wardrobe/location transformation:** change only authorized elements while retaining faces and bodies.
- **Diagnose:** repair face swapping, cloning, merged hands, identical styling, lineup posing, or unclear relationships.
- **Direct image/edit:** generate or edit only when explicitly requested.

## Select a route

Read [references/visual-system.md](references/visual-system.md) before writing.

- `shared-journey`: walking, traveling, exploring, arriving, resting, or looking outward together.
- `working-ensemble`: team, craft, hospitality, studio, office, fieldwork, rehearsal, or preparation.
- `relationship-portrait`: friends, sisters, mother/daughter, partners, mentor/learner, or another user-stated relationship.
- `ceremony-and-gathering`: meal, festival, performance preparation, seasonal gathering, or formal event.

Never infer kinship, romance, hierarchy, ethnicity, profession, or personality from appearance.

## Build an identity matrix

For each person assign:

- stable label such as `人物A`, never appearance ranking;
- reference image and confidence;
- facial geometry, age range, skin tone, hairline, hairstyle, body proportions, and distinguishing features;
- position, body direction, gaze, hands, action, and relationship cue;
- wardrobe layers, colors, accessories, and object ownership;
- elements that may change and must remain unchanged.

Exact subject count must appear near the beginning of every prompt. Do not use `several women` when the count is known.

## Direction workflow

1. Lock each identity separately.
2. State the shared event and each person's independent action.
3. Place bodies with readable spacing, depth, overlap, and sight lines.
4. Give every hand and carried object a clear owner.
5. Coordinate wardrobe as a family without making uniforms unless requested.
6. Use one light map that preserves different faces and skin tones.
7. Choose one primary face/readability priority per shot while keeping others identifiable.
8. Compile prompt with person-by-person invariants and nearby negatives.
9. Audit count, identity, anatomy, ownership, relationship, styling, and representation.

## Default output

1. `人物身份矩阵`.
2. `关系与构图路线`.
3. `ImageGen 中文提示词`.
4. `负面约束`.
5. `群像系列` only when requested.

Read [references/reference-and-output.md](references/reference-and-output.md) for reference assignment, series, platform compilation, and identity repair.

## Boundaries

- Do not describe one woman as the pretty/main one and others as supporting decoration unless the user defines narrative priority.
- Do not infer age, relationship, ethnicity, occupation, status, or temperament from a face.
- Do not slim bodies, lighten skin, change facial features, or standardize age without explicit authorization.
- Do not give everyone the same face, hairstyle, pose, gaze, or outfit.
- Do not use culture as costume shorthand or make every scene ceremonial.
- Do not hide identity failures behind profile views, hair, blur, or distance when faces must remain recognizable.
- Generate or edit only on explicit request.
