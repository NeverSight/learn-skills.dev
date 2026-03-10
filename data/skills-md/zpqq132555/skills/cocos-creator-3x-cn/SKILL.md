---
name: cocos-creator-3x-cn
description: 提供 Cocos Creator 3.8 游戏引擎的全面开发指导，包括组件系统（_decorator、Component）、生命周期回调、事件系统（EventTarget、input）、resources 资源管理、tween 缓动系统、对象池、UI 系统、物理碰撞以及可试玩广告优化。在用户编写或重构 Cocos Creator 3.x TypeScript 代码、实现游戏功能、处理资源加载与释放、优化性能/包体大小、审查代码变更、搭建可试玩广告项目架构时触发。也适用于用户提到 import from 'cc'、Component、Node、resources、tween、director 等 3.x API 时使用。
---

# Cocos Creator 3.8 开发指导技能

## 元信息 (Frontmatter)

- **技能名称**: `cocos-creator-3x-cn`
- **适用引擎**: Cocos Creator 3.8 (LTS)
- **语言**: TypeScript (ES Module, `import { ... } from 'cc'`)
- **官方文档**: https://docs.cocos.com/creator/3.8/manual/zh/
- **API 参考**: https://docs.cocos.com/creator/3.8/api/zh/

---

## 快速参考 — 与 2.x 的核心差异

| 项目 | 2.x 写法 | 3.8 写法 |
|------|----------|----------|
| 导入 | `const { ccclass } = cc._decorator` | `import { _decorator } from 'cc'; const { ccclass } = _decorator;` |
| 组件基类 | `cc.Component` | `Component` (从 `'cc'` 导入) |
| 节点类 | `cc.Node` | `Node` (从 `'cc'` 导入) |
| 调试宏 | `CC_DEBUG` | `import { DEBUG } from 'cc/env';` |
| 全局事件 | `cc.systemEvent` | `import { input, Input } from 'cc';` |
| 资源加载 | `cc.resources.load()` | `import { resources } from 'cc'; resources.load()` |
| 缓动 | `cc.tween()` | `import { tween } from 'cc'; tween()` |
| 实例化 | `cc.instantiate()` | `import { instantiate } from 'cc';` |
| 场景管理 | `cc.director` | `import { director } from 'cc';` |
| 属性类型 | `cc.Integer` | `import { CCInteger } from 'cc';` |

---

## 1. 组件系统 (Component System)

### 1.1 基础组件模板

```typescript
import { _decorator, Component, Node } from 'cc';
const { ccclass, property } = _decorator;

@ccclass('MyComponent')
export class MyComponent extends Component {
    @property(Node)
    private readonly targetNode: Node | null = null;

    @property
    private readonly speed: number = 10;

    // 生命周期见 §2
    protected onLoad(): void { }
    protected start(): void { }
    protected update(dt: number): void { }
    protected onDestroy(): void { }
}
```

### 1.2 装饰器速查

| 装饰器 | 说明 | 示例 |
|--------|------|------|
| `@ccclass('Name')` | 注册 cc 类（名称全局唯一） | `@ccclass('Player')` |
| `@property` | 序列化属性 | `@property speed = 10;` |
| `@property(Type)` | 指定类型 | `@property(Node) target: Node = null!;` |
| `@property({type: [Node]})` | 数组类型 | `children: Node[] = [];` |
| `@integer` | 整数类型简写 | `@integer count = 0;` |
| `@float` | 浮点类型简写 | `@float ratio = 1.0;` |
| `@type(T)` | 类型简写 | `@type(Node) target = null;` |
| `@executeInEditMode` | 编辑器模式执行 | `@executeInEditMode(true)` |
| `@requireComponent(T)` | 依赖组件 | `@requireComponent(Sprite)` |
| `@executionOrder(n)` | 执行优先级 | `@executionOrder(-1)` |
| `@disallowMultiple` | 禁止重复添加 | `@disallowMultiple(true)` |
| `@menu('path')` | 添加到组件菜单 | `@menu('Custom/MyComp')` |

### 1.3 属性参数

