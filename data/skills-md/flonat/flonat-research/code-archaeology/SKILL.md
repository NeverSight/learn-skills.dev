---
name: code-archaeology
description: "Recover the structure, intent, and lineage of old code, data, or analysis files. Use when inherited or dormant research code must be understood before it is changed. Not for a quality review of already-understood code."
allowed-tools: Bash(ls*), Bash(cp*), Bash(mkdir*), Bash(git*), Read, Write, Edit, Glob, Grep
argument-hint: "[project-path]"
---

# Code Audit Skill

**CRITICAL RULE: Never delete data or code files.** Copy to legacy/, never move or delete originals.

> Systematically review and understand old code, data, and analysis files.

## Purpose

Based on Scott Cunningham's workflow of reviving old projects - understanding what exists, documenting it, and making it safe to work with.

**For formal audits with cross-language replication and referee reports, use the Referee 2 agent (`.claude/agents/referee2-reviewer.md`).** This skill is for understanding and documenting existing code, not formal verification.

## When to Use

- Returning to an old project after months/years
- Taking over code from a coauthor
- Before extending existing analysis
- R&R requiring you to revisit old work

## When NOT to Use

- **Brand new projects** — use project-safety skill instead to set up structure
- **Formal code verification** — use the Referee 2 agent for cross-language replication
- **Quick code questions** — just ask directly, no need for full audit

## Workflow

1. **Explore the directory**:
   - What files exist?
   - What's the structure?
   - When were things last modified?

2. **Understand the pipeline**:
   - What are the main scripts?
   - What order do they run in?
   - What data do they use?
   - What outputs do they produce?

3. **Document findings**:
   - Create/update README.md
   - Map data flows
   - Note dependencies

4. **Establish safety**:
   - Create legacy/ folder
   - Copy (don't move) originals
   - Set up version control if not present

5. **Create audit report**:
   - What the code does
   - Potential issues found
   - Recommendations for cleanup

## Safety Rules (from Scott Cunningham)

```markdown
1. Never delete data. Under no circumstances.
2. Never delete programs. No do-files, no R scripts, nothing.
3. Stay in this folder. Can go down, not up.
4. Use a legacy folder. Move originals there for safekeeping.
5. Copy, don't move. When reorganising, always copy from legacy.
```

## Prompt Template

```
I'm returning to an old project after [TIME]. Please help me understand what's here.

1. Explore the directory and tell me what you find
2. Identify the main analysis scripts and their order
3. Map the data pipeline (inputs → processing → outputs)
4. Note any potential issues (missing files, unclear code, etc.)
5. Create a README documenting everything

Before making ANY changes, create a legacy/ folder and copy everything there.
```

## Data Flow Mapping

Understand how data moves through the project:
- What raw data files exist?
- What cleaning/transformation scripts run?
- What intermediate files are created?
- What outputs are generated?

## Compare Datasets (if multiple versions exist)

When you find multiple versions of the same data:
- Side-by-side comparison of key variables
- Identify where datasets diverge
- Visualize differences geographically/temporally
- Document which version to use going forward

## Output Files

After a code audit, you should have:

```
project/
├── README.md           ← Project overview (generated)
├── AUDIT.md            ← Audit findings and issues
├── CLAUDE.md           ← Safety rules for this project
├── legacy/             ← Protected original files
├── docs/
│   └── data_dictionary.md
└── output/
    └── audit_deck.pdf  ← Visual summary
```

## Questions to Answer

- [ ] What is the research question?
- [ ] What data is used?
- [ ] What is the identification strategy?
- [ ] What are the main results?
- [ ] Are results reproducible from the code?
- [ ] What assumptions are made?
- [ ] What are the known limitations?
- [ ] What would need to change to extend this?

## Example Prompts

**Initial exploration:**
> "Read all the .do/.R/.py files in this project and create a summary of what each script does, including inputs and outputs."

**Data comparison:**
> "Compare dataset_v1.dta and dataset_v2.dta. Show me where they differ, with summary statistics and visualizations."

**Documentation:**
> "Create a README.md that documents this project's structure, data sources, and how to reproduce the main results."

## Example Use

"Audit my Brexit replication project - I haven't touched it in 8 months. Tell me what's there, what state it's in, and what I need to do to pick it back up."
