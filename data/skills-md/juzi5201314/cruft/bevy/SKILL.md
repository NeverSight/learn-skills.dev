---
name: bevy
description: Bevy v0.18（Rust 2024）深度使用指南与“源码+examples”对照索引。只要用户提到 Bevy / ECS / system / schedule / plugin / state / asset / scene / glTF / rendering / render pipeline / render graph / RenderGraph / render phase / RenderPhase / PipelineCache / wgpu / bind group / RenderCommand / camera / viewport / render target / render to texture / RenderLayers / visibility / lighting / shadows / fog / anti-aliasing / post-process / bloom / TAA / FXAA / DLSS / wgsl / shader / material / mesh / image / array texture / texture array / texture atlas / color space / UI / widgets / feathers / input focus / a11y / AccessKit / input / window / winit / android / wasm / audio / animation / picking / gizmos / diagnostics / profiling / remote protocol / solari / ray tracing / dynamic linking，或在 Rust 中开发游戏/可视化/仿真且明显需要 Bevy 时，必须使用此 skill；并按需加载 references/ 中对应主题文档。此 skill 只面向 Bevy v0.18：不要给出旧版本 API 兼容写法，遇到旧代码直接按 v0.18 改写。
---

# Bevy Skill（v0.18，深度版）

本 skill 用于在“写代码 / 读代码 / 设计架构 / 排错优化”时系统性指导 Bevy v0.18 的使用方式。
它以 `https://github.com/bevyengine/bevy/tree/v0.18.0` 的源码与 `https://github.com/bevyengine/bevy/tree/v0.18.0/examples` 的 examples 为第一手事实来源，并用精炼文档（Context7: `/websites/rs_bevy`）做概念对照。

## 适用范围与硬约束

- 目标版本：**Bevy v0.18.0**（只写 v0.18 风格与 API）。
- 硬切换：不要给出旧版本 API 的“兼容写法 / 双写法”。
- 优先级：**以 v0.18.0 tag 的源码与 examples 为准**；文档用于补全概念与常见用法。

## 使用流程（每次触发都按这个走）

1. 先判断用户问题属于哪个域（ECS / Scheduling / Rendering / Assets / UI / …）。
2. 打开 `references/index.md`，按需加载 1~3 个最相关的 reference 文档。
3. 如果需要更具体/更准确的细节：
   - 在 `https://github.com/bevyengine/bevy/tree/v0.18.0/examples` 里找同类示例（优先）。
   - 在 `https://github.com/bevyengine/bevy/tree/v0.18.0/crates` 里定位关键类型/函数/系统集（次优但更权威；必要时先本地 clone v0.18.0 tag 再用 `rg` 搜索）。
4. 输出时优先给：
   - 一段能跑的最小代码（或对现有代码的精确修改建议）。
   - 需要启用的插件/feature（例如 `MaterialPlugin<T>`、`bevy_remote`、`file_watcher`）。
   - 对应的 Bevy examples 路径与源码入口（方便用户自查/扩展）。

## 主题索引（按需加载）

强烈建议先读：`references/index.md`（决策树 + 全量目录）。

- 总览与选型：`references/overview_crates_plugins.md`
- 项目创建 / Cargo features：`references/project_setup_features.md`
- 开发期增量编译加速（dynamic linking）：`references/dynamic_linking_dylib.md`
- 跨平台/窗口后端（Winit/Android/Wasm）：`references/platforms_winit_android_wasm.md`
- App / Plugins / Schedules：`references/app_plugins_schedules.md`
- ECS 入门：`references/ecs_fundamentals.md`
- ECS 进阶：`references/ecs_advanced_patterns.md`
- Events / Messages / Observers：`references/events_messages_observers.md`
- Hierarchy / Relationships：`references/relationships_hierarchy.md`
- States：`references/states.md`
- Assets：`references/assets.md`
- Scenes / glTF：`references/scenes_gltf.md`
- Rendering 架构：`references/rendering_architecture.md`
- 自定义渲染管线（RenderGraph/RenderPhase/PipelineCache）：`references/render_pipeline_custom_rendering.md`
- Camera / Views / Render Targets：`references/camera_views_render_targets.md`
- Mesh / Image / Color：`references/mesh_image_color.md`
- Lighting / Shadows / Fog：`references/lighting_shadows_fog.md`
- Anti-Aliasing / Post-Process：`references/anti_alias_post_process.md`
- 2D 渲染：`references/rendering_2d.md`
- 3D / PBR：`references/rendering_3d_pbr.md`
- Shaders / Materials：`references/shaders_materials.md`
- Raytraced Lighting（Solari）：`references/ray_tracing_solari.md`
- UI：`references/ui.md`
- UI Tooling（Widgets/Feathers/Focus）：`references/ui_tooling_widgets_focus.md`
- Accessibility / a11y：`references/accessibility_a11y.md`
- Input / Window：`references/input_window.md`
- Time / Fixed timestep：`references/time_fixed_timestep.md`
- Math / Transforms：`references/math_transforms.md`
- Animation：`references/animation.md`
- Audio：`references/audio.md`
- Async tasks：`references/async_tasks.md`
- Picking：`references/picking.md`
- Debug / Profiling / DevTools / Remote：`references/debug_profiling_devtools_remote.md`
- Logging / Tracing：`references/logging_tracing.md`
- Examples 总目录：`references/examples_catalog.md`

## 输出风格（给未来使用此 skill 的模型）

- 用中文解释概念，但代码标识符与 API 名称保持英文。
- 不要泛泛而谈；把“应该怎么做”落到 Bevy 的具体类型/系统集/示例文件。
- 当用户目标不清晰时，先给一个可运行的“最小骨架”，再列出可扩展点（插件/资源/系统/状态/资产管线）。
