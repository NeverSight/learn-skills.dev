---
name: memory-init
description: "初始化 .memory/ 目录结构并扫描项目生成知识库"
tools: ["Bash", "Read", "Glob"]
---

## Purpose

Initialize the Memory Hub for a project: create `.memory/` skeleton, scan the project, and populate initial knowledge files and catalog.

## Input

No arguments required. Run from the project root.

## Required Flow

### Step 1: Create skeleton

```bash
memory-hub init
```

If `ALREADY_INITIALIZED` error, stop and inform the user.

### Step 2: Scan project and generate tech-stack knowledge

1. Read the project root file listing
2. Read package manager files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, etc.)
3. Read entry files (`main.*`, `index.*`, `app.*`, `server.*`, etc.)
4. Read config files (`.env.example`, `tsconfig.json`, `webpack.config.*`, etc.)

Generate `tech-stack.md` content and write:

```bash
memory-hub write architect tech-stack.md \
  --topic tech-stack --summary "技术栈、关键依赖、使用方式与限制" --mode overwrite <<'EOF'
<generated markdown>
EOF
```

### Step 3: Generate code conventions knowledge

Based on project structure from Step 2, generate `conventions.md`:

```bash
memory-hub write dev conventions.md \
  --topic conventions --summary "目录命名规则、模块组织方式、代码约定" --mode overwrite <<'EOF'
<generated markdown>
EOF
```

### Step 4: Scan project modules and generate Catalog

Analyze directory structure, identify functional domains and key files, construct JSON:

```bash
memory-hub catalog-update <<'EOF'
{"modules": [{"name": "...", "summary": "...", "files": [{"path": "...", "description": "..."}]}]}
EOF
```

### Step 5: Quality gate

1. List `unknowns` — files/directories that don't clearly belong to any functional domain
2. Check `catalog.repair` output (auto-triggered by catalog-update):
   - `ai_actions` non-empty → execute self-healing, then run `memory-hub catalog-repair` again to confirm cleared
   - `manual_actions` non-empty → report to user

### Step 6: Output summary

Report: files created, modules identified, unknowns requiring user confirmation.

## Output

JSON envelope from each command. Final summary to user.

## Error Handling

- `ALREADY_INITIALIZED` → inform user, do not proceed
- Any command failure → stop and report the error
