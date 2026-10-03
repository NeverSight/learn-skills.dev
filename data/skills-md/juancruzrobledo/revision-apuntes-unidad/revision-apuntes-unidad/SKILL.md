---
name: revision-apuntes-unidad
description: >
  Revisa y corrige el material de apuntes de una unidad de una materia del campus Moodle (TUP/UTN u otro): documentos Word,
  PDF de presentaciones (con o sin Gamma), pptx, markdown o texto que estén publicados en el aula. Valida calidad, estilo de
  redacción (por defecto tercera persona; configurable), tiempos verbales homogéneos, rastros de IA, errores temáticos y
  técnicos, datos mínimos de portada (materia, unidad, tema y revisor) y bibliografía real, respetando el formato que el
  archivo ya tiene. Usa un subagente DETECTOR y otro CORRECTOR por actividad y una compuerta OBLIGATORIA de revisión manual
  del tutor antes de subir.
  Usala SIEMPRE que el usuario quiera auditar, revisar, validar o corregir los apuntes o el material de una unidad, aunque
  no nombre la skill: "revisá los apuntes de la unidad 4", "auditá el material de Programación 1", "corregí los Word y los
  PDF de la unidad", "verificá que esté en tercera persona", "sacale la marca de agua de Gamma a los apuntes", "chequeá que
  no haya rastros de IA en los documentos", "armá el orden de subida de los apuntes corregidos". NO la uses para corregir
  entregas de alumnos (skill corregir), subir notas, generar material desde cero (unidad-moodle-forge) ni responder
  consultas. Nunca sube nada al aula: la subida la hace el tutor a mano.
license: Apache-2.0
---

# Revisión de apuntes de una unidad

Detecta y corrige problemas en el material de una unidad (redacción, temática, formato, bibliografía), de punta a punta
y con subagentes, **excepto subir al aula, que siempre hace el tutor**.

## REGLA QUE ORDENA TODO: revisión manual obligatoria

> **Ningún archivo está listo para subir hasta que el tutor lo revise a mano y lo confirme, uno por uno.**

Dejale esto claro al tutor **al empezar** (Fase 0) y **al terminar** (Fase 7). Los subagentes pueden hacer una revisión
visual parcial y los errores dentro de imágenes (diagramas, ilustraciones) no se detectan por texto: una verificación
automática no reemplaza que una persona mire cada archivo. Por eso:

- Nunca digas "listo para subir". Decí "corregido, pendiente de tu revisión".
- La compuerta es técnica: `scripts/compuerta_revision.py` se **niega** a generar `ORDEN_DE_SUBIDA.md` si falta la
  confirmación de algún archivo, y invalida una confirmación si el archivo cambia después.
- Solo ejecutás `confirmar` cuando el tutor dijo **explícitamente en el chat** que revisó ese archivo. Jamás marques una
  confirmación por tu cuenta, ni siquiera "por ahorrar tiempo": el motivo de la compuerta es que la mire una persona.

## Qué NO hace
- No sube, edita ni borra nada en el aula (el campus es **solo lectura**).
- No inventa bibliografía, capítulos, años, ediciones ni versiones: si no lo puede verificar, lo omite o lo avisa.
- No modifica los originales: siempre trabaja sobre copias.

## Alcance y principios
- **Solo se audita el material que está en el aula** (el que ve el alumno). Lo que exista solo en la carpeta local y no esté
  publicado se informa como "sobra", no se audita.
- **Se respeta el formato que el archivo ya tiene.** No hay un formato estándar por ahora (habrá una plantilla más adelante):
  se corrige el contenido (residuos de IA, redacción, errores técnicos, contraste con lo visto) y no se reformatea el
  documento. Lo único estricto es la portada: materia, unidad, tema y **revisor** (quien hizo la auditoría). Ver
  `references/formato-primera-hoja.md`.
- **Cada materia y unidad trae material distinto.** No se presupone Gamma, PDF ni Word: se trabaja con lo que haya.
- **Gamma es opcional**: todo lo específico de Gamma solo se activa si el aula tiene presentaciones de Gamma.
- **Idioma y plataforma**: la skill está pensada para material en español y se probó en Windows. En macOS y Linux la
  exportación de Word a PDF usa LibreOffice. Los patrones de los verificadores (segunda persona, relleno de IA) son de español.

## Material soportado
Cualquier material de una unidad: Word (`.docx`), PDF de cualquier origen, PDF de presentación creado con Gamma, `.pptx`,
markdown o texto. El flujo es el mismo; lo que cambia es la herramienta:
- **Word**: se extrae con `scripts/extraer_docx.py`, se corrige sobre una copia conservando el aspecto, se verifica con
  `scripts/verificar_docx.py`, y se **exporta a PDF** con `scripts/word_a_pdf.py` (ver Fase 6).
