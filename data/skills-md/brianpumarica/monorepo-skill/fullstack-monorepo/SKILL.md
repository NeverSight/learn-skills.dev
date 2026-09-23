---
name: fullstack-monorepo
description: Estándar y runbook para monorepos full-stack en Docker — auditar, scaffoldear y refactorizar el repo (compose dev/prod, Dockerfiles multi-stage non-root, entrypoint con espera de base, hot-reload en contenedores, SPA routing) y desplegarlo con GitHub Actions a Vercel más un runner self-hosted. Usar cuando el pedido toque docker-compose, Dockerfile, entrypoint, deploy.yml, o el estado real de lo que está corriendo en el servidor. Tres modos - analiza (auditoría y plan), ejecuta (implementación y eliminación de legacy), inspecciona (diagnóstico de sólo lectura del despliegue).
---

# Fullstack Monorepo Standard & Scaffold Runbook

Este estándar proporciona un marco agnóstico, condicional y de grado de producción para crear, auditar y refactorizar monorrepos full-stack.

---

## 1. Modos de Invocación

`analiza`, `ejecuta` e `inspecciona` son **modos de esta skill**, no comandos registrados en el
host. Se piden como argumento al invocarla (`/fullstack-monorepo analiza`) o en lenguaje natural
("auditá el monorepo con el estándar"). El agente DEBE responder según el modo pedido:

> Si querés que aparezcan como slash commands propios en Claude Code, creá
> `.claude/commands/analiza.md` (y sus pares) con una línea que invoque esta skill en ese modo.
> Sin eso, `/analiza` suelto no resuelve a nada y `@fullstack-monorepo` no existe como sintaxis.

| Modo | Fase | Comportamiento Obligatorio del Agente |
| :--- | :--- | :--- |
| **`analiza`** | **Fase 1: Auditoría & Diagnóstico** | 1. Ejecuta el **Motor de Detección de Stack**.<br>2. Genera la **Matriz de Conformidad (Gap Analysis)** clasificando ítems en: ✅ Cumple, ⚠️ Desviación, ❌ Faltante Crítico, 🗑️ Legacy a Eliminar.<br>3. Aplica la **Regla de Cero Preguntas Obvias** (solo consulta dilemas no estándar).<br>4. Presenta el plan de acción listo para aprobación. |
| **`ejecuta`** | **Fase 2: Implementación & Erradicación** | 1. Aplica obligatoriamente el **Checklist de 6 Fases** para las tecnologías detectadas sin omitir entregables.<br>2. **Elimina proactivamente archivos legacy/anti-patrones**.<br>3. Ejecuta validaciones automáticas (`docker compose config`, lint, build).<br>4. Entrega el reporte de cambios completo. |
| **`inspecciona`** | **Fase 0: Inspección del Entorno Desplegado** *(solo lectura)* | 1. **Primero, el canal: ¿el pipeline llegó a correr alguna vez?** Dueño del repo vs. organización dueña del runner, etiquetas, historial de corridas y secrets cargados (ver [CI/CD §5.1](./references/ci-cd-deployment-pipeline.md)). Si nunca hubo un deploy exitoso, **no hay nada desplegado que inspeccionar** y el resto del catálogo sobra.<br>2. Recién entonces emite el **Catálogo de Diagnóstico** —comandos exclusivamente de lectura— para ejecutar en el servidor ([CI/CD §6](./references/ci-cd-deployment-pipeline.md)).<br>3. Interpreta la salida y reporta el **estado real**: inventario completo de contenedores del host, salud, recursos, versión desplegada y desvíos del entorno.<br>4. **No modifica absolutamente nada.** Lo que haya para corregir se lista y se espera aprobación explícita. |
| **(sin modo)** | **Modo Directo (All-in-One)** | Ejecuta el análisis y, si no existen dudas humanas ambiguas, **procede directamente a la ejecución exhaustiva** sin requerir confirmación intermedia. |

### Flujo recomendado

```
inspecciona   →   analiza   →   ejecuta   →   inspecciona
(el servidor)     (el repo)     (el repo)      (verificar)
```

