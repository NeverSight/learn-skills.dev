---
name: hz-unity-code-review
license: Apache-2.0
description: Reviews Unity code targeting Meta VR and Horizon OS for performance issues, rendering best practices, and common VR pitfalls. Use during code review or when diagnosing Meta VR performance problems in Unity projects.
allowed-tools: Bash(metavr:*), Bash(hzdb:*)
---

# Unity Code Review for Meta VR

## When to Use

Use this skill when reviewing Unity C# code or project settings that target Meta VR headsets. This includes:

- Reviewing scripts for VR performance issues
- Checking rendering pipeline configuration and settings
- Ensuring adherence to Meta VR-specific best practices
- Identifying common VR development pitfalls
- Validating input handling for controllers, hands, and eye tracking
- Auditing memory usage and GC allocation patterns

## Key Review Areas

### 1. Rendering Pipeline Configuration

Meta VR applications must use the Universal Render Pipeline (URP) with specific settings optimized for mobile VR. The Built-in Render Pipeline is not recommended for new Meta VR projects.

Critical settings to verify:

- **Single-pass multiview** must be enabled (Player Settings > XR Plug-in Management > Oculus > Stereo Rendering Mode)
- **Vulkan** should be the primary graphics API
- **Linear color space** is required for correct lighting
- **HDR** should be disabled in URP asset settings
- **Post-processing** should be minimal or disabled

### 2. Draw Call Budgets and Batching

Meta VR has draw call budgets that vary by workload complexity. Every draw call has CPU overhead that directly impacts frame timing.

| Metric | Quest 2 / Quest Pro | Quest 3 / Quest 3S | Meta VR Glasses |
|--------|---------------------|---------------------|-----------------|
| Draw calls (busy simulation) | 80-200 | 200-300 | 200-300 |
| Draw calls (medium simulation) | 200-300 | 400-600 | 400-600 |
| Draw calls (light simulation) | 400-600 | 700-1000 | 700-1000 |
| Triangles per frame | 750K-1M | 1M-2M | 1M-2M |
| SetPass calls | < 50 | < 80 | < 80 |

Enable and verify:
- Static batching for non-moving geometry
- GPU instancing for repeated objects
- SRP batcher for URP materials
- Dynamic batching for small meshes (< 300 vertices)

### 3. Shader Complexity

Mobile GPUs on Meta VR cannot handle desktop-class shaders. Review all materials for:

- Use of URP/Lit or URP/Simple Lit instead of Standard shader
- Custom shaders that minimize texture samples and ALU operations
- Avoidance of real-time shadows where possible (bake instead)
- No screen-space effects (SSAO, SSR, screen-space shadows)

### 4. Memory Management

GC allocations cause frame hitches and must be eliminated from hot paths.

```csharp
// BAD: Allocates every frame
void Update() {
    string label = "Score: " + score.ToString();
    var enemies = FindObjectsOfType<Enemy>();
    var filtered = enemies.Where(e => e.IsAlive).ToList();
}

// GOOD: Zero allocations in Update
private StringBuilder _sb = new StringBuilder(32);
private List<Enemy> _enemyCache = new List<Enemy>();
private Enemy[] _enemyArray;

void Start() {
    _enemyArray = FindObjectsOfType<Enemy>();
}

void Update() {
    _sb.Clear();
    _sb.Append("Score: ");
    _sb.Append(score);
}
```

### 5. Input Handling

Meta VR supports multiple input modalities. Code should handle:

- **Controllers**: Use Unity's Input System Package for new projects (recommended); `OVRInput` is maintained for legacy support
- **Hand tracking**: `OVRHand` and `OVRSkeleton` for hand pose data
- **Eye tracking**: `OVREyeGaze` (Quest Pro / Meta VR Glasses, requires permission)
- **Graceful switching** between controller and hand tracking modes

### 6. Physics Configuration

Physics simulation is expensive on mobile. Review for:

- Physics timestep set to match target frame rate (72/90/120 Hz)
- Simplified collision meshes (use primitives, not mesh colliders)
- Reduced solver iterations (4-6 is usually sufficient)
- Layer-based collision matrix to minimize pair checks
- Rigidbody sleep thresholds configured appropriately

