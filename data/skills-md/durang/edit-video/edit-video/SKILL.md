---
name: edit-video
description: Professional editing machine for video that ALREADY EXISTS, in levels — 1 Recorte (fast clean clips with captions and logo), 2 Editorial (studio typography, palette, details), 3 Estudio (advanced motion design with an approved proposal), 4 Director (proposed — generated inserts, 3D, music). Includes clipper to turn a long video into many short clips. Captions, cutting dead air, punch-in zooms, title cards, lower thirds, graphic overlays, pop-ups, music and SFX, 16:9 to 9:16 reframing, background removal, 3D objects, a named style (movie trailer, Vox explainer), or assembling several clips (for example shots generated with Seedance, Grok, Veo or Kling) into one finished MP4. Works in any agent that reads SKILL.md (Claude Code, OpenClaw, Hermes Agent, Codex, Cursor…) on top of the HyperFrames skills. Triggers on /edit-video, "edita mi video", "shotgun de estilo", "cambio de diseño", "explora direcciones", "sácame clips", "clips de esta entrevista", "nivel 1/2/3", "nivel 3 intensidad 2", "cárgalo más de efectos", "recetario", "ponle subtítulos", "córtale los silencios", "hazlo vertical para Reels", "monta estos clips", "edit my video", "add captions", "cut the pauses", or a video file plus an edit request. NOT for generating new footage from a text prompt, and NOT for re-filming one take from new camera angles.
metadata:
  version: 3.8.1
  author: Sergio Duran
  method: "Let Claude Edit Your Videos — @pauloshimas / The Creator Stack"
  engine: heygen-com/hyperframes
---

# /edit-video — la máquina de edición

**Cuatro niveles, un solo skill.** El nivel decide el motor, la línea de diseño y la aprobación:

| Nivel | Qué es | Motor | Aprobación |
|---|---|---|---|
| **1 · Recorte** | Clips limpios: subtítulo, palabra activa, gancho, logo | `clipper/` (FFmpeg) | sale directo |
| **2 · Editorial** | Tipografía de estudio, paleta, caja en la palabra, rótulo, barra, grade | `clipper/` (FFmpeg) | sale directo |
| **3 · Estudio** | Motion design avanzado, **siempre**, en 3 intensidades: 1 Profesional · 2 Dinámico · 3 Extremo (`references/nivel-3.md` §0) | HyperFrames | **propuesta aprobada** antes |
| **4 · Director** *(propuesto)* | Lo del 3 + planos generados, 3D, música a la imagen | HyperFrames + Seedance/Higgsfield | tratamiento + animatic + cada inserto |

Detalle, comandos y quién puede correr cada uno: `references/niveles.md`.

**Otro video del mismo cliente** → su kit y su plantilla, sin preguntas. **Cambio de diseño, cliente
nuevo, o propuesta de nivel 3 sin concepto claro** → **shotgun de estilo**: 3 direcciones de verdad
distintas, cuadros de estilo reales sobre el metraje, el director elige en un tablero, y lo elegido
se vuelve la plantilla del cliente y alimenta su gusto. Detalle: `references/shotgun.md`. Si el usuario no dijo el
nivel, **una** pregunta: *"¿Nivel 1, 2 o 3? ¿O todos en 1–2 y los mejores en 3?"*

**Nivel 3 en tres intensidades** (tabla en `references/nivel-3.md` §0). Se pide *"nivel 3 ·
intensidad 2 · énfasis recortes"*; sin intensidad es la **1 · Profesional**. **2 · Dinámico** carga
más cambios, sonido y recortes; **3 · Extremo** es la de *"¿qué es eso?"* y exige una prueba animada
de 5–10 s aprobada antes. Efectos probados, con tiempos exactos: `references/recetario-3.md`; si el
director pide uno por su nombre, se construye con esa receta. Al cerrar un video de nivel 3, lo
nuevo que funcionó se añade como receta.

**Tiempos reales, siempre.** Antes de lanzar un trabajo: `python3 scripts/tiempos.py estimar --nivel N
--intensidad I --tipo nuevo|subida|ronda|detalles --duracion S` y se le dice al director *"estimado
X–Y min; referencias: …"* (los 2–3 trabajos parecidos más recientes, con lo que tardaron). Si pregunta
cómo va: `tiempos.py avance --log <stream-json del constructor> …` (fase, %, hora estimada de fin).
Al terminar: `tiempos.py registrar …` (clipper registra solo). Sin historia parecida se dice que es la
primera vez y se registra.

Tú (el agente) no reproduces video. Así que antes de editar nada te das **oídos** (transcripción
con el tiempo de cada palabra) y **ojos** (fotogramas). Con eso planeas el montaje, lo enseñas,
esperas el OK, y le pasas la construcción a los skills de **HyperFrames**, que escriben el video
como una página web y lo renderizan en MP4.

