---
name: devvit-skill-setup
description: "Configure a repo's agent instruction files (AGENTS.md, CLAUDE.md, etc.) to auto-apply Devvit skill guidance. Trigger phrases: \"configure skills\", \"setup skills\", \"add devvit docs rule\"."
---

# Devvit Skill Setup

Does basic setup to make a code repository ready to use devvit skills.

1. Ensure the devvit-docs skill is added. If not, skip. If it is, call `devvit-docs` with "how does redis work" to make sure things are configured correctly. If there is an error, present it to the user.

2. Ensure the rules file adds a block about working with Devvit

Please do the following:

- Check the repo root for common instruction files (`AGENTS.md`, `CLAUDE.md`, etc.).
- Insert the following skill a close to the top of the rules file

```md
Always use the devvit-docs skill when I need library/API documentation about anything related to devvit including: documentation, code generation, setup or configuration steps without me having to explicitly ask. This includes capabilities that devvit offers like Redis, Reddit API, Media, and more as Devvit has special rules and documentation.
```

- If no instruction file exists, create `AGENTS.md` with the block above.
- Add success or failure to summary of skill call result

3. Present Results to User

Tell the user the changes you made.

## Troubleshooting

- **Permission errors**: Verify the repo is writable.
- **Wrong location**: Ensure the repo root is being edited.
- **No changes**: The rule block already exists; no update needed.
- **Missing skill**:  Ask the user to run `npx add-skill reddit/devvit-skills` to add the missing skill if they want to utilize that feature.
