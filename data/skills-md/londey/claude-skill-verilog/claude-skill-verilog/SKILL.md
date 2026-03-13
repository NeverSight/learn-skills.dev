---
name: claude-skill-verilog
description: Verilog/SystemVerilog coding style and Verilator workflow guidance
---

# Verilog/SystemVerilog Guidance

Apply when working with `.v`, `.sv`, `.vh`, `.svh` files or running Verilator.

## Documentation

All modules, wires, and registers require comments:

```systemverilog
// Module: counter
// Purpose: Simple up-counter with synchronous reset
module counter #(
    parameter WIDTH = 8  // Counter bit width
) (
    input  logic             clk,      // System clock
    input  logic             rst_n,    // Active-low reset
    output logic [WIDTH-1:0] count     // Current count value
);
```

## Fixed-Point Notation

Document all fixed-point values using TI-style Q notation:
- `Qm.n` — signed: m integer bits (including sign bit), n fractional bits, total width = m + n bits.
- `UQm.n` — unsigned: m integer bits, n fractional bits, total width = m + n bits.

Use Q notation in signal comments, localparam descriptions, and module-level documentation.

```systemverilog
logic signed [15:0] attr_val;      // Interpolated attribute, Q4.12
logic        [15:0] depth;         // Fragment depth, UQ16.0
logic signed [15:0] deriv_dx;      // dAttr/dx per scanline step, Q4.12
```

## Naming Conventions

- Active-low signals: use `_n` suffix (e.g., `rst_n`, `chip_select_n`)
- Clocks: `clk` or `clk_<domain>`
- Use descriptive names over abbreviations

## always_ff: Simple Assignments Only

`always_ff` blocks must contain ONLY simple non-blocking assignments. No logic, no expressions - this ensures Verilator simulation matches synthesized behavior. (Exceptions: memory inference and async reset synchronizers require conditional logic - see those sections.)

```systemverilog
// CORRECT - simple assignment
always_ff @(posedge clk) begin
    count <= count_next;
    state <= state_next;
end

// WRONG - logic in always_ff
always_ff @(posedge clk) begin
    count <= count + 1;           // Move to always_comb
    state <= enable ? RUNNING : IDLE;  // Move to always_comb
end
```

## always_comb: All Logic Here

All combinational logic belongs in `always_comb` blocks:

```systemverilog
always_comb begin
    count_next = count + 8'd1;
    state_next = enable ? RUNNING : IDLE;
end
```

## Formatting

- One statement per line — never chain multiple statements or assignments on a single line
- One declaration per line
- Explicit bit widths on all literals
- Start files with `` `default_nettype none ``
- Always use `begin`/`end` blocks for `if`, `else`, `case` items (prevents bugs when adding code later)
- Prefer to keep modules under ~500 lines; if a module grows significantly larger, consider refactoring into smaller sub-modules

```systemverilog
`default_nettype none

module example (
    input  logic        clk,
    input  logic        rst_n,
    input  logic [7:0]  data_in,
    output logic [7:0]  data_out
);

    logic [7:0] data_reg;    // Registered data
    logic [7:0] data_next;   // Next state value
    logic       valid;       // Data valid flag

    localparam logic [7:0] INIT_VAL = 8'd0;

endmodule

`default_nettype wire
```

## Yosys Synthesis Compatibility (DD-034)

All synthesizable RTL must work with both **Verilator** (lint/simulation) and **Yosys** (ECP5 synthesis).
Yosys supports a subset of SystemVerilog via `read_verilog -sv`.
Code that passes Verilator may still fail Yosys synthesis.

**Constructs to avoid in synthesizable RTL:**

| Avoid | Use instead |
|-------|-------------|
| `return <expr>;` in functions | `function_name = <expr>;` (Verilog-2005 style) |
| `interface` / `modport` | Explicit port lists |
| `unique case` / `priority case` | Plain `case` with `default` |
| Multi-dimensional packed arrays in ports | Flatten to single vectors |

```systemverilog
// CORRECT - Yosys-compatible function
function automatic logic [7:0] add_saturate(input logic [7:0] a, input logic [7:0] b);
    logic [8:0] sum;
    sum = {1'b0, a} + {1'b0, b};
    add_saturate = sum[8] ? 8'hFF : sum[7:0];
endfunction

// WRONG - return statement (Yosys rejects this)
function automatic logic [7:0] add_saturate(input logic [7:0] a, input logic [7:0] b);
    logic [8:0] sum;
    sum = {1'b0, a} + {1'b0, b};
    return sum[8] ? 8'hFF : sum[7:0];
endfunction
```

Always verify with `make synth` (not just `verilator --lint-only`) when using SystemVerilog features.

## Testing with Verilator

Every module requires a testbench. Build and run with Verilator:

```bash
# Build testbench
verilator --binary -Wall module_tb.sv module.sv

# Run simulation
./obj_dir/Vmodule_tb
```

Testbench structure:

```systemverilog
module counter_tb;
    logic       clk = 1'b0;  // System clock
    logic       rst_n;       // Active-low reset
    logic [7:0] count;       // DUT output

    counter dut (
        .clk(clk),
        .rst_n(rst_n),
        .count(count)
    );

    always begin
        #5 clk = ~clk;
    end

    initial begin
        rst_n = 1'b0;
        #20 rst_n = 1'b1;
        #100;
        $display("Test complete, count=%d", count);
        $finish;
    end
