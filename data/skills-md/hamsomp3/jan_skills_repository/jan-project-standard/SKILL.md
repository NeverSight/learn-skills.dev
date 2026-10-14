---
name: jan-project-standard
description: "Estandariza proyectos personales y académicos con las convenciones de Jan Polanco Velasco: Python con uv/Astral (3.13+), src-layout, Ruff, pre-commit, Makefile, pytest, CONSTITUTION.md como fuente única de verdad, Conventional Commits, README con badges, licencia MIT, gobernanza GitHub (PR/issue templates, CI, Dependabot, labels), contexto para agentes (AGENTS.md, .opencode/, tgrep), identidad Git automática (includeIf; perfil Jan o perfil propio en macOS/Windows) y diagramas de arquitectura con Archify. Úsala al crear o estandarizar un repo, redactar un CONSTITUTION.md, configurar uv/Ruff/pre-commit/CI, añadir un Makefile o README, configurar la identidad Git automática, generar un diagrama con Archify, o conectar el proyecto a GitHub. Use when scaffolding a Python repository, writing a CONSTITUTION.md, setting up uv, Ruff, pre-commit or CI, configuring automatic Git identity, generating an Archify diagram, or standardizing a project."
license: MIT
compatibility: Requiere Python 3 (el scaffolder usa solo la biblioteca estándar). Para aplicar el estándar al proyecto destino se recomienda uv, git y, opcionalmente, gh.
metadata:
  author: Jan Polanco Velasco
  version: "1.0"
  homepage: https://github.com/hamsomp3/jan_skills_repository
---

# Estándar de proyectos — Jan Polanco Velasco

Este skill encapsula **cómo se construyen y gobiernan los proyectos** de Jan: una forma
de trabajar repetible, reproducible y auditable que ya está aplicada en decenas de
repositorios personales y académicos.

> **Filosofía central:** todo lo que vive dentro de la carpeta del proyecto tiene una
> instrucción escrita. El documento que la contiene es **`CONSTITUTION.md`**, la
> **fuente única de verdad**. Un proyecto sano es un proyecto donde un agente (o una
> persona) puede leer la constitución y operar sin adivinar.

---

## Cómo invocarlo (plantilla de prompt)

No hace falta memorizar comandos: describe tu caso en lenguaje natural. Estas son las
piezas que conviene incluir:

```text
@jan-project-standard

Soy:         Jan  |  NO soy Jan → aquí mi nombre y correo
Estado:      proyecto nuevo  |  proyecto existente (ya tiene README y/o CONSTITUTION.md)
Repo:        git@github.com:<usuario>/<repo>.git
Stack:       Python (uv) · ¿paquete o app? · ¿ty? · ¿Archify?
Objetivo:    crear desde cero  |  estandarizar SIN borrar  |  solo auditar  |  añadir X
Restricción: no elimines nada existente; mejora y completa.
```

**Reglas de convivencia (obligatorias):**

- En un proyecto existente: **primero leer, luego proponer, luego aplicar**. Nunca reemplaces
  archivos del usuario (README, `CONSTITUTION.md`, código) sin revisarlos.
- Si **no eres Jan**: no uses rutas ni repos fijos; aporta tus datos (ver "Identidad Git").
- Ante la duda, **audita** (`--audit`) y muestra el informe antes de tocar nada.

---

## Cuándo usar este skill

- Crear un proyecto o repositorio nuevo desde cero.
- Estandarizar un proyecto existente que no sigue el estándar.
- Redactar, poblar o actualizar un `CONSTITUTION.md`.
- Configurar `uv` + Ruff + pre-commit + Makefile + CI.
- Conectar un proyecto local a un repositorio de GitHub.
- Preparar un README profesional con badges, licencia y estructura.

## Cuándo NO usarlo

- Proyectos que ya tienen su propio estándar y el usuario **no** quiere adoptar este.
- Cambios triviales de una línea en un repo ya estandarizado (no re-scaffold).

---

## Las 10 reglas no negociables

1. **CONSTITUTION.md primero.** La constitución se crea al inicio y se **actualiza en el
   mismo commit** ante cualquier cambio arquitectónico, tecnológico o de proceso.
2. **`uv` manda.** Gestión de entornos y dependencias **solo** con `uv`. Prohibido `pip`
   y `requirements.txt`. Dependencias en `pyproject.toml`; `uv.lock` **sí se versiona**.
