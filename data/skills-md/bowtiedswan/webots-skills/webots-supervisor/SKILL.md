---
name: webots-supervisor
description: "Use this skill when using the Webots Supervisor API for programmatic scene manipulation, node access, field modification, object tracking, simulation control, recording animations, or dynamically spawning/removing objects. Triggers on: webots supervisor, getFromDef, getField, setSFVec3f, importMFNode, scene manipulation, spawn object, track position, simulation reset, movie recording."
---

Use this skill to operate the Webots Supervisor API as the scene-level control layer for experiments, reinforcement learning loops, and automated test orchestration.

Treat Supervisor as an extension of Robot: all Robot API calls still apply, plus privileged scene graph access and mutation.

Do not explain basic controller structure, sensor APIs, or actuator APIs in this skill. Delegate those topics to `webots-controller-programming`.

## When to use

- Use for scene tree access (`getFromDef`, `getFromId`, `getRoot`, `getSelf`).
- Use for field read/write and MF insertion/removal/import workflows.
- Use for trajectory/state tracking (pose, orientation matrix, velocity, COM, contacts).
- Use for dynamic spawn/remove/reset operations in episodic RL and regression tests.
- Use for simulation mode control, world save/load/reload, and movie/animation capture.

## Enabling Supervisor

Set the `supervisor` field of the controller's Robot node to `TRUE` in the world file.

Python:

```python
from controller import Supervisor
supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())
```

C:

```c
#include <webots/robot.h>
#include <webots/supervisor.h>

int main(int argc, char **argv) {
  wb_robot_init();
  int timestep = (int)wb_robot_get_basic_time_step();
  while (wb_robot_step(timestep) != -1) {
    // wb_supervisor_* calls
  }
  wb_robot_cleanup();
  return 0;
}
```

Use the same loop semantics as a standard Robot controller; call Supervisor functions inside step cycles.

## Core operations

### Node Access

```python
from controller import Supervisor
supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())

# Get nodes by DEF name
robot_node = supervisor.getFromDef("MY_ROBOT")
# Get self node
self_node = supervisor.getSelf()
# Get root node (top-level Group)
root = supervisor.getRoot()
# Get by unique ID
node = supervisor.getFromId(42)
```

```c
WbNodeRef robot_node = wb_supervisor_node_get_from_def("MY_ROBOT");
WbNodeRef self_node = wb_supervisor_node_get_self();
WbNodeRef root = wb_supervisor_node_get_root();
WbNodeRef node = wb_supervisor_node_get_from_id(42);
```

### Field Manipulation

```python
# Get a field
translation_field = robot_node.getField("translation")
rotation_field = robot_node.getField("rotation")

# Read field values
pos = translation_field.getSFVec3f()  # returns [x, y, z]
rot = rotation_field.getSFRotation()  # returns [x, y, z, angle]

# Write field values (MOVE an object!)
translation_field.setSFVec3f([1.0, 2.0, 0.5])
rotation_field.setSFRotation([0, 0, 1, 1.57])

# MF fields (multi-value)
children_field = root.getField("children")
count = children_field.getCount()
```

```c
WbFieldRef translation_field = wb_supervisor_node_get_field(robot_node, "translation");
WbFieldRef rotation_field = wb_supervisor_node_get_field(robot_node, "rotation");

const double *pos = wb_supervisor_field_get_sf_vec3f(translation_field);
const double *rot = wb_supervisor_field_get_sf_rotation(rotation_field);

const double new_pos[3] = {1.0, 2.0, 0.5};
const double new_rot[4] = {0.0, 0.0, 1.0, 1.57};
wb_supervisor_field_set_sf_vec3f(translation_field, new_pos);
wb_supervisor_field_set_sf_rotation(rotation_field, new_rot);

WbFieldRef children_field = wb_supervisor_node_get_field(root, "children");
int count = wb_supervisor_field_get_count(children_field);
```

### Position/Orientation Tracking

