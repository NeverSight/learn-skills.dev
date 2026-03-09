---
name: webxr-dev
description: WebXR/VR development guide for Three.js on Meta Quest — camera rig, controllers, teleport, postprocessing limitations, and hard-won pitfalls from shipping VR
---

# WebXR Development Guide

A practical guide for building WebXR (VR/AR) experiences with Three.js, based on hard-won lessons from shipping VR on Meta Quest headsets.

## When to Use This Skill

Invoke with `/webxr-dev` when:
- Adding VR/AR support to a Three.js application
- Debugging WebXR rendering issues
- Implementing VR interaction systems (panels, teleport, controllers, hands)
- Adding passthrough/AR to an existing VR application

---

## Critical Rule: immersive-vr vs immersive-ar

**This is the single most important decision in your WebXR app.**

### immersive-vr (Default — Use This)
- Framebuffer is **opaque**. The compositor displays your render as-is.
- `scene.background`, `setClearColor()` work normally.
- Three.js renders backgrounds, fog, skyboxes correctly.
- Standard VR behavior — everything just works.

### immersive-ar (Passthrough — Dragons Here)
- Framebuffer **alpha controls camera blending**: alpha=0 → full passthrough, alpha=1 → full render.
- Three.js **skips `scene.background` rendering** in AR sessions intentionally.
- `setClearColor(color, 1)` may be overridden by Three.js XR path.
- Every pixel in every scene must explicitly output alpha=1.0 to block the camera feed.
- Shaders with `gl_FragColor = vec4(color, 1.0)` are fine, but MeshBasicMaterial/MeshStandard may not be.
- **You cannot toggle between VR and AR mid-session** — the session mode is fixed at request time.

### The Rule
```
Start with immersive-vr. Only switch to immersive-ar when you have:
1. A specific passthrough use case
2. The ability to test on-device
3. A plan for managing alpha in every material and shader
```

**Never** default to `immersive-ar` just because the device supports it. A Quest 3 supports both — always prefer `immersive-vr` unless passthrough is the primary experience.

---

## Session Setup

### Minimal Working Setup
```typescript
const xr = navigator.xr;
const supported = await xr.isSessionSupported("immersive-vr");
if (!supported) return;

const sessionInit: XRSessionInit = {
  optionalFeatures: [
    'local-floor',      // Floor-level reference space
    'bounded-floor',    // Room-scale boundary
    'hand-tracking',    // Quest hand tracking
    'layers',           // XRProjectionLayer + composition layers
    'hit-test',         // Ray-vs-real-world hit testing (AR)
  ],
};

const session = await xr.requestSession("immersive-vr", sessionInit);
renderer.xr.setReferenceSpaceType("local-floor");
renderer.xr.setSession(session);
```

### Valid Feature Descriptors
Only these strings are recognized in `optionalFeatures` / `requiredFeatures`:
`anchors`, `bounded-floor`, `depth-sensing`, `dom-overlay`, `hand-tracking`, `hit-test`, `layers`, `light-estimation`, `local`, `local-floor`, `secondary-views`, `unbounded`, `viewer`.

Unrecognized strings are silently ignored — they won't cause an error but they won't do anything either.

### Native Framebuffer Resolution (Anti-Pixelation)
**Critical:** The default WebXR framebuffer is low-resolution. You MUST create an `XRWebGLLayer` with native scale factor to avoid pixelated rendering:
```typescript
const onSessionStarted = (session: XRSession) => {
  session.addEventListener("end", onSessionEnded);
  renderer.xr.setReferenceSpaceType("local-floor");

  // Set high-res framebuffer — without this, everything looks pixelated
  const gl = renderer.getContext();
  const glLayer = new XRWebGLLayer(session, gl, {
    framebufferScaleFactor: XRWebGLLayer.getNativeFramebufferScaleFactor(session),
    antialias: true,
  });
  session.updateRenderState({ baseLayer: glLayer });

  renderer.xr.setSession(session);
};
```
Without this, Quest renders at a fraction of native resolution. This single change eliminates most "it looks blurry/pixelated" complaints.

### Adding Passthrough Later (If Needed)
Passthrough requires `immersive-ar`, not `immersive-vr`. There is no `'passthrough'` optional feature — that string is not part of the WebXR spec.

To enable passthrough:
```typescript
// Request an AR session — the device composites your render over the camera feed
const session = await xr.requestSession("immersive-ar", {
  optionalFeatures: ['local-floor', 'hand-tracking'],
});
// session.environmentBlendMode will be "alpha-blend" on Quest
```

In `immersive-ar`, framebuffer alpha controls camera blending: alpha=0 shows full passthrough, alpha=1 shows your render. You cannot switch between VR and AR mid-session — the mode is fixed at request time.

