---
name: jooq-patterns
description: JOOQ type-safe SQL patterns - use for database queries, repositories, complex SQL operations, and PostgreSQL-specific features
---

# JOOQ Database Patterns

## Repository Structure

```kotlin
@Repository
class EnvironmentRepository(
    private val dsl: DSLContext
) {

    fun findById(id: UUID): Environment? =
        dsl.selectFrom(ENVIRONMENT)
            .where(ENVIRONMENT.ID.eq(id))
            .fetchOne()
            ?.toEntity()

    fun findByName(name: String): Environment? =
        dsl.selectFrom(ENVIRONMENT)
            .where(ENVIRONMENT.NAME.eq(name))
            .fetchOne()
            ?.toEntity()

    fun findAll(): List<Environment> =
        dsl.selectFrom(ENVIRONMENT)
            .orderBy(ENVIRONMENT.CREATED_AT.desc())
            .fetch()
            .map { it.toEntity() }

    fun save(entity: Environment): Environment =
        dsl.insertInto(ENVIRONMENT)
            .set(ENVIRONMENT.ID, entity.id)
            .set(ENVIRONMENT.NAME, entity.name)
            .set(ENVIRONMENT.STATUS, entity.status.name)
            .set(ENVIRONMENT.CREATED_AT, entity.createdAt)
            .returning()
            .fetchOne()!!
            .toEntity()

    fun update(entity: Environment): Environment =
        dsl.update(ENVIRONMENT)
            .set(ENVIRONMENT.STATUS, entity.status.name)
            .set(ENVIRONMENT.UPDATED_AT, Instant.now())
            .where(ENVIRONMENT.ID.eq(entity.id))
            .returning()
            .fetchOne()!!
            .toEntity()

    fun delete(id: UUID): Boolean =
        dsl.deleteFrom(ENVIRONMENT)
            .where(ENVIRONMENT.ID.eq(id))
            .execute() > 0
}
```

## Record to Entity Mapping

```kotlin
// Extension function on generated Record
private fun EnvironmentRecord.toEntity() = Environment(
    id = id,
    name = name,
    status = EnvironmentStatus.valueOf(status),
    createdAt = createdAt,
    updatedAt = updatedAt
)

// For complex mappings with joins
private fun Record.toEnvironmentWithTags() = Environment(
    id = get(ENVIRONMENT.ID),
    name = get(ENVIRONMENT.NAME),
    status = EnvironmentStatus.valueOf(get(ENVIRONMENT.STATUS)),
    createdAt = get(ENVIRONMENT.CREATED_AT),
    updatedAt = get(ENVIRONMENT.UPDATED_AT),
    tags = get("tags", List::class.java) as List<String>
)
```

## Complex Queries

### Joins

```kotlin
fun findWithOwner(id: UUID): EnvironmentWithOwner? =
    dsl.select(
        ENVIRONMENT.asterisk(),
        USER.NAME.`as`("owner_name"),
        USER.EMAIL.`as`("owner_email")
    )
    .from(ENVIRONMENT)
    .join(USER).on(ENVIRONMENT.OWNER_ID.eq(USER.ID))
    .where(ENVIRONMENT.ID.eq(id))
    .fetchOne()
    ?.let { record ->
        EnvironmentWithOwner(
            environment = record.into(ENVIRONMENT).toEntity(),
            ownerName = record.get("owner_name", String::class.java),
            ownerEmail = record.get("owner_email", String::class.java)
        )
    }
```

### Filtering and Pagination

```kotlin
fun findByFilters(
    status: EnvironmentStatus?,
    search: String?,
    page: Int,
    size: Int
): Page<Environment> {
    val conditions = mutableListOf<Condition>()

    status?.let { conditions.add(ENVIRONMENT.STATUS.eq(it.name)) }
    search?.let { conditions.add(ENVIRONMENT.NAME.likeIgnoreCase("%$it%")) }

    val baseQuery = dsl.selectFrom(ENVIRONMENT)
        .where(conditions)

    val total = dsl.selectCount()
        .from(ENVIRONMENT)
        .where(conditions)
        .fetchOne(0, Long::class.java) ?: 0L

    val items = baseQuery
        .orderBy(ENVIRONMENT.CREATED_AT.desc())
        .limit(size)
        .offset(page * size)
        .fetch()
        .map { it.toEntity() }

    return Page(items, total, page, size)
}
```

