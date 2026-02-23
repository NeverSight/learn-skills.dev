---
name: protobuf-developer
description: Protobuf schema development guidelines. This skill should be used when writing, reviewing, or refactoring Protocol Buffer definitions to ensure consistency, backwards compatibility, and adherence to style guides.
---

# Protobuf Developer

This skill provides best practices and rules for developing Protocol Buffer schemas (proto3).

## When to Apply

Reference these guidelines when:

- Defining new gRPC services and message types.
- Modifying existing `.proto` files.
- Refactoring message structures.
- Ensuring backwards compatibility for evolving APIs.
- Configuring Protobuf management, linting, and code generation using Buf.

## Google AIP References

The following references are based on [Google API Improvement Proposals (AIPs)](https://google.aip.dev/). Use these when designing resource-oriented APIs.

**Important**: When implementing these patterns, you **must** modify the protobuf package name and resource type domains to match the current application context (e.g., use `package imrenagi.com.v1;` instead of `package google.example.v1;`).

### Resource Design

| Reference                                                                                                   | When to Use                                                                                |
| :---------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------- |
| [AIP-121: Resource-Oriented Design](references/google-aip/aip121-resource-oriented-design.md)               | Designing a new API or service; need to structure resources and collections consistently.  |
| [AIP-122: Resource Names](references/google-aip/aip122-resource-names.md)                                   | Defining the `name` field for resources; need the correct URI path format for identifiers. |
| [AIP-123: Resource Types](references/google-aip/aip123-resource-types.md)                                   | Annotating messages with `google.api.resource`; need to define resource type patterns.     |
| [AIP-124: Resource Association](references/google-aip/aip124-resource-association.md)                       | Referencing resources from other messages; using `google.api.resource_reference`.          |
| [AIP-126: Enumerations](references/google-aip/aip126-enumerations.md)                                       | Defining enum types; need `_UNSPECIFIED` zero-value and naming conventions.                |
| [AIP-127: HTTP/gRPC Transcoding](references/google-aip/aip127-http-grpc-transcoding.md)                     | Adding `google.api.http` annotations; need to map gRPC methods to REST endpoints.          |
| [AIP-128: Declarative-Friendly Interfaces](references/google-aip/aip128-declarative-friendly-interfaces.md) | Building APIs consumed by infrastructure-as-code tools like Terraform.                     |
| [AIP-129: Server-Modified Values](references/google-aip/aip129-server-modified-values.md)                   | Handling fields computed or modified by the server (e.g., `create_time`, `update_time`).   |

### Standard Methods

| Reference                                                                 | When to Use                                                            |
| :------------------------------------------------------------------------ | :--------------------------------------------------------------------- |
| [AIP-130: Methods](references/google-aip/aip130-methods.md)               | Understanding the general structure and naming of RPC methods.         |
| [AIP-131: Get Methods](references/google-aip/aip131-get-methods.md)       | Implementing a method to retrieve a single resource by name.           |
| [AIP-132: List Methods](references/google-aip/aip132-list-methods.md)     | Implementing a method to list resources with pagination.               |
| [AIP-133: Create Methods](references/google-aip/aip133-create-methods.md) | Implementing a method to create a new resource.                        |
| [AIP-134: Update Methods](references/google-aip/aip134-update-methods.md) | Implementing a method to update an existing resource with field masks. |
| [AIP-135: Delete Methods](references/google-aip/aip135-delete-methods.md) | Implementing a method to delete a resource.                            |
| [AIP-136: Custom Methods](references/google-aip/aip136-custom-methods.md) | Implementing non-CRUD actions (e.g., `:cancel`, `:move`, `:archive`).  |

### Field Conventions

| Reference                                                                         | When to Use                                                                |
| :-------------------------------------------------------------------------------- | :------------------------------------------------------------------------- |
| [AIP-140: Field Names](references/google-aip/aip140-field-names.md)               | Naming fields; need snake_case conventions and standard suffixes.          |
| [AIP-141: Quantities](references/google-aip/aip141-quantities.md)                 | Defining numeric fields for counts, sizes, or quantities.                  |
| [AIP-142: Time and Duration](references/google-aip/aip142-time-and-duration.md)   | Using `google.protobuf.Timestamp` and `google.protobuf.Duration`.          |
| [AIP-143: Standardized Codes](references/google-aip/aip143-standardized-codes.md) | Defining status codes, language codes, or other standardized values.       |
| [AIP-144: Repeated Fields](references/google-aip/aip144-repeated-fields.md)       | Using repeated fields for lists; understanding pluralization and ordering. |
| [AIP-145: Ranges](references/google-aip/aip145-ranges.md)                         | Defining start/end or min/max field pairs for ranges.                      |
| [AIP-146: Generic Fields](references/google-aip/aip146-generic-fields.md)         | Using `google.protobuf.Any` or `google.protobuf.Struct` for dynamic data.  |
| [AIP-147: Sensitive Fields](references/google-aip/aip147-sensitive-fields.md)     | Marking fields containing PII or secrets.                                  |
| [AIP-148: Standard Fields](references/google-aip/aip148-standard-fields.md)       | Using common fields like `name`, `display_name`, `title`, `description`.   |
| [AIP-149: Unset Field Values](references/google-aip/aip149-unset-field-values.md) | Distinguishing between unset and default values with optional fields.      |
| [AIP-203: Field Behavior](references/google-aip/aip203-field-behavior.md)         | Annotating fields with `REQUIRED`, `OUTPUT_ONLY`, `IMMUTABLE`, etc.        |

### Operations & Patterns

| Reference                                                                                         | When to Use                                                          |
| :------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------- |
| [AIP-151: Long-Running Operations](references/google-aip/aip151-long-running-operations.md)       | Operations taking > 2 seconds; using `google.longrunning.Operation`. |
| [AIP-152: Jobs](references/google-aip/aip152-jobs.md)                                             | Modeling user-managed background tasks or recurring operations.      |
| [AIP-153: Import/Export](references/google-aip/aip153-import-export.md)                           | Implementing bulk data import or export operations.                  |
| [AIP-154: ETags](references/google-aip/aip154-etags.md)                                           | Adding optimistic concurrency control with ETags.                    |
| [AIP-155: Request IDs](references/google-aip/aip155-request-id.md)                                | Supporting client-provided request IDs for idempotency.              |
| [AIP-156: Singleton Resources](references/google-aip/aip156-singleton-resources.md)               | Modeling resources with only one instance (e.g., settings, config).  |
| [AIP-157: Partial Responses](references/google-aip/aip157-partial-responses.md)                   | Allowing clients to request specific fields with read masks.         |
| [AIP-158: Pagination](references/google-aip/aip158-pagination.md)                                 | Implementing `page_size` and `page_token` for list methods.          |
| [AIP-159: Reading Across Collections](references/google-aip/aip159-reading-across-collections.md) | Listing resources across multiple parents (using `-` wildcard).      |
| [AIP-160: Filtering](references/google-aip/aip160-filtering.md)                                   | Adding filter expressions to list methods.                           |
| [AIP-161: Field Masks](references/google-aip/aip161-field-masks.md)                               | Using `google.protobuf.FieldMask` for partial updates.               |
| [AIP-162: Resource Revisions](references/google-aip/aip162-resource-revisions.md)                 | Tracking historical versions or revisions of resources.              |
| [AIP-163: Change Validation](references/google-aip/aip163-change-validation.md)                   | Validating changes before applying (dry-run mode).                   |
| [AIP-164: Soft Delete](references/google-aip/aip164-soft-delete.md)                               | Implementing soft-delete with `Undelete` and retention periods.      |
| [AIP-165: Purge](references/google-aip/aip165-purge.md)                                           | Implementing bulk deletion of soft-deleted resources.                |

### Batch Operations

| Reference                                                                 | When to Use                                                   |
| :------------------------------------------------------------------------ | :------------------------------------------------------------ |
| [AIP-231: Batch Get](references/google-aip/aip231-batch-get.md)           | Retrieving multiple resources by name in a single request.    |
| [AIP-233: Batch Create](references/google-aip/aip233-batch-create.md)     | Creating multiple resources in a single request.              |
| [AIP-234: Batch Update](references/google-aip/aip234-batch-update.md)     | Updating multiple resources in a single request.              |
| [AIP-235: Batch Delete](references/google-aip/aip235-batch-delete.md)     | Deleting multiple resources in a single request.              |
| [AIP-236: Policy Preview](references/google-aip/aip236-policy-preview.md) | Previewing the effect of policy changes before applying them. |

### Compatibility & Versioning

| Reference                                                                                   | When to Use                                                             |
| :------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------- |
| [AIP-180: Backwards Compatibility](references/google-aip/aip180-backwards-compatibility.md) | Understanding what constitutes a breaking change; evolving APIs safely. |
| [AIP-181: Stability Levels](references/google-aip/aip181-stability-levels.md)               | Marking APIs as alpha, beta, or stable.                                 |
| [AIP-182: External Dependencies](references/google-aip/aip182-external-dependencies.md)     | Managing dependencies on external proto definitions.                    |
| [AIP-185: Versioning](references/google-aip/aip185-versioning.md)                           | Structuring package names with version suffixes (v1, v2).               |

### Style & Documentation

| Reference                                                                               | When to Use                                                    |
| :-------------------------------------------------------------------------------------- | :------------------------------------------------------------- |
| [AIP-190: Naming Conventions](references/google-aip/aip190-naming-conventions.md)       | Naming messages, enums, fields, and services consistently.     |
| [AIP-191: File Structure](references/google-aip/aip191-file-structure.md)               | Organizing proto files within a package.                       |
| [AIP-192: Documentation](references/google-aip/aip192-documentation.md)                 | Writing comments and documentation in proto files.             |
| [AIP-193: Errors](references/google-aip/aip193-errors.md)                               | Returning structured errors with `google.rpc.Status`.          |
| [AIP-194: Retry](references/google-aip/aip194-retry.md)                                 | Documenting retry behavior and idempotency.                    |
| [AIP-200: Precedent](references/google-aip/aip200-precedent.md)                         | Understanding when to follow existing patterns vs. innovation. |
| [AIP-202: Field Formats](references/google-aip/aip202-field-formats.md)                 | Using format annotations for UUIDs, emails, URIs, etc.         |
| [AIP-205: Beta Blocking Changes](references/google-aip/aip205-beta-blocking-changes.md) | Managing breaking changes in beta APIs.                        |
| [AIP-210: Unicode](references/google-aip/aip210-unicode.md)                             | Handling Unicode strings and normalization.                    |
| [AIP-211: Authorization](references/google-aip/aip211-authorization.md)                 | Documenting authorization requirements.                        |
| [AIP-213: Common Components](references/google-aip/aip213-common-components.md)         | Using shared proto definitions across services.                |
| [AIP-214: Expiration](references/google-aip/aip214-expiration.md)                       | Modeling time-to-live or expiration for resources.             |
| [AIP-215: Isolation](references/google-aip/aip215-isolation.md)                         | Designing multi-tenant or isolated resource APIs.              |
| [AIP-216: States](references/google-aip/aip216-states.md)                               | Modeling resource lifecycle states.                            |
| [AIP-217: Unreachable Resources](references/google-aip/aip217-unreachable-resources.md) | Handling references to resources that may not exist.           |

## Buf References

Use these references when configuring Buf for linting, breaking change detection, and code generation.

| Reference                                                       | When to Use                                                                       |
| :-------------------------------------------------------------- | :-------------------------------------------------------------------------------- |
| [Protobuf Management with Buf](references/buf/buf.md)           | Setting up Buf for a new project; understanding `buf.yaml` and core commands.     |
| [Linting](references/buf/linting.md)                            | Configuring lint rules; resolving conflicts between Buf linter and AIP standards. |
| [Breaking Change Detection](references/buf/breaking-changes.md) | Running `buf breaking` to prevent backwards-incompatible changes.                 |
| [Directory Structure](references/buf/directory-structure.md)    | Organizing proto files and packages for Buf modules.                              |
| [Code Generation](references/buf/generation.md)                 | Configuring `buf.gen.yaml` for Go, gRPC-Gateway, and OpenAPI code generation.     |

## How to Use

1. **Read the Rules**: Before starting a new feature or refactor, browse the relevant rule files.
2. **Follow the Examples**: Use the provided "Correct" code patterns as templates.
3. **Ensure Consistency**: Apply the same patterns across all proto files.

Each rule file contains:

- Brief explanation of the rule
- "Incorrect" examples (Bad patterns)
- "Correct" examples (Recommended patterns)
- Additional context and references
