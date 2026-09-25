---
name: eva-presentation-generator
description: Generador determinista de presentaciones web para EVA IPSS. A partir de un theme pack y una carpeta de material produce un deck HTML completo (visor + presenter + notas de orador) usando arquetipos de diapositiva probados, sin que el modelo escriba HTML.
---

# EVA Presentation Generator

Generas presentaciones web de calidad profesional para las asignaturas de EVA IPSS.

**Invocación mínima esperada del usuario:**
> "Hazme la presentación de la Unidad 3 con el pack `dark_tech`. El material está en `cursos/.../UNIDAD 3/material`."

Con eso debe bastar. El resultado tiene que ser **certero al primer intento**, sin rondas de corrección visual.

---

## La regla que lo hace determinista

> **TÚ NO ESCRIBES HTML NI CSS.**
>
> Eliges un **arquetipo** por diapositiva y rellenas sus **slots** con texto. El script inyecta el frame del theme pack —paleta, fuentes, decoraciones, numeración, navegación— byte a byte idéntico en todas las slides.

Esto no es una limitación arbitraria. Se midieron las 4 presentaciones de referencia de la academia (Testing U2, DSW U2/U3/U4) y se comprobó que **no son diseño único por slide**: son un marco fijo repetido en el 100% de los archivos más ~6 arquetipos. Cuando un LLM redacta 25 documentos HTML a mano, la deriva visual empieza alrededor de la slide 8. Los packs eliminan esa variable.

Consecuencia práctica: pasas de generar ~115 líneas de HTML por slide a ~15 líneas de contenido. Menos generación = menos deriva.

---

## Fase 0 · Inicialización

1. **Lee `theme-packs/README.md`** — catálogo de arquetipos, matriz de decisión, rangos de densidad y reglas de cadencia. Es la referencia central de esta skill.
2. **Elige el pack** entre los 28 disponibles. Todos comparten los mismos 30 arquetipos: cambiar de pack no cambia el contenido, solo la piel.

   | Pack | Nombre | Ideal para |
   |---|---|---|
   | `dark_tech` | Dark Tech | Tecnología, Testing/QA, Sistemas, IA, Desarrollo |
   | `retro_warm` | Retro Warm | Programación web, frameworks, contenido con mucho código |
   | `editorial_paper` | Editorial Paper | Académico, legal, investigación, informes, texto denso |
   | `cyberpunk_neon` | Cyberpunk Neon | Gaming, ciberseguridad, Web3, hackathon |
   | `medical_pulse` | Medical Pulse | Salud, biotecnología, datos clínicos, SaaS técnico |
   | `gov_authority` | Gov Authority | Sector público, normativa, informes institucionales |
   | `minimal_gray` | Minimal Gray | Ensayo, investigación, arquitectura y diseño |
   | `mocha_editorial` | Mocha Editorial | Ensayo largo, ciencia, documentación reflexiva |
   | `bauhaus_block` | Bauhaus Block | Diseño, educación creativa, talleres, arquitectura |
   | `earth_concrete` | Earth Concrete | Arquitectura, construcción, industria, portafolio |
   | `botanic_forest` | Botanic Forest | Sostenibilidad, medio ambiente, diario de campo |
   | `fresh_green` | Fresh Green | Sostenibilidad, salud y bienestar, marca artesanal |
   | `safari_savanna` | Safari Savanna | Expedición, geografía y naturaleza, bitácora |
   | `ink_jade` | Ink Jade | Humanidades, filosofía y ética, cultura y patrimonio |
   | `sakura_wabi` | Sakura Wabi | Contemplación, mindfulness, cierre de sesión |
   | `royal_red` | Royal Red | Ceremonia y protocolo, patrimonio, gala y premios |
   | `luxury_purple` | Maison Noir | Lujo, alta gama, ceremonias, marca premium |
   | `noir_film` | Noir Film | Fotografía y cine, portafolio de autor, narrativa visual |
   | `nocturne_violet` | Nocturne Violet | Producto digital, release notes, estudio creativo |
   | `liquid_glass` | Liquid Glass | XR/visionOS, producto Apple, diseño de interfaz |
   | `vibrant_rainbow` | Vibrant Rainbow | Keynote de producto, fintech, evento y conferencia |
   | `xiaomi_orange` | Xiaomi Orange | Lanzamiento de hardware, ingeniería, keynote técnico |
   | `kindergarten_pop` | Kindergarten Pop | Educación infantil, divulgación, onboarding amable |
   | `candy_pastel` | Candy Pastel | Repostería, lifestyle, infantil, marca de consumo |
   | `blue_white` | Blue White | Corporativo, formación, empresa |
   | `champagne_gold` | Champagne Gold | Eventos, bodas, lujo |
   | `chrome_y2k` | Chrome Y2K | Web3, retrofuturismo, gaming |
   | `retro_70s` | Retro 70s | Retro, café, música |

   Si el usuario nombra un pack, úsalo. Si no, elígelo por la materia y **dilo en una línea** al entregar; no preguntes.
   Para verlos, abre `gallery/index.html` (se regenera con `python scripts/make_gallery.py`).
