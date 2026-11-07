---
name: godot-csharp
description: Godot C# specialist for .NET 8 integration, Godot 4.6.1 C# API patterns, async/await, signals, and modern C# idioms.
license: MIT
---

# Godot C# Specialist Skill (Godot 4.6.1)

Modern C# patterns for Godot 4.6.1 with .NET 8.

---

## ⚠️ EXECUTION RULES

1. **ONE PHASE PER TURN** — Execute only one phase
2. **ASK BEFORE WRITING** — Don't create files without approval
3. **MATCH PROJECT STYLE** — Check existing C# patterns in project
4. **MODERN PRACTICES** — Use Godot 4.6.1 idioms, not legacy patterns

---

## Purpose

Use this skill when:
- Writing or reviewing Godot C# code
- Setting up .NET 8 project structure
- Integrating .NET libraries
- Converting between GDScript and C#
- Modernizing legacy Godot 3 C# code

## Coding Standards Reference

**MUST follow**: `.opencode/docs/coding-standards.md` (C# section)

All C# code must comply with:
- Naming conventions (PascalCase for classes, camelCase for private fields)
- [GlobalClass] attribute for node registration
- [Export] patterns (strongly typed exports)
- [Signal] declaration patterns
- async/await with ToSignal
- Node references best practices
- GD.Print instead of Console.WriteLine

**Performance Threshold**: >1000 calls/frame → delegate to godot-gdextension

---

## Godot 4.6.1 Modern Practices

### [GlobalClass] — Register Custom Nodes

让 C# 类直接出现在编辑器的"添加节点"列表中：

```csharp
// ✅ Modern: 直接在编辑器中作为节点使用
[GlobalClass]
public partial class PlayerController : CharacterBody2D
{
    // 这个类现在可以直接在编辑器中添加
}

[GlobalClass]
public partial class HealthComponent : Node
{
    // 可作为独立组件添加到任意节点
}

// ❌ Legacy: 需要先创建 Node 再挂脚本
public partial class PlayerController : CharacterBody2D { }
```

**好处**:
- 类型直接出现在节点列表
- 无需手动创建场景文件
- 更好的类型安全

---

### Node References — 强类型导出

**❌ Legacy (Godot 3 风格)**:
```csharp
[Export] public NodePath HealthBarPath { get; set; }
private ProgressBar _healthBar;

public override void _Ready()
{
    _healthBar = GetNode<ProgressBar>(HealthBarPath);
}
```

**✅ Modern (Godot 4.6.1)**:
```csharp
// 方式 1: 直接导出节点类型
[Export]
public ProgressBar HealthBar { get; set; }

// 方式 2: 使用 Scene Unique Nodes (场景唯一节点)
// 在编辑器中将节点设为 Unique Name (%HealthBar)
private ProgressBar _healthBar;

public override void _Ready()
{
    _healthBar = GetNode<ProgressBar>("%HealthBar");
}

// 方式 3: 使用 GetNode<T> 缓存
private ProgressBar _healthBar;

public override void _Ready()
{
    _healthBar = GetNode<ProgressBar>("HealthBar");
}
```

**推荐**:
- 单一引用 → 直接 `[Export]` 节点类型
- 多处引用 → Scene Unique Node (`%NodeName`)
- 动态节点 → `GetNode<T>()`

---

### Export Attributes — 完整指南

```csharp
// 基础导出
[Export]
public float Speed { get; set; } = 200.0f;

// 范围导出
[Export(PropertyHint.Range, "0,100,0.1")]
public float Health { get; set; } = 100.0f;

// 节点导出 (Modern)
[Export]
public ProgressBar HealthBar { get; set; }

// 资源导出
[Export]
public Texture2D Icon { get; set; }

// 枚举导出
public enum EnemyType { Melee, Ranged, Boss }

[Export]
public EnemyType Type { get; set; }

// 数组导出
[Export]
public WeaponData[] Weapons { get; set; } = Array.Empty<WeaponData>();

// 文件导出
[Export(PropertyHint.File, "*.tscn")]
public string LevelPath { get; set; }
```

---

### Signals — C# 事件模式

```csharp
// 定义信号 (Godot 4 方式)
[Signal]
public delegate void HealthChangedEventHandler(float newHealth, float maxHealth);

[Signal]
public delegate void PlayerDiedEventHandler();

// 触发信号
public void TakeDamage(float amount)
{
    Health -= amount;
    EmitSignal(SignalName.HealthChanged, Health, MaxHealth);
    
    if (Health <= 0)
    {
        EmitSignal(SignalName.PlayerDied);
    }
}

// 连接信号 (Godot 4.6.1)
public override void _Ready()
{
    // C# 事件方式 (推荐)
    Button.Pressed += OnButtonPressed;
    
    // 自定义信号
    HealthChanged += OnHealthChanged;
}

private void OnButtonPressed()
{
    GD.Print("Button pressed!");
}

private void OnHealthChanged(float newHealth, float maxHealth)
{
    UpdateHealthBar(newHealth, maxHealth);
}

// 断开连接 (防止内存泄漏)
public override void _ExitTree()
{
    Button.Pressed -= OnButtonPressed;
    HealthChanged -= OnHealthChanged;
}
```

---

### GD.Print vs Console

```csharp
// ✅ 使用 Godot 的日志系统
GD.Print("普通日志");
GD.PushWarning("警告");
GD.PushError("错误");

// 调试专用
GD.PrintRich("[color=red]红色文本[/color]");
GD.PrintErr("错误输出");

// ❌ 不要用 Console (不会显示在 Godot 输出)
Console.WriteLine("...");  // 无效
```

---

## Async/Await Patterns

### 使用 ToSignal

```csharp
// ✅ 正确 — 等待 Godot 定时器
await ToSignal(GetTree().CreateTimer(1.0), SceneTreeTimer.SignalName.Timeout);

// ✅ 正确 — 等待动画完成
await ToSignal(AnimationPlayer, AnimationPlayer.SignalName.AnimationFinished);

// ✅ 正确 — 等待自定义信号
await ToSignal(this, SignalName.HealthChanged);

// ❌ 错误 — Task.Delay 会在 Godot 主循环外运行，导致帧同步问题
await Task.Delay(1000);  // 不要这样用！
```

### ⚠️ await 后必须检查节点有效性

节点可能在 await 期间被释放：

```csharp
public async void PerformAttack()
{
    IsAttacking = true;
    
    AnimationPlayer.Play("attack");
    await ToSignal(AnimationPlayer, AnimationPlayer.SignalName.AnimationFinished);
    
    // ⚠️ 必须检查！节点可能已被释放
    if (!IsInstanceValid(this)) return;
    
    DealDamage();
    IsAttacking = false;
}
```

### fire-and-forget vs Task 返回

```csharp
// fire-and-forget（事件回调用）
public async void OnButtonPressed()
{
    await LoadDataAsync();
}

// 可测试的异步方法（返回 Task）
public async Task LoadLevelAsync(string levelPath)
{
    var resource = GD.Load<PackedScene>(levelPath);
    var instance = resource.Instantiate<Node>();
    GetTree().CurrentScene.AddChild(instance);
}
```

---

## 集合类型选择

### C# 内部集合 vs Godot 集合

```csharp
// ✅ C# 内部使用 — 标准 .NET 集合（性能更好）
private List<Enemy> _activeEnemies = new();
private Dictionary<string, float> _stats = new();
private HashSet<Item> _collectedItems = new();

// ⚠️ 仅在与 GDScript 交互或导出到检查器时使用 Godot 集合
[Export] public Godot.Collections.Array<Item> StartingItems { get; set; } = new();
[Export] public Godot.Collections.Dictionary<string, int> ItemCounts { get; set; } = new();
```

### 选择指南

| 场景 | 使用类型 | 原因 |
|------|----------|------|
| C# 内部逻辑 | `List<T>`, `Dictionary<K,V>` | 性能最优，无封送开销 |
| 导出到检查器 | `Godot.Collections.Array<T>` | Godot 序列化要求 |
| 传递给 GDScript | `Godot.Collections.*` | 跨语言兼容 |
| 大量数值数据 | `Godot.Collections.Packed*Array` | 内存连续，性能优化 |

---

## JSON 处理

### System.Text.Json (.NET 8 内置，推荐)

```csharp
using System.Text.Json;
using System.Text.Json.Serialization;

// 序列化
public class PlayerData
{
    public string Name { get; set; }
    public int Level { get; set; }
    public float Health { get; set; }
}

var player = new PlayerData { Name = "Hero", Level = 10, Health = 100f };

// 序列化为 JSON
string json = JsonSerializer.Serialize(player);

// 美化输出
var options = new JsonSerializerOptions { WriteIndented = true };
string prettyJson = JsonSerializer.Serialize(player, options);

// 反序列化
var loaded = JsonSerializer.Deserialize<PlayerData>(json);

// 异步文件读写
public async Task SaveAsync(string path, PlayerData data)
{
    await using var stream = File.Create(path);
    await JsonSerializer.SerializeAsync(stream, data, options);
}

public async Task<PlayerData?> LoadAsync(string path)
{
    await using var stream = File.OpenRead(path);
    return await JsonSerializer.DeserializeAsync<PlayerData>(stream);
}
```

### 为什么不用 Newtonsoft.Json?

| 特性 | System.Text.Json | Newtonsoft.Json |
|------|------------------|-----------------|
| 性能 | ✅ 更快 | ⚠️ 较慢 |
| 内存 | ✅ 更少 | ⚠️ 更多 |
| 依赖 | ✅ .NET 内置 | ❌ 需要 NuGet |
| .NET 8 | ✅ 原生支持 | ⚠️ 兼容 |

**只有当需要 Newtonsoft 特有功能时才使用它。**

---

## Localization (Godot 4.6.1 新特性)

C# 原生支持翻译提取：

```csharp
// Godot 4.6+ 支持 C# 字符串翻译提取
public void UpdateUI()
{
    // 翻译文本
    var text = Tr("UI_START_GAME");
    StartButton.Text = text;
    
    // 带参数的翻译
    var message = Tr("PLAYER_HEALTH").Format(Health, MaxHealth);
    
    // 复数形式
    var itemText = TrN("ITEM_COUNT", "ITEM_COUNT_PLURAL", itemCount);
}

// 在编辑器中: Project → Localization → Extract Translatable Strings
// 现在可以自动提取 C# 中的 Tr() 字符串
```

---

## Common Patterns

### Singleton/Autoload

```csharp
// GameManager.cs - 添加为 Autoload
public partial class GameManager : Node
{
    public static GameManager Instance { get; private set; }
    
    public override void _Ready()
    {
        Instance = this;
    }
}

// 使用
GameManager.Instance.DoSomething();
```

### State Machine

```csharp
public interface IState
{
    void Enter();
    void Exit();
    void Update(double delta);
}

public class StateMachine : Node
{
    private IState? _currentState;
    
    public void ChangeState(IState newState)
    {
        _currentState?.Exit();
        _currentState = newState;
        _currentState.Enter();
    }
    
    public override void _Process(double delta)
    {
        _currentState?.Update(delta);
    }
}
```

### Object Pooling

```csharp
public partial class BulletPool : Node
{
    [Export] public PackedScene? BulletScene { get; set; }
    [Export] public int PoolSize { get; set; } = 50;
    
    private readonly Queue<Bullet> _pool = new();
    
    public override void _Ready()
    {
        if (BulletScene == null) return;
        
        for (int i = 0; i < PoolSize; i++)
        {
            var bullet = BulletScene.Instantiate<Bullet>();
            bullet.SetProcess(false);
            AddChild(bullet);
            _pool.Enqueue(bullet);
        }
    }
    
    public Bullet? Get()
    {
        if (_pool.Count == 0) return null;
        
        var bullet = _pool.Dequeue();
        bullet.SetProcess(true);
        return bullet;
    }
    
    public void Return(Bullet bullet)
    {
        bullet.SetProcess(false);
        bullet.Hide();
        _pool.Enqueue(bullet);
    }
}
```

---

## GDScript ↔ C# 转换速查

| GDScript | C# |
|----------|-----|
| `func _ready():` | `public override void _Ready()` |
| `func _process(delta):` | `public override void _Process(double delta)` |
| `signal health_changed(val)` | `[Signal] delegate void HealthChangedEventHandler(float val);` |
| `@export var speed: float` | `[Export] public float Speed { get; set; }` |
| `@onready var sprite = $Sprite` | `[Export] public Sprite2D Sprite { get; set; }` |
| `get_node("Path")` | `GetNode<Node>("Path")` |
| `$Sprite` | `GetNode<Sprite2D>("Sprite")` 或 `%Sprite` |
| `queue_free()` | `QueueFree()` |
| `print()` | `GD.Print()` |
| `randf()` | `GD.Randf()` |
| `randi_range(0, 10)` | `GD.RandRange(0, 10)` |
| `Vector2(1, 2)` | `new Vector2(1, 2)` |
| `Color.RED` | `Colors.Red` |
| `await get_tree().create_timer(1.0).timeout` | `await ToSignal(GetTree().CreateTimer(1.0), SceneTreeTimer.SignalName.Timeout)` |

---

## Project Structure

```
src/
├── Core/
│   └── GameManager.cs
├── Gameplay/
│   ├── Player/
│   │   └── PlayerController.cs
│   └── Enemies/
├── UI/
│   └── HUD.cs
└── Utils/
    └── Extensions.cs
```

### .csproj (Godot 4.6.1)

```xml
<Project Sdk="Godot.NET.Sdk/4.6.1">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <EnableDynamicLoading>true</EnableDynamicLoading>
    <RootNamespace>MyGame</RootNamespace>
    <Nullable>enable</Nullable>
    <ImplicitUsings>disable</ImplicitUsings>
  </PropertyGroup>
</Project>
```

---

## 常见错误避免

| 错误 | 修正 |
|------|------|
| `Console.WriteLine()` | `GD.Print()` |
| 缺少 `partial` | `public partial class Player : Node` |
| 使用 `yield` | `await ToSignal()` |
| NodePath + GetNode | 直接 `[Export]` 节点类型 |
| 硬编码路径 | 使用 Scene Unique Nodes (`%Name`) |
| 事件未取消订阅 | 在 `_ExitTree()` 中取消 |
| 使用 Newtonsoft.Json | 使用 `System.Text.Json` |
| 缺少 `[GlobalClass]` | 添加以注册节点 |

## Scene Assembly Protocol (NEW - replaces tscn generation)

### ⚠️ NEVER generate .tscn files directly

LLM-generated scene files are prone to errors:
- Invalid node paths
- Wrong resource UID references
- Property type mismatches

### Instead: Provide Assembly Guide

**After generating C# script, output:**

```markdown
## Scene Assembly Instructions

### Node Tree
```
[RootNode] (type)
├── [Child1] (type) — purpose
├── [Child2] (type) — purpose
│   └── [SubChild] (type) — purpose
```

### Required Components
| Node | Properties | Script |
|------|------------|--------|
| Player | position: (100, 200) | PlayerController.cs |

### Assembly Steps
1. Create root: Add Node → [NodeType]
2. Attach script: Drag file to node
3. Add children: Add Node → set properties
4. Enable Unique Names: Right-click → Access as Unique Name
```

**ASK**: "Scripts created. Follow assembly guide in editor?"

## Completion Recommendations (NEW)

### After C# Implementation

**Step 1: Quick LSP Check**

**TRY**: `lsp_diagnostics` on modified .cs files

**IF errors found**:
```
⚠️ LSP detected [N] issues. Fix before review.
Run `/code-review` after fixing.
```

**Step 2: Suggest Next Steps**

| Implementation Type | Recommended Next Steps |
|---------------------|------------------------|
| Core gameplay code | `/code-review` → Review quality |
| UI code | `/design-review --system UI` → UX validation |
| Performance-critical | Profile in Godot editor first |
| New system | `/technical-director` → Architecture check |

**ASK**: "Would you like to run `/code-review` on these changes?"

---

## Quick Reference

| 需求 | 写法 |
|------|------|
| 注册自定义节点 | `[GlobalClass]` |
| 导出节点引用 | `[Export] public NodeType Node { get; set; }` |
| 定义信号 | `[Signal] delegate void NameEventHandler(...);` |
| 触发信号 | `EmitSignal(SignalName.Name, args)` |
| 等待时间 | `await ToSignal(GetTree().CreateTimer(x), ...)` |
| 加载场景 | `GD.Load<PackedScene>("res://...")` |
| 实例化 | `scene.Instantiate<T>()` |
| 随机数 | `GD.Randf()`, `GD.RandRange()` |
| 日志 | `GD.Print()`, `GD.PushWarning()` |
| JSON | `JsonSerializer.Serialize/Deserialize` |
| 翻译 | `Tr("KEY")` |

---

## 相关 Skills

- **godot-specialist** — 引擎通用指导
- **godot-gdscript** — GDScript 模式 (转换参考)
- **code-review** — 代码质量检查

---

## ⚠️ 常见反模式

### 必须避免的错误

| 错误 | 修正 | 后果 |
|------|------|------|
| 缺少 `partial` 关键字 | `public partial class Player : Node` | 源生成器静默失败，极难调试 |
| 使用 `Task.Delay()` | `await ToSignal(GetTree().CreateTimer(x), ...)` | 破坏帧同步 |
| `GetNode()` 无泛型 | `GetNode<ProgressBar>(...)` | 丢失类型安全 |
| 信号未在 `_ExitTree()` 断开 | 在退出时 `-=` 断开连接 | 内存泄漏、Use-After-Free |
| 信号委托无 `EventHandler` 后缀 | `HealthChangedEventHandler` | 源生成器失败 |
| 静态字段持有节点引用 | 使用实例字段或 Autoload | 场景重载崩溃 |
| 直接调用 `_Ready()` | 让 Godot 自动调用 | 生命周期混乱 |
| Lambda 捕获 `this` 注册信号 | 使用命名方法 | 阻止 GC 回收 |

---

## 版本感知

**关键**: 你的训练数据有知识截止日期。在建议 Godot C# 代码前：

1. 读取 `.opencode/docs/engine-reference/godot/VERSION.md` 确认引擎版本
2. 检查 `deprecated-apis.md` 了解废弃的 API
3. 检查 `breaking-changes.md` 了解版本变更
4. 对于不确定的 API，使用 WebSearch 验证

**Godot 4.x C# 变化要点**:
- 源生成器现在生成 `SignalName` 和 `MethodName` 内部类
- `[GlobalClass]` 行为在不同版本可能有差异
- .NET 版本要求：Godot 4.6+ 需要 .NET 8

不要依赖本文件中的内联版本声明 — 它们可能是错的。始终检查参考文档。