---
name: orthotect-context
description: Master AI coding agent context window efficiency, progressive file disclosure, and semantic chunking. Enforces zero-scan starts, 3-tier progressive reading (skeleton → line discovery → surgical slice), parallel multi-tool fan-out, heavy directory isolation, and token budget management without degrading architectural context. Works across all autonomous agent platforms (Antigravity, Claude Code, Codex, Cursor) for beginners and senior engineers alike.
---

# Orthotect Context Architecture & Token Optimization

The house standard for maximizing autonomous AI coding agent efficiency, preventing token bloat, accelerating turn-by-turn velocity, and eliminating context pollution.

## The 5 Laws of Token-Conscious Agent Context

### Law 1: Zero-Scan Grounding (Index-First Navigation)
Never run recursive directory dumps or unbounded file tree traversals.
- Ground agent intent using project index files (`README.md`, `package.json`, `MANIFESTO.md`, or `AGENTS.md`) before running discovery commands.
- Run `orthotect context skeleton <dir>` to load a compact architectural symbol map mapping symbols to exact lines.

### Law 2: 3-Tier Progressive Disclosure
Never read an entire file over 120 lines when inspecting or modifying isolated logic. Always use the 3-tier funnel:
- **Tier 1 - Directory Skeleton:** Single-level directory check (`list_dir` or `ls`).
- **Tier 2 - Line Discovery:** Targeted grep (`grep_search` or `grep -n "symbol" <file>`) to pinpoint line numbers.
- **Tier 3 - Surgical Slice Read:** Read only a 40–80 line window (`StartLine` to `EndLine`).
- *Safety Guard:* Read top 25 lines once if file-level imports or global state are required.

### Law 3: Parallel Grouped Fan-Out
Eliminate sequential turn latency by emitting all independent file reads, searches, and syntax checks in a single turn.
- Inspecting 3 components? Emit 3 read calls in parallel.
- Shell diagnostics? Group checks into a single command with line caps (`head -n 40 file1 && tail -n 40 log2`).

### Law 4: Output Capping & Boundary Isolation
Heavy directories and unbounded logs must never enter the active context window.
- Always ignore: `node_modules`, `.git`, `dist`, `build`, `__pycache__`, `coverage`.
- Pipe shell outputs through `head -n 50` or `tail -n 50`.
- Return structured diff summaries (`git diff --stat`) rather than thousands of lines of raw compiler output.

### Law 5: Semantic Chunking & Modular Decomposition
Decompose multi-thousand line files along architectural boundaries:
- Use `orthotect context chunk <file> --max-tokens 500` to split large files at class, function, or FSM boundaries.
- Never sever closures, JSX element trees, or active state transitions mid-block.

---

## Actionable Prompts & Blueprints

### For Beginners
> "Analyze this task using Orthotect Context rules: locate the exact lines with grep first, read only the 50 lines surrounding the target, make the minimal surgical edit, and verify with tests without reading the entire repo."

### For Senior Engineers & Orchestrators
> "Run `orthotect context inspect <target>` to derive token density. If tokens exceed 1,000, generate an architectural skeleton via `orthotect context skeleton` and execute changes through progressive surgical slices."

---

## Verification Command
```bash
python3 core/context_optimizer.py inspect <path>
node bin/orthotect.js context skeleton <dir>
```
