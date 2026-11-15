---
name: blender-physics-simulation
description: Blender 5.x physics simulations — rigid body, cloth, fluid/smoke/fire (Mantaflow), soft body, particles, force fields, collisions, and simulation baking/caching via Python (bpy).
---

# Blender Physics & Simulation Expert

## Overview

This skill provides expert guidance for Blender 5.x physics simulations: rigid body dynamics, cloth, fluid (Mantaflow smoke/fire/liquid), soft body, particle systems, force fields, baking/caching, and Python automation of simulation setups. The reference files contain the complete physics type catalog and Python API patterns.

## MCP-First Approach

Prefer the **official Blender MCP Server** (Blender Lab, Blender 5.1+) for setting up rigid body / cloth / fluid sims, baking caches, reading results directly in a running Blender session. Fall back to emitting Python scripts only when the MCP server is not connected.

**Detection:** at session start, look for tools whose names match `execute_blender_code`, `get_objects_summary`, or `search_api_docs` — these belong to the official `blender-mcp` server. If any are present, MCP is available.

**Tools used by this skill:**

- `execute_blender_code` — run `bpy` Python in the live session (primary action)
- `get_objects_summary`, `get_object_detail_summary` — inspect scene state before mutating
- `get_blendfile_summary_datablocks` / `_missing_files` / `_of_linked_libraries` / `_path_info` / `_usage_guess` — inventory the file
- `search_api_docs`, `get_python_api_docs`, `search_manual_docs` — confirm correct API/operator names before calling them
- `get_screenshot_of_window_as_image` / `_as_json`, `get_screenshot_of_area_as_image` — verify visual results
- `jump_to_tab_by_name`, `jump_to_tab_by_space_type`, `jump_to_view3d_object_by_name`, `jump_to_view3d_object_data_by_name` — drive the UI to make changes visible
- `render_thumbnail_to_path`, `render_viewport_to_path` — capture quick visual feedback

**Workflow:** inspect with a `get_*` / `search_*` tool → mutate via `execute_blender_code` → verify with a screenshot or summary tool. Keep code blocks small and idempotent so failures are easy to localize.

Setup: see [docs/blender-mcp-setup.md](../../docs/blender-mcp-setup.md).

## Task Decision Tree

- **"Make objects fall / collide"** -> See Rigid Body Setup
- **"Simulate cloth / fabric"** -> See Cloth Simulation
- **"Create smoke / fire"** -> See Fluid Simulation (Gas)
- **"Simulate liquid / water"** -> See Fluid Simulation (Liquid)
- **"Particle effects (rain, sparks, etc.)"** -> See Particle Systems
- **"Add wind / gravity / turbulence"** -> See Force Fields
- **"Soft / jelly physics"** -> See Soft Body
- **"Bake / cache simulation"** -> See Baking & Caching
- **"Simulation not working"** -> See Debugging section

## Rigid Body Setup

### Active Rigid Body (Falls, Collides)

```python
import bpy

obj = bpy.context.active_object

# Add rigid body
bpy.ops.rigidbody.object_add(type='ACTIVE')
rb = obj.rigid_body

rb.mass = 1.0
rb.friction = 0.5
rb.restitution = 0.5        # Bounciness (0-1)
rb.collision_shape = 'CONVEX_HULL'  # BOX, SPHERE, CAPSULE, CYLINDER, CONE, CONVEX_HULL, MESH, COMPOUND
rb.use_margin = True
rb.collision_margin = 0.04

# Damping
rb.linear_damping = 0.04
rb.angular_damping = 0.1

# Deactivation (sleep when slow)
rb.use_deactivation = True
rb.deactivation_linear_threshold = 0.4
rb.deactivation_angular_threshold = 0.5
```

### Passive Rigid Body (Stationary Collider)

