---
name: cocos-creator
description: "Cocos Creator 3.8.x 与 COCOS 4 跨平台 2D/3D 游戏引擎开发助手。用于编写与调试 TypeScript 组件、节点与组件体系、事件系统、Tween/Animation 动画、物理与碰撞、UI（Label/Sprite/Button/Widget/Layout）、资源加载与 AssetBundle、场景管理、性能与 DrawCall 优化，以及发布到微信小游戏、抖音小游戏、H5、iOS、Android、HarmonyOS Next 等平台。当用户提到 Cocos、Cocos Creator、Creator 3.8、COCOS 4、cocos-cli、cc 模块、.scene/.prefab/.meta 文件、@ccclass/@property 装饰器、小游戏发布、Spine 动画或游戏引擎性能时使用。"
license: MIT
compatibility: "无需额外运行时依赖。scripts/ 下的体检脚本需要 Python 3.8+（可选）。命令行构建能力需要安装 Cocos Creator 编辑器或 cocos-cli。"
allowed-tools: Read Write Edit Bash Glob Grep
metadata:
  author: hsiaozzz
  version: "2.0.0"
  repository: "https://github.com/hsiaozzz/cocos-creator-skill"
  engines: "Cocos Creator 3.8.x, COCOS 4"
  languages: "TypeScript, JavaScript"
---

# Cocos Creator 开发技能

Cocos Creator 跨平台 2D/3D 游戏引擎开发助手。本文件是**入口与路由**：核心工作流和速查表在这里，深度内容按需从 `references/` 加载，避免一次性占满上下文。

## 何时使用

**适用：**

- 编写、重构、调试 Cocos Creator 的 TypeScript / JavaScript 组件脚本
- 解释 `cc` 模块 API、节点与组件体系、生命周期、事件、动画、物理、UI、资源与场景管理
- 排查构建与发布问题：微信小游戏、抖音小游戏、H5、iOS、Android、HarmonyOS Next
- 性能优化：DrawCall、合批、内存、对象池、包体与首屏加载
- 3.x → COCOS 4 的 API 迁移与版本兼容判断

**不适用：**

- Unity / Unreal / Godot / Cocos2d-x C++ 的问题（API 不通用，不要套用本技能的写法）
- 纯美术与策划数值设计（可作为上下文，但不是本技能职责）

## 第 0 步：先确认版本，再写代码

**这一步不能跳过。** 3.x 与 2.x API 不兼容；3.8 与 COCOS 4 之间也存在差异。

先确认项目实际版本，不要凭记忆假设：

```bash
# 读取项目记录的目标版本
cat project.json 2>/dev/null | head -20          # 老项目在根目录
find . -maxdepth 2 -name "package.json" -not -path "*/node_modules/*" -exec grep -l '"cc"' {} \;
```

- 拿到版本 → 按对应 API 写代码，并在回复中注明"基于 Cocos Creator X.Y.Z"。
- 拿不到版本 → **先问用户**，或明确声明"以下代码基于 3.8.x，若你的项目是 2.x 需改写 API"。

| 版本 | 状态 | 备注 |
|---|---|---|
| 2.x | 停止演进 | 保留 `cc.Class`、`cc.Node` 老 API，与 3.x 不兼容 |
| 3.8.x | 长期主力稳定版 | 3.8.9 为 2026 年最新补丁；3.8.5+ 支持 HarmonyOS Next |
| COCOS 4 | 2026 年 1 月 MIT 全开源 | 3.x 的演进版，承诺前向兼容；编辑器能力逐步迁往 Headless CLI |

## 第 1 步：定位代码该写在哪

先读项目现有结构再动手，不要按模板凭空新建目录。Cocos 项目典型约定：

```
assets/
├── scenes/              # .scene 场景
├── scripts/
│   ├── components/      # 挂载到节点的组件
│   ├── managers/        # 全局管理器（单例）
│   └── utils/           # 纯函数工具
├── prefabs/             # .prefab 预制体
├── textures/ audio/ animations/ materials/
└── resources/           # 只有此目录下资源可被 resources.load() 动态加载
```

三个硬约束：

1. **每个资源都有同名 `.meta` 文件。** 新增资源必须让编辑器生成 `.meta`，手写或漏掉会导致引用丢失、构建报错。
2. **只有 `assets/resources/` 下的资源能用 `resources.load()` 按路径加载。** 其他目录的资源必须通过 `@property` 在编辑器里挂引用。
3. **脚本与组件类的映射由 `.meta` 中的 UUID 决定。** 不要重命名或移动已被场景引用的脚本文件，会断链。

## 第 2 步：写代码

