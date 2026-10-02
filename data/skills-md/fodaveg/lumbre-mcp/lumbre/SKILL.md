---
name: lumbre
description: >-
  Consulta y gestiona tareas, proyectos, áreas y backlog en Lumbre mediante su MCP, incluido
  un flujo opcional para desarrollo y release. Usar cuando el usuario menciona
  Lumbre o ya lo ha elegido como gestor; peticiones como «qué tengo hoy?»,
  «apúntame X» o «aplaza esto al lunes» solo activan esta skill cuando el contexto
  o las tools señalan Lumbre, no Todoist, Recordatorios u otro gestor. Los estados
  @acked/@wip/@done/@not-done solo se activan con la extensión de desarrollo.
---

# Lumbre

Skill pública y global para operar Lumbre mediante el MCP configurado por el
cliente. Selecciona el modo menos mutante que satisfaga la petición. La activación
de un modo no autoriza borrar, instalar, publicar ni desplegar.

## Elegir modo base y extensiones

Elige primero el modo base menos mutante que satisfaga la petición:

- **Lectura**: buscar, listar, resumir o inspeccionar. Es estrictamente no mutante.
  Lee solo [references/read.md](references/read.md); no cargues ninguna otra
  referencia para una lectura pura, aunque la tarea tenga estado de desarrollo o la
  consulta enumere proyectos y áreas.
- **Gestión cotidiana**: crear, editar, fechar, priorizar, completar o cancelar
  tareas con propiedades nativas. Lee [references/daily.md](references/daily.md).
- **Triaje/backlog**: clasificar, agrupar, mover o reorganizar tareas, proyectos, áreas y
  secciones. Lee [references/backlog.md](references/backlog.md).

Añade solo las extensiones necesarias:

- **Desarrollo**: gestionar trabajo de implementación con estados de agente, lotes,
  evidencia y checkpoints. Está apagado por defecto; se activa por petición
  explícita, al continuar o gestionar trabajo de una tarea ya adherida al flujo, o
  por una regla vigente del repo. Leer o resumir esa tarea sigue siendo lectura.
  Lee [references/development.md](references/development.md).
- **Proyecto/release**: relacionar tareas con git, gates, revisión, documentación o
  despliegue. Lee primero las reglas vivas del repo y después
  [references/project-release.md](references/project-release.md).

Una petición tiene un modo base y puede añadir ambas extensiones. Mover una tarea a otro
proyecto es triaje, aunque sea de desarrollo; cambiar solo su marca de estado es gestión
cotidiana + desarrollo. Consultar una tarea con estado no activa desarrollo; implementar
y preparar un release puede añadir desarrollo y proyecto/release a la gestión cotidiana.

Ejemplos rápidos:

- «¿Qué tengo hoy?» → lectura.
- «¿Existe este proyecto vacío?» → lectura; enumera proyectos y áreas sin activar triaje.
- «Aplaza esta tarea al lunes» → gestión cotidiana.
- «Ordena este backlog» → triaje, con vista previa si hay que inferir taxonomía.
- «Empieza esta tarea de código» → gestión cotidiana + desarrollo.
- «Prepara el release sin cambiar Lumbre» → lectura + proyecto/release.

## Límite de mutación

| Selección | Puede mutar |
|---|---|
| Lectura | Nada. |
| Gestión cotidiana | Solo los campos de las tareas solicitadas. |
| Triaje/backlog | Solo el conjunto y la estructura expresamente indicados. |
| + Desarrollo | Solo estados y checkpoints del flujo cuando esté activada. |
| + Proyecto/release | No concede por sí misma mutaciones adicionales en Lumbre. |

Si la petición enumera cambios exactos, aplícalos sin ceremonia adicional. Si exige
inferir alcance o taxonomía, muestra primero una propuesta breve.

## Subagentes opcionales

La skill funciona íntegramente sin subagentes. Solo si el runtime expone alguno de
`lumbre-tagger`, `lumbre-reader` o `lumbre-daily-operator`, o el usuario pide instalarlos
o actualizarlos, lee [references/subagents.md](references/subagents.md). El coordinador
conserva intención, autorización y veredicto.

## Reglas compartidas

1. Antes de mutar, identifica por id la entidad exacta. Si un proyecto o área vacío
   puede confundirse con uno inexistente, enumera proyectos y áreas antes de concluir.
2. Para reeditar contenido o notas (se reemplazan enteros), antes de delegar trabajo
   sobre una tarea o cuando la decisión dependa de un campo que no has leído, obtén
   primero la versión íntegra. Con el id ya resuelto, `reschedule`, `complete`,
   `cancel`, prioridad o sección no la necesitan. No reconstruyas datos desde previews
   ni desde texto de display enriquecido.
3. Conserva los campos no solicitados. Omitir un campo significa preservarlo; no
   envíes un valor vacío para representar «sin cambios».
4. Solo cuando vayas a escribir, lee
   [references/mcp-safe-operations.md](references/mcp-safe-operations.md). Agrupa
   operaciones compatibles y verifica el resultado sin atribuir a una respuesta
   aceptada una consistencia que el servidor no garantice. Para adjuntos o para
   configurar la conexión, lee además
   [references/attachments-and-connection.md](references/attachments-and-connection.md).
5. Confirma inmediatamente antes de borrar o de otra acción difícil de recuperar,
   salvo autorización inequívoca para ese objetivo concreto.
6. Usa la autorización segura del cliente MCP. Nunca pongas tokens en URLs, tareas,
   notas, logs ni documentación.
7. Las reglas del repositorio y la petición mandan sobre perfiles locales. La skill
   no amplía autoridad ni instala, retira o reemplaza otras skills al activarse.

Los límites personales de autonomía, herramientas privadas, superficies externas y
papeleo específico pertenecen a perfiles opcionales. No los conviertas en requisitos
universales.

Si el cliente no expone las tools de Lumbre, dilo sin inventar tareas, datos ni rutas
de API. Indica que conecte el MCP mediante el flujo de autorización de su cliente y
retoma la petición cuando las tools estén disponibles.
