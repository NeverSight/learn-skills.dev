---
name: create-pr
description: Create a pull request with a concise title and body. Use when asked to open a PR for the current branch.
---

# Create PR

- Resolve the intended base and compare it with the current branch. Read the commits, relevant diff, and any PR template; describe the net changes between the base and HEAD, not intermediate steps. Stop if there is no committed work to include or the current branch is the base.
- Write a specific, short title and a compact body explaining the purpose and reviewer-relevant changes. Prefer bullets, small code snippets, or Mermaid diagrams over long prose. Don't list files or implementation trivia.
- For visual changes, include a before/after table with images or video links when available. For benchmarks, include baseline and candidate results in a table; don't invent measurements or media.
- Link a related ticket when provided or clearly identifiable from the branch or commits; don't guess or create one. Mention risks, migrations, or unusual validation only when relevant. Don't add a routine test report, generic checklist, or unverified claims just to fill space.
- Check for an existing PR before creating one. Push the branch if needed, create the PR against the resolved base, and return its URL and title. Don't create tickets or include uncommitted changes. If only asked to draft or edit copy, return the title and ready-to-paste body without pushing or publishing.
