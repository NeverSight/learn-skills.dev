---
name: kasb
description: Research public KASB standards and Q&A material with the read-only kasb CLI. Use when the user asks to find or cite Korean accounting standards from KASB, retrieve K-IFRS or KASB sections or exact paragraphs, or search or retrieve KASB Q&A, even without naming the CLI or skill. Do not use for changing the CLI, researching non-KASB sources, or giving unsourced accounting advice.
---

# KASB

Use the installed standalone CLI as the live contract for finding and retrieving KASB source material. Keep this skill procedural; do not treat it as a command manual.

## Discover the Current Interface

1. Run the installed CLI's top-level help before querying:

   ```sh
   kasb --help
   ```

2. Choose the relevant command from that output and inspect its current contract:

   ```sh
   kasb help <command>
   ```

3. Derive commands, options, required inputs, workflows, cautions, and output handling from that help. Do not rely on remembered flags or copy a previous invocation without checking it.

If `kasb` is unavailable, report that prerequisite and point to the repository's standalone installation instructions. The GitHub release channel does not establish npm registry availability. Do not silently replace KASB retrieval with memory or browser results.

## Retrieve Evidence

- Run the narrowest command that answers the request, using the same `kasb` executable.
- Follow identifiers and next steps returned by the CLI or described in its help. Never invent or translate standard numbers, paragraph references, section identifiers, or Q&A document numbers.
- Inspect structured success and failure output before deciding the next action. On invalid input, revisit that command's help and repair only the identified input.
- Treat `advisories.versionCheck` as separate release evidence; preserve the primary result even when the advisory is uncertain. Do not install or upgrade merely because an advisory is present.
- Keep the workflow read-only. Treat returned material as source evidence, not accounting, legal, tax, investment, or audit advice.

## Report the Result

- Answer in the user's language when practical while preserving exact Korean titles and source terminology.
- For each reported standard section, provide a human-readable KASB browser link in the form `https://db.kasb.or.kr/s/{stdNum}/{indexDocumentId}`.
- For each reported standard paragraph, append `?selected={paraNum}` to its section link so the browser page selects that paragraph. Use the exact `stdNum`, `indexDocumentId`, and `paraNum` returned by the CLI, URL-encode components, and label the link with the standard title and paragraph reference.
- Never substitute an API URL or a browser-route `titleDocumentId` for the `indexDocumentId` in these browser links. If the CLI result lacks an `indexDocumentId`, retrieve the paragraph or section through the CLI before linking; if it remains unavailable, state that no verified browser link can be constructed rather than guessing.
- Preserve identifiers, paragraph references, Q&A document numbers, API source URLs, warnings, truncation, partial-result markers, and source-drift notices needed to verify the answer, but do not make a JSON API URL the only user-facing link when a standard browser link can be constructed.
- Distinguish retrieved content from interpretation or inference. If the source or package cannot provide the requested evidence, state that limitation instead of filling the gap from memory.

Finish when the relevant current help was inspected, the required evidence was retrieved or a concrete limitation was established, the response retains enough source detail for the user to verify it, and every reported standard section or paragraph has a browser link or an explicit explanation of why one could not be constructed.
