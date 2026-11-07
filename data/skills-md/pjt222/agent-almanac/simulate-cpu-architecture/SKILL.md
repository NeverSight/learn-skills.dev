---
name: simulate-cpu-architecture
description: >
  Design and simulate a minimal CPU from scratch: define an instruction set
  architecture (ISA), build the datapath (ALU, register file, program counter,
  memory interface), design the control unit (hardwired or microprogrammed),
  implement the fetch-decode-execute cycle, and verify by tracing a small
  program clock cycle by clock cycle. The capstone "computer inside a computer"
  exercise that composes combinational and sequential building blocks into a
  complete processor.
license: MIT
allowed-tools: Read Grep Glob WebFetch WebSearch
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: digital-logic
  complexity: advanced
  language: multi
  tags: digital-logic, cpu-architecture, instruction-set, datapath, fetch-decode-execute
---

# Simulate CPU Architecture

Design a minimal but complete CPU by defining an instruction set architecture, composing an ALU and register file into a datapath, designing a control unit that generates the correct signals for each instruction phase, implementing the fetch-decode-execute cycle, simulating a small program to completion, and verifying every clock cycle against expected register and memory state.

## When to Use

- Learning or teaching computer architecture from first principles
- Designing a custom processor for an FPGA or educational simulator
- Verifying understanding of how instructions execute at the gate and register-transfer level
- Building a software simulation (Python, JavaScript, or structured walkthrough) of a CPU
- Composing the combinational blocks from design-logic-circuit and the sequential blocks from build-sequential-circuit into a working system

## Inputs

- **Required**: Processor complexity target -- 4-bit, 8-bit, or 16-bit data width; number of general-purpose registers (2-16)
- **Required**: Minimum instruction set -- at least: load, store, add, subtract, bitwise AND/OR, branch, halt
- **Optional**: Addressing modes beyond direct (immediate, register-indirect, indexed)
- **Optional**: Additional instructions (multiply, shift, compare, jump-and-link for subroutines)
- **Optional**: Memory size and word size
- **Optional**: Pipeline stages (single-cycle, multi-cycle, or pipelined) -- default is multi-cycle
- **Optional**: Implementation medium -- software simulation (Python/JS), HDL (Verilog/VHDL), or paper walkthrough

## Procedure

### Step 1: Define the Instruction Set Architecture

Specify everything a programmer needs to know to write machine code for this CPU:

1. **Data width**: Choose the bit width for data (ALU operand size) and addresses. Common choices: 8-bit data / 8-bit address (256 bytes addressable), 16-bit data / 16-bit address.
2. **Register file**: Define the number of general-purpose registers and any special-purpose registers.
   - **General-purpose**: R0-R(N-1). Decide if R0 is hardwired to zero (simplifies instruction encoding).
   - **Special-purpose**: Program Counter (PC), Instruction Register (IR), Status/Flags register (Zero, Carry, Negative, Overflow).
3. **Instruction format**: Design a fixed-width instruction word. Divide the bits into fields:
   - **Opcode**: Identifies the operation. With K bits, support up to 2^K instructions.
   - **Register fields**: Source and destination register addresses. With N registers, each field needs ceil(log2(N)) bits.
   - **Immediate/offset field**: For constants or branch offsets. Use remaining bits.
4. **Instruction catalog**: Define each instruction with its mnemonic, opcode encoding, operand fields, operation (in RTL notation), and affected flags.
5. **Addressing modes**: Define how operands are located.
   - **Register**: Operand is in a register.
   - **Immediate**: Operand is embedded in the instruction.
   - **Direct**: Operand address is in the instruction.
   - **Register-indirect**: Operand address is in a register.