```typescript
@property({
    type: Node,
    visible: true,
    displayName: '目标节点',
    tooltip: '要跟随的目标',
    serializable: true,
    group: { name: '基础设置' },
})
targetNode: Node | null = null;
```

常用参数: `type`, `visible`, `displayName`, `tooltip`, `serializable`, `readonly`, `min`, `max`, `step`, `range`, `slide`, `group`, `override`, `formerlySerializedAs`, `editorOnly`

---

## 2. 生命周期回调

执行顺序：`onLoad` → `onEnable` → `start` → `update` / `lateUpdate` → `onDisable` → `onDestroy`

```
 ┌─────────┐   ┌──────────┐   ┌───────┐   ┌────────┐
 │ onLoad  │──▶│ onEnable │──▶│ start │──▶│ update │──┐
 └─────────┘   └──────────┘   └───────┘   └────────┘  │
                                              ▲         │
                                              └─────────┘
                                           ┌────────────┐
                                           │ lateUpdate │
                                           └────────────┘
                                                 │
                                           ┌───────────┐   ┌─────────────┐
                                           │ onDisable │──▶│ onDestroy   │
                                           └───────────┘   └─────────────┘
```

| 回调 | 触发时机 | 典型用途 |
|------|---------|---------|
| `onLoad()` | 节点首次激活时（仅一次） | 初始化引用、获取组件 |
| `onEnable()` | 组件启用时 | 注册事件监听 |
| `start()` | 第一次 `update` 之前（仅一次） | 需要依赖其他组件 `onLoad` 完成 |
| `update(dt)` | 每帧调用 | 游戏逻辑、移动 |
| `lateUpdate(dt)` | 所有 `update` 后 | 跟随相机、后处理 |
| `onDisable()` | 组件禁用时 | 取消事件监听 |
| `onDestroy()` | 节点销毁时 | 资源释放、清理 |

**关键规则**:
- `onLoad` 中可确保节点已挂载到节点树
- 同一节点上组件的 `onLoad`/`onEnable`/`start` 按组件面板顺序执行，可通过 `@executionOrder` 控制
- `onEnable`/`onDisable` 配对使用：注册/注销事件监听
- `onDestroy` 中应释放所有动态加载资源的引用

---

## 3. 事件系统

### 3.1 自定义事件 (EventTarget)

```typescript
import { EventTarget } from 'cc';

// 创建全局事件总线
const eventTarget = new EventTarget();

// 监听
eventTarget.on('game-over', (score: number) => {
    console.log('Game Over, score:', score);
});

// 发射（最多 5 个参数）
eventTarget.emit('game-over', 100);

// 取消监听
eventTarget.off('game-over', callback, target);
```

**⚠️ 注意**: 不再推荐通过 `Node` 对象做自定义事件监听与发射。

### 3.2 全局输入事件 (input)

```typescript
import { _decorator, Component, input, Input, EventTouch, EventKeyboard, KeyCode } from 'cc';

@ccclass('InputExample')
export class InputExample extends Component {
    protected onEnable(): void {
        input.on(Input.EventType.TOUCH_START, this.onTouchStart, this);
        input.on(Input.EventType.KEY_DOWN, this.onKeyDown, this);
    }
    protected onDisable(): void {
        input.off(Input.EventType.TOUCH_START, this.onTouchStart, this);
        input.off(Input.EventType.KEY_DOWN, this.onKeyDown, this);
    }
    private onTouchStart(event: EventTouch): void {
        console.log(event.getLocation());     // 屏幕坐标
        console.log(event.getUILocation());   // UI 坐标
    }
    private onKeyDown(event: EventKeyboard): void {
        if (event.keyCode === KeyCode.SPACE) { /* ... */ }
    }
}
```

全局输入事件类型:

| 类别 | 事件类型 |
|------|---------|
| 触摸 | `TOUCH_START`, `TOUCH_MOVE`, `TOUCH_END`, `TOUCH_CANCEL` |
| 鼠标 | `MOUSE_DOWN`, `MOUSE_MOVE`, `MOUSE_UP`, `MOUSE_WHEEL` |
| 键盘 | `KEY_DOWN`, `KEY_PRESSING`, `KEY_UP` |
| 重力 | `DEVICEMOTION` |

