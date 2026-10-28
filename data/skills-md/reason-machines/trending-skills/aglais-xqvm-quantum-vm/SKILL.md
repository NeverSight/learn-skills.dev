---
name: aglais-xqvm-quantum-vm
description: Expertise in Aglais XQVM, a hardware-agnostic Rust quantum virtual machine for QUBO/Ising binary optimization models targeting quantum annealers.
triggers:
  - quantum virtual machine rust
  - QUBO ising model bytecode
  - xqasm assembler quantum
  - quantum annealer optimization rust
  - aglais xqvm bytecode
  - binary optimization quantum vm
  - xqbc bytecode format
  - travelling salesman QUBO rust
---

# Aglais XQVM Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Aglais XQVM is a hardware-agnostic virtual machine for quantum computing written in Rust. It provides a unified bytecode intermediate representation for binary optimization problems (QUBO/Ising formulations) targeting quantum annealers — think LLVM for quantum computing. The VM is stack-based with a 256-slot register file, supports `no_std + alloc` for WASM/bare-metal deployment, and ships four crates: bytecode, assembler, disassembler, and interpreter.

## Installation & Setup

### Prerequisites

```sh
# Install Rust stable
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install dev tools (cargo-nextest, clippy, etc.)
make deps
```

### Build from source

```sh
git clone https://github.com/QuipNetwork/xq-rs
cd xq-rs
cargo build --release
# Binaries: target/release/xqasm, target/release/xqdism, target/release/xqvm
```

### Add as a library dependency

```toml
# Cargo.toml
[dependencies]
aglais-xqvm-bytecode = { path = "crates/bytecode" }
aglais-xqvm-vm       = { path = "crates/vm" }
```

For `no_std` environments (WASM, bare-metal):

```toml
[dependencies]
aglais-xqvm-bytecode = { path = "crates/bytecode", default-features = false, features = ["alloc"] }
```

## Workspace Crate Overview

| Crate | Binary | Role |
|---|---|---|
| `aglais-xqvm-bytecode` | — | Opcode table, instruction types, builder, binary codec, stream reader |
| `aglais-xqvm-asm` | `xqasm` | Text assembler: `.xqasm` → `.xqbc` bytecode |
| `aglais-xqvm-disasm` | `xqdism` | Bytecode → human-readable listing |
| `aglais-xqvm-vm` | `xqvm` | Bytecode interpreter: stack, registers, QUBO/Ising execution |

## CLI Commands

### `xqasm` — Assembler

```sh
# Assemble a source file to bytecode
xqasm program.xqasm -o program.xqbc

# Assemble with verbose output
xqasm program.xqasm -o program.xqbc --verbose
```

### `xqdism` — Disassembler

```sh
# Inspect bytecode encoding as human-readable listing
xqdism program.xqbc

# Pipe to file
xqdism program.xqbc > listing.txt
```

### `xqvm` — Interpreter

```sh
# Execute bytecode
xqvm program.xqbc

# Run with debug output (if supported)
xqvm program.xqbc --debug
```

### Full pipeline

```sh
xqasm problem.xqasm -o problem.xqbc && xqdism problem.xqbc && xqvm problem.xqbc
```

## XQASM Language Reference

The assembler accepts `.xqasm` text files. The VM is stack-based; most instructions pop operands from the stack and push results.

### Basic stack operations

```asm
; push two integers and add them
PUSH 10
PUSH 32
ADD
HALT
```

### Registers (0–255)

```asm
PUSH 42
STORE 0        ; pop stack → register 0
LOAD  0        ; push register 0 → stack
```

### Arithmetic

```asm
PUSH 10
PUSH 3
ADD            ; stack: [13]
PUSH 7
SUB            ; stack: [6]
PUSH 2
MUL            ; stack: [12]
PUSH 4
DIV            ; stack: [3]
```

### Vectors / integer arrays

```asm
; build a 3-element vector [1, 2, 3]
PUSH 1
PUSH 2
PUSH 3
PUSH 3         ; length
VEC            ; stack: [Vec([1,2,3])]
STORE 1
```

### QUBO / Ising model construction

