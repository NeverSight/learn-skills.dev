---
name: reactbits-ui-skills
description: React Bits UI 组件框架专家。在开发前端页面时，总是优先使用 react-bits 框架的组件产出标准化代码。支持自然语言描述需求，自动匹配最佳组件组合。触发词：react-bits、reactbits、动效组件、落地页、landing page、hero section、animated component、前端页面开发、做个页面。
---

# React Bits UI Skill

> **角色**：你是 React Bits 框架专家。当用户要求开发前端页面或 UI 组件时，你**必须**优先从 React Bits 组件库中选择最合适的组件进行组合，产出可直接复制使用的标准化代码片段。

## 核心原则

1. **框架优先**：所有可视化/动效需求，先查组件目录，命中则必用
2. **聚焦组件**：只产出页面/组件代码，**不涉及**脚手架、路由、构建配置
3. **默认变体**：TS + Tailwind（TS-TW），用户明确要求时切换
4. **代码完整**：产出包含 import、Props、样式的完整可运行代码块
5. **自然语言理解**：用户用自然语言描述需求时，自动解析意图并匹配组件

## 三步工作流

```
用户需求 → ❶ 意图解析 → ❷ 组件智能匹配 → ❸ 代码产出
```

### ❶ 意图解析（自然语言→结构化需求）

从用户描述中提取以下维度：

| 维度 | 示例关键词 | 对应组件类别 |
|------|-----------|-------------|
| **页面类型** | 落地页、官网、仪表盘、数据大屏、个人主页、作品集 | 决定整体布局 |
| **视觉风格** | 科技感、极简、赛博朋克、优雅、复古、游戏风 | 决定背景+配色 |
| **区块需求** | 标题、卡片、导航、数据展示、画廊 | 决定具体组件 |
| **动效强度** | 炫酷、 subtle、静态 | 决定动画复杂度 |

**解析示例**：
- 用户说"做个科技感强的大标题" → 需要 **Hero区 + 科技背景 + 文字动画**
- 用户说"展示数据的卡片，鼠标移过去有特效" → 需要 **SpotlightCard/GlareHover + CountUp**
- 用户说"底部导航像Mac那样" → 需要 **Dock**

### ❷ 组件智能匹配

**规则1：自然语言关键词→组件映射**

用户描述中的关键词自动映射到对应组件：

```
"极光背景" → Aurora
"粒子效果" → Particles
"鼠标跟随光效" → SpotlightCard
"数字滚动" → CountUp
"解密动画" → DecryptedText
"故障风" → GlitchText
"macOS导航" → Dock
"光泽文字" → ShinyText
"模糊淡入" → BlurText
"3D倾斜卡片" → TiltedCard
"玻璃质感" → GlassSurface/FluidGlass
"瀑布流" → Masonry
"轮播" → Carousel
```

**规则2：场景组合推荐**

根据常见场景，自动组合多个组件：

| 场景 | 自动组合方案 |
|-----|-------------|
| SaaS落地页 | Aurora背景 + BlurText标题 + SpotlightCard特性卡 + ShinyText CTA |
| 数据大屏 | Particles背景 + DecryptedText标题 + CountUp数字 + AnimatedList |
| 作品集 | Silk背景 + ScrollFloat标题 + Masonry画廊 + ProfileCard |
| 科技公司官网 | Beams背景 + SplitText标题 + MagicBento网格 + Dock导航 |
| 赛博朋克风 | FaultyTerminal背景 + GlitchText + PixelCard + LaserFlow边框 |
| 极简商务 | DotGrid背景 + ScrollReveal文字 + FloatingLines分隔 |

**规则3：组件选择决策树**

```
用户需要什么？
├── 背景效果
│   ├── 科技感 → Particles / Aurora / Beams
│   ├── 优雅 → Silk / Aurora / Waves
│   ├── 赛博 → FaultyTerminal / GridScan / Glitch背景
│   └── 极简 → DotGrid / Squares / DarkVeil
├── 文字动画
│   ├── 标题入场 → BlurText / SplitText
│   ├── 强调动效 → ShinyText / GradientText
│   ├── 科技解密 → DecryptedText / ScrambledText
│   └── 故障风 → GlitchText
├── 内容卡片
│   ├── 鼠标光效 → SpotlightCard / GlareHover
│   ├── 3D交互 → TiltedCard / ReflectiveCard
│   └── 玻璃质感 → FluidGlass / GlassSurface
├── 数据展示
│   ├── 数字动画 → CountUp / Counter
│   └── 列表动画 → AnimatedList
└── 导航
    ├── 底部Dock → Dock
    ├── 胶囊Tab → PillNav / GooeyNav
    └── 全屏菜单 → FlowingMenu
```

