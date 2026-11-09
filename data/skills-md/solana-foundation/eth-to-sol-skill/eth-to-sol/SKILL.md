---
name: eth-to-sol
description: Translate Ethereum/Solidity contracts and EVM mental models to production-grade Solana programs. Use for EVM-to-SVM account model, PDA, SPL Token, CPI, Solana security, transaction/fee/commitment, and Anchor migration guidance.
---

# eth-to-sol

Translate Ethereum/Solidity contracts to production-grade Solana programs. The goal is not a 1:1 port — it is Solana-native code plus a teaching artifact that makes every decision legible to a developer who knows Solidity well and Solana barely.

This skill ships standalone from any app that invokes it. Keep outputs scoped to programs, accounts, transactions, and developer-facing API integration. Do not produce UI artifacts such as React components, screens, CSS, app copy, or visual design guidance.

## Two-pass protocol (hard rule)

Every translation produces two outputs in sequence. Do not collapse them.

1. **Pass 1 — Faithful port.** A semantically identical Anchor program. No restructuring, no SPL CPI substitutions, no parallelism rework. It exists so the refactor's value is legible. Mark obviously un-Solana patterns with `// SMELL:` comments rather than fixing them.
2. **Pass 2 — Solana-native refactor.** Restructured for Solana primitives: SPL programs via CPI, per-entity PDAs, parallelism-friendly account layout, explicit rent/sizing, compute-budget awareness, program splitting where warranted. Production-ready.

If a contract is trivially served by an existing Solana program (e.g. a vanilla ERC-20), the optimized version will be drastically smaller than the naive port. That is the lesson.

## Output contract

For an input named `foo`, produce exactly these artifacts:

| File | Contents |
|---|---|
| `01-original.<ext>` | The input (Solidity, Vyper, etc.). Already present; do not rewrite. |
| `02-naive-port.rs` | Pass 1. Compiles. Inline `// SMELL:` markers on antipatterns. |
| `03-optimized.rs` | Pass 2. Production-ready, fully commented at non-obvious sites. |
| `04-diff.md` | Structured diff. **Group sections by theme** (State model / Parallelism / Security / CPI & program reuse / Compute & rent / Idioms) — mirror the explanation log. Each section: short header, before/after snippets, `file:line` references to the two `.rs` files. |
| `05-explanation.md` | The explanation log. One entry per change in `04-diff.md`, grouped by theme. Schema below. |

When the optimized version meaningfully changes non-program integration (typically: SPL Token replaces a custom token surface, balance/aggregate lookups move off the program, or transaction/account lists change), append a `## Client/API integration notes` section at the bottom of `05-explanation.md`. Keep it to account derivation, required accounts, ATA creation, transaction construction, SDK call shape, and migration scoping. Do not include UI components, screens, styling, or app-specific copy. If the integration shift is minor, fold it into a relevant entry's Tradeoff instead.

`05-explanation.md` is the teaching surface. Treat it as a first-class deliverable, not a comment block.

## Read first

Before producing any translation, internalize the EVM → SVM mental shift in `translation/mental-model.md`. The one-line summary: *on Ethereum the contract knows where its state lives; on Solana the caller brings it.* Every translation rule below is a consequence — if a step ever feels wrong, return to that file.

## Decision tree — which sub-files to load

Default-load: `translation/mental-model.md`, `translation/type-mapping.md`, `translation/pattern-mapping.md`, `security/arithmetic.md`, `security/account-validation.md`, `security/pda-canonicalization.md`.

The default loads are non-negotiable. The mental-model file frames every other decision; arithmetic, account validation, and PDA canonicalization are the three security classes that bite *every* ported contract.