组件骨架（3.8.x）：

```typescript
import { _decorator, Component, Node, Vec3 } from 'cc';
const { ccclass, property } = _decorator;

@ccclass('PlayerController')
export class PlayerController extends Component {
    @property(Node)
    target: Node | null = null;

    @property({ tooltip: '移动速度（像素/秒）' })
    speed = 120;

    private _dir = new Vec3();

    onLoad() {
        // 只做自身初始化；跨节点引用在这里可能还没就绪
    }

    start() {
        // 场景内所有节点 onLoad 完成后调用，适合跨节点交互
    }

    update(dt: number) {
        if (this.speed === 0) return;
        const pos = this.node.position;
        this.node.setPosition(
            pos.x + this._dir.x * this.speed * dt,
            pos.y + this._dir.y * this.speed * dt,
            pos.z + this._dir.z * this.speed * dt,
        );
    }

    onDestroy() {
        // 在这里反注册所有全局监听，否则场景切换后回调仍会触发
    }
}
```

生命周期顺序与适用场景：

| 回调 | 时机 | 适合做什么 |
|---|---|---|
| `onLoad` | 节点激活且组件启用时，仅一次 | 自身字段初始化、缓存 `getComponent` 结果 |
| `start` | 第一次 `update` 前，仅一次 | 依赖其他节点的初始化 |
| `update(dt)` | 每帧 | 逐帧逻辑，`dt` 单位为秒 |
| `lateUpdate(dt)` | 所有 `update` 之后 | 相机跟随（避免抖动） |
| `onEnable` / `onDisable` | 组件启用 / 禁用 | 事件注册与反注册 |
| `onDestroy` | 销毁前 | 释放资源、反注册全局事件 |

完整 API 清单见 [references/api-quick-ref.md](references/api-quick-ref.md)，可直接复用的示例见 [references/examples.md](references/examples.md)。

## 第 3 步：必须验证

写完代码不能直接交付。按项目情况选择最低成本的有效验证：

```bash
# 1) 类型检查（最快，无需打开编辑器）
npx tsc --noEmit -p tsconfig.json

# 2) 项目体检（本技能自带：检查 .meta 缺失、脚本断链、resources 误放、大文件）
python skills/cocos-creator/scripts/cocos_doctor.py --project .

# 3) 编辑器 / CLI 构建
#    编辑器：预览运行（浏览器或模拟器）
#    COCOS 4：cocos-cli（支持 Headless 构建）
```

验证没跑通就如实说明，不要用"应该没问题"交付。

## 第 4 步：提交前自查常见陷阱

1. **`Node.position` 是引用语义**：`this.node.position` 返回的是引擎内部复用的对象，不要长期持有，也不要拿它当计算用的临时变量。需要向量运算时用 `Vec3` 的静态方法配一个自己的临时对象。
2. **`resources.load` 路径不带扩展名**：`resources.load('prefabs/enemy', Prefab, cb)`。写成 `prefabs/enemy.prefab` 会失败。
3. **事件必须成对反注册**：`this.node.on(...)` 配 `off`，`input.on(...)` 配 `off`，且传同一个 `this` 作为 target，否则拿不到同一个回调引用。
4. **`instantiate` 出来的节点必须 `addChild`**，否则不参与场景树，组件不会执行。
5. **频繁 `instantiate` / `destroy` 会引发 GC 抖动**，用对象池（`NodePool` 或自建池）。
6. **图集与材质是合批的前提**：同图集同材质的 Sprite 才能合批，UI 层级穿插会打断合批。
7. **异步竞态**：连续两次 `director.loadScene`，或在加载回调里操作已被销毁的节点，需要 `isValid(node)` 防护。

更多「症状 → 原因 → 方案」见 [references/troubleshooting.md](references/troubleshooting.md)。

## 渐进式参考索引

按需加载，不要一次性预读全部：

| 文件 | 内容 | 何时加载 |
|---|---|---|
| [references/api-quick-ref.md](references/api-quick-ref.md) | 常用模块导入，节点 / 事件 / 动画 / 物理 / UI / 资源 / 场景 API 速查 | 需要查具体 API 签名 |
| [references/examples.md](references/examples.md) | 玩家控制器、对象池、UI 列表、状态机等完整示例 | 需要可直接复用的完整实现 |
| [references/best-practices.md](references/best-practices.md) | 项目架构、目录约定、单例与事件总线、代码规范、资源管理策略 | 设计架构或做 Code Review |
| [references/performance.md](references/performance.md) | DrawCall、合批、内存、GC、包体、首屏加载的量化优化路径 | 出现卡顿、掉帧或包体超限 |
| [references/publishing.md](references/publishing.md) | 微信 / 抖音小游戏分包，H5、iOS、Android、HarmonyOS Next 发布清单 | 构建报错或准备上线 |
| [references/troubleshooting.md](references/troubleshooting.md) | 编辑器、脚本编译、资源、物理、UI、构建发布的排查手册 | 遇到具体报错 |
| [references/cocos4-migration.md](references/cocos4-migration.md) | 3.8 → COCOS 4 迁移、cocos-cli / Headless、AI-Native 能力变化 | 评估升级或使用 COCOS 4 |

