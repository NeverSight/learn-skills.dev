---
name: codebase-analysis
description: "TRIGGER when user asks to analyze, document, understand, or review a codebase or code module. Use when user wants to: generate technical docs, trace data flow, analyze algorithms, document data structures, understand architecture, or review code logic. Triggers on: 'analyze code', 'codebase analysis', 'document this code', 'understand this project', 'trace data flow', '算法分析', '代码分析', '代码梳理', '数据结构分析', '技术文档'. DO NOT trigger for: simple file reading, single-function explanation, general coding questions."
level: 3
version: "2.1"
triggers:
  - "codebase analysis"
  - "analyze codebase"
  - "代码分析"
  - "代码梳理"
  - "数据结构分析"
  - "algorithm flow"
argument-hint: "<target_directory_or_module>"
---

# Codebase Analysis Skill

**Purpose**: Perform rigorous, code-based analysis of software projects to generate comprehensive technical documentation similar to the fastlivo2-tech-docs reference style.

## What This Skill Does

This skill systematically analyzes a codebase and produces detailed markdown documentation covering:

1. **System Overview** (系统概述) - Architecture, modules, and relationships
2. **Data Structures** (数据结构详解) - Detailed breakdown of all key data structures
3. **Data Flow** (数据流分析) - How data moves through the system
4. **Algorithm Flows** (算法流程) - Core algorithms with step-by-step analysis
5. **Key Functions** (关键函数分析) - Deep dive into critical functions

**Key Principle**: All analysis is strictly based on actual code - no hallucinations, no assumptions without verification.

## When to Use

Invoke this skill when you need to:
- Understand a complex codebase systematically
- Create technical documentation for a project
- Analyze data structures and their relationships
- Trace data flow and algorithms
- Generate codebase reference materials
- Review and document architecture decisions

## Output Format

Each analysis module generates a corresponding `.md` file with:
- Code references with file:line:column citations
- ASCII diagrams for visualization
- Verification checkpoints
- Cross-references between documents
- Consistent structure across all documents

## Usage

```
/codebase-analysis <target_directory>
/codebase-analysis src/core
/codebase-analysis --module=StateEstimator
```

## Methodology (9 Phases for Deep Analysis)

### Phase 0: Project Context Detection & Auto-Initialization (项目上下文检测与自动初始化) ⭐ NEW

**Purpose**: Ensure CLAUDE.md exists for enhanced context, or auto-generate it
**Time**: < 1 second (if CLAUDE.md exists) or 1-3 minutes (auto-/init)
**Output**: Project context metadata + CLAUDE.md (generated if needed)

**Steps**:
1. **Detect CLAUDE.md**
   ```bash
   if [ -f "CLAUDE.md" ]; then
     echo "✓ Found CLAUDE.md - reading project context"
     # Extract: project type, build commands, conventions
     # Continue to Phase 1
   else
     echo "ℹ No CLAUDE.md found - auto-generating with /init"
     # Proceed to step 2: Auto-initialization
   fi
   ```

2. **Auto-initialization (if CLAUDE.md missing)**
   ```bash
   # Only runs if CLAUDE.md doesn't exist
   echo "🔄 Running /init to generate CLAUDE.md..."
   echo "   This may take 1-3 minutes..."
   /init

   # After /init completes:
   echo "✓ CLAUDE.md generated"
   echo "🔄 Reloading context with CLAUDE.md..."

   # Clear current context (implementation-specific)
   # Re-read CLAUDE.md with fresh context

   echo "✓ Context loaded with CLAUDE.md enhancement"
   echo ""
   echo "Note: /init took ~X minutes. This is a one-time cost."
   echo "      Future analyses will use existing CLAUDE.md (~2 seconds)."
   ```

