---
name: rtk-token-saver
description: Use this in code repositories whenever an agent needs to run terminal commands, inspect files, search code, view Git status or diffs, run builds, tests, linters, type checks, package managers, logs, Docker, Kubernetes, or database commands. This skill makes the agent prefer RTK wrappers to reduce noisy command output and save context tokens. Do not use for non-coding conversations.
---

# RTK Token Saver

## Goal

Use RTK as the default terminal-output strategy during coding work.

RTK reduces noisy command output before it enters the model context. This skill is useful for large repositories, build logs, test output, Git diffs, recursive file listings, dependency output, runtime logs, and JSON responses.

## Highest priority rule

Before running any shell command, ask internally:

> Can RTK run this command, or is there an RTK-specialized command for it?

If yes, use RTK.

Do not run noisy terminal commands directly unless RTK is unsupported, fails, or hides information required for the task.

## Reference files

For the full command conversion table, see `references/COMMAND_MAP.md`.
For safety and fallback guidance, see `references/SAFETY.md`.

## Preferred command conversions

Use these commands instead of raw equivalents:

```bash
rtk git status
rtk git diff
rtk git log
rtk git show

rtk ls
rtk tree
rtk find . -type f
rtk grep "query" .
rtk read <file>

rtk deps
rtk npm run build
rtk npm run lint
rtk npm test
rtk pnpm build
rtk pnpm test
rtk tsc --noEmit
rtk lint
rtk prettier
rtk next build
rtk jest
rtk vitest
rtk playwright test
rtk prisma

rtk pytest
rtk pip
rtk mypy
rtk ruff

rtk go test ./...
rtk cargo test
rtk mvn test
rtk gradlew test
rtk dotnet test
rtk rake test
rtk rspec
rtk rubocop

rtk docker ps
rtk docker logs <container>
rtk kubectl get pods
rtk aws sts get-caller-identity
rtk psql
```

## Commands to avoid when RTK can handle them

Avoid raw noisy commands such as:

```bash
git diff
git log
ls -R
find .
tree .
grep -R "query" .
cat large-file
npm run build
npm test
pytest
docker logs
kubectl get all -A
```

## Investigation workflow

Follow this order:

1. Search with `rtk find` or `rtk grep`.
2. Read focused files with `rtk read`.
3. Modify only the smallest required set of files.
4. Validate with focused RTK build/test/lint/typecheck commands.
5. Report only actionable errors, warnings, files changed, and next steps.

Do not load entire repositories into context.

Do not open many files blindly.

## Large output policy

Commands likely to produce large output must use RTK.

This includes:

- recursive file listings
- dependency output
- generated files
- lock files
- test suites
- build logs
- lint reports
- runtime logs
- JSON responses
- Git diffs
- search results

If output is still too large after RTK, summarize it and inspect smaller sections.

## Fallback policy

Use a raw command only when at least one condition is true:

1. RTK does not support the command.
2. RTK fails.
3. RTK hides information required to solve the task.
4. The user explicitly asks for raw output.

When falling back, say briefly:

> RTK unsupported or insufficient here, using direct command.

Then run the smallest safe raw command.

## Safety policy

Never use RTK rules as a reason to bypass normal safety.

Do not run destructive commands without user approval.

Be careful with:

```bash
rm
mv
chmod
chown
git reset
git clean
docker system prune
kubectl delete
drop database
truncate
```

Prefer dry-run, status, preview, or backup commands first.

## Verification

Check RTK is installed:

```bash
rtk --version
```

Check whether RTK usage is being recorded:

```bash
rtk gain
```

A useful smoke test is:

```bash
rtk git status
rtk deps
```