1. **`inspecciona` antes de tocar el repo** — sólo si el proyecto se despliega en un servidor que
   ya hospeda otros. Devuelve puertos ocupados, disco disponible y contenedores vecinos: sin eso,
   los puertos se eligen a ciegas y la colisión aparece recién en el primer deploy.
2. **`analiza`** — auditoría del repositorio y plan de acción.
3. **`ejecuta`** — implementación del plan.
4. **`inspecciona` después del primer deploy** — confirma que lo que corre es lo que se cree que
   corre. Complementa la sonda de versión: el job en verde prueba que el pipeline corrió; esto
   prueba que el código llegó.

`analiza` y `ejecuta` miran el **repositorio** y son las dos mitades del mismo trabajo.
`inspecciona` mira el **servidor**: es otro eje, y por eso va antes y después, nunca en el medio.
El modo directo equivale a `analiza` + `ejecuta`, y **no** incluye inspección.

> **Dónde corre `inspecciona`:** en la máquina de desarrollo, como cualquier otro modo — el
> servidor no tiene agente. Los dos canales de trabajo están en
> [Deployment Environment Profile §3](./references/deployment-environment-profile.md).

---

## 2. Motor de Detección Condicional de Stack (*Stack-Aware Engine*)

La skill NO impone tecnologías que el proyecto no utiliza. En la fase de análisis, el agente detecta el stack activo y activa **únicamente** las directivas correspondientes de forma obligatoria:

| Tecnología Detectada | Indicador en el Proyecto | Directivas Obligatorias Activadas |
| :--- | :--- | :--- |
| **Docker / Compose** | Hay Dockerfiles o `docker-compose*.yml` | • `.gitattributes` con `eol=lf` para scripts Linux en Windows.<br>• `.dockerignore` raíz centralizado.<br>• `docker-compose.yml` (dev-first sin flags) y `docker-compose.prod.yml`. |
| **Node.js / TS (Backend)** | `package.json` en backend (Express / NestJS) | • Multi-stage con `node:22-alpine` y `USER node` non-root.<br>• **`postgresql-client` en la etapa `base`** — sin él no hay `pg_isready` y el arranque muere (receta §8.3).<br>• BuildKit cache mount: `/root/.npm` con npm, `/pnpm/store` con pnpm.<br>• `entrypoint.sh` idempotente con `pg_isready` y `exec "$@"`.<br>• Hot-reload con `tsx watch` + `CHOKIDAR_USEPOLLING=true`. |
| **Gestor de paquetes** | `package-lock.json` vs `pnpm-lock.yaml` | • **El lockfile manda** y define los comandos de instalación y poda. No migrar de gestor sin pedido explícito ([`workspace-tooling.md`](./references/workspace-tooling.md)). |
| **Layout del repo** | Apps en `apps/*` vs. en la raíz | • **Eje independiente del gestor**: define el `context` del build y las rutas de los `COPY`. Cualquier combinación es válida (npm con `apps/`, pnpm con apps en la raíz).<br>• Las recetas numeradas son combinaciones frecuentes, no un menú cerrado: si el repo cae entre dos, se toman los comandos de una y las rutas de la otra (recetas §0).<br>• El `.dockerignore` va junto a **cada** contexto de build. |
| **Python (Backend)** | `requirements.txt` o `pyproject.toml` | • Multi-stage con `python:3.12-slim` y `USER appuser` non-root.<br>• **`postgresql-client`** en la etapa `base` + `ENTRYPOINT` explícito (no sólo `CMD`).<br>• Virtualenv aislado `/opt/venv`.<br>• Hot-reload con `uvicorn --reload --reload-dir <carpeta de la app>`. |
| **Frontend SPA (Vite / React / Vue)** | `vite.config.ts` o index.html cliente | • `frontend/nginx.conf` con `try_files $uri $uri/ /index.html;` y Gzip.<br>• `frontend/vercel.json` con rewrites para SPA.<br>• Servidor final ultra-ligero `nginx:alpine` (<10MB RAM). |
| **Frontend SSR (Next.js)** | `next.config.js/ts` | • `output: 'standalone'` en producción.<br>• Volumen anónimo `/app/.next` y `WATCHPACK_POLLING=true`.<br>• Inyección de variables `NEXT_PUBLIC_*` en build-time. |
| **Frontend Expo Web** | `app.json` / `eas.json` / dependencia `expo` | • Receta propia (**§7** de `dockerfile-recipes.md`). **No es Vite**: dev es `expo start --web`, build es `expo export -p web` — la salida sí es `dist/`, por eso la etapa de producción se comparte con SPA.<br>• Variables `EXPO_PUBLIC_*` en build-time (mismo mecanismo que `NEXT_PUBLIC_*`).<br>• Volumen anónimo `/app/.expo`.<br>• Si además compila a móvil (`android/`, `ios/`), **la web es un target más**: no migrar el proyecto a Vite para "cumplir el estándar".<br>• Al migrar de nativo a web, verificar módulo por módulo qué soporta realmente la implementación `.web.js`: varios no fallan, sólo hacen menos. |
| **PostgreSQL / Base de Datos** | SQL scripts, Prisma o Alembic | • Healthchecks activos con `pg_isready`.<br>• Volumen de datos nombrado persistente.<br>• Seeders seguros (variables de entorno, sin contraseñas hardcodeadas). |

