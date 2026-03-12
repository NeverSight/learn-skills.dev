---
name: litestar-custom-types
description: Add custom type decoding/encoding and schema compatibility in Litestar for domain-specific values that are not handled by default serializers. Use when handlers need strongly typed custom inputs or outputs. Do not use when built-in scalar/model types already satisfy request and response contracts.
---

# Custom Types

## Execution Workflow

1. Define the domain type and its canonical wire representation.
2. Register type decoders/encoders at the appropriate layer.
3. Ensure OpenAPI schema generation remains accurate for custom values.
4. Add round-trip tests for decode, business usage, and encode output.

## Implementation Rules

- Keep serialization behavior stable and backward compatible.
- Fail fast with actionable error messages on invalid input.
- Avoid ambiguous representations that vary by locale/timezone.
- Keep custom type support centralized to prevent drift.

## Example Pattern

```python
from datetime import datetime
from litestar import Litestar, get


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value)

@get("/echo-ts/{value:str}")
async def echo_timestamp(value: datetime) -> dict[str, str]:
    return {"value": value.isoformat()}

app = Litestar(route_handlers=[echo_timestamp], type_decoders=[(datetime, parse_timestamp)])
```

## Validation Checklist

- Confirm valid payloads decode to the intended Python types.
- Confirm invalid payloads return deterministic client errors.
- Confirm encoded responses and generated schemas match actual runtime behavior.

## Cross-Skill Handoffs

- Use `litestar-openapi` if schema customization is substantial.
- Use `litestar-requests` and `litestar-responses` when custom types appear at API boundaries.

## Litestar References

- https://docs.litestar.dev/latest/usage/custom-types.html
