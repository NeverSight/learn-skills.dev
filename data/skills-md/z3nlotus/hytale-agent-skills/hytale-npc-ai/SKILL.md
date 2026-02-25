---
name: hytale-npc-ai
description: Creating NPCs with AI behavior in Hytale. Covers NPC types, behavior trees, dialogue systems, state machines, pathfinding, and combat AI. Use when creating villagers, merchants, enemies, or any interactive characters.
---

# Hytale NPC & AI

Create intelligent NPCs and AI-driven characters for Hytale.

## NPC Types

| Type | Behavior | Examples |
|------|----------|----------|
| **Passive** | Wanders, flees from danger | Villagers, animals |
| **Neutral** | Ignores unless provoked | Guards, merchants |
| **Hostile** | Actively attacks players | Monsters, enemies |
| **Companion** | Follows and assists player | Pets, allies |

---

## Basic NPC Structure

### NPC Components (ECS Pattern)

```java
// An NPC is an entity with these components
Entity npc = world.createEntity();

npc.addComponent(new PositionComponent(x, y, z));
npc.addComponent(new HealthComponent(100, 100));
npc.addComponent(new NPCTypeComponent(NPCType.VILLAGER));
npc.addComponent(new AIControllerComponent());
npc.addComponent(new InventoryComponent());
npc.addComponent(new DialogueComponent("villager_greeting"));
```

---

## Behavior Trees

Hytale uses **behavior trees** for AI decision making:

```
                    [Selector]
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   [Is Danger?]    [Has Task?]     [Wander]
        │               │
        ▼               ▼
    [Flee]          [Do Task]
```

### Node Types

| Node | Behavior |
|------|----------|
| **Selector** | Try children until one succeeds |
| **Sequence** | Run all children in order |
| **Condition** | Check if something is true |
| **Action** | Do something |

### Example: Villager AI

```java
BehaviorTree villagerAI = BehaviorTree.builder()
    .selector()
        .sequence()  // Danger response
            .condition(this::isInDanger)
            .action(this::fleeFromDanger)
        .end()
        .sequence()  // Work during day
            .condition(this::isDaytime)
            .condition(this::hasWorkstation)
            .action(this::goToWorkstation)
            .action(this::doWork)
        .end()
        .sequence()  // Sleep at night
            .condition(this::isNighttime)
            .action(this::goToBed)
            .action(this::sleep)
        .end()
        .action(this::wanderRandomly)  // Default
    .end()
    .build();
```

---

## State Machine Pattern

Alternative to behavior trees for simpler AI:

```java
public enum NPCState {
    IDLE,
    WALKING,
    WORKING,
    FLEEING,
    SLEEPING,
    TALKING
}

public class VillagerAI {
    private NPCState currentState = NPCState.IDLE;
    
    public void update(Entity npc, float deltaTime) {
        switch (currentState) {
            case IDLE -> handleIdle(npc);
            case WALKING -> handleWalking(npc);
            case WORKING -> handleWorking(npc);
            case FLEEING -> handleFleeing(npc);
            // ...
        }
    }
    
    private void handleIdle(Entity npc) {
        if (isInDanger(npc)) {
            currentState = NPCState.FLEEING;
        } else if (shouldWork()) {
            currentState = NPCState.WALKING;
            setDestination(getWorkstation());
        }
    }
}
```

---

## Dialogue System

### Dialogue Structure

```json
{
  "dialogueId": "villager_greeting",
  "entries": [
    {
      "text": "server.dialogue.villager.hello",
      "responses": [
        {
          "text": "server.dialogue.player.trade",
          "action": "open_trade",
          "next": null
        },
        {
          "text": "server.dialogue.player.quest",
          "action": null,
          "next": "villager_quest_info"
        },
        {
          "text": "server.dialogue.player.goodbye",
          "action": "close",
          "next": null
        }
      ]
    }
  ]
}
```

### Triggering Dialogue

