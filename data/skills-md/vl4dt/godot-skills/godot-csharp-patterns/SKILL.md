---
name: godot-csharp-patterns
description: "C# Mono patterns for Godot 4.x: Export attributes, signal handling, performance optimization, GDExtension interop, and best practices for first-class C# support. Use when writing C# code in Godot."
license: MIT
compatibility:
  - godot-4.0
  - godot-4.1
  - godot-4.2
  - godot-4.3
  - godot-4.4
  - godot-4.5
  - godot-4.6
  - godot-4.7
metadata:
  author: vl4dt
  version: 0.1.0
  tags:
    - godot
    - csharp
    - mono
    - performance
  created: 2026-06-20
---

# C# Patterns for Godot 4.x

Best practices for Godot's first-class C# (Mono) support.

## Export Attributes

### Inspector Properties

```csharp
using Godot;

public partial class Player : CharacterBody2D
{
    // Basic export
    [Export] public float Speed { get; set; } = 200f;

    // With range
    [Export(PropertyHint.Range, "0,100,0.5")]
    public float JumpForce { get; set; } = 400f;

    // File path
    [Export(FileFilter = "*.png,*.svg")]
    public string IconPath { get; set; } = "";

    // Resource export
    [Export] public PackedScene BulletScene { get; set; }

    // Enum with hint
    [Export] public MovementMode MoveMode { get; set; }

    public enum MovementMode
    {
        Walk,
        Run,
        Sprint
    }
}
```

### Export Categories

```csharp
[ExportGroup("Combat")]
[Export] public int AttackDamage { get; set; } = 10;
[Export] public float AttackCooldown { get; set; } = 0.5f;

[ExportGroup("Movement")]
[Export] public float MoveSpeed { get; set; } = 200f;
[Export] public float JumpForce { get; set; } = 400f;
```

## Signal Handling

### C# Event Syntax vs Godot Signals

```csharp
// Godot signal declaration in GDScript (autoload)
// class_name EventBus extends Node
// signal player_died(Vector2 position)

// C# subscriber
public override void _Ready()
{
    // Method reference (recommended — auto-disconnect on free)
    EventBus.PlayerDied += OnPlayerDied;

    // Lambda (requires manual disconnect)
    EventBus.PlayerDied += (pos) => GD.Print($"Died at {pos}");
}

public override void _ExitTree()
{
    // Clean up lambda subscriptions
    EventBus.PlayerDied -= OnPlayerDied;
}

private void OnPlayerDied(Vector2 position)
{
    GD.Print($"Player died at {position}");
}
```

### Using Godot.Signal for C#-Side Signals

```csharp
public partial class Enemy : CharacterBody2D
{
    [Signal] public delegate void HealthChangedEventHandler(int newHealth);
    [Signal] public delegate void DefeatedEventHandler();

    private int health = 100;

    public void TakeDamage(int amount)
    {
        health -= amount;
        EmitSignal(SignalName.HealthChanged, health);

        if (health <= 0)
        {
            EmitSignal(SignalName.Defeated);
            QueueFree();
        }
    }
}
```

## Performance Considerations

### Avoiding GC Pressure

```csharp
// Bad: Creates garbage every frame
public override void _Process(double delta)
{
    var text = $"Score: {score}";  // String allocation
    label.Text = text;
}

// Good: Reuse objects, avoid allocations
private readonly StringBuilder _sb = new();

public override void _Process(double delta)
{
    _sb.Clear();
    _sb.Append("Score: ");
    _sb.Append(score);
    label.Text = _sb.ToString();
}
```

### Structs vs Classes

```csharp
// Use structs for small, short-lived data
public struct Vector2Int
{
    public int X { get; }
    public int Y { get; }
    public Vector2Int(int x, int y) => (X, Y) = (x, y);
}

// Use classes for objects with identity/lifetime
public class PlayerData : Resource
{
    public string Name { get; set; }
    public int Level { get; set; }
}
```

### Instance Pooling

```csharp
public partial class BulletPool : Node
{
    private readonly Queue<Bullet> _pool = new();
    private readonly PackedScene _bulletScene;

    public BulletPool(PackedScene bulletScene) => _bulletScene = bulletScene;

    public Bullet Get()
    {
        if (_pool.TryDequeue(out var bullet))
        {
            bullet.Visible = true;
            return bullet;
        }
        return _bulletScene.Instantiate<Bullet>();
    }

    public void Return(Bullet bullet)
    {
        bullet.Visible = false;
        bullet.QueueFree();
        _pool.Enqueue(bullet);
    }
}
```

## GDExtension Interop

### Calling GDScript from C#

```csharp
// GDScript (autoload "GameData")
// class_name GameData extends Node
// var high_score: int = 0

// C# access
var gameData = Engine.GetSingleton("GameData") as GodotObject;
var highScore = gameData.Get("high_score");
```

### Exposing C# to GDScript via GDExtension

Create a `.gdextension` file to expose C# classes to GDScript projects.

## Godot 4.7 C# Notes

- C# fully supports new 4.7 features including VirtualJoystick and tween_await()
- Use `await` with tweens for async animation sequences
- Export attributes work the same — no changes in 4.7

## MCP Bridge Tools (Optional — Live Editor Integration)

When the MCP bridge is running (Phase 2), these tools can inspect and modify your project live:

- **`script_read`** — Read C# script files for review
- **`script_edit`** — Update C# scripts directly
- **`script_validate`** — Validate C# scripts for syntax errors
- **`scene_tree`** — Inspect scene hierarchy to verify node composition
- **`class_db_info`** — Query Godot class info for C# interop patterns

> **Note:** MCP tools require the Godot editor to be running with the MCP plugin enabled. Skills work independently without the bridge.

## References

- [C# API Reference](references/csharp-api.md)
- [Performance Guide](references/performance.md)
- [GDExtension Guide](references/gdextension.md)
