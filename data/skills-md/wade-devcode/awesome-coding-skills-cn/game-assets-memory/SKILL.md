---
name: game-assets-memory
description: 管理游戏资源与内存时使用。加载/卸载、图集、包体、泄漏防治。
category: gamedev
tags: [资源, 内存, 加载]
---

# 资源与内存

## 何时用

- 新增资源加载逻辑（模型、纹理、音效、配置表）之前。
- 发现内存持续增长、场景切换后内存不降、或 Profiler 显示某类资源异常堆积时。
- 接入新的资源管理系统（Addressables、AssetBundle、自研热更）前做方案评审时。
- 出现「卸载了但内存没降」「切场景崩溃」「包体超预算」等问题排查时。

## 核心规则

### 1. 大资源必须异步加载

**规则：** 纹理、音频、场景、模型等大资源一律走异步接口加载，绝不在主线程同步读取；加载期间必须有合适的 loading 表现，加载完成回调后再使用资源。

**为什么：** 最常犯的错是原型阶段用同步加载图方便，上线前"有时间再改"——结果积累了几十处同步加载，进游戏时主线程卡顿 2 秒，ANR 投诉爆仓。另一个坑：异步加载发起后立刻用资源（还没加载完），导致空引用崩溃或用到上一次缓存的错误资源。

**怎么做：**
```csharp
// Unity 示例
// 反例 — 同步加载阻塞主线程
var tex = Resources.Load<Texture2D>("hero/sword");   // ❌ 主线程阻塞

// 正例 — 异步加载，回调中使用
IEnumerator LoadHeroAsync(string key, Action<GameObject> onLoaded) {
    var handle = Addressables.LoadAssetAsync<GameObject>(key);
    yield return handle;                          // ✅ 异步等待
    if (handle.Status == AsyncOperationStatus.Succeeded) {
        onLoaded(handle.Result);                  // ✅ 加载完再用
    } else {
        Debug.LogError($"加载失败: {key}");
    }
}
```
- 加载过程中显示 loading 进度条或骨骼屏；加载超时（如 10 秒）要有降级或报错逻辑，不能死等。
- 预加载（Preload）在合适时机（进房间动画期间）提前触发，不要等玩家操作时才开始加载。

---

### 2. 引用计数与卸载时机必须明确

**规则：** 每个资源的生命周期（谁持有、何时释放）必须在接入时明确设计；场景切换时主动释放当前场景独占的资源，不依赖 GC 或引擎的"自动"回收。

**为什么：** 最典型的泄漏路径：战斗场景加载了 50 个怪物预制体的纹理，战斗结束切回大厅，没有主动 Release，Addressables 的引用计数没归零，纹理全留在内存里。打完十场战斗内存涨到崩溃。反向问题也有：卸载太激进，在某个地方还持有引用时就强制卸载，运行时出现粉色/错误材质。

**怎么做：**
- 使用 Addressables/AssetBundle 时，每次 `LoadAssetAsync` 对应一次 `Release`，用 RAII 或引用计数封装保证配对。
- 场景切换时有明确的「场景资源卸载」阶段：先通知所有系统释放本场景资源引用，再触发 `UnloadUnusedAssets`。
- 共享资源（公共 UI 图集、常驻音效）单独管理，不随场景卸载；战斗专属资源随战斗结束卸载。
- 建立资源持有关系图（哪个系统持有哪些资源），在代码注释或文档中维护，避免「不知道谁在引用」的黑盒状态。

---

### 3. 图集与压缩格式要选对

**规则：** UI 精灵和 2D 素材必须打图集减少 Draw Call；纹理压缩格式按平台和内容类型选择（Android 用 ETC2/ASTC，iOS 用 ASTC，PC 用 BC7/DXT5），不能全部用未压缩 RGBA32。

**为什么：** 没用图集的 UI 场景，100 个图标就是 100 个 Draw Call，低端机直接掉帧。纹理压缩格式用错更隐蔽：开发时在 PC 上用 RGBA32 完全没问题，发布到手机后内存翻 4 倍（一张 1024×1024 的 RGBA32 纹理占 4MB，ASTC 6×6 只占约 0.4MB），低端安卓机直接 OOM。

**怎么做：**
- UI 按功能模块分图集（主界面、战斗 HUD、商店分别打包），单张图集不超过 2048×2048，避免单图集过大导致无法在低端机加载。
- 纹理导入设置模板化：为 Android/iOS/PC 各建一套 Preset，批量应用，避免手动逐张配置遗漏。
- 带 Alpha 通道的 UI 纹理用 ASTC 4×4（iOS/高端安卓）或 ETC2 RGBA8（中低端安卓）；无 Alpha 的背景用 ETC2 RGB8 或 ASTC 6×6。
- 定期用 Memory Profiler / Texture Overview 工具扫一遍纹理列表，找出没被图集收录的散图和格式设置异常的资源。

---

### 4. 监听/回调/缓存在销毁时必须清理

**规则：** 任何在对象初始化时注册的事件监听、委托回调、定时器、或加入全局缓存的引用，必须在对象销毁时对称地反注册/清除，禁止依赖"对象被回收后监听自动失效"的侥幸心理。

