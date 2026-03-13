---
name: nestjs-testing
description: NestJS backend test writing following Sellernote conventions. Use when creating unit tests, integration tests, or e2e tests for NestJS services, controllers, repositories, or modules. Triggers on tasks involving test writing, spec files, jest mocking, service testing, controller testing, repository testing, e2e testing, test coverage, or any backend testing work in a NestJS project. Also use when asked to write tests, add unit tests, create e2e tests, add spec files, or verify test quality for Sellernote's 3-layer architecture (Controller → Service → Repository).
---

# NestJS Testing

Write NestJS tests following Sellernote's 3-layer architecture and convention documents.

## Convention Loading

Before starting any work, Read the relevant reference files from `references/` within this skill directory:

1. **Always read first** (core rules):
   - `references/BACKEND_CONVENTION.md` - 3-layer architecture, DTO/Entity naming, test strategy, test pyramid, anti-patterns
   - `references/NESTJS_CONVENTION.md` - Project structure, DI patterns, module config, Domain Model Interface, money handling, DTO validation with `@sellernote/sellernote-nestjs-api-property`, exception handling

2. **Read when relevant**:
   - `references/BACKEND_ARCHITECTURE_CONVENTION.md` - Layer responsibility matrix (what each layer may/must not do), repository allowed/prohibited patterns, monorepo dependency direction, anti-patterns (Fat Repository, Anemic Service)
   - `references/COMMON_CONVENTION.md` - Naming conventions, error code format (`{DOMAIN}_{CATEGORY}_{DETAIL}`), error response format, logging
   - `references/TYPESCRIPT_CONVENTION.md` - Type system, import ordering, enum/union conventions, anti-patterns

## Workflow

Follow these steps sequentially. Skip a step only when it does not apply to the task.

### Step 1: Analyze Target Module

1. Identify the target feature module under `src/modules/`
2. Read the source files and understand:
   - Module structure: `controllers/`, `services/`, `repositories/`, `entities/`, `dto/`, `interfaces/`, `mappers/`
   - Service dependencies (Repositories, other Services via constructor injection)
   - Controller endpoints and DTO types
   - Repository methods (find options, QueryBuilder usage)
   - Domain Model Interface (`interfaces/{feature}.model.interface.ts`)
   - Entity relations and which fields map to the Domain Model Interface
3. Determine which test types are needed:
   - **Unit test**: Service, Repository, Controller in isolation
   - **Integration test**: Service + Repository together
   - **E2E test**: Full HTTP request/response cycle with `supertest`

### Step 2: Service Unit Test

Service tests are the most important -- they cover all business logic.

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { NotFoundException } from '@nestjs/common';
import Big from 'big.js';

import { OrderCrudService } from './order-crud.service';
import { OrderRepository } from '../repositories/order.repository';

describe('OrderCrudService', () => {
  let service: OrderCrudService;
  let orderRepository: jest.Mocked<OrderRepository>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        OrderCrudService,
        {
          provide: OrderRepository,
          useValue: {
            findOne: jest.fn(),
            save: jest.fn(),
            findByFilter: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get(OrderCrudService);
    orderRepository = module.get(OrderRepository);
  });

  describe('calculateTotal', () => {
    it('should calculate total using big.js for money precision', () => {
      const items = [
        { price: '10.50', quantity: 3 },
        { price: '20.00', quantity: 2 },
      ];

      const result = service.calculateTotal(items);

      const expected = new Big('10.50').times(3)
        .plus(new Big('20.00').times(2)).toFixed(2);
      expect(result).toBe(expected);
    });
  });

  describe('findOne', () => {
    it('should return order when found', async () => {
      const mockOrder = { id: 'uuid-1', orderNumber: 'ORD-001' };
      orderRepository.findOne.mockResolvedValue(mockOrder as any);

      const result = await service.findOne('uuid-1');

      expect(result).toEqual(mockOrder);
      expect(orderRepository.findOne).toHaveBeenCalledWith({
        where: { id: 'uuid-1' },
      });
    });

    it('should throw NotFoundException when order not found', async () => {
      orderRepository.findOne.mockResolvedValue(null);

      await expect(service.findOne('non-existent'))
        .rejects.toThrow(NotFoundException);
    });
  });
});
```

Key rules:
- [MUST] Use `jest.Mocked<T>` for type-safe mocking of all constructor-injected dependencies
- [MUST] Never connect to a real database in unit tests
- [MUST] Use `big.js` for money-related assertions (never floating-point comparison)
- [MUST] Test both happy path and error cases (NotFoundException, custom business exceptions)
- [MUST] Verify business logic lives only in Service (not Controller or Repository)
- [MUST] Mock all dependencies injected via constructor

### Step 3: Repository Unit Test

Repository tests verify query construction and data retrieval. Sellernote repositories use `extends Repository<Entity>` with `DataSource` constructor injection.

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { DataSource, SelectQueryBuilder } from 'typeorm';

import { OrderRepository } from './order.repository';
import { Order } from '../entities/order.entity';

describe('OrderRepository', () => {
  let repository: OrderRepository;
  let queryBuilder: jest.Mocked<SelectQueryBuilder<Order>>;

  beforeEach(async () => {
    queryBuilder = {
      where: jest.fn().mockReturnThis(),
      andWhere: jest.fn().mockReturnThis(),
      leftJoinAndSelect: jest.fn().mockReturnThis(),
      orderBy: jest.fn().mockReturnThis(),
      skip: jest.fn().mockReturnThis(),
      take: jest.fn().mockReturnThis(),
      getManyAndCount: jest.fn(),
      getOne: jest.fn(),
      select: jest.fn().mockReturnThis(),
      addSelect: jest.fn().mockReturnThis(),
      getRawOne: jest.fn(),
    } as any;

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        OrderRepository,
        {
          provide: DataSource,
          useValue: { createEntityManager: jest.fn() },
        },
      ],
    }).compile();

    repository = module.get(OrderRepository);
    jest.spyOn(repository, 'createQueryBuilder')
      .mockReturnValue(queryBuilder as any);
  });

  describe('findByFilter', () => {
    it('should apply pagination and return count', async () => {
      const mockOrders = [{ id: '1' }, { id: '2' }];
      queryBuilder.getManyAndCount.mockResolvedValue([mockOrders as any, 2]);

      const [orders, count] = await repository.findByFilter({
        page: 1, size: 10,
      });

      expect(orders).toHaveLength(2);
      expect(count).toBe(2);
      expect(queryBuilder.skip).toHaveBeenCalledWith(0);
      expect(queryBuilder.take).toHaveBeenCalledWith(10);
    });

    it('should apply filter conditions when provided', async () => {
      queryBuilder.getManyAndCount.mockResolvedValue([[], 0]);

      await repository.findByFilter({
        page: 1, size: 10, status: 'pending',
      });

      expect(queryBuilder.andWhere).toHaveBeenCalledWith(
        'order.status = :status',
        { status: 'pending' },
      );
    });
  });
});
```

