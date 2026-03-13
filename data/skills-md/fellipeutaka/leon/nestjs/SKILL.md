---
name: nestjs
description: |
  NestJS best practices for building production-ready REST APIs, GraphQL APIs, and microservices with TypeScript.
  Use when writing, reviewing, or refactoring NestJS code: controllers, modules, providers,
  dependency injection, guards, interceptors, pipes, exception filters, middlewares, custom
  decorators, DTOs, validation, authentication, authorization, JWT, configuration, testing,
  database (TypeORM/Prisma), caching, queues (BullMQ), OpenAPI/Swagger, WebSockets,
  GraphQL (resolvers, mutations, subscriptions, ObjectType, InputType, ArgsType, code-first,
  schema-first, PubSub), Helmet, CORS, CSRF, lifecycle hooks, graceful shutdown, and
  feature module architecture. Also use when
  working with @nestjs/jwt, @nestjs/throttler, @nestjs/terminus, @nestjs/config,
  @nestjs/swagger, @nestjs/typeorm, @nestjs/mongoose, @nestjs/graphql, @nestjs/apollo,
  @apollo/server, bullmq, class-validator, graphql, or graphql-ws.
---

# NestJS

**Version**: @nestjs/core@latest | Node >= 20 | TypeScript required

## Quick Setup

```bash
npm i -g @nestjs/cli
nest new my-app
```

Production-ready `main.ts`:

```typescript
import { NestFactory, Reflector } from '@nestjs/core';
import { ClassSerializerInterceptor, ValidationPipe, VersioningType } from '@nestjs/common';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
    transform: true,
    transformOptions: { enableImplicitConversion: true },
  }));
  app.useGlobalInterceptors(new ClassSerializerInterceptor(app.get(Reflector)));
  app.enableVersioning({ type: VersioningType.URI });
  app.enableShutdownHooks();

  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
```

## Application Structure

Organize by feature, not by technical layer:

```
src/
├── users/
│   ├── dto/
│   │   ├── create-user.dto.ts
│   │   └── update-user.dto.ts
│   ├── entities/user.entity.ts
│   ├── users.controller.ts
│   ├── users.service.ts
│   └── users.module.ts
├── shared/
│   ├── guards/
│   ├── interceptors/
│   ├── filters/
│   └── shared.module.ts
└── app.module.ts
```

| `@Module()` property | Purpose |
|---|---|
| `providers` | Services, repositories — instantiated by DI container |
| `controllers` | Route handlers |
| `imports` | Other modules whose exports are needed here |
| `exports` | Subset of providers made available to importing modules |

## Building Blocks

| Concept | Decorator | Purpose |
|---|---|---|
| Controller | `@Controller()` | Route handlers, HTTP methods |
| Provider/Service | `@Injectable()` | Business logic, DI token |
| Module | `@Module()` | Feature encapsulation |
| Guard | `@UseGuards()` | Auth/authz — returns boolean |
| Interceptor | `@UseInterceptors()` | Transform req/res, logging, caching |
| Pipe | `@UsePipes()` | Validate/transform input |
| Exception Filter | `@UseFilters()` | Centralized error handling |
| Middleware | `configure(consumer)` | Cross-cutting before guards |
| Decorator | `createParamDecorator()` | Param extraction, metadata |

## Rule Categories

| Priority | Category | Rule File | Impact |
|---|---|---|---|
| CRITICAL | Architecture & Modules | `rules/arch-modules.md` | Feature org, circular deps, module sharing |
| CRITICAL | Dependency Injection | `rules/arch-di.md` | Constructor injection, tokens, scopes |
| HIGH | HTTP Layer | `rules/http-layer.md` | Controllers, DTOs, guards, interceptors, pipes |
| HIGH | Error Handling | `rules/error-handling.md` | Exception filters, HTTP exceptions, async errors |
| HIGH | Security | `rules/security.md` | JWT, validation, guards, rate limiting |
| MEDIUM-HIGH | Testing | `rules/testing.md` | TestingModule, E2E, mocking |
| MEDIUM-HIGH | Database | `rules/database.md` | Repository pattern, N+1, transactions, migrations |
| MEDIUM | Performance | `rules/performance.md` | Caching, lazy loading, async hooks |
| MEDIUM | Config & Lifecycle | `rules/config-lifecycle.md` | ConfigModule, logging, graceful shutdown |
| MEDIUM | Advanced | `rules/advanced.md` | Microservices, queues, API versioning, OpenAPI |
| MEDIUM | GraphQL | `rules/graphql.md` | Setup, resolvers, mutations, subscriptions, guards |

## Critical Rules

### Always Do

