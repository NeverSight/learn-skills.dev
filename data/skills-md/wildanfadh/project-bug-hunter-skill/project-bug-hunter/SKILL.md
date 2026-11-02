---
name: project-bug-hunter
description: Use this skill whenever the user asks to find bugs, audit a project, review code for defects, scan the currently opened directory, investigate hidden errors, prepare a project before deployment, or check why a project might fail. This skill is for broad bug-hunting across the current working directory and should trigger on phrases like "cari bug di project ini", "cek project ini", "audit bug", "review kode", "temukan error tersembunyi", "scan direktori sekarang", "check this repo for bugs", or similar requests even if the user does not specify a language/framework. It produces an evidence-based bug report first and must not modify files unless the user explicitly asks to fix them.
---

# Project Bug Hunter

Use this skill to search for bugs in the project rooted at the current working directory. Treat the open directory as the source of truth unless the user gives a different path.

## Core principle

Find evidence before suggesting fixes. The goal is to produce a useful bug report, not to make speculative changes. Bugs should be tied to files, commands, logs, tests, traces, or code paths.

Do not edit files, install packages, run migrations, delete data, or change configuration unless the user explicitly asks for fixes after reviewing the report.

## Workflow

### 1. Confirm scope quickly

If the user gave no path, use the current working directory. If the directory is very large or contains multiple apps, identify likely project roots and ask which one to inspect only when ambiguous.

Prefer continuing without extra questions when the intent is clear.

### 2. Map the project

Inspect the repository before judging code.

Run lightweight discovery commands such as:

```bash
pwd
find . -maxdepth 3 -type f \
  \( -name 'package.json' -o -name 'pnpm-lock.yaml' -o -name 'yarn.lock' -o -name 'package-lock.json' \
  -o -name 'pyproject.toml' -o -name 'requirements.txt' -o -name 'Pipfile' \
  -o -name 'go.mod' -o -name 'Cargo.toml' -o -name 'composer.json' \
  -o -name 'build.gradle' -o -name 'settings.gradle' -o -name 'pom.xml' \
  -o -name 'pubspec.yaml' -o -name 'Gemfile' -o -name 'Dockerfile' \
  -o -name 'docker-compose.yml' -o -name '.env.example' -o -name 'README.md' \) \
  -not -path '*/node_modules/*' -not -path '*/vendor/*' -not -path '*/.git/*'
```

Also inspect:
- README/setup docs
- CI config (`.github/workflows`, `.gitlab-ci.yml`, etc.)
- test directories
- app entry points
- framework config files
- recent git changes when available (`git status`, `git diff --stat`, recent commits)

Avoid wasting time in generated or dependency directories: `node_modules`, `vendor`, `.next`, `dist`, `build`, `coverage`, `.git`, `.venv`, `target`, `Pods`, `DerivedData`.

### 3. Detect stack and available checks

Infer the language/framework from project files. Prefer built-in project commands over generic guesses.

Common checks:

**JavaScript/TypeScript**
- Read `package.json` scripts first.
- Prefer existing scripts: `test`, `lint`, `typecheck`, `build`.
- Typical safe commands: `npm test`, `npm run lint`, `npm run typecheck`, `npm run build`, or package-manager equivalents.

**Python**
- Inspect `pyproject.toml`, `requirements.txt`, `tox.ini`, `pytest.ini`.
- Typical checks: `pytest`, `python -m pytest`, `ruff check .`, `mypy .` when configured.

**Go**
- `go test ./...`
- `go vet ./...`

**Rust**
- `cargo test`
- `cargo clippy --all-targets --all-features` when available.

**PHP/Laravel**
- `composer test` or configured scripts.
- `php artisan test` when Laravel is detected.

**Java/Kotlin**
- `./gradlew test`, `./gradlew build`, or `mvn test` depending on project.

**Flutter/Dart**
- `flutter test`
- `dart analyze`

If dependencies are missing, do not install automatically. Report the missing prerequisite and continue with static inspection.

### 4. Inspect bug-prone areas

Look for high-signal defects, not style nits.

Prioritize:
- failing tests, build errors, type errors, lint errors that indicate real defects
- runtime crashes and unhandled exceptions
- incorrect async/concurrency behavior
- null/undefined/None handling mistakes
- wrong data shape assumptions
- boundary conditions and off-by-one errors
- broken routing, imports, exports, or module resolution
- configuration mismatches between code, env, and docs
- database query bugs, transaction bugs, migration/order problems
- auth/authorization logic mistakes when visible in normal code review
- API contract mismatches between frontend/backend
- resource leaks, missing cleanup, infinite loops, runaway retries
- platform-specific path/case-sensitivity bugs
- error handling that hides failures or returns success on failure

Do not frame cosmetic style preferences as bugs. If something is only a maintainability concern, put it in a separate "Risiko/Perbaikan non-kritis" section.

### 5. Validate findings

For each suspected bug, gather at least one form of evidence:
- exact command output
- file and line reference
- test failure or reproduction step
- code path explanation
- mismatch between caller and callee
- config/documentation contradiction

If a finding cannot be validated, label it as "potensi bug" and explain what would confirm it.

When a command fails, read the full relevant error and trace it to root cause before recommending a fix. Avoid piling on fixes from one symptom.

### 6. Report format

Respond in the user's language. For Indonesian users, use Indonesian.

Use this structure:

```markdown
# Laporan Bug Project

## Ringkasan
- Root project: `...`
- Stack terdeteksi: ...
- Command yang dijalankan: ...
- Hasil umum: ...

## Bug prioritas tinggi
### 1. [Judul singkat]
- Lokasi: `path/file.ext:line`
- Bukti: ...
- Dampak: ...
- Penyebab kemungkinan: ...
- Rekomendasi fix: ...
- Cara verifikasi: `command` atau langkah reproduksi

## Bug prioritas sedang/rendah
...

## Potensi bug yang perlu konfirmasi
...

## Pemeriksaan yang tidak bisa dijalankan
- Command/prasyarat: ...
- Alasan: ...
- Saran: ...

## Langkah berikutnya
1. ...
2. ...
```

If no real bugs are found, say that clearly and list the checks performed. Then mention any remaining risk areas that were not covered.

## Safety rules

- Do not modify files during bug hunting.
- Do not run destructive commands (`rm`, database reset, migrations that alter data, deploys, credential rotation, production scripts).
- Do not install dependencies without permission.
- Do not expose secrets in the report. If a secret is found, redact it and report the file/path only.
- Prefer read-only commands and project-provided test/build commands.

## When the user asks to fix bugs

After the user selects findings to fix, switch from report mode to root-cause/fix mode:
1. Reproduce the selected bug.
2. Identify root cause.
3. Make the smallest targeted change.
4. Run the verification command.
5. Summarize changed files and remaining risks.

Fix one logical bug at a time unless the user explicitly asks for a broader patch.
