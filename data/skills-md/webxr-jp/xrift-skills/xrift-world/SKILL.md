---
name: xrift-world
description: Guide for building WebXR worlds on the XRift platform. Covers React Three Fiber + Rapier physics engine + @xrift/world-components API hooks, components, code templates, and type definitions.
---

# XRift World Development Guide

A guide for creating and modifying WebXR worlds for the XRift platform.

## References

- [API Reference](references/api-reference.md) - Full specification of all hooks, components, and constants in `@xrift/world-components`
- [Code Templates](references/code-templates.md) - Implementation patterns for GLB models, textures, Skybox, interactions, and more
- [Type Definitions](references/type-definitions.md) - Type definitions for User, PlayerMovement, VRTrackingData, TeleportDestination

## Critical Rules (Must Follow)

1. **Always use `baseUrl` from `useXRift()` when loading assets**
2. **Place asset files in the `public/` directory**
3. **`baseUrl` includes a trailing `/`, so join with `${baseUrl}path`** (`${baseUrl}/path` is WRONG)

```typescript
// Correct
const { baseUrl } = useXRift()
const model = useGLTF(`${baseUrl}robot.glb`)

// Wrong
const model = useGLTF('/robot.glb')           // Absolute path - NG
const model = useGLTF(`${baseUrl}/robot.glb`) // Extra / - NG
```

## Project Overview

- **Purpose**: WebXR worlds for the XRift platform
- **Tech Stack**: React Three Fiber + Rapier physics engine + Module Federation
- **How It Works**: Uploaded to CDN, dynamically loaded by the frontend

## Project Structure

```
xrift-world-template/
├── public/              # Asset files (place directly, no subdirectories needed)
│   ├── model.glb
│   ├── texture.jpg
│   └── skybox.jpg
├── src/
│   ├── components/      # 3D components
│   ├── World.tsx        # Main world component
│   ├── dev.tsx          # Development entry point
│   ├── index.tsx        # Production export
│   └── constants.ts     # Constants
├── .triplex/            # Triplex (3D editor) config
├── xrift.json           # XRift CLI config
├── vite.config.ts       # Build config (Module Federation)
└── package.json
```

## xrift.json Configuration

### physics (Physics Settings)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `gravity` | number | 9.81 | Gravity strength (positive value; Earth=9.81, Moon=1.62, Jupiter=24.79) |
| `allowInfiniteJump` | boolean | true | Whether to allow infinite jumping |

```json
{
  "physics": {
    "gravity": 9.81,
    "allowInfiniteJump": true
  }
}
```

**Examples**:
- **Obstacle course world**: `"allowInfiniteJump": false` to add fall risk
- **Low gravity world**: `"gravity": 1.62` (Moon gravity) for floaty movement
- **High gravity world**: `"gravity": 24.79` (Jupiter gravity) for heavy movement

## Command Reference

```bash
# Development
npm run dev        # Start dev server (http://localhost:5173)
npm run build      # Production build
npm run typecheck  # Type checking

# XRift CLI
xrift login        # Authenticate
xrift create       # Create new project
xrift upload world # Upload world
xrift whoami       # Check logged-in user
xrift logout       # Log out
```

## Development Environment

Run `npm run dev` to start the dev server. You can navigate and test the world in first-person view.

| Action | Key |
|--------|-----|
| Look around | Click to lock mouse, then move mouse |
| Move | W / A / S / D |
| Ascend / Descend | E or Space / Q |
| Interact | Aim crosshair and click |
| Release mouse lock | ESC |

`Interactable` component click behavior can also be tested in the dev environment (the center Raycaster detects the `LAYERS.INTERACTABLE` layer).

### dev.tsx Structure

`src/dev.tsx` is the development-only entry point. It is not included in the production build.

**Note**: `XRiftProvider` is not needed in production (the frontend wraps it automatically).

## Dependencies

### Required (peerDependencies)
- `react` / `react-dom` ^19.0.0
- `three` ^0.182.0
- `@react-three/fiber` ^9.3.0
- `@react-three/drei` ^10.7.3
- `@react-three/rapier` ^2.1.0

### XRift-specific
- `@xrift/world-components` - XRift hooks and components

## Troubleshooting

### "useXRift must be used within XRiftProvider"

**Cause**: Not wrapped with `XRiftProvider`

**Solution**:
- Check that `src/dev.tsx` uses `XRiftProvider`
- When using Triplex: check `.triplex/provider.tsx`

### Assets fail to load

**Cause**: Not using `baseUrl`, or incorrect path concatenation

**Solution**:
```typescript
// Correct
const { baseUrl } = useXRift()
const model = useGLTF(`${baseUrl}robot.glb`)

// Wrong
const model = useGLTF('/robot.glb')
const model = useGLTF(`${baseUrl}/robot.glb`)
```

### Physics not working

**Cause**: Not wrapped with `Physics` component, or missing `RigidBody`

**Solution**:
```typescript
<Physics>
  <RigidBody type="fixed">  {/* or "dynamic" */}
    <mesh>...</mesh>
  </RigidBody>
</Physics>
```

## Links

- [XRift Documentation](https://docs.xrift.net)
- [XRift CLI (GitHub)](https://github.com/WebXR-JP/xrift-cli)
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber)
- [Rapier Physics](https://rapier.rs/docs/)
- [Triplex (Visual Editor)](https://triplex.dev/)

## Example Implementations

- **GLB model**: `src/components/Duck/index.tsx`
- **Skybox**: `src/components/Skybox/index.tsx`
- **Animation**: `src/components/RotatingObject/index.tsx`
- **Interaction**: `src/components/InteractableButton/index.tsx`
- **User tracking**: `src/components/RemoteUserHUDs/index.tsx`
- **Teleport**: `src/components/TeleportPortal/index.tsx`
- **Main world**: `src/World.tsx`
