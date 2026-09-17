---
name: spacemit-robot-peripherals
description: Use when users work with SpacemiT Robot SDK 5G/MR880A, IMU/CMP10A/MXC4005/ICM42670P, key, LED/WS2812, lidar/YDLIDAR/RPLIDAR, light sensor/W1160, misc IO/GPIO, NFC/SI512, power management, or WiFi/NetworkManager modules, including native C components, ROS 2 nodes, device setup, builds, examples, API integration, tests, hardware smoke checks, or layered debugging.
metadata:
  requires:
    bins: ["bash"]
  sdk:
    module_paths:
      - components/peripherals/5g
      - middleware/ros2/peripherals/5g
      - components/peripherals/imu
      - middleware/ros2/peripherals/imu
      - components/peripherals/key
      - middleware/ros2/peripherals/key
      - components/peripherals/led
      - middleware/ros2/peripherals/led
      - components/peripherals/lidar
      - middleware/ros2/peripherals/lidar
      - components/peripherals/light_sensor
      - middleware/ros2/peripherals/light_sensor
      - components/peripherals/misc_io
      - middleware/ros2/peripherals/misc_io
      - components/peripherals/nfc
      - middleware/ros2/peripherals/nfc
      - components/peripherals/pm
      - middleware/ros2/peripherals/pm
      - components/peripherals/wifi
      - middleware/ros2/peripherals/wifi
    primary_docs:
      - components/peripherals/5g/README.md
      - components/peripherals/5g/include/5g.h
      - components/peripherals/5g/package.xml
      - components/peripherals/5g/test.yaml
      - middleware/ros2/peripherals/5g/README.md
      - middleware/ros2/peripherals/5g/package.xml
      - middleware/ros2/peripherals/5g/test.yaml
      - components/peripherals/imu/README.md
      - components/peripherals/imu/include/imu.h
      - components/peripherals/imu/package.xml
      - components/peripherals/imu/test.yaml
      - middleware/ros2/peripherals/imu/README.md
      - middleware/ros2/peripherals/imu/package.xml
      - middleware/ros2/peripherals/imu/test.yaml
      - components/peripherals/key/README.md
      - components/peripherals/key/include/key.h
      - components/peripherals/key/package.xml
      - components/peripherals/key/test.yaml
      - middleware/ros2/peripherals/key/README.md
      - middleware/ros2/peripherals/key/package.xml
      - middleware/ros2/peripherals/key/test.yaml
      - components/peripherals/led/README.md
      - components/peripherals/led/include/led.h
      - components/peripherals/led/package.xml
      - components/peripherals/led/test.yaml
      - middleware/ros2/peripherals/led/README.md
      - middleware/ros2/peripherals/led/package.xml
      - middleware/ros2/peripherals/led/test.yaml
      - components/peripherals/lidar/README.md
      - components/peripherals/lidar/include/lidar.h
      - components/peripherals/lidar/package.xml
      - components/peripherals/lidar/test.yaml
      - middleware/ros2/peripherals/lidar/README.md
      - middleware/ros2/peripherals/lidar/package.xml
      - middleware/ros2/peripherals/lidar/test.yaml
      - components/peripherals/light_sensor/README.md
      - components/peripherals/light_sensor/include/light_sensor.h
      - components/peripherals/light_sensor/package.xml
      - components/peripherals/light_sensor/test.yaml
      - middleware/ros2/peripherals/light_sensor/README.md
      - middleware/ros2/peripherals/light_sensor/package.xml
      - middleware/ros2/peripherals/light_sensor/test.yaml
      - components/peripherals/misc_io/README.md
      - components/peripherals/misc_io/include/misc_io.h
      - components/peripherals/misc_io/package.xml
      - components/peripherals/misc_io/test.yaml
      - middleware/ros2/peripherals/misc_io/README.md
      - middleware/ros2/peripherals/misc_io/package.xml
      - middleware/ros2/peripherals/misc_io/test.yaml
      - components/peripherals/nfc/README.md
      - components/peripherals/nfc/include/nfc.h
      - components/peripherals/nfc/package.xml
      - components/peripherals/nfc/test.yaml
      - middleware/ros2/peripherals/nfc/README.md
      - middleware/ros2/peripherals/nfc/package.xml
      - middleware/ros2/peripherals/nfc/test.yaml
      - components/peripherals/pm/README.md
      - components/peripherals/pm/include/pm.h
      - components/peripherals/pm/package.xml
      - components/peripherals/pm/test.yaml
      - middleware/ros2/peripherals/pm/README.md
      - middleware/ros2/peripherals/pm/package.xml
      - middleware/ros2/peripherals/pm/test.yaml
      - components/peripherals/wifi/README.md
      - components/peripherals/wifi/include/wifi.h
      - components/peripherals/wifi/package.xml
      - components/peripherals/wifi/test.yaml
      - middleware/ros2/peripherals/wifi/README.md
      - middleware/ros2/peripherals/wifi/package.xml
      - middleware/ros2/peripherals/wifi/test.yaml
    build_hint: target_preferred
