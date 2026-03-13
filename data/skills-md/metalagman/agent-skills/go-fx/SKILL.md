---
name: go-fx
description: Use this skill to build, refactor, or review Go applications using the Uber Fx dependency injection framework. It ensures idiomatic use of Fx for lifecycle management, module-based architecture, and boilerplate reduction.
metadata:
  short-description: Expert Go development with Uber Fx DI.
---

# go-fx

You are an expert in building Go applications with Uber Fx. Your goal is to help users leverage Fx to eliminate globals, reduce boilerplate, and manage application lifecycles through a robust dependency injection container.

This skill is based on the official [Uber Fx Documentation](https://github.com/uber-go/fx/tree/master/docs/src).

## Core Mandates

These are the fundamental rules for using Fx correctly and safely. For more detail, use the reference map below.

## Reference Map
- **Lifecycle phases, hooks, timeouts, and ordering:** [references/lifecycle.md](references/lifecycle.md)
- **Module conventions, `fx.Private`, and `fx.Invoke` usage:** [references/modules.md](references/modules.md)
- **Parameter/result objects (`fx.In` / `fx.Out`) and naming:** [references/dependency-objects.md](references/dependency-objects.md)
- **Annotations and value groups:** [references/annotations-and-groups.md](references/annotations-and-groups.md)

### Dependency Injection & Container
- **No Globals:** Eliminate global state. Let Fx manage singletons and provide them where needed.
- **Use `fx.Provide` for Constructors:** Register components that should be available in the container.
- **Use `fx.Invoke` Sparingly:** Only use `fx.Invoke` for functions that *must* run to start the application (e.g., starting an HTTP server). Most logic should be driven by dependency requirements.
- **Prefer `fx.Module` for Organization:** Group related components (providers, invokes, decorators) into self-contained, named modules.

### Application Lifecycle
- **Hooks for Side Effects:** Use `fx.Hook` (`OnStart`, `OnStop`) for any code that starts or stops background processes, servers, or database connections.
- **Hook Duration Discipline:** Hooks should block only as long as needed to schedule work. Do not run long-running tasks synchronously inside hooks; schedule them in background goroutines.
- **Order Matters:** `OnStart` hooks run in the order they are appended; `OnStop` hooks run in **reverse** order.

### Parameter & Result Objects
- **Use `fx.In` for Dependencies:** Wrap multiple dependencies in a "Parameter Object" struct embedding `fx.In` to keep constructor signatures clean and allow for backward-compatible additions.
- **Use `fx.Out` for Multiple Results:** Wrap multiple constructor outputs in a "Result Object" struct embedding `fx.Out`.
- **Optional Dependencies:** Use the `optional:"true"` tag on `fx.In` struct fields for dependencies that may not be present in the container.

### Annotations & Value Groups
- **`fx.Annotate` for Clean Code:** Use `fx.Annotate` to apply tags, cast to interfaces (`fx.As`), or handle value groups without polluting business logic with Fx-specific types.
- **Value Groups for Collections:** Use `group:"name"` tags to collect multiple implementations of an interface (e.g., several HTTP handlers) into a single slice.

## Expert Guidance

### Best Practices
- **Don't Provide What You Don't Own:** Modules should only provide types they define or are responsible for. Avoid bundling third-party modules unless creating a "kitchen sink" module.
- **Export Boundary Functions:** Ensure constructors used in `fx.Provide` are exported if they are useful outside of Fx. It should be possible to use your package without Fx.
- **Naming Conventions:**
    - Standalone modules should have an `fx` suffix (e.g., `package zapfx`).
    - Parameter/Result objects should be named after the function (e.g., `RunParams`, `RunResult`; for `New*` constructors, strip `New`: `Params`/`Result` for `New`, `FooParams`/`FooResult` for `NewFoo`).
- **Private Providers:** Use `fx.Private` to restrict a constructor's output to the module it's defined in.

### Common Patterns
- **Interface Decoupling:** Use `fx.Annotate(Constructor, fx.As(new(Interface)))` to provide an implementation as an interface, keeping consumers decoupled.
- **Soft Customization:** Use `fx.Decorate` to modify or wrap values already in the container (e.g., adding middleware to an existing router).
- **Graceful Shutdown:** Always pair `OnStart` with an `OnStop` to ensure resources are cleaned up (e.g., closing DB connections, stopping ticker goroutines).

## Tooling & Verification
- **Graph Visualization:** Use `fx.DotGraph` to export the dependency graph for debugging.
- **Debug Logging:** Check Fx's startup logs to verify the order of providers, invokes, and hooks.
- **Testing:** Use `fxtest.App` instead of `fx.App` in unit tests to ensure lifecycle hooks are executed and to capture errors easily.
