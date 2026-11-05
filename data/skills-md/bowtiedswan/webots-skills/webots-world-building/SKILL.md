---
name: webots-world-building
description: "Use this skill when creating or modifying Webots simulation worlds, adding objects to scenes, configuring appearances/materials/lighting/terrain, or working with the scene tree hierarchy. Triggers on: world building, scene tree, Solid node, Shape, Appearance, PBRAppearance, lighting, terrain, ElevationGrid, boundingObject, DEF USE, add objects, create world."
---

# Webots World Building

Build and modify `.wbt` worlds by composing scene tree nodes, assigning geometry and materials, configuring lighting, and setting physically efficient collision and dynamics properties. Follow VRML97-derived syntax and ENU coordinates (`X=East`, `Y=North`, `Z=Up`, Webots R2022a+).

Do not include controller programming or API usage. Do not define new PROTO files in this skill.

## When To Use

Use this skill for:
- Creating or restructuring scene trees
- Adding `Solid` objects and collision geometry
- Building terrain, arenas, and environment props
- Applying `PBRAppearance`, textures, and lighting
- Importing external meshes/CAD assets into a world

## Core Workflow

1. Open world and identify target insertion point in the scene tree.
2. Add structural node (`Group`, `Transform`, `Pose`, `Solid`, or `Robot`) based on whether physical behavior is required.
3. Add visual geometry under `Shape` (`geometry` + `appearance`).
4. Add `boundingObject` using simple primitives for collisions.
5. Add `Physics` only when dynamic simulation is required.
6. Configure lighting/background for readability and realism.
7. Validate transforms, scale, and collision performance.

## Scene Tree And Node Hierarchy

### Choose the right container

- `Group`: collect children without transform or physics semantics.
- `Transform`: apply translation/rotation/scale to child nodes.
- `Pose`: apply transform with concise pose-centric semantics.
- `Solid`: represent a physical object in the world.
- `Robot`: use robot root when modeling articulated robots (without defining PROTO here).

Use `Solid` for anything that should collide, receive mass, or participate in dynamics. Keep purely decorative geometry under non-physical containers when possible.

### Solid essentials

For `Solid`, manage three distinct concerns:
- `children`: visual geometry and subparts
- `boundingObject`: collision representation
- `physics`: inertial and damping behavior

```vrml
Solid {
  translation 0 0 0.4
  children [
    Shape {
      appearance PBRAppearance {
        baseColor 0.7 0.7 0.7
        roughness 0.6
        metalness 0.1
      }
      geometry Box { size 0.4 0.4 0.8 }
    }
  ]
  boundingObject Box { size 0.4 0.4 0.8 }
  physics Physics { density -1 mass 12 }
}
```

### Reuse nodes with DEF/USE

Define once, reuse many times for consistent materials, geometry, or transforms.

```vrml
DEF GRAY_WALL_MAT PBRAppearance {
  baseColor 0.78 0.78 0.8
  roughness 0.85
  metalness 0
}

Shape {
  appearance USE GRAY_WALL_MAT
  geometry Box { size 4 0.1 1.2 }
}
```

### Add nodes through the scene tree UI

In the scene tree, select parent node, press `Add`, then insert node type (`Solid`, `Shape`, `PBRAppearance`, `DirectionalLight`, etc.). Prefer this path for iterative world editing and immediate visual feedback.

## Geometry Nodes

Use primitive geometry whenever possible for speed and stable collisions.

### Primitive geometry examples

```vrml
# Box
Shape {
  appearance PBRAppearance { baseColor 0.8 0.2 0.2 roughness 0.5 metalness 0 }
  geometry Box { size 1.0 0.6 0.4 }
}

# Sphere
Shape {
  appearance PBRAppearance { baseColor 0.2 0.4 0.9 roughness 0.3 metalness 0.2 }
  geometry Sphere { radius 0.2 }
}

# Cylinder
Shape {
  appearance PBRAppearance { baseColor 0.7 0.7 0.7 roughness 0.4 metalness 0.6 }
  geometry Cylinder { radius 0.1 height 0.5 }
}

# Capsule
Shape {
  appearance PBRAppearance { baseColor 0.3 0.9 0.5 roughness 0.6 metalness 0 }
  geometry Capsule { radius 0.08 height 0.4 }
}

# Cone
Shape {
  appearance PBRAppearance { baseColor 0.95 0.7 0.2 roughness 0.7 metalness 0 }
  geometry Cone { bottomRadius 0.15 height 0.4 }
}

# Plane (useful for floors)
Shape {
  appearance PBRAppearance { baseColor 0.5 0.5 0.5 roughness 0.95 metalness 0 }
  geometry Plane { size 6 6 }
}
```