---

## 3. Regla de Cero Preguntas Obvias (*No-Trivial Questions Rule*)

Para maximizar la autonomía y la velocidad, el agente DEBE aplicar este filtro estricto:

* 🚫 **PROHIBIDO PREGUNTAR (Decisiones pre-aprobadas por el estándar):**
  - "¿Quieres que consolide `docker-compose.dev.yml` en `docker-compose.yml`?" → **SÍ, la skill lo exige.**
  - "¿Deseas agregar `nginx.conf` o `vercel.json` para las rutas SPA?" → **SÍ, la skill lo exige.**
  - "¿Quieres usar Node 22 en lugar de Node 20?" → **SÍ, la skill lo exige.**
  - "¿Quieres crear `.gitattributes` para evitar CRLF en Windows?" → **SÍ, la skill lo exige.**
  - "¿Deseas ejecutar el backend como non-root?" → **SÍ, la skill lo exige.**
  - "¿Agrego rotación de logs al compose de producción?" → **SÍ, la skill lo exige.**
  - "¿Uso `gh` en vez de la web para el PR y para seguir el deploy?" → **SÍ, la skill lo exige.**

* ✅ **ÚNICAS PREGUNTAS PERMITIDAS (Dilemas arquitectónicos reales):**
  - Existencia de múltiples servicios que colisionan en responsabilidades.
  - Elección de proveedor de base de datos externa no documentada.
  - Secretos de entorno faltantes que impiden la inicialización.
  - Conservar el volumen de datos existente vs. reconstruir producción desde cero (decisión destructiva: la toma el dueño, nunca el agente).

---

## 4. Entorno de Despliegue del Operador (*Deployment Environment Profile*)

Hechos del entorno real donde se despliega: alcance y etiquetas del runner, canal de acceso al
servidor, host compartido o dedicado, exposición pública, almacén de `.env` y ruta de los
proyectos. El agente los da por ciertos y **no vuelve a preguntarlos**.

**La plantilla vacía está en
[`references/deployment-environment-profile.md`](./references/deployment-environment-profile.md).**
Se completa una vez por operador y se guarda en el `AGENTS.md` del proyecto —repositorio
privado—, nunca acá: esta skill es pública, y el dominio de la terminal web, el nombre del runner
y la ruta del almacén de secretos no son secretos pero sí son el mapa de la infra.

Lo único que el estándar fija sin importar el operador:

| Regla | Por qué |
| :--- | :--- |
| **Un `.env` por repositorio** en el almacén del servidor | Un archivo único se lo queda el primer proyecto y rompe a todos los demás (ci-cd §5.2) |
| **El repositorio tiene que estar bajo la organización dueña del runner** | Si el runner es de organización y el repo es personal, el job queda `Queued` para siempre y sin mensaje de error (ci-cd §5.1) |
| **`gh` es el canal de verificación preferido** | Antes que la web y antes que la terminal del servidor |
| **En host compartido, ningún comando `prune` ni `down` global** | Se lleva puestos los contenedores de los vecinos (perfil §2) |

---