| Source contains | Also load |
|---|---|
| ERC-20 / fungible token | `translation/stdlib-mapping.md`, `optimization/account-model.md`, `security/cpi-safety.md` |
| ERC-20 with `_update` / `_beforeTokenTransfer` override (fee-on-transfer, blacklist, paused-transfer, rebasing) | `translation/stdlib-mapping.md` (Token-2022 section); target Token-2022 with the matching extension (transfer fee, transfer hook, default account state, interest-bearing). Do **not** target classic SPL — the semantics cannot be expressed. |
| ERC-721 / ERC-1155 / NFT | `translation/stdlib-mapping.md`, `optimization/account-model.md`, `optimization/pdas.md` |
| `mapping(...)` storage | `optimization/account-model.md`, `optimization/pdas.md`, `optimization/parallelism.md` |
| Ownable / AccessControl / roles | `translation/stdlib-mapping.md`, `security/signer-checks.md` |
| Custom modifiers | `translation/pattern-mapping.md`, `security/signer-checks.md` |
| External calls / interfaces | `security/cpi-safety.md`, `security/reentrancy.md`, `optimization/program-splitting.md` |
| Heavy arithmetic / fixed-point | `security/arithmetic.md` (also default-loaded) |
| Hot-write global state (counters, `totalSupply`) | `optimization/parallelism.md`, `optimization/account-model.md` |
| Dynamic-sized state (arrays, mappings of unknown size) | `optimization/rent-and-size.md`, `optimization/account-model.md` |
| Multi-contract system | `optimization/program-splitting.md`, `security/cpi-safety.md` |
| Anything writing state after an external call | `security/reentrancy.md`, `security/cpi-safety.md` |
| Compute-pressured paths (multi-CPI swaps, loops in hot path, >300 expected CU per call) | `optimization/compute-budget.md` |
| Multiple account types owned by the program (type-confusion risk surface) | `security/account-validation.md` (also default-loaded) |
| Any PDA the program will sign for | `security/pda-canonicalization.md` (also default-loaded), `optimization/pdas.md` |
| Protocol takes a user-supplied token Mint as configuration (vault, AMM, lending market) | `security/reentrancy.md`, `security/account-validation.md`, `security/cpi-safety.md` |
| Vault/AMM/4626-shaped protocol (share/asset conversion math, deposit + withdraw + redeem semantics) | `security/arithmetic.md` (rounding-direction discipline), `optimization/account-model.md` (read aggregates from SPL Token), `optimization/parallelism.md` (read-only vault pattern) |
| Time-delta math (`now - last_update`, accumulator periods) | `security/arithmetic.md` (clock-skew + negative-delta-cast pitfall) |
| Large account graph, payment batch, swap route, many recipients, or transaction-size concern | `optimization/transactions-and-commitment.md`, `optimization/compute-budget.md` |
| Priority fees, local fee markets, compute limit, recent blockhash, retry/expiry, or landing strategy | `optimization/transactions-and-commitment.md`, `optimization/compute-budget.md` |
| Settlement, irreversible off-chain action, indexer correctness, or commitment-level choice | `optimization/transactions-and-commitment.md` |
| Client SDK/tooling/testing migration asks (`@solana/kit`, `web3.js`, Anchor client, LiteSVM, Bankrun, local validator) | `optimization/transactions-and-commitment.md` |

