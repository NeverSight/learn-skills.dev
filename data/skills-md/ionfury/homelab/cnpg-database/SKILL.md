---
name: cnpg-database
description: |
  CloudNative-PG (CNPG) PostgreSQL database management for the Kubernetes homelab.
  Covers shared platform cluster, dedicated app clusters, credential chains, and monitoring.

  Use when: (1) Adding a new database for an application, (2) Creating a dedicated CNPG cluster,
  (3) Setting up database credentials and cross-namespace replication, (4) Configuring PgBouncer
  poolers, (5) Debugging database connectivity or CNPG cluster health, (6) Adding PostgreSQL
  extensions for specialized workloads.

  Triggers: "database", "postgresql", "postgres", "cnpg", "cloudnative-pg", "pooler",
  "pgbouncer", "database credentials", "db password", "managed roles", "Database CRD",
  "database cluster", "shared database", "dedicated database", "cnpg cluster"
user-invocable: false
---

# CNPG Database Management

Guide to provisioning and managing PostgreSQL databases using CloudNative-PG (CNPG) in the
homelab Kubernetes platform. The platform supports both a shared multi-tenant cluster and
dedicated per-application clusters.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Database Architecture                             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  database namespace                                                  │
│  ┌────────────────────────────────────┐                             │
│  │  Shared Platform Cluster           │                             │
│  │  ├─ platform-0 (primary)           │ ◄── cnpg-platform-superuser │
│  │  ├─ platform-1 (replica)           │     (stays in database ns)  │
│  │  └─ platform-2 (replica)           │                             │
│  │                                    │                             │
│  │  Managed Roles (CNPG-controlled):  │                             │
│  │  ├─ authelia, lldap, sonarr, ...   │ ◄── <app>-role-password     │
│  │                                    │     (secret-generator)      │
│  │  Database CRDs (CNPG-controlled):  │                             │
│  │  ├─ authelia, lldap, sonarr-main,  │                             │
│  │  │  sonarr-log, radarr-main, ...   │                             │
│  │                                    │                             │
│  │  platform-pooler-rw (PgBouncer)    │ ◄── Apps connect here       │
│  └────────────────────────────────────┘                             │
│                                                                      │
│  ┌────────────────────────────────────┐                             │
│  │  Dedicated Cluster (e.g. Immich)   │                             │
│  │  ├─ immich-database-0 (primary)    │ ◄── immich-database-app     │
│  │  └─ immich-database-1 (replica)    │     (CNPG-generated)        │
│  └────────────────────────────────────┘                             │
│                                                                      │
│  ──── kubernetes-replicator ──────────────────────────────────────   │
│                                                                      │
│  app namespaces (authelia, zipline, immich, ...)                    │
│  ┌─────────────────────────────────────┐                            │
│  │  Replica secrets:                   │                            │
│  │  ├─ <app>-db-credentials            │ (from database/<app>-role- │
│  │  │                                  │  password via replicator)  │
│  │  └─ cnpg-immich-database-app        │ (from database/immich-     │
│  │                                     │  database-app)             │
│  └─────────────────────────────────────┘                            │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Decision Tree: Shared vs Dedicated Cluster

```
App needs a PostgreSQL database?
│
├─ Standard workload (generic SQL, no special extensions)?
│   └─ Use shared platform cluster
│      Connect via platform-pooler-rw service
│      (See: Shared Cluster Workflow below)
│
├─ Needs custom extensions (vector search, PostGIS, etc.)?
│   └─ Use dedicated cluster
│      Custom imageName with extensions pre-installed
│      (See: Dedicated Cluster Workflow below)
│
├─ Needs isolation for performance or data sensitivity?
│   └─ Use dedicated cluster
│      Independent resources, storage, and backup
│
└─ Unclear?
    └─ Start with shared cluster
       Migrate to dedicated if needed later
```

---

## Shared Platform Cluster

The shared cluster is defined at `kubernetes/platform/config/database/` and deployed
to all clusters via the platform Kustomization. It uses **CNPG managed roles** and
**Database CRDs** to declaratively provision databases and users -- no init containers
or superuser access needed in app namespaces.

### Key Files