**Cada efecto se ancla a una PALABRA, no a un segundo.** Eso es lo que hace que parezca hecho a mano.

Este skill **no reimplementa HyperFrames**: pone el método, las reglas y el idioma, y enruta.

---

## Paso 0 · ¿Editar o crear?

| El usuario tiene… | Qué hacer |
|---|---|
| Un video grabado, o clips ya generados | **Seguir aquí** |
| Solo una idea, sin material filmado | **No es este skill.** Se genera primero (Seedance, Grok, Veo, Kling…) y el montaje entra al final. Ver `references/pipeline.md` |
| Solo gráficos, sin cámara (logo animado, explicativo sin cara) | Enrutar directo a HyperFrames: `/motion-graphics`, `/faceless-explainer` |
| **Un video largo** (entrevista, podcast, charla) → **varios clips cortos** | `clipper/` (viene dentro): niveles 1–2 en volumen; los mejores en nivel 3 → propuesta, OK, y se construyen aquí. Ver `references/niveles.md` y `references/clipper.md` |
| Un video corto que quiere **nivel 3** | Propuesta según `references/nivel-3.md` → **PARADA** → Pasos 3–9 |

Si no está claro, **una** pregunta de una línea.

## Paso 1 · Todo instalado — el skill se instala lo que le falta

`SKILL_DIR` es la carpeta donde está este `SKILL.md`. Normalmente una de estas:
`~/.agents/skills/edit-video` · `~/.claude/skills/edit-video` · `~/.openclaw/skills/edit-video` ·
`~/.hermes/skills/edit-video`. Si no la sabes: `ls -d ~/.*/skills/edit-video ~/.agents/skills/edit-video`.

```bash
bash SKILL_DIR/scripts/check.sh
```

- **Sale en verde** → sigue al Paso 2.
- **Falta algo** → corre `bash SKILL_DIR/scripts/setup.sh`. **Sin `--yes` no instala nada**: solo
  imprime el plan exacto (qué falta y con qué comando) y sale con código 2. **Enséñale ese plan al
  usuario tal cual, pide permiso**, y con su sí vuelve a correr `bash SKILL_DIR/scripts/setup.sh --yes`.
  Instala FFmpeg, Node, whisper-cpp, los skills de HyperFrames en este agente y el modelo de Whisper
  multilingüe, y termina con `check.sh`.
- **Nunca instales sin permiso. Nunca trabajes alrededor de lo que falta.**

Una vez en verde, no se vuelve a instalar: las siguientes sesiones pasan directo.

**Versión al día.** El repo cambia seguido. `check.sh` compara la versión instalada con la de GitHub;
si hay una nueva, **díselo al usuario** con lo que cambió (CHANGELOG) y actualiza con su permiso
(`npx skills update edit-video -g -y`) antes de empezar. Mejoras que sirvan a todos y no seas el dueño
del repo: issue o PR (`CONTRIBUTING.md`).

## Paso 2 · Reglas del proyecto — onboarding la primera vez

Busca en la carpeta del video un `AGENTS.md` (o `CLAUDE.md`) con una sección `## edit-video`.

- **Si existe**, léela y aplícala en todo: idioma, nombres, colores, tipografías, safe zone, ritmo.
- **Si no existe**, haz el onboarding de `references/onboarding.md`: seis preguntas cortas, y
  escribe el archivo de reglas desde `templates/AGENTS.md.template`. Una sola vez; las siguientes
  sesiones ya lo encuentran.

**Cliente y aprendizaje.** Antes de seguir:

```bash
bash SKILL_DIR/scripts/sync.sh pull      # lo último de edit-video y del área de clientes
```

Si el video es de un cliente (`cliente: <slug>` en el `AGENTS.md`, o el usuario lo nombra), lee su
carpeta del área privada **antes del beat sheet**: `CLIENTE.md`, `APRENDIZAJES.md`, `kit/`. Sus reglas
mandan sobre los valores por defecto, y se parte de su `kit/plantilla.html` si existe. Cliente nuevo:
`sync.sh new-client <slug>`. Sin área de clientes instalada, dilo en una línea y sigue.
Detalle: `references/aprendizaje.md`.

## Paso 3 · Oídos y ojos

```bash
bash <SKILL_DIR>/scripts/ingest.sh TOMA.mp4          # detecta el idioma (o pásalo: es, en, pt…)
```

Deja en `TOMA.edit/`: `metadata.json`, `transcript.json` (palabras con `start`/`end`),
`transcript.txt` legible con tiempos, y `frames/` (2 fps si dura ≤10 s, 1 fps si más).

- **Idioma**: sin argumento lo detecta con 30 s de audio. Si lo pasas y el audio dice otra cosa,
  **se detiene** (código 3): repite con el idioma que dice. Nunca el modelo `small.en` por defecto de
  HyperFrames si no es inglés — el español sale destrozado.
