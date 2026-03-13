---
name: logging-backend
description: Implementa Wide Events para logging backend estructurado. Usa cuando el usuario diga "agregar logging", "add logging", "mejorar logs", "improve logs", "wide events", "observabilidad", "observability", "canonical log lines", "structured logging", o necesite logs estructurados.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Logging Backend - Wide Events

Implementa **Wide Events** (también conocidos como Canonical Log Lines): un evento estructurado por request que contiene TODO el contexto relevante en un solo registro.

## Concepto Core

Un **Wide Event** es un único log JSON que captura el ciclo completo de un request. En lugar de múltiples logs dispersos (`"user logged in"`, `"fetched data"`, `"returned response"`), emitís UN evento al final con toda la información agregada.

**Beneficios:**
- Debuggear con UN query en vez de correlacionar múltiples logs
- Análisis con SQL simple sobre campos estructurados
- Sin pérdida de contexto entre logs
- Tail sampling efectivo (solo guardar eventos interesantes)

**Comparación: Log tradicional vs Wide Event:**

```
// ❌ Log tradicional - múltiples líneas dispersas
[10:30:00] INFO: User 789 logged in
[10:30:01] INFO: Fetching orders for user 789
[10:30:02] DEBUG: Query executed in 45ms
[10:30:02] INFO: Found 3 orders
[10:30:03] ERROR: Failed to send email notification

// ✅ Wide Event - todo en un solo registro
{
  "timestamp": "2024-01-15T10:30:03.000Z",
  "user": { "id": "789" },
  "action": "fetch_orders",
  "result": { "count": 3 },
  "infra": { "db_time_ms": 45 },
  "error": { "type": "email_failed", "message": "SMTP timeout" }
}
```

## Estructura de un Wide Event

```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "level": "info",
  "service": "api-gateway",
  "trace_id": "abc123",

  "request": { "method": "POST", "path": "/api/orders", "duration_ms": 245 },
  "user": { "id": "user_789", "plan": "premium" },
  "business": { "order_id": "ord_456", "total": 150.00, "items_count": 3 },
  "infra": { "db_queries": 4, "db_time_ms": 120, "cache_hits": 2 },
  "error": null
}
```

Ver `wide-event-schema.md` para esquema completo con todos los campos recomendados.

## Workflow de Implementación

### Fase 1: Middleware Base
1. Crear middleware que inicializa el wide event al inicio del request
2. Adjuntar el evento al contexto (req.wideEvent, AsyncLocalStorage, etc.)
3. Emitir el log al finalizar el request

Ver `implementation.md` para código del middleware.

### Fase 2: Enriquecimiento
1. En cada handler/service, agregar campos al wide event
2. Usar helpers tipados: `enrichUser()`, `enrichBusiness()`, `enrichError()`
3. Acumular métricas: queries, cache hits, llamadas externas

### Fase 3: Tail Sampling
1. Implementar función de sampling que decide qué loggear
2. Siempre loggear: errores, latencia alta, usuarios específicos
3. Samplear porcentaje de requests exitosos normales

Ver `implementation.md` para función de tail sampling.

### Fase 4: Colorización (Desarrollo)
1. Configurar colores por nivel (ERROR=rojo, WARN=amarillo)
2. Configurar colores por contexto (Request=azul, User=verde)
3. Formatear output legible en terminal

Ver `colorization.md` para configuración de colores.

## Checklist Rápido

- [ ] Middleware que crea wide event por request
- [ ] Contexto accesible en toda la cadena (AsyncLocalStorage / req)
- [ ] Campos request: method, path, status, duration_ms
- [ ] Campos user: id, plan, roles (si aplica)
- [ ] Campos business: entidades del dominio
- [ ] Campos infra: db_queries, cache_hits, external_calls
- [ ] Campos error: code, message, stack (si hay error)
- [ ] Tail sampling configurado
- [ ] Formato JSON en prod, coloreado en dev

## Anti-patrones

Ver `anti-patterns.md` para errores comunes:
- Confundir structured logging con wide events
- Depender solo de OpenTelemetry
- Loggear múltiples veces por request
- No incluir contexto de negocio

## Referencias

- `wide-event-schema.md` - Esquema JSON completo con todos los campos
- `implementation.md` - Código de middleware y helpers
- `anti-patterns.md` - Qué NO hacer
- `colorization.md` - Configuración de colores para dev

## Troubleshooting

### El wide event no captura datos del usuario

**Síntoma:** `user: null` en todos los logs

**Causa común:** El middleware de auth corre después del wide event middleware.

**Solución:**
```typescript
// ❌ Orden incorrecto
app.use(wideEventMiddleware('my-service'));
app.use(authMiddleware); // user no disponible cuando se crea el evento

// ✅ Orden correcto
app.use(authMiddleware);
app.use(wideEventMiddleware('my-service')); // user ya está en req
```

### Los logs salen vacíos en infra.db

**Síntoma:** `db: { queries_count: 0, total_time_ms: 0 }`

**Causa común:** No estás usando los helpers de tracking.

**Solución:** Wrappear las queries:
```typescript
// Wrapper para tu ORM/cliente de DB
const query = async (sql: string) => {
  const start = Date.now();
  const result = await db.query(sql);
  trackDbQuery(Date.now() - start); // ← Esto falta
  return result;
};
```

### Logs demasiado grandes en producción

**Síntoma:** Costos altos de almacenamiento/ingesta

**Solución:** Implementar tail sampling agresivo:
```typescript
const shouldLog = (event: WideEvent): boolean => {
  if (event.level === 'error') return true;
  if (event.request.duration_ms > 1000) return true;
  return Math.random() < 0.01; // Solo 1% del resto
};
```

### No puedo correlacionar logs entre servicios

**Síntoma:** Cada servicio tiene su propio trace_id

**Causa:** No estás propagando el header.

**Solución:** Ver `references/implementation.md` sección "Propagación Cross-Service".

## Lecturas Recomendadas

- [Stripe Engineering - Canonical Log Lines](https://stripe.com/blog/canonical-log-lines) - El artículo original que popularizó el patrón
- [Observability Wide Events 101](https://boristane.com/blog/observability-wide-events-101/) - Guía práctica de implementación
- [Logging Sucks](https://loggingsucks.com) - Por qué el logging tradicional no escala
