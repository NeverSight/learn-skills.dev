---
name: groove-utilities-memory-install
description: "Set up memory backend and configuration."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-utilities-memory-install

## Outcome

Memory directories are created and ready for use.

## Acceptance Criteria

- `<memory>/daily/`, `<memory>/weekly/`, `<memory>/monthly/`, `<memory>/git/` exist
- `<memory>/specs/` directory exists (outcome specs; used by `/groove-work-spec`)
- `<memory>/learned/` directory exists
- User is shown the initialized paths

## Constraints

- Read `memory:` from `.groove/index.md` frontmatter (default: `.groove/memory/`)
- Create directories if they do not exist:
  ```bash
  mkdir -p <memory>/daily <memory>/weekly <memory>/monthly <memory>/git <memory>/specs <memory>/learned
  ```
- Report the initialized paths to user