## 5. Tabla de Erradicación de Anti-Patrones (*Legacy Eradication Matrix*)

Al ejecutar la refactorización, el agente DEBE eliminar activamente los siguientes anti-patrones:

| Anti-Patrón Heredado / Detectado | Acción Obligatoria de la Skill |
| :--- | :--- |
| **`docker-compose.dev.yml`** separado | **ELIMINAR / UNIFICAR DIRECTAMENTE en `docker-compose.yml`** para que `docker compose up -d` (cero flags) levante el entorno dev completo. |
| Scripts de CI/CD fragmentados (ej. `deploy-backend.yml` SSH aislado) | **REEMPLAZAR por `.github/workflows/deploy.yml`** con el pipeline dual completo (Vercel CLI + Pi Runner). |
| Dockerfile corriendo como `root` en producción | **MIGRAR OBLIGATORIAMENTE a `USER node` o `USER appuser`**. |
| Backend iniciando sin verificar disponibilidad de DB | **CREAR OBLIGATORIAMENTE `entrypoint.sh`** con bucle `pg_isready` y `exec "$@"`. |
| SPA sin configuración de servidor web | **CREAR OBLIGATORIAMENTE `nginx.conf` y `vercel.json`** para evitar errores 404 al recargar rutas. |
| Repositorio sin control de saltos de línea | **CREAR OBLIGATORIAMENTE `.gitattributes`** con `eol=lf`. |
| **Seeder que borra o sobrescribe datos** (`deleteMany`, `update` no vacío) | **REDUCIR a crear únicamente lo que falta.** El entrypoint corre en **cada** arranque del contenedor, producción incluida. |
| Cadena de fallback del entorno que termina en `.env.example` | **ELIMINAR ese último fallback.** Levantar producción con credenciales de desarrollo es peor que no levantarla: el deploy debe fallar ruidoso. |
| Comando de migraciones con `\|\| true` | **QUITAR el `\|\| true`**: abortar el arranque en lugar de servir la app contra un schema desactualizado. |
| Dev y prod generando el **mismo nombre de imagen** | **NOMBRAR distinto por entorno.** Levantar producción sin `--build` puede dejar corriendo la imagen de desarrollo. |
| Workflow de deploy que termina en `docker compose ps` | **AGREGAR verificación post-deploy** (contenedores `healthy` + smoke test al endpoint de salud) y hacer fallar el job si no pasa. |
| Job de CI que no despliega nada pero corre en cada push | **ELIMINARLO.** |
| Compose de producción sin rotación de logs | **AGREGAR `logging` con `max-size` / `max-file`** en todos los servicios: en un host compartido, un proyecto sin rotación llena el disco de todos. |
| **Imagen con `entrypoint.sh` que llama a `pg_isready` sin `postgresql-client` instalado** | **AGREGAR `postgresql-client` a la etapa `base`.** El binario no viene en `node:*-alpine` ni en `python:*-slim`: el arranque agota los reintentos y el log culpa a la base de un paquete faltante. |
| **Entrypoint con rutas relativas al `WORKDIR`** en un monorepo | **ANCLAR a la ubicación del script** (`APP_DIR` derivado de la ruta del propio script). Con `WORKDIR /app` y la app en `/app/apps/api`, ningún `if` matchea: migraciones y seed se saltean **en silencio**. |
| Cualquier `\|\| true` en el build (`cp`, `tsc`, `prisma generate`) | **QUITARLO.** Convierte un build roto en una imagen incompleta que sólo se descubre como crash-loop, semanas después. |
| Compose de **producción** publicando el puerto de Postgres al host | **QUITAR el `ports:` de la base.** El backend llega por la red interna; publicarlo expone la base a todo el host y colisiona con el Postgres de los vecinos. |
| Recetas pnpm/workspaces aplicadas a un repo con `package-lock.json` | **USAR LOS COMANDOS DEL LOCKFILE** (`dockerfile-recipes.md` §0). Migrar de gestor de paquetes —o de layout— sin pedido explícito es ruido, no cumplimiento. |
| Nombres genéricos de contenedor, imagen o volumen (`database`, `pgdata`, `backend`) en un host compartido | **PREFIJAR POR PROYECTO.** Los nombres de Docker son un espacio compartido en todo el host: dos proyectos que elijan `database` se pisan, y el segundo en desplegar gana sin avisar (`docker-compose-recipes.md` §0.1). |
| Variables con nombre propio en vez del contrato (`HOST_PORT_BACKEND`, `API_PORT`… en lugar de `BACKEND_HOST_PORT`) | **RENOMBRAR AL CONTRATO** (`docker-compose-recipes.md` §0). Los nombres son fijos en todos los repositorios; sólo los valores cambian. Un sinónimo no rompe de forma visible: cae al default y el smoke test prueba un puerto que nadie usa, con el job en verde. |
| `healthcheck` apuntando a `localhost` **dentro** del contenedor | **USAR `127.0.0.1`.** `localhost` resuelve a `::1` y la app escucha en IPv4: el contenedor queda `unhealthy` para siempre con la app perfectamente sana, y el deploy falla en cada corrida (`docker-compose-recipes.md` §4.7). |
| Subdominio anidado con punto (ej. `api.<proyecto>.<dominio>`) | **USAR SIEMPRE GUION (`api-<proyecto>.<dominio>`)**: Cloudflare Universal SSL solo cubre un nivel (`*.<dominio>`); dos puntos causan fallo de handshake TLS (`SEC_E_ILLEGAL_MESSAGE`). |
| Clonar repositorio manualmente en `~/Documents` del servidor | **ELIMINAR ESTA PRÁCTICA**: el runner ya clona en `actions-runner/_work/<repo>/<repo>`. Clonar a mano duplica espacio en la tarjeta SD y desincroniza código. |