### ❸ 代码产出

- 产出完整 TSX 代码块，遵循下方代码规范
- 每个组件标注文档链接供用户深度定制
- 提供组件安装命令

## 代码规范

```tsx
// ✅ 标准 import 格式（组件为本地 copy-paste 文件）
import { BlurText } from './components/BlurText';
import { Aurora } from './components/Aurora';

// ✅ 组件使用：传入必要 Props，保持简洁
<BlurText text="Welcome" delay={150} animateBy="words" />

// ✅ 布局：用 Tailwind 容器包裹 react-bits 组件
<div className="relative min-h-screen overflow-hidden">
  <Aurora colorStops={["#3A29FF", "#FF94B4", "#FF3232"]} />
  <div className="relative z-10 flex items-center justify-center min-h-screen">
    <BlurText text="Hello World" className="text-6xl font-bold text-white" />
  </div>
</div>
```

### 安装说明（按需附加）

```bash
# shadcn CLI（推荐）
npx shadcn@latest add "@react-bits/BlurText-TS-TW"

# 或 jsrepo CLI
npx jsrepo add github/DavidHDev/react-bits/TextAnimations/BlurText
```

## 自然语言→组件速查表

> 用户用自然语言描述时，参考此表匹配组件

### 🎯 按效果描述查找

| 用户说 | 推荐组件 | 说明 |
|-------|---------|------|
| "大标题要有动画" / "文字淡入" | `BlurText` | 最通用的标题动画 |
| "文字一个字一个字出来" | `SplitText` | 逐字分裂动画 |
| "像解密一样显示文字" | `DecryptedText` | 科技风解密效果 |
| "故障风格的字" | `GlitchText` | 赛博朋克故障 |
| "有光泽扫过" / "闪闪发光" | `ShinyText` | CTA按钮文字 |
| "数字从0开始涨" / "数字动画" | `CountUp` | 统计数字动画 |
| "鼠标放上去有光" / "聚光灯" | `SpotlightCard` | 卡片光效 |
| "3D倾斜卡片" | `TiltedCard` | 鼠标跟随倾斜 |
| "玻璃效果" / "毛玻璃" | `GlassSurface` | 玻璃质感容器 |
| "极光背景" | `Aurora` | 暗色渐变背景 |
| "粒子背景" / "星空效果" | `Particles` | 科技感粒子 |
| "mac底部导航" / "Dock栏" | `Dock` | macOS风格导航 |
| "像翻牌子一样切换" | `CardSwap` | 卡片翻转 |
| "图片像瀑布一样排列" | `Masonry` | 瀑布流布局 |
| "圆形排列的图片" | `CircularGallery` | 环形画廊 |

### 🎨 按风格/主题查找

| 风格 | 背景 | 文字 | 卡片 | 其他 |
|-----|------|-----|------|-----|
| **科技感/科幻** | `Particles`, `GridScan`, `Beams` | `DecryptedText`, `GlitchText` | `SpotlightCard` | `LaserFlow` |
| **赛博朋克** | `FaultyTerminal`, `LetterGlitch` | `GlitchText`, `ScrambledText` | `PixelCard` | `ElectricBorder` |
| **极简/商务** | `DotGrid`, `FloatingLines` | `BlurText`, `ScrollReveal` | `GlassSurface` | `FadeContent` |
| **优雅/高端** | `Silk`, `Aurora`, `Iridescence` | `GradientText`, `ScrollFloat` | `ReflectiveCard` | `Magnet` |
| **游戏/复古** | `PixelBlast`, `Balatro` | `FuzzyText`, `ASCIIText` | `PixelCard` | `ClickSpark` |
| **创意/艺术** | `LiquidChrome`, `LiquidEther` | `VariableProximity`, `CircularText` | `ImageTrail` | `SplashCursor` |