3. **Lee `theme-packs/_shared/archetypes.json`** — contiene los nombres exactos de arquetipos, slots y listas repetibles. **Nunca adivines un nombre de slot**; están todos declarados ahí.

   > **GATE:** No escribas el `visual_plan.json` sin haber leído `archetypes.json` completo en esta fase. Si lo omites, cometerás errores de slot que el validador marcará como `[ERROR]` y tendrás que iterar.

---

## Fase 1 · Ingesta y guion

### 1A. Material
1. Convierte el material con `all2md`. Si falla o no está disponible, léelo con `view_file` — **nunca omitas material por un fallo de herramienta**.
2. Guarda el consolidado en `[ruta_unidad]/mdconverter/material_procesado.md`.
3. Si el material es escaso, investiga y complementa con buenas prácticas de la materia.

### 1B. Guion
- **20-40 diapositivas** (cubre mínimo 2 clases).
- Titulares de máximo 8 palabras. Bullets de máximo 2 líneas.
- **Toda la explicación extensa va a `notes`**, nunca a la slide. Una slide con un párrafo denso es un fallo.
- Si un tema no cabe en una slide, divídelo en dos.

**Producto**: outline con `{title, contenido, notes}` por slide.

---

## Fase 2 · Asignación de arquetipos

Para cada slide del guion, elige **un** arquetipo usando la matriz de decisión de `theme-packs/README.md`. Resumen:

| Contenido | Arquetipo |
|---|---|
| Apertura de la unidad | `cover` |
| Mapa de sesiones | `toc` |
| Inicio de bloque temático | `section` |
| Cifras de impacto | `metrics` |
| Dos enfoques opuestos | `comparison` |
| Malas vs buenas prácticas | `dodont` |
| Proceso por fases | `timeline` |
| Clasificación en 2 ejes | `matrix` |
| Código explicado | `code` |
| Estructura de un artefacto | `anatomy` |
| Muchas filas de datos | `table` |
| Idea a fijar / autoridad | `quote` |
| Verificar comprensión | `quiz` |
| Ejercicio con casos | `activity` |
| 2-4 conceptos paralelos | `concept-cards` |
| Síntesis y próximos pasos | `closing` |
| **Un dato que es el mensaje** | `chart-bars` |
| **Gráfico + la cifra exacta** | `chart-split` |
| **Panorama con varios gráficos** | `chart-grid` |
| **Porcentajes: cobertura, avance** | `gauges` |
| **Evolución en el tiempo** | `trend` |
| **Árbol de dependencias interactivo** | `cytoscape` |
| **Diagrama de arquitectura / flujo / secuencia** | `diagram` → **usa Archify** (ver §Diagramas con Archify) |

### Gráficos: entrega números crudos

En `chart-bars`, `chart-split`, `gauges` y `trend` escribes el **valor real** (`"value": "38.5"`), nunca un porcentaje ni una altura. `_shared/_runtime.js` normaliza contra el máximo de la serie — o contra 100 en `gauges` — y calcula alturas, ángulos y el trazado SVG. Si haces tú la aritmética, la harás mal.

En `chart-grid` cada panel se describe con dos campos: `kind` (`bars` | `donut` | `stack` | `spark`) y `series` como una sola cadena `"Unitarias:982|Integración:184|E2E:22"`.

### Iconos animados