---

## 6. Golden Monorepo Directory Layout

```
<project-root>/
├── .github/
│   └── workflows/
│       └── deploy.yml           # Pipeline Dual: Vercel CLI (Frontend) + Pi Runner (Backend)
├── .agents/
│   └── skills/                  # Skills locales del workspace
├── apps/ (o backend / frontend)
│   ├── api/                     # Backend (NestJS / Express / FastAPI)
│   │   ├── Dockerfile           # Multi-stage, Node 22 / Python 3.12, non-root
│   │   └── entrypoint.sh        # DB readiness & startup runner
│   └── web/                     # Frontend (Next.js / Vite / React)
│       ├── Dockerfile           # Multi-stage, Nginx Alpine / Standalone
│       ├── nginx.conf           # Requerido para SPAs (Gzip + SPA Routing)
│       └── vercel.json          # Requerido para despliegues Vercel SPA
├── packages/ (opcional)
│   ├── types/                   # Interfaces TypeScript y esquemas Zod compartidos
│   └── tsconfig/                # Configuraciones base de TypeScript
├── docs/
│   ├── architecture.md          # Diagramas de flujo y topología de contenedores
│   ├── api-reference.md         # Endpoints, autenticación y payloads
│   └── deployment.md            # Guía Raspberry Pi + Cloudflare Tunnel + Vercel
├── docker/
│   └── init-db.sql              # Extensiones y esquema inicial de base de datos
├── .dockerignore                # Reglas centralizadas de exclusión
├── .env.example                 # Plantilla documentada sin secretos reales
├── .gitattributes               # Forzado de saltos LF para scripts Linux (*.sh, *.sql)
├── .gitignore                   # Ignorados exhaustivos (Node, Docker, Vercel, Turbo)
├── AGENTS.md                    # Matriz de puertos y directrices para agentes IA
├── docker-compose.yml           # DEV-FIRST por defecto (DB + Back Dev + Front Dev)
├── docker-compose.prod.yml      # PROD optimizado (Zero source mounts, non-root, restart)
├── package.json                 # Scripts raíz de orquestación (npm run docker:dev, etc.)
└── README.md                    # Guía de inicio rápido para desarrolladores
```

### Variante con las apps en la raíz (igual de válida)

**El layout no se migra.** Un repo con las apps en la raíz cumple el estándar igual que uno con
`apps/`: cambia el `context` del build y las rutas de los `COPY`, nada más. Y el layout es
**independiente del gestor de paquetes** — hay repos con npm y `apps/`, y con pnpm y las apps en
la raíz. Ver `dockerfile-recipes.md` §0, que separa los dos ejes.

