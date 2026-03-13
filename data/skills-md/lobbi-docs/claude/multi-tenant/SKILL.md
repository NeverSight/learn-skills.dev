# Multi-Tenant Architecture

Multi-tenant architecture skill for Lobbi member management system. Activates when working with tenant isolation, organization context, or row-level security patterns.

**Triggers:** multi-tenant, tenant, org_id, organization, isolation, tenant-aware, row-level-security, rls, organization_id

**Use this skill when:**
- Implementing tenant-scoped database queries
- Adding organization context to API endpoints
- Enforcing tenant isolation in repositories
- Working with tenant middleware or context propagation
- Designing multi-tenant data models

## Allowed Tools

- prisma (ORM and migrations)
- postgresql (database operations)
- express (middleware and routing)
- typescript (type safety)
- jest (testing tenant isolation)

## Instructions

### Core Principles

1. **Tenant Context Propagation**
   - Every request must carry tenant context (org_id)
   - Middleware extracts org_id from JWT or headers
   - Context flows through service → repository layers
   - Never allow cross-tenant data leakage

2. **Database Isolation Patterns**
   - Use row-level filtering with org_id in WHERE clauses
   - Prisma models must include organizationId field
   - Composite unique constraints: [organizationId, businessKey]
   - Never expose global IDs without tenant checks

3. **Tenant-Aware Repository Pattern**
   - All repository methods accept TenantContext
   - Automatic org_id filtering in base repository
   - Explicit tenant validation in create/update operations
   - Audit logging includes tenant information

### Architecture Layers

```
Request → AuthMiddleware → TenantMiddleware → Controller → Service → Repository → Database
           (extract JWT)    (set context)      (validate)   (logic)   (filter)    (RLS)
```

### Implementation Checklist

- [ ] Add organizationId to all tenant-scoped Prisma models
- [ ] Implement tenant context middleware
- [ ] Create BaseTenantRepository with auto-filtering
- [ ] Add tenant validation to all CRUD operations
- [ ] Implement tenant-aware error handling
- [ ] Add tenant isolation tests
- [ ] Document tenant security boundaries

## Code Examples

### 1. Prisma Schema Pattern

```prisma
// backend/prisma/schema.prisma

model Member {
  id             String   @id @default(cuid())
  organizationId String   @map("organization_id")
  email          String
  firstName      String   @map("first_name")
  lastName       String   @map("last_name")
  status         MemberStatus @default(ACTIVE)
  createdAt      DateTime @default(now()) @map("created_at")
  updatedAt      DateTime @updatedAt @map("updated_at")

  organization   Organization @relation(fields: [organizationId], references: [id])
  memberships    Membership[]

  // Composite unique constraint: email unique per tenant
  @@unique([organizationId, email])
  @@index([organizationId, status])
  @@index([organizationId, email])
  @@map("members")
}

model Membership {
  id             String   @id @default(cuid())
  organizationId String   @map("organization_id")
  memberId       String   @map("member_id")
  tierId         String   @map("tier_id")
  status         MembershipStatus @default(PENDING)
  startDate      DateTime @map("start_date")
  endDate        DateTime? @map("end_date")
  createdAt      DateTime @default(now()) @map("created_at")
  updatedAt      DateTime @updatedAt @map("updated_at")

  organization   Organization @relation(fields: [organizationId], references: [id])
  member         Member @relation(fields: [memberId], references: [id])
  tier           MembershipTier @relation(fields: [tierId], references: [id])

  @@unique([organizationId, memberId, tierId])
  @@index([organizationId, status])
  @@map("memberships")
}
```

### 2. Tenant Context Types

```typescript
// backend/src/types/tenant.types.ts

export interface TenantContext {
  organizationId: string;
  userId?: string;
  permissions?: string[];
}

export interface TenantRequest extends Request {
  tenant: TenantContext;
}

export class TenantError extends Error {
  constructor(message: string, public organizationId?: string) {
    super(message);
    this.name = 'TenantError';
  }
}
```

### 3. Tenant Context Middleware

```typescript
// backend/src/middleware/tenant.middleware.ts

import { Request, Response, NextFunction } from 'express';
import { TenantRequest, TenantContext } from '../types/tenant.types';
import { UnauthorizedException } from '../exceptions';

export const tenantMiddleware = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const tenantReq = req as TenantRequest;

  // Extract org_id from JWT claims (set by auth middleware)
  const organizationId = tenantReq.user?.organizationId;

  if (!organizationId) {
    throw new UnauthorizedException('Organization context required');
  }

  // Set tenant context
  tenantReq.tenant = {
    organizationId,
    userId: tenantReq.user?.id,
    permissions: tenantReq.user?.permissions || []
  };

  next();
};

// Optional: Override org_id from header (admin/support use only)
export const tenantOverrideMiddleware = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const tenantReq = req as TenantRequest;
  const overrideOrgId = req.headers['x-organization-id'] as string;

  // Only allow override if user has admin role
  if (overrideOrgId && tenantReq.user?.role === 'SUPER_ADMIN') {
    tenantReq.tenant.organizationId = overrideOrgId;
  }

  next();
};
```

