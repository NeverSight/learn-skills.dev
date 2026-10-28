---
name: gameplay-architecture
description: 设计游戏玩法代码结构时使用。状态机、解耦、避免 God object。
category: gamedev
tags: [架构, 状态机, ecs]
---

# 玩法架构

## 何时用

- 设计角色控制器、AI 行为、UI 流程等有明显状态切换的系统时。
- 两个系统开始互相引用、代码耦合越来越重时。
- 数值、配置需要被策划频繁调整时。
- 发现 GameManager/Player 脚本越来越大、什么都往里塞时。
- 讨论是用继承还是组件/ECS 实现某个能力时。

## 核心规则

### 1. 状态机：显式状态，不堆标志位

**规则：** 有明确状态切换的对象（角色、UI 流程、关卡进程），用状态机建模；不用多个 bool 标志位组合表示状态；状态转移逻辑集中在一处，而不是散在各处的 if-else。

**为什么——真实会犯的错：**
角色脚本里堆了 `isAttacking`、`isRolling`、`isStunned`、`isDead`、`isInvincible` 五个 bool，处理「受击」时需要判断 `if (!isDead && !isInvincible && !isRolling)`，忘记加 `!isAttacking`，结果攻击时被打也会触发受伤动画。类似的 bug 在每次加新状态时都会出现，因为没有一个地方能看到「所有状态的完整列表」以及「哪些状态之间互斥」。

**怎么做：**
- 定义枚举 `EPlayerState { Idle, Run, Attack, Roll, Stunned, Dead }`，同一时刻只有一个值。
- 状态转移写成 `TransitionTo(EPlayerState next)` 函数，内含前置条件检查，不在外部随意改状态。
- 每个状态的 Enter/Update/Exit 逻辑用子类或字典组织，不堆在同一个 Update 方法里。
- 复杂 AI 考虑分层状态机（HSM）或行为树，但先从平坦状态机起步，确实需要再升级。

---

### 2. 事件解耦：系统间消息通信，不硬引用

**规则：** 不同系统（战斗、背包、UI、音效、成就）之间通过事件/消息总线通信；不直接持有对方的引用；增删系统不改调用方。

**为什么——真实会犯的错：**
`CombatSystem` 里直接写 `UIManager.Instance.UpdateHPBar(hp)`、`AchievementSystem.Instance.CheckKillCount()`、`AudioManager.Instance.PlayHitSound()`，战斗系统变成了蜘蛛网的中心节点，牵一发动全身。后来要给死亡加一个「慢动作特效」，需要改 CombatSystem，但 CombatSystem 的开发者对 PostProcessManager 完全不了解，加了一行代码引入了空引用崩溃。

**怎么做：**
- 用全局事件总线：`EventBus.Emit("player_died", data)`，各系统独立订阅，互不知晓对方存在。
- Unity：UnityEvent、ScriptableObject 事件通道；Unreal：Gameplay Ability System 的 Tag 系统或 Delegate；Godot：Autoload 中的 signal 总线。
- 订阅时注意生命周期：系统销毁时取消订阅，防止向已销毁对象发送消息。
- 不是所有通信都要用事件——父子组件之间直接调用方法完全正常，事件总线是**跨系统**通信的工具。

---

### 3. 数据驱动：配置走数据，不写死代码

**规则：** 角色属性、技能数值、掉落概率、关卡参数等所有由策划控制的数据，放进数据文件（ScriptableObject、JSON、CSV、DataTable）；代码只读取数据，不硬编码具体数值。

**为什么——真实会犯的错：**
程序在代码里写了 `damage = 35; cooldown = 1.2f; range = 8.0f`，策划做数值平衡需要每次叫程序改代码、重编译、出包给 QA，一轮数值迭代要半天。上线后发现某个技能数值设高了，紧急改一行数字也需要走全流程提交代码，用热更新还得单独处理。最后策划和程序都在做本该对方做的事，沟通成本极高。

**怎么做：**
- Unity：技能数据用 ScriptableObject，每个技能一个资产文件，策划直接在编辑器里改。
- Unreal：DataTable + 结构体，或 DataAsset；蓝图默认值也是数据，可以留给策划配。
- Godot：Resource 文件（`.tres`/`.res`）或 JSON 配置，`load("res://data/skills.json")`。
- 不要把「策划会改的数值」和「程序逻辑」混在同一个文件里，分离关注点。

---

### 4. 组合优于继承：组件/ECS 拼装能力，不叠继承树

**规则：** 角色能力（可攻击、可拾取、可移动、有生命值）用组件组合实现；不用深继承树叠加能力；避免菱形继承和基类膨胀。

