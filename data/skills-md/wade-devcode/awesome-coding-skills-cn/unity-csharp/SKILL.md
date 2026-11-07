---
name: unity-csharp
description: 写 Unity C# 时使用。生命周期、协程、GC、性能、序列化的实战规范。
category: gamedev
tags: [unity, csharp, 性能]
---

# Unity C# 最佳实践

## 何时用

- 开始编写任何 Unity MonoBehaviour 或 ScriptableObject 脚本前。
- Review 他人 Unity C# 代码，发现有 Update 里调 GetComponent 或每帧 new 对象时。
- 接到性能优化任务：帧率抖动、GC Alloc 频繁、Profiler 里 Update 调用栈过深。
- 设计新的配置数据结构，考虑用 ScriptableObject 还是 public 字段时。
- 协程逻辑出现卡死、泄漏、或销毁对象后仍在跑的诡异现象时。

## 核心规则

### 1. 慎用 Update：每帧逻辑最小化

**规则：** Update 里只放真正需要每帧响应的逻辑；能用事件、协程或 InvokeRepeating 驱动的，就不放进 Update；任何 GetComponent、Find、tag 比较一律在 Awake/Start 里缓存，不在 Update 里调用。

**为什么：** AI 和新手最常见的模式是把所有逻辑堆进 Update——"反正每帧都会跑到"。结果是：GetComponent 每帧反射查找，100 个对象就是 100 次反射；倒计时用 `timer -= Time.deltaTime` 没问题，但 UI 刷新、动画触发、状态机判断全挤在里面，Profiler 一看 Update 占 80% CPU。更隐蔽的问题：新人把 `FindObjectOfType<GameManager>()` 放进 Update，场景里一有几十个对象就掉帧，排查时根本不知道从哪查。

**怎么做：**
- 初始化引用全部放 `Awake`（自身组件）或 `Start`（跨对象引用）。
- 定时逻辑用 `InvokeRepeating` 或协程 `WaitForSeconds`，不用 `Update` 里的计数器模拟低频事件。
- 状态变化用 C# event / UnityEvent 通知，订阅方在变化时响应，而不是每帧 poll `if (state == X)`。
- 真正需要每帧的（移动插值、输入读取），保留在 Update，但代码量要极简，复杂运算提取为方法并在注释说明频率必要性。

---

### 2. 防 GC 抖动：高频路径零分配

**规则：** Update、FixedUpdate、协程的热路径里禁止出现 `new`（含 LINQ、字符串拼接、装箱）；高频复用的对象用对象池管理；容器在初始化时预分配容量。

**为什么：** Unity 使用 Mono / IL2CPP 的 GC，GC 触发时会造成明显的帧率刺尖（spike）。AI 写的代码里最常见的杀手：`string.Format($"Score: {score}")` 每帧执行一次，`enemies.Where(e => e.isAlive).ToList()` 每帧生成一个新 List，`new Vector3(...)` 看起来是值类型不会 GC——但装箱到 `object` 参数时就会。新手则喜欢在子弹生成时 `Instantiate`、销毁时 `Destroy`，百发子弹就是百次 GC 压力。

**怎么做：**
- 用 `StringBuilder` 或 `TMP_Text.SetText(format, arg)` 替代字符串拼接。
- LINQ 仅用于编辑器工具或低频初始化代码，运行时热路径改用显式 for 循环。
- 子弹、特效、UI 元素用 `ObjectPool<T>`（Unity 2021+ 内置）或自实现的栈式对象池。
- 用 `List<T>(initialCapacity)` 预分配，避免频繁扩容。
- 用 Unity Profiler 的 Memory 视图确认改动前后 GC Alloc 列清零。

---

### 3. 协程与生命周期：时序清楚，防泄漏

**规则：** 明确 Awake → OnEnable → Start → Update → OnDisable → OnDestroy 的时序；协程在对象 `SetActive(false)` 或 `OnDisable` 时自动停止，但 `OnDestroy` 时不会自动停止跑在其他 MonoBehaviour 上的协程；协程引用必须在 `OnDisable`/`OnDestroy` 里主动 `StopCoroutine`。