**为什么：** 最隐蔽的内存泄漏：UI 面板注册了全局事件总线的监听（`EventBus.on("kill", OnKill)`），面板关闭时忘了反注册。面板对象被「销毁」了，但事件总线还持有对它的引用，GC 永远不会回收它。玩家反复开关面板，内存里堆着几十个"已关闭"的面板实例。更严重的是：Dead 对象收到事件后访问已回收的 UI 组件，直接 NullReferenceException 崩溃。

**怎么做：**
```csharp
// Unity 示例
public class KillFeedUI : MonoBehaviour {
    void OnEnable() {
        EventBus.Subscribe("kill", OnKill);     // ✅ 启用时注册
    }

    void OnDisable() {
        EventBus.Unsubscribe("kill", OnKill);   // ✅ 禁用时对称反注册
    }

    // 反例 — 只在 Start 注册，没有对应的 OnDestroy 反注册
    // void Start() { EventBus.Subscribe("kill", OnKill); }  // ❌
}
```
- 静态字典/列表缓存中存放对象引用时，优先使用 `WeakReference`（弱引用），或在对象销毁时主动从缓存中移除。
- Coroutine/Timer 在对象销毁前必须 Stop/Cancel；异步操作持有的 CancellationToken 在销毁时触发。

---

### 5. 内存与包体要设预算，定期用工具检查峰值

**规则：** 项目立项时为内存和包体设定明确预算（如：手机目标设备内存上限 1.2GB，包体初始安装包不超过 150MB），并在 CI 或版本里程碑节点用自动化工具检查，超预算视为 P1 问题。

**为什么：** 最常见的失控模式：开发初期没有预算约束，美术资源按"效果最好"的规格产出，等到上线前两周发现手机低端机直接崩溃或包体超出渠道限制，再来全量优化——成本是前期的 10 倍。另一个盲区：开发机内存 16GB，测试机 8GB，发布目标机 3GB，开发全程感觉"没问题"，实际目标用户全程 OOM。

**怎么做：**
- 明确定义目标设备（如：低端 Android 3GB RAM、iOS iPhone 12 作为最低支持型号）并用真机定期测试。
- 在 CI 流水线中加入包体检查脚本，超过阈值自动发告警；Memory Profiler 截图在每个里程碑节点存档对比。
- 为各类资源分配子预算（纹理、音频、代码、Shader 各多少），防止一类资源无限膨胀挤占其他资源。
- 内存峰值出现在战斗中场景最复杂时，专门在该时机做 Profiler 快照，不能只测大厅/菜单场景。

## 正例 / 反例

### 反例：忘记 Release，场景切换后内存不降

```csharp
// 反例 — 加载后没有对应的 Release，切场景时内存全留着
public class BattleManager : MonoBehaviour {
    List<AsyncOperationHandle<GameObject>> handles = new();

    async void SpawnEnemy(string key) {
        var h = Addressables.LoadAssetAsync<GameObject>(key);
        await h.Task;
        handles.Add(h);
        Instantiate(h.Result, spawnPos, Quaternion.identity);
    }

    void OnDestroy() {
        // ❌ 没有 foreach Release，所有纹理/预制体留在内存里
    }
}
```

```csharp
// 正例 — OnDestroy 中对称 Release
public class BattleManager : MonoBehaviour {
    List<AsyncOperationHandle<GameObject>> handles = new();

    async void SpawnEnemy(string key) {
        var h = Addressables.LoadAssetAsync<GameObject>(key);
        await h.Task;
        handles.Add(h);
        Instantiate(h.Result, spawnPos, Quaternion.identity);
    }

    void OnDestroy() {
        foreach (var h in handles) {
            Addressables.Release(h);   // ✅ 对称释放，引用计数归零，资源可被卸载
        }
        handles.Clear();
    }
}
```

---

### 反例：UI 精灵没打图集，Draw Call 爆炸

```
# 反例 — 每个图标单独一张纹理
Assets/UI/Icons/
  sword_icon.png       (独立纹理，1 Draw Call)
  shield_icon.png      (独立纹理，1 Draw Call)
  potion_icon.png      (独立纹理，1 Draw Call)
  ... 80 个图标 = 80 个 Draw Call ❌

# 正例 — 打成图集，共享同一纹理
Assets/UI/Atlas/
  BattleHUD_Atlas.png  (1 张图集，包含所有战斗 HUD 图标，1 Draw Call ✅)
```

## 自查清单

- [ ] 所有大资源（纹理、音频、预制体、场景）走异步加载接口，主线程没有同步 Load 调用。
- [ ] 每个 `LoadAssetAsync` 都有对应的 `Release`，且在对象销毁或场景卸载时被调用到。
- [ ] UI 精灵已按模块打图集，没有大量散图直接引用；图集大小未超过 2048×2048。
- [ ] 各平台纹理压缩格式已设置（非 RGBA32 全平台默认），通过 Texture Overview 工具确认。
- [ ] 所有事件监听、委托订阅在对象 OnDisable/OnDestroy 中有对称的反注册。
- [ ] 项目有明确的内存与包体预算文档，且在最近一次里程碑节点用 Profiler 验证未超预算。
- [ ] 内存峰值测试在战斗中场景最复杂时刻（而非菜单/大厅）在目标低端设备上完成过。
