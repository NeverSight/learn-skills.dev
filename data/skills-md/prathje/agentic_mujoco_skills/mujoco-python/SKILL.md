---
name: mujoco-python
description: >
  Guide for building and controlling MuJoCo physics simulations in Python. Use this skill whenever
  the user wants to: create or run a MuJoCo simulation, load an MJCF/XML model, step physics,
  render frames or take screenshots (offscreen or with viewer), read sensors or joint positions,
  control joints or actuators, configure the camera, change visualization flags or geom groups,
  or tune solver/integrator settings. Also trigger when the user mentions mujoco, mjcf, humanoid
  simulation, robot simulation in mujoco, or physics rendering with mujoco — even if they don't
  say "MuJoCo" explicitly but describe tasks like "simulate a robot", "render a physics scene",
  or "read joint angles from the sim".
---

# MuJoCo Python Skill

This skill covers the MuJoCo native Python bindings (`pip install mujoco`).
For installation details, read `references/SETUP.md` in this skill directory.

For the most up-to-date API reference, consult: https://mujoco.readthedocs.io/en/stable/python.html

## Agent Control (persistent simulation)

For interactive, persistent control of a running simulation (step, screenshot, read sensors
without restarting), two approaches are provided:

- **HTTP API** (`scripts/sim_server.py` + `scripts/sim_client.py`) — start a background server,
  control it from Python scripts or CLI. Zero extra deps. See `references/HTTP_API.md`.
- **MCP Server** (`scripts/sim_mcp.py`) — register as an MCP server so tools appear natively.
  Requires `pip install mcp`. See `references/MCP_SERVER.md`.

The HTTP approach is best for ad-hoc use: start the server, write a Python script using
`SimClient` to batch multiple operations (step, screenshot, read sensors) in one call.
The MCP approach is best for persistent setups where you always want simulation tools available.

The server architecture is two classes:
- **`SimApp`** — generic HTTP micro-framework with `@app.get()` / `@app.post()` decorators.
- **`MujocoSimApp(SimApp)`** — adds all MuJoCo routes. Accepts `scene_path` or existing `model`/`data`.

Custom routes can be added, and built-in routes overridden, via decorators. See `references/HTTP_API.md`.

## Quick-Start Pattern

Every MuJoCo script follows the same skeleton:

```python
import mujoco
import numpy as np

# 1. Load model and create mutable state
model = mujoco.MjModel.from_xml_path("scene.xml")
data  = mujoco.MjData(model)

# 2. (Optional) configure physics
model.opt.timestep = 0.002

# 3. Simulate
while data.time < duration:
    data.ctrl[:] = compute_controls(model, data)
    mujoco.mj_step(model, data)

# 4. (Optional) render
with mujoco.Renderer(model, height=480, width=640) as renderer:
    renderer.update_scene(data)
    pixels = renderer.render()  # numpy (H, W, 3) uint8
```

## Example Model

For a ready-made humanoid, use the Unitree G1 from MuJoCo Menagerie:

```
https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/refs/heads/main/unitree_g1/scene_with_hands.xml
```

This model references other files (meshes, textures) so it must be cloned locally:

```bash
git clone https://github.com/google-deepmind/mujoco_menagerie.git
# Then load: mujoco_menagerie/unitree_g1/scene_with_hands.xml
```

---

## Core Concepts

### model vs data

- **`MjModel`** — static description: bodies, joints, actuators, geometry, solver options. Immutable during simulation (except `model.opt` and a few tunables).
- **`MjData`** — mutable runtime state: positions, velocities, forces, sensor readings. Changes every step.

### Key size fields on model

| Field | Meaning |
|-------|---------|
| `model.nq` | Generalized position DOFs |
| `model.nv` | Generalized velocity DOFs |
| `model.nu` | Number of actuators |
| `model.nbody` | Number of bodies |
| `model.njnt` | Number of joints |
| `model.nsensor` | Number of sensors |

### Freejoint convention

A floating-base robot has a `freejoint` as its first joint. This means:
- `qpos[0:3]` = position (x, y, z)
- `qpos[3:7]` = orientation quaternion (w, x, y, z)
- `qpos[7:]`  = joint angles
- `qvel[0:3]` = linear velocity
- `qvel[3:6]` = angular velocity
- `qvel[6:]`  = joint velocities

---

## Loading Models

```python
# From file
model = mujoco.MjModel.from_xml_path("/path/to/scene.xml")

# From string (with optional assets dict for meshes/textures)
model = mujoco.MjModel.from_xml_string(xml_string, assets={"mesh.stl": mesh_bytes})

# From compiled binary
model = mujoco.MjModel.from_binary_path("/path/to/model.mjb")
```

---

## Stepping and Resetting