| File | Purpose |
|------|---------|
| `cluster.yaml` | CNPG Cluster CR with managed roles (`spec.managed.roles`) |
| `databases.yaml` | Database CRDs for each application database |
| `role-secrets.yaml` | Per-role password secrets (secret-generator + replicator) |
| `pooler.yaml` | PgBouncer Pooler for connection pooling |
| `superuser-secret.yaml` | Auto-generated superuser password (stays in database ns only) |
| `prometheus-rules.yaml` | CNPG-specific PrometheusRules for alerting |
| `kustomization.yaml` | Kustomize aggregation of all database resources |

### Cluster Configuration

```yaml
# kubernetes/platform/config/database/cluster.yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: platform
spec:
  description: "Shared platform PostgreSQL cluster"
  imageName: ghcr.io/cloudnative-pg/postgresql:17.2
  instances: ${default_replica_count}
  primaryUpdateStrategy: unsupervised

  enableSuperuserAccess: true
  superuserSecret:
    name: cnpg-platform-superuser

  # Declarative role management - CNPG creates/updates these PostgreSQL roles
  managed:
    roles:
      - name: authelia
        ensure: present
        login: true
        passwordSecret:
          name: authelia-role-password
      # ... one entry per application

  postgresql:
    parameters:
      shared_buffers: "256MB"
      max_connections: "200"
      effective_cache_size: "512MB"
      log_statement: "ddl"
      log_min_duration_statement: "1000"
    pg_hba:
      - host all all 10.0.0.0/8 scram-sha-256
      - host all all 172.16.0.0/12 scram-sha-256

  storage:
    storageClass: fast
    size: ${database_volume_size}

  monitoring:
    enablePodMonitor: true

  affinity:
    enablePodAntiAffinity: true
    topologyKey: kubernetes.io/hostname
```

### Database CRDs

Each database is declared as a separate `Database` CR. CNPG creates it if missing or
adopts it if it already exists (with `databaseReclaimPolicy: retain`):

```yaml
# kubernetes/platform/config/database/databases.yaml
apiVersion: postgresql.cnpg.io/v1
kind: Database
metadata:
  name: authelia-database
  namespace: database
spec:
  name: authelia          # PostgreSQL database name
  owner: authelia         # Must match a managed role name
  cluster:
    name: platform
  databaseReclaimPolicy: retain
```

**Note:** Some apps (sonarr, radarr, prowlarr) use multiple databases (e.g. `sonarr-main`,
`sonarr-log`) but share a single role. Each database gets its own Database CR with the
same `owner`.

### Role Password Secrets

Each managed role has a corresponding Secret in the `database` namespace. The secret
uses `secret-generator` for auto-generation and `kubernetes-replicator` for cross-namespace
replication to the app that needs it:

```yaml
# kubernetes/platform/config/database/role-secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: authelia-role-password
  namespace: database
  annotations:
    secret-generator.v1.mittwald.de/autogenerate: password
    secret-generator.v1.mittwald.de/encoding: hex
    secret-generator.v1.mittwald.de/length: "32"
    replicator.v1.mittwald.de/replication-allowed: "true"
    replicator.v1.mittwald.de/replication-allowed-namespaces: "authelia"
type: kubernetes.io/basic-auth
stringData:
  username: authelia
```

### PgBouncer Pooler

Applications connect through PgBouncer rather than directly to PostgreSQL:

```yaml
# kubernetes/platform/config/database/pooler.yaml
apiVersion: postgresql.cnpg.io/v1
kind: Pooler
metadata:
  name: platform-pooler-rw
spec:
  cluster:
    name: platform
  instances: ${default_replica_count}
  type: rw
  pgbouncer:
    poolMode: transaction
    parameters:
      max_client_conn: "1000"
      default_pool_size: "25"
  monitoring:
    enablePodMonitor: true
```

**Connection string for apps using the shared cluster:**
```
postgresql://<username>:<password>@platform-pooler-rw.database.svc:5432/<dbname>
```

---

## Workflow: Add a Database for a New App (Shared Cluster)

### Step 1: Add Managed Role to Cluster

Add a new role entry to `spec.managed.roles` in
`kubernetes/platform/config/database/cluster.yaml`:

```yaml
managed:
  roles:
    # ... existing roles
    - name: <app>
      ensure: present
      login: true
      passwordSecret:
        name: <app>-role-password
```

### Step 2: Create Role Password Secret

Add a new Secret to `kubernetes/platform/config/database/role-secrets.yaml`:

```yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: <app>-role-password
  namespace: database
  annotations:
    secret-generator.v1.mittwald.de/autogenerate: password
    secret-generator.v1.mittwald.de/encoding: hex
    secret-generator.v1.mittwald.de/length: "32"
    replicator.v1.mittwald.de/replication-allowed: "true"
    replicator.v1.mittwald.de/replication-allowed-namespaces: "<app-namespace>"
type: kubernetes.io/basic-auth
stringData:
  username: <app>
```

### Step 3: Create Database CRD

Add a new Database CR to `kubernetes/platform/config/database/databases.yaml`:

```yaml
---
apiVersion: postgresql.cnpg.io/v1
kind: Database
metadata:
  name: <app>-database
  namespace: database
spec:
  name: <app>
  owner: <app>
  cluster:
    name: platform
  databaseReclaimPolicy: retain
```

### Step 4: Create App-Namespace Credential Replica

Create a replica Secret in the app's config directory that pulls the password from
the database namespace:

```yaml
# kubernetes/clusters/<cluster>/config/<app>/<app>-db-credentials.yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: <app>-db-credentials
  namespace: <app-namespace>
  annotations:
    replicator.v1.mittwald.de/replicate-from: database/<app>-role-password
type: kubernetes.io/basic-auth
data: { }
```

### Step 5: Add Network Policy Access

The app's namespace must have the postgres access label. Add it in `kubernetes/platform/namespaces.yaml`:

```yaml
- name: <app-namespace>
  labels:
    pod-security.kubernetes.io/enforce: baseline
    network-policy.homelab/profile: standard  # or appropriate profile
    access.network-policy.homelab/postgres: "true"  # Required for DB access
```

### Step 6: Configure App to Use Database

The app should connect to the Pooler service, not the Cluster directly:

| Setting | Value |
|---------|-------|
| Host | `platform-pooler-rw.database.svc` |
| Port | `5432` |
| Database | `<app>` (created by CNPG Database CRD) |
| Username | From `<app>-db-credentials` secret (`username` key) |
| Password | From `<app>-db-credentials` secret (`password` key) |

### Step 7: Register in Kustomization

Add the new credential replica file to the app's `kustomization.yaml` and ensure the
parent config references the directory.

---

## Workflow: Create a Dedicated CNPG Cluster

Use this when an app needs custom PostgreSQL extensions or isolation from the shared cluster.

### Step 1: Define the Cluster

```yaml
# kubernetes/clusters/<cluster>/config/<app>/<app>-cluster.yaml
---
# yaml-language-server: $schema=https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/postgresql.cnpg.io/cluster_v1.json
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: <app>-database
  namespace: database
spec:
  inheritedMetadata:
    annotations:
      replicator.v1.mittwald.de/replication-allowed: "true"
      replicator.v1.mittwald.de/replication-allowed-namespaces: "<app-namespace>"
  description: "<App> PostgreSQL with <extension> support"
  imageName: <custom-image>  # e.g., ghcr.io/tensorchord/cloudnative-vectorchord:17.7-1.0.0
  instances: ${default_replica_count}
  primaryUpdateStrategy: unsupervised

  postgresql:
    shared_preload_libraries:
      - "<extension>.so"  # e.g., "vchord.so"
    parameters:
      shared_buffers: "128MB"
      max_connections: "100"

  bootstrap:
    initdb:
      database: <app>
      owner: <app>
      postInitApplicationSQL:
        - CREATE EXTENSION IF NOT EXISTS <extension> CASCADE;

  storage:
    storageClass: fast
    size: 10Gi

  resources:
    requests:
      cpu: 50m
      memory: 256Mi
    limits:
      memory: 1Gi

  monitoring:
    enablePodMonitor: true

  affinity:
    enablePodAntiAffinity: true
    topologyKey: kubernetes.io/hostname
```

**Real example:** `kubernetes/clusters/live/config/immich/immich-cluster.yaml`

### Key Differences from Shared Cluster

| Feature | Shared Cluster | Dedicated Cluster |
|---------|---------------|-------------------|
| Location | `kubernetes/platform/config/database/` | `kubernetes/clusters/<cluster>/config/<app>/` |
| Namespace | `database` (deployed by platform) | `database` (deployed by cluster config) |
| Image | Standard PostgreSQL | Custom image with extensions |
| Role management | `spec.managed.roles` + Database CRDs | `bootstrap.initdb` creates DB and owner |
| Credential source | `<app>-role-password` (secret-generator) | `<app>-database-app` (CNPG auto-generated) |
| `inheritedMetadata` | Not needed (role secrets have explicit replication) | Required for app secret replication |
| Superuser | Confined to `database` namespace | CNPG auto-generates (`<cluster-name>-superuser`) |