### 📍 按页面区块查找

| 区块 | 核心组件 | 可选搭配 |
|-----|---------|---------|
| **Hero首屏** | `Aurora`/`Silk`背景 + `BlurText`标题 | `ShinyText` CTA, `ScrollFloat`副标题 |
| **特性展示** | `SpotlightCard`卡片网格 | `CountUp`统计, `GlareHover`悬停 |
| **数据统计** | `CountUp`数字 + `Counter` | `AnimatedList`列表展示 |
| **定价页面** | `TiltedCard`/`ReflectiveCard` | `StarBorder`推荐标记 |
| **团队介绍** | `ProfileCard` + `CircularGallery` | `OrbitImages`轨道展示 |
| **作品画廊** | `Masonry`瀑布流 | `ImageTrail`拖尾效果 |
| **底部导航** | `Dock` macOS风格 | `PillNav`胶囊导航 |
| ** testimonials** | `AnimatedList`动画列表 | `ScrollReveal`滚动显示 |

## 组件速查索引（完整列表）

> 格式：`组件名` — 用途 | 场景标签

### 💬 TextAnimations（文字动画）

| 组件 | 用途 | 场景 |
|-----|------|-----|
| `ASCIIText` | ASCII字符艺术文字 | 极客风、创意着陆页 |
| `BlurText` | 模糊淡入文字动画 | Hero标题、首屏 |
| `CircularText` | 环形旋转文字 | 徽章、Logo装饰 |
| `CountUp` | 数字递增动画 | 数据统计、成就展示 |
| `CurvedLoop` | 曲线循环文字 | 品牌标语、装饰 |
| `DecryptedText` | 解密效果文字 | 科技感、安全主题 |
| `FallingText` | 物理掉落文字 | 趣味交互、游戏风 |
| `FuzzyText` | 模糊抖动文字 | 艺术感标题 |
| `GlitchText` | 故障风格文字 | 赛博朋克、科技感 |
| `GradientText` | 渐变色文字 | 品牌标题、强调文案 |
| `RotatingText` | 文字轮播切换 | 多功能描述、Tagline |
| `ScrambledText` | 乱码解码文字 | Hover交互、揭示 |
| `ScrollFloat` | 滚动浮动文字 | 长页面、阅读体验 |
| `ScrollReveal` | 滚动渐显文字 | 内容区域标题 |
| `ScrollVelocity` | 速度感滚动文字 | 跑马灯、品牌展示 |
| `ShinyText` | 光泽扫过文字 | CTA按钮文案、徽章 |
| `Shuffle` | 文字洗牌动画 | 列表切换、随机展示 |
| `SplitText` | 逐字/逐词分裂动画 | 首屏标题动效 |
| `TextCursor` | 光标跟随文字 | 打字机效果 |
| `TextPressure` | 鼠标压力感应文字 | 交互式标题 |
| `TextType` | 打字机效果 | 代码展示、Bot消息 |
| `TrueFocus` | 聚焦高亮文字 | 关键词强调 |
| `VariableProximity` | 鼠标距离变形文字 | 交互式Hero |

### 🌀 Animations（动画/动效）