---

## Shader Considerations for VR

### Inverted Sphere Skybox Pattern
For custom shader skyboxes (ray marching, procedural stars, etc.), use a standard sphere with `DoubleSide`:
```typescript
const sphereGeo = new THREE.IcosahedronGeometry(50, 5);
// Do NOT call sphereGeo.scale(-1, 1, 1) — see "Geometry Inversion Trap" below
const material = new THREE.ShaderMaterial({
  vertexShader, fragmentShader,
  side: THREE.DoubleSide,  // Guarantees visibility from inside — no culling surprises
  depthWrite: false,
});
const vrSphere = new THREE.Mesh(sphereGeo, material);
vrSphere.frustumCulled = false;
```

#### Geometry Inversion Trap
**Never combine `sphereGeo.scale(-1, 1, 1)` with `side: THREE.BackSide`.**

- `scale(-1,1,1)` flips the winding order AND normals (normals now point inward)
- `BackSide` renders the face **opposite** to the normal direction
- With inward normals, `BackSide` renders the **outside** — camera inside sees nothing
- This is a double-negation that makes the sphere invisible

**Safe options for camera-inside-sphere rendering:**
1. **`DoubleSide` (recommended):** Renders both faces, eliminates all culling ambiguity. The shader determines what to draw via ray direction — double-rendering has zero visual cost.
2. **Standard geometry + `BackSide`:** Works in theory (outward normals, BackSide renders inner faces) but winding order can be ambiguous across geometry types.
3. **Inverted geometry + `FrontSide`:** Also works but equally fragile.

Use `DoubleSide` and stop worrying about it.

### VR Camera Position
In VR, the camera is at the user's physical head position (~1.6m above floor). This affects:
- **Ray marching shaders**: If the BH/object is at origin, camera may be inside or too close to it.
- **Fix**: Position objects relative to where the user will be looking (eye level, a few meters ahead).
- **Example**: For a black hole with rs=0.2, position at (0, 1.6, -5) — eye level, 5m ahead. At 25x the Schwarzschild radius, lensing is clearly visible without overwhelming the view.

#### Object Scale in VR
Objects that look fine on desktop often feel enormous in VR because you have real spatial perception. **Always reduce the effective size of objects for VR.** Example: a black hole with mass=1.5 (rs=1.5m) works on desktop but in VR it's a room-sized sphere. Reduce to mass=0.2 for a manageable, dramatic effect. Test iteratively — there's no substitute for in-headset scale perception.

### Stereo Parallax
The VR vertex shader must pass **per-eye camera position** for correct stereo:
```glsl
varying vec3 vCameraPos;
void main() {
  vCameraPos = cameraPosition; // Three.js sets this per-eye in VR
  // ...
}
```
Do NOT hardcode camera position — each eye renders from a different offset.

---

## Post-Processing in VR

### The `postprocessing` Library Does NOT Support WebXR
The `postprocessing` npm package (EffectComposer, BloomEffect, etc.) has **zero XR/stereo awareness**. It cannot render to the XR framebuffer.

In the render loop, VR mode must bypass the composer:
```typescript
if (renderer.xr.isPresenting) {
  renderer.render(scene, camera);  // Direct render — no composer
} else {
  composer.render(delta);           // Desktop gets postprocessing
}
```

**Consequence:** Any screen-space effects (bloom, distortion, tone mapping, chromatic aberration) are completely invisible in VR.

### VR-Compatible Alternatives
Replace screen-space postprocessing with 3D scene objects:

| Desktop Effect | VR Replacement |
|----------------|----------------|
| Bloom | Emissive materials, MeshBasicMaterial with bright colors, additive blending |
| Screen distortion | Expanding shockwave ring meshes (RingGeometry + DoubleSide + fade) |
| Color grading | Adjust material colors directly |
| Glow | Larger, brighter MeshBasicMaterial spheres with transparency |

**Example — merger collision effect:**
```typescript
// Glow sphere: scale up + color shift at peak
this.glowMaterial.opacity = glowIntensity * 0.9;
this.mergerGlow.scale.setScalar(1 + glowIntensity * 5);
// Purple → white shift
this.glowMaterial.color.setRGB(
  0.39 + glowIntensity * 0.61,
  0.40 + glowIntensity * 0.60,
  0.95 + glowIntensity * 0.05
);

// Expanding shockwave ring
const shockProgress = Math.max(0, (playbackTime - mergerNorm) * 6);
if (shockProgress > 0 && shockProgress < 1) {
  shockwaveMaterial.opacity = (1 - shockProgress) * 0.7;
  shockwaveRing.scale.setScalar(1 + shockProgress * 15);
} else {
  shockwaveMaterial.opacity = 0;
}
```

---

## Camera Rig Architecture

