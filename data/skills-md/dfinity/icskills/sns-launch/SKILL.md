---
name: sns-launch
description: "Configure and launch an SNS DAO to decentralize a dapp. Covers token economics, governance parameters, testflight validation, NNS proposal submission, and decentralization swap. Use when launching an SNS, configuring tokenomics, or setting up DAO governance for a dapp. Do NOT use for NNS governance or general canister management."
license: Apache-2.0
compatibility: "icp-cli >= 0.1.0, dfx with sns extension"
metadata:
  title: SNS DAO Launch
  category: Governance
---

# SNS DAO Launch

## What This Is

Service Nervous System (SNS) is the DAO framework for decentralizing individual Internet Computer dapps. Like the NNS governs the IC network itself, an SNS governs a specific dapp -- token holders vote on proposals to upgrade code, manage treasury funds, and set parameters. Launching an SNS transfers canister control from developers to a community-owned governance system through a decentralization swap.

## Prerequisites

- An NNS neuron with sufficient stake to submit proposals (mainnet)
- Dapp canisters already deployed and working on mainnet
- `sns_init.yaml` configuration file with all parameters defined

## Canister IDs

| Canister | Mainnet ID | Purpose |
|----------|-----------|---------|
| NNS Governance | `rrkah-fqaaa-aaaaa-aaaaq-cai` | Votes on SNS creation proposals |
| SNS-W (Wasm Modules) | `qaa6y-5yaaa-aaaaa-aaafa-cai` | Deploys and initializes SNS canisters |
| NNS Root | `r7inp-6aaaa-aaaaa-aaabq-cai` | Must be co-controller of dapp before launch |
| ICP Ledger | `ryjl3-tyaaa-aaaaa-aaaba-cai` | Handles ICP token transfers during swap |

## SNS Canisters Deployed

When an SNS launch succeeds, SNS-W deploys these canisters on an SNS subnet:

| Canister | Purpose |
|----------|---------|
| **Governance** | Proposal submission, voting, neuron management |
| **Ledger** | SNS token transfers (ICRC-1 standard) |
| **Root** | Sole controller of all dapp canisters post-launch |
| **Swap** | Runs the decentralization swap (ICP for SNS tokens) |
| **Index** | Transaction indexing for the SNS ledger |
| **Archive** | Historical transaction storage |

## Mistakes That Break Your Build

1. **Setting `min_participants` too high.** If you require 500 participants but only 200 show up, the entire swap fails and all ICP is refunded. Start conservative -- most successful SNS launches use 100-200 minimum participants.

2. **Forgetting to add NNS Root as co-controller before proposing.** The launch process requires NNS Root to take over your canisters. If you submit the proposal without adding it first, the launch will fail at stage 6 when SNS Root tries to become sole controller.

3. **Not testing on SNS testflight first.** Going straight to mainnet means discovering configuration issues after your NNS proposal is live. Always deploy a testflight mock SNS on mainnet first to verify governance and upgrade flows.

4. **Token economics that fail NNS review.** The NNS community votes on your proposal. Unreasonable tokenomics (excessive developer allocation, zero vesting, absurd swap caps) will get rejected. Study successful SNS launches (OpenChat, Hot or Not, Kinic) for parameter ranges the community accepts.

5. **Not defining fallback controllers.** If the swap fails, the dapp needs controllers to return control to. Without `fallback_controller_principals`, your dapp could become uncontrollable.

6. **Setting swap duration too short.** Users across time zones need time to participate. Less than 24 hours is risky -- 3-7 days is standard.

7. **Forgetting restricted proposal types during swap.** Six governance proposal types are blocked while the swap runs: `ManageNervousSystemParameters`, `TransferSnsTreasuryFunds`, `MintSnsTokens`, `UpgradeSnsControlledCanister`, `RegisterDappCanisters`, `DeregisterDappCanisters`. Do not plan operations that require these during the swap window.

8. **Developer neurons with zero dissolve delay.** Developers can immediately dump tokens post-launch. Set dissolve delays and vesting periods (12-48 months is typical) to signal long-term commitment.

## Implementation

### SNS Configuration File (sns_init.yaml)

This is the single source of truth for all launch parameters. Copy the template from the `dfinity/sns-testing` repo and customize:

```yaml
# Note: numeric values are in e8s (1 token = 100_000_000 e8s). Time values are in seconds.

# === PROJECT METADATA ===
name: MyProject
description: >
  A decentralized application for [purpose].
  This proposal requests the NNS to create an SNS for MyProject.
logo: logo.png
url: https://myproject.com

# === NNS PROPOSAL TEXT ===
NnsProposal:
  title: "Proposal to create an SNS for MyProject"
  url: "https://forum.dfinity.org/t/myproject-sns-proposal/XXXXX"
  summary: >
    This proposal creates an SNS DAO to govern MyProject.
    Token holders will control upgrades, treasury, and parameters.

# === FALLBACK (if swap fails, these principals regain control) ===
fallback_controller_principals:
  - YOUR_PRINCIPAL_ID_HERE

# === CANISTER IDS TO DECENTRALIZE ===
dapp_canisters:
  - BACKEND_CANISTER_ID
  - FRONTEND_CANISTER_ID

# === TOKEN CONFIGURATION ===
Token:
  name: MyToken
  symbol: MYT
  transaction_fee: 0.0001 tokens
  logo: token_logo.png

# === GOVERNANCE PARAMETERS ===
Proposals:
  rejection_fee: 1 token
  initial_voting_period: 4 days
  maximum_wait_for_quiet_deadline_extension: 1 day

Neurons:
  minimum_creation_stake: 1 token

Voting:
  minimum_dissolve_delay: 1 month
  MaximumVotingPowerBonuses:
    DissolveDelay:
      duration: 8 years
      bonus: 100%                            # 2x voting power at max dissolve
    Age:
      duration: 4 years
      bonus: 25%
  RewardRate:
    initial: 2.5%
    final: 2.5%
    transition_duration: 0 seconds

# === TOKEN DISTRIBUTION ===
Distribution:
  Neurons:
    # Developer allocation (with vesting)
    - principal: DEVELOPER_PRINCIPAL
      stake: 2_000_000 tokens
      memo: 0
      dissolve_delay: 6 months
      vesting_period: 24 months

    # Seed investors
    - principal: INVESTOR_PRINCIPAL
      stake: 500_000 tokens
      memo: 1
      dissolve_delay: 3 months
      vesting_period: 12 months

  InitialBalances:
    treasury: 5_000_000 tokens               # Treasury (controlled by DAO)
    swap: 2_500_000 tokens                   # Sold during decentralization swap

  total: 10_000_000 tokens                   # Must equal sum of all allocations

# === DECENTRALIZATION SWAP ===
Swap:
  minimum_participants: 100
  minimum_direct_participation_icp: 50_000 tokens
  maximum_direct_participation_icp: 500_000 tokens
  minimum_participant_icp: 1 token
  maximum_participant_icp: 25_000 tokens
  duration: 7 days
  neurons_fund_participation: true

  VestingSchedule:
    events: 5                                # Neurons unlock in 5 stages
    interval: 3 months

  confirmation_text: >
    I confirm that I am not a resident of a restricted jurisdiction
    and I understand the risks of participating in this token swap.

  restricted_countries:
    - US
    - CN
```

### Launch Process (11 Stages)

```
Stage 1:  Developer defines parameters in sns_init.yaml
Stage 2:  Developer adds NNS Root as co-controller of dapp canisters
Stage 3:  Developer submits NNS proposal using `dfx sns propose`
Stage 4:  NNS community votes on the proposal
Stage 5:  (If adopted) SNS-W deploys uninitialized SNS canisters
Stage 6:  SNS Root becomes sole controller of dapp canisters
Stage 7:  SNS-W initializes canisters in pre-decentralization-swap mode
Stage 8:  24-hour minimum wait before swap opens
Stage 9:  Decentralization swap opens (users send ICP, receive SNS neurons)
Stage 10: Swap closes (time expires or maximum ICP reached)
Stage 11: Finalization (exchange rate set, neurons created, normal mode)
```

### Motoko

Prepare your canister for SNS control. The key requirement is that your canister accepts upgrade proposals from SNS governance:

```motoko
import Principal "mo:core/Principal";
import Runtime "mo:core/Runtime";

persistent actor {
  // SNS Root will be set as sole controller after launch.
  // Your canister code does not need to change -- SNS governance
  // controls upgrades via the standard canister management API.

  // If your canister has admin functions, transition them to
  // accept SNS governance proposals instead of direct principal checks:

  var snsGovernanceId : ?Principal = null;

  // ⚠ SECURITY: This setter MUST be access-controlled. Without a check, any caller
  // can front-run you and set themselves as governance, permanently locking you out.
  // Replace DEPLOYER_PRINCIPAL with your actual principal or use an admin list.
  public shared ({ caller }) func setSnsGovernance(id : Principal) : async () {
    // Only the deployer (or canister controllers) should call this.
    assert (Principal.isController(caller));

    switch (snsGovernanceId) {
      case (null) { snsGovernanceId := ?id };
      case (?_) { Runtime.trap("SNS governance already set") };
    };
  };

  func requireGovernance(caller : Principal) {
    switch (snsGovernanceId) {
      case (?gov) {
        if (caller != gov) { Runtime.trap("Only SNS governance can call this") };
      };
      case (null) { Runtime.trap("SNS governance not configured") };
    };
  };

  // Admin functions become governance-gated:
  public shared ({ caller }) func updateConfig(newFee : Nat) : async () {
    requireGovernance(caller);
    // ... apply config change
  };
};
```

### Rust

