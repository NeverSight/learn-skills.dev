---
name: ton-bug-triage
description: Reproduce TON bugs on a local tontester network. Use only when the task involves launching tontester validators, deploying contracts to a local network, or comparing patched validator builds — not for general TON development or testnet interaction.
---

# TON Bug Triage

Use this skill when the job is to prove something on a local `tontester` network, not just to launch validators.

Typical triggers:

- deploy a contract and trigger a bug with an internal message
- compare baseline and probing validator builds
- verify a crash, liveness failure, malformed-packet path, or compatibility claim
- collect maintainer-ready evidence for a local TON repro

The standard is: choose the smallest topology that answers the question, define the success condition before running, and collect enough evidence that the result is interpretable.

## Working Model

Keep these paths distinct:

- Skill scripts: files under this skill directory, such as `scripts/run_basic_network.py`
- Source tree: the real TON checkout passed as `--repo-root`
- Build directory: binaries and libraries such as `validator-engine`, `create-state`, `tonlibjson`, and `tolk`
- Work directory: per-run state, logs, configs, and emitted artifacts

Do not assume the skill directory and the repo are the same thing. The scripts live in the skill. They operate on the repo and build you pass in.

`wallet-env.txt` is the main handoff artifact between the launcher and follow-up helpers.

These helpers depend on `tontester` internals and private APIs. If `tontester` changes, expect to adjust helper behavior, generated bindings, or command assumptions.

## Workflow Selection

Choose one workflow before running anything:

- `Workflow A — trigger via transaction`
  Use this when the bug is reached by deploying a contract, sending an internal message, or delivering a malformed/custom payload to a contract account.

- `Workflow B — trigger via validator behavior`
  Use this when the bug requires patched validator code, mixed builds, consensus interference, malformed protocol packets, reordered traffic, or deliberately invalid block behavior.

If a repro touches both, ask one question first: can you trigger it on an unmodified network after a normal deploy/send path? If yes, start with Workflow A. If no, treat it as Workflow B.

## Core Rules

1. Start with the smallest network that can answer the question.
   Use one validator unless the path needs peers, consensus, or mixed builds.

2. Prefer ordinary deploy/send flow over zerostate edits.
   If the bug only reproduces after zerostate mutation, say that clearly.

3. Keep baseline and probing builds separate.
   Usually `vanilla-build/` is baseline and `build/` or `build-probing/` is the modified build.

4. Decide the success condition before running.
   Examples: target `mc_seqno`, explicit crash marker, process death, active contract account, inspected transaction, or honest-node rejection of a malformed packet.

5. For Workflow B, make the probing node self-immune.
   Operational meaning: the probing node may emit malformed or adversarial behavior, but it must stay alive until the target effect is observed on the honest nodes. A run is invalid if the probing node dies first and that death could explain the outcome.

6. Record enough evidence to rerun the exact scenario.
   Keep the run directory, the build directories, the commands, the relevant addresses, and the exported artifacts.

7. Before calling something maintainer-ready, rerun it from a clean checkout or detached worktree with only the intended artifacts.

## Core Scripts

Prefer the bundled scripts over one-off shell sequences.

- `scripts/run_basic_network.py`
  Launch one or more validators from a single build. Supports `--emit-wallet-env`, `--base-port`, `--validators`, and `--keep-alive`.

- `scripts/run_mixed_network.py`
  Launch baseline and probing validators from different build directories. Use this for malicious-vs-honest experiments, log-based crash detection, and probing-node survival checks.

- `scripts/compile_tolk.py`
  Compile a `.tolk` source to `.fif` and materialize the contract code BoC. It hard-fails if the `tolk` binary is stale relative to repo `HEAD`.

- `scripts/build_stateinit.py`
  Build a deployable `StateInit` BoC from code plus optional data and library-dictionary BoCs.

- `scripts/run_fift_script.py`
  Run a `.fif` script with the correct include paths.

- `scripts/wallet_send.py`
  Build and optionally send a wallet-signed message. Use `--init-boc` for deployment and `--body-boc` for arbitrary internal payloads.

- `scripts/send_boc.py`
  Send a prebuilt serialized external message BoC through tonlib without rebuilding it via `wallet_send.py`.

- `scripts/address_info.py`
  Normalize and inspect raw and friendly TON address forms when helper inputs need to be cross-checked.

- `scripts/account_state.py`
  Fetch raw account state and dump code/data BoCs for inspection.

- `scripts/get_method.py`
  Run a get-method through tonlib and print JSON.

- `scripts/inspect_latest_transaction.py`
  Fetch the latest account transaction, export raw transaction data, and save message body/init-state BoCs when tonlib returns them as `msg.dataRaw`.

- `scripts/run_liteclient.py`
  Run a `lite-client` command using `wallet-env.txt` or explicit repo/build/config inputs.

- `scripts/dump_boc.py`
  Print a BoC cell tree through Fift. Use this for payloads, `StateInit`, exported transaction data, and dumped account code/data.

- `scripts/summarize_run.py`
  Summarize node liveness and crash markers for a finished or live run directory.

- `scripts/demo_wallet_flow.py`
  Known-good end-to-end verifier for the simple wallet path.

## Workflow A

Use Workflow A when the trigger is “deploy contract, then send message”.

1. Launch a small network with `--emit-wallet-env`.
2. Compile your contract with `scripts/compile_tolk.py`, or provide a hand-built code BoC from Fift assembly if you are not using Tolk.
3. Build deployable `StateInit` with `scripts/build_stateinit.py`.
   Pass `--data-boc` and `--library-boc` only when the contract actually needs them.
