---
name: meishe-shortvideo-service-reimplementation
description: Reimplement one or more APIs, the full Meishe shortvideo service, or an existing compatible implementation from this language-neutral canonical specification. Use when an agent must reproduce or upgrade the service in Go, Python, Node.js, Rust, Java, or another language while preserving HTTP contracts, validation, business rules, errors, database and storage behavior, security, ordering, transactions, caching, background ingestion, and observable compatibility.
---

# Reimplement the Meishe Shortvideo Service

Use the bundled canonical specification as the source of truth for observable behavior. Do not translate the Spring Boot class structure mechanically and do not require access to the original Java project.

## Select a mode

- **Single API**: Resolve only the requested endpoint and its dependency closure.
- **Full Project**: Resolve every endpoint plus shared runtime and background-ingestion components.
- **Upgrade**: Compare the existing specification or target implementation with the new manifest, then change only the affected closure.

If the request is ambiguous, prefer Single API only when the user names specific methods and paths. Otherwise state the selected mode before implementation.

## Read specifications progressively

1. Read [references/architecture.md](references/architecture.md) and [references/conventions.md](references/conventions.md).
2. Find the endpoint in `references/api/index.yaml` or run:

   ```bash
   python scripts/find-api.py GET /materialcenter/listFont
   ```

3. Resolve the dependency closure:

   ```bash
   python scripts/resolve-dependencies.py material-center.list-font
   ```

4. Read only the returned API, model, behavior, infrastructure, and contract-test files.
5. Read `references/repository-analysis.md` only for full-project planning or source maintenance.
6. Read `references/unresolved.md` before claiming compatibility.

When shell execution is unavailable, follow the `dependencies` references in the endpoint file and `references/component-index.yaml` manually.

## Implement a Single API

1. Treat the endpoint specification as the HTTP and business contract.
2. Implement every item in its dependency closure and no unrelated endpoint.
3. Preserve missing, null, empty, conversion, default, and boundary behavior explicitly.
4. Preserve response field names, null emission, business error envelopes, HTTP statuses, ordering guarantees, and documented legacy quirks.
5. Treat every response model `source`, `forbiddenSources`, and `currentlyUnset` marker as authoritative. Do not select a persistence column merely because its name, extension, or content appears similar; serialize currently unset fields as documented.
6. For `material-center.list-all-assembly-material`, copy `behavior.infoJsonProjection.requiredPseudocode` and its decision table exactly. Never return `info_relative_path`, a URL, or raw JSON text in `infoJson`; type 19 returns `infoUrl` and leaves `infoJson` null, while only the documented 16/17/18/20/21 branches load a parsed object.
7. Implement the target language and framework idiomatically. Do not mirror Controller/Service/Mapper layers unless they fit the target.
8. Create focused tests from the endpoint's `contractTests` references.
9. Validate the implementation against a prepared fixture profile or both the Java oracle and target service.
10. Report passed, failed, skipped, and unresolved compatibility checks separately.

## Implement the Full Project

1. Read all entries in `references/api/index.yaml` and resolve all closures.
2. Read `references/infrastructure/runtime.yaml` and `references/behaviors/background-ingestion.yaml`; HTTP routes alone are not the whole service.
3. Design modules around target-language conventions while retaining the canonical component boundaries.
4. Implement MySQL schema compatibility, authentication, file authorization, storage providers, startup behavior, file monitoring, external HTTP downloads, media probing, and cache/concurrency rules.
5. Implement `runtime.yaml#startupSeedContract` completely: copy or embed every manifest-listed seed asset and invoke the insert-if-absent loader during enabled startup. Creating empty tables or merely leaving JSON files in the generated repository is incomplete. Verify the exact fresh-database row counts and restart idempotency defined by that contract.
6. For every watched input, follow its exact handler contract in `background-ingestion.yaml`; never infer ZIP member roles from extensions when metadata selects them. For material ZIPs, copy the control flow in `materialZipContract.metadataReadPhases.requiredPseudocode` and verify every row of its decision table: never choose primary metadata by type, keep root `extra.json` primary whenever it exists, and read root `info.json` as a second limited overlay only after the effective type becomes 19. Then implement `materialZipContract.derivedValues` exactly, including integer defaults, aspect-ratio bitmasks, shot-count precedence, and translation matching.
7. Apply `infrastructure:storage#filenamePolicy.mobileCompatibility` to every upload: every uploaded object's final filename must contain no ASCII space (`U+0020`). Treat the object persisted in `material_public.package_relative_path` only as an exception to filename rewriting, never as an exception to the no-space invariant: preserve its selected source basename exactly, expect `{uuid}[.{version}].{extension}`, and reject ingestion when that original basename contains a space. URL percent-encoding alone does not satisfy this storage-key invariant.
8. Preserve documented absence of atomicity. Do not silently add cross-side-effect transactions if doing so changes visible failure behavior.
9. Run specification validation, implementation tests, contract tests, and a full compatibility report.

## Upgrade incrementally

1. Keep the old skill directory and target implementation unchanged as the baseline.
2. Generate an impact plan from the source repository when it is available:

   ```bash
   python scripts/plan-refresh.py --skill . --source-repo /path/to/source
   ```

3. Compare old and new skills:

   ```bash
   python scripts/diff-spec.py /path/to/old-skill /path/to/new-skill
   ```

4. Reanalyze only changed source symbols and the reverse dependency closure.
5. Treat automatic classifications as evidence, not proof. Resolve `REVIEW_REQUIRED` items before release.
6. Update affected document versions, hashes, contract cases, manifest entries, and `CHANGELOG.md`.
7. Re-run contract tests for affected APIs plus shared behavior consumers.

If the old Git commit is unavailable, use the source hashes in `manifest.yaml`. Never regenerate all specifications merely because one source file changed.

## Validate

Install the portable script dependency when needed:

```bash
python -m pip install -r scripts/requirements.txt
```

Run:

```bash
python scripts/validate-spec.py
python scripts/check-manifest.py
python -m unittest discover -s tests/unit -p 'test_*.py'
python scripts/contract-test.py --help
```

For differential validation:

```bash
python scripts/contract-test.py \
  --suite tests/contract/pilot.yaml \
  --oracle-base-url http://java-service:8080 \
  --target-base-url http://target-service:8080
```

Prepare `tests/fixtures` first and select the matching suite profile. Never run contract fixtures against production data. Authentication-enabled profiles require the same test-only secret on both services and the runner's `--secret` option.

## Handle uncertainty

- Preserve `unresolved` rather than inventing behavior.
- Distinguish source-derived rules from runtime-observed rules.
- Do not turn comments or legacy documentation into stronger evidence than executable code and tests.
- Ask for runtime evidence when an unresolved item materially affects the requested implementation.
- Do not claim full compatibility when relevant checks were skipped.

## Compatibility priority

Prioritize HTTP, request and response semantics, business rules, validation, errors, database side effects, transactions, security, serialization, external interactions, cache/idempotency/concurrency, and only then internal structure.