---

# SpacemiT Robot Peripherals

## Purpose

Use this skill as the shared entry point for the current Robot SDK peripheral components and their ROS 2 adapters: 5G, IMU, key, LED, lidar, light sensor, misc IO/GPIO, NFC, PM, and WiFi.

Handle environment checks, native examples and C APIs, ROS 2 nodes and interfaces, contract tests, supervised hardware smoke checks, layered troubleshooting, and focused source changes. Treat performance support as partial: use an existing metric such as topic frequency or delay only when the selected module exposes a meaningful measurement.

## Contract

- Native modules: `components/peripherals/{5g,imu,key,led,lidar,light_sensor,misc_io,nfc,pm,wifi}`.
- ROS 2 adapters: `middleware/ros2/peripherals/{5g,imu,key,led,lidar,light_sensor,misc_io,nfc,pm,wifi}`.
- Build hint: `target_preferred`; confirm the board, target, enabled driver, and device-specific configuration when they affect the task.
- Resolve mode, `SROBOTIS_ROOT`, and target with `spacemit-robot-shared`; build with `spacemit-robot-build`; execute remote/hybrid work with `spacemit-robot-remote`; synchronize hybrid edits with `spacemit-robot-sync`.
- Do not hard-code a host, target, board, private directory, or device node. Read the selected module's real configuration.
- In remote and hybrid modes, perform builds, device access, examples, nodes, tests, and hardware diagnostics on the board.

## User Goals

| User goal | Support | Read |
| --- | --- | --- |
| Check hardware and environment | Yes | `references/device-routing.md`, then the selected README |
| Build or run a native example | Yes | `references/native-development.md` |
| Integrate a public C API | Yes | `references/native-development.md`, public header, example |
| Build or use a ROS 2 node | Yes | `references/ros2-development.md` |
| Run contract or hardware tests | Yes | `references/testing.md`, both layer-specific `test.yaml` files |
| Diagnose missing data or failures | Yes | `references/troubleshooting.md` |
| Measure performance | Partial | Existing module metric only; do not invent a common benchmark |

## Workflow

1. Identify the device, then distinguish native C, ROS 2, or end-to-end work and the task type: setup, build, example, API integration, test, troubleshooting, or source change.
2. Resolve mode, SDK root, board, and target through the base skills.
3. Read `references/device-routing.md`, then load only the one task reference and minimum SDK source-of-truth files needed.
4. Check the transport or system service, hardware identity, device node, permissions, occupancy, enabled driver, and safety impact before execution.
5. For ROS 2 work, build or install the native component before the adapter and confirm the staging/install prefix is visible.
6. For execution requests, run real commands. Do not answer a request such as “run”, “build”, or “test” with commands alone.
7. Diagnose bottom-up: hardware or system service -> native driver -> public C API -> staging/install -> ROS 2 node -> topic/service -> user application.
8. Return observed results and stop at the first unresolved failure instead of speculating.

## Execution Result Contract

For every execution request, report:

- execution mode and location;
- the real command;
- exit status;
- key output and observed device or ROS 2 state;
- artifact and log paths;
- skipped checks and missing prerequisites;
- the first failure point and the evidence supporting it.

Never fabricate sensor values, network state, topic rates, test output, or benchmark results.

## Safety Gates

Explain the impact and obtain confirmation before:

- writing an NFC block; confirm the intended card and block address;
- connecting, disconnecting, enabling AP mode, or changing a WiFi MAC when SSH or DDS may use that interface;
- 5G dialing, reset, flight-mode, PDP changes, or arbitrary AT commands;
- driving misc IO/GPIO outputs or a PM power switch without knowing the attached load;
- using `sudo`, changing group membership or permissions, deleting third-party caches, or running a supervised hardware smoke test.

Use timeouts for hardware checks and leave a device in a safe state when the selected module supports cleanup.

## References

Read only what matches the current task:

- `references/device-routing.md`: identify the device, transport, native example, ROS 2 package/node, and risk.
- `references/native-development.md`: build/run native components, call C APIs, select drivers, or change native source.
- `references/ros2-development.md`: build/run adapters, inspect parameters/interfaces, or integrate ROS 2 applications.
- `references/testing.md`: run examples, API/ROS contracts, `robot-test`, or supervised hardware smoke checks.
- `references/troubleshooting.md`: diagnose device, driver, staging, node, topic, service, network, or cache failures.

## Notes

- Prefer an SDK module `AGENTS.md` when present, then its README, public header, example, package manifest, parameters/interfaces, source, and `test.yaml` as the task requires.
- Use `scripts/test/robot-test` only for an explicit test, CI, or regression request. Ordinary example/node requests use the selected module's example or ROS 2 executable.
- Treat contract success and real hardware verification as separate evidence. Missing hardware means hardware verification was skipped, not passed.
