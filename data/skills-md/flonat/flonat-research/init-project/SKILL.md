---
name: init-project
description: "Bootstrap a new research project. Interview for details, scaffold directory structure, create Overleaf symlink, initialise git, and create project context files."
allowed-tools: Bash(mkdir*), Bash(ln*), Bash(git*), Bash(ls*), Read, Write, Edit, Glob, Grep, AskUserQuestion
argument-hint: (no arguments — starts an interview)
---

# Init Project — Research Project Scaffolder

> Interactive project setup: answer questions, get a ready-to-use research project directory.

## Protocol

### Phase 1: Interview

Ask the user these questions using `AskUserQuestion` (adapt based on what's already known):

1. **Project name** — short name for the directory (e.g., `nudge-experiment`)
2. **Paper title** — working title for the paper
3. **Research question** — one sentence
4. **Target journal/venue** — where you plan to submit
5. **Co-authors** — names and affiliations (if any)
6. **Parent directory** — where to create the project (default: `~/Research/`)
7. **Overleaf path** — path to Overleaf-synced directory for symlink (optional)
8. **Methodology** — experimental, observational, theoretical, simulation, mixed

### Phase 2: Scaffold

Create the directory structure:

```
<project-name>/
├── CLAUDE.md               # Project-specific Claude instructions
├── README.md               # Project overview
├── MEMORY.md               # Knowledge base (seeded with template)
├── paper/                  # → Overleaf symlink (or empty dir)
├── code/
│   ├── python/             # Python scripts
│   └── R/                  # R scripts
├── data/
│   ├── raw/                # Original data (never modified)
│   └── processed/          # Cleaned/transformed data
├── results/                # Analysis outputs
├── figures/                # Generated figures
├── docs/                   # Project documentation
├── correspondence/         # Referee reports, cover letters
│   └── referee2/           # Referee 2 agent reports
├── log/                    # Session logs
│   └── plans/              # Saved plans
└── .gitignore
```

### Phase 3: Populate Files

**CLAUDE.md** — project-specific instructions:
- Paper title and research question
- Co-authors and target venue
- Methodology and key conventions
- Pointer to project context files

**README.md** — human-readable overview:
- Project title and description
- Directory structure explanation
- How to compile the paper
- Co-author information

**MEMORY.md** — seeded with research project template:
- Notation Registry (empty)
- Estimand Registry (empty)
- Key Decisions (empty)
- Citations (empty)
- Anti-Patterns (empty)
- Code Pitfalls (empty)

**.gitignore** — standard research project ignores:
- Build artifacts (`out/`, `*.aux`, `*.log`)
- Data files (`data/raw/*.csv`, `data/raw/*.xlsx`)
- Python/R artifacts (`__pycache__/`, `.Rhistory`)
- OS files (`.DS_Store`)

### Phase 4: Git & Symlinks

1. **Overleaf symlink** — if a path was provided:
   ```bash
   ln -s /path/to/overleaf/dir paper
   ```
2. **Git init** — initialise the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial project scaffold"
   ```

### Phase 5: Context Update

Update the central context library:
1. Add the project to `.context/projects/_index.md`
2. Create `.context/projects/papers/<project-name>.md` with metadata

## Output

Print a summary of what was created:

```
Project created: ~/Research/<project-name>/
  Directories: 12
  Files: 4 (CLAUDE.md, README.md, MEMORY.md, .gitignore)
  Overleaf: linked / not configured
  Git: initialised with initial commit

Next steps:
  1. Start writing in paper/ (or link Overleaf)
  2. Add code to code/python/ or code/R/
  3. Run session-log when you finish working
```