```python
mujoco.mj_step(model, data)                # advance one timestep
mujoco.mj_step(model, data, nstep=20)      # advance N timesteps at once
mujoco.mj_forward(model, data)             # recompute derived quantities (no time advance)
mujoco.mj_resetData(model, data)           # reset data to model defaults
mujoco.mj_resetDataKeyframe(model, data, key_id)  # reset to a saved keyframe
```

Split-stepping (set controls between constraint and integration phases):

```python
mujoco.mj_step1(model, data)   # position-dependent computations
data.ctrl[:] = my_controls     # set controls here
mujoco.mj_step2(model, data)   # velocity integration
```

---

## Reading Joint Positions and Velocities

```python
# All joints (flat arrays)
all_qpos = data.qpos.copy()   # always .copy() if you need to persist values
all_qvel = data.qvel.copy()

# By name
q = data.joint("left_knee").qpos[0]
dq = data.joint("left_knee").qvel[0]

# Get joint index for array slicing
jnt_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, "left_knee")
qpos_adr = model.jnt_qposadr[jnt_id]
qvel_adr = model.jnt_dofadr[jnt_id]
```

---

## Controlling Joints / Actuators

```python
# Set all actuator commands
data.ctrl[:] = np.zeros(model.nu)

# Set by index
data.ctrl[0] = 1.0

# Apply external forces directly (bypasses actuators)
data.qfrc_applied[dof_index] = torque        # generalized force
data.xfrc_applied[body_id] = [fx, fy, fz, tx, ty, tz]  # Cartesian wrench

# Gravity compensation (useful baseline)
data.ctrl[:] = data.qfrc_bias[6:]  # skip freejoint DOFs if present
```

### PD control pattern

```python
def pd_control(model, data, target_qpos, kp=100.0, kd=10.0):
    """Simple PD controller for all actuated joints."""
    free = model.nq > model.nu  # has freejoint?
    qoff = 7 if free else 0
    voff = 6 if free else 0
    for i in range(model.nu):
        q  = data.qpos[qoff + i]
        dq = data.qvel[voff + i]
        data.ctrl[i] = kp * (target_qpos[i] - q) + kd * (0.0 - dq)
```

---

## Reading Sensors

```python
# All sensor data (flat array)
all_sensors = data.sensordata.copy()

# By name
imu_data = data.sensor("imu_gyro").data.copy()

# Sensor metadata
sensor_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_SENSOR, "imu_gyro")
```

---

## Camera Control

```python
cam = mujoco.MjvCamera()

# Free camera (default, orbits a point)
cam.type = mujoco.mjtCamera.mjCAMERA_FREE
cam.lookat[:] = [0, 0, 1.0]   # point to look at
cam.distance  = 3.0            # meters from lookat
cam.azimuth   = 90             # horizontal angle (degrees)
cam.elevation = -20            # vertical angle (degrees)

# Model-defined camera (from XML <camera> element)
cam.type = mujoco.mjtCamera.mjCAMERA_FIXED
cam.fixedcamid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, "front_cam")

# Tracking camera (follows a body)
cam.type = mujoco.mjtCamera.mjCAMERA_TRACKING
cam.trackbodyid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "torso")
```

---

## Offscreen Rendering and Screenshots

The `mujoco.Renderer` class handles offscreen rendering without needing a window.

```python
from PIL import Image

with mujoco.Renderer(model, height=720, width=1280) as renderer:
    # RGB image
    renderer.update_scene(data)                        # default free camera
    renderer.update_scene(data, camera="front_cam")    # named camera
    renderer.update_scene(data, camera=cam)            # MjvCamera instance
    pixels = renderer.render()                         # (H, W, 3) uint8
    Image.fromarray(pixels).save("screenshot.png")

    # Depth image
    renderer.enable_depth_rendering()
    renderer.update_scene(data)
    depth = renderer.render()   # (H, W) float32
    renderer.disable_depth_rendering()

    # Segmentation map
    renderer.enable_segmentation_rendering()
    renderer.update_scene(data)
    seg = renderer.render()
    renderer.disable_segmentation_rendering()
```

### With visualization options

```python
opt = mujoco.MjvOption()
opt.flags[mujoco.mjtVisFlag.mjVIS_JOINT] = 1
opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = 1

renderer.update_scene(data, camera=cam, scene_option=opt)
pixels = renderer.render()
```

---

## Interactive Viewer

```python
import mujoco.viewer

# Blocking (simple)
mujoco.viewer.launch(model, data)

# Non-blocking (control loop)
with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        data.ctrl[:] = compute_controls(model, data)
        mujoco.mj_step(model, data)
        viewer.sync()

        # Modify viewer settings at runtime
        with viewer.lock():
            viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = 1
```

### Quitting the simulation

- `viewer.close()` — programmatically close the viewer window
- `viewer.is_running()` — returns False when the user closes the window
- Set a duration and `break` out of the loop

---

## Visualization Flags and Groups

### Visualization flags (`MjvOption.flags`)

