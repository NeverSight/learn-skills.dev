---
name: webots-controller-programming
description: "Use this skill when writing Webots robot controllers in any language (Python, C, C++, Java, MATLAB), understanding the simulation loop, device access patterns, sensor reading, actuator control, or debugging controllers. Triggers on: webots controller, wb_robot_step, robot.step, wb_robot_get_device, getDevice, controller programming, webots python, webots C."
---

# Webots Controller Programming

Use this skill to implement and debug standard robot controllers in Webots. Focus on the controller process model, control-loop timing, device lookup, sensor/actuator data flow, and language-specific setup. Treat the simulation loop as the primary control structure.

Load `references/controller_api_reference.md` when exact API signatures, language mappings, Makefile templates, or termination semantics are needed.

## Follow the Controller Architecture Model

- Run each controller as a separate process from the Webots simulator process.
- Bind exactly one controller to each Robot node through the Robot field `controller`.
- Place controller source in `controllers/<controller_name>/`.
- Match file naming to controller naming conventions per language.

Typical structure:

```text
<project>/
  worlds/
    demo.wbt
  controllers/
    my_controller/
      my_controller.py
      # or my_controller.c, my_controller.cpp, my_controller.java, my_controller.m
```

Lifecycle rules:

- Start controller process when simulation starts or when controller reload occurs.
- Initialize controller runtime (`Robot()` in Python, `wb_robot_init()` in C) before any device call.
- Keep process alive by repeatedly calling the simulation step function.
- Terminate cleanly when step returns `-1`.

## Implement the Simulation Loop First (Critical Pattern)

Treat the following loop as mandatory scaffolding before adding robot behavior.

Python:

```python
from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

while robot.step(timestep) != -1:
    # read sensors
    # process
    # write actuators
    pass
```

C:

```c
#include <webots/robot.h>

int main() {
  wb_robot_init();
  int timestep = (int)wb_robot_get_basic_time_step();

  while (wb_robot_step(timestep) != -1) {
    // read sensors
    // process
    // write actuators
  }

  wb_robot_cleanup();
  return 0;
}
```

Execution semantics:

- Call `robot.step(timestep)` / `wb_robot_step(timestep)` once per control iteration.
- Read fresh sensor data only after a successful step call.
- Apply actuator commands before the next step boundary.
- Stop loop when step returns `-1` (simulation ended or controller terminated).
- Use a control step that is a multiple of `WorldInfo.basicTimeStep`.

## Use the Device Access Pattern

- Retrieve device handles by name using `robot.getDevice("name")` or `wb_robot_get_device("name")`.
- Match names exactly with device `name` fields defined in `.wbt` or `.proto`.
- Enable sensors with a sampling period before reading values.
- Skip enable for actuators; issue commands directly.

Python example:

```python
from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

distance = robot.getDevice("front_ds")
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")

distance.enable(timestep)
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
```

C example:

```c
#include <webots/robot.h>
#include <webots/distance_sensor.h>
#include <webots/motor.h>

int main() {
  wb_robot_init();
  int timestep = (int)wb_robot_get_basic_time_step();

  WbDeviceTag ds = wb_robot_get_device("front_ds");
  WbDeviceTag left = wb_robot_get_device("left wheel motor");
  WbDeviceTag right = wb_robot_get_device("right wheel motor");

  wb_distance_sensor_enable(ds, timestep);
  wb_motor_set_position(left, INFINITY);
  wb_motor_set_position(right, INFINITY);

  while (wb_robot_step(timestep) != -1) {
  }

  wb_robot_cleanup();
  return 0;
}
```

## Read Sensors with Correct Timing

- Enable sensor once using control period (commonly `timestep`).
- Read values only after at least one `step` following enable.
- Expect repeated values if multiple reads occur without an intervening step.
- Handle vector sensors as arrays (`gps.getValues()` in Python, pointer arrays in C APIs).

Python pattern:

```python
gps = robot.getDevice("gps")
gps.enable(timestep)

while robot.step(timestep) != -1:
    position = gps.getValues()  # [x, y, z]
```

C pattern:

```c
WbDeviceTag gps = wb_robot_get_device("gps");
wb_gps_enable(gps, timestep);

while (wb_robot_step(timestep) != -1) {
  const double *p = wb_gps_get_values(gps); /* p[0], p[1], p[2] */
}
```

## Command Actuators with Step-Aware Semantics

- Use position control via `motor.setPosition(target)` / `wb_motor_set_position(tag, target)`.
- Use velocity control by setting position to infinity, then setting velocity.
- Limit effort with torque/force APIs where supported (`setAvailableTorque`, `setAvailableForce`, C equivalents).
- Treat actuator writes as buffered commands committed at the next step.

Python pattern:

```python
left = robot.getDevice("left wheel motor")
right = robot.getDevice("right wheel motor")

left.setPosition(float('inf'))
right.setPosition(float('inf'))

while robot.step(timestep) != -1:
    speed = 3.0
    left.setVelocity(speed)
    right.setVelocity(speed)
```

C pattern:

```c
wb_motor_set_position(left, INFINITY);
wb_motor_set_position(right, INFINITY);

while (wb_robot_step(timestep) != -1) {
  double speed = 3.0;
  wb_motor_set_velocity(left, speed);
  wb_motor_set_velocity(right, speed);
}
```

## Avoid Common Pitfalls

- Avoid chaining multiple `setPosition` calls before one `step`; only the last command is applied.
- Avoid assuming repeated `getValue` calls produce fresh data without `step`; values remain unchanged.
- Avoid using sensor values in the first loop iteration immediately after `enable`; run a step first.
- Avoid non-multiple control periods; keep controller step as an integer multiple of `WorldInfo.basicTimeStep`.

## Configure Language Runtimes

Use the language-specific bootstrap that matches the selected controller language.

- Python: `from controller import Robot`
- C: `#include <webots/robot.h>`
- C++: `#include <webots/Robot.hpp>` and `using namespace webots;`
- Java: `import com.cyberbotics.webots.controller.Robot;`
- MATLAB: define function/script whose name matches controller name

Python may run with the bundled interpreter or an external system interpreter, depending on project setup.

## Read Controller Arguments

- Set controller arguments in Robot field `controllerArgs`.
- Parse in Python from `sys.argv`.
- Parse in C/C++ through `argc, argv` in `main`.

Python example:

```python
import sys
from controller import Robot

robot = Robot()
mode = sys.argv[1] if len(sys.argv) > 1 else "default"
```

C example:

```c
#include <stdio.h>
#include <webots/robot.h>

int main(int argc, char **argv) {
  wb_robot_init();
  const char *mode = (argc > 1) ? argv[1] : "default";
  printf("mode=%s\n", mode);
  wb_robot_cleanup();
  return 0;
}
```

## Set Up Development and Debugging Workflow

- Edit with the built-in Webots editor for quick iteration.
- Use external IDEs (VS Code, PyCharm, CLion, others) by opening `controllers/<name>/` as a project folder.
- Compile C/C++ controllers through Makefile-driven builds from controller directory.
- Debug C/C++ extern controllers with `gdb` or `lldb` by attaching to the controller process.
- Run extern controllers as separate processes when tighter IDE/debugger integration is required.

For C/C++ build templates, Robot API signatures, and process termination timing details, consult `references/controller_api_reference.md`.