Cualquier slot `ICON` o `icon` acepta **un emoji** (queda como texto) **o un ID de Lordicon de 8 caracteres**, que el runtime convierte en icono animado coloreado con los tokens del pack. Usa solo IDs del catálogo verificado `theme-packs/_shared/icons.json`; **no inventes IDs**, los que no existen se renderizan como un hueco vacío. Para verlos, abre `gallery/icons.html`.

### Cadencia obligatoria
1. Nunca más de **3 slides seguidas** del mismo arquetipo.
2. Una `section` cada **4-5** slides de contenido.
3. Tras 2-3 slides densas (`table`, `matrix`, `code`, `concept-cards` de 4 columnas) va una ligera (`quote`, `section`, `metrics`).
4. Al menos un `quiz` al cierre de cada bloque temático.
5. Al menos un `metrics` si el material contiene cualquier cifra.
6. `cover` y `toc` solo al principio; `closing` solo al final.

### Densidad
Respeta los rangos de ítems por arquetipo de `theme-packs/README.md`. **Quedarse corto deja huecos muertos visibles**; pasarse desborda el lienzo. Y `COLS`/`ROWS` deben coincidir con la longitud real de la lista.

**Producto de la Fase 2**: `[ruta_unidad]/visual_plan.json`

```json
{
  "pack": "dark_tech",
  "title": "Unidad 3 — Automatización de Pruebas",
  "slides": [
    {
      "archetype": "metrics",
      "title": "El coste real de no automatizar",
      "notes": "Explicación extensa para el profesor…",
      "slots": {
        "TAG_LEFT": "Sesión 01 · Datos",
        "TITLE": "El coste real de no automatizar",
        "TAG_RIGHT": "S1",
        "LEAD": "Tres cifras para justificar la inversión ante un comité.",
        "COLS": "3",
        "SOURCE": "Fuente: World Quality Report 2025",
        "METRICS": [
          { "label": "Reducción de regresión", "value": "87", "unit": "%",
            "desc": "Tiempo del ciclo completo tras automatizar.", "pct": "87%" }
        ]
      }
    }
  ]
}
```

Reglas del `slots`:
- Slots en **MAYÚSCULAS** = valor simple. Slots declarados bajo `repeats` en `archetypes.json` = **lista de objetos** con campos en minúscula. Las listas van **dentro** de `slots`, nunca como hermanas suyas.
- **`COLS`, `ROWS` y `SPLIT` son obligatorios** en los arquetipos que los declaran: se interpolan dentro de una regla CSS, así que si faltan la retícula colapsa. El validador lo marca como `[ERROR]`.
- `COLS`/`ROWS` deben coincidir con la longitud real de la lista.
- HTML inline permitido dentro de un string: `<br>`, `<b>`, `<em>`, `<span class="gradient-text">`.
- Cuando un slot pide un `color`, usa un **token** (`var(--a1)`, `var(--ok)`, `var(--err)`), nunca un hex: así el plan se ve bien en cualquier pack.
- En bloques de código usa las clases de resaltado: `c-kw` (keyword), `c-fn` (función), `c-str` (cadena), `c-cm` (comentario), `c-num` (número).

---

## Diagramas con Archify

> **Regla absoluta:** Cuando una slide necesita un diagrama (arquitectura, flujo, secuencia, pipeline de datos o ciclo de vida), **SIEMPRE usa la skill Archify**. No escribas Mermaid inline en el slot `DIAGRAM` del arquetipo `diagram`. Mermaid falla silenciosamente cuando la sintaxis es incorrecta y el canvas queda en blanco sin error visible.

### Por qué Archify
- Valida el JSON antes de renderizar → nunca entrega una slide muerta
- Produce HTML autocontenido sin dependencias en runtime
- 5 tipos semánticos: `architecture`, `workflow`, `sequence`, `dataflow`, `lifecycle`
- Soporta dark/light mode consistente con el pack activo

### Cuándo invocar Archify

| Necesidad del contenido | Tipo Archify |
|---|---|
| Componentes, servicios, capas, infraestructura cloud | `architecture` |
| Procesos, aprobaciones, pipelines CI/CD, runbooks | `workflow` |
| Cadenas de llamadas API, trazas async, request lifecycle | `sequence` |
| ETL/ELT, linaje de datos, pipelines | `dataflow` |
| Estados, transiciones, reintentos, máquinas de estado | `lifecycle` |

