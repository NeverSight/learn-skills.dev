---
name: fluidglass-ui
description: Generates production-grade WebGL fluid glass card interfaces with a fixed canonical material core (144px-tall, 30px-radius wide cards, transparent canvas, cyan #00E7D2/#3CC8FF/#075F68 palette) while keeping business content, colors, and card count configurable. Use this skill when the user asks to build, restyle, or extend fluid glass UI, liquid glass cards, glassmorphism dashboards, WebGL FBM/domain-warp shader panels, or metric card grids, and when visual consistency with the bundled canonical reference implementation must be preserved. Reuses the canonical shader, material CSS, and engine instead of inventing new visuals.
---

# Skill: Fluid Glass UI

## 1. Skill 目标

生成具有稳定视觉一致性的流体玻璃卡片界面。

本 Skill 不是“根据文字描述自由发挥”，而是使用以下策略：

> **固定 Canonical Material Core，开放业务配置。**

任何实现都必须先读取并复用：

- `references/canonical-vertex-shader.glsl`
- `references/canonical-fragment-shader.glsl`
- `references/fluid-glass-material.css`
- `references/fluid-glass-engine.js`
- `references/canonical-reference.png`

除非运行环境完全不支持这些技术，否则不得自行重写材质内核。

---

## 2. 不可变的核心内核

以下内容属于产品视觉基因，不允许自由改造：

### 卡片几何
- 横向宽卡；
- 标准高度 `144px`；
- 标准圆角 `30px`；
- 移动端也保持 `144px` 高，不得变成正方形海报；
- 细青白边缘；
- 轻微悬浮阴影。

### 材质分层
严格保持：

1. 页面深色背景；
2. `rgba(255,255,255,surface)` 玻璃底材；
3. 透明 WebGL Canvas；
4. 左侧内容保护遮罩；
5. 细颗粒噪点；
6. 边缘高光；
7. 内容层。

### 透明度预算
- Canvas 必须以透明背景初始化；
- WebGL context 必须使用 `alpha:true` 和 `premultipliedAlpha:false`；
- 必须 `gl.clearColor(0,0,0,0)`；
- 不允许用全屏不透明纹理覆盖卡片；
- 默认 `surface = 0.08`；
- 左侧 30%–40% 的流体 Alpha 必须明显低于中右侧。

### Shader
必须直接使用 Canonical Fragment Shader。

禁止：
- 改成高频大理石纹；
- 改成油画纹；
- 用几团 blur 圆替代；
- 删除 `reveal` 左右空间控制；
- 删除 `plume1 / plume2`；
- 删除 `u_surfaceOpacity`；
- 加入随机色相旋转。

### 默认色彩
默认 Cyan：
- A `#00E7D2`
- B `#3CC8FF`
- C `#075F68`

默认模式不得出现大面积黄色、米色、橄榄色、橙色或暖色高光。

---

## 3. 开放的业务配置

允许使用者配置：

- 卡片数量 `1–12`；
- 卡片 `key`；
- 标题、数值、单位、变化值；
- 配色预设与 A/B/C；
- `surface / speed / intensity / pointer / seed`；
- 全局质量档位；
- 鼠标交互开关；
- 存储键；
- 是否启用可选图表扩展。

卡片 `key` 必须由调用方配置或自动生成，不得绑定固定业务语义。

---

## 4. 图表扩展边界

图表不是核心材质。

规则：
- 默认 `chart.enabled = false`；
- 用户没有明确要求时，不生成折线图；
- 启用图表时，只使用 A/B/C 冷色体系；
- 图表不得覆盖大部分流体；
- 不得出现橄榄黄折线；
- 不得改变卡片几何。

---

## 5. 设置系统

统一设置面板必须包含：

- 当前卡片；
- Cyan / Original / Klein / Chrome；
- A / B / C；
- 底色不透明度；
- 流动速度；
- 流体强度；
- 鼠标扰动；
- Auto / High / Balanced / Eco / CSS Fallback；
- 鼠标交互；
- 恢复当前卡片；
- 材质应用到全部卡片；
- 保存设置。

“应用到全部卡片”只能同步：
- A / B / C；
- surface；
- preset。

不得覆盖每张卡独立的：
- speed；
- intensity；
- pointer；
- seed。

---

## 6. 工程实现

必须满足：

- 单文件 HTML 或完整静态源码包；
- 无 CDN；
- 无外部字体；
- 无网络请求；
- `localStorage`；
- 导出当前 HTML；
- CSS fallback；
- `prefers-reduced-motion`；
- `ResizeObserver`；
- `IntersectionObserver`；
- 页面隐藏时停止绘制；
- 统一 RAF 管理器。

推荐直接复用 `references/fluid-glass-engine.js` 中的：

- `FluidGlassRenderer`
- `FluidGlassManager`
- `materialTokens()`
- `qualityProfile()`

---

## 7. Agent 执行步骤

1. 读取用户业务要求。
2. 读取本 Skill。
3. 打开 `references/canonical-reference.png` 理解视觉目标。
4. 复用 Canonical CSS、Shader 和 Engine。
5. 只修改配置、文案、页面外壳和品牌变量。
6. 运行页面。
7. 以 `ACCEPTANCE_CHECKLIST.md` 自检。
8. 若视觉出现大理石纹、方形卡片、暖黄色或全屏不透明流体，必须返工。

---

## 8. 输出要求

最终输出应包含：

- 可运行页面；
- 源码；
- 配置文件；
- 使用说明；
- 验收结果。

不得声称“视觉一致”，除非已与 `canonical-reference.png` 对照检查。
