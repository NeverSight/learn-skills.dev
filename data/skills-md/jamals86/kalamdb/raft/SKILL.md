---
name: raft
description: 'Raft replication in KalamDB: log replication, leader election, snapshots, membership changes, and safety rules. Keywords: raft, consensus, leader, follower, log, snapshot, term.'
---

Use this skill when working on Raft replication, consensus state, or log/application ordering.

Core safety rules:
- Only the leader accepts writes; followers replicate and apply in order.
- Log matching property must hold; conflicting entries are overwritten.
- Commit index advances only when entries are replicated to a quorum.

Implementation guidance:
1) Identify the Raft module boundaries and avoid mixing consensus logic with storage or API layers.
2) Keep persistence of log/state separate from in-memory state machines.
3) Ensure snapshot installation and log truncation are consistent with the applied index.
4) Membership changes must follow the project’s chosen approach (joint consensus or staged transitions).
5) When adding new commands, ensure they are deterministic and idempotent when applied.

Testing focus:
- Leader failover and re-election.
- Log divergence and recovery.
- Snapshot restore and state replay.

Pitfalls:
- Applying out-of-order entries.
- Committing entries without quorum.
- Mixing wall-clock time with term/index logic.