### Step 2: Replicate App Credentials to Consumer Namespace

CNPG auto-generates an `<cluster-name>-app` secret in the `database` namespace.
The `inheritedMetadata` annotations allow replication to the app namespace:

```yaml
# kubernetes/clusters/<cluster>/config/<app>/database-secret-replication.yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: cnpg-<app>-database-app
  namespace: <app-namespace>
  annotations:
    replicator.v1.mittwald.de/replicate-from: database/<app>-database-app
data: { }
```

**Real example:** `kubernetes/clusters/live/config/immich/database-secret-replication.yaml`

### Step 3: Network Policy and Kustomization

Same as shared cluster workflow -- add `access.network-policy.homelab/postgres: "true"` label
and register files in `kustomization.yaml`.

---

## Credential Chain Summary

### Shared Cluster Credential Flow

```
database namespace                          app namespace
┌──────────────────────┐                    ┌──────────────────────┐
│ <app>-role-password   │  kubernetes-       │ <app>-db-credentials │
│ (secret-generator)    │──replicator──────► │ (replica)            │
│  username: <app>      │                    │  username: <app>     │
│  password: <random>   │                    │  password: <random>  │
└──────────────────────┘                    └──────────────────────┘
         │
         ▼
  CNPG Cluster (managed role)
  uses passwordSecret to set
  PostgreSQL role password
         │
         ▼
  Database CRD
  creates DB owned by role
```

**Key security property:** The superuser secret (`cnpg-platform-superuser`) never leaves
the `database` namespace. App namespaces only receive their own role password.

### Dedicated Cluster Credential Flow

```
CNPG auto-generates              kubernetes-replicator
     │                                   │
     ▼                                   ▼
<app>-database-app  ──────────► cnpg-<app>-database-app
  (database ns)                   (app ns)
```

The dedicated cluster's `inheritedMetadata` annotations make the auto-generated secret
replicable. The `replication-allowed-namespaces` controls which namespaces can pull it.

---

## Monitoring

### PodMonitor

Both the Cluster and Pooler have `enablePodMonitor: true`, which creates PodMonitor resources
that Prometheus discovers automatically. No additional ServiceMonitor configuration is needed.

### PrometheusRules

CNPG-specific alerts are defined in `kubernetes/platform/config/database/prometheus-rules.yaml`:

| Alert | Expression | Severity | Description |
|-------|-----------|----------|-------------|
| `CNPGClusterNotHealthy` | `cnpg_pg_replication_streaming == 0` | critical | Replication broken |
| `CNPGClusterHighConnections` | Connection usage > 80% of `max_connections` | warning | Near connection limit |
| `CNPGInstanceNotReady` | Replica WAL receiver down | critical | Replica cannot follow primary |

### Key Metrics

| Metric | Description |
|--------|-------------|
| `cnpg_pg_replication_streaming` | Whether streaming replication is active |
| `cnpg_pg_stat_activity_count` | Current active connections |
| `cnpg_pg_settings_setting{name="max_connections"}` | Configured max connections |
| `cnpg_pg_replication_in_recovery` | Whether instance is a replica |
| `cnpg_pg_replication_is_wal_receiver_up` | Whether WAL receiver is connected |

---

## Configuration Reference

### Cluster Spec Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `instances` | Number of PostgreSQL instances (primary + replicas) | `${default_replica_count}` |
| `imageName` | PostgreSQL container image | `ghcr.io/cloudnative-pg/postgresql:17.2` |
| `primaryUpdateStrategy` | How to handle primary upgrades | `unsupervised` (automatic failover) |
| `enableSuperuserAccess` | Whether to allow superuser connections | `true` for shared, not set for dedicated |
| `superuserSecret` | Reference to superuser credentials | `cnpg-platform-superuser` |
| `managed.roles` | Declarative PostgreSQL role definitions | See Managed Roles section |
| `storage.storageClass` | Kubernetes StorageClass for PVCs | `fast` |
| `storage.size` | Volume size per instance | `${database_volume_size}` or `10Gi` |
| `monitoring.enablePodMonitor` | Auto-create PodMonitor for Prometheus | `true` |
| `affinity.enablePodAntiAffinity` | Spread instances across nodes | `true` |
| `postgresql.pg_hba` | Client authentication rules | Allow pod CIDR with SCRAM-SHA-256 |
| `inheritedMetadata` | Annotations/labels applied to generated secrets | Replication annotations |