```python
bpy.ops.rigidbody.object_add(type='PASSIVE')
rb = obj.rigid_body
rb.collision_shape = 'MESH'  # Use mesh shape for ground/walls
rb.friction = 0.5
rb.restitution = 0.0

# Animated passive (keyframe-driven)
rb.kinematic = True
# Keyframe kinematic on/off for switching between animated and simulated
```

### Rigid Body World

```python
scene = bpy.context.scene

# Create rigid body world if not exists
if scene.rigidbody_world is None:
    bpy.ops.rigidbody.world_add()

rbw = scene.rigidbody_world
rbw.time_scale = 1.0
rbw.substeps_per_frame = 10
rbw.solver_iterations = 10
rbw.use_split_impulse = True

# Point cache
rbw.point_cache.frame_start = 1
rbw.point_cache.frame_end = 250
```

### Rigid Body Constraints

```python
# Create empty for constraint
bpy.ops.object.empty_add(location=(0, 0, 0))
empty = bpy.context.active_object

bpy.ops.rigidbody.constraint_add(type='FIXED')
# Types: FIXED, POINT, HINGE, SLIDER, PISTON, GENERIC, GENERIC_SPRING, MOTOR

rbc = empty.rigid_body_constraint
rbc.object1 = bpy.data.objects["Object1"]
rbc.object2 = bpy.data.objects["Object2"]

# For HINGE:
rbc.use_limit_ang_z = True
rbc.limit_ang_z_lower = -1.5708
rbc.limit_ang_z_upper = 1.5708

# Breaking
rbc.use_breaking = True
rbc.breaking_threshold = 100.0
```

## Cloth Simulation

```python
import bpy

obj = bpy.context.active_object

# Add cloth physics
bpy.ops.object.modifier_add(type='CLOTH')
cloth = obj.modifiers["Cloth"]
settings = cloth.settings
collision = cloth.collision_settings

# Quality
settings.quality = 5              # Simulation quality (steps/frame)
settings.time_scale = 1.0

# Physical properties
settings.mass = 0.3               # Fabric weight (kg)
settings.tension_stiffness = 15.0  # Resistance to stretching
settings.compression_stiffness = 15.0
settings.shear_stiffness = 5.0
settings.bending_stiffness = 0.5   # Resistance to bending (higher = stiffer)
settings.tension_damping = 5.0
settings.compression_damping = 5.0
settings.shear_damping = 5.0
settings.bending_damping = 0.5

# Air resistance
settings.air_damping = 1.0

# Collision
collision.use_collision = True
collision.distance_min = 0.015     # Min distance from colliders
collision.use_self_collision = True
collision.self_distance_min = 0.015
collision.self_friction = 5.0

# Pinning (vertex group)
settings.vertex_group_mass = "Pin"  # Vertex group name — weight 0 = fully pinned
```

### Cloth Presets

| Style | mass | tension | bending | air_damping |
| --- | --- | --- | --- | --- |
| Silk | 0.1 | 5 | 0.05 | 1 |
| Cotton | 0.3 | 15 | 0.5 | 1 |
| Denim | 0.5 | 40 | 10 | 1 |
| Leather | 0.5 | 80 | 150 | 1 |
| Rubber | 0.3 | 15 | 25 | 1 |

## Collision Object

```python
# Add collision to objects that cloth/particles should interact with
bpy.ops.object.modifier_add(type='COLLISION')
collision = obj.modifiers["Collision"]
settings = collision.settings

settings.thickness_outer = 0.02
settings.thickness_inner = 0.2
settings.cloth_friction = 5.0
settings.damping = 0.0
```

## Fluid Simulation (Mantaflow)

### Domain Setup

