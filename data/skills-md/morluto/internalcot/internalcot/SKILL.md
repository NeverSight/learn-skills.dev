---
name: internalcot
description: Activate a persistent visible-reasoning mode that requires detailed internalcot CLI notes before substantive tools and answers, throughout the conversation. Use only when the user explicitly invokes $internalcot, says "internalcot on", or asks to enable internalcot mode. Keep it active until the user explicitly turns it off. Do not trigger merely because a user asks to think carefully, reason deeply, or show work.
---

# InternalCoT

Install the CLI and this skill together with:

```bash
npx internalcot@latest setup
```

This file is a stable discovery skill. The installed CLI owns the version-matched workflow instructions.

## Load the current workflow

When this skill is invoked:

1. Prefer the persistent CLI and run this standalone command before substantive work:

   ```bash
   internalcot skill
   ```

2. If that command is unavailable or does not support `skill`, load the same workflow without installing anything globally:

   ```bash
   npx --yes internalcot@latest skill --npx
   ```

3. Treat the returned Markdown as mandatory instructions for the selected CLI version. Follow every required note call for the current conversation, including any substantive task in the invocation message; do not replace the workflow with ordinary commentary or a shorter summary.
4. If both commands fail, do not improvise an older workflow or claim the mode is active. Give the exact recovery command `npx internalcot@latest setup`.