### Managed Role Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `name` | PostgreSQL role name | `authelia` |
| `ensure` | Whether role should exist | `present` |
| `login` | Whether role can log in | `true` |
| `passwordSecret.name` | Secret containing the role password | `authelia-role-password` |

### Database CRD Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `spec.name` | PostgreSQL database name | `authelia` |
| `spec.owner` | Database owner (must be a managed role) | `authelia` |
| `spec.cluster.name` | Target CNPG Cluster | `platform` |
| `spec.databaseReclaimPolicy` | What happens when CRD is deleted | `retain` (keeps database) |

### Pooler Spec Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `cluster.name` | Target CNPG Cluster | `platform` |
| `instances` | Number of PgBouncer pods | `${default_replica_count}` |
| `type` | Access mode (`rw` or `ro`) | `rw` |
| `pgbouncer.poolMode` | Connection pooling mode | `transaction` |
| `pgbouncer.parameters.max_client_conn` | Max client connections | `"1000"` |
| `pgbouncer.parameters.default_pool_size` | Default server connections per pool | `"25"` |

### Bootstrap initdb Fields (Dedicated Clusters Only)

| Field | Purpose | Example |
|-------|---------|---------|
| `database` | Database name to create | `immich` |
| `owner` | Database owner role | `immich` |
| `postInitApplicationSQL` | SQL to run after database creation | `CREATE EXTENSION IF NOT EXISTS ...` |

---

## Debugging

### Cluster Health

```bash
# Check cluster status
KUBECONFIG=~/.kube/<cluster>.yaml kubectl get clusters.postgresql.cnpg.io -n database

# Detailed cluster info
KUBECONFIG=~/.kube/<cluster>.yaml kubectl describe cluster platform -n database

# Check pod status
KUBECONFIG=~/.kube/<cluster>.yaml kubectl get pods -n database -l cnpg.io/cluster=platform

# Check pooler status
KUBECONFIG=~/.kube/<cluster>.yaml kubectl get poolers.postgresql.cnpg.io -n database

# Check managed databases
KUBECONFIG=~/.kube/<cluster>.yaml kubectl get databases.postgresql.cnpg.io -n database
```

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Pods Pending | No PVs available | Check StorageClass `fast` exists, Longhorn is healthy |
| CrashLoopBackOff | OOM or bad config | Check `kubectl logs`, increase memory limits |
| Replication lag | Slow disk or network | Check `cnpg_pg_replication_streaming` metric |
| App can't connect | Network policy missing | Add `access.network-policy.homelab/postgres: "true"` label |
| App can't connect | Secret not replicated | Check replication annotations on source secret |
| Secret empty after replication | Source namespace wrong | Verify `replicate-from` points to correct `<ns>/<name>` |
| Extension not found | Wrong image | Verify `imageName` includes the extension |
| Database not created | Database CRD missing | Add Database CR to `databases.yaml` |
| Role not created | Missing from managed.roles | Add role entry to `cluster.yaml` |
| Role password mismatch | Secret not regenerated | Delete the role-password secret, secret-generator will recreate |

### Checking Connectivity

```bash
# Verify network policy allows traffic
hubble observe --from-namespace <app-ns> --to-namespace database --since 5m

# Test connection from a debug pod
KUBECONFIG=~/.kube/<cluster>.yaml kubectl run -n <app-ns> pg-test --rm -it \
  --image=postgres:17 -- psql "postgresql://user:pass@platform-pooler-rw.database.svc:5432/dbname"
```

### CNPG Plugin (Optional)

The `kubectl cnpg` plugin provides additional cluster management commands:

```bash
kubectl cnpg status platform -n database
kubectl cnpg promote platform-2 -n database  # Manual failover
```

---

## Cross-References

| Document | Relevance |
|----------|-----------|
| [kubernetes/platform/config/CLAUDE.md](../../../kubernetes/platform/config/CLAUDE.md) | Config subsystem and CRD dependency patterns |
| [secrets skill](../secrets/SKILL.md) | secret-generator, ExternalSecret, and replication patterns |
| [deploy-app skill](../deploy-app/SKILL.md) | End-to-end deployment including database setup |
| [sre skill](../sre/SKILL.md) | Debugging methodology for database incidents |
