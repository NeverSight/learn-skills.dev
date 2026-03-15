---
name: prisma-nestjs-patterns
description: >
  Patrones de integración de Prisma ORM con NestJS para aplicaciones de producción.
  Usar PROACTIVAMENTE cuando se trabaje con esquemas Prisma, migraciones, PrismaService,
  transacciones atómicas (incluyendo SELECT FOR UPDATE), repositorios como adaptadores de
  infraestructura en Clean Architecture, queries optimizadas (N+1, includes, paginación),
  seeds y testing con Prisma Mock. Activar siempre que aparezcan las palabras clave:
  Prisma, PrismaService, prisma.$transaction, prisma migrate, schema.prisma, PrismaClient,
  Prisma.validator, include/select, upsert, createMany, o cualquier operación de
  base de datos con Prisma en un proyecto NestJS.
---

# Prisma ORM + NestJS — Patrones de Producción

Guía completa de integración Prisma con NestJS siguiendo Clean Architecture. Cubre desde la
configuración base hasta transacciones atómicas críticas, repositorios, optimización de queries
y testing.

## Referencias disponibles

Lee el archivo correspondiente cuando necesites profundidad en un área específica:

- `references/setup-and-service.md` — Instalación, PrismaService, módulo global, health check
- `references/schema-and-migrations.md` — Schema design, tipos, relaciones, índices, migraciones
- `references/repository-pattern.md` — Repositorios como adaptadores de infraestructura (Clean Architecture)
- `references/transactions.md` — Transacciones atómicas, SELECT FOR UPDATE, manejo de concurrencia
- `references/query-patterns.md` — N+1 prevention, include/select, paginación, queries complejas
- `references/testing.md` — Testing con jest-mock-extended, prisma-mock, integración con testcontainers

---

## Cuándo usar cada referencia

| Tarea                                            | Referencia                 |
| ------------------------------------------------ | -------------------------- |
| Configurar Prisma por primera vez en NestJS      | `setup-and-service.md`     |
| Diseñar o modificar el schema, crear migraciones | `schema-and-migrations.md` |
| Crear repositorios para un módulo de dominio     | `repository-pattern.md`    |
| Reservas, locks, operaciones concurrentes        | `transactions.md`          |
| Optimizar queries lentas, eliminar N+1           | `query-patterns.md`        |
| Mockear Prisma en tests unitarios/integración    | `testing.md`               |

---

## Reglas críticas (siempre en contexto)

### 1. PrismaService es global, nunca instanciar PrismaClient directamente

```typescript
// ❌ Nunca
const prisma = new PrismaClient();

// ✅ Siempre via inyección de dependencias
constructor(private readonly prisma: PrismaService) {}
```

### 2. Transacciones atómicas para operaciones de escritura compuestas

```typescript
// ✅ Patrón correcto para cualquier operación que modifique >1 tabla
await this.prisma.$transaction(async (tx) => {
  const gift = await tx.gift.findUnique({ where: { id: giftId } });
  if (gift.status !== 'AVAILABLE') throw new ConflictException();
  await tx.gift.update({ where: { id: giftId }, data: { status: 'RESERVED' } });
  await tx.reservation.create({ data: { giftId, reservedById: userId } });
});
```

### 3. Repositorios en la capa de infraestructura, nunca en controllers ni services de dominio

```typescript
// La interfaz vive en el dominio
export interface ReservationRepository {
  findActiveByGiftId(giftId: string): Promise<Reservation | null>;
  create(data: CreateReservationData): Promise<Reservation>;
}

// La implementación Prisma vive en infraestructura
@Injectable()
export class PrismaReservationRepository implements ReservationRepository { ... }
```

### 4. Nunca exponer el PrismaClient fuera del módulo de infraestructura

Los módulos de dominio y aplicación trabajan contra interfaces, no contra Prisma directamente.

### 5. Siempre usar `select` o `include` explícito — nunca retornar el modelo completo

```typescript
// ❌ Retorna passwordHash, campos internos
return this.prisma.user.findUnique({ where: { id } });

// ✅ Solo los campos necesarios
return this.prisma.user.findUnique({
  where: { id },
  select: { id: true, nombre: true, email: true, createdAt: true }
});
```

---

## Fuentes y documentación oficial

- **Prisma Docs — NestJS Integration**: https://www.prisma.io/docs/guides/other/nestjs
- **Prisma Docs — Transactions**: https://www.prisma.io/docs/orm/prisma-client/queries/transactions
- **Prisma Docs — Interactive Transactions**: https://www.prisma.io/docs/orm/prisma-client/queries/transactions#interactive-transactions
- **Prisma Docs — Select/Include**: https://www.prisma.io/docs/orm/prisma-client/queries/select-fields
- **Prisma Docs — Relation Queries**: https://www.prisma.io/docs/orm/prisma-client/queries/relation-queries
- **Prisma Docs — Migrations**: https://www.prisma.io/docs/orm/prisma-migrate
- **NestJS Docs — Database**: https://docs.nestjs.com/techniques/database
- **Prisma Blog — NestJS Best Practices**: https://www.prisma.io/blog/nestjs-prisma-rest-api-7D056s1BmOL0
- **jest-mock-extended**: https://github.com/marchaos/jest-mock-extended