### Terrain with ElevationGrid

```vrml
Shape {
  appearance PBRAppearance {
    baseColorMap ImageTexture { url ["textures/soil_diffuse.jpg"] }
    roughness 1
    metalness 0
  }
  geometry ElevationGrid {
    xDimension 5
    yDimension 5
    xSpacing 1.0
    ySpacing 1.0
    height [
      0.00, 0.05, 0.10, 0.05, 0.00,
      0.02, 0.10, 0.18, 0.10, 0.02,
      0.04, 0.15, 0.30, 0.15, 0.04,
      0.02, 0.10, 0.18, 0.10, 0.02,
      0.00, 0.05, 0.10, 0.05, 0.00
    ]
  }
}
```

Use `height` arrays as procedural heightmaps. Keep grid resolution moderate for real-time performance.

### Custom mesh with IndexedFaceSet

```vrml
Shape {
  appearance PBRAppearance { baseColor 0.6 0.6 0.65 roughness 0.7 metalness 0.1 }
  geometry IndexedFaceSet {
    coord Coordinate {
      point [
        0 0 0, 1 0 0, 1 1 0, 0 1 0,
        0 0 1, 1 0 1, 1 1 1, 0 1 1
      ]
    }
    coordIndex [
      0, 1, 2, 3, -1,
      4, 5, 6, 7, -1,
      0, 1, 5, 4, -1,
      1, 2, 6, 5, -1,
      2, 3, 7, 6, -1,
      3, 0, 4, 7, -1
    ]
    creaseAngle 0.7
  }
}
```

### Import external assets with Mesh and CadShape

```vrml
# Mesh import (.obj, .stl, .dae, .fbx)
Shape {
  appearance PBRAppearance { baseColor 1 1 1 roughness 0.6 metalness 0 }
  geometry Mesh { url ["models/chair.obj"] }
}

# CAD import through CadShape
CadShape {
  url ["models/fixture.step"]
}
```

For imported visuals, pair with simplified primitive `boundingObject` instead of mesh collisions when possible.

## Appearance And Materials

### Legacy Appearance + Material

Use when backward compatibility with older assets is required.

```vrml
Shape {
  appearance Appearance {
    material Material {
      diffuseColor 0.8 0.2 0.2
      specularColor 0.2 0.2 0.2
      shininess 0.4
    }
  }
  geometry Box { size 0.4 0.4 0.4 }
}
```

### Preferred PBRAppearance

Use physically based materials for modern rendering quality.

```vrml
PBRAppearance {
  baseColor 0.7 0.7 0.7
  roughness 0.5
  metalness 0.2
  normalMap ImageTexture { url ["textures/metal_normal.png"] }
  occlusionMap ImageTexture { url ["textures/metal_ao.png"] }
}
```

### Texture mapping and UV control

```vrml
Shape {
  appearance PBRAppearance {
    baseColorMap ImageTexture { url ["textures/tiles_albedo.jpg"] }
    roughnessMap ImageTexture { url ["textures/tiles_roughness.jpg"] }
    normalMap ImageTexture { url ["textures/tiles_normal.jpg"] }
    textureTransform TextureTransform {
      scale 4 4
      rotation 0
      translation 0 0
    }
    roughness 1
    metalness 0
  }
  geometry Plane { size 8 8 }
}
```

### Example: realistic wooden table

```vrml
Solid {
  translation 0 0 0.38
  children [
    # Table top
    Shape {
      appearance PBRAppearance {
        baseColorMap ImageTexture { url ["textures/wood_albedo.jpg"] }
        roughnessMap ImageTexture { url ["textures/wood_roughness.jpg"] }
        normalMap ImageTexture { url ["textures/wood_normal.jpg"] }
        occlusionMap ImageTexture { url ["textures/wood_ao.jpg"] }
        roughness 0.85
        metalness 0
      }
      geometry Box { size 1.2 0.7 0.04 }
    }
    # Legs
    DEF TABLE_LEG Shape {
      appearance PBRAppearance {
        baseColorMap ImageTexture { url ["textures/wood_albedo.jpg"] }
        roughness 0.9
        metalness 0
      }
      geometry Box { size 0.06 0.06 0.72 }
    }
    Pose { translation 0.55 0.30 -0.38 children [ USE TABLE_LEG ] }
    Pose { translation -0.55 0.30 -0.38 children [ USE TABLE_LEG ] }
    Pose { translation 0.55 -0.30 -0.38 children [ USE TABLE_LEG ] }
    Pose { translation -0.55 -0.30 -0.38 children [ USE TABLE_LEG ] }
  ]
  boundingObject Box { size 1.2 0.7 0.76 }
  physics Physics { density -1 mass 18 }
}
```

