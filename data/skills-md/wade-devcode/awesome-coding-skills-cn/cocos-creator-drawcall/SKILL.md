---
name: cocos-creator-drawcall
description: 优化 Cocos Creator 渲染性能时使用。合批、图集、动静分离、Label。
category: gamedev
tags: [cocoscreator, 性能, drawcall]
---

# Cocos Creator 降 DrawCall

## 何时用

- 游戏在中低端机上帧率不稳，用 DrawCall 面板发现每帧 DrawCall 超过 100+ 时。
- 增加了若干 UI 节点后帧率明显下降，怀疑合批被打断时。
- UI 图片散布在多个独立贴图文件，没有合并图集时。
- 场景里有频繁移动/变色的动态节点和大量静态 UI 混排，导致静态内容也每帧重绘时。
- 动态文本（计分、倒计时）用了系统字体，导致每个 Label 都是独立 DrawCall 时。

## 核心规则

### 1. 合批条件：同材质 + 同贴图 + 连续层级，缺一不可

**规则：** Cocos Creator 3.x 的自动合批（Auto Batching）要求相邻渲染节点使用完全相同的材质实例和贴图，且在渲染树中是连续的兄弟节点；只要中间插入一个使用不同贴图的节点，从该节点开始就会打断合批，之前和之后的节点各自成为独立批次。

**为什么：** AI 生成 UI 布局时完全不考虑渲染顺序，喜欢按逻辑语义组织节点层级：把背景、图标、文字、特效各自放一层，每层里再嵌套子节点。这种结构在视觉上没问题，但渲染时背景（图集A）→ 图标（图集B）→ 文字（Label 单独纹理）→ 特效（序列帧图集C）来回切换贴图，每切换一次就是一次新的 DrawCall，最终一个看起来简单的卡片 UI 产生了 8 个 DrawCall。新手以为"用了同一个图集就能合批"，却不知道中间穿插了一个不同材质的节点就已经把批次切断了，从 DrawCall 面板看到的批次数远超预期。

**怎么做：**
- 用 Creator 编辑器的 **Render Batches 面板**（菜单 Scene → Show Batches），直观看到哪些节点形成了一批，哪里发生了断批。
- 把使用同一图集的节点在层级面板中排列为连续兄弟节点，使用不同材质的节点（特效、粒子）移到最顶层或最底层，集中放置减少切换次数。
- 避免在同材质节点序列中间插入 `Mask` 组件节点——`Mask` 会强制开启模板测试，打断合批。
- 合批验证：在 Profile 模式下运行，对比增减节点前后的 DrawCall 数，用数字而非感觉确认合批效果。

---

### 2. 图集：同屏 UI 精灵打入同一图集，权衡尺寸与内存

**规则：** 同一个界面（大厅、战斗 HUD、商店）内频繁出现的精灵必须合并到同一张图集；图集尺寸控制在 1024×1024（中端机）或 2048×2048（高端机），超出则拆分多张；不同界面的独占图集在切换界面时及时释放。

**为什么：** 没有图集是 DrawCall 爆炸最直接的原因：100 个 UI 图片分别存为独立 PNG，渲染时每个图片一次 DrawCall，哪怕它们相邻、同材质，贴图句柄不同就无法合批。AI 生成美术资源管理代码时几乎从不提图集，直接 `resources.load("sprites/icon_1")` 逐个加载散图。另一个常见错误是图集做得过大：一张 4096×4096 的图集在中端安卓机上加载耗时 200~400ms，且常驻 64MB GPU 内存，换来的收益是减少了几个 DrawCall——完全不划算。图集尺寸要根据目标机型 GPU 内存上限精心规划。