- **Diccionario permanente**: antes de que nadie lea nada, aplica las correcciones guardadas (global →
  cliente → proyecto), incluidas las de varias palabras ("near Turing" → "nearshoring") a nivel de
  palabra. Revisa `diccionario.log` y los nombres propios que falten. **Cada corrección nueva se
  guarda**, para que no vuelva a pasar:
  `python3 SKILL_DIR/scripts/diccionario.py agregar "Columbia" "Colombia" --cliente <slug>`
  (marcas y nombres del cliente → `--cliente`; términos generales → sin opción).
- **Lee TODOS los frames junto con las palabras.** Luego cuéntale al usuario, breve: qué dice,
  cuándo, qué hay en el plano, dónde están la cara, las manos y los huecos libres.

## Paso 4 · Beat sheet, y PARADA

```
| inicio | fin | palabras exactas | qué aparece en pantalla | dónde | sonido |
```

Declara formato (9:16 / 16:9 / 1:1 / 4:5), safe zone y duración estimada.
**Espera el OK explícito. No construyas nada antes.** Cambiar en papel es gratis.

## Paso 5 · Rough cut

Fuera las pausas de más de 0.3 s y las respiraciones, **nunca dentro de una palabra**, con un beat
corto antes de cada remate. Reporta la duración nueva. Efectos, después.

## Paso 6 · Construir — enrutar al skill de HyperFrames

| Lo que se pide | Skill |
|---|---|
| Subtítulos, sin tocar el metraje | `/embedded-captions` |
| Tarjetas encima: títulos, rótulos, datos, citas, panel lateral, PiP | `/talking-head-recut` |
| Varios clips, reel, sizzle, remix, montaje libre | `/general-video` |
| Pieza corta de motion: logo, contador, mapa, titular animado | `/motion-graphics` |
| Música, ducking, fades, efectos de audio | `/hyperframes-audio` |
| Recorte de fondo, TTS, SFX, música, imágenes | `/media-use` |
| No está claro | `/hyperframes` — la puerta de entrada de HyperFrames |

Al skill de HyperFrames le pasas: **el beat sheet aprobado, el `transcript.json` corregido, las
reglas del proyecto y el formato**. Él construye; tú vigilas que se cumpla cada regla.
Detalle: `references/routing.md`.

## Paso 7 · Preview, notas, verificar, render

```bash
npx hyperframes preview                 # el usuario lo mira en su navegador
npx hyperframes snapshot                # TÚ miras el frame antes de decir "listo"
npx hyperframes render -o final.mp4     # render local
npx hyperframes cloud render            # o en la nube de HeyGen (créditos, requiere auth login)
```

Notas del usuario: una por línea, con el tiempo. Aplica, haz snapshot del frame afectado,
míralo, y vuelve a enseñar. Guarda `v1`, `v2`, `v3`… antes de cada ronda.

## Paso 8 · Revisor final — obligatorio

El que construye no aprueba. Antes de decir "listo", revisa **el MP4 renderizado entero**:

```bash
bash SKILL_DIR/scripts/qa.sh final.mp4 2  <tiempos clave: transiciones, entradas grandes, cierre>
```

Mira **todas** las hojas de contacto (un cuadro cada 0.5 s) y los cuadros a tamaño completo con la
checklist de `references/qa.md`: ninguna palabra partida o cortada, nada sobre la cara, nada fuera de
la safe zone, nada ilegible en el teléfono, nada del original asomando, coherencia de movimiento.
Si el entorno permite subagentes, que la revisión la haga **otro agente** que solo vea el video.
Cada defecto: anotar en `SNAPSHOTS.md`, arreglar, re-renderizar, **re-revisar entero**.

## Paso 9 · Aprender — obligatorio al entregar

Con el video entregado, clasifica cada aprendizaje (notas del director, defectos cazados, lo que
funcionó) con una pregunta: **¿serviría en un video de otro cliente?**

- **Sí** → `edit-video` (este repo): la referencia que toque + `CHANGELOG.md` + versión. Generalizado,
  **sin nada del cliente**.
- **No** → `edit-video-clients/clients/<slug>/`: `CLIENTE.md`, `APRENDIZAJES.md`, `HISTORIAL.md`, `kit/`.

```bash
bash SKILL_DIR/scripts/sync.sh push "resumen en una línea"
```

Sube los dos repos; un guardia bloquea el público si se cuela algo privado. Reporta en una línea qué
fue a cada sitio. Procedimiento completo: `references/aprendizaje.md`.

