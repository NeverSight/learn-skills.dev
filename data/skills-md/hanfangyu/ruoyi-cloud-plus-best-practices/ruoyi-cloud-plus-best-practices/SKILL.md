---
name: ruoyi-cloud-plus-best-practices
description: "Unified best-practice skill for RuoYi-Cloud-Plus backend engineering. Use when designing, implementing, refactoring, or reviewing Java microservice code and you need one-pass guidance across DDD service modeling, foundational service/module split (ruoyi-common + ruoyi-api + ruoyi-modules), and project coding conventions."
---

# RuoYi Cloud Plus Best Practices

## Overview

Use this as the single entry skill for RuoYi-Cloud-Plus backend work.
Apply it to keep architecture, base service boundaries, and code style consistent in one run.

## Routing Rules

1. Use DDD flow first when the task is a new domain capability, aggregate boundary change, or complex business refactor.
2. Use basic-service flow first when the task is shared capability extraction or cross-service API design.
3. Use code-convention flow first when the task is code review, PR cleanup, or style alignment.
4. Run all three flows for medium-to-large feature delivery.

## Unified Execution Flow

1. Clarify scope and classify task type.
- Task type: `domain-design`, `base-capability`, `implementation`, or `review`.
- Map impacted modules: `ruoyi-modules/*`, `ruoyi-api/*`, `ruoyi-common/*`.

2. Design architecture and boundaries.
- Apply DDD package and dependency constraints.
- Keep bounded context ownership clear.
- Keep cross-service contracts in `ruoyi-api`.

3. Place reusable capability correctly.
- Put reusable infrastructure in `ruoyi-common`.
- Put cross-service contracts in `ruoyi-api`.
- Put provider and business orchestration in `ruoyi-modules`.

4. Implement with project conventions.
- Keep `controller -> service -> mapper` direction.
- Keep BO/VO/Entity separation and conversion strategy.
- Use required annotations for permission, logging, idempotency, transaction, and RPC.

5. Run final quality checks.
- Check dependency direction and module coupling.
- Check API contract isolation from local entities.
- Check formatting and naming alignment with project conventions.

## Output Contract

When using this skill, always output:
1. Scope classification and impacted modules.
2. Architecture and dependency decisions.
3. File-level implementation plan or change list.
4. Convention and risk checklist.

## References

- DDD and layered design: `references/ddd.md`
- Foundational service split: `references/basic-service.md`
- Coding conventions and review checklist: `references/code-convention.md`
