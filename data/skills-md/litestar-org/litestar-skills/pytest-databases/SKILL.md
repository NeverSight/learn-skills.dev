---
name: pytest-databases
description: "Auto-activate for pytest_databases, Docker DB fixtures, PostgreSQL/pgvector/ParadeDB, MySQL/MariaDB, Oracle/SQL Server, CockroachDB/YugabyteDB, MongoDB, Redis/Valkey, Elasticsearch, BigQuery/Spanner, Azurite, MinIO, or RustFS tests. Not for mocked databases."
---

# pytest-databases

`pytest-databases` provides session-scoped, container-backed service fixtures.
This guidance targets the immutable `v0.19.0` tag. Load only the plugin modules
the test suite uses. Consume a ready client fixture where one exists; otherwise
connect with the client already used by the project.

## Code Style Rules

- Keep database I/O consistent with the project driver. The package's
  PostgreSQL connection fixtures use synchronous `psycopg`; do not `await`
  their methods.
- Type service fixtures with the service class from the same plugin module.
- Prefer ready client fixtures when provided. For service-only plugins, build
  the project's existing client from the service object's host, port, and
  credentials.
- Keep plugin declarations in the nearest `conftest.py`; do not load every
  backend globally.

## Quick Reference

### Install and enable

```bash
pip install "pytest-databases[postgres]"
```

```python
# conftest.py
pytest_plugins = ["pytest_databases.docker.postgres"]
```

The core `pytest_databases` pytest entry point supplies `docker_client` and
`docker_service`. Each database module supplies its own fixtures.

### Choose the fixture shape

| Need | Use |
| --- | --- |
| A ready `psycopg` connection | `postgres_connection`, a versioned PostgreSQL-family connection, or `cockroachdb_connection` |
| A ready vendor client | `bigquery_client`, `spanner_connection`, `mongodb_connection`, an Oracle connection, a GizmoSQL connection, or an Azure Blob container client |
| Service coordinates for the project's own client | The backend's `*_service` fixture |
| A specific PostgreSQL-family release | Matching `*_NN_service`, `*_NN_connection`, and `*_NN_port` fixtures |
| Parallel worker isolation | The backend's exact `*_xdist_isolation_level` fixture from [xdist.md](references/xdist.md) |

See [reference.md](references/reference.md) for the exact plugin, service, and
ready-client matrix. Do not infer a `*_connection` fixture from a
`*_service` fixture's name.

<workflow>

## Workflow

1. Install the extra matching the selected backend. Backends with no bundled
   Python client, such as MySQL, MariaDB, SQL Server, and YugabyteDB, expose
   service fixtures and expect the project to supply its own driver.
2. Add only the required `pytest_databases.docker.<module>` entries to
   `pytest_plugins`.
3. Prefer a ready client fixture listed in
   [reference.md](references/reference.md). Otherwise construct the project's
   existing client from the typed service fixture.
4. Override session-scoped configuration fixtures in `conftest.py`. Use
   environment variables only where 0.19.0 explicitly reads them; see
   [config.md](references/config.md).
5. For `pytest-xdist`, keep the default `"database"` isolation when the service
   supports logical namespaces. Override the backend's exact isolation fixture
   to `"server"` when each worker needs its own container.
6. Run the focused integration tests against a Docker-compatible daemon.

</workflow>

<guardrails>

## Guardrails

- **Connection fixtures vs service fixtures**: Ready-client fixtures
  (`*_connection`, `*_client`) exist for PostgreSQL-family, CockroachDB,
  Oracle, GizmoSQL, BigQuery, Spanner, MongoDB, and Azure Blob. Service-only
  backends (MySQL, MariaDB, SQL Server, YugabyteDB, Dolt, Redis, Dragonfly,
  KeyDB, Valkey, Elasticsearch, MinIO, and RustFS) export service fixtures but
  no ready client. Build the project's client from the service object's
  coordinates; convenience `*_host`/`*_port` fixtures are backend-specific.
- **Use `azure_blob_*` names.** The module is
  `pytest_databases.docker.azure_blob`, the service is `AzureBlobService`, and
  the ready clients are `azure_blob_container_client` and
  `azure_blob_async_container_client`.
- **Keep synchronous fixtures synchronous.** `postgres_connection` is a
  `psycopg.Connection`; call `execute()` directly.
- **Do not assume every backend uses the same xdist fixture name.** Azure Blob
  uses `azure_blob_xdist_isolation_level`; most others use
  `xdist_<backend>_isolation_level`.
- **Do not hand-roll container teardown.** The package owns labelled container
  lifecycle through `docker_service`.
- **Do not pin a host port without a reason.** Dynamic ports avoid conflicts.
  Use the 0.19.0 `*_port` fixture or matching PostgreSQL-family environment
  variable only when a rootless/container-network constraint requires it.

</guardrails>

<validation>

## Validation Checkpoint

- [ ] Installed version is `pytest-databases>=0.19.0`.
- [ ] `pytest_plugins` names an existing module from
      [reference.md](references/reference.md).
- [ ] Every requested fixture exists in that module's 0.19.0 fixture row.
- [ ] Service-only backends use the project's own client rather than a
      fabricated `*_connection` fixture.
- [ ] PostgreSQL connection examples use synchronous `psycopg` calls.
- [ ] Configuration uses an actual fixture or environment variable from
      [config.md](references/config.md).
- [ ] Xdist overrides use the backend's exact isolation-fixture name.
- [ ] Container-backed tests run against a Docker-compatible daemon.

</validation>

<example>

## Example: synchronous PostgreSQL connection

```python
import psycopg

pytest_plugins = ["pytest_databases.docker.postgres"]


def test_postgres_is_ready(
    postgres_connection: psycopg.Connection,
) -> None:
    row = postgres_connection.execute("SELECT 1").fetchone()

    assert row == (1,)
```

`postgres_connection` is a synchronous `psycopg.Connection`. Use an async
driver only by constructing it separately from `postgres_service`.

</example>

---

## References Index

- [Supported database patterns](references/databases.md) — ready-client and
  service-only examples.
- [Complete fixture matrix](references/reference.md) — exact 0.19.0 modules,
  classes, service fixtures, and client/provider fixtures.
- [Xdist parallel testing](references/xdist.md) — supported isolation fixture
  names and helper functions.
- [Configuration](references/config.md) — fixture overrides and environment
  variables implemented by 0.19.0.
- [Troubleshooting](references/troubleshooting.md) — runtime, plugin, client,
  and port failures.

- [Litestar testing](../litestar-testing/SKILL.md) — integrate container-backed
  services with Litestar test clients and dependency overrides.

## Official References

- <https://pypi.org/project/pytest-databases/0.19.0/>
- <https://github.com/litestar-org/pytest-databases/tree/v0.19.0>
- <https://github.com/litestar-org/pytest-databases/tree/v0.19.0/src/pytest_databases/docker>
- <https://github.com/litestar-org/pytest-databases/tree/v0.19.0/tests>

## Shared Styleguide Baseline

- [General Principles](../litestar-styleguide/references/general.md)
- [Testing](../litestar-styleguide/references/testing.md)
- [Python](../litestar-styleguide/references/python.md)