- Enable `ValidationPipe` globally with `whitelist: true`, `forbidNonWhitelisted: true`, `transform: true`
- Use constructor injection — never property injection (except `@Optional()` dependencies)
- Organize by feature modules, not technical layers (`controllers/`, `services/` dirs are anti-patterns)
- Throw `HttpException` subclasses (`NotFoundException`, `ConflictException`, etc.) from services
- Use `@nestjs/config` with Joi/Zod validation schema — never access `process.env` directly
- Use `APP_GUARD`, `APP_INTERCEPTOR`, `APP_FILTER`, `APP_PIPE` tokens when global providers need DI
- Enable `app.enableShutdownHooks()` and implement `OnApplicationShutdown`
- Export providers from a dedicated module and import that module elsewhere — never provide the same service in multiple modules

### Never Do

- Create circular module dependencies — extract to a `SharedModule` or use events instead
- Use `@Res()` without `passthrough: true` if NestJS should still handle the response
- Use `forwardRef()` as a first solution — it hides architectural problems
- Define providers in multiple modules — creates separate instances with inconsistent state
- Catch exceptions in controllers and return manual JSON — use exception filters
- Use mutable singleton state for per-request data — use `Scope.REQUEST` or `nestjs-cls`

## Key Patterns

### Feature Module + Controller + Service

```typescript
// users.module.ts
@Module({
  imports: [TypeOrmModule.forFeature([User])],
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService],
})
export class UsersModule {}

// users.controller.ts
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get(':id')
  findOne(@Param('id', ParseUUIDPipe) id: string): Promise<User> {
    return this.usersService.findById(id);
  }

  @Post()
  @HttpCode(HttpStatus.CREATED)
  create(@Body() dto: CreateUserDto): Promise<User> {
    return this.usersService.create(dto);
  }
}

// users.service.ts
@Injectable()
export class UsersService {
  constructor(@InjectRepository(User) private readonly repo: Repository<User>) {}

  async findById(id: string): Promise<User> {
    const user = await this.repo.findOne({ where: { id } });
    if (!user) throw new NotFoundException(`User #${id} not found`);
    return user;
  }

  create(dto: CreateUserDto): Promise<User> {
    return this.repo.save(this.repo.create(dto));
  }
}
```

### DTO + Validation

```typescript
import { IsEmail, IsString, MinLength, MaxLength, Transform } from 'class-validator';

export class CreateUserDto {
  @IsString()
  @MinLength(2)
  @MaxLength(100)
  @Transform(({ value }) => value?.trim())
  name: string;

  @IsEmail()
  @Transform(({ value }) => value?.toLowerCase().trim())
  email: string;

  @IsString()
  @MinLength(8)
  password: string;
}
```

### Guard + Roles

```typescript
// decorators
export const Public = () => SetMetadata('isPublic', true);
export const Roles = (...roles: Role[]) => SetMetadata('roles', roles);

// guards registered globally via APP_GUARD
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const roles = this.reflector.getAllAndOverride<Role[]>('roles', [
      context.getHandler(), context.getClass(),
    ]);
    if (!roles) return true;
    const { user } = context.switchToHttp().getRequest();
    return roles.some(role => user.roles?.includes(role));
  }
}

// usage
@Controller('admin')
@Roles(Role.Admin)
export class AdminController {
  @Public()
  @Get('health')
  health() { return { status: 'ok' }; }
}
```

### Global Exception Filter

```typescript
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  private readonly logger = new Logger('HTTP');

  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    const status = exception instanceof HttpException
      ? exception.getStatus()
      : HttpStatus.INTERNAL_SERVER_ERROR;

    this.logger.error(`${request.method} ${request.url}`,
      exception instanceof Error ? exception.stack : String(exception));

    response.status(status).json({
      statusCode: status,
      message: exception instanceof HttpException ? exception.message : 'Internal server error',
      timestamp: new Date().toISOString(),
      path: request.url,
    });
  }
}
```

### ConfigModule Bootstrap

```typescript
// app.module.ts
@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      validationSchema: Joi.object({
        NODE_ENV: Joi.string().valid('development', 'production', 'test').required(),
        PORT: Joi.number().default(3000),
        DATABASE_URL: Joi.string().required(),
        JWT_SECRET: Joi.string().min(32).required(),
      }),
    }),
  ],
})
export class AppModule {}

// usage in service
@Injectable()
export class AppService {
  constructor(private config: ConfigService) {}

  getDatabaseUrl(): string {
    return this.config.getOrThrow<string>('DATABASE_URL');
  }
}
```

## CLI Generators

```bash
nest g resource users     # Full CRUD resource (module + controller + service + DTOs)
nest g module auth        # Module only
nest g controller users   # Controller only
nest g service users      # Service only
nest g guard jwt-auth     # Guard
nest g interceptor logging # Interceptor
nest g filter all-exceptions # Exception filter
nest g pipe parse-date    # Pipe
nest g decorator roles    # Decorator
nest g middleware logger  # Middleware
```