### 4. Base Tenant Repository

```typescript
// backend/src/repositories/base-tenant.repository.ts

import { PrismaClient } from '@prisma/client';
import { TenantContext } from '../types/tenant.types';

export abstract class BaseTenantRepository<T> {
  constructor(protected prisma: PrismaClient) {}

  /**
   * Find by ID with automatic tenant filtering
   */
  protected async findByIdWithTenant(
    model: any,
    id: string,
    tenant: TenantContext
  ): Promise<T | null> {
    return model.findFirst({
      where: {
        id,
        organizationId: tenant.organizationId
      }
    });
  }

  /**
   * Find many with automatic tenant filtering
   */
  protected async findManyWithTenant(
    model: any,
    where: any,
    tenant: TenantContext
  ): Promise<T[]> {
    return model.findMany({
      where: {
        ...where,
        organizationId: tenant.organizationId
      }
    });
  }

  /**
   * Create with automatic tenant context
   */
  protected async createWithTenant(
    model: any,
    data: any,
    tenant: TenantContext
  ): Promise<T> {
    return model.create({
      data: {
        ...data,
        organizationId: tenant.organizationId
      }
    });
  }

  /**
   * Update with tenant validation
   */
  protected async updateWithTenant(
    model: any,
    id: string,
    data: any,
    tenant: TenantContext
  ): Promise<T> {
    // First verify record belongs to tenant
    const existing = await this.findByIdWithTenant(model, id, tenant);
    if (!existing) {
      throw new Error(`Record ${id} not found for organization ${tenant.organizationId}`);
    }

    return model.update({
      where: { id },
      data
    });
  }

  /**
   * Delete with tenant validation
   */
  protected async deleteWithTenant(
    model: any,
    id: string,
    tenant: TenantContext
  ): Promise<T> {
    // First verify record belongs to tenant
    const existing = await this.findByIdWithTenant(model, id, tenant);
    if (!existing) {
      throw new Error(`Record ${id} not found for organization ${tenant.organizationId}`);
    }

    return model.delete({
      where: { id }
    });
  }
}
```

### 5. Concrete Repository Implementation

```typescript
// backend/src/repositories/member.repository.ts

import { PrismaClient, Member } from '@prisma/client';
import { BaseTenantRepository } from './base-tenant.repository';
import { TenantContext } from '../types/tenant.types';

export interface CreateMemberDto {
  email: string;
  firstName: string;
  lastName: string;
  phoneNumber?: string;
  status?: 'ACTIVE' | 'INACTIVE';
}

export interface UpdateMemberDto {
  email?: string;
  firstName?: string;
  lastName?: string;
  phoneNumber?: string;
  status?: 'ACTIVE' | 'INACTIVE';
}

export class MemberRepository extends BaseTenantRepository<Member> {
  constructor(prisma: PrismaClient) {
    super(prisma);
  }

  async findById(id: string, tenant: TenantContext): Promise<Member | null> {
    return this.findByIdWithTenant(this.prisma.member, id, tenant);
  }

  async findByEmail(email: string, tenant: TenantContext): Promise<Member | null> {
    return this.prisma.member.findUnique({
      where: {
        organizationId_email: {
          organizationId: tenant.organizationId,
          email
        }
      }
    });
  }

  async findAll(tenant: TenantContext, filters?: {
    status?: string;
    search?: string;
  }): Promise<Member[]> {
    const where: any = {
      organizationId: tenant.organizationId
    };

    if (filters?.status) {
      where.status = filters.status;
    }

    if (filters?.search) {
      where.OR = [
        { email: { contains: filters.search, mode: 'insensitive' } },
        { firstName: { contains: filters.search, mode: 'insensitive' } },
        { lastName: { contains: filters.search, mode: 'insensitive' } }
      ];
    }

    return this.prisma.member.findMany({ where });
  }

  async create(data: CreateMemberDto, tenant: TenantContext): Promise<Member> {
    // Check for duplicate email within tenant
    const existing = await this.findByEmail(data.email, tenant);
    if (existing) {
      throw new Error(`Member with email ${data.email} already exists`);
    }

    return this.createWithTenant(this.prisma.member, data, tenant);
  }

  async update(
    id: string,
    data: UpdateMemberDto,
    tenant: TenantContext
  ): Promise<Member> {
    // If updating email, check for duplicates
    if (data.email) {
      const existing = await this.findByEmail(data.email, tenant);
      if (existing && existing.id !== id) {
        throw new Error(`Member with email ${data.email} already exists`);
      }
    }

    return this.updateWithTenant(this.prisma.member, id, data, tenant);
  }

  async delete(id: string, tenant: TenantContext): Promise<Member> {
    return this.deleteWithTenant(this.prisma.member, id, tenant);
  }

  async count(tenant: TenantContext): Promise<number> {
    return this.prisma.member.count({
      where: { organizationId: tenant.organizationId }
    });
  }
}
```

