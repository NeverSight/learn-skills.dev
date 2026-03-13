---
name: docker_docker_compose
description: Contenerización de todos los servicios y entorno de desarrollo local reproducible con Docker Compose
type: Tool
priority: Esencial
mode: Self-hosted
---

# docker_docker_compose

Docker garantiza que el entorno de desarrollo, CI y producción ejecutan exactamente el mismo código con las mismas dependencias. Docker Compose orquesta todos los servicios localmente con un solo comando.

## When to use

Usar desde el día 0. Ningún desarrollador debe ejecutar servicios fuera de Docker — el objetivo es "funciona en mi máquina" siendo el mismo entorno que producción.

## Instructions

1. Estructura de `docker-compose.yml` para el sistema KYC:
   ```yaml
   version: "3.9"
   services:
     kyc-api:
       build: ./backend
       environment:
         - DATABASE_URL=postgresql+asyncpg://kyc:secret@pgbouncer:5432/kyc
         - REDIS_URL=redis://redis:6379/0
       depends_on: [postgres, redis, minio]
     postgres:
       image: postgres:16-alpine
       volumes: [postgres_data:/var/lib/postgresql/data]
     redis:
       image: redis:7-alpine
       command: redis-server --save 60 1
     minio:
       image: minio/minio:latest
       command: server /data
     nginx:
       image: openresty/openresty:alpine
       ports: ["443:443", "80:80"]
       volumes: [./nginx:/etc/nginx/conf.d]
   volumes:
     postgres_data:
   ```
2. Dockerfile multi-stage para el backend:
   ```dockerfile
   FROM python:3.11-slim AS builder
   COPY requirements.txt .
   RUN pip install --user -r requirements.txt
   FROM python:3.11-slim
   COPY --from=builder /root/.local /root/.local
   COPY ./backend /app
   WORKDIR /app
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```
3. Dockerfile separado para workers con GPU (CUDA): `FROM nvidia/cuda:12.0-runtime-ubuntu22.04`.
4. Variables de entorno en `.env` (nunca commitear a Git). Usar `.env.example` con valores de placeholder.
5. `make up` = `docker compose up -d --build`. `make down` = `docker compose down -v`.
6. Healthchecks en cada servicio para que `depends_on` espere a que estén listos.

## Notes

- Usar `docker compose --profile gpu` para servicios que requieren GPU, omitirlos en CI/CD sin GPU.
- El `docker-compose.override.yml` permite configuraciones locales que no se commitean.
- En producción, Kubernetes sustituye a Docker Compose — pero los mismos Dockerfiles se usan en ambos entornos.