### 3.3 节点事件

```typescript
// UI 节点触摸（需要 UITransform 组件）
this.node.on(Node.EventType.TOUCH_START, (event: EventTouch) => {
    event.propagationStopped = true; // 阻止冒泡
}, this);

// 使用捕获阶段
this.node.on(Node.EventType.TOUCH_START, callback, this, true);

// 事件穿透（v3.4+）
private onTouchStart(event: EventTouch): void {
    event.preventSwallow = true; // 阻止事件被吞噬
}
```

### 3.4 自定义节点事件派发

```typescript
import { Event } from 'cc';

class MyEvent extends Event {
    public readonly detail: unknown;
    constructor(name: string, bubbles?: boolean, detail?: unknown) {
        super(name, bubbles);
        this.detail = detail;
    }
}

// 派发事件（支持冒泡/捕获）
this.node.dispatchEvent(new MyEvent('custom-event', true, { data: 123 }));
```

---

## 4. 资源管理 (Asset Manager)

### 4.1 resources 加载

```typescript
import { resources, Prefab, SpriteFrame, Texture2D, instantiate, Sprite } from 'cc';

// 加载 Prefab
resources.load('prefabs/enemy', Prefab, (err, prefab) => {
    const node = instantiate(prefab);
    this.node.addChild(node);
});

// 加载 SpriteFrame（注意路径到子资源）
resources.load('images/bg/spriteFrame', SpriteFrame, (err, sf) => {
    this.getComponent(Sprite)!.spriteFrame = sf;
});

// 批量加载
resources.loadDir('textures', Texture2D, (err, assets) => { /* ... */ });

// 预加载
resources.preload('images/bg/spriteFrame', SpriteFrame);
```

### 4.2 Asset Bundle

```typescript
import { assetManager, Prefab } from 'cc';

// 加载 Bundle
assetManager.loadBundle('gameBundle', (err, bundle) => {
    // 加载 Bundle 中的资源
    bundle.load('prefabs/player', Prefab, (err, prefab) => { /* ... */ });
    // 批量加载
    bundle.loadDir('textures', (err, assets) => { /* ... */ });
    // 加载场景
    bundle.loadScene('level1', (err, scene) => {
        director.runScene(scene);
    });
});

// 获取已加载的 Bundle
const bundle = assetManager.getBundle('gameBundle');
```

### 4.3 资源释放

```typescript
import { assetManager, resources, SpriteFrame } from 'cc';

// 方式一：直接释放
assetManager.releaseAsset(asset);

// 方式二：通过 Bundle 释放
bundle.release('image', SpriteFrame);
bundle.releaseAll();

// 方式三：引用计数管理
resources.load('img/spriteFrame', SpriteFrame, (err, sf) => {
    sf.addRef();       // 持有时增加引用
    // ... 使用中
    sf.decRef();       // 不再使用时减少引用
});

// 移除 Bundle
assetManager.removeBundle(bundle);
```

### 4.4 远程资源加载

```typescript
import { assetManager, ImageAsset, Texture2D, SpriteFrame } from 'cc';

assetManager.loadRemote<ImageAsset>('https://example.com/avatar.png', (err, imageAsset) => {
    const texture = new Texture2D();
    texture.image = imageAsset;
    const sf = new SpriteFrame();
    sf.texture = texture;
});
```

---

## 5. 缓动系统 (Tween)

```typescript
import { tween, Vec3, Node, UIOpacity } from 'cc';

// 基础缓动
tween(this.node)
    .to(1, { position: new Vec3(100, 200, 0) })
    .start();

// 链式动画
tween(this.node)
    .to(0.5, { scale: new Vec3(1.2, 1.2, 1) })
    .to(0.5, { scale: new Vec3(1, 1, 1) })
    .union()          // 合并为一个动作
    .repeatForever()  // 无限循环
    .start();

// 回调
tween(this.node)
    .to(1, { position: new Vec3(0, 100, 0) })
    .call(() => { console.log('done'); })
    .start();

// 并行 & 延迟
tween(this.node)
    .parallel(
        tween().to(1, { position: new Vec3(100, 0, 0) }),
        tween().to(1, { scale: new Vec3(2, 2, 1) }),
    )
    .delay(0.5)
    .start();

// 透明度缓动（需要 UIOpacity 组件）
const opacity = this.node.getComponent(UIOpacity)!;
tween(opacity).to(0.5, { opacity: 0 }).start();

// 停止缓动
Tween.stopAllByTarget(this.node);
```

