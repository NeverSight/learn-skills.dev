---
name: hytale-ecs
description: Entity Component System (ECS) architecture patterns for Hytale plugin development. Covers ECS fundamentals, component design, system implementation, entity queries, and best practices. Use when working with entities, implementing game mechanics, or understanding Hytale's architecture.
---

# Hytale Entity Component System (ECS)

Master Hytale's ECS architecture for performant game mechanics.

## What is ECS?

ECS is an architectural pattern that separates:
- **Entity**: A unique identifier (just an ID)
- **Component**: Pure data (no logic)
- **System**: Pure logic (no data)

This enables:
- ✅ Better performance (cache-friendly)
- ✅ Easier composition (mix and match)
- ✅ Cleaner code (separation of concerns)

---

## Core Concepts

### Entity

An entity is **just an ID** - a number that groups components together.

```java
// Entity has no data or behavior itself
Entity player = world.createEntity();
Entity monster = world.createEntity();
```

### Component

Components are **data containers** - they describe what an entity "has".

```java
// Components are pure data
public record PositionComponent(float x, float y, float z) {}

public record HealthComponent(float current, float max) {}

public record VelocityComponent(float vx, float vy, float vz) {}

public record NameComponent(String name) {}
```

### System

Systems contain **logic** - they operate on entities with specific components.

```java
// Systems process entities with required components
public class MovementSystem implements System {
    @Override
    public void update(World world, float deltaTime) {
        // Query all entities with Position AND Velocity
        world.query(PositionComponent.class, VelocityComponent.class)
            .forEach((entity, pos, vel) -> {
                // Update position based on velocity
                entity.setComponent(new PositionComponent(
                    pos.x() + vel.vx() * deltaTime,
                    pos.y() + vel.vy() * deltaTime,
                    pos.z() + vel.vz() * deltaTime
                ));
            });
    }
}
```

---

## Composition Over Inheritance

### ❌ Traditional OOP (Inheritance)

```
       Entity
         │
    ┌────┴────┐
    │         │
 Character  Item
    │
┌───┴───┐
│       │
Player  NPC

Problem: What if NPC needs inventory like Player?
```

### ✅ ECS (Composition)

```
Player Entity:
  + PositionComponent
  + HealthComponent
  + InventoryComponent
  + PlayerControllerComponent

NPC Entity:
  + PositionComponent
  + HealthComponent
  + InventoryComponent  ← Easy to add!
  + AIControllerComponent

Item Entity:
  + PositionComponent
  + ItemDataComponent
```

---

## Working with Components

### Adding Components

```java
Entity player = world.createEntity();

player.addComponent(new PositionComponent(0, 64, 0));
player.addComponent(new HealthComponent(100, 100));
player.addComponent(new InventoryComponent());
```

### Getting Components

```java
// Get single component
var health = entity.getComponent(HealthComponent.class);
if (health != null) {
    float current = health.current();
}

// Check if has component
if (entity.hasComponent(FlyingComponent.class)) {
    // Handle flying entity
}

// Optional API
entity.getComponentOptional(HealthComponent.class)
    .ifPresent(h -> h.heal(10));
```

### Removing Components

```java
// Remove a component
entity.removeComponent(FlyingComponent.class);

// Entity becomes "different" without that component
// Systems that require FlyingComponent will skip it
```

---

## Entity Queries

Query entities based on their components:

```java
// All entities with Health
world.query(HealthComponent.class)
    .forEach((entity, health) -> {
        if (health.current() <= 0) {
            entity.destroy();
        }
    });

// All entities with Position AND Velocity AND NOT Flying
world.query()
    .with(PositionComponent.class)
    .with(VelocityComponent.class)
    .without(FlyingComponent.class)
    .forEach((entity, pos, vel) -> {
        // Apply gravity
    });
```

---

## Common Component Patterns

### Transform Components

```java
public record PositionComponent(float x, float y, float z) {}
public record RotationComponent(float pitch, float yaw, float roll) {}
public record ScaleComponent(float x, float y, float z) {}
```

### Gameplay Components

```java
public record HealthComponent(float current, float max) {
    public boolean isDead() { return current <= 0; }
}

public record DamageComponent(float amount, Entity source) {}

public record InventoryComponent(List<ItemStack> items) {}
```

### AI Components

```java
public record AITargetComponent(Entity target) {}
public record PatrolRouteComponent(List<Position> waypoints) {}
public record AggroRangeComponent(float range) {}
```

### Tags (Empty Components)

```java
// Tag components have no data
public record PlayerTag() {}
public record HostileTag() {}
public record InvulnerableTag() {}

// Use for filtering
world.query(PlayerTag.class, HealthComponent.class)
    .forEach((entity, _, health) -> {
        // Only players with health
    });
```

---

## System Design

### System Interface

```java
public interface System {
    void update(World world, float deltaTime);
    
    default int priority() { return 0; }  // Lower = runs first
}
```

### Example Systems

```java
public class GravitySystem implements System {
    @Override
    public void update(World world, float deltaTime) {
        world.query(VelocityComponent.class)
            .without(FlyingComponent.class)
            .forEach((entity, vel) -> {
                entity.setComponent(new VelocityComponent(
                    vel.vx(),
                    vel.vy() - 9.8f * deltaTime,  // Apply gravity
                    vel.vz()
                ));
            });
    }
    
    @Override
    public int priority() { return 10; }  // Run early
}

public class DamageSystem implements System {
    @Override
    public void update(World world, float deltaTime) {
        world.query(HealthComponent.class, DamageComponent.class)
            .forEach((entity, health, damage) -> {
                float newHealth = health.current() - damage.amount();
                entity.setComponent(new HealthComponent(newHealth, health.max()));
                entity.removeComponent(DamageComponent.class);
            });
    }
}
```

---

## Best Practices

### Do

| Practice | Why |
|----------|-----|
| Keep components small | Better cache usage |
| Use records for components | Immutable, simple |
| Prefer composition | Flexible, reusable |
| Use tag components | Clear intent |
| Query efficiently | Only needed components |

### Don't

| Anti-pattern | Why Bad |
|--------------|---------|
| Logic in components | Breaks ECS pattern |
| Giant components | Poor performance |
| Entity knowing systems | Tight coupling |
| Inheritance hierarchies | Defeats composition |

---

## Quick Reference

| Concept | What It Is |
|---------|------------|
| Entity | Just an ID |
| Component | Pure data |
| System | Pure logic |
| Query | Find entities by components |
| Tag | Empty component for filtering |

---

## Resources

- **Hytale API**: See `hytale-plugin-dev` skill
- **Java Features**: See `java-25-hytale` for records/patterns
