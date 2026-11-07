---
name: minecraft-testing
description: "Write automated tests for Minecraft mods and plugins for 1.21.x. Covers NeoForge GameTests (@GameTest annotation, GameTestHelper assertions, test structure placement), Fabric game tests (fabric-gametest-api-v1), unit testing non-Minecraft logic with JUnit 5, MockBukkit for Paper/Bukkit plugin testing (mock server, mock player, event dispatching, inventory checking), integration testing with a test server via Gradle, and GitHub Actions CI workflows that run GameTests headlessly. Includes patterns for mocking registries, testing event handlers, testing commands, and test-driven development for Minecraft projects. Use when the user asks about testing Minecraft mods or plugins, writing GameTests, setting up MockBukkit, or configuring CI for Minecraft projects."
---

# Minecraft Testing Skill

## Testing Strategies Overview

| Approach | Best For | Requires Game? |
|----------|---------|----------------|
| **JUnit 5** (pure unit tests) | Logic, data structures, NBT serialization | No |
| **MockBukkit** | Bukkit/Paper plugin events, commands, inventory | No (mocked server) |
| **NeoForge GameTests** | In-game block/entity/world interaction | Yes (test environment) |
| **Fabric GameTests** | In-game block/entity/world interaction | Yes (test environment) |
| **Integration server** | Full plugin/mod lifecycle | Yes (dedicated test server) |

### Routing Boundaries
- `Use when`: the task is designing or implementing automated tests (unit, mock, gametest, CI test jobs) for Minecraft projects.
- `Do not use when`: the task is implementing gameplay features rather than testing them (`minecraft-modding`, `minecraft-plugin-dev`, `minecraft-datapack`).
- `Do not use when`: the task is release automation or publishing pipelines (`minecraft-ci-release`).
- `Do not use when`: the task is a bot playthrough of a live dev server rather than code-level tests (`minecraft-bot-qa`).

## Bundled References And Helpers

- Layout guide: `references/test-layouts.md`
- Fixture/layout validator: `./scripts/validate-test-layout.sh --root <project>`

Use the validator before copying a test layout into a real project. It checks for
the common breakpoints that show up in 1.21.x plugin/mod test repos: missing
`useJUnitPlatform()`, MockBukkit tests without the dependency, and GameTests with
no committed structure fixtures.

---

## Unit Testing (JUnit 5 — No Minecraft)

### `build.gradle.kts` additions
```kotlin
dependencies {
    testImplementation("org.junit.jupiter:junit-jupiter:5.11.0")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

tasks.test {
    useJUnitPlatform()
    testLogging {
        events("passed", "skipped", "failed")
    }
}
```

### Example pure unit test
```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class CooldownManagerTest {

    @Test
    void playerOnCooldown_returnsFalse_afterExpiry() {
        var manager = new CooldownManager(500L); // 500ms cooldown
        manager.startCooldown("steve");
        assertTrue(manager.isOnCooldown("steve"));
        // fast-forward time by sleeping or injecting a Clock
        assertFalse(manager.isOnCooldown("notExisting"));
    }

    @Test
    void cooldown_throwsIllegalArgument_onNegativeDuration() {
        assertThrows(IllegalArgumentException.class,
            () -> new CooldownManager(-1L));
    }
}
```

---

## MockBukkit (Paper/Bukkit Plugin Tests)

### `build.gradle.kts`
```kotlin
repositories {
    maven("https://repo.papermc.io/repository/maven-public/")
    maven("https://repo.mockbukkit.org/artifactory/mockbukkit/")
}

dependencies {
    compileOnly("io.papermc.paper:paper-api:26.2.build.+")
    testImplementation("org.junit.jupiter:junit-jupiter:5.11.0")
    testImplementation("com.github.seeseemelk:MockBukkit-v1.21:3.127.0")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

tasks.test {
    useJUnitPlatform()
}
```

### Setup / teardown pattern
```java
import be.seeseemelk.mockbukkit.MockBukkit;
import be.seeseemelk.mockbukkit.ServerMock;
import be.seeseemelk.mockbukkit.entity.PlayerMock;
import org.junit.jupiter.api.*;

class MyPluginTest {

    private static ServerMock server;
    private static MyPlugin plugin;

    @BeforeAll
    static void setUp() {
        // Start mock Bukkit server and load your plugin
        server = MockBukkit.mock();
        plugin = MockBukkit.load(MyPlugin.class);
    }

    @AfterAll
    static void tearDown() {
        MockBukkit.unmock();
    }
}
```

### Testing events
```java
@Test
void playerJoin_getsWelcomeMessage() {
    PlayerMock player = server.addPlayer("Steve");
    player.simulateJoin(); // fires PlayerJoinEvent

    // Assert the player received the expected message component
    player.assertSaid("Welcome, Steve!");
    // Or for Adventure components:
    assertTrue(player.nextMessage().contains("Welcome"));
}

@Test
void onBlockBreak_cancelledForNonOp() {
    PlayerMock player = server.addPlayer();
    player.setOp(false);

    Block block = player.getWorld().getBlockAt(0, 64, 0);
    block.setType(Material.STONE);
    BlockBreakEvent event = new BlockBreakEvent(block, player);
    server.getPluginManager().callEvent(event);

    assertTrue(event.isCancelled(), "Non-op should not be able to break blocks");
}
```