Toggle what's visible in the scene. Key flags:

| Flag | What it shows |
|------|--------------|
| `mjVIS_JOINT` | Joint axes |
| `mjVIS_ACTUATOR` | Actuator indicators |
| `mjVIS_CONTACTPOINT` | Contact points |
| `mjVIS_CONTACTFORCE` | Contact force vectors |
| `mjVIS_COM` | Center of mass |
| `mjVIS_TRANSPARENT` | Transparent bodies |
| `mjVIS_CONVEXHULL` | Convex hull of meshes |
| `mjVIS_TEXTURE` | Textures on/off |
| `mjVIS_TENDON` | Tendon lines |
| `mjVIS_INERTIA` | Inertia boxes |
| `mjVIS_CONSTRAINT` | Constraint indicators |

```python
opt = mujoco.MjvOption()
opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = 1
opt.flags[mujoco.mjtVisFlag.mjVIS_JOINT] = 1
opt.flags[mujoco.mjtVisFlag.mjVIS_TRANSPARENT] = 1
```

### Render flags (scene-level)

```python
renderer.scene.flags[mujoco.mjtRndFlag.mjRND_WIREFRAME] = 1
renderer.scene.flags[mujoco.mjtRndFlag.mjRND_SHADOW] = 0
renderer.scene.flags[mujoco.mjtRndFlag.mjRND_REFLECTION] = 0
```

### Geom / Site / Joint Groups

MuJoCo assigns geoms, sites, joints to groups 0-5. Toggle group visibility:

```python
opt = mujoco.MjvOption()
opt.geomgroup[:] = [1, 1, 0, 0, 0, 0]   # show groups 0,1 only
opt.sitegroup[:] = [1, 0, 0, 0, 0, 0]   # show site group 0 only
opt.jointgroup[:] = [1, 1, 1, 0, 0, 0]  # show joint groups 0-2
```

---

## Solver and Algorithm Configuration

All physics algorithm settings live in `model.opt` (an `mjOption` struct).

### Integrator

```python
model.opt.integrator = mujoco.mjtIntegrator.mjINT_IMPLICITFAST  # default, fast
model.opt.integrator = mujoco.mjtIntegrator.mjINT_EULER         # semi-implicit Euler
model.opt.integrator = mujoco.mjtIntegrator.mjINT_RK4           # Runge-Kutta 4
model.opt.integrator = mujoco.mjtIntegrator.mjINT_IMPLICIT      # fully implicit
```

### Solver

```python
model.opt.solver = mujoco.mjtSolver.mjSOL_NEWTON  # default, most accurate
model.opt.solver = mujoco.mjtSolver.mjSOL_PGS     # Projected Gauss-Seidel
model.opt.solver = mujoco.mjtSolver.mjSOL_CG      # Conjugate Gradient
```

### Common parameters

```python
model.opt.timestep   = 0.002      # physics dt (seconds)
model.opt.iterations = 100        # solver iterations
model.opt.tolerance  = 1e-10      # solver convergence tolerance
model.opt.gravity[:] = [0, 0, -9.81]  # gravity vector
model.opt.impratio   = 1.0        # impedance ratio for contacts
model.opt.density    = 0.0        # medium density (air/water)
model.opt.viscosity  = 0.0        # medium viscosity
model.opt.wind[:]    = [0, 0, 0]  # wind vector
```

### Noslip solver (for better friction)

```python
model.opt.noslip_iterations = 20
model.opt.noslip_tolerance  = 1e-6
```

---

## Common Patterns

### Headless simulation with logging

```python
import mujoco
import numpy as np
import json

model = mujoco.MjModel.from_xml_path("scene.xml")
data = mujoco.MjData(model)

log = {"time": [], "qpos": [], "qvel": [], "ctrl": []}

duration = 5.0
while data.time < duration:
    data.ctrl[:] = np.zeros(model.nu)
    mujoco.mj_step(model, data)

    log["time"].append(float(data.time))
    log["qpos"].append(data.qpos.copy().tolist())
    log["qvel"].append(data.qvel.copy().tolist())
    log["ctrl"].append(data.ctrl.copy().tolist())

with open("sim_log.json", "w") as f:
    json.dump(log, f)
```

### Multi-camera screenshot sweep

```python
with mujoco.Renderer(model, height=480, width=640) as renderer:
    for az in [0, 90, 180, 270]:
        cam = mujoco.MjvCamera()
        cam.lookat[:] = [0, 0, 1]
        cam.distance = 3.0
        cam.azimuth = az
        cam.elevation = -20
        renderer.update_scene(data, camera=cam)
        Image.fromarray(renderer.render()).save(f"view_{az}.png")
```

### Body position tracking

```python
body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "torso")
pos = data.xpos[body_id].copy()    # (3,) world position
quat = data.xquat[body_id].copy()  # (4,) orientation quaternion
```
