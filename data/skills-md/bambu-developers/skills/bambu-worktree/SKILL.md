---
name: bambu-worktree
description: Crea un git worktree nuevo y aislado dentro de la carpeta `.worktrees/` del repo, con su propia rama, a partir de una descripción breve del requerimiento o del nombre explícito de rama/carpeta que el usuario quiera usar — para poder trabajar varias cosas en paralelo sin hacer stash/checkout dentro del mismo checkout. Usa este skill cuando el usuario pida "crea un worktree", "nuevo worktree", "quiero trabajar en paralelo", "aísla este feature en su propia carpeta", "dame un checkout aparte para X", "levanta un worktree para Y", "new worktree", "work on multiple branches at once", "set up a parallel checkout", o cuando mencione la carpeta `.worktrees/` explícitamente.
---

# Worktree aislado para trabajar en paralelo

Crea un `git worktree` nuevo en `.worktrees/<feature>/` con su propia rama, para que el usuario pueda tener varios requerimientos avanzando a la vez sin pisarse entre sí (sin `stash`/`checkout` constantes en el mismo directorio de trabajo). Es **project-agnostic**: no asume nombre de rama por defecto, package manager, ni convención de ramas — las detecta o pregunta.

## Cuándo usar este skill

- "Crea un worktree para X."
- "Necesito trabajar en paralelo en Y sin tocar lo que ya tengo en progreso."
- "Aísla este feature en su propia carpeta."
- "Dame un checkout aparte para arreglar Z mientras sigo con lo otro."
- "New worktree for the login feature", "set up a parallel checkout for this bugfix."
- El usuario ya trae un nombre de rama específico en mente y solo quiere el worktree listo.

No lo uses para operaciones normales de branch dentro del mismo checkout (`git checkout -b ...`) cuando el usuario no pidió aislamiento — esto es específicamente para trabajar **varias cosas a la vez** sin interferencia.

## Flujo de trabajo

### Paso 0 — Prerrequisitos

```bash
git rev-parse --is-inside-work-tree   # estás dentro de un repo git
git worktree list --porcelain | head -5
```

Si no hay ningún argumento ni descripción del requerimiento en el mensaje del usuario, detente y pídele una descripción breve (o el nombre de rama que quiera usar) antes de continuar — la necesitas para nombrar la carpeta y la rama.

### Paso 1 — Ubicar la raíz del repo principal

Los worktrees viven todos bajo `.worktrees/` en la raíz del **repo principal** (el primer worktree que lista `git worktree list`), nunca anidados dentro de otro worktree. Si ya estás parado dentro de un worktree existente, resuelve la raíz real con:

```bash
git worktree list --porcelain | sed -n '1,/^$/p'   # el primer bloque es siempre el worktree principal
```

y opera `.worktrees/` relativo a esa raíz, no al directorio actual.

### Paso 2 — Derivar el nombre del feature

A partir de la descripción del usuario, genera un slug en **kebab-case simple**: minúsculas, sin acentos, palabras separadas por guiones, sin prefijo de tipo de commit (`feat/`, `fix/`, …) y sin scope explícito — solo las 3-6 palabras que mejor identifiquen el requerimiento de forma única y legible.

- "agregar login con PIN a taquilla" → `agregar-login-pin-taquilla`
- "fix del cálculo de descuento por tipo de viaje" → `fix-calculo-descuento-tipo-viaje`
- "reporte de ventas por vendedor en Excel" → `reporte-ventas-vendedor-excel`

Si el usuario ya te dio explícitamente el nombre de carpeta/rama que quiere usar, respétalo tal cual (solo normaliza a kebab-case si trae espacios o mayúsculas) en vez de reinterpretarlo.

### Paso 3 — Detectar la rama base

Si el usuario indicó una rama base explícita, úsala. Si no, **detecta la rama por defecto real del repo** — nunca la hardcodees (no asumas `develop`, `main` ni `master`):

```bash
git branch --show-current
gh repo view --json defaultBranchRef --jq .defaultBranchRef.name 2>/dev/null \
  || git remote show origin 2>/dev/null | sed -n '/HEAD branch/s/.*: //p'
```

1. Si la rama actual coincide con la rama por defecto detectada, úsala como base sin preguntar — es el flujo normal de arrancar un feature nuevo.
2. Si la rama actual es otra (ya estás parado en una feature branch, o dentro de otro worktree), pregúntale al usuario si quiere basar el nuevo worktree en esa rama o en la rama por defecto — no asumas.

Corre `git fetch origin <rama-base>` antes de crear el worktree para que la rama nueva parta de la punta real, no de una copia local desactualizada.

### Paso 4 — Guardas antes de ejecutar

- Verifica que no exista ya `.worktrees/<feature>` (`ls .worktrees/` o `git worktree list`). Si existe, avísale al usuario y pregunta si quiere otro nombre o si de hecho quiere reusar/entrar a ese worktree.
- Verifica que no exista ya una rama local o remota con ese mismo nombre (`git branch --list <feature>` / `git ls-remote --heads origin <feature>`). Si existe, avisa y confirma antes de seguir (podría no ser tuya, o podría ser una rama vieja que conviene retomar en vez de crear otra).

### Paso 5 — Asegurar que `.worktrees/` esté ignorada

Esta carpeta es un conjunto de checkouts locales en paralelo — nunca debe subirse al remoto. Antes de crear el worktree, revisa el `.gitignore` del repo destino:

```bash
grep -qxF '.worktrees/' .gitignore 2>/dev/null
```

Si no está, agrega la línea `.worktrees/` al `.gitignore` del repo (no al de este repo de skills) y dilo explícitamente en el reporte final — es un cambio a un archivo versionado, así que coméntalo con el usuario si prefieres confirmarlo antes de escribirlo.

### Paso 6 — Crear el worktree

```bash
git worktree add -b <feature> .worktrees/<feature> origin/<rama-base>
```

Usa `-b <feature>` explícito (no dejes que `git worktree add` adivine el nombre de rama solo por el path) para que quede inequívoco qué rama se creó. Si `origin/<rama-base>` no existe localmente todavía, usa `<rama-base>` a secas tras el `fetch` del Paso 3.

### Paso 7 — Reporte final

Confirma al usuario:

- Ruta del worktree creado (`.worktrees/<feature>`, relativa a la raíz del repo principal).
- Nombre de la rama nueva y rama base de la que partió.
- Si agregaste `.worktrees/` al `.gitignore`, dilo explícitamente.
- Sugiere el siguiente paso obvio: `cd .worktrees/<feature>` para trabajar ahí, o abrir esa carpeta como proyecto aparte si usa el flujo de `EnterWorktree`/una sesión nueva de Claude Code.

## Reglas clave

1. **Nunca hardcodees la rama base por defecto** (`develop`/`main`/`master`) — detéctala con `gh repo view` o `git remote show origin`, o pregúntala si hay ambigüedad.
2. **Siempre verifica colisiones** de nombre de carpeta y de rama (local y remota) antes de crear — nunca sobreescribas ni reutilices sin confirmar con el usuario.
3. La carpeta es `.worktrees/` (oculta, con punto) en la raíz del repo principal, y debe estar en el `.gitignore` del repo destino — si falta, agrégala y avísalo.
4. Usa siempre `-b <feature>` explícito en `git worktree add` — nunca dejes que el nombre de la rama se infiera solo del path.
5. No inventes el slug si el usuario ya dio un nombre de rama/carpeta explícito — respétalo, solo normaliza formato.
