---
name: nestjs
description: NestJS 11 backend patterns with Fastify, modular architecture, guards, pipes, and Railway deployment. This skill should be used when building NestJS APIs, setting up backend services, or creating REST/GraphQL endpoints with NestJS.
---

# NestJS Skill

Production patterns for NestJS 11 backend services using Fastify adapter, modular architecture, and Railway deployment.

## When to Use This Skill

- Setting up a new NestJS backend project
- Creating REST API modules (controllers, services, DTOs)
- Configuring guards, pipes, interceptors, and filters
- Integrating Prisma with NestJS (PrismaModule/PrismaService)
- Deploying NestJS to Railway

## Project Bootstrap

```bash
npm i -g @nestjs/cli
nest new project-name --package-manager npm --strict
cd project-name
npm install @nestjs/platform-fastify @nestjs/config @nestjs/swagger
npm install zod
npm uninstall @nestjs/platform-express @types/express
```

## Project Structure

```
src/
  main.ts                     # Bootstrap with Fastify, PORT binding
  app.module.ts               # Root module
  app.controller.ts           # Root health check
  prisma/
    prisma.module.ts          # Global Prisma module
    prisma.service.ts         # Prisma client lifecycle
  auth/
    auth.module.ts
    auth.controller.ts
    auth.service.ts
    auth.guard.ts
    dto/
  users/
    users.module.ts
    users.controller.ts
    users.service.ts
    dto/
      create-user.dto.ts
      update-user.dto.ts
  common/
    guards/
      jwt-auth.guard.ts
    pipes/
      zod-validation.pipe.ts
    interceptors/
      transform.interceptor.ts
    filters/
      http-exception.filter.ts
    decorators/
      current-user.decorator.ts
```

## Bootstrap (main.ts)

```typescript
import { NestFactory } from '@nestjs/core';
import { FastifyAdapter, NestFastifyApplication } from '@nestjs/platform-fastify';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create<NestFastifyApplication>(
    AppModule,
    new FastifyAdapter(),
  );

  app.enableCors({
    origin: process.env.FRONTEND_URL || 'http://localhost:3000',
    credentials: true,
  });

  const config = new DocumentBuilder()
    .setTitle('API')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('docs', app, document);

  const port = process.env.PORT || 4000;
  await app.listen(port, '0.0.0.0');
  console.log(`Server running on port ${port}`);
}
bootstrap();
```

## Module Pattern

### Root Module

```typescript
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { PrismaModule } from './prisma/prisma.module';
import { AuthModule } from './auth/auth.module';
import { UsersModule } from './users/users.module';
import { HealthController } from './health/health.controller';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    PrismaModule,
    AuthModule,
    UsersModule,
  ],
  controllers: [HealthController],
})
export class AppModule {}
```

### Feature Module

```typescript
import { Module } from '@nestjs/common';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';

@Module({
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService],
})
export class UsersModule {}
```

## Prisma Integration

### PrismaService

```typescript
import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit, OnModuleDestroy {
  async onModuleInit() {
    await this.$connect();
  }

  async onModuleDestroy() {
    await this.$disconnect();
  }
}
```

### PrismaModule

```typescript
import { Global, Module } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Global()
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
```

### Using in Services

```typescript
import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class UsersService {
  constructor(private prisma: PrismaService) {}

  async findAll() {
    return this.prisma.user.findMany();
  }

  async findOne(id: string) {
    const user = await this.prisma.user.findUnique({ where: { id } });
    if (!user) throw new NotFoundException(`User ${id} not found`);
    return user;
  }

  async create(data: { email: string; name: string }) {
    return this.prisma.user.create({ data });
  }

  async update(id: string, data: { name?: string }) {
    await this.findOne(id);
    return this.prisma.user.update({ where: { id }, data });
  }

  async remove(id: string) {
    await this.findOne(id);
    return this.prisma.user.delete({ where: { id } });
  }
}
```

## Controller Pattern