**为什么：** AI 最典型的错误：在 `Awake` 里启动协程并访问 `Start` 才会初始化完毕的跨组件引用，导致 NullReferenceException；或者在 `OnDestroy` 不清理，导致协程持有对已销毁对象的引用，每帧报 `MissingReferenceException`，但对象本体早就没了，难以溯源。新手则习惯用 `StartCoroutine` 后不记返回值，后来想停却只能 `StopAllCoroutines`，误杀其他协程。

**怎么做：**
- 跨组件的初始化调用放 `Start`，同组件自身初始化放 `Awake`。
- `StartCoroutine` 返回值存成字段：`_loopCoroutine = StartCoroutine(Loop());`。
- `OnDisable` 里 `if (_loopCoroutine != null) StopCoroutine(_loopCoroutine);`。
- 需要在对象销毁后继续执行的逻辑（如过场动画），挂到场景级别的长生命周期对象上，不挂被销毁的对象上。
- 协程里访问任何外部引用之前，加 `if (this == null) yield break;` 防止僵尸协程。

---

### 4. 序列化：用 [SerializeField] 私有字段，配置走 ScriptableObject

**规则：** Inspector 可调的字段声明为 `private` + `[SerializeField]`，不用 `public` 字段；多处共享的静态配置（数值、曲线、音效引用）抽成 ScriptableObject 资产；运行时不修改 prefab 资产本身，只改实例。

**为什么：** AI 生成代码时为了"方便 Inspector 看到"，大量字段声明成 `public`，导致类的 API 边界模糊，其他脚本可以随意修改本不该暴露的状态。新手则把所有敌人的血量、速度都硬编码在 MonoBehaviour 字段里，20 种敌人要改数值就要手动改 20 个 prefab。ScriptableObject 的价值在于：一份资产，多个 prefab 引用，改一处全更新；且美术/策划可以在编辑器里直接调，不需要改代码。运行时误改 `prefab.GetComponent<X>().hp = 5` 会永久写入资产（编辑器模式下），是高频"改完关编辑器发现数值乱了"的根源。

**怎么做：**
- `[SerializeField] private float _speed = 5f;` — 外部只读时加 `public float Speed => _speed;`。
- 配置数据：创建 `[CreateAssetMenu] public class EnemyConfig : ScriptableObject`，字段暴露在 Inspector，在 prefab 里只挂引用。
- 运行时修改只改实例字段，绝对不调用 `PrefabUtility` 或直接修改资产路径上的对象。
- `[Header("")]` 和 `[Tooltip("")]` 给 Inspector 分组加注释，而不是靠 public 字段名猜。

---

### 5. 假 null 陷阱：Destroy 后引用不等于 null

**规则：** `Destroy(obj)` 后，C# 引用变量仍然持有一个"假对象"（Unity 重载了 `==` 运算符让它等于 null，但 `object.ReferenceEquals(obj, null)` 为 false）；判空用 `if (obj == null)` 而非 `if (obj != null)` 后直接用；不缓存已销毁对象的引用；用 null 条件运算符 `?.` 时要注意 Unity 假 null 会绕过重载，导致访问已销毁对象。

**为什么：** 这是 Unity C# 里最隐蔽的 bug 来源之一，AI 几乎每次都会犯。场景：`_target = FindObjectOfType<Enemy>(); ... _target?.Attack();`——Enemy 已经被 Destroy，`?.` 用的是 C# 原生引用判断（不走 Unity 重载），`_target` 不是真 null，于是 `Attack()` 被调用，访问已释放的 C++ 底层对象，抛出 `MissingReferenceException`。更诡异的是，这个异常信息指向调用栈而不是销毁点，新手排查数小时找不到原因。