endmodule
```

## Verilator Linting

Run linting on all files and fix all warnings:

```bash
verilator --lint-only -Wall module.sv
```

- Fix all warnings - do not suppress with pragmas
- Key warnings: WIDTH (bit-width mismatch), UNUSED, UNDRIVEN

## Verilator Simulation Flags

Recommended flags for simulation builds:

```bash
verilator --binary \
    -Wall \
    -Wno-fatal \
    -j 0 \
    --assert \
    --timing \
    --trace-fst \
    --trace-structs \
    --main-top-name "-" \
    --x-assign unique \
    --x-initial unique \
    module_tb.sv module.sv
```

| Flag | Purpose |
| ---- | ------- |
| `-Wall` | Enable all warnings |
| `-Wno-fatal` | Don't exit on warnings (allows full report) |
| `-j 0` | Fully parallelized compilation |
| `--assert` | Enable SystemVerilog assertions |
| `--timing` | Enable timing constructs |
| `--trace-fst` | Dump waveforms as FST (compressed) |
| `--trace-structs` | Human-readable struct dumps |
| `--main-top-name "-"` | Remove extra TOP module wrapper |
| `--x-assign unique` | Replace X with random constant per-build |
| `--x-initial unique` | Randomly initialize uninitialized variables |

## Module Instantiation

- One module per file, filename matches module name
- Always use named port connections (never positional)

```systemverilog
// CORRECT - named connections
counter #(
    .WIDTH(16)
) u_counter (
    .clk    (clk),
    .rst_n  (rst_n),
    .count  (count_value)
);

// WRONG - positional connections
counter u_counter (clk, rst_n, count_value);
```

## Avoiding Latches

Latches are inferred when signals aren't assigned in all paths. Prevent with:

- Default assignments at start of `always_comb`
- Cover all cases including `default`

```systemverilog
always_comb begin
    // Default assignments first
    data_next = data_reg;
    valid_next = 1'b0;

    case (state)
        IDLE: begin
            data_next = 8'd0;
        end
        LOAD: begin
            data_next = data_in;
        end
        default: begin
            data_next = data_reg;
        end
    endcase
end
```

## Reset Handling

Use synchronous resets when possible. For external async resets, synchronize first.

**Note:** Async reset synchronizers require conditional logic in `always_ff` for the reset condition - this is a necessary exception similar to memory inference.

```systemverilog
// Synchronous reset (preferred)
logic [7:0] count;       // Counter register
logic [7:0] count_next;  // Next counter value

always_comb begin
    count_next = rst_n ? (count + 8'd1) : 8'd0;
end

always_ff @(posedge clk) begin
    count <= count_next;
end

// Reset synchronizer for external async reset
logic [1:0] rst_sync;       // Synchronizer flip-flops
logic [1:0] rst_sync_next;  // Next synchronizer value

always_comb begin
    rst_sync_next = {rst_sync[0], 1'b1};
end

always_ff @(posedge clk or negedge rst_async_n) begin
    if (!rst_async_n) begin
        rst_sync <= 2'b00;
    end else begin
        rst_sync <= rst_sync_next;
    end
end
assign rst_n = rst_sync[1];
```

## FSM Patterns

Separate state register from next-state logic. Use enums for state encoding.

```systemverilog
typedef enum logic [1:0] {
    IDLE,
    RUN,
    DONE
} state_t;

state_t state;       // Current state register
state_t state_next;  // Next state value

// Next-state logic (combinational)
always_comb begin
    state_next = state;
    case (state)
        IDLE: begin
            if (start) begin
                state_next = RUN;
            end
        end
        RUN: begin
            if (finish) begin
                state_next = DONE;
            end
        end
        DONE: begin
            state_next = IDLE;
        end
        default: begin
            state_next = IDLE;
        end
    endcase
end

// State register (sequential)
always_ff @(posedge clk) begin
    state <= state_next;
end
```

## Clock Domain Crossing (CDC)

Single-bit signals: use 2-FF synchronizer. Multi-bit: use gray coding or handshake.

```systemverilog
// 2-FF synchronizer for single-bit CDC
logic [1:0] sync_reg;       // Synchronizer flip-flops
logic [1:0] sync_reg_next;  // Next synchronizer value
logic       signal_sync;    // Synchronized output

always_comb begin
    sync_reg_next = {sync_reg[0], signal_src};
end

always_ff @(posedge clk_dst) begin
    sync_reg <= sync_reg_next;
end
assign signal_sync = sync_reg[1];

// Gray code for multi-bit counters crossing domains
function automatic logic [WIDTH-1:0] bin2gray(input logic [WIDTH-1:0] bin);
    bin2gray = bin ^ (bin >> 1);
endfunction
```

## Memory Inference

Use standard patterns for RAM/ROM inference by synthesis tools.

**Note:** Memory patterns are an exception to the "simple assignments only" rule for `always_ff`. Synthesis tools require these specific patterns to correctly infer RAM/ROM primitives.

```systemverilog
// Single-port RAM
logic [DATA_WIDTH-1:0] mem [0:DEPTH-1];  // Memory array

always_ff @(posedge clk) begin
    if (we) begin
        mem[addr] <= wdata;
    end
    rdata <= mem[addr];
end

// ROM (initialized memory)
logic [7:0] rom [0:255];  // ROM array
initial $readmemh("rom_data.hex", rom);

always_ff @(posedge clk) begin
    rdata <= rom[addr];
end
```

## Assertions (SVA)

Use assertions for verification. They're enabled with `--assert` in Verilator.

```systemverilog
// Immediate assertion
always_comb begin
    assert (count < MAX_COUNT) else $error("Count overflow");
end

// Concurrent assertions
property p_valid_handshake;
    @(posedge clk) disable iff (!rst_n)
    valid |-> ##[1:3] ready;
endproperty

assert property (p_valid_handshake)
    else $error("Handshake timeout");

// Cover property (for functional coverage)
cover property (@(posedge clk) state == DONE);
```