**怎么做：**
- 在 Creator 编辑器中，选中存放精灵的文件夹 → 右键 → 「创建图集（Auto Atlas）」，配置最大尺寸和间距，构建时自动合图。
- 按界面分组：`hall_atlas`（大厅界面全部图标）、`battle_hud_atlas`（战斗 HUD）、`common_atlas`（全局通用小图标），不同界面图标不混打。
- 检查图集使用率（Creator Build 日志会输出各图集填充率），填充率低于 60% 的两张图集考虑合并，避免浪费内存。
- 大图（全屏背景、loading 图）单独存放，不入图集——它们本身就是独立 DrawCall，入图集反而浪费图集空间。

---

### 3. 动静分离：频繁变动节点与静态节点分层，防止静态内容被迫重绘

**规则：** 在 Cocos Creator 3.x 中，将完全静态的 UI 节点（不会移动、不会变色、不会显隐）与动态节点（血条、计分、移动角色）放在不同的渲染层；静态层节点上开启 `Static Batching`（或确保其 transform 从不改变），让引擎对静态批次做缓存而不是每帧重建。

**为什么：** Creator 3.x 的渲染器在每帧构建渲染批次时，只要某个节点的 transform 或颜色发生变化，该批次内的所有节点都需要重新提交顶点数据。如果把每秒更新 10 次的血量进度条和永远不动的背景装饰放在同一个合批组里，背景装饰每秒也被强制重新提交 10 次——本来可以被完全跳过的工作变成了持续的 CPU/GPU 负担。AI 不了解这一批次失效机制，倾向于按视觉层次（背景在下、前景在上）组织节点，把静态装饰和动态元素紧密交叉放置。

**怎么做：**
- 节点树结构：
  ```
  Canvas
  ├── StaticLayer      ← 所有永不变化的背景、装饰、边框
  │   └── (静态精灵群，使用同一图集，可合批)
  ├── DynamicLayer     ← 血条、计分、角色动画
  │   └── (动态节点，允许每帧更新)
  └── EffectLayer      ← 粒子、特效（独立材质，放最顶层集中切换）
  ```
- `StaticLayer` 下的节点在运行时绝对不调用 `setPosition`、`setRotation`、修改 `color`，否则失去静态缓存价值。
- Creator 3.x 场景图标静态节点上勾选 `Is Static`（Properties 面板），引擎会在构建时烘焙这些节点的合批，运行时不再每帧重建。
- 节点 `active` 切换也会使批次失效，静态层节点宁可用 `opacity = 0` 代替 `active = false`（但注意 opacity = 0 仍然参与渲染，不适用于需要彻底关闭的情况；权衡后选择）。

---

### 4. Label 优化：动态文本用 CHAR 缓存或 BMFont，避免系统字体每次重排

**规则：** 频繁更新的动态 Label（倒计时、伤害数字、计分）使用 `CHAR` cache mode 或 BMFont；装饰性静态文字（标题、按钮固定文字）使用 `BITMAP` cache mode；绝不在高频更新的 Label 上使用 `NONE` cache mode 或系统字体，尤其禁止在 `update` 里每帧更新系统字体 Label。

**为什么：** `Label` 在 Creator 中是最容易被忽视的 DrawCall 杀手。使用系统字体（TTF）且 cache mode 为 `NONE` 时，每次修改 `string` 都会触发一次 Canvas 2D 重新排版、重新生成纹理，生成的纹理是独立的，无法与任何 Sprite 合批，每个这样的 Label 就是一个独立 DrawCall。战斗界面里若有 10 个敌人头顶的血量数字（系统字体），就是 10 个永远无法合批的 DrawCall，还带着每帧 CPU Canvas 重排的额外开销。BMFont 的文字以精灵图集形式存在，能与同图集的 UI 精灵合批，是最优解。CHAR mode 缓存已用字符的纹理，字符数量稳定后可以合批，适合动态内容。

