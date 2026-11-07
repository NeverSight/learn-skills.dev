---
name: interrogate
description: Adversarially review a diff or design with independent lenses and evidence. Use before shipping contested or high-impact changes.
---
# Interrogate

Reviewers are attackers, not style voters.

1. Freeze the exact artifact/revision and acceptance criteria.
2. Cover at least these lenses: correctness/invariants, boundary/API compatibility, concurrency/state, tests/verification quality, and maintainability/reader load. Add security/performance when relevant.
3. Use independent workers/models when `delegate` exists. Otherwise run separate sequential lenses and disclose they share context.
4. Require each finding to include a concrete failure mode and evidence or a reproducible check. Reject unsupported nits.
5. The owning agent adjudicates every finding as fix, dismiss, or investigate. Never pass reviewer prose through unexamined.
6. Re-run targeted proof after accepted fixes.