3. **Verify CLAUDE.md loaded**
   ```bash
   # After auto-init or if already existed
   if [ -f "CLAUDE.md" ]; then
     echo "✓ CLAUDE.md context available for analysis"
     # Extract key information:
     # - Project overview
     # - Build commands
     # - Dependencies
     # - Architecture
     # - Conventions
   else
     echo "⚠️  CLAUDE.md not available - using code structure analysis"
     # Fallback to code-only analysis (still works!)
   fi
   ```

4. **Detect project type** (enhanced with CLAUDE.md)
   ```bash
   # Primary: From CLAUDE.md (if available and accurate)
   # Fallback: From code structure

   if grep -q "Project Type" CLAUDE.md 2>/dev/null; then
     PROJECT_TYPE=$(grep "Project Type" CLAUDE.md)
   elif [ -f "package.xml" ] || [ -f "CMakeLists.txt" ]; then
     PROJECT_TYPE="ROS/Catkin"
   elif [ -f "Cargo.toml" ]; then
     PROJECT_TYPE="Rust"
   # ... etc
   ```

5. **Detect build system**
   ```bash
   # Primary: From CLAUDE.md build commands
   # Fallback: From build files

   if grep -q "catkin_make" CLAUDE.md 2>/dev/null; then
     BUILD_SYSTEM="CMake (Catkin)"
   elif [ -f "CMakeLists.txt" ]; then
     BUILD_SYSTEM="CMake"
   # ... etc
   ```

**Checkpoint**:
- [ ] CLAUDE.md exists (either found or auto-generated)?
- [ ] Project type detected?
- [ ] Build system identified?
- [ ] Context loaded (with or without CLAUDE.md)?

**Key Principle**:
- ✅ **Auto-ensure CLAUDE.md**: Generate if missing for better context
- ✅ **Transparent**: User sees what's happening
- ✅ **One-time cost**: /init runs once, then reused
- ✅ **Fallback**: Works even if /init fails

**Behavior Changes**:
- **Before (v2.0)**: No CLAUDE.md → code-only analysis
- **After (v2.1)**: No CLAUDE.md → auto-/init → enhanced analysis

**User Experience**:
```bash
# First time on fresh clone
$ /codebase-analysis /path/to/fresh/clone

ℹ No CLAUDE.md found - auto-generating with /init
🔄 Running /init to generate CLAUDE.md...
   This may take 1-3 minutes...
[init output...]
✓ CLAUDE.md generated
🔄 Reloading context with CLAUDE.md...
✓ Context loaded with CLAUDE.md enhancement

Note: /init took ~2 minutes. This is a one-time cost.
      Future analyses will use existing CLAUDE.md (~2 seconds).

✓ Phase 0: Context Detection Complete
[Continues to Phase 1...]
```

**See**: `INIT_GUIDE.md` for detailed fresh clone handling

---

### ⚠️ MANDATORY PRE-REQUISITE: Read WORKFLOW.md First

> **CRITICAL**: Before starting any analysis, you **MUST** read `WORKFLOW.md` which contains the **mandatory verification workflow**.
>
> **Core Rule**: All analysis MUST be based on actual code. Every claim MUST have a [VERIFY:] tag. No exceptions.
>
> **Workflow**: Code Reading → Draft Generation → Verification → Fix Discrepancies → Final Output
>
> **Quality Gates**: Cannot proceed to next phase without passing verification checkpoints.

---

### Phase 1: Global Exploration (全局探索)
- **⚠️ MANDATORY**: Read actual source files first
- Identify project structure and key modules
- Map dependencies and relationships
- Understand framework and architecture
- **⚠️ NEW**: Generate complete module inventory

**Checkpoint**:
- [ ] Can you point to specific files for each claim?
- [ ] **NEW**: All modules/threads enumerated?
- [ ] **NEW**: Complexity assessed for each?

### Phase 1.5: Analysis Planning (分析规划) ⭐ NEW
- **⚠️ MANDATORY**: Generate explicit Phase 4 plan
- Map Phase 1 modules to Phase 4 documents
- Prioritize by complexity/importance
- Generate PHASE4_PLAN.md
- **⚠️ MANDATORY**: All Phase 1 items must have Phase 4 coverage