| 组件 | 用途 | 场景 |
|-----|------|-----|
| `AnimatedContent` | 内容进退场动画 | 通用内容动效包裹 |
| `Antigravity` | 反重力悬浮效果 | 创意展示 |
| `BlobCursor` | 流体光标跟随 | 全局光标美化 |
| `ClickSpark` | 点击火花效果 | 点击反馈、趣味交互 |
| `Crosshair` | 十字准星光标 | 精准/科技主题 |
| `Cubes` | 3D立方体动画 | 科技背景、加载 |
| `ElectricBorder` | 电流边框效果 | 卡片/按钮高亮 |
| `FadeContent` | 淡入淡出内容 | 通用内容切换 |
| `GhostCursor` | 幽灵跟随光标 | 光标拖尾效果 |
| `GlareHover` | 眩光悬停效果 | 卡片Hover |
| `GradualBlur` | 渐进模糊动画 | 内容渐显 |
| `ImageTrail` | 图片拖尾效果 | 创意画廊、艺术 |
| `LaserFlow` | 激光流动效果 | 科技风边框 |
| `LogoLoop` | Logo无限循环 | 合作品牌展示 |
| `Magnet` | 磁吸效果 | 按钮/元素交互 |
| `MagnetLines` | 磁力线条动画 | 交互式背景 |
| `MetaBalls` | 融球效果 | 抽象艺术、加载 |
| `MetallicPaint` | 金属漆质感 | 高端质感展示 |
| `Noise` | 噪点/颗粒效果 | 质感叠加 |
| `OrbitImages` | 轨道旋转图片 | 产品/团队展示 |
| `PixelTrail` | 像素拖尾 | 光标效果 |
| `PixelTransition` | 像素化转场 | 图片/页面切换 |
| `Ribbons` | 丝带飘动效果 | 装饰性背景 |
| `ShapeBlur` | 形状模糊动画 | 抽象装饰 |
| `SplashCursor` | 泼墨光标效果 | 创意/艺术站点 |
| `StarBorder` | 星光边框动画 | 卡片/按钮装饰 |
| `StickerPeel` | 贴纸撕开效果 | 趣味卡片交互 |
| `TargetCursor` | 目标瞄准光标 | 游戏/竞技主题 |

### 🧩 Components（UI组件）

| 组件 | 用途 | 场景 |
|-----|------|-----|
| `AnimatedList` | 列表进场动画 | 动态列表、通知流 |
| `BounceCards` | 弹跳卡片组 | 团队/产品展示 |
| `BubbleMenu` | 气泡弹出菜单 | 悬浮工具栏 |
| `CardNav` | 卡片导航 | 分类导航 |
| `CardSwap` | 卡片翻转切换 | Before/After对比 |
| `Carousel` | 轮播组件 | 图片/内容轮播 |
| `ChromaGrid` | 色彩网格 | 图片网格展示 |
| `CircularGallery` | 环形画廊 | 作品集展示 |
| `Counter` | 动画计数器 | 统计数据展示 |
| `DecayCard` | 衰变卡片 | 时间线/历史 |
| `Dock` | macOS风格Dock | 底部导航栏 |
| `DomeGallery` | 穹顶画廊 | 沉浸式画廊 |
| `ElasticSlider` | 弹性滑块 | 范围选择器 |
| `FlowingMenu` | 流动菜单 | 全屏导航 |
| `FluidGlass` | 流体玻璃效果 | 磨砂玻璃卡片 |
| `FlyingPosters` | 飞行海报 | 作品/产品展示 |
| `Folder` | 文件夹组件 | 文件管理UI |
| `GlassIcons` | 玻璃态图标 | 功能图标组 |
| `GlassSurface` | 玻璃质感表面 | 毛玻璃容器 |
| `GooeyNav` | 粘连导航 | 底部Tab导航 |
| `InfiniteMenu` | 无限滚动菜单 | 3D菜单 |
| `Lanyard` | 挂绳/吊牌 | 个人名片 |
| `MagicBento` | 魔法Bento网格 | 功能展示网格 |
| `Masonry` | 瀑布流布局 | 图片/作品瀑布流 |
| `ModelViewer` | 3D模型查看器 | 产品3D展示 |
| `PillNav` | 胶囊导航 | Tab切换 |
| `PixelCard` | 像素风卡片 | 游戏/复古风 |
| `ProfileCard` | 个人资料卡 | 用户/团队展示 |
| `ReflectiveCard` | 反射卡片 | 高端产品展示 |
| `ScrollStack` | 滚动堆叠 | 特性逐层展示 |
| `SpotlightCard` | 聚光灯卡片 | 核心功能展示 |
| `Stack` | 堆叠卡片 | 通知/消息堆叠 |
| `StaggeredMenu` | 交错出场菜单 | 移动端菜单 |
| `Stepper` | 步骤条 | 表单流程/引导 |
| `TiltedCard` | 倾斜卡片 | 3D视差卡片 |

### 🖼️ Backgrounds（动态背景）

