---
name: lance-format
description: Deep reference for Lance v15 columnar format, its Rust crates, and pylance - file encodings, table format, indexes, schema evolution, time travel. Use when building on the Lance crates or reading .lance datasets, not the LanceDB product.
metadata:
  version: "0.22.0"
  categories: "development, integrations"
  topics: "lance, columnar-format, vector-search, rust, lakehouse"
  upstream: "lance-format/lance@v15.0.0-beta.10"
  openclaw:
    homepage: https://github.com/tenequm/skills/tree/main/skills/lance-format
    emoji: "🗄️"
---

# Lance v15 reference

Lance is an open columnar format for multimodal AI - "a columnar data format that is 100x
faster than Parquet for random access." It is not one format but a stack of interoperating
specs: a **file format**, a **table format**, **index formats**, **catalog specs**, and a
**namespace client spec**. The Rust workspace at `lance-format/lance` implements all of them
plus Python (`pylance`) and Java bindings.

This skill tracks **`v15.0.0-beta.10`** (the `lance-format/lance` git tag), the current
development frontier; **`v14.0.2`** is the stable pin, released 2026-10-29. Pin against tags, not
`main` - Lance ships beta tags every few days and `next`-format encodings can change. Version
landscape below.

Three layers of reference, load what the task needs:

- **The deep reference** - any concrete schema, parameter, proto, or constraint. Split by topic:

  | File in `references/` | Covers | Sections |
  |------|--------|----------|
  | `format-file.md` | What Lance is, the 28 crates, file format, data types | 1-4 |
  | `format-table.md` | Dataset layout, manifests, fragments, schema evolution, versioning/tags/branches, row IDs, transactions + OCC, MemWAL | 5-10 |
  | `indexes.md` | Vector / scalar / FTS / geo indexes, distributed builds | 11-12 |
  | `ops.md` | Object store, capability matrix, source map | 13, 15, 16 |
  | `changelog-v7-v15.md` | The full v7 -> v15 delta | 14 |

  Cross-references written as "section N" resolve through `references/lance-reference.md`.
- `references/performance.md` - ALL performance guidance. Part A routes to the official text and
  adds the source-derived changes upstream has not documented; Part B is field-verified
  remote-storage practice. Load for any performance, tuning, maintenance-cost, or "why is this
  slow" question.
- `references/docs/` - a **verbatim mirror of the official docs** (`docs/src` at the tracked
  tag): every guide, quickstart, and format spec, unedited. Load when you need the full official
  text. Directory map below.