Key rules:
- [MUST] Mock `DataSource` (not `getRepositoryToken`) -- Sellernote repositories extend `Repository<Entity>` with `DataSource` constructor injection
- [MUST] Use `jest.spyOn(repository, 'createQueryBuilder')` to mock QueryBuilder
- [MUST] Mock `SelectQueryBuilder` chain methods with `mockReturnThis()`
- [MUST] Verify parameterized queries (no string interpolation in WHERE clauses)
- [MUST] Test pagination offset: `(page - 1) * size`
- [MUST] Verify no business logic in Repository (no if/else business branching, no HttpException)

### Step 4: Controller Unit Test

Controller tests verify HTTP layer delegation -- controllers must contain no business logic.

```typescript
import { Test, TestingModule } from '@nestjs/testing';

import { OrderCrudController } from './order-crud.controller';
import { OrderCrudService } from '../services/order-crud.service';

describe('OrderCrudController', () => {
  let controller: OrderCrudController;
  let service: jest.Mocked<OrderCrudService>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [OrderCrudController],
      providers: [
        {
          provide: OrderCrudService,
          useValue: {
            findOne: jest.fn(),
            create: jest.fn(),
            findList: jest.fn(),
          },
        },
      ],
    }).compile();

    controller = module.get(OrderCrudController);
    service = module.get(OrderCrudService);
  });

  describe('findOne', () => {
    it('should delegate to service and return result', async () => {
      const mockOrder = { id: 'uuid-1', orderNumber: 'ORD-001' };
      service.findOne.mockResolvedValue(mockOrder as any);

      const result = await controller.findOne('uuid-1');

      expect(service.findOne).toHaveBeenCalledWith('uuid-1');
      expect(result).toEqual(mockOrder);
    });
  });
});
```

Key rules:
- [MUST] Verify controller delegates to Service (no business logic in controller)
- [MUST] Test parameter passing from HTTP layer to Service layer
- [MUST] Mock the entire Service (controller should only orchestrate)
- [MUST] Use split controller naming when applicable (`OrderCrudController`, `OrderFulfillmentController`)

### Step 5: E2E Test

E2E tests verify the full request/response cycle.

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import * as request from 'supertest';

import { AppModule } from '../src/app.module';