```python
import bpy

# Create domain (must be mesh object, typically a cube)
bpy.ops.mesh.primitive_cube_add(size=4)
domain = bpy.context.active_object
domain.name = "FluidDomain"

bpy.ops.object.modifier_add(type='FLUID')
fluid = domain.modifiers["Fluid"]
fluid.fluid_type = 'DOMAIN'

domain_settings = fluid.domain_settings
domain_settings.domain_type = 'GAS'  # GAS (smoke/fire) or LIQUID

# Resolution
domain_settings.resolution_max = 64      # Voxel resolution (32-256 typical)
domain_settings.use_adaptive_domain = True

# Cache
domain_settings.cache_frame_start = 1
domain_settings.cache_frame_end = 250
domain_settings.cache_type = 'REPLAY'     # REPLAY, MODULAR, ALL
```

### Smoke/Fire (Gas Domain)

```python
domain_settings.domain_type = 'GAS'
domain_settings.use_noise = True          # Enable noise detail
domain_settings.noise_scale = 2           # Noise resolution multiplier

# Display
domain_settings.display_thickness = 1.0
domain_settings.slice_per_voxel = 5

# Dissolution
domain_settings.use_dissolve_smoke = True
domain_settings.dissolve_speed = 5

# Fire
domain_settings.burning_rate = 0.75
domain_settings.flame_smoke = 1.0
domain_settings.flame_vorticity = 0.5
domain_settings.flame_max_temp = 1.5
```

### Liquid Domain

```python
domain_settings.domain_type = 'LIQUID'
domain_settings.use_mesh = True           # Generate mesh surface
domain_settings.mesh_concave_upper = 3.5
domain_settings.mesh_concave_lower = 0.5
domain_settings.mesh_particle_radius = 1.0

# Particle type
domain_settings.use_spray_particles = True
domain_settings.use_foam_particles = True
domain_settings.use_bubble_particles = True

# Viscosity
domain_settings.viscosity_base = 1.0
domain_settings.viscosity_exponent = 6   # Water: base=1, exp=6
```

### Flow Object (Emitter)

```python
bpy.ops.object.modifier_add(type='FLUID')
fluid = obj.modifiers["Fluid"]
fluid.fluid_type = 'FLOW'

flow = fluid.flow_settings
flow.flow_type = 'SMOKE'         # SMOKE, FIRE, BOTH, LIQUID
flow.flow_behavior = 'INFLOW'   # INFLOW, OUTFLOW, GEOMETRY
flow.use_absolute = False
flow.temperature = 1.0           # Smoke temperature
flow.smoke_color = (0.7, 0.7, 0.7)
flow.density = 1.0
flow.fuel_amount = 0.5           # For fire

# Surface emission
flow.surface_distance = 1.5
flow.volume_density = 0.0        # 0 = surface only, 1 = volume fill

# Animated source
flow.use_particle_size = False
```

### Effector (Force)

```python
bpy.ops.object.modifier_add(type='FLUID')
fluid = obj.modifiers["Fluid"]
fluid.fluid_type = 'EFFECTOR'

effector = fluid.effector_settings
effector.effector_type = 'COLLISION'  # COLLISION or GUIDE
effector.surface_distance = 0.0
effector.use_effector = True
```

## Soft Body

```python
import bpy

obj = bpy.context.active_object

bpy.ops.object.modifier_add(type='SOFT_BODY')
sb = obj.modifiers["Softbody"].settings

# Object properties
sb.mass = 1.0
sb.friction = 0.5

# Goal (stiffness toward original shape)
sb.use_goal = True
sb.goal_default = 0.7           # 0 = fully soft, 1 = rigid
sb.goal_spring = 0.5
sb.goal_friction = 0.5
sb.vertex_group_goal = "Goal"   # Vertex group for per-vertex goal

# Edges (spring connections)
sb.use_edges = True
sb.pull = 0.5                   # Spring stiffness (pull)
sb.push = 0.5                   # Spring stiffness (push)
sb.damping = 5.0
sb.plastic = 0                  # Permanent deformation
sb.bending = 0.1                # Bending stiffness
sb.spring_length = 0            # 0 = use original edge lengths

# Self-collision
sb.use_self_collision = False
sb.ball_size = 0.49
sb.ball_stiff = 1.0
sb.ball_damp = 0.5

# Solver
sb.step_min = 1
sb.step_max = 5
sb.use_auto_step = True
sb.error_threshold = 0.1
```