```python
node = supervisor.getFromDef("ROBOT")
# Absolute position [x, y, z]
pos = node.getPosition()
# 3x3 rotation matrix (9 values)
orient = node.getOrientation()
# Velocity [vx, vy, vz, wx, wy, wz]
vel = node.getVelocity()
# Center of mass
com = node.getCenterOfMass()
# Contact points
contacts = node.getContactPoints()
```

```c
const double *pos = wb_supervisor_node_get_position(node);
const double *orient = wb_supervisor_node_get_orientation(node);
const double *vel = wb_supervisor_node_get_velocity(node);
const double *com = wb_supervisor_node_get_center_of_mass(node);
int contact_count = 0;
WbContactPoint *contacts = wb_supervisor_node_get_contact_points(node, false, &contact_count);
```

### Dynamic Scene Modification

```python
# Import (spawn) a new node
children_field = root.getField("children")
children_field.importMFNodeFromString(-1, 'DEF NEW_BOX Solid { children [ Shape { geometry Box { size 0.1 0.1 0.1 } } ] }')

# Remove a node
node = supervisor.getFromDef("OLD_BOX")
node.remove()

# Export node as string
node_string = node.exportString()
```

```c
WbFieldRef children_field = wb_supervisor_node_get_field(root, "children");
wb_supervisor_field_import_mf_node_from_string(
  children_field,
  -1,
  "DEF NEW_BOX Solid { children [ Shape { geometry Box { size 0.1 0.1 0.1 } } ] }"
);

WbNodeRef old_box = wb_supervisor_node_get_from_def("OLD_BOX");
wb_supervisor_node_remove(old_box);

const char *node_string = wb_supervisor_node_export_string(node);
```

### Simulation Control

```python
# Reset simulation to initial state
supervisor.simulationReset()
# Reset physics only
supervisor.simulationResetPhysics()
# Set simulation mode
supervisor.simulationSetMode(Supervisor.SIMULATION_MODE_FAST)
# Quit
supervisor.simulationQuit(0)
```

```c
wb_supervisor_simulation_reset();
wb_supervisor_simulation_reset_physics();
wb_supervisor_simulation_set_mode(WB_SUPERVISOR_SIMULATION_MODE_FAST);
wb_supervisor_simulation_quit(0);
```

### Recording

```python
# Start movie
supervisor.movieStartRecording("output.mp4", 640, 480, 0, 25, 1, False)
supervisor.movieStopRecording()
# Animation
supervisor.animationStartRecording("anim.html")
supervisor.animationStopRecording()
```

```c
wb_supervisor_movie_start_recording("output.mp4", 640, 480, 0, 25, 1, false);
wb_supervisor_movie_stop_recording();
wb_supervisor_animation_start_recording("anim.html");
wb_supervisor_animation_stop_recording();
```

### Label Display (HUD text)

```python
supervisor.setLabel(0, "Score: 100", 0.01, 0.01, 0.1, 0xFF0000, 0, "Arial")
```

```c
wb_supervisor_set_label(0, "Score: 100", 0.01, 0.01, 0.1, 0xFF0000, 0.0, "Arial");
```

### Save/Load World State

```python
supervisor.worldSave("snapshot.wbt")
supervisor.worldLoad("other_world.wbt")
supervisor.worldReload()
```

```c
wb_supervisor_world_save("snapshot.wbt");
wb_supervisor_world_load("other_world.wbt");
wb_supervisor_world_reload();
```

## RL/Test orchestration pattern

Use a deterministic episode loop:

1. Reset simulation or physics.
2. Reposition/reset entities via field setters.
3. Step simulation for warmup ticks.
4. Collect observations from Supervisor node/field reads.
5. Evaluate success/failure, save metrics, optionally record movie/animation.

## Operational rules and pitfalls

- Re-acquire node/field handles after world reload and after PROTO regeneration.
- Treat fields retrieved via base-node access on PROTO internals as read-only.
- Guard for NULL returns during world closing/reload transitions.
- Prefer DEF naming conventions for stable node retrieval in large scenes.
- Use pose/contact tracking enable APIs for lower-overhead repeated queries.

## Reference index

Read `references/supervisor_reference.md` for complete API coverage (C, C++, Python, Java, MATLAB), enums, and function-by-function mapping.