**Output**: PHASE4_PLAN.md
- Complete list of algorithm documents to generate
- Expected length per document
- Code locations for each
- Mathematical focus areas
- Execution order

**Checkpoint**:
- [ ] Every identified module has corresponding Phase 4 plan?
- [ ] All threads covered?
- [ ] Estimated total length ≥ 10,000 lines?

**See**: `PHASE1_ENHANCED.md` for detailed methodology

---

### Phase 2: Data Structure Analysis (关键数据结构详细梳理)
- **⚠️ MANDATORY**: Read struct/class definitions from code
- Enumerate all key data structures
- Document fields, methods, and relationships
- Create structure diagrams with ASCII art
- Cross-reference actual code definitions

**Checkpoint**: Every structure has [VERIFY: file:line] tag?

### Phase 3: Data Flow Analysis (数据流梳理)
- **⚠️ MANDATORY**: Trace through actual code execution
- Trace data movement through the system
- Identify transformation points
- Document inputs and outputs at each stage
- Validate against actual code execution paths

**Checkpoint**: All flow steps traceable to code?

### Phase 4: Algorithm Deep Dive (算法深度分析) ⭐ NEW
- **⚠️ MANDATORY**: Read algorithm implementation line-by-line
- **Mathematical formulations** with complete derivations
- **Step-by-step execution flow** with intermediate states
- **Complexity analysis** with bottlenecks identified
- **Comparison with alternative approaches**
- **Design rationale** for algorithmic choices
- **Every formula verified against code**
- Generate: `ALGORITHM_XX-[Name].md` (1500-3000 lines each)

**Checkpoint**: Every derivation has code evidence?

### Phase 5: Key Function Analysis (关键函数内部流程梳理)
- **⚠️ MANDATORY**: Read function implementation completely
- Deep dive into critical functions
- Internal logic flow with line-by-line analysis
- Dependencies and call graphs
- Verification against implementation
- Performance profiling data

**Checkpoint**: Each line analysis references actual code?

### Phase 6: Q&A Documentation (问题解答文档) ⭐ NEW
- **⚠️ MANDATORY**: All answers backed by code evidence
- Answer **"Why" questions** about design decisions
- Explain **"How" questions** about implementation
- Provide **configuration guidance** for different scenarios
- Document **common pitfalls** and solutions
- Generate: `KEY_QUESTIONS-[Module].md` (500-1000 lines each)

**Checkpoint**: Every answer has [VERIFY:] tag?

### Phase 7: Verification and Review (复核校准) ⚠️ **MANDATORY**
> **See WORKFLOW.md for complete verification protocol**

- **⚠️ MANDATORY**: Automated verification of all [VERIFY:] tags
- **⚠️ MANDATORY**: Manual code cross-reference checking
- **⚠️ MANDATORY**: Mathematical formula validation
- **⚠️ MANDATORY**: Fix all discrepancies before output
- **⚠️ MANDATORY**: Zero tolerance for hallucinations
- Cross-check all claims against code
- Validate code references
- Ensure no hallucinations
- Mathematical correctness verification
- Peer review checklist

**Quality Gate**: Cannot generate final output until:
- [ ] 100% of [VERIFY:] tags validated
- [ ] All discrepancies fixed
- [ ] Zero hallucinations detected
- [ ] All formulas match code

## Quality Guarantees

Every analysis document **MUST** include:
- **Code Evidence**: Every claim references actual code with `file:line`
- **Verification Tags**: `[VERIFY: relative/path/file:line]` on **EVERY** claim
- **Anti-Hallucination**: Zero speculation without code evidence
- **Consistency**: Uniform structure and formatting
- **Traceability**: Clear line from claim to code evidence

**⚠️ MANDATORY REQUIREMENT**:
- If you cannot provide a [VERIFY:] tag, **DO NOT** make the claim
- If you haven't read the code, **DO NOT** speculate
- If uncertain, **DELETE** the content entirely

