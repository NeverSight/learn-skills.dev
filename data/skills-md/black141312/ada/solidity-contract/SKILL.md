---
name: solidity-contract
description: Write a production-ready Solidity smart contract with tests, access control, and a deploy script
category: web3
---

# Solidity Contract

Reach for this when implementing a new on-chain contract from scratch. Favor battle-tested libraries over hand-rolled logic.

1. Pin a compiler: set an exact `pragma solidity 0.8.x;` and lock it in `foundry.toml`/`hardhat.config` (`evmVersion`, `optimizer`).
2. Scaffold from OpenZeppelin: import vetted bases (`Ownable`/`AccessControl`, `ReentrancyGuard`, `Pausable`, `SafeERC20`) instead of writing your own.
3. Define state and the external interface first: storage layout, events for every state change, custom errors instead of `require` strings.
4. Implement with checks-effects-interactions order; mark functions `external`/`view`/`pure` correctly and add `onlyRole`/`onlyOwner` guards.
5. Write tests (`forge test` or Hardhat): cover happy path, revert paths, access control, and at least one fuzz/invariant test.
6. Add a deploy script (`forge script` or Hardhat deploy) that reads addresses/params from env, never hardcoded keys.
7. Run `forge build`/`compile`, the test suite, and a linter (`solhint`) before declaring done.

## Rules
- Never use `tx.origin` for auth; use `msg.sender` with explicit roles.
- Emit an event for every meaningful state mutation so off-chain indexers can follow.
- Validate all external inputs; reject zero addresses and zero amounts explicitly.
- Avoid `delegatecall`, `selfdestruct`, and assembly unless you can justify and test them.
- Keep funds-handling functions `nonReentrant` and follow checks-effects-interactions.
- Pin dependency versions (no floating `^`) for reproducible bytecode.