**怎么做：**
- **BMFont**（最优）：美术制作字符图集，在 Creator 里创建 `BitmapFont` 资源，Label 的 Font 属性指向 BMFont，cache mode 设 `NONE`（BMFont 本身已是精灵图集，不需要额外 cache）。
- **CHAR mode**（动态数字/文字）：`label.cacheMode = Label.CacheMode.CHAR`，引擎把用过的字符缓存进共享纹理，相同字体+字号的多个 Label 共享同一纹理，可合批。
- **BITMAP mode**（静态装饰文字）：`label.cacheMode = Label.CacheMode.BITMAP`，整个 Label 渲染成一张纹理，之后不再重排，适合标题等不会改变的文本。
- 严禁在 `update` 里每帧给系统字体 Label 赋值；若不可避免要更新，至少做 dirty 检查：`if (this._lastHp !== hp) { this.hpLabel.string = String(hp); this._lastHp = hp; }`。

---

### 5. 工具验证：用 DrawCall 面板和 Frame Debugger 确认合批真实生效

**规则：** 所有 DrawCall 优化必须用工具数字验证，不凭感觉或"应该合批了"的推断交付；在编辑器 Preview 模式下打开 **Render Batches 面板**查看实时批次；在原生平台用 **RenderDoc**（Android）或 **Xcode Frame Debugger**（iOS）逐 DrawCall 分析实际 GPU 指令。

**为什么：** 这是 DrawCall 优化里被 AI 和新手最彻底忽视的一步。"我把图标都放进了同一个图集，DrawCall 应该减少了"——这句话里有太多可能出错的地方：图集打包设置里最大尺寸太小导致图标被拆到了两张图集；某个图标被意外加了 `Mask`；动态节点被插入了静态群中间。不用工具验证，所有这些失误都无法被发现。AI 生成优化方案时更不会主动说"请用 DrawCall 面板确认一下"，导致工程师以为优化已完成，实际效果为零。

**怎么做：**
- 编辑器 Preview：打开 **Stats 面板**（右上角 Stats 按钮），实时观察 DrawCall 数字变化；切换到 **Render Batches 面板**，选中节点时高亮它所在的批次。
- 优化前后对比流程：记录优化前 DrawCall 基准数 → 应用优化 → 记录优化后数字 → 计算降幅；降幅不符合预期时逐一排查合批条件（贴图、材质、层级顺序）。
- 原生平台验证：Android 接入 RenderDoc，抓帧后在 Event Browser 里逐 Draw Call 查看调用的纹理和 Shader，直接定位是哪个节点破坏了合批。
- 设定性能预算：目标机型上 DrawCall ≤ 50（UI 密集场景）或 ≤ 100（3D 场景+UI），超出预算立即优化，不拖到上线前。

---

## 正例 / 反例

### 反例：散图 + 节点层级混乱打断合批 + 系统字体每帧重排

```typescript
// 反例 — 散图精灵、动静混排、系统字体每帧更新
@ccclass
export class BattleHUD extends Component {
    @property(Sprite) iconAttack: Sprite = null!;   // ❌ 独立 PNG，独立 DrawCall
    @property(Sprite) iconDefense: Sprite = null!;  // ❌ 独立 PNG，独立 DrawCall
    @property(Sprite) iconHP: Sprite = null!;       // ❌ 独立 PNG，独立 DrawCall
    @property(Label) hpLabel: Label = null!;        // ❌ 系统字体，NONE mode
    @property(Label) atkLabel: Label = null!;       // ❌ 系统字体，NONE mode

    private _hp = 100;

    update(dt: number) {
        // ❌ 每帧给系统字体 Label 赋值，每次触发 Canvas 重排 + 新纹理
        this.hpLabel.string = "HP: " + this._hp;
        this.atkLabel.string = "ATK: " + this._atk;
        // ❌ 3 个散图图标 + 2 个系统字体 Label = 至少 5 个 DrawCall，且无法合批
    }
}
```

