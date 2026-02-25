---
name: generate-dto
description: '[Implementation] Generate entity DTO from an existing entity'
---

Generate DTO for entity: $ARGUMENTS

## Instructions

1. **Parse arguments**:
    - Entity name (required): e.g., `Employee`, `TextSnippetText`
    - Options: `--with-mapping` (include MapToEntity), `--minimal` (core props only)

2. **Find the entity**:
    - Search in `*.Domain/Entities/` folders
    - Read the entity class to understand its properties

3. **Generate DTO following platform patterns**:

    Location: `*.Application/EntityDtos/<EntityName>Dto.cs`

    Template:

    ```csharp
    public class {Entity}Dto : PlatformEntityDto<{Entity}, string>
    {
        // Empty constructor required
        public {Entity}Dto() { }

        // Constructor maps from entity
        public {Entity}Dto({Entity} entity) : base(entity)
        {
            // Map core properties
        }

        // CORE PROPERTIES
        public string? Id { get; set; }
        // ... other properties from entity

        // OPTIONAL LOAD PROPERTIES (for With* methods)
        public RelatedDto? Related { get; set; }

        // WITH* FLUENT METHODS
        public {Entity}Dto WithRelated(RelatedEntity related)
        {
            Related = new RelatedDto(related);
            return this;
        }

        // PLATFORM OVERRIDES
        protected override object? GetSubmittedId() => Id;
        protected override string GenerateNewId() => Ulid.NewUlid().ToString();
        protected override {Entity} MapToEntity({Entity} entity, MapToEntityModes mode)
        {
            // Map DTO properties back to entity
            return entity;
        }
    }
    ```

4. **Read the template file** for complete pattern:
    - `.github/prompts/create-entity-dto.prompt.md`

5. **After generation**:
    - Show the generated DTO
    - Ask if any properties should be excluded or modified
    - Offer to create the file

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
