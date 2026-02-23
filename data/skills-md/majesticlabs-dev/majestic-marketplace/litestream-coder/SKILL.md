---
name: litestream-coder
description: This skill guides configuring Litestream for continuous SQLite backup in Rails 8+ apps. Use when setting up production backups for SQLite databases (Solid Queue, Solid Cache, Solid Cable).
allowed-tools: Read Write Edit Grep Glob Bash
---

# Litestream Coder

## Overview

Litestream provides continuous streaming backup for SQLite databases to S3-compatible storage. Essential for Rails 8+ apps using SQLite in production with Solid Queue, Solid Cache, and Solid Cable.

## Configuration File

Create `config/litestream.yml`:

```yaml
dbs:
  - path: /rails/storage/production.sqlite3
    replicas:
      - type: s3
        bucket: ${BUCKET_NAME}
        path: sqlite/production
        endpoint: ${S3_ENDPOINT}
        region: ${S3_REGION}
        access-key-id: ${LITESTREAM_ACCESS_KEY_ID}
        secret-access-key: ${LITESTREAM_SECRET_ACCESS_KEY}
        force-path-style: true       # Required for S3-compatible storage
        sync-interval: 5s            # How often to sync WAL
        snapshot-interval: 1h        # Full snapshot frequency
        retention: 168h              # 7 days
        retention-check-interval: 1h
        validation-interval: 12h
```

## Retention Strategies by Database Type

**Primary database (production.sqlite3):**
- `sync-interval: 5s` - Frequent syncing for data durability
- `snapshot-interval: 1h` - Hourly snapshots
- `retention: 720h` - 30 days for recovery

**Cache database (production_cache.sqlite3):**
- `sync-interval: 10s` - Less critical, reduce load
- `snapshot-interval: 6h` - Less frequent
- `retention: 24h` - 1 day sufficient

**Queue database (production_queue.sqlite3):**
- `sync-interval: 5s` - Important for job durability
- `snapshot-interval: 1h` - Hourly
- `retention: 72h` - 3 days for debugging

**Cable database (production_cable.sqlite3):**
- `sync-interval: 10s` - Ephemeral data
- `snapshot-interval: 6h` - Infrequent
- `retention: 24h` - 1 day

## Complete Configuration Example

```yaml
dbs:
  - path: /rails/storage/production.sqlite3
    replicas:
      - type: s3
        bucket: myapp-backups
        path: sqlite/production
        endpoint: https://fsn1.your-objectstorage.com
        region: fsn1
        access-key-id: ${LITESTREAM_ACCESS_KEY_ID}
        secret-access-key: ${LITESTREAM_SECRET_ACCESS_KEY}
        force-path-style: true
        sync-interval: 5s
        snapshot-interval: 1h
        retention: 720h
        retention-check-interval: 1h
        validation-interval: 12h

  - path: /rails/storage/production_cache.sqlite3
    replicas:
      - type: s3
        bucket: myapp-backups
        path: sqlite/cache
        endpoint: https://fsn1.your-objectstorage.com
        region: fsn1
        access-key-id: ${LITESTREAM_ACCESS_KEY_ID}
        secret-access-key: ${LITESTREAM_SECRET_ACCESS_KEY}
        force-path-style: true
        sync-interval: 10s
        snapshot-interval: 6h
        retention: 24h

  - path: /rails/storage/production_queue.sqlite3
    replicas:
      - type: s3
        bucket: myapp-backups
        path: sqlite/queue
        endpoint: https://fsn1.your-objectstorage.com
        region: fsn1
        access-key-id: ${LITESTREAM_ACCESS_KEY_ID}
        secret-access-key: ${LITESTREAM_SECRET_ACCESS_KEY}
        force-path-style: true
        sync-interval: 5s
        snapshot-interval: 1h
        retention: 72h

  - path: /rails/storage/production_cable.sqlite3
    replicas:
      - type: s3
        bucket: myapp-backups
        path: sqlite/cable
        endpoint: https://fsn1.your-objectstorage.com
        region: fsn1
        access-key-id: ${LITESTREAM_ACCESS_KEY_ID}
        secret-access-key: ${LITESTREAM_SECRET_ACCESS_KEY}
        force-path-style: true
        sync-interval: 10s
        snapshot-interval: 6h
        retention: 24h
```

## Kamal 2 Deployment

Add Litestream as an accessory in `config/deploy.yml`:

```yaml
accessories:
  litestream:
    image: litestream/litestream:0.3
    host: <SERVER_IP>
    cmd: replicate
    volumes:
      - "myapp_storage:/rails/storage:ro"  # Read-only access
    files:
      - config/litestream.yml:/etc/litestream.yml
    env:
      secret:
        - LITESTREAM_ACCESS_KEY_ID
        - LITESTREAM_SECRET_ACCESS_KEY
    options:
      health-cmd: "litestream databases || exit 1"
      health-interval: 30s
      health-timeout: 5s
      health-retries: 3
```

**Key points:**
- Mount storage as read-only (`:ro`) - Litestream only reads WAL files
- Use same volume name as main app
- Health check verifies Litestream can see databases

## Secrets Configuration

In `.kamal/secrets`:

```bash
LITESTREAM_ACCESS_KEY_ID=$(op read "op://myproject/production-s3/access_key_id")
LITESTREAM_SECRET_ACCESS_KEY=$(op read "op://myproject/production-s3/secret_access_key")
```

## Disaster Recovery

### Restore Database

```bash
# Stop application first
kamal app stop

# Restore from latest backup
docker run --rm \
  -v myapp_storage:/rails/storage \
  -e LITESTREAM_ACCESS_KEY_ID="$(op read 'op://myproject/production-s3/access_key_id')" \
  -e LITESTREAM_SECRET_ACCESS_KEY="$(op read 'op://myproject/production-s3/secret_access_key')" \
  litestream/litestream:0.3 restore \
  -config /etc/litestream.yml \
  /rails/storage/production.sqlite3

# Restart application
kamal app start
```

### Point-in-Time Recovery

```bash
docker run --rm \
  -v myapp_storage:/rails/storage \
  -e LITESTREAM_ACCESS_KEY_ID="..." \
  -e LITESTREAM_SECRET_ACCESS_KEY="..." \
  litestream/litestream:0.3 restore \
  -config /etc/litestream.yml \
  -timestamp "2025-01-15T10:30:00Z" \
  /rails/storage/production.sqlite3
```

## Monitoring

Check backup status:

```bash
# Via Kamal
kamal accessory exec litestream -- litestream databases

# Direct on server
docker exec myapp-litestream litestream databases
```

## S3-Compatible Storage

Litestream works with any S3-compatible storage:

| Provider | Endpoint Example |
|----------|------------------|
| Hetzner Object Storage | `https://fsn1.your-objectstorage.com` |
| Backblaze B2 | `https://s3.us-west-002.backblazeb2.com` |
| DigitalOcean Spaces | `https://nyc3.digitaloceanspaces.com` |
| AWS S3 | (omit endpoint, use region) |

**Critical:** Always set `force-path-style: true` for non-AWS S3-compatible storage.

## Best Practices

- **Separate databases by retention needs** - Main DB needs longer retention than cache
- **Monitor backup lag** - `litestream databases` shows replication status
- **Test restores regularly** - Don't wait for a disaster to verify backups work
- **Use read-only mount** - Litestream only reads WAL files, `:ro` prevents accidents
