---
name: capstone-detail-aliases
description: >-
  Explains Capstone CS_OPT_DETAIL, CS_OPT_DETAIL_REAL, is_alias, alias_id, and
  usesAliasDetails on API 6 alpha. Use when enabling instruction detail, choosing
  alias versus real operands, debugging detail that will not turn off, or
  handling Capstone instruction aliases.
---

# Capstone detail and aliases

Verified: `cs_option` `CS_OPT_DETAIL` in `cs.c`, `map_use_alias_details` in
`Mapping.c`, fields in `capstone.h`, guide in `docs/cs_v6_release_guide.md`.

## Enable detail

```c
cs_option(handle, CS_OPT_DETAIL, CS_OPT_ON);
/* real operand/detail set even for aliases: */
cs_option(handle, CS_OPT_DETAIL, CS_OPT_DETAIL_REAL | CS_OPT_ON);
```

## Critical: detail cannot be turned OFF with `CS_OPT_OFF`

Implementation:

```c
case CS_OPT_DETAIL:
    handle->detail_opt |= (cs_opt_value)value;
```

- `CS_OPT_OFF` is `0`; `|= 0` is a no-op.
- Once `CS_OPT_ON` and/or `CS_OPT_DETAIL_REAL` bits latch, they stay set for
  the handle lifetime.
- To run without detail, open a new handle (or never enable detail).
- Docs/comments that say detail defaults OFF and can be toggled OFF describe
  intent; **current code does not clear bits**.

## Alias vs real details

`map_use_alias_details()` is true when:

- `(detail_opt & CS_OPT_ON)` and
- `!(detail_opt & CS_OPT_DETAIL_REAL)`

| Setting | Operand/detail set for alias insn |
| --- | --- |
| `CS_OPT_ON` only | Alias operand set when `is_alias` (default) |
| `CS_OPT_ON \| CS_OPT_DETAIL_REAL` | Real instruction operand set |

Insn fields (always in `cs_insn`, not only in `cs_detail`):

| Field | Role |
| --- | --- |
| `id` | Real instruction id |
| `alias_id` | Alias id when applicable (auto-sync archs) |
| `is_alias` | Decoded form is an alias |
| `usesAliasDetails` | Detail operands follow alias (true) or real (false) |
| `illegal` | Valid decode but illegal by ISA rules |

`cs_insn_name(handle, id)` / `cs_insn_name(handle, alias_id)` resolve names.

## Partial alias support (v6 guide)

- SystemZ: not enabled by default in LLVM (planned later).
- LoongArch: implemented but not fully handled yet.
- TriCore: no LLVM alias support.

Some LLVM “aliases” still appear in real enums; they should not decode as
non-alias. Treat unexpected cases as upstream issues.

## Detail pointer validity

`insn->detail` is meaningful only when detail is on **and** the insn is not a
skipdata data record (`id == 0` → detail forced NULL in batch path).

## Related

- Iter + malloc order: [../capstone-disasm-iteration/SKILL.md](../capstone-disasm-iteration/SKILL.md)
- Printed alias text syntax flags: [../capstone-options-syntax/SKILL.md](../capstone-options-syntax/SKILL.md)

## More

- [reference.md](reference.md)
- [examples.md](examples.md)
