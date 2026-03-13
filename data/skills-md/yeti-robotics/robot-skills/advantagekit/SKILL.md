---
name: advantagekit
description: >
  AdvantageKit logging framework best practices for FRC Java robots (2026 / AKit 4.x). Use when
  implementing or reviewing AdvantageKit IO layers, Logger usage, replay-compatible subsystem design,
  signal logging, output logging, or deterministic simulation. Triggers on: AdvantageKit,
  Logger.recordOutput, Logger.processInputs, LoggedRobot, IO interfaces, IOInputs, AutoLog annotation,
  replay, log-replay, non-deterministic, or any AdvantageKit-related robot code task.
---

# AdvantageKit (2026)

> Documentation sourced from [docs.advantagekit.org](https://docs.advantagekit.org). AdvantageKit is developed by Littleton Robotics (FRC 6328).

## Core IO Layer Pattern

Every hardware-interacting subsystem uses three pieces:

1. **IO interface** — declares `updateInputs()` and output methods
2. **IOInputs inner class** — annotated `@AutoLog`, holds all sensor values
3. **Subsystem** — depends on IO, calls `processInputs` in `periodic()`

The `@AutoLog` annotation generates a `<ClassName>AutoLogged` class — always instantiate the generated class, not the original.

```java
// DriveIO.java
public interface DriveIO {
    @AutoLog
    class DriveIOInputs {
        public double leftPositionRad = 0.0;
        public double rightPositionRad = 0.0;
        public double leftVelocityRadPerSec = 0.0;
        public double rightVelocityRadPerSec = 0.0;
        public double[] appliedVolts = new double[] {};
    }

    default void updateInputs(DriveIOInputs inputs) {}
    default void setVoltage(double leftVolts, double rightVolts) {}
}

// Drive.java
public class Drive extends SubsystemBase {
    private final DriveIO io;
    private final DriveIOInputsAutoLogged inputs = new DriveIOInputsAutoLogged();

    public Drive(DriveIO io) {
        this.io = io;
    }

    @Override
    public void periodic() {
        io.updateInputs(inputs);
        Logger.processInputs("Drive", inputs);
        // All logic uses inputs.leftPositionRad, etc. — never calls hardware directly
    }

    public void setVoltage(double left, double right) {
        io.setVoltage(left, right);
    }
}
```

### IO Implementations

- `DriveIOSparkMax` — real hardware, talks to CAN devices
- `DriveIOSim` — physics simulation
- `DriveIO` (interface default) — no-op for replay / unit tests

Inject the correct implementation in `RobotContainer` based on `Robot.isReal()` / `isSimulation()`.

## Logger Initialization Order

**Rule: call `Logger.start()` before instantiating any subsystem or `RobotContainer`.**

```java
public class Robot extends LoggedRobot {
    private RobotContainer robotContainer;

    @Override
    public void robotInit() {
        // Configure data receivers BEFORE start()
        Logger.addDataReceiver(new WPILOGWriter());
        Logger.addDataReceiver(new NT4Publisher());
        Logger.start(); // ← must be first

        robotContainer = new RobotContainer(); // ← safe to create subsystems now
    }
}
```

## Key Rules

| Rule | Reason |
|------|--------|
| Hardware access only inside IO implementations | Ensures all inputs are logged and replayable |
| Use `Timer.getTimestamp()` not `Timer.getFPGATimestamp()` | FPGA timestamps are non-deterministic |
| Call logging APIs from main thread only | `recordOutput` / `processInputs` are not thread-safe |
| Don't read subsystem inputs in constructors | Inputs are stale until first `periodic()` |
| Test replay regularly during development | Catches non-determinism early |

## Output Logging

Log computed values for post-match analysis:

```java
Logger.recordOutput("Drive/LeftVelocityError", setpoint - inputs.leftVelocityRadPerSec);
Logger.recordOutput("Odometry/Robot", poseEstimator.getEstimatedPosition());
Logger.recordOutput("Mechanism", mechanism2d);
```

See **[references/output-logging.md](references/output-logging.md)** for replay-based output generation and version control integration.

## Common Issues

See **[references/common-issues.md](references/common-issues.md)** for detailed guidance on:

- Non-deterministic data sources (NetworkTables, YAGSL, random, maps)
- Multithreading constraints
- Uninitialized inputs in constructors

## Recording Inputs (Detail)

See **[references/recording-inputs.md](references/recording-inputs.md)** for:

- `@AutoLog` annotation and `AutoLogged` class naming
- Units in input fields (naming convention vs. `Measure` types)
- IO implementation structure (real / sim / replay no-op)
- Dashboard inputs — `LoggedDashboardChooser`, `LoggedNetworkNumber`, etc.
- Coprocessor / vision data via IO layer
