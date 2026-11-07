---
name: qdrant-migration-tool
description: "Guides use of the Qdrant Migration Tool CLI to move vectors, metadata, and sparse embeddings from another vector database into Qdrant. Use when someone asks 'how do I migrate from Pinecone/Weaviate/Milvus/Elasticsearch/OpenSearch/pgvector/s3/Azure/Chroma/Redis/MongoDB/FAISS/Solr to Qdrant', 'move my vector database to Qdrant', 'is there a migration tool for Qdrant', 'my migration got interrupted, how do I resume it', 'migration is too slow', or 'collection wasn't created after migration'. Also use when picking migration batch size, deciding on `--net=host`, or verifying data after a migration."
---

# Qdrant Migration Tool

The tool is a Docker container (`registry.cloud.qdrant.io/library/qdrant-migration`), not a library you import. It streams data in batches through the machine it runs on rather than connecting source and target directly, and it resumes by default rather than restarting from scratch. [Migrate to Qdrant](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/)

## Picking the Right Subcommand

Use when: starting a new migration and choosing the source-specific CLI subcommand.

- Match the source to its subcommand: `pinecone`, `weaviate`, `milvus`, `elasticsearch`, `opensearch`, `pg` (pgvector), `s3` (S3 Vectors), `azure` (Azure AI Search), `chroma`, `redis`, `mongodb`, `faiss`, `solr`, or `qdrant`. [Migrate to Qdrant](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/)
- Weaviate, Redis, MongoDB, and Apache Solr do not auto-create the target collection; create it in Qdrant first with matching vector size and distance metric before running the migration. All other sources auto-create it.
- Each source has its own credential and mapping guide; read it before running the migration, since concept mapping (namespaces, indexes, metadata fields) is source-specific. [Pinecone](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/from-pinecone/) [Weaviate](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/from-weaviate/) [Milvus](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/from-milvus/) [Elasticsearch](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/from-elasticsearch/) [OpenSearch](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/from-opensearch/) [Azure AI search](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/from-azure-search/) [pgvector](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/from-pgvector/) [S3 Vectors](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/from-s3-vectors/) [Chroma](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/from-chroma/) [Redis](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/from-redis/) [MongoDB](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/from-mongodb/) [FAISS](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/from-faiss/) [Apache Solr](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/from-solr/) [Qdrant-to-Qdrant](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/from-qdrant/)
- Source not listed? Point to the GitHub issue tracker rather than improvising a custom pipeline. [Open an issue](https://github.com/qdrant/migration/issues)

## Running Against Local Instances

Use when: either the source or target database runs on the same machine as the migration container.

- Add `--net=host` to the `docker run` command; without it, the container cannot resolve `localhost` on the host machine. [Migrate to Qdrant](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/)
- Run the container on a machine with low latency to both databases. Direct source-target connectivity is not required since the tool streams through wherever it runs, but round trips from the migration host to each database still add up.

## Migration Was Interrupted

Use when: a migration stopped partway through and needs to continue, or needs to be re-run from zero.

- Re-run the exact same command. Progress is tracked in the `_migration_offsets` collection in Qdrant, so it resumes automatically rather than re-copying already-migrated points.
- Pass `--migration.restart` to discard saved progress and start over, e.g. after fixing a bad source-side filter or changing collection schema mid-migration.
- Custom offsets-collection name only matters if you're running multiple concurrent migrations into the same Qdrant instance; otherwise leave `--migration.offsets-collection` at its default to avoid tracking state you'll forget to look for later.

## Migration Is Too Slow

Use when: throughput is too low for the size of the source dataset.

- Raise `--migration.batch-size` from the default of 50 to 256 or 512 for large migrations; small batches under-use each upsert round trip.
- `--migration.num-workers` only exists for the `pg` and `qdrant` subcommands; other sources have no parallel-worker flag, so throughput there is bounded by batch size and network proximity alone.
- `--migration.batch-delay` defaults to 0; only raise it deliberately to throttle load on a source database that can't absorb full-speed reads, not as a default tuning knob.
- Run the container close to both databases rather than over a slow network path, since the tool has no way to compensate for source/target latency.

## After Migration

Use when: the migration command finished and data needs to be trusted before cutting over traffic.

- Run through the verification framework rather than spot-checking a few points: it covers pre-migration baselines, data integrity checks, and search-quality validation, not just point counts. [Migration Verification Guide](https://skills.qdrant.tech/md/documentation/migration-guidance/)
- If Postgres/pgvector stays live alongside Qdrant post-migration, set up an ongoing sync strategy (event-driven, batch, or dual-write) instead of treating the migration as a one-time cutover. [Keeping Postgres in Sync](https://skills.qdrant.tech/md/documentation/data-synchronization/)

## What NOT to Do

- Assume Weaviate, Redis, MongoDB, or Solr auto-create the target collection; these sources don't expose vector dimensions or distance metric to the tool, so the collection must be created manually first with settings that exactly match the source. [Migrate to Qdrant](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/)
- Point the `faiss` subcommand at a quantized FAISS index; only `IndexFlatL2`, `IndexFlatIP`, `IndexHNSWFlat`, and `IndexIVFFlat` are supported, since quantized indexes don't retain the original vectors. [FAISS](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/from-faiss/)
- Assume every Pinecone index can be migrated; only serverless indexes support the list operation the tool needs to enumerate vectors.[Pinecone](https://skills.qdrant.tech/md/documentation/migrate-to-qdrant/from-pinecone/)
- Run a `qdrant`-to-`qdrant` migration into an existing target collection without checking its vector size first; source and target dimensions must match exactly, only replication and shard settings are allowed to differ.
- Connect over TLS to a source or target signed by a private or self-signed CA without mounting it via `SSL_CERT_FILE`; the migration fails on certificate verification instead of degrading gracefully, and `--skip-tls-verification` should be a deliberate override, not a default fix. 
- Pass `--migration.restart` out of caution on a healthy resume; it discards saved progress and re-streams data that already migrated.
- Treat a completed migration run as verified without running data integrity and search quality checks.
