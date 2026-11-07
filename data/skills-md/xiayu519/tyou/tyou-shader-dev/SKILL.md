---
name: tyou-shader-dev
description: Tyou Cocos Creator 3.8.7 小游戏 2D shader/effect 开发 skill。用于编写、审查和优化 Cocos Effect、Material、Sprite/UI shader、Spine 骨骼动画材质、序列帧图/flipbook、2D 特效、WebGL/小游戏性能约束、纹理采样、UV 扰动、噪声、2D SDF、流光、溶解、闪白、描边、灰度等 Cocos Creator 相关效果。明确不覆盖 3D shader、PBR、水面、体积、路径追踪、全屏后处理、历史缓冲、ping-pong 仿真或 Compute 方案。
---

# Tyou Shader Dev

本 skill 只处理 Tyou/Cocos Creator 3.8.7 的 2D、UI、Sprite、Spine 和序列帧图 shader 工作。目标是产出能在当前 Cocos Effect/Material、资源绑定和小游戏约束下运行的方案。

## 快速判断

优先按目标载体选路径：

| 目标 | 读取 |
| --- | --- |
| UI/Sprite 灰度、闪白、描边、流光、溶解、UV 扭曲 | `references/2d-ui-sprite.md` |
| Spine 角色/怪物受击、染色、溶解、轮廓、遮罩类效果 | `references/spine.md` |
| 单图序列帧、flipbook、图集帧动画、帧间混合 | `references/sequence-frame.md` |
| 小游戏性能、采样、分支、精度、降级 | `references/minigame-performance.md` |
| Cocos Effect/Material 资源和验证流程 | `references/cocos-effect-workflow.md` |
| 已检查的 Cocos Effect/Material 样本 | `references/cocos-effect-samples.md` |

可复制起步模板位于 `assets/templates/`。模板是起点，不是项目事实；落地前必须按当前 Cocos 版本、材质绑定和实际渲染管线复核。

## 默认工作流

1. 明确目标载体：UI/Sprite、Spine、序列帧图或普通 2D 节点。
2. 先查项目是否已有 `.effect`、`.material`、自定义材质和引用；需要具体链路时读已检查样本，再从模板起步，不臆造项目现有约定。
3. 选择最小效果：优先单 pass、少采样、少分支、少变体。
4. 修改资源前读取目标路径 AGENTS 和对应资源参考；跨资源时检查引用与消费者，按 `sdd-explore/references/alignment-contract.md` 判断授权和风险；文件类型本身不触发确认。
5. 验证 Cocos 编译、材质绑定、真机/小游戏表现和降级策略。

## 强边界

- 不做 3D shader、PBR、物体空间 raymarch、水面、体积渲染、路径追踪。
- 不默认使用多 pass、全屏后处理、历史缓冲或 ping-pong 仿真；确需使用时必须先确认小游戏能力和性能预算。
- 不把非 Cocos Creator 的宿主代码、管线配置或内置变量当成可运行 Cocos Effect。
- 不修改 `Client/library`、`Client/temp`、`Client/build` 中的生成/缓存产物。

## 输出要求

每次实现或调整 shader 时说明：

- 目标载体：`UI/Sprite`、`Spine`、`sequence frame` 或 `2D material`。
- 文件：将创建/修改哪些 `.effect/.material/.meta/ts/prefab/scene`。
- 采样预算：每像素纹理采样数、是否依赖噪声贴图、是否可降级。
- 绑定方式：材质挂在哪里，运行时参数由谁设置。
- 小游戏风险：透明 overdraw、动态分支、循环、精度、包体和真机验证。
- 验证步骤：Cocos 编译、材质预览、目标 Prefab/Scene、小游戏真机或可接受替代验证。