`references/maintenance.md` covers refreshing this skill against a new upstream tag. Upstream
also ships its own operational agent skill, `skills/lance-table-maintenance/` in the repo
(#9610) - health indicators and maintenance operations; this skill stays the format reference.

## Lance vs LanceDB

These are two different things and conflating them produces wrong answers.

- **Lance** - the format and engine. The `lance-format/lance` repo; the `lance` /`lance-*`
  Rust crates; `pylance`. It gives you datasets, the file/table format, indexes, commits,
  scans. Consumed directly by DuckDB, Polars, Ray, Spark, PyTorch, DataFusion, or your own
  Rust/Python code. **This skill is about Lance.**
- **LanceDB** - a separate database *product* (`lancedb/lancedb`) built on top of Lance. It
  adds a query-builder API, an embedding registry, rerankers-as-API, multi-language SDK
  parity, and managed Cloud / Enterprise tiers. Not covered here - and since v15 the upstream
  `quickstart/index.md` is a LanceDB quickstart, so it is left out of the mirror.

**The wider ecosystem** (separate repos, own version lines, none covered here): Flink streaming
writes (`lance-flink`), PostgreSQL reads via `pglance`, read-only Apache Doris queries, a Cypher
graph engine (`lance-graph`), a dataset browser (`lance-data-viewer`), agentic context management
(`lance-context`), and namespace catalogs for Hive, Polaris, Gravitino, Unity Catalog, AWS Glue,
Iceberg, BigLake, Dataproc and OneLake.
The canonical docs site is **`lance.org`**. Generated per-language SDK docs live at
`lance-format.github.io/lance-python-doc` for Python and
[javadoc.io](https://www.javadoc.io/doc/org.lance/lance-core/latest/index.html) for Java - the
matching `lance-format.github.io/lance-java-doc` path 404s.

Linking the `lance` crate in `Cargo.toml` means you are using Lance directly - use this skill.
For LanceDB internals, the storage layer underneath is still Lance, so this skill remains the
authority for the format itself.

**The wrapper can hide format features.** LanceDB's `create_table` cannot enable stable row IDs;
only pylance's `write_dataset(enable_stable_row_ids=True)` can. If a format-level capability
matters to your design, check whether the wrapper exposes it before assuming the underlying
format settles the question - and reach for `pylance` directly when it does not.

## The crate workspace

28 crate directories under `rust/` at `v15.0.0-beta.10` - #10251 split DataFusion-free execution
helpers into **`lance-datafusion-exec`** (27 through every v14 tag). **`lance` is the public entry
point** - `Dataset`, scanner, indexes, commits; everything else (`lance-table`, `lance-file`,
`lance-encoding`, `lance-index`, `lance-io`, `lance-core`, `lance-datafusion`, `lance-linalg`,
`lance-namespace*`, `lance-jsonb`, ...) is a layer beneath it. Edition 2024; Python bindings need
3.10+.

| Line | arrow | datafusion | pyo3 | MSRV |
|------|-------|------------|------|------|
| v15 betas (#10397, from beta.5) | 59.2 | 55 | 0.29 | 1.95.0 |
| v14.0.x | 58 | 54 | 0.28 | 1.94.0 |

Full table with roles, versions, and every workspace dep in `references/format-file.md` section 2.

**Build prerequisites differ by line.** Through v14, six crates compile protobufs in `build.rs`,
so every consumer build needs a real `protoc` (or the `protoc` cargo feature, which vendors
`protobuf-src`); a toolchain-manager `protoc` shim can fail there because build scripts run from
the cargo registry, outside the project's pin file - point `PROTOC` at a real binary. Since
#10216 (v15) the generated code is checked in and a default Rust build never invokes `protoc`.
The default features pull in nine storage backends; trim `default-features` when you do not need
them - the lance stack is expensive to compile.

**If you depend on anything below `lance`, expect moves.** v11 deleted `lance-encoding::version`
with no re-export (`LanceFileVersion` and `ConcreteFileVersion` live in `lance-file::version`),
removed `lance_io::encodings`, and gave each format its own `versions/v2_{0,1,2,3}` module
(#8020-#8026). The transaction code moved to a `rust/lance-table/src/transaction/` module tree
(#8053/#8054/#8056); a `lance::dataset::transaction` shim still re-exports `Operation`,
`Transaction`, `TransactionBuilder`, `RewriteGroup` and `UpdateMap`. v14 and v15 removed the
`lance-linalg` batch distance functions outright (#10086, #10088 - "lance-linalg as internal")
and `PlannerIndexExt` (#10251). Section 2.1.

## File format versions

The file format carries a single major.minor version. `data_storage_version` is set per dataset
at creation - but since `v12.0.0` it is **no longer fixed once the dataset exists**. It is the
*default* for writes that omit a target: "Create and overwrite establish this default; append,
update, merge-insert, and compaction do not change it." An existing V2 dataset can take `"2.0"`,
`"2.1"`, `"2.2"` or `"2.3"` per operation without rewriting its other files (#8582-#8585), so one
dataset can hold data files at several exact V2 versions. **V1 and V2 still cannot be mixed.**
Section 3.

| Version | Status | Notes |
|---------|--------|-------|
| `0.1` (`legacy`) | deprecated | Original format. The docs call it "no longer writable", but the code still writes it; since v15 creating a dataset on it logs a removal warning (#9476) |
| `2.0` | stable | Removed row groups; null support for lists/FSL/primitives |
| `2.1` | previous default | Adaptive structural encodings; better integer/string compression; nulls in struct fields; better nested random access. Was the default from Lance 5.0.0 until `v12.0.0-beta.15` |
| `2.2` | **current default** (`stable`) | Map type, Blob v2, `VariablePackedStruct`, larger mini-blocks. Required for Map and Blob v2 |
| `2.3` | unstable (`next`) | **Planar layout** since `v14.0.0-beta.22` (#9920-#9922): a structure plane plus a value plane, with sparse as a structural policy. Codecs ALP/ALP-RD (default `auto`) and AxisDelta for integer tensors; Pcodec is a format definition only (no decoder yet, #10617). **"Earlier unstable 2.3 files have no compatibility path"** - rewrite them. Stable readers refuse it |

**`stable` resolves to 2.2** (#8657), and `2.2` is the enum `#[default]`, so a dataset created
without an explicit `data_storage_version` is written as 2.2 - Python's `write_dataset` inherits
it. **The docs still do not say so** - `format/file/versioning.md` only calls `stable` an "alias
for the default version" - so the code is the authority. `next` resolves to 2.3; there is no 2.4.
Pin an explicit number for deterministic behavior across builds: anything relying on
`WriteParams::default()` (tests, benches) silently changed format at the 2.2 switch.

On v12, a writer defaulting to 2.2 rejected legacy blob metadata outright. **Since `v13.0.0`**
(#9459) legacy blob metadata written to 2.2+ is converted to Blob v2, and a 2.0/2.1 table can
append Blob v2 without a rewrite. Blob v2 tiers by size: **64 KiB inline, 4 MiB dedicated**,
packed `.blob` sidecars between (the pre-v14 docs said 16 KiB / 2 MiB; the code never did). The
full Blob v2 spec is now `format/table/blob.md`.

The release *selectors* (`LanceFileVersion`) are a type distinct from the persisted identity
(`ConcreteFileVersion`). Details in `references/format-file.md` sections 3.1 and 3.6.

## Version landscape

The major is bumped by a bot, not a human: `ci/publish_beta.sh` re-roots at `MAJOR+1` whenever
any PR since the release root carries the GitHub `breaking-change` label - the marker is the
**label**, not a conventional-commit `!`. A major bump therefore means "some labeled breaking
change landed", not a redesign. It has fired on **eight consecutive lines** (7.2, 8.1, 9.1, 10.1,
11.1, 12.1, 13.1, 14.1): the last minor final ever shipped is `v7.1.0`. 14.1 was never tagged -
its release root and the 15 root sit on the same commit, about 16 hours apart, and the only
trigger was #10102 (zone write seeds V1). A `.1` beta pin is a dead end, never an early minor.

Finals: `v10.0.0` (2026-08-08), `v11.0.0` (2026-08-30), `v12.0.0` (2026-09-17), `v13.0.0`
(2026-10-07), `v14.0.0` (2026-10-26), then **`v14.0.1` and `v14.0.2`** - the first `x.0.N` patch
releases since `v9.0.1`. Finals and patches are cut on a stabilization branch
(`release/v14.0`), **not an ancestor of `main`**: rc tags, a vote, then the final; fixes reach it
as backport PRs with **new numbers** (#10363 -> #10364), so match a fix by title, not PR number. A
`x.y.z-beta.0` version on the branch means that patch is unreleased.

| Major | Its breaking theme |
|-------|--------------------|
| **v15** (current, `v15.0.0-beta.10`) | Zone write seeds V1 activates sticky bit 16 from default ZoneMap options (#10102, re-rooted the major); arrow 59 / DataFusion 55 / pyo3 0.29, MSRV 1.95 (#10397); `PlannerIndexExt` removed (#10251); Python classes moved to `lance._dataset.*` with no aliases (#10602); Bitmap/LabelList row-address versions (#9814). Delta below |
| **v14** (`v14.0.0` 2026-10-26; `v14.0.2` 2026-10-29) | `ScalarIndexPlugin::load_index` takes `index_version` (#9518, re-rooted the major); BTree v1 stores row addresses (#9481); jsonb vendored as `lance-jsonb` (#9534); 2.3 Planar grammar (#9920-#9922); `lance-linalg` batch fns removed (#10086); `delete_concurrency` (#9774). Unlabeled: inline transaction moved to manifest field 23 plus `Operation::Unknown` (#9482) |
| **v13** (`v13.0.0`, 2026-10-07) | `WriteParams.file_writer_options` (#9192); lazy page-metadata init with a per-page metadata cache key (#7465); `json_extract`/`json_get` stop routing to JSON indices (#9101); BM25F (#7905); JSON accessor API (#9479); `merge_columns` field ids (#9547); duplicate-pair output (#9551); covering-fields spec split (#9159) |
| **v12** (`v12.0.0`, 2026-09-17) | `WrappingObjectStore::wrap_paginated` (no default); MemWAL `ShardManifestStore` narrowed; `lance-namespace` response objects; predecessor-conditioned external stores; namespace merge-insert key lists; caller-provided Writer / `open_part` removed (#9072). Unlabeled but bigger: `stable` -> 2.2 and the IVF_RQ 5-bit default |
| **v11** (`v11.0.0`, 2026-08-30) | Fragment ids became a dataset-lifetime high-water mark; `lance-file` / `lance-encoding` reorganization; transaction code moved to `lance-table`. Net-new: covering indexes, `merge_insert` `write_mode`, row-address prefilter |
| **v10** | Blob APIs preserve null selections; cache keys became opaque BLAKE3 digests; async `create_remapper`; MemWAL renamed generation -> SSTable |
| **v9.1** (never released; renamed into v10) | FTS/inverted creation took a `block_size` param. Net-new: Data Overlay Files (unstable, env-gated), sparse structural pages, `lance-index-core` |
| **v9** | Python 3.9 dropped; `alter_columns` fails fast when casting an indexed column; FM-Index proto rename; FTS defaults to on-disk format v2 |
| **v8** | All index builds unified onto one segment-based lifecycle. Net-new: `lance-derive`, FM-Index, multi-bit IVF_RQ, `approx_mode`, TOS + GooseFS |
| **v7** | MemWAL, branches, the geo/RTree index, the `lance-select` crate, ICU FTS |

**`v14.0.2` is the stable pin** and what GitHub Releases marks `Latest`; `v14.0.3` exists only as
`v14.0.3-rc.1`. crates.io carries **finals only** and newest `lance 14.0.2` - **`14.0.0` never
reached crates.io** (its `cargo publish` failed on a `[patch.crates-io]` git pin, fixed by #10364),
so the Rust floor of the v14 line is 14.0.1; PyPI `pylance` has 14.0.0 through 14.0.2. A beta pin
means a git dependency - beta and rc wheels publish to fury.io (`https://pypi.fury.io/lance-format`),
which carries `pylance-15.0.0b1` through `b10` (b5-b9 lack the macOS arm64 wheel). Maven's
`maven-metadata.xml` `<release>` field includes betas - it is not a stable signal.

Full per-tag deltas with every PR citation: `references/changelog-v7-v15.md`.

## Manifest feature flags

A reader or writer refuses a manifest that sets a bit it does not support. The supported set is
`FLAG_UNKNOWN - 1` minus whatever the build masks out, so **the docs table is not the authority -
`rust/lance-table/src/feature_flags.rs` is**. Bits 0-6 are long-standing (deletion files, stable
row IDs, the deprecated v2 marker, table config, base paths, disabled transaction file, and the
env-gated data overlay files). Everything from bit 7 up arrived in the last five majors, and
`FLAG_UNKNOWN` moved `1 << 9` (v12.0.0) -> `1 << 14` (v13.0.0) -> `1 << 18` (v14.0.0) ->
`1 << 20` (v15 line):

| Bit | Flag | Status at `v15.0.0-beta.10` (v14.0.x where it differs) |
|-----|------|-----------------------------|
| 7 | `FLAG_COVERED_INDEX_METADATA` | Supported since v11 final (#8535) |
| 8 | `FLAG_MIXED_DATA_FILE_VERSIONS` | Supported since v12 final; sticky; a half-set manifest is a hard error |
| 9 | `FLAG_FRAG_REUSE_WITH_STABLE_ROW_IDS` | **Debug builds only** - release builds refuse it. Docs say reader/writer `Yes` |
| 10 | `FLAG_FRAGMENT_REUSE_INDEX` (tagged FRI) | Supported since `v13.0.0` (#9420); sticky |
| 11 | `FLAG_SPILLED_ROW_LINEAGE` | Supported in every build since `v14.0.0-beta.16` (#9802, #9886); the `FLAG_UNSTABLE_*` name is a deprecated alias. Spilling is opt-in via `lance.row_lineage.spill=true` |
| 12 | `FLAG_FRAGMENT_TREE` | Reserved; rejected until implemented, though the spec exists (#9060) |
| 13 | `FLAG_INDEPENDENT_COVERING_FIELDS` | Reserved and **masked out**. Docs present it as normative |
| 14 | `FLAG_MANAGED_BLOBS` | Sticky; explicit opt-in via `lance.blob.managed=true` since `v14.0.0-beta.14` |
| 15 | `FLAG_NON_REUSABLE_FIELD_IDS` | Writer-only, sticky (#8658) |
| 16 | `FLAG_ZONE_WRITE_SEEDS` | Paired, sticky. Supported in v15 (#10102); masked out in every v14 tag |
| 17 | `FLAG_OBJECT_METADATA` | Writer-only; set whenever the manifest carries clustering or nonempty fragment/index metadata (#10383). Masked out in v14 |
| 18 | `FLAG_ROW_ADDR_INDICES` | v15 only (#10352); writer-only fence for row-address-domain indexes |
| 19 | `FLAG_INLINE_DELETIONS` | v15 only (#10164); paired - deletion vectors stored inline in the manifest |

"Sticky" means the bit survives every later commit (`STICKY_PAIRED_FLAGS` = bits 8, 10, 14, 16;
`STICKY_WRITER_FLAGS` = bit 15), so setting it once permanently raises the reader floor of the
table. **The v15 docs lag the code for once**: `format/table/versioning.md` still says "Bits 16
and 17 are reserved but remain unsupported" while the build supports both.

**Three pin hazards open a table they should refuse - or brick it for older readers.**

- **Do not pin `v11.0.0-beta.4` through `beta.17`.** Those builds read bit 7 as a retired MemWAL
  flag they support, so they *open* a covering-index dataset instead of refusing it - wrong
  neighbours, no error.
- **Do not pin `v14.0.0-beta.4` through `beta.13`.** Any ordinary Blob v2 write there sets
  `FLAG_MANAGED_BLOBS`, which is sticky, so `v13.0.0` can never open the table again. #9891
  (beta.14) made it explicit opt-in, but **the docs in every v14 tag, `v14.0.2` included, still
  describe automatic activation** ("Publishing a new data file containing a Blob v2 field
  activates the Managed Blob capability"); the v15 docs are corrected (#9193). Trust the code.
- **One v15 write can lock out every v14 client.** A ZoneMap built with *default* options seeds
  string, binary, decimal, wide fixed-size-binary and nested columns, which sets sticky bit 16 -
  "This can happen with default ZoneMap options, not just an explicit `use_seeds: true`" (#10102).
  Inline deletions (`lance.deletions.inline_max_bytes`) are a one-way migration too. Keep v15
  writers off a table that v14 readers still need. Mixing v14 and v15 *writers* on a stable-row-ID
  table is worse: see the #10352 fence below.

**Covering indexes** (#8535) - `IndexMetadata.covering_fields` (proto field 11) names the
columns an index *carries* values for, so a query projecting only those is answered without a
base-table take. Under the contract every released build implements, **the carried columns are
the trailing suffix of `fields`** in emission order, and a column the index is both keyed on and
carries appears twice: "`fields = [1, 1]` with `covering_fields = [1]` is keyed on `1` and
carries `1`." #9159 specified an independent contract behind bit 13 (`fields` holds only keys),
but the build masks that bit, so it is spec only. Invalidation is wide either way: **any** index
whose `fields` include the updated column. V3 IVF auxiliary files can physically carry columns
("a reader discovers carried columns by exclusion, not by position"), bound by a
`covering_field_ids` metadata key, and coverage is per-segment. Section 11.

## The v14 final and v15 delta

**145 commits** from `v14.0.0-beta.14` to the `v14.0.0` final, 14 more across the patches to
`v14.0.3-rc.1`, and **532** on the v15 line to `beta.10`. Invariants: **17 transaction ops**,
`CommitConfig.num_retries` still 20, `stable` still 2.2, lance-namespace pins unchanged (Rust
client 0.13.0, Java 0.12.0, Python `>=0.13.0,<0.14`).

**Indexes are moving to the physical row-address domain**, versioned per index. BTree v1 (#9481,
v14, labeled breaking) stores `_rowaddr` - only on stable-row-ID tables; v13 readers skip a v1
segment with a warning and scan; external builders (Spark) must switch to row addresses. Bitmap
v1 and LabelList v2 follow in v15 (#9814). FTS v4, NGram v1, RTree v1, MinHash v1 and vector v3
are **spec only** at `v15.0.0-beta.10` (#10299: "No implementation changes are included").
"Stable row IDs do not make index maintenance unnecessary" - compaction still remaps or rebuilds.
**#10352 (v15.0.0-beta.7) is the writer fence** (bit 18): "Older writers may treat its entries as
stable row IDs and extend coverage to rewritten fragments without indexing them, silently losing
query results." It is not in any v14.0.x tag, and it repairs nothing already damaged - rebuild.

- **Compile breaks (v15):** `PlannerIndexExt` -> `create_filter_plan(...)` and
  `lance_geo::register_functions` gone (#10251); cosine batch fns removed (#10088);
  `OldIndexDataFilter::RowAddresses` (#10418); `NamespaceError::Throttling { retry_after }`
  (#10400); `ManifestLocation.last_modified` (#9438); RaBitQ query context `#[non_exhaustive]`
  (#9190). Python: `Tag`, `Branch`, `IndexFile`, `DatasetStats`, `SqlQuery` and others moved to
  `lance._dataset.*` - "No compatibility aliases or forwarding wrappers are retained" (#10602).
- **Silent behavior changes:** HNSW default `ef` is floored at 256 (#9073, was `1.5*k`) - recall
  up sharply, latency 2-3.5x; IVF builds sized by `num_partitions` now record
  `target_partition_size` (#10154), so optimize stops collapsing partitions; unknown URL schemes
  get `ConditionalPutCommitHandler` instead of the blind-writing `UnsafeCommitHandler` (#8773);
  auto-cleanup keeps tagged versions (#10541) and cleanup rejects a detached checkout (#10331);
  a stale Project or append now gets a retryable conflict instead of losing metadata (#10512,
  #10502). In v14: the AIMD ceiling rose 5000 -> 10000 req/s per controller (#10153), deletes
  got a request budget (#9707), REST namespace `count_rows` / `list_table_tags` / `stats` moved to
  POST so an older client gets 405 (#9993), and S3 `aws_copy_if_not_exists` defaults to
  `multipart` from 14.0.1.
- **Net-new format surface:** inline deletion vectors (bit 19), clustering metadata (#9878,
  #10383), generic fragment/index metadata maps (bit 17), an advisory `file_metadata_size_bytes`
  footer hint (#9168), `DataReplacement.data_change` (#9705), caller-chosen field ids via
  `lance:field_id` (#9898), MemWAL `dir_id` / `sealed_by` with no flag guard (#10432), ZoneMap V1
  statistics (#10217, #9986), and a `table_config.md` registry of `lance.` keys every
  implementation must honor. **The JSONB spec was reverted** (#9889, a vetoed format vote; #9905
  still open) - the `lance-jsonb` crate stays, the spec page is gone.
- **Net-new features (v15):** version retention policies (`CleanupPolicy`, `KeepOne`,
  `RemoveAll`, `expire_versions`; #10306) and `restore_from` (#10556); spillable sort-merge
  update joins (#9129, `guide/update_join.md`); external scalar index plugins (#10111, unstable);
  `consolidate` for vector segments without retraining (#10335); `ManagedBlobWriter` (#10233);
  opt-in `local_fsync` (#9609); `session().cache_diagnostics()` and `lance_cache_*` metrics
  (#9781). An experimental PCA pre-transform for IVF_RQ is in the code since v14.0.0 (#9967,
  spec #9968), but no creation API exposes it yet.

**Fixes needing a rebuild, rewrite or repair, not just an upgrade.** On **13 -> 14, rebuild FTS
indexes** built with `remove_stop_words` (the default for non-ngram tokenizers) or for the affected languages (Latin stop-word lists,
Arabic, Greek, Russian, Tamil, Korean, CJK): "Existing FTS indices must be rebuilt to align stored
terms with the updated tokenizer" (#10045-#10052). v14 final: dedupe after #9865 (indexed
merge_insert on overlays inserted duplicates); rebuild after #10109, #10003, #10004, #10041;
re-clone after #9768. #10145 (RLE dictionary pages unreadable) and #10454 (legacy blob in 2.2,
in `v14.0.3-rc.1` only) are read-side - upgrade the reader. `v14.0.2` fixes wrong nulls from
nullable struct merges (#10412). **v15 only, not backported:** rebuild FTS indexes whose segments
were merged under stable row IDs before #9872 (stale postings are carried into the merged
segment; #9785 is the query-time half) and cosine IVF_PQ built with `accelerator=` (#9755);
#10408 (WAND top-k), #10559 and #9638 are query-time and heal on upgrade; restore after #10080 (constant-first spatial predicates inverted a delete)
and the cleanup-deleted-branch-files family (#10327, #10392, #10447, #10488, #10489); rewrite
after #9958 / #9963. Address-domain indexes - ZoneMap, BloomFilter, FM-Index, and now BTree,
Bitmap and LabelList - lose coverage of compacted fragments rather than claim them (recalculated
when a fragment reuse index is present, #9514), and one damaged under v10 or earlier needs
recreating. Conditions for each in `references/changelog-v7-v15.md`.

**Security:** PyO3 RUSTSEC-2026-0176/0177 are fixed from `v15.0.0-beta.5` (#10397, closing
#9647) and **unfixed in every v14 tag**.

## Earlier majors in brief

**v14 betas and v13 final** - #9482 moved the inline transaction from manifest field 21 to **23**
and added `Operation::Unknown` (labeled `format-change` only, so exhaustive `match` broke without a
`breaking-change` label). `merge_columns` field ids come from the manifest (#9547; the bug made
merged columns **silently read back as null**). BM25F `CombinedFieldsQuery` (#7905). One JSON
accessor (#9479), jsonb vendored (#9534), and only `json_get_int` / `_float` / `_bool` / `_string`
reach a JSON index (#9101) - `json_extract` / `json_get` silently full-scan. Default IVF probing
moved unlabeled: #9184 adaptive bounds, #9467, and #9798 `search_effort` (0 to 1, resolved to 0.5;
overrides `nprobes`). Explicit cloud storage options beat env vars (#9719); `fast_search` no
longer adds `_rowid` (#9699); `main` is the reserved default-branch alias (#7180); raw deep-Clone
commits are rejected (#9555); the DataFusion memory pool is 150MB per *effective* partition with
per-execution pools (#9183, #9408). New: tagged FRI (#9420), the fragment metadata tree spec
(#9060), spilled row lineage (#9253), non-reusable field ids (#8658), MinHash LSH (#9076/#9114).
Rebuild, rewrite or repair after #9018, #9239, #9394, #9421, #9352, #9203, #9218, #9219, #9573,
#9447, #9176, #9595, #9085, #9760, #9524, #9620, #7706, #9857.

**v13 betas** - `WriteParams.file_writer_options` (#9192, struct literals fail to compile);
**lazy page-metadata init** (#7465): `StructuralFieldScheduler::initialize` takes
`requested_ranges`, and caching moved from per-column `FieldDataCacheKey` to per-page
`PageDataCacheKey`, so **every warm or persisted metadata cache cold-misses** across the upgrade -
the payoff is that "a cold point/range read's metadata IO is invariant to the column's total page
count". The FRI got a versioned on-disk contract (#9136). `inline_optimization_enabled` flipped
`true` -> `false` (#9180). `hf://` object store (#9236).

**v12** - mixed data-file versions shipped (#8581-#8585); `stable` -> 2.2 (#8657); **IVF_RQ
defaults to 5 bits**, ~4.4x the 1-bit index size (#8936; set `num_bits=1` to opt out);
`WrappingObjectStore` implementors must add `wrap_paginated` - "There is deliberately no default"
- and paged listing via `read_dir_page` means walking until the token is `None`, never until a
page comes back short; namespace merge-insert keys have **arity-dependent NULL semantics** (a
composite key's NULL "matches nothing"); Java's `lance-namespace` moved to 0.12.0 (#8979).

**v11** - fragment ids are a dataset-lifetime high-water mark (#8206): overwrite no longer
restarts at 0, and datasets with duplicate ids read but no longer commit. `LanceFileVersion` lost
`Ord` (#8027/#8028). `Operation::Project` / `Merge` gained `preserves_nullability` (#8347). The
external-manifest protocol made object storage authoritative (#8499) - a retained ETag makes
readers reject a good manifest with `Manifest e_tag mismatch`. #8101 silently duplicated rows on
nullable primary keys under repeat `merge_insert`; existing duplicates must be removed by hand.
Rebuild HNSW indexes hit by #8834 (v11) or #9053 (v13 betas).

## Performance questions

For anything performance-shaped - slow scans or searches, remote/object-storage cost, index
maintenance cost, memory sizing, version bloat, benchmarking - load
`references/performance.md` first. Part A routes to the official guidance plus the undocumented
source-derived changes; Part B is field-verified practice against S3-compatible storage. The
governing rule stays **minimize remote calls** - fewer commits, fewer scans, fewer round trips -
because that is where the order-of-magnitude wins are. The official **"Tuning remote scans"**
section gives a starting point for cross-region or public-internet access, where the cloud
default of 64 concurrent requests is too aggressive: `LANCE_IO_THREADS=8`,
`fragment_readahead=1`, `batch_readahead=2`, `io_buffer_size=64MB`. It is a legitimate second
move once call volume is already minimized. A "Throttle error detected" log is not proof of a
rate limit: the AIMD classifier counts any retry-exhausted error as a throttle, so the fix is
fewer requests, not wider `LANCE_AIMD_*` limits.

**AMX-FP16** (#8540) is the one performance change that alters *results*, not just speed: where
it engages, IVF partition assignment becomes **exact instead of approximate**, so recall improves
*and* assignments differ from an older build. It is shape-gated (`float16` + `dot`,
`dimension >= 32`, `num_centroids >= 32`). `LANCE_DISABLE_AMX=1` disables it and reverts
assignment to the approximate path too. The v15 HNSW `ef` floor (#9073) changes latency and recall
at default settings - re-benchmark rather than carry numbers forward.

Two cache facts to know before tuning anything remote: Lance has **no resident data cache** (a
`Session` holds only index and metadata caches, never decoded values, so repeated point reads
re-pay object-store IO), and one `Arc<Session>` shared via `DatasetBuilder::with_session` lets
datasets share it. Cold first search is dominated by paging indexes in - `prewarm_index` is the
remedy, and for FTS it loads the whole inverted index into RAM. #7465 changed the metadata cache
key shape, so the first run after a v13 upgrade re-pays that paging even against a warm cache.
v15's `cache_diagnostics()` (#9781) shows what the caches actually hold.

**Layout debt is version-dependent.** Binary-copy compaction of small appends preserves tiny
pages; a reader that pays per page (v12) turns that into tens of thousands of GETs per lookup.
Re-encode append-heavy tables, and benchmark on a fresh copy of the real store - details and
measurements in `references/performance.md` Part B.

**Time travel is not an archive mechanism.** Versions look like free history, but
`cleanup_old_versions` with no arguments removes every version **older than 14 days** (Python
default and `AutoCleanupParams`), and cleanup is part of routine maintenance - so a design that
treats old versions as the durable record loses them on the first pass. Auto-cleanup itself is
**opt-in** (`WriteParams.auto_cleanup` defaults to `None`); v15 adds retention policies and keeps
tagged versions. Keep an explicit archive if you need one. The reverse also holds: `delete` alone
does not erase data - old versions, unrewritten fragments, and indexes (deletes do not conflict
with index creation) all keep it until rewritten, cleaned up, and rebuilt. Cleanup reports
partial failure in `RemovalStats.failed_deletes` and still returns `Ok` (#9414) - check it where
completeness is a contract.

## Official docs mirror

`references/docs/` mirrors `docs/src` of `lance-format/lance` at the tracked tag, verbatim -
61 markdown files plus 5 diagrams, all directly readable.

| Directory | Files | Covers |
|-----------|-------|--------|
| `guide/` | 20 | CRUD, performance, object store, distributed write + indexing, JSON, tokenizers, data types, data evolution, blob, arrays, tags/branches, migration, observability, row IDs, indexing, vector search, scalar indexing, full-text search, update joins |
| `quickstart/` | 7 | PyLance getting started, versioning, vector search, full-text search; Rust; Java; Spark |
| `format/` | 1 | Spec-stack overview |
| `format/file/` | 3 | Container spec, structural encodings + compression (incl. the 2.3 Planar layout), format versions |
| `format/table/` | 13 + 1 svg | Layout, schema, transactions (**conflict-resolution matrix**), versioning, row-id lineage, branch/tag, MemWAL, data overlay files, fragment metadata tree, clustering, Blob v2, table config keys |
| `format/index/` | 1 + 4 svg | Index lifecycle, fragment coverage, compaction interplay, covering contracts |
| `format/index/scalar/` | 12 | fts, fmindex, ngram, btree, bitmap, bloom_filter, label_list (`array_has_any/all`), zonemap, zone_write_seeds, rtree, json, minhash_lsh |
| `format/index/vector/` | 1 | IVF / PQ / SQ / RQ / HNSW / PCA concepts and storage layout |
| `format/index/system/` | 2 | Fragment reuse index, MemWAL system index |
| `integrations/` | 1 | DataFusion SQL over Lance, incl. JSON functions |

**Not mirrored:** `docs/src/images/` and the `format/*.png` assets, so image links in the
mirrored pages do not resolve - the prose is self-contained, and the five `.svg` diagrams *are*
mirrored. Also out by design: `quickstart/index.md` (a LanceDB quickstart since v15), `community/`,
`examples/`, `integrations/{index,pytorch,tensorflow}.md`; and the landing stubs and contributor
files (`format/AGENTS.md`).

**A whole tier of docs is not in this repo at all**, so it cannot be mirrored and cannot be
enumerated from a clone. `docs/make-full-website.sh` assembles `format/catalog`,
`format/namespace`, and the integration sections (DuckDB, HuggingFace, Spark, Ray, Trino, Flink,
Context, ...) at build time from nine sibling repos with their own version lines - the checked-in
`integrations/index.md` links `duckdb/index.md`, `trino/index.md` and similar as if they were
local, but those paths do not exist in the tree. For any of those, read `lance.org` rather than
this mirror. Protobuf message bodies are likewise expanded at build time from `protos/` by
`mkdocs_protobuf`, so the mirrored spec pages show `%%% proto.message.X %%%` placeholders where
the site shows a rendered schema.
