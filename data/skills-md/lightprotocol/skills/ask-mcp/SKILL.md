---
name: ask-mcp
description: "For questions about Light Protocol's SDK, smart contracts and Solana development, Claude Code features, or agent skills. AI-powered answers grounded in repository context via DeepWiki MCP."
metadata:
  source: https://github.com/Lightprotocol/skills
  documentation: https://www.zkcompression.com
  openclaw:
    requires:
      env: []
      bins: []
allowed-tools:
  - Read
  - Glob
  - Grep
  - Task
  - WebFetch(https://zkcompression.com/*)
  - WebFetch(https://github.com/Lightprotocol/*)
  - WebSearch
  - mcp__deepwiki__read_wiki_structure
  - mcp__deepwiki__read_wiki_contents
  - mcp__deepwiki__ask_question
  - mcp__zkcompression__SearchLightProtocol
---

# DeepWiki Research

Query repositories via DeepWiki MCP to answer technical questions with precise, source-backed answers.

## Workflow

1. **Understand the question**
   - Identify what the user is asking and which domain it falls into
   - If the question is ambiguous, state your understanding and ask for clarification
2. **Gather context**
   - Match question to the [execution steps](#execution-steps) below
   - Use `Glob`, `Grep`, and `Read` to find relevant local files
   - Query DeepWiki MCP (`mcp__deepwiki__ask_question`) and `mcp__zkcompression__SearchLightProtocol` for repository-level context
   - Use `Task` subagents for parallel research across multiple repos when needed
3. **Synthesize and respond**
   - Apply [precision rules](#4-apply-precision-rules) to the answer
   - Format per [format response](#5-format-response)

## Execution Steps

### 1. Read required context in local repo

Use `Glob` and `Grep` to locate relevant files in the current repository. Use `Read` to pull in specific content needed to answer the question.

### 2. Identify question scope

Determine the domain:
- Programs, client SDKs, architecture, implementation details
- Specific components (LightAccount, ValidityProof, CPI, etc.)

### 3. Fetch repository context

Select the appropriate repository based on question scope:

**Light Protocol (compressed accounts, state trees, ZK compression, Light SDK)**
```
mcp__deepwiki__read_wiki_structure("Lightprotocol/light-protocol")
mcp__deepwiki__read_wiki_contents("Lightprotocol/light-protocol")
mcp__deepwiki__ask_question("Lightprotocol/light-protocol", "your question")
```

**Solana Development (programs, accounts, general Solana)**
```
mcp__deepwiki__read_wiki_structure("blueshift-gg/blueshift-dashboard")
mcp__deepwiki__read_wiki_contents("blueshift-gg/blueshift-dashboard")
mcp__deepwiki__ask_question("blueshift-gg/blueshift-dashboard", "your question")
```

**Claude Code (CLI features, commands, configuration)**
```
mcp__deepwiki__read_wiki_structure("anthropics/claude-code")
mcp__deepwiki__read_wiki_contents("anthropics/claude-code")
mcp__deepwiki__ask_question("anthropics/claude-code", "your question")
```

**Agent Skills (skills, subagents, patterns)**
```
mcp__deepwiki__read_wiki_structure("anthropics/skills")
mcp__deepwiki__read_wiki_contents("anthropics/skills")
mcp__deepwiki__ask_question("anthropics/skills", "your question")
```

### 4. Apply precision rules

**AVOID:**
- Vague verbs: "handles", "manages", "processes", "enables", "provides"
- Abstract nouns: "operations", "management", "coordination"
- -ing endings when a precise verb exists
- Marketing language: "comprehensive", "rich", "seamless",  "enables", "provides capability"
- ZK terminology in user-facing docs: "inclusion proof", "non-inclusion proof" → Instead describe what it does: "prove the address doesn't exist", "prove the account hash exists"
- Generic descriptions: "account metadata" instead of "CompressedAccountMeta"


**USE:**
- Exact function/method names
- Concrete data structures
- Specific operations: "sets discriminator", "creates hash", "nullifies account"
- File:line references
- "reference" when describing u8 indices that reference accounts in the accounts array (standard Solana terminology)
- "CPI" as a verb (e.g., "CPIs the Account Compression Program")
- Technical method/function names used as verbs when contextually clear

`Describe exactly what happens.`

### 5. Format response

Structure answers with:
- Technical precision
- Code examples with inline comments
- Source references (file paths, line numbers)

## Example Output

**Question:** What do you include in instruction data for compressed account creation?

**Answer:**

---

## Compressed Account Creation Instruction Data

Instruction data contains three components for proof verification and tree coordination.

**Components:**

```rust
pub struct InstructionData {
    proof: ValidityProof,
    address_tree_info: PackedAddressTreeInfo,
    output_state_tree_index: u8,
    // + custom account data
}
```

**1. Non-inclusion proof**
- `ValidityProof` proves the derived address does not exist in the specified address tree
- Client generates via `getValidityProof()` RPC call

**2. Tree location parameters**
- `PackedAddressTreeInfo`: Specifies which address tree registers the address (u8 index, not pubkey)
- `output_state_tree_index`: Specifies which state tree stores the compressed account hash

**3. Custom account data**
- Program-specific fields (e.g., `message: String`, user data)

**Execution flow:**

1. Address tree proves uniqueness, stores address
2. State tree stores account hash
3. ValidityProof cryptographically guarantees address is unused

**Why separate trees:**

Compressed accounts require client-generated cryptographic proof that address doesn't exist (unlike regular Solana where runtime checks PDA existence). Address trees enforce uniqueness; state trees store account hashes.

**Packed structs** use `u8` indices to reference accounts in `remaining_accounts`, reducing transaction size.

## Security

This skill does not pull, store, or transmit external secrets. It provides code patterns, documentation references, and development guidance only.

- **No credentials consumed.** The skill requires no API keys, private keys, or signing secrets. `env: []` is declared explicitly.
- **DeepWiki MCP accesses public repositories only.** All `mcp__deepwiki__*` calls query public GitHub repositories (Lightprotocol/light-protocol, anthropics/claude-code, anthropics/skills). No authentication tokens are required or transmitted. DeepWiki does not access private repositories unless explicitly configured with a token — this skill does not configure one.
- **User-provided configuration.** RPC endpoints, wallet keypairs, and authentication tokens (Privy, wallet adapters) are configured in the user's own application code — the skill only demonstrates how to use them.
- **Tool boundary enforced.** The `allowed-tools` list restricts this skill to read-only operations (`Read`, `Glob`, `Grep`), research subagents (`Task`), web fetches to Light Protocol domains, and MCP queries. It cannot load other skills, write files, or execute shell commands. Verify the `allowed-tools` list in the frontmatter above matches these constraints.
- **Install source.** `npx skills add Lightprotocol/skills` installs from the public GitHub repository ([Lightprotocol/skills](https://github.com/Lightprotocol/skills)). Verify the source before running.
- **Audited protocol.** Light Protocol smart contracts are independently audited. Reports are published at [github.com/Lightprotocol/light-protocol/tree/main/audits](https://github.com/Lightprotocol/light-protocol/tree/main/audits).