### Testing commands
```java
@Test
void mypluginInfo_returnsVersion() {
    PlayerMock player = server.addPlayer("Admin");
    player.setOp(true);

    boolean result = server.dispatchCommand(player, "myplugin info");

    assertTrue(result);
    player.assertSaid("Version: " + plugin.getDescription().getVersion());
}

@Test
void mypluginReload_requiresOp() {
    PlayerMock player = server.addPlayer("NonOp");
    player.setOp(false);

    server.dispatchCommand(player, "myplugin reload");

    player.assertSaid("No permission.");
}
```

### Testing inventory / items
```java
@Test
void giveKitCommand_givesPlayerItems() {
    PlayerMock player = server.addPlayer();
    
    server.dispatchCommand(player, "kit starter");
    
    // Check inventory
    assertTrue(player.getInventory().contains(Material.STONE_SWORD));
    assertTrue(player.getInventory().contains(Material.BREAD, 16));
}
```

### Testing scheduler tasks
```java
@Test
void repeatingTask_firesAfterDelay() {
    PlayerMock player = server.addPlayer();
    
    // Execute 40 ticks worth of scheduled tasks
    server.getScheduler().performTicks(40L);
    
    // Assert expected side effect happened
    assertEquals(2, plugin.getTaskCount());
}
```

### Testing Folia-safe scheduler abstractions

MockBukkit does not emulate Folia's region-threaded runtime. The safe pattern is to
wrap scheduling behind your own interface and unit test the abstraction boundary.

```java
interface SchedulerFacade {
    void runPlayerTask(Player player, Runnable task);
    void runAsync(Runnable task);
}

@Test
void playerTask_delegatesThroughFacade() {
    List<String> calls = new ArrayList<>();
    SchedulerFacade facade = new SchedulerFacade() {
        @Override
        public void runPlayerTask(Player player, Runnable task) {
            calls.add("player");
            task.run();
        }

        @Override
        public void runAsync(Runnable task) {
            calls.add("async");
            task.run();
        }
    };

    facade.runPlayerTask(server.addPlayer(), () -> calls.add("ran"));
    assertEquals(List.of("player", "ran"), calls);
}
```

### Testing PDC
```java
@Test
void pdcKillCount_incrementsOnKill() {
    PlayerMock player = server.addPlayer();
    NamespacedKey key = new NamespacedKey(plugin, "kills");
    
    // Simulate kill event
    EntityDeathEvent deathEvent = new EntityDeathEvent(
        server.addMockEntity(EntityType.ZOMBIE), new ArrayList<>(), 0
    );
    deathEvent.getEntity().setKiller(player);
    server.getPluginManager().callEvent(deathEvent);
    
    int kills = player.getPersistentDataContainer()
        .getOrDefault(key, PersistentDataType.INTEGER, 0);
    assertEquals(1, kills);
}
```

### Testing item or chunk PDC writes
```java
@Test
void itemPdc_roundTripsCustomId() {
    NamespacedKey key = new NamespacedKey(plugin, "custom_id");
    ItemStack item = new ItemStack(Material.STICK);

    item.editMeta(meta -> meta.getPersistentDataContainer().set(
        key, PersistentDataType.STRING, "wand"
    ));

    String value = item.getItemMeta().getPersistentDataContainer()
        .get(key, PersistentDataType.STRING);
    assertEquals("wand", value);
}
```

---

## NeoForge GameTests

GameTests run inside a Minecraft world. They place a **structure** (the test environment),
then run assertions using `GameTestHelper`.

### Registration
```java
// In your mod main class:
@Mod(MyMod.MOD_ID)
public class MyMod {
    public MyMod(IEventBus modEventBus) {
        modEventBus.register(MyGameTests.class);
    }
}
```

### Test class
```java
import net.minecraft.gametest.framework.*;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

@GameTestHolder(MyMod.MOD_ID)                // registers test namespace
@PrefixGameTestTemplate(false)               // don't prefix template names
public class MyGameTests {

    // Default template: 3x3x3 air structure called "mymod:empty"
    @GameTest(template = "mymod:empty")
    public static void testBlockInteraction(GameTestHelper helper) {
        // Place a block
        helper.setBlock(1, 1, 1, net.minecraft.world.level.block.Blocks.FURNACE);
        
        // Run after 1 tick
        helper.runAfterDelay(1, () -> {
            // Assert block state
            helper.assertBlock(new net.minecraft.core.BlockPos(1, 1, 1),
                b -> b.is(net.minecraft.world.level.block.Blocks.FURNACE),
                "Expected furnace");
            
            helper.succeed();
        });
    }

    @GameTest(template = "mymod:empty", timeoutTicks = 200)
    public static void testEntitySpawn(GameTestHelper helper) {
        // Spawn entity
        var entity = helper.spawnWithNoFreeWill(
            net.minecraft.world.entity.EntityType.ZOMBIE, new net.minecraft.core.BlockPos(2, 2, 2)
        );
        
        helper.runAfterDelay(5, () -> {
            helper.assertEntityPresent(
                net.minecraft.world.entity.EntityType.ZOMBIE,
                new net.minecraft.core.BlockPos(2, 2, 2), 1.0
            );
            helper.succeed();
        });
    }
}
```