```typescript
// 正例 — 图集合批 + 动静分离 + CHAR mode + dirty 检查
@ccclass
export class BattleHUD extends Component {
    // ✅ 图标全部来自同一图集（hud_atlas），三个精灵可合批为 1 个 DrawCall
    @property(Sprite) iconAttack: Sprite = null!;
    @property(Sprite) iconDefense: Sprite = null!;
    @property(Sprite) iconHP: Sprite = null!;

    // ✅ Label 使用 CHAR cache mode，动态数字字符缓存后可合批
    @property(Label) hpLabel: Label = null!;
    @property(Label) atkLabel: Label = null!;

    private _hp = 100;
    private _atk = 50;
    private _lastHp = -1;
    private _lastAtk = -1;

    onLoad() {
        // ✅ 确认 Label 使用 CHAR mode（也可在编辑器 Inspector 里设置）
        this.hpLabel.cacheMode = Label.CacheMode.CHAR;
        this.atkLabel.cacheMode = Label.CacheMode.CHAR;
    }

    // ✅ 事件驱动更新，不在 update 轮询
    onHpChanged(newHp: number) {
        if (this._lastHp === newHp) return; // ✅ dirty 检查，值未变不重排
        this._lastHp = newHp;
        this.hpLabel.string = String(newHp); // ✅ 只赋值数字，不拼"HP: "前缀（前缀用 BMFont 静态 Label）
    }

    onAtkChanged(newAtk: number) {
        if (this._lastAtk === newAtk) return;
        this._lastAtk = newAtk;
        this.atkLabel.string = String(newAtk);
    }
}
```

---

### 反例：静态装饰与动态角色混排，每帧全部重提交

```
// 反例 — 节点层级结构（伪代码）
Canvas
└── GameLayer
    ├── Background_Sprite       (图集A，静态)
    ├── Player_Spine            (Spine 动画，每帧更新) ← ❌ 插在静态节点中间，打断合批
    ├── Decoration_Sprite_1     (图集A，静态)          ← ❌ 被 Player 打断，无法与 Background 合批
    ├── Decoration_Sprite_2     (图集A，静态)
    └── HP_ProgressBar          (图集B，每帧更新)
// 结果：Background(1) + Player(1) + Decoration×2(2) + HP(1) = 5 DrawCall
// 正确分层后：StaticLayer合批(1) + DynamicLayer(2) = 3 DrawCall
```

```typescript
// 正例 — 动静分离节点结构，静态节点连续合批
@ccclass
export class GameScene extends Component {
    @property(Node) staticLayer: Node = null!;   // ✅ 背景、装饰，永不修改 transform
    @property(Node) dynamicLayer: Node = null!;  // ✅ 角色、血条，允许每帧更新
    @property(Node) effectLayer: Node = null!;   // ✅ 粒子、Spine，独立材质集中放顶层

    onLoad() {
        // ✅ 运行时不对 staticLayer 的子节点做任何 transform 修改
        // ✅ staticLayer 内所有节点来自同一图集 → 合批为 1 个 DrawCall
        // ✅ dynamicLayer 内角色和血条 → 各自独立 DrawCall 但数量可控
        // ✅ effectLayer 内特效 → 材质特殊，放顶层避免切换穿插 staticLayer
    }
}
```

---

## 自查清单

- [ ] 用 Render Batches 面板确认同一图集的相邻精灵形成了同一批次，数字有改善（非猜测）。
- [ ] 同一界面内频繁出现的图标/精灵已打入同一图集，没有散落的独立 PNG 参与渲染。
- [ ] 静态 UI 节点（背景、装饰）与动态节点（血条、动画）分层放置，`StaticLayer` 下节点运行时不修改 transform/color。
- [ ] 动态 Label（数字、倒计时）使用 `CHAR` cache mode 或 BMFont，没有系统字体 + NONE mode 的动态 Label 在 `update` 里每帧赋值。
- [ ] `Mask` 组件节点已检查，没有意外插入连续精灵序列中间打断合批。
- [ ] 原生平台用 RenderDoc 或 Xcode Frame Debugger 抓帧，逐 DrawCall 确认贴图切换次数符合预期。
- [ ] 设定了目标机型的 DrawCall 预算，优化后实测数字在预算范围内。
