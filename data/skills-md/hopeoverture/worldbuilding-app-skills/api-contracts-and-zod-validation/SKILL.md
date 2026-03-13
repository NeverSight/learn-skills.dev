---
name: api-contracts-and-zod-validation
description: Generate Zod schemas and TypeScript types for forms, API routes, and Server Actions with runtime validation. Use this skill when creating API contracts, validating request/response payloads, generating form schemas, adding input validation to Server Actions or route handlers, or ensuring type safety across client-server boundaries. Trigger terms include zod, schema, validation, API contract, form validation, type inference, runtime validation, parse, safeParse, input validation, request validation, Server Action validation.
---

# API Contracts and Zod Validation

Generate Zod schemas with TypeScript type inference for forms, API routes, and Server Actions. Validate inputs in Server Actions or route handlers with runtime type checking.

## Core Capabilities

### 1. Generate Zod Schemas from TypeScript Types

When creating API contracts or form validations:

- Analyze existing TypeScript interfaces or types
- Generate equivalent Zod schemas with proper validation rules
- Ensure bidirectional type compatibility (Zod -> TypeScript)
- Use `z.infer<typeof schema>` for automatic type inference

### 2. Form Validation Schemas

To create form validation with Zod:

- Generate schemas for React Hook Form, Formik, or native forms
- Include field-level validation rules (min/max length, regex, custom validators)
- Support nested objects, arrays, and complex data structures
- Provide helpful error messages for validation failures
- Use `references/zod_patterns.md` for common validation patterns

### 3. API Route and Server Action Validation

To add validation to API endpoints or Server Actions:

- Wrap handler logic with schema validation using `.parse()` or `.safeParse()`
- Return typed errors for validation failures
- Generate request/response schemas for API contracts
- Validate query parameters, body payloads, and route parameters
- Ensure type safety between client and server code

### 4. Schema Generation Script

Use `scripts/generate_zod_schema.py` to automate schema generation:

```bash
python scripts/generate_zod_schema.py --input types/entities.ts --output schemas/entities.ts
```

The script:
- Parses TypeScript interfaces/types
- Generates Zod schemas with appropriate validators
- Preserves JSDoc comments as descriptions
- Handles common patterns (optional fields, unions, enums)

## Resource Files

### scripts/generate_zod_schema.py
Automated TypeScript-to-Zod schema generator. Parses TypeScript AST and generates equivalent Zod schemas.

### references/zod_patterns.md
Common Zod validation patterns including:
- String validation (email, URL, UUID, custom regex)
- Number constraints (min, max, positive, integer)
- Date validation and transformation
- Array and tuple validation
- Object shape validation
- Union and discriminated unions
- Optional and nullable fields
- Custom refinements and transforms
- Error message customization

### assets/schema_templates/
Pre-built Zod schema templates:
- `form_schema_template.ts` - Basic form validation
- `api_route_schema_template.ts` - API route request/response
- `server_action_schema_template.ts` - Server Action input/output
- `entity_schema_template.ts` - Database entity validation

## Usage Workflow

### For New API Routes

1. Define request/response TypeScript types
2. Generate Zod schemas using `scripts/generate_zod_schema.py` or templates
3. Add validation middleware to route handler
4. Return typed validation errors on failure

### For Server Actions

1. Define input parameters as TypeScript types
2. Create Zod schema for validation
3. Use `.safeParse()` at the beginning of the action
4. Return validation errors in action result
5. Handle errors on the client side

### For Forms

1. Define form fields as TypeScript interface
2. Generate Zod schema with field validators
3. Integrate with form library (React Hook Form recommended)
4. Display validation errors inline

## Best Practices

- Always use `.safeParse()` instead of `.parse()` to avoid throwing exceptions
- Provide clear, user-friendly error messages
- Validate early (at API boundary or Server Action entry)
- Keep schemas colocated with routes/actions for maintainability
- Use `z.infer<typeof schema>` for automatic TypeScript types
- Document validation rules in schema comments
- Test edge cases (empty values, invalid formats, boundary conditions)

## Integration with Worldbuilding App

Common use cases for worldbuilding applications:

- **Entity creation forms**: Validate character, location, faction data
- **Relationship APIs**: Ensure valid entity IDs and relationship types
- **Timeline events**: Validate dates, ordering, and event data
- **Search/filter endpoints**: Validate query parameters and filters
- **Bulk operations**: Validate arrays of entities or updates
- **Import/export**: Validate file formats and data structure

Consult `references/zod_patterns.md` for specific validation patterns applicable to worldbuilding entities.
