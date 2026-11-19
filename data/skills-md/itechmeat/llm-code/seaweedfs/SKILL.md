---
name: seaweedfs
description: "SeaweedFS distributed storage. Covers filer, S3 API, replication, cloud tiers, and operations. Use when deploying SeaweedFS, configuring filer stores, exposing S3-compatible endpoints, or planning backup and security controls. Keywords: SeaweedFS, weed, filer, S3, object storage."
metadata:
  version: "4.48"
  release_date: "2026-09-28"
---

# SeaweedFS

This skill is a practical router for deploying and operating SeaweedFS from the upstream repository and wiki.

Prefer production guidance from multi-component setups over `weed mini` shortcuts.

## Quick Navigation

| Situation                                             | Open                                                               |
| ----------------------------------------------------- | ------------------------------------------------------------------ |
| Learn the system shape and bootstrap paths            | `references/getting-started.md`                                    |
| Stand up a local all-in-one sandbox                   | `references/quick-start-mini.md`                                   |
| Review control-plane, volume, and collection topology | `references/topology-and-setup.md`                                 |
| Check master, volume, filer, and client API surfaces  | `references/api-surfaces.md`                                       |
| Set replication, TTL, failover masters, and env vars  | `references/configuration.md`                                      |
| Work with performance notes, FAQ topics, and examples | `references/benchmarks-and-use-cases.md`                           |
| Work with filer metadata, uploads, JWT, and TUS       | `references/filer-core.md`                                         |
| Choose and scale filer metadata stores                | `references/filer-stores.md`                                       |
| Operate S3 buckets, auth, and IAM/OIDC                | `references/s3-gateway.md`                                         |
| Plan Cloud Drive and remote storage mounts            | `references/cloud-drive.md`                                        |
| Run backups, metrics, repairs, and shell workflows    | `references/backup-and-replication.md`, `references/operations.md` |
| Choose S3 encryption and client tooling               | `references/encryption.md`, `references/s3-client-tools.md`        |
| Review transport, JWT, TLS, and exposure controls     | `references/security.md`                                           |

## When to Use

- Planning a SeaweedFS deployment
- Running `weed` components in development or production
- Designing filer, S3, or cloud-tier topologies
- Choosing metadata stores and replication patterns
- Hardening SeaweedFS for public or multi-tenant use
- Operating backups, metrics, and cluster repair workflows

## Core Mental Model

- SeaweedFS separates volume management from file and object access paths.
- The filer layer adds directories, metadata stores, and higher-level protocols.
- S3, WebDAV, FUSE, and other interfaces are front doors on top of the same storage services.
- Production deployments should document topology, credentials, persistence, monitoring, and recovery paths explicitly.

## Release Highlights (4.48)

- **S3 trusted proxies (`aws:SourceIp`)**: a configurable allowlist in `security.toml` restores forwarded-header support without re-opening the spoofing hole. When the direct TCP peer is in the allowlist, `X-Forwarded-For` is walked right-to-left (then `X-Real-Ip`) to determine `aws:SourceIp`; otherwise the direct peer address is used. Applies to the bucket policy engine, the IAM attached-policy engine, and the IAM role/session policy middleware. See `references/s3-gateway.md` and `references/security.md`.
- **Admin bind default**: the `-ip` default auto-upgrades to `0.0.0.0` when `-adminPassword` or `[https.admin]` mTLS is configured; the loopback default stays for unauthenticated deployments, and an explicit `-ip` is always honored. The admin **worker/plugin gRPC** control plane now honors `-ip` too, instead of wildcard-binding every interface.
- **Multipart concurrency for remote storage and tiering**: `upload_concurrency` / `download_concurrency` are configurable per remote storage (`remote.configure -upload_concurrency` / `-download_concurrency`) and per S3 backend in `master.toml`; `volume.tier.upload|download|move|evict` accept a `-concurrent` flag. `0`/unset keeps the previous defaults (1 upload part, 5 download parts for S3). See `references/cloud-drive.md`.
- **S3 correctness**: `ListMultipartUploads` now returns the `Initiated` timestamp (repeated listings preserve the original time), POST policy uploads preserve object versions, object lock retention is honoured on version deletes, Object Lock configuration and object-lock actions are authorized separately, a list marker sorting before the prefix excludes nothing, request bodies are drained before an error response, and multipart completion commits the upload and removes `.uploads` atomically.
- **Helm**: the generated read-only S3 identity is granted `List`, master pods roll when the master config changes, and `admin.allowInsecureBind` satisfies the admin auth render guard.
- **Filer**: accepted metadata log records survive shutdown, shutdown paths are joined before the metadata store closes, the filer gained its own `disableHttp` flag, and manifest resolve error propagation is cleaned up.
- **Shell**: `fs.verify -pruneEntries` deletes entries whose needles are lost, and `fs.mergeVolumes` warns when the source holds only orphan needles.
- **Rust volume**: `tonic`/`prost` 0.14, the tail scan streams and releases the store lock, 8-15 argument functions folded into parameter structs, and a Windows build fix.
- **Enterprise**: a new KVCache subsystem - an LMCache-facing KV cache service for LLM inference KV-cache tiering, with per-collection write concurrency and bounded cleanup memory.

