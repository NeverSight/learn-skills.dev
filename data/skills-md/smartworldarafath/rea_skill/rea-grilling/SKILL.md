---
name: rea-grilling
description: Grill the user relentlessly about a reverse engineering, lost source code recovery, binary triage, web/mobile security audit, or asset extraction plan before writing code. Use when the user asks to scope, plan, or stress-test an REA task, or uses trigger phrases like 'grill me', 'scope this', 'interview me', or 'plan recovery'.
---

# REA Grilling: Interactive Target & Scope Interrogation Engine

Interview the user relentlessly until you reach a crystal-clear, shared understanding of the target, constraints, and success criteria. Map the investigation as a **decision tree**: every engineering decision branches into lower-level technical choices.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask *now* without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before moving to the next round.

Format each round like this:

```markdown
❓ **Q1** - **<question title>**: <question body with clear context and available choices>

➡️ **Recommended**: <your recommended technical answer based on initial artifact inspection>

---

❓ **Q2** - **<question title>**: <question body with clear context and available choices>

➡️ **Recommended**: <your recommended technical answer based on initial artifact inspection>
```

**Crucial Rules:**
1. **The "Yes" Rule:** Word each question and recommendation so that if the user simply replies `"yes"`, it accepts all of your recommended answers for that round.
2. **Finding Facts is Your Job:** Never ask the user for facts you can determine yourself using tools (`readelf`, `DIE`, `strings`, `open_binary`, `inspect_pe_resources`, `grep`, `file`). Inspect the target first, discover the compilers/architecture/frameworks, and then grill the user only on *intent*, *fidelity*, and *scope trade-offs*.
3. **No Skeletons Guarantee:** Once the grilling interview concludes and all frontier branches are settled, compile the final agreed specification and immediately execute the 5-Stage REA Pipeline under the **Zero-Skeleton Law**.

---

## The REA Decision Tree Frontier

When interrogating a reverse engineering or recovery target, compute questions across these frontier branches:

### Branch 1: Scope & Recovery Fidelity
- **Full Idiomatic Rewrite vs. Byte-Exact Decompilation:** Do you require 100% byte-exact binary matching, or clean, modern, idiomatic source code (e.g., C++20 / Rust / Go) that compiles cleanly and reproduces the exact feature behavior?
- **Feature Prioritization:** Are all UI modules, background workers, and protocols required, or is there a specific core subsystem to reconstruct first?

### Branch 2: Toolchain & Compiler Targeting
- **Target Compiler:** Which compiler toolchain should the 1-click build script support?
  - Options: Zig CC (`zig cc`), MSVC (`cl.exe`), MinGW GCC, Clang, Cargo, Gradle, Go.
- **Dependency Strategy:** Should third-party libraries (e.g., SQLite, zlib, OpenSSL, ImGui) be vendor-bundled, dynamically linked, or fetched via package managers (vcpkg, Conan, Cargo)?

### Branch 3: Resource & Asset Extraction Depth
- **Embedded Assets:** Should binary resources be extracted as loose editable files (valid `.ico`, `.png`, `.wav`, `.glsl`, `.ttf`) or linked directly into a compiled `.rc` resource file?
- **Database & Storage Schemas:** Should SQLite/Realm schemas be emitted as raw SQL migration files (`schema.sql`) or mapped to ORM / typed data models?

### Branch 4: Security & Sensitive Artifact Handling
- **Secret Sanitization:** When analyzing decompiled code or web bundles, how should extracted API keys, tokens, or credentials be handled?
  - Options: Auto-sanitize into `.env.example` templates, replace with mock test fixtures, or quarantine securely.
- **Vulnerability Remediation:** Should the output include direct inline code patches (remediations) alongside the vulnerability report?

### Branch 5: Verification & Acceptance Gates
- **Acceptance Criteria:** What constitutes proof of 100% successful recovery?
  - Options: 0 compilation errors and 0 warnings via `build.bat` / `build.sh`, successful automated unit/smoke tests, dynamic GUI launch test, or diff coverage against original binary exports.

---

## Interview Execution Flow

1. **Initial Artifact Triage (Silent Fact-Finding):**
   - Run REA MCP or local inspection tools to determine: file format, architecture (x86/x64/ARM64), packing/obfuscation, compiler signature, and symbol status.
2. **Round 1 (Target Scope & Fidelity):**
   - Present findings from fact-finding.
   - Ask Round 1 frontier questions (Scope, Language/Compiler target, Fidelity level) with your recommended answers.
3. **Round 2 (Toolchains, Resources & Edge Cases):**
   - Unblock dependent questions based on Round 1 answers.
   - Address dependencies, asset extraction, database reconstruction, and secret handling.
4. **Round 3 (Verification & Final Handoff):**
   - Finalize build scripts, test harness requirements, and acceptance criteria.
5. **Execution Gate:**
   - Summarize the settled **Recovery Specification**.
   - Hand off to `$rea-full-code-recovery` or the matching domain skill to reconstruct the complete codebase without any skeletons or stubs.
