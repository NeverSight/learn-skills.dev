---
name: capstone-disasm-iteration
description: >-
  Chooses between Capstone batch cs_disasm and iterative cs_disasm_iter,
  including cs_malloc/cs_free ordering with CS_OPT_DETAIL. Use when writing
  disassembly loops, comparing batch vs iter, allocating insn caches, or
  tuning Capstone decode paths on API 6 alpha.
---

# Capstone disasm: batch vs iter

Verified in `cs.c` (`cs_disasm`, `cs_malloc`, `cs_disasm_iter`) and
`tests/integration/test_iter.c`.

## Choose API

| Need | API |
| --- | --- |
| Decode N insns into a fresh array; simple ownership | `cs_disasm` + `cs_free(insns, count)` |
| Streaming / scarce memory / hot loop reusing one insn | `cs_malloc` + `cs_disasm_iter` + `cs_free(insn, 1)` |
| Stop at first invalid byte (no skipdata) | Either; both stop when decode fails |

Header notes: iter can be ~30% faster on random input vs `cs_disasm(count=1)`.

## Batch rules (`cs_disasm`)

1. On success, `*insn` is allocated; free with `cs_free(insn, count)` where
   `count` is the returned size.
2. Return `0` means failure or empty; check `cs_errno`.
3. `count == 0` means decode until buffer end or break (invalid / skipdata stop).
4. Detail buffers are allocated per insn when `handle->detail_opt` is non-zero.

## Iter rules (`cs_disasm_iter`)

1. **Order:** set `CS_OPT_DETAIL` (if needed) **before** `cs_malloc`.
   `cs_malloc` allocates `insn->detail` only when `detail_opt` is already set.
2. Pass pointers: `const uint8_t **code`, `size_t *size`, `uint64_t *address`.
   Success advances all three.
3. Return `false` on failure / end; for skipdata behavior see skipdata skill.
4. Reuse the same `cs_insn *` across iterations; do not free per step.
5. Free once: `cs_free(insn, 1)`.

## Detail coupling (critical)

```c
cs_option(handle, CS_OPT_DETAIL, CS_OPT_ON);          /* first */
cs_insn *insn = cs_malloc(handle);                    /* after DETAIL */
while (cs_disasm_iter(handle, &code, &size, &address, insn)) {
    /* use insn */
}
cs_free(insn, 1);
```

If you `cs_malloc` first and enable detail later, `insn->detail` stays NULL
even though detail mode is on — detail APIs then fail with `CS_ERR_DETAIL`.

## Related

- Detail/alias options: [../capstone-detail-aliases/SKILL.md](../capstone-detail-aliases/SKILL.md)
- Skipdata callback offsets differ batch vs iter: [../capstone-skipdata/SKILL.md](../capstone-skipdata/SKILL.md)

## More

- [reference.md](reference.md)
- [examples.md](examples.md)