```typescript
import { Controller, Get, Post, Put, Delete, Param, Body } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { UsersService } from './users.service';
import { CreateUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';

@ApiTags('users')
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get()
  @ApiOperation({ summary: 'List all users' })
  findAll() {
    return this.usersService.findAll();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get user by ID' })
  findOne(@Param('id') id: string) {
    return this.usersService.findOne(id);
  }

  @Post()
  @ApiOperation({ summary: 'Create user' })
  create(@Body() dto: CreateUserDto) {
    return this.usersService.create(dto);
  }

  @Put(':id')
  @ApiOperation({ summary: 'Update user' })
  update(@Param('id') id: string, @Body() dto: UpdateUserDto) {
    return this.usersService.update(id, dto);
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Delete user' })
  remove(@Param('id') id: string) {
    return this.usersService.remove(id);
  }
}
```

## DTO Validation with Zod

```typescript
import { z } from 'zod';
import { PipeTransform, BadRequestException } from '@nestjs/common';

// Schema
export const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(255),
});

export type CreateUserDto = z.infer<typeof createUserSchema>;

// Zod Validation Pipe
export class ZodValidationPipe implements PipeTransform {
  constructor(private schema: z.ZodSchema) {}

  transform(value: unknown) {
    const result = this.schema.safeParse(value);
    if (!result.success) {
      throw new BadRequestException(result.error.flatten());
    }
    return result.data;
  }
}

// Usage in controller
@Post()
create(@Body(new ZodValidationPipe(createUserSchema)) dto: CreateUserDto) {
  return this.usersService.create(dto);
}
```

## Health Check

```typescript
import { Controller, Get } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('health')
@Controller('health')
export class HealthController {
  @Get()
  @ApiOperation({ summary: 'Health check' })
  check() {
    return { status: 'ok', timestamp: new Date().toISOString() };
  }
}
```

## Guards

```typescript
import { Injectable, CanActivate, ExecutionContext, UnauthorizedException } from '@nestjs/common';

@Injectable()
export class JwtAuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const token = request.headers.authorization?.replace('Bearer ', '');

    if (!token) {
      throw new UnauthorizedException('No token provided');
    }

    // Verify token logic here
    return true;
  }
}

// Apply to controller or route
@UseGuards(JwtAuthGuard)
@Get('profile')
getProfile(@Req() req) {
  return req.user;
}
```

## Global Exception Filter

```typescript
import { ExceptionFilter, Catch, ArgumentsHost, HttpException, HttpStatus } from '@nestjs/common';
import { FastifyReply } from 'fastify';

@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<FastifyReply>();

    const status = exception instanceof HttpException
      ? exception.getStatus()
      : HttpStatus.INTERNAL_SERVER_ERROR;

    const message = exception instanceof HttpException
      ? exception.getResponse()
      : 'Internal server error';

    response.status(status).send({
      statusCode: status,
      message: typeof message === 'string' ? message : (message as any).message,
      timestamp: new Date().toISOString(),
    });
  }
}
```

## Environment Configuration

```typescript
// .env
DATABASE_URL=postgres://postgres:postgres@localhost:5432/myapp
FRONTEND_URL=http://localhost:3000
JWT_SECRET=your-secret-here
PORT=4000

// Accessing in services
import { ConfigService } from '@nestjs/config';

@Injectable()
export class AuthService {
  constructor(private config: ConfigService) {}

  getJwtSecret() {
    return this.config.getOrThrow<string>('JWT_SECRET');
  }
}
```

## Railway Deployment

### railway.toml

```toml
[build]
builder = "nixpacks"
buildCommand = "npx prisma generate && npx prisma migrate deploy && npm run build"

[deploy]
startCommand = "node dist/main.js"
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

### Required Environment Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `DATABASE_URL` | Railway Postgres | Auto-wired from Postgres service |
| `PORT` | Railway | Auto-provided by Railway |
| `FRONTEND_URL` | Manual | Frontend domain for CORS |
| `JWT_SECRET` | Manual | Auth token signing key |

### Port Binding

NestJS must listen on `0.0.0.0:$PORT` for Railway:

```typescript
await app.listen(process.env.PORT || 4000, '0.0.0.0');
```

## Package Scripts

```json
{
  "scripts": {
    "build": "nest build",
    "start": "nest start",
    "start:dev": "nest start --watch",
    "start:prod": "node dist/main.js",
    "lint": "eslint \"{src,apps,libs,test}/**/*.ts\" --fix",
    "test": "jest",
    "db:generate": "prisma generate",
    "db:migrate": "prisma migrate dev",
    "db:migrate:deploy": "prisma migrate deploy",
    "db:studio": "prisma studio",
    "db:seed": "tsx prisma/seed.ts"
  }
}
```