### Aggregations

```kotlin
fun countByStatus(): Map<EnvironmentStatus, Long> =
    dsl.select(ENVIRONMENT.STATUS, DSL.count())
        .from(ENVIRONMENT)
        .groupBy(ENVIRONMENT.STATUS)
        .fetch()
        .associate { record ->
            EnvironmentStatus.valueOf(record.value1()) to record.value2().toLong()
        }
```

## Batch Operations

```kotlin
fun saveAll(entities: List<Environment>): List<Environment> {
    if (entities.isEmpty()) return emptyList()

    val records = entities.map { entity ->
        dsl.newRecord(ENVIRONMENT).apply {
            id = entity.id
            name = entity.name
            status = entity.status.name
            createdAt = entity.createdAt
        }
    }

    dsl.batchInsert(records).execute()

    return entities
}

fun updateStatuses(ids: List<UUID>, status: EnvironmentStatus): Int =
    dsl.update(ENVIRONMENT)
        .set(ENVIRONMENT.STATUS, status.name)
        .set(ENVIRONMENT.UPDATED_AT, Instant.now())
        .where(ENVIRONMENT.ID.`in`(ids))
        .execute()
```

## JSON Fields (PostgreSQL)

```kotlin
// For JSONB columns
fun findByMetadata(key: String, value: String): List<Environment> =
    dsl.selectFrom(ENVIRONMENT)
        .where(
            DSL.field("metadata->>'{0}'", String::class.java, key)
                .eq(value)
        )
        .fetch()
        .map { it.toEntity() }

// Store JSON
fun updateMetadata(id: UUID, metadata: Map<String, Any>): Environment =
    dsl.update(ENVIRONMENT)
        .set(ENVIRONMENT.METADATA, JSONB.jsonb(objectMapper.writeValueAsString(metadata)))
        .where(ENVIRONMENT.ID.eq(id))
        .returning()
        .fetchOne()!!
        .toEntity()
```

## Upsert (ON CONFLICT)

```kotlin
fun upsert(entity: Environment): Environment =
    dsl.insertInto(ENVIRONMENT)
        .set(ENVIRONMENT.ID, entity.id)
        .set(ENVIRONMENT.NAME, entity.name)
        .set(ENVIRONMENT.STATUS, entity.status.name)
        .set(ENVIRONMENT.CREATED_AT, entity.createdAt)
        .onConflict(ENVIRONMENT.NAME)
        .doUpdate()
        .set(ENVIRONMENT.STATUS, entity.status.name)
        .set(ENVIRONMENT.UPDATED_AT, Instant.now())
        .returning()
        .fetchOne()!!
        .toEntity()
```

## Transaction Handling

```kotlin
// In service layer - explicit transaction control
@Service
class EnvironmentService(
    private val dsl: DSLContext,
    private val repository: EnvironmentRepository
) {

    fun createWithResources(request: CreateRequest): Environment =
        dsl.transactionResult { config ->
            val txDsl = DSL.using(config)

            // Create environment
            val env = repository.save(request.toEnvironment())

            // Create related resources in same transaction
            request.resources.forEach { resource ->
                txDsl.insertInto(RESOURCE)
                    .set(RESOURCE.ENVIRONMENT_ID, env.id)
                    .set(RESOURCE.TYPE, resource.type)
                    .execute()
            }

            env
        }
}
```

## Custom SQL Functions

```kotlin
// Using PostgreSQL functions
fun findNearExpiry(days: Int): List<Environment> =
    dsl.selectFrom(ENVIRONMENT)
        .where(
            ENVIRONMENT.EXPIRES_AT.lessOrEqual(
                DSL.currentTimestamp().plus(DSL.interval(days, DatePart.DAY))
            )
        )
        .fetch()
        .map { it.toEntity() }

// Array operations
fun findByTags(tags: List<String>): List<Environment> =
    dsl.selectFrom(ENVIRONMENT)
        .where(
            DSL.field("tags").cast(SQLDataType.VARCHAR.array())
                .contains(tags.toTypedArray())
        )
        .fetch()
        .map { it.toEntity() }
```