### The Rig Pattern
All movable objects (camera, controllers, teleport target) live under a single `cameraRig` group:
```
scene
  └── cameraRig (THREE.Group)
      ├── camera (PerspectiveCamera)
      ├── controller1
      ├── controller2
      └── teleportTarget
```

Moving the rig moves everything together. The XR system updates the camera's **local** transform from headset tracking; the rig provides the **world** offset.

### Critical: World-Space vs Local-Space Coordinates
**Any child of `cameraRig` receives positions in rig-local space.** When raycasting against world-space objects (ground plane, scene objects), you MUST convert the hit point before assigning to a rig child:

```typescript
// WRONG — world hit assigned as local position → offset by rig transform
teleportTarget.position.copy(worldHitPoint);

// CORRECT — convert to rig-local space first
teleportTarget.position.copy(worldHitPoint);
cameraRig.worldToLocal(teleportTarget.position);
```

This applies to:
- Teleport target ring/reticle
- Any preview markers or indicators that are children of the rig
- Anything positioned from a raycast result

Without `worldToLocal()`, the marker appears offset from the actual ray intersection — the offset grows as the rig moves further from origin.

---

## Locomotion

### Thumbstick Mapping (Quest Controllers)
```
Left controller:
  axes[2] = strafe (left/right)
  axes[3] = forward/back
  buttons[1] = grip (hold for fly mode)
  buttons[3] = thumbstick press (menu toggle)
  buttons[4] = X button

Right controller:
  axes[2] = horizontal turn (left/right)
  axes[3] = vertical fly (up/down)
  buttons[1] = grip
  buttons[3] = thumbstick press
```

### Ground-Locked vs Fly Mode
```typescript
if (leftGrip) {
  // Fly mode: full 3D movement following head direction
  // forward/right keep Y component from camera quaternion
} else {
  // Ground mode: project to XZ plane
  forward.y = 0; forward.normalize();
  right.y = 0; right.normalize();
}
```

### Right Stick: Horizontal Turn + Vertical Fly
```typescript
// Horizontal: rotate the rig (yaw)
if (Math.abs(rx) > DEAD_ZONE) {
  cameraRig.rotateY(-rx * TURN_SPEED * dt);
}
// Vertical: move up/down (NOT pitch rotation — see below)
if (Math.abs(ry) > DEAD_ZONE) {
  cameraRig.position.y += -ry * MOVE_SPEED * 0.5 * dt;
}
```

#### Why NOT Pitch Rotation on the Rig
**Do not use `cameraRig.rotateX()` for vertical look.** The XR headset controls camera orientation via head tracking. Rotating the rig on X conflicts with the headset's own pitch — the rotation is applied but immediately composed with the headset pose, creating disorienting or invisible results.

- **Yaw (rotateY) works** because it rotates the rig as a whole in world space — consistent with the user turning in place.
- **Pitch (rotateX) fails** because the headset already handles vertical look via physical head movement.
- **Use vertical fly** (position.y) instead — the user moves up/down and uses their head to look around.

### Teleport
- Raycast from controller against ground plane
- On trigger release, move camera rig to hit point
- Always set `cameraRig.position.y = 0` for ground-level teleport
- **Remember:** teleport target is a rig child — use `worldToLocal()` on the hit point

### Movement Speed
Default 2 m/s feels sluggish in large scenes. **5 m/s** is a good baseline for exploration. Vertical fly at half speed (2.5 m/s) feels natural.

---

## VR UI Panels

### The Pattern
Use a textured plane mesh that floats in world space. Render UI to a canvas, apply as texture.

```typescript
class VRPanel {
  mesh: THREE.Mesh;      // Plane with CanvasTexture
  canvas: HTMLCanvasElement;
  ctx: CanvasRenderingContext2D;

  // Position in front of camera
  positionInFront(camera: THREE.Camera, distance: number) {
    const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(camera.quaternion);
    this.mesh.position.copy(camera.position).addScaledVector(forward, distance);
    this.mesh.lookAt(camera.position);
  }
}
```

### Interaction
- Raycast from controller/hand against panel mesh
- Convert intersection UV to canvas coordinates
- Hit-test against button regions
- Visual feedback: reticle dot at intersection, ray color change, hover state

### Tips
- Start panel hidden, toggle with menu button (thumbstick press or X button)
- Keep buttons large (at least 0.15m tall) for easy targeting
- Use high contrast colors (panel renders at VR resolution)
- Render order matters — set `renderOrder` to ensure panel is always visible

---

## Testing & Debugging

### You Cannot Test VR Without a Headset
This is non-negotiable. Desktop browser testing tells you nothing about:
- Stereo rendering correctness
- Controller/hand interaction feel
- Performance at VR frame rates (72-120 fps)
- Alpha blending behavior in AR mode
- Spatial audio and haptics