## Lighting And Environment

Use layered lighting: environment/sun + local accent lights.

```vrml
DirectionalLight {
  direction -0.5 -0.3 -1
  color 1 0.98 0.95
  intensity 1.0
  ambientIntensity 0.25
  castShadows TRUE
}

PointLight {
  location 0 0 2.6
  color 1 0.95 0.85
  intensity 0.6
  radius 8
  castShadows TRUE
}

SpotLight {
  location 1.5 0.0 2.2
  direction -1 0 -1
  beamWidth 0.5
  cutOffAngle 0.9
  intensity 0.8
  castShadows TRUE
}

Background {
  skyColor [0.58 0.73 0.95]
  luminosity 1.0
}
```

For HDR environment reflections, assign HDR textures in `Background` texture fields where available in the world setup.

## Physics Setup

### Add Physics to dynamic solids

Use explicit mass properties for stable behavior.

```vrml
Solid {
  children [ Shape { geometry Box { size 0.4 0.3 0.2 } } ]
  boundingObject Box { size 0.4 0.3 0.2 }
  physics Physics {
    density -1
    mass 4.0
    centerOfMass [ 0 0 0 ]
    inertiaMatrix [
      0.05 0 0
      0 0.07 0
      0 0 0.09
    ]
    damping Damping {
      linear 0.01
      angular 0.02
    }
  }
}
```

### boundingObject best practices

- Prefer primitive shapes (`Box`, `Sphere`, `Capsule`, `Cylinder`) for collisions.
- Keep collision meshes coarse and convex when possible.
- Decouple visual mesh from collision geometry to reduce contact solver cost.
- Align `boundingObject` origin with `Solid` local frame to avoid offset mistakes.

### Contact properties in WorldInfo

Configure pairwise material behavior globally:

```vrml
WorldInfo {
  basicTimeStep 16
  contactProperties [
    ContactProperties {
      material1 "rubber"
      material2 "concrete"
      coulombFriction [1.0 0.8]
      bounce 0.05
      bounceVelocity 0.01
      softERP 0.2
      softCFM 0.00001
    }
  ]
}
```

## Practical World-Building Examples

### Create a simple arena with walls

```vrml
DEF FLOOR Solid {
  children [
    Shape {
      appearance PBRAppearance { baseColor 0.35 0.35 0.35 roughness 0.95 metalness 0 }
      geometry Box { size 8 8 0.1 }
    }
  ]
  boundingObject Box { size 8 8 0.1 }
  locked TRUE
}

DEF WALL_MAT PBRAppearance { baseColor 0.8 0.8 0.82 roughness 0.9 metalness 0 }

DEF WALL Solid {
  children [ Shape { appearance USE WALL_MAT geometry Box { size 8 0.2 1 } } ]
  boundingObject Box { size 8 0.2 1 }
  locked TRUE
}

Pose { translation 0 4 0.5 children [ USE WALL ] }
Pose { translation 0 -4 0.5 children [ USE WALL ] }
Pose {
  translation 4 0 0.5
  rotation 0 0 1 1.5708
  children [ USE WALL ]
}
Pose {
  translation -4 0 0.5
  rotation 0 0 1 1.5708
  children [ USE WALL ]
}
```

### Add stock objects (example: WoodenBox PROTO instance)

Instantiate built-in/available PROTO objects in the scene tree as world content:

```vrml
WoodenBox {
  translation 0.5 0.3 0.1
  size 0.4 0.3 0.2
}
```

Use object insertion from the `Add` button and tune transform/material fields in place.

### Set up indoor and outdoor environments

- Indoor: lower ambient light, add local `PointLight` and `SpotLight`, use high-roughness materials, assign wall/floor textures.
- Outdoor: use stronger `DirectionalLight`, brighter sky/background, terrain via `ElevationGrid`, sparse local fill lights.

### Import external models safely

1. Import visual mesh via `Mesh` or `CadShape`.
2. Normalize scale and orientation to ENU frame.
3. Wrap in `Solid` and add simple `boundingObject`.
4. Add `Physics` only when dynamic behavior is needed.

## Reference File

Use `references/world_building_reference.md` for detailed field-level node reference, supported texture/model formats, and physics/contact configuration tables.