```asm
; XQMX_NEW n creates an n-variable QUBO model
PUSH 4
XQMX_NEW       ; stack: [XqmxModel(4 vars)]
STORE 2

; set quadratic coupling Q[i][j] = weight
LOAD  2
PUSH  0        ; i
PUSH  1        ; j
PUSH  -1       ; weight (integer encoding)
XQMX_SET_Q    ; modifies model in reg 2

; set linear bias h[i] = weight
LOAD  2
PUSH  0
PUSH  5
XQMX_SET_H

; evaluate energy of a candidate solution
LOAD  2        ; model
PUSH  0        ; sample register (XqmxSample)
XQMX_EVAL     ; pushes energy onto stack
```

### Control flow & iteration

```asm
; RANGE lo hi → loop stack entry, ITER steps through it
PUSH 0
PUSH 5
RANGE          ; loop i in 0..5
ITER           ; advance; jumps past matching END_ITER when done
  LOAD 0
  PUSH 1
  ADD
  STORE 0
END_ITER

HALT
```

### Labels and jumps

```asm
  PUSH 0
loop:
  PUSH 1
  ADD
  DUP
  PUSH 10
  LT
  JMP_TRUE loop
HALT
```

## Rust API: Bytecode Builder

Use `aglais-xqvm-bytecode` to construct programs programmatically:

```rust
use aglais_xqvm_bytecode::{BytecodeBuilder, Instruction, Opcode};

fn build_add_program() -> Vec<u8> {
    let mut builder = BytecodeBuilder::new();

    builder.emit(Instruction::Push(10));
    builder.emit(Instruction::Push(32));
    builder.emit(Instruction::Add);
    builder.emit(Instruction::Halt);

    builder.finish()
}
```

### Decoding bytecode (stream reader)

```rust
use aglais_xqvm_bytecode::StreamReader;

fn decode(bytes: &[u8]) {
    let mut reader = StreamReader::new(bytes);
    while let Some(instr) = reader.next_instruction().unwrap() {
        println!("{:?}", instr);
    }
}
```

## Rust API: Running the VM

```rust
use aglais_xqvm_vm::Vm;

fn main() {
    // Load bytecode from a file
    let bytecode = std::fs::read("program.xqbc").expect("read bytecode");

    let mut vm = Vm::new();
    vm.load(&bytecode).expect("load");
    vm.run().expect("run");

    // Inspect top of stack after execution
    if let Some(val) = vm.stack_top() {
        println!("Result: {:?}", val);
    }
}
```

### Accessing registers after execution

```rust
use aglais_xqvm_vm::{Vm, Value};

fn run_and_inspect(bytecode: &[u8]) -> Value {
    let mut vm = Vm::new();
    vm.load(bytecode).unwrap();
    vm.run().unwrap();
    vm.register(0).cloned().unwrap_or(Value::Int(0))
}
```

## Real-World Pattern: TSP as QUBO

The `crates/vm/examples/tsp/` directory contains a complete Travelling Salesman Problem encoded as a QUBO driven by a Rust harness. The pattern is:

1. **Generate coefficients** in a Rust harness (problem-specific math).
2. **Emit `.xqasm`** files parameterised by those coefficients.
3. **Assemble + run** with `xqasm` / `xqvm`.

```rust
// crates/vm/examples/tsp/main.rs pattern
use std::process::Command;

fn assemble_and_run(src: &str, out: &str) {
    let asm = Command::new("xqasm")
        .args([src, "-o", out])
        .status()
        .expect("xqasm failed");
    assert!(asm.success());

    let run = Command::new("xqvm")
        .arg(out)
        .status()
        .expect("xqvm failed");
    assert!(run.success());
}

fn main() {
    assemble_and_run("init.xqasm",    "init.xqbc");
    assemble_and_run("problem.xqasm", "problem.xqbc");
    assemble_and_run("eval.xqasm",    "eval.xqbc");
}
```

## Common Patterns

### Pattern: build a QUBO model in assembly

