---
name: cocos-creator-tween-anim
description: 写 Cocos Creator 动效/动画时使用。tween、Animation、Spine、性能与清理。
category: gamedev
tags: [cocoscreator, 动画, tween]
---

# Cocos Creator 动画与缓动

## 何时用

- 用 `tween` 做 UI 弹出、飞金币、按钮点击反馈等动效时。
- 使用 `Animation` 组件播放帧动画，或在动画结束时触发游戏逻辑时。
- 集成 Spine 骨骼动画，遇到性能问题或换装需求时。
- 节点销毁后控制台仍然报错（回调访问已销毁节点、tween 继续运行）时。
- 动效卡顿、帧率与期望不符，或动画在不同帧率设备上速度不一致时。

## 核心规则

### 1. tween 用法：链式 API 做 UI 动效，销毁前必须 stopAllByTarget

**规则：** UI 动效优先用 `tween(node).to(...).call(...).start()` 链式写法；节点销毁、场景切换、或主动取消动效时，必须调用 `Tween.stopAllByTarget(node)` 停止该节点上所有正在运行的 tween；不要把 tween 的 `.call()` 回调里对节点的访问放在延迟后，而不先判断节点有效性。

**为什么：** 这是 Creator 项目里最高频的运行时报错来源之一。典型场景：UI 弹窗弹出动画还没播完（0.3s tween），玩家点了关闭按钮，弹窗节点被 `destroy`，0.3s 后 tween 的 `.call()` 回调执行——此时 `this` 或捕获的节点引用已销毁，访问任何属性都抛出 `Cannot read properties of null`，且错误栈指向 tween 引擎内部，极难定位。另一个常见错误：节点池归还时没有停止节点上的 tween，下次取出时旧 tween 仍在运行，与新 tween 叠加，节点产生错乱的双重动画。

**怎么做：**
- 启动：`tween(this.node).to(0.3, { scale: new Vec3(1,1,1) }, { easing: 'backOut' }).call(() => { this.onShowComplete(); }).start();`
- 节点销毁时：`onDestroy() { Tween.stopAllByTarget(this.node); }`
- 节点池归还时（`unuse`）：`Tween.stopAllByTarget(this.node);`
- 回调内访问组件：先判断 `if (!this.isValid) return;`，防止节点已销毁后回调被延迟触发。
- 需要保留 tween 引用以便手动取消：`this._showTween = tween(node).to(...).start();`，取消时 `this._showTween?.stop();`。

---

### 2. Animation 组件：帧/骨骼动画播放，关键时机用帧事件而非硬编码计时

**规则：** 帧动画和骨骼动画的时机逻辑（播放完毕后跳转状态、攻击动画命中帧触发伤害）用 Animation 的帧事件（`AnimationEvent`）或 `finished` 事件回调触发，不用 `scheduleOnce(callback, duration)` 硬编码时长。

**为什么：** `scheduleOnce(this.onAttackHit, 0.35)` 是新手最常写的"动画同步"方案。问题一：动画时长一旦被美术调整（0.35s 改 0.4s），程序代码里的数字忘了改，命中判定就永远提前或延后。问题二：设备帧率波动导致动画实际播放时长和计时器有微小偏差，在帧率不稳定的低端机上累积误差很明显。问题三：两处（动画文件和代码）维护同一个时间点，必然随着版本迭代出现不同步。帧事件直接嵌入动画文件，时机和动画帧绑定，美术改动画时机会自然跟随，不需要程序同步修改代码。

**怎么做：**
- 在 Creator 动画编辑器里，在攻击命中帧添加帧事件，函数名填 `onHitFrame`。
- 对应组件添加 `onHitFrame() { this._combatSystem.applyDamage(this._target); }`。
- 监听动画结束：`this._anim.on(Animation.EventType.FINISHED, this.onAnimFinished, this);`，在 `onDestroy` 里 `off`。
- 播放指定动作：`this._anim.play('attack');` — 状态机切换时用 `crossFade` 避免切换时的一帧跳变。
- 不在代码里硬编码任何动画时长常量，时长属于动画资源的职责，不属于逻辑代码。

---

### 3. Spine/骨骼：复用 SkeletonData，移动端控制骨骼数与换装 Mesh 合批

