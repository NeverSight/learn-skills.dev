---
name: watchdog_supervisor
description: Supervisor de procesos que reinicia workers muertos, detecta zombies y escala segun carga del pipeline KYC
type: Tool
priority: Recomendada
mode: Self-hosted
---

# watchdog_supervisor

Skill para implementar un supervisor de procesos (watchdog) que monitoriza continuamente los workers del pipeline de verificacion de identidad KYC. Detecta procesos muertos o zombies, reinicia automaticamente workers fallidos, y escala el numero de workers segun la carga actual del pipeline. Opera como una capa de resiliencia adicional por encima de Kubernetes, enfocada en la logica de negocio del pipeline de verificacion y la salud de los procesos de inferencia ML.

## When to use

Utilizar esta skill cuando el health_monitor_agent necesite implementar supervisio a nivel de proceso dentro de los contenedores del pipeline KYC. Es critica cuando los workers de inferencia ML se cuelgan sin terminar (proceso zombie con GPU reservada), cuando se necesita escalado rapido de workers dentro de un pod (multiprocessing), o cuando Kubernetes no puede detectar fallos sutiles que no se manifiestan en las probes HTTP.

## Instructions

1. Crear la clase base del supervisor watchdog con registro de workers y heartbeat:
```python
import asyncio
import psutil
import signal
import time
from dataclasses import dataclass, field
from typing import Dict, Optional
from enum import Enum

class WorkerState(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    ZOMBIE = "zombie"
    UNRESPONSIVE = "unresponsive"

@dataclass
class WorkerInfo:
    pid: int
    name: str
    started_at: float
    last_heartbeat: float
    state: WorkerState = WorkerState.RUNNING
    restart_count: int = 0

class WatchdogSupervisor:
    def __init__(self, heartbeat_timeout: float = 30.0, max_restarts: int = 5):
        self.workers: Dict[str, WorkerInfo] = {}
        self.heartbeat_timeout = heartbeat_timeout
        self.max_restarts = max_restarts
        self._running = False
```

2. Implementar el registro y arranque de workers para cada componente del pipeline:
```python
import multiprocessing as mp

class WatchdogSupervisor:
    # ...continuacion
    def register_worker(self, name: str, target_fn, args=()) -> WorkerInfo:
        process = mp.Process(target=target_fn, args=args, name=name, daemon=True)
        process.start()
        worker = WorkerInfo(
            pid=process.pid,
            name=name,
            started_at=time.monotonic(),
            last_heartbeat=time.monotonic(),
        )
        self.workers[name] = worker
        logger.info(f"Worker '{name}' started with PID {process.pid}")
        return worker

    # Ejemplo de uso para pipeline KYC
    supervisor = WatchdogSupervisor(heartbeat_timeout=30, max_restarts=5)
    supervisor.register_worker("face_match_worker_0", face_match_inference_loop)
    supervisor.register_worker("ocr_worker_0", ocr_processing_loop)
    supervisor.register_worker("liveness_worker_0", liveness_detection_loop)
```

3. Implementar deteccion de procesos zombie y workers no responsivos:
```python
    async def check_worker_health(self, worker: WorkerInfo) -> WorkerState:
        try:
            proc = psutil.Process(worker.pid)
            status = proc.status()

            if status == psutil.STATUS_ZOMBIE:
                logger.warning(f"Worker '{worker.name}' (PID {worker.pid}) is zombie")
                return WorkerState.ZOMBIE

            time_since_heartbeat = time.monotonic() - worker.last_heartbeat
            if time_since_heartbeat > self.heartbeat_timeout:
                logger.warning(
                    f"Worker '{worker.name}' unresponsive for {time_since_heartbeat:.1f}s"
                )
                return WorkerState.UNRESPONSIVE

            # Verificar uso de memoria excesivo (posible memory leak)
            mem_info = proc.memory_info()
            if mem_info.rss > 8 * 1024 * 1024 * 1024:  # 8GB
                logger.warning(f"Worker '{worker.name}' memory usage: {mem_info.rss / 1e9:.1f}GB")
                return WorkerState.UNRESPONSIVE

            return WorkerState.RUNNING

        except psutil.NoSuchProcess:
            return WorkerState.STOPPED
```