## Particle Systems

### Emitter Particles

```python
import bpy

obj = bpy.context.active_object

# Add particle system
bpy.ops.object.particle_system_add()
ps = obj.particle_systems[-1]
settings = ps.settings

settings.type = 'EMITTER'
settings.count = 1000
settings.frame_start = 1
settings.frame_end = 100
settings.lifetime = 50
settings.lifetime_random = 0.5

# Emission
settings.emit_from = 'FACE'     # VERT, FACE, VOLUME
settings.use_modifier_stack = True

# Velocity
settings.normal_factor = 1.0     # Emit along normals
settings.tangent_factor = 0.0
settings.object_align_factor = (0, 0, 0)
settings.factor_random = 0.5

# Physics
settings.physics_type = 'NEWTON'  # NO, NEWTON, KEYED, BOIDS, FLUID
settings.mass = 1.0
settings.particle_size = 0.05
settings.size_random = 0.5
settings.use_multiply_size_mass = False

# Gravity
settings.effector_weights.gravity = 1.0

# Display
settings.display_size = 0.05
settings.display_method = 'DOT'  # NONE, DOT, CIRC, CROSS, AXIS, RENDER
```

### Hair Particles

```python
settings.type = 'HAIR'
settings.hair_length = 0.5
settings.hair_step = 5            # Number of segments
settings.root_radius = 1.0
settings.tip_radius = 0.0
settings.use_hair_bspline = True

# Children
settings.child_type = 'INTERPOLATED'  # NONE, SIMPLE, INTERPOLATED
settings.child_nbr = 50            # Viewport children
settings.rendered_child_count = 100 # Render children
settings.child_length = 1.0
settings.child_radius = 0.1
settings.clump_factor = 0.0
settings.clump_shape = 0.0
settings.roughness_1 = 0.0
settings.roughness_2 = 0.0
```

### Render Settings

```python
settings.render_type = 'HALO'    # NONE, HALO, LINE, PATH, OBJECT, COLLECTION
# For mesh instances:
settings.render_type = 'OBJECT'
settings.instance_object = bpy.data.objects["InstanceMesh"]
# For collection instances:
settings.render_type = 'COLLECTION'
settings.instance_collection = bpy.data.collections["MyCollection"]
settings.use_whole_collection = True
settings.use_rotation_instance = True
settings.use_scale_instance = True
```

## Force Fields

### Adding Force Fields

```python
import bpy

# Force field types (add as empty or to existing object)
bpy.ops.object.effector_add(type='FORCE')  # Attract/repel
# Types: FORCE, WIND, VORTEX, MAGNETIC, HARMONIC, CHARGE, LENNARDJ,
#         TEXTURE, GUIDE, BOID, TURBULENCE, DRAG, SMOKE

field = bpy.context.active_object.field

# Common properties
field.type = 'FORCE'
field.strength = 5.0               # Negative = attract
field.flow = 0.0                   # Outward flow
field.noise = 0.0                  # Random noise factor
field.seed = 0
field.use_max_distance = True
field.distance_max = 10.0
field.use_min_distance = False
field.falloff_type = 'SPHERE'      # SPHERE, TUBE, CONE
field.falloff_power = 2.0          # Distance falloff exponent
```

### Common Force Field Setups

