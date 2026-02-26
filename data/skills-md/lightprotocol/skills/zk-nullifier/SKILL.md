---
name: zk-nullifier
description: "For custom ZK Solana programs and privacy-preserving applications to prevent double spending. Guide to integrate rent-free nullifier PDAs for double-spend prevention."
metadata:
  source: https://github.com/Lightprotocol/skills
  documentation: https://www.zkcompression.com
  openclaw:
    requires:
      env: []
      bins: ["node", "cargo", "light"]
---
# ZK Nullifiers

## Overview

Building a ZK Solana program requires:
- Nullifiers to prevent double spending
- Proof verification
- A Merkle tree to store state
- An indexer to serve Merkle proofs
- Encrypted state

For non zk applications see this skill to use nullifiers: skills/payments

## Workflow

1. **Clarify intent**
   - Recommend plan mode, if it's not activated
   - Use `AskUserQuestion` to resolve blind spots
   - All questions must be resolved before execution
2. **Identify references and skills**
   - Match task to [resources](#resources) below
   - Locate relevant documentation and examples
3. **Write plan file** (YAML task format)
   - Use `AskUserQuestion` for anything unclear — never guess or assume
   - Identify blockers: permissions, dependencies, unknowns
   - Plan must be complete before execution begins
4. **Execute**
   - Use `Task` tool with subagents for parallel research
   - Subagents load skills via `Skill` tool
   - Track progress with `TodoWrite`
5. **When stuck**: ask to spawn a read-only subagent with `Read`, `Glob`, `Grep`, and DeepWiki MCP access, loading `skills/ask-mcp`. Scope reads to skill references, example repos, and docs.

## Nullifiers on Solana

A nullifier is a deterministically derived hash to ensure an action can only be performed once. The nullifier cannot be linked to the action or user. For example Zcash uses nullifiers to prevent double spending.

To implement nullifiers we need a data structure that ensures every nullifier is only created once and never deleted. On Solana a straight forward way to implement nullifiers is to create a PDA account with the nullifier as seed.

PDA accounts cannot be closed and permanently lock 890,880 lamports (per nullifier rent-exemption).
Compressed PDAs are derived similar to Solana PDAs and cost 15,000 lamports to create (no rent-exemption).

| Storage | Cost per nullifier |
|---------|-------------------|
| PDA | 890,880 lamports |
| Compressed PDA | 15,000 lamports |


## Testing

```bash
# Rust tests
cargo test-sbf -p nullifier

# TypeScript tests (requires light test-validator)
light test-validator  # separate terminal
npm run test:ts
```

## Pattern Overview

```
1. Client computes nullifier = hash(secret, context)
2. Client fetches validity proof for derived address (proves it does not exist)
3. Client calls create_nullifier with nullifier values and proof
4. Program derives address from nullifier, creates compressed account via CPI
5. Light system program rejects CPI if address already exists
```

## Resources

- Full example: [program-examples/zk/nullifier](https://github.com/Lightprotocol/program-examples/tree/main/zk/nullifier)
- ZK overview: [zkcompression.com/zk/overview](https://www.zkcompression.com/zk/overview)
- Additional ZK examples: [program-examples/zk](https://github.com/Lightprotocol/program-examples/tree/main/zk) (nullifier, zk-id, mixer, shielded-pool)

## Reference Implementation

Source: [program-examples/zk/nullifier](https://github.com/Lightprotocol/program-examples/tree/main/zk/nullifier)

### Account Structure

```rust
#[derive(Clone, Debug, Default, BorshSerialize, BorshDeserialize, LightDiscriminator)]
pub struct NullifierAccount {}
```

Empty struct since existence alone proves the nullifier was used.

### Address Derivation

```rust
pub const NULLIFIER_PREFIX: &[u8] = b"nullifier";

let (address, address_seed) = derive_address(
    &[NULLIFIER_PREFIX, nullifier.as_slice()],  // seeds
    &address_tree_pubkey,                        // address tree
    &program_id,                                 // program ID
);
```

Address is deterministically derived from:
- Constant prefix (prevents collisions with other account types)
- Nullifier value (32 bytes)
- Address tree pubkey
- Program ID

### Instruction Data

```rust
#[derive(Clone, Debug, AnchorSerialize, AnchorDeserialize)]
pub struct NullifierInstructionData {
    pub proof: ValidityProof,           // ZK proof that addresses don't exist
    pub address_tree_info: PackedAddressTreeInfo,
    pub output_state_tree_index: u8,
    pub system_accounts_offset: u8,
}
```

### Create Nullifiers Function

```rust
pub fn create_nullifiers<'info>(
    nullifiers: &[[u8; 32]],
    data: NullifierInstructionData,
    signer: &AccountInfo<'info>,
    remaining_accounts: &[AccountInfo<'info>],
) -> Result<()> {
    let light_cpi_accounts = CpiAccounts::new(
        signer,
        &remaining_accounts[data.system_accounts_offset as usize..],
        LIGHT_CPI_SIGNER,
    );

    let address_tree_pubkey = data
        .address_tree_info
        .get_tree_pubkey(&light_cpi_accounts)
        .map_err(|_| ErrorCode::AccountNotEnoughKeys)?;

    let mut cpi_builder = LightSystemProgramCpi::new_cpi(LIGHT_CPI_SIGNER, data.proof);
    let mut new_address_params: Vec<NewAddressParamsAssignedPacked> =
        Vec::with_capacity(nullifiers.len());

    for (i, nullifier) in nullifiers.iter().enumerate() {
        let (address, address_seed) = derive_address(
            &[NULLIFIER_PREFIX, nullifier.as_slice()],
            &address_tree_pubkey,
            &crate::ID,
        );

        let nullifier_account = LightAccount::<NullifierAccount>::new_init(
            &crate::ID,
            Some(address),
            data.output_state_tree_index,
        );

        cpi_builder = cpi_builder.with_light_account(nullifier_account)?;
        new_address_params.push(
            data.address_tree_info
                .into_new_address_params_assigned_packed(address_seed, Some(i as u8)),
        );
    }

    cpi_builder
        .with_new_addresses(&new_address_params)
        .invoke(light_cpi_accounts)?;

    Ok(())
}
```

### Program Entry Point

```rust
#[program]
pub mod nullifier {
    pub fn create_nullifier<'info>(
        ctx: Context<'_, '_, '_, 'info, CreateNullifierAccounts<'info>>,
        data: NullifierInstructionData,
        nullifiers: Vec<[u8; 32]>,
    ) -> Result<()> {
        // Verify your ZK proof here. Use nullifiers as public inputs.
        // Example:
        // let public_inputs = [...nullifiers, ...your_other_inputs];
        // Groth16Verifier::new(...).verify()?;

        create_nullifiers(
            &nullifiers,
            data,
            ctx.accounts.signer.as_ref(),
            ctx.remaining_accounts,
        )
    }
}

#[derive(Accounts)]
pub struct CreateNullifierAccounts<'info> {
    #[account(mut)]
    pub signer: Signer<'info>,
}
```

## Client Implementation (TypeScript)

```typescript
const NULLIFIER_PREFIX = Buffer.from("nullifier");
const addressTree = new web3.PublicKey(batchAddressTree);

// Derive addresses for each nullifier
const addressesWithTree = nullifiers.map((nullifier) => {
    const seed = deriveAddressSeedV2([NULLIFIER_PREFIX, nullifier]);
    const address = deriveAddressV2(seed, addressTree, programId);
    return { tree: addressTree, queue: addressTree, address: bn(address.toBytes()) };
});

// Get validity proof (proves addresses don't exist)
const proofResult = await rpc.getValidityProofV0([], addressesWithTree);

// Build remaining accounts
const remainingAccounts = new PackedAccounts();
remainingAccounts.addSystemAccountsV2(SystemAccountMetaConfig.new(programId));
const addressMerkleTreeIndex = remainingAccounts.insertOrGet(addressTree);
const outputStateTreeIndex = remainingAccounts.insertOrGet(outputStateTree);

// Build instruction data
const data = {
    proof: { 0: proofResult.compressedProof },
    addressTreeInfo: {
        addressMerkleTreePubkeyIndex: addressMerkleTreeIndex,
        addressQueuePubkeyIndex: addressMerkleTreeIndex,
        rootIndex: proofResult.rootIndices[0],
    },
    outputStateTreeIndex,
    systemAccountsOffset: systemStart,
};

// Call program
const ix = await program.methods
    .createNullifier(data, nullifiers.map((n) => Array.from(n)))
    .accounts({ signer: signer.publicKey })
    .remainingAccounts(remainingAccounts)
    .instruction();
```

## Client Implementation (Rust)

```rust
use light_sdk::address::v2::derive_address;

let address_tree_info = rpc.get_address_tree_v2();

// Derive addresses
let address_with_trees: Vec<AddressWithTree> = nullifiers
    .iter()
    .map(|n| {
        let (address, _) = derive_address(
            &[NULLIFIER_PREFIX, n.as_slice()],
            &address_tree_info.tree,
            &program_id,
        );
        AddressWithTree {
            address,
            tree: address_tree_info.tree,
        }
    })
    .collect();

// Get validity proof (empty hashes = non-inclusion proof)
let rpc_result = rpc
    .get_validity_proof(vec![], address_with_trees, None)
    .await?
    .value;

// Build accounts
let mut remaining_accounts = PackedAccounts::default();
let config = SystemAccountMetaConfig::new(program_id);
remaining_accounts.add_system_accounts_v2(config)?;

let packed_address_tree_accounts = rpc_result
    .pack_tree_infos(&mut remaining_accounts)
    .address_trees;

let output_state_tree_index = rpc
    .get_random_state_tree_info()?
    .pack_output_tree_index(&mut remaining_accounts)?;
```

## SDK references

| Package | Link |
|---------|------|
| `light-sdk` | [docs.rs](https://docs.rs/light-sdk/latest/light_sdk/) |
| `@lightprotocol/stateless.js` | [API docs](https://lightprotocol.github.io/light-protocol/stateless.js/index.html) |
| `light-client` | [docs.rs](https://docs.rs/light-client/latest/light_client/) |
| `@lightprotocol/nullifier-program` | [npm](https://www.npmjs.com/package/@lightprotocol/nullifier-program) |
| `light-nullifier-program` | [crates.io](https://crates.io/crates/light-nullifier-program) |
| `light-program-test` | [docs.rs](https://docs.rs/crate/light-program-test/latest) |

## Security

This skill provides code patterns and documentation references only.

- **No credentials consumed.** The skill requires no API keys, private keys, or signing secrets. `env: []` is declared explicitly.
- **Subagent scope.** When stuck, the skill asks to spawn a read-only subagent with `Read`, `Glob`, `Grep` scoped to skill references, example repos, and docs.
- **Install source.** `npx skills add Lightprotocol/skills` from [Lightprotocol/skills](https://github.com/Lightprotocol/skills).
- **Audited protocol.** Light Protocol smart contracts are independently audited. Reports are published at [github.com/Lightprotocol/light-protocol/tree/main/audits](https://github.com/Lightprotocol/light-protocol/tree/main/audits).
