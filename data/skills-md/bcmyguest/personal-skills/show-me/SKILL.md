---
name: show-me
description: Point the user to the code or source behind the previous response, with a snippet plus a link to the exact lines on its forge (GitHub, GitLab, Azure DevOps, Bitbucket, Gitea/Forgejo), a link to the exact section of the source material, or both. Use when the user runs /show-me or asks where something you said comes from.
argument-hint: "[item numbers, comma-separated] [what to locate]"
---

# Show me

Show the user the evidence behind your last response, so they can check it themselves.

## Arguments

The text after the command (`$ARGUMENTS` in hosts that substitute it) holds up to two parts, both optional:

- **Item numbers,** comma-separated (`1,3`). They refer to the numbered items in your last response. When it had no numbered items, count its top-level bullets or paragraphs from 1, and state the mapping in one line.
- **Target,** any text after the numbers ("the retry logic", "the rate-limit docs"). It names what to locate.

No arguments: cover every concrete claim in the last response about code, behaviour, docs, or data.

## For each claim

| The claim rests on | Give |
| --- | --- |
| Code in a git repository | The output of `python3 <this skill's folder>/scripts/permalink.py PATH:START-END`, run from the repository: the `path:start-end` header, a permalink to the commit, and the lines read from disk. |
| Code outside git | A fenced snippet headed by `path:start-end`, copied from the file you just read. |
| Docs, a spec, a paper, an issue | A link to the exact section, plus the one or two sentences that support the claim. |
| Code and a source | Both. |

The script uses only the Python 3 standard library. It reads the forge from `git remote get-url origin` and builds the link in that forge's format. It prints the reason instead of a link when the file has uncommitted changes, the commit is on no remote branch, or the host is unknown; for a self-hosted forge whose name says nothing, pass `--forge github|gitlab|azure|bitbucket|gitea`. Several references go in one call: `permalink.py a.py:3-9 b.rs:40`.

## Rules

1. Locate before you link. Read the file or fetch the page now; a snippet or quote comes from what you read, never from memory.
2. Show the smallest span that proves the claim: usually 3 to 15 lines.
3. Never write a permalink by hand when the script can build it. When the script prints a reason instead of a link, pass the reason on.
4. Link the primary source (official docs, spec, source code, the paper itself), not a summary of it.
5. When you cannot find support for a claim, say "not found" and retract or qualify the claim. Never invent a path, line, or URL.
6. Do not re-explain. One line per item saying what the evidence shows, then the evidence.
