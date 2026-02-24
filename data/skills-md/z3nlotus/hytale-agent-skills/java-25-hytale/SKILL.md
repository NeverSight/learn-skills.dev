---
name: java-25-hytale
description: Java 25 features and patterns for Hytale plugin development. Covers modern Java syntax (records, sealed classes, pattern matching, virtual threads), JDK installation, and Hytale-specific Java conventions. Use when writing Java code for Hytale plugins or troubleshooting Java version issues.
---

# Java 25 for Hytale

Modern Java features and patterns for Hytale plugin development.

## Why Java 25?

Hytale server runs on **Java 25** - you must use this version for plugin development.

## Installation

### Windows (Recommended)

```powershell
# Using winget (Windows Package Manager)
winget install EclipseAdoptium.Temurin.25.JDK

# Verify installation
java --version
```

### Manual Download

1. Go to [Adoptium.net](https://adoptium.net/)
2. Download Temurin 25 (LTS)
3. Run installer
4. Add to PATH if not automatic

### macOS

```bash
brew install --cask temurin@25
```

### Linux

```bash
# Ubuntu/Debian
sudo apt install temurin-25-jdk

# Fedora
sudo dnf install temurin-25-jdk
```

---

## Key Java 25 Features for Hytale

### Records (Data Classes)

Perfect for immutable data objects:

```java
// Instead of verbose class with getters/equals/hashCode
public record PlayerData(String name, int level, double health) {}

// Usage
var data = new PlayerData("Steve", 10, 100.0);
System.out.println(data.name());  // "Steve"
```

### Pattern Matching

Cleaner type checks:

```java
// Old way
if (obj instanceof Player) {
    Player player = (Player) obj;
    player.sendMessage("Hello!");
}

// Java 25 way
if (obj instanceof Player player) {
    player.sendMessage("Hello!");
}
```

### Switch Expressions

```java
String message = switch (gameMode) {
    case SURVIVAL -> "Good luck surviving!";
    case CREATIVE -> "Build freely!";
    case ADVENTURE -> "Explore the world!";
    default -> "Welcome!";
};
```

### Pattern Matching in Switch

```java
Object entity = getEntity();
String type = switch (entity) {
    case Player p -> "Player: " + p.getName();
    case NPC n -> "NPC: " + n.getType();
    case Monster m -> "Monster: " + m.getName();
    case null -> "No entity";
    default -> "Unknown entity";
};
```

### Sealed Classes

Restrict inheritance:

```java
public sealed class GameEvent permits PlayerEvent, WorldEvent, BlockEvent {
    // Base event class
}

public final class PlayerEvent extends GameEvent {
    // Cannot be extended further
}
```

### Virtual Threads (Project Loom)

Lightweight concurrency for async operations:

```java
// Old way - platform threads are heavy
new Thread(() -> loadPlayerData()).start();

// Java 25 way - virtual threads are lightweight
Thread.startVirtualThread(() -> loadPlayerData());

// Or with executor
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> loadPlayerData());
    executor.submit(() -> loadWorldData());
}
```

### Text Blocks

Multi-line strings:

```java
String json = """
    {
        "name": "MyPlugin",
        "version": "1.0.0",
        "author": "YourName"
    }
    """;
```

---

## Hytale-Specific Patterns

### Null Safety

Always check for null components:

```java
// Good
var health = entity.getComponent(HealthComponent.class);
if (health != null) {
    health.heal(10);
}

// Better with Optional
entity.getComponentOptional(HealthComponent.class)
    .ifPresent(h -> h.heal(10));
```

### Functional Event Handling

```java
// Lambda for simple handlers
registerEventListener(PlayerJoinEvent.class, 
    e -> e.getPlayer().sendMessage("Welcome!"));

// Method reference for reusable handlers
registerEventListener(PlayerJoinEvent.class, this::onPlayerJoin);

private void onPlayerJoin(PlayerJoinEvent event) {
    // Complex logic here
}
```

### Stream API for Collections

```java
// Filter and process players
List<Player> onlinePlayers = getServer().getPlayers();

onlinePlayers.stream()
    .filter(p -> p.getLevel() > 10)
    .forEach(p -> p.giveReward("veteran_badge"));

// Count specific types
long monsterCount = getWorld().getEntities().stream()
    .filter(e -> e instanceof Monster)
    .count();
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Wrong Java version | Set JAVA_HOME to Java 25 |
| Class not found | Check Gradle compileOnly dependency |
| Unsupported class version | Rebuild with Java 25 toolchain |
| IntelliJ uses wrong JDK | Project Structure → SDK → Java 25 |

---

## IDE Configuration

### IntelliJ IDEA

1. **File → Project Structure → Project**
2. Set **SDK** to Java 25
3. Set **Language Level** to 25

### Gradle (build.gradle.kts)

```kotlin
java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(25))
    }
}
```