**规则：** 同一角色的多个实例必须共享同一份 `SkeletonData` 资源（通过 `@property` 引用或动态加载后 `addRef` 复用），不每次 `instantiate` 时重复加载；移动端单个 Spine 角色控制在 60 骨骼以内，换装时优先用 `Attachment` 替换而非多 `SkeletonComponent` 叠加。

**为什么：** Spine 渲染是 Creator 项目里 GPU 压力最集中的地方。`SkeletonData` 包含骨架定义、所有动画曲线、皮肤数据，体积可达数 MB；如果每个敌人实例各自走一遍 `resources.load` 加载 SkeletonData，10 个敌人就是 10 份重复数据驻留内存，纹理内存直接翻倍。换装方案的性能陷阱更隐蔽：用多个 `SkeletonComponent` 叠加（一层身体+一层装备）的方案每层产生独立 Draw Call，且每层都有自己的骨骼运算，5 个角色就是 10 次骨骼更新；而用同一套骨骼的 `Attachment` 换装，只有 1 次骨骼运算，装备替换通过贴图槽替换，不增加 Draw Call 也不增加骨骼数。

**怎么做：**
- 在 `SpawnManager` 里预加载并缓存 `SkeletonData`：`resources.load('spine/hero', sp.SkeletonData, (err, sd) => { sd.addRef(); this._heroSkeletonData = sd; })`。
- `instantiate` 时将缓存的 `SkeletonData` 赋给新节点：`node.getComponent(sp.Skeleton).skeletonData = this._heroSkeletonData;`。
- 换装：`skeleton.setAttachment('weapon_slot', 'sword_attachment');` — 仅替换对应骨骼槽的 Attachment，无额外 Draw Call。
- 场景卸载时：`this._heroSkeletonData?.decRef(); this._heroSkeletonData = null;`。
- 用 Creator Profiler 的「Renderer」面板确认 Spine 节点的 Draw Call 数，相邻 Spine 节点若使用相同纹理图集应能合批（两个 Draw Call 合为一个）。

---

### 4. 缓动手感：用 easing 曲线，时长与帧率解耦

**规则：** 所有 tween 动效必须指定 `easing` 参数（如 `backOut`、`quartOut`、`elasticOut`），不使用默认线性缓动；动效时长以秒为单位，不依赖帧数（不写 `duration = targetFrames / 60`）；动效参数（时长、幅度）集中定义在配置常量里，不在代码中散落魔法数字。

**为什么：** 线性动效是"AI 写的动画"最直观的特征——位移、缩放匀速变化，没有加速减速，机械感很强，玩家直觉上感受到"不对劲"但说不清楚。`easing: 'backOut'` 让按钮弹出时有一个超过目标值再回弹的手感，`elasticOut` 给弹窗增加果冻感，这些曲线把"感觉有生命力"和"机械感"区分开来，是动效品质的核心。帧数依赖的问题：`duration = 18 / 60 = 0.3s` 在 60fps 设备上正常，但代码的语义是"18帧"而不是"0.3秒"，一旦逻辑被移植或时间计算方式改变，这个数字就失去了含义，且不同帧率设备上 tween 时长本身是固定的（tween 基于真实时间），所以直接写秒数更清晰。

**怎么做：**
- 定义动效常量：`const ANIM = { POPUP_DURATION: 0.25, POPUP_EASING: 'backOut', COIN_FLY_DURATION: 0.6 } as const;`
- 弹窗弹出：`tween(panel).to(ANIM.POPUP_DURATION, { scale: new Vec3(1,1,1) }, { easing: ANIM.POPUP_EASING }).start();`
- 按钮点击反馈：`tween(btn).to(0.08, { scale: new Vec3(0.9,0.9,1) }).to(0.12, { scale: new Vec3(1,1,1) }, { easing: 'backOut' }).start();`
- 连续多段动画用链式 `.to(...).to(...).call(...)`，比多个 `scheduleOnce` 更易维护和取消。
- 不同时长设备测试：在低帧率手机（30fps）上验证动效时长和手感与高帧率设备是否一致（tween 基于 `dt` 时间步，应自动适配）。

---

### 5. 清理：onDestroy 停止所有 tween/动画/回调，防内存泄漏与野回调

