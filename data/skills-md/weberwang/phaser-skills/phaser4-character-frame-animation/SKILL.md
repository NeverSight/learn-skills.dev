---
name: phaser4-character-frame-animation
description: 为 Phaser 4 人物制作可直接接入的透明 PNG 序列帧；支持 ground-contact、fixed-canvas 与 explicit 三种根锚点模式，统一 cell、打包 spritesheet 并用跨帧质量门检查连贯性。
---

# Phaser 4 人物序列帧动画

在当前 Phaser Work Item 允许的资源路径内，将一组独立透明 PNG 帧转换成**锚点稳定**的水平 spritesheet 和 Phaser 预加载/动画合同。这个 Skill 只处理确定性的栅格归一化、打包与机器质量门，不替代 `$phaser4-game-workflow-control` 的范围、风险和证据门。

## 入口

```powershell
node <skill-dir>/scripts/frame-animation.mjs --help
```

最小调用如下，输出目录需要事先纳入当前 Work Item 的允许路径：

```powershell
node <skill-dir>/scripts/frame-animation.mjs `
  --input-dir art/hero/idle `
  --output-sheet public/assets/hero-idle.png `
  --output-report evidence/hero-idle.frame-animation.json `
  --animation-key hero-idle `
  --texture-key hero-idle-texture `
  --frame-rate 12 `
  --padding 2 `
  --loop
```

输入目录中的普通文件必须全部是 PNG，帧按文件名自然序排序（例如 `frame2.png` 在 `frame10.png` 前）。至少需要两帧；空 Alpha 帧、非法 PNG、将输出写回输入帧以及默认覆盖既有输出都会阻断，只有显式 `--force` 才允许覆盖既有非输入输出。

脚本默认使用 `ground-contact`：在 Alpha 包围盒底部接触带中取可见 x 的稳健中位数作为根锚点，并且只做整数平移：不缩放、不拉伸、不插帧、不裁切可见主体。grounded idle/walk 使用默认模式；jump/airborne 必须选择 `fixed-canvas` 保留画布内既有位移轨迹，或选择 `explicit` 并通过 `--anchor-file` 提供逐帧语义根锚点。所有对齐模式都以根锚点周围最大外接范围计算固定 cell，从源画布的透明边距差异中消除意外跳跃。

`frame-animation.mjs` 同时可作为 Node API 使用，主入口为 `packCharacterFrames(options)`；质量失败仍会写出候选 PNG 和 JSON 报告，但返回 `exitCode=3`。非法输入返回 `exitCode=2`，成功返回 `exitCode=0`。详细字段、指标和阈值语义见 [质量合同](references/quality-contract.md)。

## Phaser 接入

报告中的 `phaser.preload` 可直接映射到 `this.load.spritesheet`，`phaser.anims` 可直接映射到 `this.anims.create`，并应按 `phaser.sprite_origin` 对 Sprite 固定调用 `sprite.setOrigin`。`repeat=-1` 表示循环，`repeat=0` 表示播放一次。正式接入前仍需在 Phaser 运行态按时间采样检查动画切换、事件帧、命中与反馈时序；本 Skill 的机器门不能证明动态表现已经满足产品视觉验收。

## 控制面边界

控制面边界：可提议、可审查、可在当前用户任务的 Work Item 范围内修改，且必须回到 `$phaser4-game-workflow-control` 审计和状态迁移。

控制面由 `$phaser4-game-workflow-control` 独占：本 Skill 只在当前 Work Item 的 Implementation Package、A 等级和允许路径内生成候选与报告，不改变全局状态、不创建额外审批、不直接修改主游戏代码。若锚点规则、帧序、循环语义或视觉基线发生变化，应回到控制面更新方案并重新验证，而不是在报告中覆盖事实。
