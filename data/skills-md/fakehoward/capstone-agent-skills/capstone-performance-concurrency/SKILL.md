---
name: capstone-performance-concurrency
description: >-
  Guides Capstone performance and concurrency limits for API 6 alpha: prefer
  cs_disasm_iter for hot loops, avoid CS_OPT_SYNTAX_CS_REG_ALIAS at scale, use
  one handle per thread, and treat CS_OPT_MEM hooks as process-global. Use when
  optimizing Capstone throughput, multi-threading disassembly, or installing
  custom allocators.
---

# Capstone performance and concurrency

Verified: iter notes in `capstone.h`, global `cs_mem_*` in `cs.c`,
`CS_REG_ALIAS` warning in `docs/cs_v6_release_guide.md`.

## Do not promise thread safety

Capstone does **not** document a thread-safe shared `csh`. Practical rules:

1. **One handle per thread** (or external mutex around all uses of a handle).
2. Do not share a `cs_insn` from `cs_malloc` across threads.
3. **`CS_OPT_MEM` hooks are process-global** (`cs_mem_malloc`, … statics).
   Install once at startup before concurrent `cs_open`/`cs_disasm`; never
   swap hooks while other threads call Capstone.
4. No claim of internal locking around option changes or decode.

## Throughput checklist

| Lever | Guidance |
| --- | --- |
| API | Prefer `cs_disasm_iter` + reused `cs_malloc` buffer for streaming/hot loops |
| Detail | Leave detail off when only mnemonic/`op_str` needed (new handle if detail was latched on) |
| Alias text patch | Avoid `CS_OPT_SYNTAX_CS_REG_ALIAS` at scale (string replace) |
| Skipdata | Enables progress through noise; callback cost is yours |
| Batch `count=0` | Can grow large allocations; bound `count` or use iter under memory pressure |

## Memory strategy

- Constrained environments: iter (header explicitly recommends over batch).
- Custom allocators: set `CS_OPT_MEM` once, early; keep them thread-safe if
  Capstone is used concurrently.
- Free promptly: `cs_free` for batch arrays; single `cs_free(insn, 1)` for iter.

## Configuration cost

- `CS_OPT_DETAIL` / `DETAIL_REAL` bits latch (`|=`) — plan handles by workload
  (detail vs non-detail) instead of toggling.
- Runtime `CS_OPT_MODE` may reconfigure arch state; avoid per-instruction mode
  thrash.

## Related

- Iter ordering: [../capstone-disasm-iteration/SKILL.md](../capstone-disasm-iteration/SKILL.md)
- Mem setup: [../capstone-core-api/SKILL.md](../capstone-core-api/SKILL.md)

## More

- [reference.md](reference.md)
- [examples.md](examples.md)
