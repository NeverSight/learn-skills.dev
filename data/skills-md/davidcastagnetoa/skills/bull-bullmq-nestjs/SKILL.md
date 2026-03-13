---
name: bull-bullmq-nestjs
description: >
  Patrones de colas de tareas asíncronas con Bull/BullMQ en NestJS para producción.
  Usar PROACTIVAMENTE cuando se trabaje con jobs programados, recordatorios, notificaciones
  asíncronas, procesamiento en background, o cualquier tarea que no deba ejecutarse de forma
  síncrona en el ciclo de request/response. Activar siempre que aparezcan las palabras clave:
  Bull, BullMQ, @BullModule, @Processor, @Process, @OnQueueFailed, addJob, Queue, Worker,
  jobs, colas, tareas programadas, delayed jobs, recordatorio programado, notificación asíncrona,
  background job, retry, dead letter queue, o colas con Redis en NestJS.
  También activar para la transición Bull (desarrollo) → Cloud Tasks (producción GCP).
---

# Bull / BullMQ + NestJS — Colas de Tareas Asíncronas

Guía completa de implementación de colas con Bull/BullMQ en NestJS. Cubre configuración,
processors, jobs programados con delay, retry, dead letter queue, monitorización y la
estrategia de migración de Bull (desarrollo local) a Cloud Tasks (producción GCP).

## Referencias disponibles

Lee el archivo correspondiente cuando necesites profundidad en un área específica:

- `references/setup-and-config.md` — Instalación, BullModule, Redis, configuración por entorno
- `references/producers.md` — Servicios que encolan jobs: QueueService, addJob, delayed jobs
- `references/processors.md` — Workers: @Processor, @Process, manejo de errores, eventos de cola
- `references/reminder-pattern.md` — Patrón completo de recordatorio de cumpleaños (Algoritmo 3 HADA)
- `references/notification-pattern.md` — Cola de notificaciones FCM con retry y token cleanup
- `references/cloud-tasks-migration.md` — Migración de Bull a GCP Cloud Tasks en producción

---

## Cuándo usar cada referencia

| Tarea                                                  | Referencia                 |
| ------------------------------------------------------ | -------------------------- |
| Configurar Bull/BullMQ por primera vez en el proyecto  | `setup-and-config.md`      |
| Crear un servicio que añade jobs a la cola             | `producers.md`             |
| Implementar el worker que procesa los jobs             | `processors.md`            |
| Implementar Algoritmo 3 (recordatorios de cumpleaños)  | `reminder-pattern.md`      |
| Implementar envío asíncrono de notificaciones push FCM | `notification-pattern.md`  |
| Configurar Cloud Tasks para producción en GCP          | `cloud-tasks-migration.md` |

---

## Reglas críticas (siempre en contexto)

### 1. Bull para desarrollo, Cloud Tasks para producción

```typescript
// La lógica del job es la misma; solo cambia el mecanismo de scheduling
// Ver references/cloud-tasks-migration.md para la estrategia de abstracción
```

### 2. Jobs idempotentes — deben poder ejecutarse más de una vez sin efectos secundarios

```typescript
// ✅ Siempre verificar el estado actual antes de ejecutar
async processReminder(job: Job<ReminderJobData>) {
  const profile = await this.profileRepo.findById(job.data.profileId);
  // Si ya se procesó o fue cancelado, salir silenciosamente
  if (!profile || profile.reminderScheduledAt?.getTime() !== job.data.scheduledAt) {
    return; // Job obsoleto (fue reprogramado), ignorar
  }
  await this.sendNotification(profile);
}
```

### 3. Un job por (profileId + año) para evitar duplicados de recordatorio

```typescript
// jobId determinístico: si ya existe, Bull lo reemplaza
const jobId = `reminder:${profileId}:${year}`;
await this.queue.add(jobData, { jobId, delay, removeOnComplete: true });
```

### 4. Nunca bloquear el event loop en un processor — todo async/await

```typescript
// ❌ Operación síncrona larga en processor
@Process('send-notification')
handle(job: Job) {
  const result = someSyncHeavyOperation(); // Bloquea el worker
}

// ✅ Todo asíncrono
@Process('send-notification')
async handle(job: Job) {
  const result = await someAsyncOperation();
}
```

### 5. Retry con backoff exponencial — nunca retry inmediato

```typescript
await queue.add(data, {
  attempts: 3,
  backoff: { type: 'exponential', delay: 1000 }, // 1s, 5s, 25s
});
```

---

## Fuentes y documentación oficial

- **BullMQ Docs**: https://docs.bullmq.io/
- **Bull Docs (legacy, compatible)**: https://github.com/OptimalBits/bull/blob/master/REFERENCE.md
- **@nestjs/bull Docs**: https://docs.nestjs.com/techniques/queues
- **BullMQ + NestJS Guide**: https://docs.bullmq.io/patterns/nestjs
- **GCP Cloud Tasks Docs**: https://cloud.google.com/tasks/docs
- **Cloud Tasks + NestJS**: https://cloud.google.com/tasks/docs/creating-http-target-tasks
- **Bull Board (dashboard)**: https://github.com/felixmosh/bull-board
- **Redis Docs**: https://redis.io/docs/
