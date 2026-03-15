---
name: conflux-rust-integration-test
description: Create or update pytest-based integration tests for conflux-rust, including adding new test modules under integration_tests/tests, using ConfluxTestFramework and pytest fixtures (network, cw3/ew3, accounts, internal_contracts), customizing framework_class and fixtures, and running/debugging tests with pytest and xdist options.
metadata:
  short-description: Pytest integration tests for conflux-rust
---

# Pytest Integration Tests (Conflux Rust)

## Quick workflow
1) Choose location and reuse fixtures
- Pick the subdirectory under `integration_tests/tests` (e.g., `rpc/`, `internal_contracts/`, `cross_space/`, `execution_spec_tests/`).
- Check for a local `conftest.py` and reuse/extend its fixtures.

2) Pick framework and config
- Start from global fixtures in `integration_tests/tests/conftest.py` (see `references/fixtures.md`).
- If you need custom node counts or config, override `framework_class` in your test module or local `conftest.py`.
- Implement custom framework by subclassing `ConfluxTestFramework` and overriding `set_test_params()` + `setup_network()`.

3) Create the test module
- Name the file with `test` in it (e.g., `feature_test.py`) under `integration_tests/tests/...`.
- Keep setup in fixtures; tests should rely on `network`, `cw3`/`ew3`, `core_accounts`/`evm_accounts`, and `internal_contracts`.
- Prefer deterministic operations; avoid time-based sleeps unless no alternative exists.
- Add Python type hints for tests and fixtures.

4) Implement the test
- Use `network` for RPC and helpers; use `network.cw3`/`network.ew3` for Web3 access.
- Use helper utilities from `integration_tests/test_framework/util.py` (e.g., `wait_until`, `assert_tx_exec_error`).
- Log via `network.log.info(...)` instead of prints.

5) Run and debug
- Run a single module: `uv run --no-sync pytest integration_tests/tests/path/to/test_file.py -vv`
- Filter by name: `uv run --no-sync pytest integration_tests/tests -k test_name`
- Show logs: `-s` (avoid with `-n`), use `--conflux-tracetx` for opcode traces.
- Parallel: `-n logical --dist loadscope`

## Scope guidance
- Prefer `module` scope for `network` and related fixtures; balances isolation and runtime.
- Avoid `function` scope for `network` (node startup is expensive).
- Use `session` scope only if tests fully reset state.
- With xdist, prefer `--dist loadscope` so module-scoped fixtures stay within one worker.

## Pitfalls we hit (and fixes)
- `uv run` failed with “failed to open file .../.cache/uv/sdists-v9/.git: Operation not permitted”: rerun with escalated permissions (sandbox needs access to `~/.cache/uv`).
- `uv run` tried to sync deps and failed building `hive-py` (metadata name mismatch `ethereum-hive`): use `uv run --no-sync ...` for pytest runs to avoid dependency resolution.
- `eth_getBlockByHash` / `eth_getBlockTransactionCountByHash` returned `BlockNotFound` right after `generate_custom_block`: eSpace RPC may not see the block until execution; generate ~5 empty blocks afterward before querying.

## Details and references
- Core fixtures and options: `references/fixtures.md`
- Pytest scope tradeoffs: `references/pytest-scope.md`
- Common interfaces, block execution notes, config hints, templates, and key files: `references/integration-test-notes.md`

## Resources
### assets/
- `basic_test_template.py`: Starter template for a new integration test module.
- `custom_block_example.py`: Minimal custom block example.
