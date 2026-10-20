---
name: capstone-arch-loongarch
description: >-
  Guides Capstone LoongArch disassembly: LA32/LA64 modes, cs_loongarch
  REG/IMM/MEM detail, partial instruction aliases, and cs_regs_access gaps.
  Use when working with CS_ARCH_LOONGARCH, loongarch.h, LoongArchModule, or
  LoongArch Capstone options.
---

# Capstone LoongArch

Load only this skill for LoongArch work. Do not pull other architecture skills.

## Source of truth

Sibling Capstone tree (`capstone/`):

- `include/capstone/loongarch.h` — `cs_loongarch`
- `arch/LoongArch/LoongArchModule.c`
- `cs.c` — `CS_ARCH_CONFIG_LOONGARCH`
- `tests/details/loongarch.yaml`, `tests/MC/LoongArch/`, `tests/issues/`
- Alias status note: `docs/cs_v6_release_guide.md` (still marks partial)

## Valid modes

Allowed: `CS_MODE_LITTLE_ENDIAN` (0), `CS_MODE_LOONGARCH32`,
`CS_MODE_LOONGARCH64`. Big-endian rejected.

| Target | Mode |
|--------|------|
| LA32 | `CS_MODE_LOONGARCH32` |
| LA64 | `CS_MODE_LOONGARCH64` |

`Feature64Bit` is gated by `CS_MODE_LOONGARCH64`. Without it, LA64-only
encodings fail. Instructions are fixed **4** bytes.

`LoongArch_option`: `CS_OPT_MODE` **assigns** mode; `CS_OPT_SYNTAX` **ORs**.

## Options and detail

- Detail: `CS_OPT_DETAIL` / `CS_OPT_DETAIL_REAL`
- Union: `insn->detail->loongarch` (`format`, up to 8 ops)
- Ops: `REG`, `IMM`, `MEM` (`base`/`index`/`disp`) after post-decode rewrite
- Syntax: `CS_OPT_SYNTAX_NOREGNAME`, `CS_OPT_SYNTAX_NO_DOLLAR`
- Aliases: **partial** — `nop`/`move`/`ret`/`jr` (+ LA* assembler pseudos)
- `cs_regs_access`: **supported**, but `mem.index` is omitted from reads

## Workflow

1. Open with LA32 or LA64 (required for correct decode set).
2. Enable detail; expect MEM rewrite and PC-relative branch IMM → absolute.
3. For aliases like `ret`, use `CS_OPT_DETAIL_REAL` when analyzing real regs
   (default alias details may have empty operands).
4. Treat alias support as partial even though plumbing exists.

## Traps

- Wrong 32/64 mode drops LA64 encodings.
- Always LE; BE → `CS_ERR_MODE`.
- `cs_regs_access` under-reports indexed memory ops (`ldx`/`stx`/…).
- `docs/cs_v6_release_guide.md` still says LoongArch aliases are incomplete.

## More

- Modes, structs, traps: [reference.md](reference.md)
- Open/disasm snippets: [examples.md](examples.md)