describe('Order (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();

    // [MUST] Apply same ValidationPipe as production
    app.useGlobalPipes(
      new ValidationPipe({
        whitelist: true,
        forbidNonWhitelisted: true,
        transform: true,
      }),
    );

    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  describe('POST /orders', () => {
    it('should reject invalid DTO with 400', () => {
      return request(app.getHttpServer())
        .post('/orders')
        .send({ productName: '' })
        .expect(400);
    });

    it('should create order with valid data', () => {
      return request(app.getHttpServer())
        .post('/orders')
        .send({
          productName: 'Test Product',
          quantity: 1,
          totalAmount: '100.00', // money as string
        })
        .expect(201)
        .expect((res) => {
          expect(res.body.success).toBe(true);
          expect(res.body.data).toHaveProperty('id');
        });
    });
  });

  describe('GET /orders/:id', () => {
    it('should return 404 for non-existent order', () => {
      return request(app.getHttpServer())
        .get('/orders/non-existent-uuid')
        .expect(404)
        .expect((res) => {
          expect(res.body.success).toBe(false);
          expect(res.body.error).toHaveProperty('code');
          expect(res.body.error).toHaveProperty('message');
        });
    });
  });
});
```

Key rules:
- [MUST] Apply same `ValidationPipe` config as production (`whitelist`, `forbidNonWhitelisted`, `transform`)
- [MUST] Test DTO validation (invalid inputs return 400)
- [MUST] Test response format: `{ success: boolean, data: T | null, error: { code, message } | null }`
- [MUST] Money fields in request bodies must be `string` type
- [MUST] Use `beforeAll`/`afterAll` for app lifecycle (not `beforeEach` -- too slow)
- [MUST] Verify proper HTTP status codes (400, 401, 403, 404, 409, etc.)

### Step 6: Test Quality Verification

After writing tests, verify:

- [ ] All Service business logic paths covered (happy path + error cases)
- [ ] Money calculations use `big.js` in both production code and test assertions
- [ ] No real database connections in unit tests
- [ ] `jest.Mocked<T>` used for all mocked dependencies
- [ ] No business logic tested in Controller or Repository tests (those belong in Service)
- [ ] Repository tests verify no business branching (no if/else, no HttpException)
- [ ] E2E tests use production-identical `ValidationPipe` settings
- [ ] Response format tested: `{ success, data, error }`
- [ ] Error codes follow `{DOMAIN}_{CATEGORY}_{DETAIL}` format when applicable
- [ ] Test file naming: `{name}.{type}.spec.ts` for unit, `{name}.e2e-spec.ts` for e2e
- [ ] Each test has a clear, descriptive name explaining expected behavior
- [ ] Custom business exceptions tested (e.g., `InsufficientStockException`)
- [ ] Layer boundaries respected: Controller → Service → Repository (no skipping)

## File Structure Reference

```
src/modules/{feature}/
├── controllers/
│   └── {feature}-crud.controller.spec.ts     # Controller unit tests
├── services/
│   └── {feature}-crud.service.spec.ts        # Service unit tests
├── repositories/
│   └── {feature}.repository.spec.ts          # Repository unit tests
├── interfaces/
│   └── {feature}.model.interface.ts          # Domain Model Interface
├── entities/
├── dto/
└── mappers/

test/
├── {feature}.e2e-spec.ts                     # E2E tests
├── jest-e2e.json                             # E2E jest config
└── ...
```

## Sellernote-Specific Testing Patterns

### Domain Model Interface in Tests

Use the Domain Model Interface when creating test fixtures for Service or Mapper tests:

```typescript
import type { IOrderModel } from '../interfaces/order.model.interface';

const mockOrder: IOrderModel = {
  id: 'uuid-1',
  _no: 1,
  orderNumber: 'ORD-001',
  totalAmount: 10000,
  status: 'pending',
  userId: 'user-1',
  createdAt: new Date(),
  updatedAt: new Date(),
  deletedAt: null,
};
```

### Testing Custom Business Exceptions

Sellernote defines domain-specific exceptions extending HttpException subclasses:

```typescript
import { InsufficientStockException } from '../exceptions/insufficient-stock.exception';

it('should throw InsufficientStockException when stock is insufficient', async () => {
  productRepository.findOne.mockResolvedValue({ id: 'prod-1', stock: 5 } as any);

  await expect(service.decreaseStock('prod-1', 10))
    .rejects.toThrow(InsufficientStockException);
});
```

### Testing Monorepo Application → Library Dependencies

When testing Application-level Services that depend on Library Services:

```typescript
import { UserOrderService } from './user-order.service';
import { OrderLibService } from '@sellernote/order-lib';
import { PaymentLibService } from '@sellernote/payment-lib';

describe('UserOrderService', () => {
  let service: UserOrderService;
  let orderLibService: jest.Mocked<OrderLibService>;
  let paymentLibService: jest.Mocked<PaymentLibService>;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        UserOrderService,
        { provide: OrderLibService, useValue: { createOrder: jest.fn() } },
        { provide: PaymentLibService, useValue: { requestPayment: jest.fn() } },
      ],
    }).compile();

    service = module.get(UserOrderService);
    orderLibService = module.get(OrderLibService);
    paymentLibService = module.get(PaymentLibService);
  });

  it('should create order then request payment', async () => {
    orderLibService.createOrder.mockResolvedValue({ id: 'order-1' } as any);

    await service.createOrder(mockDto);

    expect(orderLibService.createOrder).toHaveBeenCalledWith(mockDto);
    expect(paymentLibService.requestPayment).toHaveBeenCalledWith(
      'order-1',
      mockDto.paymentMethod,
    );
  });
});
```

## Cross-Skill References

- **Production code implementation**: Use the `nestjs-api-dev` skill for Controller/Service/Repository code
- **Entity/TypeORM patterns**: Use the `typeorm-dev` skill for Entity definitions, Relations, and TypeORM-specific patterns
