---
name: patroni
description: Alta disponibilidad de PostgreSQL con failover automático para el datastore KYC
type: Tool
priority: Esencial
mode: Self-hosted
---

# patroni

Patroni proporciona alta disponibilidad para PostgreSQL mediante failover automático, replicación streaming y prevención de split-brain, asegurando que el datastore del pipeline de verificación de identidad permanezca operativo incluso ante fallos de nodos. Utiliza un sistema de consenso distribuido (etcd, Consul o ZooKeeper) para elegir el líder y orquestar las promociones de réplicas de forma segura.

## When to use

Usa esta skill cuando necesites configurar un cluster PostgreSQL de alta disponibilidad para el sistema KYC, con failover automático y replicación. Pertenece al **database_agent** y se aplica en entornos de producción donde la disponibilidad del 99.9% es un requisito del pipeline de verificación.

## Instructions

1. Definir la arquitectura del cluster Patroni para el pipeline KYC:
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  PostgreSQL  │     │  PostgreSQL  │     │  PostgreSQL  │
│   Primary    │────▶│  Replica 1   │────▶│  Replica 2   │
│  (Leader)    │     │ (Sync Standby)│    │(Async Standby)│
└─────────────┘     └─────────────┘     └─────────────┘
       │                    │                    │
       └────────────────────┴────────────────────┘
                            │
                    ┌───────────────┐
                    │     etcd      │
                    │   (Consensus) │
                    └───────────────┘
```

2. Crear el archivo de configuración `patroni.yml`:
```yaml
scope: verifid-kyc-cluster
name: pg-node-1

restapi:
  listen: 0.0.0.0:8008
  connect_address: pg-node-1:8008

etcd3:
  hosts: etcd1:2379,etcd2:2379,etcd3:2379

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576  # 1MB
    synchronous_mode: true
    postgresql:
      use_pg_rewind: true
      use_slots: true
      parameters:
        max_connections: 200
        shared_buffers: '2GB'
        wal_level: 'replica'
        max_wal_senders: 5
        max_replication_slots: 5
        hot_standby: 'on'
        synchronous_commit: 'on'

  initdb:
    - encoding: UTF8
    - data-checksums

  pg_hba:
    - host replication replicator 10.0.0.0/8 scram-sha-256
    - host verifid_kyc verifid_app 10.0.0.0/8 scram-sha-256

  users:
    verifid_admin:
      password: 'admin_password'
      options:
        - createrole
        - createdb
    replicator:
      password: 'repl_password'
      options:
        - replication

postgresql:
  listen: 0.0.0.0:5432
  connect_address: pg-node-1:5432
  data_dir: /var/lib/postgresql/data
  authentication:
    replication:
      username: replicator
      password: 'repl_password'
    superuser:
      username: verifid_admin
      password: 'admin_password'
```

3. Desplegar el cluster con Docker Compose para desarrollo/staging:
```yaml
services:
  etcd:
    image: quay.io/coreos/etcd:v3.5
    command:
      - etcd
      - --name=etcd0
      - --initial-advertise-peer-urls=http://etcd:2380
      - --listen-peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://etcd:2379
      - --listen-client-urls=http://0.0.0.0:2379

  pg-node-1:
    image: patroni-pg16:latest
    environment:
      PATRONI_SCOPE: verifid-kyc-cluster
      PATRONI_NAME: pg-node-1
      PATRONI_ETCD3_HOSTS: etcd:2379
    volumes:
      - pg1-data:/var/lib/postgresql/data

  pg-node-2:
    image: patroni-pg16:latest
    environment:
      PATRONI_SCOPE: verifid-kyc-cluster
      PATRONI_NAME: pg-node-2
      PATRONI_ETCD3_HOSTS: etcd:2379
    volumes:
      - pg2-data:/var/lib/postgresql/data
```

4. Configurar HAProxy para balancear las conexiones del pipeline:
```conf
global
    maxconn 1000

defaults
    mode tcp
    timeout connect 5s
    timeout client 30s
    timeout server 30s

listen postgresql-primary
    bind *:5000
    option httpchk GET /primary
    http-check expect status 200
    default-server inter 3s fall 3 rise 2
    server pg-node-1 pg-node-1:5432 check port 8008
    server pg-node-2 pg-node-2:5432 check port 8008

listen postgresql-replicas
    bind *:5001
    balance roundrobin
    option httpchk GET /replica
    http-check expect status 200
    default-server inter 3s fall 3 rise 2
    server pg-node-1 pg-node-1:5432 check port 8008
    server pg-node-2 pg-node-2:5432 check port 8008
```

5. Verificar el estado del cluster y las operaciones de failover:
```bash
# Estado del cluster
patronictl -c /etc/patroni/patroni.yml list

# Failover manual (en caso necesario)
patronictl -c /etc/patroni/patroni.yml failover

# Reiniciar un nodo
patronictl -c /etc/patroni/patroni.yml restart verifid-kyc-cluster pg-node-1
```

6. Configurar alertas para eventos de failover:
```yaml
# Patroni callback scripts
postgresql:
  callbacks:
    on_start: /scripts/notify.sh started
    on_stop: /scripts/notify.sh stopped
    on_role_change: /scripts/notify.sh role_changed
```

## Notes

- Habilitar `synchronous_mode: true` para garantizar que al menos una réplica tenga los datos más recientes antes de confirmar escrituras; esto es crítico para no perder resultados de verificación durante un failover.
- El `maximum_lag_on_failover` debe configurarse según el volumen de escrituras del pipeline; un valor de 1MB es razonable para el throughput típico del sistema KYC.
- Desplegar al menos 3 nodos etcd para tolerancia a fallos en el consenso distribuido; con 2 nodos no se puede tolerar la pérdida de ninguno.
