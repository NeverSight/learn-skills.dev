---
name: create-simulated-aeronautics-mod
description: Expertise in the Create Simulated Project — a NeoForge Minecraft mod suite adding physics-based contraptions including planes, airships, cars, and land vehicles built on the Create mod framework.
triggers:
  - add physics contraptions to my minecraft mod
  - create aeronautics neoforge mod
  - build a flying machine with create simulated
  - how to use create simulated project
  - physics based vehicles in minecraft java
  - assemble a plane or airship in create mod
  - create offroad land vehicle mod
  - propeller hot air balloon create aeronautics
---

# Create Simulated Project (Aeronautics)

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

## What Is This Project?

The Simulated Project is a suite of NeoForge Minecraft mods that extend the [Create](https://github.com/Creators-of-Create/Create) mod with real-time physics-based contraptions. It consists of three interconnected mods:

| Mod | Purpose |
|-----|---------|
| **Create Simulated** | Core assembly system, redstone components, physics interaction API |
| **Create Aeronautics** | Flying contraptions — propellers, hot air, levitation rocks |
| **Create Offroad** | Land vehicles — wheels, suspension, terrain traversal |

Physics simulation is powered by [Sable](https://github.com/ryanhcode/sable), a custom rigid-body physics engine built for Minecraft contraptions.

---

## Installation (Player/Server)

### Modrinth (Recommended)
1. Download from [modrinth.com/project/create-aeronautics](https://modrinth.com/modrinth/project/create-aeronautics)
2. Place the JAR(s) in your `mods/` folder alongside dependencies

### Required Dependencies
- **NeoForge** (matching the mod's target Minecraft version)
- **Create** mod (matching version)
- **Sable** physics library

### Recommended Launcher
Use [Modrinth App](https://modrinth.com/app) or [Prism Launcher](https://prismlauncher.org/) for dependency resolution.

---

## Developer Setup (Building from Source)

### Clone & Build
```bash
git clone https://github.com/Creators-of-Aeronautics/Simulated-Project.git
cd Simulated-Project
./gradlew build
```

### Run in Dev Environment
```bash
# Start a development client
./gradlew runClient

# Start a development server
./gradlew runServer

# Generate IDE run configurations (IntelliJ)
./gradlew genIntellijRuns
```

### Project Structure
```
Simulated-Project/
├── simulated/          # Core mod — assembly, physics API
├── aeronautics/        # Flying contraptions submod
├── offroad/            # Land vehicle submod
├── common/             # Shared utilities across submods
└── build.gradle        # Multi-project Gradle build
```

---

## Core Concepts

### 1. Simulated Contraptions
Unlike vanilla Create contraptions (which move block-by-block along tracks), Simulated contraptions are assembled into physics objects with:
- **Mass** derived from block composition
- **Moment of inertia** for rotation
- **Forces** applied by thrusters, propellers, wheels

### 2. Assembly
Players assemble a contraption using a designated assembly block (similar to Create's mechanical bearing). Once assembled, the structure becomes a rigid physics body managed by Sable.

### 3. Force Providers
Blocks that apply forces to assembled contraptions:
- `PropellerBlock` — directional thrust (Aeronautics)
- `HotAirBlock` — upward buoyancy (Aeronautics)
- `LevitationRockBlock` — magical lift (Aeronautics)
- `WheelBlock` — ground traction and propulsion (Offroad)

---

## Key API — Create Simulated Core

### Registering a Custom Force Provider

```java
import com.simulated.api.force.IForceProvider;
import com.simulated.api.contraption.SimulatedContraption;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;
import org.joml.Vector3f;

public class MyThrusterBlock extends Block implements IForceProvider {

    public MyThrusterBlock(Properties properties) {
        super(properties);
    }

    @Override
    public Vector3f getForce(SimulatedContraption contraption, BlockPos localPos, Level level) {
        // Return force vector in world space (Newtons equivalent)
        // Positive Y = upward lift, positive Z = forward thrust
        float thrustMagnitude = 500.0f;
        return new Vector3f(0, 0, thrustMagnitude);
    }

    @Override
    public Vector3f getTorque(SimulatedContraption contraption, BlockPos localPos, Level level) {
        // Torque applied around center of mass (optional)
        return new Vector3f(0, 0, 0);
    }
}
```

### Registering Your Block with NeoForge

```java
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.level.block.Block;
import net.neoforged.neoforge.registries.DeferredHolder;

public class MyModBlocks {

    public static final DeferredRegister<Block> BLOCKS =
        DeferredRegister.create(BuiltInRegistries.BLOCK, "mymod");

    public static final DeferredHolder<Block, MyThrusterBlock> MY_THRUSTER =
        BLOCKS.register("my_thruster", () -> new MyThrusterBlock(
            Block.Properties.of().strength(2.0f)
        ));

    public static void register(IEventBus eventBus) {
        BLOCKS.register(eventBus);
    }
}
```

### Accessing a SimulatedContraption at Runtime

```java
import com.simulated.api.contraption.SimulatedContraption;
import com.simulated.api.contraption.SimulatedContraptionHandler;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

public class ContraptionUtils {

    /**
     * Get the simulated contraption an entity is riding, if any.
     */
    public static SimulatedContraption getRiddenContraption(Entity entity) {
        return SimulatedContraptionHandler.getContraptionForEntity(entity);
    }

    /**
     * Apply an impulse to a contraption's physics body directly.
     */
    public static void applyImpulse(SimulatedContraption contraption, Vec3 impulse) {
        contraption.getPhysicsBody().applyImpulse(
            new org.joml.Vector3f(
                (float) impulse.x,
                (float) impulse.y,
                (float) impulse.z
            )
        );
    }
}
```

### Listening to Contraption Assembly Events

```java
import com.simulated.api.event.ContraptionAssembleEvent;
import com.simulated.api.event.ContraptionDisassembleEvent;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;

@EventBusSubscriber(modid = "mymod")
public class ContraptionEventHandler {

    @SubscribeEvent
    public static void onAssemble(ContraptionAssembleEvent event) {
        SimulatedContraption contraption = event.getContraption();
        // e.g., calculate custom mass modifier
        float customMass = contraption.getMass() * 0.8f;
        contraption.setMassOverride(customMass);

        System.out.println("Contraption assembled with " +
            contraption.getBlocks().size() + " blocks.");
    }

    @SubscribeEvent
    public static void onDisassemble(ContraptionDisassembleEvent event) {
        // Cleanup any custom data attached to this contraption
        MyContraptionData.remove(event.getContraption().getId());
    }
}
```

---

## Aeronautics — Flight Mechanics

### Propeller Configuration (In-Game)
Propellers are directional. Place them facing the direction you want thrust:
- **Facing down** → upward lift
- **Facing back** → forward thrust
- Speed (RPM) fed by Create's rotational network controls thrust magnitude

### Hot Air Balloon
1. Place **Balloon Canvas** blocks in a dome shape above a heat source
2. Connect a **Blaze Burner** below the opening
3. Assemble — the trapped hot air provides buoyancy proportional to enclosed volume

### Levitation Rock
- Rare ore providing passive vertical lift
- Useful for lighter-than-air vessels needing no fuel

### Flight Control Pattern
```java
// Example: Redstone-controlled pitch adjustment via a custom block entity
public class FlightControllerBlockEntity extends BlockEntity {

    public FlightControllerBlockEntity(BlockPos pos, BlockState state) {
        super(MyModBlockEntities.FLIGHT_CONTROLLER.get(), pos, state);
    }

    public void applyPitchInput(SimulatedContraption contraption, float pitchDelta) {
        // Torque around the X-axis to pitch the vehicle
        org.joml.Vector3f torque = new org.joml.Vector3f(pitchDelta * 100f, 0, 0);
        contraption.getPhysicsBody().applyTorqueImpulse(torque);
    }
}
```

---

## Offroad — Land Vehicles

### Wheel Setup
1. Place **Wheel blocks** at the four corners of your vehicle chassis
2. Each wheel needs rotational input from Create's shaft network
3. Assemble the contraption — wheels automatically detect ground contact

### Suspension
Wheels simulate suspension travel. Stiffer suspensions use more rigid Create structural blocks near the wheel mounts.

### Steering
Connect Create's **Rotation Speed Controller** to front wheels to implement steering differentials.

---

## Configuration

Config files generate in `config/` on first run:

```toml
# simulated-common.toml

[physics]
  # Physics simulation tick rate (ticks per second, default 20)
  simulationRate = 20
  # Maximum contraption block count before performance warnings
  maxContraptionSize = 2048
  # Enable contraption–contraption collision
  contraptionCollision = true

[aeronautics]
  # Propeller force multiplier
  propellerForceScale = 1.0
  # Hot air buoyancy multiplier
  hotAirBuoyancyScale = 1.0

[offroad]
  # Wheel traction coefficient
  wheelTraction = 0.85
  # Maximum vehicle speed (blocks/second)
  maxVehicleSpeed = 40.0
```

---

## Localization / Translations

The project uses [Crowdin](https://crowdin.com/project/create-aeronautics) for community translations.

### Adding a New Language
1. Join the Crowdin project
2. Translate strings in the web UI
3. Translations are automatically pulled into the repo

### Adding Keys Programmatically
```java
// In your lang JSON: src/main/resources/assets/mymod/lang/en_us.json
{
  "block.mymod.my_thruster": "Hyperdrive Thruster",
  "block.mymod.my_thruster.tooltip": "Applies directional thrust to assembled contraptions.",
  "mymod.contraption.overloaded": "Contraption mass exceeds safe limits!"
}
```

---

## Common Patterns

### Pattern 1: Fuel-Gated Thrust
```java
@Override
public Vector3f getForce(SimulatedContraption contraption, BlockPos localPos, Level level) {
    // Only provide thrust if a fuel item is present in an adjacent chest
    BlockEntity adjacent = level.getBlockEntity(localPos.above());
    if (adjacent instanceof net.minecraft.world.level.block.entity.ChestBlockEntity chest) {
        boolean hasFuel = !chest.isEmpty(); // simplified check
        if (hasFuel) {
            return new Vector3f(0, 0, 800.0f);
        }
    }
    return new Vector3f(0, 0, 0);
}
```

### Pattern 2: Speed-Based Thrust Scaling
```java
@Override
public Vector3f getForce(SimulatedContraption contraption, BlockPos localPos, Level level) {
    // Scale thrust with Create rotational speed at this block's position
    float rpm = contraption.getRotationalSpeedAt(localPos);
    float thrust = rpm * 2.5f; // tune this constant for your use case
    return new Vector3f(0, 0, Math.min(thrust, 2000.0f)); // cap at max
}
```

### Pattern 3: Custom Physics Data per Contraption
```java
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public class MyContraptionData {
    private static final Map<UUID, Float> fuelLevels = new HashMap<>();

    public static float getFuel(UUID contraptionId) {
        return fuelLevels.getOrDefault(contraptionId, 100.0f);
    }

    public static void consumeFuel(UUID contraptionId, float amount) {
        float current = getFuel(contraptionId);
        fuelLevels.put(contraptionId, Math.max(0, current - amount));
    }

    public static void remove(UUID contraptionId) {
        fuelLevels.remove(contraptionId);
    }
}
```

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Contraption won't assemble | Missing dependency mod (Create, Sable) | Verify all deps in `mods/` |
| Vehicle sinks through floor | Wheel blocks not receiving rotation | Check shaft connections |
| Extreme jitter / vibration | Too many conflicting force providers | Balance thrust/lift forces; reduce `propellerForceScale` in config |
| Crash on assembly | Block count exceeds `maxContraptionSize` | Increase limit in config or reduce vehicle size |
| Translations not showing | Wrong lang file path | Ensure `assets/<modid>/lang/en_us.json` path is correct |
| Physics desync on multiplayer | High server TPS drop | Lower `simulationRate` or reduce contraption count |
| `ClassNotFoundException` on IForceProvider | API jar not in classpath | Add `simulated-api` to `build.gradle` dependencies |

### Dependency Setup in `build.gradle`
```groovy
dependencies {
    // NeoForge
    implementation "net.neoforged:neoforge:${neoforge_version}"

    // Create mod (via cursemaven or modrinth maven)
    implementation fg.deobf("com.simibubi.create:create-${minecraft_version}:${create_version}:slim") {
        transitive = false
    }

    // Create Simulated API (once published to maven)
    implementation "com.aeronautics:simulated-api:${simulated_version}"
}
```

---

## Community & Support

- **Discord**: [discord.gg/createaeronautics](https://discord.gg/createaeronautics)
- **Issue Tracker**: [GitHub Issues](https://github.com/Creators-of-Aeronautics/Simulated-Project/issues) (233 open)
- **Modrinth**: [modrinth.com/project/create-aeronautics](https://modrinth.com/project/create-aeronautics)
- **Crowdin Translations**: [crowdin.com/project/create-aeronautics](https://crowdin.com/project/create-aeronautics)