```markdown
## ISA Specification
- **Data width**: [N] bits
- **Address width**: [M] bits
- **Registers**: [count] general-purpose + [list of special-purpose]
- **Instruction width**: [W] bits

### Instruction Format
| Field    | Bits      | Width |
|----------|-----------|-------|
| Opcode   | [W-1:X]  | [n]   |
| Rd       | [X-1:Y]  | [n]   |
| Rs       | [Y-1:Z]  | [n]   |
| Imm      | [Z-1:0]  | [n]   |

### Instruction Catalog
| Mnemonic | Opcode | Format    | RTL Operation          | Flags |
|----------|--------|-----------|------------------------|-------|
| LOAD     | 0000   | Rd, [addr]| Rd <- MEM[addr]       | -     |
| STORE    | 0001   | Rs, [addr]| MEM[addr] <- Rs       | -     |
| ADD      | 0010   | Rd, Rs    | Rd <- Rd + Rs         | Z,C,N |
| ...      | ...    | ...       | ...                    | ...   |
| HALT     | 1111   | -         | Stop execution         | -     |
```

**Expected:** A complete ISA specification where every instruction has a unique opcode, well-defined operand fields, an unambiguous RTL description, and documented flag effects. The instruction encoding must be decodable without ambiguity.

**On failure:** If the instruction word is too narrow to encode all needed fields, either widen the instruction, reduce the register count, use variable-length instructions (more complex decoding), or split instructions into sub-operations. If opcodes collide, reassign the encoding.

### Step 2: Design the Datapath

Build the register-transfer level hardware that moves and transforms data:

1. **ALU**: Design using the design-logic-circuit skill. The ALU takes two N-bit operands and an operation select signal, and produces an N-bit result plus flag outputs (Zero, Carry, Negative, Overflow).
   - Operations: ADD, SUB (via 2's complement add), AND, OR, XOR, NOT, SHIFT LEFT, SHIFT RIGHT, PASS-THROUGH (for moves and loads).
   - The ALU select width must accommodate all required operations.
2. **Register file**: Design using build-sequential-circuit. A bank of registers with:
   - Two read ports (source A, source B) -- combinational read with register address as input.
   - One write port (destination) -- clocked write enabled by a RegWrite control signal.
   - If R0 is hardwired to zero, override writes to R0.
3. **Program Counter (PC)**: An N-bit register with:
   - Increment logic (PC + instruction_width/8 for the next sequential instruction).
   - Load input for branch/jump targets.
   - Multiplexer selecting between increment and branch target, controlled by a PCsrc signal.
4. **Memory interface**: Separate or unified instruction and data memory.
   - **Harvard architecture**: Separate instruction memory (read-only during execution) and data memory (read-write). Simpler, allows simultaneous fetch and data access.
   - **Von Neumann architecture**: Single shared memory for instructions and data. Requires sequencing fetch and data access in different cycles.
5. **Interconnect**: Multiplexers and buses connecting the components:
   - ALU input A mux: register read port A or PC (for PC-relative addressing).
   - ALU input B mux: register read port B or sign-extended immediate.
   - Register write data mux: ALU result or memory read data (for loads).
   - Memory address mux: PC (for instruction fetch) or ALU result (for load/store).

```markdown
## Datapath Components
| Component       | Width  | Ports / Signals                    |
|----------------|--------|------------------------------------|
| ALU            | [N]-bit| OpA, OpB, ALUop -> Result, Flags  |
| Register File  | [N]-bit| RdAddrA, RdAddrB, WrAddr, WrData, RegWrite -> RdDataA, RdDataB |
| PC             | [M]-bit| PCnext, PCwrite -> PCout           |
| Instruction Mem| [W]-bit| Addr -> Instruction                |
| Data Memory    | [N]-bit| Addr, WrData, MemRead, MemWrite -> RdData |

## Datapath Multiplexers
| Mux Name     | Inputs               | Select Signal | Output      |
|-------------|----------------------|---------------|-------------|
| ALU_B_mux   | RegDataB, Immediate  | ALUsrc        | ALU OpB     |
| WrData_mux  | ALU Result, MemData  | MemToReg      | Reg WrData  |
| PC_mux      | PC+1, BranchTarget   | PCsrc         | PC next     |
```

**Expected:** A complete datapath diagram (as a component table and mux table) where every instruction in the ISA has a viable path for its data to flow from source to destination through the ALU, register file, and memory.

**On failure:** If an instruction cannot be executed with the current datapath (e.g., no path from memory to a register for LOAD), add the missing multiplexer or data path. Walk through each instruction's RTL operation and trace the required signal flow through the datapath.

### Step 3: Design the Control Unit

Build the logic that orchestrates the datapath for each instruction:

1. **Identify control signals**: List every multiplexer select, register write enable, memory read/write enable, and ALU operation select signal in the datapath.
2. **Single-cycle control** (simplest): A purely combinational control unit that derives all control signals from the opcode field of the current instruction in one clock cycle.
3. **Multi-cycle control** (recommended for learning): A finite state machine (designed using build-sequential-circuit) that breaks each instruction into phases:
   - **Fetch**: Read instruction from memory at PC address; store in IR; increment PC.
   - **Decode**: Read register file using fields from IR; sign-extend the immediate field.
   - **Execute**: Perform the ALU operation or compute the memory address.
   - **Memory access** (load/store only): Read from or write to data memory.
   - **Write-back**: Write the result to the destination register.
4. **Control signal table**: For each instruction and each phase, specify the value of every control signal.
5. **Hardwired vs. microprogrammed**:
   - **Hardwired**: The control FSM is built from gates and flip-flops. Faster, less flexible.
   - **Microprogrammed**: A microinstruction ROM stores the control signals for each state. Each microinstruction contains the control signal values plus a next-state field. Slower, but easy to modify.

```markdown
## Control Signals
| Signal     | Width | Function                              |
|-----------|-------|---------------------------------------|
| ALUop     | [k]   | Selects ALU operation                 |
| ALUsrc    | 1     | 0=register, 1=immediate for ALU B    |
| RegWrite  | 1     | Enable register file write            |
| MemRead   | 1     | Enable data memory read               |
| MemWrite  | 1     | Enable data memory write              |
| MemToReg  | 1     | 0=ALU result, 1=memory data to register |
| PCsrc     | 1     | 0=PC+1, 1=branch target              |
| IRwrite   | 1     | Enable instruction register load      |

## Multi-Cycle Control FSM
| State   | Active Signals                          | Next State         |
|---------|----------------------------------------|-------------------|
| FETCH   | MemRead, IRwrite, PC <- PC+1           | DECODE             |
| DECODE  | Read registers, sign-extend immediate   | EXECUTE            |
| EXECUTE | ALUop=[per instruction], ALUsrc=[...]  | MEM_ACCESS or WB   |
| MEM_ACC | MemRead or MemWrite                    | WRITE_BACK         |
| WB      | RegWrite, MemToReg=[...]               | FETCH              |
```

**Expected:** A control unit (combinational or FSM) that generates the correct control signal values for every instruction at every phase, with no conflicting signals (e.g., MemRead and MemWrite both active simultaneously on the same memory).

**On failure:** If a control signal conflict exists, the phases are not properly separated. Ensure that load and store instructions access memory in different phases or that the memory interface supports simultaneous read and write on separate ports. If the FSM has too many states, check whether some instructions share phases and can be merged.

### Step 4: Implement the Fetch-Decode-Execute Cycle

Connect the datapath and control unit into a working processor:

1. **Clock distribution**: Connect the system clock to all flip-flops (PC, IR, register file, control FSM state register). All state updates happen on the same clock edge.
2. **Phase sequencing**: Wire the control FSM outputs to the datapath control signals. The FSM advances one state per clock cycle, driving the datapath through Fetch -> Decode -> Execute -> Memory -> Write-back.
3. **Instruction fetch**: In the FETCH phase, the PC drives the instruction memory address bus. The fetched instruction loads into IR. The PC increments by one instruction width.
4. **Instruction decode**: In the DECODE phase, the opcode field of IR drives the control unit to determine the instruction type. Register addresses from IR drive the register file read ports.
5. **Execute and beyond**: The remaining phases depend on the instruction type:
   - **ALU instructions**: Execute (ALU computes), Write-back (result to register).
   - **Load**: Execute (ALU computes address), Memory (read data memory), Write-back (data to register).
   - **Store**: Execute (ALU computes address), Memory (write data memory).
   - **Branch**: Execute (ALU compares or checks flags), conditionally update PC.
   - **Halt**: FSM enters a terminal state and stops advancing.
6. **Interrupt and exception handling** (optional): Add a mechanism to save PC and jump to a handler address. This requires additional control states and a cause register.

```markdown
## Cycle Execution Summary
| Instruction Type | Phases                          | Cycles |
|-----------------|--------------------------------|--------|
| ALU (reg-reg)   | Fetch, Decode, Execute, WB     | 4      |
| Load            | Fetch, Decode, Execute, Mem, WB| 5      |
| Store           | Fetch, Decode, Execute, Mem    | 4      |
| Branch (taken)  | Fetch, Decode, Execute         | 3      |
| Branch (not taken)| Fetch, Decode, Execute       | 3      |
| Halt            | Fetch, Decode                  | 2      |
```

**Expected:** A fully connected processor where the control FSM drives the datapath through the correct sequence of phases for each instruction type, and all state transitions occur synchronously on the clock edge.

**On failure:** If the processor hangs (never reaches HALT) or produces incorrect results, the most likely cause is a control signal error in one specific phase. Use Step 5's cycle-by-cycle trace to isolate the failing cycle. If the PC does not increment correctly, check the FETCH phase wiring. If the wrong register is written, check the register address field extraction from IR.

### Step 5: Simulate a Small Program and Verify

Execute a concrete program and verify every clock cycle against expected state:

1. **Write a test program**: Choose a program small enough to trace completely (5-15 instructions) but complex enough to exercise multiple instruction types. Fibonacci sequence computation is ideal: it uses load-immediate, add, branch, and halt.
2. **Initialize state**: Set all registers to 0. Load the program into instruction memory starting at address 0. Set PC = 0. Set the control FSM to the FETCH state.
3. **Cycle-by-cycle trace**: For each clock cycle, record:
   - Control FSM state and phase name
   - PC value and instruction being fetched/executed
   - ALU inputs, operation, and result
   - Register file reads and writes
   - Memory reads and writes
   - Flag register values
   - All control signal values
4. **Verify against hand computation**: Independently compute the expected register and memory state after each instruction completes (not each cycle -- each instruction takes multiple cycles). Compare the simulation trace against these expected snapshots.
5. **Edge cases**: Verify behavior for:
   - Branch not taken (PC increments normally)
   - Branch taken (PC loads branch target)
   - Load followed immediately by use of loaded register (checks if write-back completes before next decode reads)
   - Writing to R0 if hardwired to zero (write should have no effect)
   - HALT instruction (processor stops cleanly)

```markdown
## Test Program: Fibonacci (first 8 terms)
| Addr | Instruction    | Mnemonic         | Comment              |
|------|---------------|------------------|----------------------|
| 0x00 | [encoding]    | LOAD R1, #1      | R1 = 1 (F1)         |
| 0x01 | [encoding]    | LOAD R2, #1      | R2 = 1 (F2)         |
| 0x02 | [encoding]    | LOAD R3, #6      | R3 = 6 (loop count) |
| 0x03 | [encoding]    | ADD R4, R1, R2   | R4 = R1 + R2        |
| 0x04 | [encoding]    | MOV R1, R2       | R1 = R2              |
| 0x05 | [encoding]    | MOV R2, R4       | R2 = R4              |
| 0x06 | [encoding]    | SUB R3, R3, #1   | R3 = R3 - 1         |
| 0x07 | [encoding]    | BNZ 0x03         | Branch if R3 != 0   |
| 0x08 | [encoding]    | HALT             | Stop                 |

## Cycle-by-Cycle Trace (excerpt)
| Cycle | Phase   | PC  | IR       | ALU Op   | Result | RegWrite | Flags |
|-------|---------|-----|----------|----------|--------|----------|-------|
| 1     | FETCH   | 0x00| LOAD R1,1| -        | -      | No       | -     |
| 2     | DECODE  | 0x01| LOAD R1,1| -        | -      | No       | -     |
| 3     | EXECUTE | 0x01| LOAD R1,1| PASS #1  | 1      | No       | -     |
| 4     | WB      | 0x01| LOAD R1,1| -        | -      | R1 <- 1  | -     |
| ...   | ...     | ... | ...      | ...      | ...    | ...      | ...   |

## Expected Final State
| Register | Value | Description         |
|----------|-------|---------------------|
| R1       | [val] | Second-to-last Fib  |
| R2       | [val] | Last computed Fib   |
| R3       | 0     | Loop counter done   |
| R4       | [val] | Same as R2          |
| PC       | 0x09  | One past HALT       |
```

**Expected:** The cycle-by-cycle trace matches the expected final state. Every instruction produces the correct register and memory updates. The program terminates at HALT with the correct Fibonacci values in registers.

**On failure:** Compare the first divergence between expected and actual state. Common causes: (1) ALU operation select is wrong for one instruction type -- check the control signal table. (2) Branch offset calculation is off by one -- verify whether branches are PC-relative from the current or next instruction address. (3) Write-back writes to the wrong register -- check the register address field extraction. (4) Flags not updated correctly -- trace the ALU flag logic for the specific operands that cause the mismatch.

## Validation

- [ ] ISA has at least load, store, add, subtract, AND, OR, branch, and halt instructions
- [ ] Every instruction has a unique opcode and unambiguous encoding
- [ ] Datapath provides a valid signal path for every instruction's RTL operation
- [ ] ALU supports all required operations with correct flag generation
- [ ] Register file has sufficient read and write ports for the instruction format
- [ ] Control unit generates correct signals for every instruction at every phase
- [ ] No control signal conflicts (e.g., simultaneous read and write to the same memory port)
- [ ] Fetch-decode-execute cycle is fully connected and clocked
- [ ] Test program executes to completion with correct final state
- [ ] Cycle-by-cycle trace is verified against hand computation
- [ ] Branch taken and not-taken cases are both verified
- [ ] HALT instruction stops execution cleanly

## Common Pitfalls

- **Branch offset off-by-one**: Branches may be relative to the current PC, PC+1, or the instruction after the branch. Define the convention in the ISA and implement it consistently. Off-by-one errors in branch targets are the single most common CPU design bug.
- **Write-back/decode hazard in multi-cycle**: If instruction I writes a register in its write-back phase at the same time instruction I+1 reads that register in its decode phase, the read may get the old value. In a multi-cycle CPU (one instruction at a time), this is not an issue. In a pipelined CPU, this requires forwarding or stalling.
- **Forgetting to increment PC during fetch**: If PC is not incremented in the FETCH phase, the CPU will execute the same instruction forever. This is a trivially common wiring error.
- **ALU flags latching**: Flags should update only on ALU instructions, not on loads, stores, or branches. If flags update unconditionally, a load between a compare and a branch will corrupt the comparison result.
- **Unsigned vs. signed confusion**: Decide at ISA definition time whether arithmetic is signed (2's complement) or unsigned, and implement the ALU and flag logic accordingly. The Carry flag has different semantics for signed vs. unsigned operations.
- **Memory alignment**: If the data width and instruction width differ, or if instructions are multi-byte, define alignment rules. A 16-bit instruction in byte-addressable memory occupies two addresses; the PC must increment by 2, not 1.
- **Overcomplicating the first design**: Start with the simplest possible CPU (8-bit, 4 registers, 8 instructions, single-cycle or multi-cycle, no pipeline). Complexity can always be added later; a working simple design teaches more than a broken complex one.

## Related Skills

- `design-logic-circuit` -- design the ALU, multiplexers, decoders, and other combinational blocks
- `build-sequential-circuit` -- design the register file, program counter, control FSM, and other sequential blocks
- `evaluate-boolean-expression` -- simplify the control logic equations for the hardwired control unit
- `derive-theoretical-result` -- formalize performance analysis (CPI, throughput, Amdahl's law)