**规则：** 组件的 `onDestroy` 里必须：① `Tween.stopAllByTarget(this.node)` 停止所有 tween；② `this._anim.off(...)` 注销所有 Animation 事件监听；③ 取消所有 `scheduleOnce`/`schedule` 调度；④ 如果持有 Spine 的 `SkeletonData` 引用，调用 `decRef()`。不做这些清理，节点销毁后回调仍会执行，轻则控制台报错，重则访问已释放内存导致不可复现的随机崩溃。

**为什么：** Creator 的 tween 系统是全局单例管理的，`tween(node).start()` 把任务注册到全局 TweenManager，节点 `destroy` 后 TweenManager 并不自动感知，仍然每帧 tick 这个 tween，直到 tween 完成并执行回调——此时节点已销毁，回调里的 `this.xxx` 全部是访问已释放的引用。Animation 事件监听器同样如此：`anim.on(FINISHED, handler, this)` 如果没有 `off`，即便 `this` 所在节点销毁，只要 Animation 组件的宿主节点还存在，事件依然会尝试回调 `handler`，`this` 已是废指针。这类 bug 极难复现——只在"动效播放到一半销毁节点"这个特定时序下触发，稳定性测试很难覆盖。

**怎么做：**
- 统一清理模板：
  ```typescript
  onDestroy() {
      // ① 停止该节点上所有 tween
      Tween.stopAllByTarget(this.node);

      // ② 注销 Animation 事件
      if (this._anim) {
          this._anim.off(Animation.EventType.FINISHED, this.onAnimFinished, this);
      }

      // ③ 取消调度器（若用了 schedule/scheduleOnce）
      this.unscheduleAllCallbacks();

      // ④ 释放 Spine SkeletonData 引用计数
      if (this._skeletonData) {
          this._skeletonData.decRef();
          this._skeletonData = null;
      }
  }
  ```
- 回调内加有效性守卫：所有异步或延迟执行的回调第一行写 `if (!this.isValid || !this.node.isValid) return;`。
- 节点池归还时同样执行：`unuse() { Tween.stopAllByTarget(this.node); this._anim?.stop(); }`
- 若 tween 链很长（多段动画序列），归还/销毁时的 `stopAllByTarget` 足以取消整个链，不需要逐段停止。

---

## 正例 / 反例

### 反例：tween 回调访问已销毁节点 + scheduleOnce 硬编码动画时机

```typescript
// 反例 — 弹窗关闭时没停 tween，回调访问已销毁的 this
import { _decorator, Component, tween, Vec3 } from 'cc';
const { ccclass } = _decorator;

@ccclass('PopupPanel')
export class PopupPanel extends Component {
    show() {
        // ❌ 没有保存 tween 引用，也没有 stopAllByTarget，关闭时无法取消
        tween(this.node)
            .to(0.3, { scale: new Vec3(1.2, 1.2, 1) })
            .to(0.15, { scale: new Vec3(1, 1, 1) })
            .call(() => {
                // ❌ 如果 0.45s 内节点被 destroy，这里报错
                this.onShowComplete();
            })
            .start();
    }

    hide() {
        // ❌ 没有 Tween.stopAllByTarget，show 的 tween 仍在运行
        this.node.destroy();
    }

    onAttack() {
        this._anim.play('attack');
        // ❌ 硬编码 0.35s，美术改动画后这里忘了同步
        this.scheduleOnce(() => { this._hitEffect.active = true; }, 0.35);
    }

    // ❌ 没有 onDestroy，tween 和 Animation 事件不清理
}
```