```
<project-root>/
├── backend/                     # manifiesto y lockfile propios
│   ├── Dockerfile               # context: ./backend
│   ├── entrypoint.sh
│   └── .dockerignore
├── frontend/                    # manifiesto y lockfile propios
│   ├── Dockerfile               # context: ./frontend
│   ├── nginx.conf
│   ├── vercel.json
│   └── .dockerignore
└── (idéntico al de arriba de acá para abajo: docker/, docs/, compose, .env.example, ...)
```

El `.dockerignore` va **junto a cada contexto de build**: uno en la raíz sirve para `context: .`,
pero es invisible para `context: ./backend`.

---

## 7. Checklist de Implementación Mandatoria (6 Fases)

Al recibir `/fullstack-monorepo /ejecuta` (o tras la aprobación de `/analiza`), el agente DEBE ejecutar ordenadamente:

### Fase 1: Normalización de Raíz
- [ ] Crear `.gitattributes` con `*.sh text eol=lf`, `*.sql text eol=lf`, `Dockerfile* text eol=lf`.
- [ ] Crear `.dockerignore` raíz y `.dockerignore` en backend.
- [ ] Actualizar `.gitignore` para monorrepos (Vercel, Turbo, logs, data).
- [ ] Crear `package.json` raíz con scripts de orquestación (`docker:dev`, `docker:prod`, `docker:down`, `docker:logs`).

### Fase 2: Orquestación Docker Compose
- [ ] Consolidar stack de desarrollo en `docker-compose.yml` (dev-first con cero flags).
- [ ] Eliminar cualquier archivo legacy redundante (`docker-compose.dev.yml`).
- [ ] Generar `docker-compose.prod.yml` con imágenes de producción, healthchecks y reinicio `unless-stopped`.

### Fase 3: Backend Hardening
- [ ] Elegir la receta por **lockfile y layout** (`dockerfile-recipes.md` §0): npm → §2/§5, pnpm+workspaces → §1/§4.
- [ ] Crear `entrypoint.sh` ejecutable, anclado con `APP_DIR` y con `exec "$@"` (`database-lifecycle.md` §1).
- [ ] **Instalar `postgresql-client` en la etapa `base` del Dockerfile** — es lo que provee `pg_isready`; sin él el contenedor no arranca.
- [ ] Configurar `Dockerfile` multi-stage (Node 22 / Python 3.12, `USER node` / `USER appuser`, BuildKit cache) — con `ENTRYPOINT` explícito **también en Python**.
- [ ] Verificar la imagen construida antes de confiar en ella (`dockerfile-recipes.md` §8.2).
- [ ] Configurar hot-reload con polling (`CHOKIDAR_USEPOLLING=true` en el servicio de backend del compose, no sólo documentado).

### Fase 4: Frontend Production Readiness
- [ ] Crear `frontend/nginx.conf` con `try_files $uri $uri/ /index.html;` y compresión gzip.
- [ ] Crear `frontend/vercel.json` con rewrites para Vercel.
- [ ] Configurar `frontend/Dockerfile` multi-stage con `nginx:alpine` para producción.

### Fase 5: CI/CD Pipeline Dual
- [ ] Crear/Unificar `.github/workflows/deploy.yml` (Job 1: Vercel CLI Frontend + Job 2: Raspberry Pi / Servidor Docker con `--force-recreate`).
- [ ] Eliminar workflows de despliegue fragmentados u obsoletos.
- [ ] Confirmar que el repositorio está **bajo la organización dueña del runner**.
- [ ] Crear el `.env` del servidor en su **carpeta por repositorio** (`/home/github-runner/env-backups/<repo>/.env`, `600`, dueño `github-runner`; verificar con `sudo`).
- [ ] Backend con `healthcheck` propio en `docker-compose.prod.yml` (§4.6 de `docker-compose-recipes.md`).
- [ ] Secrets de Vercel/Pi verificados contra el proyecto/servidor real, no copiados a ciegas de una nota guardada.
- [ ] Agregar el paso de **verificación post-deploy**: contenedores `healthy` + smoke test al endpoint de salud, con el job fallando si no pasa.