### Remote Debugging Setup
1. Enable **Developer Mode** via the Meta phone app (Devices > Headset Settings > Developer Mode)
2. Connect Quest to PC via USB, approve connection dialog in headset
3. Open `chrome://inspect/#devices` in desktop Chrome
4. Your Quest browser tabs appear — click **inspect** for full DevTools
5. **Wireless option:** `adb tcpip 5555` then `adb connect <quest-ip>:5555`

**Note:** The Developer menu location changes across Quest firmware versions. Try:
- Settings > System > Developer
- Settings > Developer
- Settings > Advanced > Developer

If no Developer option exists, you need to register at developer.meta.com first (free), enable via the phone app, and reboot the Quest.

### Quest Browser vs PWA
- **Always test in Quest Browser first** (not the PWA)
- PWAs cache aggressively — stale builds cause confusion
- Use incognito tab or hard-refresh to ensure latest code
- If the PWA is installed, it may run a completely different version

### Iteration Loop
1. Make change
2. Deploy (or use local network URL)
3. Hard-refresh in Quest Browser
4. Test specific feature
5. Check console via remote debugging

**Do not** iterate blindly without on-device testing. Four rounds of blind fixes cost more than setting up remote debugging once.

---

## Common Pitfalls

### 1. Requesting immersive-ar When You Mean immersive-vr
See the Critical Rule above. This single mistake cascades into dozens of rendering issues.

### 2. Objects at Origin with Camera at (0, 1.6, 0)
In VR, the camera is at head height. Objects at origin are at your feet. Position objects at eye level for the best experience.

### 3. scene.background Doesn't Work in AR
Three.js intentionally skips background rendering in AR sessions. You must fill the background yourself (opaque sky sphere, shader output with alpha=1).

### 4. Geometry Inversion + BackSide = Invisible
`scale(-1,1,1)` + `BackSide` double-negates face culling. Use `DoubleSide` instead. See "Geometry Inversion Trap" above.

### 5. Transparent Materials in VR
Materials with `transparent: true` render differently in AR vs VR. In VR, transparency is visual only. In AR, low alpha = passthrough camera.

### 6. Forgetting frustumCulled = false
Large skybox spheres may be culled by the VR camera's frustum. Always set `frustumCulled = false` on skybox meshes.

### 7. Not Disposing Geometries/Materials on Mode Switch
If you swap geometries (e.g., large sphere ↔ small sphere), always `.dispose()` the old one to prevent GPU memory leaks.

### 8. Default Framebuffer Resolution Is Low
Without explicitly creating an `XRWebGLLayer` with `getNativeFramebufferScaleFactor()`, the Quest renders at a fraction of native resolution. Everything looks pixelated. Always set native scale factor.

### 9. Post-Processing Effects Invisible in VR
The `postprocessing` library doesn't support WebXR. Bloom, distortion, and tone mapping are skipped when `renderer.xr.isPresenting`. Use 3D scene objects instead.

### 10. Teleport/Reticle Misaligned with Controller Ray
If the teleport target or reticle is a child of `cameraRig`, world-space hit points must be converted to local space via `cameraRig.worldToLocal()`. Otherwise the marker is offset by the rig's position.

### 11. Right Stick Pitch Rotation Doesn't Work
`cameraRig.rotateX()` conflicts with headset tracking. Use vertical position movement (fly up/down) instead. Only yaw (`rotateY`) works reliably on the rig.

---

## Architecture Recommendations

### Session Mode as App-Level Decision
Don't let individual scenes choose session mode. The XR manager should request the session, and scenes should adapt to what they get.

```typescript
// Good: XR manager decides
const mode = "immersive-vr"; // App-level decision

// Bad: Scene tries to change session type
if (userWantsPassthrough) requestSession("immersive-ar"); // Can't switch mid-session
```

### Scene Interface for VR
```typescript
interface Scene {
  supportsXR?: boolean;
  init(ctx: SceneContext): Promise<void>;
  update(dt: number, elapsed: number): void;
  dispose(): void;
}
```

Scenes should:
- Detect `renderer.xr.isPresenting` in update loop
- Switch between desktop and VR rendering modes
- Register/unregister VR panels with the XR manager
- Clean up VR state in dispose

### Passthrough as a Future Feature
If you need passthrough later, implement it as:
1. A separate "Enter AR" button (distinct from "Enter VR")
2. Using `immersive-ar` with a complete alpha management strategy tested on-device
3. Every material and shader must output correct alpha values (alpha=0 → passthrough, alpha=1 → opaque render)

There is no way to enable passthrough in an `immersive-vr` session. Never bolt passthrough onto a working VR app without dedicated on-device testing.
