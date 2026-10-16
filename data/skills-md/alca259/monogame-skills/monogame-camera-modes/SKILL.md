---
name: monogame-camera-modes
description: MonoGame 3D camera mode patterns — Fixed, Fixed Tracking, First Person, Third Person (with spring), Top-Down Fixed, and Top-Down Tracked. Use this skill whenever the user asks about camera modes, first person camera, third person camera, top-down camera, tracking camera, camera spring, follow camera, or how to implement a specific camera behaviour in a 3D game — even if they just say "I want the camera to follow the player" or "how do I make a first person / third person / top-down view".
---

# MonoGame 3D Camera Modes

This skill provides ready-to-use implementations for the six standard 3D camera modes. All modes share the same View/Projection setup — only `UpdateCameraView()` is called differently. For raw View/Projection matrix construction, see the `monogame-3d` skill.

## Shared Infrastructure

All modes use a single helper and a shared `View` field:

```csharp
// Fields shared by all modes:
private Matrix _view;
private Matrix _projection;
private Vector3 _currentCameraPos;

// Called at the end of every mode's update:
void UpdateCameraView(Vector3 position, Vector3 target)
{
    _currentCameraPos = position;
    _view = Matrix.CreateLookAt(position, target, Vector3.Up);
}
```

Set up `_projection` once in `LoadContent()`:
```csharp
_projection = Matrix.CreatePerspectiveFieldOfView(
    MathHelper.ToRadians(45f),
    GraphicsDevice.Viewport.AspectRatio,
    0.1f, 10000f);
```

Switch between modes in `Update()` via an enum dispatch — all drawing code uses the same `_view` and `_projection` regardless of mode.

## Mode 1 — Fixed Camera

Camera position and target are constant. Simplest possible mode.

```csharp
private Vector3 _fixedCameraPos = new Vector3(0f, 1550f, 5000f);

void UpdateFixedCamera()
{
    UpdateCameraView(_fixedCameraPos, Vector3.Zero);
}
```

Use when: cinematic sequences, fixed-angle puzzle games, menu scenes.

## Mode 2 — Fixed Tracking (Look-At)

Camera position is fixed; it rotates to always face the target:

```csharp
private Vector3 _trackingCameraPos = new Vector3(0f, 1550f, 5000f);

void UpdateTrackingCamera(Vector3 targetPosition)
{
    UpdateCameraView(_trackingCameraPos, targetPosition);
}
```

Use when: security-camera feel, fixed arena camera that keeps the player centred.

## Mode 3 — First Person

Camera is attached to the player's position and looks forward along the player's heading:

```csharp
// Offset from the player's origin to the camera eye point (model-local space):
private Vector3 _fpEyeOffset = new Vector3(0f, 50f, 500f);

void UpdateFirstPersonCamera(Vector3 playerPosition, float playerRotationY)
{
    Matrix rotationMatrix = Matrix.CreateRotationY(playerRotationY);

    // Transform eye offset by player's rotation, then place it in world space:
    Vector3 eyeWorld = Vector3.Transform(_fpEyeOffset, rotationMatrix) + playerPosition;

    // Look at the player's origin from the eye point:
    UpdateCameraView(eyeWorld, playerPosition);
}
```

Use when: FPS games, cockpit views, any camera that "is" the character.

**Tip:** Adjust `_fpEyeOffset.Z` (forward) and `.Y` (height) to match your model scale.

## Mode 4 — Third Person (with spring)

Camera follows behind and above the player. A spring-damper smooths the movement:

```csharp
// Camera offset behind/above the player (model-local space):
private Vector3 _tpOffset = new Vector3(0f, 1550f, 5000f);

// Spring physics state:
private Vector3 _cameraVelocity = Vector3.Zero;
private const float Stiffness = 1800f;
private const float Damping   = 600f;
private const float Mass      = 50f;

void UpdateThirdPersonCamera(Vector3 playerPosition, float playerRotationY, float elapsed)
{
    Matrix rotation = Matrix.CreateRotationY(playerRotationY);
    Vector3 desiredPos = Vector3.Transform(_tpOffset, rotation) + playerPosition;

    // Spring force: pulls camera toward desired position
    Vector3 stretch      = _currentCameraPos - desiredPos;
    Vector3 force        = -Stiffness * stretch - Damping * _cameraVelocity;
    Vector3 acceleration = force / Mass;

    _cameraVelocity     += acceleration * elapsed;
    _currentCameraPos   += _cameraVelocity * elapsed;

    UpdateCameraView(_currentCameraPos, playerPosition);
}
```

To disable the spring (instant follow), skip the physics and use `desiredPos` directly:
```csharp
_currentCameraPos = desiredPos;
UpdateCameraView(_currentCameraPos, playerPosition);
```

Use when: TPS games (Zelda-style, Souls-like), vehicle games. The spring makes sudden direction changes look natural.

**Tuning:**
- Increase `Stiffness` → snappier follow
- Increase `Damping` → less oscillation
- Increase `Mass` → heavier, slower response

## Mode 5 — Top-Down Fixed

Camera is directly above the world center, looking straight down:

```csharp
// Place far above world (adjust Y to taste)
private Vector3 _topDownPos = new Vector3(0f, 25000f, 1f);
// Note: Z must be non-zero to avoid gimbal lock with Vector3.Up as the up vector.

void UpdateTopDownFixedCamera()
{
    UpdateCameraView(_topDownPos, Vector3.Zero);
}
```

Use when: strategy games, overview maps, puzzle games. Switch to orthographic projection (`CreateOrthographic`) if you don't want perspective depth distortion.

## Mode 6 — Top-Down Tracked

Camera stays above and follows the player on the XZ plane:

```csharp
private Vector3 _topDownOffset = new Vector3(0f, 25000f, 1f);

void UpdateTopDownTrackedCamera(Vector3 playerPosition, float playerRotationY)
{
    Matrix rotation = Matrix.CreateRotationY(playerRotationY);
    Vector3 cameraPos = Vector3.Transform(_topDownOffset, rotation) + playerPosition;

    UpdateCameraView(cameraPos, playerPosition);
}
```

Use when: twin-stick shooters, top-down RPGs — keeps the player centred while the camera follows.

## Switching Between Modes

```csharp
public enum CameraMode
{
    Fixed, Tracking, FirstPerson, ThirdPerson, TopDownFixed, TopDownTracked
}

private CameraMode _cameraMode = CameraMode.Fixed;

// In Update:
switch (_cameraMode)
{
    case CameraMode.Fixed:
        UpdateFixedCamera();
        break;
    case CameraMode.Tracking:
        UpdateTrackingCamera(_modelPosition);
        break;
    case CameraMode.FirstPerson:
        UpdateFirstPersonCamera(_modelPosition, _modelRotation);
        break;
    case CameraMode.ThirdPerson:
        UpdateThirdPersonCamera(_modelPosition, _modelRotation, elapsed);
        break;
    case CameraMode.TopDownFixed:
        UpdateTopDownFixedCamera();
        break;
    case CameraMode.TopDownTracked:
        UpdateTopDownTrackedCamera(_modelPosition, _modelRotation);
        break;
}
```

## Rules

- Initialize `_currentCameraPos` to the starting camera position in `LoadContent()` — the spring modes need a valid initial value or they will snap on the first frame.
- Rebuild `_projection` when the viewport changes (window resize, fullscreen toggle).
- Top-down modes: avoid exactly `new Vector3(0, h, 0)` as camera position — the `Vector3.Up` used for the LookAt's up vector becomes undefined. Keep a small Z offset (e.g. `z = 1f`).
- All modes: `UpdateCameraView` must be called every frame, even for Fixed — it reads `_view` for rendering.

## Reference

For complete View/Projection construction, mouse picking, and fit-to-scene, see `references/camera-modes.md` and the `monogame-3d` skill.