### 7. Audio Setup

Audio is often overlooked but can impact performance:

- Compress audio clips (Vorbis for music, ADPCM for short SFX)
- Use streaming load type for clips longer than 1 second
- Limit simultaneous audio sources (target < 16)
- Spatialize audio using Meta's audio SDK for 3D positioning

## Quick Review Checklist

| Area | Target | Notes |
|------|--------|-------|
| Draw calls | 80-200 (busy) to 400-600 (light) | Use batching, instancing, atlasing |
| Triangles | 750K-1M/frame | Use LODs, occlusion culling |
| Texture resolution | Max 2K, 4K sparingly | ASTC compression required |
| Shader | URP mobile shaders | No Standard shader, no screen-space effects |
| Rendering mode | Single-pass multiview | Must be enabled in XR settings |
| FFR | Enabled (High or HighTop) | Fixed foveated rendering reduces edge fragment cost |
| MSAA | 4x quality / 2x perf | Free on tile-based GPU when configured correctly |
| Target frame rate | 72 Hz minimum | 90 Hz recommended, 120 Hz for smooth experiences |
| GC allocations | 0 B/frame in steady state | No allocations in Update/LateUpdate/FixedUpdate |
| Audio sources | < 16 simultaneous | Use pooling for audio sources |

## What to Look For in Code

### GC-Heavy Patterns

```csharp
// Flag these patterns in code review:
Camera.main                          // Calls FindWithTag internally
GameObject.Find("name")             // Linear search every call
GetComponent<T>() in Update         // Cache the result
new List<T>() in Update             // Allocates on heap
string + string in Update           // Creates new string objects
foreach on non-List collections     // Enumerator allocation
LINQ queries (.Where, .Select)      // Multiple allocations
Boxing (int -> object)              // Heap allocation
delegate/lambda in hot paths        // Closure allocation
```

### Update() Misuse

```csharp
// BAD: Empty Update still has overhead
void Update() { }

// BAD: Logic that doesn't need per-frame execution
void Update() {
    SavePlayerPrefs();  // Should be event-driven
}

// GOOD: Use events, coroutines, or InvokeRepeating for non-per-frame logic
void OnScoreChanged(int newScore) {
    UpdateScoreUI(newScore);
}
```

### Camera.main Anti-Pattern

```csharp
// BAD: Camera.main uses FindWithTag internally
void Update() {
    transform.LookAt(Camera.main.transform);
}

// GOOD: Cache the reference
private Transform _cameraTransform;

void Start() {
    _cameraTransform = Camera.main.transform;
}

void Update() {
    transform.LookAt(_cameraTransform);
}
```

### Find Calls in Hot Paths

```csharp
// BAD: Expensive search every frame
void Update() {
    var player = GameObject.FindWithTag("Player");
    var rb = player.GetComponent<Rigidbody>();
}

// GOOD: Cache in Awake/Start or use dependency injection
private Rigidbody _playerRb;

void Awake() {
    _playerRb = GameObject.FindWithTag("Player").GetComponent<Rigidbody>();
}
```

## Using metavr for Validation

You can use the `metavr` tool to validate builds and check device-side behavior. Invoke via `metavr <args>` (published as the npm package `metavr`; if `metavr` is not on PATH, run `npx -y metavr <args>`) — no install required.

```bash
# Check connected Meta VR device
metavr device list

# Install and run a build
metavr app install path/to/build.apk
metavr app launch com.company.app

# Check device logs for errors
metavr adb logcat --tag Unity

# Monitor GPU performance
metavr perf capture
```

Use device-side profiling to validate that code review findings translate to real performance improvements.

## Reference Documents

For detailed guidance on specific topics, see the following reference documents:

- [Performance Checklist](references/performance-checklist.md) — comprehensive performance targets and optimization strategies
- [Rendering Best Practices](references/rendering-best-practices.md) — Meta VR-specific rendering configuration and shader guidelines
- [Input Handling](references/input-handling.md) — controller, hand tracking, and eye tracking implementation
- [Common Pitfalls](references/common-pitfalls.md) — frequently encountered mistakes and their fixes