## Release Highlights (4.41 -> 4.45)

- **S3 write path**: large chunk lists fold into manifest chunks on the direct write path, per-object and multipart-completion uploads chunk at the filer's `maxMB`, storage class rides in cached listing metadata, and writing a bucket policy now requires a bucket-policy action. `RenameObject` is added, bucket auto-creation on upload can be disabled, and suspended-versioning/null-delete-marker handling is tightened.
- **IAM/STS maturity**: document-style policies load from the advanced IAM config, attached policies can list the buckets they grant, the admin's role session stays scoped to its role, IAM-management actions are authorized as IAM actions, and the admin UI gains a visual IAM policy editor plus bucket-policy management.
- **Master/topology heartbeat digest**: volume heartbeats carry a digest, send only the volumes that changed, and keep the master current through churn; hot-path allocation and copy removals cut memory churn, and volume listings stream.
- **Erasure coding cleanup**: encode, decode, and shard moves roll back or resume into a consistent state after interruption, `ec.balance` gains a `-volumeIds` filter, and a chaos harness exercises the EC lifecycle.
- **Filer**: conditional `UpdateEntry` with a chunk-set write condition, `filer.meta.scan` to audit a directory's change history, TUS gains configurable max size and session expiry plus a concatenation extension, and folders deleted non-recursively no longer sweep children.
- **Admin/workers**: a Lance catalog with a Rust plugin worker to maintain it, `seaweed-worker` serves health, readiness, and metrics, admin shows per-tier capacity, and bucket lifecycle rules are editable in the admin UI.
- **Core**: throughput limits for replicate/EC-shard/worker moves, Range requests return `416` only when no range overlaps and reject a start offset equal to the file size, and FUSE mount gains Windows (WinFsp) support.

## Release Highlights (4.40)

- **S3 correctness**: `CopyObject` on a missing source now returns `NoSuchKey`/`NoSuchBucket` instead of a misleading error, invalid tagging on `CopyObject` returns `InvalidTag`, `PutObjectAcl` and object-tagging writes for nested keys target the correct object, and raw semicolons in query strings are accepted.
- **IAM/OIDC hardening**: role trust policy is now enforced on direct OIDC bearer-token requests, not only on formal `AssumeRoleWithWebIdentity` flows.
- **Filer/TUS security**: TUS resumable-upload session authorization is hardened so `HEAD`/`PATCH`/`DELETE` are restricted to the session's own target path, closing a cross-prefix access gap; `filer.backup` no longer silently loses data on a transient not-found error; log-buffer flushing is optimized with generated vtproto marshalers.
- **Erasure coding**: new `ec.check.replication` shell command, `ec.encode` no longer rebalances against a topology snapshot that predates its own new shards, and stale `.ecsum` checksum sidecars are removed on shard destroy (Go/Rust aligned).
- **Shell/admin**: `volume.tier.upload` preserves existing replicas, `volume.check.disk` gains `-resurrectMissingNeedles`, `weed shell` shows the current cluster lock holder, and `cluster.ps` lists S3 servers.
- **Core**: master used-size statistics cover all collections, the Rust volume server verifies `.dat` integrity against the last indexed needle, and mount surfaces `ENOSPC` instead of waiting indefinitely.