**Retro (sin buscar en internet), tres líneas:** ¿qué corrigió el director? ¿qué cazó el revisor que
el constructor no vio? ¿qué no pudimos hacer o salió peor de lo querido? Lo tercero, si no tiene
arreglo hoy, va a `LIMITACIONES.md`: es lo que el **radar quincenal** (días 1 y 15) vigila. Se busca en internet
durante un trabajo **solo** con razón (fallo desconocido, defecto repetido, pedido que no sabemos
hacer). Detalle: `references/mejora-continua.md`.

---

## Reglas duras

1. **Beat sheet antes de construir.** Siempre.
2. **Rough cut primero, efectos después.**
3. **Nunca cortar dentro de una palabra.**
4. **El idioma se detecta o se verifica** antes de transcribir. Nunca el modelo `.en` por defecto si no es inglés.
5. **Nombres propios corregidos**, y cada corrección nueva **al diccionario**: el mismo error no se corrige dos veces.
6. **Safe zone**: nada de texto en el 20% inferior ni pegado al borde derecho (botones de la app).
7. **Una nota = un cambio**, con el tiempo. Qué, dónde, cuándo — nunca cómo.
8. **Versionar** antes de cada ronda.
9. **Revisor final antes de decir "listo"** (Paso 8): el MP4 entero, cuadro cada 0.5 s. Decir "listo" sin haberlo revisado es mentir.
13. **Cada entrega deja aprendizaje** (Paso 9): lo general al público, lo del cliente al privado. Nunca datos de un cliente en `edit-video`.
10. **La voz del usuario nunca se sustituye ni se re-sintetiza.**
11. **Máximo un zoom cada cinco segundos.** Lo raro es lo que impacta.
12. **El director es el usuario.** El gusto no se delega.

## Dónde corre

**Donde corre el agente.** Necesita el disco con los videos, Node, FFmpeg y whisper-cpp.

- Agente en tu ordenador (Claude Code, OpenClaw o Hermes en tu Mac) → **el ordenador tiene que
  estar prendido**.
- Agente en un servidor (OpenClaw o Hermes en un VPS, hablándole por Telegram o WhatsApp) → corre
  en el servidor; **tu ordenador puede estar apagado**. `setup.sh` funciona igual en Linux.
- El render pesado puede irse a la nube de HeyGen con `npx hyperframes cloud render`.
- Un chat sin terminal ni disco (una app de chat en la nube) no puede correrlo.

## Referencias

| Archivo | Cuándo |
|---|---|
| `references/onboarding.md` | Primera vez en una carpeta: las seis preguntas |
| `references/setup.md` | Instalación en cualquier agente |
| `references/routing.md` | Qué skill de HyperFrames construye cada cosa |
| `references/pipeline.md` | Combinar con modelos generativos: generar → montar |
| `references/film-it-right.md` | **Antes de grabar** |
| `references/prompts.md` | Pedidos listos, de diario y para lucirse |
| `references/styles.md` | Copiar un estilo |
| `references/motion-design.md` | **Nivel estudio**: sistema de coherencia, mapas, palabras detrás de la persona, cierre con personaje, diseño sonoro |
| `references/mejora-continua.md` | **Cuándo se investiga**: retro por video, búsqueda dirigida, radar quincenal (días 1 y 15) con revisión profunda de los niveles 2 y 3 |
| `LIMITACIONES.md` · `references/radar.md` | Lo que aún no sale bien (lo vigila el radar) · bitácora de cada radar |
| `references/shotgun.md` | **Cambiar el diseño**: direcciones, cuadros de estilo, tablero, memoria de gusto |
| `references/niveles.md` | **Los niveles**: motor, línea de diseño, comandos, aprobación |
| `references/nivel-3.md` | **Contrato del nivel 3** (siempre avanzado), tiempos, técnicas de HyperFrames, lo que ya no se hace |
| `references/recetario-3.md` | **Recetario del nivel 3**: efectos probados con tiempos exactos (R1 cierre congelado con recorte) y ejemplos por probar |
| `scripts/tiempos.py` | Tiempos reales: estimar con trabajos parecidos, avance en %, registrar al terminar |
| `references/nivel-4.md` | Nivel 4 · Director (propuesto) |
| `clipper/` | Motor de los niveles 1–2 y del corte del 3 (`clipper.py`, `studio.py`, plantillas, fuentes) |
| `references/clipper.md` | Video largo → muchos clips: cuándo clipper, cuándo aquí, y juntos |
| `references/aprendizaje.md` | **Los dos repos**: área de clientes, qué va a cada uno, `sync.sh` |
| `references/qa.md` | **Revisor final**: la checklist que decide si se entrega |
| `references/troubleshooting.md` | Defecto → arreglo |
| `scripts/check.sh` · `scripts/setup.sh` · `scripts/ingest.sh` · `scripts/qa.sh` | Comprobar · auto-instalar · oídos y ojos · revisor final |
| `templates/AGENTS.md.template` | Reglas del proyecto del usuario |