### 6. Service Layer with Tenant Context

```typescript
// backend/src/services/member.service.ts

import { MemberRepository, CreateMemberDto, UpdateMemberDto } from '../repositories/member.repository';
import { TenantContext } from '../types/tenant.types';
import { Member } from '@prisma/client';

export class MemberService {
  constructor(private memberRepository: MemberRepository) {}

  async getMember(id: string, tenant: TenantContext): Promise<Member | null> {
    return this.memberRepository.findById(id, tenant);
  }

  async getMembers(tenant: TenantContext, filters?: {
    status?: string;
    search?: string;
  }): Promise<Member[]> {
    return this.memberRepository.findAll(tenant, filters);
  }

  async createMember(data: CreateMemberDto, tenant: TenantContext): Promise<Member> {
    // Business logic validation
    if (!this.isValidEmail(data.email)) {
      throw new Error('Invalid email format');
    }

    return this.memberRepository.create(data, tenant);
  }

  async updateMember(
    id: string,
    data: UpdateMemberDto,
    tenant: TenantContext
  ): Promise<Member> {
    if (data.email && !this.isValidEmail(data.email)) {
      throw new Error('Invalid email format');
    }

    return this.memberRepository.update(id, data, tenant);
  }

  async deleteMember(id: string, tenant: TenantContext): Promise<void> {
    await this.memberRepository.delete(id, tenant);
  }

  private isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
}
```

### 7. Controller with Tenant Context

```typescript
// backend/src/controllers/member.controller.ts

import { Response, NextFunction } from 'express';
import { TenantRequest } from '../types/tenant.types';
import { MemberService } from '../services/member.service';

export class MemberController {
  constructor(private memberService: MemberService) {}

  async getMembers(req: TenantRequest, res: Response, next: NextFunction) {
    try {
      const { status, search } = req.query;
      const members = await this.memberService.getMembers(
        req.tenant,
        {
          status: status as string,
          search: search as string
        }
      );
      res.json({ data: members });
    } catch (error) {
      next(error);
    }
  }

  async getMember(req: TenantRequest, res: Response, next: NextFunction) {
    try {
      const { id } = req.params;
      const member = await this.memberService.getMember(id, req.tenant);

      if (!member) {
        return res.status(404).json({ error: 'Member not found' });
      }

      res.json({ data: member });
    } catch (error) {
      next(error);
    }
  }

  async createMember(req: TenantRequest, res: Response, next: NextFunction) {
    try {
      const member = await this.memberService.createMember(
        req.body,
        req.tenant
      );
      res.status(201).json({ data: member });
    } catch (error) {
      next(error);
    }
  }

  async updateMember(req: TenantRequest, res: Response, next: NextFunction) {
    try {
      const { id } = req.params;
      const member = await this.memberService.updateMember(
        id,
        req.body,
        req.tenant
      );
      res.json({ data: member });
    } catch (error) {
      next(error);
    }
  }

  async deleteMember(req: TenantRequest, res: Response, next: NextFunction) {
    try {
      const { id } = req.params;
      await this.memberService.deleteMember(id, req.tenant);
      res.status(204).send();
    } catch (error) {
      next(error);
    }
  }
}
```

### 8. Router with Tenant Middleware

```typescript
// backend/src/routes/member.routes.ts

import { Router } from 'express';
import { MemberController } from '../controllers/member.controller';
import { authMiddleware } from '../middleware/auth.middleware';
import { tenantMiddleware } from '../middleware/tenant.middleware';

export const createMemberRouter = (memberController: MemberController): Router => {
  const router = Router();

  // All routes require authentication and tenant context
  router.use(authMiddleware);
  router.use(tenantMiddleware);

  router.get('/', memberController.getMembers.bind(memberController));
  router.get('/:id', memberController.getMember.bind(memberController));
  router.post('/', memberController.createMember.bind(memberController));
  router.put('/:id', memberController.updateMember.bind(memberController));
  router.delete('/:id', memberController.deleteMember.bind(memberController));

  return router;
};
```

