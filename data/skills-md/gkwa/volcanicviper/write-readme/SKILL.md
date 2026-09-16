---
name: write-readme
description: Write a brief README with a CLI cheatsheet. Use when creating or writing a README.md file.
---

## README: Be Brief

When writing a README, be brief. Do not include licensing or contribution sections.

Always show a cheatsheet that demonstrates the command-line interface. Show the CLI in a code block with a short one-line comment above it indicating its purpose.

## The Shape

One code block holds every invocation, each under its own one-line comment.

Do not give each example its own fenced block, its own prose sentence, or its own heading.

```sh
# find files where tags include "python"
islandiguana ./notes '.tags[] == "python"'

# find files up to 1 level deep
islandiguana --max-depth 1 ./notes '.tags[] == "python"'

# delete a front matter key from all matched files
islandiguana ./notes '.filetype == "product"' --mutate 'del(.filetype)'
```

Prose belongs above or below the block, explaining what the tool is and any rule the reader cannot guess.

Prose does not belong between the commands.

## Output

Showing output is optional, and most cheatsheets do not.

The rule that captured output must be real rather than invented governs any output you choose to show. It never requires an example to show output, and it never justifies pairing every command with an output block.

When a command's result is the point, such as a JSON record or a parse error, show that one.
