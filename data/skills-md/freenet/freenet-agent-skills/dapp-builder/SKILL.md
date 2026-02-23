---
name: dapp-builder
description: Build decentralized applications on Freenet using river as a template. Guides through designing contracts (shared state), delegates (private state), and UI. Use when user wants to create a new Freenet dApp, design contract state, implement delegates, or build a Freenet-connected UI.
license: LGPL-3.0
---

# Freenet Decentralized Application Builder

Build decentralized applications on Freenet following the architecture patterns established in River (decentralized chat).

## How Freenet Applications Work

Freenet is a platform for building decentralized applications that run without centralized servers. Apps rely on a global, peer-to-peer **Key-Value Store** where the "Keys" are cryptographic contracts.

### Core Concept: The Contract is the Key

The "Key" for any piece of data is the **cryptographic hash of the WebAssembly (WASM) code** that controls it.

- This ties the *identity* of the data to its *logic*
- If you change the code (logic), the key changes
- This creates a "Trustless" system: You don't need to trust the node storing the data, because the data is self-verifying against the contract code

## The Three Components of a Freenet App

### 1. The Contract (Network Side)

- **Role:** Acts as the "Backend" or Database
- **Location:** Runs on the public network (untrusted peers)
- **Functionality:**
  - Defines what data (State) is valid
  - Defines how that data can be modified
- **State:** Holds the actual application data (arbitrary bytes)
- **Constraint:** Cannot hold private keys or secrets - all data is public (unless encrypted by the client)

### 2. The Delegate (Local Side)

- **Role:** Acts as the "Middleware" or private agent
- **Location:** Runs locally on the user's device (within the Freenet Kernel)
- **Functionality:**
  - **Trust Zone:** Safely stores secrets, private keys, and user data
  - **Computation:** Performs signing, encryption, and complex logic before sending data to the network
  - **Background Tasks:** Can run continuously to monitor contracts or handle notifications even when the UI is closed

### 3. The User Interface (Frontend)

- **Role:** Interaction layer for the user
- **Location:** Web Browser (SPA) or native app
- **Functionality:**
  - Connects to the local Freenet Kernel via WebSocket/HTTP
  - Built using standard web frameworks (Dioxus, React, Vue, etc.)
  - Agnostic to underlying P2P network complexity

## Data Synchronization & Consistency

Freenet solves "Eventual Consistency" using a specific mathematical requirement:

**Commutative Monoid:** The function that merges updates must be a *commutative monoid*.
- Order Independent: It shouldn't matter what order updates arrive in
- If Peer A merges Update X then Y, and Peer B merges Update Y then X, they must end up with the same result

**Efficiency:** Peers exchange **Summaries** (compact representations) and **Deltas** (patches/diffs) rather than re-downloading full state.

## Advanced Capabilities

- **Subscriptions:** Clients can subscribe to contracts and get notified of changes immediately (real-time apps)
- **Contract Interoperability:** Contracts reading other contracts' state is planned but not yet implemented

---

## Development Workflow

Follow these phases in order:

### Phase 1: Contract Design (Shared State)

Start by defining what state needs to be shared across all users.

**Key questions:**
- What data must all users see consistently?
- How should conflicts be resolved when two users update simultaneously?
- What cryptographic verification is needed?
- What are the state components and their relationships?

**Implementation steps:**
1. Define state structure using `#[composable]` macro from freenet-scaffold
2. Implement `ComposableState` trait for each component
3. Implement `ContractInterface` trait for the contract
4. Ensure all state updates satisfy the commutative monoid requirement

Reference: `references/contract-patterns.md`

### Phase 2: Delegate Design (Private State)

Determine what private data each user needs stored locally.

**Key questions:**
- What user-specific data needs persistence? (keys, preferences, cached data)
- What signing/encryption operations are needed?
- What permissions are needed for sensitive operations?

**Implementation steps:**
1. Define request/response message types
2. Implement `DelegateInterface` trait
3. Handle secret storage operations (Store, Get, Delete, List)
4. Implement cryptographic operations (signing, encryption)

Reference: `references/delegate-patterns.md`

### Phase 3: UI Design

Build the user interface connecting to contracts and delegates.

**Key questions:**
- What components/views does the app need?
- How should state synchronization work?
- What's the user flow for key operations?

**Implementation steps:**
1. Set up Dioxus project with WASM target
2. Implement WebSocket connection to Freenet gateway
3. Create synchronizer for contract state subscriptions
4. Implement delegate communication for private storage
5. Build reactive UI components

Reference: `references/ui-patterns.md`

### Phase 4: Build and Deploy

Set up the build system and deployment pipeline.

Reference: `references/build-system.md`

## Project Structure Template

```
my-dapp/
├── common/                    # Shared types between contract/delegate/UI
│   └── src/
│       ├── lib.rs
│       └── state/            # State definitions
├── contracts/
│   └── my-contract/
│       ├── Cargo.toml
│       └── src/lib.rs        # ContractInterface implementation
├── delegates/
│   └── my-delegate/
│       ├── Cargo.toml
│       └── src/lib.rs        # DelegateInterface implementation
├── ui/
│   ├── Cargo.toml
│   ├── Dioxus.toml
│   └── src/
│       ├── main.rs
│       └── components/
├── Cargo.toml                # Workspace root
└── Makefile.toml             # cargo-make build tasks
```

## Reference Project

[River](https://github.com/freenet/river) demonstrates all patterns:
- Contracts: `contracts/room-contract/`
- Delegates: `delegates/chat-delegate/`
- UI: `ui/`
- Common types: `common/`

## Key Dependencies

```toml
# For contracts
freenet-stdlib = { version = "0.1", features = ["contract"] }
freenet-scaffold = "0.1"

# For delegates
freenet-stdlib = { version = "0.1", features = ["delegate"] }

# For UI
dioxus = "0.7"
freenet-stdlib = "0.1"
```

---

## Improving This Skill

This skill is designed to be self-improving. When encountering issues while using this skill, agents should file GitHub issues or submit PRs to improve it.

### When to File an Issue

File an issue at `freenet/freenet-agent-skills` when:
- Instructions are unclear or ambiguous
- Information is missing for a common use case
- Code examples don't compile or are outdated
- Patterns don't match current River implementation
- A referenced API has changed

### How to File an Issue

```bash
gh issue create --repo freenet/freenet-agent-skills \
  --title "dapp-builder: <brief description>" \
  --body "## Problem
<describe what was unclear or incorrect>

## Context
<what were you trying to accomplish>

## Suggested Improvement
<optional: how the skill could be improved>"
```

### Submitting a PR

For concrete improvements:

```bash
# Clone and create branch
gh repo clone freenet/freenet-agent-skills
cd freenet-agent-skills
git checkout -b improve-<topic>

# Make changes to dapp-builder/SKILL.md or references/*.md
# ... edit files ...

# Submit PR
git add -A && git commit -m "dapp-builder: <description>"
gh pr create --title "dapp-builder: <description>" \
  --body "## Changes
<describe improvements>

## Reason
<why this helps>"
```

### What Makes a Good Improvement

- Fixes factual errors or outdated information
- Adds missing patterns discovered while building a dApp
- Clarifies confusing instructions based on real usage
- Adds test examples that would have helped
- Updates code to match current Freenet/River APIs