```python
# Wind
bpy.ops.object.effector_add(type='WIND')
field = bpy.context.active_object.field
field.strength = 10.0
field.noise = 2.0                  # Gusty wind
field.flow = 0.5

# Turbulence
bpy.ops.object.effector_add(type='TURBULENCE')
field = bpy.context.active_object.field
field.strength = 5.0
field.size = 1.0                   # Turbulence scale
field.flow = 0.5

# Vortex
bpy.ops.object.effector_add(type='VORTEX')
field = bpy.context.active_object.field
field.strength = 5.0
field.inflow = 0.0                 # Inward pull

# Drag
bpy.ops.object.effector_add(type='DRAG')
field = bpy.context.active_object.field
field.linear_drag = 0.1
field.quadratic_drag = 0.0        # Velocity-dependent drag
```

## Baking & Caching

### Rigid Body Bake

```python
scene = bpy.context.scene
rbw = scene.rigidbody_world

rbw.point_cache.frame_start = 1
rbw.point_cache.frame_end = 250

# Free existing cache
bpy.ops.ptcache.free_bake_all()

# Bake
bpy.ops.ptcache.bake_all(bake=True)
```

### Fluid Bake

```python
# For fluid domain
domain = bpy.data.objects["FluidDomain"]
fluid = domain.modifiers["Fluid"]
ds = fluid.domain_settings

ds.cache_frame_start = 1
ds.cache_frame_end = 250

# Bake data (must select domain first)
bpy.context.view_layer.objects.active = domain
bpy.ops.fluid.bake_data()

# Bake noise (for gas)
bpy.ops.fluid.bake_noise()

# Bake mesh (for liquid)
bpy.ops.fluid.bake_mesh()

# Bake particles (spray/foam/bubble)
bpy.ops.fluid.bake_particles()

# Free caches
bpy.ops.fluid.free_data()
bpy.ops.fluid.free_noise()
bpy.ops.fluid.free_mesh()
bpy.ops.fluid.free_particles()
```

### Cloth/Soft Body/Particle Bake

```python
# Cloth and soft body use point cache
# Select object, then bake
bpy.ops.ptcache.bake(bake=True)  # Bake active cache
bpy.ops.ptcache.free_bake()       # Free active cache
bpy.ops.ptcache.bake_all(bake=True)  # Bake all caches
bpy.ops.ptcache.free_bake_all()       # Free all caches
```

## Debugging

### Common Issues

- **Simulation not running**: Check frame range. Ensure domain/world exists. Press play or bake.
- **Objects pass through each other**: Increase collision shape precision (use MESH for complex shapes), increase substeps, reduce time scale.
- **Cloth explodes**: Reduce time scale, increase quality steps, check for initial intersections with collision objects, increase collision distance.
- **Fluid leaks through domain**: Domain must fully enclose all flow objects. Increase resolution.
- **Particles ignore force fields**: Check effector weights on the particle system. Ensure force field is in the same collection/layer.
- **Simulation is different each time**: Set seed values. Ensure deterministic settings. Bake simulation.
- **Simulation is slow**: Reduce resolution (fluid), reduce particle count, increase collision margin (rigid body), use simpler collision shapes.

### Performance Tips

1. **Rigid Body**: Use simple collision shapes (Box, Sphere) when possible. MESH shapes are expensive.
2. **Cloth**: Lower quality value for iteration, increase only for final render. Reduce mesh density if possible.
3. **Fluid**: Resolution is the main performance driver. Use 32-64 for preview, 128-256 for final. Enable adaptive domain.
4. **Particles**: Use viewport display count lower than render count. Limit children in viewport.
5. **General**: Bake simulations before rendering. Baked simulations are faster to play back.

## Physics Reference

For the complete catalog of all physics types with property listings and configuration details, consult `references/physics_reference.md`.

## Python API Reference

For complete Python API patterns including rigid body, cloth, fluid, particle, and force field setup, consult `references/python_api.md`.

## Blender 5.1 Notes

No major physics API changes in Blender 5.1. The existing physics simulation APIs (rigid body, cloth, fluid, soft body, particles) remain unchanged. Minor stability improvements and bug fixes apply across all physics systems. See the general Python 3.13 notes in the blender-python-scripting skill for scripting environment changes.