```rust
use candid::{CandidType, Deserialize, Principal};
use ic_cdk::{init, post_upgrade, query, update};
use std::cell::RefCell;

#[derive(CandidType, Deserialize, Clone)]
struct Config {
    sns_governance: Option<Principal>,
}

thread_local! {
    // ⚠ STATE LOSS: RefCell<T> in thread_local! is HEAP storage — it is wiped on every
    // canister upgrade. In production, use ic-stable-structures (StableCell or StableBTreeMap)
    // to persist this across upgrades. At minimum, implement #[pre_upgrade]/#[post_upgrade]
    // hooks to serialize/deserialize this data. Without that, an upgrade erases your
    // governance config and locks out SNS control.
    static CONFIG: RefCell<Config> = RefCell::new(Config {
        sns_governance: None,
    });
}

fn require_governance(caller: Principal) {
    CONFIG.with(|c| {
        let config = c.borrow();
        match config.sns_governance {
            Some(gov) if gov == caller => (),
            Some(_) => ic_cdk::trap("Only SNS governance can call this"),
            None => ic_cdk::trap("SNS governance not configured"),
        }
    });
}

// ⚠ SECURITY: This setter MUST be access-controlled. Without a check, any caller
// can front-run you and set themselves as governance, permanently locking you out.
#[update]
fn set_sns_governance(id: Principal) {
    // Only canister controllers should call this.
    if !ic_cdk::api::is_controller(&ic_cdk::api::msg_caller()) {
        ic_cdk::trap("Only canister controllers can set governance");
    }
    CONFIG.with(|c| {
        let mut config = c.borrow_mut();
        if config.sns_governance.is_some() {
            ic_cdk::trap("SNS governance already set");
        }
        config.sns_governance = Some(id);
    });
}

#[update]
fn update_config(new_fee: u64) {
    let caller = ic_cdk::api::msg_caller();
    require_governance(caller);
    // ... apply config change
}
```

**Cargo.toml dependencies:**

```toml
[package]
name = "sns_dapp_backend"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
candid = "0.10"
ic-cdk = "0.19"
serde = { version = "1", features = ["derive"] }
```

## Deploy & Test

### Local Testing with sns-testing

```bash
# Clone the SNS testing repository
git clone https://github.com/dfinity/sns-testing.git
cd sns-testing

# WARNING: starting a fresh network wipes all local canister data. Only use for fresh setup.
icp network start -d

# Deploy NNS canisters locally (includes governance, ledger, SNS-W)
# Note: Use the sns-testing repo's setup scripts for NNS + SNS-W canister installation.
# See https://github.com/dfinity/sns-testing for current instructions.

# Deploy your dapp canisters
icp deploy my_backend
icp deploy my_frontend

# Deploy a testflight SNS locally using your config
# Use the sns-testing repo tooling to deploy a local testflight SNS.
# See sns-testing README for the current testflight workflow.
```

### Mainnet Testflight (Mock SNS)

```bash
# Deploy a mock SNS on mainnet to test governance flows
# This does NOT do a real swap -- it creates a mock SNS you control
# Use the sns-testing repo tooling for mainnet testflight deployment.
# See https://github.com/dfinity/sns-testing for the current testflight workflow.

# Test submitting proposals, voting, and upgrading via SNS governance
```

### Mainnet Launch (Real)

```bash
# Step 1: Add NNS Root as co-controller of each dapp canister
# Requires dfx sns extension: `dfx extension install sns`
dfx sns prepare-canisters add-nns-root BACKEND_CANISTER_ID --network ic
dfx sns prepare-canisters add-nns-root FRONTEND_CANISTER_ID --network ic

# Step 2: Validate your config locally before submitting
dfx sns init-config-file validate
# Or review the rendered proposal by inspecting the yaml output carefully.
# You can also test the full flow on a local replica first (see Local Testing above).

# Step 3: Submit the proposal (THIS IS IRREVERSIBLE — double-check your config)
dfx sns propose --network ic --neuron $NEURON_ID sns_init.yaml
```

## Verify It Works

### After local testflight deployment:

```bash
# List deployed SNS canisters
icp canister id sns_governance
icp canister id sns_ledger
icp canister id sns_root
icp canister id sns_swap

# Verify SNS governance is operational
icp canister call sns_governance get_nervous_system_parameters '()'
# Expected: returns the governance parameters you configured

# Verify token distribution
icp canister call sns_ledger icrc1_total_supply '()'
# Expected: matches your total token supply

# Verify dapp canister controllers changed
icp canister status BACKEND_CANISTER_ID
# Expected: controller is the SNS Root canister, NOT your principal

# Test an SNS proposal (upgrade your canister via governance)
icp canister call sns_governance manage_neuron '(record { ... })'
# Expected: proposal created, can be voted on
```

### After mainnet launch:

```bash
# Check swap status
icp canister call SNS_SWAP_ID get_state '()' -e ic
# Expected: shows swap status, participation count, ICP raised

# Check SNS governance
icp canister call SNS_GOVERNANCE_ID get_nervous_system_parameters '()' -e ic
# Expected: returns your configured parameters

# Verify dapp controller is SNS Root
icp canister status BACKEND_CANISTER_ID -e ic
# Expected: single controller = SNS Root canister ID
```