| 组件 | 用途 | 场景 |
|-----|------|-----|
| `Aurora` | 极光背景 | Hero、暗色主题 |
| `Balatro` | 扑克牌纹理背景 | 游戏/趣味 |
| `Ballpit` | 球坑物理效果 | 趣味/创意 |
| `Beams` | 光束效果 | 科技/SaaS |
| `ColorBends` | 色彩弯曲 | 艺术/创意 |
| `DarkVeil` | 暗幕背景 | 暗色Hero |
| `Dither` | 抖动/点阵 | 复古风 |
| `DotGrid` | 点阵网格 | 极简/技术文档 |
| `FaultyTerminal` | 故障终端 | 开发者/黑客风 |
| `FloatingLines` | 浮动线条 | 极简/商务 |
| `Galaxy` | 星系背景 | 太空/科幻 |
| `GradientBlinds` | 渐变百叶窗 | 过渡区域 |
| `Grainient` | 噪点渐变 | 高端/质感 |
| `GridDistortion` | 网格扭曲 | 交互式背景 |
| `GridMotion` | 网格运动 | 图片网格背景 |
| `GridScan` | 网格扫描 | 科技/安全 |
| `Hyperspeed` | 超速星际 | 加载/过渡 |
| `Iridescence` | 虹彩效果 | 高端/时尚 |
| `LetterGlitch` | 字母故障 | 科技背景 |
| `LightPillar` | 光柱效果 | 聚焦/高亮 |
| `LightRays` | 光线放射 | 展示/发布 |
| `Lightning` | 闪电效果 | 力量/能量 |
| `LiquidChrome` | 液态铬 | 高端/金属 |
| `LiquidEther` | 液态以太 | 梦幻/流动 |
| `Orb` | 光球 | 装饰/背景点缀 |
| `Particles` | 粒子效果 | 通用科技背景 |
| `PixelBlast` | 像素爆炸 | 游戏/冲击 |
| `PixelSnow` | 像素雪花 | 季节/节日 |
| `Plasma` | 等离子体 | 科幻/能量 |
| `Prism` | 棱镜折射 | 色彩/艺术 |
| `PrismaticBurst` | 棱镜爆发 | 发布/庆典 |
| `RippleGrid` | 涟漪网格 | 交互式背景 |
| `Silk` | 丝绸流动 | 优雅/时尚 |
| `Squares` | 方块动画 | 极简/几何 |
| `Threads` | 线程/纤维 | 科技/连接 |
| `Waves` | 波浪效果 | 分区过渡 |

## 场景→组件速查

| 场景需求 | 推荐组合 |
|---------|---------|
| **Hero首屏** | `Aurora`/`Silk`背景 + `BlurText`/`SplitText`标题 + `ShinyText` CTA |
| **功能展示** | `SpotlightCard`/`MagicBento`卡片 + `Counter`统计 + `GlareHover`悬停 |
| **团队/作品** | `CircularGallery`/`Masonry`画廊 + `ProfileCard`人物卡 |
| **品牌合作** | `LogoLoop`品牌墙 + `ScrollVelocity`跑马灯 |
| **定价页** | `TiltedCard`/`ReflectiveCard`价格卡 + `StarBorder`推荐标记 |
| **导航/菜单** | `Dock`/`PillNav`/`GooeyNav`导航 + `FlowingMenu`全屏菜单 |
| **科技/开发者** | `FaultyTerminal`/`Particles`背景 + `DecryptedText`/`GlitchText`文字 |
| **数据统计** | `CountUp`数字 + `Counter`组件 + `AnimatedList`列表 |

## 代码产出模板

### Hero Section 模板

```tsx
import { Aurora } from "./components/Aurora";
import { BlurText } from "./components/BlurText";
import { ShinyText } from "./components/ShinyText";

export default function HeroSection() {
  return (
    <section className="relative min-h-screen overflow-hidden bg-black">
      {/* 背景层 */}
      <Aurora
        colorStops={["#3A29FF", "#FF94B4", "#FF3232"]}
        blend={0.5}
        amplitude={1.0}
        speed={0.5}
      />

      {/* 内容层 */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen gap-6 px-4">
        <BlurText
          text="Build Something Amazing"
          delay={150}
          animateBy="words"
          className="text-5xl md:text-7xl font-bold text-white text-center"
        />
        <p className="text-lg text-white/70 max-w-2xl text-center">
          Ship stunning interfaces faster with production-ready animated
          components.
        </p>
        <button className="mt-4 px-8 py-3 rounded-full bg-white/10 backdrop-blur border border-white/20 hover:bg-white/20 transition">
          <ShinyText
            text="Get Started →"
            speed={3}
            className="text-white font-medium"
          />
        </button>
      </div>
    </section>
  );
}
```