Always load every security/* file relevant to the constructs present. Security is non-negotiable.

## Module 1B source alignment

This skill tracks Solana Enterprise Training Module 1B, "From EVM to SVM":
https://github.com/solana-foundation/solana-enterprise-training/tree/main/module-1b-from-evm-to-svm

Use the module as source alignment, not as shipped course UI. The skill should reference the engineering concepts below and avoid slides, quizzes, UI, or app-specific teaching surfaces.

| Module 1B topic | Skill coverage |
|---|---|
| Purpose, prerequisites, and learning objectives | This `SKILL.md` assumes a Solidity-fluent reader with baseline Solana awareness and scopes outputs to translation artifacts, not course delivery. |
| Mental-model shift: "you bring the state" | `translation/mental-model.md` |
| Account model translation: storage slots, mappings, PDAs, explicit signers, upgrades, IDL/logs/time | `translation/mental-model.md`, `translation/type-mapping.md`, `translation/pattern-mapping.md`, `optimization/account-model.md`, `optimization/pdas.md` |
| ERC-20 vs SPL Token: Mint, Token Account, ATA, allowances/delegates, decimals, token-account creation | `translation/stdlib-mapping.md`, `optimization/account-model.md`, `security/cpi-safety.md` |
| Composability: EVM `call` vs Solana CPI and account-graph propagation | `translation/mental-model.md`, `security/cpi-safety.md`, `optimization/program-splitting.md` |
| Reentrancy as a structural property and the replacement failure modes | `security/reentrancy.md`, `security/cpi-safety.md`, `security/account-validation.md` |
| Solana program security checklist: ownership, signer checks, substitution, discriminators, arithmetic, CPI authority, safe close, rent | `security/account-validation.md`, `security/signer-checks.md`, `security/pda-canonicalization.md`, `security/arithmetic.md`, `security/cpi-safety.md`, `optimization/rent-and-size.md` |
| Transactions in practice: recent blockhash, expiry, versioned transactions, ALTs, compute budget, priority fees, local fee markets | `optimization/transactions-and-commitment.md`, `optimization/compute-budget.md`, `optimization/parallelism.md` |
| Commitment levels for settlement and indexing | `optimization/transactions-and-commitment.md` |
| Developer workflow: `@solana/kit`, legacy `web3.js`, Anchor client, LiteSVM, Bankrun, local validator | `optimization/transactions-and-commitment.md` |
| Cumulative EVM/SVM reference | `translation/mental-model.md` plus the referenced translation, optimization, and security files |
| Quiz and slides | Do not ship; those are course surfaces, not skill runtime material. |
| Additional resources | Keep external: Solana Cookbook, Anchor Book, Neodyme Common Pitfalls, Sec3 audit checklist, Solana Program Examples, Helius priority-fee guide, and official Solana fee docs. |

## Pre-flight checklist (gate on the optimized version)

Every item must hold before emitting `03-optimized.rs`. If one fails, fix and re-check.

- [ ] Every arithmetic op is `checked_*` — or has an inline justification for `saturating_*` / `wrapping_*`. No bare `+ - * /` on user-controlled values.
- [ ] Every `Account<'info, T>` either uses Anchor's typed checks or includes explicit owner + discriminator validation. No `AccountInfo` smuggled through without checks.
- [ ] Every signer-required path uses `Signer<'info>` or a manual `is_signer` check. No "the client won't call it without a signer" reasoning.
- [ ] Every PDA derivation either uses `seeds = [...], bump = stored_bump` (preferred — saves ~1.5k CU per call) or bare `seeds = [...], bump,` (acceptable when CU is not pressured; both forms enforce canonicalization via Anchor's `find_program_address` check). The cached form is strongly preferred — all reference examples use it. Do **not** use `bump = <user_input>` — that's the actual canonicalization vulnerability.
- [ ] CPIs use `CpiContext::new` or `CpiContext::new_with_signer`. The program arg is a `Pubkey` (use `ctx.accounts.<program>.key()`) — Anchor 1.0+ removed the `AccountInfo` form. No hand-rolled `invoke`/`invoke_signed` with manually assembled `AccountInfo` arrays unless raw Solana is justified.
- [ ] No path mutates state after a CPI to an untrusted program without re-reading and re-validating. (See `security/reentrancy.md` for why account locking is necessary but not sufficient.)
- [ ] Account sizing is explicit: `space = 8 + <sum>`; the 8 is the Anchor discriminator. Variable-size fields have hard caps.
- [ ] Errors use `#[error_code]`. No `ProgramError::Custom(n)` literals, no `msg!`-then-fail.
- [ ] No PDA shares a write lock with high-frequency unrelated state. Per-entity PDAs over global counters where the protocol allows.
- [ ] If the contract emits events that SPL programs already emit (Transfer for SPL Token), prefer not duplicating them.
- [ ] Re-init protection: PDAs that should only init once use `init` (not `init_if_needed`) and have unique seeds.

## Tooling — Solana Developer MCP `rust_autofixer`

If your environment exposes the Solana Developer MCP (`https://mcp.solana.com/mcp`), the `rust_autofixer` tool is part of the workflow — not optional.

**When to call it:** every time you have produced or modified Anchor or Pinocchio Rust that you intend to ship. That includes `02-naive-port.rs` and `03-optimized.rs`, and any in-flight fix you apply after a failed `cargo check`.

**How to call it:** pass the full Rust source. Specify the framework (`auto`, `anchor`, or `pinocchio`) if the caller hasn't already.

**The loop:**

1. Call `rust_autofixer` on the current Rust.
2. Apply every suggested fix (they are mechanical, structured, and safe).
3. Call `rust_autofixer` again.
4. Repeat until `require_another_tool_call_after_fixing` is `false`.

Only emit the artifact once the loop terminates. This is in addition to — not a replacement for — the pre-flight checklist above; the autofixer catches the structural-safety class of bug, the checklist catches design/idiom issues.

**Do not use any other Solana MCP tool** (`list_sections`, `read_section`, `search`, etc.) for this workflow. Stay scoped to `rust_autofixer`.

## Explanation log opener

Before the first `## Theme` heading, the explanation log opens with a short prose preamble. The preamble must, in this order:

1. **One paragraph: what the program does in EVM-developer terms.** State the protocol the way you'd state it to a Solidity dev who's never seen the contract — "a one-shot ERC-20 crowdfund: supporters deposit tokens before a deadline; if the goal is met the creator claims the pot, otherwise supporters refund." Don't lead with what the example *teaches*; lead with what the program *does*.
2. **One paragraph: the Solana shape it ports to.** What the program looks like on Solana at the same height of abstraction — "On Solana, the same protocol becomes one PDA per supporter plus a singleton fundraiser account; SPL Token handles the actual token movement via CPIs." Still no per-line / per-symbol detail.

Any optional context that follows (vocabulary list, reference-implementation link, etc.) comes after these two paragraphs, not before.

## Explanation log schema

Each entry is exactly five fields. Keep them tight — one to four sentences each.

```
### <short title>

- **Title rules.** When the change has a Solidity counterpart (most state-model / security / idiom entries), frame the title as `Solidity-side → Solana-side` — e.g. `mapping(address => uint256) ledger → per-supporter PDA`, not `Vec<Contribution> → per-supporter PDA`. A Solidity-fluent reader of `03-optimized.rs` has not opened the naive port; titles that name naive-port Rust types (`Vec<X>`, `iter_mut().find(...)`, etc.) read as gibberish to them. When the change is Solana-only hygiene (no Solidity counterpart — bump caching, PDA seed consolidation, account-size optimizations), use a plain descriptive title without the arrow.
- **What:** the concrete change as a diff between the naive port and the optimized port. Reference the diff section or `file:line` in the .rs files. This is the LOW-LEVEL diff view; cite specific identifiers, function names, line numbers. Written for someone reviewing the diff side-by-side.
- **Annotation:** a self-contained explanation of THIS code (the optimized version) for a Solidity-fluent reader who is looking only at the optimized file and has never seen the naive port. State what the optimized code does at this point, why a Solidity developer's mental model has to shift here, and — when meaningful — what a naive translation would have done and why this shape is preferable. Do NOT cite the naive port by filename or reference any line outside the optimized file. Two to four sentences.
- **Why:** the platform-level reasoning, structured as a two-sided contrast for a Solidity-fluent reader. Lead the first sentence(s) with **"On Ethereum, ..."** and describe the EVM/Solidity paradigm the developer is bringing with them. Then lead the next sentence(s) with **"On Solana, ..."** and describe the paradigm that diverges. Keep it HIGH-LEVEL — platform mechanics, mental model, what serializes / what doesn't, who owns what, what the runtime guarantees. Save the per-line / per-symbol detail for `What:` and `Annotation:`. Avoid backtick code fragments here unless absolutely necessary.
- **Benefit:** what is gained. Be specific: CU saved, parallelism unlocked, security class avoided, code deleted.
- **Tradeoff:** what is given up. If nothing meaningful, say so and justify briefly.
```

`What` is the "code review" view of the diff; `Annotation` is the "reader of the final code" view. They cover different audiences — both are needed because the final code is shipped on its own, but the diff is also part of the artifact set.

Group entries under thematic headers: `## State model`, `## Parallelism`, `## Security`, `## CPI & program reuse`, `## Compute & rent`, `## Idioms`.

## Explanation style — write for a Solidity-fluent reader who has never seen Solana

The reader knows Solidity well. They know financial systems. They have **not** internalized PDAs, the account model, SPL Token, rent, CPI, or Anchor's constraint vocabulary. The explanation log is where they bridge — every entry must land for that reader.

### Rules

1. **First-use translation, always inline.** The first time any Solana-specific term appears in a given explanation log, give a short EVM analog in parentheses or em-dashes. Don't assume a glossary; weave it into the prose. After first use, the term is fair game.

   Required glossing on first use (non-exhaustive):
   - **PDA** — "PDA (Program-Derived Address — a deterministic account address derived from seeds the program controls; analog of a Solidity storage slot keyed by `(address, mapping)` — but each PDA is its own account, not a slot inside the program)"
   - **SPL Token** — "SPL Token (the shared on-chain token program every fungible token reuses on Solana — instead of each ERC-20 deploying its own contract, every token is just configuration on this one program)"
   - **CPI** — "CPI (cross-program invocation — Solana's version of one contract `call`-ing another, but every account the callee will touch must already be in the caller's transaction)"
   - **rent** — "rent (a refundable SOL deposit every account pays to live on-chain; ~0.001 SOL per KB of account data, returned in full when the account is closed)"
   - **lamports** — "lamports (1 SOL = 1e9 lamports — Solana's gwei equivalent, but at 9 decimals instead of 18)"
   - **ATA / Associated Token Account** — "ATA (Associated Token Account — the canonical per-wallet token account for a given mint, with a deterministically derivable address; the analog of \"the wallet's balance for this token\")"
   - **Mint account** — "Mint account (the on-chain configuration for a token: total supply, decimals, who can mint — owned by the SPL Token program, not by the issuer)"
   - **Signer<'info>** — "Signer (an explicit `msg.sender` — Solana requires every signing account to be declared up front in the instruction's account list, vs. Solidity's implicit `msg.sender`)"
   - **Anchor** — "Anchor (the framework on top of raw Solana programs, similar to how Hardhat relates to raw EVM — provides macros, account validation, and the IDL)"
   - **init_if_needed** — "init_if_needed (an Anchor constraint that creates the account on first call and is a no-op on subsequent calls — Solana's closest analog to Solidity's implicit `mapping[key] = value`)"
   - **close = X** — "close = X (an Anchor constraint that tears the account down and refunds its rent to X when the instruction succeeds — there's no Solidity equivalent because Solidity storage slots can't be deleted)"
   - **discriminator** — "discriminator (an 8-byte type tag Anchor prepends to every account it manages, so deserializing a `Vault` account as a `Mint` fails loudly — no EVM analog because EVM has no typed account model)"
   - **has_one** — "has_one = authority (an Anchor constraint that verifies the account's stored `authority` field equals the `authority` account passed in the same instruction — the declarative form of `require(state.authority == signer)`)"
   - **seeds + bump** — "seeds (the byte inputs the program uses to derive a PDA; the `bump` is a nonce that makes the address valid). Conceptually: `keccak256(abi.encodePacked(...))` with extra steps to keep the result off the secp256k1 curve."
   - **write-lock / parallelism** — "Solana's runtime locks every writable account a transaction touches, so two transactions that mutate different accounts run in parallel — the EVM-style global single-threaded execution is replaced by per-account locks (Sealevel)."

2. **Comparative framing in Why bullets.** Prefer "In Solidity, you would have written X because Y. On Solana, the equivalent shape is Z because W" over "the PDA stores X". The reader anchors on what they already know.

3. **Plain-English code references.** When citing a Rust line by `file:line`, briefly say what it does in EVM-flavored language. Not just `f.contributors.iter_mut().find(|c| c.who == k)` — say "scans the contributor list linearly to find the supporter's row (the on-chain analog of `contributors[k]` in Solidity, but more expensive)."

4. **Spell out the consequence chain.** The reader doesn't yet know why "one PDA per supporter" matters. Don't say "no serialization of cross-supporter activity" without first explaining that Solana serializes writes to the *same account*, so isolating writes to different accounts is what unlocks parallelism. Two sentences > one tight one if the second sentence is doing teaching work.

5. **Tradeoff is honest.** Rent, extra accounts, Anchor-specific idioms a non-Anchor reader has to learn — name them concretely. The reader is evaluating a real migration; gloss only hurts.

### Side-by-side: bad → better

The current `examples/token-fundraiser/05-explanation.md` entry for §S1 reads:

> **Why:** Solidity's `mapping(address => uint256)` is one slot per supporter inside one contract — addressable by key inside one storage tree. The Solana equivalent is one account per supporter, addressable by PDA derivation. A `Vec` inside a state account is the wrong primitive: it bounds the supporter count, forces every contribute/refund to mutate the singleton state account, and scans linearly on lookup.

A Solidity-fluent reader who's never seen Solana parses "PDA derivation" as noise. Better — high-level, two clearly-marked sides:

> **Why:** On Ethereum, contract storage is global to the contract: every entry in a mapping lives in the same storage tree, and the contract is the single writer. On Solana, the equivalent of a mapping is *one on-chain account per entry* — each entry owns its own slice of state, with its own deterministic address, its own owner, and its own write-lock. The naive port collapses every entry back into one shared state account; that imitates the Solidity layout but loses the per-entry property that lets unrelated writes execute concurrently.

Same content, lower code density, lands for the reader. **Err on the side of teaching.** Length is not a virtue; clarity for the assumed reader is. Code-level identifiers belong in `What:` and in inline annotations on the .rs file — the `Why:` field is for the platform mental model. If a section already used the term, you don't need to re-explain it — the rule is "first use in this explanation log."

### Original example entry (for structure reference)

```
### Balances moved from on-chain map to SPL Token accounts

- **What:** Removed `balances: Vec<BalanceEntry>` from `TokenState` (`02-naive-port.rs:153`). Each holder now has an Associated Token Account (ATA — the canonical per-wallet token balance account, derived deterministically from `(wallet, mint)`); transfers go through `token::transfer` on the SPL Token program directly, not through this program (`03-optimized.rs` has no transfer instruction).
- **Annotation:** This program holds no balance ledger of its own — there's no `balanceOf` map, no `transferFrom`, no custody field anywhere in this file. On Solana, fungible-token balances live in the network's SPL Token program; each holder owns their own token account, and transfers run as direct CPIs to SPL Token rather than going through this program. Re-implementing a custom `mapping(address => uint256)` here would force every transfer in the system to write-lock this program's state and serialize them all.
- **Why:** On Ethereum, an ERC-20 contract holds the balance ledger inside its own storage — every holder is a slot in the contract's `balanceOf` map, and every transfer is a contract call to that contract. On Solana, balances live in the network-wide SPL Token program rather than inside any individual program — each holder has their own on-chain account, and transfers move balances directly between those accounts without going through the issuing program at all. Keeping a custom map would re-implement that shared infrastructure inside the program and force every transfer to write-lock the program's state.
- **Benefit:** Transfers between disjoint sender/recipient pairs run in parallel (Solana's runtime locks accounts, not the program — so writes to Alice→Bob and Carol→Dan don't block each other). ~150 lines of custom balance/allowance logic deleted. No path for a buggy custom balance update.
- **Tradeoff:** Holders create an ATA before first receipt — a one-time ~0.002 SOL rent deposit (refundable when the account is closed). Off-chain code computes ATA addresses to read balances instead of reading one contract account.
```

## Reference example

Trace the protocol on `examples/token-fundraiser/` end-to-end before producing translations of new inputs. The example exists so you can verify the protocol produces the contract.

## Ambiguities

When in doubt on a new translation, prefer the choice consistent with the reference examples unless the input forces otherwise. Anchor 1.0+ is the target, classic SPL Token is the default for ordinary fungible tokens, and Token-2022 is used only when the source semantics require an extension.