---

## 6. 节点与场景操作

### 6.1 节点访问

```typescript
// 子节点
const child = this.node.getChildByName('child');
const children = this.node.children;
const childByPath = find('Canvas/UI/Button', this.node); // 路径查找

// 父节点
const parent = this.node.parent;

// 全局查找
import { find } from 'cc';
const canvas = find('Canvas');

// 组件获取
const sprite = this.node.getComponent(Sprite);
const sprites = this.node.getComponentsInChildren(Sprite);
```

### 6.2 节点变换

```typescript
import { Vec3, Quat } from 'cc';

// 位置
this.node.setPosition(new Vec3(100, 200, 0));
this.node.position = new Vec3(100, 200, 0);

// 旋转 (3D 使用 Quat)
this.node.setRotationFromEuler(0, 0, 45);
this.node.angle = 45; // 2D 简写

// 缩放
this.node.setScale(new Vec3(2, 2, 1));

// 世界坐标
const worldPos = this.node.worldPosition;
this.node.setWorldPosition(worldPos);
```

### 6.3 场景管理

```typescript
import { director } from 'cc';

// 加载并切换场景
director.loadScene('GameScene');

// 带回调
director.loadScene('GameScene', (err, scene) => {
    console.log('scene loaded');
});

// 预加载场景
director.preloadScene('GameScene', (err) => {
    // 预加载完成
});

// 常驻节点
director.addPersistRootNode(this.node);
director.removePersistRootNode(this.node);
```

---

## 7. 平台宏与条件编译

```typescript
import { sys } from 'cc';
import { DEBUG, EDITOR, PREVIEW, BUILD } from 'cc/env';

// 环境宏
if (DEBUG) { /* 调试模式 */ }
if (EDITOR) { /* 编辑器模式 */ }
if (BUILD) { /* 构建后 */ }

// 平台判断
if (sys.isBrowser) { /* 浏览器 */ }
if (sys.isNative) { /* 原生平台 */ }
if (sys.platform === sys.Platform.WECHAT_GAME) { /* 微信小游戏 */ }
```

---

## 8. 模块导入规范

```typescript
// ✅ 正确：从 'cc' 模块导入
import { _decorator, Component, Node, Vec3, Color, Sprite, resources } from 'cc';

// ✅ 正确：从 'cc/env' 导入环境宏
import { DEBUG, EDITOR } from 'cc/env';

// ❌ 错误：不要使用 cc. 全局前缀
// cc.Component, cc.Node, cc.find // 3.x 中不存在
```

---

## 参考文件索引

### 框架参考 (references/framework/)
| 文件 | 说明 |
|------|------|
| [component-system.md](references/framework/component-system.md) | 组件系统、装饰器、生命周期详解 |
| [event-patterns.md](references/framework/event-patterns.md) | 事件系统、输入/节点/自定义事件模式 |
| [asset-management.md](references/framework/asset-management.md) | 资源管理、加载/释放/Bundle |
| [playable-optimization.md](references/framework/playable-optimization.md) | 可试玩广告优化、包体/性能策略 |

### 语言参考 (references/language/)
| 文件 | 说明 |
|------|------|
| [quality-hygiene.md](references/language/quality-hygiene.md) | TypeScript 代码质量与卫生规范 |
| [performance.md](references/language/performance.md) | 性能优化指南、内存/渲染/逻辑 |

### 审查参考 (references/review/)
| 文件 | 说明 |
|------|------|
| [architecture-review.md](references/review/architecture-review.md) | 架构审查清单 |
| [quality-review.md](references/review/quality-review.md) | 代码质量审查清单 |