**See**: `WORKFLOW.md` for mandatory verification protocol

## File System Structure

```
codebase-analysis-skill/
├── SKILL.md                    # Claude Code native auto-discovery
├── skill.md                    # OMC skill definition (this file)
├── WORKFLOW.md                 # ⭐ MANDATORY verification workflow (READ FIRST!)
├── README.md                   # Usage guide
├── Gotchas.md                  # Common pitfalls (MOST IMPORTANT)
├── CHANGELOG.md                # Version history
├── CONTRIBUTING.md             # Contribution guide
├── LICENSE                     # MIT License
├── templates/                  # Document generation templates
│   ├── system_overview.md      # Architecture overview
│   ├── data_structures.md      # Data structure breakdown
│   ├── algorithm_flow.md       # ⭐ Deep algorithm analysis (v2.0)
│   └── key_questions.md        # ⭐ Q&A documentation (v2.0)
├── verification/               # Verification tools
│   ├── verify_all_refs.sh      # ⭐ Automated [VERIFY:] tag checker
│   ├── verify_analysis.sh      # Full analysis verification
│   └── code_reference_checklist.md  # Manual verification checklist
├── helpers/                    # Helper scripts
│   ├── ascii_diagrams.sh       # ASCII diagram utilities
│   └── code_ref_formatter.sh   # Code reference formatting
├── docs/                       # Detailed methodology docs
│   ├── ANALYSIS_FLOW.md        # Progressive refinement explained
│   ├── INIT_GUIDE.md           # CLAUDE.md handling strategy
│   ├── PHASE1_ENHANCED.md      # Phase 1 enhanced methodology
│   └── PHASE4_GUIDE.md         # Algorithm deep dive guide
└── examples/                   # Usage examples
    └── example-output.md       # Sample output from Voxel-SLAM
```

**Critical Files** (read in this order):
1. **WORKFLOW.md** - Mandatory verification workflow
2. **Gotchas.md** - Common pitfalls to avoid
3. **skill.md** - This file (methodology overview)

## Progressive Disclosure

This skill uses file system structure for progressive disclosure (Tip 3 from skill creation guide):
- **Core**: skill.md loaded first
- **Templates**: Loaded when analysis begins
- **Helpers**: Loaded when generating output
- **Verification**: Loaded during review phase

This prevents overwhelming Claude with all context at once.

## Gotchas (Common Pitfalls)

**This is the most valuable section** - learned from real analysis failures.

See `Gotchas.md` for detailed coverage of:
- Hallucinating features not in code
- Misinterpreting data structures
- Missing critical code paths
- Incorrect data flow assumptions
- Verification blind spots

## Verification Requirements

Every document must pass:
1. ✅ All claims reference actual code (file:line:column)
2. ✅ ASCII diagrams match code structure
3. ✅ Data flows validated by execution tracing
4. ✅ No speculative statements without evidence
5. ✅ Cross-references resolve correctly
6. ✅ Verification checkpoints completed

## Example Output Style

Reference: `fastlivo2-tech-docs (reference repo)`

Key characteristics:
- Bilingual (Chinese + English) where appropriate
- Multi-layer structure (Concept → Structure → Operation → Integration → Summary)
- Extensive ASCII diagrams
- Actual code snippets with line numbers
- Step-by-step algorithm breakdowns
- Verification checklists at end of each section

---

**Next Steps**: When this skill is invoked:

1. **FIRST**: Read `WORKFLOW.md` (mandatory verification protocol)
2. **SECOND**: Read `Gotchas.md` (common pitfalls)
3. **THEN**: Begin with Phase 1 and proceed systematically
4. **ALWAYS**: Verify all claims against code before proceeding to next phase
5. **FINALLY**: Pass all quality gates before generating output

**Non-negotiable**: Zero tolerance for unverified claims or hallucinations.
