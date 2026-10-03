---
name: ue5-architecture
description: UE5.6-UE5.8 architecture planning and module boundary design for Unreal projects. Use when requests involve module layout, Build.cs dependencies, reflection exposure strategy, Public/Private API boundaries, naming conventions, and preventing circular dependencies.
---

# Quick Start
- Collect current module list, `*.Build.cs`, and major gameplay/UI systems.
- Propose one target module graph before writing code.
- Output module responsibilities and ownership in a table.

# Workflow
- Identify runtime, editor, UI, networking, and data modules from current codebase.
- Define Public API for each module as minimal headers and Blueprint surface.
- Define Private implementation boundaries and include rules.
- Define `PublicDependencyModuleNames` and `PrivateDependencyModuleNames` per module.
- Report risks: circular includes, over-exposed reflection types, and cross-layer references.

# Constraints
- Keep `UCLASS/USTRUCT/UENUM` only where reflection is required.
- Prefer forward declarations in headers; include concrete headers in `.cpp`.
- Do not move types across modules without listing migration impact.
- Keep naming aligned with Unreal conventions (`U`, `A`, `F`, `E` prefixes).

# Failure Handling
- If ownership of a class is ambiguous, place it in runtime module first and log a TODO to split after usage mapping.
- If dependency graph becomes cyclic, extract shared contracts into a thin common module.
- If Build.cs dependencies are uncertain, choose minimal set and verify compile paths immediately.

# Escalation
- Escalate when a refactor requires asset redirectors, class renames, or package path migration.
- Escalate when module split changes public Blueprint class paths used by existing content.