```asm
; 2-variable QUBO: minimise x0 - x1 + 2*x0*x1
PUSH 2
XQMX_NEW
STORE 0

LOAD 0
PUSH 0
PUSH -1        ; h[0] = -1  (linear)
XQMX_SET_H

LOAD 0
PUSH 1
PUSH -1        ; h[1] = -1  (linear)
XQMX_SET_H

LOAD 0
PUSH 0
PUSH 1
PUSH 2         ; Q[0][1] = 2 (quadratic)
XQMX_SET_Q

HALT
```

### Pattern: iterate over model variables

```asm
PUSH 4
XQMX_NEW
STORE 0

PUSH 0
PUSH 4
RANGE
ITER
  ; register 1 holds current loop index after ITER
  LOAD  0
  LOAD  1      ; index i
  LOAD  1      ; index i (diagonal → linear term)
  PUSH  -1
  XQMX_SET_Q
END_ITER

HALT
```

### Pattern: no_std bytecode decoding (WASM)

```rust
#![no_std]
extern crate alloc;

use alloc::vec::Vec;
use aglais_xqvm_bytecode::StreamReader;

pub fn decode_instructions(bytes: &[u8]) -> Vec<alloc::string::String> {
    let mut reader = StreamReader::new(bytes);
    let mut out = Vec::new();
    while let Ok(Some(instr)) = reader.next_instruction() {
        out.push(alloc::format!("{:?}", instr));
    }
    out
}
```

## Development Workflow

```sh
# Run all lints and tests (mirrors CI)
make all

# Run only tests
cargo test --workspace

# Run lints
cargo clippy --workspace --all-targets -- -D warnings

# Format
cargo fmt --all

# Run a specific example
cargo run --example tsp --manifest-path crates/vm/Cargo.toml
```

## Instruction Set Quick Reference

The opcode table in `crates/bytecode/src/types/table.rs` is the single source of truth for all **76 instructions**. Key categories:

| Category | Instructions |
|---|---|
| Stack | `PUSH`, `POP`, `DUP`, `SWAP` |
| Registers | `LOAD`, `STORE` |
| Arithmetic | `ADD`, `SUB`, `MUL`, `DIV`, `NEG` |
| Comparison | `EQ`, `LT`, `GT`, `LE`, `GE` |
| Control flow | `JMP`, `JMP_TRUE`, `JMP_FALSE`, `CALL`, `RET`, `HALT` |
| Iteration | `RANGE`, `ITER`, `END_ITER` |
| Vectors | `VEC`, `VEC_GET`, `VEC_SET`, `VEC_LEN` |
| QUBO/Ising | `XQMX_NEW`, `XQMX_SET_Q`, `XQMX_SET_H`, `XQMX_EVAL`, `XQMX_SAMPLE` |

All operands are big-endian. The binary format is a bare instruction stream with no file header.

## Troubleshooting

### `xqasm: command not found`

Ensure `target/release` is on `$PATH` or use the full path:

```sh
export PATH="$PWD/target/release:$PATH"
```

### Stack underflow at runtime

The VM is strictly stack-based. Every instruction that pops values requires them to be present. Check that `PUSH` / `LOAD` precedes every operation, and that loops don't consume values without restoring the stack balance.

### `ITER` never terminates

`RANGE` pushes loop bounds onto the **loop stack** (separate from the value stack). Ensure every `RANGE` has a matching `END_ITER` and that the range bounds (`lo`, `hi`) are pushed in the correct order (`lo` first, `hi` second).

### Build fails in `no_std` environment

Disable default features and enable the `alloc` feature on `aglais-xqvm-bytecode`:

```toml
aglais-xqvm-bytecode = { ..., default-features = false, features = ["alloc"] }
```

The VM crate (`aglais-xqvm-vm`) requires `std` and is not suitable for bare-metal.

### Inspecting unexpected bytecode

Use `xqdism` to verify the assembler output before running:

```sh
xqasm suspect.xqasm -o suspect.xqbc
xqdism suspect.xqbc   # check instruction sequence and operand values
xqvm   suspect.xqbc
```

## License

AGPL-3.0-or-later. Embedding in proprietary network services requires source disclosure under the AGPL.