## 速查：最常用的导入与片段

```typescript
import { _decorator, Component, Node, Vec3, Vec2, Prefab, instantiate, Label, Sprite,
         Button, Widget, director, resources, tween, input, Input, EventKeyboard,
         RigidBody, Collider, ICollisionEvent, Color, isValid, assetManager } from 'cc';
```

```typescript
// 节点与组件
const child = this.node.getChildByName('Child');
const label = this.node.getComponent(Label);
const btn   = this.node.getComponentInChildren(Button);

// 实例化预制体
resources.load('prefabs/enemy', Prefab, (err, prefab) => {
    if (err || !isValid(this.node)) return;
    const node = instantiate(prefab);
    this.node.addChild(node);
});

// 事件（target 一致才能 off 掉）
this.node.on(Node.EventType.TOUCH_END, this.onTap, this);
this.node.off(Node.EventType.TOUCH_END, this.onTap, this);

// Tween
tween(this.node)
    .to(0.3, { position: new Vec3(100, 0, 0) }, { easing: 'quadOut' })
    .delay(0.2)
    .call(() => console.log('done'))
    .start();

// 场景切换
director.loadScene('Game', (err) => { if (err) console.error(err); });

// 物理碰撞
this.getComponent(Collider)?.on('onCollisionEnter', (e: ICollisionEvent) => { /* ... */ });
```

## 反合理化：常见"偷懒借口"与反驳

- "先不确认版本，3.8 语法应该通用。" → 2.x 与 3.x 不兼容，写错版本等于交付废代码。先确认。
- "不用跑校验，代码看着对。" → 类型错误和 `.meta` 缺失只有工具能发现，肉眼看不出来。
- "`.meta` 文件不重要，先不提交。" → 缺少 `.meta` 会导致构建时资源引用全部丢失，必须提交。
- "资源放哪都能 `resources.load`。" → 只有 `assets/resources/` 可以，其他目录必须走 `@property` 挂引用。
- "事件不 `off` 也没事。" → 场景切换后回调仍持有已销毁节点，是崩溃与内存泄漏的高频来源。
- "性能问题最后再优化。" → DrawCall 与图集策略是结构性决策，越晚改成本越高。

## 危险信号（Red Flags）

出现任一情况，先停下来确认，不要继续往下写：

- 代码里出现 `cc.Class` / `cc.Node` 老式 API，但文件按 3.x 结构组织（版本混乱）
- 引用了 `assets/resources/` 之外的路径却用了 `resources.load`
- 新增了资源文件却看不到对应 `.meta`
- 修改了脚本文件名 / 路径，而该脚本已被 `.scene` 或 `.prefab` 引用
- `destroy()` 之后又访问该节点的属性
- 声称"已优化"但没有给出 DrawCall / 帧时间 / 内存的前后对比数据

## 验证清单（退出标准）

交付前逐项确认，拿证据说话：

- [ ] 已确认项目对应的 Creator 版本，并在回复中注明
- [ ] `npx tsc --noEmit` 通过（或明确说明为何无法运行）
- [ ] 新增资源均有 `.meta` 文件
- [ ] 所有 `on` / `off` 成对，且 `target` 一致
- [ ] 异步回调中对已销毁节点做了 `isValid` 防护
- [ ] 涉及性能改动时，给出优化前后的量化对比
- [ ] 涉及构建发布时，说明了目标平台与验证方式

## 官方资源

- 文档（3.8）：https://docs.cocos.com/creator/3.8/manual/zh/
- API（3.8）：https://docs.cocos.com/creator/3.8/api/zh/
- COCOS 4 开源仓库：https://github.com/cocos/cocos4
- COCOS CLI（Headless 构建）：https://github.com/cocos/cocos-cli
- 示例项目：https://github.com/cocos/cocos-test-projects
- 中文社区：https://forum.cocos.org/
- Cocos Store：https://store.cocos.com

> 本技能由社区维护。与官方文档不一致之处，**以官方文档为准**，并欢迎提 Issue 修正。