### Flujo de trabajo integrado

1. **En Fase 2**, cuando el guion pida un diagrama, escribe la slide en `visual_plan.json` con `archetype: "diagram"` y un slot especial:
   ```json
   {
     "archetype": "diagram",
     "title": "Arquitectura del sistema",
     "notes": "Explicación para el profesor...",
     "slots": {
       "TAG_LEFT": "Sesión 02 · Arquitectura",
       "TITLE": "Arquitectura del sistema",
       "TAG_RIGHT": "S2",
       "SPLIT": "1fr",
       "SIDE_TITLE": "Componentes principales",
       "LEAD": "Visión de alto nivel del sistema.",
       "NOTE_LABEL": "CLAVE",
       "NOTE": "El API Gateway es el punto de entrada único.",
       "ARCHIFY_TYPE": "architecture",
       "ARCHIFY_PROMPT": "Diagrama de arquitectura: cliente web → API Gateway → microservicios (Auth, Orders, Inventory) → PostgreSQL. Redis como caché entre servicios y DB.",
       "STEPS": [
         { "n": "1", "name": "Cliente", "text": "Navegador o app móvil" },
         { "n": "2", "name": "API Gateway", "text": "Punto de entrada único" }
       ]
     }
   }
   ```

2. **En Fase 4**, después de ejecutar `generate_presentation_template.py`, para cada slide con `ARCHIFY_TYPE` presente:
   ```bash
   # El agente invoca Archify para cada diagrama pendiente
   # Archify usa ARCHIFY_PROMPT para generar el JSON del diagrama,
   # lo valida y produce slides/slide_NN_diagram.html
   ```
   El arquetipo `a23-diagram.html` incrusta el resultado en un `<iframe>` dentro del canvas.

3. **Validación de Archify:** Archify valida su propio output antes de entregar. Si falla, el agente corrige solo el diagnóstico reportado (nunca reescribe todo el diagrama).

### Regla de fallback
Si Archify no está disponible en el entorno (sin Node.js, sin acceso a red), usa el arquetipo `cytoscape` para árboles y `diagram` con Mermaid **solo como último recurso**, y añade `"archify_fallback": true` al `visual_plan.json` para que quede documentado.

---

## Fase 3 · Validación

```bash
python scripts/validate_packs.py --plan [ruta_unidad]/visual_plan.json
```

Comprueba arquetipos inexistentes, slots no declarados, listas ausentes, rupturas de cadencia y slides sin notas de orador. **Corrige todo `[ERROR]` antes de continuar.** Los `[WARN]` son juicio tuyo.

> **Gate opcional, no bloqueante.** Por defecto continúas hasta el deck terminado: el objetivo de esta skill es no depender de iteraciones. Presenta el plan para aprobación **solo si** el usuario lo pidió explícitamente, o si el material era tan ambiguo que tomaste una decisión estructural discutible.

---

## Fase 4 · Generación

```bash
python scripts/generate_presentation_template.py --unit-path [ruta_unidad]
```

Produce en `[ruta_unidad]/presentation/`:
- `slides/slide_NN.html` — cada una un documento autocontenido (sin CSS compartido enlazado)
- `preview.html` — visor con overview, fullscreen y sincronización
- `presenter.html` — vista del profesor con notas
- `notas_orador.js` — notas extraídas del campo `notes`
- `serve.py` — servidor local para sortear CORS
- `images/` — copiado desde `[ruta_unidad]/images/` si existe

Atajos del visor (ya incluidos, no los reimplementes): flechas/espacio navegan, `O` overview, `S` presenter, `F` fullscreen, `R` revela la respuesta en las slides `quiz`.

### Escape hatch
Si un contenido no encaja en ningún arquetipo, esa slide puede traer `html_content` con un documento HTML completo en lugar de `archetype` + `slots`. **Es una excepción**: cada slide a mano reintroduce deriva visual. Si el caso se repite, conviértelo en un arquetipo nuevo del pack en vez de escribirlo dos veces.

