---
name: swiftzilla
description: >-
  Swift/iOS static analysis CLI. Use `depgraph` to find who calls a function,
  what breaks if you change a file, track call sites and blast radius before
  refactoring, and map symbol dependencies across files. Use `ask` to consult
  Swift/iOS/tvOS/watchOS/macOS documentation and best practices.
license: Proprietary
compatibility: Requires macOS 13+. The binary is a universal macOS executable (arm64 + x86_64).
metadata:
  author: SwiftZilla
  version: "595b091"
---

# SwiftZilla Skill Instructions

You are equipped with the **SwiftZilla** CLI, a static analysis and knowledge base tool for Swift/iOS projects. 

**CRITICAL INSTRUCTION**: Do NOT guess command arguments or syntax. You MUST follow the progressive disclosure steps below based on the user's intent.

## Step 1: Determine the User's Intent

Analyze the user's request to choose the appropriate tool:

*   **IF** the user wants to know who calls a function, what breaks if a file changes, the blast radius of a refactor, or symbol dependencies:
    *   **ACTION**: You need the **`depgraph`** tool. Proceed immediately to Step 2A.
*   **IF** the user asks a question about Swift, iOS, tvOS, watchOS, macOS best practices, implementation patterns, or architecture:
    *   **ACTION**: You need the **`ask`** tool. Proceed immediately to Step 2B.

## Step 2: Read Tool Reference (Progressive Disclosure)

Before executing any commands, you MUST read the specific reference file to understand the exact syntax and expected outputs.

### Step 2A: Using `depgraph`
1. Use your file reading tool to read `{workspace_or_agent_folder}/swiftzilla/scripts/references/depgraph.md`.
2. Understand the required command structure (`depgraph index` or `depgraph impact`).
3. Ensure the `swiftzilla` binary at `{workspace_or_agent_folder}/swiftzilla/scripts/swiftzilla` is executable (`chmod +x`).
4. Execute the command as specified in the reference.
5. Parse the output exactly as instructed in the reference to answer the user's request.

### Step 2B: Using `ask`
1. Use your file reading tool to read `{workspace_or_agent_folder}/swiftzilla/scripts/references/ask.md`.
2. Understand the required command structure (`ask "query"`).
3. Ensure the `swiftzilla` binary at `{workspace_or_agent_folder}/swiftzilla/scripts/swiftzilla` is executable (`chmod +x`).
4. Execute the command as specified in the reference.
5. Return the exact knowledge base answer to the user.

## execution guidelines

*   **No prose**: Do not output conversational filler. Execute commands directly.
*   **Pathing**: The `swiftzilla` executable is located relative to the workspace at `swiftzilla/scripts/swiftzilla`.
*   **Errors**: If the CLI returns an error, analyze the error message. If it involves missing files, verify the file paths. If it involves missing API keys, check the `ask` reference. Do not ask the user for help unless you cannot resolve the syntax or environment issue.
