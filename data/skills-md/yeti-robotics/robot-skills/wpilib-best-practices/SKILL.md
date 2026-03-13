---
name: wpilib-best-practices
description: >
  WPILib and FRC robot programming best practices, design patterns, and code guidance for Java.
  Use when writing, reviewing, or explaining WPILib robot code—command-based project structure,
  subsystems, autonomous routines, RobotContainer layout, command definition patterns (inline,
  factory, subclass), or Constants organization.
---

# WPILib Best Practices

WPILib best practices span multiple domains. Load only the reference(s) relevant to the current task.

## References

| Domain | Reference | When to load |
| ------ | --------- | ------------ |
| Command-based architecture | [references/command-based.md](references/command-based.md) | Project structure, `Robot`/`RobotContainer` layout, command definition patterns (inline vs factory vs subclass), autonomous routines, subsystem organization, `Constants` class |
| Command Scheduler | [references/command-scheduler.md](references/command-scheduler.md) | How the scheduler runs, per-iteration execution order, default commands, scheduling conflicts, event callbacks, `disable()`/`cancel()` |
| Command Compositions | [references/command-compositions.md](references/command-compositions.md) | Combining commands with `sequence`, `parallel`, `race`, `deadline`, `repeatedly`; end condition and end behavior decorators; `ConditionalCommand`; `ProxyCommand` |

## Quick Navigation

- **"How do I structure my command-based project?"** → [command-based.md](references/command-based.md) (Project Structure)
- **"Should I use a factory method or a Command subclass?"** → [command-based.md](references/command-based.md) (Pattern Selection)
- **"Where do subsystems and button bindings go?"** → [command-based.md](references/command-based.md) (RobotContainer)
- **"How do I handle multi-subsystem commands without circular deps?"** → [command-based.md](references/command-based.md) (Static Command Factories)
- **"How does the scheduler decide what runs and when?"** → [command-scheduler.md](references/command-scheduler.md) (Per-Iteration Run Sequence)
- **"What happens when two commands need the same subsystem?"** → [command-scheduler.md](references/command-scheduler.md) (Scheduling a Command)
- **"How do I run commands in sequence or parallel?"** → [command-compositions.md](references/command-compositions.md) (Composition Types)
- **"How do I add a timeout or stop-when condition to a command?"** → [command-compositions.md](references/command-compositions.md) (End Condition Decorators)
- **"How do I run different commands based on a condition?"** → [command-compositions.md](references/command-compositions.md) (Conditional Commands)