**为什么——真实会犯的错：**
`Entity → Character → Humanoid → Player`，四层继承后，Player 需要的「可游泳」能力不在任何父类里，只能加在 Player 里；「Boss 也需要游泳」又要加一次；后来 `Character` 里改了一个 `TakeDamage` 方法，不知道已经有三个子类 override 了它，测试漏了其中一个，出了 bug。继承树越深，单个改动的影响范围越难评估。

**怎么做：**
- 把「能力」拆成独立组件：`HealthComponent`、`MovementComponent`、`AttackComponent`、`SwimComponent`，挂到任意 Actor/Node 上组合。
- 组件间通信通过接口（Interface）或事件，不互相持有引用。
- Unreal 的 ActorComponent 体系、Unity 的 MonoBehaviour 组合、Godot 的节点树天然支持组合模式，优先用这些而不是深继承。
- 如果发现自己在写 `BaseEnemyAIController → RangedEnemyController → BossRangedController`，停下来重新考虑组件方案。

---

### 5. 单一职责：Manager 按职责拆分，不做万能 God object

**规则：** 每个 Manager/System 只负责一件事；「GameManager」不应该同时管存档、UI、音效、关卡加载、玩家状态；发现一个类超过 500 行就考虑拆分。

**为什么——真实会犯的错：**
`GameManager.cs` 有 2000 行，存档逻辑、UI 刷新、音频控制、关卡切换全在里面，两个程序同时改它必然冲突，merge 地狱。更隐蔽的问题：测试某个「关卡加载」功能时必须初始化整个 GameManager，而 GameManager 的 `Awake` 里要初始化音频系统，单元测试环境没有音频驱动，测试直接报错，根本无法写独立测试。

**怎么做：**
- 按职责切分：`SaveSystem`（存档）、`AudioManager`（音频）、`SceneLoader`（场景切换）、`UIManager`（界面）、`PlayerStats`（玩家状态）。
- 每个 Manager 只依赖它需要的少数其他 Manager，依赖关系画出来应该是有向无环图，不是一团乱麻。
- 超过 300 行的类，检查是否承担了两个以上的职责，找到自然的切割点拆分。
- Singleton 不是不能用，但每加一个 Singleton 前问：「这个职责真的需要全局访问吗？」

---

## 正例 / 反例

### 反例：标志位状态 + God object 硬引用

```csharp
// ❌ 反例（Unity C#）— 多 bool 标志位；直接调各系统单例
public class Player : MonoBehaviour
{
    bool isAttacking, isRolling, isStunned, isDead;

    void TakeDamage(float dmg)
    {
        // 每次加新状态都要加新 bool 判断，极易遗漏
        if (!isDead && !isRolling)
        {
            hp -= dmg;
            // 直接耦合 UI、音效、成就，Player 变成 God object
            UIManager.Instance.UpdateHP(hp);
            AudioManager.Instance.PlayHit();
            AchievementSystem.Instance.CheckDamageDealt(dmg);

            if (hp <= 0)
            {
                isDead = true;
                // 同上，继续硬引用...
                GameManager.Instance.OnPlayerDied();
            }
        }
    }
}
```

### 正例：枚举状态机 + 事件总线解耦

```csharp
// ✅ 正例（Unity C#）— 枚举状态机；事件总线解耦；单一职责
public enum PlayerState { Idle, Run, Attack, Roll, Stunned, Dead }

public class Player : MonoBehaviour
{
    [SerializeField] private HealthComponent health;  // 职责分离到组件

    private PlayerState _state = PlayerState.Idle;

    private void TransitionTo(PlayerState next)
    {
        // 状态转移集中在一处，条件清晰
        if (_state == PlayerState.Dead) return;
        _state = next;
    }

    public void TakeDamage(float dmg)
    {
        if (_state is PlayerState.Roll or PlayerState.Dead) return;

        health.Reduce(dmg);
        EventBus.Emit("player_damaged", new DamageEvent(dmg, transform.position));
        // ✅ 不知道也不关心谁在监听——UI、音效、成就系统各自订阅

        if (health.IsDead)
            TransitionTo(PlayerState.Dead);
            EventBus.Emit("player_died", gameObject);
    }
}
```

---

## 自查清单

- [ ] 有状态切换的系统用枚举状态机，没有用多个 bool 标志位组合表示互斥状态。
- [ ] 跨系统通信走事件总线或 signal，系统间没有直接的实例引用。
- [ ] 策划可调的数值/配置放在数据文件（ScriptableObject/DataTable/Resource），没有写死在代码里。
- [ ] 能力用组件组合实现，继承层级不超过 2-3 层，没有基类膨胀问题。
- [ ] 每个 Manager/System 职责单一，没有超过 500 行的万能 God object。
- [ ] 订阅事件的系统在销毁时取消订阅，不会向已销毁对象发送消息。
- [ ] 设计时能画出系统间依赖的有向无环图，不存在循环依赖。