```java
registerEventListener(PlayerInteractEvent.class, event -> {
    Entity target = event.getTarget();
    
    if (target.hasComponent(DialogueComponent.class)) {
        var dialogue = target.getComponent(DialogueComponent.class);
        event.getPlayer().openDialogue(dialogue.getDialogueId());
    }
});
```

---

## Combat AI

### Aggro System

```java
public class AggroComponent {
    private Map<Entity, Float> threatTable = new HashMap<>();
    private float aggroRange = 10.0f;
    
    public void addThreat(Entity source, float amount) {
        threatTable.merge(source, amount, Float::sum);
    }
    
    public Entity getTopThreat() {
        return threatTable.entrySet().stream()
            .max(Map.Entry.comparingByValue())
            .map(Map.Entry::getKey)
            .orElse(null);
    }
}
```

### Attack Patterns

```java
public class CombatAI {
    private float attackCooldown = 0;
    private float attackRange = 2.0f;
    
    public void update(Entity npc, Entity target, float deltaTime) {
        attackCooldown -= deltaTime;
        
        float distance = npc.distanceTo(target);
        
        if (distance > attackRange) {
            // Move toward target
            moveToward(npc, target);
        } else if (attackCooldown <= 0) {
            // Attack!
            attack(npc, target);
            attackCooldown = 1.5f;  // Reset cooldown
        }
    }
}
```

---

## Pathfinding

### Basic Pathfinding

```java
// Request path from current position to target
Path path = pathfinder.findPath(
    npc.getPosition(),
    targetPosition
);

// Follow the path
if (path != null && !path.isEmpty()) {
    Position nextWaypoint = path.getNextWaypoint();
    moveToward(npc, nextWaypoint);
    
    if (npc.distanceTo(nextWaypoint) < 0.5f) {
        path.advanceWaypoint();
    }
}
```

### Pathfinding Options

| Option | Description |
|--------|-------------|
| `avoidWater` | Don't path through water |
| `avoidDanger` | Avoid hostile areas |
| `maxDistance` | Limit path length |
| `canOpenDoors` | Allow door navigation |

---

## Spawning NPCs

### Via Plugin

```java
public void spawnVillager(World world, Position pos) {
    Entity villager = world.spawnEntity("hytale:villager", pos);
    
    // Customize
    villager.getComponent(NameComponent.class)
        .setName("Bob the Builder");
    
    villager.addComponent(new ProfessionComponent("builder"));
}
```

### Via Pack (JSON)

```json
{
  "type": "npc_spawner",
  "entityType": "hytale:villager",
  "spawnCount": { "min": 2, "max": 5 },
  "spawnArea": { "radius": 10 },
  "conditions": {
    "biome": "village",
    "minLightLevel": 8
  }
}
```

---

## Common AI Patterns

### Patrol Route

```java
public class PatrolAI {
    private List<Position> waypoints;
    private int currentWaypoint = 0;
    
    public void update(Entity npc) {
        Position target = waypoints.get(currentWaypoint);
        
        if (npc.distanceTo(target) < 1.0f) {
            currentWaypoint = (currentWaypoint + 1) % waypoints.size();
        } else {
            moveToward(npc, target);
        }
    }
}
```

### Follow Player

```java
public class FollowAI {
    private Entity owner;
    private float followDistance = 3.0f;
    private float maxDistance = 20.0f;
    
    public void update(Entity pet) {
        float distance = pet.distanceTo(owner);
        
        if (distance > maxDistance) {
            teleportTo(pet, owner.getPosition());
        } else if (distance > followDistance) {
            moveToward(pet, owner);
        }
    }
}
```

---

## Quick Reference

| AI Type | Best Pattern | Use Case |
|---------|--------------|----------|
| Simple NPC | State Machine | Basic villagers |
| Complex NPC | Behavior Tree | Quest givers, bosses |
| Combat | Aggro + State | Enemies |
| Companions | Follow + Commands | Pets |

---

## Resources

- **ECS Architecture**: See `hytale-ecs` skill
- **Plugin Development**: See `hytale-plugin-dev` skill
- **Animation**: See `hytale-animation` skill