**怎么做：**
- 判空统一用 `if (obj == null)`（走 Unity 重载），不用 `obj?.Method()`、`obj ?? fallback` 在 MonoBehaviour 引用上。
- 需要用 `?.` 语法时，先 `var safeRef = obj; if (safeRef == null) return; safeRef.Method();`。
- 对象池回收时主动将缓存字段清 null：`_target = null;`。
- 养成习惯：任何从外部注入的 MonoBehaviour 引用，使用前都过一次 `if (ref == null) { Debug.LogError(...); return; }`。

---

## 正例 / 反例

### 反例：Update 里 GetComponent + 每帧 new 字符串

```csharp
// 反例 — 每帧 GetComponent，每帧字符串格式化，每帧 GC Alloc
void Update()
{
    var rb = GetComponent<Rigidbody2D>();          // ❌ 每帧反射查找
    rb.velocity = new Vector2(_speed, rb.velocity.y);

    var ui = GetComponent<TextMeshProUGUI>();       // ❌ 又一次反射
    ui.text = "Score: " + GameManager.score;       // ❌ 每帧字符串拼接，GC Alloc
}
```

```csharp
// 正例 — 缓存引用，热路径零 GC
private Rigidbody2D _rb;
private TextMeshProUGUI _scoreText;

void Awake()
{
    _rb = GetComponent<Rigidbody2D>();             // ✅ 只查一次
    _scoreText = GetComponent<TextMeshProUGUI>();
}

void Update()
{
    _rb.velocity = new Vector2(_speed, _rb.velocity.y);
}

// 分数变化时由事件触发，不在 Update 轮询
void OnScoreChanged(int newScore)
{
    _scoreText.SetText("Score: {0}", newScore);    // ✅ TMP 零 GC 重载
}
```

---

### 反例：协程泄漏 + 假 null 陷阱

```csharp
// 反例 — 协程不清理，?.  绕过 Unity 假 null
private Enemy _target;

void Start()
{
    _target = FindObjectOfType<Enemy>();
    StartCoroutine(ChaseLoop());               // ❌ 不保存引用，无法单独停止
}

IEnumerator ChaseLoop()
{
    while (true)
    {
        _target?.MoveTo(transform.position);   // ❌ ?. 绕过 Unity == 重载，可能访问已销毁对象
        yield return new WaitForSeconds(0.1f);
    }
}
// OnDisable/OnDestroy 里什么都没有 — ❌ 协程泄漏
```

```csharp
// 正例 — 保存协程引用，OnDisable 清理，判空走 Unity 重载
private Enemy _target;
private Coroutine _chaseCoroutine;

void Start()
{
    _target = FindObjectOfType<Enemy>();
    _chaseCoroutine = StartCoroutine(ChaseLoop()); // ✅ 保存引用
}

IEnumerator ChaseLoop()
{
    while (true)
    {
        if (_target == null) yield break;          // ✅ 走 Unity == 重载，正确检测假 null
        _target.MoveTo(transform.position);
        yield return new WaitForSeconds(0.1f);
    }
}

void OnDisable()
{
    if (_chaseCoroutine != null)
    {
        StopCoroutine(_chaseCoroutine);            // ✅ 主动清理
        _chaseCoroutine = null;
    }
}
```

---

## 自查清单

- [ ] Update 里没有 GetComponent、Find、FindObjectOfType 调用，全部已在 Awake/Start 缓存。
- [ ] 热路径（Update/FixedUpdate/协程循环体）里无 `new` 分配、无字符串拼接、无 LINQ。
- [ ] 每个 StartCoroutine 的返回值都保存了，且在 OnDisable 或 OnDestroy 里有对应的 StopCoroutine。
- [ ] 所有 Inspector 可调字段声明为 `private [SerializeField]`，无不必要的 `public` 字段。
- [ ] 共享配置数据已抽为 ScriptableObject，未硬编码在 MonoBehaviour 字段或直接修改 prefab 资产。
- [ ] 对 MonoBehaviour 引用的判空全部使用 `if (obj == null)` 而不是 `?.` 或 `??`。
- [ ] Profiler 确认改动前后 GC Alloc 无异常峰值，Update 调用耗时在预算内。