## Release Highlights (4.25)

- **Security/admin path**: `4.24`-`4.25` tightens admin auth on destructive/admin endpoints and fixes Admin UI behavior under `security.toml` by attaching admin-signed auth on filer IAM gRPC calls.
- **Erasure coding / multi-disk ops**: the release line fixes several EC planner/recovery cases across multi-disk and cross-server layouts, including stale-shard cleanup and safer source-volume deletion.
- **S3/IAM hardening**: IAM users without policies are now denied instead of implicitly over-permitted, while OIDC/web-identity and audit surfaces continue to mature.

## Release Highlights (4.26 -> 4.28)

- **Erasure coding / multi-disk ops**: EC planning now packs shards across disks more reliably, includes `disk_id` in execution planning, and can rebuild lost `.ecx` / `.vif` metadata from local shards during recovery.
- **Integrity checks**: scrubbing/fsck paths now account for zero-sized volumes instead of silently skipping them, which matters for sparse or recently created topologies.
- **Filer backend reliability**: Redis3 avoids a skiplist-end panic path, and SQL-based filer stores no longer force-disable idle connection pooling.
- **S3 audit trail**: requester identity is populated more consistently for GET/HEAD/IAM operations, improving compliance and incident triage.
- **HA heartbeat path**: masters now accept volume-server ping targets on follower replicas, which improves failover visibility in multi-master deployments.

## Release Highlights (4.34 -> 4.39)

- **S3 correctness/compliance**: preserved multipart-copy checksums, account-less identities get distinct owners instead of admin, SigV4 query-value sorting, Range-offset validation, tag-value equals-sign preservation, and static config-file hot reload (`4.34`-`4.36`).
- **Iceberg / S3 Tables**: namespace property updates, table registration, multi-table transaction commits, view support, table rename, and caller-scoped S3 Tables authorization (`4.36`).
- **IAM/STS**: AssumeRole authorized by the role trust policy, STS session-policy explicit-deny enforcement, and OIDC groups/roles surfaced for resource-policy ABAC (`4.36`).
- **Volume-server crash safety**: never delete recoverable EC shards on startup, crash-safe compaction commit with a durable `.cpc` marker, and phantom-volume detection for deleted-but-open descriptors (`4.34`-`4.35`).
- **Erasure coding correctness (Rust parity)**: EC scrub improvements, EC storage/read-path fixes, and Rust volume-server scrub parity, plus S3 CRC checksumming support (`4.38`).
- **FUSE mounts**: write-pattern detection for concurrent writeback tolerance windows and cached supplementary group IDs for faster non-root access (`4.35`).
- **Performance/observability**: performance CI with profiling and throughput benchmarks, Rust volume-server streaming optimizations, native sparkline trends and per-bucket S3 metrics in the admin dashboard, and large cold `GetObject` returning `503` instead of hanging (`4.34`-`4.37`).
- **Ops**: async buffered writes in EC-shard copy, volume-tiering and filer-metadata optimizations, S3 quota measurement by logical size, and mount-failover enhancements (`4.39`).

## Release Highlights (4.31 -> 4.33)