3. **Python 3.13+** fijado en `.python-version` y en `requires-python`.
4. **src-layout** (`src/<paquete>/`) con build backend `uv_build`, salvo apps simples
   (modo `--app`).
5. **Calidad automatizada:** Ruff (lint + formato), pre-commit y pytest. Nada se sube
   con `make check` en rojo. `--no-verify` está prohibido salvo causa documentada.
6. **Makefile como interfaz.** Todos los comandos del proyecto se exponen en targets
   (`make help` los lista). La paridad local ↔ CI es obligatoria: el CI corre lo mismo.
7. **Conventional Commits** (`feat:`, `fix:`, `docs:`, `refactor:`, `style:`, `test:`,
   `chore:`) en un solo idioma claro; descripciones en imperativo.
8. **GitHub gobernado:** plantilla de Pull Request, plantillas de issue, CI, Dependabot,
   labels declarativas y rama `main` protegida por PRs.
9. **README profesional:** badges, tabla de contenidos, stack, primeros pasos, estructura,
   arquitectura (opcional, con **Archify**), contribución y licencia.
10. **Identidad Git automática:** la carpeta de proyectos hereda nombre, correo y llave SSH
    vía `includeIf` en `~/.gitconfig`. **Perfil A** para Jan
    (`~/Desktop/Repositorios/personal/`); **Perfil B** para cualquier otro usuario (macOS o
    Windows), y **solo si lo pide** (ver [`references/git-identity.md`](references/git-identity.md)).

---

## Modo A — Crear un proyecto nuevo

### Paso 1 · Ejecutar el scaffolder

El scaffolder copia las plantillas, sustituye variables y deja el proyecto listo. Usa
solo la biblioteca estándar de Python (no requiere `uv` para ejecutarse):

```bash
python3 <SKILL_DIR>/scripts/new_project.py \
  --name "Nombre del Proyecto" \
  --path ./nombre-del-proyecto \
  --description "Descripción breve del proyecto." \
  --git
```

> La autoría y el owner se **deducen solos**: `--author`/`--email` salen de
> `git config user.name` / `user.email`, y `--owner` de `git config github.user`. Puedes
> sobreescribirlos con flags si quieres.

Opciones más usadas:

| Opción | Efecto |
|--------|--------|
| `--name` | Nombre legible del proyecto (obligatorio). |
| `--path` | Carpeta destino (por defecto `.`). |
| `--repo` | Nombre del repo en GitHub (por defecto, slug del nombre). |
| `--owner` | Cuenta/organización de GitHub (por defecto: `git config github.user` o `<usuario>`). |
| `--description` | Descripción de una línea (va al README, pyproject y constitución). |
| `--author` / `--email` | Autoría (por defecto: `git config user.name` / `user.email`). |
| `--python-version` | Versión de Python (por defecto `3.13`). |
| `--app` | Proyecto de aplicación (sin paquete ni build-system), en vez de src-layout. |
| `--minimal` | Solo lo esencial: sin `.github`, sin `AGENTS.md`/`.opencode`, sin extras. |
| `--archify` | Incluye la sección **Arquitectura del proyecto** (Archify) en el README y la fila en la constitución. |
| `--no-types` | Omite `ty` (tipado estático) de dependencias, Makefile y docs. |
| `--no-github` | No genera `.github/`. |
| `--no-agents` | No genera `AGENTS.md` ni `.opencode/`. |
| `--git` / `--no-git` | Inicializa el repositorio git (rama `main`). Por defecto: sí. |
| `--sync` | Ejecuta `uv sync` y `uv run pre-commit install` al terminar. |
| `--force` | Sobrescribe archivos existentes. |
| `--dry-run` | Muestra qué haría sin escribir nada. |
| `--audit` | **Solo audita** un proyecto existente (FALTA/DIFIERE/OK) sin escribir nada; infiere el contexto del repo. |

> ⚠️ **Antes de sobrescribir:** si la carpeta destino ya tiene archivos (sobre todo un
> `CONSTITUTION.md` o `README.md` propios), **no uses `--force` a ciegas**. Investiga,
> lee lo existente y fusiona en lugar de reemplazar.

### Paso 2 · Poblar la constitución

Abre `CONSTITUTION.md` y completa, como mínimo, las secciones marcadas con `<!-- ... -->`:

- **Propósito** y **no-propósito** (una o dos frases cada uno).
- **Alcance** (qué entra y qué no).
- **Stack técnico** (confirma o corrige la tabla).
- **Decisiones iniciales** en el historial (fecha + decisión + motivo).
- **Notas y tareas pendientes** (roadmap en formato checklist).

### Paso 3 · Verificar el entorno

```bash
cd nombre-del-proyecto
uv sync
uv run pre-commit install
make check     # lint + formato + pruebas
```

### Paso 4 · Conectar a GitHub

Crea el repositorio (si no existe) y publica:

```bash
gh repo create <tu-usuario>/<repo> --private --source=. --remote=origin --push
# o, si el repo ya existe:
git remote add origin git@github.com:<tu-usuario>/<repo>.git
git push -u origin main
```

Luego protege `main` y verifica que la CI esté en verde. Detalle en
[`references/github.md`](references/github.md).

### Paso 5 · Diagrama de arquitectura (opcional, Archify)

Si el proyecto necesita un mapa de arquitectura en el README (documentación viva), instala
la skill [Archify](https://github.com/tt-a1i/archify) y genera el diagrama:

```bash
npx skills add tt-a1i/archify -g
# Luego, en el chat:
#   "Analiza este repositorio y usa Archify para crear un diagrama de arquitectura de
#    runtime. 8–12 componentes, un camino principal, dependencias externas y límites."
```

El resultado queda en `docs/arquitectura.json` (fuente versionada) y `docs/arquitectura.html`
(artefacto interactivo), y se enlaza desde el README. **No** se edita el HTML a mano:
se regenera con `deliver`. Detalle completo en [`references/archify.md`](references/archify.md).

---

## Modo B — Mejorar un proyecto existente (no destructivo)

> **Contrato de no destrucción.** El objetivo no es reemplazar, es **completar y elevar**.
> Un repo con historia, `README.md` o `CONSTITUTION.md` propios es trabajo del usuario:
> se **lee, respeta y mejora**; nunca se borra ni se sobrescribe con `--force` a ciegas.

0. **Audita sin tocar nada** (captura el contexto del propio repo):
   ```bash
   python3 <SKILL_DIR>/scripts/new_project.py --path . --audit
   ```
   Lee `pyproject.toml`, `.python-version`, `CONSTITUTION.md` y el remoto de git, y reporta
   **FALTA / DIFIERE / OK**. `DIFIERE` puede ser personalización legítima: **revísala**.
1. **Lee** `README.md`, `CONSTITUTION.md` y la estructura real antes de cambiar nada.
2. **Propón** un plan (qué se añade, qué se completa) y aplícalo de forma **aditiva**:
   ```bash
   python3 <SKILL_DIR>/scripts/new_project.py --path . --name "..." --description "..."
   ```
   Sin `--force`, el scaffolder **omite** todo archivo que ya existe (solo crea lo que falta).
3. **Fusiona los `DIFIERE` a mano:** conserva el contenido del usuario y **añade** lo que
   falte (no reemplaces secciones; no borres lo propio).
4. **Migra** solo si el usuario lo pide: `requirements.txt` → `pyproject.toml` con `uv add`;
   scripts sueltos → `src/<paquete>/`; `.ipynb` → `.py`.
5. **Registra** el cambio en el historial de la constitución y verifica con `make check`.

> El `--audit` es la herramienta para "capturar más contexto": puedes correrlo las veces que
> quieras sin efectos secundarios, incluso en repos grandes, y mostrar el informe antes de
> proponer cambios.

---

## Manifiesto de archivos del estándar

| Archivo | Propósito |
|---------|-----------|
| `CONSTITUTION.md` | Fuente única de verdad: propósito, stack, estructura, convenciones, flujo y decisiones. |
| `README.md` | Puerta de entrada pública: badges, TOC, descripción, stack, primeros pasos, estructura, contribución, licencia. |
| `pyproject.toml` | Metadatos, dependencias (`uv`), configuración de Ruff y pytest. |
| `uv.lock` | Lockfile determinista (**versionado**). |
| `.python-version` | Versión de Python fijada (`3.13`). |
| `.gitignore` | Ignora venvs, cachés, secretos, artefactos pesados y datos. |
| `.editorconfig` | Convenciones de estilo entre editores. |
| `Makefile` | Interfaz de comandos (`help`, `install`, `dev`, `lint`, `format`, `test`, `check`, `clean`). |
| `.pre-commit-config.yaml` | Higiene de archivos + Ruff + `uv-lock` antes de cada commit. |
| `LICENSE` | MIT por defecto. |
| `CONTRIBUTING.md` | Entorno, ramas, estándares, commits y proceso de PR. |
| `CODE_OF_CONDUCT.md` | Contributor Covenant 2.1 (proyectos con colaboración). |
| `AGENTS.md` | Contexto para agentes LLM (stack, flujo, reglas, tgrep). |
| `.opencode/rules/tgrep.md` | Regla de búsqueda con `tgrep` para agentes en OpenCode. |
| `.github/pull_request_template.md` | Plantilla de PR (Conventional Commits + checklist). |
| `.github/ISSUE_TEMPLATE/` | Formularios de bug, funcionalidad e investigación (spike). |
| `.github/workflows/ci.yml` | CI: pre-commit + pruebas. |
| `.github/workflows/labels.yml` | Sincroniza labels desde `.github/labels.yml`. |
| `.github/labels.yml` | Fuente única de las etiquetas del repositorio. |
| `.github/dependabot.yml` | Actualización automática de dependencias (`uv` y Actions). |
| `src/<paquete>/` | Código del paquete (src-layout). |
| `tests/` | Pruebas con pytest (patrón AAA). |
| `docs/` | Documentación, ADRs, spikes e investigación. |
| `docs/arquitectura.{json,html}` | Diagrama interactivo de arquitectura (Archify); el JSON es la fuente. Ver [`references/archify.md`](references/archify.md). |

---

## Variables de las plantillas

Las plantillas bajo `assets/templates/` usan marcadores que el scaffolder sustituye.
Si editas a mano, reemplázalos todos:

| Marcador | Significado |
|----------|-------------|
| `{{PROJECT_NAME}}` | Nombre legible (`Mi Proyecto`). |
| `{{PROJECT_SLUG}}` | Identificador kebab-case (`mi-proyecto`), usado como carpeta y repo. |
| `{{PACKAGE_NAME}}` | Identificador snake_case (`mi_proyecto`), usado como paquete Python. |
| `{{DESCRIPTION}}` | Descripción de una línea. |
| `{{OWNER}}` / `{{REPO}}` | Cuenta y nombre del repositorio. |
| `{{REPO_URL}}` / `{{SSH_URL}}` | URLs HTTPS y SSH del repositorio. |
| `{{AUTHOR}}` / `{{AUTHOR_EMAIL}}` | Autoría. |
| `{{PYTHON_VERSION}}` | Versión de Python (`3.13`). |
| `{{YEAR}}` / `{{DATE}}` | Año y fecha ISO. |

Bloques condicionales (se eliminan si la bandera es falsa):
`{{#if PACKAGE}}…{{/if}}` (src-layout), `{{#if TYPES}}…{{/if}}` (`ty`),
`{{#if GITHUB}}…{{/if}}`, `{{#if AGENTS}}…{{/if}}`.

---

## Documentación de apoyo

Carga estos archivos **solo cuando los necesites** (divulgación progresiva):

| Referencia | Contenido |
|------------|-----------|
| [`references/constitution.md`](references/constitution.md) | Anatomía completa del `CONSTITUTION.md` sección por sección, con ejemplos. |
| [`references/python-stack.md`](references/python-stack.md) | `uv`, `pyproject.toml`, Ruff, Makefile, pre-commit, `.editorconfig`, `.gitignore`. |
| [`references/github.md`](references/github.md) | Creación del repo, remotos SSH, badges, plantillas, CI, Dependabot, labels, ramas. |
| [`references/agent-context.md`](references/agent-context.md) | `AGENTS.md`, `.opencode/rules/` y tgrep. |
| [`references/git-identity.md`](references/git-identity.md) | Identidad Git automática (`includeIf`): perfil Jan y perfil propio para macOS/Windows. |
| [`references/archify.md`](references/archify.md) | Diagramas de arquitectura interactivos con Archify (instalación, tipos, validate/deliver, README). |
| [`references/slidev.md`](references/slidev.md) | Presentaciones con Slidev (proyectos de curso): monolito, hub, reglas de sintaxis, export. |

---

## Identidad Git automática (`includeIf`)

Configura Git para que todo repositorio bajo una carpeta use **automáticamente** un nombre,
un correo y una llave SSH. Es una de las piezas más útiles del estándar: elimina flags y
`gh auth` por proyecto. **Hay dos perfiles** y el agente debe decidir cuál aplica
(detalle en [`references/git-identity.md`](references/git-identity.md)).

### Perfil A — Ejemplo (configuración del autor de la skill)

> Es solo un **ejemplo real** de un perfil funcionando. Cualquier otro usuario sigue el
> **Perfil B** con sus propios datos.

Carpeta canónica de ejemplo `~/Desktop/Repositorios/personal/`:

```ini
# ~/.gitconfig
[includeIf "gitdir:~/Desktop/Repositorios/personal/"]
    path = ~/.gitconfig-personal
```

```ini
# ~/.gitconfig-personal
[user]
    name = Jan Polanco V.
    email = hamsomp3@gmail.com
[core]
    sshCommand = ssh -i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes
```

**Efecto:** todo repo bajo esa carpeta usa el nombre, correo y llave del ejemplo. Preferir
remotos **SSH** (`git@github.com:<tu-usuario>/<repo>.git`); HTTPS puede resolver con un token
de otra cuenta.

### Perfil B — Cualquier otro usuario (alumno, compañero)

Si el usuario pide identidad automática y **no** comparte el perfil de ejemplo, **pregúntale
primero** su nombre, correo, llave SSH y carpeta de proyectos, y luego configura `includeIf`
en **su** carpeta y **su** sistema operativo (macOS o Windows). Script listo:

```bash
python3 <SKILL_DIR>/scripts/setup_git_identity.py \
  --name "Pedro Pérez" --email pedro@example.com \
  --key ~/.ssh/id_ed25519 --dir ~/Repos/personal --platform mac
# Windows: --key C:/Users/pedro/.ssh/id_ed25519 --dir C:/Users/pedro/Repos --platform windows
```

El script respalda `~/.gitconfig`, es idempotente y tiene un modo `--print` que solo muestra
los bloques sin escribir nada. Pasos manuales y gotchas (orden de `includeIf`, `gitdir/i:`,
rutas con `/` en Windows, `IdentitiesOnly`) en [`references/git-identity.md`](references/git-identity.md).

> ⚙️ **Nunca** se commitea: es configuración **local de la máquina**. Vive en la constitución
> solo **como nota** (no como archivo del repo), y **solo se aplica si el usuario lo pide**.

---

## Flujo diario (commit + push)

```bash
git status                       # 1. ver cambios
make check                       # 2. lint + formato + (tipos) + pruebas
git add -A                       # 3. agregar
git commit -m "tipo: mensaje"    # 4. commitear (los hooks se ejecutan solos)
git push                         # 5. subir
```

---

## Checklist de verificación

Antes de dar por terminado un proyecto o un cambio:

- [ ] `CONSTITUTION.md` existe y está poblado (propósito, stack, estructura, flujo, decisiones).
- [ ] `uv sync` funciona y `uv.lock` está versionado.
- [ ] `make check` pasa en verde (lint + formato + pruebas).
- [ ] `uv run pre-commit run --all-files` pasa (hooks instalados).
- [ ] `README.md` tiene badges, TOC, descripción, stack, primeros pasos y licencia.
- [ ] `LICENSE` presente (MIT por defecto).
- [ ] `.github/` con PR template, issue templates, CI, Dependabot y labels (si aplica).
- [ ] `AGENTS.md` (y `.opencode/rules/tgrep.md`) describen el proyecto para agentes (si aplica).
- [ ] Identidad Git automática configurada **si el usuario lo pidió** (perfil A para Jan / perfil B para otros).
- [ ] Diagrama de arquitectura con Archify en `docs/` y enlazado desde el README (si aplica).
- [ ] Sin secretos, datos personales ni artefactos pesados versionados.
- [ ] El historial de decisiones de la constitución registra los cambios significativos.

---

## Directiva de mantenimiento

> Cada vez que se realicen cambios significativos (nuevas funcionalidades, cambios
> arquitectónicos, adición de clases/módulos o ajustes de tecnologías), **se debe
> actualizar `CONSTITUTION.md`** en el mismo commit para mantener la verdad central del
> proyecto. El checklist de la plantilla de Pull Request lo verifica explícitamente.