### Fase 6: Documentación y Agentes
- [ ] Generar `docs/architecture.md`, `docs/deployment.md` y `docs/api-reference.md`.
- [ ] Actualizar `AGENTS.md` con la matriz activa de puertos y registro de skills.
- [ ] Actualizar `README.md` con la guía de inicio rápido.
- [ ] Validar sintaxis con `docker compose config` y tests de compilación.

---

## 8. Matriz de Hot-Reloading Multiplataforma

Para evitar fallos de detección de archivos en montajes de volumen host (Windows / WSL / macOS):

| Framework / Tool | Archivo Clave | Configuración Mandatoria |
| :--- | :--- | :--- |
| **Vite** (React / Vue) | `vite.config.ts` | `server: { host: '0.0.0.0', watch: { usePolling: true, interval: 100 } }` |
| **Next.js** | `docker-compose.yml` | `environment: [WATCHPACK_POLLING=true]` + volumen anónimo `/app/.next` |
| **Express / TS** | `docker-compose.yml` | `environment: [CHOKIDAR_USEPOLLING=true]` + `"dev": "tsx watch src/index.ts"` |
| **NestJS / TS** | `nodemon.json` | `{"watch": ["src"], "ext": "ts", "legacyWatch": true, "exec": "nest start"}` |
| **Expo Web** | `docker-compose.yml` | `environment: [CHOKIDAR_USEPOLLING=true]` + volumen anónimo `/app/.expo` + `expo start --web --host lan` |
| **FastAPI / Python** | `docker-compose.yml` | `uvicorn main:app --host 0.0.0.0 --reload --reload-dir <carpeta de la app>` |

---

## 9. Referencias Detalladas y Companion Skills

Para plantillas de código listas para usar:
- [Dockerfile Recipes](./references/dockerfile-recipes.md) — **§0 elige la receta por lockfile y layout** (npm y pnpm), §7 trae las trampas de build verificadas
- [Docker Compose Recipes](./references/docker-compose-recipes.md) — **§0 es el contrato de nombres** entre compose, `.env` y workflow; §4 el endurecimiento obligatorio de producción
- [Database Lifecycle & Entrypoint](./references/database-lifecycle.md) — **reglas innegociables del arranque** (§0), el `entrypoint.sh` de referencia (§1) y cómo **traer un volcado desde un servidor sin SSH** (§7)
- [CI/CD Deployment Pipeline (GitHub Actions + Vercel CLI + Pi Runner)](./references/ci-cd-deployment-pipeline.md) — incluye el **Catálogo de Diagnóstico** del modo `inspecciona` (§6), la operación con `gh` (§7) y la sonda de versión (§8)
- [Deployment Environment Profile](./references/deployment-environment-profile.md) — plantilla del perfil del operador y reglas de host compartido
- [Workspace Tooling (pnpm + Turbo)](./references/workspace-tooling.md) — **opcional**: sólo si el proyecto ya usa esas herramientas
- [AGENTS.md Standard Template](./references/agents-md-template.md)

### Companion Skills Coordinadas:
- [`cloudflare-tunnel`](../cloudflare-tunnel/SKILL.md): Exposición segura con Zero Trust y SSL sin abrir puertos de router.
- [`vercel-monorepo-deploy`](../vercel-monorepo-deploy/SKILL.md): Despliegue de frontend monorrepo con Vercel CLI y `turbo-ignore`.
- [`docker-hardening`](../docker-hardening/SKILL.md): Seguridad de contenedores (`USER node`, `cap_drop: [ALL]`, healthchecks).
- [`turborepo-orchestration`](../turborepo-orchestration/SKILL.md): Pipelines de Turbo, filtros y remote caching.
- [`prisma-database`](../prisma-database/SKILL.md) / [`fastapi-backend`](../fastapi-backend/SKILL.md) / [`nestjs-backend`](../nestjs-backend/SKILL.md): Especializaciones por tecnología.

> Estos enlaces resuelven dentro de este repositorio. Si instalaste **sólo** `fullstack-monorepo`
> (`npx skills add <repo> --skill fullstack-monorepo`), las companion no están en tu máquina y los
> enlaces no abren nada: instalá las que necesites o ignorá la sección.