- **S3 versioning/IAM**: atomic versioned `PutObject` commits, proper `NoSuchVersion` errors, latest-pointer repair and recovery, suspended-versioning delete handling, managed IAM policy versions, and bucket read-only quota enforcement; `4.33` also fixes HTTP-date conditionals, checksum trailer headers, and empty v4 signed header names.
- **Erasure coding integrity**: per-shard checksum sidecars for bitrot detection (`4.31`), even shard spreading across machines with co-located servers treated as a single fault domain and pre-deletion shard-landing verification (`4.32`), and guards preventing EC shards from different encode runs mixing or leaving phantom `.dat` on restart (`4.33`).
- **Volume server**: fixes `maxVolumeCount` dead zone on auto-sized disks, keeps volumes writable after deletion-tail compaction, resolves EC data-shard count from `.vif` on reboot (`4.31`), and adds `CheckDisk` disk-health detection (`4.32`).
- **Filer scalability**: bounded BFS-metadata memory and byte-lexicographic S3 list order (`4.31`), streamed metadata-subscription log files (`4.32`), and object-size distribution metrics, mount-reconnect OOM fixes, per-chunk replay, a bounded flush queue, and Elasticsearch 8 (`elastic8`) support (`4.33`).
- **Admin/worker**: lane-aware scheduler pruning, `-dataDir` defaulting for persisted state and in-flight task reload on startup (`4.32`), plus full cluster volume list JSON export (`4.33`).
- **Rust volume server**: bounded request body / stored-content expansion to prevent OOM under load (`4.31`); stops EC-shard-deletion phantom `.dat` on restart (`4.33`).

## Release Highlights (4.29 -> 4.30)

- **S3 write/auth path**: object writes move toward filer-side owner routing and `ObjectTransaction` batches, reducing distributed-lock pressure; `4.30` also tightens path traversal rejection, ownership-control validation, `MetadataDirective=REPLACE`, and JWT handling for unsigned-streaming uploads.
- **FUSE and filer coordination**: POSIX advisory locks are now routed through filer ownership under `-dlm`, with session leases, keepalive, ring-change cooling, and writeback-cache crash fixes for cross-mount write workloads.
- **Erasure coding and volume repair**: EC placement uses the shared `ecbalancer.Place` path and placement snapshots, while `4.30` improves credible-replica selection, empty-stub cleanup, `.vif` preservation, writable-volume notification after vacuum, and shell safety around stuck read-only volumes and merge verification.
- **Operations surfaces**: admin exposes Prometheus metrics, and S3/IAM/volume/filer/master processes add `/healthz` and `/readyz` probes for orchestration checks.
- **Filer, sync, and remote sinks**: Redis2 now applies `keyPrefix` in KV methods, Postgres filer writes default to `ON CONFLICT` upsert, dropped filers are pruned from discovery, and sync/remote-storage paths preserve chunk size, manifest, offset, and MIME metadata more reliably.

## Release Highlights (4.20)

- **S3/IAM**: embedded IAM flows gained `ListUserPolicies`, group inline policy actions, safer user-policy round trips, and bucket-scoped cleanup on `DeleteBucket`.
- **Mount/FUSE**: `weed mount` adds `-dlm` for cross-mount write coordination and improves POSIX metadata behavior, `nlink` accounting, and filer RPC efficiency.
- **Master placement**: volume assignment is more size-aware, readonly transitions drain pending size first, and a topology bug that could cause endless growth in some DC/rack layouts was fixed.
- **Filer reliability**: PgBouncer/Postgres compatibility improved, graceful shutdown corruption was fixed, and redundant filer disk reads that caused memory/CPU regressions were removed.
- **Ops surfaces**: `weed shell` gained group-management helpers, S3 user provisioning handles existing users more safely, and master/volume now export `start_time_seconds` metrics.

## Prohibitions

- Do not use `weed mini` for production.
- Do not treat single-binary defaults as production-safe configuration.
- Do not expose S3 or filer endpoints publicly before reviewing auth, TLS, and network boundaries.
- Do not choose a filer store without validating HA, scaling, and backup properties.
- Do not design backup or replication flows without restore validation.

## Links

- [Documentation](https://github.com/seaweedfs/seaweedfs/wiki/Getting-Started)
- [Releases](https://github.com/seaweedfs/seaweedfs/releases)
- [GitHub](https://github.com/seaweedfs/seaweedfs)
- [Docker Hub](https://hub.docker.com/r/chrislusf/seaweedfs)