### Structure templates (`.nbt` files)
Place empty structure files at:  
`src/main/resources/data/mymod/structures/empty.nbt`

Generate them in-game using `/test create mymod:empty 3 3 3` (NeoForge test command).
Commit the `.nbt` files to version control.

### GameTest setup checklist

1. Verify `.nbt` structure files exist at `src/main/resources/data/<modid>/structures/`
2. Run `./gradlew runGameTestServer` — if tests fail with "Missing template", the `.nbt` file path or name is wrong
3. Check Gradle output for `PASSED`/`FAILED` per test
4. If a test times out, increase `timeoutTicks` in the `@GameTest` annotation or add intermediate assertions with `runAfterDelay`

### Running GameTests
```bash
./gradlew runGameTestServer

# In-game (dev environment):
# /test runall
# /test run mymod:test_block_interaction
```

---

## Fabric GameTests

```java
import net.fabricmc.fabric.api.gametest.v1.FabricGameTest;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.level.block.Blocks;

public class MyFabricGameTests implements FabricGameTest {

    @GameTest(template = EMPTY_STRUCTURE)
    public void testCustomBlock(GameTestHelper helper) {
        helper.setBlock(1, 1, 1, Blocks.GOLD_BLOCK.defaultBlockState());
        
        helper.runAfterDelay(2, () -> {
            helper.assertBlock(
                new BlockPos(1, 1, 1),
                b -> b.is(Blocks.GOLD_BLOCK),
                "Gold block should be placed"
            );
            helper.succeed();
        });
    }
}
```

### Register in `fabric.mod.json`
```json
{
  "entrypoints": {
    "fabric-gametest": [
      "com.example.mymod.fabric.MyFabricGameTests"
    ]
  }
}
```

---

## `GameTestHelper` Assertions Reference

```java
// Block assertions
helper.assertBlock(pos, predicate, "message");
helper.assertBlockState(pos, state -> state.is(Blocks.STONE), "Expected stone");
helper.assertBlockPresent(Blocks.GOLD_BLOCK, pos);
helper.assertBlockNotPresent(Blocks.TNT, pos);

// Entity assertions
helper.assertEntityPresent(EntityType.ZOMBIE, pos, radius);
helper.assertEntityNotPresent(EntityType.ZOMBIE);
helper.assertEntityCount(EntityType.ZOMBIE, expectedCount);
helper.assertEntityProperty(entity, entity -> entity.getHealth() > 0, "alive");

// Item assertions
helper.assertContainerContains(pos, Items.DIAMOND);
helper.assertContainerEmpty(pos);

// Control flow
helper.succeed();        // mark test as passed — REQUIRED at end
helper.fail("reason");   // mark test as failed
helper.runAfterDelay(ticks, runnable); // schedule assertion
helper.onEachTick(runnable);          // run every tick (use with care)
helper.succeedWhen(() -> { /* assertions */ }); // poll until assertions pass or timeout
helper.succeedOnTickWhen(tick, () -> { /* assertions */ });
```

---

## CI: Running Tests in GitHub Actions

Split CI into fast unit/mock coverage and slower runtime-facing jobs. MockBukkit is great
for command/event logic, but it does not prove Folia thread safety or real server bootstrap.

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
    unit-tests:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4
            - { uses: actions/setup-java@v4, with: { java-version: '21', distribution: 'temurin' } }
            - uses: gradle/actions/setup-gradle@v3
            - { name: Run unit tests, run: ./gradlew test }

    game-tests:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4
            - { uses: actions/setup-java@v4, with: { java-version: '21', distribution: 'temurin' } }
            - uses: gradle/actions/setup-gradle@v3
            - { name: Run GameTests (headless), run: ./gradlew runGameTestServer, env: { CI: true } }

    layout-checks:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4
            - { name: Validate test layout, run: ./scripts/validate-test-layout.sh --root . }
```

---

## References

- MockBukkit GitHub: https://github.com/MockBukkit/MockBukkit
- MockBukkit docs: https://mockbukkit.readthedocs.io/
- NeoForge GameTest docs: https://docs.neoforged.net/docs/misc/gametest/
- Fabric GameTest API: https://wiki.fabricmc.net/tutorial:gametests
- JUnit 5 user guide: https://junit.org/junit5/docs/current/user-guide/