```typescript
// 正例 — tween 正确停止，帧事件驱动动画时机，onDestroy 完整清理
import { _decorator, Component, tween, Tween, Vec3, Animation, sp } from 'cc';
const { ccclass, property } = _decorator;

const POPUP = { SHOW_DURATION: 0.3, EASING: 'backOut' } as const;

@ccclass('PopupPanel')
export class PopupPanel extends Component {
    @property(Animation) private _anim: Animation = null!;

    private _showTween: ReturnType<typeof tween> | null = null;

    onLoad() {
        // ✅ 动画结束事件用组件监听，onDestroy 里注销
        this._anim.on(Animation.EventType.FINISHED, this.onAnimFinished, this);
    }

    show() {
        Tween.stopAllByTarget(this.node);   // ✅ 先停掉旧的，防止叠加
        this._showTween = tween(this.node)
            .set({ scale: new Vec3(0.5, 0.5, 1) })
            .to(POPUP.SHOW_DURATION, { scale: new Vec3(1, 1, 1) }, { easing: POPUP.EASING })
            .call(() => {
                if (!this.isValid) return;  // ✅ 回调前检查节点有效性
                this.onShowComplete();
            })
            .start();
    }

    hide() {
        Tween.stopAllByTarget(this.node);   // ✅ 销毁前停止所有 tween
        tween(this.node)
            .to(0.15, { scale: new Vec3(0, 0, 1) })
            .call(() => {
                if (!this.isValid) return;
                this.node.active = false;   // ✅ 隐藏而非 destroy，支持节点池复用
            })
            .start();
    }

    // ✅ 命中帧逻辑由动画帧事件触发，不写死时长
    onHitFrame() {
        if (!this.isValid) return;
        this._hitEffect.active = true;
    }

    private onAnimFinished(type: Animation.EventType, state: AnimationState) {
        if (!this.isValid) return;
        if (state.name === 'attack') {
            this._hitEffect.active = false;
        }
    }

    onDestroy() {
        Tween.stopAllByTarget(this.node);                                       // ✅ 停所有 tween
        this._anim?.off(Animation.EventType.FINISHED, this.onAnimFinished, this); // ✅ 注销事件
        this.unscheduleAllCallbacks();                                          // ✅ 清调度器
    }
}
```

---

### 反例：Spine 每个实例重复加载 SkeletonData + 线性无 easing

```typescript
// 反例 — 每个敌人各自加载 SkeletonData，线性 tween 无手感
@ccclass('EnemySpawner')
export class EnemySpawner extends Component {
    spawnEnemy(pos: Vec3) {
        const enemy = instantiate(this.enemyPrefab);
        // ❌ 每个敌人各自 load，10 个敌人 = 10 份 SkeletonData 内存
        resources.load('spine/enemy', sp.SkeletonData, (err, sd) => {
            enemy.getComponent(sp.Skeleton)!.skeletonData = sd;
            // ❌ 默认线性缓动，弹出感机械
            tween(enemy).to(0.3, { position: pos }).start();
        });
        this.node.addChild(enemy);
    }
}
```

```typescript
// 正例 — 预加载共享 SkeletonData + easing 曲线赋予手感
@ccclass('EnemySpawner')
export class EnemySpawner extends Component {
    @property(sp.SkeletonData) enemySkeletonData: sp.SkeletonData = null!;
    // ✅ Inspector 直接引用或统一在 ResourceManager 里预加载，所有实例共享

    onLoad() {
        // ✅ 手动 addRef 延长生命周期，onDestroy 里 decRef
        this.enemySkeletonData.addRef();
    }

    spawnEnemy(spawnPos: Vec3, targetPos: Vec3) {
        const enemy = instantiate(this.enemyPrefab);
        // ✅ 共享同一份 SkeletonData，不重复加载
        enemy.getComponent(sp.Skeleton)!.skeletonData = this.enemySkeletonData;
        enemy.setPosition(spawnPos);
        this.node.addChild(enemy);

        // ✅ backOut easing 赋予弹入手感，时长用具名常量
        tween(enemy)
            .to(0.35, { position: targetPos }, { easing: 'backOut' })
            .start();
    }

    onDestroy() {
        Tween.stopAllByTarget(this.node);
        this.enemySkeletonData?.decRef();  // ✅ 释放引用计数
    }
}
```

---

## 自查清单

- [ ] 所有 `tween(...).start()` 的节点在 `onDestroy` 或归还对象池的 `unuse` 里调用了 `Tween.stopAllByTarget(node)`。
- [ ] tween `.call()` 回调内第一行有 `if (!this.isValid) return;` 或 `if (!node.isValid) return;` 守卫。
- [ ] 动画关键时机（命中帧、攻击触发、音效点）使用 Animation 帧事件或 `FINISHED` 事件，没有 `scheduleOnce` 硬编码时长。
- [ ] `Animation.EventType.FINISHED` 等动画事件在 `onDestroy` 里调用了 `off` 注销。
- [ ] Spine 的 `SkeletonData` 同场景内所有实例共享同一份引用，没有每个实例各自加载。
- [ ] 所有 tween 都指定了 `easing` 参数，没有使用默认线性缓动。
- [ ] 动效时长使用秒数常量，没有以帧数除以帧率的方式计算。
