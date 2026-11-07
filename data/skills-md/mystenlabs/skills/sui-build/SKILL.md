---
name: sui-build
description: >
  Use this skill when the user needs to build Move code, or when when the user 
  asks about sui move build.
---

# Building Packages

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information sourced exclusively from [docs.sui.io](https://docs.sui.io) and [move-book.com](https://move-book.com).

## Building

```bash
sui move build
```

This compiles all modules, validates types, enforces resource safety, and produces bytecode. Fix any errors before proceeding.

For the canonical hello-world repository, run build commands from `sui-stack-hello-world/move/hello-world`.

### `--build-env` flag

When a package has an `[environments]` section in `Move.toml` with multiple networks, use `--build-env` to target a specific environment:

```bash
sui move build --build-env testnet
sui move build --build-env mainnet
```

This resolves dependencies and package addresses for the specified environment. Without `--build-env`, the build uses the default environment or may fail with "Could not determine the correct dependencies" if multiple environments are defined and no default is set.

The `--build-env` flag also applies to `sui move test`:

```bash
sui move test --build-env testnet
```

## Testing

```bash
sui move test
```

### Key testing modules

- **`sui::test_scenario`** — Multi-transaction, multi-sender test scenarios. Simulates realistic transaction flows with `begin`, `next_tx`, and `end`.
- **`std::unit_test`** — Assertion macros for unit tests (`assert_eq!`, `assert_ne!`).

### Code coverage

Track which lines your tests exercise:

```bash
sui move test --coverage
```

View coverage results for a specific module:

```bash
sui move coverage source --module <name>
```

### Move Analyzer

Install via suiup:

```bash
suiup install move-analyzer
```

Then install the **Move Analyzer** extension in VS Code. It provides code completion, go-to-definition, inline diagnostics, and hover documentation. It activates automatically for `.move` files — no additional configuration needed.

### Debugging

- **Move Trace Debugger:** Step-through debugger for Move execution traces with variable inspection.
- **`sui replay`:** Locally re-execute any past onchain transaction and compare effects. Useful for diagnosing production issues.
- **`std::debug::print`:** Print values during test execution.