4. Deploy from the funded built-in `main-wallet` with `scripts/wallet_send.py --init-boc`.
   A deploy message that uses `--init-boc` may also invoke the contract's internal message handler. Check whether the deploy transaction itself changed contract state before sending a separate trigger.
5. Wait for activation.
   Prefer `account_state.py` plus a contract-specific get-method over assuming one masterchain advance is enough.
6. Build the trigger body as a BoC when the payload is custom or binary.
   `run_fift_script.py` is the easiest way to emit a one-off `body.boc`.
7. Send the trigger with `scripts/wallet_send.py --body-boc`.
   `--body-boc` is the authoritative payload path and overrides `--comment`.
   If you already have a signed external message BoC, use `scripts/send_boc.py --boc` instead of rebuilding it with `wallet_send.py`.
   `--wait-mc-advance` proves the network is alive. It does NOT prove the transaction succeeded, the deploy activated, or the contract state changed. Always inspect the target account directly.
8. Observe with `inspect_latest_transaction.py --out-dir` and `dump_boc.py`.
   The exported `transaction-data.boc` and `in-msg-body.boc` are the starting point for cell-level debugging.
   If the tonlib-based helpers crash (common symptom: `KeyError: '@extra'`), use `run_liteclient.py` as the fallback for all observation steps. See `references/liteclient_fallback.md`.

For the full worked sequence, read `references/contract_deploy_flow.md`.

For the simple wallet smoke path only, read `references/wallet_and_deploy_helpers.md`.

## Workflow B

Use Workflow B when the trigger is “modify validator behavior, then observe honest-node reaction”.

1. Snapshot the baseline build before probing changes.
2. Patch the probing build only, and gate every behavioral change behind explicit `TON_PROBING_*` environment variables.
3. Choose a mixed topology and explicit success and failure conditions.
   Use `--success-log`, `--failure-log`, `--require-node-alive`, and `--require-node-dead` deliberately.
4. Run the mixed network with `scripts/run_mixed_network.py`.
5. Confirm both sides of the claim:
   probing markers were hit, and the honest-node effect happened or did not happen.
6. Summarize the run with `scripts/summarize_run.py`, then inspect specific logs manually only where the summary points.

For common patch shapes, read `references/probing_patterns.md`.

For an end-to-end example, read `references/bug_hunt_example.md`.

## Negative Result

A valid “did not reproduce” is still useful evidence. Treat a run as a real negative result only if all of the following are true:

- the selected workflow actually executed its trigger path
- the relevant probing or trigger markers were present
- the network stayed healthy enough that the absence of the bug is meaningful
- the observation step looked at the right account, transaction, or node logs
- the timeout or seqno target was reached without the target effect

Stop iterating and report a negative result when a clean rerun gives the same outcome and the remaining changes are only minor parameter churn.

## Iteration And Debugging

- If `compile_tolk.py` fails with a stale-build error, rebuild `tolk` first.
  The exact fix is usually `ninja -C <build-dir> tolk`.

- If a deploy appears to succeed but the destination still looks empty, check too-early observation first.
  Wait for activation instead of assuming the deploy path is broken.

- If a contract is active but the expected get-method fails, verify the method id and the initial data layout before changing the network topology.

- If `inspect_latest_transaction.py` shows the wrong payload, dump both the original trigger BoC and the exported `in-msg-body.boc` and compare their cell trees.

- If probing markers are missing in Workflow B, the environment variables did not reach the node or the patched code path never executed.

- If the probing node dies before the target effect is observed, the run is invalid.

## Evidence Standard

Record enough to support the claim:

- exact run directory
- build directories used
- success condition used
- relevant launcher and helper commands
- target addresses or node names
- exported transaction and BoC artifacts for Workflow A
- node liveness and log markers for Workflow B

For Workflow A, remember that `--wait-mc-advance` is only a liveness hint; confirm success from the target account or transaction.

## Troubleshooting

- If `python` is missing, use `python3`.
- If `tonapi` bindings are missing, the helpers usually generate them from `test/tontester/generate_tl.py`.
- If a helper is copied outside the repo, keep passing the real repo as `--repo-root`; includes and generated artifacts come from the repo, not the skill folder.
- If tonlib-based scripts (`account_state.py`, `get_method.py`, `inspect_latest_transaction.py`, `wallet_send.py --auto-seqno`) crash with `KeyError: '@extra'` or similar tonlib wrapper errors, the local tonlib build has a compatibility issue. Fall back to `lite-client` for inspection and use `wallet_send.py` with manual `--seqno` instead of `--auto-seqno`.
  See `references/liteclient_fallback.md` for the shared fallback flow.
- If `vanilla-build/CMakeCache.txt` points at `build/`, treat `vanilla-build` as invalid and recreate it. Do not trust a build tree that reconfigures into the wrong directory.
- Do not assume `lite-client` is present in the passed build directory. Some checkouts only have `create-state`, `tonlibjson`, and `tolk` built.
- If disk is full, clear old `run-*` directories before retrying.

## References

- `references/wallet_and_deploy_helpers.md`
  Read this for the proven simple-wallet smoke path.

- `references/contract_deploy_flow.md`
  Read this for the generic Workflow A compile, deploy, trigger, inspect path.

- `references/liteclient_fallback.md`
  Read this when tonlib-based helpers fail and Workflow A needs `lite-client` inspection or manual wallet seqno handling.

- `references/probing_patterns.md`
  Read this when designing Workflow B code changes.

- `references/diagnostic_checklist.md`
  Read this when a run completed but the outcome is unclear.

- `references/bug_hunt_example.md`
  Read this for a concrete mixed-network negative-result example.
