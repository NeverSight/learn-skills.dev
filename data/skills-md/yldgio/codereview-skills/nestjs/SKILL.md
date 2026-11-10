---
name: nestjs
description: NestJS module architecture, dependency injection, guards, interceptors, and DTO validation
metadata:
  version: "1.1.0"
---

## NestJS Code Review Rules

### Security (Critical)
- **Template Safety**: Review all template variables (e.g., `{{...}}`) and ensure user input embedded in templates is escaped and not trusted. Never render undeclared template variables. If using template syntax (e.g., `{{variable}}`), validate and escape all variables before rendering to prevent injection
- **Comment Hygiene**: Never use HTML comments (`<!-- -->`) for sensitive data or instructions. Ensure HTML comments are stripped from source before deployment
- Validate all DTOs with `ValidationPipe`
- Use `@Exclude()` to hide sensitive fields in responses
- Implement rate limiting with `@nestjs/throttler`
- Sanitize user input before database queries to prevent injection attacks
- Never log sensitive data (passwords, tokens, API keys)
- Use parameterized queries or ORM methods to prevent SQL injection

### Module Architecture (Essential)
- One module per feature/domain
- Modules should export only what other modules need
- Use `forRoot`/`forRootAsync` for configurable modules
- Avoid circular dependencies between modules

### Controllers (Essential)
- Keep controllers thin (delegate to services)
- Use DTOs for request validation, not raw objects
- Apply guards at controller or handler level as appropriate
- Use proper HTTP status codes with `@HttpCode()`
- Follow RESTful conventions for resource naming

### Controllers (Advanced)
- Use consistent routing structure (e.g., `/api/v1/resources`)
- Implement API versioning when needed
- Use descriptive route paths and parameter names

### Services (Essential)
- Services contain business logic
- Use constructor injection for dependencies
- Services should be stateless (no instance variables for request data)
- Use `@Injectable()` with appropriate scope (default singleton is usually correct)
- Use `async`/`await` for asynchronous operations
- Avoid unhandled promise rejections - always handle errors
- Propagate errors appropriately (don't swallow exceptions)
- Return meaningful error messages from service layer

### DTOs and Validation
- Use `class-validator` decorators on DTO properties
- Apply `ValidationPipe` globally or per-route
- Use `class-transformer` for type transformation
- Create separate DTOs for create/update operations

### Guards and Interceptors
- Guards for authentication/authorization
- Interceptors for logging, transformation, caching
- Use `@UseGuards()` and `@UseInterceptors()` decorators
- Order matters: guards run before interceptors

### Error Handling
- Use built-in exceptions (`NotFoundException`, `BadRequestException`, etc.)
- Create exception filters for custom error formatting
- Don't catch and ignore errors silently

### Configuration (Essential)
- Use `@nestjs/config` for configuration management
- Validate environment variables on startup
- Use `ConfigModule.forRoot()` in app module
- Access config via `ConfigService` dependency injection
- Don't hardcode configuration values in code

### Testing
- Write unit tests using `@nestjs/testing`
- Mock dependencies with `createMock` or manual mocks
- Test controllers, services, and guards separately
- Use `Test.createTestingModule()` for integration tests
- Write e2e tests for critical flows
- Separate test code from implementation code

### File Organization
- Follow consistent file naming (e.g., `user.controller.ts`, `user.service.ts`)
- Group related files in feature folders
- Keep modules, controllers, services, DTOs in separate files
- Use consistent folder structure across features
- Place shared/common code in dedicated folders

### API Documentation (Advanced)
- Use `@nestjs/swagger` for automatic API documentation
- Apply `@Api*` decorators to controllers and DTOs
- Document all endpoints with `@ApiOperation()`
- Define response types with `@ApiResponse()`
- Include examples in `@ApiProperty()` decorators
- Keep Swagger docs up to date with code changes