4. Implementar reinicio automatico de workers con backoff y limite de reintentos:
```python
    async def restart_worker(self, name: str, target_fn, args=()):
        worker = self.workers.get(name)
        if not worker:
            return

        if worker.restart_count >= self.max_restarts:
            logger.error(
                f"Worker '{name}' exceeded max restarts ({self.max_restarts}). "
                "Marking as permanently failed."
            )
            worker.state = WorkerState.STOPPED
            await self.notify_permanent_failure(name)
            return

        # Terminar proceso existente si aun esta vivo
        await self._kill_process(worker.pid)

        # Backoff exponencial entre reintentos
        backoff = min(2 ** worker.restart_count, 30)
        logger.info(f"Restarting worker '{name}' in {backoff}s (attempt {worker.restart_count + 1})")
        await asyncio.sleep(backoff)

        new_process = mp.Process(target=target_fn, args=args, name=name, daemon=True)
        new_process.start()
        worker.pid = new_process.pid
        worker.restart_count += 1
        worker.last_heartbeat = time.monotonic()
        worker.state = WorkerState.RUNNING

    async def _kill_process(self, pid: int):
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except psutil.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)
        except psutil.NoSuchProcess:
            pass
```

5. Implementar el heartbeat que los workers envian al supervisor via shared memory o Redis:
```python
import redis

class WorkerHeartbeat:
    """Cada worker usa esta clase para reportar su heartbeat."""
    def __init__(self, worker_name: str, redis_client: redis.Redis):
        self.worker_name = worker_name
        self.redis = redis_client

    def beat(self):
        self.redis.set(
            f"watchdog:heartbeat:{self.worker_name}",
            time.time(),
            ex=60  # TTL de 60 segundos
        )

    def report_busy(self, task_id: str):
        self.redis.hset(f"watchdog:status:{self.worker_name}", mapping={
            "state": "busy",
            "task_id": task_id,
            "since": time.time(),
        })

# Dentro del worker de inferencia
heartbeat = WorkerHeartbeat("face_match_worker_0", redis_client)
while True:
    task = queue.get()
    heartbeat.report_busy(task.id)
    result = process_face_match(task)
    heartbeat.beat()
```

6. Implementar escalado dinamico de workers basado en la profundidad de la cola:
```python
    async def auto_scale_workers(self, queue_name: str, target_fn,
                                  min_workers: int = 2, max_workers: int = 8,
                                  scale_threshold: int = 10):
        queue_depth = int(self.redis.llen(queue_name))
        current_workers = self._count_active_workers(target_fn.__name__)

        desired = min(max(queue_depth // scale_threshold + min_workers, min_workers), max_workers)

        if desired > current_workers:
            for i in range(current_workers, desired):
                name = f"{target_fn.__name__}_{i}"
                self.register_worker(name, target_fn)
                logger.info(f"Scaled up: started worker '{name}' (queue_depth={queue_depth})")
        elif desired < current_workers and current_workers > min_workers:
            for i in range(desired, current_workers):
                name = f"{target_fn.__name__}_{i}"
                await self.graceful_shutdown_worker(name)
                logger.info(f"Scaled down: stopped worker '{name}' (queue_depth={queue_depth})")
```

7. Implementar el bucle principal del supervisor que ejecuta todas las verificaciones periodicamente:
```python
    async def run(self, check_interval: float = 5.0):
        self._running = True
        logger.info("Watchdog supervisor started")
        while self._running:
            for name, worker in list(self.workers.items()):
                state = await self.check_worker_health(worker)
                worker.state = state

                if state in (WorkerState.ZOMBIE, WorkerState.STOPPED, WorkerState.UNRESPONSIVE):
                    logger.warning(f"Worker '{name}' state: {state}. Initiating restart.")
                    await self.restart_worker(name, self._worker_targets[name])

            # Auto-scaling check
            await self.auto_scale_workers("kyc:face_match:queue", face_match_inference_loop)
            await self.auto_scale_workers("kyc:ocr:queue", ocr_processing_loop)

            await asyncio.sleep(check_interval)
```

8. Exponer metricas del supervisor para Prometheus:
```python
from prometheus_client import Gauge, Counter

workers_active = Gauge("watchdog_workers_active", "Active workers", ["service"])
workers_restarts = Counter("watchdog_worker_restarts_total", "Worker restarts", ["service"])
workers_zombies = Counter("watchdog_zombies_detected_total", "Zombie processes detected", ["service"])

# Dentro del check loop
workers_active.labels(service="face_match").set(count_active("face_match"))
workers_restarts.labels(service=name).inc()
```

## Notes

- El heartbeat timeout debe ser al menos 2x el tiempo maximo de inferencia esperado; para face matching con ArcFace el timeout recomendado es 30 segundos, para OCR con PaddleOCR es 45 segundos, para evitar falsos positivos durante procesamiento de imagenes complejas.
- Cuando un worker alcanza el maximo de reintentos (max_restarts), el supervisor debe notificar al health_monitor_agent via metrica Prometheus y no intentar mas reinicios para evitar ciclos de fallo; la intervencion manual o el reinicio del pod completo por Kubernetes es la accion correcta.
- El supervisor debe ejecutarse como proceso principal (PID 1) dentro del contenedor Docker y propagar senales SIGTERM/SIGINT a todos los workers hijos para un apagado graceful durante rolling updates de Kubernetes.
