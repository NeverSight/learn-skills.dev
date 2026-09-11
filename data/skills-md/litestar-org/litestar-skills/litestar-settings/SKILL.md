---
name: litestar-settings
description: "Auto-activate for get_env, dataclass settings, pydantic_settings, BaseSettings, lru_cache config factories, app.state settings, LITESTAR_APP, or env parsing. Not for frontend env."
---

# Litestar Settings

Use this skill for typed settings, env loading, cached settings factories, and app-state wiring.

## Code Style Rules

- Use dataclass settings plus get_env for fresh Litestar apps.
- Use pydantic-settings when the project already depends on Pydantic for config.
- Cache settings once per process.
- Keep secret values out of logs and generated docs.

## Quick Reference

- Settings patterns: [settings.md](references/settings.md)
- Pair with [litestar-di](../litestar-di/SKILL.md) for settings providers.
- Pair with [litestar-deployment](../litestar-deployment/SKILL.md) for runtime env wiring.

<workflow>

## Workflow

1. Inventory required env vars and defaults.
2. Choose dataclass settings or the existing Pydantic settings path.
3. Add a cached factory.
4. Inject settings through app state or DI.

</workflow>

<guardrails>

## Guardrails

- Do not parse env vars repeatedly in handlers.
- Do not use msgspec Structs for env loading.
- Do not bake environment-specific values into code.
- Do not log secrets while debugging config.

</guardrails>

<validation>

## Validation Checkpoint

- [ ] Settings are typed.
- [ ] Settings are cached.
- [ ] Required values fail early.
- [ ] Tests can override settings without mutating global process env unexpectedly.

</validation>

<example>

## Example

```python
from dataclasses import dataclass, field
from functools import lru_cache
from os import getenv


def get_env(key: str, default: str) -> str:
    return getenv(key, default)


@dataclass(frozen=True)
class AppSettings:
    name: str = field(default_factory=lambda: get_env("APP_NAME", "api"))


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return AppSettings()
```

</example>

## References Index

- [settings.md](references/settings.md)

## Official References

- <https://docs.litestar.dev/> - Litestar documentation
- <https://docs.litestar.dev/latest/reference/> - Litestar API reference

## Shared Styleguide Baseline

- [General](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
- [Litestar](../litestar-styleguide/references/litestar.md)