- **PDF de Gamma** (opcional, solo si hay): marca de agua y edición de texto en el lugar. Leé `references/gamma-pdf.md`.
- **Otros PDF/pptx/texto**: se revisan por contenido y redacción; si no se pueden editar en el lugar, el corrector deja el
  texto exacto a cambiar por página/diapositiva para que el tutor lo corrija en la herramienta de origen.
- **El Word formal es opcional**: si la unidad ya trae su documento, se revisa ese. Si no hay ninguno, **ofrecé** crearlo
  y que el tutor decida. Esta metodología nació con un Word agregado por el tutor porque en las actividades no existía,
  pero puede ya estar.

## Flujo (fases)

### Fase 0 — Aviso y datos
1. Avisá la regla de revisión manual (arriba).
2. Pedí estos datos (si el usuario ya los dio, no los repitas): materia y cursada; unidad (número y nombre); link a la
   sección del campus; carpeta con los documentos; carpeta con guiones/presentaciones/videos; carpeta con el código de
   ejemplo (si la materia tiene); nombre del **revisor de la unidad** (va en la portada); fuentes para la bibliografía;
   reglas técnicas de la materia (por ejemplo, versiones, namespaces o convenciones obligatorias; pueden no existir);
   carpeta de trabajo.
   **Estilo de redacción**: proponé el estilo por defecto (tercera persona e impersonal con "se", presente atemporal) y
   preguntá si lo mantiene o prefiere otro. Si elige otro, anotalo en `CRITERIOS.md` y corré los verificadores con
   `--sin-persona`.
   **No preguntes** subtítulo, institución ni fecha: no hay formato estándar, se respeta lo que cada archivo ya tiene y no se
   agrega nada nuevo a la portada. Tampoco preguntes la numeración del tema: se completa solo si falta (N = unidad, M = orden
   de la actividad en el aula, que sale del inventario de la Fase 1).
3. **Preflight**: corré `python scripts/preflight.py`. Si falta algo obligatorio, mostrale al tutor exactamente qué
   instalar y **no sigas** hasta resolverlo. Obligatorio: Python 3.10+ con PyMuPDF, python-docx y Pillow. Para leer el aula
   hace falta UNA de dos vías: la skill `tup-campus-navigator` (solo campus TUP) o Claude in Chrome con la sesión del tutor
   abierta en su campus. Recomendados: Word o LibreOffice (revisar layout) y youtube-transcript-api.
   Si no hay forma de revisar el layout, decilo en voz alta: esa revisión queda 100% en manos del tutor.

### Fase 1 — Inventario del aula (solo lectura) → esperá el OK
Recorré la unidad (introducción, actividades, práctica, microteaching, autoevaluación, encuesta) con la skill del campus
(o Claude in Chrome con la sesión del tutor). Por actividad listá: carpeta de apuntes y sus archivos, cuestionario,
práctica y resolución, videos (título, id, duración), infografías y adjuntos de código. **Ojo**: un apunte puede estar
embebido en un label y no en una carpeta. Compará con la carpeta local y mostrá: coincide / falta / sobra, duplicados con
sufijo "(1)", numeración inconsistente, actividades sin carpeta. **Frená y esperá el OK del tutor.** Detalle en
`references/flujo-detallado.md`.

### Fase 2 — Fuente de verdad de lo visto
Prioridad: (1) transcripciones reales de los videos, (2) guiones, (3) descripción de la actividad en el aula. A grandes
rasgos alcanza: se trata de saber qué temas cubre cada actividad, no de auditar cada palabra del video.
Transcripciones con `scripts/transcribir_youtube.py`: **si YouTube bloquea la IP, el script se detiene; no insistas ni uses
proxies**. Cubrí esos videos con los guiones y avisá cuáles quedaron sin transcripción.
Copiá guiones y transcripciones a `<trabajo>/fuentes/`. Avisá si un guion difiere mucho del video o tiene numeración vieja.

### Fase 3 — CRITERIOS.md único → el tutor lo aprueba
Armá `<trabajo>/CRITERIOS.md` desde `assets/templates/CRITERIOS.md.tpl` con **todas** las decisiones (estilo, reglas
técnicas si las hay, versiones **verificadas en los archivos de build del código real** si la materia tiene código, datos
mínimos de portada, bibliografía).
Es la fuente única para todos los subagentes: así las actividades quedan consistentes. Mostralo y esperá el OK.

### Fase 4 — Piloto con UNA actividad → el tutor mira el resultado
Corré el ciclo completo (detector → corrector) en una sola actividad. Verificá vos el resultado (Fase 6) y mostrale al
tutor qué se encontró, qué se corrigió y qué dudas quedan. Esperá su OK antes de lanzar el resto.

