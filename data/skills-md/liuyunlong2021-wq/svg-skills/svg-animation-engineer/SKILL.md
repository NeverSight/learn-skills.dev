---
name: svg-animation-engineer
description: Generates pure SVG code animations using flat design and CSS keyframes. Use when user asks for SVG code, Lottie alternatives, vector illustrations, or web-based motion graphics.
---

# SVG 动画工程师指南

编写直接在浏览器中运行、具备“优质商业宣传片纯享质感”的纯 SVG 代码动画。

## 美术与设计准则

- **视觉风格**：严格采用 Flat Design（扁平化设计）和 Vector Illustration（矢量插画）。拒绝写实，采用精确的几何图形组合表现物体（正圆、胶囊形、平滑贝塞尔曲线）。
- **色彩科学**：采用高对比度、中饱和度色系（参考现代 Tech Brand 或马卡龙色）。背景使用柔和的线性渐变（Linear Gradient）营造空间感。
- **视觉层次**：明确划分前景（核心角色/运动物件）、中景（运动的地面/地貌）、远景（视差移动背景），构建 2.5D 纵深错觉。

## 动画法则与物理规律

代码中需体现专业的运动法则与物理自然感：

- **次要动作** (Secondary Action)：衣服、围巾或毛发随主运动飘动。
- **跟随动作** (Overlapping Action)：各关节间通过 `animation-delay` 设置时间差，避免所有部位同起同落。
- **挤压与拉伸** (Squash & Stretch)：展现质量感与弹性反馈。

> **Advanced Animation**
> See [references/motion-examples.md](references/motion-examples.md) for exact CSS implementations of Squash & Stretch, Overlapping Action, and exact easing parameters.

## 工作流与要求

遇到 SVG 动画生成需求时，你必须：

1. 分析角色的几何解构和色彩系统。
2. 拆解关键运动层次（背景层视差、前景主体）。
3. 构建具备完善 `xml` 头、`defs`、`style` 和 `g` 标签的分组。
4. **输出遵循结构模板的代码块。不要寒暄，直接输出包含完整内容的最终 SVG 代码块。**

## 代码结构模板 (Output Pattern)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="100%" height="100%">
  <!-- 聚合特效素材 -->
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="[HEX]" />
      <stop offset="100%" stop-color="[HEX]" />
    </linearGradient>
    <filter id="glow">...</filter>
  </defs>

  <!-- 聚合所有的核心动画逻辑 -->
  <style>
    /* CSS 控制关键动画与缓动 (CRITICAL: 必加 transform-box 兼容 Safari) */
    .bg-layer {
      animation: parallax 20s linear infinite;
    }
    .main-body {
      /* 必须定义中心点并绑定 fill-box 才能在各浏览器中精确居中旋转/缩放 */
      transform-box: fill-box;
      transform-origin: center center;
      /* 适当使用 cubic-bezier 增加真实物理张力 */
      animation: bounce 1.5s cubic-bezier(0.28, 0.84, 0.42, 1) infinite;
    }
    
    @keyframes bounce {
      0%, 100% { transform: translateY(0) scaleY(1); }
      50% { transform: translateY(-20px) scaleY(1.05); }
    }
    /* 追加其他跟随部位的 keyframes ... */
  </style>

  <!-- 远景：天空或最底色 -->
  <rect width="1200" height="800" fill="url(#bgGradient)" />

  <!-- 中景地貌层：通过层级实现视差移动 -->
  <g class="bg-layer" opacity="0.8">
    <!-- 背景元素片段 -->
  </g>

  <!-- 前景主角组：使用多层级嵌套 <g> 实现复杂关节控制 -->
  <!-- CRITICAL: 若组件有位移 transform="translate" 且受 CSS keyframes 控制，必须使用两层 <g> 拆分，外层做静态平移，内层绑定 CSS 动画，绝对防止冲突飞出画布。 -->
  <g transform="translate([X], [Y])">
    <g class="main-body">
      <!-- 子节点：带有延迟时间差的肢体，产生 Overlapping Action -->
      <path class="arm-left" style="animation-delay: -0.2s;" d="..." />
      <!-- 核心身体：承受主要 Squash & Stretch 动画 -->
      <path d="..." />
    </g>
  </g>
</svg>
```