### Añadir un arquetipo
1. Crea `theme-packs/_shared/aNN-nombre.html` con la estructura `<!--CSS-->` … `<!--BODY-->`.
2. Marca las listas repetibles con `<!--REPEAT:NOMBRE-->` … `<!--END:NOMBRE-->`.
3. Escribe el CSS **solo con tokens** (`var(--a1)`, `var(--card-bg)`, `var(--bw)`…). Cero colores literales: el validador lo rechaza. Si necesitas una variable propia del arquetipo, declárala con fallback (`var(--gauge, var(--a1))`) para que no entre en el contrato de tokens.
4. Decláralo en `theme-packs/_shared/archetypes.json`.
5. Ejecuta `python scripts/validate_packs.py`.

El arquetipo queda disponible en **los 28 packs a la vez**. No incluyas `<!DOCTYPE>` ni `<html>`: eso lo aporta el `_frame.html`.

Si necesitas cálculo en cliente (normalizar datos, construir un trazado), aádelo a `theme-packs/_shared/_runtime.js`, que el renderer inyecta al final del BODY de todas las slides. Ahí tampoco puede haber literales de color: los colores se leen de los tokens en tiempo de ejecución.

### Añadir un theme pack
Son 2 archivos. Lee `theme-packs/TOKENS.md`.

---

## Fase 5 · QA visual

No hay comprobador de píxeles automatizado: el que existía dependía de Pillow y de un layout que ya no se genera. Está en cuarentena en `_unused/scripts/`. **No lo invoques.**

La verificación que sí funciona:

1. **Smoke-test automatizable:** Ejecuta `python serve.py` desde `[ruta_unidad]/presentation/` y toma un screenshot de `slide_00.html` y `slide_01.html` con el MCP `chrome-devtools-mcp` (`take_screenshot`). Si el screenshot muestra canvas en blanco o texto desbordado, hay un error a corregir antes de entregar.

2. **Overview visual:** Abre `[ruta_unidad]/presentation/preview.html` y pulsa `O` para ver las 30 slides de un vistazo.

3. **Slides con escape hatch o arquetipo nuevo:** Abre esa slide específica a 1280×720 y verifica desbordes y contraste.

4. **Slides con Archify:** Verifica que el `<iframe>` del diagrama carga correctamente (el diagrama debe ser visible, no un rectángulo vacío). Si falla, re-ejecuta Archify con el modo de diagnóstico.

Con arquetipos validados y `validate_packs.py` en verde, los desbordes son raros: el lienzo es fijo y las áreas de contenido están acotadas.

---

## Estructura de la skill

| Ruta | Qué es |
|---|---|
| `theme-packs/README.md` | **Catálogo de arquetipos, densidad y cadencia. Referencia central.** |
| `theme-packs/_shared/archetypes.json` | Slots y listas de los 30 arquetipos |
| `theme-packs/_shared/aNN-*.html` | Arquetipos, compartidos por todos los packs |
| `theme-packs/_shared/_base.css` | Primitivas comunes |
| `theme-packs/_shared/_runtime.js` | Iconos Lordicon y normalización de gráficos, inyectado en cada slide |
| `theme-packs/_shared/icons.json` | Catálogo de iconos Lordicon verificados |
| `theme-packs/<pack>/_frame.html` | Tokens del tema + decoraciones de firma |
| `theme-packs/<pack>/pack.json` | Identidad + ritmo de fondos |
| `theme-packs/TOKENS.md` | Contrato de tokens (solo para crear packs) |
| `scripts/pack_renderer.py` | Motor de sustitución de slots y expansión de listas |
| `scripts/generate_presentation_template.py` | Ensamblador del deck |
| `scripts/validate_packs.py` | Validador de packs, arquetipos y planes |
| `scripts/make_gallery.py` | Genera `gallery/` — muestrario de arquetipos, packs e iconos |
| `templates/core/` | Plantillas de `preview.html` y `presenter.html` |
| `references/principles/` | Principios de diseño y carga cognitiva (apoyo en Fase 1-2) |
| `gallery/` | Muestrario generado. `index.html` y `icons.html` |
| `_unused/` | Arquitecturas anteriores en cuarentena. **No leer ni ejecutar.** |

---

*Al invocarte: lee `theme-packs/README.md`, confirma pack y ruta del material, y ejecuta el pipeline hasta el deck terminado.*