### Fase 5 — Resto de actividades en paralelo
Un par detector/corrector por actividad, en paralelo, cada uno escribiendo solo en su carpeta. Las dudas que dejen:
resolvelas con la información disponible (aula, código, guiones) y preguntale al tutor solo lo imposible de resolver.
Si un subagente se corta, retomalo con `SendMessage` y revisá qué alcanzó a escribir antes de rehacer.

### Fase 6 — Verificación independiente
No te fíes de lo que reporta cada subagente: verificá vos con `scripts/verificar_docx.py` y `scripts/verificar_pdf.py` y
mirá las páginas editadas. **Exportá cada Word corregido a PDF** con `scripts/word_a_pdf.py` (usa Microsoft Word y, si no hay,
LibreOffice; avisa si el número de páginas no coincide o hay páginas en blanco) y revisá **todas las páginas**, no solo la 1 y la
2: armá una hoja de contactos con una fila por documento para detectar tablas cortadas, código desbordado o huecos. El PDF
exportado es un entregable más y entra también en la revisión manual. **Leé en contexto cada coincidencia de patrón antes de reportarla**: muchas son falsos positivos
("usa" en tercera persona, "considera" como verbo del sujeto). La marca de agua se verifica por píxeles, no contando imágenes.

### Fase 7 — Compuerta de revisión manual (obligatoria)
1. `python scripts/compuerta_revision.py generar --trabajo <trabajo>` crea `REVISION_MANUAL.md` con un casillero por archivo.
2. Presentale los archivos **de a uno**: qué mirar, qué dudas abiertas dejó el corrector. Para ver un PDF o un Word, abrilo
   con el visor del sistema; para un Word, convertir a PDF ayuda si hay Word o LibreOffice.
3. Con cada confirmación explícita del tutor: `compuerta_revision.py confirmar <archivo> --trabajo <trabajo> --por "<nombre>"`.
4. `compuerta_revision.py orden --trabajo <trabajo>` genera `ORDEN_DE_SUBIDA.md` **solo si todo está confirmado**. Si el
   tutor intenta saltearse la revisión, explicale por qué no se puede.
5. Cerrá repitiendo el aviso: la subida al aula la hace el tutor, y registrá en el resumen final qué confirmó.

## Subagentes (dos roles por actividad)
- **Detector**: solo lectura. Lee el documento **completo**, contrasta con videos/guiones/código real y escribe el informe
  de hallazgos. No toca ningún archivo. Prompt base: `assets/templates/prompt-detector.md`.
- **Corrector**: recibe el informe y `CRITERIOS.md`, aplica los cambios sobre una **copia** y entrega el archivo corregido y
  el registro de cambios. Prompt base: `assets/templates/prompt-corrector.md`.
Por qué dos roles: el informe queda como contrato verificable entre quien detecta y quien arregla, y un corrector que
también audita tiende a justificar lo que ya cambió. Detalle en `references/subagentes.md`.

## Qué revisar (resumen; detalle en `references/criterios-redaccion.md`)
Estilo de redacción de `CRITERIOS.md` (por defecto, tercera persona e impersonal con "se"); tiempos verbales homogéneos
(presente atemporal); rastros de IA; calidad general; contraste con lo visto (sobra / falta / contradice); corrección técnica
contra el código real si la materia lo tiene (la precisión técnica manda sobre lo que diga el video); cierre formal. Datos
mínimos de portada y control de bibliografía: `references/formato-primera-hoja.md`.

## Estructura de salida
```
<trabajo>/
  CRITERIOS.md   REVISION_MANUAL.md   ORDEN_DE_SUBIDA.md   revision_manual.json
  fuentes/{guiones,transcripciones}
  informes/      <id>_informe.md  <id>_cambios.md  gamma_<id>_cambios.md
  corregidos/Actividad_N/   AN-Documento-formal_<Tema>.docx   AN-1_<Titulo>.pdf  AN-2_...
```
Numeración por actividad y sin sufijos "(1)" ni "(2)". Los duplicados se borran solo verificando el hash y avisando.

## Qué leer y cuándo
| Archivo | Cuándo |
|---|---|
| `references/flujo-detallado.md` | Antes de la Fase 1 y 2 (cómo recorrer el aula, límites del navegador) |
| `references/criterios-redaccion.md` | Al armar CRITERIOS.md y al verificar |
| `references/formato-primera-hoja.md` | Al corregir o crear un documento |
| `references/subagentes.md` | Antes de lanzar detector/corrector |
| `references/gamma-pdf.md` | Solo si hay PDF de Gamma |
| `references/lecciones-aprendidas.md` | Ante cualquier tropiezo |
| `scripts/` | `preflight`, `extraer_docx`, `verificar_docx`, `verificar_pdf`, `word_a_pdf`, `transcribir_youtube`, `quitar_marca_gamma`, `gamma_editar`, `editar_pdf_texto`, `comparar_pdf`, `compuerta_revision` |
