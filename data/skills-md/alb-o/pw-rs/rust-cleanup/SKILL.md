---
name: rust-cleanup
description: General rust cleanup process with focus on comments vs rustdoc. Run after a complete task or feature.
---

1. review the current work for inline comments, consolidate useful technical information into proper rustdoc docstrings:

- remove trivial inline comments
- move comments explaining why or tech specs into rust docstrings
- follow rustdoc conventions: Use `# Examples`, `# Panics`, `# Errors`, `# Safety` sections where appropriate
- treat docstrings as tech specs with additional (start simple first line(s), move to spec lower, with intra-doc links)
- remove implementation-specific qualifiers and trailing parenthesized text
- remove comments used for section markers
- do NOT outright remove docstrings, especially from pubs
- MUST keep docstrings thorough and technical

2. briefly rework any inelegant or verbose code

- check for tramp data, unecessary vars that could be inlined, performative error handling, etc.
- prefer data-oriented orthogonal approaches