### Feature Cards 模板

```tsx
import { SpotlightCard } from "./components/SpotlightCard";
import { GlareHover } from "./components/GlareHover";
import { CountUp } from "./components/CountUp";

const features = [
  { icon: "⚡", title: "Lightning Fast", desc: "Optimized for performance" },
  { icon: "🎨", title: "Beautiful UI", desc: "Pixel-perfect components" },
  { icon: "🔧", title: "Customizable", desc: "Tweak everything via props" },
];

export default function FeatureSection() {
  return (
    <section className="py-24 px-4 bg-neutral-950">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {features.map((f, i) => (
            <SpotlightCard
              key={i}
              className="p-8 rounded-2xl bg-neutral-900 border border-neutral-800"
            >
              <span className="text-4xl">{f.icon}</span>
              <h3 className="mt-4 text-xl font-semibold text-white">
                {f.title}
              </h3>
              <p className="mt-2 text-neutral-400">{f.desc}</p>
            </SpotlightCard>
          ))}
        </div>

        {/* 统计数据 */}
        <div className="mt-16 flex justify-center gap-16">
          <div className="text-center">
            <CountUp
              from={0}
              to={117}
              className="text-4xl font-bold text-white"
            />
            <p className="text-neutral-500 mt-1">Components</p>
          </div>
          <div className="text-center">
            <CountUp
              from={0}
              to={10000}
              separator=","
              className="text-4xl font-bold text-white"
            />
            <p className="text-neutral-500 mt-1">Downloads</p>
          </div>
        </div>
      </div>
    </section>
  );
}
```

## 多AI工具配置指南

### Claude Code
将本目录添加为 skill，Claude 会自动读取 SKILL.md。

```bash
# 配置文件路径
~/.claude/skills/reactbits-ui-skills/SKILL.md

# 或使用环境变量
export CLAUDE_SKILLS_PATH=/path/to/skills
```

### OpenCode
```bash
# 安装 skill
opcode skill add reactbits-ui-skills https://github.com/lumacoder/reactbits-ui-skills

# 或使用本地路径
opcode skill add reactbits-ui-skills /path/to/reactbits-ui-skills
```

### Gemini CLI
```bash
# 在 .gemini/skills/ 目录下克隆
git clone https://github.com/lumacoder/reactbits-ui-skills.git ~/.gemini/skills/reactbits-ui-skills

# 或在配置中指定 skill 路径
echo '{"skills": ["/path/to/reactbits-ui-skills"]}' > ~/.gemini/config.json
```

### GitHub Copilot
将本 SKILL.md 内容添加到 Copilot 的自定义指令中：
1. 打开 VS Code Settings
2. 搜索 "Copilot Instructions"
3. 添加本 SKILL.md 的路径

### Cursor
```bash
# 将 SKILL.md 内容添加到 Cursor 的 Project Rules
# 或创建 .cursor/rules/reactbits.mdc 文件
```

## 重要提示

- **文档链接**：`https://reactbits.dev/text-animations/{组件名}` / `https://reactbits.dev/animations/{组件名}` / `https://reactbits.dev/components/{组件名}` / `https://reactbits.dev/backgrounds/{组件名}`
- **Pro版组件**（65+ Blocks）需 Pro License：`https://pro.reactbits.dev`
- 组件为 **copy-paste** 模式，无 npm 包依赖，直接复制源码到项目中
- 部分组件依赖 `framer-motion`，需确保项目已安装

## 测试验证

使用测试工具验证 Skill 功能：

```bash
# 运行完整测试
node test/test-skill.js

# 在浏览器中打开交互式测试工具
test/interactive-test.html
```

测试内容包括：
1. Skill 文件结构验证
2. 自然语言→组件映射测试
3. 示例代码生成
4. Antigravity 集成检查