### 9. Testing Tenant Isolation

```typescript
// backend/src/repositories/__tests__/member.repository.test.ts

import { PrismaClient } from '@prisma/client';
import { MemberRepository } from '../member.repository';
import { TenantContext } from '../../types/tenant.types';

describe('MemberRepository - Tenant Isolation', () => {
  let prisma: PrismaClient;
  let repository: MemberRepository;
  let tenant1: TenantContext;
  let tenant2: TenantContext;

  beforeAll(async () => {
    prisma = new PrismaClient();
    repository = new MemberRepository(prisma);

    tenant1 = { organizationId: 'org-1' };
    tenant2 = { organizationId: 'org-2' };
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  describe('Tenant Isolation', () => {
    it('should isolate members by tenant', async () => {
      // Create member for tenant 1
      const member1 = await repository.create(
        { email: 'user@tenant1.com', firstName: 'John', lastName: 'Doe' },
        tenant1
      );

      // Create member for tenant 2
      const member2 = await repository.create(
        { email: 'user@tenant2.com', firstName: 'Jane', lastName: 'Doe' },
        tenant2
      );

      // Verify tenant 1 can only see their members
      const tenant1Members = await repository.findAll(tenant1);
      expect(tenant1Members).toHaveLength(1);
      expect(tenant1Members[0].id).toBe(member1.id);

      // Verify tenant 2 can only see their members
      const tenant2Members = await repository.findAll(tenant2);
      expect(tenant2Members).toHaveLength(1);
      expect(tenant2Members[0].id).toBe(member2.id);
    });

    it('should prevent cross-tenant access by ID', async () => {
      const member = await repository.create(
        { email: 'test@tenant1.com', firstName: 'Test', lastName: 'User' },
        tenant1
      );

      // Tenant 2 should not be able to access tenant 1's member
      const result = await repository.findById(member.id, tenant2);
      expect(result).toBeNull();
    });

    it('should allow duplicate emails across tenants', async () => {
      const email = 'duplicate@example.com';

      // Create member with same email in different tenants
      const member1 = await repository.create(
        { email, firstName: 'User1', lastName: 'Tenant1' },
        tenant1
      );

      const member2 = await repository.create(
        { email, firstName: 'User2', lastName: 'Tenant2' },
        tenant2
      );

      expect(member1.email).toBe(email);
      expect(member2.email).toBe(email);
      expect(member1.id).not.toBe(member2.id);
    });

    it('should prevent duplicate emails within same tenant', async () => {
      const email = 'duplicate@tenant1.com';

      await repository.create(
        { email, firstName: 'First', lastName: 'User' },
        tenant1
      );

      // Attempt to create duplicate
      await expect(
        repository.create(
          { email, firstName: 'Second', lastName: 'User' },
          tenant1
        )
      ).rejects.toThrow();
    });
  });
});
```

## Best Practices

1. **Always validate tenant context** - Never trust org_id from client
2. **Use composite unique constraints** - [organizationId, businessKey]
3. **Audit tenant operations** - Log org_id in all mutations
4. **Test isolation rigorously** - Automated tests for cross-tenant leakage
5. **Index efficiently** - Include organizationId in all query indexes
6. **Handle errors gracefully** - Don't expose cross-tenant data in errors
7. **Document tenant boundaries** - Clear API documentation on scoping

## Common Pitfalls

- ❌ Forgetting to add organizationId to WHERE clause
- ❌ Using findUnique with just ID (bypasses tenant filter)
- ❌ Exposing global IDs without validation
- ❌ Accepting org_id from request body
- ❌ Missing indexes on [organizationId, ...]
- ❌ Not testing cross-tenant access scenarios

## Migration Checklist

When adding multi-tenancy to existing models:

1. Add `organizationId String @map("organization_id")` field
2. Add relation to Organization model
3. Update all unique constraints to include organizationId
4. Create indexes: `@@index([organizationId, otherField])`
5. Update all queries to filter by organizationId
6. Add tenant context to all repository methods
7. Write tenant isolation tests
8. Run migration: `npx prisma migrate dev`

## Related Skills

- **authentication** - JWT token structure and claims
- **rest-api** - API design with tenant scoping
- **database** - Prisma schema design and indexing
- **testing** - Integration tests for tenant isolation
